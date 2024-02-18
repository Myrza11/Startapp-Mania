from rest_framework import serializers
from .models import *
from django.core.validators import RegexValidator
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from rest_framework.validators import UniqueValidator
import re
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.password_validation import validate_password
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from .models import CustomUsers, Works, Socials
from idea.serializers import IdeaSerializer
from team.serializers import TeamSerializer


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
        fields = ['id', 'username', 'email', 'name', 'phone_number', 'avatar', 'confirmation_code',  'password', 'password_confirm', 'created_at', 'is_active']

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
    
    def create(self, validated_data):
        confirmation_code = get_random_string(length=20)

        works_data = validated_data.pop('works', None)  # Получаем данные о работах (если есть)
        socials_data = validated_data.pop('socials', None)
        
        user = CustomUsers.objects.create_user(
            username=validated_data['username'],
            name=validated_data['name'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            phone_number=validated_data['phone_number'],
            is_active=False,
            confirmation_code=confirmation_code,
        )

        if works_data:
            Works.objects.create(created_by=user, **works_data)

        if socials_data:
            Socials.objects.create(created_by=user, **socials_data)

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


class WorksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Works
        fields = ['id', 'name', 'logo', 'link']


class SocialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Socials
        fields = ['id', 'name', 'logo', 'link']


class UserSerializer(serializers.ModelSerializer):
    ideas = serializers.SerializerMethodField()
    works = serializers.SerializerMethodField()
    socials = serializers.SerializerMethodField()
    teams = serializers.SerializerMethodField()

    def get_ideas(self, obj):
        ideas = Idea.objects.filter(created_by=obj)
        serializer = IdeaSerializer(ideas, many=True)
        return serializer.data

    def get_works(self, obj):
        works = Works.objects.filter(created_by=obj)
        serializer = WorksSerializer(works, many=True)
        return serializer.data

    def get_socials(self, obj):
        socials = Socials.objects.filter(created_by=obj)
        serializer = SocialsSerializer(socials, many=True)
        return serializer.data

    def get_teams(self, obj):
        teams = Team.objects.filter(supporters=obj)
        serializer = TeamSerializer(teams, many=True)
        return serializer.data

    class Meta:
        model = CustomUsers
        fields = ['id', 'username', 'name', 'second_name', 'email', 'phone_number', 'avatar', 'created_at', 'confirmation_code',  'is_active', 'skills', 'tags',  'teams', 'works', 'socials', 'ideas']



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