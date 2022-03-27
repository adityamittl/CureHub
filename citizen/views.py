from django.http.response import HttpResponse,JsonResponse
from django.shortcuts import redirect, render
from .form import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cryptography.fernet import Fernet
from django.core.files.storage import FileSystemStorage
key = Fernet.generate_key()
from django.core import serializers
import datetime
f = Fernet(key)

def upload_report(request):
    return render(request,"index.html")

def home(request):
    # return render(request,'citizen/homepage.html')
    if(login_mode.objects.get(user=request.user).type=="citizen"):
        profile = citizen_profile.objects.get(user=request.user)
        data = Treatment.objects.filter(patient = profile)
        current = list(Treatment.objects.filter(patient = profile).filter(date_of_end = None))
        current[0].id = f.encrypt(str(current[0].id).encode()).decode('utf-8')
        print(current[0].id)
        context = {
            'prevs':data,
            'current':current,
            'profile':profile
        }
        return render(request,'citizen/home.html',context=context)
    elif(login_mode.objects.get(user=request.user).type=="doctor"):
        data = doctor.objects.get(user=request.user)
        context = {
            'data':data
        }
        return render(request,'doctor/homepage.html',context=context)
    elif(login_mode.objects.get(user=request.user).type=="hospital"):
        data = Hospital.objects.get(user=request.user)
        context = {
            'data':data
        }
        return render(request,'hospital/homepage.html',context=context)
    elif(login_mode.objects.get(user = request.user).type == 'diagnosis'):
        data = Diagnosis.objects.filter(user = request.user)
        context = {
            'data':data
        }
        return render(request,'diagnosis/homepage.html',context=context)
    else:
        return render(request,'admin/index.html')

def reports(request,id):
    id = f.decrypt(id.encode())
    data = Treatment.objects.filter(id=id)
    print(data[0].id)
    # if login_mode.objects.get(user=request.user).type == 'doctor':
    #     print("----")
    # if login_mode.objects.get(user=request.user).type == 'citizen':
    #     if any(data[0].id == x.Diagnosis_detail.id for x in Treatment.objects.filter(patient = citizen_profile.objects.get(user = request.user))):
    #         return render(request,'citizen/report.html',{'data':data})
    return HttpResponse(str(data[0].description)+"<br>"+str(data[0].report))

def current_patient(request):
    data = Treatment.objects.filter(date_of_end = None).filter(doctor = request.user)
    return render(request,'current_patient.html',{'data':data})

def patient_profile(request,slug):
    if(login_mode.objects.get(user=request.user).type=="doctor"):
        data = Treatment.objects.filter(patient = citizen_profile.objects.get(identity_number = slug))
        return render(request,'patient_profile.html',{'data':data})
    else:
        return HttpResponse("You are not authorized to view this page")

def assign_doctor(request):
    if(login_mode.objects.get(user=request.user).type=="hospital"):

        if request.method == 'POST' and request.POST.get('doctorID'):
            id = request.POST.get('patientID')
            did = request.POST.get('doctorID')
            patient = citizen_profile.objects.get(identity_number = id)
            Adoctor = doctor.objects.get(id = did)
            Treatment.objects.create(patient = patient,doctor = Adoctor,Hospital= request.user)
            messages.success(request, 'Successfully assigned to patient : '+patient.name)
            return redirect('homepage')
        elif request.method == 'POST' and request.POST.get('doctorID')==None:
            id = request.POST.get('patientID')
            patient = citizen_profile.objects.get(identity_number = id)
            context = {
                'patient':patient,
                'id': id #f.encrypt(id.encode())
            }
            return render(request,'assign_doctor.html',context=context)


    else:
        return HttpResponse("You are not authorized to view this page")


