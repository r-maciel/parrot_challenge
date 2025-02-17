from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """ Custom permission for superusers """

    def has_permission(self, request, view):
        """ Check for super user """
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_superuser
        )
