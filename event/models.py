
from django.db import models
from team.models import Team


class Event(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    started_at = models.DateTimeField()


class EventStage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    stage = models.CharField(max_length=50)


class StageRating(models.Model):
    stage = models.ForeignKey(EventStage, on_delete=models.CASCADE)
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    rating = models.IntegerField()