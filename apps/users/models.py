from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    telefon = models.CharField(max_length=13, unique=True)
    rasm = models.ImageField(upload_to='avatars/', null=True, blank=True)
    yaratilgan = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
