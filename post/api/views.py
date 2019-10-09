from rest_framework import generics
from rest_framework.response import Response

from post.models import PostModel
from post.api.serializer import PostSerializer, PostDetailSerializer, PostLikeSerializer


class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return PostModel.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostDetailSerializer


class PostLike(generics.UpdateAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostLikeSerializer

    def update(self, request, *args, **kwargs):
        user = request.user
        post = self.get_object()
        qs = post.like.filter(id=user.id)
        if not qs.exists():
            post.like.add(user)
        return Response(status=200)


class PostUnlike(generics.UpdateAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostLikeSerializer

    def update(self, request, *args, **kwargs):
        user = request.user
        post = self.get_object()
        qs = post.like.filter(id=user.id)
        if qs.exists():
            post.like.remove(user)
        return Response(status=200)
