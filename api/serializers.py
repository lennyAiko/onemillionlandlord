from rest_framework import serializers
from backend.models import Staff, Client, Tenant, Property, Order, TenantOrder, User
from django.conf import settings
from django.contrib.auth.hashers import make_password


class PropertySerializer(serializers.ModelSerializer):
    property_image = serializers.ImageField(default="default.png")

    class Meta:
        model = Property
        exclude = ["registered_by"]
        extra_kwargs = {
            "property_image": {"required": False},
            "Completion_date": {"required": False},
        }


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
        ]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ["client", "date_created"]
