from django.shortcuts import render
from django.http import HttpResponse,FileResponse
from .models import MailSeen

def track(request, token):
    if request.method == 'GET':
        mailobj = None
        try:
            mailobj = MailSeen.objects.get(token=token)
        except:
            print("Object doesnot exist")
        if mailobj is not None:
            mailobj.seen = True
            mailobj.save()
            print("Object updated")
        image_path = 'templates/1x1.png'
        response = FileResponse(open(image_path, 'rb'), content_type='image/png')
        return response