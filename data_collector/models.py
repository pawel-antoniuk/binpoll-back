from django.db import models

class AudioSample(models.Model):
    id = models.AutoField(primary_key=True)
    filepath = models.CharField(max_length=256)

    def __str__(self):
        return 'Sample: {}'.format(self.filepath)
 
class AudioSet(models.Model):
    id = models.AutoField(primary_key=True)
    samples = models.ManyToManyField(AudioSample)

class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True)
    age = models.CharField(max_length=32)
    hearing_difficulties = models.BooleanField()
    listening_test_participated = models.BooleanField()
    headphones_make_and_model = models.CharField(max_length=512, blank=True, default='')

class PollData(models.Model):
    id = models.AutoField(primary_key=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    answer = models.CharField(max_length=512)
    assigned_set = models.ForeignKey(AudioSet, on_delete=models.CASCADE)
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    poll_data = models.ForeignKey(PollData, on_delete=models.CASCADE)
    message = models.TextField(max_length=1024)

    def __str__(self):
        return 'Comment: {}'.format(self.message)

class Problem(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.TextField(max_length=1024)
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def __str__(self):
        return 'Comment: {}'.format(self.message)
