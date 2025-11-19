from django.shortcuts import render ,redirect
import traceback
import os 
from pathlib import Path
import json 
import pandas as pd
from django.http import JsonResponse
from django.core import serializers 
from django.core.files.storage import FileSystemStorage
from datetime import *
from django.template import RequestContext
import numpy as np
import shutil 
import requests
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework import generics, permissions, status,serializers
from .RegModel.registermodel import RegisterModel as Register 

from .Adm_Utils.Masters import MasterTbls
from .DAL.dboperations import dbops
from .models import Users,UA
from .UserInfo.user import UserInfo
from .Validation.validation import Validation
from .RMSE.RMSE import RMSEModel
objreg=Register()  
objmaster=MasterTbls()
objvalidation=Validation()
objdbops=dbops()
objrmse=RMSEModel() 
from .models import *

def getAPIURL():
    api_url=os.environ['API_URL']
    return api_url

def rmse_calendar(request):    
    print("calling rmse_calendar")
    api_url=getAPIURL()+"getTasks/"   
    mdl_id = request.GET.get('mdl_id','')    
    data_to_save={'uid':request.session['uid'] ,'mdl_id':mdl_id} 
    header = {
    "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
    api_data=response.json() 
    print("api data task list",api_data)
    context={'all_data_lst':api_data['all_data_lst'],'taskList':api_data['taskList']}    
    return render(request,'rmse_calendar1.html',context)


def task_registration(request):
    print("task_registration")
   
    third_party_api_url_usr_all = getAPIURL()+'task_registration/'
    api_para={  
        'uid':request.session['uid'], 
        } 
    header = {
    "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
    }
    task_reg_res = requests.get(third_party_api_url_usr_all,data= json.dumps(api_para), headers=header)
    print("response task_reg_obj--------------------------",task_reg_res.content)
    task_reg_obj = json.loads(task_reg_res.content)
    print("task_reg_obj",task_reg_obj)
    added_by=task_reg_obj['added_by']
   
    
    assigned_to=[]#[]
    approved_by=[]
    task_assignee_thread_lst=[]
    task_approver_thread_lst=[]
    originatorid=added_by
    task_Major_Ver="1"
    task_Minor_Ver="0"


    print("post data",request.POST)
    request_data = {x:request.POST.get(x) for x in request.POST.keys()}
    print("postrequest_data",request_data)
    if request.method == 'POST':
        print("post")
        department=request_data['department']
        originator=request_data['originator']
        #print("Department",department,"Orginator",originator)
        task_function=request_data['task_function']
        registration_date=request_data['registration_date']
        print("registration_date",(registration_date))
        registration_date= datetime.strptime(registration_date, '%m/%d/%Y')
        # print ("The type of the date is now",  type(registration_date))
        # print ("The date is", registration_date)

        task_type=request_data['task_type']
        sub_task_type=request_data['sub_task_type']
        task_id=request_data['task_id']
        link_id=request_data['link_id']
        priority=request_data['priority']
        end_date=request_data['end_date']
        end_date= datetime.strptime(end_date, '%m/%d/%Y')

        completion_status=0 #request_data['completion_status']
        task_name=request_data['txt_Task_Name']
        approval_status=request_data['approval_status']
        relevant_personnel=request_data['relevant_personnel']
        task_summery_check=request_data['task_summery_check']
        print("task_summery_check",task_summery_check)

        assigned_to=request.POST.getlist('assigned_to')
        approved_by=request.POST.getlist('approved_by')

        api_url=getAPIURL()+"task_registration/"       
        data_to_save={
            "task_id": task_id,
            "department": department,
            "originator": originator,
            "task_function": task_function,
            "registration_date": registration_date.strftime('%Y-%m-%d'),
            "task_type": task_type,
            "sub_task_type": sub_task_type,
            "priority": priority,
            "end_date": end_date.strftime('%Y-%m-%d'),
            "completion_status": completion_status,
            "approval_status": approval_status,
            "task_major_version": task_Major_Ver,
            "task_minor_version": task_Minor_Ver,
            "addedby": added_by,
            "link_id": link_id,
            "task_name": task_name,
            "relevant_personnel":relevant_personnel,
            "assigned_to":assigned_to,
            "approved_by":approved_by,
            "originator_relevant":request_data['originator_relevant'],
            "task_summery_check":task_summery_check,
            "task_summery_comments":request_data['task_summery_comments'],
            "task_requirements_comments":request_data['task_requirements_comments'],
            # "task_assignee_comments":request_data['task_assignee_comments'],
            # "task_approver_comments":request_data['task_approver_comments'],
            "added_by":added_by
        }
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
       
        print("response",response)

        objmaster.insertActivityTrail(task_id,"7","New task created - "+task_name,request.session['uid'],request.session['accessToken'])
 

    context={'task_function_obj':task_reg_obj['task_function_obj'],'task_priority_obj':task_reg_obj['task_priority_obj'],
             'task_type_obj':task_reg_obj['task_type_obj'],'task_approval_master':task_reg_obj['task_approval_master'],
             'originator_name':task_reg_obj['originator_name'],'user_category_obj':task_reg_obj['user_category_obj'],
             'department_obj':task_reg_obj['department_obj'],'users_obj':task_reg_obj['users_obj'],
             'mdl_overview_obj':task_reg_obj['mdl_overview_obj'],'assigned_to_arr':json.dumps(assigned_to),
             'approved_by':json.dumps(approved_by),'originatorid':originatorid,'task_approver_thread_lst':json.dumps(task_approver_thread_lst),'task_assignee_thread_lst':json.dumps(task_assignee_thread_lst)}   
    return render(request,'task_registration.html',context)  


def get_sub_task_type(request): 
    print("get_sub_task_type")

    task_type_aid=request.GET.get('task_type')

    api_url=getAPIURL()+"get_sub_task_type/"       
    api_para={  
        'task_type_aid':task_type_aid, 
        } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
    sub_task_data=response.json()
    print("sub_task_data",sub_task_data)

    return JsonResponse(sub_task_data,safe=False)


def generate_task_ID(request):
    print("generate_task_ID")
    model_id=request.GET.get('model_id')
    task_type=request.GET.get('task_type')
    task_Lbl=request.GET.get('task_Lbl')
    print("model_id",model_id)

    api_url=getAPIURL()+"generate_task_ID/"       
    api_para={  
        'model_id':model_id, 
        'task_type':task_type,
        'task_Lbl':task_Lbl,
        } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
    task_link_ID=response.json()

    return JsonResponse(task_link_ID,safe=False)


def task_approver(request):
    
    taskid =request.GET.get('id', 'False')

    api_url=getAPIURL()+"task_approver/"       
    api_para={  
        'uid':request.session['uid'], 
        'id':taskid} 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
    api_data=response.json()
    print("api_data",api_data)

    context={"task_relevant_obj":api_data['task_relevant_obj'],'task_approval_master':api_data['task_approval_master'],'taskid':taskid,
            'originator_name':api_data['originator_name'],'approver_user_obj':api_data['approver_user_obj']}
    return render(request,'task_approver.html',context)


def get_task_ID_data(request):
    print("get_task_ID_data")
    task_id=request.GET.get('id')
    print("task_id",task_id)

    api_url=getAPIURL()+"get_task_ID_data/"       
    api_para={  
        'id':task_id} 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
    api=response.json()
    print("api",api)

    return JsonResponse({
        'department': api['department'],'originator': api['originator'],'task_function_label': api['task_function_label'],
        'reg_date': api['reg_date'],'task_type_label': api['task_type_label'],'sub_task_type_label': api['sub_task_type_label'],
        'task_priority_label': api['task_priority_label'],'end_date': api['end_date'],'completion_status': api['completion_status'],
        'task_summery': api['task_summery'],'task_name': api['task_name'],'task_req': api['task_req'],
        'task_approvalstatus_label': api['task_approvalstatus_label'],'approval_status': api['approval_status'],
        'task_assignee': api['task_assignee'],'approver_comments': api['approver_comments'],
        'task_dict': api['task_dict']
    })

def update_summery_data(request):
    print("update_summery_data")
    task_id=request.POST.get('task_id')
    print("task_id",task_id)
    print("get data",request.POST)
    assignee_comments=request.POST.get('assignee_comments')
    completion_status=request.POST.get('completion_status')
    print("completion_status",completion_status)
    approval=request.POST.get('approval_status')
    approver_comments=request.POST.get('approver_comments')
    print("approver_comments",approver_comments)
    update_date=datetime.now()
    updated_by=request.session['uid']
    
    api_url=getAPIURL()+"update_summery_data/"       
    data_update={  
        'uid':request.session['uid'],
        'accessToken':request.session['accessToken'],
        'task_id':task_id,
        'assignee_comments':assignee_comments,
        'completion_status':completion_status,
        'approval':approval,
        'updated_by':updated_by,
        'approver_comments':approver_comments
        } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.put(api_url, data= json.dumps(data_update),headers=header)
        
    api=response.json()
    print("api",api)


    return JsonResponse({'updated':api['updated'],'task_assignee_lst':api['task_assignee_lst'],
                         'task_approver_lst':api['task_approver_lst'],'originatorid':api['originatorid'],'task_id':api['task_id'],
                         'task_approver_thread_lst':api['task_approver_thread_lst'],
                         'task_assignee_thread_lst':api['task_assignee_thread_lst']}) 



def edit_task(request,task_id):
    print("task_id",task_id)

    #Task Function api url
    third_party_api_url_tskfun = getAPIURL()+'task-function-master/'
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response_tskfun = requests.get(third_party_api_url_tskfun, headers=header)
    task_function_objs = json.loads(response_tskfun.content)

    # task_function_objs=TaskFunctionMaster.objects.all()

    #TaskPriorityMaster API URL
    third_party_api_url_tskpriority = getAPIURL()+'task-priority-master/'
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response_tskpriority = requests.get(third_party_api_url_tskpriority, headers=header)
    task_priority_objs = json.loads(response_tskpriority.content)

    # task_priority_objs=TaskPriorityMaster.objects.all()
    # sub_task_type_objs=SubTasktypeMaster.objects.all()

    #TaskApprovalstatusMaster api url
    third_party_api_url = getAPIURL()+'task-approval-status-master/'
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(third_party_api_url, headers=header)
    print("response edit task Approval--------------------------",response.content)
    task_approval_master_objs = json.loads(response.content)

    # task_approval_master_objs=TaskApprovalstatusMaster.objects.all()    

    
    api_url=getAPIURL()+"edit_task/"       
    api_para={  
        'id':task_id} 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
    api=response.json()
    print("api",api)


    request_data = {x:request.POST.get(x) for x in request.POST.keys()}
    print("postrequest_data",request_data)
    if request.method == 'POST':
        print("post edit")
        task_id=request_data['task_id']
        print("task_id",task_id)
        department=request_data['department']
        originator=request_data['originator']
        #print("Department",department,"Orginator",originator)
        task_function=request_data['task_function_label']
        registration_date=request_data['reg_date']
        print("registration_date",(registration_date))
        registration_date= datetime.strptime(registration_date, '%m/%d/%Y')
        print("registration_date",(registration_date))
     
        task_type=request_data['task_type_label']
        task_aid=TaskTypeMaster.objects.get(task_type_label=task_type).task_type_aid
        sub_task_type=request_data['sub_task_type_label']
        priority=request_data['task_priority_label']
        end_date=request_data['end_date']
        end_date= datetime.strptime(end_date, '%m/%d/%Y')

        completion_status=request_data['completion_status']
        approval_status=request_data['approval_status']
        task_summery=request.POST.get('task_summery', '')
        task_name=request_data['txt_Task_Name']
        print("task_summery",task_summery)
        task_req=request_data['task_req']
        print("task_req",task_req)

        api_url=getAPIURL()+"edit_task/"       
        data_to_save={
            "task_id": task_id,
            "department": department,
            "originator": originator,
            "task_function": task_function,
            "registration_date": registration_date.strftime('%Y-%m-%d'),
            "task_type": task_aid,
            "sub_task_type": sub_task_type,
            "priority": priority,
            "end_date": end_date.strftime('%Y-%m-%d'),
            "completion_status": completion_status,
            "approval_status": approval_status,
            "task_summery": task_summery,
            "task_req": task_req,
            "task_name":task_name
        }
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.put(api_url, data= json.dumps(data_to_save),headers=header)
       
        print("response",response)

        
        return redirect('getTasks')
    context={
        'task_id': api['task_id'],
        'department': api['department'],
        'originator': api['originator'],
        'task_function_label': api['task_function_label'],
        'reg_date': api['reg_date'],
        'task_name': api['task_name'],
        'task_type_label': api['task_type_label'],
        'sub_task_type_label': api['sub_task_type_label'],
        'task_priority_label': api['task_priority_label'],
        'end_date': api['end_date'],
        'completion_status': api['completion_status'],
        'task_summery': api['task_summery'],
        'task_function': api['task_function'],
        'task_req': api['task_req'],
        'approval_status': api['approval_status'],
        'approval_status_label': api['approval_status_label'],
        'task_function_objs': task_function_objs,
        'priority': api['priority'],
        'sub_task_type': api['sub_task_type'],
        'sub_task_type_objs': api['sub_task_type_objs'],
        'task_priority_objs': task_priority_objs,
        'task_approval_master_objs': task_approval_master_objs,
        'originator_name': api['originator_name'],
        'approver_user_obj': api['approver_user_obj'],
        'assignee_user_obj': api['assignee_user_obj']
    }

    return render(request,'edit_task.html',context)

def task_assignee(request):
    taskid =request.GET.get('id', 'False')
    api_url=getAPIURL()+"task_assignee/"       
    api_para={  
        'uid':request.session['uid'], 
        'id':taskid} 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
    api_data=response.json()
    print('api_data',api_data)

    context={"task_relevant_obj":api_data['task_relevant_obj'],"taskid":taskid,'assignee_user_obj':api_data['assignee_user_obj'],
            'originator_name':api_data['originator_name'],'approver_user_obj':api_data['approver_user_obj']}
    return render(request,'task_assignee.html',context)



