from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny
from .serializers import *


class EventCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class EventUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class EventListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class EventDestroyView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class EventStageCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = EventStageSerializer
    queryset = EventStage.objects.all()


class EventStageUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = EventStageSerializer
    queryset = EventStage.objects.all()


class EventStageListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EventStageSerializer
    queryset = EventStage.objects.all()


class EventStageDestroyView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = EventStageSerializer
    queryset = EventStage.objects.all()


class StageRatingCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = StageRatingSerializer
    queryset = StageRating.objects.all()


class StageRatingUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = StageRatingSerializer
    queryset = StageRating.objects.all()


class StageRatingListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = StageRatingSerializer
    queryset = StageRating.objects.all()


class StageRatingDestroyView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = StageRatingSerializer
    queryset = StageRating.objects.all()
