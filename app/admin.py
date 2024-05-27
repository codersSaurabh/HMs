from django.contrib import admin
from .models import doctor,Patient,admitPatients,Feedback,Bill

# Register your models here.
admin.site.register(doctor)
admin.site.register(Patient)
admin.site.register(admitPatients)
admin.site.register(Feedback)
admin.site.register(Bill)

