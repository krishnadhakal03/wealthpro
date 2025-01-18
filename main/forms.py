from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Your Phone Number'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Address'}))
    reason = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Reason for Contact'}))

