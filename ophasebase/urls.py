from django.conf.urls import patterns, url

from ophasebase import views

urlpatterns = patterns('',
    url(r'^$', views.WelcomeView.as_view(), name='welcome'),
)
