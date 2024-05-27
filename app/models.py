from django.db import models
import datetime

# Create your models here.
class doctor(models.Model):
    Name=models.CharField(max_length=200,null=False,blank=False)
    Password=models.CharField(max_length=20,null=False,blank=False)
    Email=models.EmailField(null=False,blank=False)
    Contact=models.IntegerField(null=False,blank=False)
    DOB=models.DateField(null=False,blank=False)
    Medical_Id=models.IntegerField(null=False,blank=False)
    City=models.CharField(max_length=100,null=False,blank=False)
    Country=models.CharField(max_length=100,null=False,blank=False)
    Specialty=models.CharField(max_length=100,null=False,blank=False)
    Language=models.CharField(max_length=30,null=False,blank=False)
    Profile=models.ImageField(upload_to="images")
    Doctor_id=models.CharField(max_length=10 ,null=False,blank=False,default="")
    permanent=models.CharField(max_length=5,default="False")
    Join=models.CharField(null=False,blank=False,default="---",max_length=11)
    Salary=models.IntegerField(null=False,blank=False)
    Status=models.CharField(null=False,blank=False,default="",max_length=10)
    Gender=models.CharField(null=False,blank=False,default="",max_length=10)

    def __str__(self) -> str:
        return self.Doctor_id

class Patient(models.Model):
    Name=models.CharField(max_length=200,null=False,blank=False)
    Time = models.TimeField(default=datetime.time(16, 00))
    Age=models.IntegerField(null=False,blank=False)
    Email=models.CharField(max_length=30,null=False,blank=False)
    Password=models.CharField(max_length=20,null=False,blank=False,default="")
    Address=models.CharField(max_length=200,null=False,blank=False)
    Contact=models.CharField(max_length=14,null=False,blank=False)
    Disease=models.CharField(max_length=200,null=False,blank=False)
    Blood_Group=models.CharField(max_length=4,null=False,blank=False)
    Doctor=models.CharField(max_length=200,null=False,blank=False)
    Patient_id=models.CharField(max_length=10 ,null=False,blank=False,default="")
    appointed=models.CharField(max_length=5,default="False")
    Date=models.CharField(default='False', max_length=15)
    checked=models.CharField(default="False",max_length=6)
    admitted=models.CharField(default="False",max_length=6)
    discharged=models.CharField(default="False",max_length=6)
    Gender=models.CharField(default="",null=False,max_length=7)
   

    def __str__(self) -> str:
        return self.Patient_id
class admitPatients(models.Model):
        Patient_id=models.CharField(max_length=10 ,null=False,blank=False,default="")
        Admit_Date=models.DateField(null=False)
        Admit_time=models.TimeField(null=False)
        Bed_no=models.IntegerField(null=False,blank=False,default=0)
        Discharge_Date=models.DateField(null=True)
        Doctor_id=models.CharField(default='',max_length=12,null=False)

        def __str__(self):
            return self.Patient_id
class Feedback(models.Model):
     Name=models.CharField(max_length=15,null=False,blank=False,default="")
     Email=models.EmailField(max_length=30,null=False,default="")
     Message=models.CharField(max_length=500,null=False,default="")
     Date=models.CharField(default='', max_length=15)
     def __str__(self):
         return self.Email
class Bill(models.Model):
     Patient_id=models.CharField(max_length=10 ,null=False,blank=False,default="")
     Room_charges=models.IntegerField(default=1200)
     Doctor_charges=models.IntegerField(default=0)
     Medicine_charges=models.IntegerField(default=0)
     Other_charges=models.IntegerField(default=0)
     Amount=models.IntegerField(default=0)
    
     Paid=models.CharField(default='False',max_length=5)
     Date=models.CharField( default="---",max_length=12)
     def __str__(self) -> str:
          return self.Patient_id+"/"+self.Date
     
        

