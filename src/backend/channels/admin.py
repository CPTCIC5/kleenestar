from django.contrib import admin
from .models import Credential,Channel,PromptFeedback
# Register your models here.
admin.site.register(Credential)
admin.site.register(Channel)
admin.site.register(PromptFeedback)