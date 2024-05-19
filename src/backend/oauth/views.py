from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from channels.models import Channel
from backend.settings import AUTH_USER_MODEL


@api_view(("GET", "POST"))
def google_oauth_callback(request):
    # https://example.com/?code=...
    code = request.query_params.get("code")

    if not code:
        return Response(
            {"detail": "something not working???"},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    # griffin
    refresh_token = ...
    customer_id = ...
    email = ...

    if isinstance(customer_id, list):
        return Response(
            {"detail": "manager accounts not allowed"},
            status=status.HTTP_403_FORBIDDEN,
        )

    # arayn
    user = get_object_or_404(AUTH_USER_MODEL,email=email)  # get the user from the email
    workspace = user.workspace_set.all()[0]
    google_channel = get_object_or_404(Channel, channel_type=1)

    google_channel.credentials.key_1 = code
    google_channel.credentials.key_2 = refresh_token
    google_channel.credentials.key_3 = customer_id
    google_channel.save()

    return Response(status=status.HTTP_200_OK)
