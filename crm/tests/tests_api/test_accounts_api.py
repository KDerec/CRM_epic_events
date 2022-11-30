from tests.test_settings import TestData
from accounts.models import User


class GeneralUserApiTestCase(TestData):
    def test_unlogged_user_cant_access_to_api(self):
        response = self.client_api.get("/api/")
        self.assertEqual(response.status_code, 401)


class ManagerUserApiTestCase(TestData):
    def setUp(self):
        self.client_api.force_authenticate(self.manager_user)

    def test_can_access_to_api(self):
        response = self.client_api.get("/api/")
        self.assertEqual(response.status_code, 200)

    def test_can_create_user_with_manager_group(self):
        response = self.client_api.post(
            "/api/users/",
            {
                "username": "Name",
                "password": "Changemepassword",
                "groups": "Manager",
            },
        )
        group = User.objects.get(username="Name").groups.get().__str__()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(group, "Manager")

    def test_can_create_user_with_sales_group(self):
        response = self.client_api.post(
            "/api/users/",
            {
                "username": "Name",
                "password": "Changemepassword",
                "groups": "Sales",
            },
        )
        group = User.objects.get(username="Name").groups.get().__str__()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(group, "Sales")

    def test_can_create_user_with_support_group(self):
        response = self.client_api.post(
            "/api/users/",
            {
                "username": "Name",
                "password": "Changemepassword",
                "groups": "Support",
            },
        )
        group = User.objects.get(username="Name").groups.get().__str__()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(group, "Support")

    def test_create_user_with_wrong_data(self):
        response = self.client_api.post(
            "/api/users/",
            {
                "username": "Name",
                "password": "Changemepassword",
                "groups": 1,
            },
        )
        self.assertEqual(response.data[0].code, "invalid")

    def test_created_user_with_post_method_can_access_to_api(self):
        self.client_api.post(
            "/api/users/",
            {
                "username": "Name",
                "password": "Changemepassword",
                "groups": "Manager",
            },
        )
        self.client_api.force_authenticate(User.objects.get(username="Name"))
        response = self.client_api.get("/api/")
        self.assertEqual(response.status_code, 200)

    def test_can_put_group_for_existing_user(self):
        response = self.client_api.put(
            f"/api/users/{self.support_user.id}/",
            {
                "username": {self.support_user.username},
                "groups": "Manager",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.support_user.groups.get().__str__(), "Manager")

    def test_can_patch_group_for_existing_user(self):
        response = self.client_api.patch(
            f"/api/users/{self.support_user.id}/",
            {
                "groups": "Manager",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.support_user.groups.get().__str__(), "Manager")

    def test_can_delete_user(self):
        self.client_api.delete(f"/api/users/{self.support_user.id}/")
        self.assertFalse(User.objects.filter(username={self.support_group}).exists())

    def test_cant_interact_with_groups_object(self):
        response = self.client_api.get("/api/groups/")
        self.assertEqual(response.status_code, 403)
        response = self.client_api.get(f"/api/groups/{self.manager_group.id}/")
        self.assertEqual(response.status_code, 403)
        response = self.client_api.post("/api/groups/", {"name": "test"})
        self.assertEqual(response.status_code, 403)
        response = self.client_api.put(
            f"/api/groups/{self.manager_group.id}/", {"name": "test"}
        )
        self.assertEqual(response.status_code, 403)
        response = self.client_api.delete(f"/api/groups/{self.manager_group.id}/")
        self.assertEqual(response.status_code, 403)

    def test_cant_interact_with_superuser(self):
        response = self.client_api.get(f"/api/users/{self.admin_user.id}/")
        self.assertEqual(response.status_code, 403)
        response = self.client_api.patch(
            f"/api/users/{self.admin_user.id}/",
            {"username": "test", "groups": "Manager"},
        )
        self.assertEqual(response.status_code, 403)
        response = self.client_api.put(
            f"/api/users/{self.admin_user.id}/", {"username": "test"}
        )
        self.assertEqual(response.status_code, 403)
        response = self.client_api.delete(f"/api/users/{self.admin_user.id}/")
        self.assertEqual(response.status_code, 403)


class SalesUserApiTestCase(TestData):
    def setUp(self):
        self.client_api.force_authenticate(self.sales_user)

    def test_can_access_to_api(self):
        response = self.client_api.get("/api/")
        self.assertEqual(response.status_code, 200)

    def test_can_view_user(self):
        response = self.client_api.get(f"/api/users/{self.support_user.id}/")
        self.assertEqual(response.status_code, 200)

    def test_cant_post_put_patch_delete_user_object(self):
        response = self.client_api.post(
            "/api/users/",
            {
                "username": "Name",
                "password": "Changemepassword",
                "groups": "Support",
            },
        )
        self.assertEqual(response.status_code, 403)

        response = self.client_api.put(
            f"/api/users/{self.support_user.id}/",
            {
                "username": {self.support_user.username},
                "groups": "Manager",
            },
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.support_user.groups.get().__str__(), "Support")

        response = self.client_api.patch(
            f"/api/users/{self.support_user.id}/",
            {
                "groups": "Manager",
            },
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.support_user.groups.get().__str__(), "Support")

        response = self.client_api.delete(f"/api/users/{self.support_user.id}/")
        self.assertEqual(response.status_code, 403)

    def test_cant_interact_with_groups_object(self):
        response = self.client_api.get("/api/groups/")
        self.assertEqual(response.status_code, 403)
        response = self.client_api.get(f"/api/groups/{self.manager_group.id}/")
        self.assertEqual(response.status_code, 403)
        response = self.client_api.post("/api/groups/", {"name": "test"})
        self.assertEqual(response.status_code, 403)
        response = self.client_api.put(
            f"/api/groups/{self.manager_group.id}/", {"name": "test"}
        )
        self.assertEqual(response.status_code, 403)
        response = self.client_api.delete(f"/api/groups/{self.manager_group.id}/")
        self.assertEqual(response.status_code, 403)


class SupportUserApiTestCase(TestData):
    def setUp(self):
        self.client_api.force_authenticate(self.support_user)

    def test_can_access_to_api(self):
        response = self.client_api.get("/api/")
        self.assertEqual(response.status_code, 200)

    def test_can_view_user(self):
        response = self.client_api.get(f"/api/users/{self.support_user.id}/")
        self.assertEqual(response.status_code, 200)

    def test_cant_post_put_patch_delete_user_object(self):
        response = self.client_api.post(
            "/api/users/",
            {
                "username": "Name",
                "password": "Changemepassword",
                "groups": "Support",
            },
        )
        self.assertEqual(response.status_code, 403)

        response = self.client_api.put(
            f"/api/users/{self.support_user.id}/",
            {
                "username": {self.support_user.username},
                "groups": "Manager",
            },
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.support_user.groups.get().__str__(), "Support")

        response = self.client_api.patch(
            f"/api/users/{self.support_user.id}/",
            {
                "groups": "Manager",
            },
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.support_user.groups.get().__str__(), "Support")

        response = self.client_api.delete(f"/api/users/{self.support_user.id}/")
        self.assertEqual(response.status_code, 403)

    def test_cant_interact_with_groups_object(self):
        response = self.client_api.get("/api/groups/")
        self.assertEqual(response.status_code, 403)
        response = self.client_api.get(f"/api/groups/{self.manager_group.id}/")
        self.assertEqual(response.status_code, 403)
        response = self.client_api.post("/api/groups/", {"name": "test"})
        self.assertEqual(response.status_code, 403)
        response = self.client_api.put(
            f"/api/groups/{self.manager_group.id}/", {"name": "test"}
        )
        self.assertEqual(response.status_code, 403)
        response = self.client_api.delete(f"/api/groups/{self.manager_group.id}/")
        self.assertEqual(response.status_code, 403)
