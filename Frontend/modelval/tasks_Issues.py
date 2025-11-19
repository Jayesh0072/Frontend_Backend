from datetime import datetime
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

BASE_DIR = Path(__file__).resolve().parent.parent
# Create your views here.
user_name = "user1"
file_path = os.path.join(BASE_DIR, 'static/Data/')
savefile_name = file_path +  "Modelinfo.csv" 
# Create your views here.
from modelval.models import *  
# DEFINE THE DATABASE CREDENTIALS
user = 'sa'
password = 'sqlAdm_18'
host = 'DESKTOP-NH98228\HCSPL18'
port = 1433
database = 'RMSE'
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
import requests
from rest_framework import generics, permissions, status,serializers

def getAPIURL():
    api_url=os.environ['API_URL']
    return api_url

# def task_registration(request):
#     print("task_registration")
#     #Username we are taking is unique
#     # user_obj=Users.objects.get(u_name=request.session['username'])
#     # print("UAID",user_obj.u_aid)
#     # added_by=user_obj.u_aid
#     # today_date=datetime.now()
#     # originator_name=user_obj.u_fname  +" " + user_obj.u_lname
#     # print("originator_name",originator_name)
#     # print("Dept_name",user_obj.dept_aid)
#     #User API URL
#     third_party_api_url_usr = getAPIURL()+'UpdateUser/'+str(request.session['uid'])
#     header = {
#     "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#     }
#     response_user = requests.get(third_party_api_url_usr, headers=header)
#     print("response User--------------------------",response_user.content)
#     user_obj = json.loads(response_user.content)
#     print("user_obj",user_obj)
#     added_by = user_obj['data']['u_aid']
#     today_date=datetime.now()
#     originator_name=user_obj['data']['u_fname']  +" " + user_obj['data']['u_lname']
#     ####
#     # department_obj=Department.objects.get(dept_aid=user_obj.dept_aid)
#     # print("dept name",department_obj.dept_label)
#     #Department URL api 
#     third_party_api_url_usr = getAPIURL()+'department/'+str(user_obj['data']['dept_aid'])
#     header = {
#     "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#     }
#     response_dept_data = requests.get(third_party_api_url_usr, headers=header)
#     department_obj = json.loads(response_dept_data.content)
#     print("department_obj",department_obj)
#     ####

#     # user_category_obj=UserCategory.objects.all()
#     #User Category API url
#     third_party_api_url = getAPIURL()+'UserCategory/'
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response_cat_data = requests.get(third_party_api_url, headers=header)
#     user_category_obj = json.loads(response_cat_data.content)
#     ###
#     # task_function_obj=TaskFunctionMaster.objects.all()
#     #Task Function api url
#     third_party_api_url_tskfun = getAPIURL()+'task-function-master/'
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response_tskfun = requests.get(third_party_api_url_tskfun, headers=header)
#     task_function_obj = json.loads(response_tskfun.content)
#     ####
#     # task_priority_obj=TaskPriorityMaster.objects.all()
#     #TaskPriorityMaster API URL
#     third_party_api_url_tskpriority = getAPIURL()+'task-priority-master/'
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response_tskpriority = requests.get(third_party_api_url_tskpriority, headers=header)
#     task_priority_obj = json.loads(response_tskpriority.content)
#     ####
#     # task_type_obj=TaskTypeMaster.objects.all()
#     #TaskTypeMaster api url
#     third_party_api_url_tsktype = getAPIURL()+'task-type-master/'
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response_tsktype = requests.get(third_party_api_url_tsktype, headers=header)
#     task_type_obj = json.loads(response_tsktype.content)
#     ###
#     task_approval_master=TaskApprovalstatusMaster.objects.all() 
#     #TaskApprovalstatusMaster api url
#     third_party_api_url = getAPIURL()+'task-approval-status-master/'
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response = requests.get(third_party_api_url, headers=header)
#     print("response edit task Approval--------------------------",response.content)
#     task_approval_data = json.loads(response.content)
#     ####   
#     # users_obj=Users.objects.all()
#     #User api url
#     third_party_api_url_usr_all = getAPIURL()+'UpdateUser/'
#     header = {
#     "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#     }
#     response_user_all = requests.get(third_party_api_url_usr_all, headers=header)
#     print("response User--------------------------",response_user_all.content)
#     users_obj = json.loads(response_user_all.content)
    
#     ####
#     mdl_overview_obj=ModelOverview.objects.all()

#     assigned_to=[]#[]
#     approved_by=[]
#     task_assignee_thread_lst=[]
#     task_approver_thread_lst=[]
#     originatorid=added_by
#     task_Major_Ver="1"
#     task_Minor_Ver="0"
#     # print("task_Id",task_Id) 
#     # print("task_max",task_max)

#     print("post data",request.POST)
#     request_data = {x:request.POST.get(x) for x in request.POST.keys()}
#     print("postrequest_data",request_data)
#     if request.method == 'POST':
#         print("post")
#         department=request_data['department']
#         originator=request_data['originator']
#         #print("Department",department,"Orginator",originator)
#         task_function=request_data['task_function']
#         registration_date=request_data['registration_date']
#         print("registration_date",(registration_date))
#         registration_date= datetime.strptime(registration_date, '%m/%d/%Y')
#         # print ("The type of the date is now",  type(registration_date))
#         # print ("The date is", registration_date)

#         task_type=request_data['task_type']
#         sub_task_type=request_data['sub_task_type']
#         task_id=request_data['task_id']
#         link_id=request_data['link_id']
#         priority=request_data['priority']
#         end_date=request_data['end_date']
#         end_date= datetime.strptime(end_date, '%m/%d/%Y')

#         completion_status=0 #request_data['completion_status']
#         task_name=request_data['txt_Task_Name']
#         approval_status=request_data['approval_status']
#         relevant_personnel=request_data['relevant_personnel']
#         task_summery_check=request_data['task_summery_check']
#         print("task_summery_check",task_summery_check)

#         assigned_to=request.POST.getlist('assigned_to')
#         approved_by=request.POST.getlist('approved_by')

#         api_url=getAPIURL()+"task_registration/"       
#         data_to_save={
#             "task_id": task_id,
#             "department": department,
#             "originator": originator,
#             "task_function": task_function,
#             "registration_date": registration_date.strftime('%Y-%m-%d'),
#             "task_type": task_type,
#             "sub_task_type": sub_task_type,
#             "priority": priority,
#             "end_date": end_date.strftime('%Y-%m-%d'),
#             "completion_status": completion_status,
#             "approval_status": approval_status,
#             "task_major_version": task_Major_Ver,
#             "task_minor_version": task_Minor_Ver,
#             "addedby": added_by,
#             "link_id": link_id,
#             "task_name": task_name,
#             "relevant_personnel":relevant_personnel,
#             "assigned_to":assigned_to,
#             "approved_by":approved_by,
#             "originator_relevant":request_data['originator_relevant'],
#             "task_summery_check":task_summery_check,
#             "task_summery_comments":request_data['task_summery_comments'],
#             "task_requirements_comments":request_data['task_requirements_comments'],
#             # "task_assignee_comments":request_data['task_assignee_comments'],
#             # "task_approver_comments":request_data['task_approver_comments'],
#             "added_by":added_by
#         }
#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }
#         response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
       
#         print("response",response)

#         objmaster.insertActivityTrail(task_id,"7","New task created - "+task_name,request.session['uid'],request.session['accessToken'])

        
#     print("department_obj",department_obj)
#     print("assigned_to before context",assigned_to)
#     context={'task_function_obj':task_function_obj,'task_priority_obj':task_priority_obj,'task_type_obj':task_type_obj,
#              'task_approval_master':task_approval_master,'originator_name':originator_name,'user_category_obj':user_category_obj,
#              'department_obj':department_obj,'users_obj':users_obj,'mdl_overview_obj':mdl_overview_obj,'assigned_to_arr':json.dumps(assigned_to),
#              'approved_by':json.dumps(approved_by),'originatorid':originatorid,'task_approver_thread_lst':json.dumps(task_approver_thread_lst),'task_assignee_thread_lst':json.dumps(task_assignee_thread_lst)}   
#     return render(request,'task_registration.html',context)  


# def get_sub_task_type(request): 
#     print("get_sub_task_type")

#     task_type_aid=request.GET.get('task_type')

#     api_url=getAPIURL()+"get_sub_task_type/"       
#     api_para={  
#         'task_type_aid':task_type_aid, 
#         } 
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
#     sub_task_data=response.json()
#     print("sub_task_data",sub_task_data)

#     return JsonResponse(sub_task_data,safe=False)



# def get_sub_issue_type(request):
#     print("get_sub_issue_type")
#     issue_type_aid=request.GET.get('issue_type')
#     print("issue_type_aid",issue_type_aid)

#     api_url=getAPIURL()+"get_sub_issue_type/"       
#     api_para={  
#         'issue_type_aid':issue_type_aid, 
#         } 
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
#     sub_issue_data=response.json()
#     print("sub_issue_data",sub_issue_data)
    
#     return JsonResponse(sub_issue_data,safe=False) 


def show_alert(request):
    user_obj=Users.objects.get(u_name=request.session['username'])
    print("UAID",user_obj.u_aid)
    
    alerts_obj=Alert.objects.filter(u_aid=user_obj.u_aid)
    for i in alerts_obj:
        print("user_id",i.recipient)
        
        #get_first_last=Users.objects.get(u_aid='')
    context={'alerts_obj':alerts_obj}
    return render(request,'show_alert.html',context)

