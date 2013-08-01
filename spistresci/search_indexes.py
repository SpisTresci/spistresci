from haystack import indexes
from models import MasterBookSolrWrapper
from models import BookstoreSolrWrapper


class IntegerMultiValueField(indexes.MultiValueField):
    field_type = 'integer'

class MasterBookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(index_fieldname='title', stored=True)
    price_lowest = indexes.IntegerField(index_fieldname='price_lowest', stored=True)

    name = indexes.MultiValueField()
    firstName = indexes.MultiValueField()
    middleName = indexes.MultiValueField()
    lastName = indexes.MultiValueField()

    url = indexes.MultiValueField()
    cover = indexes.MultiValueField()

    formats = indexes.CharField(index_fieldname='formats', stored=True)

    format_mobi = indexes.BooleanField(index_fieldname='format_mobi', stored=True)
    format_epub = indexes.BooleanField(index_fieldname='format_epub', stored=True)
    format_pdf = indexes.BooleanField(index_fieldname='format_pdf', stored=True)
    format_cd = indexes.BooleanField(index_fieldname='format_cd', stored=True)
    format_mp3 = indexes.BooleanField(index_fieldname='format_mp3', stored=True)

    bookstore = indexes.MultiValueField()
    price = IntegerMultiValueField()
    mini_format_mobi = indexes.MultiValueField()
    mini_format_epub = indexes.MultiValueField()
    mini_format_pdf = indexes.MultiValueField()
    mini_format_cd = indexes.MultiValueField()
    mini_format_mp3 = indexes.MultiValueField()

    def get_model(self):
        return MasterBookSolrWrapper

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class BookstoreIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    bookstore = indexes.CharField(index_fieldname='bookstore', stored=True)
    miniBookCount = indexes.IntegerField(index_fieldname='miniBookCount', stored=True)

    def get_model(self):
        return BookstoreSolrWrapper

    def index_queryset(self, using=None):
        return self.get_model().objects.all()