import os
import json
import base64
import requests as requests_import
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from requests.auth import HTTPBasicAuth
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required, user_passes_test
from timeAttendance.models import EmployeeDetail, TerminalDetails, EmployeeAttendance

def get_all_employee_id():

    id_list = []
    terminal_details_list = TerminalDetails.objects.values_list('terminal_id', 'terminal_ip')

    for terminal_detail in terminal_details_list:

        if(terminal_detail[1] != "0.0.0.0"):

            url = "http://"+terminal_detail[1]+"/action/SearchPersonList"

            body = {
                    "operator": "SearchPersonList",
                    "info": {
                        "DeviceID": int(terminal_detail[0]),
                        "BeginTime":"2010-06-01T00:00:00",
                        "EndTime":"2050-06-19T23:59:59",
                        "RequestCount":1000,
                        "Gender":2,
                        "Age":"0-100",
                        "MjCardNo":0,
                        "Name":"",
                        "BeginNO":0,
                        "Picture": 0
                    }
                }

            headers = {
                        'Content-Type': "application/json",
                        'Authorization': "Basic YWRtaW46YWRtaW4=",
                        'User-Agent': "PostmanRuntime/7.17.1",
                        'Accept': "*/*",
                        'Cache-Control': "no-cache",
                        'Postman-Token': "246f59d4-ccb8-4bec-a3cd-3018a46a685e,1e6fcb78-072c-405c-936a-85c58d4d6960",
                        'Host': terminal_detail[1],
                        'Accept-Encoding': "gzip, deflate",
                        'Content-Length': "169",
                        'Connection': "keep-alive",
                        'cache-control': "no-cache"
                        }

            response = requests_import.request("POST", url, json=body, headers=headers)

            json_data = response.text
            data = json.loads(json_data)
            a = data['info']['List']
            for entry in a:
                #print (entry['IdCard'])
                id_list.append(entry['IdCard'])

    return id_list

