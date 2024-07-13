from django.shortcuts import render, redirect
from .forms import MailingForm
from .models import Mailing, Batch, Attachments
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home/index.html')

@login_required
def create_mailing(request):
    if request.method == 'POST':
        print(request.POST)
        form = MailingForm(request.POST, request.FILES)
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.email = request.user.email  
            mailing.save()
            files = request.FILES.getlist('attachments')
            for file in files:
                Attachments.objects.create(file=file, mailing=mailing)  

            return redirect('success_url')  
        else:
            print("Form is invalid")
            print(form.errors)
    else:
        form = MailingForm()

    batches = Batch.objects.all()
    context = {
        'form': form,
        'batches': batches,
    }
    return render(request, 'home/create_mailing.html', context)

def base(r):
    return render(r, 'base.html')
