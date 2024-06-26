from rest_framework.permissions import IsAuthenticated, SAFE_METHODS


class UserViewSetPermissions(IsAuthenticated):
    def has_object_permission(self, request, view, instance):
        if request.user.is_authenticated and request.method not in SAFE_METHODS:
            if instance.id != request.user.id and not request.user.is_staff:
                return False

        return super().has_object_permission(request, view, instance)
