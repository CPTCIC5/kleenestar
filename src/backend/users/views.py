from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from rest_framework import permissions, status, views, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from django.shortcuts import get_object_or_404
from django.db.models import Q

from . import models, serializers


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
        login(request, user)
        return Response(status=status.HTTP_201_CREATED)


class LogoutView(views.APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
    
class ProfileView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        
        query = get_object_or_404(models.Profile,user=request.user)
        serializer = serializers.ProfileSerializer(query,many=False)

        return Response(serializer.data,status=status.HTTP_200_OK)

    """
    def post(self,request):

        serializer = serializers.ProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    """
    
    def patch(self,request):

        # Retrieve the user instance that needs to be updated.
        profile = get_object_or_404(models.Profile,user=request.user)
        # Create or update the user data.
        serializer = serializers.ProfileSerializer(instance=profile,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,status =status.HTTP_200_OK)
    
    def delete(self,request):

        profile = get_object_or_404(models.Profile,user=request.user)
        profile.user.delete()




class WorkSpaceSerializer(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):

        workspaces = models.WorkSpace.objects.filter(Q(root_user=request.user) | Q(users=request.user))
        serializer = serializers.WorkSpaceSerializer(workspaces,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


    def post(self,request):

        serializer =serializers.WorkSpaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #serializer.validated_data.get('')
        serializer.save()

        return Response(serializer.data,status=status.HTTP_201_CREATED)
        
    def patch(self,request):

        workspace = get_object_or_404(models.WorkSpace,root_user=request.user)
        serializer = serializers.WorkSpaceSerializer(instance=workspace,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,status=status.HTTP_200_OK)




class UserViewSetPermissions(IsAuthenticated):
    def has_object_permission(self, request, view, instance):
        if request.user.is_authenticated and request.method not in SAFE_METHODS:
            if instance.id != request.user.id and not request.user.is_staff:
                return False

        return super().has_object_permission(request, view, instance)


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