def alert(request):
    print("alert")
    user_obj=Users.objects.get(u_name=request.session['username'])
    print("UAID",user_obj.u_aid)
    recipient_name=user_obj.u_fname  +" " + user_obj.u_lname
    print("recipient_name",recipient_name)
    users_obj=Users.objects.all()

    if request.method =="POST":
        author=request.POST['author']
        recipient=request.POST.getlist('recipient')
        
        alert_date=request.POST['alert_date']
        alert_date= datetime.strptime(alert_date, '%d/%m/%Y')
        days_prior=request.POST['days_prior']
        period=request.POST['period']
        comments=request.POST['alert_comments']
        first_last_list=list()
        for i in recipient:
            #print("i",i)
            user_first_last=Users.objects.get(u_aid=i)
            first_last_list.append(user_first_last.u_fname +" "+user_first_last.u_lname )
            # print("firstLast",user_first_last.u_fname,user_first_last.u_lname)
            print("list",first_last_list)
        alert_obj=Alert(author=author,recipient=first_last_list,alert_date=alert_date,days_prior=days_prior,
                        period=period,comments=comments,u_aid=user_obj)
        alert_obj.save()
    context={'recipient_name':recipient_name,'users_obj':users_obj}
    return render(request,'alert.html',context)
 

# def issue_registrartion(request):
#     print("issue_registrartion")
#     user_obj=Users.objects.get(u_name=request.session['username'])
#     print("UAID",user_obj.u_aid)
#     added_by=user_obj.u_aid
#     today_date=datetime.now()
#     originator_name=user_obj.u_fname  +" " + user_obj.u_lname
#     print("originator_name",originator_name)
#     print("Dept_name",user_obj.dept_aid)

#     department_obj=Department.objects.get(dept_aid=user_obj.dept_aid)
#     print("dept name",department_obj.dept_label)

#     user_category_obj=UserCategory.objects.all()
#     issue_function_obj=IssueFunctionMaster.objects.all()
#     issue_priority_obj=IssuePriorityMaster.objects.all()
#     issue_approval_master=IssueApprovalstatusMaster.objects.all()    
#     users_obj=Users.objects.all()
#     mdl_overview_obj=ModelOverview.objects.all()
#     issue_type_obj=Issue_Type_Master.objects.all()
   

#     issue_assigned_to=[]#[]
#     issue_approved_by=[]
#     issue_assignee_thread_lst=[]
#     issue_approver_thread_lst=[]
    

#     originatorid=added_by

#     # max_issue_id=get_latest_issue()
#     # Issue_ID="I"+str(max_issue_id)+"0100"
#     issue_major_ver="1"
#     issue_minor_ver="0"
#     # print("Issue_ID",Issue_ID) 

#     print("post data",request.POST)
#     request_data = {x:request.POST.get(x) for x in request.POST.keys()}
#     print("postrequest_data",request_data)
#     if request.method == 'POST':
#         print("post")
#         department=request_data['department']
#         originator=request_data['originator']
#         #print("Department",department,"Orginator",originator)
#         issue_function=request_data['issue_function']
#         issue_registration_date=request_data['issue_registration_date']
#         print("issue_registration_date",(issue_registration_date))
#         issue_registration_date= datetime.strptime(issue_registration_date, '%m/%d/%Y')
#         # print ("The type of the date is now",  type(registration_date))
#         # print ("The date is", registration_date)

#         issue_type=request_data['issue_type']
#         sub_issue_type=request_data['sub_issue_type']
#         issue_id=request_data['issue_id']
#         link_id=request_data['link_id']
#         issue_priority=request_data['issue_priority']
#         issue_end_date=request_data['issue_end_date']
#         issue_end_date= datetime.strptime(issue_end_date, '%m/%d/%Y')

#         issue_completion_status=request_data['issue_completion_status']
#         issue_approval_status=request_data['issue_approval_status']
#         issue_relevant_personnel_check=request_data['issue_relevant_personnel_check']
#         issue_summery_check=request_data['issue_summery_check']
#         print("issue_summery_check",issue_summery_check)
     
#         issue_registration_obj=IssueRegistration(issue_id=issue_id,department=department,originator=originator,issue_function=issue_function,
#                                                registration_date=issue_registration_date,issue_type=issue_type,sub_issue_type=sub_issue_type,
#                                                priority=issue_priority,end_date=issue_end_date,completion_status=issue_completion_status,
#                                                approval_status=issue_approval_status,issue_major_ver=issue_major_ver,
#                                                issue_minor_ver=issue_minor_ver,addedby=added_by,adddate=today_date,
#                                                link_id=link_id
#                                                )         
        
#         issue_registration_obj.save()
#         objmaster.insertActivityTrail(issue_id,"10","New issue created.", request.session['uid'],request.session['accessToken'])
#         if issue_relevant_personnel_check == 'True':
#             originator_relevant=request_data['issue_originator_relevant']
#             issue_assigned_to=request.POST.getlist('issue_assigned_to')
#             issue_approved_by=request.POST.getlist('issue_approved_by')
#             print('issue_approved_by',issue_approved_by)
#             print('issue_assigned_to',issue_assigned_to)
#             # print('Relevant Personnel',relevant_personnel,originator_relevant,assigned_to,approved_by)
#             if originator_relevant:
#                 issue_relevant_personnel_obj=IssueRelevantPersonnel(u_type="Originator",u_id=user_obj.u_aid,
#                                                      issue=issue_registration_obj,addedby=added_by,adddate=today_date)
#                 issue_relevant_personnel_obj.save()

#             for i in issue_assigned_to:
#                 print('issue_assigned_to',i)
               
#                 issue_relevant_personnel_obj=IssueRelevantPersonnel(u_type="Assignee",u_id=i,
#                                                      issue=issue_registration_obj,addedby=added_by,adddate=today_date)
#                 issue_relevant_personnel_obj.save()
#                 #notification code
#                 notification_trigger="New issue registered - "+ issue_id  
#                 insert_data_notification(added_by,i,"Issue",notification_trigger,1)
#                 print("notificatio assigeee saved")
#                 thread_id=thread_creation(added_by,i)
#                 issue_assignee_thread_lst.append({"from": str(added_by), "to": str(i),"thread_id":str(thread_id)})
#             for j in issue_approved_by:
#                 print('issue_approved_by',j)      
        
#                 issue_relevant_personnel_obj=IssueRelevantPersonnel(u_type="Approver",u_id=j,
#                                                      issue=issue_registration_obj,addedby=added_by,adddate=today_date)
#                 issue_relevant_personnel_obj.save()
#                 #notification code
#                 notification_trigger="New issue registered - "+ issue_id  
#                 insert_data_notification(added_by,i,"Issue",notification_trigger,1)
#                 print("notificatio assigeee saved")
#                 thread_id=thread_creation(added_by,j)
#                 issue_approver_thread_lst.append({"from": str(added_by), "to": str(j),"thread_id":str(thread_id)})
                
#         if issue_summery_check == 'True':
#             issue_summery=request_data['issue_summery']
#             issue_requirement=request_data['issue_requirement']
#             issue_assignee_comments=request_data['issue_assignee_comments']
#             # issue_approval=request_data['issue_approval']
#             issue_approver_comments=request_data['issue_approver_comments']

            
#             issue_summery_obj=IssueSummery(issue_summery=issue_summery,issue_requirement=issue_requirement,assignee_comments=issue_assignee_comments,
#                                                      approver_comments=issue_approver_comments,
#                                                      issue=issue_registration_obj,addedby=added_by,adddate=today_date)
#             issue_summery_obj.save() 
    
#     context={'issue_function_obj':issue_function_obj,'issue_priority_obj':issue_priority_obj,'issue_type_obj':issue_type_obj,
#              'issue_approval_master':issue_approval_master,'originator_name':originator_name,'user_category_obj':user_category_obj,
#              'department_obj':department_obj,'users_obj':users_obj,'mdl_overview_obj':mdl_overview_obj,
#              'issue_type_obj':issue_type_obj,'issue_assigned_to':json.dumps(issue_assigned_to),
#              'issue_approved_by':json.dumps(issue_approved_by),'originatorid':originatorid,'issue_approver_thread_lst':issue_approver_thread_lst,'issue_assignee_thread_lst':issue_assignee_thread_lst}  
#     return render(request,'issue_registration.html',context)


# def issue_registrartion(request):
#     print("issue_registrartion")

#     #User API URL
#     third_party_api_url_usr = getAPIURL()+'UpdateUser/'+str(request.session['uid'])
#     header = {
#     "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#     }
#     response_user = requests.get(third_party_api_url_usr, headers=header)
#     print("response User--------------------------",response_user.content)
#     user_obj = json.loads(response_user.content)
#     print("user_obj",user_obj)
#     # user_obj=Users.objects.get(u_name=request.session['username'])
#     added_by = user_obj['data']['u_aid']
#     today_date=datetime.now()
#     originator_name=user_obj['data']['u_fname']  +" " + user_obj['data']['u_lname']
#     ####
#     # department_obj=Department.objects.get(dept_aid=user_obj.dept_aid)
#     # print("dept name",department_obj.dept_label)
#     #Department URL api 
#     third_party_api_depart = getAPIURL()+'department/'+str(user_obj['data']['dept_aid'])
#     header = {
#     "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#     }
#     response_dept_data = requests.get(third_party_api_depart, headers=header)
#     department_obj = json.loads(response_dept_data.content)
#     print("department_obj",department_obj)

#     #User Category API url
#     third_party_api_url = getAPIURL()+'UserCategory/'
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response_cat_data = requests.get(third_party_api_url, headers=header)
#     user_category_obj = json.loads(response_cat_data.content)

#     # user_category_obj=UserCategory.objects.all()

