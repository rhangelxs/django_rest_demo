from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model

from django_rest_demo.users.serializers import UsersDetailsSerializer
from .models import Location, Visit

from django.db.models import Avg

User = get_user_model()

class LocationsDetailsSerializer(serializers.ModelSerializer):
    """
    Location serializer
    """
    class Meta:
        model = Location
        fields = '__all__'
        #exclude = ()
        # read_only_fields = ('pk', )

    # birth_date = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y', 'iso-8601'])

class LocationVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        exclude = ()
        read_only_fields = ('date',)

class LocationRatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("visitors", "count", "avg")
        # read_only_fields = ('date',)

    visitors = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    avg = serializers.SerializerMethodField()

    def get_avg(self, obj):
        return obj.visit_set.aggregate(Avg('ratio')).get("ratio__avg")

    def get_count(self, obj):
        return obj.visit_set.count()

    def get_visitors(self, obj):
        return UsersDetailsSerializer(User.objects.filter(visit__location_id=obj).distinct(), many=True, read_only=True).data

class UserRatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("locations", "count", "avg")
        # read_only_fields = ('date',)

    locations = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    avg = serializers.SerializerMethodField()

    def get_avg(self, obj):
        return obj.visit_set.aggregate(Avg('ratio')).get("ratio__avg")

    def get_count(self, obj):
        return obj.visit_set.count()

    def get_locations(self, obj):
        # return LocationsDetailsSerializer(obj.visit_set.all().values("location_id").distinct(), many=True, read_only=True).data
        return LocationsDetailsSerializer(Location.objects.filter(visit__user_id=obj).distinct(), many=True, read_only=True).data
