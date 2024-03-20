from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from django.db.models import Q

from . import models, serializers


class WorkSpaceViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return models.WorkSpace.objects.filter(
            Q(root_user=self.request.user) | Q(users=self.request.user)
        )
