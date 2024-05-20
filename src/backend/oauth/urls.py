from django.urls import path

from . import views


urlpatterns = [
    # /api/oauth/google/
    path("google-callback/", views.google_oauth_callback),
    path("google/", views.google_oauth),
    path("facebook-callback/", views.facebook_oauth_callback),
    path("facebook/", views.facebook_oauth),
    path("twitter-callback/", views.facebook_oauth_callback),
    path("twitter/", views.facebook_oauth),
    path("linkedin-callback/", views.facebook_oauth_callback),
    path("linkedin/", views.facebook_oauth),
]
