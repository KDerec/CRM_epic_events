from tests.test_settings import TestData
from business.models import Contract


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
                "client": {self.client_one_sales_user.email},
                "sales_contact": {self.sales_user.username},
                "event": {self.event_one.event_id},
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
                "sales_contact": {self.sales_user.username},
                "event": {self.event_one.event_id},
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client_api.post(
            "/api/contracts/",
            {
                "status": "False",
                "amount": "999",
                "payment_due": "10/04/2025",
                "client": {self.client_one_sales_user.email},
                "event": {self.event_one.event_id},
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client_api.post(
            "/api/contracts/",
            {
                "status": "False",
                "amount": "999",
                "payment_due": "10/04/2025",
                "client": {self.client_one_sales_user.email},
                "sales_contact": {self.sales_user.username},
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
                "sales_contact": {self.sales_user.username},
                "event": {self.event_one.event_id},
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client_api.post(
            "/api/contracts/",
            {
                "status": "False",
                "amount": "999",
                "payment_due": "10/04/2025",
                "client": {self.client_one_sales_user.email},
                "sales_contact": "rved51",
                "event": {self.event_one.event_id},
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client_api.post(
            "/api/contracts/",
            {
                "status": "False",
                "amount": "999",
                "payment_due": "10/04/2025",
                "client": {self.client_one_sales_user.email},
                "sales_contact": {self.sales_user.username},
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
                    "client": {self.client_one_sales_user.email},
                    "sales_contact": {self.sales_user.username},
                    "event": "eevce",
                },
            )

    def test_can_put_contract(self):
        response = self.client_api.put(
            f"/api/contracts/{self.contract_client_one.contract_id}/",
            {
                "status": "False",
                "amount": "1",
                "payment_due": "10/04/2025",
                "client": {self.client_one_sales_user.email},
                "sales_contact": {self.sales_user_two.username},
                "event": {self.event_one.event_id},
            },
        )
        self.assertEqual(response.status_code, 200)
        contract = Contract.objects.get(
            contract_id=self.contract_client_one.contract_id
        )
        self.assertEqual(contract.amount, 1)
        self.assertEqual(contract.sales_contact, self.sales_user_two)

    def test_can_patch_contract(self):
        response = self.client_api.patch(
            f"/api/contracts/{self.contract_client_one.contract_id}/",
            {
                "status": "False",
                "amount": "55",
                "payment_due": "10/04/2025",
                "client": {self.client_one_sales_user.email},
                "sales_contact": {self.sales_user_two.username},
                "event": {self.event_one.event_id},
            },
        )
        self.assertEqual(response.status_code, 200)
        contract = Contract.objects.get(
            contract_id=self.contract_client_one.contract_id
        )
        self.assertEqual(contract.amount, 55)
        self.assertEqual(contract.sales_contact, self.sales_user_two)

    def test_can_delete_contract(self):
        self.client_api.delete(
            f"/api/contracts/{self.contract_client_one.contract_id}/"
        )

        self.assertFalse(
            Contract.objects.filter(
                contract_id=self.contract_client_one.contract_id
            ).exists()
        )


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
        response = self.client_api.post(
            "/api/contracts/",
            {
                "status": "False",
                "amount": "1234",
                "payment_due": "10/04/2025",
                "client": {self.client_one_sales_user.email},
                "event": {self.event_one.event_id},
            },
        )
        self.assertEqual(response.status_code, 201)
        created_contract_id = response.data["url"].split("/")[-2]
        contract = Contract.objects.get(contract_id=created_contract_id)
        self.assertEqual(contract.sales_contact, self.sales_user)

    def test_cant_post_contract_with_not_assigned_client(self):
        response = self.client_api.post(
            "/api/contracts/",
            {
                "status": "False",
                "amount": "1234",
                "payment_due": "10/04/2025",
                "client": {self.client_two_sales_user_two.email},
                "event": {self.event_two.event_id},
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_can_put_contract(self):
        response = self.client_api.put(
            f"/api/contracts/{self.contract_client_one.contract_id}/",
            {
                "status": "False",
                "amount": "1",
                "payment_due": "10/04/2025",
                "client": {self.client_one_sales_user.email},
                "event": {self.event_one.event_id},
            },
        )
        self.assertEqual(response.status_code, 200)
        contract = Contract.objects.get(
            contract_id=self.contract_client_one.contract_id
        )
        self.assertEqual(contract.amount, 1)
        self.assertEqual(contract.sales_contact, self.sales_user)

    def test_cant_put_contract_of_not_assigned_client(self):
        response = self.client_api.put(
            f"/api/contracts/{self.contract_client_two.contract_id}/",
            {
                "status": "False",
                "amount": "1",
                "payment_due": "10/04/2025",
                "client": {self.client_one_sales_user.email},
                "event": {self.event_one.event_id},
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_can_patch_contract(self):
        response = self.client_api.patch(
            f"/api/contracts/{self.contract_client_one.contract_id}/",
            {
                "status": "False",
                "amount": "1",
                "payment_due": "10/04/2025",
                "client": {self.client_one_sales_user.email},
                "event": {self.event_one.event_id},
            },
        )
        self.assertEqual(response.status_code, 200)
        contract = Contract.objects.get(
            contract_id=self.contract_client_one.contract_id
        )
        self.assertEqual(contract.amount, 1)
        self.assertEqual(contract.sales_contact, self.sales_user)

    def test_cant_patch_contract_of_not_assigned_client(self):
        response = self.client_api.patch(
            f"/api/contracts/{self.contract_client_two.contract_id}/",
            {
                "status": "False",
                "amount": "1",
                "payment_due": "10/04/2025",
                "client": {self.client_one_sales_user.email},
                "sales_contact": {self.sales_user_two.username},
                "event": {self.event_one.event_id},
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_cant_select_sales_contact(self):
        response = self.client_api.post(
            "/api/contracts/",
            {
                "status": "False",
                "amount": "999",
                "payment_due": "10/04/2025",
                "client": {self.client_one_sales_user.email},
                "sales_contact": {self.sales_user_two.username},
                "event": {self.event_one.event_id},
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_cant_select_client_and_event_of_another_client(self):
        response = self.client_api.post(
            "/api/contracts/",
            {
                "status": "False",
                "amount": "1234",
                "payment_due": "10/04/2025",
                "client": {self.client_one_sales_user.email},
                "event": {self.event_two.event_id},
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client_api.put(
            f"/api/contracts/{self.contract_client_one.contract_id}/",
            {
                "status": "False",
                "amount": "1234",
                "payment_due": "10/04/2025",
                "client": {self.client_one_sales_user.email},
                "event": {self.event_two.event_id},
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client_api.patch(
            f"/api/contracts/{self.contract_client_one.contract_id}/",
            {
                "status": "False",
                "amount": "1234",
                "payment_due": "10/04/2025",
                "client": {self.client_one_sales_user.email},
                "event": {self.event_two.event_id},
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_cant_delete_contract(self):
        response = self.client_api.delete(
            f"/api/contracts/{self.contract_client_one.contract_id}/"
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            Contract.objects.filter(
                contract_id=self.contract_client_one.contract_id
            ).exists()
        )


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
        response = self.client_api.post(
            "/api/contracts/",
            {
                "status": "False",
                "amount": "1234",
                "payment_due": "10/04/2025",
                "client": {self.client_one_sales_user.email},
                "event": {self.event_one.event_id},
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_cant_put_contract(self):
        response = self.client_api.put(
            f"/api/contracts/{self.contract_client_one.contract_id}/",
            {
                "status": "False",
                "amount": "1",
                "payment_due": "10/04/2025",
                "client": {self.client_one_sales_user.email},
                "event": {self.event_one.event_id},
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_cant_patch_contract(self):
        response = self.client_api.patch(
            f"/api/contracts/{self.contract_client_one.contract_id}/",
            {
                "status": "False",
                "amount": "1",
                "payment_due": "10/04/2025",
                "client": {self.client_one_sales_user.email},
                "event": {self.event_one.event_id},
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_cant_delete_contract(self):
        response = self.client_api.delete(
            f"/api/contracts/{self.contract_client_one.contract_id}/"
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            Contract.objects.filter(
                contract_id=self.contract_client_one.contract_id
            ).exists()
        )
