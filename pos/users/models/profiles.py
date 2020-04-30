"""Profile models."""

# Django
from django.db import models


# Models
from pos.levels.models import Level

# Utilities
from pos.utils.models import CustomModel

def profile_directory_path(instance, filename):
    return 'users/{0}/{1}'.format(instance.user.username, filename)

class Profile(CustomModel):
    """Profile model.

    A profile holds a user's public data like biography, picture,
    and statistics.
    """
     
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    description = models.CharField(null=False, blank=False, max_length=255)
    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE
    )
    last_login = models.DateTimeField(blank=True, null=True)
    picture = models.ImageField(
        'profile picture',
        upload_to=profile_directory_path,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user