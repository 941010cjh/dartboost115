from django.urls import path, include
from user.views import LoginView, SignUpView, VerificationView, ResendVerifyEmailView

from django.contrib import admin
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('user/<pk>/verify/<token>/', VerificationView.as_view()),
    path('signup/resend_verify_email/', ResendVerifyEmailView.as_view()),
]