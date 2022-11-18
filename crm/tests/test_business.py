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

    def test_support_cant_choice_support_contact_of_event(self):
        self.client.force_login(self.support_user)
        response = self.client.get(f"/business/event/{self.event_one.event_id}/change/")
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(
            soup.find("div", class_="form-row field-support_contact").find(
                "div", class_="readonly"
            )
        )

    def test_support_cant_choice_client_of_event(self):
        self.client.force_login(self.support_user)
        response = self.client.get(f"/business/event/{self.event_one.event_id}/change/")
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(
            soup.find("div", class_="form-row field-client").find(
                "div", class_="readonly"
            )
        )

    def test_manager_can_choice_support_contact_of_event(self):
        self.client.force_login(self.manager_user)
        response = self.client.get(f"/business/event/{self.event_one.event_id}/change/")
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(soup.find("select", id="id_support_contact"))

    def test_manager_can_choice_client_of_event(self):
        self.client.force_login(self.manager_user)
        response = self.client.get(f"/business/event/{self.event_one.event_id}/change/")
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(soup.find("select", id="id_client"))

    def test_sales_cant_choice_not_assigned_client_for_event(self):
        self.client.force_login(self.sales_user)
        response = self.client.get("/business/event/add/")
        soup = BeautifulSoup(response.content, "html.parser")
        client_selection = soup.find("select", id="id_client").find_all("option")
        client_selection_txt = []
        for client in client_selection:
            client_selection_txt.append(client.text)

        self.assertNotIn(self.client_two_sales_user_two.__str__(), client_selection_txt)

    def test_sales_can_choice_support_contact_of_event(self):
        self.client.force_login(self.sales_user)
        response = self.client.get(f"/business/event/{self.event_one.event_id}/change/")
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(soup.find("select", id="id_support_contact"))

    def test_manager_can_choice_all_client_of_event(self):
        self.client.force_login(self.manager_user)
        response = self.client.get("/business/event/add/")
        soup = BeautifulSoup(response.content, "html.parser")
        client_selection = soup.find("select", id="id_client").find_all("option")
        client_selection_txt = []
        for client in client_selection:
            client_selection_txt.append(client.text)

        self.assertIn(self.client_one_sales_user.__str__(), client_selection_txt)
        self.assertIn(self.client_two_sales_user_two.__str__(), client_selection_txt)

    def test_only_support_user_are_in_support_contact_selection(self):
        self.client.force_login(self.manager_user)
        response = self.client.get("/business/event/add/")
        soup = BeautifulSoup(response.content, "html.parser")
        support_selection = soup.find("select", id="id_support_contact").find_all(
            "option"
        )
        support_selection_txt = []
        for support in support_selection:
            support_selection_txt.append(support.text)

        self.assertIn(self.support_user.__str__(), support_selection_txt)
        self.assertIn(self.support_user_two.__str__(), support_selection_txt)
        self.assertNotIn(self.sales_user.__str__(), support_selection_txt)


class ContractTestCase(TestData):
    def test_manager_can_change_all_contract(self):
        self.client.force_login(self.manager_user)
        response = self.client.get(
            f"/business/contract/{self.contract_client_one.contract_id}/change/"
        )
        self.assertEqual(response.context["title"], "Modification de contract")
        response = self.client.get(
            f"/business/contract/{self.contract_client_two.contract_id}/change/"
        )
        self.assertEqual(response.context["title"], "Modification de contract")

    def test_support_can_view_contract(self):
        self.client.force_login(self.support_user)
        response = self.client.get(
            f"/business/contract/{self.contract_client_one.contract_id}/change/"
        )
        self.assertEqual(response.context["title"], "Affichage de contract")
        response = self.client.get(
            f"/business/contract/{self.contract_client_two.contract_id}/change/"
        )
        self.assertEqual(response.context["title"], "Affichage de contract")

    def test_sales_can_change_is_assigned_contract(self):
        self.client.force_login(self.sales_user)
        response = self.client.get(
            f"/business/contract/{self.contract_client_one.contract_id}/change/"
        )
        self.assertEqual(response.context["title"], "Modification de contract")

    def test_sales_cant_change_not_assigned_contract(self):
        self.client.force_login(self.sales_user)
        response = self.client.get(
            f"/business/contract/{self.contract_client_two.contract_id}/change/"
        )
        self.assertEqual(response.context["title"], "Affichage de contract")

    def test_manager_can_choice_sales_contact_of_contract(self):
        self.client.force_login(self.manager_user)
        response = self.client.get("/business/contract/add/")
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(soup.find("select", id="id_sales_contact"))
        response = self.client.get(
            f"/business/contract/{self.contract_client_one.contract_id}/change/"
        )
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(soup.find("select", id="id_sales_contact"))

    def test_sales_cant_choice_sales_contact_of_contract(self):
        self.client.force_login(self.sales_user)
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

    def test_sales_cant_choice_not_assigned_client_of_contract(self):
        self.client.force_login(self.sales_user)
        response = self.client.get("/business/contract/add/")
        soup = BeautifulSoup(response.content, "html.parser")
        client_selection = soup.find("select", id="id_client").find_all("option")
        client_selection_txt = []
        for client in client_selection:
            client_selection_txt.append(client.text)

        self.assertNotIn(self.client_two_sales_user_two.__str__(), client_selection_txt)

    def test_manager_can_choice_all_client_of_contract(self):
        self.client.force_login(self.manager_user)
        response = self.client.get("/business/contract/add/")
        soup = BeautifulSoup(response.content, "html.parser")
        client_selection = soup.find("select", id="id_client").find_all("option")
        client_selection_txt = []
        for client in client_selection:
            client_selection_txt.append(client.text)

        self.assertIn(self.client_one_sales_user.__str__(), client_selection_txt)
        self.assertIn(self.client_two_sales_user_two.__str__(), client_selection_txt)

    def test_manager_can_choice_all_event_of_contract(self):
        self.client.force_login(self.manager_user)
        response = self.client.get("/business/contract/add/")
        soup = BeautifulSoup(response.content, "html.parser")
        event_selection = soup.find("select", id="id_event").find_all("option")
        event_selection_txt = []
        for event in event_selection:
            event_selection_txt.append(event.text)

        self.assertIn(self.event_one.__str__(), event_selection_txt)
        self.assertIn(self.event_two.__str__(), event_selection_txt)

    def test_sales_cant_choice_event_of_not_assigned_client_of_contract(self):
        self.client.force_login(self.sales_user)
        response = self.client.get("/business/contract/add/")
        soup = BeautifulSoup(response.content, "html.parser")
        event_selection = soup.find("select", id="id_event").find_all("option")
        event_selection_txt = []
        for event in event_selection:
            event_selection_txt.append(event.text)

        self.assertIn(self.event_one.__str__(), event_selection_txt)
        self.assertNotIn(self.event_two.__str__(), event_selection_txt)
