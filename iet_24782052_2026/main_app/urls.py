from django.urls import path
from .views import (
    ReportListView,
    ReportDetailView,
    ReportCreateView,
    ReportUpdateView,
    ReportDeleteView,
    ReportUpdateStatusView,
    ReportSearchJsonView,
    ReportDetailJsonView,
)

urlpatterns = [
    path('', ReportListView.as_view(), {'is_landing': True}, name='landing'),
    path('reports/', ReportListView.as_view(), {'is_landing': False}, name='report_list'),
    path('reports/search/', ReportSearchJsonView.as_view(), name='report_search'),

    path('detail/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),
    path('detail-json/<int:pk>/', ReportDetailJsonView.as_view(), name='report_detail_json'),
    path('add/', ReportCreateView.as_view(), name='report_add'),
    path('edit/<int:pk>/', ReportUpdateView.as_view(), name='report_edit'),
    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='report_delete'),
    path('update-status/<int:pk>/', ReportUpdateStatusView.as_view(), name='update_status'),
]