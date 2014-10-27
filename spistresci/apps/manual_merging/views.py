# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from spistresci.models import Similarity


def manual_merging(request):
    return render_to_response('manual_merging/index.html')

def manual_merging_take(request):

    pair = Similarity.objects.order_by('?')[0]

    context = {
        "book_left": pair.lower_id.master,
        "book_right": pair.higher_id.master,
    }

    return render_to_response('manual_merging/internal/take.html', context)