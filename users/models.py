from django.contrib.auth.models import User, UserManager
from django.db import models

# Create your models here.
class VenuesUser(User):
    objects = UserManager()
    staff = models.BooleanField(default=False)