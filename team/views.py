# Ваш файл views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Message, Chat
from .serializers import MessageSerializer, ChatSerializer


from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Message, Chat, Team
from .serializers import MessageSerializer, ChatSerializer


class SendMessageView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def post(self, request, *args, **kwargs):
        chat_id = kwargs.get('chat_id')
        text = request.data.get('text')

        try:
            chat = Chat.objects.get(pk=chat_id)
        except Chat.DoesNotExist:
            # Если чат не существует, создаем новый
            team = Team.objects.filter(members=request.user).first()
            if not team:
                return Response({'detail': 'Пользователь не принадлежит ни к одной команде.'}, status=status.HTTP_400_BAD_REQUEST)

            chat = Chat.objects.create(team=team)
            chat.users.set(team.members.all())

        message = Message.objects.create(chat=chat, sender=request.user, text=text)
        serializer = MessageSerializer(message)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateTeamChatView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatSerializer

    def post(self, request, *args, **kwargs):
        team_chat = Chat.objects.create(team=request.user.team)
        team_chat.users.set(request.user.team.members.all())
        serializer = ChatSerializer(team_chat)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
