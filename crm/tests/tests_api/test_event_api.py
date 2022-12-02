from tests.test_settings import TestData
from business.models import Event


class EventManagerApiTestCase(TestData):
    def setUp(self):
        self.client_api.force_authenticate(self.manager_user)

    def test_can_get_event_list(self):
        response = self.client_api.get("/api/events/")
        self.assertEqual(response.status_code, 200)

    def test_can_get_event_instance(self):
        response = self.client_api.get(f"/api/events/{self.event_one.event_id}/")
        self.assertEqual(response.status_code, 200)

    def test_can_get_object_with_filter_in_url(self):
        response = self.client_api.get(
            f"/api/events/?client__last_name={self.client_one_sales_user.last_name}&client__email={self.client_one_sales_user.email}&event_date={self.event_one.event_date}"
        )
        self.assertEqual(response.data["count"], 1)

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
                "client": {self.client_one_sales_user.email},
                "support_contact": {self.support_user.username},
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_can_put_event(self):
        response = self.client_api.put(
            f"/api/events/{self.event_one.event_id}/",
            {
                "status": "False",
                "attendees": "2000",
                "event_date": "01/01/2023",
                "notes": "Giga party",
                "client": {self.client_one_sales_user.email},
                "support_contact": {self.support_user_two.username},
            },
        )
        self.assertEqual(response.status_code, 200)
        event = Event.objects.get(event_id=self.event_one.event_id)
        self.assertEqual(event.attendees, 2000)
        self.assertEqual(event.support_contact, self.support_user_two)

    def test_can_patch_event(self):
        response = self.client_api.patch(
            f"/api/events/{self.event_one.event_id}/",
            {
                "status": "False",
                "attendees": "2000",
                "event_date": "01/01/2023",
                "notes": "Giga party",
                "client": {self.client_one_sales_user.email},
                "support_contact": {self.support_user_two.username},
            },
        )
        self.assertEqual(response.status_code, 200)
        event = Event.objects.get(event_id=self.event_one.event_id)
        self.assertEqual(event.attendees, 2000)
        self.assertEqual(event.support_contact, self.support_user_two)

    def test_can_delete_event(self):
        self.client_api.delete(f"/api/events/{self.event_one.event_id}/")

        self.assertFalse(
            Event.objects.filter(event_id=self.event_one.event_id).exists()
        )


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
        response = self.client_api.post(
            "/api/events/",
            {
                "status": "False",
                "attendees": "20",
                "event_date": "01/01/2023",
                "notes": "New year party",
                "client": {self.client_one_sales_user.email},
                "support_contact": {self.support_user.username},
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_cant_post_event_with_support_contact_not_in_support_group(self):
        response = self.client_api.post(
            "/api/events/",
            {
                "status": "False",
                "attendees": "20",
                "event_date": "01/01/2023",
                "notes": "New year party",
                "client": {self.client_one_sales_user.email},
                "support_contact": {self.manager_user.username},
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_cant_post_event_with_not_assigned_client(self):
        response = self.client_api.post(
            "/api/events/",
            {
                "status": "False",
                "attendees": "20",
                "event_date": "01/01/2023",
                "notes": "New year party",
                "client": {self.client_two_sales_user_two.email},
                "support_contact": {self.support_user.username},
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_can_put_event(self):
        response = self.client_api.put(
            f"/api/events/{self.event_one.event_id}/",
            {
                "status": "False",
                "attendees": "2000",
                "event_date": "01/01/2023",
                "notes": "Giga party",
                "client": {self.client_one_sales_user.email},
                "support_contact": {self.support_user_two.username},
            },
        )
        self.assertEqual(response.status_code, 200)
        event = Event.objects.get(event_id=self.event_one.event_id)
        self.assertEqual(event.attendees, 2000)
        self.assertEqual(event.support_contact, self.support_user_two)

    def test_cant_put_event_with_not_assigned_client(self):
        response = self.client_api.put(
            f"/api/events/{self.event_one.event_id}/",
            {
                "status": "False",
                "attendees": "2000",
                "event_date": "01/01/2023",
                "notes": "Giga party",
                "client": {self.client_two_sales_user_two.email},
                "support_contact": {self.support_user_two.username},
            },
        )
        self.assertEqual(response.status_code, 400)
        event = Event.objects.get(event_id=self.event_one.event_id)
        self.assertEqual(event.attendees, 10)
        self.assertEqual(event.support_contact, self.support_user)

    def test_cant_put_event_of_not_assigned_client(self):
        response = self.client_api.put(
            f"/api/events/{self.event_two.event_id}/",
            {
                "status": "False",
                "attendees": "2000",
                "event_date": "01/01/2023",
                "notes": "Giga party",
                "client": {self.client_two_sales_user_two.email},
                "support_contact": {self.support_user_two.username},
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_can_patch_event(self):
        response = self.client_api.patch(
            f"/api/events/{self.event_one.event_id}/",
            {
                "status": "False",
                "attendees": "2000",
                "event_date": "01/01/2023",
                "notes": "Giga party",
                "client": {self.client_one_sales_user.email},
                "support_contact": {self.support_user_two.username},
            },
        )
        self.assertEqual(response.status_code, 200)
        event = Event.objects.get(event_id=self.event_one.event_id)
        self.assertEqual(event.attendees, 2000)
        self.assertEqual(event.support_contact, self.support_user_two)

    def test_cant_patch_event_with_not_assigned_client(self):
        response = self.client_api.patch(
            f"/api/events/{self.event_one.event_id}/",
            {
                "status": "False",
                "attendees": "2000",
                "event_date": "01/01/2023",
                "notes": "Giga party",
                "client": {self.client_two_sales_user_two.email},
                "support_contact": {self.support_user_two.username},
            },
        )
        self.assertEqual(response.status_code, 400)
        event = Event.objects.get(event_id=self.event_one.event_id)
        self.assertEqual(event.attendees, 10)
        self.assertEqual(event.support_contact, self.support_user)

    def test_cant_patch_event_of_not_assigned_client(self):
        response = self.client_api.patch(
            f"/api/events/{self.event_two.event_id}/",
            {
                "status": "False",
                "attendees": "2000",
                "event_date": "01/01/2023",
                "notes": "Giga party",
                "client": {self.client_two_sales_user_two.email},
                "support_contact": {self.support_user_two.username},
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_cant_delete_event(self):
        response = self.client_api.delete(f"/api/events/{self.event_one.event_id}/")
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Event.objects.filter(event_id=self.event_one.event_id).exists())


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
        response = self.client_api.post(
            "/api/events/",
            {
                "status": "False",
                "attendees": "20",
                "event_date": "01/01/2023",
                "notes": "New year party",
                "client": {self.client_one_sales_user.email},
                "support_contact": {self.support_user.username},
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_can_put_event(self):
        response = self.client_api.put(
            f"/api/events/{self.event_one.event_id}/",
            {
                "status": "False",
                "attendees": "2000",
                "event_date": "01/01/2023",
                "notes": "Giga party",
            },
        )
        self.assertEqual(response.status_code, 200)
        event = Event.objects.get(event_id=self.event_one.event_id)
        self.assertEqual(event.attendees, 2000)
        self.assertEqual(event.support_contact, self.support_user)
        self.assertEqual(event.client, self.client_one_sales_user)

    def test_cant_put_not_assigned_event(self):
        response = self.client_api.put(
            f"/api/events/{self.event_two.event_id}/",
            {
                "status": "False",
                "attendees": "2000",
                "event_date": "01/01/2023",
                "notes": "Giga party",
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_can_patch_event(self):
        response = self.client_api.patch(
            f"/api/events/{self.event_one.event_id}/",
            {
                "status": "False",
                "attendees": "2000",
                "event_date": "01/01/2023",
                "notes": "Giga party",
            },
        )
        self.assertEqual(response.status_code, 200)
        event = Event.objects.get(event_id=self.event_one.event_id)
        self.assertEqual(event.attendees, 2000)
        self.assertEqual(event.support_contact, self.support_user)
        self.assertEqual(event.client, self.client_one_sales_user)

    def test_cant_patch_not_assigned_event(self):
        response = self.client_api.patch(
            f"/api/events/{self.event_two.event_id}/",
            {
                "status": "False",
                "attendees": "2000",
                "event_date": "01/01/2023",
                "notes": "Giga party",
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_cant_select_support_contact(self):
        response = self.client_api.put(
            f"/api/events/{self.event_one.event_id}/",
            {
                "status": "False",
                "attendees": "2000",
                "event_date": "01/01/2023",
                "notes": "Giga party",
                "support_contact": {self.support_user_two.username},
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client_api.patch(
            f"/api/events/{self.event_one.event_id}/",
            {
                "status": "False",
                "attendees": "2000",
                "event_date": "01/01/2023",
                "notes": "Giga party",
                "support_contact": {self.support_user_two.username},
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_cant_select_client(self):
        response = self.client_api.put(
            f"/api/events/{self.event_one.event_id}/",
            {
                "status": "False",
                "attendees": "2000",
                "event_date": "01/01/2023",
                "notes": "Giga party",
                "client": {self.client_two_sales_user_two.email},
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client_api.patch(
            f"/api/events/{self.event_one.event_id}/",
            {
                "status": "False",
                "attendees": "2000",
                "event_date": "01/01/2023",
                "notes": "Giga party",
                "client": {self.client_two_sales_user_two.email},
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_cant_delete_event(self):
        response = self.client_api.delete(f"/api/events/{self.event_one.event_id}/")
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Event.objects.filter(event_id=self.event_one.event_id).exists())
