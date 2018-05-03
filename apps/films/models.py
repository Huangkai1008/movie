from django.db import models
from datetime import datetime
from users.models import UserProfile
# Create your models here.


class Tag(models.Model):
    """
    电影标签
    """
    name = models.CharField(max_length=64, unique=True, verbose_name="标签名")
    add_time = models.DateTimeField(db_index=True, default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "电影标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Movie(models.Model):
    """
    电影模型
    """
    name_cn = models.CharField(max_length=260, verbose_name="译名", blank=True, null=True)
    name = models.CharField(max_length=128, verbose_name="片名", blank=True, null=True)
    year = models.CharField(max_length=60, verbose_name="上映年份", blank=True, null=True)
    country = models.CharField(max_length=64, verbose_name="产地|国家", blank=True, null=True)
    category = models.CharField(max_length=128, verbose_name="标签", blank=True, null=True)
    language = models.CharField(max_length=64, verbose_name="电影语言", blank=True, null=True)
    subtitle = models.CharField(max_length=64, verbose_name="字幕语言", blank=True, null=True)
    release_date = models.CharField(max_length=64, verbose_name="上映时间", blank=True, null=True)
    score = models.CharField(max_length=256, verbose_name="评分", blank=True, null=True)
    file_count = models.CharField(max_length=128, verbose_name="计数", blank=True, null=True)
    duration = models.CharField(max_length=128, verbose_name="片长", blank=True, null=True)
    director = models.CharField(max_length=128, verbose_name="导演", blank=True, null=True)
    download_url = models.TextField(max_length=500, verbose_name="下载地址")

    class Meta:
        verbose_name = "电影模型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name_cn


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

    def __str__(self):
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

    def __str__(self):
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

