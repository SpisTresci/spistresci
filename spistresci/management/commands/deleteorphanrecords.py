# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from spistresci.model_controler import add_MiniBook
from spistresci.models import Bookstore
import inspect

class Command(BaseCommand):

    def handle(self, *args, **options):

        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        for name, __method__ in methods:
            if name.startswith('delete_orphan_'):
                __method__()

    def delete_orphan_BookFormat_records(self):
        pass

    def delete_orphan_Bookstore_records(self):
        pass

    def delete_orphan_BookDescription_records(self):
        pass

    def delete_orphan_ISBN_records(self):
        pass

    def delete_orphan_MasterAuthor_records(self):
        pass

    def delete_orphan_MiniAuthor_records(self):
        pass

    def delete_orphan_MasterBook_records(self):
        pass

    def delete_orphan_MiniBook_records(self):
        pass
