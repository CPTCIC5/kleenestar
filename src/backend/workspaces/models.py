from django.db import models, transaction
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone


INDUSTRIES = (
    ("E-commerce", "E-commerce"),
    ("Sales", "Sales"),
    ("Enterprise", "Enterprise"),
)


class WorkSpace(models.Model):
    SUBSCRIPTION_CHOICES = (
        (1, "Pro"),
        (2, "Scale"),
        (3, "Enterprise")
    )
    subscription_type = models.IntegerField(
        choices=SUBSCRIPTION_CHOICES, null=False, blank=False
    )

    root_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="work_space_root_user",
    )
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    business_name = models.CharField(max_length=80)
    website_url = models.URLField(unique=True)
    industry = models.CharField(
        max_length=60, choices=INDUSTRIES, blank=True, null=True
    )
    # audience_type = models.CharField(max_length=80,choices =AUDIENCE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name

    def save(self, *args, **kwargs) -> None:
        is_being_created = self._state.adding
        super().save(*args, **kwargs)

        if is_being_created:

            def add_member():
                # Add the root_user of the workspace as a member
                self.users.add(self.root_user)

            # https://stackoverflow.com/a/78053539/13953998
            transaction.on_commit(add_member)


def create_workspace_invite():
    return get_random_string(10)


class WorkSpaceInvite(models.Model):
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    invite_code = models.CharField(max_length=20, default=create_workspace_invite)
    email = models.EmailField(null=True, blank=True)
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
