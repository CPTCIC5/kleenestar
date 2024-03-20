from django.shortcuts import get_object_or_404,get_list_or_404
from rest_framework import views,permissions,status
from rest_framework.response import Response
# Create your views here.

 
class PromptFeedbackView(views.APIView):
    permission_classes = permissions.IsAuthenticated()