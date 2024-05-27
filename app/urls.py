from django.urls import path
from . import views
urlpatterns = [
    #admin urls
    path('adminIn/',views.adminIn,name="adminIn"),
    path("aboutUs/",views.aboutUs,name="about us"),#aboutuspage accessing
     path("forgetAdmin/",views.forgetAdmin,name="forgetAdmin"),
     path("Admin/",views.admin,name='admin'),
    #  path("AdminPortal/",views.logoutAdmin,name='logoutadmin'),#logout
     path("AdminLogout/",views.logoutAdmin,name='logoutadmin'),#logout
     path("Aappointments/<str:day>",views.Aappointments),#appointments
     path("ConfirmPatient/<str:pid>,<str:day>",views.confirmpatient),#confirm patient appointment
    path("Adoctors/",views.Adoctors),#Doctors in admin
    path("ConfirmDoctor/<str:did>",views.ConfirmDoctor),#confirm doctor
    path("DeleteDoctor/<str:did>",views.DeleteDoctor),#delete doctor
    path("Apatients/",views.Apatients),#accessing patient in admin
    path("AdischargedPatient/<str:pid>",views.AdischargedPatient),#discharge patient from admin
    path("Adischarged/",views.Adischarged),#accessing discharged patient in admin
    path("Genbil/<str:pid>,<str:day>",views.Genbil),#generating bill on discharging patient
    path("showbill/<str:pid>,<str:day>",views.showbill),#show
    path("PayBill/<str:pid>,<str:day>",views.PayBill,name="balance 0"),#pay bill
    path("BillList/<str:day>",views.BillList,name="bill list"),#taking list of bills
    path("Pdischarge/showbill/<str:pid>",views.showbill),
    path("Pappointment/showbill/<str:pid>,<str:day>",views.showbill),#
    path("Feedback/",views.feedback),#accessing feedbacks
    path("ShowFeedback/",views.ShowFeedback),#show feedback
    path("TodayAppointment/<str:doc>,<str:day>",views.TodayAppointment,name="check todya appointment"),#today appointment


    path("",views.home,name="home"),

    #doctor urls
    path("doctorlogin/",views.doctorlogin,name="doctorlogin"),
    path("doctorRegister/",views.doctorRegister,name="doctorlogin"),
    path("logoutDoctor/",views.logoutDoctor,name='logoutadmin'),
    path("forgetDoctor/",views.forgetDoctor,name="forgetAdmin"),

    #patient usrls
     path("patientRegister/",views.patientRegister,name="forgetAdmin"),
     path("patientlogin/",views.patientlogin,name="doctorlogin"),
     path("logoutpatient/",views.logoutpatient,name="doctorlogin"),
     path("takeAppointment/<str:email>,<str:gender>",views.takeAppointment),
     #patient portal handle
    path("Pappointment/<str:email>",views.Pappointment),
    path("Pappointmentportal/<str:email>,<str:gender>",views.Pappointmentportal),
    path("Pdischarge/<str:email>",views.Pdischarge),#to discharge patient in patient portal
     #Doctor portal appointment
     path("Dappointments/<str:did>,<str:day>",views.Dappointments),#doctor appointment
     path("admitPatient/<str:pid>,<str:day>",views.DadmitPatient),
     path("checkedPatient/<str:pid>,<str:day>",views.checkedPatient),
     path("dischargePatient/<str:pid>",views.dischargedPatient),
     #admit
     path("Dadmit/<str:did>",views.Dadmit),
     #discharged
    path("Ddischarged/<str:did>",views.Ddischarged),
    #otptaker
    path("otptaker/",views.otptaker),
    #Doctor
    path("OurDoctor/<str:doc>",views.OurDoctor,name="doctor"),
    path("bookappointment/",views.bookappointment,name="book appointment"),
    #Emergency/
    path("Emergency/",views.Emergency,name="Emergency"),
    #search patient
    path("SearchPatient/<str:doctors>",views.SearchPatient,name="Search Patient"),
    #doctor profile
    path("doctor_Profile/<str:doc>",views.doctor_Profile,name="Doctor Profile"),
]