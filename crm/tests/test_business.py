from tests.test_settings import TestData
from business.models import Client, Contract, Event
from accounts.models import User


class ClientTestCase(TestData):
    def test_user_is_here(self):
        self.assertEqual(self.support_user.username, "support_user")
        self.assertEqual(self.support_user.groups.filter(name="Support").exists(), True)
