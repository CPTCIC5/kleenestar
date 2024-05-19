from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from backend.settings import AUTH_USER_MODEL
from channels.models import Channel
import argparse
import hashlib
import os
import re
import socket
import sys
from urllib.parse import unquote
from google_auth_oauthlib.flow import Flow
import requests
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


_REDIRECT_URI = 'http://127.0.0.1:8000/api/oauth/google-callback/'
_SCOPE = "https://www.googleapis.com/auth/adwords"
configured_scopes = [_SCOPE]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Adjusted to navigate to the project root
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, 'oauth', 'utils', 'XYZ.json')
ADS_CONFIG_FILE = os.path.join(BASE_DIR, 'oauth', 'utils', 'google-ads.yaml')
flow = Flow.from_client_secrets_file(CLIENT_SECRET_FILE, scopes=configured_scopes)
flow.redirect_uri = _REDIRECT_URI
passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()


@api_view(("GET", "POST"))
def google_oauth_callback(request):
    # https://example.com/?code=...
    code = request.query_params.get("code")
    if not code:
        return Response(
        {"detail": "something not working???"},
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    elif request.query_params.get != passthrough_val:
        return Response(
        {"detail": "State token does not match the expected state."},
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    try:
        flow.fetch_token(code=code)
        access_token = flow.credentials.token
        refresh_token = flow.credentials.refresh_token

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

        client = GoogleAdsClient.load_from_storage(ADS_CONFIG_FILE, version="v16")
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
        customer_id = resource_names[0]

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


@api_view(("GET", "POST"))
def google_oauth():
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
    