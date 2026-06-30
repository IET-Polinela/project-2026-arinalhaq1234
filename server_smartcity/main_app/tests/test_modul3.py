from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from main_app.models import Report

User = get_user_model()


class WorkflowStateTests(APITestCase):
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

        self.laporan_draft = Report.objects.create(
            title="Lampu Kampus Mati",
            category="Fasilitas Umum",
            description="Lampu di depan gedung rektorat tidak menyala.",
            location="Gedung Rektorat",
            status="DRAFT",
            reporter=self.warga,
        )

        self.laporan_reported = Report.objects.create(
            title="Saluran Air Tersumbat",
            category="Infrastruktur",
            description="Saluran air di samping kantin tersumbat.",
            location="Kantin Polinela",
            status="REPORTED",
            reporter=self.warga,
        )

        self.laporan_resolved = Report.objects.create(
            title="AC Rusak di Lab",
            category="Fasilitas Umum",
            description="AC di Lab CPS 1 sudah diperbaiki.",
            location="Lab CPS 1",
            status="RESOLVED",
            reporter=self.warga,
        )

    def test_WF_01_warga_mengajukan_draf_menjadi_reported(self):
        self.client.force_authenticate(user=self.warga)

        url = f"/api/report/{self.laporan_draft.pk}/"

        payload = {
            "title": self.laporan_draft.title,
            "category": self.laporan_draft.category,
            "description": self.laporan_draft.description,
            "location": self.laporan_draft.location,
            "status": "REPORTED",
        }

        response = self.client.put(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.laporan_draft.refresh_from_db()
        self.assertEqual(self.laporan_draft.status, "REPORTED")

    def test_WF_02_tidak_bisa_edit_laporan_yang_sudah_reported(self):
        self.client.force_authenticate(user=self.warga)

        judul_awal = self.laporan_reported.title

        url = f"/api/report/{self.laporan_reported.pk}/"

        payload = {
            "title": "Judul Diubah Setelah Reported",
            "category": self.laporan_reported.category,
            "description": self.laporan_reported.description,
            "location": self.laporan_reported.location,
            "status": self.laporan_reported.status,
        }

        response = self.client.put(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.laporan_reported.refresh_from_db()
        self.assertEqual(self.laporan_reported.title, judul_awal)

    def test_WF_05_laporan_resolved_tidak_bisa_diubah(self):
        self.client.force_authenticate(user=self.warga)

        judul_awal = self.laporan_resolved.title

        url = f"/api/report/{self.laporan_resolved.pk}/"

        payload = {
            "title": "Judul Diubah Setelah Resolved",
            "category": self.laporan_resolved.category,
            "description": self.laporan_resolved.description,
            "location": self.laporan_resolved.location,
            "status": self.laporan_resolved.status,
        }

        response = self.client.put(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.laporan_resolved.refresh_from_db()
        self.assertEqual(self.laporan_resolved.title, judul_awal)


class AdminWorkflowTests(TestCase):
    def setUp(self):
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

        self.citizen = User.objects.create_user(
            username="bahlil_admin_test",
            password="orangbaik",
        )
        self.citizen.is_active = True
        if hasattr(self.citizen, "is_admin"):
            self.citizen.is_admin = False
        if hasattr(self.citizen, "is_member"):
            self.citizen.is_member = True
        self.citizen.save()

        self.laporan_reported = Report.objects.create(
            title="Jalan Rusak di Blok C",
            category="Infrastruktur",
            description="Jalan berlubang parah di area parkir Blok C.",
            location="Blok C Polinela",
            status="REPORTED",
            reporter=self.citizen,
        )

    def test_WF_03_admin_mengubah_status_reported_ke_verified(self):
        self.client.login(username="arinaladmin", password="12345678")

        url = reverse("update_status", kwargs={"pk": self.laporan_reported.pk})

        response = self.client.post(
            url,
            {
                "new_status": "VERIFIED",
                "status": "VERIFIED",
            },
        )

        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_302_FOUND])

        self.laporan_reported.refresh_from_db()
        self.assertEqual(self.laporan_reported.status, "VERIFIED")

    def test_WF_04_tidak_ada_transisi_langsung_ke_resolved_dari_reported(self):
        self.client.login(username="arinaladmin", password="12345678")

        url = reverse("update_status", kwargs={"pk": self.laporan_reported.pk})

        response = self.client.post(
            url,
            {
                "new_status": "RESOLVED",
                "status": "RESOLVED",
            },
        )

        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_302_FOUND])

        self.laporan_reported.refresh_from_db()
        self.assertNotEqual(
            self.laporan_reported.status,
            "RESOLVED",
            "Laporan REPORTED tidak boleh langsung lompat ke RESOLVED",
        )