#     third_party_api_url_issue_fun = getAPIURL()+'issue-function-master/'
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response_issuefun = requests.get(third_party_api_url_issue_fun, headers=header)
#     issue_function_obj = json.loads(response_issuefun.content)

#     # issue_function_obj=IssueFunctionMaster.objects.all()

#     third_party_api_url_issue_pri = getAPIURL()+'issue-priority-master/'
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response_issue_prio = requests.get(third_party_api_url_issue_pri, headers=header)
#     issue_priority_obj = json.loads(response_issue_prio.content)

#     # issue_priority_obj=IssuePriorityMaster.objects.all()

#     third_party_api_url_issue_appro = getAPIURL()+'issue-approval-status-master/'
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response_issue_appro = requests.get(third_party_api_url_issue_appro, headers=header)
#     issue_approval_master = json.loads(response_issue_appro.content)

#     # issue_approval_master=IssueApprovalstatusMaster.objects.all()  
#     #   
#     #User api url
#     third_party_api_url_usr_all = getAPIURL()+'UpdateUser/'
#     header = {
#     "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#     }
#     response_user_all = requests.get(third_party_api_url_usr_all, headers=header)
#     print("response User--------------------------",response_user_all.content)
#     users_obj = json.loads(response_user_all.content)

#     # users_obj=Users.objects.all()
#     mdl_overview_obj=ModelOverview.objects.all()

#     third_party_api_url_issue_type = getAPIURL()+'issue-type-master/'
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response_issuetype = requests.get(third_party_api_url_issue_type, headers=header)
#     issue_type_obj = json.loads(response_issuetype.content)
#     # issue_type_obj=Issue_Type_Master.objects.all()
   

#     issue_assigned_to=[]#[]
#     issue_approved_by=[]
#     issue_assignee_thread_lst=[]
#     issue_approver_thread_lst=[]
    

#     originatorid=added_by

#     # max_issue_id=get_latest_issue()
#     # Issue_ID="I"+str(max_issue_id)+"0100"
#     issue_major_ver="1"
#     issue_minor_ver="0"
#     # print("Issue_ID",Issue_ID) 

   
#     if request.method == 'POST':
#         print("post")
#         print("post data",request.POST)
#         request_data = {x:request.POST.get(x) for x in request.POST.keys()}
#         print("postrequest_data",request_data)
#         department=request_data['department']
#         originator=request_data['originator']
#         #print("Department",department,"Orginator",originator)
#         issue_function=request_data['issue_function']
#         issue_registration_date=request_data['issue_registration_date']
#         print("issue_registration_date",(issue_registration_date))
#         issue_registration_date= datetime.strptime(issue_registration_date, '%m/%d/%Y')
#         # print ("The type of the date is now",  type(registration_date))
#         # print ("The date is", registration_date)

#         issue_type=request_data['issue_type']
#         sub_issue_type=request_data['sub_issue_type']
#         issue_id=request_data['issue_id']
#         link_id=request_data['link_id']
#         issue_priority=request_data['issue_priority']
#         issue_end_date=request_data['issue_end_date']
#         issue_end_date= datetime.strptime(issue_end_date, '%m/%d/%Y')

#         issue_completion_status=0 #request_data['issue_completion_status']
#         issue_approval_status=request_data['issue_approval_status']
#         issue_relevant_personnel_check=request_data['issue_relevant_personnel_check']
#         issue_summery_check=request_data['issue_summery_check']
#         print("issue_summery_check",issue_summery_check)

#         api_url=getAPIURL()+"issue_registration/"       
        
#         data_to_save = {
#             "issue_id": issue_id,
#             "department": department,
#             "originator": originator,
#             "issue_function": issue_function,
#             "registration_date": issue_registration_date.strftime('%Y-%m-%d'),
#             "issue_type": issue_type,
#             "sub_issue_type": sub_issue_type,
#             "priority": issue_priority,
#             "end_date": issue_end_date.strftime('%Y-%m-%d'),
#             "completion_status": issue_completion_status,
#             "approval_status": issue_approval_status,
#             "issue_major_ver": issue_major_ver,
#             "issue_minor_ver": issue_minor_ver,
#             "addedby": added_by,
#             "link_id": link_id,

#             "issue_relevant_personnel_check":issue_relevant_personnel_check,
#             "issue_assigned_to":request.POST.getlist('issue_assigned_to'),
#             "issue_approved_by":request.POST.getlist('issue_approved_by'),
#             "issue_originator_relevant":request_data['issue_originator_relevant'],
#             "issue_summery_check":issue_summery_check,
#             "issue_summery_comments":request_data['issue_summery_comments'],
#             "issue_requirements_comments":request_data['issue_requirements_comments'],
#             # "issue_assignee_comments":request_data['issue_assignee_comments'],
#             # "issue_approver_comments":request_data['issue_approver_comments'],
#             "added_by":added_by
#         }

#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }
#         response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
       
#         print("response",response)

#         objmaster.insertActivityTrail(issue_id,"10","New issue created.", request.session['uid'],request.session['accessToken'])

        
#     context={'issue_function_obj':issue_function_obj,'issue_priority_obj':issue_priority_obj,'issue_type_obj':issue_type_obj,
#              'issue_approval_master':issue_approval_master,'originator_name':originator_name,'user_category_obj':user_category_obj,
#              'department_obj':department_obj,'users_obj':users_obj,'mdl_overview_obj':mdl_overview_obj,
#              'issue_type_obj':issue_type_obj,'issue_assigned_to':json.dumps(issue_assigned_to),
#              'issue_approved_by':json.dumps(issue_approved_by),'originatorid':originatorid,'issue_approver_thread_lst':issue_approver_thread_lst,'issue_assignee_thread_lst':issue_assignee_thread_lst}  
#     return render(request,'issue_registration.html',context)




# def generate_issueID(request):
#     print("generate_issueID")
#     model_id=request.GET.get('model_id')
#     issue_type=request.GET.get('issue_type')
#     issue_Lbl=request.GET.get('issue_Lbl')
#     print("model_id",model_id)

#     api_url=getAPIURL()+"generate_issueID/"       
#     api_para={  
#         'model_id':model_id, 
#         'issue_type':issue_type,
#         'issue_Lbl':issue_Lbl,
#         } 
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
#     issue_link_ID=response.json()

#     return JsonResponse(issue_link_ID,safe=False)

# def generate_task_ID(request):
#     print("generate_task_ID")
#     model_id=request.GET.get('model_id')
#     task_type=request.GET.get('task_type')
#     task_Lbl=request.GET.get('task_Lbl')
#     print("model_id",model_id)

#     api_url=getAPIURL()+"generate_task_ID/"       
#     api_para={  
#         'model_id':model_id, 
#         'task_type':task_type,
#         'task_Lbl':task_Lbl,
#         } 
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
#     task_link_ID=response.json()

#     return JsonResponse(task_link_ID,safe=False)


# def task_approver(request):
    
#     taskid =request.GET.get('id', 'False')
#     api_url=getAPIURL()+"task_approver/"       
#     api_para={  
#         'uid':request.session['uid'], 
#         'id':taskid} 
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
#     api_data=response.json()
#     # task_approval_master=TaskApprovalstatusMaster.objects.all()
#     # task_relevant_obj=Task_Relevant_Personnel.objects.filter(u_id=U_id,u_type="Approver")
#     context={"task_relevant_obj":api_data['task_relevant_obj'],'task_approval_master':api_data['task_approval_master'],'taskid':taskid}
#     return render(request,'task_approver.html',context)

# def edit_task(request,task_id):
#     print("task_id",task_id)


# def task_approver(request):
    
#     taskid =request.GET.get('id', 'False')

#     api_url=getAPIURL()+"task_approver/"       
#     api_para={  
#         'uid':request.session['uid'], 
#         'id':taskid} 
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
#     api_data=response.json()
#     print("api_data",api_data)

#     context={"task_relevant_obj":api_data['task_relevant_obj'],'task_approval_master':api_data['task_approval_master'],'taskid':taskid,
#             'originator_name':api_data['originator_name'],'approver_user_obj':api_data['approver_user_obj']}
#     return render(request,'task_approver.html',context)


# def task_assignee(request):
#     taskid =request.GET.get('id', 'False')
#     api_url=getAPIURL()+"task_assignee/"       
#     api_para={  
#         'uid':request.session['uid'], 
#         'id':taskid} 
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
#     api_data=response.json()
#     print('api_data',api_data)

#     context={"task_relevant_obj":api_data['task_relevant_obj'],"taskid":taskid,'assignee_user_obj':api_data['assignee_user_obj'],
#             'originator_name':api_data['originator_name'],'approver_user_obj':api_data['approver_user_obj']}
#     return render(request,'task_assignee.html',context)



# def get_task_ID_data(request):
#     print("get_task_ID_data")
#     task_id=request.GET.get('id')
#     print("task_id",task_id)

#     api_url=getAPIURL()+"get_task_ID_data/"       
#     api_para={  
#         'id':task_id} 
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
#     api=response.json()
#     print("api",api)

#     return JsonResponse({
#         'department': api['department'],'originator': api['originator'],'task_function_label': api['task_function_label'],
#         'reg_date': api['reg_date'],'task_type_label': api['task_type_label'],'sub_task_type_label': api['sub_task_type_label'],
#         'task_priority_label': api['task_priority_label'],'end_date': api['end_date'],'completion_status': api['completion_status'],
#         'task_summery': api['task_summery'],'task_name': api['task_name'],'task_req': api['task_req'],
#         'task_approvalstatus_label': api['task_approvalstatus_label'],'approval_status': api['approval_status'],
#         'task_assignee': api['task_assignee'],'approver_comments': api['approver_comments'],
#         'task_dict': api['task_dict']
#     })

