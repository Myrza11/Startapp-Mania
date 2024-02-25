
from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from idea.models import Idea
from regauth.models import CustomUsers
from .models import  Team, Invitation
from .serializers import TeamSerializer, TeamCreateSerializer, InvitationSerializer
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError


class CreateTeamFromIdea(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TeamCreateSerializer

    @extend_schema(tags=['TEAM'])
    def post(self, request, *args, **kwargs):
        idea_id = request.data.get('idea_id')
        supporters = request.data.get('supporters', [])

        idea = get_object_or_404(Idea, pk=idea_id)
        supported_users = idea.supporters.all()
        for user_id in supporters:
            if user_id not in supported_users.values_list('id', flat=True):
                raise ValidationError({'detail': 'Пользователь {} не поддерживает данную идею.'.format(user_id)})

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


class SendTeamInvitation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        team_id = request.data.get('team_id')  # предположим, что у вас есть URL с team_id

        team = Team.objects.get(id=team_id)
        if team.captain != request.user:
            return Response({'detail': 'У вас нет прав на отправку приглашения в эту команду.'}, status=status.HTTP_403_FORBIDDEN)

        invitation = Invitation.objects.create(sender=request.user, recipient_id=user_id, team_id=team_id)

        serializer = InvitationSerializer(invitation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AcceptInvitationView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(tags=['TEAM'])
    def post(self, request, *args, **kwargs):
        invitation_id = request.data.get('invitation_id')

        try:
            invitation = Invitation.objects.get(pk=invitation_id, recipient=request.user)
        except Invitation.DoesNotExist:
            return Response({'detail': 'Приглашение не найдено'}, status=status.HTTP_404_NOT_FOUND)

        invitation.accept()
        return Response({'detail': 'Приглашение принято'}, status=status.HTTP_200_OK)


class DeclineInvitationView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(tags=['TEAM'])

    def post(self, request, *args, **kwargs):
        invitation_id = request.data.get('invitation_id')
        try:
            invitation = Invitation.objects.get(pk=invitation_id, user=request.user)
        except Invitation.DoesNotExist:
            return Response({'detail': 'Приглашение не найдено'}, status=status.HTTP_404_NOT_FOUND)

        invitation.decline()
        return Response({'detail': 'Приглашение отклонено'}, status=status.HTTP_200_OK)


class UserInvitationListView(generics.ListAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(tags=['TEAM'])

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
    @extend_schema(tags=['TEAM'])

    def get_queryset(self):
        user = self.request.user
        return Team.objects.filter(supporters=user)


class TeamInfo(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    @extend_schema(tags=['TEAM'])

    def get_object(self):
        team_id = self.kwargs.get("team_id")
        return get_object_or_404(Team, id=team_id)
