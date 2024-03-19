from django.db import models
from django.core.validators import validate_image_file_extension
from users.models import Profile, WorkSpace
from django.conf import settings


class APICredentials(models.Model):
    key_1 = models.CharField(max_length=255)
    key_2 = models.CharField(max_length=255, null=True, blank=True)
    key_3 = models.CharField(max_length=255, null=True, blank=True)
    key_4 = models.CharField(max_length=255, null=True, blank=True)


class Channel(models.Model):
    CHANNEL_TYPES = (
        (1, "Google ads"),
        (2, "Meta"),
        (3, "X (Twitter)"),
        (4, "Linkedin"),
    )
    type = models.IntegerField(choices=CHANNEL_TYPES)
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    credential = models.ForeignKey(APICredentials, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PromptFeedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    note = models.TextField()

    def __str__(self):
        return str(self.user)
