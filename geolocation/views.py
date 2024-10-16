from .models import UserLocation
from .serializers import userLocationSerializer
from rest_framework import viewsets
# Create your views here.

class UserLocationViewSet(viewsets.ModelViewSet):
    queryset = UserLocation.objects.all()
    serializer_class = userLocationSerializer
    http_method_names = ['get']
