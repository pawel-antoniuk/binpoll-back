from django.db import models

class AudioSample(models.Model):
    id = models.AutoField(primary_key=True)
    filepath = models.CharField(max_length=256)

    def __str__(self):
        return 'Sample: {}'.format(self.filepath)
 
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

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    poll_data = models.ForeignKey(PollData, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return 'Comment: {}'.format(self.message)