import random

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import UsernameRegexValidator, me_username


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    username = models.CharField(
        'Имя пользователя',
        unique=True,
        blank=False,
        max_length=150,
        validators=[UsernameRegexValidator, me_username]
    )
    email = models.EmailField(
        'Почта',
        unique=True,
        blank=False,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=10,
        choices=ROLE_CHOICES,
        default=USER,
    )
    confirmation_code = models.TextField(
        'Код подтверждения',
    )

    class Meta:
        ordering = ('username',)

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def code_gen(self):
        min = settings.MIN_VALUE
        max = settings.MAX_VALUE
        random_int = random.randint(min, max)
        return random_int

    def __str__(self):
        return self.username
