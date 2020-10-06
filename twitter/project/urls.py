from django.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    url(r'^login/$', views.login , name='login'),
    url(r'^logout/$', views.logout , name='logout'),
    url(r'^callback/$', views.callback, name='callback'),
    url(r'^top/user/$', views.top_user, name='top_user'),
    url(r'^top/domain/$', views.top_domain, name='top_domain'),
]
