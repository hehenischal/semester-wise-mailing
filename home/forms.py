from django import forms
from tinymce.widgets import TinyMCE
from .models import Mailing, Batch

class MailingForm(forms.ModelForm):
    batches = forms.ModelMultipleChoiceField(
        queryset=Batch.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'aria-label': 'Multiple select example', 'size': '5', 'required': 'required'}),
        required=True,
    )

    class Meta:
        model = Mailing
        fields = ['batches', 'subject', 'message','tracking']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject', 'required': 'required'}),
            'message': TinyMCE(attrs={'cols': 50, 'rows': 10 }),
            'tracking': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'tracking'}),  
        }
