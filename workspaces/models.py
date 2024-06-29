from django.db import models, transaction
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.utils import timezone
from openai import OpenAI
from django_countries.fields import CountryField

client = OpenAI()

INSTRUCTIONS = """
You are a helpful assistant specializing in branding and marketing optimization insights and recommendations.
Your role is to analyze users' connected marketing channels in real-time, based on their queries, conversation context, 
and market knowledge, to provide accurate and actionable answers. 
Users' queries can be in different formats:

Image Query: Requires image analysis, database analysis, and market knowledge.
Text Query: Requires database analysis and market knowledge.
Text Query with Chart Output: Requires generating a chart, table, or graph, accompanied by insights or recommendations.
Instructions:

Clarification: Before answering user queries, ask clarification questions if needed to ensure you fully understand the user's needs.
Channel Connection: If a user query requests analysis from a non-connected channel, politely prompt the user to connect the necessary channel for analysis.
By following these guidelines, provide precise, insightful, and actionable marketing optimization advice.
"""


INDUSTRIES = (
    ("⁠Retail", "⁠Retail"),
    ("⁠Hospitality", "⁠Hospitality"),
    ("⁠Media", "⁠Media"),
    ("⁠Technology", "⁠Technology"),
    ("⁠Finance", "⁠Finance"),
    ("⁠Sport", "⁠Sport"),
    ("⁠Beauty", "⁠Beauty"),
    ("⁠Automotive", "⁠Automotive")
)

def create_namespace_id():
    return get_random_string(10)



class WorkSpace(models.Model):
    SUBSCRIPTION_CHOICES = (
        (1, "Pro"),
        (2, "Scale"),
        (3, "Enterprise")
    )
    subscription_type = models.IntegerField(
        choices=SUBSCRIPTION_CHOICES, null=True, blank=True
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
    assistant_id = models.CharField(max_length=40,blank=True)
    pinecone_namespace= models.CharField(max_length=50, default=create_namespace_id)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        self.website_url= self.website_url.lower()

    @property
    def monthly_bill(self):
        total_count = self.users.all().count()

        if self.subscription_type == 1:  # Pro
            base_cost = 69
            user_limit = 6
            extra_user_rate = 20
            if total_count > user_limit:
                extra_users = total_count - user_limit
                return base_cost + (extra_users * extra_user_rate)
            else:
                return base_cost

        elif self.subscription_type == 2:  # Scale
            base_cost = 169
            user_limit = 11
            extra_user_rate = 15
            if total_count > user_limit:
                extra_users = total_count - user_limit
                return base_cost + (extra_users * extra_user_rate)
            else:
                return base_cost

        elif self.subscription_type == 3:  # Enterprise
            return 800
        
        else:
            return 0


    def __str__(self):
        return self.business_name

    def save(self, *args, **kwargs) -> None:
        is_being_created = self._state.adding
        self.clean()
        super().save(*args, **kwargs)

        if is_being_created:
            assistant = client.beta.assistants.create(
                name=self.business_name,
                instructions=INSTRUCTIONS,
                tools=[{"type": "code_interpreter"}, {"type": "file_search"}],
                model="gpt-4o",
            )
            self.assistant_id = assistant.id
            self.save(update_fields=['assistant_id'])
        

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
    email = models.EmailField(null=False, blank=False)
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    """
    def save(self, *args, **kwargs):
        if self.workspace.subscription_type == 1:
            # Check if inviting more than 5 members
            if self.workspace.users.count() >= 6:
                raise ValidationError("Pro workspace can only invite up to 5 members.")

        # Check if workspace's subscription type is Scale (2)
        elif self.workspace.subscription_type == 2:
            # Check if inviting more than 10 members
            if self.workspace.users.count() >= 11:
                raise ValidationError("Scale workspace can only invite up to 10 members.")
            
        # Call the superclass save method if no validation error is raised
        super().save(*args, **kwargs)
    """


    def __str__(self):
        return str(self.workspace)

class SubSpace(models.Model):
    workspace= models.ForeignKey(WorkSpace,on_delete=models.CASCADE)
    name= models.CharField(max_length=100)
    country= models.CharField(choices=CountryField().choices, max_length=50)
    industry= models.CharField(max_length=80, choices=INDUSTRIES)
    pinecone_namespace= models.CharField(max_length=11,default=create_namespace_id)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" {str(self.workspace)}-  {self.name}"
    
    class Meta:
        ordering=['workspace','id']