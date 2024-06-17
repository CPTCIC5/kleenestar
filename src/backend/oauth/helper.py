from django.shortcuts import get_object_or_404
from channels.models import Channel
from users.models import User


def get_channel(email,channel_type_num):
    user = get_object_or_404(User,email=email)
    workspace = user.workspace_set.all()[0]
    return get_object_or_404(Channel, channel_type=channel_type_num, workspace=workspace)

def create_channel(email, channel_type_num):
    user = get_object_or_404(User,email=email)
    workspace = user.workspace_set.all()[0]

    try:
        new_channel = Channel.objects.create(
            channel_type=channel_type_num, 
            workspace=workspace,
        )
        return new_channel
    except Exception:
        return Channel.objects.get(channel_type=channel_type_num, workspace=workspace,)
    