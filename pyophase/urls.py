from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import reverse_lazy
from django.views.static import serve


admin.autodiscover()

urlpatterns = [
    url(r'^', include('website.urls', namespace='website')),
    url(r'sso/', include('pyTUID.urls')),
    url(r'^mitmachen/', include('staff.urls', namespace='staff')),
    url(r'^teilnehmer/', include('students.urls', namespace='students')),
    url(r'^klausur/', include('exam.urls', namespace='exam')),
    url(r'^workshops/', include('workshops.urls', namespace='workshops')),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^clothing/', include('clothing.urls', namespace='clothing')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', LogoutView.as_view(next_page=reverse_lazy('website:homepage')), name='logout'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]