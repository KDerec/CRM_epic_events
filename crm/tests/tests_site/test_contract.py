from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from tests.test_settings import TestData
from business.models import Contract


class ContractManagerSiteTestCase(TestData):
    def setUp(self):
        self.client.force_login(self.manager_user)

    def test_can_change_all_contract(self):
        response = self.client.get(
            f"/business/contract/{self.contract_client_one.contract_id}/change/"
        )
        self.assertEqual(response.context["title"], "Modification de contract")
        response = self.client.get(
            f"/business/contract/{self.contract_client_two.contract_id}/change/"
        )
        self.assertEqual(response.context["title"], "Modification de contract")

    def test_can_choice_sales_contact_of_contract(self):
        response = self.client.get("/business/contract/add/")
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(soup.find("select", id="id_sales_contact"))
        response = self.client.get(
            f"/business/contract/{self.contract_client_one.contract_id}/change/"
        )
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(soup.find("select", id="id_sales_contact"))

    def test_can_choice_all_client_of_contract(self):
        response = self.client.get("/business/contract/add/")
        soup = BeautifulSoup(response.content, "html.parser")
        client_selection = soup.find("select", id="id_client").find_all("option")
        client_selection_txt = []
        for client in client_selection:
            client_selection_txt.append(client.text)

        self.assertIn(self.client_one_sales_user.__str__(), client_selection_txt)
        self.assertIn(self.client_two_sales_user_two.__str__(), client_selection_txt)

    def test_can_choice_all_event_of_contract(self):
        response = self.client.get("/business/contract/add/")
        soup = BeautifulSoup(response.content, "html.parser")
        event_selection = soup.find("select", id="id_event").find_all("option")
        event_selection_txt = []
        for event in event_selection:
            event_selection_txt.append(event.text)

        self.assertIn(self.event_one.__str__(), event_selection_txt)
        self.assertIn(self.event_two.__str__(), event_selection_txt)


class ContractSalesSiteTestCase(TestData):
    def setUp(self):
        self.client.force_login(self.sales_user)

    def test_can_change_his_assigned_contract(self):
        response = self.client.get(
            f"/business/contract/{self.contract_client_one.contract_id}/change/"
        )
        self.assertEqual(response.context["title"], "Modification de contract")

    def test_cant_change_not_assigned_contract(self):
        response = self.client.get(
            f"/business/contract/{self.contract_client_two.contract_id}/change/"
        )
        self.assertEqual(response.context["title"], "Affichage de contract")

    def test_cant_choice_sales_contact_of_contract(self):
        response = self.client.get("/business/contract/add/")
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(
            soup.find("div", class_="form-row field-sales_contact").find(
                "div", class_="readonly"
            )
        )
        response = self.client.get(
            f"/business/contract/{self.contract_client_one.contract_id}/change/"
        )
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(
            soup.find("div", class_="form-row field-sales_contact").find(
                "div", class_="readonly"
            )
        )

    def test_cant_choice_not_assigned_client_for_contract(self):
        response = self.client.get("/business/contract/add/")
        soup = BeautifulSoup(response.content, "html.parser")
        client_selection = soup.find("select", id="id_client").find_all("option")
        client_selection_txt = []
        for client in client_selection:
            client_selection_txt.append(client.text)

        self.assertNotIn(self.client_two_sales_user_two.__str__(), client_selection_txt)

    def test_cant_choice_event_of_not_assigned_client_for_contract(self):
        response = self.client.get("/business/contract/add/")
        soup = BeautifulSoup(response.content, "html.parser")
        event_selection = soup.find("select", id="id_event").find_all("option")
        event_selection_txt = []
        for event in event_selection:
            event_selection_txt.append(event.text)

        self.assertIn(self.event_one.__str__(), event_selection_txt)
        self.assertNotIn(self.event_two.__str__(), event_selection_txt)

    def test_cant_create_contract_with_client_and_event_of_another_client(self):
        with self.assertRaises(ValidationError):
            Contract(
                status=False,
                amount=10000,
                payment_due="2022-12-12",
                client=self.client_one_sales_user,
                sales_contact=self.sales_user,
                event=self.event_two,
            ).full_clean()


class ContractSupportSiteTestCase(TestData):
    def setUp(self):
        self.client.force_login(self.support_user)

    def test_can_view_contract(self):
        response = self.client.get(
            f"/business/contract/{self.contract_client_one.contract_id}/change/"
        )
        self.assertEqual(response.context["title"], "Affichage de contract")
        response = self.client.get(
            f"/business/contract/{self.contract_client_two.contract_id}/change/"
        )
        self.assertEqual(response.context["title"], "Affichage de contract")
