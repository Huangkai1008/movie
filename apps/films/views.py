from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage

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
        year = request.GET.get('year', '')
        if year:
            if int(year) < 2014:
                all_movies = all_movies.filter(year < 2014)
            else:
                all_movies = all_movies.filter(year=year)
        region = request.GET.get('region', '')
        # 对电影总数进行分页, 尝试获取前台get过来的page参数,如果参数不合法那么返回默认的第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_movies, 25, request=request)
        movies = p.page(page)
        return render(request, 'films/movie_list.html', {'all_movies': movies,
                                                         'movie_counts': movie_counts,
                                                         'regions': regions,
                                                         'tags': tags,
                                                         'year': year})


class MovieDetailView(View):
    """
    电影详情视图
    """
    def get(self, request, movie_id):
        # 得到详情id
        film = Movie.objects.get(id=int(movie_id))
        if film.douban_url is not None:
            has_down = True
        else:
            has_down = False
        # 给出推荐的影片
        select_movies = Movie.objects.order_by('?')[:6]
        return render(request, 'films/movie_detail.html', {'film': film,
                                                           'select_movies': select_movies,
                                                           'has_down': has_down})
