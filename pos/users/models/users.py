""" User model."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Utilities
from pos.utils.models import CustomModel

class User(CustomModel, AbstractUser):

    email = models.EmailField(
        'email address',
        unique=True
    )

    phone_regex = RegexValidator(
        regex=r'|+?1?\d{9,15}$',
        message="Phone number must be  entered in the format: +9999999999. Up to 15 digists allowed."
    )

    phone_number = models.CharField(max_length=17, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    is_client = models.BooleanField(
        'client',
        default=True,
        help_text=(
            'Help easily distinguish users and perform queries.'
            'Clients are the main type of user'
        )
    )

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username