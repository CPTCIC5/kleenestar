import requests
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import JSONLoader
from langchain_text_splitters import RecursiveJsonSplitter
import json

load_dotenv()

API_URL = "http://127.0.0.1:8000/api/workspaces/"

def get_workspace():
    response = requests.get(API_URL, auth=("aryanjainak@gmail.com","Iamreal@123"))
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data:", response.status_code)
        return None

def main():
    workspace_data = get_workspace()
    embeddings_model = OpenAIEmbeddings()
    """
    splitter = RecursiveJsonSplitter(max_chunk_size=300)
    json_chunks = splitter.split_json(json_data=workspace_data)
    print(json_chunks,'efef')
    
    loader = JSONLoader(
    file_path=workspace_data,
    jq_schema='.messages[].content',
    )
    data = loader.load()
    """
    embeddings = embeddings_model.embed_documents(str(workspace_data))
    vectorstore = Chroma.from_documents(embeddings, embedding=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()
    docs = retriever.get_relevant_documents("What is the name of my workspace?")



if __name__ == "__main__":
    main()
