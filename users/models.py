from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон')
    city = models.CharField(max_length=100, verbose_name='город')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар',
                               null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
