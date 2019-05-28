from rest_framework import serializers
from data_collector.models import PollData

class PollDataSerialier(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PollData
        fields = ('start_date', 'end_date', 'assigned_set_id', 'answer')
