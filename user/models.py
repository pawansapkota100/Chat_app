from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None  # Remove the username field
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Add other required fields if needed

    ROLE = (
        ("STUDENT", "student"),
        ("INSTRUCTOR", "instructor"),
        ("ADMIN", "admin"),
    )

    role = models.CharField(choices=ROLE, max_length=10, default="STUDENT")  # Changed to STUDENT
    objects = CustomUserManager()

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def is_student(self):
        return self.role == "STUDENT"

    def is_instructor(self):
        return self.role == "INSTRUCTOR"

    def is_admin(self):
        return self.role == "ADMIN"

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Student_profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    course_enrolled=models.ManyToManyField('Course', related_name='students', blank=True)
    grade= models.CharField(max_length=100, null=True, blank=True)

class Instructor_profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    bio= models.TextField(null=True, blank=True)
    course_taught=models.ManyToManyField('Course', related_name='instructors', blank=True)

class Course(models.Model):
    name= models.CharField(max_length=100)
    description= models.TextField()
    instructor= models.ManyToManyField(User, related_name='courses_instructor',limit_choices_to={'role': 'INSTRUCTOR'})
    student= models.ManyToManyField(User, related_name='courses_student', blank=True, limit_choices_to={'role': 'STUDENT'})
    created_by= models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
