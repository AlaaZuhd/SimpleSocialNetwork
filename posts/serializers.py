from rest_framework import serializers
from .models import Post, Comment, Like




class PostSerializer(serializers.ModelSerializer):

    comments_count = serializers.SerializerMethodField('get_comments_count')
    likes_count = serializers.SerializerMethodField('get_likes_count')

    def get_likes_count(self, obj):
        return Like.objects.filter(post__id=obj.id).count()

    def get_comments_count(self, obj):
        return Comment.objects.filter(post__id=obj.id).count()

    class Meta:
        model = Post
        fields = '__all__'
        write_only_fields = ['title', 'content']
        read_only_fields = ['owner']


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ['owner', 'post']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ['owner', 'post']