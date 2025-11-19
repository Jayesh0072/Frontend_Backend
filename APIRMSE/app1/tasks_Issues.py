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
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework import generics, permissions, status,serializers
from .serializers import *
from rest_framework.permissions import IsAuthenticated
BASE_DIR = Path(__file__).resolve().parent.parent
# Create your views here.
user_name = "user1"
file_path = os.path.join(BASE_DIR, 'static/Data/')
savefile_name = file_path +  "Modelinfo.csv" 
# Create your views here.
from app1.models import *  
# DEFINE THE DATABASE CREDENTIALS
user = 'sa'
password = 'sqlAdm_18'
host = 'DESKTOP-NH98228\HCSPL18'
port = 1433
database = 'RMSE'
from .RegModel.registermodel import RegisterModel as Register 

from .Adm_Utils.Masters import MasterTbls
from .DAL.dboperations import dbops
from .models import Users
from .UserInfo.user import UserInfo
from .Validation.validation import Validation
from .RMSE.RMSE import RMSEModel
objreg=Register()  
objmaster=MasterTbls()
objvalidation=Validation()
objdbops=dbops()
objrmse=RMSEModel() 

def error_saving(request,data):
    print("data print",data)
    file = open('logs.txt', 'w')
    file.write(str(data))
    file.close() 

def task_registration(request):
    print("task_registration")
    #Username we are taking is unique
    user_obj=Users.objects.get(u_name=request.session['username'])
    print("UAID",user_obj.u_aid)
    added_by=user_obj.u_aid
    today_date=datetime.now()
    originator_name=user_obj.u_fname  +" " + user_obj.u_lname
    print("originator_name",originator_name)
    print("Dept_name",user_obj.dept_aid)

    department_obj=Department.objects.get(dept_aid=user_obj.dept_aid)
    print("dept name",department_obj.dept_label)

    user_category_obj=UserCategory.objects.all()
    task_function_obj=TaskFunctionMaster.objects.all()
    task_priority_obj=TaskPriorityMaster.objects.all()
    task_type_obj=TaskTypeMaster.objects.all()
    task_approval_master=TaskApprovalstatusMaster.objects.all()    
    users_obj=Users.objects.all()
    mdl_overview_obj=ModelOverview.objects.all()

    assigned_to=[]#[]
    approved_by=[]
    task_assignee_thread_lst=[]
    task_approver_thread_lst=[]
    originatorid=added_by
    task_Major_Ver="1"
    task_Minor_Ver="0"
    # print("task_Id",task_Id) 
    # print("task_max",task_max)

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
    
        task_registration_obj=TaskRegistration(task_id=task_id,department=department,originator=originator,task_function=task_function,
                                               registration_date=registration_date,task_type=task_type,sub_task_type=sub_task_type,
                                               priority=priority,end_date=end_date,completion_status=completion_status,
                                               approval_status=approval_status,task_major_version=task_Major_Ver,
                                               task_minor_version=task_Minor_Ver,addedby=added_by,adddate=today_date,
                                               link_id=link_id,task_name=task_name
                                               )         
        
        task_registration_obj.save()
        if relevant_personnel == 'True':
            originator_relevant=request_data['originator_relevant']
            assigned_to=request.POST.getlist('assigned_to')
            approved_by=request.POST.getlist('approved_by')
            print('assigned_to',assigned_to)
            print('approved_by',approved_by)
            print('Relevant Personnel',relevant_personnel,originator_relevant,assigned_to,approved_by)
            if originator_relevant:
                relevant_personnel_obj=Task_Relevant_Personnel(u_type="Originator",u_id=user_obj.u_aid,
                                                     task=task_registration_obj,addedby=added_by,adddate=today_date)
                relevant_personnel_obj.save()

            for i in assigned_to:
                print('assigned to',i)
            
                relevant_personnel_obj=Task_Relevant_Personnel(u_type="Assignee",u_id=i,
                                                     task=task_registration_obj,addedby=added_by,adddate=today_date)
                relevant_personnel_obj.save()
                #notification code
                notification_trigger="New task registered - "+task_id
                insert_data_notification(added_by,i,"Task",notification_trigger,1)
                
                print(added_by,i)
                thread_id=thread_creation(added_by,i)
                task_assignee_thread_lst.append({"from": str(added_by), "to": str(i),"thread_id":str(thread_id)})
            for j in approved_by:
                print('approved_by',j)       

                relevant_personnel_obj=Task_Relevant_Personnel(u_type="Approver",u_id=j,
                                                     task=task_registration_obj,addedby=added_by,adddate=today_date)
                relevant_personnel_obj.save()
                #notification code
                notification_trigger="New task registered - "+task_id
                insert_data_notification(added_by,j,"Task",notification_trigger,1)
                print("notificatio approver saved")
                thread_id=thread_creation(added_by,j)
                task_approver_thread_lst.append({"from": str(added_by), "to": str(j),"thread_id":str(thread_id)})
        if task_summery_check == 'True':
            task_summery=request_data['task_summery']
            task_requirement=request_data['task_requirement']
            assignee_comments=request_data['assignee_comments']
            # approval=request_data['approval']
            approver_comments=request_data['approver_comments']

            print("task_summery",task_summery)
            
            
            task_summery_obj=TaskSummery(task_summery=task_summery,task_requirement=task_requirement,assignee_comments=assignee_comments,
                                                     approver_comments=approver_comments,
                                                     task_registration=task_registration_obj,addedby=added_by,adddate=today_date)
            task_summery_obj.save()
        # print('saved') 
        # return redirect('task_registration?task_id='+task_id)

    print("assigned_to before context",assigned_to)
    context={'task_function_obj':task_function_obj,'task_priority_obj':task_priority_obj,'task_type_obj':task_type_obj,
             'task_approval_master':task_approval_master,'originator_name':originator_name,'user_category_obj':user_category_obj,
             'department_obj':department_obj,'users_obj':users_obj,'mdl_overview_obj':mdl_overview_obj,'assigned_to_arr':json.dumps(assigned_to),
             'approved_by':json.dumps(approved_by),'originatorid':originatorid,'task_approver_thread_lst':json.dumps(task_approver_thread_lst),'task_assignee_thread_lst':json.dumps(task_assignee_thread_lst)}   
    return render(request,'task_registration.html',context)  

def get_sub_task_type(request): 
    task_type_aid=request.GET.get('task_type') 
    
    sub_task_data={}
    sub_task_type_obj=SubTasktypeMaster.objects.filter(task_type_aid=task_type_aid)    
    if sub_task_type_obj:
        for j in sub_task_type_obj:
            print('sub_task_AID',j.sub_task_type_aid)
            print("sub_task_type_label",j.sub_task_type_label)
            sub_task_data[j.sub_task_type_aid] = j.sub_task_type_label
    else:
        sub_task_data['null']="NA"

    print("sub_task_data",sub_task_data)    
    
    return JsonResponse(sub_task_data,safe=False)

