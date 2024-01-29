# Ваш файл urls.py

from django.urls import path
from .views import SendMessageView, TeamInfo, CreateTeamFromIdea,UserTeamListView

urlpatterns = [
    path('<int:team_id>/send-message/<int:chat_id>/', SendMessageView.as_view(), name='send_message'),
    path('info/<int:team_id>/', TeamInfo.as_view(), name='info-team'),
    path('idea_id/<int:idea_id>/create-team/', CreateTeamFromIdea.as_view(), name='create_team_from_idea'),
    path('info/', UserTeamListView.as_view(), name='view'),



]
