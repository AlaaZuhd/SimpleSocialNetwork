from django.db import models
from profile_app.models import Profile
from helpers.extra_models import CreatedDateModel
# Create your models here.


class Story(CreatedDateModel):
    owner = models.ForeignKey(Profile, related_name='stories', on_delete=models.CASCADE)
    content = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='Stories/images', height_field=None, width_field=None, max_length=None, blank=True)

    def create(self, request_user, validated_data):
        story = Story(**validated_data)
        story.owner = Profile.objects.get(account__user=request_user)
        story.save()
        return story

