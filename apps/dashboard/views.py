from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView
from application.custom_classes import AjayDatatableView
from .forms import *
from .models import *
User = get_user_model()


                                   # Teacher Dashboard

class CreateTeacherDashboardView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TeacherDashboard
    form_class = TeacherDashboardForm
    template_name = 'teacher_dashboard/form.html'
    success_message = 'Teacher Dashboard been updated successfully'
    success_url = reverse_lazy('admin-teacher-dashboard')

    def get_object(self, queryset=None):
        teacherdashboard, _ = self.model.objects.get_or_create(pk=1)
        return teacherdashboard


                                    # Supervisor Dashboard

class CreateSupervisorDashboardView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = SupervisorDashboard
    form_class = SupervisorDashboardForm
    template_name = 'supervisor_dashboard/form.html'
    success_message = 'Supervisor Dashboard been updated successfully'
    success_url = reverse_lazy('admin_supervisor_dashboard')

    def get_object(self, queryset=None):
        supervisordashboard, _ = self.model.objects.get_or_create(pk=1)
        return supervisordashboard


                                      # Guide Dashboard

class CreateGuideDashboardView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = GuideDashboard
    form_class = GuideDashboardForm
    template_name = 'guide_dashboard/form.html'
    success_message = 'Guide Dashboard been updated successfully'
    success_url = reverse_lazy('admin_guide_dashboard')

    def get_object(self, queryset=None):
        guidedashboard, _ = self.model.objects.get_or_create(pk=1)
        return guidedashboard
