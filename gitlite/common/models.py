from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

def user_avatar_path(instance: 'User', filename):
    return f'avatars/{instance.username}_{filename}'

class User(AbstractUser):
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)

    def __str__(self):
        return f'{self.username} ({self.email})'

class Repository(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner.username} / {self.name} ({'public' if self.is_public else 'private'})'

class Commit(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.repository.name} => {self.message} => {self.timestamp}'

class File(models.Model):
    commit = models.ForeignKey(Commit, on_delete=models.CASCADE)
    path = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return f'{self.path} | {self.commit}'

class Issue(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('closed', 'Closed')])

    def __str__(self):
        return f'{self.repository.name} | {self.title} | {self.created_by.username}'

class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.issue} | {self.author}'

