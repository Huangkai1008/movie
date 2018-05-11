from django.shortcuts import render
from django.views.generic.base import View

from .models import Movie, Tag, Region
# Create your views here.


class IndexView(View):
    """
    主页视图
    """
    def get(self, request):
        # 取出10个热门的电影
        hot_movies = Movie.objects.filter(is_hot=True)[:10]
        new_movies = Movie.objects.order_by('-add_time')
        return render(request, 'index.html', {'hot_movies': hot_movies,
                                              'new_movies': new_movies})


class MovieListView(View):
    """
    电影列表视图
    """
    def get(self, request):
        # 取出所有电影
        all_movies = Movie.objects.all()
        # 电影总数
        movie_counts = all_movies.count()
        # 所有地区
        regions = Region.objects.all()
        # 所有分类
        tags = Tag.objects.all()
        return render(request, 'films/movie_list.html', {'all_movies': all_movies,
                                                         'movie_counts': movie_counts,
                                                         'regions': regions,
                                                         'tags': tags})