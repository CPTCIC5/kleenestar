from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile,Team,Feedback

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        write_only = [ 'password']
        fields = ['username','password']
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','is_active',]

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        #read_only = ['referral_code']
        fields = ['user','avatar','role','country'
                  ,'phone_number']
    
    """
    def create(self, validated_data):
        return Profile.objects.create(user=self.context['request'].user, **validated_data)
    """

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['root_user','users','name',
                  'url','budget','industry','created_at']
        
        
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['user','urgency','category',
                  'message','emoji','attachment']