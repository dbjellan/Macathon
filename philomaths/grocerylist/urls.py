from django.conf.urls import patterns, url

from grocerylist import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^displayresult$', views.displayresult, name='displayresult'),
    url(r'^createlist$', views.createlist, name='createlist'),
    url(r'^inputimage$', views.inputimage, name='inputimage'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^about$', views.about, name='about'),
    )
