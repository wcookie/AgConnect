from django.conf.urls import include, url
from django.contrib import admin
from . import views
urlpatterns = [
   
    url(r'^$', view=views.login_view, name="login"),
    url(r'^redirecter/$', view = views.test_view),
    url(r'^firstfarm/$', view = views.homepage, name = "dash"),
    url(r'^secondfarm/$', view=views.secondfarm, name="second"),
    url(r'^thirdfarm/$', view=views.thirdfarm, name="third"),
    url(r'^geo/$', view =views.geo_view),
]