from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from home.models import Batch
from .forms import BatchForm
from django.contrib import messages

def is_admin(user):
    return user.role == 'admin'

def batches(request):
    batches = Batch.objects.all()
    return render(request, 'batches/batch_form.html', {'batches': batches})

@user_passes_test(is_admin)
def batch_list(request):
    batches = Batch.objects.all()
    return render(request, 'components/batch_list.html', {'batches': batches})


@user_passes_test(is_admin)
def batch_create(request):
    if request.method == 'POST':
        form = BatchForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Batch created successfully')
        else:
            messages.error(request, 'Error creating batch',extra_tags='danger')
        return render(request, 'components/toast.html')

@user_passes_test(is_admin)
def batch_update(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    if request.method == 'POST':
        form = BatchForm(request.POST, instance=batch)
        if form.is_valid():
            form.save()
            messages.success(request, 'Batch updated successfully')
            return render(request, 'components/toast.html')
        else:
            messages.error(request, 'Error updating batch',extra_tags='danger')
            return render(request, 'components/toast.html')
    else:
        batch = Batch.objects.get(pk=pk)
    return render(request, 'components/batch_update.html', {'batch': batch})

@user_passes_test(is_admin)
def batch_delete(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    if request.method == 'POST':
        batch.delete()
        return redirect('batch_list')


