from django.urls import path
from rest_framework import routers
from rest_framework.views import RE


from . import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename='users')

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
] + router.urls
