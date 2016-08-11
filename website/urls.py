from django.conf.urls import url

from website import views

app_name = 'website'
urlpatterns = [
    url(r'^$', views.HomepageView.as_view(), name='homepage'),
    url(r'^bachelor/$', views.BachelorView.as_view(), name='bachelor'),
    url(r'^master-de/$', views.MasterDeView.as_view(), name='master-de'),
    url(r'^master-dss/$', views.MasterDssView.as_view(), name='master-dss'),
    url(r'^helfen/$', views.HelfenView.as_view(), name='helfen'),
    url(r'^intern/$', views.InternView.as_view(), name='intern'),
]
