from rest_framework import serializers
from .models import Story


class StorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Story
        fields = '__all__'

    def validate(self, data):
        if 'content' not in data and 'image' not in data:
            raise serializers.ValidationError("Must include either contentor image")
        return data
