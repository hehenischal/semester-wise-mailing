from django import forms 
from home.models import Batch

class BatchForm(forms.ModelForm):
    recipients = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Batch
        fields = ['name', 'recipients']

