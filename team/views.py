from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Message, Chat, Team
from .serializers import MessageSerializer, TeamSerializer


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
