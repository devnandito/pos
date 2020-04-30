"""Products models."""

# Django
from django.db import models

# Models
from pos.categories.models import Category

# Utilities
from pos.utils.models import CustomModel

def image_directory_path(instance, filename):
    return 'products/{0}/{1}'.format(instance.description, filename)

class Product(CustomModel):
    """Product model."""

    fkcategory = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    code = models.CharField(max_length=140, blank=False, null=False)
    description = models.CharField(max_length=140, blank=False, null=False)
    image = models.ImageField(
        'image',
        upload_to=image_directory_path,
        blank=True,
        null=True
    )
    stock = models.IntegerField(default=0, blank=False, null=False)
    purchase_price = models.DecimalField(default=0.0, max_digits=19, decimal_places=1)
    sale_price = models.DecimalField(default=0.0, max_digits=19, decimal_places=1)
    sales = models.IntegerField(default=0, blank=False, null=False)
    
    def __str__(self):
        return self.description