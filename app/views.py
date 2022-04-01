from datetime import datetime
from django.shortcuts import render, redirect
from django.db import connection
from app.db import DB
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return render(request, "authentication/starting_page.html")

def signup(request):

    if request.method == "POST":
        residentid = request.POST['residentid']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(residentid=residentid):
            messages.error(request, "residentid already exist!")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "email already exist!")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, 'password dont match!')

        myuser = User.objects.create_user(residentid, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your Account has been successfully created.")

        return redirect('signin')

    return render(request, "authentication/signup.html")

def signin(request):

    if request.POST:
        if request.POST['action'] == 'signin':
            email = request.POST.get('email', False)
            pass1 = request.POST.get('pass1', False)
            print(email, pass1)
            with connection.cursor() as cursor:
                cursor.execute("SELECT residentid FROM usertable WHERE email = email")
                user = cursor.fetchone() 
            if user is not None:
                
                with connection.cursor() as cursor:
                    cursor.execute(f"INSERT INTO activeuser VALUES ('{user[0]}')")
                return redirect('main')
       
    return render(request, "authentication/signin.html")


      


def PassUser(request):
    if request.method == 'POST':
        email = request.POST.get('email', False)
        pass1 = request.POST.get('pass1', False)
    with connection.cursor() as cursor:
        cursor.execute("SELECT residentid FROM usertable WHERE email = email")
        user = cursor.fetchone() 
    if user is not None:
        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO activeuser VALUES ('{user[0]}')")

    return user 

def index(request):
    """Shows the main page"""
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM activeuser WHERE residentid = %s", [request.POST['id']])
                return redirect("signin")
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM activeuser")
        user = cursor.fetchone()

    result_dict = DB().get_venues()

    if user is not None:
        result_dict["user"]=user[0]
    print(result_dict)
    return render(request,'app/index.html', result_dict)

 
    

# Create your views here.
def bbqpit(request):
    
    user = PassUser(request)
    
    # bookings = {'available': availtimes}
    bookings = DB().get_bbq_schedule()
    return render(request,'app/bbqpit.html', bookings)

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