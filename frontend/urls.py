from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('payment_history/', views.paymentHistory, name='payment_history'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name="logout"),

    path('user_profile', views.clientProfile, name='user_profile'),

    path('tenants', views.Tenants, name='tenants'),
    path('tenants_update/<str:pk>', views.TenantUpdate, name='tenants_update'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="user/password_reset.html"), name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="user/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="user/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="user/password_reset_done.html"), name="password_reset_complete"),
]
