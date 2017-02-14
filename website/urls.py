from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views


app_name = 'website'
urlpatterns = [
    url(r'^$', views.HomepageView.as_view(), name='homepage'),
    url(r'^details/(?P<category>[^/]+)/$', views.DetailsView.as_view(), name='details'),
    url(r'^helfen/$', views.HelfenView.as_view(), name='helfen'),
    url(r'^oinforz/$', views.OInforzView.as_view(), name='oinforz'),
]

#Redirect old links
urlpatterns += [
        url(r'^' + category + r'/$',
            RedirectView.as_view(pattern_name='website:details',
                permanent=False),
            kwargs = {'category' : category},
            name = category)
        for category in ['bachelor', 'master-de', 'master-dss', 'jba', 'edu']
]
