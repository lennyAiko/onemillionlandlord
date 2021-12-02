import django_filters
from .models import Order, Property, Client
from django_filters import DateFilter, CharFilter, NumberFilter
from django import forms


class OrderFilter(django_filters.FilterSet):
    lease_period = CharFilter(field_name="lease_period", lookup_expr="icontains",
                              widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Lease Period',
                                                            'style': 'width:15%; margin:3px'}))

    balance = NumberFilter(field_name="balance", lookup_expr="icontains",
                           widget=forms.NumberInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Balance',
                                                           'style': 'width:15%; margin:3px'}))

    class Meta:
        model = Order
        fields = ('client', 'property', 'balance', 'lease_period')


class PropertyFilter(django_filters.FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains",
                      widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Name',
                                                    'style': 'width:15%; margin:3px'})
                      )
    location = CharFilter(field_name="location", lookup_expr="icontains",
                          widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Location',
                                                        'style': 'width:15%; margin:3px'})
                          )
    amount = NumberFilter(
        field_name="amount", lookup_expr="icontains",
        widget=forms.NumberInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Location',
                                        'style': 'width:15%; margin:3px'})
    )

    class Meta:
        model = Property
        fields = '__all__'
        exclude = ['date_created', 'property_image']


class ClientFilter(django_filters.FilterSet):
    username = CharFilter(field_name="username", lookup_expr="icontains",
                          widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Username',
                                                        'style': 'width:15%; margin:3px'})
                          )
    last_name = CharFilter(field_name="last_name", lookup_expr="icontains",
                           widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Last name',
                                                         'style': 'width:15%; margin:3px'})
                           )
    first_name = CharFilter(field_name="first_name", lookup_expr="icontains",
                            widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'First name',
                                                          'style': 'width:15%; margin:3px'})
                            )

    class Meta:
        model = Client
        fields = ['username', 'first_name', 'last_name']


class ProfileFilter(django_filters.FilterSet):
    lease_period = CharFilter(field_name="lease_period", lookup_expr="icontains",
                              widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Lease Period',
                                                            'style': 'width:30%; margin:5px'}))

    balance = NumberFilter(field_name="balance", lookup_expr="icontains",
                           widget=forms.NumberInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Balance',
                                                           'style': 'width:30%; margin:5px'}))

    class Meta:
        model = Order
        fields = ('balance', 'lease_period')
