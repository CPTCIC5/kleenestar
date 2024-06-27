from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

router.register(r'subspaces', views.SubSpaceViewSet, basename="subspaces")
router.register(r'', views.WorkSpacesViewSet, basename="workspaces")

urlpatterns = router.urls
