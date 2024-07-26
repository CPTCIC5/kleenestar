from django.urls import path

from .channels import google, facebook, twitter, linkedin, reddit,tiktok, shopify, mailchimp, google_analytics, bing

urlpatterns = [
    path("google-callback/", google.google_oauth_callback),
    path("google/", google.google_oauth),
    path("google_data/", google.get_google_marketing_data),


    path("google-analytics-callback/", google_analytics.google_analytics_oauth_callback),
    path("google-analytics/", google_analytics.google_analytics_oauth),
    path("google_analytics_data/", google_analytics.get_google_analytics_data),

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
    path("reddit_data/", reddit.get_reddit_marketing_data),

    path("shopify/", shopify.shopify_oauth),
    path("shopify-callback/", shopify.shopify_oauth_callback),
    path("shopify_data/",shopify.get_shopify_data),

    path("mailchimp/", mailchimp.mailchimp_oauth),
    path("mailchimp-callback/", mailchimp.mailchimp_oauth_callback),
    path("mailchimp_data/",mailchimp.get_mailchimp_data),

    path("bing/", bing.bing_oauth),
    path("bing-callback/", bing.bing_oauth_callback),
    
]
