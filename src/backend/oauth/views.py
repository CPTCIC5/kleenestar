from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from backend.settings import AUTH_USER_MODEL
from channels.models import Channel
import hashlib
import os
from urllib.parse import unquote
from google_auth_oauthlib.flow import Flow
import requests
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from requests_oauthlib import OAuth1Session
load_dotenv()

#state value for oauth request authentication
passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()

#google
google_redirect_uri = 'http://127.0.0.1:8000/api/oauth/google-callback/'
google_scopes = ["openid","https://www.googleapis.com/auth/adwords" ,"https://www.googleapis.com/auth/userinfo.email" ,"https://www.googleapis.com/auth/userinfo.profile"]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Adjusted to navigate to the project root
google_client_secret_file = os.path.join(BASE_DIR, 'oauth', 'utils', 'XYZ.json')
flow = Flow.from_client_secrets_file(google_client_secret_file, scopes=google_scopes)
flow.redirect_uri = google_redirect_uri


#facebook
facebook_client_id = os.getenv("FACEBOOK_CLIENT_ID")
facebook_client_secret = os.getenv("FACEBOOK_CLIENT_SECRET")
facebook_authorization_base_url = 'https://www.facebook.com/dialog/oauth'
facebook_redirect_uri = 'http://127.0.0.1:8000/api/oauth/facebook-callback/'
facebook_scopes = ['ads_read','ads_management']  
facebook = OAuth2Session(facebook_client_id, redirect_uri=facebook_redirect_uri, scope=facebook_scopes)
facebook = facebook_compliance_fix(facebook)
facebook_token_url = 'https://graph.facebook.com/oauth/access_token'


#twitter
twitter_client_id = os.getenv("TWITTER_CLIENT_ID")
twitter_client_secret = os.getenv("TWITTER_CLIENT_SECRET")
twitter_redirect_uri = 'http://127.0.0.1:8000/api/oauth/twitter-callback/'
twitter_authorization_base_url = "https://api.twitter.com/oauth/authenticate"
twitter_token_url = "https://api.twitter.com/oauth/access_token"
twitter_scopes = ["email", "ads_read", "ads_management"]
resource_owner_key = ''
resource_owner_secret = ''

#linkedin
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
linkedin_client_id = os.getenv('LINKEDIN_CLIENT_ID')
linkedin_client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
linkedin_scope = ["r_ads_reporting", "r_ads", "r_organization_admin", "r_emailaddress"]
linkedin_authorization_base_url = 'https://www.linkedin.com/oauth/v2/authorization'
linkedin_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
linkedin_redirect_uri = 'http://127.0.0.1:8000/api/oauth/linkedin-callback/'
linkedin = OAuth2Session(linkedin_client_id, redirect_uri=linkedin_redirect_uri, scope=linkedin_scope)




