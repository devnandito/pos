""" Django models utilities """

# Django
from django.db import  models

class CustomModel(models.Model):
    """ Pos model. 

        Pos acts as an abstract base class from which every
        other model in the project will inherit, This class provides
            + created (DateTime): Store the datetime the object was created
            + modified (DateTime): Store the last datetime the object was modified
     """

    created_at = models .DateTimeField(
        'created_at',
        auto_now_add=True,
        help_text='Date time on which the object was created.'
    )
    update_at = models .DateTimeField(
        'update_at',
        auto_now=True,
        help_text='Date time on which the object was last modified.'
    )

    class Meta:
        """ Meta options. """

        abstract = True
        get_latest_by = 'created_at'
        ordering = ['-created_at', '-update_at']