from email.mime.image import MIMEImage
from django.shortcuts import render, redirect, get_object_or_404
from .forms import (UpdateTenant, RegisterClient, RegisterProperty,
UpdateProperty, UpdateOrder, UpdateClient, RegisterStaff, UpdateStaff,
SendEmail, SendInvoice, MakeOrder, TenantOrderForm, UpdateTenantOrder)
from django.forms import inlineformset_factory
from .filters import ClientFilter, PropertyFilter, OrderFilter, ProfileFilter
from django.core.paginator import Paginator
from .models import Client, Property, Order, Staff, Tenant, TenantOrder
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from onemillionlandlord.settings import EMAIL_HOST_USER, DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from .emails import mail



# Create your views here.

@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def dashboard(req):
    staff = Staff.objects.get(user=req.user)
    client = staff.client.all()
    prop = Property.objects.all()

    order = []
    for i in client:
        check = Order.objects.filter(client=i)
        for x in check:
            order.append(x)

    total_order = len(order)
    total_client = client.count()
    total_prop = prop.count()

    context = {
        'total_order': total_order,
        'total_client': total_client,
        'total_prop': total_prop,
    }
    return render(req, 'staff/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def done(req):
    return render(req, 'reg/done.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def registerClient(req):
    clients = Client.objects.all()
    form = RegisterClient()
    message = None
    if req.method == 'POST':
        form = RegisterClient(req.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            reffered_by = req.POST.get('reffered')
            staff = req.user

            store = Client(
                user=user,
                staff=req.user.staff,
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                registered_by=staff,
                reffered_by=reffered_by,
            )
            store.save()
            group = Group.objects.get(name='client')
            user.groups.add(group)
            mail(email, username, password)
            return redirect('done')

    context = {'form': form}
    return render(req, 'reg/register_client.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def registerTenant(req, pk):
    form = RegisterClient()
    if req.method == 'POST':
        form = RegisterClient(req.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            client = Client.objects.get(id=pk)

            store = Tenant(
                user=user,
                client=client,
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            store.save()
            group = Group.objects.get(name='tenant')
            user.groups.add(group)
            mail(email, username, password)
            return redirect('done')

    context = {'form': form}
    return render(req, 'reg/register_tenant.html', context)


def registerStaff(req):
    form = RegisterStaff()
    if req.method == 'POST':
        form = RegisterStaff(req.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            group = Group.objects.get(name='staff')
            user.groups.add(group)
            Staff.objects.create(
                user=user,
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            mail(email, username, password)
        return redirect('login')

    context = {'form': form}
    return render(req, 'register_staff.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def registerProperty(req):
    form = RegisterProperty()
    if req.method == 'POST':
        form = RegisterProperty(req.POST)
        if form.is_valid():
            data = form.cleaned_data
            register = req.user.username
            store = Property(registered_by=register, **data)
            store.save()
            return redirect('done')

    context = {'form': form}
    return render(req, 'reg/register_property.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def makeOrder(req, pk):
    form = MakeOrder()
    if req.method == 'POST':
        form = MakeOrder(req.POST)
        if form.is_valid():
            client = Client.objects.get(id=pk)
            theProperty = form.cleaned_data.get('property')
            rent = form.cleaned_data.get('rent')
            amount_paid = form.cleaned_data.get('amount_paid')
            lease_period = form.cleaned_data.get('lease_period')
            status1 = form.cleaned_data.get('status1')
            status2 = form.cleaned_data.get('status2')
            status3 = form.cleaned_data.get('status3')
            date_created = req.POST.get('ordertime')
            Order.objects.create(
                client=client,
                property=theProperty,
                rent=rent,
                amount_paid=amount_paid,
                lease_period=lease_period,
                status1=status1,
                status2=status2,
                status3=status3,
                date_created=date_created,
            )
            return redirect('done')

    context = {'form': form}
    return render(req, 'reg/make_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def editClient(req):
    clients = Client.objects.all()
    myFilter = ClientFilter(req.GET, queryset=clients)
    clients = myFilter.qs
    paginator = Paginator(clients, 6)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'clients': clients,
        'myFilter': myFilter,
        'page_obj': page_obj,
    }

    return render(req, 'edit/edit_client.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def editProperty(req):
    properties = Property.objects.all()
    myFilter = PropertyFilter(req.GET, queryset=properties)
    properties = myFilter.qs
    paginator = Paginator(properties, 6)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'properties': properties,
        'myFilter': myFilter,
        'page_obj': page_obj,
    }

    return render(req, 'edit/edit_property.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def editOrder(req):
    orders = Order.objects.all()
    myFilter = OrderFilter(req.GET, queryset=orders)
    orders = myFilter.qs
    paginator = Paginator(orders, 6)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'orders': orders,
        'myFilter': myFilter,
        'page_obj': page_obj,
    }

    return render(req, 'edit/edit_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def sendInvoice(req):
    form = SendInvoice()
    if req.method == "POST":
        form = SendInvoice(req.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            image = form.cleaned_data.get('image')
            with mail.get_connection() as connection:
                for _ in req.FILES.getlist("image"):
                    image.open('rb')
                    try:
                        img_data = image.read()
                        msg_img = MIMEImage(img_data)
                    finally:
                        image.close()
                mail.EmailMessage(
                    subject, msg_img, DEFAULT_FROM_EMAIL, [email],
                    connection=connection,
                ).send()
        return redirect('done')
    context = {'form': form}
    return render(req, 'send/invoice.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def sendEmail(req):
    form = SendEmail()
    if req.method == "POST":
        form = SendEmail(req.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            send_mail(subject, message, DEFAULT_FROM_EMAIL,
                      [email], fail_silently=False)
            return redirect('done')
    context = {'form': form}
    return render(req, 'send/email.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def updateClient(req, pk):
    client = Client.objects.get(id=pk)
    form = UpdateClient(instance=client)

    if req.method == 'POST':
        form = UpdateClient(req.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('edit_client')

    context = {
        'form': form
    }
    return render(req, 'buttons/update_client.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def updateProperty(req, pk):
    prop = Property.objects.get(id=pk)
    form = UpdateProperty(instance=prop)

    if req.method == 'POST':
        form = UpdateProperty(req.POST, instance=prop)
        if form.is_valid():
            form.save()
            return redirect('edit_property')

    context = {
        'form': form
    }
    return render(req, 'buttons/update_property.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def updateOrder(req, pk):
    order = Order.objects.get(id=pk)
    form = UpdateOrder(instance=order)

    if req.method == 'POST':
        form = UpdateOrder(req.POST, req.FILES, instance=order)
        if form.is_valid():
            form.save()
            return redirect('edit_order')

    context = {
        'form': form
    }
    return render(req, 'buttons/update_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def deleteOrder(req, pk):
    order = Order.objects.get(id=pk)
    if req.method == "POST":
        order.delete()
        return redirect('edit_order')
    context = {'item': order}
    return render(req, 'buttons/delete_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def deleteClient(req, pk):
    client = Client.objects.get(id=pk)
    if req.method == "POST":
        client.delete()
        return redirect('edit_client')
    context = {'item': client}
    return render(req, 'buttons/delete_client.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def deleteProperty(req, pk):
    prop = Property.objects.get(id=pk)
    if req.method == "POST":
        prop.delete()
        return redirect('edit_property')
    context = {'item': prop}
    return render(req, 'buttons/delete_property.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def profile(req, pk):
    client = Client.objects.get(id=pk)
    orders = client.client.all()
    order_count = orders.count()
    myFilter = ProfileFilter(req.GET, queryset=orders)
    orders = myFilter.qs
    tenants = client.tenant.all()

    context = {
        'client': client,
        'orders': orders,
        'order_count': order_count,
        'myFilter': myFilter,
        'tenants': tenants,
    }
    return render(req, 'staff/profile.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def tenant_profile(req, pk):
    tenant = Tenant.objects.get(id=pk)
    form = TenantOrderForm()
    order = TenantOrder.objects.all().filter(tenant=tenant)
    amount = order.count()

    if req.method == "POST":
        form = TenantOrderForm(req.POST)
        if form.is_valid():
            thetenant = Tenant.objects.get(id=pk)
            theproperty = form.cleaned_data.get('tenant_property')
            amount_paid = form.cleaned_data.get('amount_paid')
            lease_period = form.cleaned_data.get('lease_period')
            date_created = req.POST.get('ordertime')
            store = TenantOrder(
                tenant=thetenant,
                tenant_property=theproperty,
                amount_paid=amount_paid,
                lease_period=lease_period,
                date_created=date_created,
            )
            store.save()
            return redirect('done')

    context = {
        'tenant': tenant,
        'form': form,
        'order': order,
        'amount': amount,
    }

    return render(req, "staff/tenant_profile.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def updateTenant(req, pk):
    tenant = Tenant.objects.get(id=pk)
    form = UpdateTenant(instance=tenant)

    if req.method == 'POST':
        form = UpdateTenant(req.POST, req.FILES, instance=tenant)
        if form.is_valid():
            form.save()
            return redirect('done')

    context = {
        'form': form,
        'tenant': tenant
    }
    return render(req, 'buttons/update_tenant.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def updateTenantOrder(req, pk):
    tenant_order = TenantOrder.objects.get(id=pk)
    form = UpdateTenantOrder(instance=tenant_order)

    if req.method == 'POST':
        form = UpdateTenantOrder(req.POST, req.FILES, instance=tenant_order)
        if form.is_valid():
            form.save()
            return redirect('done')
    context = {
        'form': form,
        'tenant_order': tenant_order
    }
    return render(req, 'buttons/update_tenant_order.html', context)


def logoutStaff(req):
    logout(req)
    return redirect('login')


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['staff'])
def staffProfile(req):
    staff = req.user.staff
    form = UpdateStaff(instance=staff)
    if req.method == 'POST':
        form = UpdateStaff(req.POST, req.FILES, instance=staff)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(req, 'staff/staff_profile.html', context)