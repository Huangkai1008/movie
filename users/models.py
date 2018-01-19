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

    def __unicode__(self):
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

    def __unicode__(self):
        return self.id


class Tag(models.Model):
    """
    电影标签
    """
    name = models.CharField(max_length=50, unique=True, verbose_name="标签名")
    add_time = models.DateTimeField(db_index=True, default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "电影标签"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Movie(models.Model):
    """
    电影模型
    """
    title = models.CharField(max_length=50, verbose_name="电影名")
    url = models.URLField(max_length=255, unique=True, verbose_name="播放地址")
    info = models.TextField(max_length=500, verbose_name="电影简介")
    logo = models.ImageField(upload_to="image/%Y/%m", default="image/default.png",
                             max_length=100, verbose_name="电影图")
    star = models.SmallIntegerField(verbose_name="电影评星")
    play_num = models.BigIntegerField(verbose_name="播放次数")
    comment_num = models.BigIntegerField(verbose_name="评论次数")
    tag_id = models.ForeignKey(Tag, verbose_name="电影所属标签", on_delete=models.CASCADE)
    area = models.CharField(max_length=50, verbose_name="上映地区")
    release_time = models.DateField(verbose_name="上映日期")
    length = models.CharField(max_length=100, verbose_name="电影长度")
    add_time = models.DateTimeField(db_index=True, default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "电影模型"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title


class Preview(models.Model):
    """
    上映预告
    """
    title = models.CharField(max_length=50, unique=True, verbose_name="名称")
    logo = models.ImageField(upload_to="image/%Y/%m", default="image/default.png",
                             max_length=100, verbose_name="预告图")
    add_time = models.DateTimeField(verbose_name="添加时间", db_index=True, default=datetime.now)

    class Meta:
        verbose_name = "上映预告"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    """
    评论
    """
    content = models.TextField(max_length=500, verbose_name="评论内容")
    movie_id = models.ForeignKey(Movie, verbose_name="所属电影", on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserProfile, verbose_name="所属用户", on_delete=models.CASCADE)
    add_time = models.DateTimeField(db_index=True, verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "电影评论"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.id


class MovieLike(models.Model):
    """
    电影收藏
    """
    movie_id = models.ForeignKey(Movie, verbose_name="所属电影", on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserProfile, verbose_name="所属用户", on_delete=models.CASCADE)
    add_time = models.DateTimeField(db_index=True, verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "电影收藏"
        verbose_name_plural = verbose_name







