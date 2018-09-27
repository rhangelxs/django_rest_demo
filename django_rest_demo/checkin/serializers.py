from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import serializers

from django_rest_demo.users.serializers import UsersDetailsSerializer
from .models import Location, Visit

User = get_user_model()


class LocationsDetailsSerializer(serializers.ModelSerializer):
    """
    Location serializer
    """
    class Meta:
        model = Location
        fields = '__all__'


class LocationVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        exclude = ()
        read_only_fields = ('date',)


class LocationRatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("visitors", "count", "avg")

    visitors = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    avg = serializers.SerializerMethodField()

    def get_avg(self, obj):
        return obj.visit_set.aggregate(Avg('ratio')).get("ratio__avg")

    def get_count(self, obj):
        return obj.visit_set.count()

    def get_visitors(self, obj):
        return UsersDetailsSerializer(User.objects.filter(visit__location_id=obj).distinct(), many=True,
                                      read_only=True).data


class UserRatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("locations", "count", "avg")

    locations = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    avg = serializers.SerializerMethodField()

    def get_avg(self, obj):
        return obj.visit_set.aggregate(Avg('ratio')).get("ratio__avg")

    def get_count(self, obj):
        return obj.visit_set.count()

    def get_locations(self, obj):
        return LocationsDetailsSerializer(Location.objects.filter(visit__user_id=obj).distinct(), many=True,
                                          read_only=True).data
