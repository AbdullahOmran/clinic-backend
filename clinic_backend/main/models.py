from django.db import models
from django.contrib.auth.models import User
import datetime
import uuid
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_delete
import os





# Create your models here.
class Doctor(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER = {
        MALE: 'Male',
        FEMALE: 'Female',
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    gender = models.CharField(max_length =1, choices=GENDER, default=MALE)
    address = models.CharField(max_length=255, null =True, blank =True)
    education = models.TextField(null=True, blank =True)
    experience = models.TextField(null=True, blank =True)
    specialization = models.CharField(max_length=255,null=True)
    contact_number = models.CharField(max_length=20,null=True, blank =True)
    date_of_birth = models.DateField(null=True, blank =True)
    image = models.ImageField(upload_to='images/doctors/',null=True, blank =True)
    is_retired = models.BooleanField(default = False)
    is_on_vacation = models.BooleanField(default = False)

    @property
    def age(self):
        if self.date_of_birth is None: return None
        today_date = datetime.date.today()
        time_delta = today_date - self.date_of_birth
        age = time_delta.days // 365
        return age

    def __str__(self):
        return self.user.username


@receiver(pre_delete, sender=Doctor)
def delete_image(sender, instance, **kwargs):
    # Before deleting the record, delete the associated image file
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class Patient(models.Model):

    MALE = 'M'
    FEMALE = 'F'
    GENDER = {
        MALE: 'Male',
        FEMALE: 'Female',
    }
    A_POSITIVE = 'A+'
    B_POSITIVE = 'B+'
    AB_POSITIVE = 'AB+'
    O_POSITIVE = 'O+'
    O_NEGATIVE = 'O-'
    A_NEGATIVE = 'A-'
    B_NEGATIVE = 'B-'
    AB_NEGATIVE = 'AB-'
    BLOOD_GROUPS = {
         A_POSITIVE : 'A+',
    B_POSITIVE : 'B+',
    AB_POSITIVE: 'AB+',
    O_POSITIVE : 'O+',
    O_NEGATIVE : 'O-',
    A_NEGATIVE : 'A-',
    B_NEGATIVE : 'B-',
    AB_NEGATIVE : 'AB-',
    }
    SINGLE = 'S'
    MARRIED = 'M'
    MARITAL_STATUS = {
     SINGLE:'Single',
     MARRIED:'Married',
    }
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    first_name = models.CharField(max_length=255,null=True)
    last_name = models.CharField(max_length=255,null=True)
    gender = models.CharField(max_length =1, choices=GENDER, default=MALE)
    address = models.CharField(max_length=255, null =True, blank =True)
    education = models.TextField(null=True, blank =True)
    occupation = models.TextField(null=True, blank =True)
    surgical_history = models.TextField(null=True, blank =True)
    present_illness_history = models.TextField(null=True, blank =True)
    medical_history = models.TextField(null=True, blank =True)
    medications = models.TextField(null=True, blank =True)
    allergies = models.TextField(null=True, blank =True)
    immuzinations = models.TextField(null=True, blank =True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS, null=True, blank =True)
    date_of_birth = models.DateField(null=True, blank =True)
    contact_number = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True, blank =True)
    marital_status = models.CharField(max_length=1,choices=MARITAL_STATUS,default=SINGLE)

    

    @property
    def age(self):
        if self.date_of_birth is None: return None
        today_date = datetime.date.today()
        time_delta = today_date - self.date_of_birth
        age = time_delta.days // 365
        return age

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()   

    def __str__(self):
        return str(self.id)

class Secretary(models.Model):

    class Meta:
        verbose_name_plural = "Secretaries"

    MALE = 'M'
    FEMALE = 'F'
    GENDER = {
        MALE: 'Male',
        FEMALE: 'Female',
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    gender = models.CharField(max_length =1, choices=GENDER, default=MALE)
    address = models.CharField(max_length=255, null =True, blank =True)
    education = models.TextField(null=True, blank =True)
    experience = models.TextField(null=True, blank =True)
    contact_number = models.CharField(max_length=20,null=True, blank =True)
    date_of_birth = models.DateField(null=True, blank =True)
    image = models.ImageField(upload_to='images/secretaries/',null=True, blank =True)
    is_retired = models.BooleanField(default = False)
    is_on_vacation = models.BooleanField(default = False)

    @property
    def age(self):
        if self.date_of_birth is None: return None
        today_date = datetime.date.today()
        time_delta = today_date - self.date_of_birth
        age = time_delta.days // 365
        return age

    def __str__(self):
        return self.user.username


@receiver(pre_delete, sender=Secretary)
def delete_image(sender, instance, **kwargs):
    # Before deleting the record, delete the associated image file
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class Clinic(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null =True)
    address = models.CharField(max_length=255, null =True)
    city = models.CharField(max_length=255, null =True)
    state = models.CharField(max_length=255, null =True)
    contact_number = models.CharField(max_length=20,null=True)
    doctor = models.ManyToManyField(Doctor)
    Secretary = models.ManyToManyField(Secretary)

class Appointment(models.Model):
    PENDING= 'P'
    ACCEPTED= 'A'
    REJECTED= 'R'
    SCHEDULED= 'S'
    INSPECTION = 'I'
    CONSULTATION = 'C'
    TYPES={
        INSPECTION:'New inspection',
        CONSULTATION:'Consultation'
    }
    STATUS = {
     PENDING: 'Pending',
     ACCEPTED: 'Accepted',
     REJECTED: 'Rejected',
     SCHEDULED: 'Scheduled',
    }
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    secretary = models.ForeignKey(Secretary, on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL,null=True)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    status = models.CharField(max_length=255, default=SCHEDULED, choices=STATUS)
    appointment_type = models.CharField(max_length=255, default=INSPECTION, choices=TYPES)
    notes = models.TextField(null = True,blank=True)

class WorkingSchedule(models.Model):
    SATURDAY = 'SAT'
    SUNDAY = 'SUN'
    MONDAY = 'MON'
    TUESDAY = 'TUE'
    WEDNESDAY = 'WED'
    THURSDAY = 'THU'
    FRIDAY = 'FRI'
    DAYS={
        SATURDAY:'SAT',
        SUNDAY:'SUN',
        MONDAY:'MON',
        TUESDAY:'TUE',
        WEDNESDAY:'WED',
        THURSDAY:'THU',
        FRIDAY:'FRI',
    }
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True,blank=True)
    secretary = models.ForeignKey(Secretary, on_delete=models.SET_NULL, null=True,blank=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    day = models.CharField(max_length=3,choices=DAYS,null=True)

class Encounter(models.Model):
    pass

class Prescription(models.Model):
    date = models.DateField(null=True)
    encounter = models.OneToOneField(Encounter,null=True,on_delete=models.CASCADE)
    width = models.PositiveIntegerField(default=210)
    height = models.PositiveIntegerField(default=297)
    background_image = models.ImageField(upload_to='images/prescriptions/',null=True,blank=True)
class MedicationsStore(models.Model):
    class Meta:
        verbose_name = "medication"
        verbose_name_plural = "Medications Store"
    OTHER = '0'
    TOPICAL = '1'
    ORAL = '2'
    ROUTES  = {
        OTHER: 'Other',
        ORAL: 'Oral',
        TOPICAL: 'Topical',
    }
    name = models.CharField(max_length=255, null=True)
    route = models.CharField(max_length=1, default=OTHER, choices=ROUTES)
    image = models.ImageField(upload_to='images/medications/',null=True,blank=True)

class Medication(models.Model):
    medication = models.OneToOneField(MedicationsStore, on_delete=models.SET_NULL, null=True)
    dosage = models.CharField(max_length=255,null=True)
    frequency = models.CharField(max_length=255,null=True)
    duration = models.CharField(max_length=255,null=True)

class Treatment(models.Model):
    pass