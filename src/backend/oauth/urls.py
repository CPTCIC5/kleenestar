from django.urls import path

from . import views


urlpatterns = [
    # /api/oauth/google/
    path("google-callback/", views.google_oauth_callback),
    path("google/", views.google_oauth),
    path("facebook_data/", views.get_facebook_marketing_data),
    path("facebook-callback/", views.facebook_oauth_callback),
    path("facebook/", views.facebook_oauth),
    path("twitter-callback/", views.twitter_oauth_callback),
    path("twitter/", views.twitter_oauth),
    path("linkedin-callback/", views.linkedin_oauth_callback),
    path("linkedin/", views.linkedin_oauth),
    path("linkedin-data/", views.get_linkedin_marketing_data),
    path("tiktok-callback/", views.tiktok_oauth_callback),
    path("tiktok/", views.tiktok_oauth),
]