# def update_summery_data(request):
#     print("update_summery_data")
#     task_id=request.POST.get('task_id')
#     print("task_id",task_id)
#     print("get data",request.POST)
#     assignee_comments=request.POST.get('assignee_comments')
#     completion_status=request.POST.get('completion_status')
#     print("completion_status",completion_status)
#     approval=request.POST.get('approval_status')
#     approver_comments=request.POST.get('approver_comments')
#     print("approver_comments",approver_comments)
#     update_date=datetime.now()
#     updated_by=request.session['uid']
    
#     api_url=getAPIURL()+"update_summery_data/"       
#     data_update={  
#         'uid':request.session['uid'],
#         'accessToken':request.session['accessToken'],
#         'task_id':task_id,
#         'assignee_comments':assignee_comments,
#         'completion_status':completion_status,
#         'approval':approval,
#         'updated_by':updated_by,
#         'approver_comments':approver_comments
#         } 
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response = requests.put(api_url, data= json.dumps(data_update),headers=header)
        
#     api=response.json()
#     print("api",api)


#     return JsonResponse({'updated':api['updated'],'task_assignee_lst':api['task_assignee_lst'],
#                          'task_approver_lst':api['task_approver_lst'],'originatorid':api['originatorid'],'task_id':api['task_id'],
#                          'task_approver_thread_lst':api['task_approver_thread_lst'],
#                          'task_assignee_thread_lst':api['task_assignee_thread_lst']}) 


# def issue_approver(request): 
#     taskid =request.GET.get('id', 'False') 
#     api_url=getAPIURL()+"issue_approver/"       
#     api_para={  
#         'uid':request.session['uid'], 
#         'id':taskid} 
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
#     api_data=response.json()
#     context={"issue_relevant_obj":api_data['issue_relevant_obj'],'task_approval_master':api_data['task_approval_master'],'taskid':taskid}
#     return render(request,'issue_approver.html',context)

# def issue_assignee(request): 
#     taskid =request.GET.get('id', 'False') 
#     api_url=getAPIURL()+"issue_assignee/"       
#     api_para={  
#         'uid':request.session['uid'],
#           'id':taskid } 
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
#     api_data=response.json() 
#     context={"issue_relevant_obj":api_data['issue_relevant_obj'],'taskid':taskid}
#     return render(request,'issue_assignee.html',context)


# def issue_approver(request): 
#     issueid =request.GET.get('id', 'False') 


#     api_url=getAPIURL()+"issue_approver/"       
#     api_para={  
#         'uid':request.session['uid'], 
#         'issue_id':issueid} 
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
#     api_data=response.json()
#     print("api_data",api_data)
#     print("issueid",api_data['issueid'])
#     print("issue_relevant_obj",api_data['issue_relevant_obj'])

#     context={"issue_relevant_obj":api_data['issue_relevant_obj'],'issueid':api_data['issueid'],'originator':api_data['originator'],
#             'assignee_user_obj':api_data['assignee_user_obj'],'approver_user_obj':api_data['approver_user_obj'],
#             'issue_approval_master':api_data['issue_approval_master']}
#     return render(request,'issue_approver.html',context)

# def issue_assignee(request): 
#     issueid =request.GET.get('id', 'False') 

#     api_url=getAPIURL()+"issue_assignee/"       
#     api_para={  
#         'uid':request.session['uid'], 
#         'issue_id':issueid} 
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
#     api_data=response.json()
#     print("api_data",api_data)


#     context={"issue_relevant_obj":api_data['issue_relevant_obj'],'issueid':api_data['issueid'],'originator':api_data['originator'],
#             'assignee_user_obj':api_data['assignee_user_obj'],'approver_user_obj':api_data['approver_user_obj'],
#             'issue_approval_master':api_data['issue_approval_master']
#             }
#     return render(request,'issue_assignee.html',context)

# def get_issue_ID_data(request):
#     print("get_issue_ID_data believe")
#     # task_id=request.GET.get('id')
#     issue_id=request.GET.get('id')
#     print("issue_id",issue_id)

#     api_url=getAPIURL()+"get_issue_ID_data/"       
#     api_para={  
#         'id':issue_id} 
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
#     api=response.json()
#     print("api",api)

#     return JsonResponse({
#         'department': api['department'],
#         'originator': api['originator'],
#         'issue_function_label': api['issue_function_label'],
#         'reg_date': api['reg_date'],
#         'issue_type_label': api['issue_type_label'],
#         'sub_issue_type_label': api['sub_issue_type_label'],
#         'issue_priority_label': api['issue_priority_label'],
#         'end_date': api['end_date'],
#         'completion_status': api['completion_status'],
#         'issue_summery': api['issue_summery'],
#         'issue_req': api['issue_req'],
#         'issue_approvalstatus_label': api['issue_approvalstatus_label'],
#         'approval_status': api['approval_status'],
#         'issue_dict': api['issue_dict'],
#         'issue_assignee': api['issue_assignee'],
#         'approver_comments': api['approver_comments']
#     }
#     )

# def issue_update_summery_data(request):
#     print("issue_update_summery_data")
#     issue_id=request.POST.get('issue_id')
#     print("issue_id",issue_id)
#     print("get data",request.POST)
#     assignee_comments=request.POST.get('assignee_comments')
#     completion_status=request.POST.get('completion_status')
#     approver_comments=request.POST.get('approver_comments')
#     approval=request.POST.get('approval_status')
#     update_date=datetime.now()
#     updated_by=request.session['uid']

#     api_url=getAPIURL()+"issue_update_summery_data/"       
#     data_update={  
#         'uid':request.session['uid'],
#         'accessToken':request.session['accessToken'],
#         'issue_id':issue_id,
#         'assignee_comments':assignee_comments,
#         'completion_status':completion_status,
#         'approver_comments':approver_comments,
#         'approval':approval,
#         'updated_by':updated_by
#         } 
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response = requests.put(api_url, data= json.dumps(data_update),headers=header)
        
#     api=response.json()
#     print("api",api)

#     return JsonResponse({'updated':api['updated'],'issue_assignee_lst':api['issue_assignee_lst'],
#                             'issue_approver_lst':api['issue_approver_lst'],'originatorid':api['originatorid'],'issue_id':api['issue_id'],
#                             'issue_assignee_thread_lst':api['issue_assignee_thread_lst']})

    

def insert_data_notification(notification_from,notification_to,utility,notification_trigger,is_visible):
     
    create_date=datetime.now()
    notification_obj=NotificationDetails(notification_from=notification_from,notification_to=notification_to,utility=utility,
                                         notification_trigger=notification_trigger,is_visible=is_visible,create_date=create_date)
    notification_obj.save() 

def thread_creation(send_by,send_to): 
    print('send_by,send_to ',send_by,send_to)
    threadfilter = Thread.objects.filter(first_person = send_by,second_person = send_to) | Thread.objects.filter(second_person = send_by,first_person = send_to)
    print("threadfilter is ",threadfilter)
    if not threadfilter:
        curr_user_id = Users.objects.get(u_aid = send_by)
        print("curr_user_id",curr_user_id)
        othr_usr_id = Users.objects.get(u_aid = send_to)
        print("othr_usr_id",othr_usr_id)
        threadobj = Thread(first_person = curr_user_id,second_person = othr_usr_id)
        threadobj.save()
        thread_id = threadobj.thread_id
        print('inside if')
        return thread_id
        # print("save thread successfully")             
    else: 
        print('inside else')
        from django.db.models import Q
        threadobj = Thread.objects.get(Q(first_person = send_by,second_person = send_to) |Q(first_person = send_to,second_person = send_by) )
        # threadobj = Thread.objects.get(first_person = send_to,second_person = send_by) 
        thread_id = threadobj.thread_id
        print("pass",thread_id)
        return thread_id
        # pass
    
def show_task(request):
    print( request.session['uid'])
    task_obj=TaskRegistration.objects.filter(addedby=request.session['uid'])
    all_data_lst=list()
    dict_data=dict()
    for i in task_obj:
        # print("task_id",i.task_id)
        dict_data['task_id']=i.task_id
        dict_data['completion_status']=i.completion_status
        dict_data['reg_date']=i.registration_date
        task_type_data=TaskTypeMaster.objects.get(task_type_aid=i.task_type).task_type_label
        dict_data['task_type']=task_type_data
        print("task_type_data",task_type_data)
        sub_task_type_data=SubTasktypeMaster.objects.get(sub_task_type_aid=i.sub_task_type).sub_task_type_label
        dict_data['sub_task_type']=sub_task_type_data
        priority_data=TaskPriorityMaster.objects.get(task_priority_aid=i.priority).task_priority_label
        dict_data['priority']=priority_data
        print("approval",i.approval_status)
        approval_data=TaskApprovalstatusMaster.objects.get(task_approvalstatus_aid=i.approval_status).task_approvalstatus_label
        print("approval_data"),approval_data
        dict_data['approval_status']=approval_data
        print("dict_data",dict_data)
        all_data_lst.append(dict_data.copy())

    print("all_data_lst",all_data_lst)
    context={'all_data_lst':all_data_lst}    
    return render(request,'show_task.html',context)

# def edit_task(request,task_id):
#     print("task_id",task_id)

#     #Task Function api url
#     third_party_api_url_tskfun = getAPIURL()+'task-function-master/'
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response_tskfun = requests.get(third_party_api_url_tskfun, headers=header)
#     task_function_objs = json.loads(response_tskfun.content)

#     # task_function_objs=TaskFunctionMaster.objects.all()

