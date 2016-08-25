from django.conf.urls import url

from . import views


app_name = 'students'
urlpatterns = [
    url(r'^$', views.StudentAdd.as_view(), kwargs={'exam_enabled': True}, name='registration'),
    url(r'master/$', views.StudentAdd.as_view(), kwargs={'exam_enabled': False}, name='registration-master'),
    url(r'success/$', views.StudentAddSuccess.as_view(), name='registration_success'),
]
