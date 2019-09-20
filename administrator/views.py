from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def home(requests):
    return render(requests, "administrator/administrator_home.html")

@login_required
@user_passes_test(lambda u: u.is_superuser)
def registration(requests):

    registered = {"registered" : False}
    if requests.method == 'POST':

        data = requests.POST.copy()

        print("username = " + data.get('username'))
        print("email = " + data.get('email'))
        print("passsword = " + data.get('password'))

        user = User.objects.create_user(data.get('username'), password=data.get('password'))
        user.is_staff=True
        user.email = data.get('email')

        if(data.get('is_superuser') == "on"):
            print("admin : True")
            user.is_superuser=True
        else:
            print("admin : False")
            user.is_superuser=False

        user.save()
        registered["registered"] = True
        messages.success(requests, 'User Registered')

    context = {"registered" : registered}

    return render(requests, "administrator/registration.html", context)
