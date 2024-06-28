from rest_framework import serializers
from workspaces.serializers import WorkSpaceSerializer
from .serializers import NoteSerializer
from . import models

class ConvoSerializer(serializers.ModelSerializer):
    workspace = WorkSpaceSerializer()
    all_notes= NoteSerializer(many=True, read_only=True)

    class Meta:
        model = models.Convo
        fields = ('id', 'thread_id', 'workspace', 'title', 'archived', 'created_at', 'all_notes')

    def get_all_notes(self, obj):
        print(obj)
        notes = obj.all_notes  # Access the all_notes property
        return NoteSerializer(notes, many=True).data