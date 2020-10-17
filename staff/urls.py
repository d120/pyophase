from django.urls import path

from . import views

app_name = 'staff'
urlpatterns = [
    path('', views.StaffAdd.as_view(), name='registration'),
    path('success/', views.StaffAddSuccess.as_view(),
         name='registration_success'),
    path('tutortypen/', views.GroupCategoryList.as_view(),
         name='tutor_group_category_list'),
    path('orgaaufgaben/', views.OrgaJobList.as_view(), name='orgajob_list'),
    path('helferaufgaben/', views.HelperJobList.as_view(),
         name='helperjob_list'),
]
