from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from data_collector.serializers import PollDataSerialier, AudioSetSerializer, CommentSerializer
from data_collector.models import PollData, AudioSet, Comment
from rest_framework import mixins
from django.shortcuts import get_object_or_404

class PollDataViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):

    queryset = PollData.objects.all()
    serializer_class = PollDataSerialier

    def create(self, request, *args, **kwargs):
        data = {**request.data}
        data['user_agent'] = request.META['HTTP_USER_AGENT']
        data['ip_address'] = request.META['REMOTE_ADDR']
        data['assigned_set'] = data['assigned_set_id']

        serializer = PollDataSerialier(data=data)        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        serializer = PollDataSerialier(self.queryset, many=True)
        return Response(serializer.data)
    
class AudioSetViewSet(mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    
    queryset = AudioSet.objects.all()
    serializer_class = AudioSetSerializer

    def get(self, request):
        audio_set = get_object_or_404(self.queryset, pk=1)
        serializer = AudioSetSerializer(audio_set)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        serializer = AudioSetSerializer(self.queryset, many=True)
        return Response(serializer.data)

class CommentViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    
    queryset = Comment.objects.all()
    serializer_class = Comment

    def create(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)        
        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)