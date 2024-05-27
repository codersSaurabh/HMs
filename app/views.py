from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User 
from .models import doctor,Patient,admitPatients,Feedback,Bill
import re
from django.conf import settings
from datetime import date,timedelta,datetime
import os
import pyotp
import smtplib
from django.core.files import File
from django.core.files.storage import FileSystemStorage
#sending mail
def sendmail(msg,receiver):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('saurabh544321@gmail.com' , 'toot jqsg pdhe fadh')
    server.sendmail("saurabh544321@gmail.com",receiver,msg)
    print("mailed")
#salary of doctors
doctor_salary={"Cardiologists":50000,"Dentist":45000,"Heart Specialist":100000,"Dermatologists":60000,"Neurologists":70000,
               "Surgeon":120000,"Eye Specialist":67000,"Psychiatrists":80500,"Gyncologists":75000,"Radiologists":60000,
               "Nephrologists":55000,"Pathologists":56000,"Oncologists":68000}
Room_charges=1200
doctor_charges={"Psychiatrists":850,"Gyncologists":700,"Radiologists":1000,"Nephrologists":600,
                 "Cardiologists":100,"Dentist":700,"Heart Specialist":1500,"Neurologists":800,
                 "Surgeon":1200,"Eye Specialist":600,"Dermatologists":1500,"Pathologists":1000,"Oncologists":900}
Total_Beds=100
#for doctor opt validation 
OTpRequired={}
#Check check valid age
def checkAge(age):
    try:
        if(age.isalpha() or (int(age)<1 or int(age)>150)):
            return False
        else:
            return True
    except Exception as e:
        # print(e)
        return False
#-------------------------------------------------------------------#
# Create your views here.
#find age
def age_calculator(birthdate):
   today = datetime.today()
   age = (today - birthdate) // timedelta(days=365.2425)
   return age
#take otp from user
def otptaker(request):
    data=doctor.objects.filter(permanent="True",Status="Working").values()
    global OTpRequired
    try:
        
        if(request.method=="POST"):
            id=request.POST.get("id")
            Eotp=request.POST.get("Eotp","")
            try:
                if(OTpRequired[id][1]==Eotp):
                    object=OTpRequired[id][0]
                    
                    # print(object.Profile)
                    if("DOC" in id):
                        file_name = os.path.basename(OTpRequired[id][2])
                        object.Profile=file_name  
                    Email=object.Email 
                    object.save()
                    length=len(OTpRequired[id])
                    del OTpRequired[id]
                    if("DOC" in id):
                        msg=f"Dear {object.Name},\n Your id is: {id}\nYour account will be checked by our team till then stay updated\nRegards\nAdmin\n[AIMS]"
                        try:
                            sendmail(msg,Email)
                        except Exception as e:
                                return render(request,"registration.html",{'msg':"Check Your Internet Connection!!",'thank':True,"color":"red","doctor_salary":doctor_salary.keys()})

                        object.save()
                        return render(request,"registration.html",{'msg':"Detailed has been submitted successfully!!",'thank':True,"color":"green","doctor_salary":doctor_salary.keys()})

                    else:
                        if(length==3):
                            dicts={'msg':"Detailed has been submitted successfully!!",'thank':True,'color':'success'}
                            return OurDoctor(request,dic=dicts)

                        return render(request,"patientform.html",{"doctors":data,'msg':"Detailed has been submitted successfully!!",'thank':True,'color':'green'})
                else:
                    length=len(OTpRequired[id])
                    if("DOC" in id and(length<3)):
                        return render(request,"registration.html",{'msg':"OTP is not correct Try again!!",'thank':True,'color':'red',"doctor_salary":doctor_salary.keys()})
                    else:
                        if(length==3):
                                dicts={'msg':"OTP is not correct Try again!!",'thank':True,'color':'warning'}
                                return OurDoctor(request,dic=dicts)
        
                        return render(request,"patientform.html",{"doctors":data,'msg':"OTP is not correct Try again!!",'thank':True,'color':'red'})
            except Exception as e:
                return HttpResponse("<center><h3>You are trying to submit details again <br> go home <a href='/'>click</a></h3></center>")

    except Exception as e:
        
            length=len(OTpRequired[id])
            
            if("DOC" in id and(length<3)):
                    return render(request,"registration.html",{'msg':"Something is wrong Please try again !!",'thank':True,'color':'red',"doctor_salary":doctor_salary.keys()})
      
            else:
                 if(length==3):
                    dicts={'msg':"Something is wrong Please try again !!",'thank':True,'color':'warning'} 
                    return OurDoctor(request,dic=dicts)
                
                 return render(request,"patientform.html",{"doctors":data,'msg':"omething is wrong Please try again !!",'thank':True,'color':'red'})
#calling aboutUs
def aboutUs(request):
    return render(request,"about1.html")
#calling home page
def home(request):
    return render(request,"home.html")
#login admin
def adminIn(request):
    if 'user' in request.session:
         #retaining the user looged in
         username = request.session['user']
        #  return HttpResponse("<h1>Hi"+current_user+"</<h1><a href='/AdminLogout/'> <button  class='btn'>LogOut</button></a>")
         Patients=Patient.objects.all().values()
         length=0+len(Patient.objects.filter(appointed="True",checked="False",admitted="False").values())
         doctors=doctor.objects.all().values()
         if(len(doctors)-3<0):
            doctors=doctors[0:len(doctors)]
         else:
            doctors=doctors[len(doctors)-3:len(doctors)]
         if(len(Patients)-3<0):
            Patients=Patients[0:len(Patients)]
         else:
            Patients=Patients[len(Patients)-3:len(Patients)]
         for i in Patients:
            try:
                Doctor=doctor.objects.filter(Doctor_id=i["Doctor"]).values("Name")
                i["dName"]=Doctor[0]["Name"]
            except Exception as e:
                i["dName"]="Not found"
    
        
         totalPatient=0+len(Patient.objects.filter(admitted="True",discharged="False").values())
         dlength=0+len(doctor.objects.filter(permanent="True",Status="Working").values())
         param={"data":username,"appointment":length,"doctors":dlength,"Patient":totalPatient,"Rpatient":Patients,"Rdoctors":doctors}
         return render(request,"adportal.html",param)
    if(request.method=='POST'):
    
        username = request.POST.get("username","")  
        password = request.POST.get("password","")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user'] = username
            
            #return admin page
            #return HttpResponse("<h1>Hi"+username+"</<h1><a href='/AdminLogout/'> <button  class='btn'>LogOut</button></a>")
            Patients=Patient.objects.all().values()
            length=0+len(Patient.objects.filter(appointed="True",checked="False",admitted="False").values())
            doctors=doctor.objects.all().values()
            if(len(doctors)-3<0):
                doctors=doctors[0:len(doctors)]
            else:
                doctors=doctors[len(doctors)-3:len(doctors)]
            if(len(Patients)-3<0):
                Patients=Patients[0:len(Patients)]
            else:
                Patients=Patients[len(Patients)-3:len(Patients)]
            for i in Patients:
                try:
                    Doctor=doctor.objects.filter(Doctor_id=i["Doctor"]).values("Name")
                    i["dName"]=Doctor[0]["Name"]
                except Exception as e:
                   i["dName"]="Not found"
        
            
            totalPatient=0+len(Patient.objects.filter(admitted="True",discharged="False").values())
            dlength=0+len(doctor.objects.filter(permanent="True",Status="Working").values())
            param={"data":username,"appointment":length,"doctors":dlength,"Patient":totalPatient,"Rpatient":Patients,"Rdoctors":doctors}
            return render(request,"adportal.html",param)
            
            
        else:
            return render(request,'login.html',{'msg':'username or password is not valid'})
    return render(request,'login.html')
