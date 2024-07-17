from django.contrib.auth.decorators import login_required
import hashlib
import time
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from home.models import MailingToken
def get_filename(filename, request):
    hash_object = hashlib.sha1(str(time.time()).encode('utf-8'))
    hash_object.update(filename.encode('utf-8'))
    return f'{hash_object.hexdigest()[:10]}-{filename}'



def sendMailToken(token):
    subject = "Mailing Confirmation"
    confirm_url = settings.SITE_URL + reverse("confirm_mailing", args=[token.token])
    html_message = render_to_string(
        "home/email_to_sender.html",
        {
            "token": token,
            "confirm_url": confirm_url,
        },
    )
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = [token.mailing.email]

    email = EmailMultiAlternatives(subject, plain_message, from_email, to)
    email.attach_alternative(html_message, "text/html")

    attachments = [
        attachment.file.path for attachment in token.mailing.attachments.all()
    ]
    for attachment in attachments:
        email.attach_file(attachment)

    email.send()

@login_required
def confirm_mailing(request, token):
    mailing_token = get_object_or_404(MailingToken, token=token, sent=False)
    mailing = mailing_token.mailing

    # Render email content from template
    html_message = render_to_string(
        "home/email_to_recipients.html", {"mailing": mailing}
    )
    plain_message = strip_tags(html_message)
    subject = mailing.subject

    from_email = settings.EMAIL_HOST_USER
    recipients = []

    for batch in mailing.batches.all():
        recipients += batch.recipients.split(",")

    # Create the email message
    email = EmailMultiAlternatives(subject, plain_message, from_email, recipients)
    email.attach_alternative(html_message, "text/html")

    # Attach files
    for attachment in mailing.attachments.all():
        email.attach_file(attachment.file.path)

    # Send the email
    email.send(fail_silently=False)

    mailing_token.sent = True
    mailing_token.save()

    return HttpResponse("Email sent successfully!")
