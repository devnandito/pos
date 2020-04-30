"""Clients models."""

# Django
from django.db import models

# Utilities
from pos.utils.models import CustomModel

class Client(CustomModel):
    """Client model."""

    first_name = models.CharField(max_length=140, blank=False, null=False)
    last_name = models.CharField(max_length=140, blank=False, null=False)
    ci = models.CharField(max_length=8, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    phone = models.CharField(max_length=10, blank=False, null=False)
    direction = models.CharField(max_length=500, blank=False, null=False)
    birthday = models.DateField(blank=False, null=False)
    purchases = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return ('{} {}').format(self.first_name, self.last_name)