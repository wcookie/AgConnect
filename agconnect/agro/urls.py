from django.conf.urls import include, url
from django.contrib import admin
from . import views
urlpatterns = [
   
    url(r'^$', view=views.login_view),
    url(r'^redirecter/$', view = views.test_view),
]