from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('logout_staff/', views.logoutStaff, name='logout_staff'),
    path('register_staff_admin/', views.registerStaff, name='register'),

    path('staff_profile', views.staffProfile, name='staff_profile'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('tenant_profile/<str:pk>', views.tenant_profile, name='tenant_profile'),

    path('register_client/', views.registerClient, name='register_client'),
    path('register_tenant/<str:pk>/',
         views.registerTenant, name='register_tenant'),
    path('register_property/', views.registerProperty, name='register_property'),

    path('make_order/<str:pk>', views.makeOrder, name='make_order'),

    path('done/', views.done, name='done'),

    path('edit_client/', views.editClient, name='edit_client'),
    path('edit_property/', views.editProperty, name='edit_property'),
    path('edit_order/', views.editOrder, name='edit_order'),

    path('send_invoice/', views.sendInvoice, name='send_invoice'),
    path('send_email/', views.sendEmail, name='send_email'),

    path('update_client/<str:pk>/', views.updateClient, name='update_client'),
    path('update_property/<str:pk>/',
         views.updateProperty, name='update_property'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('update_tenant/<str:pk>/', views.updateTenant, name='update_tenant'),
    path('update_tenant_order/<str:pk>/', views.updateTenantOrder, name='update_tenant_order'),

    path('delete_client/<str:pk>/', views.deleteClient, name='delete_client'),
    path('delete_property/<str:pk>/',
         views.deleteProperty, name='delete_property'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),
]
