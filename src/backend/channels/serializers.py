from rest_framework import serializers
from users.models import User
from . import models
import json

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

class PromptInputSerializer(serializers.Serializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),many=False)
    user_query=serializers.CharField(max_length=50,required=True)
    refactored_query = serializers.CharField(allow_blank=True) #gpt 3.5 turbo 
    response_text=serializers.CharField(allow_blank=True)
    image=serializers.ImageField(allow_null=True, required=False)
    created = serializers.DateTimeField()


    def create(self, validated_data):
        try:
            # Attempt to open the existing JSON file
            with open('response_data.json', 'r') as file:
                response_data_list = json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, initialize an empty list
            response_data_list = []

        # Append the new response data to the list
        response_data_list.append({
            'user_query': validated_data['user_query'],
            'refactored_query': validated_data['refactored_query'],
            'response_text': validated_data['response_text'],
            'created': validated_data['created'].isoformat(),
        })

        # Write the updated list back to the JSON file
        with open('response_data.json', 'w') as file:
            json.dump(response_data_list, file)

        return response_data_list