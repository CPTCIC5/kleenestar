from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from app_channels.models import APICredentials
import hashlib
import os
import json
import base64
from google_auth_oauthlib.flow import Flow
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from dotenv import load_dotenv
from django.shortcuts import redirect
from oauth.helper import create_channel,get_channel
from oauth.external_urls import frontend_channel_url,google_apis_url,google_analytics_redirect_uri                        
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

google_analytics_scopes = ["openid",f"{google_apis_url}/auth/userinfo.email" ,f"{google_apis_url}/auth/userinfo.profile", f"{google_apis_url}/auth/analytics.readonly"]
flow = Flow.from_client_secrets_file(google_client_secret_file, scopes=google_analytics_scopes)
flow.redirect_uri = google_analytics_redirect_uri



@api_view(("GET",))
def google_analytics_oauth(request):

    state_dict = {'subspace_id': request.query_params.get("subspace_id"), 'passthrough_val': passthrough_val}
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
def google_analytics_oauth_callback(request):
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
    
    subspace_id = state_params.get("subspace_id", None)
    if not subspace_id:
        return Response(
            {"detail": "Unable to retrieve subspace of the user"},
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
        try:
            google_analytics_channel = get_channel(subspace_id=subspace_id, channel_type_num=8)
        except Exception:
            google_analytics_channel = create_channel(subspace_id=subspace_id, channel_type_num=8)
        
        if google_analytics_channel.credentials is None:
            credentials_new = APICredentials.objects.create(
                key_1=refresh_token,
                key_2=access_token,
            )
            google_analytics_channel.credentials = credentials_new
        else:
            google_analytics_channel.credentials.key_1 = refresh_token
            google_analytics_channel.credentials.key_2 = access_token
            google_analytics_channel.credentials.save()

        google_analytics_channel.save()

        return redirect(frontend_channel_url)

    
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )



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

    google_analytics_data = {"channel": "Google Analytics", "channel_data": []}
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
                "property_id": property['id'],
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
            google_analytics_data["channel_data"].append(analytics_data)
        
        return google_analytics_data
    
    except Exception as e:
        print("Error in Fetching Google Analytics Channel Data:" + str(e))
        return None

