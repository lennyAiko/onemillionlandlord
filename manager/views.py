from django.shortcuts import render, redirect
from backend.models import Client, Staff, Order, Property
from django.contrib.auth.decorators import login_required
from backend.decorators import allowed_users

# Create your views here.

@allowed_users(allowed_roles=['manager'])
@login_required(login_url='login')
def dashboard(request):

    staffs = Staff.objects.all()
    totalStaff = staffs.count()

    clients = Client.objects.all()
    totalClient = clients.count()

    orders = Order.objects.all()
    totalOrders = orders.count()

    props = Property.objects.all()
    totalProps = props.count()

    staffNum = 0
    for i in staffs:
        staff = i.client.all()
        num = staff.count()
        if num > staffNum:
            staffNum = num
            topStaff = i

    totalAmount = 0.0
    num = 0
    digits = []
    for i in clients:
        for x in i.client.all():
            num = x.amount_paid
            digits.append(num)
        if totalAmount < sum(digits):
            totalAmount = sum(digits)
            topClient = i
            print("amount", topClient)
        digits = []




    countProp = 0
    for i in props:
        prop = i.property.all()
        propsTotal = prop.count()
        if propsTotal > countProp:
            countProp = propsTotal
            topProp = i


    context = {
        'totalStaff': totalStaff,
        'totalClient': totalClient,
        'totalOrders': totalOrders,
        'totalProps': totalProps,
        'topStaff': topStaff,
        'staffNum': staffNum,
        'totalAmount': totalAmount,
        'topClient': topClient,
        'countProp': countProp,
        'topProp': topProp,
    }

    return render(request, "manage/dashboard.html", context)


@allowed_users(allowed_roles=['manager'])
@login_required(login_url='login')
def staff(request):
    staffs = Staff.objects.all()


    context = {
        'staffs': staffs,
    }

    return render(request, "manage/staff.html", context)


@allowed_users(allowed_roles=['manager'])
@login_required(login_url='login')
def prop(request):
    props = Property.objects.all()

    context = {
        'props': props,
    }

    return render(request, "manage/prop.html", context)
