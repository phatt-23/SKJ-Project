```python
class User(AbstractUser):
    pass

class Repository(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Commit(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class File(models.Model):
    commit = models.ForeignKey(Commit, on_delete=models.CASCADE)
    path = models.CharField(max_length=255)
    content = models.TextField()

class Issue(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('closed', 'Closed')])

class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```
