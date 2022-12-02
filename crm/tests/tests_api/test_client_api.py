from tests.test_settings import TestData
from business.models import Client


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

    def test_can_get_object_with_filter_in_url(self):
        response = self.client_api.get(
            f"/api/clients/?last_name={self.client_one_sales_user.last_name}&email={self.client_one_sales_user.email}"
        )
        self.assertEqual(response.data["count"], 1)

    def test_cant_get_unknow_client_id(self):
        response = self.client_api.get("/api/clients/99/")
        self.assertEqual(response.status_code, 404)

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
        self.assertEqual(client.sales_contact, self.sales_user)

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
        response = self.client_api.put(
            f"/api/clients/{self.client_one_sales_user.client_id}/",
            {
                "first_name": "First Name",
                "last_name": "Last Name",
                "email": "email@email.com",
                "company_name": "Company Name",
                "sales_contact": "sales_user",
            },
        )
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Client.DoesNotExist):
            Client.objects.get(email="henry.paul@email.com")

    def test_cant_put_client_without_sales_contact(self):
        response = self.client_api.put(
            f"/api/clients/{self.client_one_sales_user.client_id}/",
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

    def test_cant_put_client_with_unknow_sales_contact(self):
        response = self.client_api.put(
            f"/api/clients/{self.client_one_sales_user.client_id}/",
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

    def test_can_patch_client(self):
        response = self.client_api.patch(
            f"/api/clients/{self.client_one_sales_user.client_id}/",
            {
                "first_name": "First Name",
                "last_name": "Last Name",
                "email": "email@email.com",
                "company_name": "Company Name",
                "sales_contact": "sales_user",
            },
        )
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Client.DoesNotExist):
            Client.objects.get(email="henry.paul@email.com")

    def test_can_delete_client(self):
        response = self.client_api.delete(
            f"/api/clients/{self.client_one_sales_user.client_id}/"
        )
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Client.DoesNotExist):
            Client.objects.get(client_id=self.client_one_sales_user.client_id)


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
        response = self.client_api.post(
            "/api/clients/",
            {
                "first_name": "First Name",
                "last_name": "Last Name",
                "email": "email@email.com",
                "company_name": "Company Name",
            },
        )
        self.assertEqual(response.status_code, 201)
        client = Client.objects.get(email="email@email.com")
        self.assertEqual(client.sales_contact, self.sales_user)

    def test_can_put_his_assigned_client(self):
        response = self.client_api.put(
            f"/api/clients/{self.client_one_sales_user.client_id}/",
            {
                "first_name": "First Name",
                "last_name": "Last Name",
                "email": "email@email.com",
                "company_name": "Company Name",
            },
        )
        self.assertEqual(response.status_code, 200)
        client = Client.objects.get(email="email@email.com")
        self.assertEqual(client.sales_contact, self.sales_user)
        with self.assertRaises(Client.DoesNotExist):
            Client.objects.get(email="henry.paul@email.com")

    def test_cant_put_not_assigned_client(self):
        response = self.client_api.put(
            f"/api/clients/{self.client_two_sales_user_two.client_id}/",
            {
                "first_name": "First Name",
                "last_name": "Last Name",
                "email": "email@email.com",
                "company_name": "Company Name",
            },
        )
        self.assertEqual(response.status_code, 403)
        client = Client.objects.get(email="jack.ualo@email.com")
        self.assertEqual(client.sales_contact, self.sales_user_two)

    def test_can_patch_his_assigned_client(self):
        response = self.client_api.patch(
            f"/api/clients/{self.client_one_sales_user.client_id}/",
            {
                "first_name": "First Name",
                "last_name": "Last Name",
                "email": "email@email.com",
                "company_name": "Company Name",
            },
        )
        self.assertEqual(response.status_code, 200)
        client = Client.objects.get(email="email@email.com")
        self.assertEqual(client.sales_contact, self.sales_user)
        with self.assertRaises(Client.DoesNotExist):
            Client.objects.get(email="henry.paul@email.com")

    def test_cant_patch_not_assigned_client(self):
        response = self.client_api.patch(
            f"/api/clients/{self.client_two_sales_user_two.client_id}/",
            {
                "first_name": "First Name",
                "last_name": "Last Name",
                "email": "email@email.com",
                "company_name": "Company Name",
            },
        )
        self.assertEqual(response.status_code, 403)
        client = Client.objects.get(email="jack.ualo@email.com")
        self.assertEqual(client.sales_contact, self.sales_user_two)

    def test_cant_select_sales_contact_client(self):
        response = self.client_api.post(
            "/api/clients/",
            {
                "first_name": "First Name",
                "last_name": "Last Name",
                "email": "email@email.com",
                "company_name": "Company Name",
                "sales_contact": "sales_user_two",
            },
        )
        self.assertEqual(response.status_code, 400)
        response = self.client_api.put(
            f"/api/clients/{self.client_one_sales_user.client_id}/",
            {
                "first_name": "First Name",
                "last_name": "Last Name",
                "email": "email@email.com",
                "company_name": "Company Name",
                "sales_contact": "sales_user_two",
            },
        )
        self.assertEqual(response.status_code, 400)
        response = self.client_api.patch(
            f"/api/clients/{self.client_one_sales_user.client_id}/",
            {
                "first_name": "First Name",
                "last_name": "Last Name",
                "email": "email@email.com",
                "company_name": "Company Name",
                "sales_contact": "sales_user_two",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_cant_delete_client(self):
        response = self.client_api.delete(
            f"/api/clients/{self.client_one_sales_user.client_id}/"
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            Client.objects.filter(
                client_id=self.client_one_sales_user.client_id
            ).exists()
        )


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
        self.assertEqual(response.status_code, 403)
        with self.assertRaises(Client.DoesNotExist):
            Client.objects.get(email="email@email.com")

    def test_cant_put_client(self):
        response = self.client_api.put(
            f"/api/clients/{self.client_one_sales_user.client_id}/",
            {
                "first_name": "First Name",
                "last_name": "Last Name",
                "email": "email@email.com",
                "company_name": "Company Name",
                "sales_contact": "sales_user",
            },
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.client_one_sales_user.email, "henry.paul@email.com")

    def test_cant_patch_client(self):
        response = self.client_api.put(
            f"/api/clients/{self.client_one_sales_user.client_id}/",
            {
                "email": "email@email.com",
            },
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.client_one_sales_user.email, "henry.paul@email.com")

    def test_cant_delete_client(self):
        response = self.client_api.delete(
            f"/api/clients/{self.client_one_sales_user.client_id}/"
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            Client.objects.filter(
                client_id=self.client_one_sales_user.client_id
            ).exists()
        )