def get_sub_issue_type(request):
    print("get_sub_issue_type")
    issue_type_aid=request.GET.get('issue_type')
    print("issue_type_aid",issue_type_aid)
    # issue_type_obj=Issue_Type_Master.objects.get(issue_type_aid=issue_type_aid)
    # issue_type_label=issue_type_obj.issue_type_label
    
    sub_issue_data={}
    sub_issue_type_obj=Sub_Issue_Type_Master.objects.filter(issue_type_aid=issue_type_aid)
    if sub_issue_type_obj:
        for j in sub_issue_type_obj:
            print('sub_task_AID',j.sub_issue_type_aid)
            print("sub_task_type_label",j.sub_issue_type_label)
            sub_issue_data[j.sub_issue_type_aid] = j.sub_issue_type_label
            # sub_issue_data['issue_type'] = issue_type_label
    else:
        print("else")
        sub_issue_data['null']="NA"
    print("sub_task_data",sub_issue_data)    
    
    return JsonResponse(sub_issue_data,safe=False) 

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
 

def issue_registrartion(request):
    print("issue_registrartion")
    user_obj=Users.objects.get(u_name=request.session['username'])
    print("UAID",user_obj.u_aid)
    added_by=user_obj.u_aid
    today_date=datetime.now()
    originator_name=user_obj.u_fname  +" " + user_obj.u_lname
    print("originator_name",originator_name)
    print("Dept_name",user_obj.dept_aid)

    department_obj=Department.objects.get(dept_aid=user_obj.dept_aid)
    print("dept name",department_obj.dept_label)

    user_category_obj=UserCategory.objects.all()
    issue_function_obj=IssueFunctionMaster.objects.all()
    issue_priority_obj=IssuePriorityMaster.objects.all()
    issue_approval_master=IssueApprovalstatusMaster.objects.all()    
    users_obj=Users.objects.all()
    mdl_overview_obj=ModelOverview.objects.all()
    issue_type_obj=Issue_Type_Master.objects.all()
   

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

    print("post data",request.POST)
    request_data = {x:request.POST.get(x) for x in request.POST.keys()}
    print("postrequest_data",request_data)
    if request.method == 'POST':
        print("post")
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

        issue_completion_status=request_data['issue_completion_status']
        issue_approval_status=request_data['issue_approval_status']
        issue_relevant_personnel_check=request_data['issue_relevant_personnel_check']
        issue_summery_check=request_data['issue_summery_check']
        print("issue_summery_check",issue_summery_check)
     
        issue_registration_obj=IssueRegistration(issue_id=issue_id,department=department,originator=originator,issue_function=issue_function,
                                               registration_date=issue_registration_date,issue_type=issue_type,sub_issue_type=sub_issue_type,
                                               priority=issue_priority,end_date=issue_end_date,completion_status=issue_completion_status,
                                               approval_status=issue_approval_status,issue_major_ver=issue_major_ver,
                                               issue_minor_ver=issue_minor_ver,addedby=added_by,adddate=today_date,
                                               link_id=link_id
                                               )         
        
        issue_registration_obj.save()
        if issue_relevant_personnel_check == 'True':
            originator_relevant=request_data['issue_originator_relevant']
            issue_assigned_to=request.POST.getlist('issue_assigned_to')
            issue_approved_by=request.POST.getlist('issue_approved_by')
            print('issue_approved_by',issue_approved_by)
            print('issue_assigned_to',issue_assigned_to)
            # print('Relevant Personnel',relevant_personnel,originator_relevant,assigned_to,approved_by)
            if originator_relevant:
                issue_relevant_personnel_obj=IssueRelevantPersonnel(u_type="Originator",u_id=user_obj.u_aid,
                                                     issue=issue_registration_obj,addedby=added_by,adddate=today_date)
                issue_relevant_personnel_obj.save()

            for i in issue_assigned_to:
                print('issue_assigned_to',i)
               
                issue_relevant_personnel_obj=IssueRelevantPersonnel(u_type="Assignee",u_id=i,
                                                     issue=issue_registration_obj,addedby=added_by,adddate=today_date)
                issue_relevant_personnel_obj.save()
                #notification code
                notification_trigger="New issue registered - "+ issue_id  
                insert_data_notification(added_by,i,"Issue",notification_trigger,1)
                print("notificatio assigeee saved")
                thread_id=thread_creation(added_by,i)
                issue_assignee_thread_lst.append({"from": str(added_by), "to": str(i),"thread_id":str(thread_id)})
            for j in issue_approved_by:
                print('issue_approved_by',j)      
        
                issue_relevant_personnel_obj=IssueRelevantPersonnel(u_type="Approver",u_id=j,
                                                     issue=issue_registration_obj,addedby=added_by,adddate=today_date)
                issue_relevant_personnel_obj.save()
                #notification code
                notification_trigger="New issue registered - "+ issue_id  
                insert_data_notification(added_by,i,"Issue",notification_trigger,1)
                print("notificatio assigeee saved")
                thread_id=thread_creation(added_by,j)
                issue_approver_thread_lst.append({"from": str(added_by), "to": str(j),"thread_id":str(thread_id)})
                
        if issue_summery_check == 'True':
            issue_summery=request_data['issue_summery']
            issue_requirement=request_data['issue_requirement']
            issue_assignee_comments=request_data['issue_assignee_comments']
            # issue_approval=request_data['issue_approval']
            issue_approver_comments=request_data['issue_approver_comments']

            
            issue_summery_obj=IssueSummery(issue_summery=issue_summery,issue_requirement=issue_requirement,assignee_comments=issue_assignee_comments,
                                                     approver_comments=issue_approver_comments,
                                                     issue=issue_registration_obj,addedby=added_by,adddate=today_date)
            issue_summery_obj.save() 
    
    context={'issue_function_obj':issue_function_obj,'issue_priority_obj':issue_priority_obj,'issue_type_obj':issue_type_obj,
             'issue_approval_master':issue_approval_master,'originator_name':originator_name,'user_category_obj':user_category_obj,
             'department_obj':department_obj,'users_obj':users_obj,'mdl_overview_obj':mdl_overview_obj,
             'issue_type_obj':issue_type_obj,'issue_assigned_to':json.dumps(issue_assigned_to),
             'issue_approved_by':json.dumps(issue_approved_by),'originatorid':originatorid,'issue_approver_thread_lst':issue_approver_thread_lst,'issue_assignee_thread_lst':issue_assignee_thread_lst}  
    return render(request,'issue_registration.html',context)



def generate_issueID(request):
    print("generate_issueID")
    model_id=request.GET.get('model_id')
    issue_type=request.GET.get('issue_type')
    issue_Lbl=request.GET.get('issue_Lbl')
    print("model_id",model_id)
    issue_id=get_latest_issue(model_id,issue_Lbl,issue_type)
    print("final issue Id",issue_id)
    issue_link_ID={}
    issue_link_ID['issue_id']=issue_id
    issue_link_ID['model_id']=model_id
    return JsonResponse(issue_link_ID,safe=False)

def generate_task_ID(request):
    print("generate_task_ID")
    model_id=request.GET.get('model_id')
    task_type=request.GET.get('task_type')
    task_Lbl=request.GET.get('task_Lbl')
    print("model_id",model_id)
    task_id=get_latest_task(model_id,task_Lbl,task_type)
    print("final task Id",task_id)
    task_link_ID={}
    task_link_ID['task_id']=task_id
    task_link_ID['model_id']=model_id
    return JsonResponse(task_link_ID,safe=False)

