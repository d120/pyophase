from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy
import django.contrib.auth.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^', include('ophasebase.urls', namespace='ophasebase')),
    url(r'^mitmachen/', include('staff.urls', namespace='staff')),
    url(r'^teilnehmer/', include('students.urls', namespace='students')),
    url(r'^klausur/', include('exam.urls', namespace='exam')),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', django.contrib.auth.views.login, {'template_name': 'admin/login.html'}, name='login'),
    url(r'^accounts/logout/$', django.contrib.auth.views.logout, {'next_page': reverse_lazy('ophasebase:welcome')}, name='logout'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