#     #TaskPriorityMaster API URL
#     third_party_api_url_tskpriority = getAPIURL()+'task-priority-master/'
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response_tskpriority = requests.get(third_party_api_url_tskpriority, headers=header)
#     task_priority_objs = json.loads(response_tskpriority.content)

#     # task_priority_objs=TaskPriorityMaster.objects.all()
#     # sub_task_type_objs=SubTasktypeMaster.objects.all()

#     #TaskApprovalstatusMaster api url
#     third_party_api_url = getAPIURL()+'task-approval-status-master/'
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response = requests.get(third_party_api_url, headers=header)
#     print("response edit task Approval--------------------------",response.content)
#     task_approval_master_objs = json.loads(response.content)

#     # task_approval_master_objs=TaskApprovalstatusMaster.objects.all()    

    
#     api_url=getAPIURL()+"edit_task/"       
#     api_para={  
#         'id':task_id} 
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
#     api=response.json()
#     print("api",api)


#     request_data = {x:request.POST.get(x) for x in request.POST.keys()}
#     print("postrequest_data",request_data)
#     if request.method == 'POST':
#         print("post edit")
#         task_id=request_data['task_id']
#         print("task_id",task_id)
#         department=request_data['department']
#         originator=request_data['originator']
#         #print("Department",department,"Orginator",originator)
#         task_function=request_data['task_function_label']
#         registration_date=request_data['reg_date']
#         print("registration_date",(registration_date))
#         registration_date= datetime.strptime(registration_date, '%m/%d/%Y')
#         print("registration_date",(registration_date))
     
#         task_type=request_data['task_type_label']
#         task_aid=TaskTypeMaster.objects.get(task_type_label=task_type).task_type_aid
#         sub_task_type=request_data['sub_task_type_label']
#         priority=request_data['task_priority_label']
#         end_date=request_data['end_date']
#         end_date= datetime.strptime(end_date, '%m/%d/%Y')

#         completion_status=request_data['completion_status']
#         approval_status=request_data['approval_status']
#         task_summery=request.POST.get('task_summery', '')
#         task_name=request_data['txt_Task_Name']
#         print("task_summery",task_summery)
#         task_req=request_data['task_req']
#         print("task_req",task_req)

#         api_url=getAPIURL()+"edit_task/"       
#         data_to_save={
#             "task_id": task_id,
#             "department": department,
#             "originator": originator,
#             "task_function": task_function,
#             "registration_date": registration_date.strftime('%Y-%m-%d'),
#             "task_type": task_aid,
#             "sub_task_type": sub_task_type,
#             "priority": priority,
#             "end_date": end_date.strftime('%Y-%m-%d'),
#             "completion_status": completion_status,
#             "approval_status": approval_status,
#             "task_summery": task_summery,
#             "task_req": task_req,
#             "task_name":task_name
#         }
#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }
#         response = requests.put(api_url, data= json.dumps(data_to_save),headers=header)
       
#         print("response",response)

        
#         return redirect('getTasks')
#     context={
#         'task_id': api['task_id'],
#         'department': api['department'],
#         'originator': api['originator'],
#         'task_function_label': api['task_function_label'],
#         'reg_date': api['reg_date'],
#         'task_name': api['task_name'],
#         'task_type_label': api['task_type_label'],
#         'sub_task_type_label': api['sub_task_type_label'],
#         'task_priority_label': api['task_priority_label'],
#         'end_date': api['end_date'],
#         'completion_status': api['completion_status'],
#         'task_summery': api['task_summery'],
#         'task_function': api['task_function'],
#         'task_req': api['task_req'],
#         'approval_status': api['approval_status'],
#         'approval_status_label': api['approval_status_label'],
#         'task_function_objs': task_function_objs,
#         'priority': api['priority'],
#         'sub_task_type': api['sub_task_type'],
#         'sub_task_type_objs': api['sub_task_type_objs'],
#         'task_priority_objs': task_priority_objs,
#         'task_approval_master_objs': task_approval_master_objs,
#         'originator_name': api['originator_name'],
#         'approver_user_obj': api['approver_user_obj'],
#         'assignee_user_obj': api['assignee_user_obj']
#     }

#     return render(request,'edit_task.html',context)

# def edit_issue(request,issue_id):
#     print("issue_id",issue_id)

#     issue_function_objs=IssueFunctionMaster.objects.all()
#     issue_priority_objs=IssuePriorityMaster.objects.all()
#     issue_approval_master_objs=IssueApprovalstatusMaster.objects.all()    

#     issue_obj=IssueRegistration.objects.get(issue_id=issue_id)
#     department=issue_obj.department
#     originator=issue_obj.originator
#     added_by=issue_obj.addedby
#     issue_function=issue_obj.issue_function
#     issue_function_obj=IssueFunctionMaster.objects.get(issue_function_aid=issue_function)
#     issue_function_label=issue_function_obj.issue_function_label
#     print("issue_function_label",issue_function_label)
#     reg_date=issue_obj.registration_date
#     reg_date=reg_date.strftime('%m-%d-%Y')
#     issue_type=issue_obj.issue_type
#     issue_type_obj=Issue_Type_Master.objects.get(issue_type_aid=issue_type)
#     issue_type_label=issue_type_obj.issue_type_label
#     issue_type_aid=issue_type_obj.issue_type_aid
#     sub_issue_type_objs=Sub_Issue_Type_Master.objects.filter(issue_type_aid=issue_type_aid)
    
#     sub_issue_type=issue_obj.sub_issue_type
#     sub_issue_type_obj=Sub_Issue_Type_Master.objects.get(sub_issue_type_aid=sub_issue_type)
#     sub_issue_type_label=sub_issue_type_obj.sub_issue_type_label

#     priority=issue_obj.priority
#     print('priority',priority)
#     priority_obj=IssuePriorityMaster.objects.get(issue_priority_aid=priority)
#     issue_priority_label=priority_obj.issue_priority_label
#     print("issue_priority_label",issue_priority_label)
#     end_date=issue_obj.end_date.strftime('%m-%d-%Y')
#     completion_status=issue_obj.completion_status
#     approval_status=issue_obj.approval_status
#     approval_status_label=IssueApprovalstatusMaster.objects.get(issue_approvalstatus_aid=approval_status).issue_approvalstatus_label
#     issue_summery_obj=IssueSummery.objects.get(issue=issue_id)
#     issue_summery=issue_summery_obj.issue_summery
#     print("issue_summery",issue_summery)
#     issue_req=issue_summery_obj.issue_requirement

    

#     request_data = {x:request.POST.get(x) for x in request.POST.keys()}
#     print("postrequest_data",request_data)
#     if request.method == 'POST':
#         print("post edit")
#         issue_id=request_data['issue_id']
#         print("issue_id",issue_id)
#         department=request_data['department']
#         originator=request_data['originator']
#         issue_function=request_data['issue_function_label']
#         print("issue_function",issue_function)
#         registration_date=request_data['reg_date']
#         print("registration_date",(registration_date))
#         registration_date= datetime.strptime(registration_date, '%m/%d/%Y')

#         issue_type=request_data['issue_type_label']
#         issue_aid=Issue_Type_Master.objects.get(issue_type_label=issue_type).issue_type_aid
#         sub_issue_type=request_data['sub_issue_type_label']
#         print("sub_issue_type",sub_issue_type)
#         priority=request_data['issue_priority_label']
#         end_date=request_data['end_date']
#         end_date= datetime.strptime(end_date, '%m/%d/%Y')

#         completion_status=request_data['completion_status']
#         approval_status=request_data['approval_status']

#         issue_summery=request_data['issue_summery']
#         print("issue_summery",issue_summery)
#         issue_req=request_data['issue_req']
#         print("issue_req",issue_req)
#         issue_update_obj=IssueRegistration.objects.get(issue_id=issue_id)
#         issue_update_obj.department=department
#         issue_update_obj.originator=originator
#         issue_update_obj.issue_function=issue_function
#         issue_update_obj.registration_date=registration_date
#         issue_update_obj.issue_type=issue_aid
#         issue_update_obj.sub_issue_type=sub_issue_type 
#         issue_update_obj.priority=priority
#         issue_update_obj.end_date=end_date
#         issue_update_obj.completion_status=completion_status
#         issue_update_obj.approval_status=approval_status
#         issue_update_obj.save()
#         issue_summ_update=IssueSummery.objects.get(issue=issue_id)
#         issue_summ_update.issue_summery=issue_summery
#         issue_summ_update.issue_requirement=issue_req
#         issue_summ_update.save()
#         return redirect('show_issue')
#     context={'issue_id':issue_id,'department':department,'originator':originator,'issue_function_label':issue_function_label,'reg_date':reg_date,
#                          'issue_type_label':issue_type_label,'sub_issue_type_label':sub_issue_type_label,'issue_priority_label':issue_priority_label,
#                          'end_date':end_date ,'completion_status':completion_status,'issue_summery':issue_summery,'priority':priority,
#                          'issue_req':issue_req,'approval_status':approval_status,'issue_function_objs':issue_function_objs,'approval_status_label':approval_status_label,
#                          'sub_issue_type_objs':sub_issue_type_objs,'issue_priority_objs':issue_priority_objs,'issue_approval_master_objs':issue_approval_master_objs}
#     return render(request,'edit_issue.html',context)

# def edit_issue(request,issue_id):
#     print("issue_id",issue_id)

#     third_party_api_url_issue_fun = getAPIURL()+'issue-function-master/'
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response_issuefun = requests.get(third_party_api_url_issue_fun, headers=header)
#     issue_function_objs = json.loads(response_issuefun.content)