def get_latest_task(model_id,task_Lbl,task_type):
    task_id=""
    if task_Lbl=="Model":
        task_registration_count=TaskRegistration.objects.filter(link_id=model_id,task_major_version="1",task_minor_version="0").count()
        task_max=task_registration_count + 1
        task_id=model_id +"T"+ str(task_max) +"0100"
    elif task_Lbl=="Events":
        task_registration_count=TaskRegistration.objects.filter(task_type=task_type,task_major_version="1",task_minor_version="0").count()
        task_max=task_registration_count + 1
        task_id="ET"+ str(task_max) +"0100"
    elif task_Lbl=="Others":
        task_registration_count=TaskRegistration.objects.filter(task_type=task_type,task_major_version="1",task_minor_version="0").count()
        task_max=task_registration_count + 1
        task_id="OT"+ str(task_max) +"0100"
    else:
        task_registration_count=TaskRegistration.objects.filter(task_type=task_type,task_major_version="1",task_minor_version="0").count()
        task_max=task_registration_count + 1
        task_id="T"+ str(task_max) +"0100"
    return task_id


def get_latest_issue(modal_id,issue_Lbl,issue_type):
    print("modal_id",modal_id)
    issue_id=""
    if issue_Lbl=="Model":
        issue_registration_count=IssueRegistration.objects.filter(link_id=modal_id,issue_major_ver="1",issue_minor_ver="0").count()
        issue_max=issue_registration_count + 1
        issue_id=modal_id +"I"+ str(issue_max) +"0100"
    elif issue_Lbl=="Events":
        issue_registration_count=IssueRegistration.objects.filter(issue_type=issue_type,issue_major_ver="1",issue_minor_ver="0").count()
        issue_max=issue_registration_count + 1
        issue_id="EI"+ str(issue_max) +"0100"
    elif issue_Lbl=="Others":
        issue_registration_count=IssueRegistration.objects.filter(issue_type=issue_type,issue_major_ver="1",issue_minor_ver="0").count()
        issue_max=issue_registration_count + 1
        issue_id="OI"+ str(issue_max) +"0100"
    else:
        issue_registration_count=IssueRegistration.objects.filter(issue_type=issue_type,issue_major_ver="1",issue_minor_ver="0").count()
        issue_max=issue_registration_count + 1
        issue_id="I"+ str(issue_max) +"0100"
    return issue_id

class task_approver(APIView):
    def get(self,request):
        try:
            U_id=request.data['uid']
            task_approval_master=TaskApprovalstatusMaster.objects.all().values()
            task_relevant_obj=Task_Relevant_Personnel.objects.filter(u_id=U_id,u_type="Approver").values()
           
            context={"task_relevant_obj":task_relevant_obj,'task_approval_master':task_approval_master}
            
            return Response( context, status=status.HTTP_200_OK)
            
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class task_assignee(APIView):
    def get(self,request):
        try:
            U_id=request.data['uid']
            task_approval_master=TaskApprovalstatusMaster.objects.all().values()
            task_relevant_obj=Task_Relevant_Personnel.objects.filter(u_id=U_id,u_type="Assignee").values()
        
            context={"task_relevant_obj":task_relevant_obj,'task_approval_master':task_approval_master}
            
            return Response( context, status=status.HTTP_200_OK)
                
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

def get_task_ID_data(request):
    print("get_task_ID_data")
    task_id=request.GET.get('task_id')
    print("task_id",task_id)
    task_obj=TaskRegistration.objects.get(task_id=task_id)
    department=task_obj.department
    originator=task_obj.originator
    added_by=task_obj.addedby
    task_function=task_obj.task_function
    if task_function != None:
        task_function_obj=TaskFunctionMaster.objects.get(task_function_aid=task_function)
        task_function_label=task_function_obj.task_function_label
    else:
        task_function_label=''
    reg_date=task_obj.registration_date.strftime('%m/%d/%Y')

 
    task_type=task_obj.task_type
    task_type_obj=TaskTypeMaster.objects.get(task_type_aid=task_type)
    task_type_label=task_type_obj.task_type_label
    sub_task_type=task_obj.sub_task_type 
    task_name=task_obj.task_name
    print('sub_task_type is ',sub_task_type)
    if sub_task_type != "null" and  sub_task_type != None:
        sub_task_type_obj=SubTasktypeMaster.objects.get(sub_task_type_aid=sub_task_type)
        sub_task_type_label=sub_task_type_obj.sub_task_type_label
    else:
        sub_task_type_label="N/A"
    priority=task_obj.priority
    task_name=task_obj.task_name
    print('priority',priority)
    priority_obj=TaskPriorityMaster.objects.get(task_priority_aid=priority)
    task_priority_label=priority_obj.task_priority_label
    print("task_priority_label",task_priority_label)
    end_date=task_obj.end_date.strftime('%m/%d/%Y')
    completion_status=task_obj.completion_status
    approval_status=task_obj.approval_status
    print("approval_status",approval_status)
    approval_status_obj=TaskApprovalstatusMaster.objects.get(task_approvalstatus_aid=approval_status)
    task_approvalstatus_label=approval_status_obj.task_approvalstatus_label
    print("task_approvalstatus_label",task_approvalstatus_label)
    try:
        task_summery_obj=TaskSummery.objects.get(task_registration=task_id)
        task_summery=task_summery_obj.task_summery
        task_req=task_summery_obj.task_requirement
        task_assignee=task_summery_obj.assignee_comments
        approver_comments=task_summery_obj.approver_comments
    except:
        task_summery=''
        task_req=''
        task_assignee=''
        approver_comments= ''
    # approval=task_summery_obj.approval
    
    print("task_summery",task_summery)
    print("task_req",task_req)
    print("approver_comments",approver_comments)
    task_dict=dict()
    task_approval_master=TaskApprovalstatusMaster.objects.all()
    for i in task_approval_master:
        # print("id",i.task_approvalstatus_aid)
        # print("label",i.task_approvalstatus_label)
        task_dict[i.task_approvalstatus_aid]=i.task_approvalstatus_label

    print("task_dict",task_dict)    
    #notification purpose data
    # task_assignee_lst=[]
    # task_approver_lst=[]
    # task_assignee_obj=Task_Relevant_Personnel.objects.filter(task=task_id,u_type="Assignee")
    # for i in task_assignee_obj:
    #     task_assignee_lst.append(i.u_id)
    # print("task_assignee_lst",task_assignee_lst)    
    # task_approver_obj=Task_Relevant_Personnel.objects.filter(task=task_id,u_type="Approver")
    # for j in task_approver_obj:
    #     task_approver_lst.append(j.u_id)
    # print("task_approver_lst",task_approver_lst)    

    return JsonResponse({'department':department,'originator':originator,'task_function_label':task_function_label,'reg_date':reg_date,
                         'task_type_label':task_type_label,'sub_task_type_label':sub_task_type_label,'task_priority_label':task_priority_label,
                         'end_date':end_date,'completion_status':completion_status,'task_summery':task_summery,'task_name':task_name,
                         'task_req':task_req,'task_approvalstatus_label':task_approvalstatus_label,'approval_status':approval_status,
                         'task_assignee':task_assignee,'approver_comments':approver_comments,'task_dict':task_dict,'task_name':task_name})

