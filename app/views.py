from datetime import datetime
from time import strptime
from unittest import result
from django.shortcuts import render, redirect
from django.db import connection
from app.db import DB
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import psycopg2

# Create your views here.
def home(request):
    return render(request, "authentication/starting_page.html")

def signup(request):
    if request.method == "POST":
        unitno = request.POST['unitno']
        fname = request.POST['fname']
        lname = request.POST['lname']
        residentid = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        param = [unitno, fname,lname,residentid,pass1]

        if User.objects.filter(username=residentid):
            return render(request, 'authentication/signup.html', {'user_exists': True})

        if pass1 != pass2:
            return render(request, 'authentication/signup.html', {'password_dont_match': True})

        try:
            if unitno == 'admin':
                DB().create_admin(fname, lname, unitno, residentid)  
            else:
                DB().create_user(fname, lname, unitno, residentid)
        except Exception as e:
            print(e)
            return render(request, 'authentication/signup.html', {'user_exists': True})
        myuser = User.objects.create_user(username=residentid, password=pass1)
        myuser.first_name = fname
        myuser.last_name = lname
     
        myuser.save()
        login(request, myuser)

        # with connection.cursor() as cursor:
        #     sql_insert_query = """ INSERT INTO usertable (residentid, firstname, lastname, email, password) VALUES (%s,%s,%s,%s,%s) """
        #     result = cursor.execute(sql_insert_query, param)
        #     connection.commit()
        #     print(result)

        return redirect('main')
    return render(request, "authentication/signup.html")

def signin(request):
    if request.POST:
        if request.POST['action'] == 'signin':
            email = request.POST.get('username', False)
            pass1 = request.POST.get('pass1', False)
            print(email, pass1)
            curr_user = authenticate(username=email, password=pass1)
            if curr_user is not None:
                login(request, curr_user)
            else:
                return render(request, 'authentication/signin.html', {'not_found': True})
            # with connection.cursor() as cursor:
            #     cursor.execute("SELECT residentid FROM usertable WHERE email = email")
            #     user = cursor.fetchone() 
            # if user is not None:
                
            #     with connection.cursor() as cursor:
            #         cursor.execute(f"INSERT INTO activeuser VALUES ('{user[0]}')")
            return redirect('main')
       
    return render(request, "authentication/signin.html")

# def PassUser(request):
#     if request.method == 'POST':
#         email = request.POST.get('email', False)
#         pass1 = request.POST.get('pass1', False)
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT residentid FROM usertable WHERE email = email")
#         user = cursor.fetchone() 
#     if user is not None:
#         with connection.cursor() as cursor:
#             cursor.execute(f"INSERT INTO activeuser VALUES ('{user[0]}')")

#     return user 

@login_required
def index(request):
    """Shows the main page"""
    if request.POST:
        if request.POST['action'] == 'delete':
            logout(request)
            return redirect("main")
            # with connection.cursor() as cursor:
            #     cursor.execute("DELETE FROM activeuser WHERE residentid = %s", [request.POST['id']])
            #     return redirect("signin")
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM activeuser")
    #     user = cursor.fetchone()

    result_dict = DB().get_venues()
    # result_dict["user"] = request.user
    # if user is not None:
    #     result_dict["user"]=user[0]
    result_dict['is_admin'] = DB().check_admin(request.user.username)
    return render(request,'app/index.html', result_dict)

@login_required
def bbqpit(request):
    error = False
    if request.method == "POST":
        if request.POST['action'] == 'delete':
            print('logout')
            logout(request)
            return redirect("main")
        starttime = request.POST.get('time', False)
        if request.POST['action'] == 'cancel':
            try:
                DB().delete_entry(starttime, 'BBQ Pit')
            except Exception as e:
                error = True
                print(e)
        if request.POST['action'] == 'book':
            try:
                print(request.user.username)
                DB().create_entry(starttime, 'BBQ Pit', request.user.username)
            except Exception as e:
                error = True
                print(e)
    bookings = DB().get_bbq_schedule()
    bookings['error'] = error
    bookings['venues'] = ['BBQ Pit', 'bbqpit']
    bookings['is_admin'] = DB().check_admin(request.user.username)
    return render(request,'app/booking.html', bookings)

@login_required
def tenniscourt(request):
    error = False
    if request.method == "POST":
        if request.POST['action'] == 'delete':
            logout(request)
            return redirect("main")
        starttime = request.POST.get('time', False)
        if request.POST['action'] == 'cancel':
            try:
                DB().delete_entry(starttime, 'Tennis Court')
            except Exception:
                error = True
        if request.POST['action'] == 'book':
            try:
                DB().create_entry(starttime, 'Tennis Court', request.user.username)
            except Exception:
                error = True
    bookings = DB().get_tenniscourt_schedule()
    bookings['error'] = error
    bookings['venues'] = ['Tennis Court', 'tenniscourt']
    bookings['is_admin'] = DB().check_admin(request.user.username)
    return render(request,'app/booking.html', bookings)

@login_required
def mph(request): 
    error = False
    if request.method == "POST":
        if request.POST['action'] == 'delete':
            logout(request)
            return redirect("main")
        starttime = request.POST.get('time', False)
        if request.POST['action'] == 'cancel':
            try:
                DB().delete_entry(starttime, 'Multi-Purpose Hall')
            except Exception:
                error = True
        if request.POST['action'] == 'book':
            try:
                DB().create_entry(starttime, 'Multi-Purpose Hall', request.user.username)
            except Exception:
                error = True
    bookings = DB().get_mph_schedule()
    bookings['error'] = error
    bookings['venues'] = ['Multi-Purpose Hall', 'mph']
    bookings['is_admin'] = DB().check_admin(request.user.username)
    return render(request,'app/booking.html', bookings)

@login_required
def tabletennis(request):
    error = False
    if request.method == "POST":
        if request.POST['action'] == 'delete':
            logout(request)
            return redirect("main")
        starttime = request.POST.get('time', False)
        if request.POST['action'] == 'cancel':
            try:
                DB().delete_entry(starttime, 'Table Tennis')
            except Exception:
                error = True
        if request.POST['action'] == 'book':
            try:
                DB().create_entry(starttime, 'Table Tennis', request.user.username)
            except Exception:
                error = True
    bookings = DB().get_tabletennis_schedule()
    bookings['error'] = error
    bookings['venues'] = ['Table Tennis', 'tabletennis']
    bookings['is_admin'] = DB().check_admin(request.user.username)
    return render(request,'app/booking.html', bookings)

@login_required
def analytics(request):
    if request.method == "POST":
        if request.POST['action'] == 'delete':
            logout(request)
            return redirect("main")
    result_dict = {}
    result_dict['latest_user'] = DB().get_latest_created_user()
    result_dict['booking_count'] = DB().get_booking_count()
    result_dict['least_booked'] = DB().get_least_booked()
    result_dict['most_booked'] = DB().get_most_booked()
    result_dict['is_admin'] = DB().check_admin(request.user.username)
    result_dict['most_resident'] = DB().get_most_booked_resident()
    result_dict['never_booked_resident'] = DB().never_booked_resident()
    if not result_dict['is_admin']:
        return redirect("main")
    return render(request, 'app/analytics.html', result_dict)