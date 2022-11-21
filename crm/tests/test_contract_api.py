from tests.test_settings import TestData


class ContractManagerApiTestCase(TestData):
    def setUp(self):
        self.client_api.force_authenticate(self.manager_user)

    def test_can_get_contract_list(self):
        ...

    def test_can_get_contract_instance(self):
        ...

    def test_can_post_contract(self):
        # avec nimporte quelle sales contact, client et event
        ...

    def test_can_put_contract(self):
        # avec nimporte quelle sales contact, client et event
        ...

    def test_can_patch_contract(self):
        # avec nimporte quelle sales contact, client et event
        ...

    def test_can_delete_contract(self):
        ...


class ContractSalesApiTestCase(TestData):
    def setUp(self):
        self.client_api.force_authenticate(self.sales_user)

    def test_can_get_contract_list(self):
        ...

    def test_can_get_contract_instance(self):
        ...

    def test_can_post_contract(self):
        ...

    def test_can_put_contract(self):
        ...

    def test_can_patch_contract(self):
        ...

    def test_cant_put_contract_with_not_assigned_client(self):
        ...

    def test_cant_patch_contract_with_not_assigned_client(self):
        ...

    def test_cant_select_sales_contact(self):
        # avec post, put et patch
        ...

    def test_cant_select_event_of_not_assigned_client(self):
        # avec post, put et patch
        ...

    def test_cant_select_client_and_event_of_another_client(self):
        # avec post, put et patch
        ...

    def test_cant_delete_contract(self):
        ...


class ContractSupportApiTestCase(TestData):
    def setUp(self):
        self.client_api.force_authenticate(self.support_user)

    def test_can_get_contract_list(self):
        ...

    def test_can_get_contract_instance(self):
        ...

    def test_cant_post_contract(self):
        ...

    def test_cant_put_contract(self):
        ...

    def test_cant_patch_contract(self):
        ...

    def test_cant_delete_contract(self):
        ...
