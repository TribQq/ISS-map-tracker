from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from . import tasks


def load_pic(request):
    """ start task """
    tasks.download_cat.delay() # ставим в очередь в асинк режиме
    return HttpResponse('<h1>Load cat </h1>')