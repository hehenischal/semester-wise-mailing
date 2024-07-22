from django.shortcuts import render
from django.http import HttpResponse
from .models import MailSeen

# Create your views here.


def track(request, token):
    if request.method == 'GET':
        MailSeen.objects.get(token=token).seen = True
        response = HttpResponse(content_type='image/png')
        response['Content-Disposition'] = 'inline'
        response['Content-Length'] = '0'
        response['Content-Type'] = 'image/png'
        return response
