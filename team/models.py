# Ваш файл models.py

from django.db import models
from django.conf import settings


class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()


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
