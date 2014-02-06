import os

from django.conf import settings

from django_cron import CronJobBase, Schedule
from spistresci.management.commands.send_track_notifications import Command as send_track_notifications
from spistresci.management.commands.verify_prices import Command as verify_prices
from spistresci.management.commands.afiliant_update import Command as afiliant_update
from registration.management.commands.cleanupregistration import Command as cleanupregistration

from subprocess import call

class TrackNotificationCronJob(CronJobBase):
    RUN_AT_TIMES = ['8:00']

    # NOTE: use this schedule for tests
    # schedule = Schedule(run_every_mins=0)
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'spistresci.track_notifications'

    def do(self):
        # NOTE: dry run
        # send_track_notifications().handle(dry_run=True)
        send_track_notifications().handle()


class ClearUsersCronJob(CronJobBase):
    RUN_AT_TIMES = ['7:00']

    # NOTE: use this schedule for tests
    # schedule = Schedule(run_every_mins=0)
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'spistresci.clear_users'

    def do(self):
        cleanupregistration().handle_noargs()


class VerifyPricesCronJob(CronJobBase):
    RUN_AT_TIMES = ['7:10']

    # NOTE: use this schedule for tests
    # schedule = Schedule(run_every_mins=0)
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'spistresci.verify_prices'

    def do(self):
        verify_prices().handle(email_admins=True)


class AfiliantUpdateCronJob(CronJobBase):
    RUN_AT_TIMES = ['1:50', '3:50', '5:50', '7:50', '9:50', '11:50', '13:50',
        '15:50', '17:50', '19:50', '21:50', '23:50']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'spistresci.afiliant_update'

    def do(self):
        afiliant_update().handle()
