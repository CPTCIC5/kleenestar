from django.db import models
from workspaces.models import WorkSpace,SubSpace
from django.conf import settings
from dotenv import load_dotenv
from openai import OpenAI
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .rag import RagData
import re
from django.core.files.base import ContentFile
import uuid
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

#from langsmith import traceable
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from openai.types.beta.threads.text_content_block import TextContentBlock
from openai.types.beta.threads.image_url_content_block import ImageURLContentBlock
from openai.types.beta.threads.image_file_content_block import ImageFileContentBlock
from typing_extensions import override
from openai import AssistantEventHandler
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http.response import StreamingHttpResponse
#from .old_rag import RagData as RagData_2

load_dotenv()

client = OpenAI()
channel_layer = get_channel_layer()

class EventHandler(AssistantEventHandler):

  def __init__(self, *, user, thread):
    self.user = user
    self.thread = thread
    super().__init__()

  @override
  def on_text_created(self, text) -> None:
    print("STARTED.....")
    print(f"\nassistant > ", end="", flush=True)
      
  @override
  def on_text_delta(self, delta, snapshot):
    print("received.....")
    print("CHANNEL NAME", self.user.ws_channel_name)
    print(delta.value, end="", flush=True)
    self.user.refresh_from_db()
    if self.user.ws_channel_name:
      async_to_sync(channel_layer.send)(self.user.ws_channel_name, {"type": "prompt_text_receive", "data": {"text": delta.value}})
      
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

    def on_end(self):
      # Retrieve messages added by the Assistant to the thread
      all_messages = client.beta.threads.messages.list(
        thread_id=self.thread.id
      )

      # Return the content of the first message added by the Assistant
      assistant_response= all_messages.data[0].content[0]
    
      if type(assistant_response) == TextContentBlock:
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
        # return {'image': assistant_response.image_file.image_url_content_block}
      

#from channels.ai import generate_insights_with_gpt4

class APICredentials(models.Model):
    key_1 = models.CharField(max_length=255,null=True, blank=True)
    key_2 = models.CharField(max_length=255, null=True, blank=True)
    key_3 = models.CharField(max_length=255, null=True, blank=True)
    key_4 = models.CharField(max_length=255, null=True, blank=True)
    key_5 = models.CharField(max_length=255,blank=True,null = True)
    key_6=models.CharField(max_length=255,blank=True,null = True)

    def __str__(self):
        return "xyz"
    

class Channel(models.Model):
    # refresh token
    # client id
    CHANNEL_TYPES = (
        (1, "Google ads"),
        (2, "Meta"),
        (3, "X (Twitter)"),
        (4, "Linkedin"),
        (5, "TikTok"),
        (6, 'Reddit'),
        (7, 'Shopify'),
        (8, 'Google-Analytics'),
        (9, 'MailChimp'),
        (10, 'Instagram'),
        (11, 'Bing')
    )
    channel_type = models.IntegerField(choices=CHANNEL_TYPES)
    subspace = models.ForeignKey(SubSpace, on_delete=models.CASCADE)
    credentials = models.ForeignKey(APICredentials, on_delete=models.CASCADE,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.credentials:
            self.credentials= APICredentials.objects.create(
                key_1="",
                key_2="",
                key_3="",
                key_4="",
                key_5="",
                key_6=f"{self.subspace.workspace.business_name} - {self.channel_type}"
            )

            #if self.credentials.key_1 == "" and self.credentials.key_2 == "" and self.credentials.key_3 == "" and self.credentials.key_4 == "" and self.credentials.key_5 == "":
                #self.credentials.delete()
        super().save(*args, **kwargs)

        """
        # Check the subscription type of the workspace
        if self.workspace.subscription_type == 1:  # Pro
            # Check if the workspace already has 3 channels
            if Channel.objects.filter(workspace=self.workspace).count() > 3:
                raise ValidationError("Pro workspace can have only up to 3 channels.")

        elif self.workspace.subscription_type == 2:  # Scale
            # Check if the workspace already has 5 channels
            if Channel.objects.filter(workspace=self.workspace).count() > 5:
                raise ValidationError("Scale workspace can have only up to 5 channels.")
        # Call the superclass save method if no validation error is raised
        super().save(*args, **kwargs)
        """


    class Meta:
        unique_together = ["subspace", "channel_type"]

    def __str__(self):
        return 'xyz'

COLOR_CHOICES = (
    ("#90EE90","#90EE90"),
    ("#FFCCCC","#FFCCCC"),
    ("#D3D3D3","#D3D3D3"),
    ("#E6E6FA","#E6E6FA"),
    ("#ADD8E6","#ADD8E6")
)


class Note(models.Model):
    prompt = models.ForeignKey("Prompt",on_delete= models.CASCADE)
    blocknote = models.ForeignKey("BlockNote", on_delete=models.CASCADE)
    note_text= models.CharField(max_length=500)
    color = models.CharField(max_length=30, choices=COLOR_CHOICES, default="#ADD8E6")
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.blocknote)


