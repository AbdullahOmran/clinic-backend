from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Doctor, Patient,Secretary,Clinic,Appointment

class DoctorAdmin(ModelAdmin):
    list_display = ["id",'username', "age"]

    @admin.display(empty_value="???")
    def username(self, instance):
        return instance.user.username

admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Patient)
admin.site.register(Clinic)
admin.site.register(Secretary)
admin.site.register(Appointment)

