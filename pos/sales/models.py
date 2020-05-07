"""Sales models."""

# Django
from django.db import models

# Utilities
from pos.utils.models import CustomModel

# Models
from pos.clients.models import Client
from pos.users.models import User

class Sale(CustomModel):
    """Sale model."""

    invoice = models.IntegerField(blank=False, null=False)
    fkclient = models.ForeignKey(
        Client,
        on_delete=models.CASCADE
    )
    fkuser = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    product = models.CharField(max_length=500, blank=False, null=False)
    tax = models.DecimalField(default=0.0, max_digits=19, decimal_places=1)
    net = models.DecimalField(default=0.0, max_digits=19, decimal_places=1)
    total = models.DecimalField(default=0.0, max_digits=19, decimal_places=1)
    payment = models.CharField(max_length=500, blank=False, null=False)

    def __str__(self):
        return ('{}').format(self.code)