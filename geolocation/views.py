from .models import UserLocation
from .serializers import userLocationSerializer,NearestUserLocationSerializer
from rest_framework import viewsets
from django.contrib.gis.db.models.functions import Distance
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from rest_framework import status
# Create your views here.

class UserLocationViewSet(viewsets.ModelViewSet):
    queryset = UserLocation.objects.all()
    serializer_class = userLocationSerializer
    http_method_names = ['get', 'post']

    def post(self, request):
        # Extract coordinates and radius from the request data
        coordinates = request.data.get('coordinates')  # Expects a list or tuple [longitude, latitude]
        radius = request.data.get('radius')  # Radius in kilometers

        if not coordinates or not radius:
            return Response({"error": "Coordinates and radius are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Convert the coordinates to a GeoDjango Point (longitude, latitude)
            point = Point(float(coordinates[0]), float(coordinates[1]), srid=4326)

            # Filter locations within the specified radius using Distance and D (for distance)
            nearest_user_address = UserLocation.objects.annotate(
                distance=Distance("coordiantes", point)
            ).filter(distance__lte=radius * 1000).order_by('distance')

            # Serialize the results
            serializer = NearestUserLocationSerializer(nearest_user_address, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValueError:
            return Response({"error": "Invalid coordinates format."}, status=status.HTTP_400_BAD_REQUEST)