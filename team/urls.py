# Ваш файл urls.py

from django.urls import path
from .views import SendMessageView, TeamInfo, CreateTeamFromIdea, UserTeamListView, AcceptInvitationView, \
    DeclineInvitationView, UserInvitationListView, AllTeamsListView

urlpatterns = [
    path('create-team/', CreateTeamFromIdea.as_view(), name='create_team_from_idea'),
    path('user-teams-info/', UserTeamListView.as_view(), name='view'),
    path('all-teams/', AllTeamsListView.as_view(), name='all_teams_list'),
    path('info/<int:team_id>/', TeamInfo.as_view(), name='info-team'),
    path('invitation/accept/', AcceptInvitationView.as_view(), name='accept_invitation'),
    path('invitation/decline/', DeclineInvitationView.as_view(), name='decline_invitation'),
    path('invitation/user/', UserInvitationListView.as_view(), name='user_invitation_list'),
    path('<int:team_id>/send-message/<int:chat_id>/', SendMessageView.as_view(), name='send_message'),
]
