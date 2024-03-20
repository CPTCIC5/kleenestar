from rest_framework import serializers

from users.serializers import UserSerializer
from .models import WorkSpace


class WorkSpaceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSpace
        fields = ("business_name", "website_url", "industry")


class WorkSpaceSerializer(WorkSpaceCreateSerializer):
    root_user = UserSerializer()
    users = UserSerializer(many=True)

    class Meta(WorkSpaceCreateSerializer.Meta):
        fields = (
            "id",
            "root_user",
            "users",
            "business_name",
            "website_url",
            "industry",
            "created_at",
        )
