# Ваш файл urls.py

from django.urls import path
from .views import SendMessageView, TeamInfo, CreateTeamFromIdea, UserTeamListView, AcceptInvitationView, DeclineInvitationView, UserInvitationListView

urlpatterns = [
    path('<int:team_id>/send-message/<int:chat_id>/', SendMessageView.as_view(), name='send_message'),
    path('info/<int:team_id>/', TeamInfo.as_view(), name='info-team'),
    path('create-team/', CreateTeamFromIdea.as_view(), name='create_team_from_idea'),
    path('info/', UserTeamListView.as_view(), name='view'),
    path('invitation/accept/', AcceptInvitationView.as_view(), name='accept_invitation'),
    path('invitation/decline/', DeclineInvitationView.as_view(), name='decline_invitation'),
    path('invitation/user/', UserInvitationListView.as_view(), name='user_invitation_list'),



]
