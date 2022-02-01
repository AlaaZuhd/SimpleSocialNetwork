from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from account.models import Account
from profile_app.models import Profile
from profile_app.serializers import ProfileSerializer
from .models import FriendRequest


# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request, to_user_id):  # to user is the id
    to_user = Profile.objects.get(id=to_user_id)
    from_user = Profile.objects.get(account=Account.objects.get(user=request.user))
    # make sure to_user and from_user are not thte same
    if from_user == to_user:
        return Response({"Message": "You can't send a friend request to yourself"})
    friend_request, created = FriendRequest.objects.get_or_create(to_user=to_user, from_user=from_user)
    if created:
        return Response({"Message": "Friend Request sent successfully"})
    else:
        return Response({'Message': "Friend Request was already sent"})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, friend_request_id):
    print("hii")
    try:
        friend_request = FriendRequest.objects.get(id=friend_request_id)
        if friend_request.to_user.account.user == request.user:
            friend_request.is_accepted = True
            friend_request.to_user.friends.add(friend_request.from_user)
            friend_request.from_user.friends.add(friend_request.to_user)
            return Response({"Message": "Friend Request accepted successfully"})
        else:
            return Response({"Message": "UnAuthorized"})
    except Exception:
        return Response({"Message": "Friend request doesn't exist"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_my_friends(request):
    profile = Profile.objects.get(account__user=request.user)
    print(profile.friends)
    print("\n\n\n\n\n")
    return Response(ProfileSerializer(profile.friends, many=True).data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unfriend(request, pk):
    profile = Profile.objects.get(account__user=request.user)
    removed_user = Profile.objects.get(account__user__id=pk)
    try:
        # if profile.friends.filter(removed_user).exist():
        #     return Response({"Message": "Can't Remove friend, you are already not friends."})
        profile.friends.remove(removed_user)
        return Response({"Message": "Friend was removed successfully"})
    except Exception:
        return Response({"Message": "Error in removing the friend"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_mutual_friends(request, first_user_id, second_user_id):
    first_user_profile = Profile.objects.get(account__user__id=first_user_id)
    second_user_profile = Profile.objects.get(account__user__id=second_user_id)
    mutual_friends = first_user_profile.friends.filter(id__in=second_user_profile.friends.all())
    print(mutual_friends.all())
    return Response(ProfileSerializer(first_user_profile.friends, many=True).data)