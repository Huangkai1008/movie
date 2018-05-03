from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    """
    用户信息
    """
    GENDER_CHOICES = (
        ('male', u'男'),
        ('female', u'女')
    )

    nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default="")
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(
        max_length=5,
        verbose_name=u"性别",
        choices=GENDER_CHOICES,
        default="male")
    address = models.CharField(max_length=100, verbose_name="地址", default="")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name=u'手机号')
    image = models.ImageField(
        upload_to="image/%Y/%m",
        default=u"image/default.png",
        max_length=100,
        verbose_name=u'头像'
    )

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username











