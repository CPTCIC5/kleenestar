"""
import rag
xd = rag.RagData("What is my avatar?", "xyz@gmail.com", "123")
print(xd)
"""

import json
import os

def merge_json_files(folder_path):
    merged_data = {}

    # List all JSON files in the specified folder
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]

    # Iterate over each JSON file
    for filename in json_files:
        file_path = os.path.join(folder_path, filename)

        # Load JSON data from the file
        with open(file_path, 'r') as file:
            file_data = json.load(file)

        # Extract the key (e.g., 'xyz1', 'xyz2', ...) from the filename
        key = os.path.splitext(filename)[0]  # Remove the file extension (.json)

        # Merge the file data into the merged_data dictionary
        merged_data[key] = file_data

    return merged_data

# Specify the folder path containing the JSON files
folder_path = 'channels/'

# Merge JSON data from all files in the specified folder
merged_json = merge_json_files(folder_path)

print(merged_json)
# Print the merged JSON data
#print(json.dumps(merged_json, indent=2))  # Output the merged JSON data with indentation
