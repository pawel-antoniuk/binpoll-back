from django.shortcuts import render
from rest_framework import viewsets, status, views
from rest_framework.response import Response
from data_collector.serializers import PollDataSerialier, AudioSetSerializer
from data_collector.serializers import CommentSerializer, ProblemSerializer, SummarySerializer
from data_collector.models import PollData, AudioSet, Comment, Problem, UserInfo, PollAnswer
from rest_framework import mixins
from django.shortcuts import get_object_or_404
import random

class PollDataViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):

    queryset = PollData.objects.all()
    serializer_class = PollDataSerialier

    def create(self, request, *args, **kwargs):
        data = {**request.data}
        data['user_info']['user_agent'] = request.META['HTTP_USER_AGENT']
        data['user_info']['ip_address'] = request.META['REMOTE_ADDR']
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

    def get(self, request, *args, **kwargs):
        audio_set = get_object_or_404(self.queryset, pk=1)
        serializer = AudioSetSerializer(audio_set)
        random.shuffle(serializer.data['samples'])
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        serializer = AudioSetSerializer(self.queryset, many=True)
        return Response(serializer.data)

class CommentViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)        
        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ProblemViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    def create(self, request, *args, **kwargs):
        data = {**request.data}
        data['user_info']['user_agent'] = request.META['HTTP_USER_AGENT']
        data['user_info']['ip_address'] = request.META['REMOTE_ADDR']

        serializer = ProblemSerializer(data=data)        
        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class SummaryView(views.APIView):
    @staticmethod
    def generate_answer(poll_datas, name, append_filter):
        answer = {}
        answer['sample'] = name
        answer['user_answers'] = []
        for poll_data in poll_datas:
            answer['user_answers'].append(append_filter(poll_data))
        return answer

    def get(self, request, pk=None, *args, **kwargs):
        answers = []
        audio_set = AudioSet.objects.get(pk=pk)
        poll_datas = PollData.objects.filter(assigned_set_id=pk)
        
        for sample in audio_set.samples.all():
            answer = {}
            
            # FB
            answer['sample'] = sample.filepath + "_scene1_FB.wav"
            answer['user_answers'] = []
            for poll_data in poll_datas:
                poll_answer = PollAnswer.objects.get(sample_id=sample.filepath, poll_data_id=poll_data.pk)
                answer['user_answers'].append(poll_answer.answer_FB)
            answers.append(answer)

            # BF
            answer['sample'] = sample.filepath + "_scene2_BF.wav"
            answer['user_answers'] = []
            for poll_data in poll_datas:
                poll_answer = PollAnswer.objects.get(sample_id=sample.filepath, poll_data_id=poll_data.pk)
                answer['user_answers'].append(poll_answer.answer_BF)

            # FF
            answer['sample'] = sample.filepath + "_scene3_FF.wav"
            answer['user_answers'] = []
            for poll_data in poll_datas:
                poll_answer = PollAnswer.objects.get(sample_id=sample.filepath, poll_data_id=poll_data.pk)
                answer['user_answers'].append(poll_answer.answer_FF)

        # answer_id
        answer = SummaryView.generate_answer(poll_datas, 'answer_id', lambda poll_data : poll_data.id)
        answers.append(answer)
        # ip addr
        answer = SummaryView.generate_answer(poll_datas, 'ip_addr', lambda poll_data : poll_data.user_info.ip_address)
        answers.append(answer)
        # start date
        answer = SummaryView.generate_answer(poll_datas, 'start_date', lambda poll_data : poll_data.start_date)
        answers.append(answer)
        # age
        answer = SummaryView.generate_answer(poll_datas, 'age', lambda poll_data : poll_data.user_info.age)
        answers.append(answer)
        # hearing_difficulties
        answer = SummaryView.generate_answer(poll_datas, 'hearing_difficulties', lambda poll_data : poll_data.user_info.hearing_difficulties)
        answers.append(answer)
        # listening_test_participated
        answer = SummaryView.generate_answer(poll_datas, 'listening_test_participated', lambda poll_data : poll_data.user_info.listening_test_participated)
        answers.append(answer)
        # headphones_make_and_model
        answer = SummaryView.generate_answer(poll_datas, 'headphones_make_and_model', lambda poll_data : poll_data.user_info.headphones_make_and_model)
        answers.append(answer)

        result = SummarySerializer(answers, many=True).data
        return Response(result)
    
    
