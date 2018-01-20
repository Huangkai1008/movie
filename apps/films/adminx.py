from .models import Tag, Movie, Preview, MovieLike

import xadmin


class TagAdmin(object):
    pass


class MovieAdmin(object):
    pass


class PreviewAdmin(object):
    pass


class MovieLikeAdmin(object):
    pass


xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Movie, MovieAdmin)
xadmin.site.register(Preview, PreviewAdmin)
xadmin.site.register(MovieLike, MovieLikeAdmin)
