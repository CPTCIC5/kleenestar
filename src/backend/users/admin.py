from django.contrib import admin
from .models import Profile,Feedback,WorkSpace,User
# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(WorkSpace)
admin.site.register(Feedback)