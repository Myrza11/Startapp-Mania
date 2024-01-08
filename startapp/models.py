from django.db import models
from django.conf import settings
from authapp.models import CustomUser


class Idea(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)  # Измените это поле на IntegerField
    supporters = models.ManyToManyField(settings.AUTH_USER_MODEL, through='IdeaSupporter', related_name='supported_ideas', blank=True)
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL, through='IdeaComment', related_name='idea_comments')


class IdeaSupporter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, related_name='idea_supporters', on_delete=models.CASCADE)
    supported_at = models.DateTimeField(auto_now_add=True)


class IdeaComment(models.Model):
    idea = models.ForeignKey('Idea', related_name='comment_ideas', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)


class IdeaLikes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.ForeignKey(Idea, related_name='idea_likes', on_delete=models.CASCADE)


class IdeaCommentLikes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(IdeaComment, related_name='comment_likes', on_delete=models.CASCADE)
