from .models import *
from rest_framework import serializers


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventStage
        fields = '__all__'


class StageRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageRating
        fields = '__all__'