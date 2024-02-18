from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    phonenumber = models.CharField(max_length=13)
    profileImage = models.ImageField(upload_to='profile/', default='default.png')
    follower = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    following = models.ManyToManyField('self', symmetrical=False, related_name='followings')

    def __str__(self):
        return self.username
