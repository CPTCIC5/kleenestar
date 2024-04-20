from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from rest_framework import permissions, status, views, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import update_session_auth_hash

from workspaces.models import WorkSpaceInvite
from . import models, serializers
from .permissions import UserViewSetPermissions


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        login_serializer = serializers.LoginSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)

        user = authenticate(request, **login_serializer.data)

        if user is None:
            return Response(
                {"detail": "Account does not exist"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        if not user.is_active:
            return Response(
                {"detail": "Account disabled"}, status=status.HTTP_401_UNAUTHORIZED
            )

        login(request, user)

        return Response(status=status.HTTP_200_OK)


class SignupView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        if serializer.validated_data.get("invite_code"):
            print('here?')
            try:
                invite = WorkSpaceInvite.objects.get(
                    invite_code=serializer.validated_data["invite_code"]
                )

                # set the users subscription type to team member
                #user.subscription_type = 4
                #user.save()

                # add the user to the workspace
                invite.workspace.users.add(user)
            except WorkSpaceInvite.DoesNotExist:
                return Response(serializer.error,status=status.HTTP_404_NOT_FOUND)

        login(request, user,backend='django.contrib.auth.backends.ModelBackend')
        print('here!!')
        return Response(status=status.HTTP_201_CREATED)


class LogoutView(views.APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    permission_classes = (UserViewSetPermissions,)
    queryset = models.User.objects.all().select_related("profile")

    def list(self, request, *args, **kwargs):
        # dont list all users
        raise Http404

    @action(methods=("GET",), detail=False, url_path="me")
    def get_current_user_data(self, request):
        return Response(self.get_serializer(request.user).data)

class ChangePasswordView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self,request):
        serializer = serializers.ChangePasswordSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user = request.user
        if user.check_password(serializer.validated_data.get('current_password')):
            if serializer.validated_data.get('new_password') == serializer.validated_data.get('confirm_new_password'):
                user.set_password(serializer.validated_data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'message':'Password and Confirm Password didnt match'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)

class AddFeedback(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        serializer = serializers.FeedbackSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        print('xyz')
        serializer.save(user=request.user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)