from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    total_score = models.IntegerField(default=0)

    def __str__(self):
        return self.username