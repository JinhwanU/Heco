from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.


class UserData(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=12, unique=True)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     db_table = "common_accounts"
