from bs4 import BeautifulSoup
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

    def test_manager_can_choice_sales_contact_of_client(self):
        self.client.force_login(self.manager_user)
        response = self.client.get("/business/client/add/")
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(soup.find("select", id="id_sales_contact"))
        response = self.client.get(
            f"/business/client/{self.client_one_sales_user.client_id}/change/"
        )
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(soup.find("select", id="id_sales_contact"))

    def test_sales_cant_choice_sales_contact_of_client(self):
        self.client.force_login(self.sales_user)
        response = self.client.get("/business/client/add/")
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(
            soup.find("div", class_="form-row field-sales_contact").find(
                "div", class_="readonly"
            )
        )
        response = self.client.get(
            f"/business/client/{self.client_one_sales_user.client_id}/change/"
        )
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(
            soup.find("div", class_="form-row field-sales_contact").find(
                "div", class_="readonly"
            )
        )
