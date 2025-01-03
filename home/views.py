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
from django.core.mail import EmailMultiAlternatives
from tracking.models import MailSeen
from concurrent.futures import ThreadPoolExecutor


@login_required
def home(request):
    sent_mails = Mailing.objects.filter(email=request.user.email)
    for mail in sent_mails:
        mail.sent = MailingToken.objects.get(mailing=mail).sent
    context = {
        "sent_mails": sent_mails,
    }
    return render(request, "home/index.html", context)


def send_email_confirmation_async(email):
    email.send(fail_silently=False)

def sendMailToken(token):
    subject = "Mailing Confirmation"
    confirm_url = settings.SITE_URL + reverse("confirm_mailing", args=[token.token])
    html_message = render_to_string(
        "home/email_to_sender.html",
        {"token": token, "confirm_url": confirm_url, "mailing": token.mailing},
    )
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = [token.mailing.email]

    # Create the email message
    email = EmailMultiAlternatives(subject, plain_message, from_email, to)
    email.attach_alternative(html_message, "text/html")

    # Attach files
    attachments = [attachment.file.path for attachment in token.mailing.attachments.all()]
    for attachment in attachments:
        email.attach_file(attachment)

    # Submit email sending task to the thread pool
    executor.submit(send_email_confirmation_async, email)


@login_required
def create_mailing(request):
    if request.method == "POST":
        form = MailingForm(request.POST, request.FILES)
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.email = request.user.email
            mailing.tracking = form.cleaned_data["tracking"]

            mailing.save()
            batches = request.POST.getlist("batches")
            for batch_id in batches:
                batch = Batch.objects.get(id=batch_id)
                mailing.batches.add(batch)
            files = request.FILES.getlist("attachments")
            for file in files:
                Attachments.objects.create(file=file, mailing=mailing)
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
            messages.error(request, "There was an error creating the mailing.")
    else:
        form = MailingForm()

    batches = Batch.objects.all()
    context = {
        "form": form,
        "batches": batches,
    }
    return render(request, "home/create_mailing.html", context)


# ThreadPoolExecutor for asynchronous tasks
executor = ThreadPoolExecutor(max_workers=5)

def send_email_async(email, mailing_token):
    # Send the email
    email.send(fail_silently=False)

    # Update the token status after sending the email
    mailing_token.sent = True
    mailing_token.save()

@login_required
def confirm_mailing(request, token):
    mailing_token = get_object_or_404(MailingToken, token=token, sent=False)
    mailing = mailing_token.mailing

    if mailing.tracking:
        trackingobj = MailSeen.objects.create(mailing_id=mailing)
        tracking_url = settings.SITE_URL + reverse("track", args=[trackingobj.token])
        mailing.message = f'{mailing.message}<img src="{tracking_url}" alt="" style="display:none;">'
        mailing.save()

    # Render email content from template
    html_message = render_to_string("home/email_to_recipients.html", {"mailing": mailing})
    plain_message = strip_tags(html_message)
    subject = mailing.subject

    from_email = settings.EMAIL_HOST_USER
    recipients = [email for batch in mailing.batches.all() for email in batch.recipients.split(",")]

    # Create the email message
    email = EmailMultiAlternatives(subject, plain_message, from_email, recipients)
    email.attach_alternative(html_message, "text/html")

    # Attach files
    for attachment in mailing.attachments.all():
        email.attach_file(attachment.file.path)

    # Submit email sending task to the thread pool
    executor.submit(send_email_async, email, mailing_token)

    # Render the success page immediately
    return render(request, "home/success.html", {"mailing": mailing})

def base(r):
    return render(r, "base.html")


@login_required
def update_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)

    if request.method == "POST":
        form = MailingForm(request.POST, request.FILES, instance=mailing)
        if form.is_valid():
            # Save the updated mailing
            mailing = form.save(commit=False)
            mailing.email = request.user.email  # Ensure email is still set to the user
            mailing.save()

            # Update batches
            batches = request.POST.getlist("batches")
            mailing.batches.set(Batch.objects.filter(id__in=batches))

            # Delete existing attachments if new ones are uploaded
            if request.FILES.getlist("attachments"):
                mailing.attachments.all().delete()
                files = request.FILES.getlist("attachments")
                for file in files:
                    Attachments.objects.create(file=file, mailing=mailing)
            mailing_token = MailingToken.objects.get(mailing=mailing)

            sendMailToken(mailing_token)
            messages.success(request, "Mailing updated successfully! Check your inbox for the update notification.")
            return redirect("index")
        else:
            messages.error(request, "There was an error updating the mailing.")
    else:
        form = MailingForm(instance=mailing)

    batches = Batch.objects.all()
    context = {
        "form": form,
        "batches": batches,
        "mailing": mailing,
    }
    messages.add_message(request, messages.ERROR, "You need to provide the attachments again.", extra_tags='danger')
    return render(request, "home/update_mailing.html", context)


def view_mailing(req,pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    return render(req,'components/view_mail.html',{'mailing':mailing})



