from django.db import models
from django.contrib.auth.models import User
from datetime import time


class RegisterUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=100)
    password_expiry = models.TimeField(default=time, blank=True)

    def __str__(self):
        return self.user.username