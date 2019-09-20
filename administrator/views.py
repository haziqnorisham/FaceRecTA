from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(requests):
    return render(requests, "administrator/administrator_home.html")
