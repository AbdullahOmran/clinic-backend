from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Doctor, Patient,Secretary

class DoctorAdmin(ModelAdmin):
    list_display = ["id",'username', "age"]

    @admin.display(empty_value="???")
    def username(self, obj):
        return obj.user.username

admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Patient)
admin.site.register(Secretary)
# Register your models here.
