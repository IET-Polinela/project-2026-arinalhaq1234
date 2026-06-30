from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from main_app.models import Report

User = get_user_model()


class CRUDAndValidationTests(APITestCase):
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

        self.client.force_authenticate(user=self.warga)

    def test_FT_01_buat_laporan_dengan_data_lengkap(self):
        url = reverse("report-list")

        payload = {
            "title": "Laporan Baru dari Test",
            "category": "Infrastruktur",
            "description": "Deskripsi laporan lengkap dari automated test.",
            "location": "Polinela",
            "status": "DRAFT",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(
            Report.objects.filter(title="Laporan Baru dari Test").exists()
        )

        laporan = Report.objects.get(title="Laporan Baru dari Test")
        self.assertEqual(laporan.reporter, self.warga)

    def test_FT_02_ditolak_jika_judul_kosong(self):
        url = reverse("report-list")

        payload = {
            "category": "Infrastruktur",
            "description": "Laporan tanpa judul.",
            "location": "Polinela",
            "status": "DRAFT",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_FT_03_ditolak_jika_deskripsi_kosong(self):
        url = reverse("report-list")

        payload = {
            "title": "Laporan Tanpa Deskripsi",
            "category": "Infrastruktur",
            "location": "Polinela",
            "status": "DRAFT",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("description", response.data)

    def test_FT_04_xss_script_disimpan_sebagai_string_literal(self):
        url = reverse("report-list")

        kode_xss = '<script>alert("xss")</script>'

        payload = {
            "title": "Laporan XSS Test",
            "category": "Keamanan",
            "description": kode_xss,
            "location": "Lab Keamanan Siber",
            "status": "DRAFT",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        laporan = Report.objects.get(title="Laporan XSS Test")

        self.assertIn("script", laporan.description.lower())