#calling admin tab from navbar
def admin(request):
    if 'user' in request.session:
         #retaining the user looged in
         username = request.session['user']
        #  return HttpResponse("<h1>Hi"+current_user+"</<h1><a href='/AdminLogout/'> <button  class='btn'>LogOut</button></a>")
         Patients=Patient.objects.all().values()
         length=0+len(Patient.objects.filter(appointed="True",checked="False",admitted="False").values())
         doctors=doctor.objects.all().values()
         if(len(doctors)-3<0):
            doctors=doctors[0:len(doctors)]
         else:
            doctors=doctors[len(doctors)-3:len(doctors)]
         if(len(Patients)-3<0):
            Patients=Patients[0:len(Patients)]
         else:
            Patients=Patients[len(Patients)-3:len(Patients)]
         for i in Patients:
            try:
                Doctor=doctor.objects.filter(Doctor_id=i["Doctor"]).values("Name")
                i["dName"]=Doctor[0]["Name"]
            except Exception as e:
                pass
    
        
         totalPatient=0+len(Patient.objects.filter(admitted="True",discharged="False").values())
         dlength=0+len(doctor.objects.filter(permanent="True",Status="Working").values())
         param={"data":username,"appointment":length,"doctors":dlength,"Patient":totalPatient,"Rpatient":Patients,"Rdoctors":doctors}
         return render(request,"adportal.html",param)
            
    else:
        return render(request,'admin.html')
#change password of admin
def forgetAdmin(request):
    if(request.method=='POST'):
    
        username = request.POST.get("username","")  
        password = request.POST.get("password","")
        repassword=request.POST.get('repassword',"")
        if(password==repassword):
            try:
                user=User.objects.get(username=username)
                if(user):
                    user.set_password(password)
                    user.save()
            except Exception as e:
                return render(request,"adminReset.html",{'msg':'username not define!!'})
        else:
         return render(request,"adminReset.html",{'msg':"Pssword don't match!!"})
    return render(request,"adminReset.html")
#logout admin
def logoutAdmin(request):
    try:
        del request.session['user']
    except:
        return redirect("/")
    return redirect("/")
#admin appointments portal
def Aappointments(request,day):
    if(day=="all"):
        data=Patient.objects.all().values()
    else:
        date=datetime.today().strftime("%Y-%m-%d")
        data=Patient.objects.filter(Date=date).values()
   
    for i in data:
        
        Doctor=doctor.objects.filter(Doctor_id=i["Doctor"]).values("Name")
        try:
            i["dName"]=Doctor[0]["Name"]
        except Exception as e:
            i["dName"]="Not found"
    data=list(data)
    data.reverse()
    return render(request,"Aappointments.html",{"data":data,"day":day})
# confirmpatient
def confirmpatient(request,pid,day):
     data=Patient.objects.get(Patient_id=pid)
     doctors=doctor.objects.get(Doctor_id=data.Doctor)
     patient=Patient.objects.filter(Date=data.Date,Doctor=data.Doctor,appointed=True).values()
     date=datetime.strptime(data.Date, "%Y-%m-%d")
     Rtime=data.Time
     ct=datetime.now().time()
     if(ct>Rtime and date.date()==datetime.today().date()):
         date+=timedelta(1)
         if(date.weekday()==6):
            date+=timedelta(1)
         patient=Patient.objects.filter(Date=data.Date,Doctor=data.Doctor,appointed=True).values() 
     while(len(patient)>=27):
            date+=(timedelta(1))
 
            patient=Patient.objects.filter(Date=date,Doctor=data.Doctor,appointed=True).values()
     Rtime=datetime.strptime(str(Rtime),"%H:%M:%S")
     minute=Rtime.minute
     minute=(15-(minute%15))  
     if((minute%15)!=0):
      Rtime+=timedelta(minutes=minute)  
     if(datetime.strptime(data.Date,"%Y-%m-%d").date()==date.date() and (len(Patient.objects.filter(Date=data.Date,Time=Rtime,appointed=True,Doctor=data.Doctor))==0)):
             
           Rtime=Rtime        
     else:
        while(len(Patient.objects.filter(Date=datetime.strftime(date,"%Y-%m-%d"),Time=Rtime.time(),appointed=True,Doctor=data.Doctor))!=0):
            if(Rtime==datetime.strptime("12:45:00","%H:%M:%S")):
                Rtime+=timedelta(hours=1,minutes=15)
            elif(Rtime==datetime.strptime("16:45:00","%H:%M:%S")):
                date+=timedelta(1)
                Rtime=datetime.strptime("9:00:00","%H:%M:%S")
                if(date.weekday()==6):
                    date+=timedelta(1)
            else:
                Rtime+=timedelta(minutes=15)   
            
     data.Date=date.strftime("%Y-%m-%d") 
     data.Time=Rtime
     data.appointed=True
     data.save()
     
     msg="Appointment of {0} has been approved with doctor {1} on {2} at '{3}'. by Hospital.\nUsername: {4} \nPassword: {5}.\nYou can came to hospital on appointed date and make sure that you are on appointed time. \nThank You for Choosing us Stay\
Safe. \n\nWith Regards\nAIIMS".format(data.Name,doctors.Name,data.Date,Rtime.strftime("%H-%M") ,data.Email,data.Password)
     Email=data.Email
     try:
        sendmail(msg,Email)
     except Exception as e:
        pass
     if("DOC" in day):
         return TodayAppointment(request,doctors.Doctor_id,day)
     return redirect("/Aappointments/"+day)
