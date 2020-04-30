"""Levels models."""

# Django
from django.db import models

# Utilities
from pos.utils.models import CustomModel

class Level(CustomModel):
    """Level model."""

    description = models.CharField(max_length=140, blank=False, null=False)

    def __str__(self):
        return self.description