def push_report(request):
    if request.method == 'POST':
        pId = request.POST.get('pid')
        Tname = request.POST.get('Tname')
        remark = request.POST.get('remark')
        price = request.POST.get('price')
        report = request.FILES['Report']
        fs = FileSystemStorage(location='media/')
        filename = fs.save(report.name, report)
        data = Diagnosis()
        data.name = Tname
        data.price = price
        data.report = filename
        data.description = "Noneee"
        data.remark = remark
        data.save()
        patient = citizen_profile.objects.get(identity_number = pId)
        a = Treatment.objects.filter(patient = patient).filter(date_of_end = None)
        test = tests.objects.get(name = Tname)
        a[0].required_tests.remove(test)
        a[0].Diagnosis_detail.add(data)
        # a[0].save()
        print(pId,Tname,remark,price,report)
    # if(login_mode.objects.get(user=request.user).type=="doctor" or login_mode.objects.get(user=request.user).type=="diagnosis"):
    #     if request.method == 'POST':
    #         form = diagnosis_form(request.POST,request.FILES)
    #         if form.is_valid():
    #             form.save()
    #             return HttpResponse("Report has been uploaded successfully")
    #         else:
    #             return HttpResponse("Report has not been uploaded successfully")
    #     else:
    #         form = diagnosis_form()
    #         return render(request,'push_report.html',{'form':form})

    return render(request,'diagnosis/submit_report.html')


# def test(request):
#     if request.method == 'POST':
#         buffer = request.FILES['imagess']
#     return render(request,'test.html')

def doctor_home(request):
    return render(request,'doctor/home.html')

def activep(request):
    return render(request,"doctor/active_patients.html")


def new_patients(request):
    usr = request.user()
    data = Treatment.objects.filter(doctor = doctor.objects.get(user = usr), done_checkup = False)
    return JsonResponse(data,safe=False)

def docHome(request):
    return render(request,'doctor/active_patients.html')

import json

def setPrescription(request):
    if request.method == 'POST':
        meds = json.loads((request.body).decode('utf-8'))
        medDetail = json.loads(meds['pres'])
        TreatId = f.decrypt(meds['assert'].encode()).decode('utf-8')
        print(TreatId,medDetail)
        treat = Treatment.objects.get(id = TreatId)
        treat.meds_duration = meds['duration']
        for i in medDetail:
            a= prescription()
            a.name = medDetail[i]['name']
            a.quantity = int(medDetail[i]['qty'])
            a.taking_instructions = medDetail[i]['decs']
            a.save()
            treat.meds.add(a)
        treat.save()
        print(treat.meds.all())
        return JsonResponse('Successful',safe=False)


def hospialHome(request):
    if login_mode.objects.get(user=request.user).type == 'hospital':
        data = Hospital.objects.get(id = 1)
        data2 = doctor.objects.filter(servicing = data)
        context = {
            'data1':data,
            'data2':data2
        }
        return render(request,'hospital/homepage.html',context = context)
    return HttpResponse("You are not authorized to visit this page")

def searchDoctors(request):
    if request.method == 'POST':
        if login_mode.objects.get(user=request.user).type == 'hospital':
            data = doctor.objects.filter(servicing = Hospital.objects.get(id = Hospital.objects.get(user = request.user).id))
            data = json.loads(serializers.serialize('json',data))
            res = {}
            for i in range(len(data)):
                # print(data[i])
                pData = data[i]['fields']
                res1 = {}
                res1['name'] = pData['First_name']+" "+pData['Last_name']
                res1['domain'] = pData['domain']
                res1['experience'] = pData['experience']
                # print(pData.id)
                res1['assert'] = f.encrypt(str(data[i]['pk']).encode()).decode('utf-8')
                res[str(i)] = res1
            return JsonResponse(res)

def searchPatient(request):
    if request.method == 'POST':
        pid = json.loads(request.body.decode('utf-8'))
        data = citizen_profile.objects.get(identity_number = pid['pid'])
        # data = serializers.serialize('json',data)
        res = {}
        res['name'] = data.First_name + " " + data.Last_name
        res['age'] =datetime.date.today().year-data.Date_of_birth.year 
        res['Address'] = data.Address+"-"+data.City + "-"+ data.State+'-'+data.Country
        res['email'] = data.Email
        res['Phone_number'] = data.Phone_number
        res['image'] =data.image.url

        # print(res)
        
        return JsonResponse(res,safe=False)

