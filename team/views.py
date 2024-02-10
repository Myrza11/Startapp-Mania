from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from idea.models import Idea
from regauth.models import CustomUsers
from .models import Message, Chat, Team, Invitation
from .serializers import MessageSerializer, TeamSerializer, TeamCreateSerializer, InvitationSerializer
from django.shortcuts import get_object_or_404


class CreateTeamFromIdea(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TeamCreateSerializer

    def post(self, request, *args, **kwargs):
        idea_id = request.data.get('idea_id')
        supporters = request.data.get('supporters', [])

        team_data = {
                    'name': request.data.get('name'),
                    'description': request.data.get('description', ''),
                    'captain': request.user.pk,
                    'idea': idea_id,

        }

        serializer = self.serializer_class(data=team_data)
        if serializer.is_valid():
            team = serializer.save(idea_id=idea_id, captain=request.user)
            for user_id in supporters:
                user = get_object_or_404(CustomUsers, id=user_id)
                Invitation.objects.create(recipient=user, team=team)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendMessageView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def post(self, request, *args, **kwargs):
        team_id = kwargs.get('team_id')
        chat_id = kwargs.get('chat_id')
        text = request.data.get('text')

        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({'detail': 'Команда не найдена'}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in team.participants.all():
            return Response({'detail': 'Вы не являетесь участником этой команды'}, status=status.HTTP_403_FORBIDDEN)

        try:
            chat = Chat.objects.get(pk=chat_id, team=team)
        except Chat.DoesNotExist:
            # Если чат не существует, создаем новый
            chat = Chat.objects.create(team=team)
            chat.users.set(team.participants.all())

        message = Message.objects.create(chat=chat, sender=request.user, text=text)
        serializer = MessageSerializer(message)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AcceptInvitationView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        invitation_id = request.data.get('invitation_id')

        try:
            invitation = Invitation.objects.get(pk=invitation_id, recipient=request.user)
        except Invitation.DoesNotExist:
            return Response({'detail': 'Приглашение не найдено'}, status=status.HTTP_404_NOT_FOUND)

        # Принятие приглашения
        invitation.accept()
        return Response({'detail': 'Приглашение принято'}, status=status.HTTP_200_OK)


class DeclineInvitationView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        invitation_id = request.data.get('invitation_id')
        try:
            invitation = Invitation.objects.get(pk=invitation_id, user=request.user)
        except Invitation.DoesNotExist:
            return Response({'detail': 'Приглашение не найдено'}, status=status.HTTP_404_NOT_FOUND)

        # Отклонение приглашения
        invitation.decline()
        return Response({'detail': 'Приглашение отклонено'}, status=status.HTTP_200_OK)


class UserInvitationListView(generics.ListAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Invitation.objects.filter(recipient=user)


class AllTeamsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class UserTeamListView(generics.ListAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Team.objects.filter(supporters=user)


class TeamInfo(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_object(self):
        team_id = self.kwargs.get("team_id")
        return get_object_or_404(Team, id=team_id)
