from django.conf.urls import url

from workshops import views

urlpatterns = [
    url(r'^$', views.WorkshopCreate.as_view(), name='create'),
    url(r'success/$', views.WorkshopCreateSuccess.as_view(), name='create_success'),
]
