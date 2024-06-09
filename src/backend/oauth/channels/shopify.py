import requests
import urllib.parse
import os
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from oauth.external_urls import frontend_channel_url,shopify_redirect_uri
from oauth.helper import get_channel,create_channel
from dotenv import load_dotenv
from channels.models import APICredentials

load_dotenv()

shop = 'kleenestar'  
shopify_client_id = os.getenv("SHOPIFY_CLIENT_ID")
scopes = 'read_products,read_orders'


@api_view(("GET",))
def shopify_oauth(request):
    try:
        authorization_url = f"https://{shop}.myshopify.com/admin/oauth/authorize?client_id={shopify_client_id}&scope={scopes}&redirect_uri={urllib.parse.quote(shopify_redirect_uri)}"

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
def shopify_oauth_callback(request):
    try:
        code = request.query_params.get('code')
        shop = request.query_params.get('shop')
        hmac = request.query_params.get('hmac')
        
        access_token = exchange_code_for_token(shop, code)
        print(access_token)

        try:
            shopify_channel = get_channel(email=request.user.email, channel_type_num=7)
        except Exception:
            shopify_channel = create_channel(email=request.user.email, channel_type_num=7)
        
        if shopify_channel.credentials is None:
            credentials = APICredentials.objects.create(
                key_1=access_token
            )
            shopify_channel.credentials = credentials
        else:
            shopify_channel.credentials.key_1 = access_token
            shopify_channel.credentials.save()

        shopify_channel.save()
        return redirect(frontend_channel_url)
    
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    

def exchange_code_for_token(shop, code):
    api_key = os.getenv("SHOPIFY_CLIENT_ID")
    api_secret = os.getenv("SHOPIFY_CLIENT_SECRET")
    token_url = f"https://{shop}/admin/oauth/access_token"
    payload = {
        'client_id': api_key,
        'client_secret': api_secret,
        'code': code
    }
    response = requests.post(token_url, data=payload)
    access_token = response.json().get('access_token')
    return access_token