def update_summery_data(request):
    print("update_summery_data")
    task_id=request.POST.get('task_id')
    print("task_id",task_id)
    print("get data",request.POST)
    assignee_comments=request.POST.get('assignee_comments')
    completion_status=request.POST.get('completion_status')
    print("completion_status",completion_status)
    approval=request.POST.get('approval_status')
    print("approval",approval)
    update_date=datetime.now()
    updated_by=request.session['uid']
    
    #notification code
    task_assignee_lst=[]
    task_approver_lst=[]
    task_assignee_thread_lst=[]
    task_approver_thread_lst=[]
    # print("task_assignee_thread_lst",task_assignee_thread_lst)    
    # task_approver_obj=Task_Relevant_Personnel.objects.filter(task=task_id,u_type="Approver")
    # for j in task_approver_obj:
    #     task_approver_lst.append(j.u_id) 
    #     if updated_by != j.u_id:
    #         task_approver_thread_lst.append({"from": str(updated_by), "to": str(j.u_id),"thread_id":str(thread_creation(updated_by,j.u_id))})
    # print("task_approver_thread_lst",task_approver_thread_lst) 

    if approval:
        approver_comments=request.POST.get('approver_comments')
        print("approver_comments",approver_comments)
        approver_obj=TaskSummery.objects.get(task_registration=task_id)
        # approver_obj.approval=approval
        approver_obj.approver_comments=approver_comments
        approver_obj.updatedate=update_date
        approver_obj.updatedby=updated_by
        approver_obj.save()
        task_registration_obj=TaskRegistration.objects.get(task_id=task_id)
        task_registration_obj.approval_status=approval
        task_registration_obj.updatedate=update_date
        task_registration_obj.updatedby=updated_by
        task_registration_obj.completion_status=completion_status
        task_registration_obj.save()
    if assignee_comments: 
        summery_obj=TaskSummery.objects.get(task_registration=task_id)
        summery_obj.assignee_comments=assignee_comments
        summery_obj.updatedate=update_date
        summery_obj.updatedby=updated_by
        summery_obj.save()
        task_registration_obj=TaskRegistration.objects.get(task_id=task_id)
        task_registration_obj.updatedate=update_date
        task_registration_obj.updatedby=updated_by
        task_registration_obj.completion_status=completion_status
        task_registration_obj.save() 

        task_assignee_obj=Task_Relevant_Personnel.objects.filter(task=task_id).exclude(u_id = updated_by)
        for i in task_assignee_obj:
            task_assignee_lst.append(i.u_id) 
            # print('tr(updated_by) != str(i.u_id) ',str(updated_by) , str(i.u_id),str(updated_by) != str(i.u_id))
            if str(updated_by) != str(i.u_id):            
                task_assignee_thread_lst.append({"from": str(updated_by), "to": str(i.u_id),"thread_id":str(thread_creation(updated_by,i.u_id))})
                notification_trigger="Task "+task_id+" updated"
                insert_data_notification(updated_by,i,"Task",notification_trigger,1)

    # return response("Response check")  
    print('task_assignee_thread_lst final ',task_assignee_thread_lst)  
    print('task_approver_thread_lst final ',task_approver_thread_lst)
    return JsonResponse({'updated':'true','task_assignee_lst':json.dumps(task_assignee_lst),
                         'task_approver_lst':json.dumps(task_approver_lst),'originatorid':int(updated_by),'task_id':task_id,'task_approver_thread_lst':json.dumps(task_approver_thread_lst),'task_assignee_thread_lst':json.dumps(task_assignee_thread_lst)}) 

class issue_approver(APIView):
    def get(self,request):
        try:
            print("U_id",request.data['uid'])
            print("issue_id",request.data['id'])
            U_id=request.data['uid']
            issueid =request.data['id']
            # modelmetricnmaster = ModelMetricMaster.objects.all()
            # serializer =  ModelMetricMasterSerializer(modelmetricnmaster,many=True)
            # issue_approval_master=IssueApprovalstatusMaster.objects.all()
            issue_relevant_obj=IssueRelevantPersonnel.objects.filter(u_id=U_id,u_type="Approver")
            serializer =  IssueRelevantPersonnelSerializer(issue_relevant_obj,many=True)
            # print("serializer",serializer)
            print("serializer",serializer.data)

            context={"issue_relevant_obj":serializer.data,'issueid':issueid}
            return Response( context, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)


