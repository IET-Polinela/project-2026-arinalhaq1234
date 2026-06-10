from django.http import JsonResponse
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Report
from .forms import ReportForm


class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Silakan login terlebih dahulu.')
            return redirect('login')

        if not request.user.is_admin:
            messages.error(request, 'Akses Ditolak. Hanya admin yang dapat mengakses fitur ini.')
            return redirect('report_list')

        return super().dispatch(request, *args, **kwargs)


class OwnerDraftRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Silakan login terlebih dahulu.')
            return redirect('login')

        report = self.get_object()

        if report.reporter != request.user or report.status != 'DRAFT':
            messages.error(request, 'Akses ditolak. Laporan hanya dapat diubah atau dihapus oleh pemilik saat status masih DRAFT.')
            return redirect('report_list')

        return super().dispatch(request, *args, **kwargs)


# READ (List)
class ReportListView(ListView):
    model = Report
    template_name = 'home.html'
    context_object_name = 'reports'
    ordering = ['-id']

    def get_queryset(self):
        user = self.request.user

        queryset = Report.objects.filter(
            Q(status__in=['REPORTED', 'VERIFIED', 'IN_PROGRESS', 'RESOLVED'])
        )

        if user.is_authenticated:
            queryset = queryset | Report.objects.filter(status='DRAFT', reporter=user)

        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_landing'] = self.kwargs.get('is_landing', False)
        return context


# DETAIL PAGE
class ReportDetailView(DetailView):
    model = Report
    template_name = 'detail_report.html'
    context_object_name = 'report'


# DETAIL JSON FOR MODAL
class ReportDetailJsonView(View):
    def get(self, request, pk, *args, **kwargs):
        report = get_object_or_404(Report, pk=pk)

        data = {
            'id': report.id,
            'title': report.title,
            'category': report.category,
            'description': report.description,
            'location': report.location,
            'status': report.status,
        }

        return JsonResponse(data)


# LIVE SEARCH JSON
class ReportSearchJsonView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip()
        user = request.user

        reports = Report.objects.filter(
            Q(status__in=['REPORTED', 'VERIFIED', 'IN_PROGRESS', 'RESOLVED'])
        )

        if user.is_authenticated:
            reports = reports | Report.objects.filter(status='DRAFT', reporter=user)

        reports = reports.order_by('-id')

        if query:
            reports = reports.filter(
                Q(title__icontains=query) |
                Q(category__icontains=query) |
                Q(location__icontains=query) |
                Q(status__icontains=query)
            )

        data = [
            {
                'id': report.id,
                'title': report.title,
                'category': report.category,
                'location': report.location,
                'status': report.status,
                'can_manage': (
                    request.user.is_authenticated
                    and report.reporter == request.user
                    and report.status == 'DRAFT'
                ),
            }
            for report in reports[:50]
        ]

        return JsonResponse({'results': data})


# CREATE
class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'add_report.html'
    success_url = reverse_lazy('report_list')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        form.instance.status = 'DRAFT'

        response = super().form_valid(form)
        messages.success(self.request, 'Laporan berhasil ditambahkan.')
        return response


# UPDATE
class ReportUpdateView(OwnerDraftRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'edit_report.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        form.instance.status = 'DRAFT'

        response = super().form_valid(form)
        messages.success(self.request, 'Laporan berhasil diperbarui.')
        return response


# DELETE
class ReportDeleteView(OwnerDraftRequiredMixin, DeleteView):
    model = Report
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, 'Laporan berhasil dihapus.')
        return super().form_valid(form)


# WORKFLOW STATUS
class ReportUpdateStatusView(AdminRequiredMixin, View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')

        allowed_transitions = {
            'REPORTED': 'VERIFIED',
            'VERIFIED': 'IN_PROGRESS',
            'IN_PROGRESS': 'RESOLVED',
        }

        if report.status in allowed_transitions and allowed_transitions[report.status] == new_status:
            report.status = new_status
            report.save()
            messages.success(request, f'Status laporan berhasil diubah ke {new_status}.')
        else:
            messages.error(request, 'Perubahan status tidak valid.')

        return redirect('report_list')