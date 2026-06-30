from django.http import JsonResponse
from django.views.generic import TemplateView, View
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from main_app.models import Report


class AdminOnlyMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = "login"

    def test_func(self):
        user = self.request.user
        return (
            user.is_staff
            or user.is_superuser
            or getattr(user, "is_admin", False)
        )


class DashboardView(AdminOnlyMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'


class DashboardStatsJsonView(AdminOnlyMixin, View):
    def get(self, request, *args, **kwargs):
        total_reports = Report.objects.count()
        total_reported = Report.objects.filter(status='REPORTED').count()
        total_resolved = Report.objects.filter(status='RESOLVED').count()

        status_counts_qs = Report.objects.values('status').annotate(total=Count('id')).order_by('status')
        category_counts_qs = Report.objects.values('category').annotate(total=Count('id')).order_by('category')

        latest_reported_qs = Report.objects.filter(status='REPORTED').order_by('-id')[:5]
        latest_resolved_qs = Report.objects.filter(status='RESOLVED').order_by('-id')[:5]

        status_counts = list(status_counts_qs)
        category_counts = list(category_counts_qs)

        latest_reported = [
            {
                'title': report.title,
                'category': report.category,
                'location': report.location,
                'status': report.status,
            }
            for report in latest_reported_qs
        ]

        latest_resolved = [
            {
                'title': report.title,
                'category': report.category,
                'location': report.location,
                'status': report.status,
            }
            for report in latest_resolved_qs
        ]

        return JsonResponse({
            'summary': {
                'total_reports': total_reports,
                'total_reported': total_reported,
                'total_resolved': total_resolved,
            },
            'status_counts': status_counts,
            'category_counts': category_counts,
            'latest_reported': latest_reported,
            'latest_resolved': latest_resolved,
        })