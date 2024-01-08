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
        fields = '__all__'

    def get_replies(self, obj):
        replies = IdeaComment.objects.filter(parent_comment=obj)
        return IdeaCommentSerializer(replies, many=True).data

    def get_likes_count(self, obj):
        return IdeaCommentLikes.objects.filter(comment=obj).count()


class IdeaSerializer(serializers.ModelSerializer):
    comments = IdeaCommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    supporters_count = serializers.SerializerMethodField()

    class Meta:
        model = Idea
        fields = '__all__'

    def get_likes_count(self, obj):
        return IdeaLikes.objects.filter(likes=obj).count()

    def get_supporters_count(self, obj):
        return IdeaSupporter.objects.filter(idea=obj).count()
