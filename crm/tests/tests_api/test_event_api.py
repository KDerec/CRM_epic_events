from tests.test_settings import TestData


class EventManagerApiTestCase(TestData):
    def setUp(self):
        self.client_api.force_authenticate(self.manager_user)

    def test_can_get_event_list(self):
        response = self.client_api.get("/api/events/")
        self.assertEqual(response.status_code, 200)

    def test_can_get_event_instance(self):
        response = self.client_api.get(f"/api/events/{self.event_one.event_id}/")
        self.assertEqual(response.status_code, 200)

    def test_cant_get_unknow_contract_id(self):
        response = self.client_api.get("/api/events/99/")
        self.assertEqual(response.status_code, 404)

    def test_can_post_event(self):
        response = self.client_api.post(
            "/api/events/",
            {
                "status": "False",
                "attendees": "20",
                "event_date": "01/01/2023",
                "notes": "New year party",
                f"client": {self.client_one_sales_user.email},
                f"support_contact": {self.support_user.username},
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_can_put_event(self):
        # avec n'importe quels client ou support_contact
        ...

    def test_can_patch_event(self):
        # avec n'importe quels client ou support_contact
        ...

    def test_can_delete_event(self):
        ...


class EventSalesApiTestCase(TestData):
    def setUp(self):
        self.client_api.force_authenticate(self.sales_user)

    def test_can_get_event_list(self):
        response = self.client_api.get("/api/events/")
        self.assertEqual(response.status_code, 200)

    def test_can_get_event_instance(self):
        response = self.client_api.get(f"/api/events/{self.event_one.event_id}/")
        self.assertEqual(response.status_code, 200)

    def test_can_post_event(self):
        ...

    def test_can_put_event(self):
        ...

    def test_can_patch_event(self):
        ...

    def test_cant_post_event_with_not_assigned_client(self):
        ...

    def test_cant_put_event_with_not_assigned_client(self):
        ...

    def test_cant_patch_event_with_not_assigned_client(self):
        ...

    def test_cant_delete_event(self):
        ...


class EventSupportApiTestCase(TestData):
    def setUp(self):
        self.client_api.force_authenticate(self.support_user)

    def test_can_get_event_list(self):
        response = self.client_api.get("/api/events/")
        self.assertEqual(response.status_code, 200)

    def test_can_get_event_instance(self):
        response = self.client_api.get(f"/api/events/{self.event_one.event_id}/")
        self.assertEqual(response.status_code, 200)

    def test_cant_post_event(self):
        ...

    def test_can_put_event(self):
        ...

    def test_can_patch_event(self):
        ...

    def test_cant_put_not_assigned_event(self):
        ...

    def test_cant_patch_not_assigned_event(self):
        ...

    def test_cant_select_support_contact(self):
        # avec post, put et patch
        ...

    def test_cant_select_client(self):
        # avec post, put et patch
        ...

    def test_cant_delete_event(self):
        ...