class BlockNote(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    subspace= models.ForeignKey(SubSpace, on_delete=models.CASCADE)
    title=  models.CharField(max_length=50)
    image= models.CharField(max_length=500,blank=True)
    created_at =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
"""

class Folder(models.Model):
    text=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
"""

class Convo(models.Model):
    #folder= models.ForeignKey(Folder, on_delete=models.PROTECT, blank=True, null=True)
    thread_id= models.CharField(max_length=100,blank=True,null=True)
    subspace= models.ForeignKey(SubSpace, on_delete=models.CASCADE)
    title= models.CharField(max_length=100,default= 'New Chat')
    archived=  models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
    
    @property
    def all_notes(self):
        # Fetch all Prompts related to the Convo
        prompts = self.prompt_set.all()
        # Fetch all Notes related to the Prompts
        notes = Note.objects.filter(prompt__in=prompts)
        return notes
    
#@traceable(name="insights")
def generate_insights_with_gpt4(user_query: str, convo: int, namespace, file=None, *, user):
    get_convo = get_object_or_404(Convo, id=convo)
    history = get_convo.prompt_set.all()
    all_prompts = history.count()
    all_notes= get_convo.all_notes

    

    # Call RagData function with the user query to get RAG context
    rag_context = RagData(user_query, namespace) #we need to pass namespaces into this function how can we do it?
    print('this-is-rag-contextttt',rag_context)



    # Creating a new conversation thread
    if all_prompts >= 2: #system prompt counts as a prompt 
        thread = client.beta.threads.retrieve(
            thread_id=get_convo.thread_id
        )
        knowledge_base=get_convo.subspace.knowledgebase.knowledge_source.all()
        for knowledge in knowledge_base:
            
            if knowledge.created_at > get_convo.created_at:
                knowledge_message = client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="assistant",
                    content=knowledge.text_data,
                    metadata={'mesasage_type': 'this is for knowledgebase'}
                )
            else:
                continue
    else:
        thread = client.beta.threads.create()
        get_convo.thread_id = thread.id
        get_convo.save()
        #convo.assistant_id = thread
        knowledge_base=get_convo.subspace.knowledgebase.knowledge_source.all()
        for knowledge in knowledge_base:
            knowledge_message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="assistant",
                content=knowledge.text_data,
                metadata={'mesasage_type': 'this is for knowledgebase'}
            )
        

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
            content=context.page_content,
            metadata={'mesasage_type': 'this is rag input'}
        )

    # Initiating a run
    '''run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=get_convo.workspace.assistant_id,
        stream=True
    )

    for event in run:
        # wait until the run is completed
        if event.event == "thread.message.completed":
            break'''

    event_handler = EventHandler(user = user, thread=thread)

    print("FINALLY")
    with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=get_convo.subspace.workspace.assistant_id,
    event_handler=event_handler,
    ) as stream:
        stream.until_done()


def followup_questions(query, output, assist_id, *, user):

    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"this is the query: {query} this is the output: {output} plesase create 3 follow up questions and say 'those are the follow up questions'")

    event_handler = EventHandler(user = user, thread=thread)
    with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assist_id,
    event_handler=event_handler,
    ) as stream:
        stream.until_done()

    all_messages = client.beta.threads.messages.list(
        thread_id=thread.id
        )
    assistant_response= all_messages.data[0].content[0]
    
    return {'questions': assistant_response.text.value}

class Prompt(models.Model):
    convo= models.ForeignKey(Convo,on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    text_query = models.TextField(max_length=10_000)
    file_query = models.FileField(upload_to='Prompts-File/', blank=True,null=True)
    
    response_text=  models.TextField(max_length=10_000,blank=True, null=True)  #GPT generated response
    response_file = models.FileField(upload_to='Response-File/',blank= True, null= True) # gpt generated file
    #blocknote = models.ForeignKey(BlockNote,on_delete=models.CASCADE,blank=True,null=True)
    #blocknote = models.ManyToManyField(BlockNote,null=True, blank=True)
    similar_questions= models.TextField(max_length=10_000,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    """
    def save(self,*args,**kwargs):

        history_counts= self.convo.prompt_set.all().count()
        if history_counts >= 1:
            thread= client.beta.threads.retrieve(
                thread_id=self.convo.thread_id
            )

        else:
            thread = client.beta.threads.create()
            self.convo.thread_id = thread.id
            self.convo.save()


        super().save(*args, **kwargs)

        # error is coming from here
        print('namespace',self.convo.subspace.pinecone_namespace)
        response_data = generate_insights_with_gpt4(user_query=self.text_query, 
                                                    convo=self.convo.id, 
                                                    file=self.file_query or None, 
                                                    namespace= self.convo.subspace.pinecone_namespace
                                                    )
        self.response_text = response_data.get('text', None)
        self.response_file = response_data.get('image', None)
        x1=followup_questions(self.text_query,self.response_text, assist_id=self.convo.subspace.workspace.assistant_id)
        self.similar_questions= x1['questions']

        super().save()
        """
    
    
    class Meta:
        ordering  = ['author','id']

    def __str__(self):
        return str(self.convo)


CATEGORY  = (
        (1, "Don't like the style"),
        (2, "Not factually correct"),
        (3, "Being Lazy"),
        (4, "Other")
    )
class PromptFeedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prompt = models.ForeignKey(Prompt,on_delete=models.CASCADE)
    category = models.IntegerField(choices=CATEGORY)
    note = models.TextField()

    def __str__(self):
        return str(self.user)
    

class KnowledgeSource(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text_data=models.TextField(blank=False,null=False)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text_data
    


class KnowledgeBase(models.Model):
    subspace= models.OneToOneField(SubSpace, on_delete=models.CASCADE)
    knowledge_source= models.ManyToManyField(KnowledgeSource,null=True,blank=True)
    created_at=  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.subspace)
    
    class Meta:
        ordering= ['subspace' , '-created_at']
        verbose_name_plural = 'KnowledgeBase'

    @receiver(post_save, sender=SubSpace)
    def create_knowledgebase(sender, instance, created, **kwargs):
        if created:
            KnowledgeBase.objects.create(subspace=instance)