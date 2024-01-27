# Ваш файл urls.py

from django.urls import path
from .views import SendMessageView, TeamInfo

urlpatterns = [
    path('<int:team_id>/send-message/<int:chat_id>/', SendMessageView.as_view(), name='send_message'),
    path('info/<int:team_id>/', TeamInfo.as_view(), name='info-team'),
]
