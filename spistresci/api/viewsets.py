from rest_framework import viewsets

from spistresci.api.serializers import (
    BookFormatSerializer,
    BookFormatTypeSerializer,
    MasterBookSerializer,
    MiniBookSerializer,
    MiniBookSimilaritySerializer,
)
from spistresci.models import (
    BookFormat,
    BookFormatType,
    MasterBook,
    MiniBook,
    Similarity,
)


class BookFormatTypeViewSet(viewsets.ModelViewSet):
    queryset = BookFormatType.objects.all()
    serializer_class = BookFormatTypeSerializer


class BookFormatViewSet(viewsets.ModelViewSet):
    queryset = BookFormat.objects.all()
    serializer_class = BookFormatSerializer


class MasterBookViewSet(viewsets.ModelViewSet):
    queryset = MasterBook.objects.all()
    serializer_class = MasterBookSerializer


class MiniBookViewSet(viewsets.ModelViewSet):
    queryset = MiniBook.objects.all()
    serializer_class = MiniBookSerializer


class MiniBookSimilarityViewSet(viewsets.ModelViewSet):
    queryset = Similarity.objects.all()
    serializer_class = MiniBookSimilaritySerializer