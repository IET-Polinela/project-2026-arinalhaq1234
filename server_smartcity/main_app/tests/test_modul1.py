from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.warga = User.objects.create_user(
            username="bahlil",
            password="orangbaik",
        )
        self.warga.is_active = True
        if hasattr(self.warga, "is_admin"):
            self.warga.is_admin = False
        if hasattr(self.warga, "is_member"):
            self.warga.is_member = True
        self.warga.save()

        self.admin = User.objects.create_user(
            username="arinaladmin",
            password="12345678",
        )
        self.admin.is_active = True
        self.admin.is_staff = True
        self.admin.is_superuser = True
        if hasattr(self.admin, "is_admin"):
            self.admin.is_admin = True
        if hasattr(self.admin, "is_member"):
            self.admin.is_member = False
        self.admin.save()

    def test_AUTH_01_login_warga_dengan_kredensial_valid(self):
        url = reverse("token_obtain_pair")

        payload = {
            "username": "bahlil",
            "password": "orangbaik",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_AUTH_02_login_warga_dengan_password_salah(self):
        url = reverse("token_obtain_pair")

        payload = {
            "username": "bahlil",
            "password": "password_salah",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", response.data)

    def test_AUTH_03_warga_tidak_bisa_akses_halaman_admin(self):
        self.client.force_login(self.warga)

        response = self.client.get("/dashboard/")

        self.assertIn(
            response.status_code,
            [status.HTTP_302_FOUND, status.HTTP_403_FORBIDDEN],
        )