class issue_assignee(APIView):
    def get(self,request):
        try:
            U_id=request.data['uid']
            taskid =request.data['id']
            print('U_id',U_id)

            issue_relevant_obj=IssueRelevantPersonnel.objects.filter(u_id=U_id,u_type="Assignee").values()
            context={"issue_relevant_obj":issue_relevant_obj,'taskid':taskid}
            return Response( context, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class getIssues(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            print("rmse_calendar_issue10000")
            all_data_lst=list()
            dict_data=dict()
            allissues=objrmse.getAllIssuesByUser(request.data['uid'])
            # print("allissues",allissues)
            for i in allissues:
            
                dict_data['title']=allissues[i]["Issue_ID"]
                dict_data['start']= allissues[i]["end_date"]
                # convert string to date object
                d1 = datetime.strptime(allissues[i]["end_date"], "%Y-%m-%d")
                d2 = datetime.strptime(datetime.strftime(datetime.now(),"%Y-%m-%d"), "%Y-%m-%d")
                # difference between dates in timedelta
                delta = d2 - d1
                # print("delta",delta)
                # print("delta",delta.days)
                if delta.days>0 :
                    dict_data['className']='text-danger'   
                elif delta.days<0 and delta.days >=-7  :
                    dict_data['className']='text-warning'   
                else:
                    dict_data['className']='text-success'
                all_data_lst.append(dict_data.copy())
    
            context={'all_data_lst':json.dumps(all_data_lst)}    
            return Response( context, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)





def get_issue_ID_data(request):
    print("get_issue_ID_data")
    issue_id=request.GET.get('issue_id')
    print("issue_id",issue_id)
    issue_obj=IssueRegistration.objects.get(issue_id=issue_id)
    department=issue_obj.department
    originator=issue_obj.originator
    issue_function=issue_obj.issue_function
    print("issue_function",issue_function)
    issue_function_obj=IssueFunctionMaster.objects.get(issue_function_aid=issue_function)
    issue_function_label=issue_function_obj.issue_function_label
    reg_date=issue_obj.registration_date

    print(reg_date)
    issue_type=issue_obj.issue_type
    print("issue_type",issue_type)
    issue_type_obj=Issue_Type_Master.objects.get(issue_type_aid=issue_type)
    issue_type_label=issue_type_obj.issue_type_label
    sub_issue_type=issue_obj.sub_issue_type
    print("sub_issue_type",sub_issue_type)
    sub_issue_type_obj=Sub_Issue_Type_Master.objects.get(sub_issue_type_aid=sub_issue_type)
    sub_issue_type_label=sub_issue_type_obj.sub_issue_type_label
    priority=issue_obj.priority
    print('priority',priority)
    priority_obj=IssuePriorityMaster.objects.get(issue_priority_aid=priority)
    issue_priority_label=priority_obj.issue_priority_label
    print("issue_priority_label",issue_priority_label)
    end_date=issue_obj.end_date
    print("end_date",end_date)
    completion_status=issue_obj.completion_status
    approval_status=issue_obj.approval_status
    print("approval_status",approval_status)
    approval_status_obj=IssueApprovalstatusMaster.objects.get(issue_approvalstatus_aid=approval_status)
    issue_approvalstatus_label=approval_status_obj.issue_approvalstatus_label
    print("issue_approvalstatus_label",issue_approvalstatus_label)
    issue_summery_obj=IssueSummery.objects.get(issue=issue_id)
    issue_summery=issue_summery_obj.issue_summery
    issue_req=issue_summery_obj.issue_requirement
    # approval=issue_summery_obj.approval
    issue_assignee=issue_summery_obj.assignee_comments
    approver_comments=issue_summery_obj.approver_comments

    issue_dict=dict()
    issue_approval_master=IssueApprovalstatusMaster.objects.all()
    for i in issue_approval_master:
        # print("id",i.task_approvalstatus_aid)
        # print("label",i.task_approvalstatus_label)
        issue_dict[i.issue_approvalstatus_aid]=i.issue_approvalstatus_label

    print("issue_dict",issue_dict) 

    print("issue_assignee",issue_assignee)
    print("issue_summery",issue_summery)
    print("issue_req",issue_req)
    return JsonResponse({'department':department,'originator':originator,'issue_function_label':issue_function_label,'reg_date':reg_date.strftime('%m-%d-%Y'),
                         'issue_type_label':issue_type_label,'sub_issue_type_label':sub_issue_type_label,'issue_priority_label':issue_priority_label,
                         'end_date':end_date.strftime('%m-%d-%Y'),'completion_status':completion_status,'issue_summery':issue_summery,
                         'issue_req':issue_req,'issue_approvalstatus_label':issue_approvalstatus_label,'approval_status':approval_status,'issue_dict':issue_dict,
                         'issue_assignee':issue_assignee,'approver_comments':approver_comments})

def issue_update_summery_data(request):
    print("issue_update_summery_data")
    issue_id=request.POST.get('issue_id')
    print("issue_id",issue_id)
    print("get data",request.POST)
    assignee_comments=request.POST.get('assignee_comments')
    completion_status=request.POST.get('completion_status')
    approval=request.POST.get('approval_status')
    update_date=datetime.now()
    updated_by=request.session['uid']
    #notification code
    issue_assignee_lst=[]
    issue_approver_lst=[]
    issue_assignee_thread_lst=[]
    issue_assignee_obj=IssueRelevantPersonnel.objects.filter(issue=issue_id).exclude(u_id = updated_by)
    for i in issue_assignee_obj:
        issue_assignee_lst.append(i.u_id) 
        # print('tr(updated_by) != str(i.u_id) ',str(updated_by) , str(i.u_id),str(updated_by) != str(i.u_id))
        if str(updated_by) != str(i.u_id):            
            issue_assignee_thread_lst.append({"from": str(updated_by), "to": str(i.u_id),"thread_id":str(thread_creation(updated_by,i.u_id))})

    # issue_approver_obj=IssueRelevantPersonnel.objects.filter(issue=issue_id,u_type="Approver")
    # for j in issue_approver_obj:
    #     issue_approver_lst.append(j.u_id)
    # print("issue_approver_lst",issue_approver_lst) 

    #notification update
    for i in issue_approver_lst:
        notification_trigger="Issue "+issue_id+" updated"
        insert_data_notification(updated_by,i,"Issue",notification_trigger,1)
        print("notification approver Updated")
    
    for i in issue_assignee_lst:
        notification_trigger="Issue "+issue_id+" updated"
        insert_data_notification(updated_by,i,"Issue",notification_trigger,1)
        print("notification assignee Updated")

    if approval:
        approver_comments=request.POST.get('approver_comments')
        print("approval",approval)
        print("approver_comments",approver_comments)
        approver_obj=IssueSummery.objects.get(issue=issue_id)
        # approver_obj.approval=approval
        approver_obj.approver_comments=approver_comments
        approver_obj.updatedate=update_date
        approver_obj.updatedby=updated_by
        approver_obj.save()
        issue_registration_obj=IssueRegistration.objects.get(issue_id=issue_id)
        issue_registration_obj.approval_status=approval
        issue_registration_obj.updatedate=update_date
        issue_registration_obj.updatedby=updated_by
        issue_registration_obj.approval_status=approval
        issue_registration_obj.completion_status=completion_status
        issue_registration_obj.save()
    if assignee_comments:
        print("assignee_comments",assignee_comments)
        summery_obj=IssueSummery.objects.get(issue=issue_id)
        summery_obj.assignee_comments=assignee_comments
        summery_obj.updatedate=update_date
        summery_obj.updatedby=updated_by
        summery_obj.save()
        issue_registration_obj=IssueRegistration.objects.get(issue_id=issue_id)
        issue_registration_obj.updatedate=update_date
        issue_registration_obj.updatedby=updated_by
        issue_registration_obj.completion_status=completion_status
        issue_registration_obj.save()
    updated=True
    return JsonResponse({'updated':'true','issue_assignee_lst':json.dumps(issue_assignee_lst),
                         'issue_approver_lst':json.dumps(issue_approver_lst),'originatorid':int(updated_by),'issue_id':issue_id,'issue_assignee_thread_lst':json.dumps(issue_assignee_thread_lst)})


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

def edit_task(request,task_id):
    print("task_id",task_id)

    task_function_objs=TaskFunctionMaster.objects.all()
    task_priority_objs=TaskPriorityMaster.objects.all()
    # sub_task_type_objs=SubTasktypeMaster.objects.all()
    task_approval_master_objs=TaskApprovalstatusMaster.objects.all()    

    task_obj=TaskRegistration.objects.get(task_id=task_id)
    department=task_obj.department
    originator=task_obj.originator
    task_function=task_obj.task_function
    task_function_obj=TaskFunctionMaster.objects.get(task_function_aid=task_function)
    task_function_label=task_function_obj.task_function_label
    print("task_function_label",task_function_label)
    reg_date=task_obj.registration_date.strftime('%m/%d/%Y')  
    task_type=task_obj.task_type 
    task_type_obj=TaskTypeMaster.objects.get(task_type_aid=task_type)
    task_type_label=task_type_obj.task_type_label 
    task_type_aid=task_type_obj.task_type_aid
    task_name=task_obj.task_name
    sub_task_type_objs=SubTasktypeMaster.objects.filter(task_type_aid=task_type_aid)
    
    sub_task_type=task_obj.sub_task_type
    if sub_task_type=='null':
        sub_task_type_label="NA"
    else:
        sub_task_type_obj=SubTasktypeMaster.objects.get(sub_task_type_aid=sub_task_type)
        sub_task_type_label=sub_task_type_obj.sub_task_type_label
    priority=task_obj.priority
    print('priority',priority)
    priority_obj=TaskPriorityMaster.objects.get(task_priority_aid=priority)
    task_priority_label=priority_obj.task_priority_label
    print("task_priority_label",task_priority_label)
    end_date=task_obj.end_date.strftime('%m/%d/%Y')
    completion_status=task_obj.completion_status
    approval_status=task_obj.approval_status
    approval_status_label=TaskApprovalstatusMaster.objects.get(task_approvalstatus_aid=approval_status).task_approvalstatus_label
    try:
        task_summery_obj=TaskSummery.objects.get(task_registration=task_id)
        task_summery=task_summery_obj.task_summery 
        task_req=task_summery_obj.task_requirement
    except Exception as e:
        task_summery="" 
        task_req=""

    all_user=list()
    users_obj=Users.objects.all()
    dict_data=dict()

    print("dict_data",dict_data)    
    print("all user",all_user)    
    relevant_personal_originator=Task_Relevant_Personnel.objects.get(task=task_id,u_type='Originator').u_id
    print("relevant_personal_originator",relevant_personal_originator)
    originator_user=Users.objects.get(u_aid=relevant_personal_originator)
    first_last=originator_user.u_fname + ' '+ originator_user.u_lname
    print("fist last name",first_last)
    
    print("all user count",Users.objects.all().count())
   
    assignee_user=list()
    relevant_personal_assignee=Task_Relevant_Personnel.objects.filter(task=task_id,u_type='Assignee')
    for i in relevant_personal_assignee:
        #print("relevant_personal_assignee",i.u_id)
        
        assignee_user_obj=Users.objects.filter(u_aid=i.u_id)
        for k in assignee_user_obj:
            assignee_user.append(k.u_aid)
    print("assignee_user",assignee_user)

    assignee_user_lst=list()
    for i in users_obj:
        if i.u_aid in assignee_user:
            dict_data["selected"]="selected"
        else:
            dict_data["selected"]=""
        dict_data["u_aid"]=i.u_aid
        dict_data['first_name']=i.u_fname
        dict_data['last_name']=i.u_lname
        assignee_user_lst.append(dict_data.copy())   

    #print("assignee_user_lst",assignee_user_lst)

    approver_user=list()    
    relevant_personal_approver=Task_Relevant_Personnel.objects.filter(task=task_id,u_type='Approver')
    for j in relevant_personal_approver:
        #print("relevant_personal_approver",j.u_id)
        approver_user_obj=Users.objects.filter(u_aid=j.u_id)
        for k in approver_user_obj:
            print("approved by",k.u_aid)
            approver_user.append(k.u_aid)
    print("approver_user",approver_user)

    approver_user_lst=list()
    for i in users_obj:
        if i.u_aid in approver_user:
            dict_data["selected"]="selected"
        else:
            dict_data["selected"]=""
        dict_data["u_aid"]=i.u_aid
        dict_data['first_name']=i.u_fname
        dict_data['last_name']=i.u_lname
        approver_user_lst.append(dict_data.copy())   
 


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
        task_summery=request_data['task_summery']
        task_name=request_data['txt_Task_Name']
        print("task_summery",task_summery)
        task_req=request_data['task_req']
        print("task_req",task_req)
        task_update_obj=TaskRegistration.objects.get(task_id=task_id)
        task_update_obj.department=department
        task_update_obj.originator=originator
        task_update_obj.task_function=task_function
        task_update_obj.registration_date=registration_date
        task_update_obj.task_type=task_aid
        task_update_obj.sub_task_type=sub_task_type
        task_update_obj.priority=priority
        task_update_obj.end_date=end_date
        task_update_obj.completion_status=completion_status
        task_update_obj.approval_status=approval_status
        task_update_obj.task_name=task_name
        task_update_obj.save()
        task_summ_update=TaskSummery.objects.get(task_registration=task_id)
        task_summ_update.task_summery=task_summery
        task_summ_update.task_requirement=task_req
        
        task_summ_update.save()
        return redirect('getTaskss')
    context={'task_id':task_id,'department':department,'originator':originator,'task_function_label':task_function_label,'reg_date':reg_date,'task_name':task_name,
                         'task_type_label':task_type_label,'sub_task_type_label':sub_task_type_label,'task_priority_label':task_priority_label,
                         'end_date':end_date,'completion_status':completion_status,'task_summery':task_summery,'task_function':task_function,
                         'task_req':task_req,'approval_status':approval_status,'approval_status_label':approval_status_label,'task_function_objs':task_function_objs,'priority':priority,'sub_task_type':sub_task_type,
                         'sub_task_type_objs':sub_task_type_objs,'task_priority_objs':task_priority_objs,'task_approval_master_objs':task_approval_master_objs,
                         'originator_name':first_last,'approver_user_obj':approver_user_lst,'assignee_user_obj':assignee_user_lst}
    return render(request,'edit_task.html',context)

def edit_issue(request,issue_id):
    print("issue_id",issue_id)

    task_function_objs=TaskFunctionMaster.objects.all()
    task_priority_objs=TaskPriorityMaster.objects.all()
    # sub_task_type_objs=SubTasktypeMaster.objects.all()
    task_approval_master_objs=TaskApprovalstatusMaster.objects.all()    

    issue_obj=IssueRegistration.objects.get(issue_id=issue_id)
    department=issue_obj.department
    originator=issue_obj.originator
    added_by=issue_obj.addedby
    issue_function=issue_obj.issue_function
    issue_function_obj=TaskFunctionMaster.objects.get(task_function_aid=issue_function)
    issue_function_label=issue_function_obj.task_function_label
    print("issue_function_label",issue_function_label)
    reg_date=issue_obj.registration_date
    reg_date=reg_date.strftime('%m-%d-%Y')
    issue_type=issue_obj.issue_type
    issue_type_obj=Issue_Type_Master.objects.get(issue_type_aid=issue_type)
    issue_type_label=issue_type_obj.issue_type_label
    issue_type_aid=issue_type_obj.issue_type_aid
    sub_issue_type_objs=Sub_Issue_Type_Master.objects.filter(issue_type_aid=issue_type_aid)
    
    sub_issue_type=issue_obj.sub_issue_type
    sub_issue_type_obj=Sub_Issue_Type_Master.objects.get(sub_issue_type_aid=sub_issue_type)
    sub_issue_type_label=sub_issue_type_obj.sub_issue_type_label

    priority=issue_obj.priority
    print('priority',priority)
    priority_obj=TaskPriorityMaster.objects.get(task_priority_aid=priority)
    issue_priority_label=priority_obj.task_priority_label
    print("issue_priority_label",issue_priority_label)
    end_date=issue_obj.end_date.strftime('%m-%d-%Y')
    completion_status=issue_obj.completion_status
    approval_status=issue_obj.approval_status
    approval_status_label=TaskApprovalstatusMaster.objects.get(task_approvalstatus_aid=approval_status).task_approvalstatus_label
    issue_summery_obj=IssueSummery.objects.get(issue=issue_id)
    issue_summery=issue_summery_obj.issue_summery
    print("issue_summery",issue_summery)
    issue_req=issue_summery_obj.issue_requirement

    

    request_data = {x:request.POST.get(x) for x in request.POST.keys()}
    print("postrequest_data",request_data)
    if request.method == 'POST':
        print("post edit")
        issue_id=request_data['issue_id']
        print("issue_id",issue_id)
        department=request_data['department']
        originator=request_data['originator']
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
        issue_update_obj=IssueRegistration.objects.get(issue_id=issue_id)
        issue_update_obj.department=department
        issue_update_obj.originator=originator
        issue_update_obj.issue_function=issue_function
        issue_update_obj.registration_date=registration_date
        issue_update_obj.issue_type=issue_aid
        issue_update_obj.sub_issue_type=sub_issue_type 
        issue_update_obj.priority=priority
        issue_update_obj.end_date=end_date
        issue_update_obj.completion_status=completion_status
        issue_update_obj.approval_status=approval_status
        issue_update_obj.save()
        issue_summ_update=IssueSummery.objects.get(issue=issue_id)
        issue_summ_update.issue_summery=issue_summery
        issue_summ_update.issue_requirement=issue_req
        issue_summ_update.save()
        return redirect('show_issue')
    context={'issue_id':issue_id,'department':department,'originator':originator,'issue_function_label':issue_function_label,'reg_date':reg_date,
                         'issue_type_label':issue_type_label,'sub_issue_type_label':sub_issue_type_label,'issue_priority_label':issue_priority_label,
                         'end_date':end_date ,'completion_status':completion_status,'issue_summery':issue_summery,'priority':priority,
                         'issue_req':issue_req,'approval_status':approval_status,'task_function_objs':task_function_objs,'approval_status_label':approval_status_label,
                         'sub_issue_type_objs':sub_issue_type_objs,'task_priority_objs':task_priority_objs,'task_approval_master_objs':task_approval_master_objs}
    return render(request,'edit_issue.html',context)

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
class allocate_icq(APIView):
    def get(self,request): 
        try:            
            userobj = Users.objects.all()
           
            context={'sections':objmaster.getSections(),'user':userobj,'review':objmaster.getICQIds()}
            return Response( context, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class save_allocation(APIView):
    def post(self,request):  
        try:     
            section_aid = request.data['section_aid']
            users = request.data['users']
            # end_date = request_data['end_date'][6:] + "-" + request_data['end_date'][3:5] + "-" + request_data['end_date'][:2]
            if request.data['rv_id'] == "addnew":
                last_rvid_obj = IcqQuestionRatingAllocation.objects.aggregate(max('review_id'))
                last_rvid = last_rvid_obj['review_id__max']
                splt_rvid = last_rvid.split('_')
                latest_rvid = int(splt_rvid[1]).__add__(1) #used magic method django
                for user, section_id in [(x,y) for x in users for y in section_aid]:
                    allocate_obj = IcqQuestionRatingAllocation(review_id ="Rv_"+str(latest_rvid),review_name = request.data['rv_name'],section_aid = section_id,allocated_to = user,end_date = None)
                    allocate_obj.save()
                return Response( {"isvalid":"true"}, status=status.HTTP_200_OK) 
            else:
                for user, section_id in [(x,y) for x in users for y in section_aid]:
                    allocate_obj = IcqQuestionRatingAllocation(review_id =request.data['rv_id'],review_name = request.data['rv_name'],section_aid = section_id,allocated_to = user,end_date = None)
                    allocate_obj.save() 
                return Response( {"isvalid":"true"}, status=status.HTTP_200_OK)
        except Exception as e: 
            print(traceback.print_exc())
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)


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
        prioobj = IssuePriorityMaster.objects.all()
        return render(request, 'show_issue_priority.html',{'actPage' :'RMSE - Issue Priority','users':prioobj})
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
        print("---------save_issue_priority",request.GET)
        request_data = {x:request.GET.get(x) for x in request.GET.keys()}
        update_id=request.GET.get('update_id')
        label=request.GET.get('label')
        desc=request.GET.get('desc')
        if update_id:
            print("update priority")
            print("request_data['update_id']",(update_id))
            issue_priority_obj=IssuePriorityMaster.objects.get(issue_priority_aid=update_id)
            issue_priority_obj.issue_priority_label=label
            issue_priority_obj.issue_priority_description=desc
            issue_priority_obj.save()
            return JsonResponse({"isvalid":"update"})
        else:    
            print("save")
            issue_obj = IssuePriorityMaster(issue_priority_label = request_data['label'],issue_priority_description = request_data['desc'])
            issue_obj.save()
            print("save successfully")
        return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print("setuppycaret is",e) 
        print('setuppycaret traceback is ', traceback.print_exc()) 
        return JsonResponse(e)
    
def show_issue_approval_status(request):
    try: 
        prioobj = IssueApprovalstatusMaster.objects.all()
        return render(request, 'show_issue_approval_status.html',{'actPage' :'RMSE - Issue Approval Status','users':prioobj})
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
        print("---------save_issue_approval_status",request.GET)
        #request_data = {x:request.GET.get(x) for x in request.GET.keys()}
        update_id=request.GET.get('update_id')
        label=request.GET.get('label')
        desc=request.GET.get('desc')
        if update_id:
            print("update")
            print("request_data['update_id']",(update_id))
            issue_approval_obj=IssueApprovalstatusMaster.objects.get(issue_approvalstatus_aid=update_id)
            issue_approval_obj.issue_approvalstatus_label=label
            issue_approval_obj.issue_approvalstatus_description=desc
            issue_approval_obj.save()
            return JsonResponse({"isvalid":"update"})
        else:    
            print("save")
            issue_approval_obj = IssueApprovalstatusMaster(issue_approvalstatus_label = label,issue_approvalstatus_description = desc)
            issue_approval_obj.save()
            print("save successfully")
        return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print("setuppycaret is",e) 
        print('setuppycaret traceback is ', traceback.print_exc()) 
        return JsonResponse(e)

def show_issue_type(request):
    try: 
        typeobj =Issue_Type_Master.objects.all()
        print("-----------------",typeobj)
        return render(request, 'show_issue_type.html',{'actPage' :'RMSE - Issue Type','users':typeobj})
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
    print()
    try:
        print("---------save_issue_type",request.GET)
        #request_data = {x:request.GET.get(x) for x in request.GET.keys()}
        update_id=request.GET.get('update_id')
        label=request.GET.get('label')
        desc=request.GET.get('desc')
        if update_id:
            print("update")
            print("request_data['update_id']",(update_id))
            issue_obj=Issue_Type_Master.objects.get(issue_type_aid=update_id)
            issue_obj.issue_type_label=label
            issue_obj.issue_type_description=desc
            issue_obj.save()
            return JsonResponse({"isvalid":"update"})
        else:    
            print("save")
            issuetype_obj = Issue_Type_Master(issue_type_label = label,issue_type_description = desc)
            issuetype_obj.save()
            print("save successfully")
            return JsonResponse({"isvalid":"true"})
        
    except Exception as e:
        print("setuppycaret is",e) 
        print('setuppycaret traceback is ', traceback.print_exc()) 
        return JsonResponse(e)

def show_sub_issue(request):
    try: 
        subtypeobj = Sub_Issue_Type_Master.objects.all()
        print("-----------------",subtypeobj)
        return render(request, 'show_sub_issue.html',{'actPage' :'RMSE - Sub Issue Type','users':subtypeobj})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())

def add_sub_issue_type(request):
    try: 
        typeobj = Issue_Type_Master.objects.all()
        return render(request, 'add_sub_issue_type.html',{'actPage':'RMSE - Add Sub Issue Type','issuetypes':typeobj})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def save_sub_issue_type(request):
    print()
    try:
        print("---------save_sub_issue_type",request.GET)
        request_data = {x:request.GET.get(x) for x in request.GET.keys()}

        update_id=request.GET.get('update_id')
        issuetype=request.GET.get('issuetype')
        label=request.GET.get('label')
        desc=request.GET.get('desc')
        print("update_id",update_id)
        print("issuetype",issuetype)
        if update_id:
            print("update")
            # issue_type_aid = Issue_Type_Master.objects.get(issue_type_label = issuetype).issue_type_aid
            # print("issue_type_aid",issue_type_aid)
            sub_issue_type_obj=Sub_Issue_Type_Master.objects.get(sub_issue_type_aid=update_id)
            sub_issue_type_obj.sub_issue_type_label=label
            sub_issue_type_obj.sub_issue_type_description=desc
            # sub_issue_type_obj.issue_type_aid=issue_type_aid
            sub_issue_type_obj.save()
            return JsonResponse({"isvalid":"update"})
        else:        
            print("save")
            issue_type_obj = Issue_Type_Master.objects.get(issue_type_aid = issuetype)
            print("------------------issue_type_obj",issue_type_obj)
            sub_issue_obj =Sub_Issue_Type_Master(sub_issue_type_label = label,sub_issue_type_description =desc ,issue_type_aid = issue_type_obj)
            sub_issue_obj.save()
            print("save successfully")
            return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print("setuppycaret is",e) 
        print('setuppycaret traceback is ', traceback.print_exc()) 
        return JsonResponse(e)

def edit_issue_function(request,id):
    print("edit_issue_function",id)
    try: 
        issue_fun_obj=IssueFunctionMaster.objects.get(issue_function_aid=id)
        issue_function_label=issue_fun_obj.issue_function_label
        issue_function_desc=issue_fun_obj.issue_function_description
        return render(request, 'add_new_issue.html',{'issue_function_label':issue_function_label,
                                                     'issue_function_desc':issue_function_desc,'id':id})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())

