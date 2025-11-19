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


def rmse_calendar_issue(request):
    api_url=getAPIURL()+"getIssue/"       
    mdl_id = request.GET.get('mdl_id','')    
    data_to_save={'uid':request.session['uid'] ,'mdl_id':mdl_id} 
    header = {
    "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
    api_data=response.json() 
    context={'all_data_lst':api_data['all_data_lst'],'issueList':api_data['mdldata']}       
    return render(request,'rmse_calendar_issue.html',context)  



def issue_registrartion(request):
    print("issue_registrartion")

    third_party_api_url_usr_all = getAPIURL()+'issue_registration/'
    api_para={  
        'uid':request.session['uid'], 
        } 
    header = {
    "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
    }
    issue_reg_res = requests.get(third_party_api_url_usr_all,data= json.dumps(api_para), headers=header)
    print("response issue_reg_res--------------------------",issue_reg_res.content)
    issue_reg_obj = json.loads(issue_reg_res.content)
    print("issue_reg_obj",issue_reg_obj)
    added_by=issue_reg_obj['added_by']
   

    issue_assigned_to=[]#[]
    issue_approved_by=[]
    issue_assignee_thread_lst=[]
    issue_approver_thread_lst=[]
    

    originatorid=added_by

    # max_issue_id=get_latest_issue()
    # Issue_ID="I"+str(max_issue_id)+"0100"
    issue_major_ver="1"
    issue_minor_ver="0"
    # print("Issue_ID",Issue_ID) 

   
    if request.method == 'POST':
        print("post")
        print("post data",request.POST)
        request_data = {x:request.POST.get(x) for x in request.POST.keys()}
        print("postrequest_data",request_data)
        department=request_data['department']
        originator=request_data['originator']
        #print("Department",department,"Orginator",originator)
        issue_function=request_data['issue_function']
        issue_registration_date=request_data['issue_registration_date']
        print("issue_registration_date",(issue_registration_date))
        issue_registration_date= datetime.strptime(issue_registration_date, '%m/%d/%Y')
        # print ("The type of the date is now",  type(registration_date))
        # print ("The date is", registration_date)

        issue_type=request_data['issue_type']
        sub_issue_type=request_data['sub_issue_type']
        issue_id=request_data['issue_id']
        link_id=request_data['link_id']
        issue_priority=request_data['issue_priority']
        issue_end_date=request_data['issue_end_date']
        issue_end_date= datetime.strptime(issue_end_date, '%m/%d/%Y')

        issue_completion_status=0 #request_data['issue_completion_status']
        issue_approval_status=request_data['issue_approval_status']
        issue_relevant_personnel_check=request_data['issue_relevant_personnel_check']
        issue_summery_check=request_data['issue_summery_check']
        print("issue_summery_check",issue_summery_check)

        api_url=getAPIURL()+"issue_registration/"       
        
        data_to_save = {
            "issue_id": issue_id,
            "department": department,
            "originator": originator,
            "issue_function": issue_function,
            "registration_date": issue_registration_date.strftime('%Y-%m-%d'),
            "issue_type": issue_type,
            "sub_issue_type": sub_issue_type,
            "priority": issue_priority,
            "end_date": issue_end_date.strftime('%Y-%m-%d'),
            "completion_status": issue_completion_status,
            "approval_status": issue_approval_status,
            "issue_major_ver": issue_major_ver,
            "issue_minor_ver": issue_minor_ver,
            "addedby": added_by,
            "link_id": link_id,

            "issue_relevant_personnel_check":issue_relevant_personnel_check,
            "issue_assigned_to":request.POST.getlist('issue_assigned_to'),
            "issue_approved_by":request.POST.getlist('issue_approved_by'),
            "issue_originator_relevant":request_data['issue_originator_relevant'],
            "issue_summery_check":issue_summery_check,
            "issue_summery_comments":request_data['issue_summery_comments'],
            "issue_requirements_comments":request_data['issue_requirements_comments'],
            # "issue_assignee_comments":request_data['issue_assignee_comments'],
            # "issue_approver_comments":request_data['issue_approver_comments'],
            "added_by":added_by
        }

        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
       
        print("response",response)

        objmaster.insertActivityTrail(issue_id,"10","New issue created.", request.session['uid'],request.session['accessToken'])

        
    context={'issue_function_obj':issue_reg_obj['issue_function_obj'],'issue_priority_obj':issue_reg_obj['issue_priority_obj'],
             'issue_type_obj':issue_reg_obj['issue_type_obj'],'issue_approval_master':issue_reg_obj['issue_approval_master'],
             'originator_name':issue_reg_obj['originator_name'],'user_category_obj':issue_reg_obj['user_category_obj'],
             'department_obj':issue_reg_obj['department_obj'],'users_obj':issue_reg_obj['users_obj'],
             'mdl_overview_obj':issue_reg_obj['mdl_overview_obj'],
             'issue_assigned_to':json.dumps(issue_assigned_to),
             'issue_approved_by':json.dumps(issue_approved_by),'originatorid':originatorid,'issue_approver_thread_lst':issue_approver_thread_lst,'issue_assignee_thread_lst':issue_assignee_thread_lst}  
    return render(request,'issue_registration.html',context)



def get_sub_issue_type(request):
    print("get_sub_issue_type")
    issue_type_aid=request.GET.get('issue_type')
    print("issue_type_aid",issue_type_aid)

    api_url=getAPIURL()+"get_sub_issue_type/"       
    api_para={  
        'issue_type_aid':issue_type_aid, 
        } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
    sub_issue_data=response.json()
    print("sub_issue_data",sub_issue_data)
    
    return JsonResponse(sub_issue_data,safe=False) 


def generate_issueID(request):
    print("generate_issueID")
    model_id=request.GET.get('model_id')
    issue_type=request.GET.get('issue_type')
    issue_Lbl=request.GET.get('issue_Lbl')
    print("model_id",model_id)

    api_url=getAPIURL()+"generate_issueID/"       
    api_para={  
        'model_id':model_id, 
        'issue_type':issue_type,
        'issue_Lbl':issue_Lbl,
        } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
    issue_link_ID=response.json()

    return JsonResponse(issue_link_ID,safe=False)



def issue_approver(request): 
    issueid =request.GET.get('id', 'False') 


    api_url=getAPIURL()+"issue_approver/"       
    api_para={  
        'uid':request.session['uid'], 
        'issue_id':issueid} 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
    api_data=response.json()
    print("api_data",api_data)
    print("issueid",api_data['issueid'])
    print("issue_relevant_obj",api_data['issue_relevant_obj'])

    context={"issue_relevant_obj":api_data['issue_relevant_obj'],'issueid':api_data['issueid'],'originator':api_data['originator'],
            'assignee_user_obj':api_data['assignee_user_obj'],'approver_user_obj':api_data['approver_user_obj'],
            'issue_approval_master':api_data['issue_approval_master']}
    return render(request,'issue_approver.html',context)

def issue_assignee(request): 
    issueid =request.GET.get('id', 'False') 

    api_url=getAPIURL()+"issue_assignee/"       
    api_para={  
        'uid':request.session['uid'], 
        'issue_id':issueid} 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
    api_data=response.json()
    print("api_data",api_data)


    context={"issue_relevant_obj":api_data['issue_relevant_obj'],'issueid':api_data['issueid'],'originator':api_data['originator'],
            'assignee_user_obj':api_data['assignee_user_obj'],'approver_user_obj':api_data['approver_user_obj'],
            'issue_approval_master':api_data['issue_approval_master']
            }
    return render(request,'issue_assignee.html',context)

def get_issue_ID_data(request):
    print("get_issue_ID_data believe")
    # task_id=request.GET.get('id')
    issue_id=request.GET.get('id')
    print("issue_id",issue_id)

    api_url=getAPIURL()+"get_issue_ID_data/"       
    api_para={  
        'id':issue_id} 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
    api=response.json()
    print("api",api)

    return JsonResponse({
        'department': api['department'],
        'originator': api['originator'],
        'issue_function_label': api['issue_function_label'],
        'reg_date': api['reg_date'],
        'issue_type_label': api['issue_type_label'],
        'sub_issue_type_label': api['sub_issue_type_label'],
        'issue_priority_label': api['issue_priority_label'],
        'end_date': api['end_date'],
        'completion_status': api['completion_status'],
        'issue_summery': api['issue_summery'],
        'issue_req': api['issue_req'],
        'issue_approvalstatus_label': api['issue_approvalstatus_label'],
        'approval_status': api['approval_status'],
        'issue_dict': api['issue_dict'],
        'issue_assignee': api['issue_assignee'],
        'approver_comments': api['approver_comments']
    }
    )

def issue_update_summery_data(request):
    print("issue_update_summery_data")
    issue_id=request.POST.get('issue_id')
    print("issue_id",issue_id)
    print("get data",request.POST)
    assignee_comments=request.POST.get('assignee_comments')
    completion_status=request.POST.get('completion_status')
    approver_comments=request.POST.get('approver_comments')
    approval=request.POST.get('approval_status')
    update_date=datetime.now()
    updated_by=request.session['uid']

    api_url=getAPIURL()+"issue_update_summery_data/"       
    data_update={  
        'uid':request.session['uid'],
        'accessToken':request.session['accessToken'],
        'issue_id':issue_id,
        'assignee_comments':assignee_comments,
        'completion_status':completion_status,
        'approver_comments':approver_comments,
        'approval':approval,
        'updated_by':updated_by
        } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.put(api_url, data= json.dumps(data_update),headers=header)
        
    api=response.json()
    print("api",api)

    return JsonResponse({'updated':api['updated'],'issue_assignee_lst':api['issue_assignee_lst'],
                            'issue_approver_lst':api['issue_approver_lst'],'originatorid':api['originatorid'],'issue_id':api['issue_id'],
                            'issue_assignee_thread_lst':api['issue_assignee_thread_lst']})

    

def edit_issue(request,issue_id):
    print("issue_id",issue_id)

    third_party_api_url_issue_fun = getAPIURL()+'issue-function-master/'
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response_issuefun = requests.get(third_party_api_url_issue_fun, headers=header)
    issue_function_objs = json.loads(response_issuefun.content)

    # issue_function_objs=IssueFunctionMaster.objects.all()

    third_party_api_url_issue_pri = getAPIURL()+'issue-priority-master/'
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response_issue_prio = requests.get(third_party_api_url_issue_pri, headers=header)
    issue_priority_objs = json.loads(response_issue_prio.content)

    # issue_priority_objs=IssuePriorityMaster.objects.all()

    third_party_api_url_issue_appro = getAPIURL()+'issue-approval-status-master/'
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response_issue_appro = requests.get(third_party_api_url_issue_appro, headers=header)
    issue_approval_master_objs = json.loads(response_issue_appro.content)

    # issue_approval_master_objs=IssueApprovalstatusMaster.objects.all()    

    api_url=getAPIURL()+"edit_issue/"       
    api_para={  
        'id':issue_id} 
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
        issue_id=request_data['issue_id']
        print("issue_id",issue_id)
        department=request_data['department']
        originator=request_data['originator']
        print("originator",originator)
        issue_function=request_data['issue_function_label']
        print("issue_function",issue_function)
        registration_date=request_data['reg_date']
        print("registration_date",(registration_date))
        registration_date= datetime.strptime(registration_date, '%m/%d/%Y')
        
        issue_type=request_data['issue_type_label']
        issue_aid=Issue_Type_Master.objects.get(issue_type_label=issue_type).issue_type_aid
        sub_issue_type=request_data['sub_issue_type_label']
        print("sub_issue_type",sub_issue_type)
        priority=request_data['issue_priority_label']
        end_date=request_data['end_date']
        end_date= datetime.strptime(end_date, '%m/%d/%Y')

        
        completion_status=request_data['completion_status']
        approval_status=request_data['approval_status']

        issue_summery=request_data['issue_summery']
        print("issue_summery",issue_summery)
        issue_req=request_data['issue_req']
        print("issue_req",issue_req)

        api_url=getAPIURL()+"edit_issue/"       
        
        data_to_save = {
            "issue_id": issue_id,
            "department": department,
            "originator": originator,
            "issue_function": issue_function,
            "registration_date": registration_date.strftime('%Y-%m-%d'),
            "issue_aid": issue_aid,
            "sub_issue_type": sub_issue_type,
            "priority": priority,
            "end_date": end_date.strftime('%Y-%m-%d'),
            "completion_status": completion_status,
            "approval_status": approval_status,
            "issue_summery":issue_summery,
            "issue_req":issue_req,

            # "issue_major_ver": issue_major_ver,
            # "issue_minor_ver": issue_minor_ver,
            # "addedby": added_by,
            # "link_id": link_id,

            # "issue_relevant_personnel_check":issue_relevant_personnel_check,
            # "issue_assigned_to":request.POST.getlist('issue_assigned_to'),
            # "issue_approved_by":request.POST.getlist('issue_approved_by'),
            # "issue_originator_relevant":request_data['issue_originator_relevant'],
            # "issue_summery_check":issue_summery_check,
            # "issue_summery_comments":request_data['issue_summery_comments'],
            # "issue_requirements_comments":request_data['issue_requirements_comments'],
            # "issue_assignee_comments":request_data['issue_assignee_comments'],
            # "issue_approver_comments":request_data['issue_approver_comments'],
            # "added_by":added_by
        }

        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.put(api_url, data= json.dumps(data_to_save),headers=header)
       
        print("response",response)

        return redirect('getIssues')

    context = {
        'issue_id': api['issue_id'],
        'department': api['department'],
        'originator': api['originator'],
        'issue_function_label': api['issue_function_label'],
        'issue_function': api['issue_function'],
        'reg_date': api['reg_date'],
        'issue_type_label': api['issue_type_label'],
        'sub_issue_type_label': api['sub_issue_type_label'],
        'sub_issue_type': api['sub_issue_type'],
        'issue_priority_label': api['issue_priority_label'],
        'end_date': api['end_date'],
        'completion_status': api['completion_status'],
        'issue_summery': api['issue_summery'],
        'priority': api['priority'],
        'assignee_user_obj': api['assignee_user_obj'],
        'approver_user_obj': api['approver_user_obj'],
        'issue_req': api['issue_req'],
        'approval_status': api['approval_status'],
        'issue_function_objs': issue_function_objs,
        'approval_status_label': api['approval_status_label'],
        'sub_issue_type_objs': api['sub_issue_type_objs'],
        'issue_priority_objs': issue_priority_objs,
        'issue_approval_master_objs': issue_approval_master_objs,
    }

    return render(request,'edit_issue.html',context)

