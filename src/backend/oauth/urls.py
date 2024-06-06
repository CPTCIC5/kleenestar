from django.urls import path

from .channels import google
from .channels import facebook
from .channels import twitter
from .channels import linkedin
from .channels import tiktok
from .channels import reddit

urlpatterns = [
    # /api/oauth/google/
    path("google-callback/", google.google_oauth_callback),
    path("google/", google.google_oauth),
    path("google_data/", google.get_google_marketing_data),

    path("facebook/", facebook.facebook_oauth),
    path("facebook-callback/", facebook.facebook_oauth_callback),
    path("facebook_data/", facebook.get_facebook_marketing_data),

    path("twitter-callback/", twitter.twitter_oauth_callback),
    path("twitter/", twitter.twitter_oauth),
    path("twitter_data/", twitter.get_twitter_marketing_data),

    path("linkedin-callback/", linkedin.linkedin_oauth_callback),
    path("linkedin/", linkedin.linkedin_oauth),
    path("linkedin_data/", linkedin.get_linkedin_marketing_data),

    path("tiktok_data/", tiktok.get_tiktok_marketing_data),
    path("tiktok-callback/", tiktok.tiktok_oauth_callback),
    path("tiktok/", tiktok.tiktok_oauth),
    
    path("reddit/", reddit.reddit_oauth),
    path("reddit-callback/", reddit.reddit_oauth_callback),
    path("reddit_data/", reddit.get_reddit_marketing_data)
]
