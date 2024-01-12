from rest_framework import serializers
from .models import CustomUsers
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from rest_framework.validators import UniqueValidator
import re
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.password_validation import validate_password
from urllib.parse import urlparse


class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    username = serializers.CharField(
        validators=[RegexValidator(regex='^[a-zA-Z]*$', message='Only letters are allowed.'),
                    UniqueValidator(queryset=CustomUsers.objects.all(), message='This username is already in use.')]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=CustomUsers.objects.all(), message='This email is already in use.')
        ]
    )
    phone_number = PhoneNumberField()
    name = serializers.CharField(max_length=50)
    surename = serializers.CharField(max_length=50)
    social_media = serializers.CharField(required=False)


    class Meta:
        model = CustomUsers
        fields = ['id', 'username', 'email', 'name', 'phone_number', 'avatar', 'confirmation_code', "avatar", 'password', 'password_confirm', 'created_at', 'is_active', 'surename', 'social_media']

    def validate_password(self, data):
        if validate_password(data) is not None:
            raise serializers.ValidationError("Password min length is 8")
        return data

    def validate_email(self, data):
        if not re.match(r'^[^@]+@gmail\.com$', data):
            raise serializers.ValidationError("Only Gmail addresses are allowed.")
        return data

    def validate(self, data):
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError("Passwords do not match.")
        return data
        
    def input_social_link(self, data):
        while True:
            social_link = data
            parsed_url = urlparse(social_link)
            
            # Проверяем, что введенная строка имеет схему http или https и хост не пустой
            if parsed_url.scheme in ['http', 'https'] and parsed_url.netloc:
                return social_link
            else:
                print("Неправильный формат ссылки. Пожалуйста, введите корректную ссылку.")
    
    def create(self, validated_data):
        confirmation_code = get_random_string(length=20)
        
        user = CustomUsers.objects.create_user(
            username=validated_data['username'],
            name=validated_data['name'],
            surename=validated_data['surename'],
            social_media=validated_data.get('social_media', ''),
            email=validated_data.get('email'),
            password=validated_data['password'],
            phone_number=validated_data['phone_number'],
            is_active=False, 
            confirmation_code=confirmation_code,
        )

        subject = 'Confirmation code'
        message = f'Your confirmation code is: {confirmation_code}'
        from_email = 'bapaevmyrza038@gmail.com'
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return user
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ChangeUsernameSerializer(serializers.Serializer):
    new_username = serializers.CharField(required=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    new_password = serializers.CharField(write_only=True, required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = '__all__'