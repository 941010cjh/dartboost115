from django.shortcuts import render

from django.http import HttpResponseRedirect

from django.contrib import messages

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView

from django.views.generic import CreateView
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

from user.forms import LoginForm, SignUpForm, VerificationEmailForm
from user.models import User
from user.mixins import VerifyEmailMixin

from dartboost import settings


LOGIN_VIEW_TEMPLATE = '/user_form.html'
RESEND_URL= '/signup/resend_verify_email/'
VERIFY_URL='/user/verify/'
LOGIN_URL = settings.LOGIN_URL

class LoginView(LoginView):
    template_name= __package__ + LOGIN_VIEW_TEMPLATE
    authentication_form = LoginForm
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text']='login'
        return context

    def form_invalid(self, form):
        messages.error(self.request, '이메일/비밀번호 입력이 올바르지 않습니다.', extra_tags='danger')
        return super().form_invalid(form)

class SignUpView(VerifyEmailMixin, CreateView):
    model = get_user_model()
    form_class = SignUpForm
    success_url = RESEND_URL
    verify_url = VERIFY_URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text']='signup'
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if form.instance:
            self.send_verification_email(form.instance)
        return response

    def form_invalid(self, form):
        messages.error(self.request, '회원가입에 실패하였습니다.', extra_tags='danger')
        return super().form_invalid(form)

class VerificationView(TemplateView):

    model = get_user_model()
    redirect_url = LOGIN_URL
    token_generator = default_token_generator

    def get(self, request, *args, **kwargs):
        if self.is_valid_token(**kwargs):
            messages.info(request, '인증이 완료되었습니다.')
        else:
            messages.error(request, '인증이 실패되었습니다.', extra_tags='danger')
        return HttpResponseRedirect(self.redirect_url)   # 인증 성공여부와 상관없이 무조건 로그인 페이지로 이동

    def is_valid_token(self, **kwargs):
        pk = kwargs.get('pk')
        token = kwargs.get('token')
        user = self.model.objects.get(pk=pk)
        is_valid = self.token_generator.check_token(user, token)
        if is_valid:
            user.is_active = True
            user.save()     # 데이터가 변경되면 반드시 save() 메소드 호출
        return is_valid

class ResendVerifyEmailView(VerifyEmailMixin, FormView):
    model = get_user_model()
    form_class = VerificationEmailForm
    success_url = RESEND_URL
    template_name = __package__ + LOGIN_VIEW_TEMPLATE
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text']='재발송'
        return context

    def form_valid(self, form):
        try:
            email = form.cleaned_data['email']
            user = self.model.objects.get(email=email)
        except self.model.DoesNotExist:
            messages.error(self.request, '알 수 없는 사용자 입니다.', extra_tags='danger')
        else:
            self.send_verification_email(user)
        return super().form_valid(form)

    def form_invalid(self,form):
        messages.error(self.request, '알 수 없는 사용자 입니다.', extra_tags='danger')
        return super().form_valid(form)