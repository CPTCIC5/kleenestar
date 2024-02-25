from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

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
        read_only = ['referral_code']
        fields = ['user','phone_number','avatar','position'
                  ,'country','referral_code','total_referrals']
    
"""
    def create(self, validated_data):
        return Profile.objects.create(user=self.context['request'].user, **validated_data)
"""