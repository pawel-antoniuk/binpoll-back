from django.shortcuts import render
from rest_framework import viewsets
from data_collector.serializers import PollDataSerialier
from data_collector.models import PollData

class PollDataViewSet(viewsets.ModelViewSet):
    queryset = PollData.objects.all()
    serializer_class = PollDataSerialier
    