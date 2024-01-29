from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from idea.models import Idea
from .models import Message, Chat, Team
from .serializers import MessageSerializer, TeamSerializer, TeamCreateSerializer
from django.shortcuts import get_object_or_404


class CreateTeamFromIdea(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TeamCreateSerializer

    def post(self, request, *args, **kwargs):
        idea_id = kwargs.get('idea_id')

        team_data = {
                    'name': request.data.get('name'),
                    'description': request.data.get('description',''),
                    'captain': request.user.pk,
                    'idea': idea_id,  # Используйте idea.id вместо жестко заданного значения
                    'supporters': request.data.get('supporters', [])  # Получаем supporters из request.data

        }

        try:
            idea = Idea.objects.get(pk=idea_id)
        except Idea.DoesNotExist:
            return Response({'detail': 'Идея с указанным ID не найдена'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=team_data)
        if serializer.is_valid():
            serializer.save(idea=idea, captain=request.user)
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


class TeamInfo(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_object(self):
        team_id = self.kwargs.get("team_id")
        return get_object_or_404(Team, id=team_id)


class UserTeamListView(generics.ListAPIView):
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Team.objects.filter(participants=user)


# class CreateTeamFromIdea(APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = TeamCreateSerializer
#
#     def post(self, request, idea_id):
#
#         idea = get_object_or_404(Idea, pk=idea_id)
#
#         name = request.data.get('name')
#         description = request.data.get('description', '')
#         supporters_ids = request.data.get('supporters', [])
#
#         team_data = {
#             'name': name,
#             'description': description,
#             'captain': request.user.pk,
#             'idea': idea.id,  # Используйте idea.id вместо жестко заданного значения
#         }
#
#         team_serializer = TeamCreateSerializer(data=team_data)
#         if team_serializer.is_valid():
#             team = team_serializer.save()
#             team_serializer.save_supporters(team, supporters_ids)
#             return Response(team_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(team_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
