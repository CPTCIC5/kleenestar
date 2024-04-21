from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import ConvoViewSet, PromptViewSet

from . import views

router = DefaultRouter()
router.register('convos/',ConvoViewSet,basename="convos")
router.register('promptinputs/', PromptViewSet,basename="prompt")
router.register("", views.ChannelViewSet, basename="channels")


urlpatterns = [
    path('', include(router.urls)),
]