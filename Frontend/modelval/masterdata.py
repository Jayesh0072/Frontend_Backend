from django.shortcuts import render,redirect
import traceback
import os 
from pathlib import Path
import json 
import pandas as pd
from django.http import JsonResponse
from django.core import serializers
from datetime import date
from django.core.files.storage import FileSystemStorage

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

BASE_DIR = Path(__file__).resolve().parent.parent
# Create your views here.
user_name = "user1"
file_path = os.path.join(BASE_DIR, 'static/Data/')
savefile_name = file_path +  "Modelinfo.csv" 
# Create your views here.    
# DEFINE THE DATABASE CREDENTIALS
user = 'sa'
password = 'sqlAdm@2023'
host = 'LAPTOP-H38D1CC4\SQLEXPRESS'
port = 1433
database = 'RMSE_Latest'
from .RegModel.registermodel import RegisterModel as Register 

from .Adm_Utils.Masters import MasterTbls
from .DAL.dboperations import dbops
from .models import Users,UA
from .UserInfo.user import UserInfo
from .Validation.validation import Validation 
from modelval.models import *  
objreg=Register()  
objmaster=MasterTbls()
objvalidation=Validation()
objdbops=dbops()
import requests
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework import generics, permissions, status,serializers

def getAPIURL():
    api_url=os.environ['API_URL']
    return api_url
def dashboard(request):
    try:
        if(str(objmaster.isAutherized(request.session['ucaid'],'2')) =="0"):
            print('not autherized')
            return render(request, 'blank.html',{'actPage':'RMSE'}) 
        modelinfo=objreg.getModelListByUSerid(request.session['uid'],str(request.session['ulvl']),'0')
        print("-------------1 modelinfo",modelinfo)
        modelriskcnt=objreg.getModelRiskCntByUserid(request.session['uid'],str(request.session['ulvl'])) 
        print("-------------2 modelriskcnt",modelriskcnt)
        modelsrccnt=objreg.getModelSrcCntByUserid('0',request.session['uid'])
        print("-------------3 modelsrccnt",modelsrccnt)
        srcCnt= [
            {
            'value': modelsrccnt[modelsrccnt['lbl'] == 'Internal'].values[0][0],
            'itemStyle': {
                'color': 'red'
            }
            }, 
            {
            'value': modelsrccnt[modelsrccnt['lbl'] == 'Legacy'].values[0][0],
            'itemStyle': {
                'color': 'Yellow'
            }
            },
            {
            'value': modelsrccnt[modelsrccnt['lbl'] == 'Vendor'].values[0][0],
            'itemStyle': {
                'color': 'Green'
            }
            }, 
        ]

        cnt= [
            {
            'value': modelriskcnt[modelriskcnt['lbl'] == 'High'].values[0][1],
            'itemStyle': {
                'color': '#ee6666'
            }
            }, 
            {
            'value': modelriskcnt[modelriskcnt['lbl'] == 'Medium'].values[0][1],
            'itemStyle': {
                'color': '#fac858'
            }
            },
            {
            'value': modelriskcnt[modelriskcnt['lbl'] == 'Low'].values[0][1],
            'itemStyle': {
                'color': '#91cc75'
            }
            },
            {
            'value': modelriskcnt[modelriskcnt['lbl'] == 'None'].values[0][1],
            'itemStyle': {
                'color': '#bf444c'
            }
            },
        ]
        #New Code added  by Jayesh
        user_id = request.session['uid']
        # print("--------------------uid",user_id)
        # print("--------------------srccnt",srcCnt)
        content = UserDashboardContentMaster.objects.filter(user_id = user_id)
        # print("---------------------content",content)
        return render(request, 'dashboard.html',{'modelinfo':modelinfo,'srcCnt':srcCnt,'toolCnt':objreg.getToolCntByUserId(request.session['uid'],str(request.session['ulvl'])) ,'modelttl':str(len(modelinfo)),'mdlRiskCnt':cnt,'modeltypes':objreg.getModelTypeByUserId(request.session['uid'],str(request.session['ulvl'])),'actPage':'RMSE - Quick View','content':content})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc())

