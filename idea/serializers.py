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
    user_liked = serializers.SerializerMethodField()
    is_supported = serializers.SerializerMethodField()

    class Meta:
        model = Idea
        fields = ['id', 'name', 'description', 'created_at', 'likes', 'created_by', 'supporters', 'comments', 'user_liked', 'tag', 'is_supported']

    def get_supporters(self, obj):
        return [user.id for user in obj.supporters.all()]

    def get_user_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return IdeaLikes.objects.filter(user=request.user, likes=obj).exists()
        return False

    def get_is_supported(self, obj):  # Метод для определения, поддерживает ли пользователь данную идею
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return IdeaSupporter.objects.filter(user=request.user, idea=obj).exists()
        return False

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        idea_comments = IdeaComment.objects.filter(idea=instance)
        comments_data = IdeaCommentSerializer(idea_comments, many=True).data
        representation['comments'] = comments_data
        return representation


