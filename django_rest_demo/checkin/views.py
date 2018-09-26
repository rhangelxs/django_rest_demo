from rest_framework import generics, viewsets, permissions, mixins
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from .serializers import LocationsDetailsSerializer, LocationVisitSerializer, LocationRatioSerializer

from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Location, Visit


# class UserIsOwnerOrReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.id == request.user.id


class LocationList(mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationsDetailsSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly, UserIsOwnerOrReadOnly]

class LocationVisit(generics.CreateAPIView):
    def get_queryset(self):
        queryset = Visit.objects.filter(location_id=self.kwargs["pk"])
        return queryset
    serializer_class = LocationVisitSerializer

class LocationRatio(generics.RetrieveAPIView):
    def get_queryset(self):
        queryset = Location.objects.filter(pk=self.kwargs["pk"])
        return queryset
    serializer_class = LocationRatioSerializer