@csrf_exempt
@api_view(("GET",))
@permission_classes([AllowAny]) 
def google_oauth_callback(request):
    credentials = {
    "developer_token": "IxYU10YtrXbo7exsbvETNw",
    "client_id": "127357063070-13vjj74l6rmd6qi773k8fgraukp0e8vi.apps.googleusercontent.com",
    "client_secret": "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",
    "use_proto_plus": "false"
    }
    # code to get access token from refresh token

    # refresh_token = 'your_refresh_token'
    # client_id = 'your_client_id'
    # client_secret = 'your_client_secret'
    # token_uri = 'https://oauth2.googleapis.com/token'


    # creds = Credentials.from_authorized_user_info({
    #     'refresh_token': refresh_token,
    #     'client_id': client_id,
    #     'client_secret': client_secret,
    #     'token_uri': token_uri
    # })

    # if creds and creds.expired and creds.refresh_token:
    #     creds.refresh(Request())

    # access_token = creds.token

    # https://example.com/?code=...
    code = request.query_params.get("code")
    if not code:
        return Response(
        {"detail": "something not working???"},
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    elif request.query_params.get("state") != passthrough_val:
        return Response(
        {"detail": "State token does not match the expected state."},
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    try:
        flow.fetch_token(code=code)
        access_token = flow.credentials.token
        refresh_token = flow.credentials.refresh_token
        credentials["refresh_token"] = refresh_token

        response = requests.get(
            'https://www.googleapis.com/oauth2/v1/userinfo',
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

        client = GoogleAdsClient.load_from_dict(credentials , version='v16')
        customer_service = client.get_service("CustomerService")

        accessible_customers = customer_service.list_accessible_customers()
        
        if len(accessible_customers.resource_names) > 1:
            return Response(
                {"detail": "Manager accounts not allowed"},
                status=status.HTTP_403_FORBIDDEN,
            )

        resource_names = accessible_customers.resource_names

        if isinstance(resource_names, list):
            return Response(
                {"detail": "manager accounts not allowed"},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        customer_id = resource_names[0].split('/')[1]

        user = get_object_or_404(AUTH_USER_MODEL,email=email)  # get the user from the email
        workspace = user.workspace_set.all()[0]
        google_channel = get_object_or_404(Channel, channel_type=1)

        google_channel.credentials.key_1 = code
        google_channel.credentials.key_2 = refresh_token
        google_channel.credentials.key_3 = access_token
        google_channel.credentials.key_4 = customer_id
        google_channel.save()

        return Response(status=status.HTTP_200_OK)
    
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("GET",))
def google_oauth(request):
    try:
        authorization_url, state = flow.authorization_url(
            access_type="offline",
            state=passthrough_val,
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


@api_view(("GET",))
def facebook_oauth(request):
    try:
        authorization_url, state = facebook.authorization_url(url=facebook_authorization_base_url, state=passthrough_val)
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
def facebook_oauth_callback(request):

    redirect_response = request.build_absolute_uri()

    if request.query_params.get("state") != passthrough_val:
        return Response(
            {"detail": "State token does not match the expected state."},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    try:
        token = facebook.fetch_token(token_url=facebook_token_url, client_secret=facebook_client_secret, # 60days validity
                                     authorization_response=redirect_response)

        user_info_url = 'https://graph.facebook.com/v10.0/me?fields=id,name,email'
        user_info_response = facebook.get(user_info_url)
        email = user_info_response.json()['email']

        # aryan # creds to store in the db

        # filed name : value
        # access_token: token
        # email: email

        return Response({"detail": "OAuth process completed successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
def twitter_get_oauth_token(verifier, ro_key, ro_secret):
    oauth_token = OAuth1Session(client_key=twitter_client_id,
                                client_secret=twitter_client_secret,
                                resource_owner_key=ro_key,
                                resource_owner_secret=ro_secret,
                                scope=twitter_scopes)
    url = 'https://api.twitter.com/oauth/access_token'
    data = {"oauth_verifier": verifier}
    access_token_data = oauth_token.post(url, data=data)
    access_token_list = str.split(access_token_data.text, '&')
    return access_token_list

def twitter_get_oauth_request_token():
    global resource_owner_key
    global resource_owner_secret
    request_token = OAuth1Session(client_key=twitter_client_id, client_secret=twitter_client_secret, callback_uri=twitter_redirect_uri)
    url = 'https://api.twitter.com/oauth/request_token'
    data = request_token.get(url)
    data_token = str.split(data.text, '&')
    ro_key = str.split(data_token[0], '=')
    ro_secret = str.split(data_token[1], '=')
    callback_confirmed = str.split(data_token[2], '=')[1] if len(data_token) > 2 else None
    resource_owner_key = ro_key[1]
    resource_owner_secret = ro_secret[1]
    if callback_confirmed != 'true':
        return Response(
            {"detail": "Unauthorized request error!!!"},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

def twitter_oauth(request):
    try:
        twitter_get_oauth_request_token()
        url = "https://api.twitter.com/oauth/authenticate?oauth_token=" + resource_owner_key
        return Response({
            "url": url},
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
def twitter_oauth_callback(request):
    try:
        if not request.query_params.get("oauth_verifier"):
            return Response(
                {"detail": "something not working???"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
        oauth_verifier  = request.query_params.get("oauth_verifier")
        oauth_list = twitter_get_oauth_token(oauth_verifier,resource_owner_key,resource_owner_secret)
        access_token = {}
        for token in oauth_list:
            key, value = token.split('=')
            access_token[key] = value

        key = access_token['oauth_token'] # life long validity until revoked
        secret = access_token['oauth_token_secret']
        
        # Create OAuth1Session with the obtained access token
        oauth_user = OAuth1Session(client_key=resource_owner_key,
                                client_secret=resource_owner_secret,
                                resource_owner_key=key,
                                resource_owner_secret=secret)
        
        url_user = 'https://api.twitter.com/1.1/account/verify_credentials.json'
        params = {"include_email": 'true'}
        user_data = oauth_user.get(url_user, params=params)
        
        user_json = user_data.json()
        email = user_json.get('email', None)
    
        # aryan # creds to store in the db

        # filed name : value
        # consumer_key :  resource_owner_key
        # consumer_secret: resource_owner_secret
        # access_token: key
        # access_token_secret: secret
        # email: email

        return Response(status=status.HTTP_200_OK)

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
def linkedin_oauth(request):
    try:
        authorization_url, state = linkedin.authorization_url(url=linkedin_authorization_base_url, state=passthrough_val)
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
    
def linkedin_oauth_callback(request):
    try:
        if request.query_params.get("state") != passthrough_val:
            return Response(
            {"detail": "State token does not match the expected state."},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        redirect_response = request.build_absolute_uri()

        token = linkedin.fetch_token(token_url=linkedin_token_url, client_secret=linkedin_client_secret,  #60 days validity
                             include_client_id=True,
                             authorization_response=redirect_response)

        # Get the user's email address
        email_address_url = 'https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))'
        email_response = linkedin.get(email_address_url)
        email = email_response.json()['elements'][0]['handle~']['emailAddress']
        
        # aryan # creds to store in the db

        # filed name : value
        # access_token: token
        # email: email

        return Response(
            status=status.HTTP_200_OK
        )
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    