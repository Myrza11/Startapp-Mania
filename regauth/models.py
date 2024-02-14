from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField

from idea.models import Idea
from team.models import Team


# Create your models here.


class CustomUsers(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50, blank=True)
    second_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmation_code = models.CharField(max_length=20, blank=True)
    ability = models.TextField(blank=True)
    link = models.CharField(max_length=50, blank=True)
    link_name = models.CharField(max_length=50, blank=True)


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