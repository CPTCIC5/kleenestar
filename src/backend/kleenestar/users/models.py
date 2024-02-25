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


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10,blank=True,unique=True)
    avatar=models.ImageField(upload_to='avatars/',default='default.jpeg',validators=[validate_image_file_extension])
    position = models.CharField(max_length=50,choices=POSITIONS,blank=True)
    country = models.CharField(choices=CountryField().choices, max_length=50,blank=True)
    referral_code = models.CharField(max_length=6,unique=True,blank=True)
    total_referrals = models.IntegerField(default=0)

    def create_random(self):
        return ''.join([str(randint(0, 9)) for _ in range(6)])


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()



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

    def  __str__(self):
        return str(self.user)
    