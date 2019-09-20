from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def home(requests):
    return render(requests, "administrator/administrator_home.html")

@login_required
@user_passes_test(lambda u: u.is_superuser)
def registration(requests):
    return render(requests, "administrator/registration.html")
