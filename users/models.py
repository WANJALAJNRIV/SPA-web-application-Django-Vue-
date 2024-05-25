from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', default="default.jpg")
    date_of_birth = models.DateField(null=True, blank=True)
    favorite_categories = models.ManyToManyField('api.Category', blank=True)

    def __str__(self):
        return self.username