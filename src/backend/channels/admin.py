from django.contrib import admin
from .models import Channel,PromptFeedback,APICredentials,Prompt
# Register your models here.

admin.site.register(Channel)
admin.site.register(PromptFeedback)
admin.site.register(APICredentials)
admin.site.register(Prompt)