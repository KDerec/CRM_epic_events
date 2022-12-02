from django.test import TestCase
from django.test import Client as TestClient
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APIClient
from business.models import Client, Contract, Event
from accounts.models import User


class TestData(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = TestClient()
        cls.client_api = APIClient()
        cls.manager_group, created = Group.objects.get_or_create(name="Manager")
        cls.sales_group, created = Group.objects.get_or_create(name="Sales")
        cls.support_group, created = Group.objects.get_or_create(name="Support")

        user_ct = ContentType.objects.get_for_model(User)
        client_ct = ContentType.objects.get_for_model(Client)
        contract_ct = ContentType.objects.get_for_model(Contract)
        event_ct = ContentType.objects.get_for_model(Event)

        user_permission = Permission.objects.filter(content_type=user_ct)
        client_permission = Permission.objects.filter(content_type=client_ct)
        contract_permission = Permission.objects.filter(content_type=contract_ct)
        event_permission = Permission.objects.filter(content_type=event_ct)

        for perm in user_permission:
            cls.manager_group.permissions.add(perm)
            if perm.codename == "view_user":
                cls.sales_group.permissions.add(perm)
                cls.support_group.permissions.add(perm)

        for perm in client_permission:
            cls.manager_group.permissions.add(perm)
            cls.sales_group.permissions.add(perm)
            if perm.codename == "view_client":
                cls.support_group.permissions.add(perm)
            if "delete" in perm.codename:
                cls.sales_group.permissions.remove(perm)

        for perm in contract_permission:
            cls.manager_group.permissions.add(perm)
            cls.sales_group.permissions.add(perm)
            if perm.codename == "view_contract":
                cls.support_group.permissions.add(perm)
            if "delete" in perm.codename:
                cls.sales_group.permissions.remove(perm)

        for perm in event_permission:
            cls.manager_group.permissions.add(perm)
            cls.sales_group.permissions.add(perm)
            if perm.codename == "view_event":
                cls.support_group.permissions.add(perm)
            if perm.codename == "change_event":
                cls.support_group.permissions.add(perm)
            if "delete" in perm.codename:
                cls.sales_group.permissions.remove(perm)

        cls.admin_user = User.objects.create_superuser(
            username="admin", password="admin", is_staff=True, is_superuser=True
        )
        cls.manager_user = User.objects.create_user(
            username="manager_user", password="managerpassword84", is_staff=True
        )
        cls.sales_user = User.objects.create_user(
            username="sales_user", password="salespassword84", is_staff=True
        )
        cls.sales_user_two = User.objects.create_user(
            username="sales_user_two", password="salespassword84", is_staff=True
        )
        cls.support_user = User.objects.create_user(
            username="support_user", password="supportpassword84", is_staff=True
        )
        cls.support_user_two = User.objects.create_user(
            username="support_user_two", password="supportpassword84", is_staff=True
        )

        cls.manager_user.groups.add(cls.manager_group)
        cls.sales_user.groups.add(cls.sales_group)
        cls.sales_user_two.groups.add(cls.sales_group)
        cls.support_user.groups.add(cls.support_group)
        cls.support_user_two.groups.add(cls.support_group)

        cls.client_one_sales_user = Client.objects.create(
            first_name="Henry",
            last_name="Paul",
            email="henry.paul@email.com",
            company_name="THE WORLD",
            sales_contact=cls.sales_user,
        )
        cls.client_two_sales_user_two = Client.objects.create(
            first_name="Jack",
            last_name="Ualo",
            email="jack.ualo@email.com",
            company_name="THE HOUSE",
            sales_contact=cls.sales_user_two,
        )
        cls.event_one = Event.objects.create(
            event_status=False,
            attendees=10,
            event_date="2022-11-12",
            client=cls.client_one_sales_user,
            support_contact=cls.support_user,
        )
        cls.event_two = Event.objects.create(
            event_status=False,
            attendees=20,
            event_date="2024-11-12",
            client=cls.client_two_sales_user_two,
            support_contact=cls.support_user_two,
        )
        cls.contract_client_one = Contract.objects.create(
            status=False,
            amount=10000,
            payment_due="2022-12-12",
            client=cls.client_one_sales_user,
            sales_contact=cls.sales_user,
            event=cls.event_one,
        )
        cls.contract_client_two = Contract.objects.create(
            status=False,
            amount=20000,
            payment_due="2023-12-12",
            client=cls.client_two_sales_user_two,
            sales_contact=cls.sales_user_two,
        )
