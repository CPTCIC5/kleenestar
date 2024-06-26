from django.contrib import admin
from . import models


admin.site.register(models.WorkSpace)
admin.site.register(models.WorkSpaceInvite)
admin.site.register(models.SubSpace)