#doctors in admin
def Adoctors(request):
    data=doctor.objects.all().values()
    data=list(data)
    data.reverse()
    return render(request,"Adoctors.html",{"data":data})
 #confirm doctor
def ConfirmDoctor(request,did):
    data=doctor.objects.get(Doctor_id=did)
    data.permanent=True
    data.Join=datetime.today().strftime("%d-%m-%Y")
    data.Status="Working"
    data.save()
    msg=f"Dear {data.Name},\nWe are pleased to inform you that your application for the rol of {data.Specialty} at Aims has been approved.\n\
Your account has been activated, and you can now access all the privileges and benefits of membership.\
\n\n\nWe believe that your expertise and experience will be valuable assets to our hospital and the patients we serve.\
We look forward to working with you and to the contributions you will make to our healthcare community. If you have\
    any questions or need assistance, please do not hesitate to contact us.\
\nDoctor_Id: {did} \nPassword: {data.Password} \n  \
\nOnce again, congratulations on your membership approval. We are excited to have you on board.\n\n\n\n\n\nBest regards\nAdmin\n[AIMS]"
    Email=data.Email
    try:
        sendmail(msg,Email)
    except Exception as e:
        pass
    return Adoctors(request)
#delelte doctor
def DeleteDoctor(request,did):
    data=doctor.objects.get(Doctor_id=did)
    if(data.permanent=="False"):
        email=data.Email
        data.delete()
    else:
       email=data.Email
       data.Status="Left"
       data.save()

    
    msg=f"Dear Dr. {data.Name},\n\nI hope this message finds you well. I am writing to inform you that effective {datetime.today().strftime("%d-%m-%Y")}, you will no longer be serving as a doctor at our hospital. We appreciate the dedication and expertise you have brought to our team during your time here.\
    \n\n\nYour contributions have been invaluable, and while we are sad to see you go, we understand that transitions are a natural part of professional life. We wish you all the best in your future endeavors, both personally and professionally.\
    \n\n\nPlease let us know if there are any outstanding matters or administrative tasks that require attention before your departure date. Additionally, if you need any assistance with transitioning your patients or responsibilities, we are here to support you.\
    \n\n\nOnce again, thank you for your service to our hospital. We extend our sincerest wishes for your continued success and fulfillment in your career.\
    \n\n\nBest regards,\
    \n\n\nAdmin\nAIMS"
    try:
        sendmail(msg,email)
        
    except Exception as e:
        pass

    return Adoctors(request)
#patient in admin
def Apatients(request,thank="False"):
    data=Patient.objects.filter(admitted="True",discharged="False").values()
    for i in data:
        Doctor=doctor.objects.filter(Doctor_id=i["Doctor"]).values("Name")
        Admit=admitPatients.objects.filter(Patient_id=i["Patient_id"]).values("Admit_Date","Bed_no")
        try:
            i["dName"]=Doctor[0]["Name"]
           
        except Exception as e:
            i["dName"]="Not found"
        i["Bed_no"]=Admit[0]["Bed_no"]
        i["aDate"]=Admit[0]["Admit_Date"]
    data=list(data)
    data.reverse()
    return render(request,"Apatient.html",{"data":data,"thank":thank})
#discharge patient from admiin
def AdischargedPatient(request,pid):
     Discharged_Date = datetime.now()
     Discharged_Date=  Discharged_Date.strftime('%Y-%m-%d')
     data=Patient.objects.get(Patient_id=pid)
     bill=Bill.objects.filter(Patient_id=pid,Date=Discharged_Date).values()
     if(len(bill)==0 or bill[0]["Paid"]=="False"):
         #Today bill not recieved first recieved the bill
         return Apatients(request,"True")
     else:
        data.discharged=True
        data.save()
        msg=f"{data.Name} has been Discharged from Hospital. \n Thank You for Choosing us Stay Safe "
        Email=data.Email
        try:
            sendmail(msg,Email)
        except Exception as e:
            pass
        admitPatient=admitPatients.objects.get(Patient_id=pid)
        admitPatient.Discharge_Date=Discharged_Date
        admitPatient.save()
        return Apatients(request,"False")
    #  
    #  return redirect("/Adischarged/")
#generate bill  on discharging patient
def Genbil(request,pid,day):
    global Room_charges
    if(request.method=="POST"):
    #    print("hello")
       Room_charge=Room_charges
       patient=Patient.objects.filter(Patient_id=pid).values("Doctor")
       Doctor=doctor.objects.filter(Doctor_id=patient[0]["Doctor"]).values("Specialty")
       Doctor=doctor_charges.get(Doctor[0]["Specialty"],0)
       medicine=int(request.POST.get("medicine-cost",0))
       other=int(request.POST.get("other-charges",0))
       date=datetime.today().strftime("%Y-%m-%d")
       time=datetime.now().strftime("%H:%M:%S")
       if(time<"10:00:00"):
           Room_charge=0
       
       Amount=Room_charge+Doctor+medicine+other
       bill=Bill(Date=date,Patient_id=pid,Room_charges=Room_charge,Doctor_charges=Doctor,Medicine_charges=medicine,Other_charges=other,Amount=Amount)
       if(len(Bill.objects.filter(Patient_id=pid,Date=date))>0):
           return HttpResponse("<center><h2>Bill has been already Generated</h2></center>")
       bill.save()
       return redirect("/BillList/"+day)
    else:
        print(day)
        date=datetime.today().strftime("%d-%m-%Y")
        return render(request,"genbil.html",{"id":pid,"date":date,"day":day})
