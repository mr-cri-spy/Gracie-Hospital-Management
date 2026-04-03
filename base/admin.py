from django.contrib import admin
from base import models as base_models

class BillingAdmin(admin.ModelAdmin):
    list_display = ['billing_id', 'patient', 'total_inr', 'status', 'utr_number', 'date']
    list_filter = ['status']
    search_fields = ['billing_id', 'utr_number', 'patient__full_name']

    def total_inr(self, obj):
        return f"₹{obj.total}"
    total_inr.short_description = "Total (₹)"

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost_inr', 'doctor_count']
    search_fields = ['name']

    def cost_inr(self, obj):
        return f"₹{obj.cost}"
    cost_inr.short_description = "Cost (₹)"

    def doctor_count(self, obj):
        return obj.available_doctors.count()
    doctor_count.short_description = "Doctors"

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['appointment_id', 'patient', 'doctor', 'service', 'status', 'appointment_date']
    list_filter = ['status']
    search_fields = ['appointment_id', 'patient__full_name', 'doctor__full_name']

admin.site.register(base_models.Service, ServiceAdmin)
admin.site.register(base_models.Appointment, AppointmentAdmin)
admin.site.register(base_models.Billing, BillingAdmin)
admin.site.register(base_models.MedicalRecord)
admin.site.register(base_models.LabTest)
admin.site.register(base_models.Prescription)
