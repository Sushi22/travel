from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import User, Trip
from time import strftime, strptime
from django.contrib import messages
import datetime
import bcrypt
from .models import Season,Summer,Winter,Autumn
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from geopy.geocoders import Nominatim
import requests
import json
import time
#import pyowm 
import pprint


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "index.html" 

def index(request):
    dests=Season.objects.all()
    return render(request, "index.html",{'dests' : dests})


def gmap(request,pk,string):
    geolocator = Nominatim(user_agent="travel_app")
    
    # own=pyowm.OWM('97c5fd064b1993fa5c4db42b98a0e68f')

    obj=get_object_or_404(Summer,pk=pk)
    endpoint="https://maps.googleapis.com/maps/api/place/nearbysearch/json?"

    dest=obj.name
    location = geolocator.geocode(dest)
    #city=own.weather_at_place(dest)

    #l = city.get_location()

    latitude=location.latitude#str(l.get_lat())
    print(latitude)
    longitude=location.longitude#str(l.get_lon())
    print(longitude)
    if(string=='Meal'):

        prop='restaurant'
    
    else:
        prop='tourist_attraction'

    API_KEY='AIzaSyCYjGHqszlEfDknxs_6tGyLzsNmbSy3Gjw'#'AIzaSyDF3scZqIFGSYQk__pXmgv1H0no97g2R64'#'AIzaSyD0_Xn90qEIim4dUg_2r4Ix3AKljo14png'

    user_req= "location={},{}&radius=6000&keyword={}&key={}".format(latitude,longitude,prop,API_KEY)

    url=endpoint+user_req

    # pprint.pprint(url)

    response=requests.get(url)

    res=response.text

    pydata=json.loads(res)

    #pprint.pprint(pydata)

    my_data=pydata['results']

    # for i in my_data:
    #     print(pprint.pprint(i))

    result=get_info(request,my_data)
    #print(my_data)
    return result

def get_info(request,*args):
    mylist=[]
    data=args
    my_data=args[0]
    print(len(my_data))
    #pprint.pprint(my_data)
    #print('###########################################################################################')
    if request.method=="GET":
        for i in range(0,6):
            #pprint.pprint(my_data[i])
            #if my_data[i]['rating']>=4:
            mylist.append(my_data[i])
        # print(mylist[0])
        return render(request,'maps.html',{'mylist':mylist})

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def summer(request):
    summ=Summer.objects.all()
    return render(request, "summer.html",{'summ' : summ})

def winter(request):
    win=Winter.objects.all()
    return render(request, "winter.html",{'win' : win})

def autumn(request):
    aut=Autumn.objects.all()
    return render(request, "autumn.html",{'aut' : aut})

def hotels(request):
    return render(request, "hotels.html")
def phpindex(request):
    return render(request, "phpindex.html")


def homepage(request):
    return render(request, "homepage.html")

def register_page(request):
    #if "user_id" in request.session:
        #return redirect("/")
    return render(request, "register.html")

def login_page(request):
    #if "user_id" in request.session:
        #return redirect("/")
    return render(request, "login.html")

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/register")
    else:
        password = request.POST["pw"]
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(pw_hash)
        new_user = User.objects.create(first_name = request.POST["fname"], last_name = request.POST["lname"], email = request.POST["email"], pw = pw_hash)
        request.session["user_id"] = new_user.id
        return redirect("/dashboard")

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/dashboard")
    else:
        user = User.objects.filter(email = request.POST["email"])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST["pw"].encode(), logged_user.pw.encode()):
                request.session["user_id"] = logged_user.id
                return redirect("/dashboard")
            return redirect("/login")

def dashboard(request):
    if "user_id" not in request.session:
        messages.error(request, "You are no longer logged in")
        return redirect("/login")
    else:
        context = {
            "all_trips": Trip.objects.all(),
            "user_id": User.objects.get(id=request.session["user_id"])
        }
        return render(request, "dashboard.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")

def add_trip_page(request):
    if "user_id" not in request.session:
        messages.error(request, "Not logged in")
        return redirect("/login")
    else:
        context = {
            "user_id": User.objects.get(id=request.session["user_id"])
        }
        return render(request, "addtrip.html", context)

def add_trip(request):
    errors = User.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/trip/add")
    else:
        user = User.objects.get(id = request.session["user_id"])
        dest = request.POST["destination"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        plan = request.POST["plan"]
        Trip.objects.create(user = user, destination = dest, start_date = start_date, end_date = end_date, plan = plan)
        messages.success(request, "Successfully added new trip!")
        return redirect("/dashboard")

def edit_trip_page(request, num):
    if "user_id" not in request.session:
        messages.error(request, "Not logged in")
        return redirect("/login")
    else:
        context = {
            "user_id": User.objects.get(id = request.session["user_id"]),
            "trip": Trip.objects.get(id = num)
        }
        return render(request, "edit.html", context)

def edit_trip(request, num):
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/trip/edit/{num}")
    else:
        update_trip = Trip.objects.get(id = num)
        update_trip.destination = request.POST["destination"]
        update_trip.start_date = request.POST["start_date"]
        update_trip.end_date = request.POST["end_date"]
        update_trip.plan = request.POST["plan"]
        update_trip.save()
        messages.success(request, "Successfully edited your trip!")
        return redirect("/dashboard")

def trip_info_page(request, num):
    if "user_id" not in request.session:
        messages.error(request, "Not logged in")
        return redirect("/login")
    else:
        context={
            "user_id": User.objects.get(id=request.session["user_id"]),
            "trip": Trip.objects.get(id=num)
        }
        return render(request, 'trip_info.html', context)

def delete_trip(request, num):
    if "user_id" not in request.session:
        messages.error(request, "Not logged in")
        return redirect('/login')
    trip = Trip.objects.get(id = num)
    if request.session['user_id'] != trip.user.id:
        messages.error(request, "You didn't make this")
        return redirect('/')
    else:
        trip = Trip.objects.get(id = num)
        trip.delete()
        return redirect("/dashboard")



#def index(request):
    #return render(request, "index.html")



