from django.contrib import admin
from django.contrib.admin.apps import AdminConfig

from pyophase.dashboard_links import DashboardLinks


class PyophaseAdminConfig(AdminConfig):
    default_site = 'pyophase.admin.PyophaseAdminSite'


class PyophaseAdminSite(admin.AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        context.update({
            "navigation_links": DashboardLinks.get_navigation_links()
        })
        return context
