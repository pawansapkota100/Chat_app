from django.contrib import admin
from .models import User, Student_profile, Instructor_profile
# Register your models here.
admin.site.register(User)
admin.site.register(Student_profile)
admin.site.register(Instructor_profile)