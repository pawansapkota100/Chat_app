from django.contrib import admin

from .models import UserLocation

# Register your models here.

class userLocationAdmin(admin.ModelAdmin):

    list_display = ('user', 'description', 'coordiantes')
admin.site.register(
    UserLocation,
    userLocationAdmin
)