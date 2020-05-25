from django.contrib import admin
from .models import Patient


class PatientAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'phone', 'email', 'sex', 'date_of_birth']


admin.site.register(Patient, PatientAdmin)
