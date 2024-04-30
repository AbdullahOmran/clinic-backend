from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import (Doctor,
                    Patient,Secretary,Clinic,
                    Appointment,WorkingSchedule,Prescription,
                    Encounter,Medication,Treatment,
                    MedicationsStore,SymptomDiagnosisPair,
                    ClinicUser,BufferTime, AppointmentSettings, ClinicAvailability
                    )
from django.contrib.auth.models import User                  
from django.contrib.auth.admin import UserAdmin


class UserAdminCustom(UserAdmin):
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            clinic = Clinic.objects.filter(admin = request.user)[0]
            obj.save()
            is_exists = ClinicUser.objects.filter(user = obj ).count() > 0
            if not is_exists:
                new_user = ClinicUser.objects.create(user = obj, clinic = clinic)
                new_user.save()
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        clinic = Clinic.objects.filter(admin=request.user)[0]
        clinic_users = ClinicUser.objects.filter(clinic=clinic)
        users = [u.user.id for u in clinic_users]
        return qs.filter(id__in = users)

admin.site.unregister(User)
admin.site.register(User, UserAdminCustom)


class DoctorAdmin(ModelAdmin):
    list_display = ["id",'username', "age"]
    
    @admin.display(empty_value="???")
    def username(self, instance):
        return instance.user.username

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "clinic" and not request.user.is_superuser:
            kwargs["queryset"] = Clinic.objects.filter(admin=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ClinicAdmin(ModelAdmin):
    pass

admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Patient)
admin.site.register(Clinic, ClinicAdmin)
admin.site.register(Secretary)
admin.site.register(Appointment)
admin.site.register(WorkingSchedule)
admin.site.register(Encounter)
admin.site.register(Prescription)
admin.site.register(Medication)
admin.site.register(MedicationsStore)
admin.site.register(Treatment)
admin.site.register(SymptomDiagnosisPair)
admin.site.register(ClinicUser)
admin.site.register(ClinicAvailability)
admin.site.register(BufferTime)
admin.site.register(AppointmentSettings)
admin.site.site_header = 'Medcy Administration'
admin.site.site_title = 'Medcy Administration'
admin.site.site_url = 'http://localhost:3000/'
