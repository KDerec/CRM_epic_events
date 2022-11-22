from tests.test_settings import TestData
from business.models import Client
from accounts.models import User


class ClientManagerApiTestCase(TestData):
    def setUp(self):
        self.client_api.force_authenticate(self.manager_user)

    def test_can_get_client_list(self):
        response = self.client_api.get("/api/clients/")
        self.assertEqual(response.status_code, 200)

    def test_can_get_client_instance(self):
        response = self.client_api.get(
            f"/api/clients/{self.client_one_sales_user.client_id}/"
        )
        self.assertEqual(response.status_code, 200)

    def test_can_post_client(self):
        response = self.client_api.post(
            "/api/clients/",
            {
                "first_name": "First Name",
                "last_name": "Last Name",
                "email": "email@email.com",
                "company_name": "Company Name",
                "sales_contact": "sales_user",
            },
        )
        client = Client.objects.get(email="email@email.com")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(client)
        self.assertEqual(client.sales_contact, User.objects.get(username="sales_user"))

    def test_cant_post_client_without_sales_contact(self):
        response = self.client_api.post(
            "/api/clients/",
            {
                "first_name": "First Name",
                "last_name": "Last Name",
                "email": "email@email.com",
                "company_name": "Company Name",
            },
        )
        self.assertEqual(response.status_code, 400)
        with self.assertRaises(Client.DoesNotExist):
            Client.objects.get(email="email@email.com")

    def test_cant_post_client_with_unknow_sales_contact(self):
        response = self.client_api.post(
            "/api/clients/",
            {
                "first_name": "First Name",
                "last_name": "Last Name",
                "email": "email@email.com",
                "company_name": "Company Name",
                "sales_contact": "unknow_username",
            },
        )
        self.assertEqual(response.status_code, 400)
        with self.assertRaises(Client.DoesNotExist):
            Client.objects.get(email="email@email.com")

    def test_can_put_client(self):
        ...

    def test_can_patch_client(self):
        # avec n'importe quels sales contact
        ...

    def test_can_delete_client(self):
        ...


class ClientSalesApiTestCase(TestData):
    def setUp(self):
        self.client_api.force_authenticate(self.sales_user)

    def test_can_get_client_list(self):
        response = self.client_api.get("/api/clients/")
        self.assertEqual(response.status_code, 200)

    def test_can_get_client_instance(self):
        response = self.client_api.get(
            f"/api/clients/{self.client_one_sales_user.client_id}/"
        )
        self.assertEqual(response.status_code, 200)

    def test_can_post_client(self):
        ...

    def test_can_put_his_assigned_client(self):
        ...

    def test_can_patch_his_assigned_client(self):
        ...

    def test_cant_put_not_assigned_client(self):
        ...

    def test_cant_patch_not_assigned_client(self):
        ...

    def test_cant_select_sales_contact_client(self):
        # avec post, put et patch
        ...

    def test_cant_delete_client(self):
        ...


class ClientSupportApiTestCase(TestData):
    def setUp(self):
        self.client_api.force_authenticate(self.support_user)

    def test_can_get_client_list(self):
        response = self.client_api.get("/api/clients/")
        self.assertEqual(response.status_code, 200)

    def test_can_get_client_instance(self):
        response = self.client_api.get(
            f"/api/clients/{self.client_one_sales_user.client_id}/"
        )
        self.assertEqual(response.status_code, 200)

    def test_cant_post_client(self):
        ...

    def test_cant_put_client(self):
        ...

    def test_cant_patch_client(self):
        ...

    def test_cant_delete_client(self):
        ...
