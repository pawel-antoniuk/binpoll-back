from django.db import models


class AudioSample(models.Model):
    id = models.AutoField(primary_key=True)
    filepath = models.CharField(max_length=256)
 
class AudioSet(models.Model):
    id = models.AutoField(primary_key=True)
    samples = models.ManyToManyField(AudioSample)

class PollData(models.Model):
    id = models.AutoField(primary_key=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    assigned_set = models.ForeignKey(AudioSet, on_delete=models.CASCADE)
    answer = models.CharField(max_length=512)
    user_agent = models.TextField()
    ip_address = models.GenericIPAddressField()
