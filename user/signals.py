from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Instructor_profile, Student_profile

User = get_user_model()


@receiver(post_save, sender=User)
def createUserProfile(sender, instance, created, **kwargs):
    if created:
        if instance.role == "INSTRUCTOR":
            profile= Instructor_profile.objects.create(user=instance)
            profile.save()
        if instance.role == "STUDENT":
            profile= Student_profile.objects.create(user=instance)
            profile.save()
