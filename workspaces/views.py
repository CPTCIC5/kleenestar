from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import create_workspace_invite
from django.core.mail import send_mail
import os
from .permissions import WorkSpaceViewSetPermissions

# from . import permissions
from rest_framework import permissions
from .serializers import WorkSpaceSerializer, WorkSpaceCreateSerializer,WorkSpaceInviteCreateSerializer,SubspaceSerializer,SubSpaceCreateSerializer


class WorkSpacesViewSet(viewsets.ModelViewSet):
    # permission_classes = (WorkSpaceViewSetPermissions,)
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = WorkSpaceSerializer

    def get_queryset(self):
        # All the workspaces the request user is a member of
        return self.request.user.workspace_set.all()
    #https://xyz.com
    
    

    def create(self, request, *args, **kwargs):
        serializer = WorkSpaceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(root_user=self.request.user)

        return Response(self.get_serializer(instance).data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = WorkSpaceCreateSerializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)

        new_instance = serializer.save()

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(self.get_serializer(new_instance).data)

    @action(methods=("POST",), detail=True, url_path="create-invite")
    def create_workspace_invite(self, request, pk):

        #workspace = self.get_object().id
        workspace = self.get_object()

        invite_code = create_workspace_invite()
        #email = request.data["email"]  # Assuming email is provided in request data
        
        """
        serializer = WorkSpaceInviteCreateSerializer(data= {
            "workspace": workspace,
            "invite_code": invite_code,
            "email": email
            })
        """

        serializer = WorkSpaceInviteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            workspace=workspace,
            invite_code=invite_code
            )
        print(os.environ['EMAIL_HOST_USER'])


        # Extract the email address from the validated data and send the email
        recipient_email = serializer.validated_data.get("email")
        print(recipient_email)

        #sending mail
        send_mail(
            'Subject here',
            f'Here is the message. Your code is {invite_code}',
            os.environ['EMAIL_HOST_USER'],  # Sender's email address
            [recipient_email],  # List of recipient email addresses as strings
        )
        
        return Response(serializer.data,status=status.HTTP_201_CREATED)
