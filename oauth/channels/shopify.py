import requests
from urllib.parse import urlencode, parse_qs, quote
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

load_dotenv(override=True)


shopify_client_id = os.getenv("SHOPIFY_CLIENT_ID")
scopes = 'read_products,read_orders,read_marketing_events,read_marketing_activity'


@api_view(("GET",))
def shopify_oauth(request):

    shop = request.query_params.get("shop")
    subspace_id = request.query_params.get("subspace_id")
    state = urlencode({'subspace_id': subspace_id})
    try:
        authorization_url = (
            f"https://{shop}.myshopify.com/admin/oauth/authorize"
            f"?client_id={shopify_client_id}&scope={scopes}&redirect_uri={quote(shopify_redirect_uri)}&state={state}"
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
    

def exchange_code_for_token(shop, code):
    url = f"https://{shop}/admin/oauth/access_token"
    payload = {
        'client_id': shopify_client_id,
        'client_secret': os.getenv("SHOPIFY_CLIENT_SECRET"),
        'code': code
    }
    response = requests.post(url, data=payload)
    response_data = response.json()
    return response_data['access_token']


@csrf_exempt
@api_view(("GET",))
@permission_classes([AllowAny]) 
def shopify_oauth_callback(request):
    try:
        code = request.query_params.get('code')
        shop = request.query_params.get('shop')
        hmac = request.query_params.get('hmac')
        state = request.query_params.get('state')

        state_params = parse_qs(state)
        print(state_params)
        subspace_id = state_params.get('subspace_id', [None])[0]
        
        access_token = exchange_code_for_token(shop, code)
        print(access_token)
        print(shop.split('.myshopify.com')[0])

        if not subspace_id:
            return Response(
                {"detail": "Unable to retrieve subspace of the user"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        try:
            shopify_channel = get_channel(subspace_id=subspace_id, channel_type_num=7)
        except Exception:
            shopify_channel = create_channel(subspace_id=subspace_id, channel_type_num=7)
        
        if shopify_channel.credentials is None:
            credentials = APICredentials.objects.create(
                key_1=access_token,
                key_2=shop
            )
            shopify_channel.credentials = credentials
        else:
            shopify_channel.credentials.key_1 = access_token
            shopify_channel.credentials.key_2 = shop.split('.myshopify.com')[0]
            shopify_channel.credentials.save()

        shopify_channel.save()
        return redirect(frontend_channel_url)

    
    except Exception as e:
        print(f"Exception occurred: {e}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    

def get_shopify_product_data(access_token, shop_name, api_version):
    url = f"https://{shop_name}.myshopify.com/admin/api/{api_version}/products.json"
    
    headers = {
        "X-Shopify-Access-Token": access_token
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    products_data = response.json().get('products', [])
    product_lists = [{
        "id": product['id'],
        "title": product['title'],
        "variants": [{
            "price": variant['price'],
            "inventory_quantity": variant['inventory_quantity']
        } for variant in product['variants']]
    } for product in products_data]
    
    return product_lists


def get_shopify_product_analytics(access_token, shop_name, api_version, product):
    url = f"https://{shop_name}.myshopify.com/admin/api/{api_version}/products/{product['id']}/metafields.json"
    
    headers = {
        "X-Shopify-Access-Token": access_token
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json().get('metafields', [])
    
    product_views = 0
    add_to_cart = 0
    purchases = 0
    conversion_rate = 0.0
    
    for metafield in data:
        if metafield['key'] == 'product_views':
            product_views = int(metafield['value'])
        elif metafield['key'] == 'add_to_cart':
            add_to_cart = int(metafield['value'])
        elif metafield['key'] == 'purchases':
            purchases = int(metafield['value'])
        elif metafield['key'] == 'conversion_rate':
            conversion_rate = float(metafield['value'])
    
    product_analytics = {
        'product_views': product_views,
        'add_to_cart': add_to_cart,
        'purchases': purchases,
        'conversion_rate': conversion_rate
    }
    product['product_analytics'] = product_analytics
    return product


def get_shopify_order_statistics(access_token, shop_name, api_version):
    url = f"https://{shop_name}.myshopify.com/admin/api/{api_version}/orders.json"
    
    headers = {
        "X-Shopify-Access-Token": access_token
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    orders_data = response.json().get('orders', [])
    
    order_statistics = [{
        'id': order['id'],
        'created_at': order['created_at'],
        'total_price': order['total_price'],
        'line_items': [{
            'quantity': item['quantity'],
            'price': item['price']
        } for item in order['line_items']],
        'financial_status': order['financial_status'],
        'fulfillment_status': order.get('fulfillment_status'),
        'customer': {
            'first_name': order['customer']['first_name'],
            'last_name': order['customer']['last_name'],
            'email': order['customer']['email']
        },
        'currency': order['currency']
    } for order in orders_data]
    
    return order_statistics

def get_shopify_marketing_events(access_token, shop_name, api_version):
    url = f"https://{shop_name}.myshopify.com/admin/api/{api_version}/marketing_events.json"
    
    headers = {
        "X-Shopify-Access-Token": access_token
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    marketing_events_data = response.json().get('marketing_events', [])
    
    marketing_events = [{
        'id': event['id'],
        'event_type': event['event_type'],
        'remote_id': event['remote_id'],
        'started_at': event['started_at'],
        'budget': event['budget'],
        'currency': event['currency'],
        'marketing_channel': event['marketing_channel'],
        'target_audience': event.get('target_audience', {}),
        'engagement': {
            'clicks': event.get('engagement', {}).get('clicks', 0),
            'impressions': event.get('engagement', {}).get('impressions', 0),
            'spend': event.get('engagement', {}).get('spend', 0.0),
            'conversion_rate': event.get('engagement', {}).get('conversion_rate', 0.0)
        }
    } for event in marketing_events_data]
    
    return marketing_events
    

def get_shopify_data(access_token, shop_name):

    api_version = '2024-01'
    
    try:
        product_data = get_shopify_product_data(access_token, shop_name, api_version)
        
        for product in product_data:
            product = get_shopify_product_analytics(access_token, shop_name, api_version, product)
        
        order_statistics = get_shopify_order_statistics(access_token, shop_name, api_version)
        
        marketing_events = get_shopify_marketing_events(access_token, shop_name, api_version)
        
        
        shopify_data = {
            "channel": "Shopify Channel",
            'product_data': product_data,
            'order_statistics': order_statistics,
            'marketing_events': marketing_events,
        }
        
        return shopify_data
    
    except Exception as e:
        print(f"Error fetching Shopify data: {e}")
        return None