#     # issue_function_objs=IssueFunctionMaster.objects.all()

#     third_party_api_url_issue_pri = getAPIURL()+'issue-priority-master/'
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response_issue_prio = requests.get(third_party_api_url_issue_pri, headers=header)
#     issue_priority_objs = json.loads(response_issue_prio.content)

#     # issue_priority_objs=IssuePriorityMaster.objects.all()

#     third_party_api_url_issue_appro = getAPIURL()+'issue-approval-status-master/'
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response_issue_appro = requests.get(third_party_api_url_issue_appro, headers=header)
#     issue_approval_master_objs = json.loads(response_issue_appro.content)

#     # issue_approval_master_objs=IssueApprovalstatusMaster.objects.all()    

#     api_url=getAPIURL()+"edit_issue/"       
#     api_para={  
#         'id':issue_id} 
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
#     api=response.json()
#     print("api",api)

#     request_data = {x:request.POST.get(x) for x in request.POST.keys()}
#     print("postrequest_data",request_data)
#     if request.method == 'POST':
#         print("post edit")
#         issue_id=request_data['issue_id']
#         print("issue_id",issue_id)
#         department=request_data['department']
#         originator=request_data['originator']
#         print("originator",originator)
#         issue_function=request_data['issue_function_label']
#         print("issue_function",issue_function)
#         registration_date=request_data['reg_date']
#         print("registration_date",(registration_date))
#         registration_date= datetime.strptime(registration_date, '%m/%d/%Y')
        
#         issue_type=request_data['issue_type_label']
#         issue_aid=Issue_Type_Master.objects.get(issue_type_label=issue_type).issue_type_aid
#         sub_issue_type=request_data['sub_issue_type_label']
#         print("sub_issue_type",sub_issue_type)
#         priority=request_data['issue_priority_label']
#         end_date=request_data['end_date']
#         end_date= datetime.strptime(end_date, '%m/%d/%Y')

        
#         completion_status=request_data['completion_status']
#         approval_status=request_data['approval_status']

#         issue_summery=request_data['issue_summery']
#         print("issue_summery",issue_summery)
#         issue_req=request_data['issue_req']
#         print("issue_req",issue_req)

#         api_url=getAPIURL()+"edit_issue/"       
        
#         data_to_save = {
#             "issue_id": issue_id,
#             "department": department,
#             "originator": originator,
#             "issue_function": issue_function,
#             "registration_date": registration_date.strftime('%Y-%m-%d'),
#             "issue_aid": issue_aid,
#             "sub_issue_type": sub_issue_type,
#             "priority": priority,
#             "end_date": end_date.strftime('%Y-%m-%d'),
#             "completion_status": completion_status,
#             "approval_status": approval_status,
#             "issue_summery":issue_summery,
#             "issue_req":issue_req,

#             # "issue_major_ver": issue_major_ver,
#             # "issue_minor_ver": issue_minor_ver,
#             # "addedby": added_by,
#             # "link_id": link_id,

#             # "issue_relevant_personnel_check":issue_relevant_personnel_check,
#             # "issue_assigned_to":request.POST.getlist('issue_assigned_to'),
#             # "issue_approved_by":request.POST.getlist('issue_approved_by'),
#             # "issue_originator_relevant":request_data['issue_originator_relevant'],
#             # "issue_summery_check":issue_summery_check,
#             # "issue_summery_comments":request_data['issue_summery_comments'],
#             # "issue_requirements_comments":request_data['issue_requirements_comments'],
#             # "issue_assignee_comments":request_data['issue_assignee_comments'],
#             # "issue_approver_comments":request_data['issue_approver_comments'],
#             # "added_by":added_by
#         }

#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }
#         response = requests.put(api_url, data= json.dumps(data_to_save),headers=header)
       
#         print("response",response)

#         return redirect('getIssues')

#     context = {
#         'issue_id': api['issue_id'],
#         'department': api['department'],
#         'originator': api['originator'],
#         'issue_function_label': api['issue_function_label'],
#         'issue_function': api['issue_function'],
#         'reg_date': api['reg_date'],
#         'issue_type_label': api['issue_type_label'],
#         'sub_issue_type_label': api['sub_issue_type_label'],
#         'sub_issue_type': api['sub_issue_type'],
#         'issue_priority_label': api['issue_priority_label'],
#         'end_date': api['end_date'],
#         'completion_status': api['completion_status'],
#         'issue_summery': api['issue_summery'],
#         'priority': api['priority'],
#         'assignee_user_obj': api['assignee_user_obj'],
#         'approver_user_obj': api['approver_user_obj'],
#         'issue_req': api['issue_req'],
#         'approval_status': api['approval_status'],
#         'issue_function_objs': issue_function_objs,
#         'approval_status_label': api['approval_status_label'],
#         'sub_issue_type_objs': api['sub_issue_type_objs'],
#         'issue_priority_objs': issue_priority_objs,
#         'issue_approval_master_objs': issue_approval_master_objs,
#     }

#     return render(request,'edit_issue.html',context)


def show_issue(request):
    print( request.session['uid'])
    issue_obj=IssueRegistration.objects.filter(addedby=request.session['uid'])

    all_data_lst=list()
    dict_data=dict()
    for i in issue_obj:
        print("issue_id",i.issue_id)
        dict_data['issue_id']=i.issue_id
        dict_data['completion_status']=i.completion_status
        dict_data['reg_date']=i.registration_date
        issue_type_data=Issue_Type_Master.objects.get(issue_type_aid=i.issue_type).issue_type_label
        dict_data['issue_type']=issue_type_data
        print("issue_type_data",issue_type_data)
        sub_issue_type_data=Sub_Issue_Type_Master.objects.get(sub_issue_type_aid=i.sub_issue_type).sub_issue_type_label
        dict_data['sub_issue_type']=sub_issue_type_data
        priority_data=TaskPriorityMaster.objects.get(task_priority_aid=i.priority).task_priority_label
        dict_data['priority']=priority_data
        print("approval",i.approval_status)
        approval_data=TaskApprovalstatusMaster.objects.get(task_approvalstatus_aid=i.approval_status).task_approvalstatus_label
        print("approval_data"),approval_data
        dict_data['approval_status']=approval_data
        print("dict_data",dict_data)
        all_data_lst.append(dict_data.copy())

    print("all_data_lst",all_data_lst)
    context={'all_data_lst':all_data_lst}

    return render(request,'show_issue.html',context)


def getSub_Sections(request):
    print("-------------request",request.GET['secid[]'])
    print("-------------request list",request.GET.getlist('secid[]') )
    
    # request_data = dict(zip(request.GET.keys(), request.GET.values()))
    # request_data = {x:request.GET.get(x) for x in request.GET.values()}
    # print('request_data',request_data)
    lst = []
    selid = request.GET.getlist('secid[]')
    print("selid list",selid)
    for i in selid:
        icq_sub1 = models.IcqSubSections.objects.filter(section_aid = i)
        print("icq_subsection",icq_sub1)
        for obj in icq_sub1:
            dict = {
                '0':{
                    'Sub_Section_Label':obj.sub_section_label,
                    'Sub_Section_AID':obj.sub_section_aid
                }
            }
            lst.append(dict)
    print(lst)
    return JsonResponse({"list":lst})

def getSub_Sub_Sections(request):
    print("-------------request",request.GET['secid[]'])
    lst = []
    selid = request.GET.getlist('secid[]')
    print("selidlist",selid)
    for i in selid:
        icq_sub1 = models.IcqSubSubSections.objects.filter(sub_section_aid = i)
        print("icq_sub_subsection",icq_sub1)
        for obj in icq_sub1:
            dict = {
                '0':{
                    'Sub_Sub_Section_Label':obj.sub_sub_section_label,
                    'Sub_Sub_Section_AID':obj.sub_sub_section_aid
                }
            }
            lst.append(dict)
    print(lst)
    return JsonResponse({"list":lst})


def getSub_Sub_Sub_Sections(request):
    print("-------------request",request.GET['secid[]'])
    lst = []
    selid = request.GET.getlist('secid[]')
    print("selidlist",selid)
    for i in selid:
        icq_sub1 = models.IcqSubSubSubSections.objects.filter(sub_sub_section_aid = i)
        print("icq_sub_subsection",icq_sub1)
        for obj in icq_sub1:
            dict = {
                '0':{
                    'Sub_Sub_Sub_Section_Label':obj.sub_sub_sub_section_label,
                    'Sub_Sub_Sub_Section_AID':obj.sub_sub_sub_section_aid
                }
            }
            lst.append(dict)
    print(lst)
    return JsonResponse({"list":lst}) 



