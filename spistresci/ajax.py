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
def get_track_form(request, book_id, callback, template="track/track_form.html", placeholder="#popup_container"):
    dajax = Dajax()

    book = get_object_or_404(MasterBook, pk=book_id)
    initial = dict()

    if request.user.is_authenticated():
        booktrack = BookTrack.objects.filter(masterbook=book, user=request.user).exclude(price=None)
        #initial = dict(price=booktrack[0].price/100.0)

    form = BookTrackForm(initial=initial)

    html = render_to_string(template, dict(track_form=form, product=book, user=request.user))
    #dajax.assign('#track_form_container_%s' % book_id,'innerHTML', html)
    dajax.assign(placeholder,'innerHTML', html)

    dajax.add_data(book_id, callback)

    return dajax.json()

@dajaxice_register
def get_track_form_static(request, book_id, callback):
    return get_track_form(request, book_id, callback, template="track/track_form__book.html", placeholder="#track_placeholder")


@dajaxice_register
def post_track_form(request, form, error_placeholder="#track_bottom_msg_%(id)s", msg_placeholder="#track_popup_%(id)s"):
    dajax = Dajax()

    values = deserialize_form(form)

    book_id = values['book']
    book = get_object_or_404(MasterBook, pk=book_id)
    booktrack = BookTrack.objects.get_or_create(masterbook=book, user=request.user)[0]

    form = BookTrackForm(values, instance=booktrack)

    error_placeholder = error_placeholder % {"id":book_id}
    msg_placeholder = msg_placeholder  % {"id":book_id}

    if form.is_valid():
        dajax.remove_css_class('#track_form input', 'error')
        track = form.save()

        if track.price != None:
            dajax.assign(msg_placeholder,'innerHTML', u'<h1>Trop został zapisany</h1>')
        else:
            dajax.assign(msg_placeholder,'innerHTML', u'<h1>Trop został usunięty</h1>')

    else:
        dajax.assign(error_placeholder,'innerHTML', u'Podaj cenę, np. 9.99')
        # dajax.remove_css_class('#track_form input', 'error')
        # for error in form.errors:
        #     dajax.add_css_class('#id_%s' % error, 'error')


    return dajax.json()

@dajaxice_register
def post_track_form_static(request, form):
    return post_track_form(request, form, error_placeholder="#track_bottom_msg_%(id)s", msg_placeholder="#track_bottom_msg_%(id)s")
