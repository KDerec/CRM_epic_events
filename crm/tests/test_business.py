from tests.test_settings import TestData
from business.models import Client, Contract, Event
from accounts.models import User


class ClientTestCase(TestData):
    def test_manager_can_change_all_client(self):
        self.client.force_login(self.manager_user)
        response = self.client.get("/business/client/3/change/")
        self.assertEqual(response.context["title"], "Modification de client")
        response = self.client.get("/business/client/4/change/")
        self.assertEqual(response.context["title"], "Modification de client")

    def test_support_can_view_client(self):
        self.client.force_login(self.support_user)
        response = self.client.get("/business/client/3/change/")
        self.assertEqual(response.context["title"], "Affichage de client")
        response = self.client.get("/business/client/4/change/")
        self.assertEqual(response.context["title"], "Affichage de client")

    def test_sales_can_change_is_assigned_client(self):
        self.client.force_login(self.sales_user)
        response = self.client.get("/business/client/3/change/")
        self.assertEqual(response.context["title"], "Modification de client")

    def test_sales_cant_change_not_assigned_client(self):
        self.client.force_login(self.sales_user)
        response = self.client.get("/business/client/4/change/")
        self.assertEqual(response.context["title"], "Affichage de client")
