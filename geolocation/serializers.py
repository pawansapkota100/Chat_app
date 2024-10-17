
from .models import UserLocation
from rest_framework import serializers

class userLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = '__all__'

class NearestUserLocationSerializer(serializers.ModelSerializer):
    # radius=serializers.FloatField()
    class Meta:
        model = UserLocation
        fields = ['coordiantes']

