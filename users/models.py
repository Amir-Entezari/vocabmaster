from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username


class BlackToken(models.Model):
    token = models.CharField(
        verbose_name="Token to blacklist", max_length=60, null=False, blank=False
    )
