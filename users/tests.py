import json

from django.db import IntegrityError
from django.test import TestCase, Client
from django.urls import reverse_lazy

from .models import CustomUser as User


class UserModelTests(TestCase):
    def setUp(self):
        # Create a sample book instance for testing
        self.admin_user = User.objects.create_superuser(
            username="admin", password="admin", email='admin@local.com'
        )
        self.simple_user = User.objects.create_superuser(
            username="simple_user", password="simple_user", email='simple_user@local.com'
        )

    def test_create_new_user(self):
        """
        In this scenario we test creating a user that is already existed. It should
        """
        new_user = User.objects.create_user(
            username="newuser", password="newuser", email='newuser@local.com'
        )

        # Check if the new user was created successfully
        self.assertEqual(new_user.username, "newuser")
        self.assertTrue(new_user.check_password('newuser'))
        self.assertEqual(new_user.email, 'newuser@local.com')

        # Verify the new user exists in the database
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_create_existed_user(self):
        try:
            new_user = User.objects.create_user(
                username="simple_user", password="simple_user", email='simple_user@local.com'
            )
            self.assertTrue(False, msg="Existed user is created again!")
        except IntegrityError:
            self.assertTrue(True)

    def test_get_user(self):
        self.assertTrue(User.objects.filter(username="admin").exists())


class UserTests(TestCase):
    def setUp(self) -> None:
        user_1 = User.objects.create_user(
            username="admin",
            password="admin",
            first_name="admin",
            last_name="adminian",
            email="admin@admin.com",
        )
        user_1.is_superuser = True
        user_1.save()
        user_2 = User.objects.create_user(
            username="test-2",
            password="test-2",
            first_name="test-2",
            last_name="test-2",
            email="test-2@test.com",
        )
        user_3 = User.objects.create_user(
            username="test-3",
            password="test-3",
            first_name="test-3",
            last_name="test-3",
            email="test-3@test.com",
        )

        self.client = Client()

    def _login(self, username: str, password: str, realm: str):
        response = self.client.post(
            path=reverse_lazy('public_api:user_login'),
            data={"username": username, "password": password},
            content_type="application/json",
        )
        return json.loads(response.content)
