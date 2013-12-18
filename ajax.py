# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form

from spistresci.track.forms import BookTrackForm
from spistresci.models import MasterBook
from spistresci.track.models import BookTrack

@dajaxice_register
def get_track_form(request, book_id, callback):
    dajax = Dajax()

    book = get_object_or_404(MasterBook, pk=book_id)
    initial = dict()

    if request.user.is_authenticated():
        booktrack = BookTrack.objects.filter(masterbook=book, user=request.user).exclude(price=None)
        #initial = dict(price=booktrack[0].price/100.0)

    form = BookTrackForm(initial=initial)

    html = render_to_string('track/track_form.html', dict(track_form=form, product=book, user=request.user))
    dajax.assign('#track_form_container_%s' % book_id,'innerHTML', html)

    dajax.add_data(book_id, callback)

    return dajax.json()


@dajaxice_register
def post_track_form(request, form):
    dajax = Dajax()

    values = deserialize_form(form)

    book_id = values['book']
    book = get_object_or_404(MasterBook, pk=book_id)
    booktrack = BookTrack.objects.get_or_create(masterbook=book, user=request.user)[0]

    form = BookTrackForm(values, instance=booktrack)
    if form.is_valid():
        dajax.remove_css_class('#track_form input', 'error')
        track = form.save()
        dajax.assign('#track_form_container_%s' % book_id,'innerHTML', '')
        dajax.assign('#track_form_container_%s' % book_id,'innerHTML', '')

        if track.price != None:
            dajax.alert(u'Trop został zapisany');
        else:
            dajax.alert(u'Trop został usunięty');

    else:
        dajax.alert(u'Podaj prawidłową cenę');
        # dajax.remove_css_class('#track_form input', 'error')
        # for error in form.errors:
        #     dajax.add_css_class('#id_%s' % error, 'error')



    return dajax.json()
