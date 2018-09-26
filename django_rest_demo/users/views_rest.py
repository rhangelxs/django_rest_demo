from rest_framework import generics, viewsets

from .serializers import UsersDetailsSerializer

from django.contrib.auth import get_user_model
User = get_user_model()


class UserList(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersDetailsSerializer
