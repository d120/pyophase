from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pyophase.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', include('ophasebase.urls', namespace='ophasebase', app_name='ophasebase')),
    url(r'^mitmachen/', include('staff.urls', namespace='staff', app_name='staff')),
    url(r'^teilnehmer/', include('students.urls', namespace='students', app_name='students')),
    url(r'^klausur/', include('exam.urls', namespace='exam', app_name='exam')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': reverse_lazy('ophasebase:welcome')}, name='logout'),
)
