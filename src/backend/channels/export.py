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

"""

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


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Allow access logged in user
def merge_json_files(request):
    user= request.user
    workspace= user.workspace_set.all()[0]
    google_cred= get_object_or_404(Channel, workspace=workspace,channel_type=1).credentials
    meta_cred= get_object_or_404(Channel, workspace=workspace,channel_type=2).credentials
    twitter_cred= get_object_or_404(Channel, workspace=workspace,channel_type=3).credentials
    linkedin_cred= get_object_or_404(Channel, workspace=workspace,channel_type=4).credentials
    tiktok_cred= get_object_or_404(Channel, workspace=workspace,channel_type=5).credentials


    merged_data = []
    
    #Get data from each marketing channel function
    google_data = views.get_google_marketing_data(google_cred.key_1, google_cred.key_3) #pass key1 and key3 as params
    facebook_data = views.get_facebook_marketing_data(meta_cred.key_1, meta_cred.key_2) #pass key1 and key2 as params
    twitter_data = views.get_twitter_marketing_data(twitter_cred.key_1, twitter_cred.key_2, twitter_cred.key_3, twitter_cred.key_4)
    linkedin_data = views.get_linkedin_marketing_data(linkedin_cred.key_1)
    tiktok_data = views.get_tiktok_marketing_data()

    merged_data.extend([google_data, facebook_data, twitter_data, linkedin_data, tiktok_data])


    return Response(merged_data)