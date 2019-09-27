from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from django.views.decorators.csrf import csrf_exempt
import sqlite3
from sqlite3 import Error
from django.contrib.auth.decorators import login_required
from timeAttendance.models import EmployeeAttendance
from django.forms.models import model_to_dict
from datetime import date, datetime, timedelta

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn
def home(request):

    return render(request, 'timeAttendance/home.html')
def get_terminal_information(ipAddress, username, passwrod):

    a = None

    #username = this.username
    #username = request.POST.get("username")
    #password = request.POST.get("password")

    #url = "http://192.168.0.33/action/GetSysParam"
    url = "http://"+ipAddress+"/action/GetSysParam"

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

    #response = requests.request("POST", url, headers=headers, auth=HTTPBasicAuth('admin', 'admin'))

    response = requests.request("POST", url, headers=headers, auth=HTTPBasicAuth(username, password))

    json_data = response.text
    data = json.loads(json_data)
    a = data['info']
    response_data = {}
    response_data['info'] = a

@csrf_exempt
@login_required
def GetDeviceID(request):

    date2 = None
    date_tag = None
    if request.GET.get('date') and request.GET.get('date2'):
        message = 'You submitted: %r' % request.GET['date']
        date2 = datetime.strptime(request.GET['date'], "%Y-%m-%d" ).date()
        date_tag = {'date' : request.GET['date']}
        date_tag_to = {'date_to' : request.GET['date2']}
        date_to = datetime.strptime(request.GET['date2'], "%Y-%m-%d" ).date()
        #print()
        #print(request.GET['date'])
        #print(request.GET['date2'])
        #print()
    else:
        date_tag = {'date' : str(date.today())}
        date_tag_to = {'date_to' : str(date.today())}

        date2 = date.today()
        date_to = date.today()

    todays_employee = []
    data=[]
    emp=[]
    emp_grouped = [[None]]
    #emp_grouped[0] = [0,2]
    # Create a connectin to the database
    #conn = create_connection(r"C:\sqlite\db\pythonsqlite.db")
    #cur = conn.cursor()
    #cur.execute(r"SELECT * FROM attendence")
    #cur.execute(r"SELECT * FROM attendence WHERE date(enter_time) = date('now') and name like 'basyir'")
    #cur.execute(r"SELECT * FROM attendence WHERE date(enter_time) = date('now')")
    #rows = cur.fetchall()

    temp_data = EmployeeAttendance.objects.all()
    temp_data_list = []
    date_range = []
    #for temp_data2 in temp_data:
        #temp_data_list.append(model_to_dict(temp_data2))

    #print(type(temp_data))
    try:
        delta = date_to - date2

        for i in range(delta.days + 1):
            day = date2 + timedelta(days=i)
            print()
            print(day)
            print()
            date_range.append(day)

    except:
        pass

    date_range_dict_list = []
    for date_temp in date_range:
        date_range_dict = {
            'date' : date_temp
            }
        date_range_dict_list.append(date_range_dict)

    employee_id_list_list = []
    for date_range_individual in date_range:
        #employee_id_list = EmployeeAttendance.objects.values('employee_id').filter(capture_time__contains = str(date2)).distinct()
        employee_id_list = EmployeeAttendance.objects.values('EmployeeDetail').filter(capture_time__contains = str(date_range_individual)).distinct()
        #employee_id_list_list.append(EmployeeAttendance.objects.values('employee_id').filter(capture_time__contains = str(date_range_individual)).distinct())


        for employee_id_dict in employee_id_list:

            #temp2 = EmployeeAttendance.objects.filter(employee_id = employee_id_dict['employee_id'], capture_time__contains = str(date2))
            temp2 = EmployeeAttendance.objects.filter(EmployeeDetail = employee_id_dict['EmployeeDetail'], capture_time__contains = str(date_range_individual))

            temp2_earliest = temp2.earliest('capture_time')
            temp2_latest = temp2.latest('capture_time')

            temp2_datetime_earliest = datetime.strptime(temp2_earliest.capture_time,"%Y-%m-%dT%H:%M:%S")
            temp2_datetime_latest = datetime.strptime(temp2_latest.capture_time,"%Y-%m-%dT%H:%M:%S")

            working_hours = temp2_datetime_latest - temp2_datetime_earliest

            temp_employee_daily_info = { 'branch': temp2_earliest.EmployeeDetail.branch ,'department': temp2_earliest.EmployeeDetail.department,'employee_id': temp2_earliest.EmployeeDetail.id, 'name': temp2_earliest.EmployeeDetail.name, 'capture_time_earliest': temp2_earliest.capture_time, 'capture_location_earliest': temp2_earliest.capture_location.terminal_name, 'capture_time_latest': temp2_latest.capture_time, 'capture_location_latest':temp2_latest.capture_location.terminal_name, 'working_hours':str(working_hours), 'date':date_range_individual}

            temp_data_list.append(temp_employee_daily_info)

    #MUST BE A LIST OF DICTIONARY
    context= {
        'data': temp_data_list,
        'date_tag': date_tag,
        'date_tag2': date_tag_to,
        'date_range': date_range_dict_list
        }

    return render(request, 'timeAttendance/deviceDetails.html', context)
