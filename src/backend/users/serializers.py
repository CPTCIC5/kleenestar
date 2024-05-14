from rest_framework import serializers
from .models import User, Profile, Feedback


class UserCreateSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()
    invite_code = serializers.CharField(required=False)

    class Meta:
        model = User
        write_only = ["password", "confirm_password"]
        fields = ["email", "password", "confirm_password", "invite_code","newsletter"]

    def create(self, validated_data):
        if validated_data["password"] == validated_data["confirm_password"]:
            print('matchingg')
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

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or create profile related to the user
        if profile_data:
            profile_instance, _ = Profile.objects.update_or_create(user=instance, defaults=profile_data)
            # Update profile instance with nested serializer data
            ProfileSerializer(profile_instance, data=profile_data).is_valid(raise_exception=True)
            profile_instance.save()
        return instance


class FeedbackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ("urgency", "subject", "message", "emoji", "attachment")

    """
    def create(self, validated_data):
        return Feedback.objects.create(
            user=self.context['request'].user,
            **validated_data
        )
    """


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True,write_only=True)
    new_password = serializers.CharField(required=True,write_only=True)
    confirm_new_password= serializers.CharField(required=True,write_only=True)