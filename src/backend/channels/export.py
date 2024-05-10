"""
import rag
xd = rag.RagData("What is my avatar?", "xyz@gmail.com", "123")
print(xd)
"""

import json
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def merge_json_files(request):
    merged_data = {}

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
        merged_data[key] = file_data

    return Response(merged_data)