from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import User
from business.models import Client, Contract, Event


def create_group_and_permission():

    manager_group, created = Group.objects.get_or_create(name="Manager")
    sales_group, created = Group.objects.get_or_create(name="Sales")
    support_group, created = Group.objects.get_or_create(name="Support")

    user_ct = ContentType.objects.get_for_model(User)
    client_ct = ContentType.objects.get_for_model(Client)
    contract_ct = ContentType.objects.get_for_model(Contract)
    event_ct = ContentType.objects.get_for_model(Event)

    user_permission = Permission.objects.filter(content_type=user_ct)
    client_permission = Permission.objects.filter(content_type=client_ct)
    contract_permission = Permission.objects.filter(content_type=contract_ct)
    event_permission = Permission.objects.filter(content_type=event_ct)

    manager_permissions = []
    sales_permissions = []
    support_permissions = []

    for perm in user_permission:
        manager_group.permissions.add(perm)

    for perm in client_permission:
        manager_group.permissions.add(perm)
        sales_group.permissions.add(perm)
        if perm.codename == "view_client":
            support_group.permissions.add(perm)
        if "delete" in perm.codename:
            sales_group.permissions.remove(perm)

    for perm in contract_permission:
        manager_group.permissions.add(perm)
        sales_group.permissions.add(perm)
        if perm.codename == "view_contract":
            support_group.permissions.add(perm)
        if "delete" in perm.codename:
            sales_group.permissions.remove(perm)

    for perm in event_permission:
        manager_group.permissions.add(perm)
        sales_group.permissions.add(perm)
        if perm.codename == "view_event":
            support_group.permissions.add(perm)
        if perm.codename == "change_event":
            support_group.permissions.add(perm)
        if "delete" in perm.codename:
            sales_group.permissions.remove(perm)
