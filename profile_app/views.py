from django.shortcuts import render
from rest_framework.response import Response

from django.contrib.auth.models import User
from rest_framework import viewsets, status
from account.models import Account
from helpers.permissions import IsAuthenticated, IsOwner, IsProfileOwner
from .models import Profile
from .serializers import ProfileSerializer
# Create your views here.


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.filter(account__user__is_active=True)# update, list, retreive and destroy active users.
    serializer_class = ProfileSerializer
    #authentication_classes = [IsAuthenticated]
    #permission_classes = [IsAuthenticated and (IsOwner)]



    def get_permissions(self):
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'delete':
            permission_classes = [IsAuthenticated and IsProfileOwner]
        else: # come back for ths permission
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_object(self):
        if self.kwargs.get('pk', None) == 'me':
            self.kwargs['pk'] = Profile.objects.get(account__user__id =self.request.user.pk).id
        return super(ProfileViewSet, self).get_object()

    def create(self, request, *args, **kwargs):
        profile = Profile.create(self, request.user, request.data)
        response = {
            'status': status.HTTP_201_CREATED,
            'code': status.HTTP_201_CREATED,
            'message': 'Profile Created Successfully',
            'data': self.get_serializer(profile).data,
            'ok': True
        }
        return Response(response)

    def partial_update(self, request, *args, **kwargs):
        profile = self.get_object()
        profile.bio = request.data.get('bio', profile.bio)
        profile.address = request.data.get('address', profile.address)
        return Response({"Message": self.get_serializer(profile).data})

