from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.views.generic.base import View
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile, EmailVerifyRecord
import json
from django.db.models import Q  # 并集
from .forms import LoginForm, RegisterForm, ResetPwdForm, UserInfoForm, UploadImageForm, ForgetPwdForm
from apps.utils.email_send import send_register_email


# Create your views here.


class CustomBackend(ModelBackend):
    """
    重写ModelBackend下的authenticate方法实现邮箱和用户名均可以登录
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    # 直接调用get方法免去判断
    def get(self, request):
        redirect_url = request.GET.get('next', '')
        return render(request, "users/login.html", {
            "redirect_url": redirect_url
        })

    def post(self, request):
        login_form = LoginForm(request.POST)

        # is_valid判断我们字段是否有错执行我们原有逻辑，验证失败跳回login页面
        if login_form.is_valid():
            # 取不到时为空，username，password为前端页面name值
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")

            # 成功返回user对象,失败返回null
            user = authenticate(username=user_name, password=pass_word)

            # 如果不是null说明验证成功
            if user is not None:
                # 只有当用户激活时才给登录
                if user.is_active:
                    login(request, user)
                    redirect_url = request.POST.get('next', '')
                    if redirect_url:
                        return HttpResponseRedirect(redirect_url)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(
                        request, "users/login.html", {
                            "msg": "用户名未激活! 请前往邮箱进行激活"})
            # 当用户真的密码出错时
            else:
                return render(request, "users/login.html", {"msg": "用户名或密码错误!"})
        # 验证不成功跳回登录页面
        # 没有成功说明里面的值是None，并再次跳转回主页面
        else:
            return render(
                request, "users/login.html", {
                    "login_form": login_form})


class ActiveUserView(View):
    """
    激活注册用户
    """

    def get(self, request, active_code):
        #   查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)

        if all_record:
            for record in all_record:
                # 获取对应邮箱
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True

                user.save()
        else:
            return render(request, 'users/active_fail.html')
        return render(request, 'users/login.html')


class RegisterView(View):
    """
    注册视图
    """

    def get(self, request):
        register_form = RegisterForm()
        return render(request, "users/register.html", {'register_form': register_form})

    def post(self, request):
        # 实例化生成注册表单
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', None)
            # 如果用户已经存在
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'users/register.html',
                              {'register_form': register_form, 'msg': '用户已经存在'})
            pass_word = request.POST.get('password', None)
            # 实例化UserProfile
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            # 默认注册后用户是未激活的
            user_profile.is_active = False
            # hash算法加密密码
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_email(user_name, 'register')
            messages.success(request, "已经发送了激活邮件，请查收")
            return render(request, 'users/register.html')
        else:
            return render(request, 'users/register.html', {'register_form': register_form})


class ResetPwdView(View):
    """
    重设密码视图
    """

    def post(self, request):
        reset_form = ResetPwdForm(request.POST)
        if reset_form.is_valid():
            username = request.user.username
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 != password2:
                return render(request, 'users/reset.html', {'msg': '两次输入的密码不一致'})
            user = UserProfile.objects.get(username=username)
            user.password = make_password(password2)
            user.save()
            return render(request, 'users/login.html', {'msg': '密码修改成功,请使用新密码登录'})
        else:
            # 密码位数不够
            return render(request, 'users/reset.html', {'reset_form': reset_form})


class UserInfoView(LoginRequiredMixin, View):
    """
    用户中心视图
    """
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        return render(request, 'users/user.html')

    def post(self, request):
        # 修改，增加instance属性
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user = UserProfile.objects.get(pk=request.user.id)
            user.nick_name = user_info_form.cleaned_data['nick_name']
            user.gender = user_info_form.cleaned_data['gender']
            user.sign = user_info_form.cleaned_data['sign']
            user.address = user_info_form.cleaned_data['address']
            user.mobile = user_info_form.cleaned_data['mobile']
            user.save()
            return HttpResponseRedirect(reverse('user_info'))
        else:
            # 通过json的dumps方法把字典转换成字符串
            return HttpResponse(
                json.dumps(user_info_form.errors),
                content_type='application/json'
            )


class UploadImageView(LoginRequiredMixin, View):
    """
    用户头像修改
    """
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            # return HttpResponse('{"status": "success"}', content_type='application/json')
            return HttpResponseRedirect(reverse('user_info'))
        else:
            return HttpResponse('{"status": "fail"}', content_type='application/json')


class ForgetPwdView(View):
    """
    找回密码视图
    """
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'users/forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', None)
            send_register_email(email, 'forget')
            return render(request, 'index.html')
        else:
            return render(request, 'users/forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "users/reset.html", {"email": email})
        else:
            return render(request, "users/active_fail.html")
        return render(request, "users/login.html")


class LogOutView(View):
    """
    退出登录
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))







