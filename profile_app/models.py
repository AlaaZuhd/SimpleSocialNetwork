from django.db import models
from account.models import Account
# Create your models here.


class Profile(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    updated_date = models.DateTimeField(auto_now=True, editable=False, null=True)
    bio = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    friends = models.ManyToManyField("Profile", blank=True)

    #
    # def __str__(self):
    #     return self.account.user.username
    #
    def create(self, user, validated_data):
        profile = Profile()
        if validated_data.get('bio', None) != None:
            profile.bio =validated_data['bio']
        elif validated_data.get('address', None) != None:
            profile.address =validated_data['address']
        account = Account.objects.filter(user=user).first()
        profile.account = account
        profile.save()
        return profile