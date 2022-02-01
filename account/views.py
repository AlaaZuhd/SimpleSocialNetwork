from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from helpers.permissions import IsAuthenticated, IsOwner
from .models import Account
from .serializers import AccountCreateSerializer, AccountDisplaySerializer, AccountUpdateSerializer
# Create your views here.


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.filter(user__is_active=True)# update, list, retreive and destroy active users.

    def get_serializer_class(self):
        if self.action == 'create':
            return AccountCreateSerializer
        elif self.action == 'update':
            return AccountUpdateSerializer
        else:
            return AccountDisplaySerializer

    def get_permissions(self):
        if self.action == 'post':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated and (IsOwner)]
        return [permission() for permission in permission_classes]

    # def get_object(self):
    #     if self.kwargs.get('pk', None) == 'me':
    #         self.kwargs['pk'] = self.request.user.pk
    #     return super(AccountViewSet, self).get_object()

    def create(self, request, *args, **kwargs):
        print(request.data)
        try:
            new_user = User(username=request.data["username"], password=request.data["password"])
            new_user.set_password(request.data['password'])
            new_user.save()
            new_account = Account(user=new_user)
            new_account.save()
        except Exception:
            return Response({"errorMessage": "Invalid username"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response("Account Created Successfully", status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        user.is_active = False
        user.save()
        return Response("user has been deactivated successfully", status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        user  = User.objects.get(username= request.user.username)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user.set_password(serializer.data.get("password"))
            user.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


