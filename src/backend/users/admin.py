from django.contrib import admin
from .models import Profile,Feedback,Team
# Register your models here.

admin.site.register(Profile)
admin.site.register(Team)
admin.site.register(Feedback)