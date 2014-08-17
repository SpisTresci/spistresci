from haystack import indexes
from .models import MasterBook


class MasterBookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title', faceted=True)

    def get_model(self):
        return MasterBook

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
