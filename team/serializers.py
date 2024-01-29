# Ваш файл serializers.py

from rest_framework import serializers
from .models import Message, Chat, Team
from regauth.models import CustomUsers


class TeamCreateSerializer(serializers.ModelSerializer):
    supporters = serializers.PrimaryKeyRelatedField(queryset=CustomUsers.objects.all(), many=True, required=False)

    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'team_logo', 'captain', 'supporters')

    def create(self, validated_data):
        supporters_data = validated_data.pop('supporters', [])
        team = Team.objects.create(**validated_data)
        team.supporters.set(supporters_data)
        return team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
