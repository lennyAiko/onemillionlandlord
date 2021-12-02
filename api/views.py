from django.shortcuts import render
from rest_framework import generics, permissions
from backend.models import Staff, Client, Tenant, Property, Order, TenantOrder
from .serializers import PropertySerializer, ClientSerializer
from django.contrib.auth.models import Group
from backend.emails import mail

# Create your views here.


class AdminOnly(permissions.BasePermission):
    note = "Access Denied"

    def has_permission(self, request, view):
        group = request.user.groups.all()[0].name
        if group == "client" or group == "tenant":
            return note


class PropertyList(generics.ListCreateAPIView):
    """
    Get the list of properties.
    """

    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated | AdminOnly]

    def get_queryset(self):
        queryset = Property.objects.filter(registered_by=self.request.user.username)
        return queryset

    def perform_create(self, serializer):
        serializer.save(registered_by=self.request.user.username)


class PropertyDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Perform a RUD operation on a property.
    """

    permission_classes = [permissions.IsAuthenticated | AdminOnly]
    serializer_class = PropertySerializer

    def get_queryset(self):
        queryset = Property.objects.filter(registered_by=self.request.user.username)
        return queryset


class ClientList(generics.ListAPIView):
    """
    Get the list of clients.
    """

    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated | AdminOnly]

    def get_queryset(self):
        queryset = Client.objects.filter(staff=self.request.user.staff)
        return queryset


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Perform a RUD operation on a client.
    """

    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated | AdminOnly]

    def get_queryset(self):
        queryset = Client.objects.filter(staff=self.request.user.staff)
        return queryset


class OrderList(generics.ListAPIView):
    """
    View orders
    """

    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated | AdminOnly]

    # def get_queryset(self):
