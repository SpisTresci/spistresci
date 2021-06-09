from haystack import indexes
from .models import MasterBook


class MasterBookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title', faceted=True)
    format = indexes.MultiValueField()
    bookstore = indexes.MultiValueField()
    price_lowest = indexes.DecimalField()
    price_highest = indexes.DecimalField()

    def prepare_bookstore(self, obj):
        return obj.bookstores()

    def prepare_format(self, obj):
        return [format.name for format in obj.formats.all()]

    def prepare_price_lowest(self, obj):
        return obj.price_lowest()

    def prepare_price_highest(self, obj):
        return obj.price_highest()

    def get_model(self):
        return MasterBook

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
