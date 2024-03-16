from rest_framework import serializers
from .models import User, Profile, Team, Feedback


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        write_only = ["password"]
        fields = ["email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # read_only = ['referral_code']
        fields = ["avatar", "role", "country", "phone_number"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "email",
            "last_name",
            "is_active",
            "profile",
        ]


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            "root_user",
            "users",
            "name",
            "url",
            "budget",
            "industry",
            "created_at",
        ]


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["id", "user", "urgency", "category", "message", "emoji", "attachment"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
