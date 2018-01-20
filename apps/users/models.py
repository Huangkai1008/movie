from django.db import models
from datetime import datetime
# Create your models here.


class UserProfile(models.Model):
    """
    用户信息
    """
    name = models.CharField(max_length=50, verbose_name="昵称", default="", unique=True)
    pwd = models.CharField(max_length=50, verbose_name="密码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="手机号")
    info = models.TextField(max_length=255)
    face = models.ImageField(upload_to="image/%Y/%m", default="image/default.png", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="添加时间")
    uuid = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserLog(models.Model):
    """
    会员登录日志
    """
    user_id = models.ForeignKey(UserProfile, verbose_name="所属会员", on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(verbose_name="ip地址")
    add_time = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "会员登录日志"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id









