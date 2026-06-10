from rest_framework import serializers

from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            "id",
            "title",
            "category",
            "description",
            "location",
            "status",
            "reporter",
            "is_owner",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "reporter",
            "is_owner",
            "created_at",
            "updated_at",
        ]

    def get_reporter(self, obj):
        """
        Pada tab Feed Kota, identitas pelapor disensor langsung
        dari backend agar username asli tidak bocor melalui Network tab.
        """
        request = self.context.get("request")

        if request is not None:
            tab = request.query_params.get("tab")

            if tab == "feed":
                return "Warga Anonim"

        if obj.reporter is None:
            return "Warga Anonim"

        return obj.reporter.username

    def get_is_owner(self, obj):
        """
        Mengirim informasi apakah laporan merupakan milik
        pengguna yang sedang login.
        """
        request = self.context.get("request")

        if request is None:
            return False

        user = request.user

        if not user or not user.is_authenticated:
            return False

        return obj.reporter == user

    def validate_status(self, value):
        """
        Citizen hanya boleh membuat draft atau mengajukan laporan.
        Perubahan status lanjutan diproses oleh petugas/admin.
        """
        request = self.context.get("request")

        if request is None:
            return value

        if request.user and request.user.is_staff:
            return value

        allowed_statuses = ["DRAFT", "REPORTED"]

        if value not in allowed_statuses:
            raise serializers.ValidationError(
                "Citizen hanya dapat memilih status DRAFT atau REPORTED."
            )

        return value