from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MailingForm
from .models import Mailing, Batch, Attachments, MailingToken
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import uuid
import os
from django.urls import reverse
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives


@login_required
def home(request):
    sent_mails = Mailing.objects.filter(email=request.user.email)
    context = {
        "sent_mails": sent_mails,
    }
    return render(request, "home/index.html", context)


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
def create_mailing(request):
    if request.method == "POST":
        print(request.POST)
        form = MailingForm(request.POST, request.FILES)
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.email = request.user.email
            mailing.save()

            batches = request.POST.getlist("batches")
            for batch_id in batches:
                batch = Batch.objects.get(id=batch_id)
                mailing.batches.add(batch)

            files = request.FILES.getlist("attachments")
            for file in files:
                Attachments.objects.create(file=file, mailing=mailing)

            # Create a mailing_token for the mailing
            token = str(uuid.uuid4())
            mailing_obj = MailingToken.objects.create(
                mailing=mailing, token=token, sent=False
            )
            sendMailToken(mailing_obj)
            messages.success(
                request,
                "Mailing created successfully! Check your inbox for the confirmation email.",
            )
            return redirect("index")
        else:
            print("Form is invalid")
            print(form.errors)
    else:
        form = MailingForm()

    batches = Batch.objects.all()
    context = {
        "form": form,
        "batches": batches,
    }
    return render(request, "home/create_mailing.html", context)

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


def base(r):
    return render(r, "base.html")
