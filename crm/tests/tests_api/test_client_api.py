from tests.test_settings import TestData


class ClientManagerApiTestCase(TestData):
    def setUp(self):
        self.client_api.force_authenticate(self.manager_user)

    def test_can_get_client_list(self):
        response = self.client_api.get("/api/clients/")
        self.assertEqual(response.status_code, 200)

    def test_can_get_client_instance(self):
        ...

    def test_can_post_client(self):
        # avec n'importe quels sales contact
        ...

    def test_can_put_client(self):
        # avec n'importe quels sales contact
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
        ...

    def test_can_get_client_instance(self):
        ...

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
        ...

    def test_can_get_client_instance(self):
        ...

    def test_cant_post_client(self):
        ...

    def test_cant_put_client(self):
        ...

    def test_cant_patch_client(self):
        ...

    def test_cant_delete_client(self):
        ...
