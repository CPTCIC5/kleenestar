from dotenv import load_dotenv
import json, os, ast, requests, sys
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAI 



load_dotenv()


API_URL = "http://127.0.0.1:8000/api/workspaces/"

def get_workspace():
    from langchain.text_splitter import CharacterTextSplitter
    from langchain.schema.document import Document
    
    response = requests.get(API_URL, auth=("aryanjainak@gmail.com","Iamreal@123"))
    if response.status_code == 200:
        ResponseData = response.json()
        # return response.json()
    else:
        print("Failed to fetch data:", response.status_code)
        return None

    text_splitter = CharacterTextSplitter(chunk_size=25, chunk_overlap=15)
    docs = [Document(page_content=x) for x in text_splitter.split_text(str(ResponseData))]
    return docs









    # from langchain_community.document_loaders import TextLoader
    # loader = TextLoader("channels/test.json")
    # data = loader.load()
    # return data
    # with open("channels/test.json", "rb+") as f:
    #     xd = f.read()

    
    # data = loader.load()


def main():
    question = str(sys.argv[1]).strip()
    embeddings_model = OpenAIEmbeddings()
    data = get_workspace()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=80, chunk_overlap=30, length_function=len, is_separator_regex=False)
    data = text_splitter.split_documents(data)
    db = Chroma(embedding_function=embeddings_model)
    db.add_documents(data)
    result = db.similarity_search_with_score(question, k=5)
    def format_docs(docs):
        return "\n\n---\n\n".join([doc.page_content for doc,_score in result])
    prompt = hub.pull("rlm/rag-prompt")
    example_messages = prompt.invoke({"context": "filler context", "question": "filler question"}).to_messages()
    retriever = db.as_retriever()

    llm = OpenAI()

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt | llm | StrOutputParser()
    )
    os.system("clear")

    system_answer = rag_chain.invoke(question)
    print(question, "\n", system_answer)
    return str(system_answer)




    
    # splitter = RecursiveCharacterTextSplitter(separators=",")
    # json_chunks = splitter.split_text(workspace_data)
    # print(json_chunks, type(json_chunks))
    
    # data = json.loads(workspace_data)
    # embeddings = embeddings_model.embed_documents(workspace_data)

    # embedded_query = embeddings.embed_query("What is the name of my workspace?")
    
    # vectorstore = Chroma.from_texts(workspace_data, embedding=OpenAIEmbeddings())
    # retriever = vectorstore.as_retriever()

    # xd = vectorstore.similarity_search("workspace")
    # docs = retriever.invoke("What is my workspace called?")
    # print(docs, type(docs))
    
    # GOTTA FINISH THIS WHEN I WAKE UP, BECAUSE I AM ALREADY FURIOUS IT DOESN'T WORK

    # # docs = retriever.get_relevant_documents("What is the name of my workspace?")
    # docs = retriever.invoke("What is my workspace called?")
    # print(docs, type(docs))

    
if __name__ == "__main__":
    main()
    # get_workspace()