def edit_issue_type(request,id):
    print("edit_issue_type",id)
    try: 
        issue_type_obj=Issue_Type_Master.objects.get(issue_type_aid=id)
        issue_type_label=issue_type_obj.issue_type_label
        issue_type_description=issue_type_obj.issue_type_description
        return render(request, 'add_issue_type.html',{'issue_type_label':issue_type_label,
                                                     'issue_type_description':issue_type_description,'id':id})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())       

def edit_sub_issue_type(request,id):
    print("edit_sub_issue_type",id)
    try: 
        sub_issue_type_obj=Sub_Issue_Type_Master.objects.get(sub_issue_type_aid=id)
        issue_type=sub_issue_type_obj.issue_type_aid
        sub_issue_type_label=sub_issue_type_obj.sub_issue_type_label
        sub_issue_type_description=sub_issue_type_obj.sub_issue_type_description
        return render(request, 'add_sub_issue_type.html',{'sub_issue_type_label':sub_issue_type_label,
                                                     'sub_issue_type_description':sub_issue_type_description,'id':id,'issue_type':issue_type,
                                                     'check':'true'})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())         

def edit_issue_priority(request,id):
    print("edit_issue_priority",id)
    try: 
        issue_priority_obj=IssuePriorityMaster.objects.get(issue_priority_aid=id)
        issue_priority_label=issue_priority_obj.issue_priority_label
        issue_priority_description=issue_priority_obj.issue_priority_description
        return render(request, 'add_issue_priority.html',{'issue_priority_label':issue_priority_label,
                                                     'issue_priority_description':issue_priority_description,'id':id})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())         