#Changes in function
def allocate_icq(request): 
    try:
        if request.method=="POST":
            section=request.POST.get('section','False')
            sub_section=request.POST.get('sub_section','False')
            sub_sub_section=request.POST.get('sub_sub_section','False')
            sub_sub_sub_section=request.POST.get('sub_sub_sub_section','False')

            print(section,sub_section,sub_sub_section,sub_sub_sub_section)

            if sub_section == '' and sub_sub_section == '' and sub_sub_sub_section == '':
                print("session selected")
                question_obj_filter=IcqQuestionMaster.objects.filter(section_aid=section)
            elif sub_sub_section == '' and sub_sub_sub_section == '':
                print("sub section selected")
                question_obj_filter=IcqQuestionMaster.objects.filter(Q(sub_section_aid=sub_section) | Q(section_aid=section))
            elif sub_sub_sub_section == '':
                print("sub sub section selected")
                question_obj_filter=IcqQuestionMaster.objects.filter(Q(sub_sub_section_aid=sub_sub_section) | Q(sub_section_aid=sub_section) | Q(section_aid=section))  
    
            else:
                print("else")
                question_obj_filter=IcqQuestionMaster.objects.filter(section_aid=section,sub_section_aid=sub_section,
                                            sub_sub_section_aid=sub_sub_section,sub_sub_sub_section_aid=sub_sub_sub_section)
            
            list_data=[]
            dict_data=dict()
            for i in question_obj_filter:
                print("question",i.question_label)
                print('question id',i.question_aid)
                dict_data[i.question_aid]=i.question_label
                # dict_data['question']=i.question_label
                # dict_data['id']=i.question_aid
                print("dict_data",dict_data)
                # list_data.append(dict_data)
            #print('list data',list_data)    
            return JsonResponse(dict_data,safe=False)
	#Jayesh Code 
        userobj = Users.objects.all()
        review_name = IcqQuestionRatingAllocation.objects.values('review_id','review_name').distinct()
        print("review name",review_name)
        return render(request,'allocate_icq.html',{'sections':objmaster.getSections(),'user':userobj,'review':objmaster.getICQIds()})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 


def save_allocation(request):
    request_data = {x:request.GET.get(x) for x in request.GET.keys()}
    section_aid = request.GET.getlist('section_aid[]')
    users = request.GET.getlist('users[]')
    api_url=getAPIURL()+"save_allocation/"       
    data_to_save={'section_aid':section_aid,
        'users':users,
        'rv_id': request_data['rv_id'],
        'rv_name':request_data['rv_name'],} 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
        
    api_data=response.json()
    return JsonResponse({"isvalid":api_data['isvalid']}) 
    # request_data = {x:request.GET.get(x) for x in request.GET.keys()}
    # section_aid = request.GET.getlist('section_aid[]')
    # users = request.GET.getlist('users[]')
    # # end_date = request_data['end_date'][6:] + "-" + request_data['end_date'][3:5] + "-" + request_data['end_date'][:2]
    # if request_data['rv_id'] == "addnew":
    #     last_rvid_obj = IcqQuestionRatingAllocation.objects.aggregate(Max('review_id'))
    #     last_rvid = last_rvid_obj['review_id__max']
    #     splt_rvid = last_rvid.split('_')
    #     latest_rvid = int(splt_rvid[1]).__add__(1) #used magic method django
    #     for user, section_id in [(x,y) for x in users for y in section_aid]:
    #         allocate_obj = IcqQuestionRatingAllocation(review_id ="Rv_"+str(latest_rvid),review_name = request_data['rv_name'],section_aid = section_id,allocated_to = user,end_date = None)
    #         allocate_obj.save()
    #     return JsonResponse({"isvalid":"true"}) 
    # else:
    #     for user, section_id in [(x,y) for x in users for y in section_aid]:
    #         allocate_obj = IcqQuestionRatingAllocation(review_id =request_data['rv_id'],review_name = request_data['rv_name'],section_aid = section_id,allocated_to = user,end_date = None)
    #         allocate_obj.save()
    #     return JsonResponse({"isvalid":"true"}) 


def get_parent_Sections(request):
    print("-------------request new",request.GET['secid[]'])
    lst = []
    selid = request.GET.getlist('secid[]')
    print("selidlist",selid)
    for i in selid:
        sub_sub_sub_id = models.IcqSubSubSubSections.objects.get(sub_sub_sub_section_aid = i)
        print("sub_sub_sub_id------------------",sub_sub_sub_id.sub_sub_section_aid)
        sub_sub_id = models.IcqSubSubSections.objects.get(sub_sub_section_aid = sub_sub_sub_id.sub_sub_section_aid.sub_sub_section_aid)
        print("sub_sub_id",sub_sub_id.sub_sub_section_label)
        sub_id = models.IcqSubSections.objects.get(sub_section_aid = sub_sub_id.sub_section_aid.sub_section_aid)
        print("sub_id",sub_id.sub_section_label)
        section_id = models.IcqSections.objects.get(section_aid = sub_id.section_aid.section_aid)
        print("section_id",section_id.section_label)
        dict = {
                '0':{
                    'Sub_sub_sub_parent_id':sub_sub_sub_id.sub_sub_section_aid.sub_sub_section_aid,
                    'Sub_Sub_sub_parent_label':sub_sub_id.sub_sub_section_label,
                    'Sub_Sub_parent_id':sub_sub_id.sub_section_aid.sub_section_aid,
                    'Sub_Sub_parent_label':sub_id.sub_section_label,
                    'Sub_parent_id':sub_id.section_aid.section_aid,
                    'Sub_parent_label':section_id.section_label
                }
            }
        lst.append(dict)
    print(lst)
    return JsonResponse({"list":lst})


