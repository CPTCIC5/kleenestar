from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
import os
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException
"""
This file is to refresh all the credentials 

----> validity info for all the channels:

google - access_token expires after 1 hour , then need to refresh 

*facebook - access_token is valid for 60 days

twitter - do not expire

linkedin - access token is valid for 60 days , and then refresh

reddit - valid for 1 hour and then refresh

shopify - access token has no expiry, it is expired after the user uninstalls the app

*tiktok - expires in few hours (yet to figure out refresh token)

"""

def check_update_google_credentials(access_token, refresh_token):
    credentials = Credentials(
    token=access_token,
    refresh_token=refresh_token,
    token_uri="https://oauth2.googleapis.com/token",
    client_id= os.getenv("GOOGLE_CLIENT_ID"),
    client_secret= os.getenv("GOOGLE_CLIENT_SECRET")
    )

    try:
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            return True, credentials.token
        else:
            return False
        
    except RefreshError as e:
            raise Exception("Failed to refresh token.")


def check_update_facebook_credentials(access_token):
    debug_token_url = "https://graph.facebook.com/debug_token"
    app_id = os.getenv("FACEBOOK_CLIENT_ID")
    app_secret = os.getenv("FACEBOOK_CLIENT_SECRET")
    
    try:
        response = requests.get(
            debug_token_url,
            params={
                'input_token': access_token,
                'access_token': f'{app_id}|{app_secret}'
            }
        )
        response_data = response.json()
        
        if response.status_code == 200 and 'data' in response_data:
            data = response_data['data']
            if data['is_valid']:
                return True, access_token
            else:
                raise Exception("Facebook access token is invalid or expired.")
        else:
            raise Exception("Failed to validate Facebook access token.")
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to check Facebook access token: {e}")
    

def check_update_twitter_credentials(access_token, access_token_secret):
    verify_credentials_url = "https://api.twitter.com/1.1/account/verify_credentials.json"
    consumer_key = os.getenv("TWITTER_CLIENT_ID")
    consumer_secret = os.getenv("TWITTER_CLIENT_SECRET")

    try:
        response = requests.get(
            verify_credentials_url,
            auth=HTTPBasicAuth(consumer_key, consumer_secret),
            headers={
                'Authorization': f'Bearer {access_token}',
                'oauth_token': access_token,
                'oauth_token_secret': access_token_secret
            }
        )
        
        if response.status_code == 200:
            return True, access_token
        else:
            raise Exception("Twitter access token is invalid or expired.")
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to check Twitter access token: {e}")
    

def check_update_linkedin_credentials(access_token, refresh_token):
    verify_credentials_url = "https://api.linkedin.com/v2/me"
    refresh_token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    client_id = os.getenv("LINKEDIN_CLIENT_ID")
    client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")

    try:
        response = requests.get(
            verify_credentials_url,
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )

        if response.status_code == 200:
            return True, access_token
        else:
            refresh_response = requests.post(
                refresh_token_url,
                data={
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token,
                    'client_id': client_id,
                    'client_secret': client_secret,
                }
            )

            if refresh_response.status_code == 200:
                new_token_data = refresh_response.json()
                new_access_token = new_token_data.get('access_token')
                if new_access_token:
                    return True, new_access_token
                else:
                    raise Exception("Failed to obtain new access token from refresh response.")
            else:
                raise Exception("Failed to refresh LinkedIn access token.")
    
    except RequestException as e:
        raise Exception(f"Failed to check LinkedIn access token: {e}")
    

def check_update_tiktok_credentials(access_token):
    verify_credentials_url = "https://open-api.tiktok.com/oauth/userinfo/"
    try:
        response = requests.get(
            verify_credentials_url,
            headers={
                'Authorization': f'Bearer {access_token}'

            }
        )
        if response.status_code == 200:
            return True, access_token
        else:
            raise Exception("TikTok access token is invalid or expired.")
    
    except RequestException as e:
        raise Exception(f"Failed to check TikTok access token: {e}")


def check_update_reddit_credentials(access_token, refresh_token):
    verify_credentials_url = "https://oauth.reddit.com/api/v1/me"
    refresh_token_url = "https://www.reddit.com/api/v1/access_token"
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = "Kleenestar/1.0 by Powerful-Parsley4755"

    try:
        response = requests.get(
            verify_credentials_url,
            headers={
                'Authorization': f'Bearer {access_token}',
                'User-Agent': user_agent
            }
        )

        if response.status_code == 200:
            return True, access_token
        else:
            auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
            refresh_response = requests.post(
                refresh_token_url,
                auth=auth,
                data={
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token,
                },
                headers={
                    'User-Agent': user_agent
                }
            )

            if refresh_response.status_code == 200:
                new_token_data = refresh_response.json()
                new_access_token = new_token_data.get('access_token')
                if new_access_token:
                    return True, new_access_token
                else:
                    raise Exception("Failed to obtain new access token from refresh response.")
            else:
                raise Exception("Failed to refresh Reddit access token.")
    
    except RequestException as e:
        raise Exception(f"Failed to check Reddit access token: {e}")


def check_update_shopify_credentials(access_token, shop_name):
    shop_name = 'kleenestar'  
    api_version = "2024-01"
    verify_credentials_url = f"https://{shop_name}.myshopify.com/admin/api/{api_version}/shop.json"

    try:
        response = requests.get(
            verify_credentials_url,
            headers={
                'X-Shopify-Access-Token': access_token,
            }
        )
        if response.status_code == 200:
            return True, access_token
        else:
            raise Exception("Shopify access token is invalid or expired.")
    
    except RequestException as e:
        raise Exception(f"Failed to check Shopify access token: {e}")