from rest_framework import serializers
from .models import Account


class AccountDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'


class AccountCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(style={'input_type': 'password'})
    username = serializers.CharField(max_length=100)
    class Meta:
        model = Account
        fields = ['username', 'password']


class AccountUpdateSerializer(serializers.ModelSerializer):
    model = Account
    confirm_password = serializers.CharField(max_length=100, style={'input_type': 'password'})
    password = serializers.CharField(style={'input_type': 'password'})
    #old_password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = Account
        fields = ['password', 'confirm_password']

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and "
                                              "confirm it.")
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")
        return data