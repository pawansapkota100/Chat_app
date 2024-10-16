
from .models import UserLocation
from rest_framework import serializers

class userLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = '__all__'