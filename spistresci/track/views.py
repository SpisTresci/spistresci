from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from spistresci.models import MasterBook
from spistresci.track.models import BookTrack
from spistresci.track.forms import BookTrackForm


class BookTrack(FormView):
    """
    to save new track for user send post to this view
    """
    template_name = '' # this is not important because we are using only post method
    form_class = BookTrackForm
    success_url = '/' # todo

    def form_valid(self, form):
        book = get_object_or_404(MasterBook, pk=self.kwargs['masterbook_pk'])
        form.save(self.reqest.user, book)
        return super(BookTrack, self).form_valid(form)

class TrackedBookList(ListView):
    model = BookTrack
    template_name = 'track/tracked_book_list.html'

    def get_queryset(self):
        return self.request.user.book_tracks.all()
