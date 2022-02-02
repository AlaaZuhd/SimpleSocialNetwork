from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from account.models import Account
from helpers.permissions import IsOwner, IsToUser, IsFromUser
from profile_app.models import Profile
from profile_app.serializers import ProfileSerializer
from .models import FriendRequest


# Create your views here.
from .serializers import FriendRequestSerializer, FriendRequestCreateSerializer

#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def send_friend_request(request, to_user_id):  # to user is the id
#     to_user = Profile.objects.get(id=to_user_id)
#     from_user = Profile.objects.get(account=Account.objects.get(user=request.user))
#     # make sure to_user and from_user are not thte same
#     if from_user == to_user:
#         return Response({"Message": "You can't send a friend request to yourself"})
#     friend_request, created = FriendRequest.objects.get_or_create(to_user=to_user, from_user=from_user)
#     if created:
#         return Response({"Message": "Friend Request sent successfully"})
#     else:
#         return Response({'Message': "Friend Request was already sent"})
#
#
# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def accept_friend_request(request, friend_request_id):
#     print("hii")
#     try:
#         friend_request = FriendRequest.objects.get(id=friend_request_id)
#         if friend_request.to_user.account.user == request.user:
#             friend_request.is_accepted = True
#             friend_request.to_user.friends.add(friend_request.from_user)
#             friend_request.from_user.friends.add(friend_request.to_user)
#             return Response({"Message": "Friend Request accepted successfully"})
#         else:
#             return Response({"Message": "UnAuthorized"})
#     except Exception:
#         return Response({"Message": "Friend request doesn't exist"})
#
#
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def show_my_friends(request):
#     profile = Profile.objects.get(account__user=request.user)
#     print(profile.friends)
#     paginator = PageNumberPagination()
#     paginator.page_size = 2
#     result_page = paginator.paginate_queryset(profile.friends, request)
#     serializer = ProfileSerializer(result_page, many=True)
#     return paginator.get_paginated_response(serializer.data)
#
#
# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def unfriend(request, pk):
#     profile = Profile.objects.get(account__user=request.user)
#     removed_user = Profile.objects.get(account__user__id=pk)
#     try:
#         # if profile.friends.filter(removed_user).exist():
#         #     return Response({"Message": "Can't Remove friend, you are already not friends."})
#         profile.friends.remove(removed_user)
#         return Response({"Message": "Friend was removed successfully"})
#     except Exception:
#         return Response({"Message": "Error in removing the friend"})
#
#
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def show_mutual_friends(request, first_user_id, second_user_id):
#     first_user_profile = Profile.objects.get(account__user__id=first_user_id)
#     second_user_profile = Profile.objects.get(account__user__id=second_user_id)
#     mutual_friends = first_user_profile.friends.filter(id__in=second_user_profile.friends.all())
#     paginator = PageNumberPagination()
#     paginator.page_size = 2
#     result_page = paginator.paginate_queryset(mutual_friends, request)
#     serializer = ProfileSerializer(result_page, many=True)
#     return paginator.get_paginated_response(serializer.data)





class FriendViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return FriendRequestCreateSerializer
        elif self.action == "retrieve":
            return ProfileSerializer
        else:
            return FriendRequestSerializer


    def get_permissions(self):
        if self.action == 'create' or self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated and (IsFromUser or IsToUser)]
        return [permission() for permission in permission_classes]

    def partial_update(self, request, *args, **kwargs):
        friend_request = self.get_object()
        friend_request.is_accepted = request.data.get('is_accepted', friend_request.is_accepted)
        friend_request.is_rejected = request.data.get('is_rejected', friend_request.is_rejected)
        friend_request.save()
        if friend_request.is_accepted:
            friend_request.to_user.friends.add(friend_request.from_user)
            friend_request.from_user.friends.add(friend_request.to_user)
        return Response({"data": self.get_serializer(friend_request).data})

    def retrieve(self, request, *args, **kwargs):
        profile = Profile.objects.get(account__user=kwargs['pk'])
        page = self.paginate_queryset(profile.friends.all())
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(self.get_serializer(profile.friends, many=True).data)

    @action(detail=False, methods=['post'])
    def send_friend_request(self, request):  # to user is the id
        to_user = Profile.objects.get(id=request.data["to_user_id"])
        from_user = Profile.objects.get(account=Account.objects.get(user=request.user))
        # make sure to_user and from_user are not thte same
        if from_user == to_user:
            return Response({"Message": "You can't send a friend request to yourself"})
        # check if they are already friends
        #3
        ##
        friend_request, created = FriendRequest.objects.get_or_create(to_user=to_user, from_user=from_user)
        if created:
            return Response({"Message": "Friend Request sent successfully"})
        else:
            return Response({'Message': "Friend Request was already sent"})


    @action(detail=False, methods=['get'])
    def show_mutual_friends(self, request):
        first_user_profile = Profile.objects.get(account__user__id=request.data['first_user_id'])
        second_user_profile = Profile.objects.get(account__user__id=request.data['second_user_id'])
        mutual_friends = first_user_profile.friends.filter(id__in=second_user_profile.friends.all())
        paginator = PageNumberPagination()
        paginator.page_size = 2
        result_page = paginator.paginate_queryset(mutual_friends, request)
        serializer = ProfileSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=True, methods=['delete'])
    def unfriend(self, request, pk):
        profile = Profile.objects.get(account__user=request.user)
        removed_user = Profile.objects.get(account__user__id=pk)
        try:
            # if profile.friends.filter(removed_user).exist():
            #     return Response({"Message": "Can't Remove friend, you are already not friends."})
            profile.friends.remove(removed_user)
            return Response({"Message": "Friend was removed successfully"})
        except Exception:
            return Response({"Message": "Error in removing the friend"})