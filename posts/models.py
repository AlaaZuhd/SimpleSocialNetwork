from django.db import models
from helpers.extra_models import CreatedDateModel
from profile_app.models import Profile

# Create your models here.


class Post(CreatedDateModel):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=300)
    owner = models.ForeignKey(Profile, related_name='posts', on_delete=models.CASCADE)

    def __str__(self):
        return self.owner.__str__()

    def create(self, request_user, validated_data):
        post = Post(**validated_data)
        post.owner = Profile.objects.get(account__user=request_user)
        print(post)
        post.save()
        return post


class Comment(CreatedDateModel):
    content = models.CharField(max_length=300)
    owner = models.ForeignKey(Profile, null=True, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    def create(self, request_user, post_id, validated_data):
        comment = Comment(**validated_data)
        comment.owner = Profile.objects.get(account__user=request_user)
        comment.post = Post.objects.filter(id=post_id).first()
        comment.save()
        return comment


class Like(models.Model):
    owner = models.ForeignKey(Profile, null=True, related_name='likes_owner', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, related_name='likes_owner', on_delete=models.CASCADE)

    def create(self, request_user, post_id, validated_data):
        like = Like(**validated_data)
        like.owner = Profile.objects.get(account__user=request_user)
        like.post = Post.objects.filter(id=post_id).first()
        like.save()
        return like

    def get_likes_count(self, post):
        return Like.objects.filter(post__id=post.id).count()

