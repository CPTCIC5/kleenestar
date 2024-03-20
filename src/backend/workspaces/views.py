from rest_framework import viewsets
from rest_framework.response import Response

from . import permissions
from .serializers import WorkSpaceSerializer, WorkSpaceCreateSerializer


class WorkSpacesViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.WorkSpaceViewSetPermissions,)
    serializer_class = WorkSpaceSerializer

    def get_queryset(self):
        # All the workspaces the request user is a member of
        return self.request.user.workspace_set.all()

    def create(self, request, *args, **kwargs):
        serializer = WorkSpaceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(root_user=self.request.user)

        return Response(self.get_serializer(instance).data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = WorkSpaceCreateSerializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)

        new_instance = serializer.save()

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(self.get_serializer(new_instance).data)
