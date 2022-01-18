from __future__ import absolute_import
from dartboost.celery import app

from django.core.mail import send_mail


@app.task
def email_user_to(subject, message, email, from_email=None, **kwargs): # 이메일 발송 메소드
    send_mail(subject, message, from_email, [email], **kwargs)