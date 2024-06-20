from langchain_text_splitters import RecursiveJsonSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone.grpc import PineconeGRPC as Pinecone
import requests
import json



API_URL = "http://127.0.0.1:8000/api/channels/xyz/"

# Function to fetch workspace data
def get_workspace():
    response = requests.get(API_URL)
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

    return documents

def add_to_pinecone_vectorestore_openai(documents): 
    embeddings= OpenAIEmbeddings(model='text-embedding-3-large')
    pinecone_vs = PineconeVectorStore.from_documents(embedding=embeddings, index_name='kleenestar', documents=documents)

    return pinecone_vs 