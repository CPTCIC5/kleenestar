from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
import os
import requests
from requests_oauthlib import OAuth1Session
from requests.exceptions import RequestException
from oauth.exceptions import RefreshException
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

instagram - yet to be completed

bing - access token - 60 days, and refresh token - 365 days

"""
#done
def check_update_google_credentials(refresh_token,access_token):
    credentials = Credentials(
    token=access_token,
    refresh_token=refresh_token,
    token_uri="https://accounts.google.com/o/oauth2/token",
    client_id= os.getenv("GOOGLE_CLIENT_ID"),
    client_secret= os.getenv("GOOGLE_CLIENT_SECRET")
    )

    try:
        url = "https://oauth2.googleapis.com/tokeninfo"
        params = {'access_token': access_token}
        response = requests.get(url, params=params)
        print(response)
        if response.status_code == 200:
            return False, ""
        else:
            credentials.refresh(Request())
            print("updated access token - google")
            return True, credentials.token
        
    except RefreshError as e:
            raise RefreshException("Invalid Credentials")

#not-done
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
                return True
            else:
                raise RefreshException("Invalid Credentials")
        else:
            raise RefreshException("Invalid Credentials")
    
    except requests.exceptions.RequestException as e:
        raise RefreshException("Invalid Credentials")
    
#done
def check_update_twitter_credentials(access_token, access_token_secret):
    consumer_key = os.getenv("TWITTER_CLIENT_ID")
    consumer_secret = os.getenv("TWITTER_CLIENT_SECRET")

    try:
        url = "https://api.twitter.com/1.1/account/verify_credentials.json"
        auth = OAuth1Session(client_key=consumer_key,
                                   client_secret=consumer_secret,
                                   resource_owner_key=access_token,
                                   resource_owner_secret=access_token_secret)

        response = auth.get(url)
        print(response)
        if response.status_code == 200:
            return True
        else:
            raise RefreshException("Invalid Credentials")
        
    except requests.exceptions.RequestException as e:
        print(str(e))
        raise RefreshException("Invalid Credentials")

#done
def check_update_linkedin_credentials(access_token, refresh_token):
    verify_credentials_url = "https://api.linkedin.com/v2/userinfo"
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

        print(response)
        response.raise_for_status()
        if response.status_code == 200:
            return False, ""
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
                    print("updated access token - linkedin")
                    return True, new_access_token
                else:
                    raise RefreshException("Invalid Credentials")
            else:
                raise RefreshException("Invalid Credentials")
    
    except RequestException as e:
        print(str(e))
        raise RefreshException("Invalid Credentials")
    
#not-done
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
            return True
        else:
            raise RefreshException("Invalid Credentials")
    
    except RequestException as e:
        raise RefreshException("Invalid Credentials")

#done
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
        print(response)
        if response.status_code == 200:
            return False, ""
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
                    print("updated access token - reddit")
                    return True, new_access_token
                else:
                    raise RefreshException("Invalid Credentials")
            else:
                raise RefreshException("Invalid Credentials")
    
    except RequestException as e:
        raise RefreshException("Invalid Credentials")

#done
def check_update_shopify_credentials(access_token, shop_name):

    api_version = "2024-01"
    verify_credentials_url = f"https://{shop_name}.myshopify.com/admin/api/{api_version}/shop.json"

    try:
        response = requests.get(
            verify_credentials_url,
            headers={
                'X-Shopify-Access-Token': access_token,
            }
        )
        print(response)
        if response.status_code == 200:
            return True
        else:
            raise RefreshException("Invalid Credentials")
    
    except RequestException as e:
        raise RefreshException("Invalid Credentials")
    
#done
def check_update_mailchimp_credentials(api_key, server_prefix):
    verify_credentials_url = f"https://{server_prefix}.api.mailchimp.com/3.0/"

    try:
        response = requests.get(
            verify_credentials_url,
            auth=('anystring', api_key)
        )
        print(response)
        if response.status_code == 200:
            return True
        else:
            raise RefreshException("Invalid Credentials")
    
    except RequestException as e:
        raise RefreshException("Invalid Credentials")


# not done
# def check_update_instagram_credentials():


# done
def check_update_bing_credentials(access_token, refresh_token):
    verify_credentials_url = "https://graph.microsoft.com/v1.0/me" 
    refresh_token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    client_id = os.getenv("BING_CLIENT_ID")
    client_secret = os.getenv("BING_CLIENT_SECRET")
    
    try:
        # Verify the current access token
        response = requests.get(
            verify_credentials_url,
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )

        if response.status_code == 200:
            return False, access_token
        else:
            print("Access token invalid, refreshing...")
            refresh_response = requests.post(
                refresh_token_url,
                data={
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token,
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'scope': 'https://ads.microsoft.com/msads.manage offline_access'
                }
            )

            if refresh_response.status_code == 200:
                new_token_data = refresh_response.json()
                new_access_token = new_token_data.get('access_token')
                if new_access_token:
                    print("Updated access token - Bing Ads")
                    return True, new_access_token
                else:
                    raise RefreshException("Failed to obtain new access token")
            else:
                raise RefreshException("Failed to refresh access token")
    
    except RequestException as e:
        print(f"Request exception: {e}")
        raise RefreshException("Failed to verify or refresh access token")
