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

from django.urls import path, include, re_path
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings
from movie.settings import MEDIA_ROOT
from users.views import LoginView, RegisterView, ResetPwdView, ActiveUserView
from films.views import IndexView, MovieListView, MovieDetailView, CommentView
import xadmin

urlpatterns = [
    # path('admin/', admin.site.urls),  #  注释掉原本的admin url
    # 添加xadmin的url
    path('xadmin/', xadmin.site.urls),
    # 处理图片显示的url, 使用django自带的serve，传入media_root的参数
    re_path(r'^media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
    # 添加验证码url
    path('captcha', include('captcha.urls')),
    # 登录注册url
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    # 重设密码url
    path('reset_pwd/', ResetPwdView.as_view(), name='reset_pwd'),
    # path('users/', include('users.urls')),
    # 添加详情
    # path('detail/', TemplateView.as_view(template_name='films/movie_detail.html'), name='detail'),
    re_path('movie_list/(?P<movie_id>\d+)/', MovieDetailView.as_view(), name='movie_detail'),
    # 主页url
    # path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('', IndexView.as_view(), name='index'),
    # 电影列表视图
    path('movie_list/', MovieListView.as_view(), name='movie_list'),
    # path('films/', include('films.urls', namespace='films')),
    # 激活账户验证码url
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name='user_active'),
    # haystack url
    path('search/', include('haystack.urls')),
    # 评论url
    path('comment', CommentView.as_view(), name='comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   # 配置xadmin的图像文件加载路径


