from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.utils import json

from helpers.permissions import IsAuthenticated, IsOwner
from profile_app.models import Profile
from .models import Story
from .serializers import StorySerializer
# Create your views here.


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    parser_classes = (FormParser, MultiPartParser)

    def get_permissions(self):
        if self.action == 'post':
            permission_classes = [IsAuthenticated]
        else: # add IsFriend Permissions.
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        try:
            data = {'image': "", "content": ""}
            # print(request.FILES['image'])
            data['image'] = request.FILES["image"]
            # data['content'] = json.loads(request.data['data'])
            # print(data['content'])

            story = Story.create(self, request.user, data)
            # serializer = StorySerializer(story)
            # if serializer.is_valid():
            #     print("yes")
            # else:
            #     print("no")
        except Exception:
            return Response({"errorMessage": "Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(StorySerializer(story).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        return Response("Story has been created successfully", status=status.HTTP_204_NO_CONTENT)
