"""Serializer User"""
from rest_framework import serializers
from sidgro.users.models import User



class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'nickname',
            'active',
            'userUpdate'
        )
