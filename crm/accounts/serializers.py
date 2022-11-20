from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from accounts.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "password", "groups"]
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
        }

    def is_valid(self, *, raise_exception=False):
        available_groups = [
            "http://127.0.0.1:8000/api/groups/1/",
            "http://127.0.0.1:8000/api/groups/2/",
            "http://127.0.0.1:8000/api/groups/3/",
        ]
        group_input = self.initial_data["groups"]
        if group_input not in available_groups:
            if group_input.upper() == "MANAGER":
                self.initial_data["groups"] = ["http://127.0.0.1:8000/api/groups/1/"]
            elif group_input.upper() == "SALES":
                self.initial_data["groups"] = ["http://127.0.0.1:8000/api/groups/2/"]
            elif group_input.upper() == "SUPPORT":
                self.initial_data["groups"] = ["http://127.0.0.1:8000/api/groups/3/"]
            else:
                raise ValueError(
                    "Veuillez saisir un nom de groupe valide (Manager, Sales ou Support)."
                )

        return super().is_valid(raise_exception=raise_exception)

    def validate(self, attrs):
        user = User(username=attrs["username"], password=attrs["password"])
        password = attrs.get("password")
        validate_password(password=password, user=user)

        return super().validate(attrs)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    permissions = serializers.SerializerMethodField("get_permission_name")

    class Meta:
        model = Group
        fields = ["url", "name", "permissions"]

    def get_permission_name(self, obj):
        permission_name_list = [permission.name for permission in obj.permissions.all()]
        return permission_name_list
