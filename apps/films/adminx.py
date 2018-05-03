from .models import Tag, Movie, Preview, MovieLike

import xadmin


class TagAdmin(object):
    pass


class MovieAdmin(object):
    list_display = ('name_cn', 'name', 'year', 'country', 'category', 'language', 'subtitle',
                    'release_date', 'score', 'duration', 'director', 'download_url')
    list_filter = ('year', 'country', 'category', 'language', 'score', 'director')
    search_fields = ('name_cn', 'name', 'country', 'category', 'director')


class PreviewAdmin(object):
    pass


class MovieLikeAdmin(object):
    pass


xadmin.site.register(Movie, MovieAdmin)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Preview, PreviewAdmin)
xadmin.site.register(MovieLike, MovieLikeAdmin)
