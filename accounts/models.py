from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USERS_ROLE = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student')
    )

    role = models.CharField(max_length=50, choices=USERS_ROLE, default='student')

    def __str__(self):
        return f"{self.username} ({self.role})"