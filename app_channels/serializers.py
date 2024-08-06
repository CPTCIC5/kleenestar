from rest_framework import serializers
from workspaces.serializers import WorkSpaceSerializer,SubspaceSerializer
from users.serializers import UserSerializer
from . import models

class APICredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.APICredentials
        fields = ['key_1', 'key_2', 'key_3', 'key_4', 'key_5', 'key_6']

class ChannelSerializer(serializers.ModelSerializer):
    subspace = SubspaceSerializer()
    credentials = APICredentialsSerializer()

    class Meta:
        model = models.Channel
        fields = ['id', 'channel_type', 'subspace', 'credentials', 'created_at']
        read_only = ['subspace']

class ChannelCreateSerializer(serializers.ModelSerializer):
    credentials = APICredentialsSerializer()

    class Meta:
        model = models.Channel
        fields = ["channel_type", "subspace", "credentials"]




class ConvoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Convo
        fields = ['title', 'archived', 'subspace']




class CreateNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Note
        fields = ["note_text", "color","blocknote"]

class NoteSerializer(serializers.ModelSerializer):
    prompt = serializers.SerializerMethodField()
    blocknote = serializers.SerializerMethodField()

    class Meta:
        model = models.Note
        fields = ['note_text', 'created_at', 'color', 'prompt', 'blocknote', 'id']

    def get_prompt(self, obj):
        return PromptSerializer(obj.prompt).data

    def get_blocknote(self, obj):
        return BlockNoteSerializer(obj.blocknote).data
    




class CreateBlockNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BlockNote
        fields = ("title", "image", "subspace")

class BlockNoteSerializer(serializers.ModelSerializer):
    #user = UserSerializer()
    #workspace = WorkSpaceSerializer()
    notes= NoteSerializer(many=True,read_only=True,source='note')
    
    class Meta:
        model = models.BlockNote
        fields = ("user", "subspace", "title", "image", "id", "created_at","notes")

    

    




class PromptCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Prompt
        fields = ("text_query", "file_query")

class ConvoSerializer(serializers.ModelSerializer):
    subspace = SubspaceSerializer()
    all_notes = NoteSerializer(many=True)

    class Meta:
        model = models.Convo
        fields = ('id', 'thread_id', 'subspace', 'title', 'archived', 'created_at', 'all_notes')


class PromptSerializer(serializers.ModelSerializer):
    convo= ConvoSerializer()
    class Meta:
        model = models.Prompt
        fields = ('id', 'convo', 'author', 'text_query', 'file_query', 'response_text', 'response_file', 'created_at')





class PromptFeedbackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PromptFeedback
        fields = ('category', 'note')



class KnowledgeSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KnowledgeSource
        fields = ['id', 'text_data', 'created_at']

class KnowledgeBaseSerializer(serializers.ModelSerializer):
    knowledge_source = KnowledgeSourceSerializer(many=True, read_only=True)

    class Meta:
        model = models.KnowledgeBase
        fields = ['id', 'subspace', 'knowledge_source', 'created_at']
        read_only_fields = ['created_at']

class CreateKnowledgeBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KnowledgeBase
        fields = ['id', 'subspace', 'knowledge_source']



        

"""
class PromptInputSerializer(serializers.Serializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),many=False)
    text_query=serializers.CharField(max_length=50,required=True)
    image_query=serializers.ImageField(allow_null=True, required=False)
    refactored_image = serializers.CharField(allow_blank=True) #gpt 4.0 will refactor the query 
    response_text=serializers.CharField(allow_blank=True)
    response_image= serializers.ImageField(allow_null=True, required=False)
    created = serializers.DateTimeField()


    def create(self, validated_data):
        try:
            # Attempt to open the existing JSON file
            with open('response_data.json', 'r') as file:
                response_data_list = json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, initialize an empty list
            response_data_list = []

        # Append the new response data to the list
        response_data_list.append({
            'user_query': validated_data['user_query'],
            'refactored_query': validated_data['refactored_query'],
            'response_text': validated_data['response_text'],
            'created': validated_data['created'].isoformat(),
        })

        # Write the updated list back to the JSON file
        with open('response_data.json', 'w') as file:
            json.dump(response_data_list, file)

        return response_data_list
"""