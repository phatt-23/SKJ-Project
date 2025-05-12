from django.db import models

from SKJ.project.minigithub.users.models import User

# Create your models here.

class Repository(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(black=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Commit(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


