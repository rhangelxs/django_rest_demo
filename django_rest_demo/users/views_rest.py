from rest_framework import generics, viewsets, permissions, mixins
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, IsAuthenticatedOrReadOnly

from .serializers import UsersDetailsSerializer

from django.contrib.auth import get_user_model
User = get_user_model()


class UserIsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id


class UserList(mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               mixins.ListModelMixin,
               viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UsersDetailsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, UserIsOwnerOrReadOnly]
