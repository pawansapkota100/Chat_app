from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from geolocation.models import UserLocation


User = get_user_model() 

class Command(BaseCommand):
    help="generate random location for user"
    def handle(self, *args, **kwargs):
        faker=Faker()

        users = User.objects.all()

        for user in users:
            longitude= faker.longitude()
            latitude= faker.latitude()
            point= Point((longitude, latitude), srid=4326)

            UserLocation.objects.update_or_create(
                user=user,
                    defaults={
                        'description': faker.text(max_nb_chars=50),
                        'coordiantes': point  # Corrected spelling
                    }
            )
            user.save()


