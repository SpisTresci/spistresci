# -*- coding: utf-8 -*-
from haystack.views import SearchView
from spistresci.models import BookFormatType, BookFormat

class SpisTresciSearchView(SearchView):

    def extra_context(self):

        formats=[]
        for group in BookFormatType.objects.all():
           formats.append({
               'name': group.name,
               'items': BookFormat.objects.filter(type=group),
           })

        return {
            'filters': {
                'formats': formats,
            },
        }



        ctx.setdefault(
            'password_change_form',
            self.form_class(user=user, prefix='password_change')
        )
        ctx.setdefault(
            'change_email_form',
            self.change_email_form_class(self.request.POST, prefix='change_email')
        )
