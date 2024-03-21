from rest_framework import serializers
from . import models

class APICredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.APICredentials
        fields  = ['key_1','key_2','key_3','key_4']


class ChannelSerializer(serializers.ModelSerializer):
    credentials = APICredentialsSerializer()
    class Meta:
        model = models.Channel
        fields  = ['activated','channel_type','connected','workspace','credential']


class PromptFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PromptFeedback
        fields = ['user','note']