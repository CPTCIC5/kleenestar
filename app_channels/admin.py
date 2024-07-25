from django.contrib import admin
from .models import Channel,PromptFeedback,APICredentials,Prompt,Convo,BlockNote,KnowledgeBase,Note,KnowledgeSource
# Register your models here.

admin.site.register(Channel)
admin.site.register(PromptFeedback)
admin.site.register(APICredentials)
admin.site.register(Convo)
admin.site.register(Prompt)

admin.site.register(Note)
admin.site.register(BlockNote)

admin.site.register(KnowledgeSource)
admin.site.register(KnowledgeBase)