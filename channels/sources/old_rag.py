import json, requests
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document



# FOR SAVED SNIPPET IN MULTILINE COMMENT
# from langchain import hub
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough
# from langchain_openai import OpenAI 
# import sys
# from langchain.text_splitter import CharacterTextSplitter







API_URL ="http://127.0.0.1:8000/api/channels/xyz/"

def get_workspace():
    
    response = requests.get(API_URL)
    if response.status_code == 200:
        ResponseData = response.json()
    else:
        print("Failed to fetch data:", response.status_code)
        return None

    # text_splitter = CharacterTextSplitter(chunk_size=25, chunk_overlap=15)
    # ORIGINAL PART HERE, Pasting from main()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=128, chunk_overlap=30, length_function=len, is_separator_regex=False)
    ResponseData = [Document(page_content=x) for x in text_splitter.split_text(str(ResponseData))]
    return ResponseData



def RagData(question): 
    embeddings_model = OpenAIEmbeddings()
    data = get_workspace()
    db = Chroma(embedding_function=embeddings_model)
    db.add_documents(data)
    result = db.similarity_search_with_score(question, k=5)

    def format_docs(result):
        return "\n\n---\n\n".join([doc.page_content for doc,_score in result])
    

    RaggedData = format_docs(result)
    return str(RaggedData).replace("\n", "")
    
    #DATA-FLOW: API -> DATA SEGMENTATION -> EMBEDDINGS -> ADD TO DB -> SIMILARITY SEARCH -> FORMAT DATA -> RETURN DATA
    
    
    
    
    
    ''' THIS SNIPPET IS BEING SAVED JUST IN CASE | IN-FILE LLM INTEGRATION 
    prompt = hub.pull("rlm/rag-prompt")
    example_messages = prompt.invoke({"context": "filler context", "question": "filler question"}).to_messages()
    retriever = db.as_retriever()

    llm = OpenAI()

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt | llm | StrOutputParser())
    os.system("clear")

    system_answer = rag_chain.invoke(question)
    print(question, "\n", system_answer)
    return str(system_answer)'''
    
if __name__ != "__main__":
    pass
