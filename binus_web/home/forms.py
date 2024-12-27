from django.forms import ModelForm
from django import forms

from .models import BookSeat,Contact,Tutorial



class BookingForm(ModelForm):
    # Using ModelChoiceField to dynamically load the options from Tutorial model
    subject = forms.ModelChoiceField(
        queryset=Tutorial.objects.all(),  # Fetch all tutorials from the database
        widget=forms.Select(attrs={'class': 'custom-select border-0 px-4', 'style': 'height: 47px'}),
        empty_label='Select A Class',  # Optional: A default placeholder option
    )

    class Meta:
        model = BookSeat
        fields = ['name', 'email', 'phone_number','place', 'subject']

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 characters long.")
        return name

    
class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phonenumber', 'subject', 'message']

    def clean_name(self):
        
        name = self.cleaned_data.get('name')

        if len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 characters long.")
        return name
    def clean_phonenumber(self):
        phonenumber = self.cleaned_data.get('phonenumber')
        if not phonenumber.isdigit() or len(phonenumber) != 10:
            raise forms.ValidationError("Phone number must be a valid 10-digit number.")
        return phonenumber

    