from spistresci.track.models import BookTrack
from django import forms

class BookTrackForm(forms.ModelForm):

	class Meta:
		model = BookTrack
		fields = ['price']

	def save(self, user, book):
		track = super(BookTrackForm, self).save(comit=False)
		track.user = user
		track.book = book
		track.save()
		return track
