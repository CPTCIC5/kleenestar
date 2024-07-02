import requests
import os
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from oauth.external_urls import frontend_channel_url,mailchimp_redirect_uri, mailchimp_token_uri, mailchimp_metadata_uri
from oauth.helper import get_channel,create_channel
from dotenv import load_dotenv
import json
import base64
import hashlib
from channels.models import APICredentials
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

load_dotenv(override=True)

# State value for OAuth request authentication
passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()

mailchimp_client_id = os.getenv('MAILCHIMP_CLIENT_ID')
mailchimp_client_secret = os.getenv('MAILCHIMP_CLIENT_SECRET')

@api_view(("GET",))
def mailchimp_oauth(request):
    state_dict = {'subspace_id': request.query_params.get("subspace_id"), 'passthrough_val': passthrough_val}
    state_json = json.dumps(state_dict)
    state_encoded = base64.urlsafe_b64encode(state_json.encode()).decode()
    try:
        authorization_url = f"https://login.mailchimp.com/oauth2/authorize?response_type=code&client_id={mailchimp_client_id}&redirect_url={mailchimp_redirect_uri}&state={state_encoded}"

        return Response({"url": authorization_url}, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@csrf_exempt
@api_view(("GET",))
@permission_classes([AllowAny])
def mailchimp_oauth_callback(request):
    try:
        state_encoded = request.query_params.get('state')
        state_json = base64.urlsafe_b64decode(state_encoded).decode()
        state_params = json.loads(state_json)

        if state_params.get("passthrough_val", None) != passthrough_val:
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

        code = request.query_params.get('code')
        if not code:
            return Response(
                {"detail": "Code is missing in the redirect URI, invalid request!"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        
        params = {
        "grant_type": "authorization_code",
        "client_id": mailchimp_client_id,
        "client_secret": mailchimp_client_secret,
        "redirect_uri": mailchimp_redirect_uri,
        "code": code
        }

        response = requests.post(mailchimp_token_uri, data=params)

        response = response.json()

        access_token =  response.get("access_token", None)

        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        metadata_response = requests.get(mailchimp_metadata_uri, headers=headers)

        metadata_response = metadata_response.json()
        print(metadata_response)
        server_prefix = metadata_response.get("dc", None)

        if server_prefix and access_token:

            print(access_token, server_prefix)
            
            try:
                mailchimp_channel = get_channel(subspace_id=subspace_id, channel_type_num=9)
            except Exception:
                mailchimp_channel = create_channel(subspace_id=subspace_id, channel_type_num=9)
            
            if mailchimp_channel.credentials is None:
                credentials = APICredentials.objects.create(
                    key_1=access_token,
                    key_2=server_prefix,
                )
                mailchimp_channel.credentials = credentials
            else:
                mailchimp_channel.credentials.key_1 = access_token
                mailchimp_channel.credentials.key_2 = server_prefix
                mailchimp_channel.credentials.save()

            mailchimp_channel.save()
            return redirect(frontend_channel_url)
        
        else:
            return Response(
                {"detail": f"Error: {response.content}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )



def get_client(api_key, server_prefix):
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": api_key,
        "server": server_prefix
    })
    return client

def get_automations(client):
    automations_data = []
    try:
        automations = client.automations.list()
        for automation in automations['automations']:
            workflow_id = automation['id']
            workflow_details = client.automations.get(workflow_id)
            emails = client.automations.list_all_workflow_emails(workflow_id)
            for email in emails['emails']:
                email_id = email['id']
                email_details = client.automations.get_workflow_email(workflow_id, email_id)
                queue = client.automations.get_workflow_email_subscriber_queue(workflow_id, email_id)
                automations_data.append({
                    "workflow_details": workflow_details,
                    "email_details": email_details,
                    "queue": queue
                })
    except ApiClientError as error:
        print("Error: {}".format(error.text))
    return automations_data

def get_campaigns(client):
    campaigns_data = []
    try:
        campaigns = client.campaigns.list()
        for campaign in campaigns['campaigns']:
            campaign_id = campaign['id']
            details = client.campaigns.get(campaign_id)
            content = client.campaigns.get_content(campaign_id)
            report = client.reports.get_campaign_report(campaign_id)
            campaigns_data.append({
                "campaign_details": details,
                "content": content,
                "report": report
            })
    except ApiClientError as error:
        print("Error: {}".format(error.text))
    return campaigns_data

def get_conversations(client):
    conversations_data = []
    try:
        conversations = client.conversations.list()
        for conversation in conversations['conversations']:
            conversation_id = conversation['id']
            messages = client.conversations.get_conversation_messages(conversation_id)
            conversations_data.append({
                "conversation_id": conversation_id,
                "messages": messages
            })
    except ApiClientError as error:
        print("Error: {}".format(error.text))
    return conversations_data

def get_connected_sites(client):
    connected_sites_data = []
    try:
        sites = client.connectedSites.list()
        for site in sites['sites']:
            site_id = site['foreign_id']
            details = client.connectedSites.get(site_id)
            connected_sites_data.append(details)
    except ApiClientError as error:
        print("Error: {}".format(error.text))
    return connected_sites_data


def get_ecommerce_stores(client):
    ecommerce_data = []
    try:
        stores = client.ecommerce.stores()
        for store in stores['stores']:
            store_id = store['id']
            store_details = client.ecommerce.get_store(store_id)
            products = client.ecommerce.get_all_store_products(store_id)
            orders = client.ecommerce.get_order(store_id)
            customers = client.ecommerce.get_all_store_customers(store_id)
            ecommerce_data.append({
                "store_details": store_details,
                "products": products,
                "orders": orders,
                "customers": customers
            })
    except ApiClientError as error:
        print("Error: {}".format(error.text))
    return ecommerce_data

def get_facebook_ads(client):
    facebook_ads_data = []
    try:
        ads = client.facebookAds.list()
        for ad in ads['facebook_ads']:
            ad_id = ad['id']
            details = client.facebookAds.get_ad(ad_id)
            facebook_ads_data.append(details)
    except ApiClientError as error:
        print("Error: {}".format(error.text))
    return facebook_ads_data

def get_activity(list_id, client):
    try:
        activity = client.lists.get_list_recent_activity(list_id)
        return activity
    except ApiClientError as error:
        print("Error: {}".format(error.text))
        return []

def get_subscriber_hash(email):
    email = email.lower().encode('utf-8')
    subscriber_hash = hashlib.md5(email).hexdigest()
    return subscriber_hash

def get_all_members(list_id, client):
    try:
        members = client.lists.get_list_members_info(list_id)
        return members['members']
    except ApiClientError as error:
        print("Error: {}".format(error.text))
        return []

def get_member_activity(list_id, email, client):
    subscriber_hash = get_subscriber_hash(email)
    try:
        activity = client.lists.get_list_member_activity(list_id, subscriber_hash)
        return activity
    except ApiClientError as error:
        print("Error: {}".format(error.text))
        return []

def get_member_activities(list_id, client):
    all_activities = {}
    members = get_all_members(list_id, client)
    for member in members:
        email = member['email_address']
        activity = get_member_activity(list_id, email, client)
        all_activities[email] = activity
    return all_activities

def get_locations(list_id, client):
    try:
        locations = client.lists.get_list_locations(list_id)
        return locations
    except ApiClientError as error:
        print("Error: {}".format(error.text))
        return []

def get_reports(client):
    reports_data = []
    try:
        reports = client.reports.get_all_campaign_reports()
        for report in reports['reports']:
            reports_data.append(report)
    except ApiClientError as error:
        print("Error: {}".format(error.text))
    return reports_data



def get_mailchimp_data(access_token,server_prefix):

    try:
        client = get_client(access_token, server_prefix)
        lists = client.lists.get_all_lists()
        list_ids = [lst['id'] for lst in lists['lists']]

        marketing_data = {
            "channel_type": "Mailchimp",
            "automations": get_automations(client),
            "campaigns": get_campaigns(client),
            "conversations": get_conversations(client),
            "connected_sites": get_connected_sites(client),
            "ecommerce_stores": get_ecommerce_stores(client),
            "facebook_ads": get_facebook_ads(client),
            "activity": {list_id: get_activity(list_id, client) for list_id in list_ids},
            "locations": {list_id: get_locations(list_id, client) for list_id in list_ids},
            "member_activity": {list_id: get_member_activities(list_id, client) for list_id in list_ids},
            "reports": get_reports(client)
        }

        return marketing_data
    
    except Exception as e:
        print("Error in Fetching Mailchimp Channel Data:" + str(e))
        return None
