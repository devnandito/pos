from pos.levels.models import Level
from pos.users.models import User, Profile
from django.shortcuts import get_object_or_404


user = get_object_or_404(User, pk=1)
level = Level(id=1, description='Administrador')
level.save()
l1 = get_object_or_404(Level, pk=1)
profile = Profile(user = user, description='admin', level=l1)
profile.save()
