from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status,pagination
from rest_framework.response import Response
from . import models, serializers
from rest_framework.decorators import action

class CustomPagination(pagination.PageNumberPagination):
    page_size = 10



class ChannelViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Channel.objects.all()
    serializer_class = serializers.ChannelSerializer

    def get_queryset(self):
        # Customize queryset based on the request or user
        user = self.request.user
        return models.Channel.objects.filter(subspace__workspace=user.workspace_set.all()[0])
    

    def create(self, request, *args, **kwargs):
        serializer = serializers.ChannelCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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
        #instance.activated = False
        #instance.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
    

class ConvoViewSet(viewsets.ModelViewSet):
    queryset = models.Convo.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ConvoSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        workspace = self.request.user.workspace_set.all()[0]
        return models.Convo.objects.filter(subspace__workspace=workspace)
    

    def create(self, request, *args, **kwargs):
        serializer = serializers.ConvoCreateSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
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
        instance = self.get_object()
        self.perform_destroy(instance)
        workspace = self.request.user.workspace_set.all()[0]

        if models.Convo.objects.filter(workspace=workspace).count() < 1:
            models.Convo.objects.create(
                workspace= workspace,
                
            )
            
        return Response(status=status.HTTP_200_OK)

        

class PromptViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Prompt.objects.all()
    serializer_class = serializers.PromptSerializer
    pagination_class = CustomPagination

    def get_queryset(self,*args,**kwargs):
        convo_id = self.kwargs.get('pk')  # Retrieve 'pk' from URL kwargs
        convo = get_object_or_404(models.Convo, id=convo_id)
        #n1=models.Prompt.objects.filter(convo=convo)
        #return models.Prompt.objects.filter(convo=convo)
        #print(convo.prompt_set.all())
        return convo.prompt_set.all()  # Return prompts associated with the 
    
    def create(self, request, *args, **kwargs):
        serializer = serializers.PromptCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        convo = get_object_or_404(models.Convo, pk=self.kwargs['pk'])
        serializer.save(convo=convo, author=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial',False)
        instance = self.get_object()
        serializer = serializers.PromptCreateSerializer(
            instance,request.data,partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance= self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=("POST",) ,detail=True, url_path="feedback")
    def prompt_feedback_upload(self,request,pk):
        prompt= get_object_or_404(models.Prompt,id=pk)
        serializer = serializers.PromptFeedbackCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, prompt= prompt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    @action(methods=("POST",), detail=True, url_path="create-note")  
    def create_note(self,request,pk):
        prompt= get_object_or_404(models.Prompt,id=pk)
        serializer = serializers.CreateNoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(prompt=prompt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


"""
class PromptFeedbackView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = serializers.PromptFeedbackCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
"""


class BlockNoteViewSet(viewsets.ModelViewSet):
    queryset = models.BlockNote.objects.all()
    serializer_class = serializers.BlockNoteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        filter = models.BlockNote.objects.filter(user=self.request.user)
        return filter
    
    
    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(models.BlockNote,pk=kwargs['pk'], user=request.user)
        notes = (instance.note_set.all())
        note_serializer = serializers.NoteSerializer(notes, many=True)
        return Response(note_serializer.data)
        #return Response(xyz)
    
    
    def create(self, request, *args, **kwargs):
        serializer = serializers.CreateBlockNoteSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=request.user,
            workspace= request.user.workspace_set.all()[0]  
                        )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,headers=headers)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance= self.get_object()
        serializer = serializers.CreateBlockNoteSerializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance= self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class KnowledgeBaseView(viewsets.ModelViewSet):
    queryset = models.KnowledgeBase.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.KnowlodgeBaseSerializer

    def get_queryset(self):
        user = self.request.user
        return models.KnowledgeBase.objects.filter(workspace=user.workspace_set.all()[0])
    
    def create(self, request, *args, **kwargs):
        serializer = serializers.CreateKnowledgeBaseSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=request.user,
            workspace=request.user.workspace_set.all()[0])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = serializers.CreateKnowledgeBaseSerializer(
            instance,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)