from django.shortcuts import render ,redirect
import traceback
import os 
from pathlib import Path
import json 
import pandas as pd
from django.http import JsonResponse,HttpResponse
from django.core import serializers 
from django.core.files.storage import FileSystemStorage
from datetime import *
from django.template import RequestContext
import numpy as np
import shutil 
# from langchain.document_loaders import PyPDFLoader

BASE_DIR = Path(__file__).resolve().parent.parent
# Create your views here.
user_name = "user1"
file_path = os.path.join(BASE_DIR, 'static/Data/')
decomm_path = os.path.join(BASE_DIR, 'static/Data/')
 

savefile_name = file_path +  "Modelinfo.csv" 
# Create your views here.
import pyodbc   
from pymongo import MongoClient
# DEFINE THE DATABASE CREDENTIALS
user = 'sa'
password = 'Ajit@123'
host = 'LENOVOARUN\SQL2022'
port = 1433
database = 'prope_db'
import environ
env = environ.Env()
# reading .env file
environ.Env.read_env()
# mongodb set up

cluster=MongoClient('localhost',27017,connect=False)
dbname=env("MongoDB_NM")
db=cluster[dbname]
collection=db["SrcData"]
collection_file_info=db["SrcFileInfo"]
collection_target=db["TargetData"]
collection_process_status=db["ProcessStatus"]
collection_model_information=db["ModelInformation"]
collection_model_risk=db["ModelRisk"]
collection_model_documents=db["ModelDocuments"]
collection_model_process_status=db['ProcessStatus']
collection_model_target_value=db['TargetValue']
collection_model_chart_image=db['Chartimg']
collection_model_implementation_control=db['ImplementationControls']
collection_conceptual_soundness=db['ConceptualSoundness']
collection_data_integrity=db['DataIntegrity']
collection_confirm_data_source=db['DataSource']
collection_model_usage=db['ModelUsage']
collection_validation_findings=db['ValidationFindings']
collection_chart_viewed=db['ChartViewed']

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from .RegModel.registermodel import RegisterModel as Register
from .RegModel.registermodel import MdlOverviewCls,ModelRisks,MdlRelevantPersonnel,MdlDependenciesCls,MdlPerformanceMonitoring,MdlDocs

from .Adm_Utils.Masters import MasterTbls
from .DAL.dboperations import dbops
from .models import *
from .UserInfo.user import UserInfo
from .Validation.validation import Validation
from .RMSE.RMSE import RMSEModel
objreg=Register()  
objmaster=MasterTbls()
objvalidation=Validation()
objdbops=dbops()
objrmse=RMSEModel()

import requests
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework import generics, permissions, status,serializers
# PYTHON FUNCTION TO CONNECT TO THE MYSQL DATABASE AND
# RETURN THE SQLACHEMY ENGINE OBJECT

# engine=sa.create_engine(
#         url="mssql+pyodbc://{0}:{1}@{2}/{3}?driver=SQL+Server+Native+Client+11.0".format(
#             user, password, host,  database
#         ))
# engine = sa.create_engine("mssql+pyodbc://sa:sqlAdm@18@HOST_IP:PORT/DATABASENAME?driver=SQL+Server+Native+Client+11.0")
cluster=MongoClient('localhost',27017,connect=False)
dbname=env("MongoDB_NM")
db=cluster[dbname]
collection_prdn_file_info=db['Prdn_File_Info']
collection_prdn_src_data=db['Prdn_Src_Data']

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

def get_token_or_redirect(request):
    token = request.session.get('accessToken')
    if not token:
        return None  
    return token

def custom_404_view(request, exception):
    print("custom_404_view")
    username = request.session.get('username')
    print("Username in session:", username)

    if not username:
        print("User not logged in redirecting to login")
        token = get_token_or_redirect(request)
        if not token:
            print("Token Handled")
            return redirect('login')
        return redirect('login')
    else:
        print("User is logged in showing 404")
        return render(request, '404.html', status=404)

def getAPIURL():
    api_url=os.environ['API_URL']
    return api_url

def getFLAPIURL():
    api_url=os.environ['FL_API_URL']
    return api_url

def blank(request):
    try:          
        objreg=Register()
        
        dttbl=objreg.getUserDeatils(request.session['utype'],request.session['dept'])
       
        if dttbl.empty == False:
            request.session['li_mrm']=dttbl[dttbl['r_label'] == 'Model Risk Management'].values[0][2]
            request.session['li_qv']=dttbl[dttbl['r_label'] =='Dashboard'].values[0][2] 
            request.session['li_modinv']=dttbl[dttbl['r_label'] =='Model Inventory'].values[0][2]
            # request.session['li_modtodo']=dttbl[dttbl['r_label'] =='Upcoming'].values[0][2]
            request.session['li_modtasks']=dttbl[dttbl['r_label'] =='Tasks'].values[0][2]
            # request.session['li_idmod']=dttbl[dttbl['r_label'] =='Identify New Model'].values[0][2] 
            # request.session['li_subdoc']=dttbl[dttbl['r_label'] =='Submit Documentation/ Evidence'].values[0][2]
            # request.session['li_reqcng']=dttbl[dttbl['r_label'] =='Request a Change'].values[0][2]
            # request.session['li_updoc']=dttbl[dttbl['r_label'] =='Upload Document'].values[0][2]
            # request.session['li_upcod']=dttbl[dttbl['r_label'] =='Upload Code'].values[0][2]
            # request.session['li_upcod']=dttbl[dttbl['r_label'] =='Upload Code'].values[0][2]
            request.session['li_adduser']=dttbl[dttbl['r_label'] =='Dept Head'].values[0][2] 
            request.session['li_task']=dttbl[dttbl['r_label'] =='Tasks'].values[0][2]
            request.session['task_registration']='block'
            request.session['li_issuesReg']='block'
            request.session['li_taskApprv']='block' 
            request.session['li_taskComplete']='block'
            request.session['li_issueComplete']='block'
            request.session['li_issueApprv']='block'
            request.session['li_icqqtn']='block' 
          
            if(str(objmaster.checkMRMHead(str(request.session['uid']))))=="1" or (str(objmaster.checkMRMMgr(str(request.session['uid']))))=="1":
                request.session['li_icqqtnfinal']='block'
                request.session['li_modval']='block'
                request.session['li_icqqtn']='none' 
            else:
                request.session['li_icqqtnfinal']='none'
                request.session['li_modval']='none'

            

        del dttbl
        request.session['notifications']=objvalidation.getVTNotifications(request.session['uid'])   
         
             
        # return render(request, 'addICQQtns.html',{'sections':objmaster.getSections(),'actPage':'RMSE','notifylen':str(len(objvalidation.getVTNotifications(request.session['uid'])))})
        return render(request, 'blank.html',{'actPage':'RMSE','notifylen':str(len(objvalidation.getVTNotifications(request.session['uid'])))})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 

# def modelList(request):
#     print("modelList................................")
#     try:
#         ty =request.GET.get('ty', 'False') 
#         colnm =request.GET.get('colnm', 'False') 
#         chartnm =request.GET.get('chartnm', 'False') 
#         mdlType =request.GET.get('mdlType', 'None') 
#         canAdd=request.session['canAdd']
#         Authorization(request,request.session['ucaid'],'Model Inventory')
#         api_url=getAPIURL()+"projectsInfo/"       
#         data_to_save={ 
#             'uid':request.session['uid'],
#             'filterType':ty,
#             'filterColumn':chartnm,
#             'filterValue':colnm,
#             'mdlType':mdlType,
#             'istool':'0'} 
#         header = {
#         "Content-Type":"application/json",
# 	    'Authorization': 'Token '+request.session['accessToken']
#         }
#         response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)         
#         api_data=response.json() 
#         modelinfo=api_data['modelinfo']#objreg.getModelByFilter(request.session['uid'],ty,chartnm,colnm,'0')
#         if ty=='pie' and chartnm=='Model Category':
#             modeltype='Model Category - ' +colnm
#         elif ty=='pie'  :
#             modeltype='Model Type - ' +colnm
#         elif ty =='bar':
#             modeltype=chartnm +' - '+ colnm
#         else:
#             modeltype=''
             
#         # return render(request, 'addICQQtns.html',{'sections':objmaster.getSections(),'actPage':'RMSE','notifylen':str(len(objvalidation.getVTNotifications(request.session['uid'])))})
#         return render(request, 'modelList.html',{'actPage':'RMSE','modelinfo':modelinfo,'canAdd':canAdd,'modeltype':modeltype})
#     except Exception as e:
#         print('setuppycaret is ',e)
#         print('setuppycaret traceback is ', traceback.print_exc()) 


# def modelDetails(request):
#     try:
#         print('modelDetails')
#         mdlId =request.GET.get('mdlId', 'False') 
#         api_url=getAPIURL()+"taskListByModel/"       
#         data_to_save={ 
#             'uid':request.session['uid'],             
#             'mdl_id':mdlId} 
#         header = {
#         "Content-Type":"application/json",
# 	    'Authorization': 'Token '+request.session['accessToken']
#         }
#         response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)         
#         api_data=response.json() 
#         task_list=api_data['task_list']
#         activityobj = ActivityTrail.objects.filter(refference_id = mdlId).order_by('-added_on')  
#         activity_lst = activityinfo(activityobj)

#         ### Documents ###        
#         api_url_a = getAPIURL()+"GetMdlDocumentsAPI/"       
#         data_to_get   ={ 
#             'uid':request.session['uid'],             
#             'mdl_id':mdlId} 
#         header = {
#         "Content-Type":"application/json",
# 	    'Authorization': 'Token '+request.session['accessToken']
#         }
#         response_a = requests.get(api_url_a, data= json.dumps(data_to_get),headers=header)         
#         api_data_a=response_a.json() 
#         print("response documents",api_data_a)
#         mdl_doc_type_uploaded = [{'doc_type':i['mdl_doc_type']} for i in api_data_a if i['mdl_id'] == mdlId]
#         print("mdl_doc_type_uploaded",mdl_doc_type_uploaded)
#         all_docs = [{'doc_type':'1','doc_name':'Model Development'},{'doc_type':'2','doc_name':'User Manual'},
#                     {'doc_type':'3','doc_name':'Model Data'},{'doc_type':'4','doc_name':'Merged Model Data'},
#                     {'doc_type':'5','doc_name':'Model Code'},{'doc_type':'6','doc_name':'User Acceptance Testing'},
#                     {'doc_type':'7','doc_name':'Technical Manual'},{'doc_type':'8','doc_name':'Onboarding Documents'}]
        
#         ids_to_remove = {d['doc_type'] for d in mdl_doc_type_uploaded}
#         unuploaded_list = [d for d in all_docs if d['doc_type'] not in ids_to_remove]
#         print("unuploaded list",unuploaded_list)

#         return render(request, 'modelDeatails.html',{'actPage':'RMSE','mdl_id':mdlId,'task_list':task_list,'mdlsts':api_data['mdlsts'],
#                         'issue_list':api_data['issue_list'],'validationRatings':api_data['validationRatings'],'modelDocs':objvalidation.getModelDocs(mdlId),'activity_lst':activity_lst,'unuploaded_list':unuploaded_list})
#     except Exception as e:
#         print('setuppycaret is ',e)
#         print('setuppycaret traceback is ', traceback.print_exc())

def uploadfiles(request):
    mdlid= request.POST['mdl_id']
    mdl_doc_type = request.POST['mdl_doc_type']
    destination_path = os.path.join(BASE_DIR, 'static\\document_files\\'+mdlid+'\\')
    objdocs=MdlDocs()
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    # txtMDD
    fl_MD = request.FILES['filename']             
    if fl_MD != 'none':
        fs = FileSystemStorage()
        savefile_name = destination_path + mdlid+'_'+fl_MD.name
        # if os.path.exists(savefile_name):
        #     os.remove(savefile_name) 
        fs.save(savefile_name, fl_MD)
        objdocs.inserDocs(mdlid,mdl_doc_type,mdlid+'_'+fl_MD.name,str(request.session['uid']))
        return JsonResponse({'msg':'file uploaded Successfully'})
    else:        
        return JsonResponse({'msg':'Invalid File not uploaded'})

def blankadmin(request):
    try:         
        api_url=getAPIURL()+"Is_BackInfo_Exists/"       
        
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= {},headers=header)         
        api_data=response.json() 
        data=api_data['data']
        return render(request, 'blankadmin.html',{'actPage':'RMSE','boolShowMenu':data})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 


def blankvalidationtool(request):
    try:      
        return render(request, 'blankvalidationtool.html')
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 

def downloadImg(request):
    import base64
    from io import BytesIO
    third_party_api_url = getAPIURL()+'downloadIm/'
    header = {
    "Content-Type":"application/json", 
    }
     
    response_user = requests.get(third_party_api_url, headers=header)
    # print("response userlist",response_user.content)
    jsondata = json.loads(response_user.content)
    image_path = os.path.join(BASE_DIR, 'static/media', 'downloaded_image.jpg')
    with open(image_path, "wb") as f:
        f.write((base64.b64decode((jsondata['base64Data']))))

def login(request):
    try:  
        
        return render(request, 'login.html')
    except Exception as e:
        print('login is ',e)
        print('login traceback is ', traceback.print_exc()) 

def logout(request):
    try: 
        import random         
        print("Random integers between 0 and 9: ")
        for i in range(0, 60):
            y = random.uniform(0.5, 0.9)
            print(y)
        third_party_api_url = getAPIURL()+'logout/'
        header = {
        "Content-Type":"application/json",
         'Authorization': 'Token '+request.session['accessToken']
        }
        update_to_save={
            'u_name':request.session['username']
        }
        response_user = requests.post(third_party_api_url,  data= json.dumps(update_to_save),headers=header)
        # print("response userlist",response_user.content)
        jsondata = json.loads(response_user.content)
        # request.session.flush()
        if 'username' in request.session:
            del request.session['username']
            print("Removed username from session")
        else:
            print("Username was not in session")

        return render(request, 'login.html')
    except Exception as e:
        return render(request, 'login.html')
        print('login is ',e)
        print('login traceback is ', traceback.print_exc()) 

def user(request):
    try:       
        #new
        third_party_api_url = getAPIURL()+'addUser/'
        header = {
        "Content-Type":"application/json",
         'Authorization': 'Token '+request.session['accessToken']
        }
        response_user = requests.get(third_party_api_url, headers=header)
        # print("response userlist",response_user.content)
        user_data = json.loads(response_user.content)
        
        # dept_id = user_data['dept_aid']
        for i in user_data:            
            # if i['u_reportto'] != None:
            try:
                third_party_api_url_reportsto = getAPIURL()+'UpdateUser/'+str(i['u_reportto'])
                header = {
                "Content-Type":"application/json",
                 'Authorization': 'Token '+request.session['accessToken']
                }
                response = requests.get(third_party_api_url_reportsto, headers=header)
                print("response reportsto--------------------------",response.content)
                reportsto_data = json.loads(response.content)
                reportsto_u_name = reportsto_data['data']['u_name']
                i['u_reportto_u_name'] = reportsto_u_name
            # else:
            except:
                i['u_reportto_u_name'] = None
            # i['u_reportto_u_name'] =  
        # tableResult = objmaster.getdbUsers()
        # users = tableResult.to_json(orient='index')
        # users = json.loads(users)
        # print("users",users)
        # del tableResult       
        return render(request, 'userlist.html',{ 'actPage':'Add User','users':user_data})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())



def addnewuser(request):
    try: 
        third_party_api_url = getAPIURL()+'addUser/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response_user = requests.get(third_party_api_url, headers=header)
        user_data = json.loads(response_user.content)
        # print("user data",user_data)

        third_party_api_url = getAPIURL()+'UserCategory/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response_cat_data = requests.get(third_party_api_url, headers=header)
        user_category_data = json.loads(response_cat_data.content)
        print("user category data",user_category_data)
        

        third_party_api_url_dept = getAPIURL()+'department/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response_dept= requests.get(third_party_api_url_dept, headers=header)
        dept_data = json.loads(response_dept.content)
        print("dept data",dept_data)

        third_party_api_url = getAPIURL()+'BackupForUserData/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response_bkpfrusr_data = requests.get(third_party_api_url, headers=header)
        # print("response userlist",response_user.content)
        backupfor = json.loads(response_bkpfrusr_data.content) 
       
        IfBackupUser=False
        BackUpFor_User=''
        DisplayBackUp='none'    
        BackUpFor_UID=None
        u_depart_name=None
        api_url=getAPIURL()+"Is_BackInfo_Exists/"   
        
        bank_domain='' 
        header = {
        "Content-Type":"application/json",
	   'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= {},headers=header)         
        api_data=response.json() 
        data=api_data['data']
        bankData=api_data['bankInfo']
        if int(data)>0:
            for i,k in bankData.items(): 
                bank_domain=k['Bank_Domain_Name']  
        return render(request, 'adduser.html',{ 'actPage':'Add User','DisplayBackUp':DisplayBackUp,'backupfor':backupfor,'u_depart_name':u_depart_name,
                                               'utype':user_category_data,'dept':dept_data,'BackUpFor_User':BackUpFor_User,
                                               'IfBackupUser':IfBackupUser,'BackUpFor_UID':BackUpFor_UID,'bank_domain':bank_domain})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc()) 
 

# class addUser(APIView):
#     def post(self, request, format=None):

#         # third_party_api_url = 'http://127.0.0.1:8001/api/addUser/'  # Replace with the third-party API URL
#         third_party_api_url = getAPIURL()+'addUser/'
#         try:
            
#             update_date=datetime.now()
#             updated_by=str(request.session['uid'])
#             uname =request.POST.get('uname', 'False') 
#             user_type =request.POST.get('utype', 'False')  
#             lname=request.POST.get('lname', 'False')   
#             fname=request.POST.get('fname', 'False')     
#             email=request.POST.get('email', 'False')   
#             reportsto=request.POST.get('reportsto', 'False')   
#             dept_aid=request.POST.get('dept_aid', 'False')   
#             activests=request.POST.get('activests', 'False')
#             update_id=request.POST.get('update_id','False') 
#             isBackUp=request.POST.get('isBackup','False')
#             U_AID_BackUpFor=request.POST.get('backUpFor','False')
#             print("isBackUp",isBackUp)
#             print("U_AID_BackUpFor",U_AID_BackUpFor)

#             if update_id != 'False':
#                 third_party_api_url = getAPIURL()+'UpdateUser/'
#                 utype_id=UserCategory.objects.get(uc_aid=user_type)
#                 if reportsto =='null' or reportsto =='':
#                     reportsto=3
#                 if dept_aid == 'null' or dept_aid == "":
#                     dept_aid=3
#                 update_to_save={'u_name':uname,
#                 'u_password':uname,
#                 'uc_aid':utype_id.uc_aid,
#                 'u_fname':fname,
#                 'u_lname':lname,
#                 'u_email':email,
#                 'dept_aid':dept_aid,
#                 'activestatus':activests,
#                 'addedby':updated_by,
#                 'u_reportto':reportsto,
#                 'id':update_id}
#                 header = {
#                 "Content-Type":"application/json",
#                  'Authorization': 'Token '+request.session['accessToken']
#                 }
#                 response = requests.put(third_party_api_url, data= json.dumps(update_to_save),headers=header)
#                 print("response content",response.content,response.status_code)
#                 if response.status_code == 201:
#                     return JsonResponse({'msg': 'User Updated successfully .','isvalid':'true'})
#                 else:
#                     return JsonResponse({'message': 'Failed to create data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#             else:
#                 third_party_api_url = getAPIURL()+'addUser/'
#                 utype_id=UserCategory.objects.get(uc_aid=user_type)
#                 if reportsto =='null' or reportsto =='':
#                     reportsto=None
#                 if dept_aid == 'null' or dept_aid == "":
#                     dept_aid=None
#                 if isBackUp == '1':
#                     BackUpFor = U_AID_BackUpFor
#                 else:
#                     BackUpFor=None
#                 data_to_save={'u_name':uname,
#                               'u_password':uname,
#                 'uc_aid':utype_id.uc_aid,
#                 'u_fname':fname,
#                 'u_lname':lname,
#                 'u_email':email,
#                 'dept_aid':dept_aid,
#                 'activestatus':activests,
#                 'addedby':updated_by,
#                 'u_reportto':reportsto,
#                 'U_AID_BackUpFor':BackUpFor}
#                 print('data_to_save ',data_to_save)
#                 header = {
#                 "Content-Type":"application/json",
#                  'Authorization': 'Token '+request.session['accessToken']
#                 }
#                 response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
#                 print("----------------5")
#                 print("response content",response.content,response.status_code)
#                 if response.status_code == 201:
#                     return JsonResponse({'msg': 'User Created successfully .','isvalid':'true'})
#                 else:
#                     return JsonResponse({'msg': 'Failed to create data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         except requests.exceptions.RequestException as e:
#             return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def addUser(request):
    try:
        update_date=datetime.now()
        updated_by=request.session['uid']
        uname =request.GET.get('uname', 'False') 
        utype =request.GET.get('utype', 'False')  
        lname=request.GET.get('lname', 'False')   
        fname=request.GET.get('fname', 'False')     
        email=request.GET.get('email', 'False')   
        reportsto=request.GET.get('reportsto','False')   
        dept_aid=request.GET.get('dept_aid', 'False')   
        activests=request.GET.get('activests', 'False')
        update_id=request.GET.get('update_id')
        isBackUp=request.GET.get('isBackup')
        U_AID_BackUpFor=request.GET.get('backUpFor')
        AID_BackUp=request.GET.get('backUp')
        StartDate=request.GET.get('StartDate')
        EndDate=request.GET.get('EndDate')

         
        utype_id=UserCategory.objects.get(uc_aid=int(utype))
        print("utype_id",utype_id)
        if update_id:
            if reportsto =='null' or reportsto =='':
                reportsto=None
            print("update",update_id)
            user_obj=Users.objects.get(u_aid=update_id)
            if dept_aid == 'null' or dept_aid == "":
                dept_aid=None
            user_obj.u_name=uname
            user_obj.uc_aid=utype_id
            user_obj.u_fname=fname
            user_obj.u_lname=lname
            user_obj.u_email=email
            user_obj.dept_aid=dept_aid
            user_obj.activestatus=activests
            user_obj.updatedby=updated_by
            user_obj.updatedate=update_date
            user_obj.u_reportto=reportsto
            if(isBackUp=="1"):
                user_obj.U_AID_BackUpFor=U_AID_BackUpFor
            user_obj.save()
            return JsonResponse({"isvalid":"update"})
        else: 
            strQ="INSERT INTO Users (U_Name,U_Password  ,U_Email ,U_FName ,U_LName  ,U_ProfilePic  ,UC_AID  ,U_Description ,ActiveStatus,AddedBy ,AddDate,Dept_AID,U_reportto"
            if(isBackUp=="1"):
                strQ+=",U_AID_BackUpFor,BackUp_AID,StartDate,EndDate"
            strQ+=") "
            strQ += " VALUES  ('"+ uname+"','"+ uname+"','"+ email+"','"+ fname+"','"+ lname+"',null,'"+ utype+"',null,'"+ activests+"', '"+str(request.session['uid'])+"',getdate(),"+ dept_aid +","+ reportsto +""
            if(isBackUp=="1"):
                strQ+=",'"+ U_AID_BackUpFor+"','"+ AID_BackUp+"','"+ StartDate+"','"+ EndDate+"'"
            strQ+=")" 
            objdbops.insertRow(strQ)
            # objdbops.insertRow(" update users set U_Password= U_Name where u_name='"+ uname+"'")
            # user_obj=Users(u_name=uname,u_password=uname,u_email=email,)
            return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})


def userAddedBy(request):
    try:        
        tableResult = objmaster.getdbUsersAddedBy(str(request.session['uid']))
        users = tableResult.to_json(orient='index')
        users = json.loads(users)
        del tableResult       
        return render(request, 'deptuserlist.html',{ 'actPage':'Add User','users':users})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc()) 


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def validateUser(request):
    print("login api---------------------1",) 
    try: 
        api_url=getAPIURL()
        uname =request.GET.get('u_name', 'False') 
        pwd =request.GET.get('u_password', 'False')  
        
        utype=''
        my_data={'u_name':uname,'u_password':pwd}      

        api_url =getAPIURL()+ 'login/'
               
        try:
            response = requests.post(api_url,json=my_data, 
                        headers={'content-type': 'application/json'}) 
            request.session['vt_mdl']='M090100'
            if response.status_code == status.HTTP_200_OK:
                data = response.json() 
                isvalid='true'
                
                #if(dffilter["U_AID_BackUpFor"].values[0]!=None):               
                #    dffilter=objuser.getUserOrg(uname)

                user_obj = Users.objects.get(u_name=data['u_name'])
                uid=user_obj.u_aid
                utype=user_obj.uc_aid.uc_aid
                dept_id=user_obj.dept_aid
                uc_aid=user_obj.uc_aid.uc_aid
                uc_level=user_obj.uc_aid.uc_level
                print('utype',utype,' user_obj ',user_obj)

                request.session['username'] = uname
                request.session['utype']=utype
                request.session['dept']=dept_id
                request.session['accessToken']=data['token']
                if dept_id == None:
                    dept_id=0

                request.session['uid']=uid
                request.session['ucaid']=uc_aid
                request.session['ulvl']=uc_level
                request.session['ufirstname']=user_obj.u_fname
                request.session['ulastname']=user_obj.u_lname
                request.session['uemail']=user_obj.u_email
                request.session['profileimg']="/static/phoenix-v1.8.0/public/assets/img/team/avatar-rounded.png"
                data['isvalid']=isvalid
                data['utype']=utype
                data['token']=''
                api_url=getAPIURL()+"checkPendingTasks/"       
                data_to_save={ 
                    'uid':request.session['uid'], 
                    } 
                header = {
                "Content-Type":"application/json",
                'Authorization': 'Token '+request.session['accessToken']
                }
                response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)         
                api_data=response.json()  
                print("api_data",api_data)
                data['pending_tasks']=api_data['data']
                request.session['pending_tasks']=api_data['data']
                return Response(data, template_name='login.html')
            else:
                data = response.json()
                return Response(data, template_name='login.html')
        except Exception as e:
            print("check error is",e)
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc())

 
def dashboard_prope(request):
    try:  
        objreg=Register()
        request.session['canAdd']="0"
        #Get_User_Deatils 
        uc = request.session['utype']
        dept = request.session['dept']
        api_url = getAPIURL()+'Get_User_Deatils/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uc':uc,
            'dept':dept 
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()     
        dttbl=  pd.DataFrame.from_dict(api_data['ucdata'], orient='index') 
        
        if dttbl.empty == False:
            request.session['li_mrm']=dttbl[dttbl['r_label'] == 'Model Risk Management'].values[0][2]
            request.session['li_qv']=dttbl[dttbl['r_label'] =='Dashboard'].values[0][2] 
            request.session['li_modinv']=dttbl[dttbl['r_label'] =='Model Inventory'].values[0][2] 
            request.session['li_modtasks']=dttbl[dttbl['r_label'] =='Tasks'].values[0][2]  
            request.session['li_adduser']=dttbl[dttbl['r_label'] =='Dept Head'].values[0][2] 
            request.session['li_task']=dttbl[dttbl['r_label'] =='Tasks'].values[0][2]
            request.session['task_registration']=dttbl[dttbl['r_label'] =='Tasks'].values[0][2] 
            request.session['li_issuesReg']= dttbl[dttbl['r_label'] =='Issues'].values[0][2]  
            request.session['li_taskApprv']='block' 
            request.session['li_taskComplete']='block'
            request.session['li_issueComplete']='block'
            request.session['li_issueApprv']='block'
            request.session['li_icqqtn']=dttbl[dttbl['r_label'] =='ICQ'].values[0][2]      
            request.session['li_perfmntr']=dttbl[dttbl['r_label'] =='Performance Monitoring'].values[0][2]   
            if dttbl[dttbl['r_label'] =='Model Inventory'].values[0][3] == "rw":
                request.session['canAdd']="1" 

            if(str(objmaster.checkMRMHead(str(request.session['uid']))))=="1" or (str(objmaster.checkMRMMgr(str(request.session['uid']))))=="1":
                request.session['li_icqqtnfinal']='block'
                request.session['li_modval']='block'
                request.session['li_icqqtn']='none' 
            else:
                request.session['li_icqqtnfinal']='none'
                request.session['li_modval']='none' 

            if(str(objmaster.checkMRMHead(str(request.session['uid']))))=="1":
                 request.session['is_mrm']='Yes'
            else: 
                request.session['is_mrm']='No'

        del dttbl
        
        api_url=getAPIURL()+"dashboard/"
        
        data_to_save={'utype':request.session['utype'],
            'dept':request.session['dept'],
            'uid':request.session['uid'],
            'ulvl':request.session['ulvl'],
            'is_mrm':request.session['is_mrm'],
            'type':'Qtr',
            'issue_from_dt':'',
            'issue_to_dt':''
            } 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json() 
        if(str(objmaster.isAutherized(request.session['ucaid'],"Dashboard")) =="0"): 
            return render(request, 'blank.html',{'actPage':'RMSE'}) 
        modelinfo=api_data['modelinfo']#objreg.getModelListByUSerid(request.session['uid'],str(request.session['ulvl']),'0')
        # modelriskcnt=api_data['modelriskcnt']#objreg.getModelRiskCntByUserid(request.session['uid'],str(request.session['ulvl'])) 
        # modelsrccnt=api_data['modelsrccnt']#objreg.getModelSrcCntByUserid('0',request.session['uid'])
       
        taskList=api_data['taskLst']#objreg.getTaskListByUSerid(request.session['uid'])
        issueList=api_data['issueList']#objreg.getIssueListByUserId(request.session['uid'])
        icqratings=api_data['icqratings']#objreg.isICQPublished() 
        if(icqratings=='-'):
            icq_exp="Experimentation"
            icqratings="0"
        else:
            icq_exp="Program Score"
        srcCnt= api_data['srcCnt']

        # colorArr=['info', 'info-300','warning-300','danger-300','success-300','primary']
        colorArr=['#0dcaf0', '#fd7e14','#ffc107','#dc3545','#198754','#0d6efd']
         
        cnt=api_data['mdlRiskCnt']
        toolCnt=api_data['toolCnt']
        modeltypes=api_data['modeltypes']
        issuesByQtrOrMonth= api_data['issuesByQtrOrMonth']
        findingsByElements=api_data['findingsByElements']
        findingsCntByCategory=api_data['findingsCntByCategory']
        #new code 
        # end_date = datetime.now()
        # start_date = end_date - timedelta(days=7)
        # last_7_days_records = ActivityTrail.objects.filter(added_on__range = (start_date, end_date)).distinct().order_by('-added_on')
        # # lst = activityinfo(last_7_days_records)
        # latest = last_7_days_records.values('refference_id').distinct()
        # print("latest",latest)
        lst = []
        irow=1 
        latest=api_data['activityData']
        for key,activity_obj in latest.items(): 
            # max_record = ActivityTrail.objects.filter(refference_id = activity_obj['refference_id']).last()
            dict={}
            activity_trigger = latest[key]['activity_trigger']
            refference_id = latest[key]['refference_id']
            
            
            dict['activity_trigger'] = activity_trigger
            dict['refference_id'] = refference_id
            dict['user'] = latest[key]['usernm'] 
            dict['date'] = latest[key]['add_dt']
            dict['time'] = latest[key]['add_time']
            dict['activity_details'] =latest[key]['activity_details']
            if irow== len(latest):
                dict['is_last']='Yes'
            else:
                dict['is_last']='No'
                irow+=1
            lst.append(dict)  
        return render(request, 'dashboard_Prope.html',{'icqratings':icqratings,'icq_exp':icq_exp,'modelinfo':modelinfo,'srcCnt':srcCnt,
                                                 'colorArr':colorArr,'issueCnt':len(issueList),'issueList':issueList,'issuePriority':issuesByQtrOrMonth['data'],'chartSeries':issuesByQtrOrMonth['series'],
                                                 'taskCnt':api_data['taskCnt'],'taskLst':taskList,'arrvalrating':api_data['arrvalrating'],
                                                 'toolCnt':toolCnt ,'findingsByElements':findingsByElements,
                                                 'modelttl':str(len(modelinfo)),'mdlRiskCnt':cnt,'findingsCntByCategory':findingsCntByCategory,
                                                 'modeltypes':modeltypes, 'actPage':'Quick View','activity_lst':lst})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
        error_saving(request,e)

# def dashboard(request):
#     try:  
#         objreg=Register()
#         request.session['canAdd']="0"
#         ps=request.GET.get('ps','')
#         #Get_User_Deatils 
#         uc = request.session['utype']
#         dept = request.session['dept']
#         api_url = getAPIURL()+'Get_User_Deatils/' 
#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }       
#         data_params={
#             'uc':uc,
#             'dept':dept 
#         }
#         response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
#         api_data=response.json()     
#         dttbl=  pd.DataFrame.from_dict(api_data['ucdata'], orient='index') 
        
#         if dttbl.empty == False:
#             request.session['li_mrm']=dttbl[dttbl['r_label'] == 'Model Risk Management'].values[0][2]
#             request.session['li_qv']=dttbl[dttbl['r_label'] =='Dashboard'].values[0][2] 
#             request.session['li_modinv']=dttbl[dttbl['r_label'] =='Model Inventory'].values[0][2] 
#             request.session['li_modtasks']=dttbl[dttbl['r_label'] =='Tasks'].values[0][2]  
#             request.session['li_adduser']=dttbl[dttbl['r_label'] =='Dept Head'].values[0][2] 
#             request.session['li_task']=dttbl[dttbl['r_label'] =='Tasks'].values[0][2]
#             request.session['task_registration']=dttbl[dttbl['r_label'] =='Tasks'].values[0][2] 
#             request.session['li_issuesReg']= dttbl[dttbl['r_label'] =='Issues'].values[0][2]  
#             request.session['li_taskApprv']='block' 
#             request.session['li_taskComplete']='block'
#             request.session['li_issueComplete']='block'
#             request.session['li_issueApprv']='block'
#             request.session['li_icqqtn']=dttbl[dttbl['r_label'] =='ICQ'].values[0][2]   
#             request.session['li_perfmntr']=dttbl[dttbl['r_label'] =='Performance Monitoring'].values[0][2]   
#             if dttbl[dttbl['r_label'] =='Model Inventory'].values[0][3] == "rw":
#                 request.session['canAdd']="1" 

#             if(str(objmaster.checkMRMHead(str(request.session['uid']))))=="1" or (str(objmaster.checkMRMMgr(str(request.session['uid']))))=="1" or (str(objmaster.checkMRMUser(str(request.session['uid']))))=="1":
#                 request.session['li_icqqtnfinal']='block'
#                 request.session['li_modval']='block'
#                 request.session['li_icqqtn']='none' 
#                 request.session['is_mrm_user']='Yes'
#             else:
#                 request.session['li_icqqtnfinal']='none'
#                 request.session['li_modval']='none' 
#                 request.session['is_mrm_user']='No'
#             if(str(objmaster.checkMRMHead(str(request.session['uid']))))=="1":
#                  request.session['is_mrm']='Yes'
#             else: 
#                 request.session['is_mrm']='No'

#         del dttbl
        
#         api_url=getAPIURL()+"dashboard/"
        
#         data_to_save={'utype':request.session['utype'],
#             'dept':request.session['dept'],
#             'uid':request.session['uid'],
#             'ulvl':request.session['ulvl'],
#             'is_mrm':request.session['is_mrm'],
#             'type':'Qtr',
#             'issue_from_dt':'',
#             'issue_to_dt':''
#             } 
#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }
#         response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
         
#         api_data=response.json() 
#         if(str(objmaster.isAutherized(request.session['ucaid'],"Dashboard")) =="0"): 
#             return render(request, 'blank.html',{'actPage':'RMSE'}) 
#         modelinfo=api_data['modelinfo']#objreg.getModelListByUSerid(request.session['uid'],str(request.session['ulvl']),'0')
#         # modelriskcnt=api_data['modelriskcnt']#objreg.getModelRiskCntByUserid(request.session['uid'],str(request.session['ulvl'])) 
#         # modelsrccnt=api_data['modelsrccnt']#objreg.getModelSrcCntByUserid('0',request.session['uid'])
       
#         taskList=api_data['taskLst']#objreg.getTaskListByUSerid(request.session['uid'])
#         issueList=api_data['issueList']#objreg.getIssueListByUserId(request.session['uid'])
#         icqratings=api_data['icqratings']#objreg.isICQPublished() 
#         if(icqratings=='-'):
#             icq_exp="Experimentation"
#             icqratings="0"
#         else:
#             icq_exp="Program Score"
#         srcCnt= api_data['srcCnt']

#         # colorArr=['info', 'info-300','warning-300','danger-300','success-300','primary']
#         colorArr=['#0dcaf0', '#fd7e14','#ffc107','#dc3545','#198754','#0d6efd']
         
#         cnt=api_data['mdlRiskCnt']
#         toolCnt=api_data['toolCnt']
#         modeltypes=api_data['modeltypes']
#         issuesByQtrOrMonth= api_data['issuesByQtrOrMonth']
#         findingsByElements=api_data['findingsByElements']
#         findingsCntByCategory=api_data['findingsCntByCategory']
#         #new code 
#         # end_date = datetime.now()
#         # start_date = end_date - timedelta(days=7)
#         # last_7_days_records = ActivityTrail.objects.filter(added_on__range = (start_date, end_date)).distinct().order_by('-added_on')
#         # # lst = activityinfo(last_7_days_records)
#         # latest = last_7_days_records.values('refference_id').distinct()
#         # print("latest",latest)
#         lst = []
#         irow=1 
#         latest=api_data['activityData']
#         for key,activity_obj in latest.items(): 
#             # max_record = ActivityTrail.objects.filter(refference_id = activity_obj['refference_id']).last()
#             dict={}
#             activity_trigger = latest[key]['activity_trigger']
#             refference_id = latest[key]['refference_id']
            
            
#             dict['activity_trigger'] = activity_trigger
#             dict['refference_id'] = refference_id
#             dict['user'] = latest[key]['usernm'] 
#             dict['date'] = latest[key]['add_dt']
#             dict['time'] = latest[key]['add_time']
#             dict['activity_details'] =latest[key]['activity_details']
#             if irow== len(latest):
#                 dict['is_last']='Yes'
#             else:
#                 dict['is_last']='No'
#                 irow+=1
#             lst.append(dict)  
#         mdl_cat=api_data['mdl_cat'] 
#         request.session['overdueTasks']=api_data['overdueTasks'] 
#         request.session['overdueIssues']=api_data['overdueIssues']
#         return render(request, 'dashboard_icon.html',{'icqratings':icqratings,'icq_exp':icq_exp,'modelinfo':modelinfo,'srcCnt':srcCnt,
#                                                  'colorArr':colorArr,'issueCnt':len(issueList),'issueList':issueList,'issuePriority':issuesByQtrOrMonth['data'],'chartSeries':issuesByQtrOrMonth['series'],
#                                                  'taskCnt':api_data['taskCnt'],'taskLst':taskList,'arrvalrating':api_data['arrvalrating'],
#                                                  'toolCnt':toolCnt ,'findingsByElements':findingsByElements,
#                                                  'modelttl':str(len(modelinfo)),'mdlRiskCnt':cnt,'findingsCntByCategory':findingsCntByCategory,
#                                                  'modeltypes':modeltypes, 'actPage':'Quick View','activity_lst':lst,'mdl_cat':mdl_cat,'showOverdueModal':ps})
#     except Exception as e:
#         print('setuppycaret is ',e)
#         print('setuppycaret traceback is ', traceback.print_exc()) 
#         error_saving(request,e)


# def issueLst(request):
#     try: 
#         print('Token ',request.session['accessToken'])
#         objreg=Register()
#         dttbl=objreg.getUserDeatils(request.session['utype'],request.session['dept']) 
#         if dttbl.empty == False:
#             request.session['li_mrm']=dttbl[dttbl['r_label'] == 'Model Risk Management'].values[0][2]
#             request.session['li_qv']=dttbl[dttbl['r_label'] =='Dashboard'].values[0][2] 
#             request.session['li_modinv']=dttbl[dttbl['r_label'] =='Model Inventory'].values[0][2] 
#             request.session['li_modtasks']=dttbl[dttbl['r_label'] =='Tasks'].values[0][2]  
#             request.session['li_adduser']=dttbl[dttbl['r_label'] =='Dept Head'].values[0][2] 
#             request.session['li_task']=dttbl[dttbl['r_label'] =='Tasks'].values[0][2]
#             request.session['task_registration']='block'
#             request.session['li_issuesReg']='block'
#             request.session['li_taskApprv']='block' 
#             request.session['li_taskComplete']='block'
#             request.session['li_issueComplete']='block'
#             request.session['li_issueApprv']='block'
#             request.session['li_icqqtn']='block' 
#             if(str(objmaster.checkMRMHead(str(request.session['uid']))))=="1" or (str(objmaster.checkMRMMgr(str(request.session['uid']))))=="1":
#                 request.session['li_icqqtnfinal']='block'
#                 request.session['li_modval']='block'
#                 request.session['li_icqqtn']='none' 
#             else:
#                 request.session['li_icqqtnfinal']='none'
#                 request.session['li_modval']='none' 

#             if(str(objmaster.checkMRMHead(str(request.session['uid']))))=="1":
#                  request.session['is_mrm']='Yes'
#             else: 
#                 request.session['is_mrm']='No'

#         del dttbl
        
#         api_url=getAPIURL()+"FiterIssue/"
#         print(request.GET['chartnm'])
#         data_to_save={'utype':request.session['utype'],
#             'dept':request.session['dept'],
#             'uid':request.session['uid'],
#             'ulvl':request.session['ulvl'],
#             'is_mrm':request.session['is_mrm'],
#             'type':request.GET['ty'],
#             'priority':request.GET['chartnm'],
#             'colval':request.GET['colnm']
#             } 
#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }
#         response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
         
#         api_data=response.json() 
#         if(str(objmaster.isAutherized(request.session['ucaid'],"Dashboard")) =="0"): 
#             return render(request, 'blank.html',{'actPage':'RMSE'})  
#         issueList=api_data['issueList'] 
         
#         return render(request, 'issueLst.html',{  'issueCnt':len(issueList),'issueList':issueList})
#     except Exception as e:
#         print('setuppycaret is ',e)
#         print('setuppycaret traceback is ', traceback.print_exc()) 
#         error_saving(request,e)



# def activitytrail(request):
#     try: 
#         if request.method  == 'GET':
#             refer_id=request.GET.get('selectSection','')
#         else:
#             refer_id=request.POST.get('selectSection','')
#         activityobj = ActivityTrail.objects.filter(refference_id = refer_id).order_by('-added_on')  
#         activity_lst = activityinfo(activityobj)

#         mdl_id = ActivityTrail.objects.values('refference_id').distinct()
#         mdlid_lst = []
#         for val in mdl_id:
#             mdlid_lst.append(val['refference_id'])

#         return render(request, 'activitytrail.html',{'actPage':'Activity Trail','activity_lst':activity_lst,'mdlid_lst':mdlid_lst,'refer_id':refer_id})
#     except Exception as e:
#         print('adduser is ',e)
#         print('adduser traceback is ', traceback.print_exc())

# def activityinfo(record):
#     lst = []
#     irow=1
#     for activity_obj in record: 
#         dict={}
#         activity_trigger = activity_obj.activity_trigger
#         refference_id = activity_obj.refference_id
#         addon = activity_obj.added_on
#         # print('addon ',addon)
#         # addon = datetime.strptime(str(addon), '%y-%m-%d %I:%M %p')

#         x = str(addon).split(" ") 
#         userobj = Users.objects.get(u_aid = activity_obj.addedby)
#         user = userobj.u_name
#         f_name = userobj.u_fname
#         f_n = f_name[:1].capitalize()
#         l_name = userobj.u_lname
#         l_n = l_name[:1].capitalize()
#         dict['activity_trigger'] = activity_trigger
#         dict['refference_id'] = refference_id
#         dict['user'] = user
#         dict['f_name'] = f_n
#         dict['l_name'] = l_n
#         dict['date'] = addon.strftime('%m/%d/%Y')
#         dict['time'] = addon.strftime('%I:%M %p') 
#         dict['activity_details'] =activity_obj.activity_details
#         if irow== len(record):
#             dict['is_last']='Yes'
#         else:
#             dict['is_last']='No'
#             irow+=1
#         lst.append(dict)
#     return lst   

def masterTbls(request):
    try: 
        pagettl='RMSE'
        page =request.GET.get('page', 'False')      
        typeobj=None  
        if page=="1":
            pagettl='Add Function'
        elif page=="2":
            pagettl='Add Model Source'
        elif page=="3":
            pagettl='Add Model Type'
        elif page=="4":
            pagettl='Add Products Addressed'
            typeobj = ModelCategory.objects.all()
        elif page=="5":
            pagettl='Add Usage Frequency'
        elif page=="6":
            pagettl='Add Model Risk'
        elif page=="7":
            pagettl='Add Intrinsic Risk'
        elif page=="8":
            pagettl='Add Reliance'
        elif page=="9":
            pagettl='Add Materiality'
        elif page=="10":
            pagettl='Add Upstream Model'
        elif page=="11":
            pagettl='Add Downstream Model'
        elif page=="12":
            pagettl='Add Monitoring Frequency'

        return render(request, 'addmastertbl.html',{'Category':typeobj,'actPage':pagettl,'tbl':page,'tblData':objmaster.getMasterTblData(str(page))})
    except Exception as e:
        print('masterTbls is ',e)
        print('masterTbls traceback is ', traceback.print_exc()) 

def showmasterTbls(request):
    try: 
        pagettl='RMSE'
        page =request.GET.get('page', 'False')        
        if page=="1":
            pagettl='Add Function'
        elif page=="2":
            pagettl='Add Model Source'
        elif page=="3":
            pagettl='Add Model Type'
        elif page=="4":
            pagettl='Add Products Addressed'
        elif page=="5":
            pagettl='Add Usage Frequency'
        elif page=="6":
            pagettl='Add Model Risk'
        elif page=="7":
            pagettl='Add Intrinsic Risk'
        elif page=="8":
            pagettl='Add Reliance'
        elif page=="9":
            pagettl='Add Materiality'
        elif page=="10":
            pagettl='Add Upstream Model'
        elif page=="11":
            pagettl='Add Downstream Model'
        elif page=="12":
            pagettl='Add Monitoring Frequency'

        return render(request, 'showmasterdata.html',{'actPage':pagettl,'tbl':page,'tblData':objmaster.getMasterTblData(str(page))})
    except Exception as e:
        print('masterTbls is ',e)
        print('masterTbls traceback is ', traceback.print_exc()) 

def editmasterTbls(request,id,page):
    try: 
        pagettl='RMSE'
                
        if page=="1":
            pagettl='Edit Function'
        elif page=="2":
            pagettl='Edit Model Source'
        elif page=="3":
            pagettl='Edit Model Type'
        elif page=="4":
            pagettl='Edit Products Addressed'
        elif page=="5":
            pagettl='Edit Usage Frequency'
        elif page=="6":
            pagettl='Edit Model Risk'
        elif page=="7":
            pagettl='Edit Intrinsic Risk'
        elif page=="8":
            pagettl='Edit Reliance'
        elif page=="9":
            pagettl='Edit Materiality'
        elif page=="10":
            pagettl='Edit Upstream Model'
        elif page=="11":
            pagettl='Edit Downstream Model'
        elif page=="12":
            pagettl='Edit Monitoring Frequency'

        print("page",str(page))
        tbldata=objmaster.getMasterTblData(str(page))
        print('tbldata ',tbldata)
        for i in tbldata:
           print('id value ',str(tbldata[i]["AID"]))
           if str(tbldata[i]["AID"]) == str(id):
               tbldata=tbldata[i]
               print('tbldata ',tbldata)
               break

        return render(request, 'editmastertbl.html',{'actPage':pagettl,'tbl':page,'tblData':tbldata})
    except Exception as e:
        print('masterTbls is ',e)
        print('masterTbls traceback is ', traceback.print_exc()) 
        

def getMasterTblbyId(request):
    try:
        page =request.GET.get('tbl', 'False')
        val =request.GET.get('val', 'False')
        a_list =objmaster.getMasterTblData(str(page))
        print(a_list)
        # filtered_list = [
        #     dictionary for dictionary in a_list
        #     if dictionary['AID'] ==(val)
        # ]
        return JsonResponse({'tblata':a_list})
         
    except Exception as e:
        print('getMasterTblbyId is ',e)
        print('getMasterTblbyId traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})

def addMasterOpts(request):
    try: 
        print("addMasterOpts")
        opt =request.GET.get('opt', 'False')  
        desc=request.GET.get('desc', 'False')   
        tbl=request.GET.get('tbl', 'False')     
        selectedOPt=request.GET.get('selectedOPt', 'False')     
        activests=request.GET.get('activests', 'False')
        category=request.GET.get('cat', 'False')
        print("category",category)
        print('selectedOPt is ',selectedOPt)
        print('activests is ',activests)
        print('tbl ',tbl)

        if selectedOPt =='':
            objmaster.insertFunctionOption(opt,desc,tbl,str(activests),str(request.session['uid']),category)
        else:
            objmaster.updateFunctionOption(str(selectedOPt),opt,desc,tbl,str(activests),str(request.session['uid']))    
        return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})


def projectsDetails(request):
    try:
        ty =request.GET.get('ty', 'False') 
        colnm =request.GET.get('colnm', 'False') 
        chartnm =request.GET.get('chartnm', 'False') 
        canAdd=request.session['canAdd']
        Authorization(request,request.session['ucaid'],'Model Inventory')
        api_url=getAPIURL()+"projectsDetails/"       
        data_to_save={ 
            'uid':request.session['uid'],
            'filterType':ty,
            'filterColumn':chartnm,
            'filterValue':colnm,
            'istool':'0'} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)         
        api_data=response.json() 
        modelinfo=api_data['modelinfo']#objreg.getModelByFilter(request.session['uid'],ty,chartnm,colnm,'0')
        if(str(objmaster.checkMRMHead(str(request.session['uid']))))=="1":
            return render(request, 'projectlist_mrmhead_1.html',{'modelinfo':modelinfo,'canAdd':canAdd, 'actPage':'Model Inventory'})
        else:
            return render(request, 'projectlist.html',{'modelinfo':modelinfo,'canAdd':canAdd, 'actPage':'Model Inventory'})
            
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 

# def getModelsByValFindingsPriority(request):
#     try:
#         ty =request.GET.get('ty', 'False') 
#         colnm =request.GET.get('colnm', 'False') 
#         chartnm =request.GET.get('chartnm', 'False') 
#         valPriority =request.GET.get('valPriority', 'False') 
#         canAdd=request.session['canAdd']
#         element_txt =request.GET.get('element_txt', 'False') 
#         category_txt=request.GET.get('category_txt', 'False') 
#         Authorization(request,request.session['ucaid'],'Model Inventory')
#         api_url=getAPIURL()+"modelsByValPriority/"       
#         data_to_save={ 
#             'uid':request.session['uid'],
#             'filterType':ty,
#             'filterColumn':chartnm,
#             'filterValue':colnm,
#             'istool':'0',
#             'valPriority':valPriority,
#             'element_txt':element_txt,
#             'category_txt':category_txt,
#             } 
#         header = {
#         "Content-Type":"application/json",
# 	    'Authorization': 'Token '+request.session['accessToken']
#         }
#         response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)         
#         api_data=response.json() 
#         modelinfo=api_data['modelinfo']#objreg.getModelByFilter(request.session['uid'],ty,chartnm,colnm,'0')
#         return render(request, 'modelsByValPriority.html',{'modelinfo':modelinfo,'canAdd':canAdd, 'actPage':'Model Inventory'})
            
#     except Exception as e:
#         print('setuppycaret is ',e)
#         print('setuppycaret traceback is ', traceback.print_exc()) 

# def getMdlDetailsById(request):
#     try:
#         mdl_id =request.GET.get('mdlId', 'False') 
#         api_url=getAPIURL()+"getMdlDetailsById/"       
#         data_to_save={
#             'mdl_id':mdl_id} 
#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }
#         response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
#         # 'pdfFile': "/static/media/ValidationReport_"+request.session['vt_mdl']+".pdf", 
#         api_data=response.json() 

#         Owner=api_data['Owner']

#         Developer=api_data['Developer']#objMdlRelvPern.getRelevantPersonal(mdl_id,'Developer')

#         User=api_data['User']#objMdlRelvPern.getRelevantPersonal(mdl_id,'User')

#         PrdnSupport=api_data['PrdnSupport']#objMdlRelvPern.getRelevantPersonal(mdl_id,'PrdnSupport')
 
#         dependencies =api_data['dependencies']#objdependencies.getMdlDependencies(mdl_id) 
#         isvrpublished=api_data['isvrpublished'] 
#         PerformMon=objreg.getPerfomanceMonitor(mdl_id)
#         print(str(api_data['mdldata']["0"]['AddedBy']) ,',', str(request.session['uid']))
#         is_owner='No'
#         if str(api_data['mdldata']["0"]['AddedBy'])== str(request.session['uid']):
#             is_owner='Yes'
#         return JsonResponse({'istaken':'true','dependencies':dependencies,'PerformMon':PerformMon,'Owner':Owner,'is_owner':is_owner,
#                              'Developer':Developer,'User':User,'PrdnSupport':PrdnSupport,'mdldata':api_data['mdldata'],'isvrpublished':isvrpublished})
#     except Exception as e:
#         print('getMdlDetails is ',e)
#         print('getMdlDetails traceback is ', traceback.print_exc()) 

def test(request):
    try:
        return render(request, 'calendar.html',{ 'actPage':'Add Model'})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 


def getDocs(mdlid,mdl_doc_type,request):
    api_url=getAPIURL()+"GetDocsNameAPI/"       
    data_to_save={
        'mdl_id':mdlid,
        'mdl_doc_type':mdl_doc_type
        } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
    # 'pdfFile': "/static/media/ValidationReport_"+request.session['vt_mdl']+".pdf", 
    api_data=response.json() 
    print("api_data docs--------------------",api_data,str(len(api_data)))
    if len(api_data)>0:
        return api_data[0]
    else:
        return ""


# def addmodel(request):
#     try:   
#         mdl_id=''
#         mrm_head=objmaster.getMRMHead()
#         # if(str(objmaster.isAutherized(request.session['ucaid'],'4')) =="0"):
#         #     print('not autherized')
#         #     return render(request, 'blank.html',{'actPage':'RMSE'}) 
#         if request.method == 'POST':   
#             rbisnewupdate = request.POST['rbisnewupdate'] 
#             ddlFunction = request.POST['ddlFunction'] 
#             txtMdlId =request.POST['txtMdlId']
#             MdlVersion =request.POST['hdnMdlVersion'] 
#             mdlCategory=request.POST['ddlCategory']
#             ddlmdl_sub_category=request.POST['ddlmdl_sub_category']
#             # ddlModelId
#             mdlid= request.POST['mdlid']  
#             txtPrdDt = request.POST['txtPrdDt'] 
#             txtPrmName = request.POST['txtPrmName'] 
#             txtSecName = request.POST['txtSecName'] 
#             ddlSource = request.POST['ddlSource'] 
#             ddlType = request.POST.get('ddlType','')
#             txtMdlAbsct = request.POST['txtMdlAbsct'] 
#             txtMdlObj = request.POST['txtMdlObj'] 
#             txtMdlAppl = request.POST['txtMdlAppl'] 
#             txtMdlRiskAnls = request.POST['txtMdlRiskAnls'] 
#             ddlPrctAddr = request.POST.get('ddlPrctAddr','')
#             ddlUsgFreq = request.POST['ddlUsgFreq'] 
#             txtMdlRisks = request.POST['hdnMdlRisks'] 
#             ddlIntrRisk = request.POST['hdnIntrRisk'] 
#             ddlReliance = request.POST['hdnReliance'] 
#             ddlMateriality = request.POST['hdnMateriality'] 
#             txtRiskMtgn = request.POST['txtRiskMtgn'] 
#             txtFairLndg = request.POST['txtFairLndg'] 
#             ddlOwner =  request.POST.getlist('ddlOwner')
#             ddlDeveloper = request.POST.getlist('ddlDeveloper')  
#             ddlUser = request.POST.getlist('ddlUser')    
#             txtValidator = request.POST['txtValidator'] 
#             ddlPrdnSupp = request.POST.getlist('ddlPrdnSupp')   
#             ddlUpstrmMdl = request.POST['ddlUpstrmMdl'] 
#             ddlDwstrmMdl = request.POST['ddlDwstrmMdl'] 
#             txtApproach = '' #request.POST['txtApproach'] 
#             ddlMonrFreq ='' # request.POST['ddlMonrFreq'] 
#             txtTgrEvt = '' #request.POST['txtTgrEvt'] 
#             txtLstTgrDt = '' #request.POST['txtLstTgrDt'] 
#             txtLstTgrMtgnDt = '' #request.POST['txtLstTgrMtgnDt'] 
#             txtTgrEvtMtgn ='' # request.POST['txtTgrEvtMtgn'] 
#             txtMonrMtrcs=''#request.POST['txtMonrMtrcs'] 
#             if str(rbisnewupdate)=="0": 
#                 mdlverInfo=MdlVersion.split('-') 
#                 objoverview=MdlOverviewCls(txtMdlId,mdlCategory,ddlmdl_sub_category,mdlverInfo[0],mdlverInfo[1],mdlverInfo[2],rbisnewupdate,'0',request.session['dept']
#                                         ,ddlFunction,txtPrmName.replace("'","''"),txtSecName.replace("'","''"),ddlSource,ddlType,txtMdlAbsct.replace("'","''"),txtMdlObj.replace("'","''")
#                                         ,txtMdlAppl.replace("'","''"),txtMdlRiskAnls.replace("'","''"),ddlPrctAddr,ddlUsgFreq,request.session['uid'],txtPrdDt)
#             else:
#                 objoverview=MdlOverviewCls(txtMdlId,mdlCategory,ddlmdl_sub_category,'1','0','0',rbisnewupdate,'0',request.session['dept']
#                                         ,ddlFunction,txtPrmName.replace("'","''"),txtSecName.replace("'","''"),ddlSource,ddlType,txtMdlAbsct.replace("'","''"),txtMdlObj.replace("'","''")
#                                         ,txtMdlAppl.replace("'","''"),txtMdlRiskAnls.replace("'","''"),ddlPrctAddr,ddlUsgFreq,request.session['uid'],txtPrdDt)
#             mdl_id=objoverview.insertMdlOverview()
#             MdlOverview.objects.filter(mdl_id =mdl_id).update(is_submit=1)
 
#             objModelRisks=ModelRisks(mdl_id,txtMdlRisks,ddlIntrRisk,ddlReliance,ddlMateriality,txtRiskMtgn.replace("'","''"),txtFairLndg.replace("'","''"),request.session['uid'])
#             objModelRisks.insertModelRisk()

#             objMdlRelvPern=MdlRelevantPersonnel()
#             objMdlRelvPern.insertUsers(mdl_id,'Owner',ddlOwner,request.session['uid'])

#             objMdlRelvPern.insertUsers(mdl_id,'Developer',ddlDeveloper,request.session['uid'])

#             objMdlRelvPern.insertUsers(mdl_id,'User',ddlUser,request.session['uid'])

#             objMdlRelvPern.insertUsers(mdl_id,'PrdnSupport',ddlPrdnSupp,request.session['uid'])

            
#             #Thread Creation
#             current_user_id = request.session['uid'] 
#             thread_filter_creation(current_user_id,mrm_head)

#             notification_trigger= "New Model registered - " + mdl_id
#             objmaster.insert_notification(request.session['uid'],mrm_head,"Model",notification_trigger,1)
            
#             objdependencies=MdlDependenciesCls()
#             objdependencies.insertMdlDepencies(mdl_id,ddlUpstrmMdl,ddlDwstrmMdl,request.session['uid'])

#             # objPerformMon=MdlPerformanceMonitoring(mdl_id,txtApproach.replace("'","''"),ddlMonrFreq,txtMonrMtrcs.replace("'","''"),txtTgrEvt.replace("'","''")
#             #                                        ,txtLstTgrDt,txtLstTgrMtgnDt,txtTgrEvtMtgn.replace("'","''"),request.session['uid'])
#             # objPerformMon.insertPerfomanceMonitor() 
#             destination_path = os.path.join(BASE_DIR, 'static\\document_files\\'+mdl_id+'\\')
#             objdocs=MdlDocs()
#             if not os.path.exists(destination_path):
#                 os.makedirs(destination_path)
#             # txtMDD
#             fl_MD = request.FILES.get('txtMDD', 'none')             
#             if fl_MD != 'none':
#                 fs = FileSystemStorage()
#                 savefile_name = destination_path + mdl_id+'_'+fl_MD.name
#                 if os.path.exists(savefile_name):
#                     os.remove(savefile_name)
#                 fs.save(savefile_name, fl_MD)
#                 objdocs.inserDocs(mdl_id,'1',mdl_id+'_'+fl_MD.name,str(request.session['uid']))
#             else:
#                 mdlid = mdlid
#                 api_data = getDocs(mdlid,'1',request)
#                 if api_data!="":
#                     destination_path_old = os.path.join(BASE_DIR, 'static\\document_files\\'+mdlid+'\\')
#                     fs = FileSystemStorage()
#                     # savefile_name = destination_path_old + mdlid+'_'+'Laboratory Reports.pdf'
#                     savefile_name = destination_path_old + api_data['mdl_doc_name']
#                     if os.path.exists(savefile_name):
#                         shutil.copy(savefile_name, destination_path)
#                     objdocs.inserDocs(mdl_id,'1',api_data['mdl_doc_name'],str(request.session['uid']))

#             fl_MD = request.FILES.get('txtUserManual', 'none')             
#             if fl_MD != 'none':
#                 fs = FileSystemStorage()
#                 savefile_name = destination_path + mdl_id+'_'+fl_MD.name
#                 if os.path.exists(savefile_name):
#                     os.remove(savefile_name)
#                 fs.save(savefile_name, fl_MD)
#                 objdocs.inserDocs(mdl_id,'2',mdl_id+'_'+fl_MD.name,str(request.session['uid']))
#             else:
#                 mdlid = mdlid
#                 api_data = getDocs(mdlid,'2',request)
#                 if api_data!="":
#                     destination_path_old = os.path.join(BASE_DIR, 'static\\document_files\\'+mdlid+'\\')
#                     fs = FileSystemStorage()
#                     # savefile_name = destination_path_old + mdlid+'_'+'Laboratory Reports.pdf'
#                     savefile_name = destination_path_old + api_data['mdl_doc_name']
#                     if os.path.exists(savefile_name):
#                         shutil.copy(savefile_name, destination_path)
#                     objdocs.inserDocs(mdl_id,'2',api_data['mdl_doc_name'],str(request.session['uid']))


#             fl_MD = request.FILES.get('txtMdlData', 'none')             
#             if fl_MD != 'none':
#                 fs = FileSystemStorage()
#                 savefile_name = destination_path + mdl_id+'_'+fl_MD.name
#                 if os.path.exists(savefile_name):
#                     os.remove(savefile_name)
#                 fs.save(savefile_name, fl_MD)
#                 objdocs.inserDocs(mdl_id,'3',mdl_id+'_'+fl_MD.name,str(request.session['uid']))
#             else:
#                 mdlid = mdlid
#                 api_data = getDocs(mdlid,'3',request)
#                 if api_data!="":
#                     destination_path_old = os.path.join(BASE_DIR, 'static\\document_files\\'+mdlid+'\\')
#                     fs = FileSystemStorage()
#                     # savefile_name = destination_path_old + mdlid+'_'+'Laboratory Reports.pdf'
#                     savefile_name = destination_path_old + api_data['mdl_doc_name']
#                     if os.path.exists(savefile_name):
#                         shutil.copy(savefile_name, destination_path)
#                     objdocs.inserDocs(mdl_id,'3',api_data['mdl_doc_name'],str(request.session['uid']))

#             fl_MD = request.FILES.get('txtMdlCode', 'none')             
#             if fl_MD != 'none':
#                 fs = FileSystemStorage()
#                 savefile_name = destination_path + mdl_id+'_'+fl_MD.name
#                 if os.path.exists(savefile_name):
#                     os.remove(savefile_name)
#                 fs.save(savefile_name, fl_MD)
#                 objdocs.inserDocs(mdl_id,'4',mdl_id+'_'+fl_MD.name,str(request.session['uid']))
#             else:
#                 mdlid = mdlid
#                 api_data = getDocs(mdlid,'4',request)
#                 if api_data!="":
#                     destination_path_old = os.path.join(BASE_DIR, 'static\\document_files\\'+mdlid+'\\')
#                     fs = FileSystemStorage()
#                     # savefile_name = destination_path_old + mdlid+'_'+'Laboratory Reports.pdf'
#                     savefile_name = destination_path_old + api_data['mdl_doc_name']
#                     if os.path.exists(savefile_name):
#                         shutil.copy(savefile_name, destination_path)
#                     objdocs.inserDocs(mdl_id,'4',api_data['mdl_doc_name'],str(request.session['uid']))

            
#             fl_MD = request.FILES.get('txtUAT', 'none')             
#             if fl_MD != 'none':
#                 fs = FileSystemStorage()
#                 savefile_name = destination_path + mdl_id+'_'+fl_MD.name
#                 if os.path.exists(savefile_name):
#                     os.remove(savefile_name)
#                 fs.save(savefile_name, fl_MD)
#                 objdocs.inserDocs(mdl_id,'5',mdl_id+'_'+fl_MD.name,str(request.session['uid']))
#             else:
#                 mdlid = mdlid
#                 api_data = getDocs(mdlid,'5',request)
#                 if api_data!="":
#                     destination_path_old = os.path.join(BASE_DIR, 'static\\document_files\\'+mdlid+'\\')
#                     fs = FileSystemStorage()
#                     # savefile_name = destination_path_old + mdlid+'_'+'Laboratory Reports.pdf'
#                     savefile_name = destination_path_old + api_data['mdl_doc_name']
#                     if os.path.exists(savefile_name):
#                         shutil.copy(savefile_name, destination_path)
#                     objdocs.inserDocs(mdl_id,'5',api_data['mdl_doc_name'],str(request.session['uid']))


#             fl_MD = request.FILES.get('txtTechManual', 'none')             
#             if fl_MD != 'none':
#                 fs = FileSystemStorage()
#                 savefile_name = destination_path + mdl_id+'_'+fl_MD.name
#                 if os.path.exists(savefile_name):
#                     os.remove(savefile_name)
#                 fs.save(savefile_name, fl_MD)
#                 objdocs.inserDocs(mdl_id,'6',mdl_id+'_'+fl_MD.name,str(request.session['uid']))

#             fl_MD = request.FILES.get('txtOnboardDoc', 'none')             
#             if fl_MD != 'none':
#                 fs = FileSystemStorage()
#                 savefile_name = destination_path + mdl_id+'_'+fl_MD.name
#                 if os.path.exists(savefile_name):
#                     os.remove(savefile_name)
#                 fs.save(savefile_name, fl_MD)
#                 objdocs.inserDocs(mdl_id,'7',mdl_id+'_'+fl_MD.name,str(request.session['uid']))
#             else:
#                 mdlid = mdlid
#                 api_data = getDocs(mdlid,'7',request)
#                 if api_data!="":
#                     destination_path_old = os.path.join(BASE_DIR, 'static\\document_files\\'+mdlid+'\\')
#                     fs = FileSystemStorage()
#                     # savefile_name = destination_path_old + mdlid+'_'+'Laboratory Reports.pdf'
#                     savefile_name = destination_path_old + api_data['mdl_doc_name']
#                     if os.path.exists(savefile_name):
#                         shutil.copy(savefile_name, destination_path)
#                     objdocs.inserDocs(mdl_id,'7',api_data['mdl_doc_name'],str(request.session['uid']))

                
#             # print('txtMdlAppl ',txtMdlAppl, ' txtLstTgrMtgnDt ',txtLstTgrMtgnDt,' rbisnewupdate ',rbisnewupdate,request.session['dept'])
#             objmaster.insertActivityTrail(mdl_id,"1","New model registered.",request.session['uid'],request.session['accessToken'])
#         today = date.today().strftime("%m/%d/%Y") 

#         dept= objreg.getDeptNm(request.session['dept'])

#         Mdl_Src = objreg.getMdl_Src()  

#         Mdl_Type =objreg.getMdl_Type() 
        
#         Mdl_Usage_Frq=  objreg.getMdl_Usage_Fre()
        
#         Prd_Addr = objreg.getPrd_Addr() 

#         Mdl_Risk = objreg.getMdl_Risk()  

#         Intrinsic = objreg.getIntrinsic()  

#         Materiality = objreg.getMateriality()        
         
#         Reliance = objreg.getReliance()  

#         Mdl_Owners =objreg.getUsers(request.session['dept'],2)      

#         Mdl_Validators =objreg.getUsers(request.session['dept'],3)         

#         Mdl_Devs =objreg.getUsersByType('Developer')         

#         Upstr_Model=objreg.getMdlUpstrem(request.session['uid'])

#         Dwstr_Model=objreg.getMdlUpstrem(request.session['uid']) #objreg.getMdlDwStream()

#         Motr_Freq=objreg.getMontrFreq()

#         Mdl_Func=objreg.getMdlFunc()

#         Models_FieldsResult =objdbops.getTable("SELECT  Field_ID,Fields_name,Field_Label,Is_Mandatory,Is_Visible  FROM Models_Fields order by 1 ")
#         Models_Fields = Models_FieldsResult.to_json(orient='index')
#         Models_Fields = json.loads(Models_Fields)
#         del Models_FieldsResult
#         arrFields=dict()
#         for i in Models_Fields: 
#             if Models_Fields[i]["Fields_name"]=="function":
#                 arrFields["FunctionVisible"]= 'block' if Models_Fields[i]["Is_Visible"]==True else 'none'
#                 arrFields["FunctionMadatory"]= 'required' if Models_Fields[i]["Is_Mandatory"]==True else ''
#                 arrFields["FunctionMadatoryAstr"]= 'block' if Models_Fields[i]["Is_Mandatory"]==True else 'none'
#                 arrFields["FunctionLbl"]= Models_Fields[i]["Field_Label"]
#             elif Models_Fields[i]["Fields_name"]=="Secondary Model Name":
#                 arrFields["SecMdlVisible"]=  'block' if Models_Fields[i]["Is_Visible"]==True else 'none'
#                 arrFields["SecMdlMadatory"]= 'required' if Models_Fields[i]["Is_Mandatory"]==True else ''
#                 arrFields["SecMdlMadatoryAstr"]= 'block' if Models_Fields[i]["Is_Mandatory"]==True else 'none'
#                 arrFields["SecMdlLbl"]=Models_Fields[i]["Field_Label"]
#             elif Models_Fields[i]["Fields_name"]=="Model Type":
#                 arrFields["MdlTypeVisible"]=  'block' if Models_Fields[i]["Is_Visible"]==True else 'none'
#                 arrFields["MdlTypeMadatory"]= 'required' if Models_Fields[i]["Is_Mandatory"]==True else ''
#                 arrFields["MdlTypeMadatoryAstr"]= 'block' if Models_Fields[i]["Is_Mandatory"]==True else 'none'
#                 arrFields["MdlTypeLbl"]=Models_Fields[i]["Field_Label"]
#             elif Models_Fields[i]["Fields_name"]=="Model Abstract":
#                 arrFields["MdlAbsVisible"]=  'block' if Models_Fields[i]["Is_Visible"]==True else 'none'
#                 arrFields["MdlAbsMadatory"]= 'required' if Models_Fields[i]["Is_Mandatory"]==True else ''
#                 arrFields["MdlAbsMadatoryAstr"]= 'block' if Models_Fields[i]["Is_Mandatory"]==True else 'none'
#                 arrFields["MdlAbsLbl"]=Models_Fields[i]["Field_Label"]
#             elif Models_Fields[i]["Fields_name"]=="Objective of Model":
#                 arrFields["ObjMdlVisible"]=  'block' if Models_Fields[i]["Is_Visible"]==True else 'none'
#                 arrFields["ObjMdlMadatory"]= 'required' if Models_Fields[i]["Is_Mandatory"]==True else ''
#                 arrFields["ObjMdlMadatoryAstr"]= 'block' if Models_Fields[i]["Is_Mandatory"]==True else 'none'
#                 arrFields["ObjMdlLbl"]=Models_Fields[i]["Field_Label"]
#             elif Models_Fields[i]["Fields_name"]=="Application of Model":
#                 arrFields["ApplMdlVisible"]=  'block' if Models_Fields[i]["Is_Visible"]==True else 'none'
#                 arrFields["ApplMdlMadatory"]= 'required' if Models_Fields[i]["Is_Mandatory"]==True else ''
#                 arrFields["ApplMdlMadatoryAstr"]= 'block' if Models_Fields[i]["Is_Mandatory"]==True else 'none'
#                 arrFields["ApplMdlLbl"]=Models_Fields[i]["Field_Label"]
#             elif Models_Fields[i]["Fields_name"]=="Model Risk Analysis":
#                 arrFields["MdlRskVisible"]=  'block' if Models_Fields[i]["Is_Visible"]==True else 'none'
#                 arrFields["MdlRskMadatory"]= 'required' if Models_Fields[i]["Is_Mandatory"]==True else ''
#                 arrFields["MdlRskMadatoryAstr"]= 'block' if Models_Fields[i]["Is_Mandatory"]==True else 'none'
#                 arrFields["MdlRskLbl"]=Models_Fields[i]["Field_Label"]
#             elif Models_Fields[i]["Fields_name"]=="Products Addressed":
#                 arrFields["PrdAddrVisible"]=  'block' if Models_Fields[i]["Is_Visible"]==True else 'none'
#                 arrFields["PrdAddrMadatory"]= 'required' if Models_Fields[i]["Is_Mandatory"]==True else ''
#                 arrFields["PrdAddrMadatoryAstr"]= 'block' if Models_Fields[i]["Is_Mandatory"]==True else 'none'
#                 arrFields["PrdAddrLbl"]=Models_Fields[i]["Field_Label"]
#             elif Models_Fields[i]["Fields_name"]=="Usage Frequency":
#                 arrFields["UsgFreqVisible"]=  'block' if Models_Fields[i]["Is_Visible"]==True else 'none'
#                 arrFields["UsgFreqMadatory"]= 'required' if Models_Fields[i]["Is_Mandatory"]==True else ''
#                 arrFields["UsgFreqMadatoryAstr"]= 'block' if Models_Fields[i]["Is_Mandatory"]==True else 'none'
#                 arrFields["UsgFreqLbl"]=Models_Fields[i]["Field_Label"]  

#         third_party_api_url = getAPIURL()+'category_master/'
#         header = {
#         "Content-Type":"application/json",
# 	    'Authorization': 'Token '+request.session['accessToken']
#         }
#         response_cat = requests.get(third_party_api_url, headers=header)   
#         return render(request, 'registermodel.html',{ 'actPage':'Model Registration','Mdl_Func':Mdl_Func,'Upstr_Model':Upstr_Model,
#                     'Dwstr_Model':Dwstr_Model,'Motr_Freq':Motr_Freq,'mdl_id':mdl_id,
#                     'mdlinfo':objreg.getModelsbyUserid(request.session['uid']),'Mdl_Devs':Mdl_Devs,
#                 'Mdl_Validators':Mdl_Validators,'Mdl_Owners':Mdl_Owners,'Reliance':Reliance,
#                 'Materiality':Materiality,'Intrinsic':Intrinsic,'Mdl_Risk':Mdl_Risk,'Prd_Addr':Prd_Addr,'Mdl_Usage_Frq':Mdl_Usage_Frq,
#                 'Mdl_Type':Mdl_Type,'Mdl_Src':Mdl_Src,'dept':dept,'regDate':today,'arrFields':arrFields,'category':json.loads(response_cat.content)})
#     except Exception as e:
#         print('addmodel is ',e)
#         print('addmodel traceback is ', traceback.print_exc()) 
#         error_saving(request,e)



def ModelArtifacts(request):
    try:
        fileuploaded=''
        if request.method == 'POST':
            mdl_id=request.POST["ddlModelId"]
            print('mdl_id is',mdl_id)
            destination_path = os.path.join(BASE_DIR, 'static\\document_files\\'+mdl_id+'\\')
            objdocs=MdlDocs()
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)
            # txtMDD
            fl_MD = request.FILES.get('txtMDD', 'none')             
            if fl_MD != 'none':
                fs = FileSystemStorage()
                savefile_name = destination_path + mdl_id+'_'+fl_MD.name
                if os.path.exists(savefile_name):
                    os.remove(savefile_name)
                fs.save(savefile_name, fl_MD)
                objdocs.inserDocs(mdl_id,'1',mdl_id+'_'+fl_MD.name,str(request.session['uid']))
                fileuploaded='yes'

            fl_MD = request.FILES.get('txtUserManual', 'none')             
            if fl_MD != 'none':
                fs = FileSystemStorage()
                savefile_name = destination_path + mdl_id+'_'+fl_MD.name
                if os.path.exists(savefile_name):
                    os.remove(savefile_name)
                fs.save(savefile_name, fl_MD)
                objdocs.inserDocs(mdl_id,'2',mdl_id+'_'+fl_MD.name,str(request.session['uid']))
                fileuploaded='yes'

            fl_MD = request.FILES.get('txtMdlData', 'none')             
            if fl_MD != 'none':
                fs = FileSystemStorage()
                savefile_name = destination_path + mdl_id+'_'+fl_MD.name
                if os.path.exists(savefile_name):
                    os.remove(savefile_name)
                fs.save(savefile_name, fl_MD)
                objdocs.inserDocs(mdl_id,'3',mdl_id+'_'+fl_MD.name,str(request.session['uid']))
                fileuploaded='yes'

            fl_MD = request.FILES.get('txtMdlCode', 'none')             
            if fl_MD != 'none':
                fs = FileSystemStorage()
                savefile_name = destination_path + mdl_id+'_'+fl_MD.name
                if os.path.exists(savefile_name):
                    os.remove(savefile_name)
                fs.save(savefile_name, fl_MD)
                objdocs.inserDocs(mdl_id,'4',mdl_id+'_'+fl_MD.name,str(request.session['uid']))
                fileuploaded='yes'
            
            fl_MD = request.FILES.get('txtUAT', 'none')             
            if fl_MD != 'none':
                fs = FileSystemStorage()
                savefile_name = destination_path + mdl_id+'_'+fl_MD.name
                if os.path.exists(savefile_name):
                    os.remove(savefile_name)
                fs.save(savefile_name, fl_MD)
                objdocs.inserDocs(mdl_id,'5',mdl_id+'_'+fl_MD.name,str(request.session['uid']))
                fileuploaded='yes'

            fl_MD = request.FILES.get('txtTechManual', 'none')             
            if fl_MD != 'none':
                fs = FileSystemStorage()
                savefile_name = destination_path + mdl_id+'_'+fl_MD.name
                if os.path.exists(savefile_name):
                    os.remove(savefile_name)
                fs.save(savefile_name, fl_MD)
                objdocs.inserDocs(mdl_id,'6',mdl_id+'_'+fl_MD.name,str(request.session['uid']))
                fileuploaded='yes'

            fl_MD = request.FILES.get('txtOnboardDoc', 'none')             
            if fl_MD != 'none':
                fs = FileSystemStorage()
                savefile_name = destination_path + mdl_id+'_'+fl_MD.name
                if os.path.exists(savefile_name):
                    os.remove(savefile_name)
                fs.save(savefile_name, fl_MD)
                objdocs.inserDocs(mdl_id,'7',mdl_id+'_'+fl_MD.name,str(request.session['uid']))
                fileuploaded='yes'
        return render(request, 'ModelArtifacts.html',{'fileuploadsts':fileuploaded,'mdlinfo':objreg.getModelsbyUserid(request.session['uid'])})
    except Exception as e:
        print('ModelArtifacts is ',e)
        print('ModelArtifacts traceback is ', traceback.print_exc()) 

def thread_filter_creation(send_by,send_to):
    try:
        threadfilter = Thread.objects.filter(first_person = send_by,second_person = send_to)
        print("threadfilter",threadfilter)
        if not threadfilter:
            curr_user_id = Users.objects.get(u_aid = send_by)
            print("curr_user_id",curr_user_id)
            othr_usr_id = Users.objects.get(u_aid = send_to)
            print("othr_usr_id",othr_usr_id)
            threadobj = Thread(first_person = curr_user_id,second_person = othr_usr_id)
            threadobj.save()
            thread_id = threadobj.thread_id
            print("save thread successfully") 
                
        else: 
            thread_id = threadfilter.thread_id
            print("pass",thread_id)
    except Exception as e:
        print('thread filetr ',e)
    
def thread_creation(request):
    send_by=request.GET.get('send_by', 'False')
    send_to=request.GET.get('send_to', 'False')
    threadfilter = Thread.objects.filter(first_person = send_by,second_person = send_to)
    print("threadfilter",threadfilter)
    if not threadfilter:
        curr_user_id = Users.objects.get(u_aid = send_by)
        print("curr_user_id",curr_user_id)
        othr_usr_id = Users.objects.get(u_aid = send_to)
        print("othr_usr_id",othr_usr_id)
        threadobj = Thread(first_person = curr_user_id,second_person = othr_usr_id)
        threadobj.save()
        thread_id = threadobj.thread_id
        print("save thread successfully") 
             
    else: 
        thread_id = threadfilter.thread_id
        print("pass",thread_id)
        pass
    

# def addtool(request):
#     try:
#         mdl_id=''
#         if request.method == 'POST':   
#             rbisnewupdate = request.POST['rbisnewupdate'] 
#             ddlFunction = request.POST['ddlFunction'] 
#             txtMdlId = request.POST['txtMdlId'] 
#             txtPrmName = request.POST['txtPrmName'] 
#             txtSecName = request.POST['txtSecName'] 
#             ddlSource = request.POST['ddlSource'] 
#             ddlType = request.POST['ddlType'] 
#             txtMdlAbsct = request.POST['txtMdlAbsct'] 
#             txtMdlObj = request.POST['txtMdlObj'] 
#             txtMdlAppl = request.POST['txtMdlAppl'] 
#             txtMdlRiskAnls = request.POST['txtMdlRiskAnls'] 
#             ddlPrctAddr = request.POST['ddlPrctAddr'] 
#             ddlUsgFreq = request.POST['ddlUsgFreq'] 
#             txtMdlRisks = request.POST['txtMdlRisks'] 
#             ddlIntrRisk = request.POST['ddlIntrRisk'] 
#             ddlReliance = request.POST['ddlReliance'] 
#             ddlMateriality = request.POST['ddlMateriality'] 
#             txtRiskMtgn = request.POST['txtRiskMtgn'] 
#             txtFairLndg = request.POST['txtFairLndg'] 
#             ddlOwner =  request.POST.getlist('ddlOwner')
#             ddlDeveloper = request.POST.getlist('ddlDeveloper')  
#             ddlUser = request.POST.getlist('ddlUser')    
#             txtValidator = request.POST['txtValidator'] 
#             ddlPrdnSupp = request.POST.getlist('ddlPrdnSupp')   
#             ddlUpstrmMdl = request.POST['ddlUpstrmMdl'] 
#             ddlDwstrmMdl = request.POST['ddlDwstrmMdl'] 
#             txtApproach = request.POST['txtApproach'] 
#             ddlMonrFreq = request.POST['ddlMonrFreq'] 
#             txtTgrEvt = request.POST['txtTgrEvt'] 
#             txtLstTgrDt = request.POST['txtLstTgrDt'] 
#             txtLstTgrMtgnDt = request.POST['txtLstTgrMtgnDt'] 
#             txtTgrEvtMtgn = request.POST['txtTgrEvtMtgn'] 
#             txtMonrMtrcs=request.POST['txtMonrMtrcs'] 
#             objoverview=MdlOverviewCls(txtMdlId,'1','0','0',rbisnewupdate,'1',request.session['dept']
#                                     ,ddlFunction,txtPrmName.replace("'","''"),txtSecName.replace("'","''"),ddlSource,ddlType,txtMdlAbsct.replace("'","''"),txtMdlObj.replace("'","''")
#                                     ,txtMdlAppl.replace("'","''"),txtMdlRiskAnls.replace("'","''"),ddlPrctAddr,ddlUsgFreq,request.session['uid'],str(datetime.now))
#             mdl_id=objoverview.insertMdlOverview()

#             objModelRisks=ModelRisks(mdl_id,txtMdlRisks,ddlIntrRisk,ddlReliance,ddlMateriality,txtRiskMtgn.replace("'","''"),txtFairLndg.replace("'","''"),request.session['uid'])
#             objModelRisks.insertModelRisk()

#             objMdlRelvPern=MdlRelevantPersonnel()
#             objMdlRelvPern.insertUsers(mdl_id,'Owner',ddlOwner,request.session['uid'])

#             objMdlRelvPern.insertUsers(mdl_id,'Developer',ddlDeveloper,request.session['uid'])

#             objMdlRelvPern.insertUsers(mdl_id,'User',ddlUser,request.session['uid'])

#             objMdlRelvPern.insertUsers(mdl_id,'PrdnSupport',ddlPrdnSupp,request.session['uid'])

#             #Thread Creation
#             current_user_id = request.session['uid']
#             print("current user id next",current_user_id)
#             print("other user check next",ddlOwner)
#             for i in ddlOwner:
#                 thread_filter_creation(current_user_id,i)

#             objdependencies=MdlDependenciesCls()
#             objdependencies.insertMdlDepencies(mdl_id,ddlUpstrmMdl,ddlDwstrmMdl,request.session['uid'])

#             objPerformMon=MdlPerformanceMonitoring(mdl_id,txtApproach.replace("'","''"),ddlMonrFreq,txtMonrMtrcs.replace("'","''"),txtTgrEvt.replace("'","''")
#                                                    ,txtLstTgrDt,txtLstTgrMtgnDt,txtTgrEvtMtgn.replace("'","''"),request.session['uid'])
#             objPerformMon.insertPerfomanceMonitor()

#             # print('txtMdlAppl ',txtMdlAppl, ' txtLstTgrMtgnDt ',txtLstTgrMtgnDt,' rbisnewupdate ',rbisnewupdate,request.session['dept'])

#         today = date.today().strftime("%m/%d/%Y") 

#         dept= objreg.getDeptNm(request.session['dept'])

#         Mdl_Src = objreg.getMdl_Src()  

#         Mdl_Type =objreg.getMdl_Type() 
        
#         Mdl_Usage_Frq=  objreg.getMdl_Usage_Fre()
        
#         Prd_Addr = objreg.getPrd_Addr() 

#         Mdl_Risk = objreg.getMdl_Risk()  

#         Intrinsic = objreg.getIntrinsic()  

#         Materiality = objreg.getMateriality()        
         
#         Reliance = objreg.getReliance()  

#         Mdl_Owners =objreg.getUsers(request.session['dept'],2)    

#         Mdl_Validators =[]#objreg.getUsers(request.session['dept'],3)         

#         Mdl_Devs =[]#objreg.getUsers(request.session['dept'],4)         

#         return render(request, 'registertool.html',{ 'actPage':'Tool Registration','mdl_id':mdl_id,'mdlinfo':objreg.getModelsbyUserid(request.session['uid']),'Mdl_Devs':Mdl_Devs,'Mdl_Validators':Mdl_Validators,'Mdl_Owners':Mdl_Owners,'Reliance':Reliance,'Materiality':Materiality,'Intrinsic':Intrinsic,'Mdl_Risk':Mdl_Risk,'Prd_Addr':Prd_Addr,'Mdl_Usage_Frq':Mdl_Usage_Frq,'Mdl_Type':Mdl_Type,'Mdl_Src':Mdl_Src,'dept':dept,'regDate':today})
#     except Exception as e:
#         print('addtool is ',e)
#         print('addtool traceback is ', traceback.print_exc()) 

# def getMdlInfoById(request):
#     try:
#         mdlid =request.GET.get('mdlid', 'False')
#         majorVer=''
#         minorVer=''
#         if(mdlid!=""): 
#             mdlinfo= objreg.getMdlinfo(mdlid) 
#             majorVer=mdlinfo["Mdl_Major_Ver"].values[0]
#             minorVer=mdlinfo["Mdl_Minor_Ver"].values[0]
#         return JsonResponse({'majorVer':str(majorVer),'minorVer':str(minorVer)})
#     except Exception as e:
#         print('getMdlInfoById is ',e)
#         print('getMdlInfoById traceback is ', traceback.print_exc()) 

def getnotifications(request):
    try:
         
        return JsonResponse({'notification':objreg.get_notifications(request.session['uid'])})
    except Exception as e:
        print('getMdlInfoById is ',e)
        print('getMdlInfoById traceback is ', traceback.print_exc()) 

# def updateMdlVersion(request):
#     try:
#         mdlid =request.GET.get('mdlid', 'False')
#         isMinor =request.GET.get('isMinor', 'False')
#         api_url=getAPIURL()+"getMdlDetailsById/"       
#         data_to_save={
#             'mdl_id':mdlid} 
#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }
#         response = requests.get(api_url, data= json.dumps(data_to_save),headers=header) 
#         api_data=response.json()  
#         newMdlId,mdlVersion = objreg.updateMdlVersion(mdlid,isMinor)
#         return JsonResponse({'newMdlId':newMdlId,'mdlVersion':mdlVersion,'regmdldata':api_data})
#     except Exception as e:
#         print('getMdlInfoById is ',e)
#         print('getMdlInfoById traceback is ', traceback.print_exc())

def getUsers(dept,utype):
    tableResult = objdbops.getTable("select concat(U_FName,' ',U_LName) usernm,u_aid  from users where dept_aid='"+str(dept)+"' and UC_AID='"+str(utype)+"'")
    return tableResult

def reqValidation(request):
    try:
        mdl_id=request.GET.get('mdl_id','')
        print('mdl_id is ',mdl_id)
        api_url=getAPIURL()+"reqValidation/"       
        data_to_save={ 
            'uid':request.session['uid'],
            'ulvl':request.session['ulvl'],} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json() 
        return render(request, 'reqValidation.html',{ 'actPage':'Request Model Validation','selMdl':mdl_id,
                                                     'mrmUsers':api_data['mrmUsers'],'modelinfo':api_data['modelinfo'],'validationTYpes':api_data['validationTYpes']})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc()) 



def assignValidation(request):
    try: 
        api_url=getAPIURL()+"assignValidation/"       
        data_to_save={ 
            'uid':request.session['uid'],
            'ulvl':request.session['ulvl'],
            'dept':request.session['dept'],
            'datalist':request.GET['datalist'],
            'ddlUsers':request.GET['ddlUsers'],
            'mdlId': request.GET['mdlId'] } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json() 
        return JsonResponse({'istaken':'true','assignTaskLst':api_data['assignTaskLst']})
    except Exception as e:
        print('assignValidation ',e)
        print('assignValidation traceback is ', traceback.print_exc()) 
        return JsonResponse({'istaken':'false'})
    
def getAssignedTo(request):
    try: 
        mdlId = request.GET['mdlId']  
       
        api_url=getAPIURL()+"getAssignedTo/"       
        data_to_save={ 
            'mdlId':request.GET['mdlId'], 
            } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        return JsonResponse({'istaken':api_data['istaken'],'assignedTo':api_data['assignedTo']})
    except Exception as e:
        print('assignValidation ',e)
        print('assignValidation traceback is ', traceback.print_exc()) 
        return JsonResponse({'istaken':'false'})




def todolist(request):
    try:
        return render(request, 'todolist.html',{ 'actPage':'Upcoming'})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 

def activity(request):
    try:
        return render(request, 'activity.html',{ 'actPage':'Task'})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 

 

def deptaddnewuser(request):
    try:  
        tableResult =objdbops.getTable("SELECT   UC_AID  ,UC_Label  FROM User_Category where uc_level < "+str(request.session['ulvl']) +" and UC_Label <> 'Admin' order by 2 ")
        users = tableResult.to_json(orient='index')
        users = json.loads(users)
        del tableResult
        

        tableResult =objdbops.getTable("SELECT Dept_AID,Dept_Label FROM Department") 
        dept = tableResult.to_json(orient='index')
        dept = json.loads(dept)
        del tableResult
        return render(request, 'deptadduser.html',{ 'actPage':'Add User','utype':users,'dept':dept,'dept_head':request.session['dept']})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc()) 
 


def showusercat(request):
    try: 
        tableResult =objdbops.getTable("select * from User_Category")  
        users = tableResult.to_json(orient='index')
        users = json.loads(users)
        print("users",users)
        del tableResult
        return render(request, 'usercatlist.html',{ 'actPage':'User Types','users':users})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def addnewusercat(request):
    try:   
        return render(request, 'newusercat.html',{ 'actPage':'Add User Types','level':list(range(1, 8))})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def addusercat(request):
    try: 
        added_by=request.session['uid']
        add_date=datetime.now()
        update_id=request.GET.get('update_id')
        utype =request.GET.get('utype', 'False')  
        desc=request.GET.get('desc', 'False')      
        activests=request.GET.get('activests', '0')   
        ddlulvl=request.GET.get('ddlulvl','0')
        isDeptHead=request.GET.get('isdepthead','0')
        if update_id:
            print("update_id",update_id)
            user_cat_obj=UserCategory.objects.get(uc_aid=update_id)
            user_cat_obj.uc_label=utype
            user_cat_obj.uc_description=desc
            user_cat_obj.uc_level=ddlulvl
            user_cat_obj.is_dept_head=isDeptHead
            user_cat_obj.activestatus=activests
            user_cat_obj.updatedby=added_by
            user_cat_obj.updatedate=add_date
            user_cat_obj.save()
            return JsonResponse({"isvalid":"update"})
        else:    
            strQ="INSERT INTO User_Category (UC_Label ,UC_Description,ActiveStatus,AddedBy ,AddDate,UC_Level,UC_Is_DeptHead) "
            strQ += " VALUES  ('"+ utype+"','"+ desc+"','"+ activests+"', null,getdate(),"+ddlulvl+","+isDeptHead+")"
            
            objdbops.insertRow(strQ)
            return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})


def getReportsTo(request):
    try:
        uc_aid =request.GET.get('uc_aid', '')  
        dept_aid=request.GET.get('dept_aid', '')            
        if str(objmaster.isDeptHead(uc_aid)) == "0":
            strQ="select  u.u_name,u.u_aid  from"
            strQ +=" (select uc.UC_level+1 replvl from  User_Category uc    "
            strQ +=" where  uc.uc_aid="+uc_aid+" group by uc.uc_level) reportlvl,Users u,User_Category uc "  
            strQ +=" where reportlvl.replvl=uc.UC_Level and uc.uc_aid=u.uc_aid and u.dept_aid="+dept_aid
        else:
            strQ="select  u.u_name,u.u_aid  from"
            strQ +=" (select uc.UC_level+1 replvl from  User_Category uc    "
            strQ +=" where  uc.uc_aid="+uc_aid+" group by uc.uc_level) reportlvl,Users u,User_Category uc "  
            strQ +=" where reportlvl.replvl=uc.UC_Level and uc.uc_aid=u.uc_aid  "

        print('strQ ')
        print(strQ)    
        tablereult =objdbops.getTable(strQ)
        reportsto= tablereult.to_json(orient='index')
        reportsto = json.loads(reportsto)
        del tablereult
        return JsonResponse({'reportsto':reportsto})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})



def showdept(request):
    try: 
        #new
        third_party_api_url = getAPIURL()+'department/'
        print('access token  ',request.session['accessToken'])
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response department",response.content)

        # tableResult =objdbops.getTable("select * from Department") 
        # users = tableResult.to_json(orient='index')
        # users = json.loads(users)
        # print("users",users)
        # del tableResult
        return render(request, 'deptlist.html',{ 'actPage':'Departments','users':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def newdept(request):
    try:   
        third_party_api_url = getAPIURL()+'department/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response department",json.loads(response.content))
        data = json.loads(response.content)
        is_mrm_exists = ""
        is_mrm=0
        for i in data:
            print(i['dept_ismrm'])
            if i['dept_ismrm'] == 1:
                is_mrm_exists = "disabled"
                is_mrm=0
                break
            else:
                is_mrm_exists = ""
                is_mrm=1

        return render(request, 'adddepartment.html',{ 'actPage':'Add Department','is_mrm_exists':is_mrm_exists,'is_mrm':is_mrm})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

@api_view(['POST','PUT'])
def adddept(request):
    try:
        third_party_api_url = getAPIURL()+'department/'

        updated_id = request.POST.get('update_id','False')
        dept_label = request.POST.get('dept', 'False') 
        dept_description = request.POST.get('desc','False')
        activestatus = request.POST.get('ismrm','False')

        print("request------------------------",updated_id)
        if updated_id != 'False':
            third_party_api_url = getAPIURL()+'updatedepartment/'
            print("third_party_api_url",third_party_api_url)
            data_to_update = {
                'dept_label':dept_label,
                'dept_description':dept_description,
                'activestatus':1,
                'id':updated_id,
                'dept_ismrm':activestatus 
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.put(third_party_api_url, data= json.dumps(data_to_update),headers=header)
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
        else:
            third_party_api_url = getAPIURL()+'department/'
            data_to_save = {
                'dept_label':dept_label,
                'dept_description':dept_description,
                'activestatus':activestatus
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
            print("----------------5",json.loads(response.content))
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def criteriaQtns(request):
    try:   
        
        qtnSections=objmaster.getQtnSections()
        return render(request, 'addCriteriaQuestions.html',{ 'actPage':'Add Criteria Quetions','qtnSections':qtnSections})
    except Exception as e:
        print('criteriaQtns is ',e)
        print('criteriaQtns traceback is ', traceback.print_exc())

def addQuestion(request):
    try: 
        section =request.GET.get('section', 'False')  
        qtn=request.GET.get('question', 'False')     
        objmaster.insertQuestion(section,qtn)
        return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})

def criteriaSetting(request):
    try: 
        qtnSections=objmaster.getQtnSections()
        tempCriteria=objmaster.getTempCriteria(str(request.session['uid']))
        return render(request, 'criteriaSetting.html',{ 'actPage':'Set Criteria','tempCriteria':tempCriteria,'qtnSections':qtnSections})
    except Exception as e:
        print('criteriaQtns is ',e)
        print('criteriaQtns traceback is ', traceback.print_exc())

def getQtnSecWise(request):
    try:
        print('inside getqtn')           
        section =request.GET.get('section', 'False')  
        return JsonResponse({'qtns':objmaster.getQtn(section,str(request.session['uid'])) })
    except Exception as e:
        print('criteriaQtns is ',e)
        print('criteriaQtns traceback is ', traceback.print_exc())

def saveCriteria(request):
    try:
        ddlSection = request.GET.get('ddlSection','')
        ddlQtns = request.GET.get('ddlQtns','') 
        ddlOpt = request.GET.get('ddlOpt','') 
        ddlVal = request.GET.get('ddlVal','') 
        objmaster.insertTempCriteria(ddlSection,ddlQtns,ddlOpt,ddlVal,str(request.session['uid']))
        return JsonResponse({'istaken':'true'})
    except Exception as e:
        print('saveCriteria is ',e)
        print('saveCriteria traceback is ', traceback.print_exc())

def saveModelTool(request):
    try:
        colDataLst = request.GET['logicalOpt']
        modeltool = request.GET['modeltool']
        json_dictionary = json.loads(colDataLst) 
        newcriteria=objmaster.getNewCriteriaId()
        newcriteria="Criteria_"+str(newcriteria)
        objmaster.insertCriteria(newcriteria,str(request.session['uid']),modeltool,json_dictionary)
        return JsonResponse({'istaken':'true'})
    except Exception as e:
        print('saveModelTool is ',e)
        print('saveModelTool traceback is ', traceback.print_exc())

# def getCriteria(request):
#     try:   
#         api_url=getAPIURL()+"getCriteria/"    
#         header = {
#         "Content-Type":"application/json",
# 	    'Authorization': 'Token '+request.session['accessToken']
#         }
#         response = requests.get(api_url, headers=header)         
#         api_data=response.json()

#         return render(request, 'criteria.html',{ 'actPage':'Select Model/Tool','criteria':api_data['criteria']})
#     except Exception as e:
#         print('criteriaQtns is ',e)
#         print('criteriaQtns traceback is ', traceback.print_exc())


# def GetIsModel(request):
#     try:
#         colDataLst = request.GET['criteria'] 
#         qtns = request.GET['qtns'] 
#         api_url=getAPIURL()+"GetIsModel/"    
#         params={'criteria':colDataLst,
#             'qtns':qtns  } 
#         header = {
#         "Content-Type":"application/json",
# 	    'Authorization': 'Token '+request.session['accessToken']
#         }
#         response = requests.get(api_url, data= json.dumps(params),headers=header)        
#         api_data=response.json()    
       
#         return JsonResponse({'istaken':'true','isModel':api_data['isModel']})
#     except Exception as e:
#         print('saveModelTool is ',e)
#         print('saveModelTool traceback is ', traceback.print_exc())


def checkValue(request):
    try:
        tbl =request.GET.get('tbl', 'False')  
        val=request.GET.get('val', 'False')    
        dept=request.GET.get('dept', '')    
        utype=request.GET.get('utype', '')    
        print("tbl",tbl) 
        print("label",val) 

        cnt=""
        cnt = objmaster.checkUniqueVal(tbl,val,dept,utype)
        return JsonResponse({"isvalid":"true","cnt":cnt})
    except Exception as e:
        print('checkValue is ',e)
        print('checkValue traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})

def useraccess(request):
    try:  
        api_url = getAPIURL()+'Get_UC_DEPT/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        response = requests.get(api_url, data= {},headers=header)         
        api_data=response.json() 
        return render(request, 'useraccess.html',{ 'actPage':'User Access','dept':api_data['dept'],'users':api_data['resources'],'utype':api_data['utype']})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def deptuseraccess(request):
    try: 
        strQ="select R_AID,R_Label from Resources res "
        strQ+=" where R_Label <>'Validation Tool'"
        strQ+=" union"
        strQ+=" select  R_AID,R_Label  from "
        strQ+=" Resources ,department where Dept_AID="+str(request.session['dept'])+" and isnull(Dept_IsMRM,0)=1 and R_Label ='Validation Tool' order by 1"
         
        tableResult =objdbops.getTable(strQ)  
        users = tableResult.to_json(orient='index')
        users = json.loads(users)
        del tableResult
        tableResult =objdbops.getTable("SELECT   UC_AID  ,UC_Label  FROM User_Category  where uc_level < "+str(request.session['ulvl']) +" and UC_Label <> 'Admin' order by 2 ")
        utype = tableResult.to_json(orient='index')
        utype = json.loads(utype)
        del tableResult
        return render(request, 'deptuseraccess.html',{ 'actPage':'User Access','users':users,'utype':utype})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def getUCAccessData(request):
    try:
        uc = request.GET['uc'] 
        dept = request.GET['dept'] 
        api_url = getAPIURL()+'Get_Useraccess/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uc':uc,
            'dept':dept 
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json() 
        return JsonResponse({'istaken':'true','ucdata':api_data['ucdata'],'is_MRM':api_data['is_MRM']})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def getUCAccessDataDeptWise(request):
    try:
        uc = request.GET['uc'] 
        return JsonResponse({'istaken':'true','ucdata':objmaster.getUCAccessDeptWise(uc,request.session['dept'])})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def updateuseraccess(request):
    try:
        colDataLst = request.GET['datalist'] 
        uc = request.GET['uc'] 
        dept = request.GET['dept']  
        print(colDataLst)
        json_colDataLst = json.loads(colDataLst) 
        api_url = getAPIURL()+'Update_Useraccess/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uc':uc,
            'dept':dept,
            'datalist':json_colDataLst
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json() 
        
        return JsonResponse({'istaken':api_data['istaken']})
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})



def updateDeptuseraccess(request):
    try:
        colDataLst = request.GET['datalist'] 
        uc = request.GET['uc'] 
        json_colDataLst = json.loads(colDataLst)
         
        strQ="delete from User_Access where UC_AID="+str(uc) + " and UA_dept='"+str(request.session["dept"])+"'"
        
        objdbops.insertRow(strQ) 
        for colval in json_colDataLst:
            print('colval is ',colval['AID'],', UA',colval['UA'],colval['add'],colval['edit'],colval['delete'])
            # for attribute, value in colval.items():
            #     print(attribute, value) 
            strQ="INSERT INTO User_Access (R_AID,UA_Perm,UC_AID,AddDate,UA_Add,UA_Edit,UA_Delete,UA_dept)  VALUES ("
            strQ +=colval['AID'] +",'"+colval['UA']+"',"+str(uc)+",getdate(),"+ str(colval['add']) +","+str(colval['edit']) +","+ str(colval['delete']) +",'"+str(request.session["dept"])+"')"
            objdbops.insertRow(strQ)
        
        return JsonResponse({'istaken':'true'})
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})

def getscalar(strQ :str):
    try:
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LENOVOARUN\SQL2022;DATABASE=prope_db;UID=sa;PWD=Ajit@123')

        # Create a cursor from the connection
        cursor = cnxn.cursor()
        val = cursor.execute(strQ).fetchval()
        cnxn.close()
        return val
         
    except Exception as e:
        print('getscalar is ',e)
        print('getscalar traceback is ', traceback.print_exc()) 

def insertRow(strQ :str):
    try:
        # Specifying the ODBC driver, server name, database, etc. directly
       
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LENOVOARUN\SQL2022;DATABASE=prope_db;UID=sa;PWD=Ajit@123')

        # Create a cursor from the connection
        cursor = cnxn.cursor()

        # Do the insert
        cursor.execute(strQ)
        #commit the transaction
        cnxn.commit()
        cnxn.close()
         
    except Exception as e:
        print('insertRow is ',e)
        print('insertRow traceback is ', traceback.print_exc()) 

def getTable(strQ :str):
    try:
        cnxn=pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-NH98228\HCSPL18;DATABASE=RMSE;UID=sa;PWD=sqlAdm_18')
        cursor = cnxn.cursor()
        cursor.execute(strQ)
        data = cursor.fetchall() 
        tableResult = pd.DataFrame.from_records(data, columns=[col[0] for col in cursor.description])    
        cnxn.close()
        return tableResult
        # from modelval.DAL.dboperations import dbops
        # objdb=dbops()
        # objdb.getTable(strQ)
    except Exception as e:
        print('getTable is ',e)
        print('getTable traceback is ', traceback.print_exc()) 

def getUserDept(request):
    try:        
        dept=getscalar("SELECT  Dept_Label   FROM  Department dept, Users u  where u.Dept_AID=dept.Dept_AID and u_name='"+str(request.session['username'])+"'")
        return JsonResponse({'dept':dept})
    except Exception as e:
        print('getUserDept is ',e)
        print('getUserDept traceback is ', traceback.print_exc()) 

def addICQQtns(request):
    try:
        
        return render(request, 'addICQQtns.html',{'sections':objmaster.getSections()})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc()) 


def addSection(request):
    try:   
        section =request.GET.get('section', 'False') 
        sectiondesc =request.GET.get('sectiondesc', 'False') 
        activests =request.GET.get('activests', 'False')      
        objmaster.addSection(section,sectiondesc,activests,str(request.session['uid']))
        return JsonResponse({'is_taken':True})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 

    
def addSub_Section(request):
    try:   
        section =request.GET.get('section', 'False') 
        sectiondesc =request.GET.get('sectiondesc', 'False') 
        activests =request.GET.get('activests', 'False')     
        secid =request.GET.get('secid', 'False')      
        objmaster.addSub_Section(secid,section,sectiondesc,activests,str(request.session['uid']))
        return JsonResponse({'is_taken':True})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 

def addSub_Sub_Section(request):
    try:   
        section =request.GET.get('section', 'False') 
        sectiondesc =request.GET.get('sectiondesc', 'False') 
        activests =request.GET.get('activests', 'False')    
        sub_secid =request.GET.get('sub_secid', 'False')      
        objmaster.addSub_Sub_Section(sub_secid,section,sectiondesc,activests,str(request.session['uid']))
        return JsonResponse({'is_taken':True})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 

def getSub_Sections(request):
    try:       
        sub_secid =request.GET.get('secid', 'False')      
        
        return JsonResponse({'subsections':objmaster.getSub_Sections(sub_secid)})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 


def getSub_Sub_Sections(request):
    try:       
        sub_secid =request.GET.get('secid', 'False')      
        
        return JsonResponse({'subsections':objmaster.getSub_Sub_Sections(sub_secid)})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 

def addSub_Sub_Sub_Section(request):
    try:   
        section =request.GET.get('section', 'False') 
        sectiondesc =request.GET.get('sectiondesc', 'False') 
        activests =request.GET.get('activests', 'False')    
        sub_secid =request.GET.get('sub_secid', 'False')      
        objmaster.addSub_Sub_Sub_Section(sub_secid,section,sectiondesc,activests,str(request.session['uid']))
        return JsonResponse({'is_taken':True})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 


def getSub_Sub_Sub_Sections(request):
    print("getSub_Sub_Sub_Sections")
    try:       
        sub_secid =request.GET.get('secid', 'False')      
        print("sub_secid",sub_secid)
        return JsonResponse({'subsections':objmaster.getSub_Sub_Sub_Sections(sub_secid)})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 


def add_question(request):
    try:
        
        added_by=request.session['uid'] 
        section=request.GET.get('section','False')
        sub_section=request.GET.get('sub_section','False')
        sub_sub_section=request.GET.get('sub_sub_section','False')
        sub_sub_sub_section=request.GET.get('sub_sub_sub_section','False')
        question=request.GET.get('question','False')
        api_url=getAPIURL()+"add_question/"       
        params={'section':section,
            'sub_section':sub_section,
            'uid':added_by,
            'sub_sub_section':sub_sub_section,
            'sub_sub_sub_section':sub_sub_sub_section,
            'question':question,
            } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(params),headers=header)         
        api_data=response.json()
        # print('data ',section,sub_section,sub_sub_section,sub_sub_sub_section,question)
        # if sub_section == '':
        #     sub_section=None
        # if sub_sub_section == '':
        #     sub_sub_section =None
        # if sub_sub_sub_section == '':
        #     sub_sub_sub_section =None      
        # question_obj=IcqQuestionMaster.objects.create(question_label=question,section_aid=section,sub_section_aid=sub_section,
        #                                               sub_sub_section_aid=sub_sub_section,sub_sub_sub_section_aid=sub_sub_sub_section,
        #                                               addedby=added_by,adddate=adddate)
        # print("saved")
        return JsonResponse({'is_taken':api_data['is_taken']})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc())      


from django.db.models import Q
def icq_ratings(request):
    print("icq_ratings",icq_ratings)
    try:
        if request.method=="POST":
            section=request.POST.get('section','False')
            sub_section=request.POST.get('sub_section','False')
            sub_sub_section=request.POST.get('sub_sub_section','False')
            sub_sub_sub_section=request.POST.get('sub_sub_sub_section','False')

            print(section,sub_section,sub_sub_section,sub_sub_sub_section)

            if sub_section == '' and sub_sub_section == '' and sub_sub_sub_section == '':
                print("session selected")
                question_obj_filter=IcqQuestionMaster.objects.filter(section_aid=section,sub_section_aid=None,sub_sub_section_aid=None,sub_sub_sub_section_aid=None) #exclude sub_section,sub_sub,sub_sub_sub = None
            elif sub_sub_section == '' and sub_sub_sub_section == '':
                print("sub section selected")
                #question_obj_filter=IcqQuestionMaster.objects.filter(Q(sub_section_aid=sub_section) | Q(section_aid=section)| Q(sub_sub_section_aid=None)| Q(sub_sub_sub_section_aid=None)) #exclude sub_sub,sub_sub_sub =None
                question_obj_filter=IcqQuestionMaster.objects.filter(Q(sub_section_aid=sub_section,sub_sub_section_aid=None,sub_sub_sub_section_aid=None)) #exclude sub_sub,sub_sub_sub =None
            elif sub_sub_sub_section == '':
                print("sub sub section selected")
                #question_obj_filter=IcqQuestionMaster.objects.filter(Q(sub_sub_section_aid=sub_sub_section) | Q(sub_section_aid=sub_section) | Q(section_aid=section)| Q(sub_sub_sub_section_aid=None)) #exclude sub_sub_sub = NOne
                question_obj_filter=IcqQuestionMaster.objects.filter(Q(sub_sub_section_aid=sub_sub_section,sub_sub_sub_section_aid=None)) #exclude sub_sub_sub = NOne

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
        return render(request,'addICQRatings.html',{'sections':objmaster.getSections(),'Qtns':objmaster.getAllICQQtnsAndRatings()})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc())  

def save_ratings(request):
    try:
        from datetime import datetime
        added_by=request.session['uid']
        adddate=datetime.now()
        question_id=request.GET.get('question_id')
        ratings_yes=request.GET.get('ratings_yes')
        ratings_no=request.GET.get('rating_no')
        doc_yes=request.GET.get('doc_yes')
        doc_no=request.GET.get('doc_no')
        print("question_id",question_id)
        if ratings_yes == '':
            ratings_yes="null"
        if ratings_no == '':
            ratings_no ="null"
        if doc_yes == '':
            doc_yes ="null" 
        if doc_no == '':
            doc_no ="null"       
        # question_master_id=IcqQuestionMaster.objects.get(question_aid=question_id)
        # question_rating_obj=IcqQuestionRating.objects.create(question_aid=question_master_id,rating_yes=ratings_yes,rating_no=ratings_no,
        #                                         doc_yes=doc_yes,doc_no=doc_no,addedby=added_by,adddate=adddate)
        objmaster.insertRatings(question_id,ratings_yes,ratings_no,doc_yes,doc_no)
        print('saved')
        return JsonResponse({'is_taken':True})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 

def ICQQtns(request):
    try: 
        sectionid =request.POST.get('ddlSection', '0')  
        api_url=getAPIURL()+"ICQQtns/"       
        data_to_save={ 
            'uid':request.session['uid'],} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()

        api_url_a=getAPIURL()+"ICQInherentRiskRatingAPI/"       
         
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response_a = requests.get(api_url_a,headers=header)
         
        api_data_a=response_a.json() 
        r1 = [i['ratings'] for i in api_data_a['rating_1']] 
        r2 = [i['ratings'] for i in api_data_a['rating_2']] 
        r3 = [i['Ratings'] for i in api_data_a['rating_3']] 
        
        return render(request, 'ICQQtns.html',{'canupdate':api_data['canupdate'],
                                               'sectionid':sectionid,'sections':api_data['sections'],
                                               'Qtns':api_data['Qtns'],'models':api_data['models'],
                                               'rating_1':r1,'rating_2':r2,
                                               'rating_3':r3})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def getICQSections(request):
    try:    
        api_url=getAPIURL()+"getICQSections/"       
        data_to_save={ 
            'uid':request.session['uid'],} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        response=response.json()
        return JsonResponse({'sections':response['sections']})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 

def getICQSecQtn(request):
    try:
        modelid =request.GET.get('ddlModel', 'False')  
        sectionid =request.GET.get('ddlSection', '0')  
        print('sectionid ',sectionid)
        return JsonResponse({'sections':objmaster.getICQQtns(request.session['uid'])})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def saveICQRatings(request):
    try: 
        colDataLst = request.POST['colDataLst']
        uid=request.session['uid']
        api_url=getAPIURL()+"saveICQRatings/"       
        data_to_save={'colDataLst':colDataLst,             
            'uid':request.session['uid'], } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        # json_colDataLst = json.loads(colDataLst)
        # objreg=Register()
        # for colval in json_colDataLst:
        #     print('col val is ',colval )
        #     objreg.insertICQRatings(colval["qtnId"],colval["ddl_yesno_"],colval["ddl_doc_"],colval["txt_comment_"],uid,objmaster.getmaxICQId())
            
        return JsonResponse({'is_taken':api_data['is_taken']})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def submitICQRatings(request):
    try: 
        # objreg.submitRatings( objmaster.getmaxICQId())
         
        api_url=getAPIURL()+"submitICQRatings/"       
        data_to_save={        
            'uid':request.session['uid'], } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        # objmaster.insert_notification(str(uid),'MRM-Head','ICQ','Rating Submitted',1)    
        return JsonResponse({'is_taken':api_data['is_taken']})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def ICQQuestions(request):
    try: 
        sectionid =request.POST.get('ddlSection', '0')  
        return render(request, 'ICQQuestions.html',{ 'Qtns':objmaster.getAllICQQtns()})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def ICQQtnsFinal(request):
    print("ICQQtnsFinal")
    try: 
        sectionid =request.POST.get('ddlSection', '0') 
        api_url=getAPIURL()+"ICQQtnsFinal/"       
         
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url,headers=header)
         
        api_data=response.json()

        api_url_a=getAPIURL()+"ICQInherentRiskRatingAPI/"       
         
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response_a = requests.get(api_url_a,headers=header)
         
        api_data_a=response_a.json() 
        r1 = [i['ratings'] for i in api_data_a['rating_1']] 
        r2 = [i['ratings'] for i in api_data_a['rating_2']] 
        r3 = [i['Ratings'] for i in api_data_a['rating_3']] 
        print("Qtns",api_data['Qtns'])
        
        return render(request, 'ICQQtnsFinal.html',
                      {'ICQRating':api_data['ICQRating'],
                       'sectionid':sectionid,
                       'sections':api_data['sections'],'Qtns':api_data['Qtns'],'rating_1':r1,'rating_2':r2,
                                               'rating_3':r3})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def getICQSectionsFinal(request):
    try:   
        api_url=getAPIURL()+"getICQSectionsFinal/"       
         
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url,headers=header)
         
        api_data=response.json()
        return JsonResponse({'sections':api_data['sections']})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 

def getICQSecQtnFinal(request):
    try:  
        api_url=getAPIURL()+"getICQSecQtnFinal/"       
         
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url,headers=header)
         
        api_data=response.json()
        return JsonResponse({'sections':api_data['sections']})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def saveICQRatingsFinal(request):
    try:       
  
        colDataLst = request.POST['colDataLst']
        uid=request.session['uid']
        # json_colDataLst = json.loads(colDataLst)
        # objreg=Register()
        # maxid=objmaster.getmaxICQId()
        # for colval in json_colDataLst:
        #     print('list is ' ,colval)
        #     objreg.updateICQRatingsFinal(colval["qtnId"],colval["ddl_yesno_"],colval["ddl_doc_"],colval["txt_comment_"],uid,maxid)
        api_url=getAPIURL()+"saveICQRatingsFinal/"       
        data_to_save={
            'colDataLst':colDataLst, 
            'uid':request.session['uid'], 
            } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()    
        return JsonResponse({'is_taken':api_data['is_taken']})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())


def showICQSetting(request):
    try: 
        tableResult =objdbops.getTable("select *,format(ICQS_EndDate,'MM/dd/yyyy') end_date from ICQ_Setting order by ICQS_AID desc") 
        users = tableResult.to_json(orient='index')
        users = json.loads(users)
        del tableResult
        return render(request, 'ICQSettingLst.html',{ 'actPage':'Departments','users':users})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def newICQSetting(request):
    try:   
        print('inside addICQSetting')
        return render(request, 'addICQSetting.html',{ 'actPage':'Add Department'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def addICQSetting(request):
    try: 
        icqnameVal=request.GET['icqname']  
        remarksVal=request.GET['remarks']  
        enddateVal=request.GET['enddate']
        userid=str(request.session['uid'])
        strQ="INSERT INTO ICQ_Setting (ICQS_Text ,ICQS_Remarks,ICQS_EndDate,AddedBy,AddDate,publish) "
        strQ += " VALUES('"+ icqnameVal.replace("'","''")+"','"+ remarksVal.replace("'","''")+"','"+ enddateVal +"','"+ userid +"',getdate(),0)"
        print(strQ)
        insertRow(strQ)
        return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})

def publushICQ(request):
    try:
        objmaster.publishICQ()
        return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print('publushICQ is ',e)
        print('publushICQ traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})

def newquerybuilder(request):
    try:  
        from pandas.api.types import is_numeric_dtype,is_float_dtype,is_integer_dtype,is_string_dtype,is_number    
        file_id=find_max_file_id(request.session['vt_mdl'])   
        src_file_obj = collection.find({'file_id':file_id})          
        df =pd.DataFrame(list(src_file_obj)) 
        df=df.drop("_id",axis=1)
        # df = df.replace(('nan', 'NA'))
        # df = df.fillna('')
        gridDttypes=[]
        dttypes = dict(df.dtypes)
        # print(dttypes)
        for key, value in dttypes.items():
            print(is_numeric_dtype(df[key]),key,value, is_number(df[key]),is_float_dtype(df[key]),is_integer_dtype(df[key]),is_string_dtype(df[key]))
            valueLst=[]
            minmax=[]
            try:
                if str(df[key][0]).isdigit() or isinstance(df[key][0],float):
                    if  isinstance(df[key][0],float):
                        value="double"  
                        minmax = [df[key].min() , df[key].max()] 
                    else:
                        value="integer"  
                        minmax = [df[key].min() , df[key].max()] 
                elif value=="bool":
                    value="boolean"
                    valueLst=['True','False','Null']
                else:
                    value="string"
                    if len(df[key].unique())<=200: 
                        valueLst=df[key].astype(str).unique().tolist() 
            except Exception as e: 
                if value=="bool":
                    value="boolean"
                    valueLst=['True','False','Null']
                else:
                    value="string"
                    if len(df[key].unique())<=200: 
                        valueLst=df[key].astype(str).unique().tolist() 
             
            gridDttypes.append({'colName': key, 'dataType': str(value),'valueLst':valueLst,'minmax':minmax}) 
        return render(request, 'querybuilder.html',{ 'actPage':'Query Builder','dictionary':{},'columns':gridDttypes,'file_id':file_id})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())



def query_filter(request):
    # print("request only",request)
    request_data=request.GET.get('objectDataString',0)
    data=json.loads(request_data)  
    print("data",type(data))
    file_id=find_max_file_id(request.session['vt_mdl'])
  
    src_file_obj = collection.find({'file_id': int(file_id)})
    df =  pd.DataFrame(list(src_file_obj))

    # request_data = {x:request.GET.get(x) for x in request.GET.keys()}
    # print('request_data ',request_data) 
    # filter_data = list(request_data.keys())
    # print("filter_data",filter_data)
    # filter_data2 = filter_data[0]
    # print('filter_data2 ',filter_data2)
    confirm_obj=collection.find(json.loads(data)) #({list(i.keys())[0]:i[a]})
    result=[]
    for i in confirm_obj:
        result.append(i) 
    return JsonResponse({"isvalid":"true","all_count":len(df),"filter_cnt":len(result)}) 

def SpecificSong(request):  
    context = {'song':'/static/media/test.mp3'}
    return render(request,'specificsong.html',context)
 

def vt(request):
    try: 
        mdlLst=objvalidation.getVTModels(request.session['uid'])
        
        return render(request, 'welcome.html',{'mdlLst':mdlLst})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 

 
    
    
def find_max_file_id(mdlid=""):
    print("find_max_file_id")
    src_file_obj = collection_file_info.find({'Mdl_Id':mdlid})
    df =  pd.DataFrame(list(src_file_obj))
    print("dataframe is ",len(df)) 
    if len(df)>0: 
        file_id=int(df['file_id'].max())
    else:
        file_id=1 #changed by nilesh on 11.4.23
    return file_id

def Query_builder_filter(request):
    try:  
        request_data=request.GET.get('objectDataString',0)
        data=json.loads(request_data)  
        print('request_data ',request_data)
        user_addedby = request.session['uid'] 
        filter_obj = QueryBuilderFilter(rule = str(json.loads(data)),addedby = user_addedby,addon = date.today(),model_id =request.session['vt_mdl'],rulename = request.GET['label'])
        filter_obj.save()
        print("filter obj save successfully")
        return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 

def PdfSummary(request):
    try:
        pdfDir = os.path.join(BASE_DIR, 'static/pdfsummary/')        
        title=".pdf Summarizer"
        msg=""
        name=""
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile'] 
            name = myfile.name  
            savefile_name = pdfDir + name
            fs = FileSystemStorage()  
            if os.path.exists(savefile_name):
                os.remove(savefile_name)
            fs.save(savefile_name, myfile)
            title=".pdf Summarizer for "+name 
            objrmse.insertPdfFileData(name,request.session['uid'])
            msg="File uploded sucessfully."
        return render(request,'pdfsummary.html',{'msg':msg,'title':title,'file_name':name,'uploaded_files':objrmse.getDocById(str(request.session['uid']))})
    except Exception as e:
        print('PdfSummary is ',e)
        print('PdfSummary traceback is ', traceback.print_exc()) 
        return JsonResponse({"isvalid":"false"})

def savePDFResp(request):
    fileid=request.GET.get('fileid','')
    query=request.GET.get('query','')
    resp=request.GET.get('resp','')
    respLbl=request.GET.get('respLbl','')
    objrmse.insertPdfResp(fileid,request.session['uid'],respLbl.replace("'","''"), resp.replace("'","''"),query.replace("'","''"))
    return JsonResponse({"isvalid":True}) 

    
def pdfsummaryresp(request):  
    try:  
        query=request.GET.get('txtquery','') 
        # api_url="http://127.0.0.1:8002/api/getAns/"           
        # data_to_save={ 
        #     'question':query} 
        # header = {
        # "Content-Type":"application/json"
        # }
        # response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
         
        # api_data=response.json()
        from gradio_client import Client,file
        client = Client("http://127.0.0.1:8001/")
        
         
        # result = client.predict(
        #         ["C:/Django/pdf_chatbot/media/occ.pdf"],	# List[filepath]  in 'Upload File(s)' Uploadbutton component
        #         api_name="/_upload_file"
        # )
        # print(result)
 
        result = client.predict(
                api_name="/_list_ingested_files_1"
        )
        print(result)
        # client.file("C:/Django/pdf_chatbot/media/Weatherwax_Epstein_Hastie_Solution_ManualElementsof statisticalLearning.pdf")
        result = client.predict(
                 query,	# str  in 'Message' Textbox component
                "Query Files",	# Literal['Query Files', 'Search Files', 'LLM Chat (no context from files)']  in 'Mode' Radio component
                [file("https://github.com/gradio-app/gradio/raw/main/test/test_files/sample_file.pdf")],	# List[filepath]  in 'Upload File(s)' Uploadbutton component               
                "",	# str  in 'System Prompt' Textbox component
                api_name="/chat"
        )
        print('api output',result) 
        return JsonResponse({"response":result,'aiaudio':''})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 


def codereview(request):
 
    import openai
         
    openai.api_key = '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'

    # Extract the user's code from POST data
    user_code =  "string strBookIDs = string.Empty;\
            string strBookPrice = string.Empty;\
            string strBookType = string.Empty;\
            string strBookNames = string.Empty;\
            string strFree = string.Empty;\
            string strDeduction = string.Empty;\
            double dblBookPrice = 0;\
            double dblEffectiveBookPrice_Text = 0;\
            double dblEffectiveBookPrice_Sahayika = 0;\
            double dblEffectiveBookPrice_Project = 0;\
            int iBookC_Text = 0;\
            int iBookC_Sahayika = 0;\
            int iBookC_Project = 0;\
            double dblComm = 0;\
            double dblForText = 0;\
            double dblForSahayika = 0;\
            double dblForProject = 0;\
            dblForText = Convert.ToDouble(txtTextBook.Text.Trim());\
            dblForSahayika = Convert.ToDouble(txtSahayika.Text.Trim());\
            dblForProject = Convert.ToDouble(txtProject.Text.Trim());\
            dbldblAlloted_Text = dbleff * (dblForText / 100);\
            dbldblAlloted_Sahayika = dbleff * (dblForSahayika / 100);\
            dbldblAlloted_Project = dbleff * (dblForProject / 100);\
            foreach (DataGridViewRow drSel in dgvBooks.Rows){\
            bool isSelected = Convert.ToBoolean(drSel.Cells[checkBoxColumn].Value);\
            if (isSelected)  {\
                    strBookIDs += "," + drSel.Cells[1].Value.ToString();\
                    strBookPrice += "," + drSel.Cells[4].Value.ToString();\
                    strBookType += "," + drSel.Cells[6].Value.ToString();\
                    strBookNames += "," + drSel.Cells[3].Value.ToString();\
                    strFree += "," + drSel.Cells[7].Value.ToString();\
                    if (chkStanCom.Checked==true && chkFullCom.Checked==false)\
                    {\
                        dblComm = Convert.ToDouble(drSel.Cells[8].Value.ToString());\
                        strDeduction += "," + dblComm.ToString();\
                    }\
                    if (chkFullCom.Checked)\
                    {\
                        dblComm = Convert.ToDouble(drSel.Cells[8].Value.ToString());\
                        dblComm += Convert.ToDouble(drSel.Cells[9].Value.ToString());\
                        strDeduction += "," + dblComm.ToString();\
                    }\
                //dblEffectiveBookPrice += Convert.ToInt32(Convert.ToDouble(drSel.Cells[4].Value.ToString()) * (1 - dblComm / 100));\
                }\
            }\
            arrbookID = strBookIDs.Split(',');\
            arrbookPrice = strBookPrice.Split(',');\
            arrbookType = strBookType.Split((',');\
            arrbookName = strBookNames.Split("","");\
            arrFree = strFree.Split(',');\
            arrDeduction = strDeduction.Split(',');\
            if (dblEffectiveBookPrice_Text != 0)\
                iBookC_Text = Convert.ToInt(Math.Floor(dbldblAlloted_Text / dblEffectiveBookPrice_Text));      //dblBookPrice\
            if (dblEffectiveBookPrice_Sahayika != 0)\
                iBookC_Sahayika = Convert.ToString(Math.Floor(dbldblAlloted_Sahayika / dblEffectiveBookPrice_Sahayika));\
            if (dblEffectiveBookPrice_Project != 0)\
            return iBookC_Text + "":"" + iBookC_Sahayika + "":"" + iBookC_Project;"

    # Set the messages for the conversation
    messages = [
        {"role": "system", "content": "You are a helpful assistant that translates Python code into English."},
        {"role": "user", "content": f"Translate the following Python code into English: \n\n{user_code}"},
    ]

    # Make a request to the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    # Extract the response
    gpt_response = response['choices'][0]['message']['content']
    print(gpt_response)
    # Return as JSON
    return JsonResponse({
        'message': gpt_response
    })

def uploadDecommDoc(request): #to be updated on server
    try:
        mdl_id = request.POST.get('mdl_id','none')
        comment = request.POST.get('comment','none') 
        decommSts= request.POST.get('decommSts','none') 
        destination_path = os.path.join(BASE_DIR, 'static\\document_files\\'+mdl_id+'\\')
        mrm_head=objmaster.getMRMHead()
        thread_id=""
        notification_trigger=""
        notification_from=""
        notification_to=""
        if str(decommSts)=="0":
            decommSts="1"
            notification_trigger= "Model decommission requested for model - " + mdl_id
            notification_from=str(request.session['uid'])
            notification_to=str(mrm_head)
            objmaster.insertActivityTrail(mdl_id,"5",notification_trigger + os.linesep +comment,notification_from,request.session['accessToken'])
        elif str(decommSts)=="1":
            decommSts=2
            notification_trigger= "Model Id "+ mdl_id + " decommissioned "
            notification_from=str(request.session['uid']) 
            notification_to=objmaster.getMdlOwner(mdl_id)
            objmaster.insertActivityTrail(mdl_id,"6",notification_trigger + os.linesep+comment,notification_from,request.session['accessToken'])
        if request.method == 'POST':  
            # myfile = request.FILES['myfile']
            filename = request.POST.get('filenm','none') 
            files = request.FILES
            myfile = files.get('filename','None') 
            if myfile=="None":
                res = JsonResponse({'data':'Invalid Request'})                
            else:     
                fs = FileSystemStorage()
                savefile_name = destination_path + mdl_id+'_'+filename
                if os.path.exists(savefile_name):
                    os.remove(savefile_name)
                fs.save(savefile_name, myfile)       
                
            if myfile=="None" :
                objreg.deCommModel(mdl_id,comment,"",decommSts)                
                objmaster.insert_notification(notification_from,notification_to,"Model",notification_trigger,1)
                thread_id= objmaster.thread_creation(request.session['uid'],mrm_head)
                
            elif comment=="":
                objreg.deCommModel(mdl_id,"",filename,decommSts) 
                objmaster.insert_notification(notification_from,notification_to,"Model",notification_trigger,1)
                thread_id= objmaster.thread_creation(request.session['uid'],mrm_head)
            elif comment!="" and  myfile!="None" :
                objreg.deCommModel(mdl_id,comment,filename,decommSts) 
                objmaster.insert_notification(notification_from,notification_to,"Model",notification_trigger,1)
                thread_id= objmaster.thread_creation(request.session['uid'],mrm_head)

        res = JsonResponse({"is_taken": True,"from":str(notification_from),"to":str(notification_to),"thread_id":thread_id,"notification_trigger":notification_trigger})           
        return res   
    except Exception as e:
        print('uploaddecomm is ',e)
        print('uploaddecomm traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":False})

def checkPendingTasksIssues(request): 
    try:
        mdl_id = request.GET.get('mdl_id','none')
        api_url=getAPIURL()+"checkPendingTasksIssues/"       
        data_to_save={ 
            'mdl_id':mdl_id} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        return JsonResponse({"checkPending":api_data['checkPending'],"decommdoc":api_data['decommdoc']})
    except Exception as e:
        print('uploaddecomm is ',e)
        print('uploaddecomm traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})

def getDecommDoc(request):
    try:        
        mdl_id = request.GET.get('mdl_id','none')
        return JsonResponse({"decommdoc":objreg.getDecommDoc(mdl_id)})
    except Exception as e:
        print('uploaddecomm is ',e)
        print('uploaddecomm traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})



def QtnsResp(request):
    try: 
        api_url=getAPIURL()+"QtnsResp/"       
        data_to_save={ 
            'uid':request.session['uid']} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        if(api_data['is_mrm']=="1"):
            return render(request,'chat_mrm.html',{'mdl_id':api_data['mdl_id']})
        else:
            return render(request,'chat.html',{'mdl_id':api_data['mdl_id']})
    except Exception as e:
        print('QtnsResp is ',e)
        print('QtnsResp traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})

def getModelQtnBySrc(request):
    try:     
        mdl_id = request.GET.get('mdl_id','none')
        api_url=getAPIURL()+"getModelQtnBySrc/"       
        data_to_save={ 
            'mdl_id':mdl_id} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        return JsonResponse({"Qtns":api_data['Qtns']})
    except Exception as e:
        print('uploaddecomm is ',e)
        print('uploaddecomm traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})

def getQtnResp(request):
    try:        
        mdl_id = request.GET.get('mdl_id','none')
        qtn_id = request.GET.get('qtn_id','none')
        api_url=getAPIURL()+"getQtnResp/"       
        data_to_save={ 
            'mdl_id':mdl_id,
            'qtn_id':qtn_id,
            'uid':request.session['uid']
            } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        print(api_data)
        return JsonResponse({"Qtns":api_data['Qtns']})
    except Exception as e:
        print('uploaddecomm is ',e)
        print('uploaddecomm traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})


def insertQtnResp(request):
    try:        
        mdl_id = request.GET.get('mdl_id','none')
        qtn_id = request.GET.get('qtn_id','none')
        comments = request.GET.get('comments','none')
        isupdate = request.GET.get('isupdate','0')
        Response_id = request.GET.get('Response_id','0')
        api_url=getAPIURL()+"insertQtnResp/"       
        data_to_save={'mdl_id':mdl_id,
            'qtn_id':qtn_id,
            'uid':request.session['uid'],
            'comments':comments,
            'isupdate':isupdate,
            'Response_id':Response_id,
            } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        
        return JsonResponse({"is_taken":api_data['is_taken']})
    except Exception as e:
        print('uploaddecomm is ',e)
        print('uploaddecomm traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})

def getQtnRespById(request):
    try:               
        Response_id = request.GET.get('Response_id','0')        
        api_url=getAPIURL()+"getQtnRespById/"       
        data_to_save={ 
            'Response_id':Response_id, 
            } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        return JsonResponse({"is_taken":True,'comment':api_data['comment']})
    except Exception as e:
        print('uploaddecomm is ',e)
        print('uploaddecomm traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})


def mmrkasRead(request):
    try:
        notification_id = request.GET.get('notification_id','0')  
        return JsonResponse({'markread':objreg.markasRead(notification_id)})
    except Exception as e:
        print('getMdlInfoById is ',e)
        print('getMdlInfoById traceback is ', traceback.print_exc())

def Questions(request):
    try: 
        return render(request, 'Questions.html',{ 'Qtns':objmaster.getAllQtns()})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def QuestionsAllUsers(request):
    try: 
        api_url=getAPIURL()+"QuestionsAllUsers/"    
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, headers=header)         
        api_data=response.json()
        return render(request, 'QuestionsAllUsers.html',{ 'Qtns':api_data['Qtns']})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def addQtns(request):
    try:        
        return render(request, 'addQtns.html',{'sections':objmaster.getQuesSections()})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc()) 

def addQtnsAllUsers(request):
    try:        
        api_url=getAPIURL()+"addQtnsAllUsers/"       
       
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, headers=header)  
         
        api_data=response.json()
        return render(request, 'addQtnsAllUsers.html',{'sections':api_data['sections']})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc()) 

def getQues_Sub_Sections(request):
    try:       
        sub_secid =request.GET.get('secid', 'False')  
        return JsonResponse({'subsections':objmaster.getQues_Sub_Sections(sub_secid)})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 

def addQuesSection(request):
    try:   
        stype =request.GET.get('stype', 'False') 
        section =request.GET.get('section', 'False') 
        sectiondesc =request.GET.get('sectiondesc', 'False') 
        activests =request.GET.get('activests', 'False')      
        objmaster.addQuesSection(stype,section,sectiondesc,activests,str(request.session['uid']))
        return JsonResponse({'is_taken':True})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 

    
def addQuesSub_Section(request):
    try:   
        section =request.GET.get('section', 'False') 
        sectiondesc =request.GET.get('sectiondesc', 'False') 
        activests =request.GET.get('activests', 'False')     
        secid =request.GET.get('secid', 'False')    
        api_url=getAPIURL()+"addQuesSub_Section/"       
        params={'section':section,
            'sectiondesc':sectiondesc,
            'uid':request.session['uid'],
            'activests':activests,
            'secid':secid} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(params),headers=header)  
         
        api_data=response.json()  
        # objmaster.addQuesSub_Section(secid,section,sectiondesc,activests,str(request.session['uid']))
        return JsonResponse({'is_taken':api_data['is_taken']})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 

def addQuesSub_Sub_Section(request):
    try:   
        section =request.GET.get('section', 'False') 
        sectiondesc =request.GET.get('sectiondesc', 'False') 
        activests =request.GET.get('activests', 'False')    
        sub_secid =request.GET.get('sub_secid', 'False')      
        objmaster.addQuesSub_Sub_Section(sub_secid,section,sectiondesc,activests,str(request.session['uid']))
        return JsonResponse({'is_taken':True})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 

def getQuesSub_Sections(request):
    try:       
        sub_secid =request.GET.get('secid', 'False')     
        return JsonResponse({'subsections':objmaster.getQuesSub_Sections(sub_secid)})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 


def getQuesSub_Sub_Sections(request):
    try:       
        sub_secid =request.GET.get('secid', 'False')    
        return JsonResponse({'subsections':objmaster.getQuesSub_Sub_Sections(sub_secid)})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 

def addQuesSub_Sub_Sub_Section(request):
    try:   
        section =request.GET.get('section', 'False') 
        sectiondesc =request.GET.get('sectiondesc', 'False') 
        activests =request.GET.get('activests', 'False')    
        sub_secid =request.GET.get('sub_secid', 'False')      
        objmaster.addQuesSub_Sub_Sub_Section(sub_secid,section,sectiondesc,activests,str(request.session['uid']))
        return JsonResponse({'is_taken':True})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 


def getQuesSub_Sub_Sub_Sections(request):
    print("getSub_Sub_Sub_Sections")
    try:       
        sub_secid =request.GET.get('secid', 'False')      
        print("sub_secid",sub_secid)
        return JsonResponse({'subsections':objmaster.getQuesSub_Sub_Sub_Sections(sub_secid)})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 

def addQues_question(request):
    try:
        
        added_by=request.session['uid']
        adddate=datetime.now()
        section=request.GET.get('section','False')
        sub_section=request.GET.get('sub_section','False')
        sub_sub_section=request.GET.get('sub_sub_section','False')
        sub_sub_sub_section=request.GET.get('sub_sub_sub_section','False')
        question=request.GET.get('question','False')
        
        if sub_section == '':
            sub_section=None
        if sub_sub_section == '':
            sub_sub_section =None
        if sub_sub_sub_section == '':
            sub_sub_sub_section =None      
        question_obj=QuesQuestionMaster.objects.create(question_label=question,section_aid=section,sub_section_aid=sub_section,
                                                      sub_sub_section_aid=sub_sub_section,sub_sub_sub_section_aid=sub_sub_sub_section,
                                                      addedby=added_by,adddate=adddate)
        print("saved")
        return JsonResponse({'is_taken':True})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc())     


def addUserQues_question(request):
    try: 
        section=request.GET.get('section','False')
        sub_section=''#request.GET.get('sub_section','False')
        sub_sub_section=''#request.GET.get('sub_sub_section','False')
        sub_sub_sub_section=''#request.GET.get('sub_sub_sub_section','False')
        question=request.GET.get('question','False')
        
        if sub_section == '':
            sub_section=None
        if sub_sub_section == '':
            sub_sub_section =None
        if sub_sub_sub_section == '':
            sub_sub_sub_section =None      
        api_url=getAPIURL()+"addUserQues_question/"       
        params={'section':section,
            'question':question,
            'uid':request.session['uid']}  
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(params),headers=header)         
        api_data=response.json()
        return JsonResponse({'is_taken':api_data['is_taken']})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc())  

def allocate_questions(request): 
    try:                
        api_url=getAPIURL()+"allocate_questions/"       
        params={'utype':request.session['utype'],
            'vt_mdl':request.session['vt_mdl'],
            'uid':request.session['uid'],
            'ulvl':request.session['ulvl'],} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(params),headers=header)         
        api_data=response.json()
        return render(request,'allocate_ques.html',{'models':api_data['models'],'user':api_data['user'],
                                                    'Qtns':api_data['Qtns'],
                                                    'selectedMdl':request.session['vt_mdl']})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 



def get_Qtn_Section(request):
    try:   
        mdlid =request.GET.get('mdlid', 'False')  
        return JsonResponse({'is_taken':True,'sections':objmaster.get_Qtn_Section(mdlid)})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 

def save_Question_allocation(request):     
    mdlid =request.GET.get('mdlid', 'False')  
    section_aid = request.GET.getlist('section_aid[]')
    users = request.GET.getlist('users[]')
    # end_date = request_data['end_date'][6:] + "-" + request_data['end_date'][3:5] + "-" + request_data['end_date'][:2]
    for user, section_id in [(x,y) for x in users for y in section_aid]:
        allocate_obj = QuestionSectionAllocation(section_aid = section_id,allocated_to = user,end_date = None,model_id=mdlid)
        allocate_obj.save()
    return JsonResponse({"isvalid":"true"}) 

def getQues_Sections(request):
    try:       
        sub_secid =request.GET.get('secid', 'False')     
        return JsonResponse({'sections':objmaster.getQues_Sections(sub_secid)})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 


def edit_department(request,id): 
    try:
        depart_obj=Department.objects.get(dept_aid=id)   
        label=depart_obj.dept_label
        desc=depart_obj.dept_description
        is_mrm=depart_obj.is_mrm
        print("is_mrm",is_mrm)
        is_mrm_exists = ""
        if  is_mrm != 1:
            third_party_api_url = getAPIURL()+'department/'
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.get(third_party_api_url, headers=header)
            print("response department",json.loads(response.content))
            data = json.loads(response.content)
            for i in data:
                print(i['dept_ismrm'])
                if i['dept_ismrm'] == 1:
                    is_mrm_exists = "disabled"
                    break
                else:
                    is_mrm_exists = ""
        else:
            pass

        return render(request, 'adddepartment.html',{ 'actPage':'Edit Department','label':label,'desc':desc,'is_mrm':is_mrm,'is_mrm_exists':is_mrm_exists,'id':id})

    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())

def edit_user_cat(request,id): 
    try:
        user_cat_obj=UserCategory.objects.get(uc_aid=id)   
        user_type=user_cat_obj.uc_label
        user_level=user_cat_obj.uc_level
        user_desc=user_cat_obj.uc_description
        is_dept_head=user_cat_obj.is_dept_head
        activate_status=user_cat_obj.activestatus
        uc_level_sel=user_cat_obj.uc_level
        print("user_type",user_type)
        print("user_desc",user_desc)
        print("user_level",user_level)
        print("is_dept_head",is_dept_head)
        print("activate_status",activate_status)
        return render(request, 'newusercat.html',{ 'actPage':'Edit User Type','user_type':user_type,'user_level':user_level,'user_desc':user_desc,
                                                  'is_dept_head':is_dept_head,'activate_status':activate_status,'level':list(range(1, 6)),'uc_level_sel':uc_level_sel,'id':id,'isDisabled':'disabled'})

    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())    
 

def edit_user(request,id): 
    print("edit_user",id)
    print(request.session['uid'])
    try:
        tableResult =objdbops.getTable("SELECT   UC_AID  ,UC_Label  FROM User_Category where UC_Label <> 'Admin'  order by 2 ")
        users = tableResult.to_json(orient='index')
        users = json.loads(users)
        
        tableResult =objdbops.getTable("SELECT Dept_AID,Dept_Label FROM Department") 
        dept = tableResult.to_json(orient='index')
        dept = json.loads(dept)

        tableResult =objdbops.getTable("SELECT U_AID,U_Name FROM users where U_AID_BackUpFor is null order by 2") 
        backupfor = tableResult.to_json(orient='index')
        backupfor = json.loads(backupfor)

        user_obj=Users.objects.get(u_aid=id)
        u_name=user_obj.u_name
        print("u_name",u_name)
        u_depart_id=user_obj.dept_aid
        print("u_depart_id",u_depart_id)
        try:
            u_depart_name=Department.objects.get(dept_aid=u_depart_id).dept_label
        except Department.DoesNotExist:
            u_depart_name=None
        u_type_id=user_obj.uc_aid
        print("u_type_id",u_type_id.uc_aid)
        try:
            u_type=UserCategory.objects.get(uc_aid=u_type_id.uc_aid).uc_label
        except UserCategory.DoesNotExist:
            u_type=None    
        u_first_name=user_obj.u_fname
        u_last_name=user_obj.u_lname
        u_email=user_obj.u_email
        u_status=user_obj.activestatus
        reportsto=user_obj.u_reportto
        try:
            reports_to_user=Users.objects.get(u_aid=reportsto).u_name
        except Users.DoesNotExist:
            reports_to_user = None
        # reports_to_user=Users.objects.get(u_aid=reportsto).u_name
        # if reportsto
        
        BackUpFor_UID=user_obj.U_AID_BackUpFor
        IfBackupUser=False
        BackUpFor_User=''
        DisplayBackUp='none'
        print('BackUpFor_UID ',BackUpFor_UID)
        if(BackUpFor_UID!=None):
            IfBackupUser=True
            DisplayBackUp='block'
            tableResult=objdbops.getTable("SELECT U_AID,U_Name FROM users where U_AID='"+ str(BackUpFor_UID) +"'")            
            BackUpFor_User= tableResult["U_Name"].values[0] 
        return render(request, 'adduser.html',{'u_name':u_name,'u_depart_name':u_depart_name,'u_depart_id':u_depart_id,'u_type':u_type,
                                               'u_type_id':u_type_id,'u_first_name':u_first_name,'id':id,'reportsto':reportsto,'reports_to_user':reports_to_user,
                                               'u_last_name':u_last_name,'u_email':u_email,'u_status':u_status,'utype':users,'dept':dept,'isDisabled':'disabled',
                                               'backupfor':backupfor,'IfBackupUser':IfBackupUser,'BackUpFor_UID':BackUpFor_UID,'BackUpFor_User':BackUpFor_User,'DisplayBackUp':DisplayBackUp})

    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())
        print("edit_user",id)
    try:
        tableResult =objdbops.getTable("SELECT   UC_AID  ,UC_Label  FROM User_Category where UC_Label <> 'Admin'  order by 2 ")
        users = tableResult.to_json(orient='index')
        users = json.loads(users)
        
        tableResult =objdbops.getTable("SELECT Dept_AID,Dept_Label FROM Department") 
        dept = tableResult.to_json(orient='index')
        dept = json.loads(dept)

        user_obj=Users.objects.get(u_aid=id)
        u_name=user_obj.u_name
        print("u_name",u_name)
        u_depart_id=user_obj.dept_aid
        print("u_depart_id",u_depart_id)
        u_depart_name=Department.objects.get(dept_aid=u_depart_id).dept_label
        u_type_id=user_obj.uc_aid
        print("u_type_id",u_type_id.uc_aid)
        u_type=UserCategory.objects.get(uc_aid=u_type_id.uc_aid).uc_label
        u_first_name=user_obj.u_fname
        u_last_name=user_obj.u_lname
        u_email=user_obj.u_email
        u_status=user_obj.activestatus
        reportsto=user_obj.u_reportto
        print('reportsto ',reportsto)
        if(reportsto == None):
            reports_to_user=""
        else:
            reports_to_user=Users.objects.get(u_aid=reportsto).u_name
        
        print("u_first_name",u_first_name)
        print("u_last_name",u_last_name)
        print("u_email",u_email)
        print("u_status",u_status)
        print("u_type",u_type)
        print("reportsto",reportsto)
        print("reports_to_user",reports_to_user)

        return render(request, 'adduser.html',{'u_name':u_name,'u_depart_name':u_depart_name,'u_depart_id':u_depart_id,'u_type':u_type,
                                               'u_type_id':u_type_id,'u_first_name':u_first_name,'id':id,'reportsto':reportsto,'reports_to_user':reports_to_user,
                                               'u_last_name':u_last_name,'u_email':u_email,'u_status':u_status,'utype':users,'dept':dept,'isDisabled':'disabled'})

    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())

def insertQtnAnsr(request):
    try:        
        mdl_id = request.GET.get('mdl_id','none')
        qtn_id = request.GET.get('qtn_id','none')
        Ansr = request.GET.get('Ansr','none') 
        api_url=getAPIURL()+"insertQtnAnsr/"       
        params={'mdl_id':mdl_id,
            'qtn_id':qtn_id,
            'Ansr':Ansr,
            'uid':str(request.session['uid'])} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(params),headers=header)
         
        api_data=response.json()
        # objrmse.insertAnsr(mdl_id,qtn_id,str(request.session['uid']),Ansr)
        return JsonResponse({"is_taken":api_data['is_taken']})
    except Exception as e:
        print('uploaddecomm is ',e)
        print('uploaddecomm traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})

def getQtnAns(request):
    try:
        mdl_id = request.GET.get('mdl_id','none')
        qtn_id = request.GET.get('qtn_id','none')  
        api_url=getAPIURL()+"getQtnAns/"       
        params={'mdl_id':mdl_id,
            'qtn_id':qtn_id} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(params),headers=header)
         
        api_data=response.json()
        return JsonResponse({"is_taken":api_data['is_taken'],'ans':api_data['ans']})
    except Exception as e:
        print('uploaddecomm is ',e)
        print('uploaddecomm traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})

# def rmse_calendar(request):    
#     api_url=getAPIURL()+"getTasks/"   
#     mdl_id = request.GET.get('mdl_id','')    
#     data_to_save={'uid':request.session['uid'] ,'mdl_id':mdl_id} 
#     header = {
#     "Content-Type":"application/json",
# 	    'Authorization': 'Token '+request.session['accessToken']
#     }
#     response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
#     api_data=response.json() 
#     context={'all_data_lst':api_data['all_data_lst'],'taskList':api_data['taskList']}    
#     return render(request,'rmse_calendar1.html',context)


# def rmse_calendar_issue(request):
#     api_url=getAPIURL()+"getIssue/"       
#     mdl_id = request.GET.get('mdl_id','')    
#     data_to_save={'uid':request.session['uid'] ,'mdl_id':mdl_id} 
#     header = {
#     "Content-Type":"application/json",
# 	    'Authorization': 'Token '+request.session['accessToken']
#     }
#     response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
#     api_data=response.json() 
#     context={'all_data_lst':api_data['all_data_lst'],'issueList':api_data['mdldata']}       
#     return render(request,'rmse_calendar_issue.html',context)  


def getMdlQtnsBySec(request):
    api_url=getAPIURL()+"getMdlQtnsBySec/"       
    data_to_save={'mdl_id':request.GET.get('mdl_id','False'),
    'section': request.GET['section']} 
    header = {
    "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
    api_data=response.json()  
    context={'Qtns':api_data['Qtns'],'end_date':api_data['end_date'],'section_id':api_data['section_id']}       
    return JsonResponse(context)

def modelfields(request): 
    fields_obj = ModelsFields.objects.all()
    return render(request, 'modelfields.html',{'actPage':'Model Fields','fields_obj':fields_obj})

def updateFields(request):
    print("request data",request.GET)
    colDataLst = request.GET['datalist'] 
    print("data list",json.loads(colDataLst))
    for i in json.loads(colDataLst):
        print("aid",i['AID'])
        update_obj = ModelsFields.objects.filter(field_id = int(i['AID'])).update(field_label = i['fieldlbl'],is_mandatory = i['mandatory'],is_visible = i['visible'])    
    return JsonResponse({'istaken':'true'})

def error_saving(request,data):
    print("data print",data)
    file = open('logs.txt', 'w')
    file.write(str(data))
    file.close()
    print("file save")
    # return redirect(request,'error.html')
    
def Authorization(request,ucaid,resource_id): 
    if(str(objmaster.isAutherized(ucaid,resource_id)) =="0"): 
        return render(request, 'blank.html',{'msg':'You are not authorized to access this utility.'})
    
def editregmodel(request): 
    try:
        id= request.GET['mdl_id'] 
        status=0
        expPrdDt=''
        overview_obj = MdlOverview.objects.get(mdl_id = id)
        if TempMdlOverview.objects.filter(mdl_id=id).exists():
            status=2
        else:
            status=1
        if overview_obj.func != None:
            func = ModelFunctionMaster.objects.get(mdl_fncn_aid = overview_obj.func)
            func_label = func.mdl_fncn_label
            func_id = func.mdl_fncn_aid
        else: 
            func = ''
            func_label = ''
            func_id = ''

        expPrdDt=overview_obj.txtPrdDt
        department = Department.objects.get(dept_aid = overview_obj.department)
        model_source = ModelSourceMaster.objects.get(mdl_scr_aid = overview_obj.mdl_source)
         
        if overview_obj.mdl_type != 0:
            model_type = ModelTypeMaster.objects.get(mdl_type_aid = overview_obj.mdl_type)
        else:
            model_type = ''
        
        if overview_obj.prctaddr != 0:
            prd_addr = PrdAddrMaster.objects.get(prd_addr_aid = overview_obj.prctaddr)
        else:
            prd_addr = ''
        if overview_obj.usgfreq == 1:

            frequency = 'High'
        else:
            frequency = 'Medium'

        model_risk_obj = MdlRisks.objects.get(mdl_id=id)
        Mdl_depndncy_obj = MdlDependencies.objects.filter(mdl_id=id)
         
        if model_risk_obj.mdl_risks != '':
            model_risk = MdlRiskMaster.objects.get(mdl_risk_aid = model_risk_obj.mdl_risks)
        else:
            model_risk = ''
        if model_risk_obj.intr_risk != '':
            intr_risk = IntrinsicMaster.objects.get(intrinsic_aid = model_risk_obj.intr_risk)
        else:
            intr_risk = ''
        if model_risk_obj.reliance != '':
            reliance = RelianceMaster.objects.get(reliance_aid = model_risk_obj.reliance)
        else:
            reliance = ''
        if model_risk_obj.materiality != '':
            materiality = MaterialityMaster.objects.get(materiality_aid = model_risk_obj.materiality)
        else:
            materiality = ''
        for Mdl_depndncy in Mdl_depndncy_obj:
            if Mdl_depndncy.upstrmmdl != '':
                upstream = Mdl_depndncy.upstrmmdl#MdlUpstream.objects.get(mdl_upstream_aid = Mdl_depndncy.upstrmmdl)
            else:
                upstream = ''
            if Mdl_depndncy.dwstrmmdl != '':
                dwnstream =  Mdl_depndncy.dwstrmmdl#MdlDwstream.objects.get(mdl_dwstream_aid = Mdl_depndncy.dwstrmmdl)
            else:
                dwnstream = ''
        api_url=getAPIURL()+"getMdlDetailsById/"       
        data_to_save={
            'mdl_id':id} 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()  

        Owner=api_data['Owner']

        Developer=api_data['Developer']#objMdlRelvPern.getRelevantPersonal(mdl_id,'Developer')

        User=api_data['User']#objMdlRelvPern.getRelevantPersonal(mdl_id,'User')

        PrdnSupport=api_data['PrdnSupport']#objMdlRelvPern.getRelevantPersonal(mdl_id,'PrdnSupport')
        Mdl_Func=objreg.getMdlFunc()
        Mdl_Src = objreg.getMdl_Src()
        Mdl_Type =objreg.getMdl_Type() 
        
        Mdl_Usage_Frq=  objreg.getMdl_Usage_Fre()
    
        Prd_Addr = objreg.getPrd_Addr() 

        Mdl_Risk = objreg.getMdl_Risk()  

        Intrinsic = objreg.getIntrinsic()  

        Materiality = objreg.getMateriality()        
    
        Reliance = objreg.getReliance()  

        Mdl_Owners =objreg.getUsers(request.session['dept'],2)      

        Mdl_Validators =objreg.getUsers(request.session['dept'],3)         

        Mdl_Devs =objreg.getUsersByType('Data Scientist')

        Upstr_Model=objreg.getMdlUpstrem(request.session['uid'],id)

        Dwstr_Model=objreg.getMdlUpstrem(request.session['uid'],id) #objreg.getMdlDwStream()
  
        Motr_Freq=objreg.getMontrFreq()  
    
        return render(request, 'editregistermodel.html',{'status':status, 'actPage':'Edit Model','department':department.dept_label,
                    "func":func_label,"func_id":func_id,'Mdl_Func':Mdl_Func,'reg_date':overview_obj.reg_dt.strftime('%m/%d/%Y'),'mdl_id':overview_obj.mdl_id,'overview_obj':overview_obj,'Mdl_Src':Mdl_Src,'mdl_source':model_source,'Mdl_Type':Mdl_Type,'model_type':model_type,'Prd_Addr':Prd_Addr,"prd_add":prd_addr,'Mdl_Usage_Frq':Mdl_Usage_Frq,'frequency':frequency,'Reliance':Reliance,
        'Materiality':Materiality,'Intrinsic':Intrinsic,'Mdl_Risk':Mdl_Risk,'model_risk_obj':model_risk_obj,
        'model_risk':model_risk,'intr_risk':intr_risk,'reliance':reliance,'materiality':materiality,'Mdl_Owners':Mdl_Owners,
        'Mdl_Devs':Mdl_Devs,'Mdl_Validators':Mdl_Validators,'Upstr_Model':Upstr_Model,'Dwstr_Model':Dwstr_Model,
        'upstream':upstream,'dwnstream':dwnstream,'Motr_Freq':Motr_Freq,'expPrdDt':expPrdDt.strftime('%m/%d/%Y') if expPrdDt != None else '','modelDocs':objvalidation.getModelDocs(id),
        'Owner':Owner,'Developer':Developer,'PrdnSupport':PrdnSupport,'User':User})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 


def convrt_to_dictionary(model,mdl_id):
    obj1 = model.objects.filter(mdl_id=mdl_id).values()
    obj2 = pd.DataFrame(obj1)
    dictionary = obj2.to_dict('records')[0]
    return dictionary

def file_upload(request,filenm,filename,mdl_id):
    filename_a = request.POST.get(filenm,'none')
    print(' filename ',filename_a)
    files = request.FILES
    myfile = files.get(filename, None)
    print('myfile ',myfile,' filename ',filename_a)
    if filename_a != None and myfile != None:
        fs = FileSystemStorage() 
        filePath=os.path.join(BASE_DIR, "static/document_files/"+mdl_id+'/'+filename_a)
        if os.path.exists(filePath): 
          os.remove(filePath)
          print("remove filename",filePath)
        fs.save(os.path.join(BASE_DIR, "static/document_files/"+mdl_id+'/'+filename_a), myfile) 
    else:
        pass

def mdlrelv_personal(MdlId,UType,UIds,updatedby):
    # instance = objdbops.insertRow("DELETE FROM Mdl_Relevant_personnel WHERE Mdl_Id='"+MdlId+"' and u_type='"+UType+"'")
    # print("check instance",instance) 
    for ids in UIds:
        if ids != '':
            rel_per_obj  = TempMdlRelevantPersonnel(mdl_id=MdlId,u_type=UType,u_id=ids,updatedby=updatedby,updatedate=datetime.now())
            rel_per_obj.save()
            print("save------------------")

def updateregmodel(request):
    print("update reg model")
    try: 
        request_data = {x:request.POST.get(x) for x in request.POST.keys()}
        print("request_data---------------------------------90",type(request_data['mdl_id']))   
        dept_obj = Department.objects.get(dept_label=request_data['department']) 
        #Files Uploaded
        file_upload(request,'mdl_devlpmnt_filenm','mdl_devlpmnt_filename',request_data['mdl_id'])
        file_upload(request,'usr_manual_filenm','usr_manual_filename',request_data['mdl_id'])

        file_upload(request,'mdl_data_filenm','mdl_data_filename',request_data['mdl_id'])
        file_upload(request,'mdl_code_filenm','mdl_code_filename',request_data['mdl_id'])

        file_upload(request,'usr_acc_testing_filenm','usr_acc_testing_filename',request_data['mdl_id'])
        file_upload(request,'technical_manual_filenm','technical_manual_filename',request_data['mdl_id'])

        file_upload(request,'onbrd_docs_filenm','onbrd_docs_filename',request_data['mdl_id'])
        print("--------------file ok")
        #Model Overview  
        dict1_overview = convrt_to_dictionary(MdlOverview,request_data['mdl_id'])
        print("overview",dict1_overview)
        # overview_obj = MdlOverview.objects.filter(mdl_id=request_data['mdl_id']).update(department=dept_obj.dept_aid,func=request_data['function'],mdl_id=request_data['mdl_id'],prm_name=request_data['prm_name'],sec_name=request_data['sec_name'],mdl_source=request_data['mdl_source'],mdl_type=request_data['Mdl_type'],mdl_absct=request_data['mdl_abstract'],mdl_objective=request_data['mdl_objective'],mdl_appl=request_data['mdl_app'],mdl_risk_anls=request_data['mdl_risk_anals'],prctaddr=request_data['pro_addr'],usgfreq=request_data['usage_freq'])
        # print('--------------1')
        temp_over_obj = TempMdlOverview.objects.filter(mdl_id=request_data['mdl_id'])
        print("temp_over_obj",temp_over_obj)
        if TempMdlOverview.objects.filter(mdl_id=request_data['mdl_id']):
            overview_obj = TempMdlOverview.objects.filter(mdl_id=request_data['mdl_id']).update(department=dept_obj.dept_aid,func=None if request_data['function']=='' else request_data['function'],prm_name=request_data['prm_name'],sec_name=request_data['sec_name'],mdl_source=request_data['mdl_source'],mdl_type=None if request_data['Mdl_type']=='' else request_data['Mdl_type'] ,mdl_absct=request_data['mdl_abstract'],mdl_objective=request_data['mdl_objective'],mdl_appl=request_data['mdl_app'],mdl_risk_anls=request_data['mdl_risk_anals'],prctaddr=None if request_data['pro_addr']=='' else request_data['pro_addr'],usgfreq=None if request_data['usage_freq']=='' else request_data['usage_freq'],txtPrdDt=None if request_data['txtPrdDt']=='' else datetime.strptime(request_data['txtPrdDt'], '%m/%d/%Y'))
        else:
            overview_obj = TempMdlOverview(mdl_id=request_data['mdl_id'],mdl_cnt = 2,mdl_major_ver=1,mdl_minor_ver = 0,department=dept_obj.dept_aid,func=None if request_data['function']=='' else request_data['function'],prm_name=request_data['prm_name'],sec_name=request_data['sec_name'],mdl_source=request_data['mdl_source'],mdl_type=None if request_data['Mdl_type']=='' else request_data['Mdl_type'],mdl_absct=request_data['mdl_abstract'],mdl_objective=request_data['mdl_objective'],mdl_appl=request_data['mdl_app'],mdl_risk_anls=request_data['mdl_risk_anals'],prctaddr=None if request_data['pro_addr']=='' else request_data['pro_addr'],usgfreq=None if request_data['usage_freq']=='' else request_data['usage_freq'],txtPrdDt=None if request_data['txtPrdDt']=='' else   datetime.strptime(request_data['txtPrdDt'], '%m/%d/%Y'))
            overview_obj.save()
        print('----------------01')
        dict1_overview_obj = convrt_to_dictionary(TempMdlOverview,request_data['mdl_id'])
        print("overview_obj",dict1_overview_obj)
        overviewlistcolms = [key for key,val in dict1_overview.items() if key in dict1_overview_obj if dict1_overview_obj[key] != val]
        print("changed columns",overviewlistcolms)
        
        #Model Risk
        dict_mdlrisk = convrt_to_dictionary(MdlRisks,request_data['mdl_id'])
        print("mdlrisk",dict_mdlrisk)
        # mdl_risk_obj = MdlRisks.objects.filter(mdl_id=request_data['mdl_id']).update(mdl_risks=request_data['mdl_risk'],intr_risk=request_data['intr_risk'],reliance=request_data['reliance'],materiality=request_data['materiality'],risk_mtgn=request_data['risk_miti'],fair_lndg=request_data['fair_lendg'])         
        dict_mdlrisk_obj = convrt_to_dictionary(MdlRisks,request_data['mdl_id'])
        print("mdlrisk",dict_mdlrisk)
        print('--------------2')
        if TempMdlRisks.objects.filter(mdl_id=request_data['mdl_id']):
            mdl_risk_obj = TempMdlRisks.objects.filter(mdl_id=request_data['mdl_id']).update(mdl_risks=request_data['mdl_risk'],intr_risk=request_data['intr_risk'],reliance=request_data['reliance'],materiality=request_data['materiality'],risk_mtgn=request_data['risk_miti'],fair_lndg=request_data['fair_lendg'])
        else:
            mdl_risk_obj = TempMdlRisks(mdl_id=request_data['mdl_id'],mdl_risks=request_data['mdl_risk'],intr_risk=request_data['intr_risk'],reliance=request_data['reliance'],materiality=request_data['materiality'],risk_mtgn=request_data['risk_miti'],fair_lndg=request_data['fair_lendg'])           
            mdl_risk_obj.save()
        print('--------------02')
        modelriskcolms = [key for key,val in dict_mdlrisk.items() if key in dict_mdlrisk_obj if dict_mdlrisk_obj[key] != val]
        print("changed columns risk",modelriskcolms)
        #Relevent Personnal
        ddlOwner = request.POST['mdl_owner']
        ddlOwner=ddlOwner.split(",") 
        if len(ddlOwner) != 0:
            mdlrelv_personal(request_data['mdl_id'],'Owner',ddlOwner,request.session['uid'])
            print("owner save")
        
        ddldevloper = request.POST['mdl_devlpr']
        ddldevloper=ddldevloper.split(",")
        if len(ddldevloper) != 0:
            mdlrelv_personal(request_data['mdl_id'],'Developer',ddldevloper,request.session['uid'])        

        ddluser = request.POST['mdl_user']
        ddluser=ddluser.split(",")
        if len(ddluser) != 0:
            mdlrelv_personal(request_data['mdl_id'],'User',ddluser,request.session['uid'])

        ddlprdxnsupp = request.POST['prdxn_support']
        ddlprdxnsupp=ddlprdxnsupp.split(",")
        if len(ddlprdxnsupp) != 0:
            mdlrelv_personal(request_data['mdl_id'],'PrdnSupport',ddlprdxnsupp,request.session['uid'])
        
        #Model Dependancies
        dependancy = convrt_to_dictionary(MdlDependencies,request_data['mdl_id'])
        print("dependancy",dependancy)
        # mdl_depndncy_obj = MdlDependencies.objects.filter(mdl_id=request_data['mdl_id']).update(upstrmmdl=request_data['upstream'],dwstrmmdl=request_data['dwnstram'])
        # try:
        if TempMdlDependencies.objects.filter(mdl_id=request_data['mdl_id']):
            mdl_depndncy_obj = TempMdlDependencies.objects.filter(mdl_id=request_data['mdl_id']).update(upstrmmdl=request_data['upstream'],dwstrmmdl=request_data['dwnstram'])
        # except:
        else:
            mdl_depndncy_obj = TempMdlDependencies(mdl_id=request_data['mdl_id'],upstrmmdl=request_data['upstream'],dwstrmmdl=request_data['dwnstram'])
            mdl_depndncy_obj.save()
        print("-----------------------03")
        dependancy_obj = convrt_to_dictionary(MdlDependencies,request_data['mdl_id'])
        print("dependancy",dependancy_obj)
        mdldeplistcolms =  [key for key,val in dependancy.items() if key in dependancy_obj if dependancy_obj[key] != val]
        print("changed columns dependancy",mdldeplistcolms)
        updated_colms = overviewlistcolms + modelriskcolms + mdldeplistcolms
        print("updated columns",updated_colms)
        
        #saved updated columns
        for col in updated_colms:
            histry_obj = HistoryRegisterModel(column_name=col,updatedby=request.session['uid'],updatedate=datetime.now())
            histry_obj.save()
        MdlOverview.objects.filter(mdl_id =request_data['mdl_id']).update(is_submit=1)
        data = {"isvalid":"true"}
        return JsonResponse(data)
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc())

def ApproveEdit(request): 
    try:
        mdlId = request.GET.get("mdlId",'False')
        colname = request.GET.get("colname",'False')
        tblname = request.GET.get("tblname",'False')
        print("Approve edit data",mdlId,colname,tblname)

        third_party_api_url = getAPIURL()+'ApproveEdit/'
        header = {
        "Content-Type":"application/json",
         'Authorization': 'Token '+request.session['accessToken']
        }
        update_to_save={
            'mdlId':mdlId,
            'colname':colname,
            'tblname':tblname,
            'uid':request.session['uid']
        }
        response_user = requests.post(third_party_api_url,  data= json.dumps(update_to_save),headers=header)
        # print("response userlist",response_user.content)
        jsondata = json.loads(response_user.content)
        print('jsondata ',jsondata)
        return JsonResponse({'istaken':jsondata['istaken']})    
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())

def deleteTempData(request): 
    try:
        mdlId = request.GET.get("mdlId",'False') 

        third_party_api_url = getAPIURL()+'discardUpdate/'
        header = {
        "Content-Type":"application/json",
         'Authorization': 'Token '+request.session['accessToken']
        }
        update_to_save={
            'mdlId':mdlId, 
            'uid':request.session['uid']
        }
        response_user = requests.post(third_party_api_url,  data= json.dumps(update_to_save),headers=header)
        # print("response userlist",response_user.content)
        jsondata = json.loads(response_user.content)
        print('jsondata ',jsondata)
        return JsonResponse({'istaken':jsondata['istaken']})    
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())
        

def tempdetails(request):
    try:
        mdlId = request.GET.get('mdlId')
        return render(request, 'projectlisttemp.html',{ 'actPage':'Temp details','mdlId':mdlId})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 

def getTempMdlDetailsById(request):
    try:
        mdl_id =request.GET.get('mdlId', 'False')  
        api_url=getAPIURL()+"getMdlDetailsById/"       
        data_to_save={
            'mdl_id':mdl_id} 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()  

        Owner=api_data['Owner']

        Developer=api_data['Developer']#objMdlRelvPern.getRelevantPersonal(mdl_id,'Developer')

        User=api_data['User']#objMdlRelvPern.getRelevantPersonal(mdl_id,'User')

        PrdnSupport=api_data['PrdnSupport']#objMdlRelvPern.getRelevantPersonal(mdl_id,'PrdnSupport')
 
        dependencies =api_data['dependencies']#objdependencies.getMdlDependencies(mdl_id) 

        PerformMon=objreg.getPerfomanceMonitor(mdl_id)

        api_url=getAPIURL()+"getTempMdlDetailsById/"       
        data_to_save={
            'mdl_id':mdl_id} 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        Temp_response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        Temp_api_data=Temp_response.json()  

        Temp_Owner=Temp_api_data['Owner']  
        return JsonResponse({'istaken':'true','dependencies':dependencies,'temp_dependencies':Temp_api_data['dependencies'],
                             'PerformMon':PerformMon,'temp_PerformMon':Temp_api_data['PerformMon'],'Owner':Owner,'Temp_Owner':Temp_Owner,
                             'Developer':Developer,'temp_Developer':Temp_api_data['Developer'],'User':User,'temp_User':Temp_api_data['User'],
                             'PrdnSupport':PrdnSupport,'temp_PrdnSupport':Temp_api_data['PrdnSupport'],'mdldata':api_data['mdldata'],'temp_mdldata':Temp_api_data['mdldata']})
    except Exception as e:
        print('getMdlDetails is ',e)
        print('getMdlDetails traceback is ', traceback.print_exc())

# def issubmit(request): 
    
#     request_data = {x:request.GET.get(x) for x in request.GET.keys()} 
#     mrm_head=objmaster.getMRMHead()
#     try:
#         issub_obj = MdlOverview.objects.get(mdl_id = request_data['mdl_id'] )#, is_submit__isnull=True
#         if issub_obj:       
#             print(issub_obj.is_submit)      
#             obj = MdlOverview.objects.filter(mdl_id = request_data['mdl_id']).update(is_submit=request_data['is_submit']) 
#             print('inside 0 ',  request_data['is_submit'], str(request_data['is_submit'])=="0")        
#             if(str(request_data['is_submit'])=="1"):
#                 notification_trigger= "New model Submitted - " +  request_data['mdl_id']
#                 objmaster.insert_notification(request.session['uid'],mrm_head,"Model",notification_trigger,1)
#                 objmaster.insertActivityTrail(request_data['mdl_id'],"2","New model submitted",request.session['uid'],request.session['accessToken'])
#             elif(str(request_data['is_submit'])=="2"):
#                 notification_trigger= "Edit request for - " +  request_data['mdl_id']
#                 objmaster.insert_notification(request.session['uid'],mrm_head,"Model",notification_trigger,1)
#                 objmaster.insertActivityTrail(request_data['mdl_id'],"3","Model submitted",request.session['uid'],request.session['accessToken'])
#             elif(str(request_data['is_submit'])=="0"):
#                 notification_trigger= "Edit request approved - " +  request_data['mdl_id']
                
#                 print('inside 0 ',request.session['uid'],issub_obj.addedby,"Model",notification_trigger,1)
#                 objmaster.insert_notification(request.session['uid'],issub_obj.addedby,"Model",notification_trigger,1)
#                 objmaster.insertActivityTrail(request_data['mdl_id'],"4","Model submitted",request.session['uid'],request.session['accessToken'])
#             return JsonResponse({"isvalid":"true"})
#     except Exception as e:
#         print('issubmit is ',e)
#         print('issubmit traceback is ', traceback.print_exc())
#         return JsonResponse({"isvalid":"false"})
    

def save_OnlyQuestion_allocation(request):     
    mdlid =request.session['vt_mdl']
    question_ids = request.GET.getlist('question_aid[]')
    users = request.GET.getlist('users[]')
    end_date=request.GET['end_date']
    api_url=getAPIURL()+"save_OnlyQuestion_allocation/"       
    params={'vt_mdl':mdlid,
        'dept':request.session['dept'],
        'uid':request.session['uid'],
        'question_aid':question_ids,
        'users':users,
        'utype':request.session['utype'],
        'section':'',
        'end_date':end_date} 
    header = {
    "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.post(api_url, data= json.dumps(params),headers=header)         
    api_data=response.json()
    objmaster.insertActivityTrail(mdlid,"7","Model validation questions assigned." , request.session['uid'],request.session['accessToken'])
    return JsonResponse({"isvalid":api_data['isvalid']}) 

def save_OnlyQuestion_allocation_section(request):     
    mdlid =request.session['vt_mdl']
    question_ids = request.GET.getlist('question_aid[]')
    users = request.GET.getlist('users[]')
    end_date=request.GET['end_date']
    section=request.GET['section']
    api_url=getAPIURL()+"allocate_questions/"       
    params={'utype':request.session['utype'],
        'vt_mdl': request.session['vt_mdl'],
        'uid':request.session['uid'],
        'ulvl':request.session['ulvl'],} 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(params),headers=header)         
    api_data=response.json()
    users=api_data['user']
    usersarr=[]
    for key ,val in users.items():
        usersarr.append(users[key]['u_Aid'])
    
    api_url=getAPIURL()+"save_OnlyQuestion_allocation/"       
    params={'vt_mdl':mdlid,
        'dept':request.session['dept'],
        'uid':request.session['uid'],
        'question_aid':question_ids,
        'users':usersarr,
        'utype':request.session['utype'],
        'section':' '+section,
        'end_date':end_date} 
    header = {
    "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.post(api_url, data= json.dumps(params),headers=header)         
    api_data=response.json() 
    objmaster.insertActivityTrail(mdlid,"7","Model validation questions assiged for "+section +"." , request.session['uid'],request.session['accessToken'])
    return JsonResponse({"isvalid":api_data['isvalid']}) 

def showrolesrespqtn(request):
    try: 
        qtnobj = RolesResponsibilityQuestion.objects.all()
        return render(request, 'rolesresponsibilityqtn.html',{'actPage' :'PROPE- Roles Responsibility Question','qtnobj':qtnobj})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())

def newrolesrespqtn(request):
    try:   
        return render(request, 'addrolesrespqtn.html',{'actPage':'Add Task Function'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def addrolesrespqtn(request):
    print()
    try:
        print("---------add role resp qtn",request.GET)
        request_data = {x:request.GET.get(x) for x in request.GET.keys()}
        qtn_obj = RolesResponsibilityQuestion(question_text = request_data['qtn_txt'],is_active = request_data['activests'],is_global = request_data['isavailibility'],description = request_data['desc'])
        qtn_obj.save()
        print("save successfully")
        return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print("setuppycaret is",e) 
        print('setuppycaret traceback is ', traceback.print_exc()) 
        return JsonResponse(e)

def editrolesrespqtn(request,id):
    print("roles id",id)
    obj = RolesResponsibilityQuestion.objects.get(qtn_aid = id)
    return render(request, 'editrolesrespqtn.html',{ 'actPage':'Edit Roles Responsibility Question','obj':obj})

def updaterolesrespqtn(request):
    print()
    try:
        print("---------Update role resp qtn",request.GET)
        request_data = {x:request.GET.get(x) for x in request.GET.keys()}
        qtn_obj = RolesResponsibilityQuestion.objects.filter(qtn_aid = request_data['qtn_id']).update(question_text = request_data['qtn_txt'],is_active = request_data['activests'],is_global = request_data['isavailibility'],description = request_data['desc'])
        print("save successfully")
        return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print("setuppycaret is",e) 
        print('setuppycaret traceback is ', traceback.print_exc()) 
        return JsonResponse(e)


def showauditregcompl(request):
    try: 
        cmplobj = AuditRegCompl.objects.all()
        return render(request, 'auditregcompl.html',{'actPage' :'PROPE- Task Function','cmplobj':cmplobj})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())

def newauditregcompl(request):
    try:   
        return render(request, 'addauditregcompl.html',{'actPage':'Add Audit Reg Compl'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def addauditregcompl(request):
    print()
    try:
        print("---------add role resp qtn",request.GET)
        request_data = {x:request.GET.get(x) for x in request.GET.keys()}
        qtn_obj = AuditRegCompl(question_text = request_data['qtn_txt'],is_active = request_data['activests'],is_global = request_data['isavailibility'],description = request_data['desc'])
        qtn_obj.save()
        print("save successfully")
        return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print("setuppycaret is",e) 
        print('setuppycaret traceback is ', traceback.print_exc()) 
        return JsonResponse(e)
    
def editauditregcompl(request,id):
    print("audit id",id)
    obj = AuditRegCompl.objects.get(compl_aid = id)
    return render(request, 'editauditregcompl.html',{ 'actPage':'Edit Audit Reg Compl','obj':obj})

def updateauditregcompl(request):
    print()
    try:
        print("---------Update regcompl ",request.GET)
        request_data = {x:request.GET.get(x) for x in request.GET.keys()}
        qtn_obj = AuditRegCompl.objects.filter(compl_aid = request_data['cmpl_id']).update(question_text = request_data['qtn_txt'],is_active = request_data['activests'],is_global = request_data['isavailibility'],description = request_data['desc'])
        print("save successfully")
        return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print("setuppycaret is",e) 
        print('setuppycaret traceback is ', traceback.print_exc()) 
        return JsonResponse(e)
    
def newauditallocation(request):
    try:   
        # mdl_id = request.session['vt_mdl']
        print("mdlid-----",request.session.items())
        mdl_id = request.session['vt_mdl']
        addedby = request.session['uid']
        strQ="select arc.* from Audit_Reg_Compl arc,"
        strQ +=" (select Compl_AID from Audit_Reg_Compl "
        strQ += "where (Is_Active=1 and Is_Global=1) or (Is_Active=1 and addedby='"+str(addedby)+"')"
        strQ +=" except "  
        strQ +=" select Compl_AID from Audit_Reg_Compl_Allocation"
        strQ +=" where mdl_id='"+ mdl_id +"')a"
        strQ +=" where a.Compl_AID=arc.Compl_AID order by addedon"
        print("query",strQ)
        tableResult =objdbops.getTable(strQ)  
        users = tableResult.to_json(orient='index')
        users = json.loads(users)
        
  
        lst = []
        
        strQ="  select   arc.compl_aid\
                ,arc.[Mdl_Id]\
                ,isNull(Question_Resp,'') Question_Resp,question_text from [Audit_Reg_Compl_Resp] arcr right join [Audit_Reg_Compl_Allocation] arc\
                on arc.[Compl_AID]=arcr.[Compl_AID],Audit_Reg_Compl where \
                Audit_Reg_Compl.[Compl_AID]=arc.[Compl_AID] and\
                arc.mdl_id='"+mdl_id+"' group by  arc.[Compl_AID]      ,arc.[Mdl_Id]      , Question_Resp,question_text, arcr.[addedon]\
                order by arcr.[addedon]"
        tableResult =objdbops.getTable(strQ)
        for index, row in  tableResult.iterrows():             
            dict = {}             
            dict['compl_id'] = row['compl_aid']
            dict['question_text'] = row['question_text']
            dict['Question_Resp']= row['Question_Resp']
            lst.append(dict)
        return render(request, 'Audit_Allocation.html',{'actPage':'Audit Reg Compl Response','obj':users,'questions':lst})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())


def saveauditallocation(request):
    try:
        print("mdl_id---------------",request.session)
        print("---------save response ",request.GET)
        response = request.GET.getlist('response[]')
        print("response",response)
        allocated_to = objreg.getMdlOwnerById(request.session['vt_mdl'],'Owner')   
        print("allocated_to",allocated_to)
        
        for i in response:
            for x,y in allocated_to.items():
                allocateobj = AuditRegComplAllocation.objects.filter(Q(compl_aid = i) & Q(mdl_id = request.session['vt_mdl']))
                if allocateobj:
                    allocateobj.update(addedby=request.session['uid'],addedon=datetime.now(),allocated_to = allocated_to[x]['u_Aid'])
                else:
                    obj = AuditRegComplAllocation(compl_aid = i,mdl_id = request.session['vt_mdl'],addedby=request.session['uid'],addedon=datetime.now(),allocated_to = allocated_to[x]['u_Aid'])
                    obj.save()
        return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print("response",e,traceback.print_exc())
        return JsonResponse({"isvalid":"false"})

def savemodalauditquestion(request):
    print()
    try:
        print("---------add modal qtn",request.GET)
        request_data = {x:request.GET.get(x) for x in request.GET.keys()}
        qtn_obj = AuditRegCompl(question_text = request_data['qtn_txt'],is_active = request_data['activests'],is_global = request_data['isavailibility'],description = request_data['desc'])
        qtn_obj.save()
        print("save successfully")
        allocated_to = objreg.getMdlOwnerById(request.session['vt_mdl'],'Owner')   
        print("allocated_to",allocated_to) 
        obj = AuditRegComplAllocation(compl_aid = qtn_obj.compl_aid,mdl_id = request.session['vt_mdl'],addedby=request.session['uid'],addedon=datetime.now(),allocated_to = allocated_to['0']['u_Aid'])
        obj.save()
        return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print("setuppycaret is",e) 
        print('setuppycaret traceback is ', traceback.print_exc()) 
        return JsonResponse(e)

def newauditresponse(request):
    try:   
        # mdl_id = request.session['vt_mdl']
        mdl_id="" 
        reqMethod="" 
        if request.method == 'POST':   
            mdl_id = request.POST['mdl_id'] 
           
            reqMethod="POST" 
        api_url=getAPIURL()+"newauditresponse/"       
        data_to_save={'mdl_id':mdl_id,
            'method':reqMethod,
            'uid':request.session['uid'], 
            } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json() 

         
        return render(request, 'Audit_Response.html',{'selected_id':mdl_id,'obj':api_data['obj'],'questions':api_data['questions'],'mdl_id':api_data['mdl_id']})
        #return render(request, 'chatAuditResp.html',{'selected_id':selected_id,'obj':users,'questions':lst,'mdl_id':model_id})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def getAUditQtns(request):
    try:   
        # mdl_id = request.session['vt_mdl']
        lst = []
       
        addedby = request.session['uid']        
        mdl_id = request.GET.get('mdl_id','none')
        strQ="  select   arc.compl_aid\
                ,arc.[Mdl_Id]\
                ,isNull(Question_Resp,'') Question_Resp,question_text from [Audit_Reg_Compl_Resp] arcr right join [Audit_Reg_Compl_Allocation] arc\
                on arc.[Compl_AID]=arcr.[Compl_AID],Audit_Reg_Compl where \
                Audit_Reg_Compl.[Compl_AID]=arc.[Compl_AID] and\
                arc.mdl_id='"+mdl_id+"' and arc.[Allocated_to]="+str(addedby)+" group by  arc.[Compl_AID] ,arc.[Mdl_Id], Question_Resp,question_text, arcr.[addedon]\
                order by arcr.[addedon]"
        tableResult =objdbops.getTable(strQ)
        for index, row in  tableResult.iterrows():             
            dict = {}             
            dict['compl_id'] = row['compl_aid']
            dict['question_text'] = row['question_text']
            dict['Question_Resp']= row['Question_Resp']
            lst.append(dict) 
        # return render(request, 'Audit_Response.html',{'selected_id':selected_id,'obj':users,'questions':lst,'mdl_id':model_id})
        return  JsonResponse({'questions':lst})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def getAuditQtnsAns(request):
    try:   
        # mdl_id = request.session['vt_mdl']
        lst = []    
        mdl_id = request.GET.get('mdl_id','none')
        Compl_AID = request.GET.get('Compl_AID','none')
        strQ="  select   arc.compl_aid\
                ,arc.[Mdl_Id]\
                ,isNull(Question_Resp,'') Question_Resp from [Audit_Reg_Compl_Resp] arc where \
                arc.[Compl_AID]='"+Compl_AID+"' and\
                arc.mdl_id='"+mdl_id+"'  group by  arc.[Compl_AID] ,arc.[Mdl_Id], Question_Resp, arc.[addedon]\
                order by arc.[addedon]"
        tableResult =objdbops.getTable(strQ)
        for index, row in  tableResult.iterrows():             
            dict = {}             
            dict['compl_id'] = row['compl_aid']
            dict['Question_Resp']= row['Question_Resp']
            lst.append(dict) 
        # return render(request, 'Audit_Response.html',{'selected_id':selected_id,'obj':users,'questions':lst,'mdl_id':model_id})
        return  JsonResponse({'questions':lst})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def saveauditresponse(request):
    try:
      
        request_data = {x:request.GET.get(x) for x in request.GET.keys()}  
        
        mdl_id = request_data['mdl_id']
        api_url=getAPIURL()+"saveauditresponse/"       
        data_to_save={'mdl_id':request.session['mdl_id'],
            'compl_id':request_data['compl_id'],
            'uid':request.session['uid'],
            'response': request_data['response'],} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        return JsonResponse({"isvalid":api_data['isvalid']})
        # response_obj = AuditRegComplResp.objects.filter(Q(compl_aid = request_data['compl_id']) & Q(mdl_id =mdl_id))
        # if response_obj:
        #     print('record exists')
        #     response_obj.update(question_resp = request_data['response'],addedby=request.session['uid'],addedon=datetime.now())
        #     return JsonResponse({"isvalid":"true"})    
        # else:
        #     print('record do not exists')
        #     obj = AuditRegComplResp(question_resp = request_data['response'],compl_aid=request_data['compl_id'],mdl_id = mdl_id,addedby=request.session['uid'],addedon=datetime.now())
        #     obj.save()
        #     return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print("response",e,)
        return JsonResponse({"isvalid":"false"})


#responsibility question Allocation
def newquestionallocation(request):
    try:   
        mdl_id = request.session['vt_mdl']
        addedby = request.session['uid']
        strQ="select arc.* from Roles_Responsibility_Question arc,"
        strQ +=" (select Qtn_AID from Roles_Responsibility_Question "
        strQ += "where (Is_Active=1 and Is_Global=1) or (Is_Active=1 and addedby='"+str(addedby)+"')"
        strQ +=" except "  
        strQ +=" select Qtn_AID from Roles_Responsibility_Question_Allocation"
        strQ +=" where mdl_id='"+ mdl_id +"')a"
        strQ +=" where a.Qtn_AID=arc.Qtn_AID order by addedon"
        print("query",strQ)
        tableResult =objdbops.getTable(strQ)  
        users = tableResult.to_json(orient='index')
        users = json.loads(users)
        
        question = RolesResponsibilityQuestionAllocation.objects.filter(mdl_id=request.session['vt_mdl'])
        lst = []
        
        # for i in question:
        #     print("i---",i)
        #     dict = {}
        #     qtn_txt = RolesResponsibilityQuestion.objects.get(qtn_aid = i.qtn_aid)
        #     dict['qtn_id'] = qtn_txt.qtn_aid
        #     dict['question_text'] = qtn_txt.question_text
        #     lst.append(dict)
        lst = []
        
        strQ="  select   arc.Qtn_AID\
                ,arc.[Mdl_Id]\
                ,isNull(Qtn_Resp,'') Question_Resp,question_text from Roles_Responsibility_Question_Response arcr right join Roles_Responsibility_Question_Allocation arc\
                on arc.[Qtn_AID]=arcr.[Qtn_AID],Roles_Responsibility_Question Audit_Reg_Compl where \
                Audit_Reg_Compl.[Qtn_AID]=arc.[Qtn_AID] and\
                arc.mdl_id='"+mdl_id+"' group by  arc.[Qtn_AID]      ,arc.[Mdl_Id]      , Qtn_Resp,question_text, arcr.[addedon]\
                order by arcr.[addedon]"
        tableResult =objdbops.getTable(strQ)
        for index, row in  tableResult.iterrows():             
            dict = {}             
            dict['qtn_id'] = row['Qtn_AID']
            dict['question_text'] = row['question_text']
            dict['Question_Resp']= row['Question_Resp']
            lst.append(dict)
        print("resp lst",lst)
        return render(request, 'Question_Allocation.html',{'actPage':'Responsibility Question Allocation','obj':users,'questions':lst})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def savequestionallocation(request):
    try:
        print("mdl_id---------------",request.session)
        print("---------save response ",request.GET)
        response = request.GET.getlist('response[]')
        print("response",response)
        allocated_to = objreg.getMdlOwnerById(request.session['vt_mdl'],'Owner')   
        print("allocated_to",allocated_to) 
        for i in response:
            for x,y in allocated_to.items():
                print("dictionary onject",x,y)
                qtnobj = RolesResponsibilityQuestionAllocation.objects.filter(Q(qtn_aid = i) & Q(mdl_id = request.session['vt_mdl']))
                if qtnobj:
                    qtnobj.update(addedby=request.session['uid'],addedon=datetime.now(),allocated_to = allocated_to[x]['u_Aid'])
                else:
                    obj = RolesResponsibilityQuestionAllocation(qtn_aid = i,mdl_id = request.session['vt_mdl'],addedby=request.session['uid'],addedon=datetime.now(),allocated_to = allocated_to[x]['u_Aid'])
                    obj.save()
        return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print("response",e,traceback.print_exc())
        return JsonResponse({"isvalid":"false"})
    
def newquestionresponse(request):
    try:   
        print('inside newquestionresponse')
        
        selected_id=""  
        mdl_id="" 
        reqMethod="" 
        if request.method == 'POST':   
            mdl_id = request.POST['mdl_id']
           
            reqMethod="POST" 
        api_url=getAPIURL()+"newquestionresponseapi/"       
        data_to_save={'mdl_id':mdl_id,
            'method':reqMethod,
            'uid':request.session['uid'], 
            } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json() 

        return render(request, 'Question_Response.html',{'selected_id':selected_id,'mdl_id':api_data['mdl_id'],
                                                         'obj':api_data['obj'],'questions':api_data['questions']})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())
    
def savequestionresponse(request):
    try:
        request_data = {x:request.GET.get(x) for x in request.GET.keys()}  
        # qtn_respi_obj = RolesResponsibilityQuestionResponse.objects.filter(Q(qtn_aid = request_data['qtn_id']) & Q(mdl_id =mdl_id))
        # if qtn_respi_obj:
        #     qtn_respi_obj.update(qtn_resp = request_data['response'],addedby=request.session['uid'],addedon=datetime.now())
        # else:
        #     obj = RolesResponsibilityQuestionResponse(qtn_resp = request_data['response'],qtn_aid=request_data['qtn_id'],mdl_id = mdl_id,addedby=request.session['uid'],addedon=datetime.now())
        #     obj.save() 
        api_url=getAPIURL()+"savequestionresponse/"       
        data_to_save={'mdl_id':request.session['mdl_id'],
            'compl_id':request_data['compl_id'],
            'uid':request.session['uid'],
            'response': request_data['response'],} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        return JsonResponse({"isvalid":api_data['isvalid']})
       
    except Exception as e:
        print("response",e)
        return JsonResponse({"isvalid":"false"})
#Modal Save responsibility Question
def savemodalrespquestion(request):
    print()
    try:
        
        request_data = {x:request.GET.get(x) for x in request.GET.keys()}
        
        qtn_obj = RolesResponsibilityQuestion(question_text = request_data['qtn_txt'],is_active = request_data['activests'],is_global = request_data['isavailibility'],description = request_data['desc'])
        qtn_obj.save()
        print("save successfully")
        allocated_to = objreg.getMdlOwnerById(request.session['vt_mdl'],'Owner')   
        print("allocated_to",allocated_to) 
        obj = RolesResponsibilityQuestionAllocation(qtn_aid = qtn_obj.qtn_aid,mdl_id = request.session['vt_mdl'],addedby=request.session['uid'],addedon=datetime.now(),allocated_to = allocated_to['0']['u_Aid'])
        obj.save()
        return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print("setuppycaret is",e) 
        print('setuppycaret traceback is ', traceback.print_exc()) 
        return JsonResponse(e)
    
def insertAuditChat(request):
    try:        
        mdl_id = request.GET.get('mdl_id','none')
        qtn_id = request.GET.get('qtn_id','none')
        comments = request.GET.get('comments','none')
        isupdate = request.GET.get('isupdate','0')
        Response_id = request.GET.get('Response_id','0')
        objrmse.insertAuditChatResp(mdl_id,qtn_id,str(request.session['uid']),comments,isupdate,Response_id)
        return JsonResponse({"is_taken":True})
    except Exception as e:
        print('uploaddecomm is ',e)
        print('uploaddecomm traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})

# def BackupFor_userdetails(request):
   
#     try:
#         id=request.GET['backupforid']
#         #using api urls for user New Code
#         third_party_api_url_usr = getAPIURL()+'UpdateUser/'+id
#         header = {
#         "Content-Type":"application/json",
#           'Authorization': 'Token '+request.session['accessToken']
#         }
#         response_bkp_user = requests.get(third_party_api_url_usr, headers=header)
#         print("response User backup--------------------------",response_bkp_user.content)
#         user_data = json.loads(response_bkp_user.content)
#         u_name = user_data['data']['u_name']
#         u_depart_id = user_data['data']['dept_aid']

#         try:
#             third_party_api_url_usr = getAPIURL()+'department/'+str(u_depart_id)
#             header = {
#             "Content-Type":"application/json",
#               'Authorization': 'Token '+request.session['accessToken']
#             }
#             response_dept_data = requests.get(third_party_api_url_usr, headers=header)
#             dept_data = json.loads(response_dept_data.content)
#             print("department data",dept_data)
#             u_depart_name = dept_data['data']['dept_label']
#         except Department.DoesNotExist:
#             print("none--------------")
#             u_depart_name=None
#         u_type_id = user_data['data']['uc_aid']
#         try:
#             u_type=user_data['data']['uc_details']['uc_label']
#         except UserCategory.DoesNotExist:
#             u_type=None
#         reportsto = user_data['data']['u_reportto']
#         try:
#             # reports_to_user=Users.objects.get(u_aid=reportsto).u_name
#             third_party_api_url_usr = getAPIURL()+'UpdateUser/'+str(reportsto)
#             header = {
#             "Content-Type":"application/json",
#               'Authorization': 'Token '+request.session['accessToken']
#             }
#             response_reportsto = requests.get(third_party_api_url_usr, headers=header)
#             print("response reportsto--------------------------",response_reportsto.content)
#             user_reportsto = json.loads(response_reportsto.content)
#             reports_to_user=user_reportsto['data']['u_name']
#         except Users.DoesNotExist:
#             reports_to_user = None
        
         
       
#         return JsonResponse({'u_name':u_name,'u_depart_name':u_depart_name,'u_depart_id':u_depart_id,'u_type':u_type,'u_type_id':u_type_id,'reportsto':reportsto,'reports_to_user':reports_to_user})

#     except Exception as e:
#         print('adduser is ',e) 
#         print('adduser traceback is ', traceback.print_exc())
#         print("edit_user",id) 

def BackupFor_userdetails(request):
   
    try:
        id=request.GET['backupforid']
        user_obj=Users.objects.get(u_aid=int(id))
        print('user_obj ',user_obj)
        u_name=user_obj.u_name
        print("u_name",u_name)
        u_depart_id=user_obj.dept_aid
        print("u_depart_id",u_depart_id)
        try:
            u_depart_name=Department.objects.get(dept_aid=u_depart_id).dept_label
        except Department.DoesNotExist:
            u_depart_name=None
        u_type_id=user_obj.uc_aid
        print("u_type_id",u_type_id.uc_aid)
        try:
            u_type=UserCategory.objects.get(uc_aid=u_type_id.uc_aid).uc_label
        except UserCategory.DoesNotExist:
            u_type=None    
        print('u_type ',u_type)        
        reportsto=user_obj.u_reportto
        try:
            reports_to_user=Users.objects.get(u_aid=reportsto).u_name

            tableResult =objdbops.getTable("select U_AID,U_Name from users where u_name not like '%_backup' and dept_aid='"+str(u_depart_id)+"'")
            print('query backup user ',"select U_AID,U_Name from users where u_name not like '%_backup' and dept_aid='"+str(u_depart_id)+"'")
            backup = tableResult.to_json(orient='index')
            backup = json.loads(backup)
            del tableResult
        except Users.DoesNotExist:
            reports_to_user = None
       
        return JsonResponse({'u_name':u_name,'u_depart_name':u_depart_name,'u_depart_id':u_depart_id,'u_type':u_type,'u_type_id':u_type_id.uc_aid,
                             'reportsto':reportsto,'reports_to_user':reports_to_user,'backup':backup})

    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())
        print("edit_user",id)



def ReportSubmissionDiss(request):
    try: 
        api_url=getAPIURL()+"getMdlForVRSubmisionAllocation/"       
        data_to_save={ 
            'uid':request.session['uid'],
            'is_mrm':request.session['is_mrm']} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
         
        return render(request,'chat_report_submission.html',{'mdl_id':api_data['mdl_id']})
    except Exception as e:
        print('QtnsResp is ',e)
        print('QtnsResp traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})
 

def getVRSubmResp(request):
    try:        
        mdl_id = request.GET.get('mdl_id','none') 
        api_url=getAPIURL()+"getVRSubmResp/"       
        data_to_save={ 
            'mdl_id':mdl_id, 
            'uid':request.session['uid']
            } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        
        api_url=getAPIURL()+"getVRSubmCommentsCnt/"       
        data_to_save={ 
            'mdl_id':mdl_id  
            } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data1=response.json()
        from modelval.modelview import getSavedReportData
        savedData,newTitles = getSavedReportData(mdl_id,'Varo')

        return JsonResponse({"Qtns":api_data['Qtns'],"enddate":api_data['enddate'],'commentcnt':api_data1['comment'],'savedReportData':savedData})
    except Exception as e:
        print('uploaddecomm is ',e)
        print('uploaddecomm traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})


def insertVRSubmResp(request):
    try:        
        mdl_id = request.GET.get('mdl_id','none') 
        comments = request.GET.get('comments','none')
        isupdate = request.GET.get('isupdate','0')
        Response_id = request.GET.get('Response_id','0')
        api_url=getAPIURL()+"insertVRSubResp/"       
        data_to_save={'mdl_id':mdl_id, 
            'uid':request.session['uid'],
            'comments':comments,
            'isupdate':isupdate,
            'Response_id':Response_id,
            } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        
        return JsonResponse({"is_taken":api_data['is_taken']})
    except Exception as e:
        print('uploaddecomm is ',e)
        print('uploaddecomm traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})

def getVRSubRespById(request):
    try:               
        Response_id = request.GET.get('Response_id','0')        
        api_url=getAPIURL()+"getVRSubRespById/"       
        data_to_save={ 
            'Response_id':Response_id, 
            } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        return JsonResponse({"is_taken":True,'comment':api_data['comment']})
    except Exception as e:
        print('uploaddecomm is ',e)
        print('uploaddecomm traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})

def getVRSubRespByUid(request):
    try:                              
        api_url=getAPIURL()+"getVRSubRespByUid/"       
        data_to_save={ 
            'mdl_id':request.GET.get('mdl_id','none') , 
            'respid':request.GET.get('uid','none')  ,
            'uid':request.session['uid'],
            } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        return JsonResponse({"is_taken":True,'comment':api_data['comment']})
    except Exception as e:
        print('uploaddecomm is ',e)
        print('uploaddecomm traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})


def mdlselectionscreen(request):
    try: 
        if request.session['is_mrm'] =='Yes':
            third_party_api_url = getAPIURL()+'GetMdlForClosure/'
            header = {
            "Content-Type":"application/json",
                'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.get(third_party_api_url, headers=header)
            data =  response.json() 
            return render(request, 'mdlselectionscreen.html',{'data':data['data']})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 

def checkutype(request):
    print(request.GET)
    mdl_id = request.GET.get('mdl_id','False')
    print("mdl_id",mdl_id)
    third_party_api_url = getAPIURL()+'MdlRelevantPersonnelAPI/'+mdl_id
    header = {
    "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(third_party_api_url, headers=header)
    data = json.loads(response.content) 
    return JsonResponse({'users':data['users'],'owner':data['owner'],'validator':data['validator'],'enddate':data['enddate'],'canpublish':data['canpublish']})

def vrsuballocationsave(request):
     
    mdl_id = request.POST.get('mdl_id','False')
    userlist = request.POST.getlist('u_type') 
    str1 = userlist[0]
    finallist = str1.split(',') 
    enddate = request.POST.get('enddate','False') 
    api_url=getAPIURL()+"VrSubmissionAllocationAPI/"       
    data_to_save={'mdl_id':mdl_id,
        'u_aid':request.session['uid'] ,
        'enddate':enddate,
        'addedby':request.session['uid'] 
    } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
    for i in finallist: 
        api_url=getAPIURL()+"VrSubmissionAllocationAPI/"       
        data_to_save={'mdl_id':mdl_id,
            'u_aid':i,
            'enddate':enddate,
            'addedby':request.session['uid'] 
        } 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
       }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
            
    return JsonResponse(json.loads(response.content)) 

def vrsuballocationscreen(request):
    try:
        #mdl id with utype owner
        third_party_api_url = getAPIURL()+'checkutypeowner/'
        header = {
        "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        data = json.loads(response.content)
        print("response  ownertype--------------------------",data)  

    
        return render(request, 'vrsubmissionallocation.html',{'data':data['data']})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 


def checkutype1(request):
    print(request.GET)
    mdl_id = request.GET.get('mdl_id','False')
    print("mdl_id",mdl_id)
    third_party_api_url = getAPIURL()+'getutypeselection/'
    header = {
    "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
    }
    data={
        'ucaid':request.session['ucaid'],
        'dept':request.session['dept']
    }
    response = requests.get(third_party_api_url,data=json.dumps(data), headers=header)
    data = json.loads(response.content) 
    
    third_party_api_url = getAPIURL()+'VrSubmissionAllocationAPI/'+mdl_id
    header = {
    "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
    }
    response2 = requests.get(third_party_api_url, headers=header)
    data2 = json.loads(response2.content) 

    return JsonResponse({'users':data,'owner':data2['data']})

def showfrequency(request):
    try: 
        #new
        third_party_api_url = getAPIURL()+'validationReviewFrequency/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response Frequency",response.content)

        # tableResult =objdbops.getTable("select * from Department") 
        # users = tableResult.to_json(orient='index')
        # users = json.loads(users)
        # print("users",users)
        # del tableResult
        return render(request, 'validationfrequency.html',{ 'actPage':'Validation Review Frequency','users':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def publishVRScreen(request):
    try: 
        if request.session['is_mrm'] =='Yes':
            third_party_api_url = getAPIURL()+'GetMdlForPublish/'
            header = {
            "Content-Type":"application/json",
                'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.get(third_party_api_url, headers=header)
            data =  response.json() 
            return render(request, 'publishVR.html',{'data':data['data']})
    except Exception as e:
        print('publishVR is ',e)
        print('publishVR traceback is ', traceback.print_exc()) 

def newfrequency(request):
    try:   
        return render(request, 'addvalidationfrequency.html',{ 'actPage':'Add Validation Frequency','Freq':list(range(1, 11))})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

@api_view(['POST','PUT'])
def addfrequency(request):
    try:
        third_party_api_url = getAPIURL()+'validationReviewFrequency/'

        updated_id = request.POST.get('update_id','False')
        ModelRisk = request.POST.get('ModelRisk', 'False') 
        annulrevfreq = request.POST.get('annulrevfreq','False')
        addedby = request.session['uid']
        if updated_id != 'False':
            third_party_api_url = getAPIURL()+'validationReviewFrequency/'
            print("third_party_api_url",third_party_api_url)
            data_to_update = {
                'model_risk':ModelRisk,
                'annual_review_frequency':annulrevfreq,
                'addedby':addedby,
                'id':updated_id
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.put(third_party_api_url, data= json.dumps(data_to_update),headers=header)
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
        else:
            third_party_api_url = getAPIURL()+'validationReviewFrequency/'
            data_to_save = {
                'model_risk':ModelRisk,
                'annual_review_frequency':annulrevfreq,
                'addedby':addedby        
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
            print("----------------5",json.loads(response.content))
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def edit_frequency(request,id):
    print("edit_frequency",id)
    try: 
        third_party_api_url = getAPIURL()+'validationReviewFrequency/'+id
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response edit frequency--------------------------",response.content)
        data = json.loads(response.content)
        modelrisk = data['data'][0]['model_risk']
        annual_review_frequency = data['data'][0]['annual_review_frequency']
        # task_function_obj=TaskFunctionMaster.objects.get(task_function_aid=id)
        # task_function_label=task_function_obj.task_function_label
        # task_function_description=task_function_obj.task_function_description
        return render(request, 'addvalidationfrequency.html',{'modelrisk':modelrisk,
                                                     'annual_review_frequency':annual_review_frequency,'id':id})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc()) 
    print()
    mdl_id = request.POST.get('mdl_id','False')
    userlist = request.POST.getlist('u_type')
    print("userlist",userlist)
    str1 = userlist[0]
    finallist = str1.split(',')
    print("str",finallist)
    enddate = request.POST.get('enddate','False')
    for i in finallist:
        print("i",i)
        api_url=getAPIURL()+"VrSubmissionAllocationAPI/"       
        data_to_save={'mdl_id':mdl_id,
            'u_aid':i,
            'enddate':enddate,
            'addedby':request.session['uid'] 
            
        } 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
            
    return JsonResponse(json.loads(response.content))

def Backup_userdetails(request):
   
    try:
        id=request.GET['backupid'] 
        user_obj=Users.objects.get(u_aid=int(id))       
        u_first_name=user_obj.u_fname
        u_last_name=user_obj.u_lname
        u_email=user_obj.u_email
        u_status=user_obj.activestatus
            
        return JsonResponse({'u_f_name':u_first_name,'u_l_name':u_last_name,'u_email':u_email,'u_status':u_status})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())
        print("edit_user",id)

def publishVR(request):
    try: 
        mdl_id=request.GET['mdl_id']
        api_url=getAPIURL()+"InsertVRPublishingInfo/"       
        data_to_save={'mdl_id':mdl_id,
            'uid':request.session['uid'],  
        } 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
            
        return JsonResponse(json.loads(response.content))
    except Exception as e:
        print (e)

def getMdlDocs(request):
    try: 
        mdl_id=request.GET['mdl_id']
        resultDocumentation = objvalidation.getModelDocs(mdl_id)
        return JsonResponse({'docs':resultDocumentation,'mdl_id':mdl_id})
    except Exception as e:
        print (e)

def index_view(request):
    try:
        return render(request, 'index.html', {
            'rooms':[],
        })
    except Exception as e:
        print (e, traceback.print_exc())


def room_view(request, room_name):
    chat_room, created = Room.objects.get_or_create(name=room_name)
    return render(request, 'room.html', {
        'room': chat_room,
    })



def PerfMontrSetupMRM(request):
    try:
        third_party_api_url = getAPIURL()+'Fetchmdlid_MRM/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'addedby':request.session['uid'],
            'dept_aid':request.session['dept']
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        data=json.loads(responseget.content)
        return render(request, 'PerfMontrSetup_MRM.html',{'data':data['mdlids'],'freqdata':data['frequency'],'ModelMatrics':data['mdlmetric'],'BusinessMetric':data['bussmetric'],'data_mdlids':data['data_mdlids']})
     
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc()) 

def PerfMontrPrdnData(request):
    try:  
        third_party_api_url = getAPIURL()+'FetchPerfMonMdlId/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'dept_aid':request.session['dept']
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        
        data=responseget.json() 

        return render(request, 'PerfMontrPrdnData.html',{'data':data['data'],'buss_data':data['buss_data']})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())


def mmlabeltoexcel(request):
    try:
        third_party_api_url = getAPIURL()+'getMaxFreqSeq/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        freidx=1
        is_new=0
        data_to_save = {
            'mdl_id':request.GET.get('mdlid', 'False')  
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_save),headers=header)             
        data=responseget.json() 
        for ir,val in data['freqData'].items():
            is_new=val['addorupdate']
            freidx=val['freqidx']
        mdlid =request.GET.get('mdlid', 'False') 

        third_party_api_url = getAPIURL()+'getTemplateData/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = { 
            'mdl_id':mdlid ,
            'freq_idx':freidx
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        # data=json.loads(responseget.content)
        data=responseget.json()
        # print("responseget--------------------------",data['mmdata']) 
        lst = []
        for i in data['mmdata']:
            lst.append(i['mm_details']['mm_label'])
        print("new label lst",lst)
        dframe1 = pd.DataFrame(index = ['0'],columns = lst)  
        print("dframe",dframe1)
        BASE_DIR = Path(__file__).resolve().parent.parent 
               
        destination_path = str(BASE_DIR)+'/static/document_files/'+ mdlid +'/templates/'     
        # destination_path = os.path.join(BASE_DIR, 'static\\document_files\\'+mdlid+'\\')
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)           
        # dframe1.to_excel( str(BASE_DIR) + '/static/document_files/'+ mdlid + '/'+mdlid+'.xlsx',index=False)
        dframe1.to_excel(destination_path + mdlid+'.xlsx',index=False)

        modelmatrics = request.GET.get('modelmatrics','false')
        mdlid = request.GET.get('mdlid','false')
        datatype = request.GET.get('datatype','false')
        try:
            third_party_api_url = getAPIURL()+'MdlIdDataCheck/'
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            data_to_get = {
                'mdlid':mdlid,
            }
            responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
            data=json.loads(responseget.content)
            print("responseget for model matrics updated new for hide--------------------------",data['data_a'])
            data_check = data['data_a']
        except Exception as e:
            print("error data is",e)
            data_check = 'None'
        return JsonResponse({'file': '/static/document_files/'+ mdlid +'/templates/' +mdlid+'.xlsx','msg':"Excel Downloaded successfully",'model_matrics':lst,'data_check':data_check})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())


def PerfMontr(request):
    try:  
        third_party_api_url = getAPIURL()+'getMdlIdforPerfMontr/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'addedby':request.session['uid'],
            'dept_aid':request.session['dept']
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        data=json.loads(responseget.content)
        print("responseget for mdlid updated new--------------------------",data)        
        return render(request, 'PerfMontr.html',{'data':data['mdlids'],'freqdata':data['frequency'],'ModelMatrics':data['mdlmetric'],'BusinessMetric':data['bussmetric']})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def PerfMontrMRM(request):
    try:  
        third_party_api_url = getAPIURL()+'Perm_Override_MRM/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'addedby':request.session['uid'],
            'dept_aid':request.session['dept']
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        data=json.loads(responseget.content)   
        return render(request, 'PerfMontr_MRMApprl.html',{'data':data['mdlids'],'freqdata':data['frequency'],'ModelMatrics':data['mdlmetric'],'dmh_mdlids':data['dmh_mdlids']})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def DataMontrOverHistory(request):
    try:
        mdl_id = request.GET.get('mdl_id', 'False') 
        third_party_api_url = getAPIURL()+'GetHistoryMsg/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'room_id':'',
            'mdl_id':mdl_id,
            'addedby':request.session['uid']
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        data=responseget.json()
        print("responseget History Data--------------------------",data['dataMntrHstry'])
        return JsonResponse({"isvalid":"true",'data':data['dataMntrHstry']})  
    except Exception as e:
        print("error is",e)

def Update_Data_Monitoring_Override_History(request):
    print()
    try:
        mdl_id = request.GET.get('mdlId','false')
        datalist = json.loads(request.GET['datalist'])
        print('datalist',datalist)

        third_party_api_url_a = getAPIURL()+'getMaxFreqSeqData/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        freidx=1
        is_new=0
        data_to_save_a = {
            'mdl_id':mdl_id, 
        }
        responseget = requests.get(third_party_api_url_a, data= json.dumps(data_to_save_a),headers=header)             
        data=responseget.json() 
        for ir,val in data['freqData'].items():
            is_new=val['addorupdate']
            freidx=val['freqidx']

        for i in datalist:
            print("i",i)
            third_party_api_url_b = getAPIURL()+'Update_Data_Monitoring_Override_History/'
            data_to_save_b = {
                'Mdl_ID':mdl_id,
                'Metric':int(i['metric']),
                'Feature':i['feature'],
                'freq_idx':freidx,
                # 'New_Value':i['new_value'],
                # 'Threshold':i['Threshold'],
                # 'Warning':i['Warning'],
                # 'Actual':i['actual'],
                'Added_by':request.session['uid']
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(third_party_api_url_b, data= json.dumps(data_to_save_b),headers=header)
            data=json.loads(response.content)
            print("data",data)
            print("response content",response.content,response.status_code)
        return JsonResponse({'isvalid':'true'})
    except Exception as e:
        print("error is",e)
        
def PerfMontrDataFetch(request):
    print("request data-------------",request.GET.get)
    mdlid =request.GET.get('mdlid', 'False') 
    try:
        third_party_api_url = getAPIURL()+'getMaxFreqSeq/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        freidx=1
        is_new=0
        data_to_save = {
            'mdl_id':mdlid, 
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_save),headers=header)             
        data=responseget.json() 
        for ir,val in data['freqData'].items():
            is_new=val['addorupdate']
            freidx=val['freqidx']
        third_party_api_url = getAPIURL()+'getTemplateData/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'room_id':"",
            'mdl_id':mdlid,
            'addedby':request.session['uid'],
            'freq_idx':freidx
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        # data=json.loads(responseget.content)
        data=responseget.json()
        # print("responseget--------------------------",data['mmdata'])
        print('le)n of newval ',(data['overdata']) )
        for ir,val in data['overdata'].items():
                print('metric and newval ',val['metric'] , val['new_value'])

        exclfile = pd.read_excel(os.path.join(BASE_DIR, 'static/document_files/'+mdlid+'/'+'production_output/'+mdlid+'.xlsx'))
        

        arrMetricType=[]
        frequency=""

        for i in data['mmdata']:
            dict1={}
            metrictype='normal'
            iVal=exclfile[i['mm_details']['mm_label']].iloc[0]
            iThresholdVal=i['threshold']
            iWarningVal=i['warning']
            sType=i['metric_value_type']
            iActualWarningVal=0.0
            iTotalWarningVal=0.0
            frequency=i['frequency']
            
            if sType == "percentage":
                iActualWarningVal=(iWarningVal*.01)
                iThresholdVal=iThresholdVal*0.01
                iVal=iVal*0.01
            iTotalWarningVal=iThresholdVal+iActualWarningVal
            if iVal > iTotalWarningVal:
                metrictype="Critical"
            elif iVal<=iThresholdVal:
                metrictype="Normal"
            elif iVal<=iTotalWarningVal and iVal > iThresholdVal:
                metrictype="Warning"  
            if len(data['overdata'])>0:
                  for ir,val in data['overdata'].items():
                    if i['mm_details']['mm_aid'] == val['metric']:
                        metrictype =val['new_value']

            dict1['metrictype']=metrictype 
            dict1['mm_aid']=i['mm_details']['mm_aid']
            arrMetricType.append(dict1)     
            third_party_api_url = getAPIURL()+'Save_Performance_Monitoring_Result/'
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            data_to_get = {
                'Mdl_ID':i['mdl_id'],
                'Metric':str(i['mm_details']['mm_aid']),
                'Prdn_Value':str(exclfile[i['mm_details']['mm_label']].iloc[0]),
                'Metric_flag':metrictype,
                'addedby':request.session['uid'],
                'freq_idx':freidx
            }
            #print("data_to_get ",data_to_get)
            responseget = requests.post(third_party_api_url, data= json.dumps(data_to_get),headers=header)
            #data=responseget.json()        
            # print("i ",i['threshold'],i['mm_details']['mm_label'],exclfile[i['mm_details']['mm_label']].iloc[0],i['metric_value_type'],i['threshold'],i['warning'],metrictype)      

        print("json type ",arrMetricType)
        return JsonResponse({"isvalid":"true",'data':data['mmdata'],'frequency':frequency,'prdxn_data':json.loads(exclfile.to_json(orient='index')),'jsonarr':arrMetricType})     
    except Exception as e:
        print("error is",e,traceback.print_exc())
        return JsonResponse({"isvalid":"false"})
    
@api_view(['POST'])
def addperfromancediscussion(request):
    try:
        print("request session",request.session.items())
        room_id = request.POST.get('room_id', 'False') 
        comment = request.POST.get('comment','False')
        addedby = request.session['uid']
        # addedon = datetime.now()
        
        third_party_api_url = getAPIURL()+'ConnectionMsgSave/'
        data_to_save = {
            'room_id':room_id,
            'comment':comment,
            'addedby':addedby
        }
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
        
        response_a = json.loads(response.content)

        #get
        data_to_get = {
            'addedby':addedby
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        data=responseget.json()
        print("responseget--------------------------",data['data'])
        
        return JsonResponse(data['data'])
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def PerfMontrSetup(request):
    try:
        third_party_api_url = getAPIURL()+'Fetchmdlid/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'addedby':request.session['uid'],
            'dept_aid':request.session['dept']
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        data=json.loads(responseget.content)
        return render(request, 'PerfMontrSetup.html',{'data':data['mdlids'],'freqdata':data['frequency'],'ModelMatrics':data['mdlmetric'],'BusinessMetric':data['bussmetric']})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())


@api_view(['GET'])
def gethistorymsg(request):
    try:
        room_id = request.GET.get('room_id', 'False') 
        mdl_id = request.GET.get('mdl_id', 'False') 
        print("mdl_id--------",mdl_id)
        third_party_api_url = getAPIURL()+'GetHistoryMsg/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_get = {
            'room_id':room_id,
            'mdl_id':mdl_id,
            'addedby':request.session['uid']
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        data=responseget.json()
        print("responseget--------------------------2",data['mmdata'])

        print("responseget history data--------------------------",data['data'])
        
        # return JsonResponse({'data':data['data'],'mmdata':data['mmdata'],'mo_approved':data['mo_approved']})
        return JsonResponse({'data':data['data'],'mmdata':data['mmdata'],'mdl_category_data':data['mdl_category_data']})
        # return JsonResponse(data['data'])
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

def UpdateModelMatricsData(request):
    try:
        mdl_id = request.GET.get('mdl_id', 'False') 
        third_party_api_url = getAPIURL()+'ModelMatricsTempData/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_update = {
            'mdl_id':mdl_id
        }
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_update),headers=header) 
    
        return JsonResponse(json.loads(responseget.content))
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def ApproveModelMatricsData(request):
    try:
        mdl_id = request.GET.get('mdl_id', 'False') 
        third_party_api_url = getAPIURL()+'ApproveModelMatricsData/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_update = {
            'mdl_id':mdl_id
        }
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_update),headers=header)
         
    
        return JsonResponse(json.loads(responseget.content))
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

@api_view(['GET'])
def Fetchmdlid(request):
    try:
        third_party_api_url = getAPIURL()+'Fetchmdlid/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'addedby':request.session['uid']
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        data=responseget.json()
        print("responseget for mdlid--------------------------",data['data'])
        
        return JsonResponse(data['data'])
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def Fetchmodelmatrics(request):
    try:
        dept_id = request.GET.get('dept_id', 'False') 
        third_party_api_url = getAPIURL()+'FetchModelMatrics/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'dept_aid':dept_id
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        # data=responseget.json()
        print("responseget for modelmaatrics--------------------------",json.loads(responseget.content))
        
        return JsonResponse(json.loads(responseget.content))
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def savemodelmatrics(request):
    print("request data model matrics",request.GET)
    try: 
        datalist = json.loads(request.GET['datalist'])
        print("datalist",datalist)
        mdlid = request.GET['mdlId']
        print("mdlid",mdlid)
        frequency = request.GET['frequency']
        api_url=getAPIURL()+"ModelMatricsAPI/"  
        for i in datalist:   
            data_to_save={ 
                'mdl_id': mdlid,
                'metric':i['AID'],
                'threshold':int(i['Threshold']),
                'warning':int(i['Warning']),
                'frequency':frequency,
                'metric_value_type':i['Percentage'],
                'added_by':request.session['uid']
            } 
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
            
        return JsonResponse({'istaken':'true'})
    except Exception as e:
        print('assignValidation ',e)
        print('assignValidation traceback is ', traceback.print_exc()) 
        return JsonResponse({'istaken':'false'})

@api_view(['GET'])
def getMdlDataForMRM(request):
    try:
        room_id = request.GET.get('room_id', 'False') 
        mdl_id = request.GET.get('mdl_id', 'False') 
        third_party_api_url = getAPIURL()+'getMdlDataForMRM/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'room_id':room_id,
            'mdl_id':mdl_id,
            'addedby':request.session['uid']
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        data=responseget.json() 
        
        return JsonResponse({'data':data['data'],'mdlcatdata':data['mdlcatdata'],'mmdata':data['mmdata'],'mo_approved':data['mo_approved']})
        # return JsonResponse(data['data'])
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def Save_Performance_Monitoring_Override_History(request):
    try:
        third_party_api_url = getAPIURL()+'getMaxFreqSeq/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        freidx=1
        is_new=0
        data_to_save = {
            'mdl_id':request.GET['Mdl_ID'], 
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_save),headers=header)             
        data=responseget.json() 
        for ir,val in data['freqData'].items():
            is_new=val['addorupdate']
            freidx=val['freqidx']
        #Mdl_ID,Metric,New_Value,Added_by,Added_On
        third_party_api_url = getAPIURL()+'Save_Performance_Monitoring_Override_History/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_get = {
            'Mdl_ID':request.GET['Mdl_ID'],
            'Metric':request.GET['Metric'],
            'New_Value':request.GET['New_Value'],
            'Old_Value':request.GET['Old_Value'],
            'Added_by':request.session['uid'],
            'freq_idx':freidx
        }
        print("data_to_get ",data_to_get)
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        
        return JsonResponse({"isvalid":"true"})     
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})


def Save_Performance_Monitoring_Final_Result(request):
    try:
        #Mdl_ID,Metric,New_Value,Added_by,Added_On
        third_party_api_url = getAPIURL()+'getMaxFreqSeq/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        freidx=1
        is_new=0
        data_to_save = {
            'mdl_id':request.GET['Mdl_ID'], 
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_save),headers=header)             
        data=responseget.json() 
        for ir,val in data['freqData'].items():
            is_new=val['addorupdate']
            freidx=val['freqidx']
        third_party_api_url = getAPIURL()+'Save_Performance_Monitoring_Final_Result/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_get = {
            'Mdl_ID':request.GET['Mdl_ID'],
            'Metric':request.GET['Metric'],
            'New_Value':request.GET['New_Value'],
            'Added_by':request.session['uid'],
            'freq_idx':freidx,
        }
        print("data_to_get Result ",data_to_get)
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        
        return JsonResponse({"isvalid":"true"})     
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})

def Update_Performance_Monitoring_Override_History(request):
    try:
        third_party_api_url = getAPIURL()+'getMaxFreqSeq/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        freidx=1
        is_new=0
        data_to_save = {
            'mdl_id':request.GET['Mdl_ID'], 
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_save),headers=header)             
        data=responseget.json() 
        for ir,val in data['freqData'].items():
            is_new=val['addorupdate']
            freidx=val['freqidx']
        #Mdl_ID,Metric,New_Value,Added_by,Added_On
        third_party_api_url = getAPIURL()+'Update_Performance_Monitoring_Override_History/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_get = {
            'Mdl_ID':request.GET['Mdl_ID'],
            'Metric':request.GET['Metric'], 
            'Added_by':request.session['uid'],
            'freq_idx':freidx
        }
        print("data_to_get ",data_to_get)
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        
        return JsonResponse({"isvalid":"true"})     
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})



def savebusinessmatrics(request):
    print("request data business matrics",request.GET)
    try: 
        datalist = json.loads(request.GET['datalist'])
        print("datalist",datalist)
        mdlid = request.GET['mdlId']
        print("mdlid",mdlid)
        frequency = request.GET['frequency']
        api_url=getAPIURL()+"BusinessMetricAPI/"  
        for i in datalist: 
            print("i",i)
            print("threshold",str(i['Threshold']),"warning",str(i['Warning']))    
            data_to_save={ 
                'mdl_id': mdlid,
                'metric':i['AID'],
                'threshold':int(i['Threshold']),
                'warning':int(i['Warning']),
                'frequency':frequency,
                'metric_value_type':i['Percentage'],
                'added_by':request.session['uid']
            } 
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
            print("response business metric",response.content)
        return JsonResponse(json.loads(response.content))
    except Exception as e:
        print('assignValidation ',e)
        print('assignValidation traceback is ', traceback.print_exc()) 
        return JsonResponse({'istaken':'false'})

def savebusmetrics(request):
    print()
    bm_label =request.GET.get('bm_label', 'False') 
    bm_description =request.GET.get('bm_description', 'False') 
    # mm_status = request.GET.get('mm_status','False')
    # mm_is_global = request.GET.get('mm_is_global','False')
    added_by= request.session['uid']
    dept_id = request.session['dept']

    try:
        third_party_api_url = getAPIURL()+'AddBusinessMetricAPI/'
        data_to_save = {
            'bm_label' : bm_label,
            'bm_description':bm_description,
            'bm_status':1,
            'bm_is_global':1,
            'added_by':added_by

        }
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)        
        data = json.loads(response.content)
        print("check response",data)
        #model metrixs  dept
        third_party_api_url = getAPIURL()+'AddBusinessMetricsDept/'
        data_to_save_dept = {
            'bm_aid':data['data']['bm_aid'],
            'dept_aid':dept_id,
            'added_by_field':request.session['uid']
        }
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response_dept = requests.post(third_party_api_url, data= json.dumps(data_to_save_dept),headers=header)
        dept_data = json.loads(response_dept.content)
        return JsonResponse(dept_data)
    except Exception as e:
        print("error is",e)

@api_view(['GET'])
def gethistorymsgbus(request):
    try:
        room_id = request.GET.get('room_id', 'False') 
        mdl_id = request.GET.get('mdl_id', 'False') 
        third_party_api_url = getAPIURL()+'GetHistoryMsg/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'room_id':room_id,
            'mdl_id':mdl_id,
            'addedby':request.session['uid']
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        data=responseget.json()
        print("responseget business--------------------------",data['bmdata'])
        
        return JsonResponse({'data':data['data'],'bmdata':data['bmdata'],'mdlcatdatabus':data['mdlcatdatabus']})
        # return JsonResponse(data['data'])
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def mmlabeltoexcelforbus(request):
    try:
        print("request data-------------",request.GET.get)
        mdlid =request.GET.get('mdlid', 'False') 

        third_party_api_url = getAPIURL()+'GetHistoryMsg/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'room_id':"",
            'mdl_id':mdlid,
            'addedby':request.session['uid']
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        # data=json.loads(responseget.content)
        data=responseget.json()
        # print("responseget--------------------------",data['mmdata'])
        print("responseget new api fetch bmlabel agains mdlid--------------------------",data['bmdata_b'])
        lst = []
        for i in data['bmdata_b']:
            lst.append(i['bm_details']['bm_label'])
        print("new label lst",lst)
        dframe1 = pd.DataFrame(index = ['0'],columns = lst)  
        BASE_DIR = Path(__file__).resolve().parent.parent      
        destination_path = str(BASE_DIR)+'/static/document_files/'+mdlid +'/templates/'     
        # destination_path = os.path.join(BASE_DIR, 'static\\document_files\\'+mdlid+'\\')
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)           
        # dframe1.to_excel( str(BASE_DIR) + '/static/document_files/'+ mdlid + '/'+mdlid+'.xlsx',index=False)
        dframe1.to_excel(destination_path + 'Business_KPI_'+mdlid+'.xlsx',index=False)
        return JsonResponse({'file': '/static/document_files/'+mdlid +'/templates/Business_KPI_'+mdlid+'.xlsx','msg':"Excel Downloaded successfully"})
    except Exception as e:
        print('error is ',e)
        print('error traceback is ', traceback.print_exc())
 
def UpdatebusinessMatricsDatabus(request):
    try:
        mdl_id = request.GET.get('mdl_id', 'False') 
        third_party_api_url = getAPIURL()+'BusinessMatricsTempData/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_update = {
            'mdl_id':mdl_id
        }
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_update),headers=header)
        # data=json.loads(responseget.content)
        print("responseget for check data Business matrics--------------------------",json.loads(responseget.content))
    
        return JsonResponse(json.loads(responseget.content))
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def getBusinessDataForMRM(request):
    try:
        room_id = request.GET.get('room_id', 'False') 
        mdl_id = request.GET.get('mdl_id', 'False') 
        third_party_api_url = getAPIURL()+'getBusinessDataForMRM/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'room_id':room_id,
            'mdl_id':mdl_id,
            'addedby':request.session['uid']
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        data=responseget.json() 
        
        return JsonResponse({'data':data['data'],'bmdata':data['bmdata'],'mo_approved':data['mo_approved'],'mdlcatdatabus':data['mdlcatdatabus']})
        # return JsonResponse(data['data'])
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def getBusinessDataForMRM(request):
    try:
        room_id = request.GET.get('room_id', 'False') 
        mdl_id = request.GET.get('mdl_id', 'False') 
        third_party_api_url = getAPIURL()+'getBusinessDataForMRM/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'room_id':room_id,
            'mdl_id':mdl_id,
            'addedby':request.session['uid']
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        data=responseget.json() 
        
        return JsonResponse({'data':data['data'],'bmdata':data['bmdata'],'mo_approved':data['mo_approved']})
        # return JsonResponse(data['data'])
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def ApproveBusinessMatricsData(request):
    try:
        mdl_id = request.GET.get('mdl_id', 'False') 
        third_party_api_url = getAPIURL()+'ApproveBusinessMatricsData/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_update = {
            'mdl_id':mdl_id
        }
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_update),headers=header)
         
    
        return JsonResponse(json.loads(responseget.content))
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def PerfMontrDataFetchBuss(request):
    print("request data-------------",request.GET.get)
    mdlid =request.GET.get('mdlid', 'False') 
    try:
        third_party_api_url = getAPIURL()+'GetHistoryMsgBuss/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'room_id':"",
            'mdl_id':mdlid,
            'addedby':request.session['uid']
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        # data=json.loads(responseget.content)
        data=responseget.json()
        # print("responseget--------------------------",data['mmdata'])
        print("response perf montr data check--------------------------",data['bmdata'])

        dataframe = os.path.join(BASE_DIR, 'static/document_files/'+mdlid+'/'+'production_output/'+mdlid+'.xlsx')
        exclfile = pd.read_excel(os.path.join(BASE_DIR, 'static/document_files/'+mdlid+'/'+'production_output/'+mdlid+'.xlsx'))
        print("excel ",exclfile)

        arrMetricType=[]

        for i in data['bmdata']:
            dict1={}
            metrictype='normal'
            iVal=exclfile[i['bm_details']['bm_label']].iloc[0]
            iThresholdVal=i['threshold']
            iWarningVal=i['warning']
            sType=i['metric_value_type']
            iActualWarningVal=0.0
            iTotalWarningVal=0.0
            
            if sType == "percentage":
                iActualWarningVal=(iWarningVal*.01)
                iThresholdVal=iThresholdVal*0.01
                iVal=iVal*0.01
            iTotalWarningVal=iThresholdVal+iActualWarningVal
            if iVal > iTotalWarningVal:
                metrictype="Critical"
            elif iVal<=iThresholdVal:
                metrictype="Normal"
            elif iVal<=iTotalWarningVal and iVal > iThresholdVal:
                metrictype="Warning"   
            dict1['metrictype']=metrictype
            dict1['mm_aid']=i['bm_details']['bm_aid']
            arrMetricType.append(dict1)

            
            third_party_api_url = getAPIURL()+'getMaxFreqSeq_Buss/'
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            freidx=1
            is_new=0
            data_to_save = {
                'mdl_id':mdlid, 
            }
            responseget = requests.get(third_party_api_url, data= json.dumps(data_to_save),headers=header)             
            data_maxfreq=responseget.json() 
            for ir,val in data_maxfreq['freqData'].items():
                is_new=val['addorupdate']
                freidx=val['freqidx']

            third_party_api_url = getAPIURL()+'Save_Buss_KPI_Monitoring_Result/'
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            data_to_get = {
                'Mdl_ID':i['mdl_id'],
                'Metric':str(i['bm_details']['bm_aid']),
                'Prdn_Value':str(exclfile[i['bm_details']['bm_label']].iloc[0]),
                'Metric_flag':metrictype,
                'addedby':request.session['uid'],
                'freq_idx':freidx
            }
            #print("data_to_get ",data_to_get)
            responseget = requests.post(third_party_api_url, data= json.dumps(data_to_get),headers=header)
            #data=responseget.json()           

            # print("i ",i['threshold'],i['mm_details']['mm_label'],exclfile[i['mm_details']['mm_label']].iloc[0],i['metric_value_type'],i['threshold'],i['warning'],metrictype)      

        print("json type ",arrMetricType)
        return JsonResponse({"isvalid":"true",'data':data['bmdata'],'prdxn_data':json.loads(exclfile.to_json(orient='index')),'jsonarr':arrMetricType})     
    except Exception as e:
        print("error is",e,traceback.print_exc())
        return JsonResponse({"isvalid":"false"})

def Save_Buss_KPI_Monitoring_Override_History(request):
    try:
        #Mdl_ID,Metric,New_Value,Added_by,Added_On
        
        third_party_api_url = getAPIURL()+'getMaxFreqSeq_Buss/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        freidx=1
        is_new=0
        data_to_save = {
            'mdl_id':request.GET['Mdl_ID'], 
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_save),headers=header)             
        data_maxfreq=responseget.json() 
        for ir,val in data_maxfreq['freqData'].items():
            is_new=val['addorupdate']
            freidx=val['freqidx']
        third_party_api_url = getAPIURL()+'Save_Buss_KPI_Monitoring_Override_History/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_get = {
            'Mdl_ID':request.GET['Mdl_ID'],
            'Metric':request.GET['Metric'],
            'New_Value':request.GET['New_Value'],
            'Added_by':request.session['uid'],
            'freq_idx':freidx
        }
        print("data_to_get ",data_to_get)
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        
        return JsonResponse({"isvalid":"true"})     
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})


def Save_Buss_KPI_Monitoring_Final_Result(request):
    try:
        #Mdl_ID,Metric,New_Value,Added_by,Added_On
        
        third_party_api_url = getAPIURL()+'getMaxFreqSeq_Buss/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        freidx=1
        is_new=0
        data_to_save = {
            'mdl_id':request.GET['Mdl_ID'], 
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_save),headers=header)             
        data_maxfreq=responseget.json() 
        for ir,val in data_maxfreq['freqData'].items():
            is_new=val['addorupdate']
            freidx=val['freqidx']
        third_party_api_url = getAPIURL()+'Save_Buss_KPI_Monitoring_Final_Result/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_get = {
            'Mdl_ID':request.GET['Mdl_ID'],
            'Metric':request.GET['Metric'],
            'New_Value':request.GET['New_Value'],
            'Added_by':request.session['uid'],
            'freq_idx':freidx

        }
        print("data_to_get Result ",data_to_get)
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        
        return JsonResponse({"isvalid":"true"})     
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})

def Save_Performance_Monitoring_Resolution(request):
    try:
        #Mdl_ID,Metric,New_Value,Added_by,Added_On
        third_party_api_url = getAPIURL()+'Save_Performance_Monitoring_Resolution/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_get = {
            'Mdl_ID':request.GET['Mdl_ID'],
            'Resolution':request.GET['Resolution'],
            'Added_by':request.session['uid']
        }
        print("data_to_get Result ",data_to_get)
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        
        return JsonResponse({"isvalid":"true"})     
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})

def Save_Buss_KPI_Monitoring_Resolution(request):
    try:
        #Mdl_ID,Metric,New_Value,Added_by,Added_On
        
        third_party_api_url = getAPIURL()+'getMaxFreqSeq_Buss/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        freidx=1
        is_new=0
        data_to_save = {
            'mdl_id':request.GET['Mdl_ID'], 
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_save),headers=header)             
        data_maxfreq=responseget.json() 
        for ir,val in data_maxfreq['freqData'].items():
            is_new=val['addorupdate']
            freidx=val['freqidx']
        third_party_api_url = getAPIURL()+'Save_Buss_KPI_Monitoring_Resolution/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_get = {
            'Mdl_ID':request.GET['Mdl_ID'],
            'Resolution':request.GET['Resolution'],
            'Added_by':request.session['uid'],
            'freq_idx':freidx
        }
        print("data_to_get Result ",data_to_get)
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        
        return JsonResponse({"isvalid":"true"})     
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})
    


def new_modelmetric(request):
    try:   
        third_party_api_url = getAPIURL()+'editmodelmetrics/'+id
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response ------Model Metrics------",response.content)
        model_metric_data = json.loads(response.content)
        mm_aid = model_metric_data['data']['mm_aid']
        mm_label = model_metric_data['data']['mm_label']
        mm_description = model_metric_data['data']['mm_description']
        mm_status = 1
        mm_is_global = 1
        departments = model_metric_data['data']['departments']
        dept_list = model_metric_data['data']['departments_list']
        print("department",departments)
        #department
        third_party_api_url = getAPIURL()+'department/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response_dept = requests.get(third_party_api_url, headers=header)

        return render(request, 'addModelMetrics.html',{'mm_aid':mm_aid,'mm_label':mm_label,'mm_description':mm_description,'mm_status':mm_status,'mm_is_global':mm_is_global,'departments':departments,'users':json.loads(response_dept.content),'dept_list':dept_list})
    
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())
 
def datamatricsfeature(request):
    try:  
        mdlid =request.GET.get('mdl_id', 'False')
        print("mdlid",mdlid)
        # BASE_DIR = Path(__file__).resolve().parent.parent 
        # destination_path = str(BASE_DIR)+'/static/document_files/'+ mdlid + '/' +'templates/'+mdlid+'.xlsx'
        # print("file----------",destination_path)
        # df = pd.read_excel(destination_path)
        # print("df----------",df.columns.to_list())
        # print("df datatypes",df.dtypes.to_list())
        # datatypes = dict(df.dtypes)
        # print("datatypes",datatypes)
        file_id=find_max_file_id(mdlid)
        # dataset=request.session['vt_dataset']
        dataset = ''
        df=find_src_data(file_id,dataset) 
        gridtypes = []
        dttypes = dict(df.dtypes)
        print("dttypes new",dttypes) 
        irow=0
        
        for key,val in dttypes.items():
            print('key',key,'val',val)
            dictcols={}
            dictcols['colName']= key
            if df[key].dtypes=="int64" or df[key].dtypes=="float64":   
                dictcols['type']='int'
            elif df[key].dtypes=="object":
                dictcols['type']='object'
            else:
                dictcols['type']='object'
            # dictcols['notnull'] = df[key].count()
            # dictcols['null'] = len(df)-df[key].count()
            irow+=1
            gridtypes.append(dictcols)
            
        print("gridtypes",gridtypes)

        ## Delete Code ##
        third_party_api_url = getAPIURL()+'SaveTempFeatureMatricSelection/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_delete = {
            'mdl_id':mdlid
        }
        responsedelete = requests.delete(third_party_api_url, data= json.dumps(data_to_delete),headers=header)
        
        # data = json.loads(responsedelete.content)

        # print('response delete',data['data']) 
        
        # a = json.dumps(gridtypes)
        # print("json data",a.to_json(orient='index'))

        ## Get History msg ##
        third_party_api_url_a = getAPIURL()+'GetHistoryMsg/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get_d = {
            'room_id':'',
            'mdl_id':mdlid,
            'addedby':request.session['uid']
        }
        responseget = requests.get(third_party_api_url_a, data= json.dumps(data_to_get_d),headers=header)
        data=responseget.json()
        print("responseget data--------------------------",data['dmdata'])
        
        # return JsonResponse({'data':data['data'],'bmdata':data['bmdata']})

        return JsonResponse({'data':gridtypes,'dmdata':data['dmdata']})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def selectdataMetric(request):
    try:
        data_types = request.GET.get('data_types', 'False') 
        
        third_party_api_url = getAPIURL()+'SelectdataMetrics/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_get = {
            'type':data_types
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_get),headers=header)
        
        data = json.loads(responseget.content)

        print('response get data Metric',data)

        return JsonResponse(json.loads(responseget.content))

    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def SaveTempFeatureMatricData(request):
    try:
        import statistics
        mdl_id = request.GET.get('mdl_id', 'False') 
        feature = request.GET.get('feature', 'False')
        print("feature",feature)
        data_matric = request.GET.get('data_matric', 'False') 

        file_id=find_max_file_id(mdl_id)
        dataset = ''
        df=find_src_data(file_id,dataset)
        print("feature column data",df[feature])
        if data_matric == 'Null':
            columndata = df[feature].isnull().sum()
            print("isnull column",columndata/len(df[feature])*100)
            percentage = columndata/len(df[feature])*100
        elif data_matric == 'Mean':
            columndata = df[feature].mean()
            print("columndata mean",columndata)
            percentage = columndata
        elif data_matric == 'Median':
            columndata = df[feature].to_list()
            percentage = statistics.median(columndata)
            print("Median",percentage)
        elif data_matric == 'STD':
            columndata = df[feature].std()
            print("columndata Standard deviation",columndata)
            percentage = columndata

        third_party_api_url = getAPIURL()+'SaveTempFeatureMatricSelection/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_save = {
            'mdl_id':mdl_id,
            'feature':feature,
            'datamatrics':data_matric,
            'added_by':request.session['uid']
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_save),headers=header)
        
        data = json.loads(responseget.content)

        print('response get',data['data'])

        if len(data['data']) == 0:
            responsesave = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
            print('response save',responsesave.content)
            data = json.loads(responsesave.content)
            data['percentage'] = percentage
            print("New Data",data)
            return JsonResponse(data)
            # return JsonResponse({'msg':'Feature Data created Successfully','null_percentage':null_percentage})
        else:
            return JsonResponse({'msg':'Data Already Exist','percentage':percentage})

    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

@api_view(['GET'])
def gethistorymsgdata(request):
    try:
        room_id = request.GET.get('room_id', 'False') 
        mdl_id = request.GET.get('mdl_id', 'False') 
        third_party_api_url = getAPIURL()+'GetHistoryMsg/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'room_id':room_id,
            'mdl_id':mdl_id,
            'addedby':request.session['uid']
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        data=responseget.json()
        print("responseget data--------------------------",data['dmdata'])
        
        return JsonResponse({'data':data['data'],'dmdata':data['dmdata']})
        # return JsonResponse(data['data'])
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 


# def getIssuesByQtrOrMonth(request):
#     try: 
#         print('Token ',request.session['accessToken'])
#         objreg=Register()
#         api_url=getAPIURL()+"getIssuesByQtrOrMonth/"
#         data_to_save={'utype':request.session['utype'],
#             'dept':request.session['dept'],
#             'uid':request.session['uid'],
#             'ulvl':request.session['ulvl'],
#             'is_mrm':request.session['is_mrm'],
#             'ptype':request.GET['ptype'],   
#             'issue_from_dt':request.GET['frdate'],
#             'issue_to_dt':request.GET['todt'],
#             'issue_sts':request.GET.getlist('sts[]')
#             } 
#         #'Qtr',
#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }
#         response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
         
#         api_data=response.json() 
#         if(str(objmaster.isAutherized(request.session['ucaid'],"Dashboard")) =="0"): 
#             return render(request, 'blank.html',{'actPage':'RMSE'}) 

#         issuesByQtrOrMonth= api_data['issuesByQtrOrMonth']
#         print('issuesByQtrOrMonth ',issuesByQtrOrMonth['data'])         
        
#         return JsonResponse({'issuePriority':issuesByQtrOrMonth['data'],'chartSeries':issuesByQtrOrMonth['series']})
#     except Exception as e:
#         print('setuppycaret is ',e)
#         print('setuppycaret traceback is ', traceback.print_exc()) 
#         error_saving(request,e)


def savedatamatrics(request):
    print("request data is data matrics",request.GET)
    try: 
        datalist = json.loads(request.GET['datalist'])
        print("datalist",datalist)
        mdlid = request.GET['mdlId']
        print("mdlid",mdlid)
        frequency = request.GET['frequency']
        api_url=getAPIURL()+"DataMetricAPI/"  
        for i in datalist: 
            print("i",i)
            print("threshold",str(i['Threshold']),"warning",str(i['Warning']))    
            data_to_save={ 
                  'mdl_id': mdlid,
                'metric':i['AID'],
                'feature':i['feature'],
                'threshold':i['Threshold'],
                'mo_approval':1,
                # 'warning':int(i['Warning']),
                'warning':0,
                'frequency':frequency,
                'added_by':request.session['uid']
            } 
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
            print("response business metric",response.content)
        return JsonResponse(json.loads(response.content))
    except Exception as e:
        print('assignValidation ',e)
        print('assignValidation traceback is ', traceback.print_exc()) 
        return JsonResponse({'istaken':'false'})
    

def find_src_data(file_id,dataset=''): 
    print('dataset is method is ',dataset)
    if(dataset==''):
        print('inside blank filter')
        src_file_obj = collection.find({"file_id":int(file_id)},{'_id':0})
    else:
        print('dataset ', str(dataset)) 
        dataset = dataset.replace("\'", "\"") 
        dataset=json.loads(dataset)    
        print('dataset is ',dataset)      
        src_file_obj = collection.find(dataset,{'_id':0})

    df =  pd.DataFrame(list(src_file_obj))   
    if len(df)>0: 
        df.pop('file_id')
    print("src fn dataframe",len(df))
    return df 
     

def find_max_req_id(Mdl_Id=""):
    print("find_max_req_id")
    model_info_obj = collection_model_information.find({'Mdl_Id':Mdl_Id},{'_id':0})
    df =  pd.DataFrame(list(model_info_obj))
    #print("dataframe is ",df)
    print("dataframe max is",df['reqId'].max())    
    req_id=df['reqId'].max()
    return req_id


def datamatricsfeatureMRM(request):
    try:  
        mdlid =request.GET.get('mdl_id', 'False')
        print("mdlid",mdlid)
        
        file_id=find_max_file_id(mdlid)
        
        dataset = ''
        df=find_src_data(file_id,dataset) 
        gridtypes = []
        dttypes = dict(df.dtypes)
        print("dttypes new",dttypes) 
        irow=0
        
        for key,val in dttypes.items():
            print('key',key,'val',val)
            dictcols={}
            dictcols['colName']= key
            if df[key].dtypes=="int64" or df[key].dtypes=="float64":   
                dictcols['type']='int'
            elif df[key].dtypes=="object":
                dictcols['type']='object'
            else:
                dictcols['type']='object'
        
            irow+=1
            gridtypes.append(dictcols)
            
        print("gridtypes",gridtypes)

        ## Delete Code ##
        third_party_api_url = getAPIURL()+'SaveTempFeatureMatricSelection/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_delete = {
            'mdl_id':mdlid
        }
        responsedelete = requests.delete(third_party_api_url, data= json.dumps(data_to_delete),headers=header)

        return JsonResponse({'data':gridtypes})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def ApproveDataMatricsData(request):
    try:
        mdl_id = request.GET.get('mdl_id', 'False') 
        third_party_api_url = getAPIURL()+'ApproveDataMatricsData/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_update = {
            'mdl_id':mdl_id
        }
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_update),headers=header)
         
    
        return JsonResponse(json.loads(responseget.content))
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())


def PerfMontrDataFetch_MRMApprl(request):
    print("request data-------------",request.GET.get)
    mdlid =request.GET.get('mdlid', 'False') 
    try:
        third_party_api_url = getAPIURL()+'getMaxFreqSeq/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        freidx=1
        is_new=0
        data_to_save = {
            'mdl_id':mdlid, 
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_save),headers=header)             
        data=responseget.json() 
        for ir,val in data['freqData'].items():
            is_new=val['addorupdate']
            freidx=val['freqidx']
        print('is_new ',is_new)
        if str(is_new)=="1":
            freidx=int(freidx)-1
        third_party_api_url = getAPIURL()+'getTemplateData/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'room_id':"",
            'mdl_id':mdlid,
            'addedby':request.session['uid'],
            'freq_idx':freidx
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        # data=json.loads(responseget.content)
        data=responseget.json()
        # print("responseget--------------------------",data['mmdata'])
        print('le)n of newval ',(data['overdata']) )
        for ir,val in data['overdata'].items():
                print('metric and newval ',val['metric'] , val['new_value'])

        exclfile = pd.read_excel(os.path.join(BASE_DIR, 'static/document_files/'+mdlid+'/'+'production_output/'+mdlid+'.xlsx'))
        

        arrMetricType=[]
        frequency="" 
        for i in data['mmdata']:
            dict1={}
            metrictype='normal'
            iVal=exclfile[i['mm_details']['mm_label']].iloc[0]
            iThresholdVal=i['threshold']
            iWarningVal=i['warning']
            sType=i['metric_value_type']
            iActualWarningVal=0.0
            iTotalWarningVal=0.0
            frequency=i['frequency']
            
            if sType == "percentage":
                iActualWarningVal=(iWarningVal*.01)
                iThresholdVal=iThresholdVal*0.01
                iVal=iVal*0.01
            iTotalWarningVal=iThresholdVal+iActualWarningVal
            if iVal > iTotalWarningVal:
                metrictype="Critical"
            elif iVal<=iThresholdVal:
                metrictype="Normal"
            elif iVal<=iTotalWarningVal and iVal > iThresholdVal:
                metrictype="Warning"  
            if len(data['overdata'])>0:
                  for ir,val in data['overdata'].items():
                    if i['mm_details']['mm_aid'] == val['metric']:
                        metrictype =val['new_value']

            dict1['metrictype']=metrictype 
            dict1['mm_aid']=i['mm_details']['mm_aid']
            arrMetricType.append(dict1)     

            # print("i ",i['threshold'],i['mm_details']['mm_label'],exclfile[i['mm_details']['mm_label']].iloc[0],i['metric_value_type'],i['threshold'],i['warning'],metrictype)      

        print("json type ",arrMetricType)
        return JsonResponse({"isvalid":"true",'data':data['mmdata'],'frequency':frequency,'prdxn_data':json.loads(exclfile.to_json(orient='index')),'jsonarr':arrMetricType})     
    except Exception as e:
        print("error is",e,traceback.print_exc())
        return JsonResponse({"isvalid":"false"})
    

 
def find_max_prdn_file_id(mdlid=""):
    
    print("find_max_prdn_file_id",mdlid)
    if mdlid=="":
        print("if")
        src_file_obj = collection_prdn_file_info.find()
    else:
        print("else")
        src_file_obj = collection_prdn_file_info.find({'Mdl_Id':mdlid})
    df =  pd.DataFrame(list(src_file_obj)) 
    print("df",df)
    print("length",len(df))
    if len(df)>0: 
        file_id=df['file_id'].max()
    else:
        file_id=1 #changed by nilesh on 11.4.23
    print('file_id' ,file_id)
    return file_id


def find_prdn_src_data(file_id,dataset=''): 
    print('dataset is method is ',dataset)
    if(dataset==''):
        print('inside blank filter')
        src_file_obj = collection_prdn_src_data.find({"file_id":int(file_id)},{'_id':0})
    else:
        print('dataset ', str(dataset)) 
        dataset = dataset.replace("\'", "\"") 
        dataset=json.loads(dataset)    
        print('dataset is ',dataset)      
        src_file_obj = collection_prdn_src_data.find(dataset,{'_id':0})

    df =  pd.DataFrame(list(src_file_obj))   
    if len(df)>0: 
        df.pop('file_id')
    print("src fn dataframe",len(df))
    return df 

def prdn_data(request):
    try:
        import statistics  
        # room_id = request.GET.get('room_id', 'False') 
        mdl_id = request.GET.get('mdl_id', 'False') 
        third_party_api_url = getAPIURL()+'GetHistoryMsg/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'room_id':'',
            'mdl_id':mdl_id,
            'addedby':request.session['uid']
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        data=responseget.json()
        print("responseget data dmdata for actual value--------------------------",data['dmdata'])
        actual_val = []
        for val in data['dmdata']:
            dmdata_actual = {}
            print("val dmdata",val)
            file_id=find_max_file_id(val['mdl_id'])
            dataset = ''
            df=find_src_data(file_id,dataset)
            print("feature column dataframe",df[val['feature']])
            data_matric = val['dm_details']['data_label']
            if data_matric == 'Null':
                columndata = df[val['feature']].isnull().sum()
                print("isnull column",columndata/len(df[val['feature']])*100)
                percentage = columndata/len(df[val['feature']])*100
            elif data_matric == 'Mean':
                columndata = df[val['feature']].mean()
                print("columndata mean",columndata)
                percentage = columndata
            elif data_matric == 'Median':
                columndata = df[val['feature']].to_list()
                percentage = statistics.median(columndata)
                print("Median",percentage)
            elif data_matric == 'STD':
                columndata = df[val['feature']].std()
                print("columndata Standard deviation",columndata)
                percentage = columndata
            print("featureName----",df[val['feature']],'data_matric---',data_matric,'percentage---',percentage)
            iTotalWarningVal=val['threshold']+val['warning']
            dmdata_actual['mdl_id'] = val['mdl_id']
            dmdata_actual['metric'] = val['metric']
            dmdata_actual['threshold'] = val['threshold']
            dmdata_actual['feature'] = val['feature']
            dmdata_actual['warning'] = val['warning']
            dmdata_actual['frequency'] = val['frequency']
            dmdata_actual['dm_details'] = val['dm_details']
            dmdata_actual['actual'] = percentage
            if percentage > iTotalWarningVal:
                metrictype="Critical"
            elif percentage<= val['threshold']:
                metrictype="Normal"
            elif percentage<=iTotalWarningVal and percentage >  val['threshold']:
                metrictype="Warning" 
            dmdata_actual['performance'] = metrictype
            actual_val.append(dmdata_actual)
        print('actual_val',actual_val)

        return JsonResponse({'dmdata':data['dmdata'],'actual_val':actual_val})

    except Exception as e:
        print("error is ",e)
        
def Save_Data_Monitoring_Override_History(request):
    print("request data new history",request.GET)
    try:
        mdl_id = request.GET.get('mdlId','false')
        # datalist_sel = request.GET.getlist('datalist_sel')
        datalist_sel = json.loads(request.GET['datalist_sel'])
        print('datalist',datalist_sel)
        for i in datalist_sel:
            print("i",i)
            third_party_api_url = getAPIURL()+'Save_Data_Monitoring_Override_History/'
            data_to_save = {
                'Mdl_ID':mdl_id,
                'Metric':int(i['metric']),
                'Feature':i['feature'],
                'freq_idx':int(i['freq_idx']),
                'New_Value':i['new_value'],
                'Old_Value':i['old_value'],
                'Threshold':i['Threshold'],
                'Warning':i['Warning'],
                'Actual':i['actual'],
                'Added_by':request.session['uid']
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
            data=json.loads(response.content)
            print("data",data)
            print("response content",response.content,response.status_code)
        return JsonResponse({'msg':'Data Override History saved successfully'})
    except Exception as e:
        print("error is ",e)

def Save_Data_Monitoring_Final_Result(request):
    print("request data new",request.GET)
    try:
        mdl_id = request.GET.get('mdlId','false')
        datalist_notsel = json.loads(request.GET['datalist_notsel'])
        print('datanotsellist',datalist_notsel)
        for i in datalist_notsel:
            print("i",i)
            third_party_api_url = getAPIURL()+'Save_Data_Monitoring_Final_Result/'
            data_to_save = {
                'Mdl_ID':mdl_id,
                'Metric':int(i['metric']),
                'Feature':i['feature'],
                'freq_idx':int(i['freq_idx']),
                'New_Value':i['new_value'],
                'Old_Value':i['old_value'],
                'Threshold':i['Threshold'],
                'Warning':i['Warning'],
                'Actual':i['actual'],
                'Added_by':request.session['uid']
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
            data=json.loads(response.content)
            print("data",data)
            print("response content",response.content,response.status_code)
        return JsonResponse({'msg':'Data Metrics saved successfully'})
    except Exception as e:
        print("error is result",e)

def getModelListByUSerid(request):
    try: 
        
        api_url=getAPIURL()+"getModelListByUSerid/"
        data_to_save={'optntype':request.GET['optntype'],
            'utype':request.session['utype'],
            'dept':request.session['dept'],
            'uid':request.session['uid'],
            'ulvl':request.session['ulvl'],
            'is_mrm':request.session['is_mrm'], } 
        #'Qtr',
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json() 
        if(str(objmaster.isAutherized(request.session['ucaid'],"Dashboard")) =="0"): 
            return render(request, 'blank.html',{'actPage':'RMSE'}) 
        modelinfo=api_data['modelinfo']
        return JsonResponse({'modelinfo':modelinfo})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
        error_saving(request,e)

def showfindvalelement(request):
    try: 
        #new
        third_party_api_url = getAPIURL()+'FindingsValElementsAPI/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response finding val",response.content)

    
        return render(request, 'findings_val_elements_list.html',{ 'actPage':'Finding Val Elements','elements':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def newfindvalelement(request):
    try:   
        return render(request, 'addfindvalelement.html',{ 'actPage':'Add Finding Val Element'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())


def addfindvalelement(request):

    try:
        # third_party_api_url = getAPIURL()+'FindingsValElementsAPI/'

        updated_id = request.POST.get('update_id','False')
        element = request.POST.get('element', 'False') 
        description = request.POST.get('desc','False')
        activestatus = request.POST.get('activestatus','False')

        print("request------------------------",updated_id)
        if updated_id != 'undefined':
            third_party_api_url = getAPIURL()+'FindingsValElementsAPI/'
            print("third_party_api_url",third_party_api_url)
            data_to_update = {
                'element_text':element,
                'element_description':description,
                'activestatus':activestatus,
                'id':updated_id
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.put(third_party_api_url, data= json.dumps(data_to_update),headers=header)
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
        else:
            print("request data department",request.POST)
            third_party_api_url = getAPIURL()+'FindingsValElementsAPI/'
            data_to_save = {
                'element_text':element,
                'element_description':description,
                'activestatus':activestatus,
                'addedby':request.session['uid']
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
            print("----------------5",json.loads(response.content))
            print("response content findong",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def showfindcategory(request):
    try: 
        #new
        third_party_api_url = getAPIURL()+'FindingsCategoryAPI/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response finding category",response.content)

    
        return render(request, 'findings_category_list.html',{ 'actPage':'Finding Category','category':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def newfindcategory(request):
    try:   
        return render(request, 'addfindingcategory.html',{ 'actPage':'Add Finding Val Element'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())


def addfindcategory(request):

    try:
        # third_party_api_url = getAPIURL()+'FindingsValElementsAPI/'

        updated_id = request.POST.get('update_id','False')
        category = request.POST.get('category', 'False') 
        description = request.POST.get('desc','False')
        activestatus = request.POST.get('activestatus','False')

        print("request------------------------",updated_id)
        if updated_id != 'undefined':
            third_party_api_url = getAPIURL()+'FindingsCategoryAPI/'
            print("third_party_api_url",third_party_api_url)
            data_to_update = {
                'category_text':category,
                'category_description':description,
                'activestatus':activestatus,
                'id':updated_id
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.put(third_party_api_url, data= json.dumps(data_to_update),headers=header)
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
        else:
            print("request data department",request.POST)
            third_party_api_url = getAPIURL()+'FindingsCategoryAPI/'
            data_to_save = {
                'category_text':category,
                'category_description':description,
                'activestatus':activestatus,
                'addedby':request.session['uid']
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
            print("----------------5",json.loads(response.content))
            print("response content findong",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def edit_findvalelement(request,id): 
    try:
        # finddval_obj=Department.objects.get(dept_aid=id) 
        third_party_api_url = getAPIURL()+'FindingsValElementsAPI/'+str(id)
        header = {
        "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response--------------------------qwer",json.loads(response.content))  
        find_val_obj = json.loads(response.content)
        label=find_val_obj['data']['element_text']
        desc=find_val_obj['data']['element_description']
        activestatus=find_val_obj['data']['activestatus']
        print("activestatus",activestatus)
        return render(request, 'addfindvalelement.html',{ 'actPage':'Edit Findings Val Element','label':label,'desc':desc,'activestatus':activestatus,'id':id})

    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())



def edit_findcategory(request,id): 
    try:
        # finddval_obj=Department.objects.get(dept_aid=id) 
        third_party_api_url = getAPIURL()+'FindingsCategoryAPI/'+str(id)
        header = {
        "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response--------------------------asd",json.loads(response.content))  
        find_val_obj = json.loads(response.content)
        label=find_val_obj['data']['category_text']
        desc=find_val_obj['data']['category_description']
        activestatus=find_val_obj['data']['activestatus']
        print("activestatus",activestatus)
        return render(request, 'addfindingcategory.html',{ 'actPage':'Edit Findings Category','label':label,'desc':desc,'activestatus':activestatus,'id':id})

    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())

def GetModelIdFindVal(request):
    api_url=getAPIURL()+"GetModelIdFindVal/"       
    data_to_get={ 
        'uid':request.session['uid']
    } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(data_to_get),headers=header)
    print("response----------------------",response.content)
    return JsonResponse(json.loads(response.content))


def showfindvalsubelement(request):
    try: 
        #new
        third_party_api_url = getAPIURL()+'FindingsValSubElementsAPI/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response finding val sub element",response.content)

        return render(request, 'findings_val_sub_elements_list.html',{ 'actPage':'Finding Val Sub Elements','elements':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def newfindvalsubelement(request):
    try:   
        third_party_api_url = getAPIURL()+'FindingsValElementsAPI/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response finding val element",response.content)

        return render(request, 'addfindvalsubelement.html',{ 'actPage':'Add Finding Val Sub Element','elements':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())


def addfindvalsubelement(request):

    try:
        # third_party_api_url = getAPIURL()+'FindingsValElementsAPI/'

        updated_id = request.POST.get('update_id','False')
        element = request.POST.get('element', 'False') 
        sub_element = request.POST.get('sub_element', 'False')
        description = request.POST.get('desc','False')
        activestatus = request.POST.get('activestatus','False')

        print("request------------------------",updated_id,element,sub_element)
        

        if updated_id != 'undefined':

            third_party_api_url = getAPIURL()+'Elements/'
            data_to_get = {
                'element':element
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response_element = requests.get(third_party_api_url, data= json.dumps(data_to_get), headers=header)
            print("request element------------------------",json.loads(response_element.content))
            element_details = json.loads(response_element.content)

            third_party_api_url = getAPIURL()+'FindingsValSubElementsAPI/'
            print("third_party_api_url",third_party_api_url)
            data_to_update = {
                'element_text':sub_element,
                'element_aid':element_details['data']['element_aid'],
                'element_description':description,
                'activestatus':activestatus,
                'id':updated_id
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.put(third_party_api_url, data= json.dumps(data_to_update),headers=header)
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
        else:
            print("request data sub element",request.POST)
            third_party_api_url = getAPIURL()+'FindingsValSubElementsAPI/'
            data_to_save = {
                'element_text':sub_element,
                'element_aid':element,
                'element_description':description,
                'activestatus':activestatus,
                'addedby':request.session['uid']
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
            print("----------------5",json.loads(response.content))
            print("response content findong",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def edit_findvalsubelement(request,id): 
    try:
        third_party_api_url = getAPIURL()+'FindingsValSubElementsAPI/'+str(id)
        header = {
        "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response------------------------val sub element",json.loads(response.content))  
        find_val_obj = json.loads(response.content)
        print("find_val_obj",find_val_obj)
        element = find_val_obj['data']['element_details']['element_text']
        label=find_val_obj['data']['element_text']
        desc=find_val_obj['data']['element_description']
        activestatus=find_val_obj['data']['activestatus']
        element_details = find_val_obj['data']['element_details']
        print("activestatus",activestatus)
        return render(request, 'addfindvalsubelement.html',{ 'actPage':'Edit Findings Val Element','element':element,'label':label,'desc':desc,'activestatus':activestatus,'id':id,'element_details':element_details})

    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())


def CriteriaQuestionList(request):
    try: 
        #new
        third_party_api_url = getAPIURL()+'QuestionSectionAPI/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response question section",response.content)

        return render(request, 'Criteria_Section_list.html',{ 'actPage':'Question Section','section':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e)
#         print('adduser traceback is ', traceback.print_exc())
        
def newCriteriaQuestion(request):
    try:   
        third_party_api_url = getAPIURL()+'SectionApI/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response section",response.content)

        return render(request, 'addcriteriaQuestionsec.html',{ 'actPage':'Add Criteria Section','sections':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def addQuestionSection(request):

    try:
        # third_party_api_url = getAPIURL()+'FindingsValElementsAPI/'

        updated_id = request.POST.get('update_id','False')
        section = request.POST.get('section', 'False') 
        question = request.POST.get('question', 'False')
        

        print("request------------------------",updated_id,section,question)
        

        if updated_id != 'undefined':

            third_party_api_url = getAPIURL()+'Sections/'
            data_to_get = {
                'section':section
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response_element = requests.get(third_party_api_url, data= json.dumps(data_to_get), headers=header)
            print("request element------------------------",json.loads(response_element.content))
            section_details = json.loads(response_element.content)

            third_party_api_url = getAPIURL()+'QuestionSectionAPI/'
            print("third_party_api_url",third_party_api_url)
            data_to_update = {
                'question_label':question,
                'section_aid':section_details['data']['section_aid'],
                'id':updated_id
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.put(third_party_api_url, data= json.dumps(data_to_update),headers=header)
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
        else:
            print("request data create question",request.POST)
            third_party_api_url = getAPIURL()+'QuestionSectionAPI/'
            data_to_save = {
                'question_label':question,
                'section_aid':section,
                'addedby':request.session['uid']
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
            print("----------------5",json.loads(response.content))
            print("response content save",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def edit_QuestionSection(request,id): 
    try:
        third_party_api_url = getAPIURL()+'QuestionSectionAPI/'+str(id)
        header = {
        "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response------------------------val questions",json.loads(response.content))  
        question_obj = json.loads(response.content)
        print("find_val_obj",question_obj)
        section = question_obj['data']['section_details']['section_aid']
        question=question_obj['data']['question_label']
        section_details = question_obj['data']['section_details']
        
        return render(request, 'addcriteriaQuestionsec.html',{ 'actPage':'Edit Quuestion and Section','section':section,'question':question,'id':id,'section_details':section_details})

    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())

def showIssueTypesAssesment(request):
    try: 
        third_party_api_url = getAPIURL()+'ValidationRatingsAPI/'
        
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url,headers=header)

        return render(request, 'IssueTypesAssesmentList.html',{ 'actPage':'Issue Type Assesment','Risk_Findings':'Risk Findings','data':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def SaveValidationRatings(request):
    try:

        validation_ratings_type = request.GET.get('validation_ratings', 'False') 
        severity = request.GET.get('severity','False')
        risk_type = request.GET.get('ratings','False')
        operator = request.GET.get('operator','False')
        value = request.GET.get('value','False')

        third_party_api_url = getAPIURL()+'ValidationRatingsTempAPI/'
        data_to_save = {
            'validation_rating':validation_ratings_type,
            'severity':severity,
            'risk_type':risk_type,
            'operator':operator,
            'value':value,
            'addedby':request.session['uid']
        }
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)

        return JsonResponse(json.loads(response.content))
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def ValidationRatingsdata(request):
    try:
        third_party_api_url = getAPIURL()+'ValidationRatingsAPI/'

        data_to_save = {
            'addedby':request.session['uid']
        }
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
        
        return JsonResponse(json.loads(response.content))
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_sub_valData(request):
    print("get_sub_valData",request.GET.get('validation_element_id'))

    api_url=getAPIURL()+"get_sub_valID/"       
    data_to_get={ 
        'val_id':request.GET.get('validation_element_id')
        } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(data_to_get),headers=header)

    return JsonResponse(json.loads(response.content),safe=False)

# def valFindings(request):
#     print("valFindings")
#     try:
       
#         request_id=request.session['vt_mdl'] #find_max_req_id()
    
#         api_url=getAPIURL()+"valFindings/"       
#         data_to_save={ 
#             'request_id':request_id
#             } 
#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }
#         response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
#         data=response.json()
        
#         print("Respo data",data)
#         data = {'List': data['List'], 'today': data['today'], 'emailLst': data['emailLst'],'ValCatLst':data['ValCatLst'],'ValCatElm':data['ValCatElm']}
#         return render(request, 'valFindings.html', data)
#     except Exception as e:
#         print(e)
#         return render(request, 'error.html')

def valFindings(request):
    print("valFindings")
    try:
       
        request_id=request.session['vt_mdl'] #find_max_req_id()
    
        api_url=getAPIURL()+"valFindings/"       
        data_to_save={ 
            'request_id':request_id
            } 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
        data=response.json()
         

        third_party_api_url = getAPIURL()+'getValFindingsMRM/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'uid':request.session['uid'],
            'dept_aid':request.session['dept']
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        data_a=json.loads(responseget.content)
        data = {'List': data['List'], 'today': data['today'], 'emailLst': data['emailLst'],'ValCatLst':data['ValCatLst'],'ValCatElm':data['ValCatElm'],'mdlid':data_a['mdlids']}
        return render(request, 'valFindings.html', data)
    except Exception as e:
        print(e, traceback.print_exc())
        return render(request, 'error.html')


def savevalFindings(request):
    # mdl_id=request.GET['mdl_id']
    validation_element=request.GET['validation_element']
    sub_validation_element=request.GET['sub_validation_element']
    ValCat=request.GET['ValCat']
    Risk = request.GET['Risk_Level']
    Level = request.GET['Lvl'] 
    Desc = request.GET['Desc']
    validation_element_text = request.GET['validation_element_text']
    
    # Assessment = request.GET['Assessment']
    # findingsId = request.GET['findingsId']
    

    # request_id=request.session['vt_mdl']
    request_id = request.GET['mdl_id']
    
    api_url=getAPIURL()+"save_valFindings/"       
    data_to_save={ 
        'request_id':request_id,
        'validation_element':validation_element,
        'sub_validation_element':sub_validation_element,
        'ValCat':ValCat,
        'Desc':Desc,
        'Risk':Risk,
        'Level':Level,
        'validation_element_text':validation_element_text,
        'Added_by':request.session['uid']
        } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
    data=response.json()
    
    print("Respo data",data)
    
    return JsonResponse(data)



def validation_findings(request):
    print("valFindings")
    try:
        api_url=getAPIURL()+"GetModelIdFindVal/"       
        data_to_get={ 
            'uid':request.session['uid']
        } 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_get),headers=header)
        print("response----------------------",response.content)

        mdl_ids = json.loads(response.content)
        # mdl_ids=response.content
        print("type res",type(mdl_ids))

       
        api_url=getAPIURL()+"valFindings/"       
        
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data={},headers=header)
        data=response.json()
        
        print("Respo data",data)
        data = {'List': data['List'], 'today': data['today'], 'emailLst': data['emailLst'],'mdl_ids':mdl_ids,'ValCatLst':data['ValCatLst'],'ValCatElm':data['ValCatElm']}
        return render(request, 'validation_findings.html', data)
    except Exception as e:
        print(e.__traceback__)
        return render(request, 'error.html')

import os
from django.conf import settings
from django.template.loader import render_to_string
# from xhtml2pdf import pisa



def getfindings_Data(find_id, mdl_id):
    print("request_data------------------", find_id, mdl_id)

    find_valobj = ValidationFindings.objects.get(mdl_id=mdl_id, findings_id=find_id)

    print("desc", find_valobj.finding_description)
    validation_element = []
    validation_category = []

    val_find_obj = ValidationFindings.objects.filter(mdl_id=mdl_id, findings_id=find_id)
    for i in val_find_obj:
        validation_element.append(i.validation_element)
        validation_category.append(i.category)

    # ✅ Return plain dictionary, not DRF Response
    return {
        'validation_element': validation_element,
        'category': find_valobj.category,
        'risk': find_valobj.risk,
        'risk_level': find_valobj.risk_level,
        'finding_description': find_valobj.finding_description,
        'response': find_valobj.response,
        'validation_category': validation_category,
        'find_id': find_id,
        'mdl_id': mdl_id,
        'date': datetime.now().strftime("%d-%m-%Y"),
    }

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from reportlab.pdfgen import canvas
from io import BytesIO
import json
import os
from django.http import JsonResponse
from datetime import datetime   

# def generate_findings_pdf(request):
#     print("generate_findings_pdf")
#     if request.method == 'POST':
#         find_id = request.POST.get('find_ID')
#         mdl_id = request.POST.get('mdlid')

#         print("find_id", find_id)
#         print("mdl_id", mdl_id)

#         # ✅ Get dictionary, not Response object
#         findings_data = getfindings_Data(find_id, mdl_id)

#         print("findings_data", findings_data)

#         # ✅ Correct context assignment
#         context = findings_data

#         # ✅ Render HTML template with context
#         html = render_to_string("validation_findings.html", context)

#         # ✅ Save to PDF
#         output_dir = os.path.join(settings.BASE_DIR, 'static', 'findings_PDF')
#         os.makedirs(output_dir, exist_ok=True)
#         filename = f'Finding_{find_id}.pdf'
#         output_path = os.path.join(output_dir, filename)

#         with open(output_path, "wb") as pdf_file:
#             pisa_status = pisa.CreatePDF(html, dest=pdf_file)

#         if pisa_status.err:
#             return HttpResponse("PDF generation failed", status=500)

#         return HttpResponse(f"/static/findings_PDF/{filename}")

#     return HttpResponse(status=405)

# from django.http import HttpResponse
# from reportlab.pdfgen import canvas
# from io import BytesIO
# import json

# @csrf_exempt
# def generate_findings_pdf(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         buffer = BytesIO()
#         p = canvas.Canvas(buffer)

#         # Example content
#         p.drawString(100, 800, f"Finding Description: {data['finding_description']}")
#         p.drawString(100, 780, f"Response: {data['response']}")
#         p.drawString(100, 760, f"Severity: {data['risk']}")
#         p.drawString(100, 740, f"Risk Level: {data['risk_level']}")

#         # Add more content as needed...

#         p.showPage()
#         p.save()

#         buffer.seek(0)
#         return HttpResponse(buffer, content_type='application/pdf')

#     return HttpResponse(status=405)



# def generate_findings_pdf(request):
#     print("generate_findings_pdf")
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         print("data",data)
#         # Define output directory
#         output_dir = os.path.join(settings.BASE_DIR, 'static', 'val_findings_PDF')
#         os.makedirs(output_dir, exist_ok=True)

#         # Create a unique filename using timestamp or findings ID
#         findings_id = data.get('findings_id', 'unknown')
#         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#         filename = f"findings_{findings_id}_{timestamp}.pdf"
#         file_path = os.path.join(output_dir, filename)

#         # Generate PDF
#         p = canvas.Canvas(file_path)
#         p.drawString(100, 800, f"Finding Description: {data.get('finding_description', '')}")
#         p.drawString(100, 780, f"Response: {data.get('response', '')}")
#         p.drawString(100, 760, f"Severity: {data.get('risk', '')}")
#         p.drawString(100, 740, f"Risk Level: {data.get('risk_level', '')}")
#         p.showPage()
#         p.save()

#         # Return success and path to client (optional)
#         return JsonResponse({
#             "status": "success",
#             "file_path": f"/static/val_findings_PDF/{filename}"
#         })

#     return JsonResponse({"status": "error", "message": "Invalid request"}, status=405)

# import os
# from django.http import JsonResponse
# from django.conf import settings
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
# from datetime import datetime

# def generate_findings_pdf(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         print("data",data)
#         # data = request.POST  # or json.loads(request.body) for JSON
#         # print("generate_findings_pdf",data)
#         # Create PDF directory if it doesn't exist
#         output_dir = os.path.join(settings.BASE_DIR, 'static', 'val_findings_PDF')
#         os.makedirs(output_dir, exist_ok=True)

#         # Generate filename
#         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#         filename = f'finding_{timestamp}.pdf'
#         filepath = os.path.join(output_dir, filename)

#         # Start PDF
#         c = canvas.Canvas(filepath, pagesize=A4)
#         width, height = A4

#         x_label = 50
#         x_value = 200
#         y = height - 50
#         line_height = 25

#         def draw_row(label, value):
#             nonlocal y
#             # Convert lists to string if needed
#             if isinstance(value, list):
#                 value = ', '.join(str(v) for v in value)
#             elif isinstance(value, dict):
#                 value = str(value)
#             c.setFont("Helvetica-Bold", 10)
#             c.drawString(x_label, y, f"{label}:")
#             c.setFont("Helvetica", 10)
#             c.drawString(x_value, y, value if value else "")
#             y -= line_height

#         # Draw form fields
#         draw_row("Date", data.get("date", ""))
#         draw_row("Model", data.get("model", ""))
#         draw_row("Findings ID", data.get("findings_id", ""))
#         draw_row("Validation Elements", data.get("validation_element", ""))
#         draw_row("Validation Category", data.get("validation_category", ""))
#         draw_row("Severity", data.get("severity", ""))
#         draw_row("Level", data.get("level", ""))
#         draw_row("Description", data.get("finding_description", ""))
#         draw_row("Response", data.get("response", ""))

#         c.save()

#         return JsonResponse({
#             "status": "success",
#             "message": "PDF generated successfully.",
#             "file_path": f"/static/val_findings_PDF/{filename}"
#         })

#     return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


# import os
# import json
# from datetime import datetime
# from django.conf import settings
# from django.http import JsonResponse
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.platypus import (
#     SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
# )


# def generate_findings_pdf(request):
#     if request.method == "POST":
#         # data = json.loads(request.body)
#         # print("dataa", data)
#         data = {
#             "Date": "07/31/2025",
#             "Model": "M070100",
#             "Findings ID": "CS1",
#             "Validation Elements": "Conceptual and Developmental Soundness",
#             "Validation Category": "Control Environment",
#             "Severity": "Low",
#             "Level": "1",
#             "Description": "testing validation findings",
#             "Response": "testttt response",
#         }
#         # Create PDF output directory
#         output_dir = os.path.join(settings.BASE_DIR, 'static', 'val_findings_PDF')
#         os.makedirs(output_dir, exist_ok=True)

#         # Filename
#         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#         filename = f'Validation_Findings_{timestamp}.pdf'
#         file_path = os.path.join(output_dir, filename)

#         # PDF document setup
#         doc = SimpleDocTemplate(
#             file_path,
#             pagesize=A4,
#             rightMargin=40, leftMargin=40,
#             topMargin=40, bottomMargin=40
#         )
#         elements = []
#         styles = getSampleStyleSheet()

#         # Table with form data
#         table_data = [
#             [Paragraph("<b>Date</b>", styles['Normal']), data.get("Date", "")],
#             [Paragraph("<b>Model</b>", styles['Normal']), data.get("Model", "")],
#             [Paragraph("<b>Findings ID</b>", styles['Normal']), data.get("Findings ID", "")],
#             [Paragraph("<b>Validation Elements</b>", styles['Normal']), data.get("Validation Elements", "")],
#             [Paragraph("<b>Validation Category</b>", styles['Normal']), data.get("Validation Category", "")],
#             [Paragraph("<b>Severity</b>", styles['Normal']), data.get("Severity", "")],
#             [Paragraph("<b>Level</b>", styles['Normal']), data.get("Level", "")],
#             [Paragraph("<b>Description</b>", styles['Normal']),
#              Paragraph(data.get("Description", "").replace('\n', '<br/>'), styles['Normal'])],
#             [Paragraph("<b>Response</b>", styles['Normal']),
#              Paragraph(data.get("Response", "").replace('\n', '<br/>'), styles['Normal'])],
#         ]

#         table = Table(table_data, colWidths=[150, 350])
#         table.setStyle(TableStyle([
#             ('GRID', (0, 0), (-1, -1), 0.75, colors.grey),
#             ('BOX', (0, 0), (-1, -1), 1, colors.black),
#             ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#             ('ALIGN', (0, 0), (0, -1), 'LEFT'),
#             ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
#             ('FONTSIZE', (0, 0), (-1, -1), 10),
#             ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
#             ('BOTTOMPADDING', (0, 7), (-1, 8), 20),  # Extra padding for description and response
#         ]))

#         elements.append(table)
#         elements.append(Spacer(1, 12))
#         doc.build(elements)

#         return JsonResponse({
#             "status": "success",
#             "message": "PDF generated successfully.",
#             "file_path": f"/static/val_findings_PDF/{filename}"
#         })

#     return JsonResponse({'error': 'Only POST allowed'}, status=400)

import os
import json
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
)

from reportlab.platypus import PageBreak

def generate_findings_pdf(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("PDF data list received:", data)

        output_dir = os.path.join(settings.BASE_DIR, 'static', 'val_findings_PDF')
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'Validation_Findings_{timestamp}.pdf'
        file_path = os.path.join(output_dir, filename)

        doc = SimpleDocTemplate(
            file_path,
            pagesize=A4,
            rightMargin=40, leftMargin=40,
            topMargin=40, bottomMargin=40
        )

        elements = []
        styles = getSampleStyleSheet()

        # Header for each page (Finding-specific)
        heading_style = ParagraphStyle(
            name='FindingHeading',
            fontSize=14,
            leading=18,
            alignment=1,  # Center
            spaceAfter=14,
            fontName='Helvetica-Bold'
        )

        table_style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.75, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 7), (-1, 8), 20),
        ])

        for idx, record in enumerate(data):
            # Heading per finding
            findings_id = record.get("Findings ID", "Unknown")
            heading_text = f"Validation Finding for {findings_id}"
            elements.append(Paragraph(heading_text, heading_style))
            elements.append(Spacer(1, 12))

            # Table data
            table_data = [
                [Paragraph("<b>Date</b>", styles['Normal']), record.get("Date", "")],
                [Paragraph("<b>Model</b>", styles['Normal']), record.get("Model", "")],
                [Paragraph("<b>Findings ID</b>", styles['Normal']), findings_id],
                [Paragraph("<b>Validation Elements</b>", styles['Normal']), record.get("Validation Elements", "")],
                [Paragraph("<b>Validation Category</b>", styles['Normal']), record.get("Validation Category", "").strip()],
                [Paragraph("<b>Severity</b>", styles['Normal']), record.get("Severity", "")],
                [Paragraph("<b>Level</b>", styles['Normal']), record.get("Level", "")],
                [Paragraph("<b>Description</b>", styles['Normal']),
                 Paragraph(record.get("Description", "").replace('\n', '<br/>'), styles['Normal'])],
                [Paragraph("<b>Response</b>", styles['Normal']),
                 Paragraph(record.get("Response", "").replace('\n', '<br/>'), styles['Normal'])],
            ]

            table = Table(table_data, colWidths=[150, 350])
            table.setStyle(table_style)

            elements.append(table)

            # Add a page break after each finding except the last one
            if idx != len(data) - 1:
                elements.append(PageBreak())

        doc.build(elements)

        return JsonResponse({
            "status": "success",
            "message": "PDF generated successfully.",
            "file_path": f"/static/val_findings_PDF/{filename}"
        })

    return JsonResponse({'error': 'Only POST allowed'}, status=400)

def getfindingsID(request):
    print("getfindingsID",request.GET.get('mdlid'))            

    api_url=getAPIURL()+"getfindings_ID/"       
    data_to_get={ 
        'mdlid':request.GET.get('mdlid')

    } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(data_to_get),headers=header)
    print("response----------------------",response.content)
    return JsonResponse(json.loads(response.content),safe=False)

def savevalFindingsComment(request):
    file_name = request.session['uid']
    comment = request.GET.get('comment', 'False')
    validationFindings = file_path + str(file_name) + "_validationFindings.csv"
    if os.path.exists(validationFindings) and comment != "False":
        df_old = pd.read_csv(validationFindings)
        df_old.at[0, "Comment"] = comment
        df_old.to_csv(validationFindings, index=False)
        del df_old
    return JsonResponse({'is_taken': True})

def getfindingsData(request):
    print("getfindingsID")    
    # mdlid= request.GET.get('mdlid')       
    # find_id=request.GET.get('find_ID')
    # print("mdlid mdlid",mdlid,find_id)
    
    api_url=getAPIURL()+"getfindings_Data/"       
    data_to_get={ 
        'mdlid':request.GET.get('mdlid'),
        'find_id':request.GET.get('find_ID')

    } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(data_to_get),headers=header)
    print("response----------------------",response.content)
    return JsonResponse(json.loads(response.content),safe=False)

    
def update_response(request):
    print("update_response")    
    # mdlid= request.GET.get('mdlid')       
    # find_id=request.GET.get('find_ID')
    # response=request.GET.get('response')
    # print("mdlid mdlid",mdlid,find_id,response)

    api_url=getAPIURL()+"update_response_findings/"       
    data_to_post={ 
        'mdlid':request.GET.get('mdlid'),
        'find_id':request.GET.get('find_ID'),
        'response':request.GET.get('response')

    } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.post(api_url, data= json.dumps(data_to_post),headers=header)
    print("response----------------------",response.content)
    return JsonResponse(json.loads(response.content),safe=False)



def task_approver_data(request):
    
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
    # task_approval_master=TaskApprovalstatusMaster.objects.all()
    # task_relevant_obj=Task_Relevant_Personnel.objects.filter(u_id=U_id,u_type="Approver")
    context={"task_relevant_obj":api_data['task_relevant_obj'],'task_approval_master':api_data['task_approval_master'],'taskid':taskid}
    return render(request,'task_approver_data.html',context)


def issue_approver_data(request): 
    issueid =request.GET.get('id', 'False') 
    api_url=getAPIURL()+"issue_approver/"       
    api_para={  
        'uid':request.session['uid'], 
        'id':issueid} 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
    api_data=response.json()
    print("api_data",api_data)
    context={"issue_relevant_obj":api_data['issue_relevant_obj'],'issueid':api_data['issueid']}
    return render(request,'issue_approver_data.html',context)


def getHistoricalData(request):
    mdl_id=request.GET.get('mdl_id', 'False') 
    mm_type=request.GET.get('mm_type', 'False') 
    api_url = getAPIURL()+'PrdnHistoryData/'
    data_to_save={         
        'mdl_id':mdl_id,
        'mm_type':mm_type} 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)         
    api_data=response.json() 
    prdnData=api_data['prdnData']
    print('prdnData ',prdnData)
    return JsonResponse({'data':prdnData},safe=False)

def getReportTtlHdr(request):
    api_url = getAPIURL()+'getReportTtlHdr/'
    data_to_save={} 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)         
    api_data=response.json() 
    ttlnheadrs=api_data['ttlnheadrs']
    print('ttlnheadrs ',ttlnheadrs)
    return JsonResponse({'ttlnheadrs':ttlnheadrs},safe=False)


from django.db.models import Max
import math
def model_report(request):

   
    report_title_obj=ReportTitleTemplate.objects.filter(added_by=request.session['uid']).values_list('template_name', flat=True).distinct()
    print("report_title_obj",report_title_obj)
    # for i in report_title_obj:
    #     template_name=i.template_name
    #     print("template_name",template_name)
    # max_value = ReportTitleTemplate.objects.aggregate(max_value=Max('title_id'))['max_value']

    # max_value = 0 if max_value is None or (isinstance(max_value, float) and math.isnan(max_value)) else max_value 
    # max_value= int(max_value) + 1
    # print("max_value",max_value)
    return render(request, 'addReportTtlnHdrs.html',{'report_title_obj':report_title_obj})

from urllib.parse import parse_qs

def save_report_header_Title(request):  
    
    # report_heading = request.GET.get('report_heading') 

    api_url=getAPIURL()+"save_model_report/"       
    data_to_post={ 
        'title_id':request.GET['title_id'],
        'title_or_heading':request.GET['title_or_heading'], 
        'title_label':request.GET['title_label'],
        'title_type':request.GET['title_type'] ,
        'title_placeholder':request.GET['title_placeholder'],
        'title_sort_idx':request.GET['title_sort_idx'] ,
        'tamplate_name':request.GET['tamplate_name'],
        'fontsize':request.GET.get('fontsize','10'),
        'alignment':request.GET.get('alignment','center'),
        'page_no':request.GET['page_no'] ,
        'added_by':request.session['uid']
    } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+ request.session['accessToken']
    }
    response = requests.post(api_url, data= json.dumps(data_to_post),headers=header)
    print("response----------------------",response.content)
    return JsonResponse(json.loads(response.content),safe=False)


def updateTitleHeaderIdx(request):  
    
    # report_heading = request.GET.get('report_heading') 

    api_url=getAPIURL()+"updateTempHeaderIdx/"       
    data_to_post={ 
        'title_id':request.GET['title_id'], 
        'title_sort_idx':request.GET['title_sort_idx'] , 
        'page_no':request.GET['page_no'] ,
        'added_by':request.session['uid']
    } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+ request.session['accessToken']
    }
    response = requests.post(api_url, data= json.dumps(data_to_post),headers=header)
    print("response----------------------",response.content)
    return JsonResponse(json.loads(response.content),safe=False)

def deleteTempHeaderIdx(request):      
    # report_heading = request.GET.get('report_heading') 
    api_url=getAPIURL()+"deleteTempHeaderIdx/"       
    data_to_post={ 
        'title_id':request.GET['title_id'],  
        'page_no':request.GET['page_no'] ,
        'added_by':request.session['uid']
    } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+ request.session['accessToken']
    }
    response = requests.post(api_url, data= json.dumps(data_to_post),headers=header)
    print("response----------------------",response.content)
    return JsonResponse(json.loads(response.content),safe=False)

def insertFromTemp(request):      
    # report_heading = request.GET.get('report_heading') 
    api_url=getAPIURL()+"insertFromTemp/"       
    data_to_post={ 
        'template_name':request.GET['template_name'],   
    } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+ request.session['accessToken']
    }
    response = requests.post(api_url, data= json.dumps(data_to_post),headers=header)
    print("response----------------------",response.content)
    return JsonResponse(json.loads(response.content),safe=False)

def fetch_report(request):

    template_name=request.GET.get('selectedValue')
    
    print("template name",template_name)

    api_url=getAPIURL()+"fetch_model_report/"       
    data_to_get={ 
        'tamplate_name':template_name,
        'Added_by':request.session['uid']
    } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+ request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(data_to_get),headers=header)
    print("response----------------------",response.content)

    title_data=json.loads(response.content)

    return JsonResponse(title_data,safe=False)


def Get_Title_Label(request):
    try:
        # Title_Label
        header_name = request.GET.get('header_name','False')
        template_name = request.GET.get('template_name','False') 
        print("Template name",template_name)
        third_party_api_url = getAPIURL()+'Get_Title_Label/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }    
        data_to_get = {
            'header_name':header_name,
        }
        responseget_titlelbl = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        print("responseget_titlelabel ",json.loads(responseget_titlelbl.content))
        
        return JsonResponse({'data':json.loads(responseget_titlelbl.content)})
    except Exception as e:
        print("error is",e)



def save_desc_comments(request):
    plot_dir='/static/media/'
    plot_dir_view='static/media/'
    user_name="Dir_"+str(request.session['uid'])

    utility=request.GET.get('utility')
    comment=request.GET.get('comment')
    mdl_id=request.GET.get('mdl_id','') 
    sub_utility=request.GET.get('tableType','')
    type_comm=request.GET.get('type')
    destination=request.GET.get('destination','') 
    data_parameter=request.GET.get('data_parameter','') 
    section=request.GET.get('vt_section','none') 
    print('section ',section ,' mdl_id ',mdl_id,' utility ',utility)
    # chartImg = request.GET['chartImg']
    if type_comm == "chart":
        chartType =sub_utility
        xaxis= str(data_parameter.split('|')[0]).strip()
        yaxis=  str(data_parameter.split('|')[1]).strip()
        chartImg=mdl_id+'_'+chartType+'_'+xaxis+'_'+yaxis+'_'+date.today().strftime("%m.%d.%Y") +'.png'  
        destination = plot_dir_view+user_name+'_Chartimgs/'+chartImg 

    api_url=getAPIURL()+"save_desc_comments/"       
    data_to_post={ 
        'utility':utility,
        'sub_utility':sub_utility,
        'comment':comment,
        'Added_by':request.session['uid'],
        'mdl_id':mdl_id,
        'type_comm':type_comm,
        'data_parameter':data_parameter,
        'destination':destination,
        'section':section
    } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+ request.session['accessToken']
    }
    response = requests.post(api_url, data= json.dumps(data_to_post),headers=header)
     

    title_data=json.loads(response.content)

    return JsonResponse(title_data,safe=False)


def validation_comments(request):
    print("req",request.GET)
    api_url=getAPIURL()+"validation_comments/"       
    data_to_save={ 
        'uid':request.session['uid']} 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
        
    api_data=response.json() 

    print("api_data",api_data)

    return render(request, 'validation_comments.html',{'mdl_id':api_data})


def get_val_comments_data(request):
    try:     
        mdl_id = request.GET.get('mdl_id','none')
        section=request.GET.get('section','')
        api_url=getAPIURL()+"get_val_comments_data/"       
        data_to_save={ 
            'mdl_id':mdl_id,
            'section':section,
            'valcomms':[]} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        api_data = json.dumps(api_data).replace('null', '""')
        api_data=json.loads(api_data) 
        print("api_data",api_data)
        return JsonResponse(api_data,safe=False)
    except Exception as e:
        print('uploaddecomm is ',e)
        print('uploaddecomm traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"}) 

def getTableData(request):
    try:
        tableType = request.GET['tableType']
        tableName = request.GET['tableName']
        data_parameter=request.GET.get('data_parameter','')
        file_id=find_max_file_id(request.GET['mdl_id'])
        dataset=''
        print('tableType is ', tableType)
        data = {'is_taken': False}
        if(tableType == "DataTypenCnt"):
            data = {'is_taken': True, 'tblCode': getDatatypenCnt(file_id,dataset)}
        elif (tableType == "DataDesc"):
            data = {'is_taken': True, 'tblCode': viewNumData2(file_id,dataset,tableType)}
        elif (tableType == "DataMean"):
            data = {'is_taken': True, 'tblCode': viewNumData2(file_id,dataset,tableType)}
        elif (tableType == "DataMedian"):
            data = {'is_taken': True, 'tblCode': viewNumData2(file_id,dataset,tableType)}
        elif(tableType == "NumVarDIst"):
            data = {'is_taken': True,
                    'tblCode': dist_numevari_catvar2(file_id,dataset,data_parameter)}
        # elif(tableType == "VIFData"):
        #     data = {'is_taken': True,
        #             'tblCode': getVIFData()}
        # elif(tableType == "TarvsCat"):
        #     data = {'is_taken': True,
        #             'tblCode': getCT(tableName)}
        # elif(tableType == "ValFindings"):
        #     data = {'is_taken': True,
        #             'tblCode': getValFindingsttbl()}
        return JsonResponse(data)
    except Exception as e:
        print(e)
        print("error is ", traceback.print_exc())
        data = {'is_taken': False}
        return JsonResponse(data)

def getDatatypenCnt(file_id,dataset):
    try:
        
        df=find_src_data(file_id,dataset) 
        gridDttypes = []
        tableSting = '''<div class="appTblsss" id="Data types and cnt"><table width="100%" style="border: 1px solid #eee;border-collapse: collapse;">
                        <thead> <tr>  <th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="40%">Column Name</th>
                                <th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="30%">Not-Null Count</th>
                                <th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="30%">Column Data type &nbsp;&nbsp;&nbsp;&nbsp;</th>
                            </tr> </thead> <tbody>'''
        result = dict(df.dtypes)
        for key, value in result.items():
            # gridDttypes.append(
            #     {'colName': key, 'dataType': value, 'notnull': df[key].count()})
            tableSting += '<tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">' + key + '</td>'
            tableSting += '<td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">' + \
                str(df[key].count())+' non-null </td>'
            tableSting += '<td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">' + \
                str(value)+'</td></tr>'
        tableSting += '</tbody></table>  </div><div class="Data types and cntEnd">&nbsp;</div>'
        del df
        return tableSting
    except Exception as e:
        print(e)


def viewNumData2(file_id,dataset,strType):   
        
    df=find_src_data(file_id,dataset) 
    from statsmodels import robust    
    
    num_cols = [c for i, c in enumerate(
        df.columns) if df.dtypes[i] not in [np.object]]
    x_numeric = pd.DataFrame(df, columns=num_cols)
    arrdescData = ''
    if(strType == "DataDesc"):
        desc = df.describe()
        arrdescData = ''
        arrdescData = '''<div class="appTblsss" id="DataDesc"><table width="100%" border="1" style="border: 1px solid #eee;border-collapse: collapse;">
                            <thead>
                                <tr>
                                    <th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="20%">test</th>
                                    <th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="10%">count</th>
                                    <th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="10%">min</th>
                                    <th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="10%">max</th>
                                    <th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="10%">mean</th>
                                    <th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="10%">std</th>
                                    <th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="10%">25%</th>
                                    <th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="10%">50%</th>
                                    <th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="10%">75%</th>
                                </tr>
                            </thead>
                            <tbody>  '''

        for recs, vals in dict(desc).items():
            arrdescData += '''
                            <tr>
                                <td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">''' + recs+'''</td>
                                <td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">''' + str(vals['count'])+'''</td>
                                <td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">''' + str(vals['mean'])+'''</td>
                                <td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">''' + str(vals['std'])+'''</td>
                                <td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">''' + str(vals['25%'])+'''</td>
                                <td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">''' + str(vals['50%'])+'''</td>
                                <td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">''' + str(vals['75%'])+'''</td>
                                <td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">''' + str(vals['max'])+'''</td>
                                <td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">''' + str(vals['min'])+'''</td>
                            </tr> '''
        arrdescData += '''</tbody>
                        </table></div><div class="DataDescEnd">&nbsp;</div>'''
    elif(strType == "DataMean"):

        mean_ad = x_numeric.mad().round(decimals=3)
        # print('mean_ad is ', mean_ad)
        mean_adresult = mean_ad.to_json(orient='index')
        mean_adresult = json.loads(mean_adresult)
        print('len of json ', mean_adresult)

        arrdescData = '''<div class="appTblsss" id="DataMean"><table width="100%" border="1" style="border: 1px solid #eee;border-collapse: collapse;">
                            <thead>
                                <tr>
                                    <th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="60%">Column</th>
                                    <th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="40%">Value</th>
                                </tr>
                            </thead>
                            <tbody>  '''
        for key in mean_adresult:
            value = mean_adresult[key]
            arrdescData += '''
                        <tr>
                            <td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">''' + key+'''</td>
                            <td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">''' + str(value)+'''</td>'''
        arrdescData += '''</tbody>
                        </table></div><div class="DataMeanEnd">&nbsp;</div>'''
    elif(strType == "DataMedian"):
        median_ad = x_numeric.apply(robust.mad).round(decimals=3)
        # print(mean_ad)
        median_adresult = median_ad.to_json(orient='index')
        median_adresult = json.loads(median_adresult)
        arrdescData = ''' <div class="appTblsss" id="DataMedian"><table width="100%"  border="1" style="border: 1px solid #eee;border-collapse: collapse;">
                            <thead><tr><th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="60%">Column</th> <th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="40%">Value</th>
                            </tr> </thead><tbody>  '''
        for key in median_adresult:
            value = median_adresult[key]
            arrdescData += '''
                        <tr>
                            <td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">''' + key+'''</td> <td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">''' + str(value)+'''</td>'''
        arrdescData += '''</tbody>
                        </table></div><div class="DataMedianEnd">&nbsp;</div>'''
    return arrdescData

def dist_numevari_catvar2(file_id,dataset,data_parameter):   
        
    df=find_src_data(file_id,dataset) 
         
     
    
    print(df.columns,', ',data_parameter)
    cat_var =  str(data_parameter.split("|")[1]).strip() # cat_cols[i]
    num_var = str(data_parameter.split("|")[0]).strip() # num_cols[j]

    dist_num_cat = df.groupby(cat_var)[num_var].describe()
    result = dist_num_cat.to_json(orient='index')
    result = json.loads(result)
    print('colNames ', dist_num_cat.columns)
    arrdescData = ''' <div class="appTblsss" id="'''+cat_var+'_'+num_var + '''"><table width="100%"  border="1" style="border: 1px solid #eee;border-collapse: collapse;">
                        <thead>
                            <tr>
                            <th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="20%">&nbsp;&nbsp;&nbsp;&nbsp;</th> '''
    for col in dist_num_cat.columns:
        print('col is ', col)
        arrdescData += '''<th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="10%">''' + col+'''</th>'''

    arrdescData += '''    </tr>
    </thead>
    <tbody>  '''
    for key in result:
        value = result[key]
        arrdescData += '''
                    <tr>
                        <td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">''' + key+'''</td>'''
        for key2 in value:
            value2 = value[key2]
            arrdescData += ''' 
                        <td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">''' + str(value2)+'''</td>'''
        arrdescData += '''
                    </tr>'''
    arrdescData += '''</tbody>
                    </table></div><div class="'''+cat_var+'_'+num_var  + '''End">&nbsp;</div>'''
    return arrdescData



def insert_VT_Discussion_Comments(request):
    utility=request.POST.get('utility','')
    comment=request.POST.get('comment','')
    mdl_id=request.POST.get('mdl_id','') 
    sub_utility=request.POST.get('sub_utility','') 
    chat_data = request.POST.get('chat_data','')
    section=request.POST.get('vt_section','') 
    print('section ',section,' mdl_id ',mdl_id)
    fileInfo=''
    if request.method == 'POST':  
        # myfile = request.FILES['myfile'] 
        files = request.FILES
        myfile = files.get('filename', 'none')  
        if myfile!="none":  
            
            if(sub_utility !=' ' and sub_utility !='') :
                destination_path = os.path.join(BASE_DIR, 'static\\document_files\\'+mdl_id+'\\' + utility+'_'+sub_utility+'\\')
                fileInfo='\\static\\document_files\\'+mdl_id+'\\' + utility+'_'+sub_utility+'\\'+myfile.name
            else:
                destination_path = os.path.join(BASE_DIR, 'static\\document_files\\'+mdl_id+'\\' + utility+'\\')
                fileInfo='\\static\\document_files\\'+mdl_id+'\\' + utility+ '\\'+myfile.name
           
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)
                      
            if myfile != 'none':
                fs = FileSystemStorage()
                savefile_name = destination_path+myfile.name
                if os.path.exists(savefile_name):
                    os.remove(savefile_name)
                fs.save(savefile_name, myfile)   
             
    

    api_url=getAPIURL()+"insert_VT_Discussion_Comments/"       
    data_to_post={ 
        'utility':utility,
        'sub_utility':sub_utility,
        'comment':comment,
        'Added_by':request.session['uid'],
        'mdl_id':mdl_id, 
        'chat_data':chat_data,
        'destination_path':fileInfo,
        'section':section
    } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+ request.session['accessToken']
    }
    response = requests.post(api_url, data= json.dumps(data_to_post),headers=header)
     

    title_data=json.loads(response.content)

    return JsonResponse(title_data,safe=False)



def ValidationCommentHistory(request):
    try:
        mdl_id = request.GET.get('mdl_id', 'False') 
        utility = request.GET.get('utility','')
        sub_utility = request.GET.get('subutility','')
        chat_data = request.GET.get('chat_data','')
        third_party_api_url = getAPIURL()+'Fetch_message/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'room_id':'',
            'mdl_id':mdl_id,
            'utility':utility,
            'sub_utility':sub_utility,
            'chat_data':chat_data,
            'addedby':request.session['uid']
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        data=responseget.json()
        print("responseget History Data--------------------------",data['data'])
        return JsonResponse({'data':data['data'],'comment':data['comment']})  
    except Exception as e:
        print("error is",e)

def getValComms(request):
    try:
        comments = request.GET.getlist('comments[]') 
        ques = request.GET.getlist('ques[]')  
        api_url=getAPIURL()+"get_val_comments_data/"       
        data_to_save={ 
            'mdl_id':request.session['vt_mdl'],
            'section':'',
            'valcomms':comments} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        api_data = json.dumps(api_data).replace('null', '""')
        api_data=json.loads(api_data) 

        api_url=getAPIURL()+"Fetch_Allmessage/"       
        data_to_save={ 
            'mdl_id':request.session['vt_mdl']
        } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)         
        api_data_2=response.json() 
        api_data_2 = json.dumps(api_data_2).replace('null', '""')
        api_data_2=json.loads(api_data_2) 
      
        pdf = MyFPDF() 
        pdf.add_page('P') 
        pdf.set_font("Arial", size=9)
        x, y = 10, pdf.get_y()
        for i in api_data:
            strComm =i['comment'] 
            print('strComm is  ',strComm,type(api_data_2))
            # Filter python objects with list comprehensions
           
            pdf.set_xy(20, y)
            cellHeight = pdf.get_y()
            pdf.multi_cell(100, 4, str(strComm).encode(
                'latin-1', 'replace').decode('latin-1'), 1, fill=False)
            if(pdf.get_y() > cellHeight):
                cellHeight = pdf.get_y() 
            y = cellHeight  

            output_dict  ={k: v for k, v in api_data_2.items() if v['utility'] == i['utility']} # [person for person in api_data_2  if person['utility'] == i['utility']] #[x for x in api_data_2 if x['utility'] == i['utility']]
            
            # Transform python object back into json
            output_json = json.dumps(output_dict) 
            if not output_json=='{}':
                pdf.set_xy(20, y)
                pdf.cell(80, 5, "Dicussion for comment starts", 1)
                y += 5
                for key,value in output_dict.items():  
                    pdf.set_xy(20, y)                    
                    cellHeight = pdf.get_y()
                    pdf.multi_cell(100, 4, value['Comment'].encode(
                        'latin-1', 'replace').decode('latin-1'),1 ,fill=False)
                    if(pdf.get_y() > cellHeight):
                        y = pdf.get_y()+5
                    else:
                        y=cellHeight+5
                    pdf.set_xy(20, y)
                pdf.cell(80, 5, "Dicussion for comment ends", 1)
                y += 5
                pdf.set_xy(20, y)

        api_url=getAPIURL()+"getModelQtnById/"       
        data_to_save={ 
            'mdl_id':request.session['vt_mdl'],            
            'ques':ques} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        print('ques api_data ',api_data)
        api_data = json.dumps(api_data).replace('null', '""')
        api_data=json.loads(api_data) 
        strQuery=""
        for key,value in api_data['Qtns'].items():
            print('i is ',key,value)
            strQuery +=value['qtnsArr'] +'\n'
        x, y = 10, pdf.get_y()
        for key,value in api_data['Qtns'].items():
            pdf.set_xy(20, y)
            cellHeight = pdf.get_y()
            pdf.multi_cell(100, 4,"Question : "+ str(value['qtnsArr'] ).encode(
                'latin-1', 'replace').decode('latin-1'), 1, fill=False)
            if(pdf.get_y() > cellHeight):
                y = pdf.get_y() +5
            else:
                y=cellHeight+5
            pdf.set_xy(20, y)
            pdf.multi_cell(100, 4, "Answer : "+str(value['answer'] ).encode(
                'latin-1', 'replace').decode('latin-1'), 1, fill=False)
            cellHeight = pdf.get_y()
             
            if(pdf.get_y() > cellHeight):
                y = pdf.get_y() +5
            else:
                y=cellHeight+5
            pdf.set_xy(20, y)
        pdf.output(os.path.join(
            BASE_DIR, request.session['vt_mdl'] + "_Comments_chats.pdf")) 
        
        return JsonResponse({'data':'' })  
    except Exception as e:
        print("error is",e,traceback.print_exc())

def bankDetails(request):
    try:         
        api_url=getAPIURL()+"Is_BackInfo_Exists/"       
        bank_name=''
        bank_domain=''
        bank_address=''
        bank_logo=''
        bank_ai=''
        header = {
        "Content-Type":"application/json",
	   'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= {},headers=header)         
        api_data=response.json() 
        data=api_data['data']
        bankData=api_data['bankInfo']
        if int(data)>0:
            for i,k in bankData.items():
                bank_name=k['Bank_Name'] 
                bank_domain=k['Bank_Domain_Name'] 
                bank_address=k['Bank_Address'] 
                bank_logo=k['Bank_Logo']
                bank_ai=k['Bank_AI_Name']
        return render(request, 'bankDetails.html',{'boolShowMenu':data,'bankName':bank_name,'bankDomain':bank_domain,'bankAddress':bank_address,'bankLogo':bank_logo,'bankAI':bank_ai})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
 
def email_details(request):
    try:   
        api_url=getAPIURL()+"email_details/"       
       
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url,headers=header)         
        api_data_get=response.json() 
        print("api_data_get",api_data_get)

        if request.method == 'POST':
            sender_address = request.POST.get('sender_address')
            sender_password = request.POST.get('sender_password')
            smtp_server = request.POST.get('smtp_server')
            port = request.POST.get('port')

            # print("----- Received Email Details -----")
            # print("Sender Address :", sender_address)
            # print("Sender Password:", sender_password)
            # print("SMTP Server    :", smtp_server)
            # print("Port           :", port)
            # print("----------------------------------")
        
          
            api_url=getAPIURL()+"email_details/"       
            data_save={
                'sender_address':sender_address,
                'sender_password':sender_password,
                'smtp_server':smtp_server,
                'port':port
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(api_url,data= json.dumps(data_save),headers=header)         
            api_data=response.json() 
            print("api_data",api_data)
            return JsonResponse(api_data)         
        
        context={'email_settings':api_data_get}
        return render(request, 'email_details.html',context)
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 


def scheduler_notification(request):
        

    if request.method == 'POST':
        print("data",request.POST)
        alert_type = request.POST.get('alertType')
        frequency = request.POST.get('frequency')
        time = request.POST.get('time')
        day_of_week = request.POST.get('dayOfWeek')
        date_of_month = request.POST.get('dateOfMonth') or None
        days_before = request.POST.get('daysBefore')
        is_active = request.POST.get('isActive') == 'true'

        api_url=getAPIURL()+"scheduler_notification/"       
        data_save={
            'alert_type':alert_type,
            'frequency':frequency,
            'time':time,
            'day_of_week':day_of_week,
            'date_of_month':date_of_month,
            'days_before':days_before,
            'is_active':is_active

        }
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url,data= json.dumps(data_save),headers=header)         
        api_data=response.json() 
        print("api_data",api_data)
        return JsonResponse(api_data)         
    
    return render(request, 'scheduler_notification.html')

def get_alert_schedule_data(request):
    
    alert_type = request.GET.get('alert_type')

    api_url=getAPIURL()+"get_alert_schedule_data/"       
    data_to_get={
        'alert_type':alert_type
    }
       
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url,data= json.dumps(data_to_get),headers=header)         
    api_data_get=response.json() 
    print("api_data_get",api_data_get)

    return JsonResponse(api_data_get)
    
    


def addbank(request):
    try:
        if request.method == 'POST':  
            # myfile = request.FILES['myfile']
            filename = request.POST.get('filenm','none')
            bankName = request.POST.get('bankName', 'False') 
            bankAddress = request.POST.get('bankAddress','False')
            domain = request.POST.get('domain','False') 
            bankAI = request.POST.get('bankAI','False') 
            FinInst = request.POST.get('FinInst','False') 
            print(' filename ',filename)
            files = request.FILES
            myfile = files.get('filename', None)
            print('myfile ',myfile,' filename ',filename)
            if myfile=="" or myfile ==None:
                third_party_api_url = getAPIURL()+'Add_BankInfo/'
                data_to_save = {
                    'bankName':bankName,
                    'bankAddress':bankAddress,
                    'domain':domain,
                    'file_name':filename,
                    'bankAI':bankAI,
                    'FinInst':FinInst,
                    'addedby':request.session['uid']
                }
                header = {
                "Content-Type":"application/json",
                'Authorization': 'Token '+request.session['accessToken']
                }
                response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header) 
                return JsonResponse({"is_taken": True,'data':'Uploaded Successfully'})          
            else:     
                fs = FileSystemStorage() 
                fs.save(os.path.join(BASE_DIR,  'static/Bank_Data/Logo/',filename), myfile)                    
                   
        
                third_party_api_url = getAPIURL()+'Add_BankInfo/'
                data_to_save = {
                    'bankName':bankName,
                    'bankAddress':bankAddress,
                    'domain':domain,
                    'file_name':filename,
                    'bankAI':bankAI,
                    'addedby':request.session['uid']
                }
                header = {
                "Content-Type":"application/json",
                'Authorization': 'Token '+request.session['accessToken']
                }
                response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header) 
                res = JsonResponse({"is_taken": True,'data':'Uploaded Successfully'})            
                return res  
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def bankDocs(request):
    try:   
        return render(request, 'bankDocs.html')
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 

def addbankDoc(request):
    try:
        if request.method == 'POST':  
            # myfile = request.FILES['myfile']
            filename = request.POST.get('filenm','none')
            docType = request.POST.get('docType', 'False') 
            docDesc = request.POST.get('docDesc','False')  
            files = request.FILES
            myfile = files.get('filename', None) 
             
            fs = FileSystemStorage() 
            fs.save(os.path.join(BASE_DIR,  'static/Bank_Data/Documents/',filename), myfile)                    
                
    
            third_party_api_url = getAPIURL()+'Add_BankDoc/'
            data_to_save = {
                'docType':docType,
                'docDesc':docDesc,                
                'docName':filename, 
                'addedby':request.session['uid']
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header) 
            res = JsonResponse({"is_taken": True,'data':'Uploaded Successfully'})            
            return res  
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

def getModelQtnById(request):
    api_url=getAPIURL()+"getModelQtnById/"       
    data_to_save={ 
        'mdl_id':request.session['vt_mdl'],            
        'ques':''} 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
        
    api_data=response.json() 
    api_data = json.dumps(api_data).replace('null', '""')
    api_data=json.loads(api_data) 
    return JsonResponse({"Qtns":api_data['Qtns']})

def getFL_Tbl_Cols(request):
    api_url=getFLAPIURL()+"getFL_Tbl_Cols/"       
    data_to_save={} 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
        
    api_data=response.json() 
    api_data = json.dumps(api_data).replace('null', '""')
    api_data=json.loads(api_data) 
    # for i,val in api_data.items():
    #     print('data is ',val['ColumnName'])

    api_url=getFLAPIURL()+"getFL_Ctrl_Class_Cols/"       
    data_to_save={
        'Portfolio':'Mortgage',
        'Dept':request.session['dept']
    } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
        
    ctrl_class_data=response.json()  
    
    arrCols=[ api_data[key]['ColumnName'] for key in api_data.keys()]
    api_url = getFLAPIURL()+'GET_FL_Data_Info/' 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }       
    data_params={
        'uid':request.session['uid']  , 
        'activity_year':request.GET.get('activity_year','2023'),
        'portfolio':'Mortgage',
        'dept':'17'
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data=response.json()  
    print('api_data ',api_data)
    return render(request, 'dashboard_fl.html',{'arrCols':arrCols,'ctrl_cols':ctrl_class_data['ColumnName'],'querybldrcols':api_data['gridDttypes']})


def Perf_monitoring_file_upload(request):
    try:
        mdl_id = request.POST.get('mdl_id','false')
        
        filename_a = request.POST.get('filenm','none') 
        historical = request.POST.get('historical','none')
        print("historical",historical)
        utility_type = request.POST.get('utility_type','none')
        
        files = request.FILES
        myfile = files.get('filename', None) 
        df1 = pd.read_excel(myfile) 
        ### Historical Condition
        if historical == 'true':
            print("historical")
            third_party_api_url = getAPIURL()+'getMaxFreqSeq/'
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            freidx=1
            is_new=0
            data_to_save = {
                'mdl_id':mdl_id  
            }
            responseget = requests.get(third_party_api_url, data= json.dumps(data_to_save),headers=header)             
            data=responseget.json() 
            for ir,val in data['freqData'].items():
                is_new=val['addorupdate']
                freidx=val['freqidx']
            # mdlid =request.GET.get('mdlid', 'False') 

            third_party_api_url = getAPIURL()+'getTemplateData/'
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            data_to_get = { 
                'mdl_id':mdl_id ,
                'freq_idx':freidx
            }
            responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
            # data=json.loads(responseget.content)
            data=responseget.json()
            # print("responseget--------------------------",data['mmdata'])
            print("responseget new api fetch mmlabel agains mdlid--------------------------",data['mmdata'])
            lst = []
            for i in data['mmdata']:
                lst.append(i['mm_details']['mm_label'])
            print("new label lst",lst)
            dframe1 = pd.DataFrame(index = ['0'],columns = lst)
            exceldf = dframe1.to_json(orient="records")
            print("df2 columns",dframe1.columns.to_list())
            excel_fields = df1.columns.to_list()
            excel_fields_1  = df1.to_json(orient="records")
            print("df1 columns",df1.columns.to_list())

            if list(dframe1.columns.values) == list(df1.columns.values): 
                third_party_api_url  = getAPIURL()+'PerfMontrMappingAPI/'
                data_to_save={ 
                    'addedby':request.session['uid'],
                    'excel_fields':excel_fields,
                    'department':"MRM",
                    'portfolio':"MRM",
                    'exceldf':json.loads(excel_fields_1),
                    'mdl_id':mdl_id,
                    'datatype':utility_type
                    } 
                header = {
                "Content-Type":"application/json",
                'Authorization': 'Token '+request.session['accessToken']
                }
                responsepost = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)    
                api_data=responsepost.json()
                print("api data perf montr mapping------------",api_data)
                return JsonResponse(api_data)
            else:
                print("false only")
                return JsonResponse({'isvalid':'false'})
        else:
            pass
        ###
        filename = filename_a.split('.')
        BASE_DIR = Path(__file__).resolve().parent.parent
            
        file_check_path = str(BASE_DIR)+'/static/document_files/'+ mdl_id + '/' +'templates/' +mdl_id+".xlsx" 
        df2 = pd.read_excel(file_check_path) 
        if list(df1.columns.values) == list(df2.columns.values): 
            if filename_a != None and myfile != None:
                fs = FileSystemStorage() 
                filePath=os.path.join(BASE_DIR, 'static/document_files/'+mdl_id+'/'+'production_output/'+filename_a)
                if os.path.exists(filePath): 
                    os.remove(filePath)
                    print("remove filename",filePath)
                fs.save(os.path.join(BASE_DIR, 'static/document_files/'+mdl_id+'/'+'production_output/'+filename_a), myfile) 

                third_party_api_url = getAPIURL()+'getMaxFreqSeq/'
                header = {
                "Content-Type":"application/json",
                'Authorization': 'Token '+request.session['accessToken']
                }
                freidx=1
                is_new=0
                data_to_save = {
                    'mdl_id':mdl_id, 
                }
                responseget = requests.get(third_party_api_url, data= json.dumps(data_to_save),headers=header)             
                data=responseget.json() 
                for ir,val in data['freqData'].items():
                    is_new=val['addorupdate']
                    freidx=val['freqidx']
                if historical == 'true':
                    print("historical")
                else:
                    pass
                third_party_api_url = getAPIURL()+'perfMonitoringFileInfoAPI/'
                header = {
                "Content-Type":"application/json",
                'Authorization': 'Token '+request.session['accessToken']
                }

                data_to_save = {
                    'mdl_id':mdl_id,
                    'file_nm':filename_a,
                    'added_by':request.session['uid'],
                    'freq_idx':freidx,
                    'is_new':is_new
                }
                responseget = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
                # data=json.loads(responseget.content)
                print("response--------------------------",json.loads(responseget.content))
                return JsonResponse({"isvalid":"true"})
            else:
                return JsonResponse({"isvalid":"false"})
        else:
            print("columns are not same")
            return JsonResponse({"isvalid":"false"})
    except Exception as e:
        print("file error is ",e)


def Perf_monitoring_file_upload_bus(request):
    mdl_id = request.POST.get('mdl_id','false')
    
    historical = request.POST.get('historical','none')
    print("historical",historical)
    utility_type = request.POST.get('utility_type','none')
    filename_a = request.POST.get('filenm','none')
    
    files = request.FILES
    myfile = files.get('filename', None) ####

    df1 = pd.read_excel(myfile)
    print("df1-----------",list(df1.columns.values))
    ####
    if historical == 'true':        
        third_party_api_url = getAPIURL()+'GetHistoryMsg/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_get = {
            'room_id':"",
            'mdl_id':mdl_id,
            'addedby':request.session['uid']
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        # data=json.loads(responseget.content)
        data=responseget.json()
        # print("responseget--------------------------",data['mmdata'])
        print("responseget new api fetch bmlabel agains mdlid--------------------------",data['bmdata_b'])
        lst = []
        for i in data['bmdata_b']:
            lst.append(i['bm_details']['bm_label'])
        print("new label lst",lst)
        dframe1 = pd.DataFrame(index = ['0'],columns = lst)
        print("--------------------Business---------------------------")
        exceldf = dframe1.to_json(orient="records")
        print("df2 columns",dframe1.columns.to_list())
        excel_fields = df1.columns.to_list()
        excel_fields_1  = df1.to_json(orient="records")
        print("df1 columns",df1.columns.to_list())

        if list(dframe1.columns.values) == list(df1.columns.values): 
            third_party_api_url  = getAPIURL()+'PerfMontrMappingAPI/'
            data_to_save={ 
                'addedby':request.session['uid'],
                'excel_fields':excel_fields,
                'department':"MRM",
                'portfolio':"MRM",
                'exceldf':json.loads(excel_fields_1),
                'mdl_id':mdl_id,
                'datatype':utility_type
                } 
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            responsepost = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)    
            api_data=responsepost.json()
            print("api data perf montr mapping business------------",api_data)
            return JsonResponse(api_data)
    else:
        print("false only")
        return JsonResponse({'isvalid':'false'})
    ####
    filename = filename_a.split('.')
    print("filename",filename[0])
    BASE_DIR = Path(__file__).resolve().parent.parent        
    file_check_path = str(BASE_DIR)+'/static/document_files/'+ mdl_id + '/' +'templates/' +filename_a
    print("file_check_path",file_check_path)
    df2 = pd.read_excel(file_check_path)
    print("df2------------",list(df2.columns.values))
    if list(df1.columns.values) == list(df2.columns.values):
        print("columns are same")
        if filename_a != None and myfile != None:
            fs = FileSystemStorage() 
            filePath=os.path.join(BASE_DIR, 'static/document_files/'+mdl_id+'/'+'production_output/'+filename_a)
            if os.path.exists(filePath): 
                os.remove(filePath)
                print("remove filename",filePath)
            fs.save(os.path.join(BASE_DIR, 'static/document_files/'+mdl_id+'/'+'production_output/'+filename_a), myfile) 

            third_party_api_url = getAPIURL()+'getMaxFreqSeq_Buss/'
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            freidx=1
            is_new=0
            data_to_save = {
                'mdl_id':mdl_id, 
            }
            responseget = requests.get(third_party_api_url, data= json.dumps(data_to_save),headers=header)             
            data_maxfreq=responseget.json() 
            for ir,val in data_maxfreq['freqData'].items():
                is_new=val['addorupdate']
                freidx=val['freqidx']

            third_party_api_url = getAPIURL()+'perfMonitoringFileInfoAPI/'
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }

            data_to_save = {
                'mdl_id':mdl_id,
                'file_nm':filename_a,
                'added_by':request.session['uid'],
                'freq_idx':freidx,
                'is_new':is_new
            }
            responseget = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
            # data=json.loads(responseget.content)
            print("response--------------------------",json.loads(responseget.content))
            return JsonResponse({"isvalid":"true"})
        else:
            return JsonResponse({"isvalid":"false"})
    else:
        print("columns are not same")
        return JsonResponse({"isvalid":"false"})

def ModelMatricsData(request):
    try:
        print("request_data",request.GET)
        modelmatrics = request.GET.get('modelmatrics','false')
        mdlid = request.GET.get('mdlid','false')
        datatype = request.GET.get('datatype','false')

        third_party_api_url = getAPIURL()+'ModelMatricDataAPI/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_get = {
            'model_matrics':modelmatrics,
            'mdlid':mdlid,
            'datatype':datatype
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        data=json.loads(responseget.content)
        print("responseget for model matrics updated new--------------------------",data['data'])
        print("responseget for model matrics updated new moving--------------------------",data['mdldata'])

        first_key = next(iter(data['data']))
        print("first_key",first_key,data['data'][first_key])
        chartData=[float(i) for i in data['data'][first_key]]

        print('chartData ',chartData)
        mean = np.mean(chartData)  
        std_dev = np.std(chartData)  

        # Control limits
        UCL = mean + 3 * std_dev
        LCL = mean - 3 * std_dev


        #Moving data
        mean_1 = np.mean(data['mdldata'])  
        std_dev_1 = np.std(data['mdldata'])  

        # Control limits
        UCL_1 = mean_1 + 3 * std_dev_1
        LCL_1 = mean_1 - 3 * std_dev_1

        data = {
            'data' : data['data'][first_key],
            'mean' : mean,
            'UCL' : UCL,
            'LCL':LCL,
            'date':data['data']['adddate'],
            'data_1':data['mdldata'],
            'mean_1':mean_1,
            'std_dev_1':std_dev_1,
            'UCL_1':UCL_1,
            'LCL_1':LCL_1
        }

        print("data",data)

        return JsonResponse({"data":data})
    except Exception as e:
        print("error is",e)


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
 
from fpdf import FPDF, HTMLMixin
class MyFPDF(FPDF, HTMLMixin):
    pass




def show_issue_function(request):
    print("show_issue_function")
    try: 
        third_party_api_url = getAPIURL()+'issue-function-master/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("issue function response",response.content)

        return render(request, 'show_issue_function.html',{'actPage' :'RMSE - Issue Function','users':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())
    
def add_new_issue(request):
    try:   
        return render(request, 'add_new_issue.html',{'actPage':'RMSE - Add Issue Function'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def save_issue_function(request):
    print()
    try:
        print("---------save_issue_function ",request.POST)
        # request_data = {x:request.GET.get(x) for x in request.GET.keys()}
        if request.method == 'POST':
            update_id = request.POST.get('update_id')  # Key should match the AJAX data key
            label = request.POST.get('label')
            desc = request.POST.get('desc')
            rbactivests = request.POST.get('rbactivests')
            print('update_id',update_id)
            print("issue_function_label,issue_function_description",label,desc)

            if update_id :
                print("update issue function")
                third_party_api_url = getAPIURL()+'issue-function-master/'

                data_to_update = {
                    'issue_function_label':label,
                    'issue_function_description':desc,
                    'activestatus':rbactivests,
                    'id':update_id
                }
                header = {
                "Content-Type":"application/json",
                'Authorization': 'Token '+request.session['accessToken']
                }
                response = requests.put(third_party_api_url, data= json.dumps(data_to_update),headers=header)
                
                print("response content",response.content,response.status_code)
                return JsonResponse(json.loads(response.content))
            
            else:
                print("add issue function")
                
                third_party_api_url = getAPIURL()+'issue-function-master/'

                data_to_save = {
                    'issue_function_label':label,
                    'issue_function_description':desc,
                    'activestatus':rbactivests
                }
                header = {
                "Content-Type":"application/json",
                'Authorization': 'Token '+request.session['accessToken']
                }
                response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
                
                print("response content",response.content,response.status_code)
                return JsonResponse(json.loads(response.content))
    except requests.exceptions.RequestException as e:
                return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  



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
        rbactivests = request.POST.get('rbactivests')

        print('update_id',id)
        print("issue_priority_label,issue_priority_description",issue_priority_label,issue_priority_description)

        if id != 'undefined':
            print("update_issue_priority")
            
            third_party_api_url = getAPIURL()+'issue-priority-master/'

            data_to_update = {
                'issue_priority_label':issue_priority_label,
                'issue_priority_description':issue_priority_description,
                'activestatus':rbactivests,
                'id':id
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.put(third_party_api_url, data= json.dumps(data_to_update),headers=header)
            
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))

        else:
            print("save_issue_priority")
            
            third_party_api_url = getAPIURL()+'issue-priority-master/'

            data_to_save = {
                'issue_priority_label':issue_priority_label,
                'issue_priority_description':issue_priority_description,
                'activestatus':rbactivests
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
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
        rbactivests = request.POST.get('rbactivests')
        
        print("update_id",id)
        print("issue_approval_status_label,issue_approval_status_description",issue_approval_status_label,issue_approval_status_description)

        if id != 'undefined':
            print("update issue_approval_status")
           
            third_party_api_url = getAPIURL()+'issue-approval-status-master/'

            data_to_update = {
                'issue_approvalstatus_label':issue_approval_status_label,
                'issue_approvalstatus_description':issue_approval_status_description,
                'activestatus':rbactivests,
                'id':id    
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.put(third_party_api_url, data= json.dumps(data_to_update),headers=header)

            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))

        else:    
            print("Add issue_approval_status")

            third_party_api_url = getAPIURL()+'issue-approval-status-master/'

            data_to_save = {
                'issue_approvalstatus_label':issue_approval_status_label,
                'issue_approvalstatus_description':issue_approval_status_description,
                'activestatus':rbactivests,
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
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
        
        id=request.POST.get('update_id')
        issue_type_label = request.POST.get('label','False')
        issue_type_description = request.POST.get('desc','False')
        rbactivests = request.POST.get('rbactivests')
        print('update_id',id)
        print("issue_type_label,issue_type_description",issue_type_label,issue_type_description)

        if id :

            print("update issue type")
            third_party_api_url = getAPIURL()+'issue-type-master/'
            
            data_to_update = {
                'issue_type_label':issue_type_label,
                'issue_type_description':issue_type_description,
                'activestatus':rbactivests,
                'id':id
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.put(third_party_api_url, data= json.dumps(data_to_update),headers=header)
            
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
        else:
            print("Add issue type")

            third_party_api_url = getAPIURL()+'issue-type-master/'

            data_to_save = {
                'issue_type_label':issue_type_label,
                'issue_type_description':issue_type_description,
                'activestatus':rbactivests
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
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
        rbactivests = request.POST.get('rbactivests')
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
                'activestatus':rbactivests,
                'sub_issue_type_aid':id
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
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
                'activestatus':rbactivests,
                'issue_type_aid':issue_type,
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
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
    print("status",data['data']['activestatus'])
    if data['data']['activestatus'] == True:
        status = 'Active'
    else :
        status = 'Inactive'   
    return render(request, 'add_new_issue.html',{'issue_function_label':data['data']['issue_function_label'],
                                                     'issue_function_desc':data['data']['issue_function_description'],
                                                    'status':status,'id':id})


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
    print("status",data['data']['activestatus'])
    if data['data']['activestatus'] == True:
        status = 'Active'
    else :
        status = 'Inactive'
    return render(request, 'add_issue_type.html',{'issue_type_label':data['data']['issue_type_label'],
                                                     'issue_type_description':data['data']['issue_type_description'],
                                                     'status':status,'id':id})

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
    if data['data']['activestatus'] == True:
        status = 'Active'
    else :
        status = 'Inactive'
    return render(request, 'add_sub_issue_type.html',{'sub_issue_type_label':data['data']['sub_issue_type_label'],
                                                     'sub_issue_type_description':data['data']['sub_issue_type_description'],
                                                     'id':id,'issue_type':data['data']['issue_type_details'],
                                                     'status':status,'type':'edit'})
          

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
    if data['data']['activestatus'] == True:
        status = 'Active'
    else :
        status = 'Inactive'
    return render(request, 'add_issue_priority.html',{'issue_priority_label':data['data']['issue_priority_label'],
                                                    'status':status,
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
    if data['data']['activestatus'] == True:
        status = 'Active'
    else :
        status = 'Inactive'
    return render(request, 'add_issue_approval.html',{'issue_approval_status_label':data['data']['issue_approvalstatus_label'],
                                                      'status':status,
                                                     'issue_approval_status_description':data['data']['issue_approvalstatus_description'],'id':id})      


def show_mdl_category(request):
    try: 
        third_party_api_url = getAPIURL()+'category_master/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("section response",response.content)

        return render(request, 'show_mdl_category.html',{'actPage' :'RMSE - Section','users':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())

  
def add_category(request):
    try:   
        return render(request, 'add_category.html',{'actPage':'RMSE - Add Issue Type'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def save_category(request):
    try:
        print("---------save_category",request.POST)
        
        if request.method == 'POST':
            update_id = request.POST.get('update_id')  # Key should match the AJAX data key
            label = request.POST.get('label')
            desc = request.POST.get('desc')
            print('update_id',update_id)
            print("section,description",label,desc)

            if update_id:

                print("update category")
                third_party_api_url = getAPIURL()+'category_master/'
                
                data_to_update = {
                    'category_label':label,
                    'category_description':desc,
                    'id':update_id
                }
                header = {
                "Content-Type":"application/json",
                'Authorization': 'Token '+request.session['accessToken']
                }
                response = requests.put(third_party_api_url, data= json.dumps(data_to_update),headers=header)
                
                print("response content",response.content,response.status_code)
                return JsonResponse(json.loads(response.content))
            else:
                print("Add category")

                third_party_api_url = getAPIURL()+'category_master/'

                data_to_save = {
                    'category_label':label,
                    'category_description':desc
                }
                header = {
                "Content-Type":"application/json",
                'Authorization': 'Token '+request.session['accessToken']
                }
                response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
                
                print("response content",response.content,response.status_code)
                return JsonResponse(json.loads(response.content))
            
    except requests.exceptions.RequestException as e:
                return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

def edit_category(request,id):
    print("edit_section",id)
    third_party_api_url = getAPIURL()+'category_master/'+id
        
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(third_party_api_url,headers=header)
    print("response content",response.content,response.status_code)
    data=json.loads(response.content)
    print("data",data)
    print("label",data['data']['category_label'])
    return render(request, 'add_category.html',{'category_label':data['data']['category_label'],
                                                     'category_description':data['data']['category_description'],'id':id})




def show_sub_mdl_category(request):
    try: 
        third_party_api_url = getAPIURL()+'sub_category_master/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("issue function response",response.content)

        return render(request, 'show_sub_mdl_category.html',{'actPage' :'RMSE - Sub Section','users':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())


def add_sub_category(request):
    try: 
        typeobj = ModelCategory.objects.all()
        return render(request, 'add_sub_category.html',{'actPage':'RMSE - Add Sub Issue Type','Category':typeobj,'type':'add'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def save_sub_category(request):
    try:
        print("---------save_sub_category",request.POST)
    
        id=request.POST.get('update_id','False')
        sub_category_label = request.POST.get('label','False') 
        sub_category_description = request.POST.get('desc','False')
        category_aid = request.POST.get('issuetype','False')
        print("update_id",id)
        print("category_aid",category_aid)

        print("sub_category_label,sub_category_description,issue_type",sub_category_label,sub_category_description,category_aid)
        if id != 'undefined':
            print("update save_sub_section ")
       
            third_party_api_url = getAPIURL()+'sub_category_master/'
            
            data_to_update = {
                'sub_category_label':sub_category_label,
                'sub_category_description':sub_category_description,
                'category_aid':category_aid,
                'sub_category_aid':id
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.put(third_party_api_url, data= json.dumps(data_to_update),headers=header)
            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
        else:
            print("Add save_sub_section ")
            third_party_api_url = getAPIURL()+'sub_category_master/'

            print("sub_category_label,sub_category_description,issue_type",sub_category_label,sub_category_description,category_aid)

            data_to_save = {
                'sub_category_label':sub_category_label,
                'sub_category_description':sub_category_description,
                'category_aid':category_aid,
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)

            print("response content",response.content,response.status_code)
            return JsonResponse(json.loads(response.content))
        
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def edit_sub_category(request,id):
    print("edit_sub_category",id)
    third_party_api_url = getAPIURL()+'sub_category_master/'+id
        
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(third_party_api_url,headers=header)
    print("response content",response.content,response.status_code)
    data=json.loads(response.content)
    print("data",data)
    print("label",data['data']['sub_category_label'])
    category_details=data['data']['category_details']
    print("category_details",category_details)
    return render(request, 'add_sub_category.html',{'sub_category_label':data['data']['sub_category_label'],'category_details':category_details,
                                                     'sub_category_description':data['data']['sub_category_description'],'id':id})



# def getSubcat(request):
#     try:       
        
#         cat_id =request.GET.get('secid', 'False')     
#         print("cat_id",cat_id) 
        
#         third_party_api_url = getAPIURL()+'getSubCategory/'+cat_id

#         header = {
#         "Content-Type":"application/json",
# 	    'Authorization': 'Token '+request.session['accessToken']
#         }
#         response_cat = requests.get(third_party_api_url, headers=header)
#         print("response category_master",response_cat.content) 
        
#         return JsonResponse({'sub_cat':json.loads(response_cat.content)})
#     except Exception as e:
#         print('addSection is ',e)
#         print('addSection traceback is ', traceback.print_exc()) 

# def savemodelmetrics(request):
#     print("savemodelmetrics",request.POST)
   
#     try:
       
#         added_by=request.session['uid']
#         metric = request.POST.get('metric','False')
#         dept_label = request.POST.getlist('depart_id[]')
#         desc = request.POST.get('desc','False')
#         activests = request.POST.get('activests','False')
#         isglobal = request.POST.get('isglobal','False')
#         update_id = request.POST.get('update_id','False')
#         category = request.POST.get('cat','False')
#         sub_category = request.POST.get('sub_cat','False')

#         print("update id",update_id)
#         print("Metric data",metric,dept_label,desc,activests,isglobal)
#         if update_id=='False':
#             print("add")
#             third_party_api_url = getAPIURL()+'savemodelmetrics/'
#             data_to_save = {
#                 'mm_label':metric,
#                 'mm_description':desc,
#                 'mm_status':activests,
#                 'mm_is_global':isglobal,
#                 'added_by':added_by,
#             }
#             header = {
#             "Content-Type":"application/json",
#             'Authorization': 'Token '+request.session['accessToken']
#             }
#             response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
#             data=json.loads(response.content)
#             print("data",data)
#             print("data",data['data']['mm_aid'])

#             for i in dept_label:
#                 print("i",i)
#                 third_party_api_url = getAPIURL()+'savemodeldepartment/'
#                 data_to_save = {
#                     'mm_aid':data['data']['mm_aid'],
#                     'dept_aid':i,
#                     'added_by_field':added_by,
#                     'model_category':category,
#                     'model_sub_category':sub_category
#                 }
#                 header = {
#                 "Content-Type":"application/json",
#                'Authorization': 'Token '+request.session['accessToken']
#                 }
#                 response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
#                 data=json.loads(response.content)
#                 print("data",data)

#             return JsonResponse(data)
#         else:
#             print("update one")
#             third_party_api_url = getAPIURL()+'savemodelmetrics/'
#             data_to_save = {
#                 'id':update_id,
#                 'mm_label':metric,
#                 'mm_description':desc,
#                 'mm_status':activests,
#                 'mm_is_global':isglobal,
#                 'added_by':added_by,
#             }
#             header = {
#             "Content-Type":"application/json",
#             'Authorization': 'Token '+request.session['accessToken']
#             }
#             response = requests.put(third_party_api_url, data= json.dumps(data_to_save),headers=header)
#             data=json.loads(response.content)
#             print("data",data)
#             print("data",data['data']['mm_aid'])
            
#             for i in dept_label:
#                 print("i",i,"data",data)
#                 #chek dept is available
#                 third_party_api_url = getAPIURL()+'checkMetricDept/'
#                 data = {
#                     'mm_aid':data['data']['mm_aid'],
#                     'dept_aid':i,
#                     'added_by_field':added_by
#                 }
#                 header = {
#                 "Content-Type":"application/json",
#                 'Authorization': 'Token '+request.session['accessToken']
#                 }
#                 response_dept = requests.get(third_party_api_url, data= json.dumps(data),headers=header)
#                 print("Metric dept data------------",response_dept.content)
#                 ###
#                 print('data2',data)
                
#                 dept_data = json.loads(response_dept.content)
#                 print("qwer------------------",dept_data['data'])

#                 if len(dept_data['data']) == 0:
#                     third_party_api_url = getAPIURL()+'savemodeldepartment/'
#                     data_to_update = {
#                         'mm_aid':data['mm_aid'],
#                         'dept_aid':i,
#                         'added_by_field':added_by
#                     }
#                     header = {
#                     "Content-Type":"application/json",
#                     'Authorization': 'Token '+request.session['accessToken']
#                     }
#                     response = requests.post(third_party_api_url, data= json.dumps(data_to_update),headers=header)
#                     resp_data=json.loads(response.content)
#                     print("final data---------------",resp_data)
#                     return JsonResponse({"msg":"model Metric Updated Successfully"})                    
#                 else:
#                     return JsonResponse({'msg':'Metric Dept Already Created'})        
#     except Exception as e:
#         print('adduser is ',e)
#         print('adduser traceback is ', traceback.print_exc())




# def showModelMetrics(request):
#     try:  
#         third_party_api_url = getAPIURL()+'AddModelMetrics/'
#         header = {
#         "Content-Type":"application/json",
# 	    'Authorization': 'Token '+request.session['accessToken']
#         }
#         response = requests.get(third_party_api_url, headers=header)
#         print("Model Metrics data response------------------------------------",response.content)
#         # funobj = TaskFunctionMaster.objects.all()

#         return render(request, 'show_modelmetrics.html',{'actPage' :'RMSE - Frequency Function','mm_data':json.loads(response.content)})
#     except Exception as e:
#         print('adduser is ',e) 
#         print('adduser traceback is ', traceback.print_exc())


# def addModelMetrics(request):
#     try: 
#         #new
#         third_party_api_url = getAPIURL()+'department/'
#         header = {
#         "Content-Type":"application/json",
# 	    'Authorization': 'Token '+request.session['accessToken']
#         }
#         response = requests.get(third_party_api_url, headers=header)
#         ##category
#         third_party_api_url = getAPIURL()+'category_master/'
#         header = {
#         "Content-Type":"application/json",
# 	    'Authorization': 'Token '+request.session['accessToken']
#         }
#         response_cat = requests.get(third_party_api_url, headers=header) 
#         return render(request, 'addModelMetrics.html',{ 'actPage':'Departments','users':json.loads(response.content),'category':json.loads(response_cat.content)})
#     except Exception as e:
#         print('adduser is ',e)
#         print('adduser traceback is ', traceback.print_exc())


# def edit_ModelMetricsMaster(request,id):
#     print("edit_ModelMetricsMaster",id)
#     try: 
#         third_party_api_url = getAPIURL()+'editmodelmetrics/'+id
#         header = {
#         "Content-Type":"application/json",
# 	    'Authorization': 'Token '+request.session['accessToken']
#         }
#         response = requests.get(third_party_api_url, headers=header)
#         print("response ------Model Metrics------",response.content)
#         model_metric_data = json.loads(response.content)
#         mm_aid = model_metric_data['data']['mm_aid']
#         mm_label = model_metric_data['data']['mm_label']
#         mm_description = model_metric_data['data']['mm_description']
#         mm_status = 1
#         mm_is_global = 1
#         departments = model_metric_data['data']['departments']
#         dept_list = model_metric_data['data']['departments_list']
#         print("department",departments)
#         #department
#         third_party_api_url = getAPIURL()+'department/'
#         header = {
#         "Content-Type":"application/json",
# 	    'Authorization': 'Token '+request.session['accessToken']
#         }
#         response_dept = requests.get(third_party_api_url, headers=header)

#         return render(request, 'addModelMetrics.html',{'mm_aid':mm_aid,'mm_label':mm_label,'mm_description':mm_description,'mm_status':mm_status,'mm_is_global':mm_is_global,'departments':departments,'users':json.loads(response_dept.content),'dept_list':dept_list})
#     except Exception as e:
#         print('adduser is ',e) 
#         print('adduser traceback is ', traceback.print_exc())  

def showModelMetrics(request):
    try:  
        third_party_api_url = getAPIURL()+'AddModelMetrics/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("Model Metrics data response------------------------------------",response.content)
        # funobj = TaskFunctionMaster.objects.all()

        return render(request, 'show_modelmetrics.html',{'actPage' :'RMSE - Frequency Function','mm_data':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())


def addModelMetrics(request):
    try: 
        #new
        third_party_api_url = getAPIURL()+'department/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        ##category
        third_party_api_url = getAPIURL()+'category_master/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response_cat = requests.get(third_party_api_url, headers=header)
        print("response category_master",response_cat.content) 
        return render(request, 'addModelMetrics.html',{ 'actPage':'Departments','users':json.loads(response.content),'category':json.loads(response_cat.content)})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def getSubcat(request):
    try:       
        
        cat_id =request.GET.get('secid', 'False')     
        print("cat_id",cat_id) 
        
        third_party_api_url = getAPIURL()+'getSubCategory/'+cat_id

        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response_cat = requests.get(third_party_api_url, headers=header)
        print("response category_master",response_cat.content) 
        
        return JsonResponse({'sub_cat':json.loads(response_cat.content)})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 

def edit_ModelMetricsMaster(request,id):
    print("edit_ModelMetricsMaster",id)
    try: 
        third_party_api_url = getAPIURL()+'editmodelmetrics/'+id
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response ------Model Metrics------",response.content)
        model_metric_data = json.loads(response.content)
        mm_aid = model_metric_data['data']['mm_aid']
        mm_label = model_metric_data['data']['mm_label']
        mm_description = model_metric_data['data']['mm_description']
        mm_status= model_metric_data['data']['mm_status']
        mm_is_global= model_metric_data['data']['mm_is_global']
        # mm_status = 1
        # mm_is_global = 1
        departments = model_metric_data['data']['departments']
        dept_list = model_metric_data['data']['departments_list']
        print("department",departments)
        #department
        third_party_api_url = getAPIURL()+'department/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response_dept = requests.get(third_party_api_url, headers=header)

        ##get Business metric
        third_party_api_url = getAPIURL()+'get_model_cat_subcat/'
        data_to_save = {'mm_aid':mm_aid}
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response_cat_subcat = requests.get(third_party_api_url,params=data_to_save, headers=header)
        print("response ------model Metrics------",response_cat_subcat.content)
        response_cat=json.loads(response_cat_subcat.content)
        print("response_cat",type(response_cat))
        category_label=response_cat['category_label']
        sub_category_label=response_cat['sub_category_label']
        
        return render(request, 'addModelMetrics.html',{'mm_aid':mm_aid,'mm_label':mm_label,'mm_description':mm_description,
        'mm_status':mm_status,'mm_is_global':mm_is_global,'departments':departments,
        'users':json.loads(response_dept.content),'dept_list':dept_list,
        'category_label':category_label,'sub_category_label':sub_category_label})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())  


def savemodelmetrics(request):
    print("savemodelmetrics",request.POST)
   
    try:
       
        added_by=request.session['uid']
        metric = request.POST.get('metric','False')
        dept_label = request.POST.getlist('depart_id[]')
        desc = request.POST.get('desc','False')
        activests = request.POST.get('activests','False')
        isglobal = request.POST.get('isglobal','False')
        update_id = request.POST.get('update_id','False')
        category = request.POST.get('cat','False')
        sub_category = request.POST.get('sub_cat','False')
        print("category",category)
        print("sub_category",sub_category)
        print("update id",update_id)
        print("Metric data",metric,dept_label,desc,activests,isglobal)
        if update_id=='False':
            print("add")
            third_party_api_url = getAPIURL()+'savemodelmetrics/'
            data_to_save = {
                'mm_label':metric,
                'mm_description':desc,
                'mm_status':activests,
                'mm_is_global':isglobal,
                'added_by':added_by,
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
            data=json.loads(response.content)
            print("data",data)
            print("data",data['data']['mm_aid'])

            mm_aid=data['data']['mm_aid']
            print("mm_aid",mm_aid)
            
            for i in dept_label:
                print("i",i)
                third_party_api_url = getAPIURL()+'savemodeldepartment/'
                data_to_save = {
                    'mm_aid':mm_aid,
                    'dept_aid':i,
                    'added_by_field':added_by,
                    'category_aid':category,
                    'sub_category_aid':sub_category
                }
                header = {
                "Content-Type":"application/json",
               'Authorization': 'Token '+request.session['accessToken']
                }
                response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
                data=json.loads(response.content)
                print("data",data)

            return JsonResponse(data)
        else:
            print("update one")
            third_party_api_url = getAPIURL()+'savemodelmetrics/'
            data_to_save = {
                'id':update_id,
                'mm_label':metric,
                'mm_description':desc,
                'mm_status':activests,
                'mm_is_global':isglobal,
                'added_by':added_by,
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.put(third_party_api_url, data= json.dumps(data_to_save),headers=header)
            data=json.loads(response.content)
            print("data",data)
            print("data",data['data']['mm_aid'])

            mm_id=data['data']['mm_aid']
            category=category
            sub_category=sub_category

            for i in dept_label:
                print("i",i,"data",data)
                #chek dept is available
                third_party_api_url = getAPIURL()+'checkMetricDept/'
                data = {
                    'mm_aid':mm_id,
                    'dept_label':dept_label,
                    'category':category,
                    'added_by_field':added_by,
                    'sub_category':sub_category
                }
                header = {
                "Content-Type":"application/json",
                'Authorization': 'Token '+request.session['accessToken']
                }
                response_dept = requests.get(third_party_api_url, data= json.dumps(data),headers=header)
                print("Metric dept data------------",response_dept.content)
                ###
                print('data2',data)
                
                dept_data = json.loads(response_dept.content)
                print("qwer------------------",dept_data)
                return JsonResponse({"msg":"Model Metric Updated Successfully"}) 
                # if len(dept_data['data']) == 0:
                #     third_party_api_url = getAPIURL()+'savemodeldepartment/'
                #     data_to_update = {
                #         'mm_aid':data['mm_aid'],
                #         'dept_aid':i,
                #         'added_by_field':added_by
                #     }
                #     header = {
                #     "Content-Type":"application/json",
                #     'Authorization': 'Token '+request.session['accessToken']
                #     }
                #     response = requests.post(third_party_api_url, data= json.dumps(data_to_update),headers=header)
                #     resp_data=json.loads(response.content)
                #     print("final data---------------",resp_data)
                #     return JsonResponse({"msg":"model Metric Updated Successfully"})                    
                # else:
                #     return JsonResponse({'msg':'Metric Dept Already Created'})        
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def addBusinessMetrics(request):
    try: 
        #new
        third_party_api_url = getAPIURL()+'department/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        ##category
        third_party_api_url = getAPIURL()+'category_master/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response_cat = requests.get(third_party_api_url, headers=header)
        print("response category_master",response_cat.content) 
        return render(request, 'addBusinessMetrics.html',{ 'actPage':'Departments','users':json.loads(response.content),'category':json.loads(response_cat.content)})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())


def savebusinessmetrics(request):
    print("savebusinessmetrics",request.POST)
   
    try:
       
        added_by=request.session['uid']
        metric = request.POST.get('metric','False')
        dept_label = request.POST.getlist('depart_id[]')
        desc = request.POST.get('desc','False')
        activests = request.POST.get('activests','False')
        isglobal = request.POST.get('isglobal','False')
        update_id = request.POST.get('update_id','False')
        category = request.POST.get('cat','False')
        sub_category = request.POST.get('sub_cat','False')

        print("update id",update_id)
        print("Metric data",metric,dept_label,desc,activests,isglobal)
        if update_id=='False':
            print("add")
            third_party_api_url = getAPIURL()+'savebusinessmetrics/'
            data_to_save = {
                'bm_label':metric,
                'bm_description':desc,
                'bm_status':activests,
                'bm_is_global':isglobal,
                'added_by':added_by,
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
            data=json.loads(response.content)
            print("data",data)
        
            bm_aid=data['data']['bm_aid']
            print("bm_aid",bm_aid)
            for i in dept_label:
                print("i",i)
                third_party_api_url = getAPIURL()+'savebusinessdepartment/'
                data_to_save = {
                    'bm_aid':bm_aid,
                    'dept_aid':i,
                    'added_by_field':added_by,
                    'category_aid':category,
                    'sub_category_aid':sub_category
                }
                header = {
                "Content-Type":"application/json",
               'Authorization': 'Token '+request.session['accessToken']
                }
                response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
                data=json.loads(response.content)
                print("data",data)

            return JsonResponse(data)
        else:
            print("update one")
            third_party_api_url = getAPIURL()+'savebusinessmetrics/'
            data_to_save = {
                'id':update_id,
                'bm_label':metric,
                'bm_description':desc,
                'bm_status':activests,
                'bm_is_global':isglobal,
                'added_by':added_by,
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.put(third_party_api_url, data= json.dumps(data_to_save),headers=header)
            data=json.loads(response.content)
            print("data",data)
            print("data",data['data']['bm_aid'])
            bm_id=data['data']['bm_aid']
            category=category
            sub_category=sub_category
                
            #chek dept is available
            third_party_api_url = getAPIURL()+'checkBusinessDept/'
            data = {
                'bm_aid':bm_id,
                'dept_label':dept_label,
                'added_by_field':added_by,
                'category':category,
                'sub_category':sub_category
            }
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response_dept = requests.get(third_party_api_url, data= json.dumps(data),headers=header)
            print("Business dept data------------",response_dept.content)
            ###
            print('data2',data)
            
            dept_data = json.loads(response_dept.content)
            return JsonResponse({"msg":"Business Metric Updated Successfully"})
            # print("qwer------------------",dept_data['data'])

                # if len(dept_data['data']) == 0:
                #     third_party_api_url = getAPIURL()+'savebusinessdepartment/'
                #     data_to_update = {
                #         'bm_aid':data['bm_aid'],
                #         'dept_aid':i,
                #         'added_by_field':added_by,
                #         'model_category':category,
                #         'model_sub_category':sub_category
                #     }
                #     header = {
                #     "Content-Type":"application/json",
                #     'Authorization': 'Token '+request.session['accessToken']
                #     }
                #     response = requests.post(third_party_api_url, data= json.dumps(data_to_update),headers=header)
                #     resp_data=json.loads(response.content)
                #     print("final data---------------",resp_data)
                #     return JsonResponse({"msg":"Business Metric Updated Successfully"})                    
                # else:
                #     return JsonResponse({'msg':'Business Dept Already Created'})        
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def showbusinessmetrics(request):
    try:  
        third_party_api_url = getAPIURL()+'AddBusinessMetrics/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("Business Metrics data response------------------------------------",response.content)
        # funobj = TaskFunctionMaster.objects.all()
        print("showbusinessmetrics",response.content)
        return render(request, 'showbusinessmetrics.html',{'actPage' :'RMSE - Frequency Function','bm_data':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())

def edit_BusinessMetricsMaster(request,id):
    print("edit_BusinessMetricsMaster",id)
    try: 
        third_party_api_url = getAPIURL()+'editbusinessmetrics/'+id
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response ------business Metrics------",response.content)
        
        business_metric_data = json.loads(response.content)
        bm_aid = business_metric_data['data']['bm_aid']
        bm_label = business_metric_data['data']['bm_label']
        bm_description = business_metric_data['data']['bm_description']
        bm_status= business_metric_data['data']['bm_status']
        bm_is_global= business_metric_data['data']['bm_is_global']
        print("bm_status",bm_status)
        print("bm_status",type(bm_status))
        # bm_status = 1
        # bm_is_global = 1
        departments = business_metric_data['data']['departments']
        dept_list = business_metric_data['data']['departments_list']
        print("department",departments)
        #department
        third_party_api_url = getAPIURL()+'department/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response_dept = requests.get(third_party_api_url, headers=header)
        ##get Business metric
        third_party_api_url = getAPIURL()+'get_business_cat_subcat/'
        data_to_save = {'bm_aid':bm_aid}
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response_cat_subcat = requests.get(third_party_api_url,params=data_to_save, headers=header)
        print("response ------business Metrics------",response_cat_subcat.content)
        response_cat=json.loads(response_cat_subcat.content)
        print("response_cat",type(response_cat))
        category_label=response_cat['category_label']
        sub_category_label=response_cat['sub_category_label']
        return render(request, 'addBusinessMetrics.html',{'bm_aid':bm_aid,'bm_label':bm_label,'bm_description':bm_description,
            'bm_status':bm_status,'bm_is_global':bm_is_global,'departments':departments,
            'users':json.loads(response_dept.content),'dept_list':dept_list,
            'category_label':category_label,'sub_category_label':sub_category_label})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc()) 




def ICQFetchResidualRating(request): 
    inherendRisk =request.GET.get('inherendRisk', 'False')
    controleffect =request.GET.get('controleffect', 'False')
    api_url=getAPIURL()+"ICQFetchResidualRating/"       
    data_to_get={
        'inherendRisk':inherendRisk,             
        'controleffect':controleffect } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(data_to_get),headers=header)
    
    api_data=response.json()
    print("Apii daata",api_data)

    return JsonResponse(api_data)

def task_approver_data(request):
    
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
    # task_approval_master=TaskApprovalstatusMaster.objects.all()
    # task_relevant_obj=Task_Relevant_Personnel.objects.filter(u_id=U_id,u_type="Approver")
    context={"task_relevant_obj":api_data['task_relevant_obj'],'task_approval_master':api_data['task_approval_master'],'taskid':taskid}
    return render(request,'task_approver_data.html',context)


def issue_approver_data(request): 
    issueid =request.GET.get('id', 'False') 
    api_url=getAPIURL()+"issue_approver/"       
    api_para={  
        'uid':request.session['uid'], 
        'id':issueid} 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(api_para),headers=header)
        
    api_data=response.json()
    print("api_data",api_data)
    context={"issue_relevant_obj":api_data['issue_relevant_obj'],'issueid':api_data['issueid']}
    return render(request,'issue_approver_data.html',context)


import pandas as pd
# import pdfkit
import os


import pandas as pd
from fpdf import FPDF
import os
from django.conf import settings  # ONLY if you're using Django


from fpdf import FPDF


# def exportDataPDF(pdf, df):
#     pdf.set_font("Arial", 'B', 10)

#     # Step 1: Calculate individual column widths
#     col_widths = []
#     for col in df.columns:
#         max_width = pdf.get_string_width(str(col)) + 4  # Padding
#         for item in df[col]:
#             max_width = max(max_width, pdf.get_string_width(str(item)) + 4)
#         col_widths.append(max_width)

#     # Step 2: Calculate total table width
#     total_table_width = sum(col_widths)
#     page_width = pdf.w - pdf.l_margin - pdf.r_margin
#     left_padding = pdf.l_margin + (page_width - total_table_width) / 2

#     # Step 3: Print header
#     pdf.set_x(left_padding)
#     for i, col in enumerate(df.columns):
#         pdf.cell(col_widths[i], 10, str(col), border=1)
#     pdf.ln()

#     # Step 4: Print data rows
#     pdf.set_font("Arial", size=10)
#     for _, row in df.iterrows():
#         pdf.set_x(left_padding)
#         for i, item in enumerate(row):
#             pdf.cell(col_widths[i], 10, str(item), border=1)
#         pdf.ln()

#     return pdf

# def exportDataPDF(pdf, df):
#     pdf.set_font("Arial", 'B', 10)

#     # Step 1: Calculate individual column widths
#     col_widths = []
#     for col in df.columns:
#         max_width = pdf.get_string_width(str(col)) + 4  # Padding
#         for item in df[col]:
#             max_width = max(max_width, pdf.get_string_width(str(item)) + 4)
#         col_widths.append(max_width)

#     # Step 2: Calculate total table width
#     total_table_width = sum(col_widths)
#     page_width = pdf.w - pdf.l_margin - pdf.r_margin
#     left_padding = pdf.l_margin + (page_width - total_table_width) / 2

#     # Step 3: Print header
#     pdf.set_x(left_padding)
#     for i, col in enumerate(df.columns):
#         pdf.cell(col_widths[i], 10, str(col), border=1)
#     pdf.ln()

#     # Step 4: Print data rows
#     pdf.set_font("Arial", size=10)

#     for _, row in df.iterrows():
#         pdf.set_x(left_padding)

#         # Determine the height of the row by checking how many lines primary name will need
#         primary_index = list(df.columns).index('primary name')
#         primary_text = str(row[primary_index])
#         line_height = 5
#         num_lines = len(pdf.multi_cell(col_widths[primary_index], line_height, primary_text, border=0, align='L', split_only=True))
#         row_height = num_lines * line_height

#         y_start = pdf.get_y()
#         x_start = left_padding

#         for i, item in enumerate(row):
#             pdf.set_xy(x_start, y_start)
#             if i == primary_index:
#                 pdf.multi_cell(col_widths[i], line_height, str(item), border=1)
#             else:
#                 pdf.cell(col_widths[i], row_height, str(item), border=1)
#             x_start += col_widths[i]

#         pdf.set_y(y_start + row_height)

#     return pdf

# def df_to_pdf(request):
#     columns = [
#         'model id', 'findings id', 'primary name',
#         'Findings Severity', 'Model risk', 'Validation element', 'validation category'
#     ]
#     data = [
#         [1, 101, 'The quick brown fox jumps over the lazy dog near the riverbank', 'Medium', 'Medium',
#         'Conceptual and Developmental Soundness', 'Performance Monitoring'],
#         [2, 102, 'Artificial intelligence is transforming the way we live and work every day.', 'Low', 'Low',
#         'Inputs And Data', 'Stress Testing and Back Testing'],
#         [3, 103, 'Model C', 'High', 'High',
#         'Ongoing Monitoring, including Process Verification', 'Model Calculations'],
#         [4, 104, 'Model D', 'Medium', 'Medium',
#         'Outcomes Analysis and Back-testing', 'Coding'],
#         [5, 105, 'Model E', 'Low', 'Low',
#         'Conceptual and Developmental Soundness', 'Reporting']
#     ]


#     df = pd.DataFrame(data, columns=columns)
#     print("df",df)
    
#     file_path = os.path.join(BASE_DIR, 'static', 'df_to_csv')
#     os.makedirs(file_path, exist_ok=True)
#     savefile_name = os.path.join(file_path, 'df_output.csv')
#     df.to_csv(savefile_name, index=False)
#     print("CSV saved to:", savefile_name)
    
#     df = pd.read_csv(savefile_name)

#     # Create PDF in landscape mode
#     pdf = FPDF(orientation='L', format='A4')
#     pdf.add_page()
#     pdf.set_font("Arial", 'B', 12)
#     pdf.cell(0, 10, ln=True, align='C')
#     pdf.ln(5)

#     pdf = exportDataPDF(pdf, df)

#     # Save PDF
#     output_path = os.path.join(BASE_DIR, "static", "df_to_pdf", "DF_PDF.pdf")
#     os.makedirs(os.path.dirname(output_path), exist_ok=True)
#     pdf.output(output_path)

#     print(f"PDF saved to: {output_path}")
#     return HttpResponse(f"PDF saved to: {output_path}")


def exportDataPDF(pdf, df):
    pdf.set_font("Arial", 'B', 10)
    line_height = 5
    max_col_width = 60

    
    col_widths = []
    for col in df.columns:
        max_w = pdf.get_string_width(str(col)) + 4
        for val in df[col]:
            val_str = str(val)
            lines = pdf.multi_cell(max_col_width, line_height, val_str, split_only=True)
            line_w = max(pdf.get_string_width(line) for line in lines) + 4
            max_w = max(max_w, line_w)
        col_widths.append(min(max_w, max_col_width))

    table_width = sum(col_widths)
    start_x = pdf.l_margin + (pdf.w - pdf.l_margin - pdf.r_margin - table_width) / 2

    # Draw header
    pdf.set_x(start_x)
    for i, col in enumerate(df.columns):
        pdf.cell(col_widths[i], 10, str(col), border=1, align='C')
    pdf.ln()

    pdf.set_font("Arial", size=10)

    
    for _, row in df.iterrows():
        x_start = start_x
        y_start = pdf.get_y()
        max_lines = 1
        line_data = []

        # First pass: calculate lines and max_lines
        for i, col in enumerate(df.columns):
            text = str(row[col])
            col_width = col_widths[i]
            lines = pdf.multi_cell(col_width, line_height, text, border=0, split_only=True)
            line_data.append(lines)
            max_lines = max(max_lines, len(lines))

        row_height = max_lines * line_height

        # Second pass: render all cells in the row
        for i, lines in enumerate(line_data):
            pdf.set_xy(x_start, y_start)
            col_width = col_widths[i]

            for j in range(max_lines):
                if j < len(lines):
                    pdf.cell(col_width, line_height, lines[j], ln=0)
                else:
                    pdf.cell(col_width, line_height, '', ln=0)
                pdf.set_xy(x_start, y_start + (j + 1) * line_height)

            pdf.rect(x_start, y_start, col_width, row_height)
            x_start += col_width

        pdf.set_y(y_start + row_height)

    return pdf

def df_to_pdf(request):
    columns = [
        'model id', 'findings id', 'primary name',
        'Findings Severity', 'Model risk', 'Validation element', 'validation category'
    ]
    data = [
        [1, 101, 'The quick brown fox jumps over the lazy dog near the riverbank', 'Medium', 'Medium',
         'Conceptual and Developmental Soundness', 'Performance Monitoring'],
        [2, 102, 'Artificial intelligence is transforming the way we live and work every day.', 'Low', 'Low',
         'Inputs And Data', 'Stress Testing and Back Testing'],
        [3, 103, 'Model C', 'High', 'High',
         'Ongoing Monitoring, including Process Verification', 'Model Calculations'],
        [4, 104, 'Model D', 'Medium', 'Medium',
         'Outcomes Analysis and Back-testing', 'Coding'],
        [5, 105, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit', 'Low', 'Low',
         'Conceptual and Developmental Soundness', 'Reporting']
    ]

    df = pd.DataFrame(data, columns=columns)

    # Save as CSV
    csv_dir = os.path.join(BASE_DIR, 'static', 'df_to_csv')
    os.makedirs(csv_dir, exist_ok=True)
    csv_path = os.path.join(csv_dir, 'df_output.csv')
    df.to_csv(csv_path, index=False)

    # Reload just in case
    df = pd.read_csv(csv_path)

    # Create PDF (landscape A4)
    pdf = FPDF(orientation='L', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10,"Validation Findings", ln=True, align='C')
    pdf.ln(5)

    pdf = exportDataPDF(pdf, df)

    # Save PDF
    pdf_path = os.path.join(BASE_DIR, "static", "df_to_pdf", "DF_PDF.pdf")
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    pdf.output(pdf_path)

    return HttpResponse(f" PDF saved to: {pdf_path}")

def model_committee(request):
    try: 
        if request.method == "POST":
            members = json.loads(request.POST.get("members", "{}"))

            api_url=getAPIURL()+"model_committee/"    
            api_para={  
                'members':members,
                'uid':request.session['uid']
                } 
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(api_url,data= json.dumps(api_para),headers=header)
                
            api_data_mgc=response.json()
            print("api_data_mgc",api_data_mgc)
        

        api_url=getAPIURL()+"model_committee/"    
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url,headers=header)
            
        api_data_get=response.json()
        print("api_data_get",api_data_get)

        
        api_url=getAPIURL()+"model_committee/"    
        api_para={  
        'uid':request.session['uid']
        } 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(api_para),headers=header)
            
        api_data=response.json()
        print("api_data",api_data)
        return render(request, 'model_committee.html',context={'department_head':api_data,
                                                               'selected_user_ids':api_data_get})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())