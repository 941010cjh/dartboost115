from django.shortcuts import render
from user.views import LoginView


HOMEVIEW_TEMPLATE = '/home.html'
class HomeView(LoginView):
    template_name= __package__ + HOMEVIEW_TEMPLATE