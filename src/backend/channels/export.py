"""
import rag
xd = rag.RagData("What is my avatar?", "xyz@gmail.com", "123")
print(xd)
"""

# import json
# import os
# from rest_framework.decorators import permission_classes
# from rest_framework.permissions import AllowAny
# from oauth.channels import google,facebook,twitter,linkedin,reddit,tiktok,shopify
# from channels.models import Channel
# from django.shortcuts import get_object_or_404


# @api_view(['GET'])
# @permission_classes([AllowAny])  # Allow access to anyone
# def merge_json_files(request):
#     # GET the user email check the workspace and then get the credentials for the particular channel based on channel_type(parameter)
#     merged_data = []
    
#     # List all JSON files in the specified folder
#     json_files = [f for f in os.listdir("channels/") if f.endswith(".json")]

#     # Iterate over each JSON file
#     for filename in json_files:
#         file_path = os.path.join("channels/", filename)

#         # Load JSON data from the file
#         with open(file_path, "r") as file:
#             file_data = json.load(file)

#         # Extract the key (e.g., 'xyz1', 'xyz2', ...) from the filename
#         key = os.path.splitext(filename)[0]  # Remove the file extension (.json)

#         # Merge the file data into the merged_data dictionary
#         merged_data.append(file_data)

#     return Response(merged_data)


from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import logging
from .models import Channel
from oauth.channels import google, facebook, twitter, linkedin, tiktok, reddit, shopify
from oauth.helper import refresh_credentials
logger = logging.getLogger(__name__)


@api_view(("GET",))
def merge_json_files(request):
    print(request.user.email)
    user = request.user
    workspace = user.workspace_set.first() # Use first() instead of all()[0] for better practice

    if not workspace:
        return Response({"error": "No workspace found for the user"}, status=400)

    merged_data = []
    
    channel_types = {
        1: [google.get_google_marketing_data, google.get_google_analytics_data],
        2: facebook.get_facebook_marketing_data,
        3: twitter.get_twitter_marketing_data,
        4: linkedin.get_linkedin_marketing_data,
        5: tiktok.get_tiktok_marketing_data,
        6: reddit.get_reddit_marketing_data,
        7: shopify.get_shopify_data
    }

    try:
        channels = Channel.objects.filter(workspace=workspace)

        for channel in channels:
            print(channel.channel_type)

            get_data_func = channel_types.get(channel.channel_type)
            refresh_credentials(channel) # Check-Refresh the credentials of this channel

            if get_data_func:
                credentials = channel.credentials
                if channel.channel_type == 1:
                    data = [get_data_func[0](credentials.key_1, credentials.key_3, credentials.key_4), get_data_func[1](credentials.key_2)]
                elif channel.channel_type == 2: #not-finished
                    data = get_data_func(credentials.key_1, credentials.key_2)
                elif channel.channel_type == 3:
                    data = get_data_func(credentials.key_3, credentials.key_4)
                elif channel.channel_type == 4:
                    data = get_data_func(credentials.key_1)
                elif channel.channel_type == 5: #not-finished
                    data = get_data_func(credentials.key_1, credentials.key_2)
                elif channel.channel_type == 6:
                    data = get_data_func(credentials.key_1)
                elif channel.channel_type == 7:
                    data = get_data_func(credentials.key_1,credentials.key_2)
                merged_data.append(data)
        
        logger.info(f"Merged data: {merged_data}")
        
        return Response(
            merged_data, status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

