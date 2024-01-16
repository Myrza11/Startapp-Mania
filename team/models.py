# Ваш файл models.py

from django.db import models
from django.conf import settings


class Team(models.Model):
    name = models.CharField(max_length=50)
    discribtion = models.TextField()
    idea = models.OneToOneField(Idea)
    team_logo = models.ImageField(upload_to='team-logo/', null=True, blank=True)
    captain = models.ForeignKey(settings.CustomUsers, on_delete=models.CASCADE)


class Invitation(models.Model):
    PENDING = 'Pending'
    ACCEPTED = 'Accepted'
    DECLINED = 'Declined'

    INVITATION_STATUS_CHOICES = [
        (ACCEPTED, 'accepted'),
        (DECLINED, 'declined'),
        (PENDING, 'pending')

    ]

    user = models.ForeignKey(settings.CustomUsers, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    invitation_status = models.CharField(max_length=20, choices=INVITATION_STATUS_CHOICES, default=PENDING)

    def accept(self):
        if self.invitation_status == Invitation.ACCEPTED:
            self.team.participants.add(self.user)
            self.team.save()

    def decline(self):
        if self.invitation_status == Invitation.PENDING:
            self.invitation_status = Invitation.DECLINED
            self.save()


class Chat(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='chats')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chats')


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class UnreadMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='unread_messages')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='unread_users')
