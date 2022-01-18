from django.urls import path
from root.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]