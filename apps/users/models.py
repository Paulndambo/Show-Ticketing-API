from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.core.models import AbstractBaseModel
from apps.core.constants import GENDER_CHOICES, USER_ROLES


# Create your models here.
class User(AbstractUser, AbstractBaseModel):
    phone_number = models.CharField(max_length=255)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    role = models.CharField(max_length=50, choices=USER_ROLES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