# Add user dashboard content code added by jayesh
def addusrdashbcontent(request):
    print()
    user_id = request.session['uid']
    # print("----------------user_id add",user_id)
    try:
        print("---------add user dashboard content",request.GET)
        request_data = {x:request.GET.get(x) for x in request.GET.keys()}
        filter_srt_indx = UserDashboardContentMaster.objects.filter(sorting_index = request_data['sortindex'])
        if filter_srt_indx:
            return JsonResponse({"isvalid":"false"})
        else:
            taskfun_obj = UserDashboardContentMaster(display_type = request_data['displaytype'],source = request_data['source'],sorting_index = request_data['sortindex'],user_id = user_id)
            taskfun_obj.save()
            print("save successfully")
            return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print("setuppycaret is",e) 
        print('setuppycaret traceback is ', traceback.print_exc()) 
        return JsonResponse(e)

def error_saving(request,data):
    print("data print",data)
    file = open('logs.txt', 'w')
    file.write(str(data))
    file.close()
    print("file save")
    return redirect('redirectError')


# New Code By Jayesh
def showtaskfun(request):
    try:  
        third_party_api_url = getAPIURL()+'task-function-master/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("task function response------------------------------------",response.content)
        # funobj = TaskFunctionMaster.objects.all()
        return render(request, 'taskfunlist.html',{'actPage' :'RMSE - Task Function','users':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())
        # error_saving(request,e)
        return redirect('redirectError',pk=e)
        # return redirect(reverse(redirectError,pk=e))
        # return render(request, 'error.html')
    
def redirectError(request,pk):
    print("data print request",pk)
    file = open('logs.txt', 'w')
    file.write(str(pk))
    file.close()
    print("file save")
    return render(request,'error.html')


def newtaskfun(request):
    try:   
        return render(request, 'addtaskfun.html',{'actPage':'RMSE - Add Task Function'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())


@api_view(['POST'])

def addtskfun(request):
    try:
        # third_party_api_url = api_url+'task-function-master/'

        task_function_label = request.POST.get('label', 'False') 
        task_function_description = request.POST.get('desc','False')
        update_id = request.POST.get('update_id','False')
        active_status=request.POST.get('rbactivests','False')
        print("active_status",active_status)

        print("form content",task_function_label,task_function_description,update_id)
        if update_id != 'undefined':
            third_party_api_url = getAPIURL()+'task-function-master/'
            data_to_update = {
                'task_function_label':task_function_label,
                'task_function_description':task_function_description,
                'id':update_id,
                'activestatus':active_status
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.put(third_party_api_url, data= json.dumps(data_to_update),headers=header)
            print("----------------5")
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
        else:
            print("create----------------")
            third_party_api_url = getAPIURL()+'task-function-master/'
            data_to_save = {
                'task_function_label':task_function_label,
                'task_function_description':task_function_description,
                'activestatus':active_status
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
            print("response content create",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
       
def showtasktype(request):
    try: 
        third_party_api_url = getAPIURL()+'task-type-master/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        # typeobj = TaskTypeMaster.objects.all()
        # print("-----------------",typeobj)
        return render(request, 'tasktypelist.html',{'actPage' :'RMSE - Task Type','users':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())

def newtasktype(request):
    try:   
        return render(request, 'addtasktype.html',{'actPage':'RMSE - Add Task Type'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

   
        
@api_view(['POST'])

def addtsktype(request):
    try: 
        label = request.POST.get('label', 'False') 
        description = request.POST.get('desc','False')        
        update_id = request.POST.get('update_id','False') 
        active_status=request.POST.get('rbactivests','False')
        print("active_status",active_status)

        if update_id != 'undefined':
            third_party_api_url = getAPIURL()+'task-type-master/'
            data_to_update = {
                'task_type_label':label,
                'task_type_description':description,
                'id':update_id,
                'activestatus':active_status
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.put(third_party_api_url, data= json.dumps(data_to_update),headers=header)
            print("----------------5")
            # print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
        else:
            print("-----------addtasktype-3")
            third_party_api_url = getAPIURL()+'task-type-master/'
            data_to_save = {
                'task_type_label':label,
                'task_type_description':description,
                'activestatus':active_status
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
            print("----------------5")
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
        
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def showsubtasktype(request):
    try: 
        third_party_api_url = getAPIURL()+'sub-task-type-master/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response sub task type",response.content)
        # subtypeobj = SubTasktypeMaster.objects.all()
        print("-----------------",response.content)
        return render(request, 'subtasktypelist.html',{'actPage' :'RMSE - Sub Task Type','users':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())

def newtaskpriority(request):
    try:   
        return render(request, 'addtaskpriority.html',{'actPage':'RMSE - Add Task Priority'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

 
   
def showtaskpriority(request):
    try: 
        third_party_api_url = getAPIURL()+'task-priority-master/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        # prioobj = TaskPriorityMaster.objects.all()
        return render(request, 'taskprioritylist.html',{'actPage' :'RMSE - Task Priority','users':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())


@api_view(['POST'])

def addtskpriority(request):
    try:
        third_party_api_url = getAPIURL()+'task-priority-master/'

        label = request.POST.get('label', 'False') 
        description = request.POST.get('desc','False')
        update_id = request.POST.get('update_id','False')
        active_status=request.POST.get('rbactivests','False')
        print("active_status",active_status)

        if update_id != 'undefined':
            data_to_update = {
                'task_priority_label':label,
                'task_priority_description':description,
                'id':update_id,
                'activestatus':active_status
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.put(third_party_api_url, data= json.dumps(data_to_update),headers=header)
            print("----------------5")
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
        else:
            data_to_save = {
                'task_priority_label':label,
                'task_priority_description':description,
                'activestatus':active_status
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
            print("----------------5")
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def showtaskapprovalstatus(request):
    try: 
        third_party_api_url = getAPIURL()+'task-approval-status-master/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        # prioobj = TaskApprovalstatusMaster.objects.all()
        return render(request, 'taskapprovalstatuslist.html',{'actPage' :'RMSE - Task Approval Status','users':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())


def newtaskapprovalstatus(request):
    try:   
        return render(request, 'addtaskapprovalstatus.html',{'actPage':'RMSE - Add Task Approval Status'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())


@api_view(['POST'])

def addtskapprovalstatus(request):
    try:
        third_party_api_url = getAPIURL()+'task-approval-status-master/'

        label = request.POST.get('label', 'False') 
        description = request.POST.get('desc','False')
        update_id = request.POST.get('update_id','False')
        active_status=request.POST.get('rbactivests','False')
        print("active_status",active_status)

        if update_id != 'undefined':
            print()
            data_to_update = {
            'task_approvalstatus_label':label,
            'task_approvalstatus_description':description,
            'id':update_id,
            'activestatus':active_status
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.put(third_party_api_url, data= json.dumps(data_to_update),headers=header)
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
        else:
            data_to_save = {
                'task_approvalstatus_label':label,
                'task_approvalstatus_description':description,
                'activestatus':active_status
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
            print("----------------5")
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#Code for profile Update by Jayesh
def updateprofile(request):
    print("--------------idrequired",request.session['uid'])
    try:
        if request.session['username'] == 'admin':
            user = Users.objects.get(u_aid = request.session['uid'])
            print("---------------user_required",user)
            context = {
                'actPage':'RMSE - Update Profile',
                'fname':user.u_fname,
                'lname':user.u_lname,
                'email':user.u_email
            }
            print("-------------context",context['fname'])
            return render(request, 'updateprofile.html',context)
        else:
            user = Users.objects.get(u_aid = request.session['uid'])
            # print("---------------user_required base",user)
            context = {
                'actPage':'RMSE - Update Profile',
                'fname':user.u_fname,
                'lname':user.u_lname,
                'email':user.u_email
            }
            # print("-------------context base",context['fname'])
            return render(request, 'updateprofilebase.html',context)
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())
        # return render(request, 'updateprofile.html',{'actPage':'RMSE - Update Profile'})


def updateprofilerecord(request):
    try:
        print("---------add task type",request.GET)
        request_data = {x:request.GET.get(x) for x in request.GET.keys()}
        print("--------------------request_data",request_data)
        profile = Users.objects.get(u_aid=request_data['id'])
        profile.u_fname = request_data['fname']
        profile.u_lname = request_data['lname']
        profile.u_email = request_data['email']
        profile.save()
        print("save successfully")
        return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print("setuppycaret is",e) 
        print('setuppycaret traceback is ', traceback.print_exc()) 
        return JsonResponse(e)

#sub task type screen code bye jayesh
def showsubtasktype(request):
    try: 
        subtypeobj = SubTasktypeMaster.objects.all()
        print("-----------------",subtypeobj)
        return render(request, 'subtasktypelist.html',{'actPage' :'RMSE - Sub Task Type','users':subtypeobj})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())

def newsubtasktype(request):
    try: 
        third_party_api_url = getAPIURL()+'task-type-master/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("-----------------new",response.content)
        # typeobj = TaskTypeMaster.objects.all()
        return render(request, '    .html',{'actPage':'RMSE - Add Sub Task Type','tasktype':json.loads(response.content),'type':'add'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

            
@api_view(['POST'])

def addsubtsktype(request):
    try:
        third_party_api_url = getAPIURL()+'sub-task-type-master/'

        label = request.POST.get('label', 'False') 
        description = request.POST.get('desc','False')
        task_type_id = request.POST.get('task_type_aid','False')
        update_id = request.POST.get('update_id','False')
        active_status=request.POST.get('rbactivests','False')
        print("active_status",active_status)
        
        print("task_type_aid",task_type_id)
        if update_id != 'undefined':
            print()
            data_to_update= {
                'sub_task_type_label':label,
                'sub_task_type_description':description,
                'task_type_aid':task_type_id,
                'id':update_id,
                'activestatus':active_status
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.put(third_party_api_url, data= json.dumps(data_to_update),headers=header)
            print("----------------5")
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
        else:
            data_to_save = {
                'sub_task_type_label':label,
                'sub_task_type_description':description,
                'task_type_aid':task_type_id,
                'activestatus':active_status
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
            print("----------------5")
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#dashboard content screen
def showdashboardcontent(request):
    try: 
        content = DashboardContentMaster.objects.all()
        print("-----------------",content)
        return render(request, 'dashboardcontent.html',{'actPage' :'RMSE - Dashboard Content ','content':content})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())

def newdashboardcontent(request):
    try: 
        return render(request, 'adddashboardcontent.html',{'actPage':'RMSE - Add Dashboard Content'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def adddashboardcontent(request):
    print()
    try:
        print("---------add sub task type",request.GET)
        request_data = {x:request.GET.get(x) for x in request.GET.keys()}
        filter_srt_indx = DashboardContentMaster.objects.filter(sorting_index = request_data['sortindex'])
        if filter_srt_indx:
            return JsonResponse({"isvalid":"false"})
        else:
            taskfun_obj = DashboardContentMaster(display_type = request_data['displaytype'],source = request_data['source'],sorting_index = request_data['sortindex'])
            taskfun_obj.save()
            print("save successfully")
            return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print("setuppycaret is",e) 
        print('setuppycaret traceback is ', traceback.print_exc()) 
        return JsonResponse(e)



