from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import serializers
from accounts.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context["request"].method == "PUT":
            self.fields.pop("password")

    class Meta:
        model = User
        fields = ["url", "username", "password", "groups"]
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
        }

    def is_valid(self, *, raise_exception=False):
        try:
            self.initial_data["groups"]
        except MultiValueDictKeyError:
            return super().is_valid(raise_exception=raise_exception)
        self.initial_data._mutable = True
        self.initial_data.pop("groups")
        return super().is_valid(raise_exception=raise_exception)

    def validate(self, attrs):
        try:
            user = User(username=attrs["username"], password=attrs["password"])
            password = attrs.get("password")
            validate_password(password=password, user=user)
        except KeyError:
            pass
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("groups")
        user = User.objects.create_user(**validated_data, is_staff=True)
        return user


class GroupSerializer(serializers.ModelSerializer):
    permissions_name = serializers.SerializerMethodField("get_permission_name")

    class Meta:
        model = Group
        fields = ["url", "name", "permissions", "permissions_name"]
        extra_kwargs = {
            "permissions": {"write_only": True},
        }

    def get_permission_name(self, obj):
        permission_name_list = [permission.name for permission in obj.permissions.all()]
        return permission_name_list
