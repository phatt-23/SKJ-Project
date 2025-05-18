from django.contrib import admin 
from . import models

admin.site.register(models.User)
admin.site.register(models.Repository)
admin.site.register(models.Commit)
admin.site.register(models.File)
admin.site.register(models.Issue)
admin.site.register(models.Comment)

admin.site.header = 'Stengah Administration'
admin.site.title = 'Stengah Administration'
