from django.contrib import admin
from .models import Tag, Movie, MovieLike, Language, Region


class TagAdmin(admin.ModelAdmin):
    pass


class MovieAdmin(admin.ModelAdmin):
    pass


class LanguageAdmin(admin.ModelAdmin):
    pass


class RegionAdmin(admin.ModelAdmin):
    pass


class MovieLikeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tag, TagAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(MovieLike, MovieLikeAdmin)
admin.site.register(Region, RegionAdmin)

# Register your models here.
