from bs4 import BeautifulSoup
from tests.test_settings import TestData


class EventGeneralSiteTestCase(TestData):
    def setUp(self):
        self.client.force_login(self.manager_user)

    def test_only_support_user_are_in_support_contact_selection(self):
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


class EventManagerSiteTestCase(TestData):
    def setUp(self):
        self.client.force_login(self.manager_user)

    def test_can_change_all_event(self):
        response = self.client.get(f"/business/event/{self.event_one.event_id}/change/")
        self.assertEqual(response.context["title"], "Modification de event")

    def test_can_choice_support_contact_of_event(self):
        response = self.client.get(f"/business/event/{self.event_one.event_id}/change/")
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(soup.find("select", id="id_support_contact"))

    def test_can_choice_client_of_event(self):
        response = self.client.get(f"/business/event/{self.event_one.event_id}/change/")
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(soup.find("select", id="id_client"))

    def test_can_choice_all_client_of_event(self):
        response = self.client.get("/business/event/add/")
        soup = BeautifulSoup(response.content, "html.parser")
        client_selection = soup.find("select", id="id_client").find_all("option")
        client_selection_txt = []
        for client in client_selection:
            client_selection_txt.append(client.text)

        self.assertIn(self.client_one_sales_user.__str__(), client_selection_txt)
        self.assertIn(self.client_two_sales_user_two.__str__(), client_selection_txt)


class EventSalesSiteTestCase(TestData):
    def setUp(self):
        self.client.force_login(self.sales_user)

    def test_can_change_assigned_event(self):
        response = self.client.get(f"/business/event/{self.event_one.event_id}/change/")
        self.assertEqual(response.context["title"], "Modification de event")

    def test_cant_change_not_assigned_event(self):
        self.client.force_login(self.sales_user_two)
        response = self.client.get(f"/business/event/{self.event_one.event_id}/change/")
        self.assertEqual(response.context["title"], "Affichage de event")

    def test_cant_choice_not_assigned_client(self):
        response = self.client.get("/business/event/add/")
        soup = BeautifulSoup(response.content, "html.parser")
        client_selection = soup.find("select", id="id_client").find_all("option")
        client_selection_txt = []
        for client in client_selection:
            client_selection_txt.append(client.text)

        self.assertNotIn(self.client_two_sales_user_two.__str__(), client_selection_txt)

    def test_can_choice_support_contact(self):
        response = self.client.get(f"/business/event/{self.event_one.event_id}/change/")
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(soup.find("select", id="id_support_contact"))


class EventSupportSiteTestCase(TestData):
    def setUp(self):
        self.client.force_login(self.support_user)

    def test_can_change_assigned_event(self):
        response = self.client.get(f"/business/event/{self.event_one.event_id}/change/")
        self.assertEqual(response.context["title"], "Modification de event")

    def test_cant_change_not_assigned_event(self):
        self.client.force_login(self.support_user_two)
        response = self.client.get(f"/business/event/{self.event_one.event_id}/change/")
        self.assertEqual(response.context["title"], "Affichage de event")

    def test_cant_choice_support_contact(self):
        response = self.client.get(f"/business/event/{self.event_one.event_id}/change/")
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(
            soup.find("div", class_="form-row field-support_contact").find(
                "div", class_="readonly"
            )
        )

    def test_cant_choice_client(self):
        response = self.client.get(f"/business/event/{self.event_one.event_id}/change/")
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(
            soup.find("div", class_="form-row field-client").find(
                "div", class_="readonly"
            )
        )
