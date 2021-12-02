from django.shortcuts import render, redirect
from backend.models import Client, Property, Order, Tenant, TenantOrder
from backend.forms import UpdateClient, UpdateTenantOrder
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from backend.decorators import allowed_users, unauthenticated_user, client_only


# Create your views here.

@login_required(login_url='login')
@client_only
@allowed_users(allowed_roles=['client'])
def home(request):
    client = Client.objects.get(username=request.user)
    orders = client.client.all()
    count = orders.count()


    date = client.date_created.now()

    context = {
        'client': client,
        'orders': orders,
        'count': count,
        'date': date
    }

    return render(request, 'client/index.html', context)


@login_required(login_url='login')
@client_only
@allowed_users(allowed_roles=['client'])
def paymentHistory(request):
    client = Client.objects.get(username=request.user)
    orders = client.client.all()

    context = {
        'client': client,
        'orders': orders,
    }

    return render(request, 'client/payment.html', context)


@unauthenticated_user
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if request.user.groups.all()[0].name == "client":
                    return redirect('home')
                elif request.user.groups.all()[0].name == "staff":
                    return redirect('dashboard')
                else:
                    return redirect('manager_home')
            else:
                messages.info(request, 'Username OR Password is incorrect')

        return render(request, 'user/front_login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@client_only
@allowed_users(allowed_roles=['client'])
def clientProfile(request):
    client = request.user.client
    staff = request.user.client.staff
    form = UpdateClient(instance=client)

    if request.method == 'POST':
        form = UpdateClient(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
        return redirect('home')

    context = {
        'form': form,
        'staff': staff
    }
    return render(request, 'client/user_profile.html', context)


@login_required(login_url='login')
@client_only
@allowed_users(allowed_roles=['client'])
def Tenants(request):
    client = Client.objects.get(username=request.user)
    tenants = TenantOrder.objects.all()


    context = {
        'client': client,
        'tenants': tenants,
    }

    return render(request, "client/tenants.html", context)

@login_required(login_url='login')
@client_only
@allowed_users(allowed_roles=['client'])
def TenantUpdate(req, pk):
    order = TenantOrder.objects.get(id=pk)
    form = UpdateTenantOrder(instance=order)
    if req.method == "POST":
        form = UpdateTenantOrder(req.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form,
        'order': order,
    }

    return render(req, "client/tenants_update.html", context)
