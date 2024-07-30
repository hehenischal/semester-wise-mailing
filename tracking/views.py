from django.shortcuts import get_object_or_404,render
from django.http import FileResponse
from pathlib import Path
from django.conf import settings
from .models import MailSeen
from home.models import Mailing

def track(request, token):
    mail_seen = get_object_or_404(MailSeen, token=token)
    seen_mails = request.COOKIES.get('seen_mails', '')

    if str(mail_seen.mailing_id) not in seen_mails.split(','):
        mail_seen.increase_count()
        seen_mails = f"{seen_mails},{mail_seen.mailing_id}" if seen_mails else str(mail_seen.mailing_id)

    response = FileResponse(open(Path(settings.STATIC_ROOT) / '1x1.png', 'rb'), content_type='image/png')
    response.set_cookie('seen_mails', seen_mails, max_age=365*24*60*60)  
    return response


def analytics(request):
    mailings = Mailing.objects.filter(email=request.user.email)
    context = {
        "mailings": mailings,
    }
    return render(request, "analytics/mail_tracker.html", context)