#show bill and download it
def showbill(request,pid,day="all"):
        path=request.path
        try:
           
            data=Patient.objects.filter(Patient_id=pid).values("Name","Contact","Address","Doctor","Disease")
            doctors=doctor.objects.filter(Doctor_id=data[0]["Doctor"]).values("Name")
            detail=admitPatients.objects.filter(Patient_id=pid).values()
            if(day=="today"):
                
                
                date=datetime.today().strftime("%Y-%m-%d")
                
                bill=Bill.objects.filter(Patient_id=pid,Date=date).values()
                Balance=0
                for i in bill:
                    if(i["Paid"]=="False"):
                        Balance=i["Amount"]
                    i["Balance"]=Balance

                        
                param={"data":data[0],"Doctor":doctors[0],"date":date,"bill":bill[0],"detail":detail[0],"day":day}
                return render(request,"billing.html",param)
            else:
                Rcharge=0
                Dcharge=0
                Ocharge=0
                Mcharge=0
                total=0
                Balance=0
                if(request.method=="POST"):
                     from_Date=request.POST.get("from",0)
                     
                     to_Date=request.POST.get("to",0)
                     
                     if(from_Date=="" or to_Date==""): 
                        #  return redirect("/SearchPatient/False")
                        return SearchPatient(request,"False",pid)
                     else:
                         from_Date=datetime.strptime(from_Date,"%Y-%m-%d")
                         to_Date=datetime.strptime(to_Date,"%Y-%m-%d")
                         
                         if(from_Date>to_Date):
                             return redirect("/SearchPatient/False")
                         to_date=to_Date.date()
                         from_date=from_Date

                         while(from_Date <= to_Date):
                            
                            
                            bill=Bill.objects.filter(Patient_id=pid,Date=from_Date.date()).values()
                            
                            for i in bill:
                                to_date=i["Date"]
                                Rcharge+=i["Room_charges"]
                                Dcharge+=i["Doctor_charges"]
                                Ocharge+=i["Other_charges"]
                                Mcharge+=i["Medicine_charges"]
                                total+=i["Amount"]
                                if(i["Paid"]=="False"):
                                    Balance+=i["Amount"]
                               
                            from_Date+=(timedelta(1))
                         bill=[{"Room_charges":Rcharge,"Doctor_charges":Dcharge,"Other_charges":Ocharge,"Medicine_charges":Mcharge,"Amount":total,"Balance":Balance}]
                         param={"data":data[0],"Doctor":doctors[0],"date":f"{from_date.date()} - {to_date}","bill":bill[0],"detail":detail[0],"day":day}

                         return render(request,"billing.html",param)
                if(detail[0]["Discharge_Date"]==None):
                    today=datetime.today().strftime("%Y-%m-%d")
                else:
                    
                    today=detail[0]["Discharge_Date"]
                days=(today-detail[0]["Admit_Date"]).days
                bill=Bill.objects.filter(Patient_id=pid).values()
                
               
                for i in bill:
                    
                    Rcharge+=i["Room_charges"]
                    Dcharge+=i["Doctor_charges"]
                    Ocharge+=i["Other_charges"]
                    Mcharge+=i["Medicine_charges"]
                    total+=i["Amount"]
                    if(i["Paid"]=="False"):
                        Balance+=i["Amount"]
                
                bill=[{"Room_charges":Rcharge,"Doctor_charges":Dcharge,"Other_charges":Ocharge,"Medicine_charges":Mcharge,"Amount":total,"Balance":Balance}]

                
                param={"data":data[0],"Doctor":doctors[0],"days":days,"bill":bill[0],"date":today,"detail":detail[0],"day":day}
            if(total!=0):
             return render(request,"billing.html",param)
            else:
               raise(KeyError)

        
        except Exception as e:
           print(e)
           print(path)
           if ("/Pappointment/" in   path or "/Pdischarge" in path):
               
               return render(request,"BillMessage.html",{"msg":"Bill"})
           print("hello")
           return render(request,"BillNotFound.html",{"pid":pid,"day":day})
#on pay bill clicked
def PayBill(request,pid,day):
    ob=Bill.objects.get(Patient_id=pid,Date=datetime.today().strftime("%Y-%m-%d"))
    ob.Paid="Paid"
    ob.save()
    return redirect("/BillList/"+day)
#Bill List
def BillList(request,day):

    data=Patient.objects.filter(admitted="True").values()

    if(day=="all"):
       datas=Patient.objects.filter(admitted="True").values()
       for i in datas:
           bill=Bill.objects.filter(Patient_id=i["Patient_id"]).values("Amount","Paid")
           Total=0
           Balance=0
           for j in bill:
               Total+=j["Amount"]
               if(j["Paid"]=="False"):
                   Balance+=j["Amount"]
           i["Total"]=Total
           i["Balance"]=Balance
           bed=admitPatients.objects.filter(Patient_id=i["Patient_id"]).values("Bed_no")
           i["bed"]=bed[0]["Bed_no"]
        


           
    else:
        date=datetime.today().strftime("%Y-%m-%d")
        
        
        data=list(data)
        datas=[]
       
        for i in (data):
            if(i["discharged"]=="True"):
                # print(len(data))
                detail=admitPatients.objects.get(Patient_id=i["Patient_id"])
                
                # print(detail.Discharge_Date)
                Date=(detail.Discharge_Date).strftime("%Y-%m-%d")
                
                if( Date!=date ):
                    # print(detail.Discharge_Date)
                    continue

            
            # print(detail.Discharge_Date) 
           
            
            bill=Bill.objects.filter(Date=date,Patient_id=i["Patient_id"]).values()
            bed=admitPatients.objects.filter(Patient_id=i["Patient_id"]).values("Bed_no")
            try:
                i["bed"]=bed[0]["Bed_no"]
                i["Bill"]=bill[0]["Amount"]
                i["Paid"]=bill[0]["Paid"]
            except Exception as e:
                i["bed"]=bed[0]["Bed_no"]
                i["Bill"]=" "
                i["Paid"]=" "
            finally:
                # datas.append(0)
                datas.append(i)
                
                
            # print(datas)
    datas=list(datas)
    datas.reverse()
    return render(request,"TodayBill.html",{"data":datas,"day":day})
#discharged patient in admin
def Adischarged(request):
    data=Patient.objects.filter(discharged=True,).values()
    for i in data:
        Doctor=doctor.objects.filter(Doctor_id=i["Doctor"]).values("Name")
        date=admitPatients.objects.filter(Patient_id=i["Patient_id"]).values("Discharge_Date","Admit_Date")
       
        try:
             i["dDate"]=date[0]["Discharge_Date"]
             i["aDate"]=date[0]["Admit_Date"]
             i["dName"]=Doctor[0]["Name"]
        except Exception as e:
            i["dName"]="Not found"
    data=list(data)
    data.reverse()
    return render(request,"Adischarged.html",{"data":data,"date":date})
