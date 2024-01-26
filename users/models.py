from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон')
    city = models.CharField(max_length=100, verbose_name='город')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар',
                               null=True, blank=True)

    role = models.CharField(max_length=9, choices=UserRoles.choices,
                            default=UserRoles.MEMBER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
