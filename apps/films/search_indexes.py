from haystack import indexes
from .models import Movie


class MovieIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    add_time = indexes.DateTimeField(model_attr='add_time')

    def get_model(self):
        """
        重载get_model方法
        """
        return Movie

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

