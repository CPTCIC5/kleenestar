from django.db import models
from django.core.validators import validate_image_file_extension
from users.models import Team


# Create your models here.
class Credential(models.Model):
    api_code = models.CharField(max_length=4000)  # token api inputted via user

    def __str__(self):
        return self.api_code


class Channel(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    logo = models.ImageField(
        upload_to="Channel-Logo", validators=[validate_image_file_extension]
    )
    name = models.CharField(max_length=40)
    basic_info = models.CharField(max_length=150)
    desc = models.TextField()
    credential = models.ForeignKey(Credential, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
