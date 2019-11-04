from django.contrib import admin
from django.db.models import When, Count, Case, IntegerField
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from ophasebase.models import Ophase
from students.admin_actions import generate_part_cert
from .models import Newsletter, Settings, Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'prename', 'tutor_group', 'want_exam']
    list_filter = ['want_exam', 'tutor_group']
    list_display_links = ['name', 'prename']
    search_fields = ['name', 'prename']
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ['newsletters']
    actions = [generate_part_cert]


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', '_categories', 'active', '_num_new_abo', '_export']
    list_filter = ['active']
    list_display_links = ['name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(num=Count(Case(
                When(student__ophase=Ophase.current(), then=1),
                output_field=IntegerField())))

    def _num_new_abo(self, item):
        return item.num
    _num_new_abo.short_description = _("# Neue Abos")
    _num_new_abo.admin_order_field = 'num'

    def _categories(self, item):
        return "Alle" if item.categories.count() == 0 else ", ".join(str(x) for x in item.categories.all())
    _categories.short_description = _("Kategorie(n)")

    def _export(self, item):
        return format_html("<a href='{}'><span class='fa fa-share-alt'></span></a>",
                           reverse("dashboard:students:newsletter_export", args=(item.pk,)))
    _export.short_description = _("Export")




@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['student_registration_enabled']
