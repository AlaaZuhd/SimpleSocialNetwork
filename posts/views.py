from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.response import Response

from helpers.permissions import IsAuthenticated, IsPostOwner
from posts.models import Post, Like, Comment
from posts.serializers import PostSerializer, LikeSerializer, CommentSerializer
from profile_app.models import Profile


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(owner__account__user__is_active=True)# update, list, retreive and destroy active users.
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action == 'post':
            permission_classes = []
        elif self.action == 'update' or self.action == 'destroy':
            print("whhh")
            permission_classes = [IsAuthenticated and (IsPostOwner)]
        else: # come back for ths permission
            permission_classes = []
        return [permission() for permission in permission_classes]

    # def get_object(self):
    #     if self.kwargs.get('pk', None) == 'me':
    #         self.kwargs['pk'] = Post.objects.get(prfile__account__user__id =self.request.user.pk).id
    #     return super(PostViewSet, self).get_object()

    def list(self, request, *args, **kwargs):
        if self.kwargs.get('pk', None) != None:
            post = Post.objects.get(id=self.kwargs['pk'])
            return Response(PostSerializer(post).data)
        else:
            return Response({"Message": "Error"})

    def destroy(self, request, *args, **kwargs):
        try:
            print("b\n\n")
            instance = self.get_object()
            print(instance)
            self.perform_destroy(instance)
        except Exception:
            return Response("Not Found")
        return Response("Post delete successfully")


    def create(self, request, *args, **kwargs):
        # get the registered account for this profile
        post = Post.create(self, request.user, request.data)
        response = {
            'status': status.HTTP_201_CREATED,
            'code': status.HTTP_201_CREATED,
            'message': 'Profile Created Successfully',
            'data': PostSerializer(post).data,
            'ok': True
        }
        return Response(response)



class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.filter(owner__account__user__is_active=True)# update, list, retreive and destroy active users.
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action == 'post':
            permission_classes = []
        else: # come back for ths permission
            permission_classes = []
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        if self.kwargs.get('post_id', None) != None:
            likes = Like.objects.filter(post__id=self.kwargs['post_id'])
            return Response(CommentSerializer(likes, many=True).data)
        else:
            return Response({"Message": "Error"})


    def create(self, request, *args, **kwargs):
        print(kwargs)
        if self.kwargs.get('post_id', None) != None:
            like = Like.create(self, request.user, kwargs['post_id'], request.data)
            response = {
                'status': status.HTTP_201_CREATED,
                'code': status.HTTP_201_CREATED,
                'message': 'Like added Successfully',
                'data': LikeSerializer(like).data,
                'ok': True
            }
            return Response(response)
        else:
            return Response({"Message": "Error"}) # will never occur


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(owner__account__user__is_active=True)# update, list, retreive and destroy active users.
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action == 'post':
            permission_classes = []
        else: # come back for ths permission
            permission_classes = []
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        if self.kwargs.get('post_id', None) != None:
            comments = Comment.objects.filter(post__id=self.kwargs['post_id'])
            return Response(CommentSerializer(comments, many=True).data)
        else:
            return Response({"Message": "Error"})


    def create(self, request, *args, **kwargs):
        print(kwargs)
        if self.kwargs.get('post_id', None) != None:
            comment = Comment.create(self, request.user, kwargs['post_id'], request.data)
            response = {
                'status': status.HTTP_201_CREATED,
                'code': status.HTTP_201_CREATED,
                'message': 'Comment added Successfully',
                'data': CommentSerializer(comment).data,
                'ok': True
            }
            return Response(response)
        else:
            return Response({"Message": "Error"}) # will never occur