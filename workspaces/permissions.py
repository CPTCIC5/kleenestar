from rest_framework.permissions import BasePermission, SAFE_METHODS

class WorkSpaceViewSetPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            # Allow workspace creation for authenticated users
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            # Allow safe methods (GET, HEAD, OPTIONS) for workspace members or staff
            return obj.users.filter(id=request.user.id).exists() or obj.root_user == request.user or request.user.is_staff
        return obj.root_user == request.user or request.user.is_staff