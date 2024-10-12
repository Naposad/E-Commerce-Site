from rest_framework import permissions

class IsFournisseur(permissions.BasePermission):
    """
    Permission to only allow users in the 'Fournisseur' group.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Fournisseur').exists()
    

