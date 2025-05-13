from django.contrib import admin 
from . import models

admin.site.register(models.User)
admin.site.register(models.Repository)
admin.site.register(models.Commit)
admin.site.register(models.File)
admin.site.register(models.Issue)
admin.site.register(models.Comment)

admin.site.header = 'GitLite Administration'
admin.site.title = 'GitLite Administration'
