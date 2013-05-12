from django.http import HttpResponse
#-*- coding: utf-8 -*-
def main(request):
    return HttpResponse("Tutaj powstaje nowy serwis dla wszystkich miłośników książek elektronicznych.Jeżeli chcesz być powiadomiony o starcie serwisu, zostaw proszę nam swój adres email:")

