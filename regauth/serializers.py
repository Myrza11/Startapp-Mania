from rest_framework import serializers
from .models import *
from django.core.validators import RegexValidator
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from rest_framework.validators import UniqueValidator
import re
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.password_validation import validate_password


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

    class Meta:
        model = CustomUsers
        fields = ['id', 'username', 'email', 'name', 'phone_number', 'avatar', 'confirmation_code', "avatar", 'password', 'password_confirm', 'created_at', 'is_active']

    def validate_password(self, data):
        if validate_password(data) is not None:
            raise serializers.ValidationError("Password min length is 8")
        return data

    def validate_email(self, data):
        # Проверка, что домен email'а - это Gmail
        if not re.match(r'^[^@]+@gmail\.com$', data):
            raise serializers.ValidationError("Only Gmail addresses are allowed.")
        return data

    def validate(self, data):
        
        # Проверяем, что пароли совпадают
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError("Passwords do not match.")

        return data
    
    def create(self, validated_data):
        confirmation_code = get_random_string(length=20)
        
        user = CustomUsers.objects.create_user(
            username=validated_data['username'],
            name=validated_data['name'],
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
        fields = ["id", "last_login", "is_superuser", "first_name", "last_name", "is_staff", "is_active", "date_joined", "username","name",
    "second_name",
    "email",
    "phone_number",
    "avatar",
    "created_at",
    "confirmation_code",
    "ability",
    "link",
    "link_name",
    "groups",
    "user_permissions"
                  ]


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = ['id', 'username', 'name', 'email', 'phone_number', 'avatar']

#
# class FriendshipSerializer(serializers.ModelSerializer):
#     sender = CustomUserSerializer()
#     receiver = CustomUserSerializer()
#
#     class Meta:
#         model = Friendship
#         fields = ['id', 'sender', 'receiver', 'status', 'created_at']
#
#
# class FriendshipCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Friendship
#         fields = ['sender', 'receiver', 'status']