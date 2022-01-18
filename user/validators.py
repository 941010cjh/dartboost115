from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from dart_fss import set_api_key
from dart_fss.errors import APIKeyError


class LoginFormValidator:
    user_model = get_user_model()
    code = 'invalid'
    def __call__(self, email, password):            
        try:
            user = self.user_model.objects.get(email=email)
            if not user.is_active:
                raise ValidationError({'username':'로그인에 실패했습니다. 이메일 인증을 완료해주세요'}, code=self.code)
            if not check_password(password, user.password):
                raise ValidationError({'password':'올바르지 않은 비밀번호입니다.'}, code=self.code)
        except self.user_model.DoesNotExist:
            raise ValidationError({'username':'가입되지 않은 이메일입니다.'}, code=self.code)

        return

class RegisteredEmailValidator:
    user_model = get_user_model()
    code = 'invalid'
    
    def __call__(self, email):
        try:
            user = self.user_model.objects.get(email=email)
        except self.user_model.DoesNotExist:
            raise ValidationError({'email':'가입되지 않은 이메일입니다.'}, code=self.code)
        else:
            if user.is_active:
                raise ValidationError({'email':'이미 인증되어 있습니다.'}, code=self.code)
        return

class APIKeyValidator:
    code = 'invalid'
    def __call__(self,api_key):
        try:
            set_api_key(api_key)
        except APIKeyError:
            raise ValidationError({'api_key':'등록되지 않은 인증키입니다.'}, code=self.code)
        return
