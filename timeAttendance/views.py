from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from django.views.decorators.csrf import csrf_exempt
import sqlite3
from sqlite3 import Error



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
def GetDeviceID(request):

    data=[]
    emp=[]
    emp_grouped = [[None]]
    #emp_grouped[0] = [0,2]
    # Create a connectin to the database
    conn = create_connection(r"C:\sqlite\db\pythonsqlite.db")
    cur = conn.cursor()
    #cur.execute(r"SELECT * FROM attendence")
    #cur.execute(r"SELECT * FROM attendence WHERE date(enter_time) = date('now') and name like 'basyir'")
    cur.execute(r"SELECT * FROM attendence WHERE date(enter_time) = date('now')")
    rows = cur.fetchall()


    #rows = [rows[0], rows[-1]]



    for row in rows:
        data.append({'id':row[0],'name':row[1],'time':row[2]})

    for rows in data:

        insert_check = True

        if not emp:
            emp.append(rows)
            print('inserted')
            continue

        for rows_check in emp:
            if (rows['id'] == rows_check['id']):
                insert_check = False


        if insert_check:
            print('true')
            emp.append(rows)

    for i in range(len(emp)):
        for index, temp_dat in enumerate(data):
            if (temp_dat['id'] == emp[i]['id']):
                emp_grouped[i][index]=temp_dat


    context= {
        'data': emp
        }

    return render(request, 'timeAttendance/deviceDetails.html', context)
