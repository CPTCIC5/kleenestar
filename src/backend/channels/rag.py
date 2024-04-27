from langchain_community.document_loaders import JSONLoader
import json
import requests
from pathlib import Path
from pprint import pprint

def get_workspace():
    #file_path=requests.get("",headers={"sessionid":,"X-CSRFToken":"zZAzJ7omDS63g9gRV7ELeIADEoZZZzb2"})
    file_path = requests.get("http://127.0.0.1:8000/api/workspaces",auth=("aryanjainak@gmail.com","Iamreal@123"))
    print(file_path.text)
    #data = json.loads((file_path).read_text())