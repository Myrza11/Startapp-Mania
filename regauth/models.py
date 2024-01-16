from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class CustomUsers(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField()
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmation_code = models.CharField(max_length=20, blank=True)

    
    def __str__(self):
        return self.username

    def generate_confirmation_code(self):
        code = get_random_string(length=20)
        return ConfirmationCode.objects.create(user=self, code=code)



class ConfirmationCode(models.Model):
    user = models.ForeignKey('CustomUsers', on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.code}"
    
