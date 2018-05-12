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


class Region(models.Model):
    """
    上映地区
    """
    name = models.CharField(max_length=128, unique=True, verbose_name="地区名")
    add_time = models.DateTimeField(db_index=True, default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "上映地区"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Language(models.Model):
    """
    电影语言
    """
    name = models.CharField(max_length=128, unique=True, verbose_name="电影语言名")
    add_time = models.DateTimeField(db_index=True, default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "电影语言"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Movie(models.Model):
    """
    电影模型
    """
    name = models.CharField(max_length=260, verbose_name="片名")
    year = models.CharField(max_length=60, verbose_name="上映年份")
    name_other = models.CharField(max_length=128, verbose_name="别名", blank=True, null=True)
    director = models.CharField(max_length=128, verbose_name="导演", default='')
    actor = models.CharField(max_length=280, verbose_name="主演", default='')
    tags = models.ManyToManyField(Tag, verbose_name="电影类型")
    image = models.ImageField(upload_to="movie/%Y/%m", default="movie/default.png",
                              max_length=100, verbose_name="电影图")
    languages = models.ManyToManyField(Language, verbose_name="语言")
    regions = models.ManyToManyField(Region, verbose_name="上映地区|国家")
    release_date = models.DateField(verbose_name="上映时间")
    intro = models.TextField(max_length=500, verbose_name="电影介绍", default='')
    is_hot = models.BooleanField(verbose_name="是否热门", default=False)
    duration = models.CharField(max_length=128, verbose_name="片长")
    score_douban = models.FloatField(verbose_name="豆瓣评分", null=True, blank=True)
    score_imdb = models.FloatField(verbose_name="IMDB评分", null=True, blank=True)
    douban_url = models.TextField(max_length=500, verbose_name="豆瓣电影链接地址", default='')
    imdb_url = models.TextField(max_length=500, verbose_name="IMDB链接地址", default='')
    download_url = models.TextField(max_length=500, verbose_name="下载地址", default='')
    add_time = models.DateTimeField(verbose_name="添加时间", db_index=True, default=datetime.now)

    class Meta:
        verbose_name = "电影模型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


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


