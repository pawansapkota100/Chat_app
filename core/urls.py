from django.urls import path
from .views import index,room,login_view


urlpatterns = [
    path("", index, name="index"),
    path('login/', login_view, name='login'),

    path("<str:room_name>/",room, name="room"),
]
