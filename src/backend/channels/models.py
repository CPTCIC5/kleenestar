from django.db import models
from django.core.validators import validate_image_file_extension
from users.models import Profile,WorkSpace


# Create your models here.
class Credential(models.Model):
    api_code = models.CharField(max_length=4000)  # token api inputted via user

    def __str__(self):
        return self.api_code


class Channel(models.Model):
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    logo = models.ImageField(
        upload_to="Channel-Logo", validators=[validate_image_file_extension]
    )
    name = models.CharField(max_length=40)
    basic_info = models.CharField(max_length=150)
    desc = models.TextField()
    credential = models.ForeignKey(Credential, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

COMMONS = (
    ("Don't like the style","Don't like the style"),
    ("Being lazy","Being lazy"),
    ("Refused when it shouldn't have","Refused when it shouldn't have"),
    ("Not factually correct","Not factually correct"),
    ("Other","Other")

)

class PromptFeedback(models.Model):
    user= models.ForeignKey(Profile,on_delete=models.CASCADE)
    channel =  models.ForeignKey(Channel,on_delete=models.CASCADE)
    commons= models.CharField(max_length=50,choices=COMMONS)
    note = models.TextField()

    def __str__(self):
        return str(self.user)