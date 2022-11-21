from django.contrib.auth.models import Group
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from accounts.permissions import IsSuperUser, MyDjangoModelPermissions
from accounts.models import User
from accounts.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [MyDjangoModelPermissions]

    def create(self, request, *args, **kwargs):
        try:
            group_name = request.data["groups"]
        except MultiValueDictKeyError:
            group_name = "is_empty"
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, group_name)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer, group_name):
        save_and_add_user_in_group(serializer, group_name)

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def update(self, request, *args, **kwargs):
        check_not_superuser_try_to_modify_superuser(self, request)
        try:
            group_name = request.data["groups"]
        except MultiValueDictKeyError:
            group_name = "is_empty"
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, group_name)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer, group_name):
        save_and_add_user_in_group(serializer, group_name)

    def retrieve(self, request, *args, **kwargs):
        check_not_superuser_try_to_modify_superuser(self, request)
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        check_not_superuser_try_to_modify_superuser(self, request)
        return super().destroy(request, *args, **kwargs)


class GroupViewSet(viewsets.ModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsSuperUser | MyDjangoModelPermissions]


def save_and_add_user_in_group(serializer, group_name):
    if group_name == "is_empty":
        raise ValidationError("Veuillez renseigner un groupe.")
    if (
        group_name.upper() == "MANAGER"
        or group_name.upper() == "SALES"
        or group_name.upper() == "SUPPORT"
    ):
        user = serializer.save()
        remove_user_from_all_group(user)
        user.groups.add(Group.objects.get(name=group_name))
    elif "http:" in group_name:
        user = serializer.save()
        if "groups/1/" in group_name:
            group_name = "Manager"
        if "groups/2/" in group_name:
            group_name = "Sales"
        if "groups/3/" in group_name:
            group_name = "Sales"
        remove_user_from_all_group(user)
        user.groups.add(Group.objects.get(name=group_name))
    else:
        raise ValidationError(
            "Veuillez renseigner un nom de groupe valide (Manager, Sales ou Support)."
        )


def check_not_superuser_try_to_modify_superuser(self, request):
    if self.get_object().is_superuser and not request.user.is_superuser:
        raise PermissionDenied(
            "Il faut être superuser pour intéragir avec cet utilisateur."
        )


def remove_user_from_all_group(user):
    if user.groups.exists():
        for g in user.groups.all():
            user.groups.remove(g)