def edit_issue_approval_status(request,id):
    print("edit_issue_approval_status",id)
    try: 
        issue_approval_status_obj=IssueApprovalstatusMaster.objects.get(issue_approvalstatus_aid=id)
        issue_approval_status_label=issue_approval_status_obj.issue_approvalstatus_label
        issue_approval_status_description=issue_approval_status_obj.issue_approvalstatus_description
        return render(request, 'add_issue_approval.html',{'issue_approval_status_label':issue_approval_status_label,
                                                     'issue_approval_status_description':issue_approval_status_description,'id':id})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())         

def edit_task_function(request,id): 
    try: 
        task_function_obj=TaskFunctionMaster.objects.get(task_function_aid=id)
        task_function_label=task_function_obj.task_function_label
        task_function_description=task_function_obj.task_function_description
        return render(request, 'addtaskfun.html',{'task_function_label':task_function_label,
                                                     'task_function_description':task_function_description,'id':id,'isDisabled':'disabled'})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())  

def edit_task_type(request,id): 
    try: 
        task_type_obj=TaskTypeMaster.objects.get(task_type_aid=id)
        task_type_label=task_type_obj.task_type_label
        task_type_description=task_type_obj.task_type_description
        return render(request, 'addtasktype.html',{'task_type_label':task_type_label,
                                                     'task_type_description':task_type_description,'id':id,'isDisabled':'disabled'})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc()) 

