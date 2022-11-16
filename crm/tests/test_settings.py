from django.test import TestCase, Client
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from business.models import Client, Contract, Event
from accounts.models import User


class TestData(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
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

        cls.manager_user.groups.add(manager_group)
        cls.sales_user.groups.add(sales_group)
        cls.sales_user_two.groups.add(sales_group)
        cls.support_user.groups.add(support_group)
        cls.support_user_two.groups.add(support_group)

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
