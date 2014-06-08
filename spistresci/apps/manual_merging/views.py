# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

def manual_merging(request):
    return render_to_response('manual_merging/index.html')

def manual_merging_take(request):
    return render_to_response('manual_merging/internal/take.html')