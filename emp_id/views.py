from datetime import datetime
from random import randint

import mysql.connector
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from .models import Employee
import mysql.connector as sql

# Create your views here.

firstn = ''
lastn = ''
s = ''
email = ''
passw = ''
otp=''

def signup(request):
    global firstn, lastn, s, email, passw
    if request.method == "POST":
        m = sql.connect(host="localhost", user='root', password='YES', database='login')
        cursor = m.cursor()
        d = request.POST

        for key, value in d.items():
            if key == 'first_name':
                firstn = value
            if key == 'last_name':
                lastn = value
            if key == 'sex':
                s = value
            if key == 'email':
                email = value
            if key == 'password':
                passw = value

            c = "insert into users values('{}','{}','{}','{}','{}','{}')".format(firstn, lastn, s, email, passw,otp)
            cursor.execute(c)
            m.commit()
    return render(request, 'signup.html')


em = ''
pwd = ''


def login(request):
    global em, pwd
    if request.method == "POST":
        m = sql.connect(host="localhost", user='root', password='YES', database='login')
        cursor = m.cursor()
        d = request.POST
        for key, value in d.items():
            if key == "email":
                em = value
            if key == "password":
                pwd = value
        c = "select * from users where email='{}' and password='{}'".format(em, pwd)
        cursor.execute(c)
        t = tuple(cursor.fetchall())
        if t == ():
            return HttpResponse("not registeres user")
        else:
            return render(request, "index.html")
    return render(request, "login_page.html")


def index(request):
    if request == 'POST':
        return render(request, 'index.html')
    else:
        return HttpResponse("singin first")


def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    print(context)
    return render(request, 'view_all_emp.html', context)


def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        dept = int(request.POST['dept'])
        role = int(request.POST['role'])
        new_emp = Employee(first_name=first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone,
                           dept_id=dept, role_id=role, hire_date=datetime.now())
        new_emp.save()
        return HttpResponse('Employee added Successfully')
    elif request.method == 'GET':
        return render(request, 'add_emp.html')
    else:
        return HttpResponse("An Exception Occured! Employee Has Not Been Added")


def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("employee removed successfully")
        except:
            return HttpResponse("please enter a valid emp-id")
    emps = Employee.objects.all
    context = {
        'emps': emps
    }
    return render(request, 'remove_emp.html', context)


def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps = emps.filter(dept__name__icontains=dept)
        if role:
            emps = emps.filter(role__name__icontains=role)

        context = {
            'emps': emps
        }
        return render(request, 'view_all_emp.html', context)

    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse('An Exception Occurred')


def forgotpassword(request):
    if request.method=='POST':
        email = request.POST.get('email')
        otp = ''
        for i in range(5):
            otp = otp + str(randint(0, 9))
        otp = int(otp)
        test = sql.connect(host="localhost", username="root", password='YES', database='login')
        crs = test.cursor()
        query = "select password from users where email ='" + email + "'"
        crs.execute(query)
        data = crs.fetchall()

        print(data)
        if data is None:
            return HttpResponse("you are not registered ! or email is incorrect")
        else:
            query = 'update users set otp=%s where email=%s'
            crs.execute('set sql_safe_updates=0')
            crs.execute(query, (otp, email))
            test.commit()
            return render(request,"restpassword.html")


def resetpassword(request):
    if request.method=='POST':
        mail = request.POST.get('email')
        new_password = request.POST.get('new_password')
        otp = int(request.POST.get('otp'))

        db = mysql.connector.connect(host="localhost", username="root", password='YES', database='login')
        crs = db.cursor()
        query = "select otp from users where email='" + mail + "'"
        crs.execute(query)
        data = crs.fetchall()
        
        v=int(data[0][0])

        if v == otp:
            query = "update users set password='" + new_password + "' where email='" + mail + "'"
            crs.execute(query)
            crs.execute("update users set otp=Null where email='" + mail + "'")
            db.commit()
            return HttpResponse("password reset succefffully! Please login again..")
        else:
            return HttpResponse("your otp is incorrect!try again")



def enter_email(request):
    return render(request,"enter_email.html")