#feedback form data
def feedback(request):
    if(request.method=="POST"):
        Name=request.POST.get("name","")
        Email=request.POST.get("email","")
        Message=request.POST.get("message","")
        Date = datetime.now()
        Date=Date.strftime('%Y-%m-%d')
        # print(Name,Email,Message)
        Feedbacks=Feedback(Name=Name,Email=Email,Message=Message,Date=Date)
        Feedbacks.save()
        msg="Thank you for giving your feedback.\n Take care and Be Safe"
        try:
            sendmail(msg,Email)
            return render(request,'Feedback.html',{'msg':'Thank you for submitting your feedback','thank':True})
        except Exception as e:
                 return render(request,"Feedback.html",{'msg':" Email is not valid!!",'thank':True,"color":"red"})

        
    return render(request,"feedback.html")
#ShowFeedback to admin
def ShowFeedback(request):
    data=Feedback.objects.all().values()
    return render(request,"ShowFeedback.html",{"data":data})
#login doctor
def doctorlogin(request):
    if('doctor' in request.session ):
        #return to doctor page
        user=request.session['doctor']
        data=doctor.objects.filter(Doctor_id=user).values()[0]
       
        Patients=Patient.objects.filter(Doctor=user,appointed="True",admitted="False",checked="False").values()
        patient=0+len(Patient.objects.filter(Doctor=user,admitted="True",discharged="False").values())
        discharge=0+len(Patient.objects.filter(Doctor=user,discharged="True").values())

        length=0+len(Patient.objects.filter(Doctor=user,appointed="True",admitted="False",checked="False").values())
        if(length-3<0):
            last=0
        else:
            last=length-3
        stat=[length,patient,discharge]
        
        param={"data":data,"stat":stat,"Patient":Patients[last:length],}

        
        return render(request,"doctorportal.html",param)
    else:
         if(request.method=='POST'):
            
            Doctor_id = request.POST.get("doctorId","") 
            password = request.POST.get("password","")

            data=doctor.objects.filter(Doctor_id=Doctor_id,Password=password).values() 
            if(len(data)==1):
                if(data[0]['permanent']=="False"):
                    return render(request,"message.html",{"msg":"account"})
                else:
                    request.session['doctor'] = Doctor_id
                    #redirect to doctor page
                    data=doctor.objects.filter(Doctor_id=Doctor_id).values()[0]
                    Patients=Patient.objects.filter(Doctor=Doctor_id,appointed="True",admitted="False",checked="False").values()
                    patient=0+len(Patient.objects.filter(Doctor=Doctor_id,admitted="True",discharged="False").values())
                    discharge=0+len(Patient.objects.filter(Doctor=Doctor_id,discharged="True").values())
                    length=0+len(Patient.objects.filter(Doctor=Doctor_id,appointed="True",admitted="False",checked="False").values())

                    if(length-3<0):
                        last=0
                    else:
                        last=length-3
                    stat=[length,patient,discharge]
                    
                    param={"data":data,"stat":stat,"Patient":Patients[last:length]}

                    
                    return render(request,"doctorportal.html",param)
                            
            else:
               
                 return render(request,'doctorlogin.html',{'msg':'username or password is not valid','thank':True})
                
    return render(request,"doctorlogin.html")
#doctor registration
def doctorRegister(request):
    global image
    if(request.method=="POST"):
        Name=request.POST.get("name","")
        Email=request.POST.get("email","")
        Password=request.POST.get("password","")
        City=request.POST.get("city","")
        Country=request.POST.get("country","")
        Language=request.POST.get("language","")
        DOB=request.POST.get("dob","")
        y,m,d=DOB.split("-")
        DOB = datetime(int(y),int(m),int(d))
        gender=request.POST.get("gender","")
        Contact=request.POST.get("contact","")
        specialty=request.POST.get("specialty","")
        Profile=request.FILES['image']
        id=(doctor.objects.all().values("id"))
        

        doctor_id="DOC"+str(100+(id[len(id)-1]["id"])+1)
        Medical_Id=request.POST.get("medicalId","")
       
        if(age_calculator(DOB)>21 and age_calculator(DOB)<60):
            if(len(doctor.objects.filter(Medical_Id=Medical_Id).values())!=0 or len(doctor.objects.filter(Email=Email).values())!=0):
                #return a message that id is already exist
                return render(request,"registration.html",{'msg':"Medical ID or Email already exist!!",'thank':True,"color":"red","doctor_salary":doctor_salary.keys()})
            else:
                fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                filename = fs.save(Profile.name, Profile)
                file_url = fs.url(filename)
                totp_secret = pyotp.random_base32()
                # Create a TOTP object
                totp = pyotp.TOTP(totp_secret)
                # Generate the OTP
                otp = totp.now()
                msg=f"Dear {Name}, \n Your one time password is {otp} , It will be valid for 60 seconds \n\n\n\n Thank You."

                try:
                    sendmail(msg,Email)
                    Doctor=doctor(Salary=doctor_salary.get(specialty,0),Gender=gender,Name=Name,Password=Password,Email=Email,City=City,Country=Country,Language=Language,
                        Doctor_id=doctor_id,DOB=DOB,Specialty=specialty,Medical_Id=Medical_Id,Contact=int(Contact),Profile=Profile)
                    OTpRequired[doctor_id]=[Doctor,otp,file_url]
                    
                    return render(request,'otptaker.html',{"id":doctor_id})
                 


                except Exception as e:
                    # print(e)
                    return render(request,"registration.html",{'msg':" Email is not valid!!",'thank':True,"color":"red","doctor_salary":doctor_salary.keys()})
                
               
                
                
                
        else:
             return render(request,"registration.html",{'msg':"Age is not valid !!",'thank':True,"color":"red","doctor_salary":doctor_salary.keys()})
    return render(request,"registration.html",{"doctor_salary":doctor_salary.keys()})
#logout doctor
def logoutDoctor(request):
    try:
        del request.session['doctor']
    except:
        return redirect("/")
    return redirect("/")
