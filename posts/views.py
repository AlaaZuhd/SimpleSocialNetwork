from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from helpers.permissions import IsAuthenticated, IsPostOwner, IsLikeOwner, IsCommentOwner
from posts.models import Post, Like, Comment
from posts.serializers import PostSerializer, LikeSerializer, CommentSerializer
from profile_app.models import Profile


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(owner__account__user__is_active=True)# update, list, retreive and destroy active users.
    serializer_class = PostSerializer

    # def get_serializer_class(self):
    #     if self.action == 'update' or self.action == 'partial_update':
    #         return PostUpdateSerializer
    #     else:
    #         return PostSerializer

    def get_permissions(self):
        if self.action == 'post':
            permission_classes = [IsAuthenticated]
        elif self.action == 'update' or self.action == 'destroy' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated and IsPostOwner]
        else: # come back for ths permission
            permission_classes = []
        return [permission() for permission in permission_classes]

    # def get_object(self):
    #     if self.kwargs.get('pk', None) == 'me':
    #         self.kwargs['pk'] = Post.objects.get(prfile__account__user__id =self.request.user.pk).id
    #     return super(PostViewSet, self).get_object()

    @action(detail=False, methods=['get'])
    def friends_posts(self, request):
        friends = Profile.objects.get(account__user__id=request.user.id).friends.all()
        print(friends)
        posts = Post.objects.filter(owner__id__in=friends)
        paginator = PageNumberPagination()
        paginator.page_size = 2
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)



    def create(self, request, *args, **kwargs):
        # get the registered account for this profile
        if request.data.get('title') and request.data.get('content'):
            post = Post.create(self, request.user, request.data)
            response = {
                'status': status.HTTP_201_CREATED,
                'code': status.HTTP_201_CREATED,
                'message': 'Post Created Successfully',
                'data': self.get_serializer(post).data,
                'ok': True
            }
            return Response(response)
        else:
            return Response({"Message": "both title and content fields are required"})



class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.filter(owner__account__user__is_active=True)# update, list, retreive and destroy active users.
    serializer_class = LikeSerializer

    def get_permissions(self):
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'delete':
            permission_classes = [IsAuthenticated and IsLikeOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        if self.kwargs.get('post_id'):
            likes = Like.objects.filter(post__id=self.kwargs['post_id'])
            print(likes)
        else:
            likes = Like.objects.all()
        page = self.paginate_queryset(likes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(self.get_serializer(likes, many=True).data)

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
            return Response({"Message": "You need to select a post to add like on"})


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(owner__account__user__is_active=True)# update, list, retreive and destroy active users.
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'delete':
            permission_classes = [IsAuthenticated and IsCommentOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        if self.kwargs.get('post_id'):
            comments = Comment.objects.filter(post__id=self.kwargs['post_id'])
        else:
            comments = Comment.objects.all()
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(self.get_serializer(comments, many=True).data)

    def create(self, request, *args, **kwargs):
        print(kwargs)
        if self.kwargs.get('post_id'):
            comment = Comment.create(self, request.user, kwargs['post_id'], request.data)
            response = {
                'status': status.HTTP_201_CREATED,
                'code': status.HTTP_201_CREATED,
                'message': 'Comment added Successfully',
                'data': self.get_serializer(comment).data,
                'ok': True
            }
            return Response(response)
        else:
            return Response({"Message": "You need to select a post to add a comment on"})