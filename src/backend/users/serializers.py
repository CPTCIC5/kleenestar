from rest_framework import serializers
from .models import User, Profile, Feedback


class UserCreateSerializer(serializers.ModelSerializer):
    invite_code = serializers.CharField(required=False)

    class Meta:
        model = User
        write_only = ["password", "confirm_password"]
        fields = ["email", "password", "confirm_password", "invite_code"]

    def create(self, validated_data):
        if validated_data["password"] == validated_data["confirm_password"]:
            return User.objects.create_user(
                email=validated_data["email"], password=validated_data["password"]
            )
        else:
            return  serializers.ValidationError("Password and confirmation do not match.") 


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        read_only = ["referral_code"]
        fields = (
            "id",
            "user",
            "avatar",
            "country",
            "phone_number",
            "referral_code",
            "total_referrals",
        )


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "email",
            "last_name",
            "is_active",
            "profile",
        )


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ("id", "user", "urgency", "category", "message", "emoji", "attachment")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True,write_only=True)
    new_password = serializers.CharField(required=True,write_only=True)
    confirm_new_password= serializers.CharField(required=True,write_only=True)