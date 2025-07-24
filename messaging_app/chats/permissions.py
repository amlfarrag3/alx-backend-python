from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to view/send/edit/delete messages.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        method = request.method

        # Read permissions (GET, HEAD, OPTIONS) or modifying ones (PUT, PATCH, DELETE)
        if method in SAFE_METHODS or method in ["PUT", "PATCH", "DELETE"]:
            if hasattr(obj, 'conversation'):
                return user in obj.conversation.participants.all()
            elif hasattr(obj, 'participants'):
                return user in obj.participants.all()

        return False
 
   