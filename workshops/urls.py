from django.conf.urls import url

from . import views


app_name = 'workshops'
urlpatterns = [
    url(r'^$', views.WorkshopCreate.as_view(), name='create'),
    url(r'success/$', views.WorkshopCreateSuccess.as_view(), name='create_success'),
]
