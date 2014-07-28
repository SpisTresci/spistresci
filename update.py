import os
from django_cron import CronJobBase, Schedule
from spistresci.connectors.generic.GenericConnector import GenericConnector
from spistresci.connectors.utils.ConfigReader import ConfigReader
from spistresci.connectors import Tools
from spistresci.connectors.management.commands.connectorsupdate \
    import Command as connectorsupdate

class UpdateManager(CronJobBase):
    RUN_AT_TIMES = ['8:00']

    # NOTE: use this schedule for tests
    schedule = Schedule(run_every_mins=0)
    #schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'spistresci.update'

    def do(self):
        connectorsupdate.handle()