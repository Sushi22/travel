from django.urls import path     
from . import views
from django.conf.urls import url

urlpatterns = [
    
    path('', views.index, name="index"),
    path('register', views.register_page),
    path('login', views.login_page),
    path('register/process', views.register),
    path('login/process', views.login),
    path('about', views.about),
    path('contact', views.contact),
    path('hotels', views.hotels),
    path('phpindex', views.phpindex),
    url(r'^summer/$', views.summer),
    url(r'^summ/(?P<pk>\d+)/summ/(?P<string>[\w\-]+)/$', views.gmap,name='gmap'),
    #url(r'^get_info/$', views.get_info,name='get_info'),
    url(r'^summer/$', views.summer),
    url(r'^summ/(?P<pk>\d+)/summ/(?P<string>[\w\-]+)/$', views.gmap,name='gmap'),
    url(r'^summer/$', views.summer),
    url(r'^summ/(?P<pk>\d+)/summ/(?P<string>[\w\-]+)/$', views.gmap,name='gmap'),
    path('', views.homepage),
    path('dashboard', views.dashboard),	 
    path('logout', views.logout),
    path('trip/add', views.add_trip_page),
    path('add_trip', views.add_trip),  
    path('trip/edit/<int:num>', views.edit_trip_page),
    path('trip/edit/<int:num>/process', views.edit_trip),
    path('trip/<int:num>', views.trip_info_page),
    path('delete/<int:num>', views.delete_trip)
    
]