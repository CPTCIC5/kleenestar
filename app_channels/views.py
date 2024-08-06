from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status,pagination
from rest_framework.response import Response
from . import models, serializers
from rest_framework.decorators import action
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from openai import OpenAI
from dotenv import load_dotenv
from django.http import StreamingHttpResponse
import uuid
from .models import generate_insights_with_gpt4,followup_questions
from workspaces.serializers import SubSpaceCreateSerializer

load_dotenv()
client= OpenAI()
class CustomPagination(pagination.PageNumberPagination):
    page_size = 10



class ChannelViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Channel.objects.all()
    serializer_class = serializers.ChannelSerializer
    filterset_fields = ('subspace',)

    def get_queryset(self):
        # Customize queryset based on the request or user
        user = self.request.user
        return models.Channel.objects.filter(subspace__workspace=user.workspace_set.first())
    

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

    # @action(methods=("GET",), detail=True, url_path="subspace-channels")
    # def get_subspace_channels(self, request, pk):
    #     return Response(serializers.ChannelSerializer(models.Channel.objects.filter(subspace_id=int(pk)), many=True).data)



class ConvoViewSet(viewsets.ModelViewSet):
    queryset = models.Convo.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ConvoSerializer
    pagination_class = CustomPagination
    filterset_fields = ('subspace',)

    def get_queryset(self):
        workspace = self.request.user.workspace_set.first()
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
        subspace = instance.subspace
        # should work ig idk test and see

        self.perform_destroy(instance)
        workspace = self.request.user.workspace_set.first()

        if models.Convo.objects.filter(subspace=subspace).count() < 1:
            models.Convo.objects.create(
                subspace=subspace,
                
            )
            
        return Response(status=status.HTTP_200_OK)
    
    @action(methods=("GET",), detail=True, url_path="subspace-convos")
    def get_subspace_convos(self, request, pk):
        return Response(serializers.ConvoSerializer(models.Convo.objects.filter(subspace_id=int(pk)), many=True).data)

        

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
        channel_layer = get_channel_layer()

        if request.user.ws_channel_name:
            async_to_sync(channel_layer.send)(request.user.ws_channel_name, {"type": "test"})


        serializer = serializers.PromptCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        convo = get_object_or_404(models.Convo, pk=self.kwargs['pk'])

        # Create Prompt instance but do not save it yet
        prompt_instance = serializer.save(convo=convo, author=request.user)

        history_counts = convo.prompt_set.all().count()
        if history_counts >= 1:
            thread = client.beta.threads.retrieve(thread_id=convo.thread_id)
        else:
            thread = client.beta.threads.create()
            convo.thread_id = thread.id
            convo.save()

        generate_insights_with_gpt4(
            user_query=prompt_instance.text_query, 
            convo=convo.id, 
            file=prompt_instance.file_query or None, 
            namespace=convo.subspace.pinecone_namespace,
            user=request.user,
        )

            # prompt_instance.response_text = response_data.get('text', None)
            # if response_data.get('image', None):
            #     prompt_instance.response_file.save(f"{uuid.uuid4()}.png", response_data['image'], save=False)

            # x1 = followup_questions(prompt_instance.text_query, prompt_instance.response_text, assist_id=convo.subspace.workspace.assistant_id)
            # prompt_instance.similar_questions = x1['questions']

            # # Now save the instance with the updated fields
            # prompt_instance.save()

            # yield f"data: {serializer.data}\n\n"

        return Response("done")

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
    filterset_fields = ('subspace',)

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
    serializer_class = serializers.KnowledgeBaseSerializer
    filterset_fields = ('subspace',)

    def get_queryset(self):
        user = self.request.user
        return models.KnowledgeBase.objects.filter(subspace__workspace=user.workspace_set.first())

    def create(self, request, *args, **kwargs):
        serializer = serializers.CreateKnowledgeBaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workspace = request.user.workspace_set.first()
        knowledge_base = serializer.save(subspace__workspace=workspace)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = serializers.CreateKnowledgeBaseSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def create_knowledge_source(self, request):
        serializer = serializers.KnowledgeSourceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        knowledge_source = serializer.save(user=request.user)
        return Response(serializers.KnowledgeSourceSerializer(knowledge_source).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def list_knowledge_sources(self, request):
        user = request.user
        knowledge_sources = models.KnowledgeSource.objects.filter(user=user)
        serializer = serializers.KnowledgeSourceSerializer(knowledge_sources, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put', 'patch'])
    def update_knowledge_source(self, request, pk=None):
        instance = models.KnowledgeSource.objects.get(pk=pk)
        serializer = serializers.KnowledgeSourceSerializer(instance, data=request.data, partial=request.method == 'PATCH')
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def delete_knowledge_source(self, request, pk=None):
        instance = models.KnowledgeSource.objects.get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubspaceViewSet(viewsets.ModelViewSet):
    permission_classes= [permissions.IsAuthenticated]
    serializer_class = serializers.SubspaceSerializer
    
    def get_queryset(self):
        return models.SubSpace.objects.filter(workspace=self.request.user.workspace_set.first())

    
    def create(self, request, *args, **kwargs):
        serializer = SubSpaceCreateSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = SubSpaceCreateSerializer(
            instance=instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance= self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)