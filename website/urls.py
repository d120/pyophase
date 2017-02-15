from django.conf.urls import url

from . import views


app_name = 'website'
urlpatterns = [
    url(r'^$', views.HomepageView.as_view(), name='homepage'),
    url(r'^detail/(?P<slug>[^/]+)/$', views.CategoryDetailView.as_view(), name='detail_view'),
    url(r'^helfen/$', views.HelperView.as_view(), name='helfen'),
    url(r'^oinforz/$', views.OInforzView.as_view(), name='oinforz'),
]
