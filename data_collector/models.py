from django.db import models

class AudioSample(models.Model):
    filepath = models.CharField(max_length=128, primary_key=True)

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
    answers = models.ManyToManyField(AudioSample, through='PollAnswer')
    assigned_set = models.ForeignKey(AudioSet, on_delete=models.CASCADE)
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

class PollAnswer(models.Model):
    sample = models.ForeignKey(AudioSample, on_delete=models.CASCADE)
    poll_data = models.ForeignKey(PollData, on_delete=models.CASCADE)
    answer_FB = models.CharField(max_length=32)
    answer_BF = models.CharField(max_length=32)
    answer_FF = models.CharField(max_length=32)
    class Meta:
        unique_together = (("sample", "poll_data"),)
    def __str__(self):
        return 'Answer: FB: {}, BF: {}, FF: {}'.format(self.answer_FB, self.answer_BF, self.answer_FF)

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
