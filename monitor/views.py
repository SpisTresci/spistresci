# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from models import *
from datetime import datetime, timedelta

def monitor(request):

    if request.user.is_authenticated() and request.user.username == 'admin':
        services = list(Service.objects.all())
        services.sort(key=lambda x: x.name.lower())
        update_statuses = UpdateStatus.objects.order_by('id')[:25].reverse()

        table = []
        for us in update_statuses:
            s_stable = []
            table.append(s_stable)
            for service in services:
                uss_s = UpdateStatusService.objects.filter(update_status_id = us.id, service_name = service.name)
                uss = uss_s[0] if len(uss_s) != 0 else None
                s_stable.append(uss)

        repair_dates(update_statuses)
        return render(request, 'monitor/index.html', {"data": table, "services":services, "update_statuses": update_statuses})
    else:
        return redirect("/")


def repair_dates(update_statuses):
    for us in update_statuses:
        if us.start:
            us.start = us.start - timedelta(hours=1)
        if us.end:
            us.end = us.end - timedelta(hours=1)
