from rest_framework import permissions


class IsOwnerAndDraftOrReadOnly(permissions.BasePermission):
    """
    Membatasi perubahan laporan:
    - Semua user login boleh membaca data yang tersedia dari queryset.
    - Hanya pemilik laporan yang boleh mengubah atau menghapus laporan.
    - Hanya laporan berstatus DRAFT yang boleh diubah atau dihapus.
    """

    message = (
        "Laporan hanya dapat diubah atau dihapus oleh pemiliknya "
        "selama masih berstatus DRAFT."
    )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            obj.reporter == request.user
            and obj.status == "DRAFT"
        )