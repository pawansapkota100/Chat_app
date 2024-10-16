from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model

user= get_user_model()

# Create your models here.
class UserLocation(models.Model):
    user= models.OneToOneField(user, on_delete=models.CASCADE, related_name='location')
    description= models.TextField()
    coordiantes= models.PointField()

    def __str__(self):
        return self.user.email



