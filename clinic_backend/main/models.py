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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length =1, choices=GENDER, default=MALE)
    address = models.CharField(max_length=255, null =True, blank =True)
    education = models.TextField(null=True, blank =True)
    experience = models.TextField(null=True, blank =True)
    specialization = models.CharField(max_length=255)
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
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null =True)
    address = models.CharField(max_length=255, null =True)
    city = models.CharField(max_length=255, null =True)
    state = models.CharField(max_length=255, null =True)
    contact_number = models.CharField(max_length=20,null=True)