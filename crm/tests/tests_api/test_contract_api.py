from tests.test_settings import TestData


class ContractManagerApiTestCase(TestData):
    def setUp(self):
        self.client_api.force_authenticate(self.manager_user)

    def test_can_get_contract_list(self):
        response = self.client_api.get("/api/contracts/")
        self.assertEqual(response.status_code, 200)

    def test_can_get_contract_instance(self):
        response = self.client_api.get(
            f"/api/contracts/{self.contract_client_one.contract_id}/"
        )
        self.assertEqual(response.status_code, 200)

    def test_cant_get_unknow_contract_id(self):
        response = self.client_api.get("/api/contracts/99/")
        self.assertEqual(response.status_code, 404)

    def test_can_post_contract(self):
        response = self.client_api.post(
            "/api/contracts/",
            {
                "status": "False",
                "amount": "999",
                "payment_due": "10/04/2025",
                f"client": {self.client_one_sales_user.email},
                f"sales_contact": {self.sales_user.username},
                f"event": {self.event_one.event_id},
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_cant_post_with_missing_data(self):
        response = self.client_api.post(
            "/api/contracts/",
            {
                "status": "False",
                "amount": "999",
                "payment_due": "10/04/2025",
                f"sales_contact": {self.sales_user.username},
                f"event": {self.event_one.event_id},
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client_api.post(
            "/api/contracts/",
            {
                "status": "False",
                "amount": "999",
                "payment_due": "10/04/2025",
                f"client": {self.client_one_sales_user.email},
                f"event": {self.event_one.event_id},
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client_api.post(
            "/api/contracts/",
            {
                "status": "False",
                "amount": "999",
                "payment_due": "10/04/2025",
                f"client": {self.client_one_sales_user.email},
                f"sales_contact": {self.sales_user.username},
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_cant_post_with_unknow_data(self):
        response = self.client_api.post(
            "/api/contracts/",
            {
                "status": "False",
                "amount": "999",
                "payment_due": "10/04/2025",
                "client": "fvb15",
                f"sales_contact": {self.sales_user.username},
                f"event": {self.event_one.event_id},
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client_api.post(
            "/api/contracts/",
            {
                "status": "False",
                "amount": "999",
                "payment_due": "10/04/2025",
                f"client": {self.client_one_sales_user.email},
                "sales_contact": "rved51",
                f"event": {self.event_one.event_id},
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client_api.post(
            "/api/contracts/",
            {
                "status": "False",
                "amount": "999",
                "payment_due": "10/04/2025",
                f"client": {self.client_one_sales_user.email},
                f"sales_contact": {self.sales_user.username},
                "event": "99",
            },
        )
        self.assertEqual(response.status_code, 400)

        with self.assertRaises(ValueError):
            self.client_api.post(
                "/api/contracts/",
                {
                    "status": "False",
                    "amount": "999",
                    "payment_due": "10/04/2025",
                    f"client": {self.client_one_sales_user.email},
                    f"sales_contact": {self.sales_user.username},
                    "event": "eevce",
                },
            )

    def test_can_put_contract(self):
        # avec nimporte quelle sales contact, client et event
        ...

    def test_can_patch_contract(self):
        # avec nimporte quelle sales contact, client et event
        ...

    def test_can_delete_contract(self):
        ...


class ContractSalesApiTestCase(TestData):
    def setUp(self):
        self.client_api.force_authenticate(self.sales_user)

    def test_can_get_contract_list(self):
        response = self.client_api.get("/api/contracts/")
        self.assertEqual(response.status_code, 200)

    def test_can_get_contract_instance(self):
        response = self.client_api.get(
            f"/api/contracts/{self.contract_client_one.contract_id}/"
        )
        self.assertEqual(response.status_code, 200)

    def test_can_post_contract(self):
        ...

    def test_can_put_contract(self):
        ...

    def test_can_patch_contract(self):
        ...

    def test_cant_put_contract_with_not_assigned_client(self):
        ...

    def test_cant_patch_contract_with_not_assigned_client(self):
        ...

    def test_cant_select_sales_contact(self):
        # avec post, put et patch
        ...

    def test_cant_select_event_of_not_assigned_client(self):
        # avec post, put et patch
        ...

    def test_cant_select_client_and_event_of_another_client(self):
        # avec post, put et patch
        ...

    def test_cant_delete_contract(self):
        ...


class ContractSupportApiTestCase(TestData):
    def setUp(self):
        self.client_api.force_authenticate(self.support_user)

    def test_can_get_contract_list(self):
        response = self.client_api.get("/api/contracts/")
        self.assertEqual(response.status_code, 200)

    def test_can_get_contract_instance(self):
        response = self.client_api.get(
            f"/api/contracts/{self.contract_client_one.contract_id}/"
        )
        self.assertEqual(response.status_code, 200)

    def test_cant_post_contract(self):
        ...

    def test_cant_put_contract(self):
        ...

    def test_cant_patch_contract(self):
        ...

    def test_cant_delete_contract(self):
        ...
