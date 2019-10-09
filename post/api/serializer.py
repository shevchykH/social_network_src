from rest_framework import serializers

from post.models import PostModel


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['id', 'title', 'content', 'user']
        extra_kwargs = {'user': {'read_only': True}}


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['id', 'title', 'content', 'user', 'like']
        extra_kwargs = {
            'like': {'read_only': True},
            'user': {'read_only': True},
        }


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['like']
