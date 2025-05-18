from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.aggregates import Max

from stengah.settings import TIMESTAMP_URL_FORMAT

# Create your models here.

def user_avatar_path(instance: 'User', filename):
    return f'avatars/{instance.username}_{filename}'

class User(AbstractUser):
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)

    def __str__(self):
        return f'{self.username} - {self.email} - {'ADMIN' if self.is_superuser else 'NORMAL'}'


class Repository(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.owner.username}/{self.name}] - {self.description} - {'public' if self.is_public else 'private'}'

    @property
    def last_commit(self):
        commits = Commit.objects.filter(repository=self).order_by('-timestamp')
        return commits[0] if len(commits) > 0 else None

    @property
    def last_timestamp(self):
        commit = self.last_commit
        return commit.timestamp if commit else self.created_at
    
    @property
    def open_issues(self):
        return self.issues.filter(status='open')


class Commit(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def urlsafe_timestamp(self):
        return datetime.strftime(self.timestamp, TIMESTAMP_URL_FORMAT)

    def __str__(self):
        return f'[{self.repository.owner.username}/{self.repository.name}] ' + \
               f"{self.author} | commited on {self.timestamp} with message '{self.message}'"


class File(models.Model):
    commit = models.ForeignKey(Commit, on_delete=models.CASCADE, related_name='files')
    path = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return f'[{self.commit.repository.owner.username}/{self.commit.repository.name}' + \
               f' | {self.commit.timestamp} | {self.commit.message} ] '+ \
               f'- {self.commit.author} - COMMITED - {self.path}'

    @property
    def size_bytes(self):
        return len(self.content.encode('utf-8'))

    @property
    def size_kb(self):
        return self.size_bytes / 1024


class Issue(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='issues')
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('closed', 'Closed')], default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    closing_comment = models.ForeignKey('Comment', on_delete=models.SET_NULL, null=True, blank=True, related_name='closed_issue')

    def __str__(self):
        max_length = 32 
        if len(self.title) > max_length:
            title = self.title[:max_length - 3] + '...'
        else:
            title = self.title
        return f'[{self.repository.owner.username}/{self.repository.name}] - {title} - by @{self.created_by.username}'

    @property
    def last_active_comment(self):
        comments = Comment.objects.filter(issue=self).order_by('-created_at')
        return comments[0] if len(comments) > 0 else None

    @property
    def last_active_prop(self):
        comment = self.last_active_comment
        return comment.created_at if comment else self.created_at

    @property
    def is_open(self):
        return self.status == 'open'


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.created_at}] {self.issue} | {self.author} | commented "{self.content}"'


