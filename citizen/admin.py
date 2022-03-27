from django.contrib import admin
from .models import *

admin.site.register(citizen_profile)
admin.site.register(Hospital)
admin.site.register(doctor)
admin.site.register(Insurence)
admin.site.register(Treatment)
admin.site.register(Diagnosis)
admin.site.register(login_mode)
admin.site.register(diagnosis_center)
admin.site.register(tests)
admin.site.register(prescription)