def startTreatment(request):
    print(login_mode.objects.get(user = request.user))
    if login_mode.objects.get(user = request.user).type == 'hospital' :
        data = request.body
        data = data.decode('utf-8')
        data = json.loads(data)
        pIdNo = data['PRNO'];
        DiD = f.decrypt(data['assert'].encode()).decode('utf-8')
        res = {'id':pIdNo,'DiD':DiD}
        patient = citizen_profile.objects.get(identity_number=pIdNo)
        print(res)
        fee = Hospital.objects.get(user = request.user).reg_fees
        a = bill(det = 'Hospital Registration Fees',ammount = fee,currency = 'Rs').save()
        Treatment(patient = patient, Treating_hospital = Hospital.objects.get(user = request.user), Treating_doctor = doctor.objects.get(id = DiD),bill_breakdown = a,price = fee).save()
        return JsonResponse("Success",safe=False)

def currentPatientList(request):
    if request.method == 'GET':
        data = Treatment.objects.filter(Treating_doctor = doctor.objects.get(id= 1), done_checkup = False,waiting_fore_reports = False)
        data = json.loads(serializers.serialize('json',data))
        res = {} 
        for i in range(len(data)):
            rData = data[i]['fields']['patient']
            pData = citizen_profile.objects.get(id = rData)
            res1 = {}
            res1['assert'] = f.encrypt(str(data[i]['pk']).encode()).decode('utf-8') # Treatment ID
            res1['name'] = pData.First_name+" "+pData.Last_name
            res1['age'] = datetime.date.today().year-pData.Date_of_birth.year
            res1['image'] = pData.image.url
            res1['sex'] = pData.sex
            res[str(i)] = res1
        return JsonResponse(res)

def getHistory(request):
    if request.method == 'POST':
        temp = json.loads((request.body).decode('utf-8'))['assert']
        id = f.decrypt(temp.encode()).decode('utf-8')
        patient = Treatment.objects.get(id = id).patient
        history = json.loads(serializers.serialize('json',Treatment.objects.filter(patient = patient , done_checkup = True)))
        print(len(history))
        x = []
        for i in range(len(history)):
            res = {}
            res['name'] = history[i]['fields']['name']
            res['date'] = history[i]['fields']['date_of_start']
            a = doctor.objects.get(id = history[i]['fields']['Treating_doctor'])
            res['doctor'] = a.First_name+" "+a.Last_name
            res['km'] = f.encrypt(str(history[i]['pk']).encode()).decode('utf-8')
            x.append(res)
        print(x)
        if(history == '[]'):
            return JsonResponse("No History",safe=False)
        return JsonResponse(x,safe=False)


def typeOfTests(request):
    if request.method== 'GET':
        data = tests.objects.all()
        data = json.loads(serializers.serialize('json',data))
        res = {}
        for i in range(len(data)):
            res[str(i)] = data[i]['fields']['name']
        return JsonResponse(res)

def history(request,id):
    if request.method == 'GET':
        id = f.decrypt(id.encode()).decode('utf-8')
        data = Treatment.objects.get(id = id)
        med = data.meds.all()
        return render(request,'doctor/expanded_history.html',{'data':data,'meds':med})

def submit_test(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        data = json.loads(data)
        id = f.decrypt(data['patient'].encode()).decode('utf-8')
        treat = Treatment.objects.get(id = id)
        for i in range(len(data['tests'])):
            treat.required_tests.add(tests.objects.get(name = data['tests'][i]))
        treat.waiting_fore_reports = True
        treat.save()
        return JsonResponse("Success",safe=False)

def Diag_fetch(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        print("----",data)
        data = json.loads(data)['patientID']
        patient = citizen_profile.objects.get(identity_number = data)
        treat = Treatment.objects.filter(patient = patient)[0]
        report = treat.required_tests.all()
        res = {}
        res['image'] = patient.image.url
        res['name'] = patient.First_name+" "+patient.Last_name
        res['city'] = patient.City
        res['state'] = patient.State
        res['country'] = patient.Country
        res['doctor'] = treat.Treating_doctor.First_name+" "+treat.Treating_doctor.Last_name
        res['tests'] = []
        for i in range(len(report)):
            res['tests'].append(report[i].name)
        try:
            res['disease'] = treat.name
        except:
            res['disease'] = 'None'
        
        return JsonResponse(res)


