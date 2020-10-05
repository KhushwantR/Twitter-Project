from django.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    url(r'^login/$', views.login , name='login'),
    url(r'^logout/$', views.logout , name='logout'),
    url(r'^callback/$', views.callback, name='callback'),
]
