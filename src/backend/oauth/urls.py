from django.urls import path

from . import views


urlpatterns = [
    # /api/oauth/google/
    path("google-callback/", views.google_oauth_callback),
    path("google/", views.google_oauth),

]