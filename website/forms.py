from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserInformation, Doctor, Patient

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    phone_number = forms.IntegerField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    address = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    city = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    state = forms.CharField(label="", max_length=2, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
    zipcode = forms.IntegerField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'city', 'state', 'zipcode', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'User Name'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

class AddUserInformationForm(forms.ModelForm):
    class Meta:
        model = UserInformation
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'zipcode']
        widgets = {
            'first_name': forms.TextInput(attrs={"placeholder": "First Name", "class": "form-control"}),
            'last_name': forms.TextInput(attrs={"placeholder": "Last Name", "class": "form-control"}),
            'email': forms.TextInput(attrs={"placeholder": "Email", "class": "form-control"}),
            'phone': forms.TextInput(attrs={"placeholder": "Phone", "class": "form-control"}),
            'address': forms.TextInput(attrs={"placeholder": "Address", "class": "form-control"}),
            'city': forms.TextInput(attrs={"placeholder": "City", "class": "form-control"}),
            'state': forms.TextInput(attrs={"placeholder": "State", "class": "form-control"}),
            'zipcode': forms.TextInput(attrs={"placeholder": "Zipcode", "class": "form-control"}),
        }

class RecommendationForm(forms.Form):
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}))
    symptoms = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your symptoms'}))
    medical_conditions = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'List any known medical conditions'}))
    exercise = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your weekly exercise routine'}))
