# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from spistresci.models import CommandStatus, BookstoreCommandStatus
from datetime import datetime, timedelta

def monitor(request):

    if True:#request.user.is_authenticated() and request.user.username == 'admin':

        context = {}

        commands = list(CommandStatus.objects.all())
        commands.reverse()
        commands = commands[:20]
        context['commands'] = commands

        bookstores = {}
        for command in commands:
            for bcs in command.bookstorecommandstatus_set.all():
                bookstores[bcs.bookstore.name] = bcs.bookstore

        bookstores = [bookstores[key] for key in sorted(bookstores)]
        context['bookstores'] = bookstores

        data = []
        for command in commands:
            row = {'command': command, 'innerrows': []}
            data.append(row)

            for type, desc in BookstoreCommandStatus.TYPE_CHOICES:
                inner_row = []
                row['innerrows'].append(inner_row)
                for bookstore in bookstores:
                    try:
                        bcs = BookstoreCommandStatus.objects.get(
                            cmd_status=command,
                            bookstore=bookstore,
                            type=type
                        )
                    except BookstoreCommandStatus.DoesNotExist:
                        bcs = None

                    inner_row.append(bcs)

        context['data'] = data

        return render(request, 'monitor/index.html', context)
    else:
        return redirect("/")


def repair_dates(update_statuses):
    for us in update_statuses:
        if us.start:
            us.start = us.start - timedelta(hours=1)
        if us.end:
            us.end = us.end - timedelta(hours=1)
