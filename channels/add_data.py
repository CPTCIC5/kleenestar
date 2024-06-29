from langchain_text_splitters import RecursiveJsonSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
import requests
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes,api_view
from rest_framework.response import Response

from dotenv import load_dotenv
import os

load_dotenv()


API_URL = "http://127.0.0.1:8000/api/channels/xyz/"

# Function to fetch workspace data
def get_workspace():
    response = requests.get(API_URL)
    if response.status_code == 200:
        response_data = response.json()

    else:
        print("Failed to fetch data:", response.status_code)
        return response.raise_for_status()

 
    text_splitter= RecursiveJsonSplitter(max_chunk_size=80)
    documents = text_splitter.create_documents(texts=response_data)

    for i, document in enumerate(documents):
        
        if 'channel' in document.page_content:
            document.metadata['channel'] = json.loads(document.page_content)['channel']

        else:
            document.metadata['channel'] = documents[i-1].metadata['channel']

    return documents


def stats():
    pc= Pinecone(api_key=os.environ['PINECONE_API_KEY'])
    index= pc.Index("kleenestar")
    return index.describe_index_stats()

def delete_vectores(namespace):
    pc= Pinecone(api_key=os.environ['PINECONE_API_KEY'])
    index= pc.Index("kleenestar")
    index.delete(delete_all=True, namespace=namespace)

def add_to_pinecone_vectorestore_openai(documents, namespace):
    embeddings= OpenAIEmbeddings(model='text-embedding-3-large')
    pinecone_vs = PineconeVectorStore.from_documents(embedding=embeddings, index_name='kleenestar', namespace=namespace, documents=documents)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_channels(request):
    namespace = request.user.workspace_set.first().pinecone_namespace
    print(namespace)
    documents= get_workspace()
    if namespace in stats()['namespaces']:
        print('block-1')
        delete_vectores(namespace=namespace)
        add_to_pinecone_vectorestore_openai(documents=documents, namespace=namespace)
    else:
        print('block-2')
        add_to_pinecone_vectorestore_openai(documents=documents, namespace=namespace)
    
    pc= Pinecone(api_key=os.environ['PINECONE_API_KEY'])
    index= pc.Index("kleenestar")

    return  Response({'detail':'xyz'})