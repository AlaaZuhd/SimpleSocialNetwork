from rest_framework import serializers
from .models import FriendRequest

class FriendRequestSerializer(serializers.ModelSerializer):
    model = FriendRequest

    class Meta:
        model = FriendRequest
        fields = '__all__'



class FriendRequestCreateSerializer(serializers.ModelSerializer):

    to_user_id = serializers.IntegerField()

    class Meta:
        model = FriendRequest
        fields = ['to_user_id']