#doctorforget
def forgetDoctor(request):
    if(request.method=='POST'):
    
        Doctor_Id = request.POST.get("Doctor_Id","")  
        password = request.POST.get("password","")
        repassword=request.POST.get('repassword',"")
        if(password==repassword):
            try:
                doctors= doctor.objects.get(Doctor_id=Doctor_Id)
                print("doctor",doctors)
                if(doctors):
                    doctors.Password=password
                    doctors.save()
                    
                    return redirect("/doctorlogin/")
            except Exception as e:
                
                return render(request,"doctorreset.html",{'msg':'username not define!!'})
        else:
         return render(request,"doctorreset.html",{'msg':"Pssword don't match!!"})
    return render(request,"doctorreset.html")
#hadling patient
def patientRegister(request):
   data=doctor.objects.filter(permanent="True",Status="Working").values()
   if("patient" in request.session):
        Email=request.session["patient"]
        data=Patient.objects.filter(Email=Email).values()
        
        # print(data)
        datas=data[(len(data)-1)]
        doctors=doctor.objects.filter(Doctor_id=datas["Doctor"]).values()
        param={"data":datas,"doctors":doctors[0]}
        # print(doctors)
        return render(request,"Patientportal.html",param)
   else:
    if(request.method=="POST"):
        Name=request.POST.get("name","")
        Email=request.POST.get("email","")
        Contact=request.POST.get("contact","")
        Doctor=request.POST.get("doctor","")
        Disease=request.POST.get("Disease","")
        Age=(request.POST.get("age",""))
        Blood_group=request.POST.get("blood","")
        Address=request.POST.get("address","")
        Date=request.POST.get("date","")
        id=(Patient.objects.all().values("id"))
        Patient_id="PATNT"+str(100+(id[len(id)-1]["id"])+1)
        Gender=request.POST.get("gender","")
        Password=request.POST.get("password","")
        now=datetime.now().strftime("%H:%M:%S")
        now=datetime.strptime(now,"%H:%M:%S")
        time=datetime.strptime(request.POST.get("time","")+":00","%H:%M:%S")
        if(checkAge(Age) and datetime.strptime(Date,"%Y-%m-%d").date()>=datetime.today().date() and (time<datetime.strptime("13:00:00","%H:%M:%S") or time>=datetime.strptime("14:00:00","%H:%M:%S") ) and (datetime.strptime(Date,"%Y-%m-%d")).weekday()<6):
            if(datetime.strptime(Date,"%Y-%m-%d").date()==datetime.today().date() and time<=now):
                return render(request,"patientform.html",{'msg':" Invalid time for Today !!",'thank':True,"doctors":data,"color":"red"})
            
            
            Age=int(Age)
            totp_secret = pyotp.random_base32()
                # Create a TOTP object
            totp = pyotp.TOTP(totp_secret)
                # Generate the OTP
            otp = totp.now()
            msg=f"Dear {Name}, \n Your one time password is {otp} , It will be valid for 60 seconds \n\n\n\n Thank You."
            try:
                sendmail(msg,Email)
                patient=Patient(Time=time,Password=Password,Name=Name,Email=Email,Address=Address,Age=Age,Gender=Gender,
                            Blood_Group=Blood_group,Doctor=Doctor,Patient_id=Patient_id,Contact=Contact,Disease=Disease,Date=Date)
                OTpRequired[Patient_id]=[patient,otp]
                return render(request,'otptaker.html',{"id":Patient_id})
            except Exception as e:
                return render(request,"patientform.html",{'msg':" Email is not valid!!","doctors":data,'thank':True,"color":"red"})

        else:
            if(not checkAge(Age)):
                return render(request,"patientform.html",{'msg':" Age is not valid !!",'thank':True,"doctors":data,"color":"red"})
            elif((datetime.strptime(Date,"%Y-%m-%d")).weekday()==6):
                    return render(request,"patientform.html",{'msg':" NO Appointment on Sunday  !!",'thank':True,"doctors":data,"color":"red"})

            return render(request,"patientform.html",{'msg':" Time or  Date is not valid !!",'thank':True,"doctors":data,"color":"red"})

    
    return render(request,"patientform.html",{"doctors":data})
#login patient
def patientlogin(request):
    if("patient" in request.session):
        Email=request.session["patient"]
        data=Patient.objects.filter(Email=Email).values()
        
        # print(data)
        data=data[(len(data)-1)]
        doctors=doctor.objects.filter(Doctor_id=data["Doctor"]).values()
        param={"data":data,"doctors":doctors[0]}
        # print(doctors)
        return render(request,"Patientportal.html",param)
    else:
        if(request.method=='POST'):
                
                Email = request.POST.get("Email","") 
                Password= request.POST.get("Password","")

                data=Patient.objects.filter(Password=Password,Email=Email).values() 
                if(len(data)>0):
                    if(data[0]['appointed']=="False"):
                        return render(request,"message.html",{"msg":"appointment"})
                    else:
                        request.session['patient'] = Email
                        #redirect to doctor page
                        data=Patient.objects.filter(Email=Email).values()
                        data=data[(len(data)-1)]
                        doctors=doctor.objects.filter(Doctor_id=data["Doctor"]).values()
                        param={"data":data,"doctors":doctors[0]}
                        print(doctors)
                        return render(request,"Patientportal.html",param)
                else:
                    
                    return render(request,'patientLogin.html',{'msg':'Email or password is not valid','thank':True})
                    
    return render(request,"PatientLogin.html")
#patient appointment portal accessing
def Pappointmentportal(request,email,gender):
    data={"email":email,"Gender":gender}
    return render(request,"patient_appointment_portal.html",{"data":data})
#taking appointment
def takeAppointment(request,email,gender):
    datas=doctor.objects.filter(permanent=True,Status="Working").values()
    if(request.method=="POST"):
        Name=request.POST.get("patientName","")
        Doctor=request.POST.get("doctor","")
        Disease=request.POST.get("description","")
        data=Patient.objects.filter(Email=email).values()[0]
        id=(Patient.objects.all().values("id"))
        Patient_id="PATNT"+str(100+(id[len(id)-1]["id"])+1)
        Age=request.POST.get("Age","")
        Blood_group=request.POST.get("Blood_group","")
        Date=request.POST.get("Date","")
        Gender=request.POST.get("Gender","")
        now=datetime.now().strftime("%H:%M:%S")
        now=datetime.strptime(now,"%H:%M:%S")
        time=datetime.strptime(request.POST.get("time","")+":00","%H:%M:%S")

        if(checkAge(Age) and datetime.strptime(Date,"%Y-%m-%d").date()>=datetime.today().date() and (time<datetime.strptime("13:00:00","%H:%M:%S") or time>=datetime.strptime("14:00:00","%H:%M:%S") ) and (datetime.strptime(Date,"%Y-%m-%d")).weekday()<6):
            if(datetime.strptime(Date,"%Y-%m-%d").date()==datetime.today().date() and time<=now):
                return render(request,"appoint.html",{'msg':" Invalid time for Today !!",'thank':True,"doctors":datas,"color":"red"})
            
            Age=int(Age)
            patient=Patient(Password=data["Password"],Name=Name,Email=email,Address=data["Address"],Age=Age,Gender=Gender,
                            Blood_Group=Blood_group,Doctor=Doctor,Patient_id=Patient_id,Contact=data["Contact"],Disease=Disease,Date=Date,Time=time)
            patient.save()
            return redirect("/Pappointment/"+email)
        else:
          if(not checkAge(Age) ):
                return render(request,"appoint.html",{'msg':"Age is not valid !!",'thank':True,"doctors":datas,"color":"red"})

          
          return render(request,"appoint.html",{'msg':"Date or Time is not valid !!",'thank':True,"doctors":datas,"color":"green"})

    return render(request,"appoint.html",{"email":email,"gender":gender,"doctors":datas})
