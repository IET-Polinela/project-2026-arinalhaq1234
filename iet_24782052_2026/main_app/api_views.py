from django.db.models import Q
from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Report
from .permissions import IsOwnerAndDraftOrReadOnly
from .serializers import ReportSerializer


class ReportPagination(PageNumberPagination):
    """
    Pagination utama maksimal 10 item per halaman.
    Parameter page_size tetap diaktifkan agar rekap sidebar
    dapat mengambil data pengguna dengan limit besar.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    pagination_class = ReportPagination

    def get_queryset(self):
        """
        Memisahkan visibilitas data berdasarkan tab:
        - my_reports: hanya laporan milik akun login.
        - feed: hanya laporan warga lain yang bukan DRAFT.
        - default: laporan milik akun login dan laporan publik.
        """

        user = self.request.user
        tab = self.request.query_params.get("tab")

        queryset = Report.objects.all().order_by("-updated_at")

        if tab == "my_reports":
            return queryset.filter(reporter=user)

        if tab == "feed":
            return queryset.exclude(
                reporter=user
            ).exclude(
                status="DRAFT"
            )

        return queryset.filter(
            Q(reporter=user) |
            ~Q(status="DRAFT")
        )

    def get_permissions(self):
        """
        Seluruh endpoint membutuhkan login.
        Update, PATCH, dan DELETE memiliki validasi tambahan:
        hanya pemilik draft yang diizinkan.
        """

        if self.action in [
            "update",
            "partial_update",
            "destroy",
        ]:
            permission_classes = [
                permissions.IsAuthenticated,
                IsOwnerAndDraftOrReadOnly,
            ]
        else:
            permission_classes = [
                permissions.IsAuthenticated,
            ]

        return [
            permission()
            for permission in permission_classes
        ]

    def perform_create(self, serializer):
        """
        Reporter tidak dikirim oleh frontend.
        Reporter otomatis berasal dari JWT user login.
        """

        serializer.save(reporter=self.request.user)