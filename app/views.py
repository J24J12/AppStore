from datetime import datetime
from django.shortcuts import render, redirect
from django.db import connection
from app.db import DB

# Create your views here.
def index(request):
    """Shows the main page"""

    ## Delete customer
    # if request.POST:
    #     if request.POST['action'] == 'delete':
    #         with connection.cursor() as cursor:
    #             cursor.execute("DELETE FROM customers WHERE customerid = %s", [request.POST['id']])

    result_dict = DB().get_venues()

    return render(request,'app/index.html',result_dict)

# Create your views here.
def bbqpit(request):
    # availtimes = []
    # curryear = 2022
    # currmonth = 2
    # currdate = 2
    # starttime = 8
    # endtime = 22
    
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT eventstartdate FROM bookings WHERE venue='BBQ Pit'")
    #     fetched = cursor.fetchall()
    
    # unavailtimes = list(sum(fetched, ()))
    
    # for i in range(endtime - starttime):
    #     startstamp = datetime(curryear, currmonth, currdate, i + starttime, 0)
    #     endstamp = datetime(curryear, currmonth, currdate, i + starttime + 1, 0)
    #     availtimes.append([startstamp, endstamp, startstamp in unavailtimes])
    
    # bookings = {'available': availtimes}
    bookings = DB().get_bbq_schedule()
    return render(request,'app/bbqpit.html', bookings)

def tenniscourt(request):
    bookings = DB().get_tenniscourt_schedule()
    return render(request,'app/tenniscourt.html', bookings)

def mph(request):
    bookings = DB().get_mph_schedule()
    return render(request,'app/mph.html', bookings)

def tabletennis(request):
    bookings = DB().get_tabletennis_schedule()
    return render(request,'app/tabletennis.html', bookings)


# Create your views here.
def view(request, id):
    """Shows the main page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
        customer = cursor.fetchone()
    result_dict = {'cust': customer}

    return render(request,'app/view.html',result_dict)

# Create your views here.
def add(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM customers WHERE customerid = %s", [request.POST['customerid']])
            customer = cursor.fetchone()
            ## No customer with same id
            if customer == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO customers VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                           request.POST['dob'] , request.POST['since'], request.POST['customerid'], request.POST['country'] ])
                return redirect('index')    
            else:
                status = 'Customer with ID %s already exists' % (request.POST['customerid'])


    context['status'] = status
 
    return render(request, "app/add.html", context)

# Create your views here.
def edit(request, id):
    """Shows the main page"""

    # dictionary for initial data with
    # field names as keys
    context ={}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        ##TODO: date validation
        with connection.cursor() as cursor:
            cursor.execute("UPDATE customers SET first_name = %s, last_name = %s, email = %s, dob = %s, since = %s, country = %s WHERE customerid = %s"
                    , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                        request.POST['dob'] , request.POST['since'], request.POST['country'], id ])
            status = 'Customer edited successfully!'
            cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
            obj = cursor.fetchone()


    context["obj"] = obj
    context["status"] = status
 
    return render(request, "app/edit.html", context)