from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path, reverse_lazy

from ophasebase.views import LoginSelectView, LandingPageView

admin.autodiscover()

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing_page'),
    path('mitmachen/', include('staff.urls', namespace='staff')),
    path('teilnehmer/', include('students.urls', namespace='students')),
    path('klausur/', include('exam.urls', namespace='exam')),
    path('workshops/', include('workshops.urls', namespace='workshops')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('clothing/', include('clothing.urls', namespace='clothing')),
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginSelectView.as_view(), name='login'),
    path('accounts/local/login/',
         LoginView.as_view(template_name='admin/login.html'),
         name='local_login'),
    path('accounts/logout/',
         LogoutView.as_view(next_page=reverse_lazy('landing_page')),
         name='logout'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
