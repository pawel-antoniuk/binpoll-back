from rest_framework import serializers
from data_collector.models import PollData, AudioSet, AudioSample, Comment, UserInfo, Problem

class UserInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('id', 'user_agent', 'ip_address', 'age', 'hearing_difficulties',
                  'listening_test_participated', 'headphones_make_and_model')

class PollDataSerialier(serializers.HyperlinkedModelSerializer):
    assigned_set = serializers.PrimaryKeyRelatedField(queryset=AudioSet.objects.all())
    user_info = UserInfoSerializer(many=False)
    class Meta:
        model = PollData
        fields = ('id', 'start_date', 'end_date', 'assigned_set', 'answer',
                  'user_info')
    def create(self, validated_data):
        user_info = validated_data.pop('user_info')
        user_info_obj = UserInfo.objects.create(**user_info)
        user_info_obj.save()
        validated_data['user_info_id'] = user_info_obj.pk 
        poll_data = PollData.objects.create(**validated_data)
        return poll_data

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

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    poll_data = serializers.PrimaryKeyRelatedField(queryset=PollData.objects.all())
    class Meta:
        model = Comment
        fields = ('id', 'poll_data', 'message')

class ProblemSerializer(serializers.HyperlinkedModelSerializer):
    user_info = UserInfoSerializer(many=False)
    class Meta:
        model = Problem
        fields = ('id', 'message', 'user_info')
    def create(self, validated_data):
        user_info = validated_data.pop('user_info')
        user_info_obj = UserInfo.objects.create(**user_info)
        user_info_obj.save()
        validated_data['user_info_id'] = user_info_obj.pk 
        problem = Problem.objects.create(**validated_data)
        UserInfo.objects.create(**user_info)
        return problem