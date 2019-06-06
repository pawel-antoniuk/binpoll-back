from rest_framework import serializers
from data_collector.models import PollData, AudioSet, AudioSample

class PollDataSerialier(serializers.HyperlinkedModelSerializer):
    assigned_set = serializers.PrimaryKeyRelatedField(queryset=AudioSet.objects.all())
    class Meta:
        model = PollData
        fields = ('id', 'start_date', 'end_date', 'assigned_set', 'answer', 'user_agent', 'ip_address')

class AudioSampleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AudioSample
        fields = ('id', 'filepath')

class AudioSetSerializer(serializers.HyperlinkedModelSerializer):
    # samples = AudioSampleSerializer(many=True, read_only=True)
    samples = serializers.SlugRelatedField(many=True, read_only=True, slug_field='filepath')
    class Meta:
        model = AudioSet
        fields = ('id', 'samples')
