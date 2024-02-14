from django.urls import path
from .views import *



urlpatterns = [
    path('create-event/', EventCreateView.as_view()),
    path('update-event/<int:pk>', EventUpdateView.as_view()),
    path('list-event/', EventListView.as_view()),
    path('destroy-event/<int:pk>', EventDestroyView.as_view()),
    path('create-eventstage/', EventStageCreateView.as_view()),
    path('update-eventstage/<int:pk>', EventStageUpdateView.as_view()),
    path('list-eventstage/', EventStageListView.as_view()),
    path('destroy-eventstage/<int:pk>', EventStageDestroyView.as_view()),
    path('create-stgerating/', StageRatingCreateView.as_view()),
    path('update-stgerating/<int:pk>', StageRatingUpdateView.as_view()),
    path('list-stgerating/', StageRatingListView.as_view()),
    path('destroy-stgerating/<int:pk>', StageRatingDestroyView.as_view()),
    ]