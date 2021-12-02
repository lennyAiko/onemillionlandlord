from django.forms import ModelForm
from django import forms
from .models import Client, Order, Property, Staff, TenantOrder, Tenant
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterClient(UserCreationForm):
    password1 = forms.CharField(label='Enter password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2',]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
        }


class RegisterStaff(UserCreationForm):
    password1 = forms.CharField(label='Enter password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
        }


class RegisterProperty(forms.ModelForm):
    completion_date = forms.DateTimeField(widget=forms.SelectDateWidget)

    class Meta:
        model = Property
        fields = '__all__'
        exclude = ['registered_by', ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of property'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location of property'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
        }


YEARS = [x for x in range(2015, 2030)]


class MakeOrder(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['client', 'date_created', ]

        widgets = {
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount paid'}),
            'lease_period': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Lease period'}),
        }


class TenantOrderForm(ModelForm):
    class Meta:
        model = TenantOrder
        fields = '__all__'
        exclude = ['tenant', 'date_created']

        widgets = {
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount paid'}),
            'lease_period': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Lease period'}),
        }


class UpdateClient(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ('registered_by', 'username',
                   'user', 'staff', 'reffered_by',)

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'reffered_by': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Reffered by'}),
        }


class UpdateTenant(ModelForm):
    class Meta:
        model = Tenant
        fields = '__all__'
        exclude = ('client', 'user',)

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'reffered_by': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Reffered by'}),
        }


class UpdateStaff(ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'
        exclude = ('user', 'username',)

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
        }


class UpdateProperty(ModelForm):
    completion_date = forms.DateTimeField(widget=forms.SelectDateWidget)

    class Meta:
        model = Property
        fields = '__all__'
        exclude = ['registered_by', ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of property'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location of property'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
        }


class UpdateOrder(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['client', ]

        widgets = {
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount paid'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Balance'}),
            'lease_period': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Lease period'}),
        }



class UpdateTenantOrder(ModelForm):
    class Meta:
        model = TenantOrder
        fields = '__all__'
        exclude = ['tenant', 'date_created', ]

        widgets = {
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount paid'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Balance'}),
            'lease_period': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Lease period'}),
        }


class SendEmail(forms.Form):
    email = forms.EmailField(label='Enter email',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    subject = forms.CharField(label='Enter Subject',
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control', 'placeholder': 'Enter subject'})
                              )
    message = forms.CharField(label='Enter message',
                              widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter message'}))

    class Meta:
        fields = ['email', 'subject', 'message', ]


class SendInvoice(forms.Form):
    email = forms.EmailField(label='Enter email',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    subject = forms.CharField(label='Enter Subject',
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control', 'placeholder': 'Enter subject'})
                              )
    image = forms.ImageField()

    class Meta:
        fields = ['email', 'subject', 'image', ]