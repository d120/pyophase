from django.conf.urls import url

from ophasebase import views

app_name = 'ophasebase'
urlpatterns = [
    url(r'^$', views.WelcomeView.as_view(), name='welcome'),
]
