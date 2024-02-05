from rest_framework.permissions import BasePermission

class IsSuperuser(BasePermission):
    def has_permission(self,request,view):
        # print(request.user)
        return request.user and request.user.is_staff