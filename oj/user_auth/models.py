from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    AbstractUser already includes:
    username
    email
    password
    first_name, last_name
    is_active, is_superuser, etc.
    """

    dob = models.DateField(null=True, blank=True)
    mobile_no = models.CharField(max_length=15, blank=True, null=True)



# def __str__(self):
#     return self.username
