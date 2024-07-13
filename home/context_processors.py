from django.contrib import admin
from django.contrib.auth.decorators import login_required

@login_required
def userprocessor(request):
    return {'user': request.user}