def edit_sub_task_type(request,id):
    try: 
        sub_task_type_obj=SubTasktypeMaster.objects.get(sub_task_type_aid=id)
        task_type=sub_task_type_obj.task_type_aid
        sub_task_type_label=sub_task_type_obj.sub_task_type_label
        sub_task_type_description=sub_task_type_obj.sub_task_type_description
        return render(request, 'addsubtasktype.html',{'sub_task_type_label':sub_task_type_label,
                                                     'sub_task_type_description':sub_task_type_description,'id':id,'task_type':task_type,'isDisabled':'disabled'})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc()) 

def edit_task_priority(request,id): 
    try: 
        task_priority_obj=TaskPriorityMaster.objects.get(task_priority_aid=id)
        task_priority_label=task_priority_obj.task_priority_label
        task_priority_description=task_priority_obj.task_priority_description
        return render(request, 'addtaskpriority.html',{'task_priority_label':task_priority_label,
                                                     'task_priority_description':task_priority_description,'id':id,'isDisabled':'disabled'})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())

def edit_task_approval(request,id): 
    try: 
        task_approval_status_obj=TaskApprovalstatusMaster.objects.get(task_approvalstatus_aid=id)
        task_approval_status_label=task_approval_status_obj.task_approvalstatus_label
        task_approval_status_description=task_approval_status_obj.task_approvalstatus_description
        return render(request, 'addtaskapprovalstatus.html',{'task_approval_status_label':task_approval_status_label,
                                                     'task_approval_status_description':task_approval_status_description,'id':id,'isDisabled':'disabled'})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())    

def checkUserRole(request):
    try:
        mdl_id = request.GET.get('mdl_id','none') 
        return JsonResponse({'role': objrmse.checkUserRole(request.session['uid'],mdl_id)})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())   

class checkUserRole_Issue(APIView):
    def get(self,request):
        try:
            issue_id = request.data['mdl_id']
            print("issue_id",issue_id)
            return Response({'role': objrmse.checkUserRole_Issue(request.data['uid'],issue_id)}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)