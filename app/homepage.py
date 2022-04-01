from django.contrib import admin
from django.urls import path, include
from . import views 


urlpatterns = [
    path('', views.home, name='home'), 
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),

    path('main', views.index, name='main'),
    path('bbqpit', views.bbqpit, name='bbqpit')
]