from django.contrib import admin
from . import models

admin.site.register(models.PollData)
admin.site.register(models.AudioSample)
admin.site.register(models.AudioSet)
admin.site.register(models.Comment)

# Register your models here.
