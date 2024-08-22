from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.IntegerChoices):
    DIET = 1
    BEGINNER = 2
    INTERMEDIATE = 3
    ADVANCED = 4


class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    contents = models.CharField(max_length=2000)
    image_url = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.IntegerField(choices=Category.choices)
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="user_id",
    )


class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    contents = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="user_id",
    )
    post_id = models.ForeignKey(
        "Posts",
        on_delete=models.CASCADE,
        db_column="post_id",
    )
