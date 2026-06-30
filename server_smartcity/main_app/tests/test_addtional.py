from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from main_app.models import Report
from main_app.serializers import ReportSerializer


User = get_user_model()


class SerializerAndModelCoverageTests(APITestCase):
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

    def test_report_model_str(self):
        report = Report.objects.create(
            title="Laporan Str Uji",
            category="Lainnya",
            description="Deskripsi",
            location="Lokasi",
            status="REPORTED",
            reporter=self.warga,
        )

        self.assertEqual(str(report), "Laporan Str Uji")

    def test_report_serializer_no_request_context(self):
        report = Report.objects.create(
            title="Laporan Serializer Uji",
            category="Lainnya",
            description="Deskripsi",
            location="Lokasi",
            status="REPORTED",
            reporter=self.warga,
        )

        serializer = ReportSerializer(report, context={})

        self.assertIn("reporter", serializer.data)
        self.assertIn("is_owner", serializer.data)
        self.assertFalse(serializer.data["is_owner"])


class MainAppMonolithicViewsCoverageTests(TestCase):
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
            username="bahlil",
            password="orangbaik",
        )
        self.citizen.is_active = True

        if hasattr(self.citizen, "is_admin"):
            self.citizen.is_admin = False

        if hasattr(self.citizen, "is_member"):
            self.citizen.is_member = True

        self.citizen.save()

        self.report = Report.objects.create(
            title="Laporan Monolitik Uji",
            category="Infrastruktur",
            description="Ada kerusakan infrastruktur.",
            location="Bandung",
            status="REPORTED",
            reporter=self.citizen,
        )

    def test_home_view(self):
        response = self.client.get(reverse("landing"))
        self.assertEqual(response.status_code, 200)

    def test_report_list_view_unauthenticated(self):
        response = self.client.get(reverse("report_list"))

        # Di project ini halaman daftar laporan masih bisa dibuka tanpa login
        self.assertEqual(response.status_code, 200)

    def test_report_list_view_citizen(self):
        self.client.login(username="bahlil", password="orangbaik")

        response = self.client.get(reverse("report_list"))

        # Di project ini citizen juga masih bisa membuka halaman report list
        self.assertEqual(response.status_code, 200)

    def test_report_list_view_admin(self):
        self.client.login(username="arinaladmin", password="12345678")

        response = self.client.get(reverse("report_list"))

        self.assertEqual(response.status_code, 200)

    def test_report_detail_view_admin(self):
        self.client.login(username="arinaladmin", password="12345678")

        response = self.client.get(
            reverse("report_detail", kwargs={"pk": self.report.id})
        )

        self.assertEqual(response.status_code, 200)

    def test_report_search_admin(self):
        self.client.login(username="arinaladmin", password="12345678")

        response = self.client.get(reverse("report_search") + "?q=Monolitik")

        self.assertEqual(response.status_code, 200)

    def test_report_detail_json_valid(self):
        response = self.client.get(
            reverse("report_detail_json", kwargs={"pk": self.report.id})
        )

        self.assertEqual(response.status_code, 200)