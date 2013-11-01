from django import forms

from spistresci.blogger.models import BookRecommendation, BloggerRecommendation

class BookRecommendationForm(forms.ModelForm):

    class Meta:
        model = BookRecommendation

