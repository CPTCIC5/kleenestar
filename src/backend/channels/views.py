from django.shortcuts import get_object_or_404
from rest_framework import views, permissions, status
from rest_framework.response import Response
from . import models, serializers

class PromptFeedbackView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = serializers.PromptFeedbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ChannelView(views.APIView):
    
    def get(self,request,pk,format=None):
        serializer = serializers.ChannelSerializer(many=False,pk=pk)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.ChannelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(workspace=request.user.workspace)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        channel = get_object_or_404(models.Channel, pk=pk)
        serializer = serializers.ChannelSerializer(instance=channel, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(workspace=request.user.workspace)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        channel = get_object_or_404(models.Channel, pk=pk)
        channel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)