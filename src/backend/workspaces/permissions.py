from rest_framework.permissions import SAFE_METHODS


class WorkSpaceViewSetPermissions:
    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.is_staff or request.user.subscription_type is not None

        return (
            request.user.is_staff
            or request.user.subscription_type is not None
            or request.user.is_team_member
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return (
                obj.users.contains(
                    request.user
                )  # check if the user is a member of that workspace
                or obj.root_user == request.user
                or request.user.is_staff
            )

        else:
            return obj.root_user == request.user or request.user.is_staff
