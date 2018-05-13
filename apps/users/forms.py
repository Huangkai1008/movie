from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile


class LoginForm(forms.Form):
    """
    用户登录表单
    """
    username = forms.CharField(required=True, error_messages={'required': u'用户名或者邮箱不能为空'})
    password = forms.CharField(required=True, min_length=5, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    """
    用户注册表单
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    captcha = CaptchaField(required=True, error_messages={'invalid': u'输入的验证码错误'})


class ResetPwdForm(forms.Form):
    """
    用户重置密码表单
    """
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)


class UserInfoForm(forms.ModelForm):
    """
    用户个人中心
    """
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birthday', 'address', 'mobile']

