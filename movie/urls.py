"""movie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from users.views import LoginView, RegisterView, ResetPwdView
from django.contrib.auth import views as auth_views
import xadmin

urlpatterns = [
    # path('admin/', admin.site.urls),  #  注释掉原本的admin url
    # 添加xadmin的url
    path('xadmin/', xadmin.site.urls),
    # 添加验证码url
    path('captcha', include('captcha.urls')),
    # 登录注册url
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    # 重设密码url
    path('reset_pwd', ResetPwdView.as_view(), name='reset_pwd'),
    # path('users/', include('users.urls')),
    # 主页url
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
]

