from django.db import models


class PollData(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    assigned_set_id = models.IntegerField()
    answer = models.CharField(max_length=512)
    user_agent = models.TextField()
    ip_address = models.GenericIPAddressField()

