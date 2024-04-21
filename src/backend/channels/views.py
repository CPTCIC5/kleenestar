from django.shortcuts import get_object_or_404
from rest_framework import views,viewsets, permissions, status,pagination
from rest_framework.response import Response
from . import models, serializers
from workspaces.permissions import WorkSpaceViewSetPermissions

class CustomPagination(pagination.PageNumberPagination):
    page_size = 10



class ChannelViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Channel.objects.all()
    serializer_class = serializers.ChannelSerializer

    def get_queryset(self):
        # Customize queryset based on the request or user
        user = self.request.user
        return models.Channel.objects.filter(workspace=user.workspace_set.all()[0])
    

    def create(self, request, *args, **kwargs):
        serializer = serializers.ChannelCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(workspace=request.user.workspace_set.all()[0])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = serializers.ChannelCreateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.activated = False
        instance.save()
        #self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
    

class ConvoViewSet(viewsets.ModelViewSet):
    queryset = models.Convo.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ConvoSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        workspace = self.request.user_workspace.set.all()[0]
        return models.Convo.objects.filter(workspace=workspace)
    

    def create(self, request, *args, **kwargs):
        serializer = serializers.ConvoCreateSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(workspace=self.request.user_workspace.set.all()[0])
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = serializers.ConvoCreateSerializer(
            instance=instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy()
        return Response(status=status.HTTP_200_OK)

        

class PromptViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated)
    queryset = models.Prompt.objects.all()
    serializer_class = serializers.PromptInputSerializer
    pagination_class = CustomPagination

class PromptFeedbackView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = serializers.PromptFeedbackCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)