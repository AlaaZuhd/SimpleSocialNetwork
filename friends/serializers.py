from rest_framework import serializers
from .models import FriendRequest

class FriendRequestSerializer(serializers.ModelSerializer):
    model = FriendRequest

    class Meta:
        model = FriendRequest
        fields = '__all__'
