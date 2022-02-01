from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    # def create(self, validated_data):
    #     try:
    #         if not validated_data["username"]:
    #             raise ValueError(('The username mustbe set'))
    #         if not validated_data["password"]:
    #             raise ValueError(('The password must be set'))
    #             # if CustomUser.objects.filter(email= email):
    #         user = User(username=validated_data['username'])
    #         user.set_password(validated_data['password'])
    #         user.is_active = True
    #         try:
    #             user.save()
    #         except Exception:
    #             raise Exception("Error in saving")
    #         return user
    #     except Exception:
    #         raise ("Error")
