from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.core.validators import validate_image_file_extension

from .managers import CustomUserManager

from random import randint


class User(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        is_created = self._state.adding

        super().save(*args, **kwargs)

        if is_created:
            Profile.objects.create(user=self)


"""
POSITIONS = (
    ("Developer", "Developer"),
    ("Manager", "Manager"),
    ("Designer", "Designer"),
    # Add more positions as needed
)
"""


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to="avatars/",
        default="default.jpeg",
        null=True,
        blank=True,
        validators=[validate_image_file_extension],
    )
    # role = models.CharField(max_length=50, choices=POSITIONS, blank=True, null=True)
    country = models.CharField(
        choices=CountryField().choices, max_length=50, blank=True, null=True
    )
    phone_number = models.CharField(max_length=10, blank=True, null=True, unique=True)

    referral_code = models.CharField(max_length=6, unique=True, blank=True)
    total_referrals = models.IntegerField(default=0)

    def create_random(self):
        return "".join([str(randint(0, 9)) for _ in range(6)])

    def save(self, *args, **kwargs):
        if not self.referral_code:
            referal_codee = self.create_random()
            # print('ur reff is ',referal_codee)
            if Profile.objects.filter(referral_code=referal_codee).exists():
                while Profile.objects.filter(referral_code=referal_codee).exists():
                    referal_codee = self.create_random()
                    # print("new ref code",referal_codee)
                    self.referral_code = referal_codee
            self.referral_code = referal_codee
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user)


"""
AUDIENCE = (
    (1,"Beginner"),
    (2,"Intermediate"),
)
"""

FEEDBACK_CATEGORIES = (
    ("General", "General"),
    ("Technical", "Technical"),
    ("To improve", "To improve"),
    ("Feeback", "Feedback"),
    ("Others", "Others"),
)
URGENCYY = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
)

URGENCYY = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9))


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    urgency = models.IntegerField(choices=URGENCYY)
    category = models.CharField(max_length=30, choices=FEEDBACK_CATEGORIES)
    message = models.TextField()
    emoji = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.user.username