@login_required
def home(requests):

    terminal_dict_list = []


    terminal_obj_list = TerminalDetails.objects.all()
    for index,terminal_obj in enumerate(terminal_obj_list):
        temp_model = model_to_dict(terminal_obj)
        temp_model["counter"] = index
        terminal_dict_list.append(temp_model)


    context= {
        "terminal_dict_list" : terminal_dict_list
        }

    return render(requests, "administrator/administrator_home.html", context)

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

    ip_address_list = []
    ip_address_list2 = []
    deviceID_list = []

    if requests.method == 'GET':
        data = requests.GET.copy()
        if "sync" in requests.GET.keys():
            try:
                #ip_address_list = data.get("ip_list").splitlines()
                print(requests.GET.keys())

                for key in requests.GET.keys():

                    print(str(data.get(key)) == "sync")
                    if (str(data.get(key)) == "sync"):
                        t=None
                    else:
                        print(data.get(key))
                        ip_address_list.append(data.get(key))

                for ip_address in ip_address_list:
                    a2 = None

                    #username = this.username
                    #username = request.POST.get("username")
                    #password = request.POST.get("password")

                    #url = "http://192.168.0.33/action/GetSysParam"
                    url = "http://"+ip_address+"/action/GetSysParam"

                    headers = {
                        'Content-Type': "application/json",
                        'User-Agent': "PostmanRuntime/7.16.3",
                        'Accept': "*/*",
                        'Cache-Control': "no-cache",
                        'Postman-Token': "299fa413-9e09-4776-ab1d-5dae8c1ad2e7,95df307a-1643-4b35-b8fd-db3ed2e78a60",
                        'Host': ip_address,
                        'Accept-Encoding': "gzip, deflate",
                        'Content-Length': "",
                        'Connection': "keep-alive",
                        'cache-control': "no-cache"
                        }

                    #response = requests.request("POST", url, headers=headers, auth=HTTPBasicAuth('admin', 'admin'))

                    response = requests_import.request("POST", url, headers=headers, auth=HTTPBasicAuth("admin", "admin"))

                    json_data = response.text
                    data = json.loads(json_data)
                    a2 = data['info']
                    response_data = {}
                    response_data['info'] = a2
                    print(a2["DeviceID"])
                    deviceID_list.append(a2["DeviceID"])

                    encoded_string = None
                    all_employee = EmployeeDetail.objects.all()
                    for employee in all_employee:
                        #print(employee)

                        image_name = employee.image_name
                        with open("static/"+image_name, "rb") as image_file:
                            encoded_string = base64.b64encode(image_file.read())
                            #print(type(encoded_string))
                        picjson = "data:image/jpeg;base64,"+encoded_string.decode("utf-8")
                        a = None

                        #username = this.username
                        #username = request.POST.get("username")
                        #password = request.POST.get("password")

                        #url = "http://192.168.0.33/action/GetSysParam"
                        url = "http://"+ip_address+"/action/AddPerson"

                        headers = {
                            'Content-Type': "application/json",
                            'User-Agent': "PostmanRuntime/7.16.3",
                            'Accept': "*/*",
                            'Cache-Control': "no-cache",
                            'Postman-Token': "299fa413-9e09-4776-ab1d-5dae8c1ad2e7,95df307a-1643-4b35-b8fd-db3ed2e78a60",
                            'Host': ip_address,
                            'Accept-Encoding': "gzip, deflate",
                            'Content-Length': "",
                            'Connection': "keep-alive",
                            'cache-control': "no-cache"
                            }

                        body = {
                                "operator": "AddPerson",
                                "info": {
                                    "DeviceID":int(a2["DeviceID"]),
                                    "IdType":0,
                                    "PersonType": 0,
                                    "Name":str(employee.name),
                                    "Gender":employee.gender,
                                    "CardType":0,
                                    "IdCard":str(employee.id),
                                    "CustomizeID":employee.id,
                                    "Native": "",
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
            except:
                return HttpResponse("ERROR Synching")

        else:
            print(requests.GET.keys())

            for key in requests.GET.keys():
                #print(data.get(key))
                ip_address_list2.append(data.get(key))

            for ip_address in ip_address_list2:
                try:
                    print(ip_address)
                    TerminalDetails.objects.get(terminal_ip=ip_address).delete()
                except:
                    pass


    #return HttpResponse("<h1>Synching Done</h1>")
    return render(requests, "administrator/sync.html")

@login_required
@user_passes_test(lambda u: u.is_superuser)
def employee_add(requests):

    registered = {"registered" : False}

    if requests.method == 'POST':
        data = requests.POST.copy()
        emp = EmployeeDetail()
        emp.name = data.get("Name")
        emp.id = int(data.get("Employee_ID"))
        if (data.get("Employee") == "male"):
            emp.gender = 0
        else:
            emp.gender = 1
        emp.image_name = data.get("img_name")
        emp.department = data.get("Department")
        emp.branch = data.get("Branch")
        emp.status = 0
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

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_device(requests):

    if requests.method == 'POST':
        data = requests.POST.copy()
        terminal_obj = TerminalDetails()
        terminal_obj.terminal_ip = data.get("ip_address")
        terminal_obj.terminal_name = data.get("device_name")

        ip_address = data.get("ip_address")

        try:
            a = None
            url = "http://"+ip_address+"/action/GetSysParam"
            server_url = "http://"+str(data.get("server_ip_address"))+":80"
            print(server_url)

            headers = {
                'Content-Type': "application/json",
                'User-Agent': "PostmanRuntime/7.16.3",
                'Accept': "*/*",
                'Cache-Control': "no-cache",
                'Postman-Token': "299fa413-9e09-4776-ab1d-5dae8c1ad2e7,95df307a-1643-4b35-b8fd-db3ed2e78a60",
                'Host': ip_address,
                'Accept-Encoding': "gzip, deflate",
                'Content-Length': "",
                'Connection': "keep-alive",
                'cache-control': "no-cache"
                }

            response = requests_import.request("POST", url, headers=headers, auth=HTTPBasicAuth("admin", "admin"))

            json_data = response.text
            data = json.loads(json_data)
            a = data['info']
            response_data = {}
            response_data['info'] = a
            print(a["DeviceID"])
            terminal_obj.terminal_id = int(a["DeviceID"])



            body2 = {
                    "operator": "Subscribe",
                    "info": {
                        "DeviceID": int(a["DeviceID"]),
                        "Num": 2,
                        "Topics":["Snap", "Verify"],
                        "SubscribeAddr":server_url,
                        "SubscribeUrl":{"Snap":"/Subscribe/Snap", "Verify":"/Subscribe/Verify", "HeartBeat":"/Subscribe/heartbeat"},
                        "Auth":"Basic",
                        "User": "admin",
                        "Pwd": "admin"
                        }
                    }

            headers2 = {
                'Content-Type': "application/json",
                'Authorization': "Basic YWRtaW46YWRtaW4=",
                'User-Agent': "PostmanRuntime/7.16.3",
                'Accept': "*/*",
                'Cache-Control': "no-cache",
                'Postman-Token': "60ee7fb9-57cd-48c0-9d83-388d78ce51ea,4e2240de-573c-49d0-a6e1-26b8fdc47c15",
                'Host': ip_address,
                'Accept-Encoding': "gzip, deflate",
                'Content-Length': "392",
                'Connection': "keep-alive",
                'cache-control': "no-cache"
                }

            url2 = "http://"+ip_address+"/action/Subscribe"
            requests_import.request("POST", url2, json=body2, headers=headers2)
            terminal_obj.save()
            messages.success(requests, 'Successfully Added Device')
        except:
            messages.error(requests, 'Failed Adding Device')

    return render(requests, "administrator/add_device.html")

@login_required
def employee_list(requests):

    if requests.method == 'POST':
        data = requests.POST.copy()
        print(data.get("employee_id"))

        temp_emp = EmployeeDetail.objects.get(id = data.get("employee_id"))
        temp_emp.status = 0
        temp_emp.delete()

        terminal_details_list = TerminalDetails.objects.values_list('terminal_id', 'terminal_ip')


        for terminal_detail in terminal_details_list:

            print()
            print(terminal_detail[1])
            print(terminal_detail[0])
            print()

            if(terminal_detail[1] != "0.0.0.0"):
                url = "http://"+terminal_detail[1]+"/action/DeletePerson"

                body = {
                        "operator": "DeletePerson",
                        "info": {
                            "DeviceID": int(terminal_detail[0]),
                            "TotalNum": 1,
                            "IdType": 0,
                            "CustomizeID": [int(data.get("employee_id"))],
                            }
                        }

                headers = {
                            'Content-Type': "application/json",
                            'Authorization': "Basic YWRtaW46YWRtaW4=",
                            'User-Agent': "PostmanRuntime/7.17.1",
                            'Accept': "*/*",
                            'Cache-Control': "no-cache",
                            'Postman-Token': "246f59d4-ccb8-4bec-a3cd-3018a46a685e,1e6fcb78-072c-405c-936a-85c58d4d6960",
                            'Host': terminal_detail[1],
                            'Accept-Encoding': "gzip, deflate",
                            'Content-Length': "169",
                            'Connection': "keep-alive",
                            'cache-control': "no-cache"
                            }

                response = requests_import.request("POST", url, json=body, headers=headers)

    employee_dict_list = []
    temp = "Female"

    employee_list = EmployeeDetail.objects.all()
    for employee in employee_list:



        if(employee.gender == "0"):
            temp = "Male"
        else:
            temp = "Female"

        employee_dict = {
                    "name": employee.name,
                    "employee_id": employee.id,
                    "gender": temp,
                    "img_name": employee.image_name,
                    "branch": employee.branch,
                    "department": employee.department
        }

        if(employee.status == 0):
            employee_dict_list.append(employee_dict)


    context={
        "employee_list": employee_dict_list
    }
    return render(requests, "administrator/employee_list.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def full_reset(requests):

    EmployeeDetail.objects.all().delete()
    EmployeeAttendance.objects.all().delete()

    terminal_details_list = TerminalDetails.objects.values_list('terminal_id', 'terminal_ip')
    for terminal_detail in terminal_details_list:

        print()
        print(terminal_detail[1])
        print(terminal_detail[0])
        print()

        if(terminal_detail[1] != "0.0.0.0"):
            for emp_num in get_all_employee_id():
                url = "http://"+terminal_detail[1]+"/action/DeletePerson"

                body = {
                        "operator": "DeletePerson",
                        "info": {
                            "DeviceID": int(terminal_detail[0]),
                            "TotalNum": 1,
                            "IdType": 0,
                            "CustomizeID": [emp_num]
                            }
                        }

                headers = {
                            'Content-Type': "application/json",
                            'Authorization': "Basic YWRtaW46YWRtaW4=",
                            'User-Agent': "PostmanRuntime/7.17.1",
                            'Accept': "*/*",
                            'Cache-Control': "no-cache",
                            'Postman-Token': "246f59d4-ccb8-4bec-a3cd-3018a46a685e,1e6fcb78-072c-405c-936a-85c58d4d6960",
                            'Host': terminal_detail[1],
                            'Accept-Encoding': "gzip, deflate",
                            'Content-Length': "169",
                            'Connection': "keep-alive",
                            'cache-control': "no-cache"
                            }

                response = requests_import.request("POST", url, json=body, headers=headers)

    TerminalDetails.objects.all().delete()
    temp_term = TerminalDetails()
    temp_term.terminal_id = 0
    temp_term.terminal_ip = "0.0.0.0"
    temp_term.terminal_name = "Terminal Unavailable"
    temp_term.save()

    return render(requests, "administrator/full_reset.html")

@login_required
@user_passes_test(lambda u: u.is_superuser)
def bld(requests):
    return HttpResponse("<h1>10102019T0710P")
