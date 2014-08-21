# -*- coding: utf-8 -*-

from datetime import datetime
from django.utils import timezone
from collections import defaultdict
from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings

from spistresci.common.helpers import send_email
from spistresci.track.models import BookTrackNotification


class Command(BaseCommand):

    email_template = 'track/notification_email.html'

    option_list = BaseCommand.option_list + (
        make_option('-d', '--dry-run',
                    action='store_true',
                    dest='dry_run',
                    help='Dry run just to print notifications without sending emails',
                    default=False),
    )

    def group_tracks(self):
        result = defaultdict(list)
        for track in self.tracks:
            result[track.user].append(track)
        self.tracks = result

    def handle(self, *args, **options):
        self.tracks = BookTrackNotification.objects.filter(sent_date=None)
        self.group_tracks()

        for user, tracks in self.tracks.iteritems():
            if not user.email:
                continue
            dry_run = options.get('dry_run')
            masterbooks = map(lambda x: x.masterbook, tracks)

            print '************'
            print 'Sending notification to user %s (email: %s)' % (user.username, user.email)
            print 'Books: \t',
            print '\n\t'.join(map(lambda x: "%s, price: %s" % (x.title, x.price), masterbooks))

            context = dict(user=user,
                           masterbooks=masterbooks)
            email_from = getattr(settings, 'DEFAULT_EMAIL_FROM', 'no-replay@spistresci.pl')
            subject = u"Powiadomienie o cenie książki"
            if dry_run:
                continue
            try:
                send_email(self.email_template, context, email_from,
                           [user.email], subject)

            except Exception as inst:
                print "can't send email"
                print str(inst)
            else:
                for track in tracks:
                    track.sent_date = timezone.localtime(timezone.now())
                    track.save()
