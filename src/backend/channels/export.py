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

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Allow access logged in user
def merge_json_files(request):
    merged_data = []

    # Get data from each marketing channel function
    google_data = views.get_google_marketing_data()
    facebook_data = views.get_facebook_marketing_data()
    twitter_data = views.get_twitter_marketing_data()
    linkedin_data = views.get_linkedin_marketing_data()
    tiktok_data = views.get_tiktok_marketing_data()

    # Append each data to the merged_data list
    merged_data.append(google_data)
    merged_data.append(facebook_data)
    merged_data.append(twitter_data)
    merged_data.append(linkedin_data)
    merged_data.append(tiktok_data)

    return Response(merged_data)