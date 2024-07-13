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
        fields = ['batches', 'subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': TinyMCE(attrs={'cols': 80, 'rows': 30}),  # Adjust cols and rows as needed
        }
