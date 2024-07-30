from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from home.models import Batch
from .forms import BatchForm

def is_admin(user):
    return user.role == 'admin'

@user_passes_test(is_admin)
def batch_list(request):
    batches = Batch.objects.all()
    return render(request, 'batches/batch_list.html', {'batches': batches})

@user_passes_test(is_admin)
def batch_detail(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    return render(request, 'batches/batch_detail.html', {'batch': batch})

@user_passes_test(is_admin)
def batch_create(request):
    if request.method == 'POST':
        form = BatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('batch_list')
    else:
        form = BatchForm()
    return render(request, 'batches/batch_form.html', {'form': form})

@user_passes_test(is_admin)
def batch_update(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    if request.method == 'POST':
        form = BatchForm(request.POST, instance=batch)
        if form.is_valid():
            form.save()
            return redirect('batch_detail', pk=batch.pk)
    else:
        form = BatchForm(instance=batch)
    return render(request, 'batches/batch_form.html', {'form': form})

@user_passes_test(is_admin)
def batch_delete(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    if request.method == 'POST':
        batch.delete()
        return redirect('batch_list')
    return render(request, 'batches/batch_confirm_delete.html', {'batch': batch})


