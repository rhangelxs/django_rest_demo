from rest_framework import generics, viewsets, permissions, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import LocationsDetailsSerializer, LocationVisitSerializer, LocationRatioSerializer, \
    UserRatioSerializer

from .models import Location, Visit

from django.contrib.auth import get_user_model

User = get_user_model()


class VisitorIsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_id == request.user


class LocationList(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationsDetailsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class LocationVisit(generics.CreateAPIView):
    def get_queryset(self):
        queryset = Visit.objects.filter(location_id=self.kwargs["pk"])
        return queryset

    serializer_class = LocationVisitSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class LocationRatio(generics.RetrieveAPIView):
    def get_queryset(self):
        queryset = Location.objects.filter(pk=self.kwargs["pk"])
        return queryset

    serializer_class = LocationRatioSerializer


class UserRatio(generics.RetrieveAPIView):
    def get_queryset(self):
        queryset = User.objects.filter(pk=self.kwargs["pk"])
        return queryset

    serializer_class = UserRatioSerializer


class VisitList(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):
    queryset = Visit.objects.all()
    serializer_class = LocationVisitSerializer
    permission_classes = [VisitorIsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
