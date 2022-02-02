import datetime

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.utils import json

from helpers.permissions import IsAuthenticated, IsOwner, IsStoryOwner
from profile_app.models import Profile
from simple_social_network import settings
from .models import Story
from .serializers import StorySerializer
# Create your views here.


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.filter(created_date__gt=timezone.now() - datetime.timedelta(hours=24))
    serializer_class = StorySerializer
    parser_classes = (FormParser, MultiPartParser)

    def get_permissions(self):
        if self.action == 'post' or self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated and IsStoryOwner]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        try:
            data = {'image': "", "content": ""}
            if request.FILES.get('image'):
                data['image'] = request.FILES["image"]
            if request.data.get('content'):
                data['content'] = request.data['content']
            story = Story.create(self, request.user, data)
        except Exception:
            return Response({"Message": Exception}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(self.get_serializer(story).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def friends_stories(self, request):
        #friends = Profile.objects.get(account__user=request.user).friends.all()
        #date_time_before_24_hours = timezone.now() - datetime.timedelta(hours=24)
        stories = self.get_queryset()#Story.objects.filter(created_date__gt=date_time_before_24_hours, owner__id__in=friends)
        paginator = PageNumberPagination()
        paginator.page_size = 2
        result_page = paginator.paginate_queryset(stories, request)
        serializer = self.get_serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def list(self, request, *args, **kwargs):
        # get user's friends
        friends = Profile.objects.get(account__user=request.user).friends.all()
        # then get stories for all friends
        #date_time_before_24_hours = timezone.now() - datetime.timedelta(hours=24)
        stories = self.get_queryset()#Story.objects.filter(created_date__gt=date_time_before_24_hours, owner__id__in=friends)
        page = self.paginate_queryset(stories)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(StorySerializer(stories, many=True).data)
