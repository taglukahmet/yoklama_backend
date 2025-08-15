from django.urls import path
from django.contrib import admin
from .views import run_script, run_script_for_pres
from lecturer_data.models import University

class CustomScriptAdmin(admin.ModelAdmin):
    change_list_template = 'admin/custom_script_page.html'

    def get_urls(self):
        urls = super().get_urls()  # Get default admin URLs
        custom_urls = [
            path('run_uni_licence_scraper/', self.admin_site.admin_view(run_script), name='run_uni_licence_scraper'),
            path('run_uni_pre_licence_scraper/', self.admin_site.admin_view(run_script_for_pres), name='run_uni_pre_licence_scraper'), 
        ]
        return custom_urls + urls  # Combine custom URLs with default ones

# Register model with custom admin view
admin.site.register(University, CustomScriptAdmin)

