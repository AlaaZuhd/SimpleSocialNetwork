from django.shortcuts import render
from rest_framework.response import Response

from django.contrib.auth.models import User
from rest_framework import viewsets, status
from account.models import Account
from helpers.permissions import IsAuthenticated, IsOwner
from .models import Profile
from .serializers import ProfileSerializer
# Create your views here.


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.filter(account__user__is_active=True)# update, list, retreive and destroy active users.
    serializer_class = ProfileSerializer
    #authentication_classes = [IsAuthenticated]
    #permission_classes = [IsAuthenticated and (IsOwner)]



    def get_permissions(self):
        if self.action == 'post':
            permission_classes = []
        elif self.action == 'update':
            permission_classes = [IsAuthenticated and (IsOwner)]
        else: # come back for ths permission
            permission_classes = []
        return [permission() for permission in permission_classes]

    def get_object(self):
        if self.kwargs.get('pk', None) == 'me':
            self.kwargs['pk'] = Profile.objects.get(account__user__id =self.request.user.pk).id
        return super(ProfileViewSet, self).get_object()

    def list(self, request, *args, **kwargs):
        pass

    def create(self, request, *args, **kwargs):
        # get the registered account for this profile
        user = User.objects.get(id=request.user.id)
        Profile.create(self, request.user, request.data)
        response = {
            'status': status.HTTP_201_CREATED,
            'code': status.HTTP_201_CREATED,
            'message': 'Profile Created Successfully',
            'data': [],
            'ok': True
        }
        return Response(response)

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        if kwargs.get('bio', None) != None:
            profile.bio = kwargs['bio']
        if kwargs.get('address', None) != None:
            profile.address = kwargs['address']
        return Response({"Message": ProfileSerializer(profile).data})

