from rest_framework import serializers
from rest_framework.reverse import reverse

from spistresci.models import (
    BookFormat,
    BookFormatType,
    MasterBook,
    MiniBook,
    Similarity,
)


class BookFormatTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookFormatType


class BookFormatSerializer(serializers.ModelSerializer):
    type = serializers.RelatedField()

    class Meta:
        model = BookFormat
        fields = ('name', 'type')


class MiniBookSerializer(serializers.ModelSerializer):

    formats = BookFormatSerializer()

    class Meta:
        model = MiniBook


class MasterBookSerializer(serializers.HyperlinkedModelSerializer):
    mini_books = MiniBookSerializer(many=True)

    formats = BookFormatSerializer()

    class Meta:
        model = MasterBook


class MiniBookSimilaritySerializer(serializers.HyperlinkedModelSerializer):

    lower_masterbook = serializers.SerializerMethodField('get_lower_masterbook')
    higher_masterbook = serializers.SerializerMethodField('get_higher_masterbook')

    def get_lower_masterbook(self, obj):
        return reverse(
            'masterbook-detail',
            args=[obj.lower_id.master.id],
            request=self.context['request']
        )

    def get_higher_masterbook(self, obj):
        return reverse(
            'masterbook-detail',
            args=[obj.higher_id.master.id],
            request=self.context['request']
        )

    class Meta:
        model = Similarity
        #fields = ('id', 'result', 'lower_id', 'higher_id', 'lower_masterbook_id', 'higher_masterbook_id',)