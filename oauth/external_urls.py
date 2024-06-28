production = False

if not production:
    backend_url =  "http://127.0.0.1:8000/"
    frontend_channel_url = "http://localhost:3000/channels/"
else:
    backend_url = "https://polite-awake-bobcat.ngrok-free.app/"
    frontend_channel_url = "https://kleenestar.vercel.app/channels/"

google_apis_url = "https://www.googleapis.com"
google_redirect_uri = f'{backend_url}api/oauth/google-callback/'

facebook_authorization_base_url = 'https://www.facebook.com/v20.0/dialog/oauth'
facebook_redirect_uri = 'https://127.0.0.1:8000/api/oauth/facebook-callback/'
facebook_api_url = "https://graph.facebook.com/v20.0"
facebook_token_url = 'https://graph.facebook.com/v20.0/oauth/access_token'

twitter_ads_api_url = 'https://ads-api.twitter.com/'
twitter_redirect_uri = f'{backend_url}api/oauth/twitter-callback/'
twitter_authorization_base_url = "https://twitter.com/oauth/authorize"
twitter_token_url = "https://twitter.com/oauth/access_token"

linkedin_authorization_base_url = 'https://www.linkedin.com/oauth/v2/authorization'
linkedin_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
linkedin_redirect_uri = f'{backend_url}api/oauth/linkedin-callback/'

# configured in tiktok app (browser)
tiktok_redirect_uri = 'https://a7b1-2401-4900-57e1-6bfc-4182-80ff-5d55-cbdf.ngrok-free.app/api/oauth/tiktok-callback/'
tiktok_token_url = 'https://business-api.tiktok.com/open_api/v1.3/oauth2/access_token/'
tiktok_api_url = "https://business-api.tiktok.com/open_api"
tiktok_sandbox_api_url = "https://sandbox-ads.tiktok.com/open_api"

reddit_token_url = 'https://www.reddit.com/api/v1/access_token'
reddit_api_url = "https://ads-api.reddit.com/api/v3"
reddit_redirect_uri = f'{backend_url}api/oauth/reddit-callback/'


shopify_redirect_uri = f"{backend_url}api/oauth/shopify-callback/"

google_analytics_redirect_uri = f'{backend_url}api/oauth/google-analytics-callback/'

mailchimp_redirect_uri = f"{backend_url}api/oauth/mailchimp-callback/"
mailchimp_token_uri = "https://login.mailchimp.com/oauth2/token"
mailchimp_metadata_uri = "https://login.mailchimp.com/oauth2/metadata"