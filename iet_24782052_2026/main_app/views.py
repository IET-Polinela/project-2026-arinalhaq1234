from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from .models import Report

# 🔵 READ (List)
class ReportListView(ListView):
    model = Report
    template_name = 'home.html'
    context_object_name = 'reports'


# 👁️ DETAIL
class ReportDetailView(DetailView):
    model = Report
    template_name = 'detail_report.html'
    context_object_name = 'report'


# 🟢 CREATE
class ReportCreateView(CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'add_report.html'
    success_url = reverse_lazy('report_list')


# 🟡 UPDATE
class ReportUpdateView(UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'edit_report.html'
    success_url = reverse_lazy('report_list')


# 🔴 DELETE
class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'confirm_delete.html'  # opsional (bisa langsung delete juga)
    success_url = reverse_lazy('report_list')


# 🔥 WORKFLOW STATUS (WAJIB LAB 4)
class ReportUpdateStatusView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')
        report.status = new_status
        report.save()
        return redirect('report_list')