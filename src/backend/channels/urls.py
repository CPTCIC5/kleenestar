from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

router = DefaultRouter()
router.register("channels/", views.ChannelViewSet, basename="channels")


urlpatterns = [
    path('prompt-feedback/',views.PromptFeedbackView.as_view(),name='feedback'),
    path('input/',views.PromptInputView.as_view(),name='prompt')
]