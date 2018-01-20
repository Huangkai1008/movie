from django.contrib import admin
from .models import Tag, Movie, Preview, MovieLike


class TagAdmin(admin.ModelAdmin):
    pass


class MovieAdmin(admin.ModelAdmin):
    pass


class PreviewAdmin(admin.ModelAdmin):
    pass


class MovieLikeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tag, TagAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Preview, PreviewAdmin)
admin.site.register(MovieLike, MovieLikeAdmin)

# Register your models here.
