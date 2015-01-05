# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def __init__(self):
        super(Command, self).__init__()
        self.logger = None

    def handle(self, *args, **options):
        pass