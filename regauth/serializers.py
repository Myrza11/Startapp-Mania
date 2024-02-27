import os
from sqlite3 import IntegrityError
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
import phonenumbers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    username = serializers.CharField(
        validators=[RegexValidator(regex='^[a-zA-Z]*$', message='Only letters are allowed.')]
    )
    email = serializers.EmailField()
    name = serializers.CharField(max_length=50)
    phone_number = serializers.CharField()

    class Meta:
        model = CustomUsers
        fields = ['id', 'username', 'email', 'name', 'phone_number', 'avatar', 'confirmation_code', 'password', 'password_confirm', 'created_at', 'is_active']

    def validate_password(self, data):
        if len(data) < 8:
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
        try:
            existing_user = CustomUser.objects.get(email=validated_data['email'])
            raise serializers.ValidationError("User with this email already exists")
        except ObjectDoesNotExist:
            pass
        try:
            confirmation_code = get_random_string(length=20)

            works_data = validated_data.pop('works', None)
            socials_data = validated_data.pop('socials', None)

            phone_number = validated_data.get('phone_number')  # Получаем значение телефонного номера из данных, если оно существует

            if phone_number is None:  # Если телефонный номер отсутствует
                raise serializers.ValidationError("Phone number is required")

            # Парсинг телефонного номера с использованием phonenumbers
            parsed_phone_number = phonenumbers.parse(phone_number, None)

            user = CustomUsers.objects.create_user(
                username=validated_data['username'],
                name=validated_data['name'],
                email=validated_data['email'],
                password=validated_data['password'],
                phone_number=phone_number,  # Используем значение телефонного номера
                is_active=False,
                confirmation_code=confirmation_code,
            )

            if works_data:
                Works.objects.create(created_by=user, **works_data)

            if socials_data:
                Socials.objects.create(created_by=user, **socials_data)

            return user

        except IntegrityError:
            raise serializers.ValidationError("Email already exists")

    def validate_phone_number(self, value):
        if not value:
            raise serializers.ValidationError("Phone number is required")
        return value


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
        fields = ['id', 'name', 'link']

    def validate(self, data):
        name = data.get('name')
        link = data.get('link')

        if not name:
            raise serializers.ValidationError("Name field cannot be empty")

        if not link:
            raise serializers.ValidationError("Link field cannot be empty")

        return data

    def create(self, validated_data):
        link = validated_data.get('link', '')

        social_networks = {
            'github': 'github.com',
            'gitlab': 'gitlab.com',
            'figma': 'figma.com',
            # Другие социальные сети...
        }

        for network, url in social_networks.items():
            if url in link:
                validated_data['name'] = network
                break

        return super().create(validated_data)

    def get_social_network_logo(self, social_network):
        LOGO_DIR = 'logos/'
        # Маппинг логотипов для каждой социальной сети
        social_network_logos = {
            'github': 'github_logo.png',
            'gitlab': 'gitlab_logo.png',
            'figma': 'figma_logo.png',
            # Другие социальные сети...
        }
        logo_filename = social_network_logos.get(social_network)
        if logo_filename:
            # Полный путь к логотипу
            return os.path.join(LOGO_DIR, logo_filename)
        return None


class SocialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Socials
        fields = ['id', 'name', 'link']

    def validate(self, data):
        name = data.get('name')
        link = data.get('link')

        if not name:
            raise serializers.ValidationError("Name field cannot be empty")

        if not link:
            raise serializers.ValidationError("Link field cannot be empty")

        return data

    def create(self, validated_data):
        link = validated_data.get('link', '')

        social_networks = {
            'whatsapp': 'whatsapp.com',
            'instagram': 'instagram.com',
            'telegram': 'telegram.org',
            'gmail': 'gmail.com',
            # Другие социальные сети...
        }

        for network, url in social_networks.items():
            if url in link:
                validated_data['name'] = network
                break

        return super().create(validated_data)

    def get_social_network_logo(self, social_network):
        # Директория, в которой хранятся логотипы социальных сетей
        LOGO_DIR = 'logos/'
        # Маппинг логотипов для каждой социальной сети
        social_network_logos = {
            'whatsapp': 'whatsapp_logo.png',
            'instagram': 'instagram_logo.png',
            'telegram': 'telegram_logo.png',
            'gmail': 'gmail_logo.png',
        }
        logo_filename = social_network_logos.get(social_network)
        if logo_filename:
            # Полный путь к логотипу
            return os.path.join(LOGO_DIR, logo_filename)
        return None


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
        fields = ['id', 'username', 'name', 'second_name', 'email', 'phone_number', 'avatar',  'created_at', 'confirmation_code',  'is_active', 'skills', 'tags',  'teams', 'works', 'socials', 'ideas']



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