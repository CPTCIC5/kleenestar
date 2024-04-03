from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import ConvoViewSet, PromptInputViewSet

from . import views

router = DefaultRouter()
router.register("channels/", views.ChannelViewSet, basename="channels")
router.register(r'convos', ConvoViewSet)
router.register(r'promptinputs', PromptInputViewSet)


urlpatterns = [
    path('', include(router.urls)),
]