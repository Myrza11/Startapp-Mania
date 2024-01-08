from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Idea, IdeaLikes, IdeaComment, IdeaCommentLikes, IdeaSupporter
from .serializers import IdeaSerializer, IdeaCommentSerializer, IdeaSupporterSerializer
from rest_framework.permissions import IsAuthenticated


class CommentReplyCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IdeaCommentSerializer

    def post(self, request, *args, **kwargs):
        idea_id = kwargs.get('idea_id')
        parent_comment_id = kwargs.get('parent_comment_id')
        user = request.user

        serializer_data = {
            'idea': idea_id,
            'user': user.id,
            'text': request.data.get('text'),
            'parent_comment': parent_comment_id
        }
        serializer = self.serializer_class(data=serializer_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IdeaCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IdeaSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        request_data = request.data.copy()
        request_data['created_by'] = user.id
        serializer = self.serializer_class(data=request_data)

        if serializer.is_valid():
            idea = serializer.save(created_by=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IdeaLikeView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IdeaSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        idea_id = kwargs.get('pk')
        idea = Idea.objects.get(pk=idea_id)

        if IdeaLikes.objects.filter(user=user, likes=idea).exists():
            return Response({'detail': 'You have already liked this idea.'}, status=status.HTTP_400_BAD_REQUEST)

        idea.likes += 1
        idea.save()

        IdeaLikes.objects.create(user=user, likes=idea)

        serializer = self.serializer_class(idea)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IdeaDetailView(generics.RetrieveAPIView):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class IdeaCommentCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IdeaCommentSerializer

    def post(self, request, *args, **kwargs):
        idea_id = kwargs.get('pk')
        idea = Idea.objects.get(pk=idea_id)
        user = request.user

        serializer_data = {'idea': idea.id, 'user': user.id, 'text': request.data.get('text')}
        serializer = self.serializer_class(data=serializer_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IdeaCommentLikeView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IdeaCommentSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        comment_id = kwargs.get('pk')
        comment = IdeaComment.objects.get(pk=comment_id)

        if IdeaCommentLikes.objects.filter(user=user, comment=comment).exists():
            return Response({'detail': 'You have already liked this comment.'}, status=status.HTTP_400_BAD_REQUEST)

        IdeaCommentLikes.objects.create(user=user, comment=comment)

        serializer = self.serializer_class(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IdeaSupporterView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IdeaSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        idea_id = kwargs.get('pk')
        idea = Idea.objects.get(pk=idea_id)

        if IdeaSupporter.objects.filter(user=user, idea=idea).exists():
            return Response({'detail': 'You have already supported this idea.'}, status=status.HTTP_400_BAD_REQUEST)

        IdeaSupporter.objects.create(user=user, idea=idea)

        serializer = self.serializer_class(idea)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserIdeasView(generics.ListAPIView):
    serializer_class = IdeaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Idea.objects.filter(created_by=user)