def show_issue_priority(request):
    try: 
        third_party_api_url = getAPIURL()+'issue-priority-master/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("task function response",response.content)

        return render(request, 'show_issue_priority.html',{'actPage' :'RMSE - Issue Priority','users':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())

def add_issue_priority(request):
    try:   
        return render(request, 'add_issue_priority.html',{'actPage':'RMSE - Add Issue Priority'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def save_issue_priority(request):
    print()
    try:
        print("---------save_issue_priority",request.POST)
        
        id=request.POST.get('update_id','False')
        
        issue_priority_label = request.POST.get('label','False')
        issue_priority_description = request.POST.get('desc','False')
        print('update_id',id)
        print("issue_priority_label,issue_priority_description",issue_priority_label,issue_priority_description)

        if id != 'undefined':
            print("update_issue_priority")
            
            third_party_api_url = getAPIURL()+'issue-priority-master/'

            data_to_update = {
                'issue_priority_label':issue_priority_label,
                'issue_priority_description':issue_priority_description,
                'id':id
            }
            header = {
            "Content-Type":"application/json"
            }
            response = requests.put(third_party_api_url, data= json.dumps(data_to_update),headers=header)
            
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))

        else:
            print("save_issue_priority")
            
            third_party_api_url = getAPIURL()+'issue-priority-master/'

            data_to_save = {
                'issue_priority_label':issue_priority_label,
                'issue_priority_description':issue_priority_description
            }
            header = {
            "Content-Type":"application/json"
            }
            response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
            
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
        
    except requests.exceptions.RequestException as e:
            return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
  
    
def show_issue_approval_status(request):
    try: 
        third_party_api_url = getAPIURL()+'issue-approval-status-master/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("task function response",response.content)

        return render(request, 'show_issue_approval_status.html',{'actPage' :'RMSE - Issue Approval Status','users':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())


def add_issue_approval(request):
    try:   
        return render(request, 'add_issue_approval.html',{'actPage':'RMSE - Add Issue Approval Status'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def save_issue_approval_status(request):
    print()
    try:
        print("---------save_issue_approval_status",request.POST)
       
        id=request.POST.get('update_id','False')

        issue_approval_status_label = request.POST.get('label','False') 
        issue_approval_status_description = request.POST.get('desc','False')
        print("update_id",id)
        print("issue_approval_status_label,issue_approval_status_description",issue_approval_status_label,issue_approval_status_description)

        if id != 'undefined':
            print("update issue_approval_status")
           
            third_party_api_url = getAPIURL()+'issue-approval-status-master/'

            data_to_update = {
                'issue_approvalstatus_label':issue_approval_status_label,
                'issue_approvalstatus_description':issue_approval_status_description,
                'id':id    
            }
            header = {
            "Content-Type":"application/json"
            }
            response = requests.put(third_party_api_url, data= json.dumps(data_to_update),headers=header)

            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))

        else:    
            print("Add issue_approval_status")

            third_party_api_url = getAPIURL()+'issue-approval-status-master/'

            data_to_save = {
                'issue_approvalstatus_label':issue_approval_status_label,
                'issue_approvalstatus_description':issue_approval_status_description
            }
            header = {
            "Content-Type":"application/json"
            }
            response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
    
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
            
    except requests.exceptions.RequestException as e:
            return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    


def show_issue_type(request):
    try: 
        third_party_api_url = getAPIURL()+'issue-type-master/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("issue function response",response.content)

        return render(request, 'show_issue_type.html',{'actPage' :'RMSE - Issue Function','users':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())
  
def add_issue_type(request):
    try:   
        return render(request, 'add_issue_type.html',{'actPage':'RMSE - Add Issue Type'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def save_issue_type(request):
    try:
        print("---------save_issue_type",request.POST)
        
        id=request.POST.get('update_id','False')
        issue_type_label = request.POST.get('label','False')
        issue_type_description = request.POST.get('desc','False')
        print('update_id',id)
        print("issue_type_label,issue_type_description",issue_type_label,issue_type_description)

        if id != 'undefined':

            print("update issue type")
            third_party_api_url = getAPIURL()+'issue-type-master/'
            
            data_to_update = {
                'issue_type_label':issue_type_label,
                'issue_type_description':issue_type_description,
                'id':id
            }
            header = {
            "Content-Type":"application/json"
            }
            response = requests.put(third_party_api_url, data= json.dumps(data_to_update),headers=header)
            
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
        else:
            print("Add issue type")

            third_party_api_url = getAPIURL()+'issue-type-master/'

            data_to_save = {
                'issue_type_label':issue_type_label,
                'issue_type_description':issue_type_description
            }
            header = {
            "Content-Type":"application/json"
            }
            response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
            
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
        
    except requests.exceptions.RequestException as e:
                return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
    

def show_sub_issue(request):
    try: 
        third_party_api_url = getAPIURL()+'sub-issue-type-master/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("issue function response",response.content)

        return render(request, 'show_sub_issue.html',{'actPage' :'RMSE - Sub Issue Type','users':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())


def add_sub_issue_type(request):
    try: 
        typeobj = Issue_Type_Master.objects.all()
        return render(request, 'add_sub_issue_type.html',{'actPage':'RMSE - Add Sub Issue Type','issuetypes':typeobj,'type':'add'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def save_sub_issue_type(request):
    print("save_sub_issue_type")
    try:
        print("---------save_sub_issue_type",request.POST)
    
        id=request.POST.get('update_id','False')
        sub_issue_type_label = request.POST.get('label','False') 
        sub_issue_type_description = request.POST.get('desc','False')
        issue_type = request.POST.get('issuetype','False')
        print("update_id",id)
        print("issuetype",issue_type)

        print("sub_issue_type_label,sub_issue_type_description,issue_type",sub_issue_type_label,sub_issue_type_description,issue_type)
        if id != 'undefined':
            print("update sub_issue_type ")
       
            third_party_api_url = getAPIURL()+'sub-issue-type-master/'
            
            data_to_update = {
                'sub_issue_type_label':sub_issue_type_label,
                'sub_issue_type_description':sub_issue_type_description,
                'issue_type_aid':issue_type,
                'sub_issue_type_aid':id
            }
            header = {
            "Content-Type":"application/json"
            }
            response = requests.put(third_party_api_url, data= json.dumps(data_to_update),headers=header)
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
        else:
            print("Add sub_issue_type ")
            third_party_api_url = getAPIURL()+'sub-issue-type-master/'

            print("sub_issue_type_label,sub_issue_type_description,issue_type",sub_issue_type_label,sub_issue_type_description,issue_type)

            data_to_save = {
                'sub_issue_type_label':sub_issue_type_label,
                'sub_issue_type_description':sub_issue_type_description,
                'issue_type_aid':issue_type,
            }
            header = {
            "Content-Type":"application/json"
            }
            response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)

            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
        
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

def edit_issue_function(request,id):
    print("edit_issue_function",id)

    third_party_api_url = getAPIURL()+'issue-function-master/'+id
        
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(third_party_api_url,headers=header)
    print("response content",response.content,response.status_code)
    data=json.loads(response.content)
    print("data",data)
    print("label",data['data']['issue_function_label'])
    return render(request, 'add_new_issue.html',{'issue_function_label':data['data']['issue_function_label'],
                                                     'issue_function_desc':data['data']['issue_function_description'],'id':id})

def edit_issue_type(request,id):
    print("edit_issue_type",id)
    third_party_api_url = getAPIURL()+'issue-type-master/'+id
        
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(third_party_api_url,headers=header)
    print("response content",response.content,response.status_code)
    data=json.loads(response.content)
    print("data",data)
    print("label",data['data']['issue_type_label'])
    return render(request, 'add_issue_type.html',{'issue_type_label':data['data']['issue_type_label'],
                                                     'issue_type_description':data['data']['issue_type_description'],'id':id})

def edit_sub_issue_type(request,id):
    print("edit_sub_issue_type",id)
    third_party_api_url = getAPIURL()+'sub-issue-type-master/'+id
        
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(third_party_api_url,headers=header)
    print("response content",response.content,response.status_code)
    data=json.loads(response.content)
    print("data",data)
    print("label",data['data']['sub_issue_type_label'])
    print("issue_type",data['data']['issue_type_details'])

    return render(request, 'add_sub_issue_type.html',{'sub_issue_type_label':data['data']['sub_issue_type_label'],
                                                     'sub_issue_type_description':data['data']['sub_issue_type_description'],'id':id,'issue_type':data['data']['issue_type_details'],'type':'edit'})
          

def edit_issue_priority(request,id):
    print("edit_issue_priority",id)

    third_party_api_url = getAPIURL()+'issue-priority-master/'+id
        
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(third_party_api_url,headers=header)
    print("response content",response.content,response.status_code)
    data=json.loads(response.content)
    print("data",data)
    print("label",data['data']['issue_priority_label'])
    return render(request, 'add_issue_priority.html',{'issue_priority_label':data['data']['issue_priority_label'],
                                                     'issue_priority_description':data['data']['issue_priority_description'],'id':id})
         
def edit_issue_approval_status(request,id):
    print("edit_issue_approval_status",id)

    third_party_api_url = getAPIURL()+'issue-approval-status-master/'+id
        
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(third_party_api_url,headers=header)
    print("response content",response.content,response.status_code)
    data=json.loads(response.content)
    print("data",data)
    print("label",data['data']['issue_approvalstatus_label'])
    return render(request, 'add_issue_approval.html',{'issue_approval_status_label':data['data']['issue_approvalstatus_label'],
                                                     'issue_approval_status_description':data['data']['issue_approvalstatus_description'],'id':id})      

 

def edit_task_function(request,id):
    print("edit_task_function",id)
    try: 
        third_party_api_url = getAPIURL()+'task-function-master/'+id
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response edit task function--------------------------",response.content)
        task_function_data = json.loads(response.content)
        task_function_label = task_function_data['data']['task_function_label']
        task_function_description = task_function_data['data']['task_function_description']
        # task_function_obj=TaskFunctionMaster.objects.get(task_function_aid=id)
        # task_function_label=task_function_obj.task_function_label
        # task_function_description=task_function_obj.task_function_description
        return render(request, 'addtaskfun.html',{'task_function_label':task_function_label,
                                                     'task_function_description':task_function_description,'id':id})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())  


def edit_task_type(request,id):
    print("edit_task_type",id)
    try:
        third_party_api_url = getAPIURL()+'task-type-master/'+id
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response edit task function--------------------------",response.content)
        task_type_data = json.loads(response.content)
        task_type_label = task_type_data['data']['task_type_label']
        task_type_description = task_type_data['data']['task_type_description'] 
        # task_type_obj=TaskTypeMaster.objects.get(task_type_aid=id)
        # task_type_label=task_type_obj.task_type_label
        # task_type_description=task_type_obj.task_type_description
        return render(request, 'addtasktype.html',{'task_type_label':task_type_label,
                                                     'task_type_description':task_type_description,'id':id})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc()) 



def edit_sub_task_type(request,id):
    print("edit_sub_task_type",id)
    try: 
        third_party_api_url = getAPIURL()+'sub-task-type-master/'+id
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response edit task function--------------------------",response.content)
        task_sub_type_data = json.loads(response.content)
        sub_task_type_label = task_sub_type_data['data']['sub_task_type_label']
        sub_task_type_description = task_sub_type_data['data']['sub_task_type_description'] 
        task_type = task_sub_type_data['data']['task_type_details']
        # sub_task_type_obj=SubTasktypeMaster.objects.get(sub_task_type_aid=id)
        # task_type=sub_task_type_obj.task_type_aid
        # sub_task_type_label=sub_task_type_obj.sub_task_type_label
        # sub_task_type_description=sub_task_type_obj.sub_task_type_description
        return render(request, 'addsubtasktype.html',{'sub_task_type_label':sub_task_type_label,
                                                     'sub_task_type_description':sub_task_type_description,'id':id,'task_type':task_type,'type':'edit'})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc()) 

def edit_task_priority(request,id):
    print("edit_task_priority",id)
    try: 
        third_party_api_url = getAPIURL()+'task-priority-master/'+id
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response edit task Priority--------------------------",response.content)
        task_priority_data = json.loads(response.content)
        task_priority_label = task_priority_data['data']['task_priority_label']
        task_priority_description = task_priority_data['data']['task_priority_description']
        # task_priority_obj=TaskPriorityMaster.objects.get(task_priority_aid=id)
        # task_priority_label=task_priority_obj.task_priority_label
        # task_priority_description=task_priority_obj.task_priority_description
        return render(request, 'addtaskpriority.html',{'task_priority_label':task_priority_label,
                                                     'task_priority_description':task_priority_description,'id':id})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())

 

def edit_task_approval(request,id):
    print("edit_task_approval",id)
    try:
        third_party_api_url = getAPIURL()+'task-approval-status-master/'+id
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response edit task Approval--------------------------",response.content)
        task_approval_data = json.loads(response.content)
        task_approval_status_label = task_approval_data['data']['task_approvalstatus_label']
        task_approval_status_description = task_approval_data['data']['task_approvalstatus_description'] 
        # task_approval_status_obj=TaskApprovalstatusMaster.objects.get(task_approvalstatus_aid=id)
        # task_approval_status_label=task_approval_status_obj.task_approvalstatus_label
        # task_approval_status_description=task_approval_status_obj.task_approvalstatus_description
        return render(request, 'addtaskapprovalstatus.html',{'task_approval_status_label':task_approval_status_label,
                                                     'task_approval_status_description':task_approval_status_description,'id':id})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())     

# def checkUserRole(request):
#     try:
#         mdl_id = request.GET.get('mdl_id','none') 
#         return JsonResponse({'role': objrmse.checkUserRole(request.session['uid'],mdl_id)})
#     except Exception as e:
#         print('adduser is ',e) 
#         print('adduser traceback is ', traceback.print_exc())   

# def checkUserRole_Issue(request):
#     try:
#         issue_id = request.GET.get('mdl_id','none') 
      
#         api_url=getAPIURL()+"checkUserRole_Issue/"       
#         data_to_save={'uid':request.session['uid'] ,
#                       'mdl_id':issue_id} 
#         header = {
#         "Content-Type":"application/json",
# 	    'Authorization': 'Token '+request.session['accessToken']
#         }
#         response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)         
#         api_data=response.json() 
#         context={'role':api_data['role']}  
#         return JsonResponse(context)
#     except Exception as e:
#         print('adduser is ',e) 
#         print('adduser traceback is ', traceback.print_exc())