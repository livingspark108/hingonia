from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView
from settings.models import *
from django.views.generic import View


# Create your views here.

class SettingsView(View):
    template_name = "settings.html"

    def get(self, request):
        return render(request, self.template_name)
