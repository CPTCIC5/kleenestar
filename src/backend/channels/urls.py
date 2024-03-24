from django.urls import path
from . import views


urlpatterns = [
    path('prompt-feedback/',views.PromptFeedbackView.as_view(),name='feedback'),
    # path('channels/',views.ChannelViewSet.as_view(),name='channels'),
    path('input/',views.PromptInputView.as_view(),name='prompt')
]