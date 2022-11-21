from tests.test_settings import TestData
from accounts.models import User


class UserSiteTestCase(TestData):
    def test_user_and_group_exist_in_db(self):
        self.assertEqual(self.support_user.username, "support_user")
        self.assertTrue(self.support_user.groups.filter(name="Support").exists())

    def test_user_can_login(self):
        self.client.force_login(self.manager_user)
        response = self.client.get("/")
        self.assertTrue(response.context["user"].is_authenticated)


class UserApiTestCase(TestData):
    def test_unlogged_user_cant_access_to_api(self):
        response = self.client_api.get("/api/")
        self.assertEqual(response.status_code, 403)

    def test_logged_user_and_access_to_api(self):
        self.client_api.force_authenticate(self.manager_user)
        response = self.client_api.get("/api/")
        self.assertEqual(response.status_code, 200)

    def test_manager_can_create_user_with_group_manager(self):
        self.client_api.force_authenticate(self.manager_user)
        response = self.client_api.post(
            "/api/users/",
            {
                "username": "username_name",
                "password": "correctpassword",
                "groups": "Manager",
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_manager_can_create_user_with_group_sales(self):
        self.client_api.force_authenticate(self.manager_user)
        response = self.client_api.post(
            "/api/users/",
            {
                "username": "username_name1",
                "password": "correctpassword",
                "groups": "Sales",
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_manager_can_create_user_with_group_support(self):
        self.client_api.force_authenticate(self.manager_user)
        response = self.client_api.post(
            "/api/users/",
            {
                "username": "username_name2",
                "password": "correctpassword",
                "groups": "Support",
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_manager_create_user_with_wrong_data(self):
        self.client_api.force_authenticate(self.manager_user)
        response = self.client_api.post(
            "/api/users/",
            {
                "username": "username_name3",
                "password": "correctpassword",
                "groups": 1,
            },
        )
        self.assertEqual(response.data[0].code, "invalid")

    def test_created_manager_can_access_to_api(self):
        self.client_api.force_authenticate(self.manager_user)
        self.client_api.post(
            "/api/users/",
            {
                "username": "username_name4",
                "password": "correctpassword",
                "groups": "Manager",
            },
        )
        self.client_api.force_authenticate(User.objects.get(username="username_name4"))
        response = self.client_api.get("/api/")
        self.assertEqual(response.status_code, 200)

    def test_sales_cant_create_user(self):
        self.client_api.force_authenticate(self.sales_user)
        response = self.client_api.post(
            "/api/users/",
            {
                "username": "usernametest",
                "password": "correctpassword",
                "groups": "Support",
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_support_cant_create_user(self):
        self.client_api.force_authenticate(self.support_user)
        response = self.client_api.post(
            "/api/users/",
            {
                "username": "usernametest",
                "password": "correctpassword",
                "groups": "Support",
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_manager_can_put_groups_of_user(self):
        self.client_api.force_authenticate(self.manager_user)
        response = self.client_api.put(
            f"/api/users/{self.support_user.id}/",
            {
                f"username": {self.support_user.username},
                "groups": "Manager",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.support_user.groups.get().__str__(), "Manager")

    def test_manager_can_patch_groups_of_user(self):
        self.client_api.force_authenticate(self.manager_user)
        response = self.client_api.patch(
            f"/api/users/{self.support_user.id}/",
            {
                "groups": "Manager",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.support_user.groups.get().__str__(), "Manager")

    def test_sales_cant_update_user(self):
        self.client_api.force_authenticate(self.sales_user)
        response = self.client_api.put(
            f"/api/users/{self.support_user.id}/",
            {
                "groups": "Manager",
            },
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.support_user.groups.get().__str__(), "Support")

    def test_support_cant_update_user(self):
        self.client_api.force_authenticate(self.support_user)
        response = self.client_api.put(
            f"/api/users/{self.support_user.id}/",
            {
                "groups": "Manager",
            },
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.support_user.groups.get().__str__(), "Support")

    def test_manager_cant_interact_with_groups(self):
        self.client_api.force_authenticate(self.manager_user)
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
        response = self.client_api.delete(
            f"/api/groups/{self.manager_group.id}/", {"name": "test"}
        )
        self.assertEqual(response.status_code, 403)

    def test_sales_cant_interact_with_groups(self):
        self.client_api.force_authenticate(self.sales_user)
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
        response = self.client_api.delete(
            f"/api/groups/{self.manager_group.id}/", {"name": "test"}
        )
        self.assertEqual(response.status_code, 403)

    def test_support_cant_interact_with_groups(self):
        self.client_api.force_authenticate(self.support_user)
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
        response = self.client_api.delete(
            f"/api/groups/{self.manager_group.id}/", {"name": "test"}
        )
        self.assertEqual(response.status_code, 403)

    def test_manager_cant_modify_superuser(self):
        self.client_api.force_authenticate(self.manager_user)
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
