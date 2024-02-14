from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import (Doctor,
                    Patient,Secretary,Clinic,
                    Appointment,WorkingSchedule,Prescription,
                    Encounter,Medication,Treatment,
                    MedicationsStore,SymptomDiagnosisPair
                    )

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
admin.site.register(WorkingSchedule)
admin.site.register(Encounter)
admin.site.register(Prescription)
admin.site.register(Medication)
admin.site.register(MedicationsStore)
admin.site.register(Treatment)
admin.site.register(SymptomDiagnosisPair)
admin.site.site_header = 'Medcy Administration'
admin.site.site_title = 'Medcy Administration'
admin.site.site_url = 'http://localhost:3000/'
