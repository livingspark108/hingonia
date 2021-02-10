from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView
from application.custom_classes import AjayDatatableView, StudentRequiredMixin

User = get_user_model()


class FrontendHomeView(View):
    def get(self, request):

        if request.user.is_authenticated:
            if request.user.type == "student":


                context = {}
            else:
                context = {}
            return render(request, 'frontend/home.html', context)
        else:
            return HttpResponseRedirect(reverse('auth-login'))