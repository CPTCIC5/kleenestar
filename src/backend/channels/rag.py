from dotenv import load_dotenv
import json, os, ast, requests
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

## Debugging imports
#nvm
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
    #workspace_data = get_workspace()
    workspace_data = ast.literal_eval(str(get_workspace()))
    workspace_data = json.dumps(workspace_data)
    embeddings_model = OpenAIEmbeddings()
    """
    splitter = RecursiveJsonSplitter(max_chunk_size=300)
    json_chunks = splitter.split_json(json_data=workspace_data)
    print(json_chunks,'efef')
    """
    dataToLoad = workspace_data
    data = json.loads(dataToLoad)
    embeddings = str(data) #embeddings_model.embed_documents(str(data))

    # embedded_query = embeddings.embed_query("What is the name of my workspace?")
    vectorstore = Chroma.from_texts(embeddings, embedding=OpenAIEmbeddings())
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=20, chunk_overlap=20)
    xd =text_splitter.split_text(str(data))#[:5]
    print(xd)
    

    
    retriever = vectorstore.as_retriever()
    # docs = retriever.get_relevant_documents("What is the name of my workspace?")
    docs = retriever.invoke("")
    #english is the only lang ik xD I suppose. This is polish fyi. From my complicated debugging method I realised that it stores everything as 1 char
    # i see , 1 char
    #complicated issue. for some1 who did this before probably not. For us? hell yeah true
    print(docs)

    
    # print(type(docs), "\n \n \n",str(docs))
if __name__ == "__main__":
    main()