#action on click appoi/ntments
def Pappointment(request,email):
    data=Patient.objects.filter(Email=email).values()
    
   
    
    for i in data:
        Doctor=doctor.objects.filter(Doctor_id=i["Doctor"]).values("Name")
        i["dName"]=Doctor[0]["Name"]
    data=list(data)
    data.reverse()
    return render(request,"Pappointment.html",{"data":data})
def Pdischarge(request,email):
    data=Patient.objects.filter(Email=email,discharged=True).values()
    for i in data:
        try:
            Doctor=doctor.objects.filter(Doctor_id=i["Doctor"]).values("Name","Contact")
            date=admitPatients.objects.filter(Patient_id=i["Patient_id"]).values("Discharge_Date","Admit_Date")
            i["dDate"]=date[0]["Discharge_Date"]
            i["dContact"]=Doctor[0]["Contact"]
            i["aDate"]=date[0]["Admit_Date"]
            i["dName"]=Doctor[0]["Name"]
        except Exception as e:
            pass
    return render(request,"Pdischarge.html",{"data":data})
def logoutpatient(request):
    try:
        del request.session['patient']
    except:
        return redirect("/")
    return redirect("/")
#accessing appointment page
def Dappointments(request,did,day,thank="false"):
    try:
        if(day=="all"):
            data=Patient.objects.filter(Doctor=did,appointed="True").values()
        else:
            date=datetime.today().strftime("%Y-%m-%d")
            data=Patient.objects.filter(Date=date,Doctor=did).values()
        # print(data)
        data=list(data)
        data.reverse()
        return render(request,"Dappointment.html",{"data":data,"day":day,"thank":thank})
    except Exception as e:
       print(e)
       return HttpResponse("<center>Opps!! there is some error!!!!</center>")
#admit patient through doctor
def DadmitPatient(request,pid,day):
    global Total_Beds
    try:
        Admit_Date = datetime.now()
        Admit_time=Admit_Date.strftime('%H:%M:%S')
        Admit_Date=Admit_Date.strftime('%Y-%m-%d')
        bed=0
        Beds=admitPatients.objects.filter(Discharge_Date=None).values("Bed_no")
        Beds=list(Beds)
        Beds=[i["Bed_no"] for i in Beds]
        for i in range(1,Total_Beds):
            if(i not in Beds):
                bed=i
                break
        if(bed==0):
            return redirect("/Dappointments/"+data.Doctor+","+day,"True")
        data=Patient.objects.get(Patient_id=pid)
        data.admitted=True
        data.save()
        msg=f"{data.Name} has been Admitted. \n Thank You for Choosing us Stay Safe and Updated"
        Email=data.Email
        try:
            sendmail(msg,Email)
        except Exception as e:
            pass
        admitPatient=admitPatients(Bed_no=bed,Patient_id=pid,Admit_Date=Admit_Date,Admit_time=Admit_time,Doctor_id=data.Doctor)
        admitPatient.save()
        return redirect("/Dappointments/"+data.Doctor+","+day)
    except Exception as e:
         print(e)
         return HttpResponse("<center>Opps!! there is some error!!!!</center>")
#dischargePatient
def dischargedPatient(request,pid):
     Discharged_Date = datetime.now()
     Discharged_Date=  Discharged_Date.strftime('%Y-%m-%d')
     data=Patient.objects.get(Patient_id=pid)
     bill=Bill.objects.filter(Patient_id=pid,Date=Discharged_Date).values()
     
     Doctor=data.Doctor
     if(len(bill)==0 or bill[0]["Paid"]=="False"):
         #Today bill not recieved first recieved the bill
         return Dadmit(request,Doctor,"True",)
     else:
        data.discharged=True
        data.save()
        msg=f"{data.Name} has been Discharged from Hospital. \n Thank You for Choosing us Stay Safe "
        Email=data.Email
        try:
            sendmail(msg,Email)
        except Exception as e:
            pass
        admitPatient=admitPatients.objects.get(Patient_id=pid)
        admitPatient.Discharge_Date=Discharged_Date
        admitPatient.save()
        return Ddischarged(request,Doctor)
#checked admit through doctor
def checkedPatient(request,pid,day):
        data=Patient.objects.get(Patient_id=pid)
        data.checked=True
        msg=f"CheckUp of {data.Name} has been done.\n Thank You for Choosing us Stay Safe "
        Email=data.Email
        try:
            sendmail(msg,Email)
        except Exception as e:
            pass

        data.save()
        return redirect("/Dappointments/"+data.Doctor+","+day)
#accessing doctor admit page
def Dadmit(request,did,thank="False"):
    
        data=Patient.objects.filter(Doctor=did,admitted="True",discharged="False").values()
        for i in data:
            Admit=admitPatients.objects.filter(Patient_id=i["Patient_id"]).values("Admit_Date","Bed_no")
            i["aDate"]=Admit[0]["Admit_Date"]
            i["Bed_no"]=Admit[0]["Bed_no"]
        data=list(data)
        data.reverse()
        return render(request,"Dadmit.html",{"data":data,"thank":thank})
    
