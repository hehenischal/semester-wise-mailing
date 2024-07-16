from django.shortcuts import render, redirect, get_object_or_404
from .forms import MailingForm
from .models import Mailing, Batch, Attachments, MailingToken
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import uuid
from .utils import sendMailToken
from django.urls import reverse


@login_required
def home(request):
    sent_mails = Mailing.objects.filter(email=request.user.email)
    context = {
        "sent_mails": sent_mails,
    }
    return render(request, "home/index.html", context)




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

def base(r):
    return render(r, "base.html")
