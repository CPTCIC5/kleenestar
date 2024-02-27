from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.validators import validate_image_file_extension
from django.dispatch import receiver 
from django.db.models.signals import post_save
from random import randint


POSITIONS = (
    ('Developer', 'Developer'),
    ('Manager', 'Manager'),
    ('Designer', 'Designer'),
    # Add more positions as needed
)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10,blank=True,unique=True)
    avatar=models.ImageField(upload_to='avatars/',default='default.jpeg',validators=[validate_image_file_extension])
    position = models.CharField(max_length=50,choices=POSITIONS,blank=True)
    country = models.CharField(choices=CountryField().choices, max_length=50,blank=True)
    #referral_code = models.CharField(max_length=6,unique=True,blank=True)
    total_referrals = models.IntegerField(default=0)

    """
    def create_random(self):
        return ''.join([str(randint(0, 9)) for _ in range(6)])
    """

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

        
    """
    def save(self, *args, **kwargs):
        if not self.referral_code:
            referal_codee = self.create_random()
            #print('ur reff is ',referal_codee)
            if Profile.objects.filter(referral_code=referal_codee).exists():
                while Profile.objects.filter(referral_code=referal_codee).exists():
                    referal_codee = self.create_random()
                    #print("new ref code",referal_codee)
                    self.referral_code = referal_codee
            self.referral_code = referal_codee
        super().save(*args, **kwargs)
    """

    def  __str__(self):
        return str(self.user)
    

INDUSTRIES  = (
    ("E-commerce","E-commerce"),
    ("Sales", "Sales"),
    ("Enterprise","Enterprise")
 )   

AUDIENCE = (
    (1,"Beginner"),
    (2,"Intermediate"),
)

class WorkSpace(models.Model):
    profile = models.ManyToManyField()
    name = models.CharField(max_length=80)
    industry = models.CharField(max_length=60,choices=INDUSTRIES)
    budget = models.FloatField()
    audience_type = models.CharField(max_length=80,choices =AUDIENCE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    

FEEDBACK_CATEGORIES = (
    ("General","General"),
    ("Technical","Technical"),
    ("To improve", "To improve"),
    ("Feeback","Feedback"),
    ("Others","Others")
)

URGENCYY = (
    ("1","1"),
    ("2","2"),
    ("3","3"),
    ("4",'4'),
    ("5","5"),
    ("6","6"),
    ("7",'7'),
    ("8","8"),
    ("9","9"),
    ("10","10")
)

class Feedback(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    urgency=models.CharField(max_length=3,choices=URGENCYY)
    category=models.CharField(max_length=30,choices=FEEDBACK_CATEGORIES)
    message = models.TextField()
    attachment = models.ImageField()


    def __str__(self):
        return self.user.user.username