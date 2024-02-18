from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField

from idea.models import Idea
from startappmania import settings
from team.models import Team


# Create your models here.

class Works(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_works', null=True)
    name = models.CharField(max_length=70, blank=True)
    logo = models.ImageField(upload_to='avatars/', null=True, blank=True)
    link = models.URLField(blank=True)


class Socials(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_socials', null=True)
    name = models.CharField(max_length=70, blank=True)
    logo = models.ImageField(upload_to='avatars/', null=True, blank=True)
    link = models.URLField(blank=True)


class CustomUsers(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50, blank=True)
    second_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmation_code = models.CharField(max_length=20, blank=True)
    skills = models.TextField(blank=True)
    tags = models.CharField(max_length=200, blank=True)
    works = models.ForeignKey(Works, on_delete=models.CASCADE, null=True, blank=True)
    socials = models.ForeignKey(Socials, on_delete=models.CASCADE, null=True, blank=True)
    ideas = models.ManyToManyField(Idea, related_name='idea',blank=True)
    teams = models.ManyToManyField(Team, related_name='members', blank=True)



    def __str__(self):
        return self.username

    def generate_confirmation_code(self):
        code = get_random_string(length=20)
        return ConfirmationCode.objects.create(user=self, code=code)

    @property
    def invitations(self):
        return self.received_invitations.all()


class ConfirmationCode(models.Model):
    user = models.ForeignKey('CustomUsers', on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.code}"




# class Friendship(models.Model):
#     sender = models.ForeignKey(CustomUsers, related_name='sent_invitations', on_delete=models.CASCADE)
#     receiver = models.ForeignKey(CustomUsers, related_name='received_invitations', on_delete=models.CASCADE)
#     status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ['sender', 'receiver']
