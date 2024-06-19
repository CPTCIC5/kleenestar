from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from channels.models import APICredentials
import hashlib
import os
import json
import base64
from google_auth_oauthlib.flow import Flow
import requests
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from dotenv import load_dotenv
from django.shortcuts import redirect
from oauth.helper import create_channel,get_channel
from oauth.external_urls import frontend_channel_url,google_apis_url,google_redirect_uri                        
from google.auth.exceptions import GoogleAuthError
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric, Pivot, OrderBy, RunPivotReportRequest, RunRealtimeReportRequest
from google.analytics.admin import AnalyticsAdminServiceClient
from google.oauth2.credentials import Credentials
from google.analytics.admin_v1alpha.types import ListPropertiesRequest

load_dotenv(override=True)


#state value for oauth request authentication
passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()

"""
APP - CONFIGURATIONS
"""

credentials = {
"developer_token": os.getenv("GOOGLE_DEVELOPER_TOKEN"),
"client_id": os.getenv("GOOGLE_CLIENT_ID"),
"client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
"use_proto_plus": "false"
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
google_client_secret_file = os.path.join(BASE_DIR, 'utils', 'XYZ.json')

google_scopes = ["openid",f"{google_apis_url}/auth/adwords" ,f"{google_apis_url}/auth/userinfo.email" ,f"{google_apis_url}/auth/userinfo.profile", f"{google_apis_url}/auth/analytics.readonly"]
flow = Flow.from_client_secrets_file(google_client_secret_file, scopes=google_scopes)
flow.redirect_uri = google_redirect_uri



@api_view(("GET",))
def google_oauth(request):

    state_dict = {'email': request.user.email, 'passthrough_val': passthrough_val}
    state_json = json.dumps(state_dict)
    state_encoded = base64.urlsafe_b64encode(state_json.encode()).decode()
    
    try:
        authorization_url, state = flow.authorization_url(
            access_type="offline",
            state=state_encoded,
            prompt="consent",
            include_granted_scopes="true",
        )
        return Response({
            "url": authorization_url},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@csrf_exempt
@api_view(("GET",))
@permission_classes([AllowAny]) 
def google_oauth_callback(request):
    code = request.query_params.get("code")
    state_encoded = request.query_params.get('state')
    state_json = base64.urlsafe_b64decode(state_encoded).decode()
    state_params = json.loads(state_json)
    if not code:
        return Response(
        {"detail": "something not working???"},
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    elif state_params.get("passthrough_val", None) != passthrough_val:
        return Response(
        {"detail": "State token does not match the expected state."},
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    
    user_email = state_params.get("email", None)
    if not user_email:
        return Response(
            {"detail": "Unable to retrieve user email"},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    
    try:
        flow.fetch_token(code=code)
        access_token = flow.credentials.token
        refresh_token = flow.credentials.refresh_token
        credentials["refresh_token"] = refresh_token
        response = requests.get(
            f'{google_apis_url}/oauth2/v1/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        if response.status_code == 200:
            email = response.json().get('email')
        else:
            print(f"Failed to get user info: {response.content}")
            return Response(
                {"detail": "Failed to get user info"},
                status=status.HTTP_400_BAD_REQUEST
            )

        google_client = GoogleAdsClient.load_from_dict(credentials , version='v16')
        customer_service = google_client.get_service("CustomerService")

        accessible_customers = customer_service.list_accessible_customers()
        
        if len(accessible_customers.resource_names) > 1:
            return Response(
                {"detail": "Manager accounts not allowed"},
                status=status.HTTP_403_FORBIDDEN,
            )
        resource_names = accessible_customers.resource_names

        manager_id = resource_names[0].split('/')[1]
        
        client_id_list = []
        query = """
            SELECT
                customer_client.client_customer,
                customer_client.level,
                customer_client.manager,
                customer_client.descriptive_name,
                customer_client.currency_code,
                customer_client.time_zone,
                customer_client.id
            FROM
                customer_client
            WHERE   
                customer_client.level <= 1
        """
        google_client = GoogleAdsClient.load_from_dict(credentials , version='v16')
        google_ads_service = google_client.get_service("GoogleAdsService")
        response = google_ads_service.search(customer_id=manager_id, query=query)
        
        for row in response:
            if(row.customer_client.id != int(manager_id)):
                client_id_list.append(str(row.customer_client.id))
        
        if len(client_id_list) == 0:
            return Response(
                {"detail": "No ads account found allowed"},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        """
        Email of the workspace user is passed as a argument,
        along with the channel type
        
        """
        try:
            google_channel = get_channel(email=user_email, channel_type_num=1)
        except Exception:
            google_channel = create_channel(email=user_email, channel_type_num=1)
        
        if google_channel.credentials is None:
            credentials_new = APICredentials.objects.create(
                key_1=refresh_token,
                key_2=access_token,
                key_3=manager_id,
                key_4=client_id_list
            )
            google_channel.credentials = credentials_new
        else:
            google_channel.credentials.key_1 = refresh_token
            google_channel.credentials.key_2 = access_token
            google_channel.credentials.key_3 = manager_id
            google_channel.credentials.key_4 = client_id_list
            google_channel.credentials.save()

        google_channel.save()

        return redirect(frontend_channel_url)

    
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )



def get_google_marketing_data(refresh_token,manager_id, client_id_list):


    credentials["refresh_token"] = refresh_token
    
    credentials["login_customer_id"] = manager_id

    google_client = GoogleAdsClient.load_from_dict(credentials , version='v16')
    marketing_data = []

    for id in eval(client_id_list):

        # end_date = datetime.now().date()
        # start_date = end_date - timedelta(days=30)
        ga_service = google_client.get_service("GoogleAdsService")
        results = {
            "channel": "Goolge Ads",
            "campaigns": [],
            "ad_groups": [],
            "ad_group_ads": []
        }
        campaign_query = """
        SELECT campaign.id, campaign.name, campaign.status, campaign.serving_status, campaign.advertising_channel_type, campaign.start_date, campaign.end_date, campaign.campaign_budget, campaign.target_cpa.cpc_bid_ceiling_micros, campaign.target_cpa.cpc_bid_floor_micros, campaign.target_cpa.target_cpa_micros, campaign_budget.id, campaign_budget.name, campaign_budget.period, campaign_budget.amount_micros, campaign_budget.status, campaign_budget.recommended_budget_estimated_change_weekly_views, campaign_budget.recommended_budget_estimated_change_weekly_interactions, campaign_budget.recommended_budget_estimated_change_weekly_cost_micros, campaign_budget.recommended_budget_estimated_change_weekly_clicks, campaign_budget.recommended_budget_amount_micros, campaign_budget.type, campaign_budget.total_amount_micros, campaign_group.id, campaign_group.name, campaign_group.resource_name, campaign_group.status, metrics.cost_micros, metrics.conversions_value, metrics.clicks, metrics.interaction_rate, metrics.view_through_conversions, metrics.average_cpc, metrics.conversions, metrics.ctr, metrics.all_conversions, metrics.cost_per_conversion, metrics.value_per_conversion, metrics.all_conversions_value, metrics.conversions_from_interactions_rate FROM campaign"""  # + f"""WHERE segments.date BETWEEN {start_date} AND {end_date} """
        
        ad_group_query = """
        SELECT campaign.name, ad_group.id, ad_group.name, ad_group.status, ad_group.campaign, ad_group.effective_target_cpa_micros, ad_group.effective_target_cpa_source, ad_group.type, ad_group.target_cpm_micros, ad_group.target_cpa_micros, metrics.cost_micros, metrics.conversions_value, metrics.clicks, metrics.interaction_rate, metrics.view_through_conversions, metrics.average_cpc, metrics.conversions, metrics.ctr, metrics.all_conversions, metrics.cost_per_conversion, metrics.value_per_conversion, metrics.all_conversions_value, metrics.conversions_from_interactions_rate FROM ad_group """ # + f"""WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'""" 

        ad_group_ad_query = """ 
        SELECT campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.status, ad_group_ad.ad.final_urls, ad_group_ad.ad.text_ad.description1, ad_group_ad.ad.text_ad.description2, ad_group_ad.ad.type, metrics.cost_micros, metrics.conversions_value, metrics.clicks, metrics.interaction_rate, metrics.view_through_conversions, metrics.average_cpc, metrics.conversions, metrics.ctr, metrics.all_conversions, metrics.cost_per_conversion, metrics.value_per_conversion, metrics.all_conversions_value, metrics.conversions_from_interactions_rate FROM ad_group_ad """  # + f"""WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'""" 
        keyword_view_query = """
        SELECT campaign.name, ad_group.name,keyword_view.resource_name, metrics.cost_micros, metrics.conversions_value, metrics.clicks, metrics.interaction_rate, metrics.view_through_conversions, metrics.average_cpc, metrics.conversions, metrics.ctr, metrics.all_conversions, metrics.cost_per_conversion, metrics.value_per_conversion, metrics.all_conversions_value, metrics.conversions_from_interactions_rate FROM keyword_view """
        try:
            campaign_response = ga_service.search(customer_id=id, query=campaign_query)
            campaign_data = []
            ad_group_response = ga_service.search(customer_id=id, query=ad_group_query)
            ad_group_data = []
            ad_group_ad_response = ga_service.search(customer_id=id, query=ad_group_ad_query)
            ad_group_ad_data = []
            keyword_view_response = ga_service.search(customer_id=id, query=keyword_view_query)
            keyword_view_data = []

            for campaign_row in campaign_response:
                campaign_data.append({
                    "campaign_id": campaign_row.campaign.id,
                    "campaign_name": campaign_row.campaign.name,
                    "campaign_status": campaign_row.campaign.status,
                    "campaign_serving_status": campaign_row.campaign.serving_status,
                    "campaign_advertising_channel_type": campaign_row.campaign.advertising_channel_type,
                    "campaign_start_date": campaign_row.campaign.start_date,
                    "campaign_end_date": campaign_row.campaign.end_date,
                    "campaign_budget": campaign_row.campaign.campaign_budget,
                    "campaign_target_cpa": {
                        "cpc_bid_ceiling_micros": campaign_row.campaign.target_cpa.cpc_bid_ceiling_micros,
                        "cpc_bid_floor_micros": campaign_row.campaign.target_cpa.cpc_bid_floor_micros,
                        "target_cpa_micros": campaign_row.campaign.target_cpa.target_cpa_micros
                    },
                    "campaign_budget_details": {
                        "budget_id": campaign_row.campaign_budget.id,
                        "budget_name": campaign_row.campaign_budget.name,
                        "period": campaign_row.campaign_budget.period,
                        "amount_micros": campaign_row.campaign_budget.amount_micros,
                        "status": campaign_row.campaign_budget.status,
                        "recommended_budget_estimated_change_weekly_views": campaign_row.campaign_budget.recommended_budget_estimated_change_weekly_views,
                        "recommended_budget_estimated_change_weekly_interactions": campaign_row.campaign_budget.recommended_budget_estimated_change_weekly_interactions,
                        "recommended_budget_estimated_change_weekly_cost_micros": campaign_row.campaign_budget.recommended_budget_estimated_change_weekly_cost_micros,
                        "recommended_budget_estimated_change_weekly_clicks": campaign_row.campaign_budget.recommended_budget_estimated_change_weekly_clicks,
                        "recommended_budget_amount_micros": campaign_row.campaign_budget.recommended_budget_amount_micros,
                        "type": campaign_row.campaign_budget.type_,
                        "total_amount_micros": campaign_row.campaign_budget.total_amount_micros,
                    },
                    "campaign_group": {
                        "group_id": campaign_row.campaign_group.id,
                        "group_name": campaign_row.campaign_group.name,
                        "resource_name": campaign_row.campaign_group.resource_name,
                        "status": campaign_row.campaign_group.status,
                    },
                    "metrics": {
                        "cost_micros": campaign_row.metrics.cost_micros,
                        "conversions_value": campaign_row.metrics.conversions_value,
                        "clicks": campaign_row.metrics.clicks,
                        "interaction_rate": campaign_row.metrics.interaction_rate,
                        "view_through_conversions": campaign_row.metrics.view_through_conversions,
                        "average_cpc": campaign_row.metrics.average_cpc,
                        "conversions": campaign_row.metrics.conversions,
                        "ctr": campaign_row.metrics.ctr,
                        "all_conversions": campaign_row.metrics.all_conversions,
                        "cost_per_conversion": campaign_row.metrics.cost_per_conversion,
                        "value_per_conversion": campaign_row.metrics.value_per_conversion,
                        "all_conversions_value": campaign_row.metrics.all_conversions_value,
                        "conversions_from_interactions_rate": campaign_row.metrics.conversions_from_interactions_rate,
                    }
                })

            for ad_group_row in ad_group_response:
                ad_group_data.append({
                    "ad_group_id": ad_group_row.ad_group.id,
                    "ad_group_name": ad_group_row.ad_group.name,
                    "campaign_name": ad_group_row.campaign.name,
                    "ad_group_status": ad_group_row.ad_group.status,
                    "campaign_id": ad_group_row.ad_group.campaign,
                    "effective_target_cpa_micros": ad_group_row.ad_group.effective_target_cpa_micros,
                    "effective_target_cpa_source": ad_group_row.ad_group.effective_target_cpa_source,
                    "ad_group_type": ad_group_row.ad_group.type_,
                    "target_cpm_micros": ad_group_row.ad_group.target_cpm_micros,
                    "target_cpa_micros": ad_group_row.ad_group.target_cpa_micros,
                    "metrics": {
                        "cost_micros": ad_group_row.metrics.cost_micros,
                        "conversions_value": ad_group_row.metrics.conversions_value,
                        "clicks": ad_group_row.metrics.clicks,
                        "interaction_rate": ad_group_row.metrics.interaction_rate,
                        "view_through_conversions": ad_group_row.metrics.view_through_conversions,
                        "average_cpc": ad_group_row.metrics.average_cpc,
                        "conversions": ad_group_row.metrics.conversions,
                        "ctr": ad_group_row.metrics.ctr,
                        "all_conversions": ad_group_row.metrics.all_conversions,
                        "cost_per_conversion": ad_group_row.metrics.cost_per_conversion,
                        "value_per_conversion": ad_group_row.metrics.value_per_conversion,
                        "all_conversions_value": ad_group_row.metrics.all_conversions_value,
                        "conversions_from_interactions_rate": ad_group_row.metrics.conversions_from_interactions_rate
                    }
                })
            

            for ad_group_ad_row in ad_group_ad_response:
                ad_group_ad_data.append({
                    "ad_id": ad_group_ad_row.ad_group_ad.ad.id,
                    "ad_name": ad_group_ad_row.ad_group_ad.ad.name,
                    "campaign_name": ad_group_ad_row.campaign.name,
                    "ad_group_name": ad_group_ad_row.ad_group.name,
                    "ad_status": ad_group_ad_row.ad_group_ad.status,
                    "final_urls": list(ad_group_ad_row.ad_group_ad.ad.final_urls),
                    "description1": ad_group_ad_row.ad_group_ad.ad.text_ad.description1,
                    "description2": ad_group_ad_row.ad_group_ad.ad.text_ad.description2,
                    "ad_type": ad_group_ad_row.ad_group_ad.ad.type_,
                    "metrics": {
                        "cost_micros": ad_group_ad_row.metrics.cost_micros,
                        "conversions_value": ad_group_ad_row.metrics.conversions_value,
                        "clicks": ad_group_ad_row.metrics.clicks,
                        "interaction_rate": ad_group_ad_row.metrics.interaction_rate,
                        "view_through_conversions": ad_group_ad_row.metrics.view_through_conversions,
                        "average_cpc": ad_group_ad_row.metrics.average_cpc,
                        "conversions": ad_group_ad_row.metrics.conversions,
                        "ctr": ad_group_ad_row.metrics.ctr,
                        "all_conversions": ad_group_ad_row.metrics.all_conversions,
                        "cost_per_conversion": ad_group_ad_row.metrics.cost_per_conversion,
                        "value_per_conversion": ad_group_ad_row.metrics.value_per_conversion,
                        "all_conversions_value": ad_group_ad_row.metrics.all_conversions_value,
                        "conversions_from_interactions_rate": ad_group_ad_row.metrics.conversions_from_interactions_rate
                    }
                })

            def get_keyword(criterion_id):
                get_keyword_query = f"""
                    SELECT
                        ad_group_criterion.keyword.text,
                        ad_group_criterion.keyword.match_type
                    FROM
                        ad_group_criterion
                    WHERE
                        ad_group_criterion.criterion_id = {criterion_id}
                """ 
                keyword_response = ga_service.search(customer_id=id, query=get_keyword_query)
                for response in keyword_response:
                    keyword = response.ad_group_criterion.keyword
                    return [keyword.text, keyword.match_type]
                

        
            for keyword_view_row in keyword_view_response:
                keyword_view_data.append({
                    "resource_name": keyword_view_row.keyword_view.resource_name,
                    "keyword_text": get_keyword(keyword_view_row.keyword_view.resource_name.split("~")[-1])[0],
                    "keyword_match_type": get_keyword(keyword_view_row.keyword_view.resource_name.split("~")[-1])[1],
                    "campaign_name": keyword_view_row.campaign.name,
                    "ad_group_name": keyword_view_row.ad_group.name,
                    "metrics": {
                        "cost_micros": keyword_view_row.metrics.cost_micros,
                        "conversions_value": keyword_view_row.metrics.conversions_value,
                        "clicks": keyword_view_row.metrics.clicks,
                        "interaction_rate": keyword_view_row.metrics.interaction_rate,
                        "view_through_conversions": keyword_view_row.metrics.view_through_conversions,
                        "average_cpc": keyword_view_row.metrics.average_cpc,
                        "conversions": keyword_view_row.metrics.conversions,
                        "ctr": keyword_view_row.metrics.ctr,
                        "all_conversions": keyword_view_row.metrics.all_conversions,
                        "cost_per_conversion": keyword_view_row.metrics.cost_per_conversion,
                        "value_per_conversion": keyword_view_row.metrics.value_per_conversion,
                        "all_conversions_value": keyword_view_row.metrics.all_conversions_value,
                        "conversions_from_interactions_rate": keyword_view_row.metrics.conversions_from_interactions_rate
                    }
                })
            results["channel_type"] = "Google Channel"
            results["keyword_views"] = keyword_view_data
            results["ad_group_ads"] = ad_group_ad_data
            results["ad_groups"] = ad_group_data
            results["campaigns"] = campaign_data
            marketing_data.append(results)

            return marketing_data
        
        except GoogleAdsException as ex:
            print(f"Request failed with status {ex.error.code().name} and includes the following errors:")
            for error in ex.failure.errors:
                print(f"\tError with message {error.message}.")
                if error.location:
                    for field_path_element in error.location.field_path_elements:
                        print(f"\t\tOn field: {field_path_element.field_name}")
            return None
            
#-----------------------------------------GOOGLE ANALYTICS INFORMATION-----------------------------------------------#


def get_valid_metrics(client, property_id):
    metadata = client.get_metadata(name=f"properties/{property_id}/metadata")
    valid_metrics = {metric.api_name for metric in metadata.metrics}
    return valid_metrics

def filter_and_add_metrics(client, property_id, metrics):
    valid_metrics = get_valid_metrics(client, property_id)
    filtered_metrics = [metric for metric in metrics if metric.name in valid_metrics]
    return filtered_metrics

def run_pivot_report(client, property_id, metrics, dimensions, pivots, start_date="2023-01-01", end_date="today"):
    request = RunPivotReportRequest(
        property=f"properties/{property_id}",
        metrics=metrics,
        dimensions=dimensions,
        pivots=pivots,
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)]
    )

    response = client.run_pivot_report(request)
    response_list = []

    dimension_headers = [header.name for header in response.dimension_headers]
    metric_headers = [header.name for header in response.metric_headers]

    for row in response.rows:
        row_data = {}
        for i, dimension_value in enumerate(row.dimension_values):
            row_data[dimension_headers[i]] = dimension_value.value
        for j, metric_value in enumerate(row.metric_values):
            row_data[metric_headers[j]] = metric_value.value
        response_list.append(row_data)

    return response_list


def run_realtime_report(client, property_id, metrics, dimensions=[Dimension(name="country")]):
    request = RunRealtimeReportRequest(
        property=f"properties/{property_id}",
        metrics=metrics,
        dimensions=dimensions
    )

    response = client.run_realtime_report(request)
    response_list = []

    dimension_headers = [header.name for header in response.dimension_headers]
    metric_headers = [header.name for header in response.metric_headers]

    for row in response.rows:
        row_data = {}
        for i, dimension_value in enumerate(row.dimension_values):
            row_data[dimension_headers[i]] = dimension_value.value
        for j, metric_value in enumerate(row.metric_values):
            row_data[metric_headers[j]] = metric_value.value
        response_list.append(row_data)

    return response_list


def run_report(client, property_id, metrics, dimensions=[Dimension(name="date")]):
    request = RunReportRequest(
        property=f"properties/{property_id}",
        metrics=filter_and_add_metrics(client, property_id, metrics),
        dimensions=dimensions,
        date_ranges=[DateRange(start_date="2023-01-01", end_date="today")],
    )
    
    response = client.run_report(request)
    response_list = []

    dimension_headers = [header.name for header in response.dimension_headers]
    metric_headers = [header.name for header in response.metric_headers]

    for row in response.rows:
        row_data = {}
        for i, dimension_value in enumerate(row.dimension_values):
            row_data[dimension_headers[i]] = dimension_value.value
        for j, metric_value in enumerate(row.metric_values):
            row_data[metric_headers[j]] = metric_value.value
        response_list.append(row_data)

    return response_list

def get_user_metrics(client, property_id):
    metrics = [
        Metric(name="activeUsers"),
        Metric(name="newUsers"),
        Metric(name="totalUsers"),
        Metric(name="crashFreeUsersRate"),
        Metric(name="crashAffectedUsers"),
        Metric(name="userEngagementDuration"),
        Metric(name="userStickiness"),
        Metric(name="userRetention"),
    ]
    return run_report(client, property_id, metrics)

# Session Metrics
def get_session_metrics(client, property_id):
    metrics = [
        Metric(name="sessions"),
        Metric(name="engagedSessions"),
        Metric(name="sessionsPerUser"),
        Metric(name="averageSessionDuration"),
        Metric(name="bounceRate"),
        Metric(name="engagementRate"),
        Metric(name="sessionDurationPerUser"),
    ]
    return run_report(client, property_id, metrics)

# Event Metrics
def get_event_metrics(client, property_id):
    metrics = [
        Metric(name="eventCount"),
        Metric(name="eventValue"),
        Metric(name="eventCountPerUser"),
        Metric(name="eventsPerSession"),
    ]
    return run_report(client, property_id, metrics)

# E-commerce Metrics
def get_ecommerce_metrics(client, property_id):
    metrics = [
        Metric(name="purchaseRevenue"),
        Metric(name="transactions"),
        Metric(name="purchaserRate"),
        Metric(name="averagePurchaseRevenue"),
        Metric(name="refundAmount"),
        Metric(name="averagePurchaseValue"),
        Metric(name="ecommercePurchases"),
    ]
    return run_report(client, property_id, metrics)

# Engagement Metrics
def get_engagement_metrics(client, property_id):
    metrics = [
        Metric(name="averageSessionDuration"),
        Metric(name="bounceRate"),
        Metric(name="engagementRate"),
        Metric(name="screenPageViews"),
        Metric(name="engagedSessionsPerUser"),
        Metric(name="userEngagementDuration"),
        Metric(name="screenPageViewsPerSession"),
    ]
    return run_report(client, property_id, metrics)

# Ad Metrics
def get_ad_metrics(client, property_id):
    metrics = [
        Metric(name="adClicks"),
        Metric(name="adCost"),
        Metric(name="adImpressions"),
        Metric(name="adRevenue"),
        Metric(name="returnOnAdSpend"),
        Metric(name="adCostPerClick"),
        Metric(name="adClickThroughRate"),
    ]
    dimensions = [
        Dimension(name="sessionCampaignName")
    ]
    return run_report(client, property_id, metrics, dimensions)

# Lifetime Value Metrics
def get_lifetime_value_metrics(client, property_id):
    metrics = [
        Metric(name="lifetimeValueRevenue"),
        Metric(name="lifetimeValuePurchases"),
        Metric(name="averageLifetimeValue"),
        Metric(name="customerLifetimeValue"),
    ]
    return run_report(client, property_id, metrics)

# Demographic Metrics
def get_demographic_metrics(client, property_id):
    metrics = [
        Metric(name="country"),
    ]
    return run_report(client, property_id, metrics, dimensions=[Dimension(name="date"), Dimension(name="country")])

# Technology Metrics
def get_technology_metrics(client, property_id):
    metrics = [
        Metric(name="deviceCategory"),
        Metric(name="operatingSystem"),
        Metric(name="browser"),
        Metric(name="screenResolution"),
        Metric(name="appVersion"),
        Metric(name="platform"),
    ]
    return run_report(client, property_id, metrics, dimensions=[Dimension(name="date"), Dimension(name="deviceCategory"), Dimension(name="operatingSystem"), Dimension(name="browser"), Dimension(name="screenResolution"), Dimension(name="appVersion"), Dimension(name="platform")])

# Goal Metrics
def get_goal_metrics(client, property_id):
    metrics = [
        Metric(name="goalCompletionsAll"),
        Metric(name="goalConversionRateAll"),
        Metric(name="goalValueAll"),
        Metric(name="goalStartsAll"),
    ]
    return run_report(client, property_id, metrics)

# Content Metrics
def get_content_metrics(client, property_id):
    metrics = [
        Metric(name="pageviews"),
        Metric(name="uniquePageviews"),
        Metric(name="timeOnPage"),
        Metric(name="entrances"),
        Metric(name="pageValue"),
        Metric(name="exitRate"),
    ]
    return run_report(client, property_id, metrics)

def get_ga4_accounts(credentials):
    client = AnalyticsAdminServiceClient(credentials=credentials)
    try:
        accountList = []
        accounts = list(client.list_account_summaries().account_summaries)
        for item in accounts:
            accountList.append(item.account.split("accounts/")[1])
        return accountList
    except GoogleAuthError as e:
        print(f"Authentication error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def get_ga4_properties(credentials, accountList):
    client = AnalyticsAdminServiceClient(credentials=credentials)
    try:
        for account_id in accountList:
            properties = client.list_properties(
            ListPropertiesRequest(filter=f"parent:accounts/{account_id}", show_deleted=True)
            )
            propertiesList = []
            for property in properties:

                propertiesList.append({
                    "id": property.name.split("properties/")[1],
                    "create_time": property.create_time,
                    "parent": property.parent,
                    "display_name":property.display_name,
                    "industry_category": property.industry_category,
                    "time_zone": property.time_zone,
                    "currency_code": property.currency_code,
                    "service_level":property.service_level,
                    "account_id": property.account
                })

        return propertiesList
    
    except GoogleAuthError as e:
        print(f"Authentication error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def get_google_analytics_data(access_token):

    google_analytics_data = [{"channel_type": "Google Analytics"}]
    try:
        # Build the Admin API client to get the GA4 property ID
        credentials = Credentials(token=access_token)

        accountList = get_ga4_accounts(credentials)
        accountProperties = get_ga4_properties(credentials,accountList)
        # # Create the Data API client using the credentials
        data_api_client = BetaAnalyticsDataClient(credentials=credentials)

        for property in accountProperties:
            # Standard Metrics
            user_metrics = get_user_metrics(data_api_client, property['id'])
            session_metrics = get_session_metrics(data_api_client, property['id'])
            event_metrics = get_event_metrics(data_api_client, property['id'])
            ecommerce_metrics = get_ecommerce_metrics(data_api_client, property['id'])
            engagement_metrics = get_engagement_metrics(data_api_client, property['id'])
            ad_metrics = get_ad_metrics(data_api_client, property['id'])
            lifetime_value_metrics = get_lifetime_value_metrics(data_api_client, property['id'])
            demographic_metrics = get_demographic_metrics(data_api_client, property['id'])
            technology_metrics = get_technology_metrics(data_api_client, property['id'])
            goal_metrics = get_goal_metrics(data_api_client, property['id'])
            content_metrics = get_content_metrics(data_api_client, property['id'])

            # Real-time Metrics
            realtime_metrics = run_realtime_report(data_api_client, property['id'], [
                Metric(name="activeUsers"),
                Metric(name="screenPageViews")
            ], dimensions=[Dimension(name="country")])

            # Pivot Report
            pivots = [
                Pivot(
                    field_names=["date", "country"],
                    order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"))],
                    offset=0,
                    limit=10
                )
            ]
            pivot_metrics = run_pivot_report(data_api_client, property['id'], [
                Metric(name="sessions"),
                Metric(name="bounceRate")
            ], dimensions=[Dimension(name="date"), Dimension(name="country")], pivots=pivots)

            # Return all metrics
            analytics_data = {
                "property_details": property,
                "user_metrics": user_metrics,
                "session_metrics": session_metrics,
                "event_metrics": event_metrics,
                "ecommerce_metrics": ecommerce_metrics,
                "engagement_metrics": engagement_metrics,
                "ad_metrics": ad_metrics,
                "lifetime_value_metrics": lifetime_value_metrics,
                "demographic_metrics": demographic_metrics,
                "technology_metrics": technology_metrics,
                "goal_metrics": goal_metrics,
                "content_metrics": content_metrics,
                "realtime_metrics": realtime_metrics,
                "pivot_metrics": pivot_metrics,
            }
            google_analytics_data.append(analytics_data)
        
        return google_analytics_data
    
    except Exception as e:
        print("Error in Fetching Google Analytics Channel Data:" + str(e))
        return None

