from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    login = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
