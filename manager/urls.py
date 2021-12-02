from django.urls import path
from .views import *


urlpatterns = [
    path('', dashboard, name="manager_home"),
    path('staff/', staff, name="staff"),
    path('prop/', prop, name="prop"),
]
