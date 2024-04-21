from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import ConvoViewSet, PromptViewSet

from . import views

router = DefaultRouter()
router.register("/", views.ChannelViewSet, basename="channels")
router.register(r'convos', ConvoViewSet)
router.register(r'promptinputs', PromptViewSet)


urlpatterns = [
    path('', include(router.urls)),
]