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
        #fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'gender', 'birth_date', 'country')
        exclude = ()
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
        fields = ("visits", "count", "avg")
        # read_only_fields = ('date',)

    visits = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    avg = serializers.SerializerMethodField()

    def get_avg(self, obj):
        return obj.visit_set.aggregate(Avg('ratio')).get("ratio__avg")

    def get_count(self, obj):
        return obj.visit_set.count()

    def get_visits(self, obj):
        return LocationVisitSerializer(obj.visit_set.all().order_by('id'), many=True, read_only=True).data
