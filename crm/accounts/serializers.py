from django.contrib.auth.models import Group
from accounts.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    permissions = serializers.SerializerMethodField("get_permission_name")

    class Meta:
        model = Group
        fields = ["url", "name", "permissions"]

    def get_permission_name(self, obj):
        permission_name_list = [permission.name for permission in obj.permissions.all()]
        return permission_name_list
