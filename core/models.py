from django.db import models
from django.contrib.auth import get_user_model  

user= get_user_model()
# Create your models here.


class Chatroom(models.Model):
    name= models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class Message(models.Model):
    room= models.ForeignKey(Chatroom, on_delete=models.CASCADE, related_name='messages')
    user= models.ForeignKey(user, on_delete=models.CASCADE, related_name='messages')
    content= models.TextField()
    timestamp= models.DateTimeField(auto_now_add=True)      

    class Meta:
        ordering= ('timestamp',)
    
    def __str__(self):
        return f' {self.content[:50]}'