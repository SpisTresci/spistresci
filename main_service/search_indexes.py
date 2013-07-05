from haystack import indexes
from models import MasterBookSolrWrapper

class MasterBookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(index_fieldname='title', stored=True)
    price_lowest = indexes.CharField(index_fieldname='price_lowest', stored=True)

    name = indexes.MultiValueField()
    firstName = indexes.MultiValueField()
    middleName = indexes.MultiValueField()
    lastName = indexes.MultiValueField()

    image_url = indexes.CharField(index_fieldname='image_url', stored=True)
    formats = indexes.CharField(index_fieldname='formats', stored=True)

    format_mobi =  indexes.MultiValueField()
    format_epub =  indexes.MultiValueField()
    format_pdf =  indexes.MultiValueField()

    def get_model(self):
        return MasterBookSolrWrapper

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
