from celery import shared_task
from channels.rag import stats, delete_vectores, add_to_pinecone_vectorestore_openai
from workspaces.models import WorkSpace
from rest_framework.response import Response
from langchain_text_splitters import RecursiveJsonSplitter
import requests
import json
from backend.celery import app
from django.core.cache import cache
from datetime import datetime, timedelta

"""
channel_task function will be tasked to celery to make sure that the pinecone
vector store has the latest embeddings stored in the appropriate namespaces.
"""

API_URL = "http://127.0.0.1:8000/api/channels/xyz/"

@shared_task(name="channel_task_runner")
def channel_task():
    
    print(f"Task Running...")
    
    for workspace in WorkSpace.objects.all():
            namespace = workspace.pinecone_namespace
            documents , response_data = retrive_workspace_channel_data(workspace)
            
            add_to_pinecone(documents, namespace)
            
            cache.set(workspace.id , response_data) # store the result in redis store
            cache.expire_at(workspace.id , datetime.now() + timedelta(hours=12)) # presists for 12 hours until next task finishes
            
            print(f"Workspace - {workspace.id} - {workspace} added")
    
    print("Task Completed")


# checks if the namespace exist and if yes then overrites it.
def add_to_pinecone(documents, namespace):    
    try:
        if namespace in stats()['namespaces']:
            print('pinecone namespace added (create)')
            delete_vectores(namespace=namespace)
            add_to_pinecone_vectorestore_openai(documents=documents, namespace=namespace)
        else:
            print('pinecone namespace added (override)')
            add_to_pinecone_vectorestore_openai(documents=documents, namespace=namespace)
        
        return  Response({'detail':'xyz'})
    except Exception as e:
        print(f"Error adding to pinecone:" + str(e))
        return None
    

# this function collects all the marketing data and convert them as documents
def retrive_workspace_channel_data(workspace):
    response = requests.get(API_URL +  f"?workspace_id={workspace.id}")
    if response.status_code == 200:
        response_data = response.json()

    else:
        print("Failed to fetch data:", response.status_code)
        return response.raise_for_status()

    text_splitter= RecursiveJsonSplitter(max_chunk_size=128)
    documents = text_splitter.create_documents(texts=response_data)

    for i, document in enumerate(documents):
        
        if 'channel' in document.page_content:
            document.metadata['channel'] = json.loads(document.page_content)['channel']

        else:
            document.metadata['channel'] = documents[i-1].metadata['channel']

    return documents, response_data