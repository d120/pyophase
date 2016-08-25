from django.conf.urls import url

from . import views


app_name = 'website'
urlpatterns = [
    url(r'^$', views.HomepageView.as_view(), name='homepage'),
    url(r'^bachelor/$', views.ScheduleView.as_view(), kwargs={'degree': 'BSC'}, name='bachelor'),
    url(r'^master-de/$', views.ScheduleView.as_view(), kwargs={'degree': 'MSC'}, name='master-de'),
    url(r'^master-dss/$', views.ScheduleView.as_view(), kwargs={'degree': 'DSS'}, name='master-dss'),
    url(r'^helfen/$', views.HelfenView.as_view(), name='helfen'),
]
