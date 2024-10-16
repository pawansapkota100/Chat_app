
from django.urls import path
from .views import UserLocationViewSet
urlpatterns = [
    path("user_location/",UserLocationViewSet.as_view({'get':'list'}),name="user_location"),
]
