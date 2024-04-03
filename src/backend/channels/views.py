from django.shortcuts import get_object_or_404
from rest_framework import views,viewsets, permissions, status,pagination
from rest_framework.response import Response
from . import models, serializers

class CustomPagination(pagination.PageNumberPagination):
    page_size = 10


class PromptFeedbackView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = serializers.PromptFeedbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ChannelViewSet(viewsets.ModelViewSet):
    queryset = models.Channel.objects.all()
    serializer_class = serializers.ChannelSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(workspace=request.user.workspace)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(workspace=request.user.workspace)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ConvoViewSet(viewsets.ModelViewSet):
    queryset = models.Convo.objects.all()
    serializer_class = serializers.ConvoSerializer
    pagination_class = CustomPagination

class PromptInputViewSet(viewsets.ModelViewSet):
    queryset = models.PromptInput.objects.all()
    serializer_class = serializers.PromptInputSerializer
    pagination_class = CustomPagination