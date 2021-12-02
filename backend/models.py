from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

to_set_year = datetime.datetime.now() - datetime.timedelta(days=3*365)


class Staff(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE, related_name="staff")
    username = models.CharField(
        max_length=60, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    profile_pic = models.ImageField(null=True, default="default.png")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.username}"

    class Meta:
        ordering = ['-date_created']

    def total(self):
        i = self.client.all()
        total = len(i)
        return total


class Client(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    staff = models.ForeignKey(
        Staff, null=True, on_delete=models.SET_NULL, related_name="client")
    username = models.CharField(
        max_length=60, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    profile_pic = models.ImageField(null=True, default="default.png")
    registered_by = models.CharField(null=True, blank=True, max_length=60)
    reffered_by = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.username}"

    class Meta:
        ordering = ['-date_created']


class Tenant(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    client = models.ForeignKey(
        Client, null=True, on_delete=models.SET_NULL, related_name="tenant")
    username = models.CharField(
        max_length=60, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    profile_pic = models.ImageField(null=True, default="default.png")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.username}"

    class Meta:
        ordering = ['-date_created']


class Property(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)
    amount = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=2)
    registered_by = models.CharField(null=True, blank=True, max_length=60)
    property_image = models.ImageField(null=True, default="default.png")
    completion_date = models.DateTimeField(
        auto_now=False, null=True, default=to_set_year)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.amount} - {self.location}"

    class Meta:
        ordering = ['-date_created']
        verbose_name = "Property"
        verbose_name_plural = "Properties"


class Order(models.Model):
    TYPE = (
        ("Yes", "Yes"),
        ("No", "No"),
    )
    client = models.ForeignKey(
        Client, null=True, on_delete=models.CASCADE, related_name="client")
    property = models.ForeignKey(
        Property, null=True, on_delete=models.CASCADE, related_name="property")
    rent = models.CharField(choices=TYPE, null=True,
                            default="No", max_length=4)
    amount_paid = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=2)
    lease_period = models.IntegerField(blank=True, null=True)
    status1 = models.ImageField(null=True, blank=True, default="white.jpg")
    status2 = models.ImageField(null=True, blank=True, default="white.jpg")
    status3 = models.ImageField(null=True, blank=True, default="white.jpg")
    date_created = models.DateTimeField(auto_now_add=False, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.property.name} - {self.client.username}"

    class Meta:
        ordering = ['date_created']

    def balance(self):
        num1 = float(self.property.amount)
        num2 = float(self.amount_paid)
        value = num1 - num2
        return float(value)

    def date(self):
        data = self.date_created
        year = self.date_created.year + self.lease_period
        date_expiry = data.replace(year=year)
        return date_expiry


class TenantOrder(models.Model):
    tenant = models.ForeignKey(
        Tenant, null=True, on_delete=models.CASCADE, related_name="tenantOrder")
    tenant_property = models.ForeignKey(
        Property, null=True, on_delete=models.CASCADE, related_name="tenantProperty")
    amount_paid = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=2)
    lease_period = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=False, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.tenant_property.name}"

    class Meta:
        ordering = ['date_created']

    def balance(self):
        num1 = float(self.tenant_property.amount)
        num2 = float(self.amount_paid)
        value = num1 - num2
        return float(value)

    def date(self):
        data = self.date_created
        year = self.date_created.year + self.lease_period
        date_expiry = data.replace(year=year)
        return date_expiry
