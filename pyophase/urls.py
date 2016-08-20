from django.conf.urls import include, url
from django.urls import reverse_lazy
import django.contrib.auth.views

from django.conf import settings
from django.views.static import serve

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^', include('website.urls', namespace='website')),
    url(r'^mitmachen/', include('staff.urls', namespace='staff')),
    url(r'^teilnehmer/', include('students.urls', namespace='students')),
    url(r'^klausur/', include('exam.urls', namespace='exam')),
    url(r'^workshops/', include('workshops.urls', namespace='workshops')),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^clothing/', include('clothing.urls', namespace='clothing')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', django.contrib.auth.views.login, {'template_name': 'admin/login.html'}, name='login'),
    url(r'^accounts/logout/$', django.contrib.auth.views.logout, {'next_page': reverse_lazy('website:homepage')}, name='logout'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
