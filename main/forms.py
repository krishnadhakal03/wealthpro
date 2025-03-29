from django import forms
from django.core.validators import RegexValidator
from main.models import Appointment

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control'}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Your Phone Number', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Address', 'class': 'form-control', 'rows': 3}))
    addressline2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Your Address Line 2', 'class': 'form-control'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}))
    zipcode = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Zip Code', 'class': 'form-control'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Country', 'class': 'form-control'}))
    reason = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Reason for Contact', 'class': 'form-control', 'rows': 4}))


class AppointmentForm(forms.Form):
    name = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Name', 
            'class': 'form-control'
        })
    )
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = forms.CharField(
        validators=[phone_regex], 
        max_length=20, 
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Phone Number', 
            'class': 'form-control'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your Email',
            'class': 'form-control'
        })
    )
    
    address = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Address',
            'class': 'form-control'
        })
    )
    
    addressline2 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Address Line 2 (optional)',
            'class': 'form-control'
        })
    )
    
    city = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'City',
            'class': 'form-control'
        })
    )
    
    zipcode = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Zip Code',
            'class': 'form-control'
        })
    )
    
    # Use choices from the model
    state = forms.ChoiceField(
        choices=Appointment.STATE_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    country = forms.CharField(
        initial='US',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Country',
            'class': 'form-control'
        })
    )
    
    appointment = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'placeholder': 'YYYY-MM-DD',
            'class': 'form-control'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        
        # Add any cross-field validation here if needed
        # For example, validate appointment date is not in the past
        
        return cleaned_data


