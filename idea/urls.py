from django.urls import path
from .views import *

urlpatterns = [
    path('create/', IdeaCreate.as_view(), name='idea-create'),
    path('ideas/<int:pk>/like/', IdeaLikeView.as_view(), name='idea-like'),
    path('ideas/<int:pk>/delite-like/', IdeaDeliteLikeView.as_view(), name='idea-like-delite'),
    path('ideas/<int:pk>/comment/', IdeaCommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/like/', IdeaCommentLikeView.as_view(), name='comment-like'),
    path('ideas/<int:pk>/supporter/', IdeaSupporterView.as_view(), name='idea-supporter'),
    path('ideas/<int:pk>/supporter-decline/', IdeaSupporterDeclineView.as_view(), name='idea-supporter-decline'),
    path('all-user-ideas/', UserIdeasView.as_view(), name='user-ideas'),
    # path('ideas/<int:idea_id>/comment/<int:parent_comment_id>/comment/', CommentReplyCreateView.as_view(),name='comment_reply_create'),
    path('ideas/<int:pk>/show-comments/', IdeaAllCommentsView.as_view(), name='idea-without-comments'),
    path('get-idea/<int:pk>/', IdeaDetailView.as_view(), name='idea-detail'),
    path('all-ideas/', IdeaAllView.as_view(), name='idea-detail'),
]
