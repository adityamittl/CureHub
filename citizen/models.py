from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class tests(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Insurence(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    price = models.IntegerField()
    Insurence_number= models.CharField(max_length=50)
    def __str__(self):
        return self.name

class citizen_profile(models.Model):
    First_name = models.CharField(max_length=50)
    Last_name = models.CharField(max_length=50)
    sex = models.CharField(max_length=10,default="Male")
    Email = models.EmailField(max_length=50)
    Phone_number = models.CharField(max_length=50)
    Address = models.CharField(max_length=100)
    City = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    Zip_code = models.CharField(max_length=50)
    Country = models.CharField(max_length=50)
    Date_of_birth = models.DateField()
    identity_type = models.CharField(max_length=50)
    identity_number = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', blank=True)
    insured = models.OneToOneField(Insurence, on_delete=models.CASCADE,blank = True)
    def __str__(self):
        return self.First_name


class diagnosis_center(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    regno = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pathologist = models.CharField(max_length=50)
    available_tests = models.ManyToManyField(tests)

    def __str__(self):
        return self.name  

class Hospital(models.Model):
    name = models.CharField(max_length=50)
    regno = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    diagnosisC = models.OneToOneField(diagnosis_center,on_delete=models.CASCADE,null=True,blank = True)
    reg_fees = models.CharField(max_length=100,default=0)
    def __str__(self):
        return self.name

class doctor(models.Model):
    First_name = models.CharField(max_length=50)
    Last_name = models.CharField(max_length=50)
    domain = models.CharField(max_length=100)
    Email = models.EmailField(max_length=50)
    Phone_number = models.CharField(max_length=50)
    Address = models.CharField(max_length=100)
    City = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    Zip_code = models.CharField(max_length=50)
    Country = models.CharField(max_length=50)
    experience = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', blank=True)
    servicing = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    def __str__(self):
        return self.First_name



class Diagnosis(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100,null=True)
    report = models.ImageField(upload_to='report_pics', blank=True)
    remark = models.TextField()
    price = models.IntegerField()
    center = models.ForeignKey(diagnosis_center, on_delete=models.CASCADE, blank=None, null=True)

    def __str__(self):
        return self.name

class prescription(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    taking_instructions = models.CharField(max_length=50)

class bill(models.Model):
    det = models.CharField(max_length=50)
    ammount = models.IntegerField()
    currency = models.CharField(max_length=50)

class Treatment(models.Model):
    date_of_start = models.DateField(default=now)
    name = models.CharField(max_length=50,null=True,blank = True)
    description = models.TextField(null=True,blank = True)
    bill_breakdown = models.ForeignKey(bill, on_delete=models.CASCADE,null=True,blank = True)
    price = models.IntegerField(null=True,blank = True,default=0)
    patient = models.ForeignKey(citizen_profile, on_delete=models.CASCADE)
    Treating_hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    Treating_doctor = models.ForeignKey(doctor, on_delete=models.CASCADE)
    need_diagnosis = models.BooleanField(default=False,blank = True)
    required_tests = models.ManyToManyField(tests,null=True,blank = True)
    Diagnosis_detail = models.ManyToManyField(Diagnosis,null=True,blank = True)
    viewed_report = models.BooleanField(default=False,blank = True)
    meds_duration = models.CharField(max_length=50,null=True,blank = True)
    next_followup = models.DateField(null = True,blank = True)
    date_of_end = models.DateField(null=True, blank=True)
    claimed_ammount = models.IntegerField(default=0,blank = True)
    meds = models.ManyToManyField(prescription, null=True,blank = True)
    done_checkup = models.BooleanField(default=False,blank = True) 
    waiting_fore_reports = models.BooleanField(default=False,blank = True)

    def __str__(self):
        return str(self.patient.First_name)


class login_mode(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    verified = models.BooleanField(default=False)

