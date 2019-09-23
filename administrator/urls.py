from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='administrator_home'),
    path('registration/', views.registration, name='registration'),
    path('Sync/', views.sync, name='Sync'),
    path('employee_add/', views.employee_add, name='employee_add'),
    path('add_device/', views.add_device, name='add_device'),
]
