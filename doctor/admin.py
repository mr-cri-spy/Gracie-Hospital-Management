from django.contrib import admin
from doctor import models as doctor_models

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'specialization', 'qualifications', 'city', 'state', 'mobile', 'years_of_experience']
    list_filter = ['specialization', 'city', 'state']
    search_fields = ['full_name', 'specialization', 'registration_number']
    fieldsets = (
        ('Personal Info', {
            'fields': ('user', 'full_name', 'image', 'mobile', 'bio')
        }),
        ('Professional Info', {
            'fields': ('specialization', 'qualifications', 'years_of_experience', 'registration_number')
        }),
        ('Location', {
            'fields': ('city', 'state')
        }),
        ('Availability', {
            'fields': ('next_available_appointment_date',)
        }),
    )

admin.site.register(doctor_models.Doctor, DoctorAdmin)
admin.site.register(doctor_models.Notification)
