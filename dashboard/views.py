from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

DASHBOARD_TEMPLATE = '/main.html'
class DashboardView(LoginRequiredMixin,TemplateView):
    template_name= __package__ + DASHBOARD_TEMPLATE