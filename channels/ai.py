from dotenv import load_dotenv
from openai import OpenAI
from .models import Convo
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
import uuid
from .rag import RagData
from typing_extensions import override
from openai import AssistantEventHandler
from openai.types.beta.threads.text_content_block import TextContentBlock
from openai.types.beta.threads.image_url_content_block import ImageURLContentBlock
from openai.types.beta.threads.image_file_content_block import ImageFileContentBlock

load_dotenv()

client = OpenAI()

 
# First, we create a EventHandler class to define
# how we want to handle the events in the response stream.
 
class EventHandler(AssistantEventHandler):    
  @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)
      
  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)
      
  def on_tool_call_created(self, tool_call):
    print(f"\nassistant > {tool_call.type}\n", flush=True)
  
  def on_tool_call_delta(self, delta, snapshot):
    if delta.type == 'code_interpreter':
      if delta.code_interpreter.input:
        print(delta.code_interpreter.input, end="", flush=True)
      if delta.code_interpreter.outputs:
        print(f"\n\noutput >", flush=True)
        for output in delta.code_interpreter.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)

"""
def get_convo_prompts(convo:int):
    get_convo= get_object_or_404(Convo,id=convo)
    history = get_convo.prompt_set.all()
    return history
"""


"""
def get_history(convo_id:int):
    history = get_convo_prompts(convo_id)
    if history.count() >= 1:
        history_list = []
        for i in history:
            history_list.append(i.text_query)
        return str(history_list)
    else:
        return False
"""
def generate_insights_with_gpt4(user_query: str, convo: int, file=None):
    get_convo = get_object_or_404(Convo, id=convo)
    history = get_convo.prompt_set.all()
    all_prompts = history.count()

    

    # Call RagData function with the user query to get RAG context
    rag_context = RagData(user_query, 'KRmPlTxd9W')
    print('this-is-rag-contextttt',rag_context)



    # Creating a new conversation thread
    if all_prompts >= 1:
        thread = client.beta.threads.retrieve(
            thread_id=get_convo.thread_id
        )

    else:
        thread = client.beta.threads.create()
        get_convo.thread_id = thread.id
        get_convo.save()
        #convo.assistant_id = thread


        

    if file is not None:
        file.open()

        message_file = client.files.create(
          file=file.file.file, purpose="assistants"
        )
        file.close()

        message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_query,
                attachments=[
            {
                "file_id": message_file.id,
                "tools": [{"type": "file_search"}, {"type":"code_interpreter"} ]
            }
        ]
        )
        
    else:
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_query
        )

    # Posting RAG context as a message in the thread for the Assistant
    for context in rag_context:
        rag_message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="assistant",
            content=context.page_content
        )

    # Initiating a run

    with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=get_convo.subspace.workspace.assistant_id,
    event_handler=EventHandler(),
    ) as stream:
        stream.until_done()

    all_messages = client.beta.threads.messages.list(
        thread_id=thread.id
        )
    assistant_response= all_messages.data[0].content[0]
    # Return the content of the first message added by the Assistant
    return {'text': assistant_response.text.value}


    '''if type(assistant_response) == TextContentBlock:
        print('block-1')
        return {'text': assistant_response.text.value}
    elif  type(assistant_response) == ImageFileContentBlock:
        print('block-2')
        file_content = client.files.content(assistant_response.image_file.file_id).content
        image_file = ContentFile(file_content, name=f"{uuid.uuid4()}.png")
        if 'text' in assistant_response.type:
            return {'text': assistant_response.text.value, 'image': image_file}
        else:
            return {'image': image_file}
    
    elif  type(assistant_response) == ImageURLContentBlock:
        raise Exception("received ImageURLContentBlock, unable to process this...")
        # print('block-3')
        # print(assistant_response.image_url_content_block)
        # return {'image': assistant_response.image_file.image_url_content_block}'''


def followup_questions(query, output):

    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"this is the query: {query} this is the output: {output} plesase create 3 follow up questions and say 'this is the follow up questions'")

    with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id="asst_Tr8r4a1O8QnZFNZshEIpqZGf",
    event_handler=EventHandler(),
    ) as stream:
        stream.until_done()
    all_messages = client.beta.threads.messages.list(
        thread_id=thread.id
        )
    assistant_response= all_messages.data[0].content[0]
    
    return {'questions': assistant_response.text.value}
if __name__ == '__main__':
    output= generate_insights_with_gpt4('how does my marketing data look like accross all channels', convo=1)['text']
    followup_questions(query='how does my marketing data look like accross all channels', output=output)