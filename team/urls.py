# Ваш файл urls.py

from django.urls import path
from .views import SendMessageView, CreateTeamChatView

urlpatterns = [
    path('send-message/<int:chat_id>/', SendMessageView.as_view(), name='send_message'),
    path('create-team-chat/', CreateTeamChatView.as_view(), name='create_team_chat'),
]
