from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Your Phone Number'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Address'}))
    addressline2 = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Address Line 2'}))
    city = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'City'}))
    zipcode = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Zip Code'}))
    state = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'State'}))
    country = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Country'}))
    reason = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Reason for Contact'}))


class AppointmentForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Your Phone Number'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Address'}))
    addressline2 = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Address Line 2'}))
    city = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'City'}))
    zipcode = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Zip Code'}))
    state = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'State'}))
    country = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Country'}))
    appointment = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'Date of Appointment'}))


