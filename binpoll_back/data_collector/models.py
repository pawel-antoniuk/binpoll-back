from django.db import models
from django.core import validators

class PollData(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    assigned_set_id = models.IntegerField()
    answer = models.CharField(max_length=256, 
        validators=[validators.validate_comma_separated_integer_list])
    user_agent = models.TextField()
    ip_address = models.GenericIPAddressField()

