"""
import rag
xd = rag.RagData("What is my avatar?", "xyz@gmail.com", "123")
print(xd)
"""



import json
import os
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from oauth import views
from channels.models import Channel
from django.shortcuts import get_object_or_404



@api_view(['GET'])
@permission_classes([AllowAny])  # Allow access to anyone
def merge_json_files(request):
    # GET the user email check the workspace and then get the credentials for the particular channel based on channel_type(parameter)
    merged_data = []
    
    # List all JSON files in the specified folder
    json_files = [f for f in os.listdir("channels/") if f.endswith(".json")]

    # Iterate over each JSON file
    for filename in json_files:
        file_path = os.path.join("channels/", filename)

        # Load JSON data from the file
        with open(file_path, "r") as file:
            file_data = json.load(file)

        # Extract the key (e.g., 'xyz1', 'xyz2', ...) from the filename
        key = os.path.splitext(filename)[0]  # Remove the file extension (.json)

        # Merge the file data into the merged_data dictionary
        merged_data.append(file_data)

    return Response(merged_data)




"""
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import json
import logging
from .models import Channel
from oauth import views

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def merge_json_files(request):
    user = request.user
    workspace = user.workspace_set.first()  # Use first() instead of all()[0] for better practice

    if not workspace:
        return Response({"error": "No workspace found for the user"}, status=400)

    merged_data = []

    channel_types = {
        1: views.get_google_marketing_data,
        2: views.get_facebook_marketing_data,
        3: views.get_twitter_marketing_data,
        4: views.get_linkedin_marketing_data,
        5: views.get_tiktok_marketing_data
    }

    channels = Channel.objects.filter(workspace=workspace)

    for channel in channels:
        get_data_func = channel_types.get(channel.channel_type)
        if get_data_func:
            credentials = channel.credentials
            if channel.channel_type == 1:
                data = get_data_func(credentials.key_1, credentials.key_3)
            elif channel.channel_type == 2:
                data = get_data_func(credentials.key_1, credentials.key_2)
            elif channel.channel_type == 3:
                data = get_data_func(credentials.key_1, credentials.key_2, credentials.key_3, credentials.key_4)
            elif channel.channel_type == 4:
                data = get_data_func(credentials.key_1)
            elif channel.channel_type == 5:
                data = get_data_func()
            merged_data.append(data)
    
    logger.info(f"Merged data: {merged_data}")

    return Response(merged_data)
"""