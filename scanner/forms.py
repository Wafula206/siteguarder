from django import forms

class ScanForm(forms.Form):
    url = forms.URLField(label='Website URL', widget=forms.URLInput(attrs={'placeholder': 'https://example.com'}))