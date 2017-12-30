from models import *
from django.shortcuts import render_to_response


def populate(request):
    return render_to_response('index.html')