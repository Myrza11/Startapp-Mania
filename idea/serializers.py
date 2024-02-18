from rest_framework import serializers
from .models import Idea, IdeaComment, IdeaSupporter, IdeaLikes, IdeaCommentLikes


class IdeaSupporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdeaSupporter
        fields = '__all__'


class IdeaCommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = IdeaComment
        fields = ["id", "likes_count", "replies", "text", "created_at", "idea", "user", "parent_comment"]

    def get_replies(self, obj):
        if obj and isinstance(obj, IdeaComment):
            replies = IdeaComment.objects.filter(parent_comment=obj)
            return IdeaCommentSerializer(replies, many=True).data
        return []

    def get_likes_count(self, obj):
        if isinstance(obj, IdeaComment):
            return IdeaCommentLikes.objects.filter(comment=obj).count()
        return 0

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        return representation


class IdeaSerializer(serializers.ModelSerializer):
    supporters = serializers.SerializerMethodField()

    class Meta:
        model = Idea
        fields = ['id', 'name', 'description', 'created_at', 'likes', 'created_by', 'supporters', 'comments']

    def get_supporters(self, obj):
        return [user.username for user in obj.supporters.all()]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        idea_comments = IdeaComment.objects.filter(idea=instance)
        comments_data = IdeaCommentSerializer(idea_comments, many=True).data
        representation['comments'] = comments_data
        return representation


