from django.db import models
from django.conf import settings
from idea.models import Idea


class Team(models.Model):
    name = models.CharField(max_length=50,  unique=True)
    description = models.TextField()
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE,  null=True, blank=True)
    team_logo = models.ImageField(upload_to='team-logo/', null=True, blank=True)
    captain = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, default=None)
    supporters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='supported_teams')


class Invitation(models.Model):
    PENDING = 'Pending'
    ACCEPTED = 'Accepted'
    DECLINED = 'Declined'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declined')
    ]

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_invitations', null=True, blank=True)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_invitations', null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    def accept(self):
        self.status = Invitation.ACCEPTED
        self.save()
        self.team.supporters.add(self.recipient)

    def decline(self):
        self.status = Invitation.DECLINED
        self.save()



