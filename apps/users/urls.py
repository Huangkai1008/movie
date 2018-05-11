from django.urls import path
from django.contrib.auth.views import login, logout, logout_then_login
from django.contrib.auth.decorators import login_required

app_name = 'users'

urlpatterns = [
    # 登录登出
    # path('login/', login, name='login'),  # 用户登录视图
    # path('logout/', logout, name='logout'),  # 用户登出视图
    # path('logout-then-login', logout_then_login, name='logout_then_login'),  # 用户登出再登录视图
    # 用户中心
]