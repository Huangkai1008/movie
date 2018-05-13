from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views.generic.base import View
from django.contrib import messages
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage
import markdown
from datetime import datetime
from .forms import CommentForm

from .models import Movie, Tag, Region, Comment
from users.models import UserProfile
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
    def get(self, request, *tag_type):
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
        region_id = request.GET.get('region', '')
        if region_id:
            all_movies = all_movies.filter(regions__pk=int(region_id))

        score = request.GET.get('score', '')
        if score:
            all_movies = all_movies.filter(score_douban__gte=float(score), score_douban__lte=float(float(score) + 1))

        tag_id = request.GET.get('tag', '')
        if tag_id:
            all_movies = all_movies.filter(tags__pk=int(tag_id))
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
                                                         'year': year,
                                                         'region_id': region_id,
                                                         'score': score,
                                                         'tag_id': tag_id,
                                                         'tag_type': tag_type})


class MovieDetailView(View):
    """
    电影详情视图
    """
    def get(self, request, movie_id):
        # 得到详情id
        film = Movie.objects.get(id=int(movie_id))
        if film.download_url is not None:
            has_down = True
        else:
            has_down = False
        # 给出推荐的影片
        select_movies = Movie.objects.order_by('?')[:6]
        comments = Comment.objects.filter(movie_id=film.id)
        for comment in comments:
            comment.content = markdown.markdown(comment.content,
                                                extensions=[
                                                    'markdown.extensions.extra',
                                                    'markdown.extensions.codehilite',
                                                    'markdown.extensions.toc',
                                                ])
        return render(request, 'films/movie_detail.html', {'film': film,
                                                           'select_movies': select_movies,
                                                           'has_down': has_down,
                                                           'comments': comments,
                                                           })


class CommentView(View):
    """
    评论视图
    """
    def get(self, request):
        comment_form = CommentForm()
        return render(request, 'films/movie_detail.html', {'comment_form':
                                                           comment_form})

    def post(self, request):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = Comment()
            comment.content = request.POST.get('content', None)
            comment.user_id_id = str(request.POST.get('user_id', None))
            movie_id = request.POST.get('movie_id', None)
            # comment.user_id = UserProfile.objects.get(pk=user_id_id)
            comment.movie_id_id = str(request.POST.get('movie_id', None))
            # comment.movie_id = Movie.objects.get(pk=movie_id_id)
            comment.add_time = datetime.now()
            comment.save()
            messages.success(request, '评论成功')
            return HttpResponseRedirect(reverse('movie_detail', kwargs={'movie_id': movie_id}))
        else:
            messages.error(request, '评论失败', extra_tags='bg-warning text-warning')

        return render(request, 'films/movie_detail.html', {'comment_form':
                                                           comment_form})

