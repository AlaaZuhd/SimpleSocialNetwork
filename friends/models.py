from django.db import models
from profile_app.models import Profile
from helpers.extra_models import CreatedDateModel
# Create your models here.


class FriendRequest(CreatedDateModel):
    from_user = models.ForeignKey(Profile, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(Profile, related_name='to_user', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    # is_pended = !is_rejected && !is_accepted.

    def __str__(self):
        return self.from_user.account.user.username + " -> " + self.to_user.account.user.username