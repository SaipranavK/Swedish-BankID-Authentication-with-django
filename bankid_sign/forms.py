from django import forms
from django.forms import ValidationError

class MobileAuthForm(forms.Form):
    pnr = forms.CharField(max_length = 12, 
    help_text="Enter your Personal Number without whitespaces or hyphen('-')", 
    widget=forms.TextInput(attrs={'placeholder': 'yyyymmddnnnn'}), 
    label = '',
    required = True
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        pnr = cleaned_data.get('pnr', None)

        if len(pnr) < 12:
            raise forms.ValidationError("Please enter your correct Personal Number")

        if '-' in pnr or " " in pnr:
            raise forms.ValidationError("Please remove whitespaces and hyphens('-') in your Personal Number input")
