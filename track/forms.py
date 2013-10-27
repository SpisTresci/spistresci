# -*- coding: utf-8 -*-

from decimal import Decimal
from spistresci.track.models import BookTrack
from django import forms

class BookTrackForm(forms.ModelForm):

    price = forms.CharField(max_length=10, required=False)

    class Meta:
        model = BookTrack
        fields = ['price']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price:
            try:
                return int(Decimal(price.replace(',', '.')) * 100)
            except:
                raise forms.ValidationError(u"Podaj prawidłową cenę")
