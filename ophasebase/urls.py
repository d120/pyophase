from django.conf.urls import patterns, url

from ophasebase import views

urlpatterns = [
    url(r'^$', views.WelcomeView.as_view(), name='welcome'),
]
