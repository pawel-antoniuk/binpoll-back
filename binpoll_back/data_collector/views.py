from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from data_collector.serializers import PollDataSerialier
from data_collector.models import PollData
from rest_framework import mixins

class PollDataViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):

    queryset = PollData.objects.all()
    serializer_class = PollDataSerialier

    def create(self, request):
        data = {**request.data}
        data['user_agent'] = request.META['HTTP_USER_AGENT']
        data['ip_address'] = request.META['REMOTE_ADDR']

        serializer = PollDataSerialier(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        serializer = PollDataSerialier(self.queryset, many=True)
        return Response(serializer.data)
    