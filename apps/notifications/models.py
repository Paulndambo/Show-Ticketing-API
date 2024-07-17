from django.db import models
from apps.core.models import AbstractBaseModel
# Create your models here.
class Message(AbstractBaseModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    message_type = models.CharField(max_length=255, null=True)
    subject = models.CharField(max_length=255)

    def __str__(self):
        return self.subject
