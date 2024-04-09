from django.db import models
from workspaces.models import WorkSpace
from django.conf import settings


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
    credential = models.ForeignKey(APICredentials, on_delete=models.CASCADE)


    class Meta:
        unique_together = ["workspace", "channel_type"]

    def __str__(self):
        return "xyz"


class Convo(models.Model):
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
    
class Prompt(models.Model):
    convo= models.ForeignKey(Convo,on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    text_query = models.TextField(max_length=10_000)
    image_query = models.ImageField(upload_to='Prompts-Query/', blank=True,null=True)

    refactored_text = models.TextField(max_length=20_000,blank=True) #gpt4 refactored text
    
    response_text=  models.TextField(max_length=10_000,blank=True)  #GPT generated response
    response_image = models.ImageField(upload_to='Response-Image/',blank= True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    """
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
    """

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