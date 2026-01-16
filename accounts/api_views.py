from __future__ import annotations

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response(
        {
            "id": user.id,
            "username": user.get_username(),
            "email": getattr(user, "email", ""),
            "is_staff": bool(user.is_staff),
            "is_superuser": bool(user.is_superuser),
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    # Token auth: delete the current token (client must re-login to get a new one)
    token = getattr(request, "auth", None)
    if token is not None:
        token.delete()
    else:
        # Fallback if authentication class didn't attach request.auth
        try:
            request.user.auth_token.delete()
        except Exception:
            pass

    return Response(status=status.HTTP_204_NO_CONTENT)
