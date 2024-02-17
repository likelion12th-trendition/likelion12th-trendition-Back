from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import ASCIIUsernameValidator

class CustomUser(AbstractUser):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phonenumber = models.CharField(max_length=13)
    profileImage = models.ImageField(upload_to='profile_image/', blank=True, null=True)
    id = models.CharField(max_length=20, unique=True, validators=[ASCIIUsernameValidator()], primary_key=True)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        if len(self.password) < 8:
            raise ValueError("비밀번호는 8자 이상이어야 합니다.")
        special_characters = "!@#$%^&*()-+"
        if not any(char in special_characters for char in self.password):
            raise ValueError("비밀번호는 특수문자를 포함해서 설정해야 합니다.")
        super().save(*args, **kwargs)

# Create your models here.
