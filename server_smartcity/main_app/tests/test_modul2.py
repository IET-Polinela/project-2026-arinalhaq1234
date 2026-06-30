from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from main_app.models import Report

User = get_user_model()


def get_results(response):
    if isinstance(response.data, dict) and "results" in response.data:
        return response.data["results"]
    return response.data


class PrivacyAndDataHidingTests(APITestCase):
    def setUp(self):
        self.warga_a = User.objects.create_user(
            username="bahlil",
            password="orangbaik",
        )
        self.warga_a.is_active = True
        if hasattr(self.warga_a, "is_admin"):
            self.warga_a.is_admin = False
        if hasattr(self.warga_a, "is_member"):
            self.warga_a.is_member = True
        self.warga_a.save()

        self.warga_b = User.objects.create_user(
            username="warga_b",
            password="TestPass123!",
        )
        self.warga_b.is_active = True
        if hasattr(self.warga_b, "is_admin"):
            self.warga_b.is_admin = False
        if hasattr(self.warga_b, "is_member"):
            self.warga_b.is_member = True
        self.warga_b.save()

        self.draft_milik_b = Report.objects.create(
            title="Draf Rahasia Warga B",
            category="Infrastruktur",
            description="Ini adalah draf yang belum diajukan.",
            location="Lokasi Rahasia",
            status="DRAFT",
            reporter=self.warga_b,
        )

        self.laporan_publik_a = Report.objects.create(
            title="Jalan Berlubang di Depan Kampus",
            category="Infrastruktur",
            description="Ada lubang besar yang membahayakan pengendara.",
            location="Jl. Soekarno Hatta",
            status="REPORTED",
            reporter=self.warga_a,
        )

        self.laporan_publik_b = Report.objects.create(
            title="Sampah Menumpuk di Trotoar",
            category="Kebersihan",
            description="Sampah tidak diangkut selama seminggu.",
            location="Jl. Gatot Subroto",
            status="REPORTED",
            reporter=self.warga_b,
        )

    def test_PRIV_01_feed_kota_menyembunyikan_identitas_reporter(self):
        self.client.force_authenticate(user=self.warga_a)

        response = self.client.get("/api/report/?tab=feed")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = get_results(response)
        self.assertTrue(len(results) > 0)

        for laporan in results:
            self.assertEqual(laporan["reporter"], "Warga Anonim")

    def test_PRIV_02_laporan_saya_menampilkan_nama_asli(self):
        self.client.force_authenticate(user=self.warga_a)

        response = self.client.get("/api/report/?tab=my_reports")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = get_results(response)
        self.assertTrue(len(results) > 0)

        for laporan in results:
            self.assertEqual(laporan["reporter"], "bahlil")

    def test_PRIV_03_tidak_bisa_baca_draf_orang_lain(self):
        self.client.force_authenticate(user=self.warga_a)

        url = f"/api/report/{self.draft_milik_b.pk}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_PRIV_04_tidak_bisa_modifikasi_draf_orang_lain(self):
        self.client.force_authenticate(user=self.warga_a)

        judul_awal = self.draft_milik_b.title
        deskripsi_awal = self.draft_milik_b.description

        url = f"/api/report/{self.draft_milik_b.pk}/"

        payload = {
            "title": "Judul Diubah Paksa",
            "category": self.draft_milik_b.category,
            "description": "Deskripsi diubah oleh orang lain",
            "location": self.draft_milik_b.location,
            "status": self.draft_milik_b.status,
        }

        response = self.client.put(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.draft_milik_b.refresh_from_db()
        self.assertEqual(self.draft_milik_b.title, judul_awal)
        self.assertEqual(self.draft_milik_b.description, deskripsi_awal)