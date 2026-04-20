from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Report
from .forms import ReportForm


# READ (List)
class ReportListView(ListView):
    model = Report
    template_name = 'home.html'
    context_object_name = 'reports'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_landing'] = self.kwargs.get('is_landing', False)
        return context


# DETAIL
class ReportDetailView(DetailView):
    model = Report
    template_name = 'detail_report.html'
    context_object_name = 'report'


# CREATE
class ReportCreateView(CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'add_report.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Laporan berhasil ditambahkan.')
        return response


# UPDATE
class ReportUpdateView(UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'edit_report.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Laporan berhasil diperbarui.')
        return response


# DELETE
class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, 'Laporan berhasil dihapus.')
        return super().form_valid(form)


# WORKFLOW STATUS
class ReportUpdateStatusView(View):
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