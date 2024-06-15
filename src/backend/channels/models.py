from django.db import models
from workspaces.models import WorkSpace
from django.conf import settings
from dotenv import load_dotenv
from openai import OpenAI
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .rag import RagData
import re


from openai.types.beta.threads.text_content_block import TextContentBlock
from openai.types.beta.threads.image_url_content_block import ImageURLContentBlock
from openai.types.beta.threads.image_file_content_block import ImageFileContentBlock
#from .old_rag import RagData as RagData_2

load_dotenv()

client = OpenAI()

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
        (7, 'Shopify')
    )
    channel_type = models.IntegerField(choices=CHANNEL_TYPES)
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
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
                key_6=f"{self.workspace.business_name} - {self.channel_type}"
            )

            #if self.credentials.key_1 == "" and self.credentials.key_2 == "" and self.credentials.key_3 == "" and self.credentials.key_4 == "" and self.credentials.key_5 == "":
                #self.credentials.delete()
        super().save(*args, **kwargs)

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


    class Meta:
        unique_together = ["workspace", "channel_type"]

    def __str__(self):
        return 'xyz'

COLOR_CHOICES = (
    ("9#0EE90","#90EE90"),
    ("#FFCCCC","#FFCCCC"),
    ("#D3D3D3","#D3D3D3"),
    ("#E6E6FA","#E6E6FA"),
    ("#ADD8E6","#ADD8E6")
)


class Note(models.Model):
    prompt = models.ForeignKey("Prompt",on_delete= models.CASCADE)
    blocknote = models.ForeignKey("BlockNote", on_delete=models.CASCADE)
    note_text= models.CharField(max_length=100)
    created_at= models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=30, choices=COLOR_CHOICES, default="#ADD8E6")

    def __str__(self):
        return str(self.blocknote)


class BlockNote(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    workspace= models.ForeignKey(WorkSpace, on_delete=models.CASCADE, null=True, blank=True)
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
    thread_id = models.CharField(max_length=100,blank=True,null=True)
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,default= 'New Chat')
    archived =  models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
    


def generate_insights_with_gpt4(user_query: str, convo: int, file=None):
    get_convo = get_object_or_404(Convo, id=convo)
    history = get_convo.prompt_set.all()
    all_prompts = history.count()

    

    # Call RagData function with the user query to get RAG context
    rag_context = RagData(user_query)
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
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=get_convo.workspace.assistant_id,
        stream=True
    )

    for event in run:
        # wait until the run is completed
        if event.event == "thread.message.completed":
            break

    # Retrieve messages added by the Assistant to the thread
    all_messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    # Return the content of the first message added by the Assistant
    assistant_response= all_messages.data[0].content[0]
    print(assistant_response)

    if type(assistant_response) == TextContentBlock:
        print('block-1')
        return {'text': assistant_response.text.value}
    elif  type(assistant_response) == ImageFileContentBlock:
        print('block-2')
        if 'text' in assistant_response.type:
            return {'text': assistant_response.text.value, 'image': assistant_response.image_file}
        else:
            return {'image': assistant_response.image_file.file_id}
    
    elif  type(assistant_response) == ImageURLContentBlock:
        print('block-3')
        print(assistant_response.image_url_content_block)
        return {'image': assistant_response.image_file.image_url_content_block}

def retrieve_file_content(file_id):
    return client.files.content(file_id)

    
class Prompt(models.Model):
    convo= models.ForeignKey(Convo,on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    text_query = models.TextField(max_length=10_000)
    file_query = models.FileField(upload_to='Prompts-File/', blank=True,null=True)
    
    response_text=  models.TextField(max_length=10_000,blank=True, null=True)  #GPT generated response
    response_image = models.ImageField(upload_to='Response-Image/',blank= True, null=True) # gpt generated image
    #blocknote = models.ForeignKey(BlockNote,on_delete=models.CASCADE,blank=True,null=True)
    #blocknote = models.ManyToManyField(BlockNote,null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    chart_data = models.JSONField(blank=True, null=True)
    table_data= models.JSONField(null=True, blank=True)


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
        response_data = generate_insights_with_gpt4(self.text_query, self.convo.id, self.file_query or None)
        self.response_text = response_data.get('text', None)
        self.response_image = response_data.get('image', None)

        super().save()
    
    """
    def save(self, *args, **kwargs):
        response_data = generate_insights_with_gpt4(self.text_query, self.convo.id, self.file_query)
        raw_response_text = response_data.get('text')

        # Extract table data from response text
        table_pattern = re.compile(r'(\|.*?\|(?:\n\|.*?\|)+)')  # Adjust the regex as per your table format
        
        tables = table_pattern.findall(raw_response_text)
        print(tables)

        # Convert tables to JSON-compatible format
        json_tables = []
        for table in tables:
            rows = table.strip().split('\n')
            headers = [header.strip() for header in rows[0].strip('|').split('|')]
            json_table = []
            for row in rows[1:]:
                values = [value.strip() for value in row.strip('|').split('|')]
                json_table.append(dict(zip(headers, values)))
            json_tables.append(json_table)
        
        # Remove table data from response text
        text_without_tables = table_pattern.sub('', raw_response_text).strip()
        
        self.response_text = text_without_tables
        self.table_data = json_tables
        self.response_image = response_data.get('image', None)
        
        super().save(*args, **kwargs)
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
    

class KnowledgeBase(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    workspace= models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    file=  models.FileField(upload_to='Knowledge-Base')
    title= models.CharField(max_length=80)
    created_at=  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering= ['workspace','user','-created_at']
        verbose_name_plural = 'KnowledgeBase'