#accessing discharge page
def Ddischarged(request,did):
    data=Patient.objects.filter(discharged=True,Doctor=did).values()
    for i in data:
        date=admitPatients.objects.filter(Patient_id=i["Patient_id"]).values("Discharge_Date","Admit_Date")
        i["dDate"]=date[0]["Discharge_Date"]
        i["aDate"]=date[0]["Admit_Date"]
             
        
    data=list(data)
    data.reverse()
    
    return render(request,"Ddischarged.html",{"data":data})
#accessing Emergency page
def Emergency(request):
    return render(request,"emergency.html")
#accessing doctors page
def OurDoctor(request,doc="all",dic=""):
    specialty=doctor.objects.filter(Status="Working").values("Specialty").distinct()
    # doc=request.POST.get("Search","all")
    if( doc!="all"):
        data=doctor.objects.filter(Status="Working",Specialty=doc).values()
        specialty=list(specialty)
        for i in specialty:
            if i["Specialty"]==doc:
             specialty.remove(i)
                
        return render(request,"doctor.html",{"data":data,"specialty":specialty,"special":doc,'dic':dic})

    
    data=doctor.objects.filter(Status="Working").values()
    return render(request,"doctor.html",{"data":data,"specialty":specialty,"special":doc,"dic":dic})
    
def bookappointment(request):
     if(request.method=="POST"):

        Name=request.POST.get("name","")
        Email=request.POST.get("email","")
        Contact=request.POST.get("contact","")
        Doctor=request.POST.get("doctor","")
        Disease=request.POST.get("Disease","")
        Age=(request.POST.get("age",""))
        Blood_group=request.POST.get("blood","")
        Address=request.POST.get("address","")
        Date=request.POST.get("date","")
        id=(Patient.objects.all().values("id"))
        Patient_id="PATNT"+str(100+(id[len(id)-1]["id"])+1)
        Gender=request.POST.get("gender","")
        Password=request.POST.get("password","")
        now=datetime.now().strftime("%H:%M:%S")
        now=datetime.strptime(now,"%H:%M:%S")

        time=datetime.strptime(request.POST.get("time","")+":00","%H:%M:%S")

        if(checkAge(Age) and datetime.strptime(Date,"%Y-%m-%d").date()>=datetime.today().date() and (time<datetime.strptime("13:00:00","%H:%M:%S") or time>=datetime.strptime("14:00:00","%H:%M:%S") ) and (datetime.strptime(Date,"%Y-%m-%d")).weekday()<6):
            if(datetime.strptime(Date,"%Y-%m-%d").date()==datetime.today().date() and time<=now):
                dicts={'msg':" Invalid time for Today !!",'thank':True,"color":"red"}
                return OurDoctor(request,dic=dicts)
            
            Age=int(Age)
            totp_secret = pyotp.random_base32()
                # Create a TOTP object
            totp = pyotp.TOTP(totp_secret)
                # Generate the OTP
            otp = totp.now()
            msg=f"Dear {Name}, \n Your one time password is {otp} , It will be valid for 60 seconds \n\n\n\n Thank You."
            try:
                sendmail(msg,Email)
                patient=Patient(Password=Password,Name=Name,Email=Email,Address=Address,Age=Age,Gender=Gender,
                            Blood_Group=Blood_group,Doctor=Doctor,Patient_id=Patient_id,Contact=Contact,Disease=Disease,Date=Date,Time=time)
                OTpRequired[Patient_id]=[patient,otp,"take"]
                return render(request,'otptaker.html',{"id":Patient_id})
            except Exception as e:
                dicts={'msg':" Email is not valid!!",'thank':True,"color":"warning"}
                return OurDoctor(request,dic=dicts)

        else:
            if(not checkAge(Age)):  
                dicts={'msg':" Age is not valid !!",'thank':True,"color":"warining"}
                return OurDoctor(request,dic=dicts)
            dicts={'msg':"date or time is not valid!!",'thank':True,"color":"warning"}
            return OurDoctor(request,dic=dicts)
#Search particular patient
def SearchPatient(request,doctors,pid=" "):
    if(request.method=="POST"):
        
        id=request.POST.get("id","")
        if(id==""):
            id=pid
           
        
        data=Patient.objects.filter(Patient_id=id).values()
        
       
        date=[]
        try:
          Doctor=doctor.objects.filter(Doctor_id=data[0]["Doctor"]).values("Name","Specialty")
          if(data[0]["admitted"]=="True"):
              date=admitPatients.objects.filter(Patient_id=id).values("Admit_Date","Discharge_Date")
              return render(request,"searchPatient.html",{"data":data[0],"doctor":Doctor[0],"date":date[0],"Doctor":doctors})
          else:
             return render(request,"searchPatient.html",{"data":data[0],"doctor":Doctor[0],"Show":True,"Doctor":doctors})
          
          
        except Exception as e:
           
            data=[{"Patient_id":"Sorry id doesn't exist !!"}]
            return render(request,"searchPatient.html",{"data":data[0],"Error":True,"Doctor":doctors})

    return render(request,"searchPatient.html",{"Show":False,"Doctor":doctors})
#TodayAppointment/
def TodayAppointment(request,doc,day="all"):
    dname=doctor.objects.get(Doctor_id=doc)
    dname=dname.Name
    if(day!="all"):
        # print("doc:",doc)
        date=datetime.today().strftime("%Y-%m-%d")
        data=Patient.objects.filter(Date=date,Doctor=doc).values()
        
        return render(request,"TodayAppointment.html",{"data":data,"day":day,"Name":dname})
    else:
        print("doc:",doc)
        data=Patient.objects.filter(Doctor=doc).values()
        # print(data[0])
        return render(request,"TodayAppointment.html",{"data":data,"day":day,"Name":dname})
#to check the details of the doctor 
def doctor_Profile(request,doc):
    
    data=doctor.objects.filter(Doctor_id=doc).values()
    if(data[0]["permanent"]=="False"):
        data=doctor.objects.all().values()
        data=list(data)
        data.reverse()
        return render(request,"Adoctors.html",{"data":data})
    else:
        for i in data:
            i["total"]=len(Patient.objects.filter(Doctor=doc,appointed="True").values())
            i["Active"]=len(Patient.objects.filter(Doctor=doc,admitted="True",discharged="False").values())
            i["pending"]=len(Patient.objects.filter(Doctor=doc,appointed="True",checked="False",admitted="False").values())
            i["discharge"]=len(Patient.objects.filter(Doctor=doc,discharged="True").values())
            i["Fee"]=doctor_charges.get(i["Specialty"],0)    
            return render(request,"profile.html",{"data":data[0]})

