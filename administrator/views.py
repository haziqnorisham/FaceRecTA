import os
import json
import base64
import requests as requests_import
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from requests.auth import HTTPBasicAuth
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from timeAttendance.models import EmployeeDetail
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

@login_required
@user_passes_test(lambda u: u.is_superuser)
def sync(requests):
    encoded_string = None
    all_employee = EmployeeDetail.objects.all()
    for employee in all_employee:
        print(employee)

        image_name = employee.img_name
        with open("static/"+image_name, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            print(type(encoded_string))
        picjson = "data:image/jpeg;base64,"+encoded_string.decode("utf-8")
        a = None

        #username = this.username
        #username = request.POST.get("username")
        #password = request.POST.get("password")

        #url = "http://192.168.0.33/action/GetSysParam"
        url = "http://"+"192.168.0.33"+"/action/AddPerson"

        headers = {
            'Content-Type': "application/json",
            'User-Agent': "PostmanRuntime/7.16.3",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Postman-Token': "299fa413-9e09-4776-ab1d-5dae8c1ad2e7,95df307a-1643-4b35-b8fd-db3ed2e78a60",
            'Host': "192.168.0.33",
            'Accept-Encoding': "gzip, deflate",
            'Content-Length': "",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
            }

        body = {
                "operator": "AddPerson",
                "info": {
                    "DeviceID":1306861,
                    "IdType":0,
                    "PersonType": 0,
                    "Name":str(employee.name),
                    "Gender":employee.Gender,
                    "CardType":0,
                    "IdCard":str(employee.employee_id),
                    "CustomizeID":employee.employee_id,
                    "Native": "Johor",
                    "Tempvalid": 0,
                    " ChannelAuthority0":"1",
                    " ChannelAuthority1":"1",
                    " ChannelAuthority2":"1",
                    " ChannelAuthority3":"1"
                  },
                	"picinfo": picjson
                }

        #response = requests.request("POST", url, headers=headers, auth=HTTPBasicAuth('admin', 'admin'))

        response = requests_import.request("POST", url, headers=headers, auth=HTTPBasicAuth("admin", "admin"), json=body)

        json_data = response.text
        data = json.loads(json_data)
        a = data['info']
        response_data = {}
        response_data['info'] = a



    #return HttpResponse("<h1>Synching Done</h1>")
    return HttpResponse("Added All Person From Database")

@login_required
@user_passes_test(lambda u: u.is_superuser)
def employee_add(requests):

    registered = {"registered" : False}

    if requests.method == 'POST':
        data = requests.POST.copy()
        emp = EmployeeDetail()
        emp.name = data.get("Name")
        emp.employee_id = int(data.get("Employee_ID"))
        if (data.get("Employee") == "male"):
            emp.Gender = 0
        else:
            emp.Gender = 1
        emp.img_name = data.get("img_name")
        emp.CustomizeID = 1

        emp.save()
        registered["registered"] = True
        messages.success(requests, 'User Registered')

    temp_list = []

    files = os.listdir("static")
    for file in files:
        temp_list.append({"name" : str(file)})

    temp_list.reverse()

    context= {
        'image': temp_list,
        "registered" : registered
        }

    return render(requests, "administrator/employee_add.html", context)
