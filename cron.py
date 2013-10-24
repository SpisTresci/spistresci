from django_cron import CronJobBase, Schedule
from spistresci.management.commands.send_track_notifications import Command as send_track_notifications
from registration.management.commands.cleanupregistration import Command as cleanupregistration


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
