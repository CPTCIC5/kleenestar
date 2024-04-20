from django.db import models
from workspaces.models import WorkSpace
from django.conf import settings
from dotenv import load_dotenv
from openai import OpenAI
from django.shortcuts import get_object_or_404

load_dotenv()

client = OpenAI()

#from channels.ai import generate_insights_with_gpt4

class APICredentials(models.Model):
    key_1 = models.CharField(max_length=255,unique=True)
    key_2 = models.CharField(max_length=255, null=True, blank=True,unique=True)
    key_3 = models.CharField(max_length=255, null=True, blank=True,unique=True)
    key_4 = models.CharField(max_length=255, null=True, blank=True,unique=True)

    def __str__(self):
        return self.key_1


class Channel(models.Model):
    CHANNEL_TYPES = (
        (1, "Google ads"),
        (2, "Meta"),
        (3, "X (Twitter)"),
        (4, "Linkedin"),
        (5, "TikTok")
    )
    activated = models.BooleanField(default=True)
    channel_type = models.IntegerField(choices=CHANNEL_TYPES)
    connected = models.BooleanField(default=True)
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    credentials = models.ForeignKey(APICredentials, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ["workspace", "channel_type"]

    def __str__(self):
        return "xyz"


class Convo(models.Model):
    assistant_id = models.CharField(max_length=100,blank=True,null=True)
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


def generate_insights_with_gpt4(user_query:str,convo:int,file=None):
    get_convo = get_object_or_404(Convo,id=convo)
    history = get_convo.prompt_set.all()
    all_prompts = history.count()

    # Creating a new conversation thread
    if all_prompts >= 1:
        thread = client.beta.threads.retrieve(
            thread_id=get_convo.assistant_id
        )

    else:
        thread = client.beta.threads.create()
        get_convo.assistant_id = thread.id
        get_convo.save()
        #convo.assistant_id = thread


    if file != None:
    # Posting user's query as a message in the thread
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_query,
            file_ids= [file]
        )
    else:
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_query
        )


    # Initiating a run
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id="asst_wljmLStVyrLtU7AyxcyXlU7d"
    )


    while run.status != "completed":
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(f"Run status: {keep_retrieving_run.status}")

        if keep_retrieving_run.status == "completed":
            break

    # Retrieve messages added by the Assistant to the thread
    all_messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
        
    # Print the messages from the user and the assistant
    return (all_messages.data[0].content[0])


    
class Prompt(models.Model):
    convo= models.ForeignKey(Convo,on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    text_query = models.TextField(max_length=10_000)
    file_query = models.FileField(upload_to='Prompts-File/', blank=True,null=True)
    
    response_text=  models.TextField(max_length=10_000,blank=True)  #GPT generated response
    response_image = models.ImageField(upload_to='Response-Image/',blank= True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    
    def save(self,*args,**kwargs):
        self.response_text= generate_insights_with_gpt4(self.text_query, self.convo.id, self.file_query).text.value
        if self.response_image:
            self.response_image = generate_insights_with_gpt4(self.text_query, self.convo.id, self.file_query).image_file
        super().save(*args,**kwargs)
    
    
    

    class Meta:
        ordering  = ['author','id']

    def __str__(self):
        return str(self.author)
    

class PromptFeedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prompt = models.ForeignKey(Prompt,on_delete=models.CASCADE)
    note = models.TextField()

    def __str__(self):
        return str(self.user)