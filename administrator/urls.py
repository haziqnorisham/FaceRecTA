from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='administrator_home'),
    path('registration/', views.registration, name='registration'),
    path('Sync/', views.sync, name='Sync'),
]
