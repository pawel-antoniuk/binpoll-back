from django.contrib import admin
from . import models

admin.site.register(models.PollData)
admin.site.register(models.AudioSample)
admin.site.register(models.AudioSet)

# Register your models here.
