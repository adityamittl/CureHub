from django.contrib import admin
from django.urls import path,include
from citizen.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('authentication.urls')),
    path('',upload_report),
    path('home',home),
    # path('test',test),
    path('upload_report',push_report),
    path('doc',doctor_home),
    path('active',activep),
    path('reports/<str:id>',reports),
    path('dochome',docHome),
    path('sendpres',setPrescription),
    path('hospitalhome',hospialHome),
    path('getPatient',searchPatient),
    path('getDoctors',searchDoctors),
    path('startTreatment',startTreatment),
    path("currentPatientList",currentPatientList),
    path('gethistory',getHistory),
    path('getTests',typeOfTests),
    path('history/<str:id>',history),
    path('submit_test',submit_test),
    path('diagnosis/fetch',Diag_fetch)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)