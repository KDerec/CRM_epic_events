from tests.test_settings import TestData


class ClientTestCase(TestData):
    def test_manager_can_change_all_client(self):
        self.client.force_login(self.manager_user)
        response = self.client.get(
            f"/business/client/{self.client_one_sales_user.client_id}/change/"
        )
        self.assertEqual(response.context["title"], "Modification de client")
        response = self.client.get(
            f"/business/client/{self.client_two_sales_user_two.client_id}/change/"
        )
        self.assertEqual(response.context["title"], "Modification de client")

    def test_support_can_view_client(self):
        self.client.force_login(self.support_user)
        response = self.client.get(
            f"/business/client/{self.client_one_sales_user.client_id}/change/"
        )
        self.assertEqual(response.context["title"], "Affichage de client")
        response = self.client.get(
            f"/business/client/{self.client_two_sales_user_two.client_id}/change/"
        )
        self.assertEqual(response.context["title"], "Affichage de client")

    def test_sales_can_change_is_assigned_client(self):
        self.client.force_login(self.sales_user)
        response = self.client.get(
            f"/business/client/{self.client_one_sales_user.client_id}/change/"
        )
        self.assertEqual(response.context["title"], "Modification de client")

    def test_sales_cant_change_not_assigned_client(self):
        self.client.force_login(self.sales_user)
        response = self.client.get(
            f"/business/client/{self.client_two_sales_user_two.client_id}/change/"
        )
        self.assertEqual(response.context["title"], "Affichage de client")


class EventTestCase(TestData):
    def test_manager_can_change_all_event(self):
        self.client.force_login(self.manager_user)
        response = self.client.get(f"/business/event/{self.event_one.event_id}/change/")
        self.assertEqual(response.context["title"], "Modification de event")

    def test_support_can_change_assigned_event(self):
        self.client.force_login(self.support_user)
        response = self.client.get(f"/business/event/{self.event_one.event_id}/change/")
        self.assertEqual(response.context["title"], "Modification de event")

    def test_support_cant_change_not_assigned_event(self):
        self.client.force_login(self.support_user_two)
        response = self.client.get(f"/business/event/{self.event_one.event_id}/change/")
        self.assertEqual(response.context["title"], "Affichage de event")

    def test_sales_can_change_assigned_event(self):
        self.client.force_login(self.sales_user)
        response = self.client.get(f"/business/event/{self.event_one.event_id}/change/")
        self.assertEqual(response.context["title"], "Modification de event")

    def test_sales_cant_change_not_assigned_event(self):
        self.client.force_login(self.sales_user_two)
        response = self.client.get(f"/business/event/{self.event_one.event_id}/change/")
        self.assertEqual(response.context["title"], "Affichage de event")


