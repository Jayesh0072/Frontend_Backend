from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import Users,UserCategory,TaskRegistration,Task_Relevant_Personnel,TaskSummery,Alert,IssueRegistration,IssueRelevantPersonnel
from .serializers import *
from rest_framework.views import APIView
from rest_framework import generics, permissions, status,serializers
import environ
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
password = 'sqlAdm_18'
host = 'DESKTOP-NH98228\HCSPL18'
port = 1433
database = 'RMSE'

# mongodb set up
cluster=MongoClient('localhost',27017,connect=False)
db=cluster["validation_tool"]
collection=db["SrcData"]
collection_file_info=db["SrcFileInfo"]
collection_process_status=db["ProcessStatus"]

collection_model_target_value=db['TargetValue']
collection_da_src_file_Info=db['DASrcFileInfo']
collection_da_src_data=db['DASrcData']
collection_confirm_data_source=db['DataSource']

collection_conceptual_soundness=db['ConceptualSoundness']
collection_model_implementation_control=db['ImplementationControls']
collection_model_usage=db['ModelUsage']
collection_validation_findings=db['ValidationFindings']


from .RegModel.registermodel import RegisterModel as Register
from .RegModel.registermodel import MdlOverviewCls,ModelRisks,MdlRelevantPersonnelFuncs,MdlDependenciesCls,MdlPerformanceMonitoring,MdlDocs,UserDeatilsSerializers
# from .RegModel.registermodel import MdlRelevantPersonnel as MdlRelevantPersonnel_cls

from .Adm_Utils.Masters import MasterTbls
from .DAL.dboperations import dbops
from .models import *
from .UserInfo.user import UserInfo
from .Validation.validation import Validation
from .RMSE.RMSE import RMSEModel
from django.db.models import Max

objreg=Register()  
objmaster=MasterTbls()
objvalidation=Validation()
objdbops=dbops()
objrmse=RMSEModel()
from rest_framework.permissions import IsAuthenticated
#comment
import matplotlib.pyplot as plt
plot_dir_view='static/media/'
from fpdf import FPDF, HTMLMixin 
import base64
from io import BytesIO

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication 
import PIL.Image
import pandas as pd
import numpy as np
np.object = object 
collection_chart_viewed=db['ChartViewed']
# end comment  
# PYTHON FUNCTION TO CONNECT TO THE MYSQL DATABASE AND
# RETURN THE SQLACHEMY ENGINE OBJECT

# engine=sa.create_engine(
#         url="mssql+pyodbc://{0}:{1}@{2}/{3}?driver=SQL+Server+Native+Client+11.0".format(
#             user, password, host,  database
#         ))
# engine = sa.create_engine("mssql+pyodbc://sa:sqlAdm@18@HOST_IP:PORT/DATABASENAME?driver=SQL+Server+Native+Client+11.0")
def blank(request):
    try:          
        objreg=Register()
        
        dttbl=objreg.getUserDeatils(request.session['utype'],request.session['dept'])
       
        if dttbl.empty == False:
            request.session['li_mrm']=dttbl[dttbl['r_label'] == 'Model Risk Management'].values[0][2]
            request.session['li_qv']=dttbl[dttbl['r_label'] =='Quick View'].values[0][2]
            request.session['li_cr']=dttbl[dttbl['r_label'] =='Create Report'].values[0][2]
            request.session['li_modinv']=dttbl[dttbl['r_label'] =='Model Inventory'].values[0][2]
            # request.session['li_modtodo']=dttbl[dttbl['r_label'] =='Upcoming'].values[0][2]
            request.session['li_modtasks']=dttbl[dttbl['r_label'] =='Tasks'].values[0][2]
            # request.session['li_idmod']=dttbl[dttbl['r_label'] =='Identify New Model'].values[0][2]
            request.session['li_reqval']=dttbl[dttbl['r_label'] =='Request a Model Validation'].values[0][2]
            # request.session['li_subdoc']=dttbl[dttbl['r_label'] =='Submit Documentation/ Evidence'].values[0][2]
            # request.session['li_reqcng']=dttbl[dttbl['r_label'] =='Request a Change'].values[0][2]
            # request.session['li_updoc']=dttbl[dttbl['r_label'] =='Upload Document'].values[0][2]
            # request.session['li_upcod']=dttbl[dttbl['r_label'] =='Upload Code'].values[0][2]
            # request.session['li_upcod']=dttbl[dttbl['r_label'] =='Upload Code'].values[0][2]
            request.session['li_adduser']=dttbl[dttbl['r_label'] =='Dept Head'].values[0][2]
            request.session['li_vmtool']=dttbl[dttbl['r_label'] =='Validation Tool'].values[0][2]
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
        return render(request, 'blank.html',{'actPage':'RMSE',
                                             'notifylen':str(len(objvalidation.getVTNotifications(request.session['uid'])))})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 

def blankadmin(request):
    try:          
        objreg=Register()
        dttbl=objreg.getUserDeatils(request.session['utype'],'0') 
        if dttbl.empty == False:
            request.session['li_mrm']=dttbl[dttbl['r_label'] == 'Model Risk Management'].values[0][2]
            request.session['li_qv']=dttbl[dttbl['r_label'] =='Quick View'].values[0][2]
            # request.session['li_cr']=dttbl[dttbl['r_label'] =='Create Report'].values[0][2]
            request.session['li_modinv']=dttbl[dttbl['r_label'] =='Model Inventory'].values[0][2]
            # request.session['li_modtodo']=dttbl[dttbl['r_label'] =='Upcoming'].values[0][2]
            request.session['li_modtasks']=dttbl[dttbl['r_label'] =='Tasks'].values[0][2]
            # request.session['li_idmod']=dttbl[dttbl['r_label'] =='Identify New Model'].values[0][2]
            # request.session['li_reqval']=dttbl[dttbl['r_label'] =='Request a Model Validation'].values[0][2]
            # request.session['li_subdoc']=dttbl[dttbl['r_label'] =='Submit Documentation/ Evidence'].values[0][2]
            # request.session['li_reqcng']=dttbl[dttbl['r_label'] =='Request a Change'].values[0][2]
            # request.session['li_updoc']=dttbl[dttbl['r_label'] =='Upload Document'].values[0][2]
            # request.session['li_upcod']=dttbl[dttbl['r_label'] =='Upload Code'].values[0][2]
        del dttbl
        return render(request, 'blankadmin.html',{'actPage':'RMSE'})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 


def blankvalidationtool(request):
    try:      
        return render(request, 'blankvalidationtool.html')
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 

def login(request):
    try: 
        return render(request, 'login.html')
    except Exception as e:
        print('login is ',e)
        print('login traceback is ', traceback.print_exc()) 

def user(request):
    try:        
        tableResult = objmaster.getdbUsers()
        users = tableResult.to_json(orient='index')
        users = json.loads(users)
        print("users",users)
        del tableResult       
        return render(request, 'userlist.html',{ 'actPage':'Add User','users':users})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())


def addnewuser(request):
    try:  
        tableResult =objdbops.getTable("SELECT   UC_AID  ,UC_Label  FROM User_Category where UC_Label <> 'Admin'  order by 2 ")
        users = tableResult.to_json(orient='index')
        users = json.loads(users)
        del tableResult

        

        tableResult =objdbops.getTable("SELECT Dept_AID,Dept_Label FROM Department") 
        dept = tableResult.to_json(orient='index')
        dept = json.loads(dept)
        del tableResult
        return render(request, 'adduser.html',{ 'actPage':'Add User','utype':users,'dept':dept})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc()) 

# def addUser(request):
#     try:
#         update_date=datetime.now()
#         updated_by=request.session['uid']
#         uname =request.GET.get('uname', 'False') 
#         user_type =request.GET.get('utype', 'False')  
#         lname=request.GET.get('lname', 'False')   
#         fname=request.GET.get('fname', 'False')     
#         email=request.GET.get('email', 'False')   
#         reportsto=request.GET.get('reportsto', 'False')   
#         dept_aid=request.GET.get('dept_aid', 'False')   
#         activests=request.GET.get('activests', 'False')
#         update_id=request.GET.get('update_id')
#         print("update_id",update_id)
#         print("utype",user_type)
#         print("reportsto",reportsto)
#         # print("utype",utype.uc_aid)

#         # u_type_id=user_obj.uc_aid
#         # print("u_type_id",u_type_id.uc_aid)
#         # u_type=UserCategory.objects.get(uc_aid=u_type_id.uc_aid).uc_label

#         utype_id=UserCategory.objects.get(uc_aid=user_type)
      
#         if update_id: 
#             user_obj=Users.objects.get(u_aid=update_id)
#             user_obj.u_name=uname
#             user_obj.uc_aid=utype_id
#             user_obj.u_fname=fname
#             user_obj.u_lname=lname
#             user_obj.u_email=email
#             user_obj.dept_aid=dept_aid
#             user_obj.activestatus=activests
#             user_obj.updatedby=updated_by
#             user_obj.updatedate=update_date
#             user_obj.u_reportto=reportsto
#             user_obj.save()
#             return JsonResponse({"isvalid":"update"})
#         else:
#             print("insert")
#             strQ="INSERT INTO Users (U_Name ,U_Password ,U_Email ,U_FName ,U_LName  ,U_ProfilePic  ,UC_AID  ,U_Description ,ActiveStatus,AddedBy ,AddDate,Dept_AID,U_reportto) "
#             strQ += " VALUES  ('"+ uname+"','"+ uname+"','"+ email+"','"+ fname+"','"+ lname+"',null,'"+ user_type+"',null,'"+ activests+"', '"+str(request.session['uid'])+"',getdate(),"+ dept_aid +","+ reportsto +")"
#             print('strQ is',strQ)
#             objdbops.insertRow(strQ)
#             return JsonResponse({"isvalid":"true"})
#     except Exception as e:
#         print('setuppycaret is ',e)
#         print('setuppycaret traceback is ', traceback.print_exc()) 
#         JsonResponse({"isvalid":"false"})

# def addUser(request):
#     try:
#         update_date=datetime.now()
#         updated_by=request.session['uid']
#         uname =request.GET.get('uname', 'False') 
#         utype =request.GET.get('utype', 'False')  
#         lname=request.GET.get('lname', 'False')   
#         fname=request.GET.get('fname', 'False')     
#         email=request.GET.get('email', 'False')   
#         reportsto=request.GET.get('reportsto','False')   
#         dept_aid=request.GET.get('dept_aid', 'False')   
#         activests=request.GET.get('activests', 'False')
#         update_id=request.GET.get('update_id')
#         print("update_id",update_id)
#         print("utype",type(utype))
#         print("utype",utype)
#         print("reportsto",reportsto)
#         print("dept_aid",dept_aid)
#         # print("utype",utype.uc_aid)
#         # if reportsto == None:
#         #     reportsto=
#         # if reportsto and reportsto =='null':
#         #     reportsto=reportsto
#         # else:
#         #     reportsto=None
#         # print("reportsto",reportsto)    
#         # u_type_id=user_obj.uc_aid
#         # print("u_type_id",u_type_id.uc_aid)
#         # u_type=UserCategory.objects.get(uc_aid=u_type_id.uc_aid).uc_label

#         utype_id=UserCategory.objects.get(uc_aid=int(utype))
#         print("utype_id",utype_id)
#         if update_id:
#             if reportsto =='null' or reportsto =='':
#                 reportsto=None
#             print("update",update_id)
#             user_obj=Users.objects.get(u_aid=update_id)
#             if dept_aid == 'null' or dept_aid == "":
#                 dept_aid=None
#             user_obj.u_name=uname
#             user_obj.uc_aid=utype_id
#             user_obj.u_fname=fname
#             user_obj.u_lname=lname
#             user_obj.u_email=email
#             user_obj.dept_aid=dept_aid
#             user_obj.activestatus=activests
#             user_obj.updatedby=updated_by
#             user_obj.updatedate=update_date
#             user_obj.u_reportto=reportsto
#             user_obj.save()
#             return JsonResponse({"isvalid":"update"})
#         else:
#             print("insert")
#             strQ="INSERT INTO Users (U_Name ,U_Password ,U_Email ,U_FName ,U_LName  ,U_ProfilePic  ,UC_AID  ,U_Description ,ActiveStatus,AddedBy ,AddDate,Dept_AID,U_reportto) "
#             strQ += " VALUES  ('"+ uname.replace("'","''")+"','"+ uname.replace("'","''")+"','"+ email.replace("'","''")+"','"+ fname.replace("'","''")+"','"+ lname.replace("'","''")+"',null,'"+ utype.replace("'","''")+"',null,'"+ activests.replace("'","''")+"', '"+str(request.session['uid']).replace("'","''")+"',getdate(),"+ dept_aid.replace("'","''") +","+ reportsto.replace("'","''") +")"
#             print('strQ is',strQ)
#             objdbops.insertRow(strQ)
#             # user_obj=Users(u_name=uname,u_password=uname,u_email=email,)
#             return JsonResponse({"isvalid":"true"})
#     except Exception as e:
#         print('setuppycaret is ',e)
#         print('setuppycaret traceback is ', traceback.print_exc()) 
#         JsonResponse({"isvalid":"false"})

from django.contrib.auth.hashers import make_password,check_password
class addNewUser(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            print("request_data check user",request.data)
            custom_salt = "mysalt123"
            update_date=datetime.now()
            updated_by=request.data['updated_by']
            uname =request.data['u_name']  
            upass  = make_password(request.data['u_name'],custom_salt )
            utype =request.data['utype']  
            lname=request.data['u_lname']  
            fname=request.data['u_fname']    
            email=request.data['u_email']   
            reportsto=request.data['u_reportto']  
            dept_aid=request.data['dept_aid'] 
            activests=request.data['activestatus']
            update_id=request.data['update_id']
            print("update_id",update_id)
            print("utype",type(utype))
            print("utype",utype)
            print("reportsto",reportsto)
            print("dept_aid",dept_aid)
            # print("utype",utype.uc_aid)
            # if reportsto == None:
            #     reportsto=
            # if reportsto and reportsto =='null':
            #     reportsto=reportsto
            # else:
            #     reportsto=None
            # print("reportsto",reportsto)    
            # u_type_id=user_obj.uc_aid
            # print("u_type_id",u_type_id.uc_aid)
            # u_type=UserCategory.objects.get(uc_aid=u_type_id.uc_aid).uc_label

            utype_id=UserCategory.objects.get(uc_aid=int(utype))
            print("utype_id",utype_id)
            if update_id != None:
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
                user_obj.save()
                return JsonResponse({"isvalid":"update"})
            else:
                print("insert user")
                strQ="INSERT INTO Users (U_Name ,U_Password ,U_Email ,U_FName ,U_LName  ,U_ProfilePic  ,UC_AID  ,U_Description ,ActiveStatus,AddedBy ,AddDate,Dept_AID,U_reportto) "
                strQ += " VALUES  ('"+ uname.replace("'","''")+"','"+ upass.replace("'","''")+"','"+ email.replace("'","''")+"','"+ fname.replace("'","''")+"','"+ lname.replace("'","''")+"',null,'"+ utype.replace("'","''")+"',null,'"+ activests.replace("'","''")+"', '"+str(request.data['addedby']).replace("'","''")+"',getdate(),"+ dept_aid.replace("'","''") +","+ reportsto.replace("'","''") +")"
                print('strQ is',strQ)
                objdbops.insertRow(strQ)
                # user_obj=Users(u_name=uname,u_password=uname,u_email=email,)
                return JsonResponse({"isvalid":"true"})
        except Exception as e:
            print('setuppycaret is ',e)
            print('setuppycaret traceback is ', traceback.print_exc()) 
            JsonResponse({"isvalid":"false"})


class ResetPassword(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            print("request_data check user",request.data)
            custom_salt = "mysalt123"
            uname =request.data['u_name'] 
            upass  = make_password(request.data['u_password'], custom_salt)  
            update_id=request.data['update_id']
            print("update_id",update_id)            
            print("update",update_id) 
            user_obj=Users.objects.filter(u_aid=update_id,u_name=uname).update(u_password = upass)
            return JsonResponse({"isvalid":"true"})
            
        except Exception as e:
            print('setuppycaret is ',e)
            print('setuppycaret traceback is ', traceback.print_exc()) 
            JsonResponse({"isvalid":"false"})

class check_current_password(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            custom_salt = "mysalt123"
            print("request_data check user",request.data)
            uname =request.data['u_name'] 
            upass  = make_password(request.data['u_password'],custom_salt)  
            update_id=request.data['update_id'] 
            user_obj=Users.objects.filter(u_aid=update_id,u_name=uname,u_password = upass)
            print('user_obj ',user_obj)
            if user_obj:
                return JsonResponse({"isvalid":"true"})
            else:
                return JsonResponse({"isvalid":"false"})
            
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


def validateUser(request): 
    try:        
        uname =request.GET.get('uname', 'False') 
        pwd =request.GET.get('pwd', 'False')  
        isvalid='false'
        utype=''
        objuser=UserInfo() 
        dffilter=objuser.validateUser(uname,pwd)
        if dffilter.empty==True:
            isvalid='false'
        else:
            isvalid='true'
            request.session['username'] = uname
            request.session['utype']=dffilter["UC_AID"].values[0]
            utype=dffilter["UC_AID"].values[0]
            if dffilter["Dept_AID"].values[0] == None:
                request.session['dept']=0
            else:
                request.session['dept']=dffilter["Dept_AID"].values[0]
            request.session['uid']=dffilter["U_AID"].values[0]
            request.session['ucaid']=dffilter["UC_AID"].values[0]
            request.session['ulvl']=dffilter["UC_Level"].values[0]
            request.session['profileimg']=  "/static/phoenix-v1.8.0/public/assets/img/team/avatar-rounded.png"
            # print('utype is ',dffilter["U_profilepic"].values[0],", ",  "/static/phoenix-v1.8.0/public/assets/img/team/"+  dffilter["profileimg"].values[0])
        return JsonResponse({'isvalid':isvalid,'utype':str(utype)})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc())

# class Dashboard(APIView): 
#     permission_classes=[IsAuthenticated] 
#     def post(self,request):
#         try: 
#             objreg=Register() 
#             dttbl=objreg.getUserDeatils(request.data['utype'],request.data['dept'])          
            
#             modelinfo=objreg.getModelListByUSerid(request.data['uid'],str(request.data['ulvl']),'0')
#             modelriskcnt=objreg.getModelRiskCntByUserid(request.data['uid'],str(request.data['ulvl'])) 
#             modelsrccnt=objreg.getModelSrcCntByUserid('0',request.data['uid'])
#             validationrating=objreg.getModelValidationRatingCntByUserid(request.data['uid'])
#             taskList,taskcnt=objreg.getTaskListByUSerid(request.data['uid'])
#             issueList=objreg.getIssueListByUserId(request.data['uid'])
#             issuesByQtrOrMonth=objreg.getIssuesByMonthOrQtr(request.data['type'],request.data['uid'],request.data['is_mrm'],request.data['issue_from_dt'],request.data['issue_to_dt'])
#             icqratings=objreg.isICQPublished() 
#             findingsByElements=objreg.getFindingsCntByElements()
#             findingsCntByCategory=objreg.getFindingsCntByCategory()
#             findingsByUpstreamMdl=objreg.getFindingsCntByUpstreamMdls(request.data['uid'])
#             findingsCntByMdls=objreg.getFindingsCntByMdls(request.data['uid'])
#             if(icqratings=='-'):
#                 icq_exp="Experimentation"
#                 icqratings="0"
#             else:
#                 icq_exp="Program Score"
#             srcCnt=[]  
            
#             if modelsrccnt.empty:
#                 srcCnt=[]
#             else:
#                 srcCnt= [
#                     {
#                     'value': 0 if modelsrccnt[modelsrccnt['lbl'] == 'Internal'].empty else modelsrccnt[modelsrccnt['lbl'] == 'Internal'].values[0][0],
#                     'itemStyle': {
#                         'color': 'red'
#                     }
#                     }, 
#                     {     
#                     'value': 0 if modelsrccnt[modelsrccnt['lbl'] == 'Legacy'].empty else modelsrccnt[modelsrccnt['lbl'] == 'Legacy'].values[0][0],
#                     'itemStyle': {
#                         'color': 'Yellow'
#                     }
#                     },
#                     {
#                     'value': 0 if modelsrccnt[modelsrccnt['lbl'] == 'Vendor'].empty else modelsrccnt[modelsrccnt['lbl'] == 'Vendor'].values[0][0],
#                     'itemStyle': {
#                         'color': 'Green'
#                     }
#                     }, 
#                 ]

#             colorArr=['#0dcaf0', '#fd7e14','#ffc107','#dc3545','#198754','#0d6efd']
        
#             if modelriskcnt.empty:
#                 cnt=[]
#             else:
#                 cnt= [
#                     {
#                     'value': modelriskcnt[modelriskcnt['lbl'] == 'High'].values[0][1],
#                     'itemStyle': {
#                         'color': '#ee6666'
#                     }
#                     }, 
#                     {
#                     'value': modelriskcnt[modelriskcnt['lbl'] == 'Medium'].values[0][1],
#                     'itemStyle': {
#                         'color': '#fac858'
#                     }
#                     },
#                     {
#                     'value': modelriskcnt[modelriskcnt['lbl'] == 'Low'].values[0][1],
#                     'itemStyle': {
#                         'color': '#91cc75'
#                     }
#                     },
#                     {
#                     'value': modelriskcnt[modelriskcnt['lbl'] == 'None'].values[0][1],
#                     'itemStyle': {
#                         'color': '#800080'
#                     }
#                     },
#                 ]  
            
#             if validationrating.empty:
#                 arrvalrating=[]
#             else:
#                 arrvalrating= [
#                     {
#                     'value': validationrating[validationrating['lbl'] == 'High'].values[0][1],
#                     'itemStyle': {
#                         'color': '#ee6666'
#                     }
#                     }, 
#                     {
#                     'value': validationrating[validationrating['lbl'] == 'Medium'].values[0][1],
#                     'itemStyle': {
#                         'color': '#fac858'
#                     }
#                     },
#                     {
#                     'value': validationrating[validationrating['lbl'] == 'Low'].values[0][1],
#                     'itemStyle': {
#                         'color': '#91cc75'
#                     }
#                     },
#                     {
#                     'value': validationrating[validationrating['lbl'] == 'None'].values[0][1],
#                     'itemStyle': {
#                         'color': '#800080'
#                     }
#                     },
#                 ]  
#             print('arrvalrating ',arrvalrating)
#             return Response({'dttbl':dttbl,'icqratings':icqratings,'icq_exp':icq_exp,'modelinfo':modelinfo,'srcCnt':srcCnt,
#                                                     'colorArr':colorArr,'issueCnt':len(issueList),'issueList':issueList,'arrvalrating':arrvalrating,
#                                                     'taskCnt':taskcnt,'taskLst':taskList,'issuesByQtrOrMonth':issuesByQtrOrMonth,'findingsByElements':findingsByElements,
#                                                     'toolCnt':objreg.getToolCntByUserId(request.data['uid'],str(request.data['ulvl'])) ,
#                                                     'modelttl':str(len(modelinfo)),'mdlRiskCnt':cnt,'findingsCntByCategory':findingsCntByCategory,
#                                                     'modeltypes':objreg.getModelTypeByUserId(request.data['uid'],str(request.data['ulvl'])),
#                                                     'activityData':objreg.getLatestActivity(request.data['uid']) , 'actPage':'Quick View','findingsByUpstreamMdl':findingsByUpstreamMdl,'findingsCntByMdls':findingsCntByMdls},
#                                                     status=status.HTTP_200_OK)
           
#         except Exception as e:
#             print('setuppycaret is ',e)
#             print('setuppycaret traceback is ', traceback.print_exc()) 
#             error_saving(request,e)
#             return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)


class Dashboard(APIView): 
    permission_classes=[IsAuthenticated] 
    def post(self,request):
        try: 
            objreg=Register() 
            dttbl=objreg.getUserDeatils(request.data['utype'],request.data['dept'])          
            
            modelinfo=objreg.getModelListByUSerid(request.data['uid'],str(request.data['ulvl']),'0')
            modelriskcnt=objreg.getModelRiskCntByUserid(request.data['uid'],str(request.data['ulvl'])) 
            modelsrccnt=objreg.getModelSrcCntByUserid('0',request.data['uid'])
            validationrating=objreg.getModelValidationRatingCntByUserid(request.data['uid'])
            taskList,taskcnt=objreg.getTaskListByUSerid(request.data['uid'])
            overdueTasks=objreg.getOverdueTaskListByUSerid(request.data['uid'])
            issueList,issuecnt=objreg.getIssueListByUserId(request.data['uid'])
            overdueIssues=objreg.getOverdueIssueListByUserId(request.data['uid'])
            issuesByQtrOrMonth=objreg.getIssuesByMonthOrQtr(request.data['type'],request.data['uid'],request.data['is_mrm'],request.data['issue_from_dt'],request.data['issue_to_dt'])
            icqratings=objreg.isICQPublished() 
            findingsByElements=objreg.getFindingsCntByElements()
            findingsCntByCategory=objreg.getFindingsCntByCategory()
            valstscnt=objreg.getValStsCntByUserid('0',request.data['uid'])
            mdlstscnt=objreg.getMdlStsCntByUserid('0',request.data['uid']) 
            riskcnts=objreg.getMdlRisksCnt(request.data['uid'],request.data['is_mrm'])
            dashboardSetting=objreg.getDashboardSetting(request.data['uid'])
            findingsByUpstreamMdl=objreg.getFindingsCntByUpstreamMdls(request.data['uid'])
            findingsCntByMdls=objreg.getFindingsCntByMdls(request.data['uid'])
            if(icqratings=='-'):
                icq_exp="Experimentation"
                icqratings="0"
            else:
                icq_exp="Program Score"
            srcCnt=[]  
            
            if modelsrccnt.empty:
                srcCnt=[]
            else:
                srcCnt= [
                    {
                    'value': 0 if modelsrccnt[modelsrccnt['lbl'] == 'Internal'].empty else modelsrccnt[modelsrccnt['lbl'] == 'Internal'].values[0][0],
                    'itemStyle': {
                        'color': 'red'
                    }
                    }, 
                    {
                    'value': 0 if modelsrccnt[modelsrccnt['lbl'] == 'Legacy'].empty else modelsrccnt[modelsrccnt['lbl'] == 'Legacy'].values[0][0],
                    'itemStyle': {
                        'color': 'Yellow'
                    }
                    },
                    {
                    'value': 0 if modelsrccnt[modelsrccnt['lbl'] == 'Vendor'].empty else modelsrccnt[modelsrccnt['lbl'] == 'Vendor'].values[0][0],
                    'itemStyle': {
                        'color': 'Green'
                    }
                    }, 
                ]

            colorArr=['#0dcaf0', '#fd7e14','#ffc107','#dc3545','#198754','#0d6efd']
            
            if modelriskcnt.empty:
                cnt=[]
            else:
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
                        'color': '#800080'
                    }
                    },
                ]   
            if validationrating.empty:
                arrvalrating=[]
            else:
                arrvalrating= [
                    {
                    'value': validationrating[validationrating['lbl'] == 'High'].values[0][1],
                    'itemStyle': {
                        'color': '#ee6666'
                    }
                    }, 
                    {
                    'value': validationrating[validationrating['lbl'] == 'Medium'].values[0][1],
                    'itemStyle': {
                        'color': '#fac858'
                    }
                    },
                    {
                    'value': validationrating[validationrating['lbl'] == 'Low'].values[0][1],
                    'itemStyle': {
                        'color': '#91cc75'
                    }
                    },
                    {
                    'value': validationrating[validationrating['lbl'] == 'None'].values[0][1],
                    'itemStyle': {
                        'color': '#800080'
                    }
                    },
                ]   
            return Response({'dttbl':dttbl,'icqratings':icqratings,'icq_exp':icq_exp,'modelinfo':modelinfo,'srcCnt':srcCnt,
                            'colorArr':colorArr,'issueCnt':len(issueList),'issueList':issueList,'arrvalrating':arrvalrating,
                            'taskCnt':taskcnt,'taskLst':taskList,'issuesByQtrOrMonth':issuesByQtrOrMonth,'findingsByElements':findingsByElements,
                            'toolCnt':objreg.getToolCntByUserId(request.data['uid'],str(request.data['ulvl'])) ,
                            'modelttl':str(len(modelinfo)),'mdlRiskCnt':cnt,'findingsCntByCategory':findingsCntByCategory,
                            'modeltypes':objreg.getModelTypeByUserId(request.data['uid'],str(request.data['ulvl'])),
                            'activityData':objreg.getLatestActivity(request.data['uid']) ,'mdl_cat':objreg.getModelCategoryByUserId(request.data['uid']), 
                            'actPage':'Quick View','overdueTasks':overdueTasks,'overdueIssues':overdueIssues,'valstscnt':valstscnt,
                            'mdlstscnt':mdlstscnt,'riskcnts':riskcnts,'issuecnt':issuecnt,'dashboardSetting':dashboardSetting,
                            'findingsByUpstreamMdl':findingsByUpstreamMdl,'findingsCntByMdls':findingsCntByMdls},
                            status=status.HTTP_200_OK)
           
        except Exception as e:
            print('setuppycaret is ',e)
            print('setuppycaret traceback is ', traceback.print_exc()) 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)


def masterTbls(request):
    try: 
        pagettl='RMSE'
        page =request.GET.get('page', 'False')        
        if page=="1":
            pagettl='RMSE - Add Function'
        elif page=="2":
            pagettl='RMSE - Add Model Source'
        elif page=="3":
            pagettl='RMSE - Add Model Type'
        elif page=="4":
            pagettl='RMSE - Add Products Addressed'
        elif page=="5":
            pagettl='RMSE - Add Usage Frequency'
        elif page=="6":
            pagettl='RMSE - Add Model Risk'
        elif page=="7":
            pagettl='RMSE - Add Intrinsic Risk'
        elif page=="8":
            pagettl='RMSE - Add Reliance'
        elif page=="9":
            pagettl='RMSE - Add Materiality'
        elif page=="10":
            pagettl='RMSE - Add Upstream Model'
        elif page=="11":
            pagettl='RMSE - Add Downstream Model'
        elif page=="12":
            pagettl='RMSE - Add Monitoring Frequency'

        return render(request, 'addmastertbl.html',{'actPage':pagettl,'tbl':page,'tblData':objmaster.getMasterTblData(str(page))})
    except Exception as e:
        print('masterTbls is ',e)
        print('masterTbls traceback is ', traceback.print_exc()) 

def showmasterTbls(request):
    try: 
        pagettl='RMSE'
        page =request.GET.get('page', 'False')        
        if page=="1":
            pagettl='RMSE - Add Function'
        elif page=="2":
            pagettl='RMSE - Add Model Source'
        elif page=="3":
            pagettl='RMSE - Add Model Type'
        elif page=="4":
            pagettl='RMSE - Add Products Addressed'
        elif page=="5":
            pagettl='RMSE - Add Usage Frequency'
        elif page=="6":
            pagettl='RMSE - Add Model Risk'
        elif page=="7":
            pagettl='RMSE - Add Intrinsic Risk'
        elif page=="8":
            pagettl='RMSE - Add Reliance'
        elif page=="9":
            pagettl='RMSE - Add Materiality'
        elif page=="10":
            pagettl='RMSE - Add Upstream Model'
        elif page=="11":
            pagettl='RMSE - Add Downstream Model'
        elif page=="12":
            pagettl='RMSE - Add Monitoring Frequency'

        return render(request, 'showmasterdata.html',{'actPage':pagettl,'tbl':page,'tblData':objmaster.getMasterTblData(str(page))})
    except Exception as e:
        print('masterTbls is ',e)
        print('masterTbls traceback is ', traceback.print_exc()) 

def editmasterTbls(request,id,page):
    try: 
        pagettl='RMSE'
                
        if page=="1":
            pagettl='RMSE - Edit Function'
        elif page=="2":
            pagettl='RMSE - Edit Model Source'
        elif page=="3":
            pagettl='RMSE - Edit Model Type'
        elif page=="4":
            pagettl='RMSE - Edit Products Addressed'
        elif page=="5":
            pagettl='RMSE - Edit Usage Frequency'
        elif page=="6":
            pagettl='RMSE - Edit Model Risk'
        elif page=="7":
            pagettl='RMSE - Edit Intrinsic Risk'
        elif page=="8":
            pagettl='RMSE - Edit Reliance'
        elif page=="9":
            pagettl='RMSE - Edit Materiality'
        elif page=="10":
            pagettl='RMSE - Edit Upstream Model'
        elif page=="11":
            pagettl='RMSE - Edit Downstream Model'
        elif page=="12":
            pagettl='RMSE - Edit Monitoring Frequency'

        tbldata=objmaster.getMasterTblData(str(page))
        for i in tbldata:
           if str(tbldata[i]["AID"]) == str(id):
               tbldata=tbldata[i]
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
        opt =request.GET.get('opt', 'False')  
        desc=request.GET.get('desc', 'False')   
        tbl=request.GET.get('tbl', 'False')     
        selectedOPt=request.GET.get('selectedOPt', 'False')     
        activests=request.GET.get('activests', 'False')
        print('selectedOPt is ',selectedOPt)
        if selectedOPt =='':
            objmaster.insertFunctionOption(opt,desc,tbl,str(activests),str(request.session['uid']))
        else:
            objmaster.updateFunctionOption(str(selectedOPt),opt,desc,tbl,str(activests),str(request.session['uid']))    
        return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})

class projectsDetails(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            ty =request.data['filterType']
            colnm =request.data['filterValue']#request.GET.get('colnm', 'False') 
            chartnm =request.data['filterColumn']#request.GET.get('chartnm', 'False') 
            canAdd="1" 
            # Authorization(request.data['ucaid'],'Model Inventory') 
            modelinfo=objreg.getModelByFilter(request.data['uid'],ty,chartnm,colnm,'0')
            is_MrmHead=str(objmaster.checkMRMHead(str(request.data['uid'])))            
            return Response( {'modelinfo':modelinfo,'canAdd':canAdd, 'is_MrmHead':is_MrmHead},status=status.HTTP_200_OK)          
                
        except Exception as e:
           error_saving(request,e)
           return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)
        


class getMdlDetailsById(APIView):
    permission_classes=[IsAuthenticated] 
    def get(self,request):
        try: 
            mdl_id =request.data.get('mdl_id', 'False') 
            objMdlRelvPern=MdlRelevantPersonnelFuncs()

            Owner=objMdlRelvPern.getRelevantPersonal(mdl_id,'Owner')

            Developer=objMdlRelvPern.getRelevantPersonal(mdl_id,'Developer')

            User=objMdlRelvPern.getRelevantPersonal(mdl_id,'User')

            PrdnSupport=objMdlRelvPern.getRelevantPersonal(mdl_id,'PrdnSupport')

            objdependencies=MdlDependenciesCls()
            dependencies =objdependencies.getMdlDependencies(mdl_id) 

            PerformMon=objreg.getPerfomanceMonitor(mdl_id)
            mdldata=objreg.getModelById(mdl_id)
            isvrpublished=objreg.isVRPublished(mdl_id)
            print('mdldata ',mdldata,' ,',request.data)
            return Response(
            {'istaken':'true','dependencies':dependencies,'PerformMon':PerformMon,'Owner':Owner,'Developer':Developer,'User':User,
             'PrdnSupport':PrdnSupport,'mdldata':mdldata,'isvrpublished':isvrpublished},status=status.HTTP_200_OK)
        except Exception as e:
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)
        
class getTempMdlDetailsById(APIView):
    permission_classes=[IsAuthenticated] 
    def get(self,request):
        try:
            mdl_id =request.data.get('mdl_id', 'False') 
            print('mdl_id ',mdl_id)
            objMdlRelvPern=MdlRelevantPersonnelFuncs()

            Owner=objMdlRelvPern.getTempRelevantPersonal(mdl_id,'Owner')
            print('Owner ',Owner)

            Developer=objMdlRelvPern.getTempRelevantPersonal(mdl_id,'Developer')
            print('Developer ',Developer)

            User=objMdlRelvPern.getTempRelevantPersonal(mdl_id,'User')

            PrdnSupport=objMdlRelvPern.getTempRelevantPersonal(mdl_id,'PrdnSupport')

            objdependencies=MdlDependenciesCls()
            dependencies =objdependencies.getTempMdlDependencies(mdl_id) 
            print('dependencies ',dependencies)


            PerformMon=objreg.getTempPerfomanceMonitor(mdl_id)
            print('PerformMon ',PerformMon)
            return Response(
            {'istaken':'true','dependencies':dependencies,'PerformMon':PerformMon,'Owner':Owner,'Developer':Developer,'User':User,
             'PrdnSupport':PrdnSupport,'mdldata':objreg.getTempModelById(mdl_id)},status=status.HTTP_200_OK)
        except Exception as e:
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class ApproveEdit(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            mdlid = request.data.get("mdlId",'False')
            colname = request.data.get("colname",'False')
            tblname = request.data.get("tblname",'False')
            print("Approve edit data",mdlid,colname,tblname)
            objreg.updateApprovedData(mdlid,tblname,colname)
            return Response({'istaken':'true'},status=status.HTTP_200_OK)
        except Exception as e:
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

def test(request):
    try:
        return render(request, 'calendar.html',{ 'actPage':'Add Model'})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 


def addmodel(request):
    try:
        mdl_id=''
        mrm_head=objmaster.getMRMHead()
        # if(str(objmaster.isAutherized(request.session['ucaid'],'4')) =="0"):
        #     print('not autherized')
        #     return render(request, 'blank.html',{'actPage':'RMSE'}) 
        if request.method == 'POST':   
            rbisnewupdate = request.POST['rbisnewupdate'] 
            ddlFunction = request.POST['ddlFunction'] 
            txtMdlId = request.POST['txtMdlId'] 
            # txtMdlId= request.POST.getlist('txtMdlId')   
             
            txtPrmName = request.POST['txtPrmName'] 
            txtSecName = request.POST['txtSecName'] 
            ddlSource = request.POST['ddlSource'] 
            ddlType = request.POST['ddlType'] 
            txtMdlAbsct = request.POST['txtMdlAbsct'] 
            txtMdlObj = request.POST['txtMdlObj'] 
            txtMdlAppl = request.POST['txtMdlAppl'] 
            txtMdlRiskAnls = request.POST['txtMdlRiskAnls'] 
            ddlPrctAddr = request.POST['ddlPrctAddr'] 
            ddlUsgFreq = request.POST['ddlUsgFreq'] 
            txtMdlRisks = request.POST['hdnMdlRisks'] 
            ddlIntrRisk = request.POST['hdnIntrRisk'] 
            ddlReliance = request.POST['hdnReliance'] 
            ddlMateriality = request.POST['hdnMateriality'] 
            txtRiskMtgn = request.POST['txtRiskMtgn'] 
            txtFairLndg = request.POST['txtFairLndg'] 
            ddlOwner =  request.POST.getlist('ddlOwner')
            ddlDeveloper = request.POST.getlist('ddlDeveloper')  
            ddlUser = request.POST.getlist('ddlUser')    
            txtValidator = request.POST['txtValidator'] 
            ddlPrdnSupp = request.POST.getlist('ddlPrdnSupp')   
            ddlUpstrmMdl = request.POST['ddlUpstrmMdl'] 
            ddlDwstrmMdl = request.POST['ddlDwstrmMdl'] 
            txtApproach = request.POST['txtApproach'] 
            ddlMonrFreq = request.POST['ddlMonrFreq'] 
            txtTgrEvt = request.POST['txtTgrEvt'] 
            txtLstTgrDt = request.POST['txtLstTgrDt'] 
            txtLstTgrMtgnDt = request.POST['txtLstTgrMtgnDt'] 
            txtTgrEvtMtgn = request.POST['txtTgrEvtMtgn'] 
            txtMonrMtrcs=request.POST['txtMonrMtrcs'] 
            objoverview=MdlOverviewCls(txtMdlId,'1','0','0',rbisnewupdate,'0',request.session['dept']
                                    ,ddlFunction,txtPrmName.replace("'","''"),txtSecName.replace("'","''"),ddlSource,ddlType,txtMdlAbsct.replace("'","''"),txtMdlObj.replace("'","''")
                                    ,txtMdlAppl.replace("'","''"),txtMdlRiskAnls.replace("'","''"),ddlPrctAddr,ddlUsgFreq,request.session['uid'])
            mdl_id=objoverview.insertMdlOverview()
 
            objModelRisks=ModelRisks(mdl_id,txtMdlRisks,ddlIntrRisk,ddlReliance,ddlMateriality,txtRiskMtgn.replace("'","''"),txtFairLndg.replace("'","''"),request.session['uid'])
            objModelRisks.insertModelRisk()

            objMdlRelvPern=MdlRelevantPersonnel()
            objMdlRelvPern.insertUsers(mdl_id,'Owner',ddlOwner,request.session['uid'])

            objMdlRelvPern.insertUsers(mdl_id,'Developer',ddlDeveloper,request.session['uid'])

            objMdlRelvPern.insertUsers(mdl_id,'User',ddlUser,request.session['uid'])

            objMdlRelvPern.insertUsers(mdl_id,'PrdnSupport',ddlPrdnSupp,request.session['uid'])

            
            #Thread Creation
            current_user_id = request.session['uid']
             
            thread_filter_creation(current_user_id,mrm_head)

            notification_trigger= "New Model registered - " + mdl_id
            objmaster.insert_notification(request.session['uid'],mrm_head,"Model",notification_trigger,1)
            
            objdependencies=MdlDependenciesCls()
            objdependencies.insertMdlDepencies(mdl_id,ddlUpstrmMdl,ddlDwstrmMdl,request.session['uid'])

            objPerformMon=MdlPerformanceMonitoring(mdl_id,txtApproach.replace("'","''"),ddlMonrFreq,txtMonrMtrcs.replace("'","''"),txtTgrEvt.replace("'","''")
                                                   ,txtLstTgrDt,txtLstTgrMtgnDt,txtTgrEvtMtgn.replace("'","''"),request.session['uid'])
            objPerformMon.insertPerfomanceMonitor() 
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

            fl_MD = request.FILES.get('txtUserManual', 'none')             
            if fl_MD != 'none':
                fs = FileSystemStorage()
                savefile_name = destination_path + mdl_id+'_'+fl_MD.name
                if os.path.exists(savefile_name):
                    os.remove(savefile_name)
                fs.save(savefile_name, fl_MD)
                objdocs.inserDocs(mdl_id,'2',mdl_id+'_'+fl_MD.name,str(request.session['uid']))

            fl_MD = request.FILES.get('txtMdlData', 'none')             
            if fl_MD != 'none':
                fs = FileSystemStorage()
                savefile_name = destination_path + mdl_id+'_'+fl_MD.name
                if os.path.exists(savefile_name):
                    os.remove(savefile_name)
                fs.save(savefile_name, fl_MD)
                objdocs.inserDocs(mdl_id,'3',mdl_id+'_'+fl_MD.name,str(request.session['uid']))

            fl_MD = request.FILES.get('txtMdlCode', 'none')             
            if fl_MD != 'none':
                fs = FileSystemStorage()
                savefile_name = destination_path + mdl_id+'_'+fl_MD.name
                if os.path.exists(savefile_name):
                    os.remove(savefile_name)
                fs.save(savefile_name, fl_MD)
                objdocs.inserDocs(mdl_id,'4',mdl_id+'_'+fl_MD.name,str(request.session['uid']))
            
            fl_MD = request.FILES.get('txtUAT', 'none')             
            if fl_MD != 'none':
                fs = FileSystemStorage()
                savefile_name = destination_path + mdl_id+'_'+fl_MD.name
                if os.path.exists(savefile_name):
                    os.remove(savefile_name)
                fs.save(savefile_name, fl_MD)
                objdocs.inserDocs(mdl_id,'5',mdl_id+'_'+fl_MD.name,str(request.session['uid']))

            fl_MD = request.FILES.get('txtTechManual', 'none')             
            if fl_MD != 'none':
                fs = FileSystemStorage()
                savefile_name = destination_path + mdl_id+'_'+fl_MD.name
                if os.path.exists(savefile_name):
                    os.remove(savefile_name)
                fs.save(savefile_name, fl_MD)
                objdocs.inserDocs(mdl_id,'6',mdl_id+'_'+fl_MD.name,str(request.session['uid']))

            fl_MD = request.FILES.get('txtOnboardDoc', 'none')             
            if fl_MD != 'none':
                fs = FileSystemStorage()
                savefile_name = destination_path + mdl_id+'_'+fl_MD.name
                if os.path.exists(savefile_name):
                    os.remove(savefile_name)
                fs.save(savefile_name, fl_MD)
                objdocs.inserDocs(mdl_id,'7',mdl_id+'_'+fl_MD.name,str(request.session['uid']))
                
            # print('txtMdlAppl ',txtMdlAppl, ' txtLstTgrMtgnDt ',txtLstTgrMtgnDt,' rbisnewupdate ',rbisnewupdate,request.session['dept'])

        today = date.today().strftime("%m/%d/%Y") 

        dept= objreg.getDeptNm(request.session['dept'])

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

        Upstr_Model=objreg.getMdlUpstrem(request.session['uid'])

        Dwstr_Model=objreg.getMdlUpstrem(request.session['uid']) #objreg.getMdlDwStream()

        Motr_Freq=objreg.getMontrFreq()

        Mdl_Func=objreg.getMdlFunc()

        Models_FieldsResult =objdbops.getTable("SELECT  Field_ID,Fields_name,Field_Label,Is_Mandatory,Is_Visible  FROM Models_Fields order by 1 ")
        Models_Fields = Models_FieldsResult.to_json(orient='index')
        Models_Fields = json.loads(Models_Fields)
        del Models_FieldsResult
        arrFields=dict()
        for i in Models_Fields: 
            if Models_Fields[i]["Fields_name"]=="function":
                arrFields["FunctionVisible"]= 'block' if Models_Fields[i]["Is_Visible"]==True else 'none'
                arrFields["FunctionMadatory"]= 'required' if Models_Fields[i]["Is_Mandatory"]==True else ''
                arrFields["FunctionMadatoryAstr"]= 'block' if Models_Fields[i]["Is_Mandatory"]==True else 'none'
                arrFields["FunctionLbl"]= Models_Fields[i]["Field_Label"]
            elif Models_Fields[i]["Fields_name"]=="Secondary Model Name":
                arrFields["SecMdlVisible"]=  'block' if Models_Fields[i]["Is_Visible"]==True else 'none'
                arrFields["SecMdlMadatory"]= 'required' if Models_Fields[i]["Is_Mandatory"]==True else ''
                arrFields["SecMdlMadatoryAstr"]= 'block' if Models_Fields[i]["Is_Mandatory"]==True else 'none'
                arrFields["SecMdlLbl"]=Models_Fields[i]["Field_Label"]
            elif Models_Fields[i]["Fields_name"]=="Model Type":
                arrFields["MdlTypeVisible"]=  'block' if Models_Fields[i]["Is_Visible"]==True else 'none'
                arrFields["MdlTypeMadatory"]= 'required' if Models_Fields[i]["Is_Mandatory"]==True else ''
                arrFields["MdlTypeMadatoryAstr"]= 'block' if Models_Fields[i]["Is_Mandatory"]==True else 'none'
                arrFields["MdlTypeLbl"]=Models_Fields[i]["Field_Label"]
            elif Models_Fields[i]["Fields_name"]=="Model Abstract":
                arrFields["MdlAbsVisible"]=  'block' if Models_Fields[i]["Is_Visible"]==True else 'none'
                arrFields["MdlAbsMadatory"]= 'required' if Models_Fields[i]["Is_Mandatory"]==True else ''
                arrFields["MdlAbsMadatoryAstr"]= 'block' if Models_Fields[i]["Is_Mandatory"]==True else 'none'
                arrFields["MdlAbsLbl"]=Models_Fields[i]["Field_Label"]
            elif Models_Fields[i]["Fields_name"]=="Objective of Model":
                arrFields["ObjMdlVisible"]=  'block' if Models_Fields[i]["Is_Visible"]==True else 'none'
                arrFields["ObjMdlMadatory"]= 'required' if Models_Fields[i]["Is_Mandatory"]==True else ''
                arrFields["ObjMdlMadatoryAstr"]= 'block' if Models_Fields[i]["Is_Mandatory"]==True else 'none'
                arrFields["ObjMdlLbl"]=Models_Fields[i]["Field_Label"]
            elif Models_Fields[i]["Fields_name"]=="Application of Model":
                arrFields["ApplMdlVisible"]=  'block' if Models_Fields[i]["Is_Visible"]==True else 'none'
                arrFields["ApplMdlMadatory"]= 'required' if Models_Fields[i]["Is_Mandatory"]==True else ''
                arrFields["ApplMdlMadatoryAstr"]= 'block' if Models_Fields[i]["Is_Mandatory"]==True else 'none'
                arrFields["ApplMdlLbl"]=Models_Fields[i]["Field_Label"]
            elif Models_Fields[i]["Fields_name"]=="Model Risk Analysis":
                arrFields["MdlRskVisible"]=  'block' if Models_Fields[i]["Is_Visible"]==True else 'none'
                arrFields["MdlRskMadatory"]= 'required' if Models_Fields[i]["Is_Mandatory"]==True else ''
                arrFields["MdlRskMadatoryAstr"]= 'block' if Models_Fields[i]["Is_Mandatory"]==True else 'none'
                arrFields["MdlRskLbl"]=Models_Fields[i]["Field_Label"]
            elif Models_Fields[i]["Fields_name"]=="Products Addressed":
                arrFields["PrdAddrVisible"]=  'block' if Models_Fields[i]["Is_Visible"]==True else 'none'
                arrFields["PrdAddrMadatory"]= 'required' if Models_Fields[i]["Is_Mandatory"]==True else ''
                arrFields["PrdAddrMadatoryAstr"]= 'block' if Models_Fields[i]["Is_Mandatory"]==True else 'none'
                arrFields["PrdAddrLbl"]=Models_Fields[i]["Field_Label"]
            elif Models_Fields[i]["Fields_name"]=="Usage Frequency":
                arrFields["UsgFreqVisible"]=  'block' if Models_Fields[i]["Is_Visible"]==True else 'none'
                arrFields["UsgFreqMadatory"]= 'required' if Models_Fields[i]["Is_Mandatory"]==True else ''
                arrFields["UsgFreqMadatoryAstr"]= 'block' if Models_Fields[i]["Is_Mandatory"]==True else 'none'
                arrFields["UsgFreqLbl"]=Models_Fields[i]["Field_Label"]  

        return render(request, 'registermodel.html',{ 'actPage':'Model Registration','Mdl_Func':Mdl_Func,'Upstr_Model':Upstr_Model,
                    'Dwstr_Model':Dwstr_Model,'Motr_Freq':Motr_Freq,'mdl_id':mdl_id,
                    'mdlinfo':objreg.getModelsbyUserid(request.session['uid']),'Mdl_Devs':Mdl_Devs,
                'Mdl_Validators':Mdl_Validators,'Mdl_Owners':Mdl_Owners,'Reliance':Reliance,
                'Materiality':Materiality,'Intrinsic':Intrinsic,'Mdl_Risk':Mdl_Risk,'Prd_Addr':Prd_Addr,'Mdl_Usage_Frq':Mdl_Usage_Frq,
                'Mdl_Type':Mdl_Type,'Mdl_Src':Mdl_Src,'dept':dept,'regDate':today,'arrFields':arrFields})
    except Exception as e:
        print('addmodel is ',e)
        print('addmodel traceback is ', traceback.print_exc()) 
        error_saving(request,e)

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
    
# def thread_creation(request):
#     send_by=request.GET.get('send_by', 'False')
#     send_to=request.GET.get('send_to', 'False')
#     threadfilter = Thread.objects.filter(first_person = send_by,second_person = send_to)
#     print("threadfilter",threadfilter)
#     if not threadfilter:
#         curr_user_id = Users.objects.get(u_aid = send_by)
#         print("curr_user_id",curr_user_id)
#         othr_usr_id = Users.objects.get(u_aid = send_to)
#         print("othr_usr_id",othr_usr_id)
#         threadobj = Thread(first_person = curr_user_id,second_person = othr_usr_id)
#         threadobj.save()
#         thread_id = threadobj.thread_id
#         print("save thread successfully") 
             
#     else: 
#         thread_id = threadfilter.thread_id
#         print("pass",thread_id)
#         pass
    

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


def addtool(request):
    try:
        mdl_id=''
        if request.method == 'POST':   
            rbisnewupdate = request.POST['rbisnewupdate'] 
            ddlFunction = request.POST['ddlFunction'] 
            txtMdlId = request.POST['txtMdlId'] 
            txtPrmName = request.POST['txtPrmName'] 
            txtSecName = request.POST['txtSecName'] 
            ddlSource = request.POST['ddlSource'] 
            ddlType = request.POST['ddlType'] 
            txtMdlAbsct = request.POST['txtMdlAbsct'] 
            txtMdlObj = request.POST['txtMdlObj'] 
            txtMdlAppl = request.POST['txtMdlAppl'] 
            txtMdlRiskAnls = request.POST['txtMdlRiskAnls'] 
            ddlPrctAddr = request.POST['ddlPrctAddr'] 
            ddlUsgFreq = request.POST['ddlUsgFreq'] 
            txtMdlRisks = request.POST['txtMdlRisks'] 
            ddlIntrRisk = request.POST['ddlIntrRisk'] 
            ddlReliance = request.POST['ddlReliance'] 
            ddlMateriality = request.POST['ddlMateriality'] 
            txtRiskMtgn = request.POST['txtRiskMtgn'] 
            txtFairLndg = request.POST['txtFairLndg'] 
            ddlOwner =  request.POST.getlist('ddlOwner')
            ddlDeveloper = request.POST.getlist('ddlDeveloper')  
            ddlUser = request.POST.getlist('ddlUser')    
            txtValidator = request.POST['txtValidator'] 
            ddlPrdnSupp = request.POST.getlist('ddlPrdnSupp')   
            ddlUpstrmMdl = request.POST['ddlUpstrmMdl'] 
            ddlDwstrmMdl = request.POST['ddlDwstrmMdl'] 
            txtApproach = request.POST['txtApproach'] 
            ddlMonrFreq = request.POST['ddlMonrFreq'] 
            txtTgrEvt = request.POST['txtTgrEvt'] 
            txtLstTgrDt = request.POST['txtLstTgrDt'] 
            txtLstTgrMtgnDt = request.POST['txtLstTgrMtgnDt'] 
            txtTgrEvtMtgn = request.POST['txtTgrEvtMtgn'] 
            txtMonrMtrcs=request.POST['txtMonrMtrcs'] 
            objoverview=MdlOverviewCls(txtMdlId,'1','0','0',rbisnewupdate,'1',request.session['dept']
                                    ,ddlFunction,txtPrmName.replace("'","''"),txtSecName.replace("'","''"),ddlSource,ddlType,txtMdlAbsct.replace("'","''"),txtMdlObj.replace("'","''")
                                    ,txtMdlAppl.replace("'","''"),txtMdlRiskAnls.replace("'","''"),ddlPrctAddr,ddlUsgFreq,request.session['uid'])
            mdl_id=objoverview.insertMdlOverview()

            objModelRisks=ModelRisks(mdl_id,txtMdlRisks,ddlIntrRisk,ddlReliance,ddlMateriality,txtRiskMtgn.replace("'","''"),txtFairLndg.replace("'","''"),request.session['uid'])
            objModelRisks.insertModelRisk()

            objMdlRelvPern=MdlRelevantPersonnel()
            objMdlRelvPern.insertUsers(mdl_id,'Owner',ddlOwner,request.session['uid'])

            objMdlRelvPern.insertUsers(mdl_id,'Developer',ddlDeveloper,request.session['uid'])

            objMdlRelvPern.insertUsers(mdl_id,'User',ddlUser,request.session['uid'])

            objMdlRelvPern.insertUsers(mdl_id,'PrdnSupport',ddlPrdnSupp,request.session['uid'])

            #Thread Creation
            current_user_id = request.session['uid']
            print("current user id next",current_user_id)
            print("other user check next",ddlOwner)
            for i in ddlOwner:
                thread_filter_creation(current_user_id,i)

            objdependencies=MdlDependenciesCls()
            objdependencies.insertMdlDepencies(mdl_id,ddlUpstrmMdl,ddlDwstrmMdl,request.session['uid'])

            objPerformMon=MdlPerformanceMonitoring(mdl_id,txtApproach.replace("'","''"),ddlMonrFreq,txtMonrMtrcs.replace("'","''"),txtTgrEvt.replace("'","''")
                                                   ,txtLstTgrDt,txtLstTgrMtgnDt,txtTgrEvtMtgn.replace("'","''"),request.session['uid'])
            objPerformMon.insertPerfomanceMonitor()

            # print('txtMdlAppl ',txtMdlAppl, ' txtLstTgrMtgnDt ',txtLstTgrMtgnDt,' rbisnewupdate ',rbisnewupdate,request.session['dept'])

        today = date.today().strftime("%m/%d/%Y") 

        dept= objreg.getDeptNm(request.session['dept'])

        Mdl_Src = objreg.getMdl_Src()  

        Mdl_Type =objreg.getMdl_Type() 
        
        Mdl_Usage_Frq=  objreg.getMdl_Usage_Fre()
        
        Prd_Addr = objreg.getPrd_Addr() 

        Mdl_Risk = objreg.getMdl_Risk()  

        Intrinsic = objreg.getIntrinsic()  

        Materiality = objreg.getMateriality()        
         
        Reliance = objreg.getReliance()  

        Mdl_Owners =objreg.getUsers(request.session['dept'],2)    

        Mdl_Validators =[]#objreg.getUsers(request.session['dept'],3)         

        Mdl_Devs =[]#objreg.getUsers(request.session['dept'],4)         

        return render(request, 'registertool.html',{ 'actPage':'Tool Registration','mdl_id':mdl_id,'mdlinfo':objreg.getModelsbyUserid(request.session['uid']),'Mdl_Devs':Mdl_Devs,'Mdl_Validators':Mdl_Validators,'Mdl_Owners':Mdl_Owners,'Reliance':Reliance,'Materiality':Materiality,'Intrinsic':Intrinsic,'Mdl_Risk':Mdl_Risk,'Prd_Addr':Prd_Addr,'Mdl_Usage_Frq':Mdl_Usage_Frq,'Mdl_Type':Mdl_Type,'Mdl_Src':Mdl_Src,'dept':dept,'regDate':today})
    except Exception as e:
        print('addtool is ',e)
        print('addtool traceback is ', traceback.print_exc()) 

def getMdlInfoById(request):
    try:
        mdlid =request.GET.get('mdlid', 'False')
        majorVer=''
        minorVer=''
        if(mdlid!=""): 
            mdlinfo= objreg.getMdlinfo(mdlid) 
            majorVer=mdlinfo["Mdl_Major_Ver"].values[0]
            minorVer=mdlinfo["Mdl_Minor_Ver"].values[0]
        return JsonResponse({'majorVer':str(majorVer),'minorVer':str(minorVer)})
    except Exception as e:
        print('getMdlInfoById is ',e)
        print('getMdlInfoById traceback is ', traceback.print_exc()) 

def getnotifications(request):
    try:
         
        return JsonResponse({'notification':objreg.get_notifications(request.session['uid'])})
    except Exception as e:
        print('getMdlInfoById is ',e)
        print('getMdlInfoById traceback is ', traceback.print_exc()) 

def updateMdlVersion(request):
    try:
        mdlid =request.GET.get('mdlid', 'False')
        isMinor =request.GET.get('isMinor', 'False')
        
        return JsonResponse({'newMdlId':objreg.updateMdlVersion(mdlid,isMinor)})
    except Exception as e:
        print('getMdlInfoById is ',e)
        print('getMdlInfoById traceback is ', traceback.print_exc())

def getUsers(dept,utype):
    tableResult = objdbops.getTable("select concat(U_FName,' ',U_LName) usernm,u_aid  from users where dept_aid='"+str(dept)+"' and UC_AID='"+str(utype)+"'")
    return tableResult

class reqValidation(APIView):
    permission_classes=[IsAuthenticated] 
    def get(self,request):
        try:
            modelinfo=objreg.getModelListByUSerid(request.data['uid'],str(request.data['ulvl']),'0')
            validationTYpes=objmaster.getValidationTypes()
            mrmUsers=objmaster.getMRMUsers()
            context={'mrmUsers':mrmUsers,'modelinfo':modelinfo,'validationTYpes':validationTYpes}
            return Response( context, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST) 


class assignValidation(APIView):
    permission_classes=[IsAuthenticated]  
    def post(self,request):
        try: 
            colDataLst = request.data['datalist'] 
            mdlId = request.data['mdlId'] 
            assigedto =request.data['ddlUsers']  
            json_colDataLst = json.loads(colDataLst) 
            assigedto = json.loads(assigedto)  
            department = request.data['dept']
            originator = request.data['uid']
            
            assignTaskLst=objvalidation.assignValidation(json_colDataLst,assigedto,mdlId,str(request.data['uid']),department,originator) 
            
            for user in assigedto:
                thread_filter_creation(request.data['uid'],user["UID"])
                notification_trigger= "Model  "+ mdlId +" validation requested"
                objmaster.insert_notification(request.data['uid'],user["UID"],"Validation request",notification_trigger,1)
                trail_obj = ActivityTrail(refference_id  = mdlId,activity_trigger = "Task Created - Validation Request.",activity_details = "Model validation assignment.",addedby=originator,added_on=datetime.now(),)
                trail_obj.save()
            return Response({'istaken':'true','assignTaskLst':assignTaskLst}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)
    
class getAssignedTo(APIView):
    def get(self,request):
        try: 
            mdlId = request.data['mdlId']  
            return Response({'istaken':'true','assignedTo':objvalidation.getAssiged(mdlId)}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class getVTMenus(APIView):
    def get(self,request):
        try: 
            mdlId = request.data['mdlId']  
            uid = request.data['uid']  
            return Response({'istaken':'true','assignedTo':objvalidation.getVTMenus(mdlId,uid)}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)
         



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
        return render(request, 'newusercat.html',{ 'actPage':'Add User Types','level':list(range(1, 6))})
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
        uc_aid =request.GET.get('uc_aid', 'False')  
        dept_aid=request.GET.get('dept_aid', 'False') 
           
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
        tableResult =objdbops.getTable("select * from Department") 
        users = tableResult.to_json(orient='index')
        users = json.loads(users)
        print("users",users)
        del tableResult
        return render(request, 'deptlist.html',{ 'actPage':'Departments','users':users})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def newdept(request):
    try:   
        return render(request, 'adddepartment.html',{ 'actPage':'Add Department'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def adddept(request):
    try: 
        added_by=request.session['uid']
        add_date=datetime.now()
        dept =request.GET.get('dept', 'False')  
        desc=request.GET.get('desc', 'False')     
        IsMRM=request.GET.get('ismrm', 'False') 
        print("IsMRM",IsMRM)
        update_id=request.GET.get('update_id')
        if update_id:
            print("update",update_id)
            dept_obj=Department.objects.get(dept_aid=update_id)
            dept_obj.dept_label=dept
            dept_obj.dept_description=desc
            dept_obj.is_mrm=IsMRM
            dept_obj.updatedby=added_by
            dept_obj.updatedate=add_date
            dept_obj.save()
            return JsonResponse({"isvalid":"update"})
        else:    
            print("insert")
            strQ="INSERT INTO Department (Dept_Label ,Dept_Description,AddDate,Dept_IsMRM) "
            strQ += " VALUES  ('"+ dept.replace("'","''")+"','"+ desc.replace("'","''")+"',getdate(),"+IsMRM+")"

            objdbops.insertRow(strQ)
            return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})

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

class getCriteria(APIView):
    permission_classes = (IsAuthenticated,) 
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:   
            return Response({ 'actPage':'Select Model/Tool','criteria':objmaster.getCriteria()}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class GetIsModel(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            colDataLst = request.data['criteria'] 
            qtns = request.data['qtns'] 
            json_dictionary = json.loads(colDataLst)  
            qtns_dictionary = json.loads(qtns)   
        
            return Response({'istaken':'true','isModel': objreg.getIsModel(json_dictionary,qtns_dictionary)}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class checkValue(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            tbl =request.data['tbl']
            val=request.data['val']
            dept=request.data['dept'] 
            utype=request.data['utype']  
            cnt=""
            cnt = objmaster.checkUniqueVal(tbl,val,dept,utype)
            return Response({"isvalid":"true","cnt":cnt}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

def useraccess(request):
    try: 
        tableResult =objdbops.getTable("select * from Resources order by 1")  
        users = tableResult.to_json(orient='index')
        users = json.loads(users)
        del tableResult
        tableResult =objdbops.getTable("SELECT   UC_AID  ,UC_Label  FROM User_Category order by 2 ")
        utype = tableResult.to_json(orient='index')
        utype = json.loads(utype)
        del tableResult
        return render(request, 'useraccess.html',{ 'actPage':'User Access','users':users,'utype':utype})
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
        return JsonResponse({'istaken':'true','ucdata':objmaster.getUCAccess(uc)})
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
        json_colDataLst = json.loads(colDataLst)
         
        strQ="delete from User_Access where UC_AID="+str(uc)
        objdbops.insertRow(strQ) 
        for colval in json_colDataLst:
            print('colval is ',colval['AID'],', UA',colval['UA'],colval['add'],colval['edit'],colval['delete'])
            # for attribute, value in colval.items():
            #     print(attribute, value) 
            strQ="INSERT INTO User_Access (R_AID,UA_Perm,UC_AID,AddDate,UA_Add,UA_Edit,UA_Delete)  VALUES ("
            strQ +=colval['AID'] +",'"+colval['UA']+"',"+str(uc)+",getdate(),"+ str(colval['add']) +","+str(colval['edit']) +","+ str(colval['delete']) +")"
            objdbops.insertRow(strQ)
        
        return JsonResponse({'istaken':'true'})
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
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-NH98228\HCSPL18;DATABASE=RMSE;UID=sa;PWD=sqlAdm_18')

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
       
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-NH98228\HCSPL18;DATABASE=RMSE;UID=sa;PWD=sqlAdm_18')

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

class addICQQtns(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:            
            return Response({'sections':objmaster.getSections()}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)


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

class add_question(APIView):
    permission_classes=[IsAuthenticated] 
    def post(self,request):
        try:        
            added_by=request.data['uid']
            adddate=datetime.now()
            section=request.data['section']
            sub_section=request.data['sub_section']
            sub_sub_section=request.data['sub_sub_section']
            sub_sub_sub_section=request.data['sub_sub_sub_section']
            question=request.data['question'] 
            if sub_section == '':
                sub_section=None
            if sub_sub_section == '':
                sub_sub_section =None
            if sub_sub_sub_section == '':
                sub_sub_sub_section =None      
            question_obj=IcqQuestionMaster.objects.create(question_label=question,section_aid=section,sub_section_aid=sub_section,
                                                        sub_sub_section_aid=sub_sub_section,sub_sub_sub_section_aid=sub_sub_sub_section,
                                                        addedby=added_by,adddate=adddate)
            print("saved")
            return JsonResponse({'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)
        


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

class ICQQtns(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        print("request_data",request.data)
        try: 
            uid=request.data['uid'] 
            return Response({'canupdate':objmaster.canUpdateRatings(uid),'sections':objmaster.getICQQtnSection(uid),
                           'Qtns':objmaster.getICQQtns(uid),'models':objmaster.getICQModels(str(uid))}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            print(traceback.print_exc())
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class getICQSections(APIView):
    def get(swlf,request):
        try:   
            uid=request.data['uid']
            return JsonResponse({'sections':objmaster.getICQQtnSection(uid)}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST) 

class getICQSecQtn(APIView):
    permission_classes=[IsAuthenticated] 
    def get(self,request):
        try: 
            sectionid =request.GET.get('ddlSection', '0')  
            return Response({'sections':objmaster.getICQQtns(sectionid)}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)
           
class saveICQRatings(APIView):
    permission_classes=[IsAuthenticated]
    # def post(self,request):
    #     try: 
    #         colDataLst = request.data['colDataLst']
    #         uid=request.data['uid']
    #         json_colDataLst = json.loads(colDataLst)
    #         objreg=Register()
    #         for colval in json_colDataLst:
    #             print('col val is ',colval )
    #             objreg.insertICQRatings(colval["qtnId"],colval["ddl_yesno_"],colval["ddl_doc_"],colval["txt_comment_"],colval['ddl_InherentRisk_'],colval['ddl_ControllEffectiveness_'],colval['ddl_Residual_'],colval['txt_control_desc_'],uid,objmaster.getmaxICQId())
                
    #         return Response({'is_taken':True}, status=status.HTTP_200_OK)
    #     except Exception as e: 
    #         error_saving(request,e)
    #         return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)
    def post(self,request):
        try: 
            colDataLst = request.data['colDataLst']
            print("colDataLst",colDataLst)
            uid=request.data['uid']
            json_colDataLst = json.loads(colDataLst)
            print("json_colDataLst",json_colDataLst)
            objreg=Register()
            for colval in json_colDataLst:
                print('col val is ',colval )
                # objreg.insertFLRatings(colval["qtnId"],colval["ddl_yesno_"],colval["ddl_doc_"],colval["txt_comment_"],uid,objmaster.getmaxFLId())
                obj = IcqQuestionRatingData.objects.filter(review_id=objmaster.getmaxFLId(),question_aid=colval["qtnId"],addedby=uid)
                if obj:    
                    print("if")
                    IcqQuestionRatingData.objects.filter(review_id=objmaster.getmaxFLId(),question_aid=colval["qtnId"],addedby=uid).update(rating_yes_no=colval["ddl_yesno_"],doc_yes_no=colval["ddl_doc_"],comments=colval["txt_comment_"],inherent_risk_rating = colval['ddl_InherentRisk_'],control_effectiveness_ratings = colval['ddl_ControllEffectiveness_'],residual_ratings = colval['ddl_Residual_'],control_description= colval['txt_control_desc_'],override_residual_ratings = colval['ddl_override_Residual_'],override_comments = colval['txt_override_comment_'])
                else: 
                    print("else")
                    try:   
                        print("review_id",objmaster.getmaxFLId(),"question_aid",colval["qtnId"])
                        save_obj = IcqQuestionRatingData.objects.create(review_id=objmaster.getmaxFLId(),question_aid=colval["qtnId"],rating_yes_no=colval["ddl_yesno_"],doc_yes_no=colval["ddl_doc_"],comments=colval["txt_comment_"],inherent_risk_rating = colval['ddl_InherentRisk_'],control_effectiveness_ratings = colval['ddl_ControllEffectiveness_'],residual_ratings = colval['ddl_Residual_'],control_description= colval['txt_control_desc_'],override_residual_ratings = colval['ddl_override_Residual_'],override_comments = colval['txt_override_comment_'],addedby=uid)

                    except Exception as e:
                        print("error is",e.__traceback__)
            return Response({'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)


class submitICQRatings(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try: 
            objreg.submitRatings( objmaster.getmaxICQId())
            uid=request.data['uid']
            objmaster.insert_notification(str(uid),'MRM-Head','ICQ','Rating Submitted',1)    
            return JsonResponse({'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class submitFLRatings1(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try: 
            print("check---------------------------",request.data)
            objreg.FLsubmitRatings(objmaster.getmaxFLId())
            uid=request.data['uid']
            objmaster.insert_notification(str(uid),'MRM-Head','FL','Rating Submitted',1)    
            return JsonResponse({'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e: 
            print("error is",e)
            error_saving(request,e)  
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

def ICQQuestions(request):
    try: 
        sectionid =request.POST.get('ddlSection', '0')  
        return render(request, 'ICQQuestions.html',{ 'Qtns':objmaster.getAllICQQtns()})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

class ICQQtnsFinal(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
        
            context={'ICQRating':objreg.getICQRatings(objmaster.getmaxICQId()), 
                                                        'sections':objmaster.getICQQtnSectionFinal(),'Qtns':objmaster.getICQQtnsFinal()}
            return Response( context, status=status.HTTP_200_OK)
        except Exception as e: 
            print(traceback.print_exc())
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class FLQtnsFinal(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:            
            context={'FLRating':objreg.getFLRatingsFinal(objmaster.getmaxFLId()), 
                                                        'sections':objmaster.getFLtnSectionFinal(),'Qtns':objmaster.getFLQtnsFinal()}
            return Response( context, status=status.HTTP_200_OK)
        except Exception as e: 
            print(traceback.print_exc())  
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)


class getICQSectionsFinal(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:     
            return  Response({'sections':objmaster.getICQQtnSectionFinal()}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class getICQSecQtnFinal(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:  
            return Response( {'sections':objmaster.getICQQtnsFinal()}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class getFLSecQtnFinal(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:  
            return Response( {'sections':objmaster.getFLQtnsFinal()}, status=status.HTTP_200_OK)
        except Exception as e:
            print(traceback.print_exc()) 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)


class saveICQRatingsFinal(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:      
    
            colDataLst = request.data['colDataLst']
            print("list  check",colDataLst)
            uid=request.data['uid']
            json_colDataLst = json.loads(colDataLst)
            objreg=Register()
            maxid=objmaster.getmaxICQId()
            for colval in json_colDataLst: 
                print("colval",colval)    
                objreg.updateICQRatingsFinal(colval["qtnId"],colval["ddl_yesno_"],colval["ddl_doc_"],colval["txt_comment_"],colval['ddl_InherentRisk_'],colval['ddl_ControllEffectiveness_'],colval['ddl_Residual_'],colval['txt_control_desc_'],colval['ddl_override_Residual_'], colval['txt_override_comment_'],uid,maxid)
                 
            print("All save")
            return Response({'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e: 
            print("error is",e)
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class saveFLRatingsFinal(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:          
            colDataLst = request.data['colDataLst']
            print("colDataLst",colDataLst)
            uid=request.data['uid']
            json_colDataLst = json.loads(colDataLst)
            objreg=Register()
            maxid=objmaster.getmaxFLId()
            for colval in json_colDataLst: 
                objreg.updateFLRatingsFinal(colval["qtnId"],colval["ddl_yesno_"],colval["ddl_doc_"],colval["txt_comment_"],colval['ddl_InherentRisk_'],colval['ddl_ControllEffectiveness_'],colval['ddl_Residual_'],colval['txt_control_desc_'],colval['ddl_override_Residual_'], colval['txt_override_comment_'],uid,maxid)
 
            return Response( {'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)


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

class publushICQ(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            objmaster.publishICQ() 
            return Response( {"isvalid":"true"}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class publishFL(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            objmaster.publishFL() 
            return Response( {"isvalid":"true"}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)


def newquerybuilder(request):
    try:  
        from pandas.api.types import is_numeric_dtype,is_float_dtype,is_integer_dtype,is_string_dtype,is_number    
        file_id=find_max_file_id(request.session['vt_mdl'])   
        src_file_obj = collection.find({'file_id':file_id})          
        df =pd.DataFrame(list(src_file_obj))
        print('df len is  ',len(df))
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
                print('is_bool_dtype after error ',e,key,value,str(df[key][0]))
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
        from langchain.document_loaders import PyPDFLoader
        from langchain.document_loaders import Docx2txtLoader
        from langchain.document_loaders import TextLoader
        from langchain.embeddings import OpenAIEmbeddings
        from langchain.vectorstores import Chroma
        from langchain.llms import OpenAI
        from langchain.chat_models import ChatOpenAI
        from langchain.chains import ConversationalRetrievalChain
        from langchain.memory import ConversationBufferMemory
        from langchain.text_splitter import CharacterTextSplitter
        from langchain.prompts import PromptTemplate
        from langchain.chains.question_answering import load_qa_chain
        from django.shortcuts import render,HttpResponse
        from django.core.files import File
        from django.views.decorators.csrf import csrf_exempt
        import pyttsx3

        
        # os.environ["OPENAI_API_KEY"] = "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"      
        # os.environ["OPENAI_API_KEY"] = "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"    #chat gpt 4

        response=""
        fileName=request.GET.get('fileName','')
        query=request.GET.get('txtquery','')
       
        print('fileName ',fileName,' ',query)
        
        BASE_DIR = Path(__file__).resolve().parent.parent
        pdfDir = os.path.join(BASE_DIR, 'static\\pdfsummary\\')
        savefile_name = pdfDir + fileName 
        import requests

        headers = { 
            'x-api-key': 'ask_ad92639cbc21f332ed95712131d456a2'
        }

        file_data = open(savefile_name, 'rb')
        print(file_data)

        response = requests.post('https://api.askyourpdf.com/v1/api/upload', headers=headers,
        files={'file': file_data})
        doc_id=""
        if response.status_code == 201:
            response=response.json()
            doc_id=response['docId'] 
            headers = {
             'Content-Type': 'application/json',
            'x-api-key': 'ask_ad92639cbc21f332ed95712131d456a2'
             }
            data = [
            {
                "sender": "User",
                "message": query
            }
            ]

            response = requests.post('https://api.askyourpdf.com/v1/chat/'+doc_id , 
            headers=headers, data=json.dumps(data))

            if response.status_code == 200:
                airesp=response.json() 
                response=airesp['answer']['message']                 
                engine = pyttsx3.init('sapi5')                
                voices = engine.getProperty("voices")[0]
                engine.setProperty('voice', voices)
                # engine.say(tts)
                engine.save_to_file(response,  os.path.join(BASE_DIR, 'static/data/'+fileName +'_resp.mp3'))
                engine.runAndWait()
            else:
                print('Error:', response.status_code)
        else:
            print('Error:', response.status_code)

        

        # file = PyPDFLoader(savefile_name)
        # documents = file.load()
        # chain = load_qa_chain(llm=OpenAI()) 
        # response = chain.run(input_documents=documents, question=query)to be uncommented


        # text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
        # documents = text_splitter.split_documents(documents)

        # #os.remove('./data')
        # vectordb = Chroma.from_documents(documents, embedding=OpenAIEmbeddings(), persist_directory=os.path.join(BASE_DIR, 'static/data'))
        # vectordb.persist()

        # pdf_qa = ConversationalRetrievalChain.from_llm(
        # ChatOpenAI(temperature=0.9, model_name="gpt-3.5-turbo"),
        # vectordb.as_retriever(search_kwargs={'k': 6}),
        # return_source_documents=True,
        # verbose=False
        # )   

        # chat_history = []

        # while True:             
        #     result = pdf_qa({"question": query,"chat_history": chat_history })
        #     chat_history.append((query, result["answer"]))
        #     response=result["answer"]
        #     context={
        #         #'k':response,
        #     }
        #     print(response)
        
        return JsonResponse({"response":response,'aiaudio':'/static/data/'+fileName +'_resp.mp3'})
    except Exception as e:
        print('Error is',e,traceback.print_exc())
        return JsonResponse({"response":"false"})
    
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
        elif str(decommSts)=="1":
            decommSts=2
            notification_trigger= "Model Id "+ mdl_id + " decommissioned "
            notification_from=str(request.session['uid']) 
            notification_to=objmaster.getMdlOwner(mdl_id)
        if request.method == 'POST':  
            # myfile = request.FILES['myfile']
            filename = request.POST.get('filenm','none')
            print(' filename ',filename)
            files = request.FILES
            myfile = files.get('filename','None')
            print('myfile ',myfile,' filename ',filename)
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
        error_saving(request,e)
        return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class checkPendingTasksIssues(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request): 
        try:
            mdl_id = request.data['mdl_id']
            print('mdl_id',mdl_id)
            return Response({"checkPending":objreg.checkPendingTaskIssue(mdl_id),"decommdoc":objreg.getDecommDoc(mdl_id)},status=status.HTTP_200_OK)
        except Exception as e:
            print('uploaddecomm is ',e)
            print('uploaddecomm traceback is ', traceback.print_exc()) 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

def getDecommDoc(request):
    try:        
        mdl_id = request.GET.get('mdl_id','none')
        return JsonResponse({"decommdoc":objreg.getDecommDoc(mdl_id)})
    except Exception as e:
        print('uploaddecomm is ',e)
        print('uploaddecomm traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})


class QtnsResp(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try: 
            return Response({'is_mrm':str(objmaster.checkMRMHead(str(request.data['uid']))),
                             'mdl_id':objrmse.getModelsbyId(str(request.data['uid']))}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)
         
class getModelQtnBySrc(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:     
            mdl_id = request.data['mdl_id']
            return Response({"Qtns":objrmse.getModelQtns(mdl_id)}, status=status.HTTP_200_OK)
        except Exception as e: 
                error_saving(request,e)
                return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class getQtnResp(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:        
            mdl_id = request.data['mdl_id']
            qtn_id = request.data['qtn_id']
            return Response({"Qtns":objrmse.getQtnResp(mdl_id,qtn_id,str(request.data['uid']))}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class insertQtnResp(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:        
            mdl_id = request.data['mdl_id']
            qtn_id = request.data['qtn_id']
            comments = request.data['comments']
            isupdate = request.data['isupdate']
            Response_id = request.data['Response_id']
            objrmse.insertResp(mdl_id,qtn_id,str(request.data['uid']),comments,isupdate,Response_id)
            return Response({"is_taken":True}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class getQtnRespById(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:               
            Response_id = request.data('Response_id')        
            return Response({"is_taken":True,'comment':objrmse.getQtnRespById(Response_id)}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)


def mmrkasRead(request):
    try:
        notification_id = request.GET.get('notification_id','0')  
        return JsonResponse({'markread':objreg.markasRead(notification_id)})
    except Exception as e:
        print('getMdlInfoById is ',e)
        print('getMdlInfoById traceback is ', traceback.print_exc())

class Questions(APIView):
    def ger(self, request):
        try: 
            return Response({'Qtns':objmaster.getAllQtns()}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)


class QuestionsAllUsers(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try: 
            return Response({ 'Qtns':objmaster.getAllQtns()}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)


def addQtns(request):
    try:        
        return render(request, 'addQtns.html',{'sections':objmaster.getQuesSections()})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc()) 

class addQtnsAllUsers(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:        
            return Response({'sections':objmaster.getQuesSections()}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

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

class addQuesSub_Section(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:   
            section =request.data['section']
            sectiondesc =request.data['sectiondesc'] 
            activests =request.data['activests']     
            secid =request.data['secid']   
            objmaster.addQuesSub_Section(secid,section,sectiondesc,activests,str(request.data['uid']))
            return Response({'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class addQuesSub_Sub_Section(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:    
            section =request.data['section']
            sectiondesc =request.data['sectiondesc'] 
            activests =request.data['activests']     
            sub_secid =request.data['sub_secid']       
            objmaster.addQuesSub_Sub_Section(sub_secid,section,sectiondesc,activests,str(request.data['uid']))
            return Response({'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class getQuesSub_Sections(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:       
            sub_secid =request.data['secid']  
            return Response({'subsections':objmaster.getQuesSub_Sections(sub_secid)}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class getQuesSub_Sub_Sections(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:       
            sub_secid =request.data['secid']  
            return Response({'subsections':objmaster.getQuesSub_Sub_Sections(sub_secid)}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class addQuesSub_Sub_Sub_Section(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:    
            section =request.data['section']
            sectiondesc =request.data['sectiondesc'] 
            activests =request.data['activests']     
            sub_secid =request.data['sub_secid']             
            objmaster.addQuesSub_Sub_Sub_Section(sub_secid,section,sectiondesc,activests,str(request.data['uid']))
            return Response({'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)


def getQuesSub_Sub_Sub_Sections(request):
    print("getSub_Sub_Sub_Sections")
    try:       
        sub_secid =request.GET.get('secid', 'False')      
        print("sub_secid",sub_secid)
        return JsonResponse({'subsections':objmaster.getQuesSub_Sub_Sub_Sections(sub_secid)})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 

class addQues_question(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            
            added_by=request.data['uid']
            adddate=datetime.now()
            section=request.data['section']
            sub_section=request.data['sub_section']
            sub_sub_section=request.data['sub_sub_section']
            sub_sub_sub_section=request.data['sub_sub_sub_section']
            question=request.data['question'] 
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
            return Response({'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)  

class allocate_questions(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request): 
        try:  
            modelinfo=objreg.getModelListByUSerid(request.data['uid'],str(request.data['ulvl']),'0')      
            userobj = objreg.getMdlOwnerById(request.data['vt_mdl'],'Owner')   
            print('userobj ',userobj)    
            return Response({'models':modelinfo,'user':userobj,
                            'Qtns':objmaster.getAllQtns(request.data['vt_mdl']),'selectedMdl':request.data['vt_mdl']},
                            status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)



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

class getQues_Sections(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:       
            sub_secid =request.data('secid')     
            return Response({'sections':objmaster.getQues_Sections(sub_secid)}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)


def edit_department(request,id): 
    try:
        depart_obj=Department.objects.get(dept_aid=id)   
        label=depart_obj.dept_label
        desc=depart_obj.dept_description
        is_mrm=depart_obj.is_mrm
        print("is_mrm",is_mrm)
        return render(request, 'adddepartment.html',{ 'actPage':'Edit Department','label':label,'desc':desc,'is_mrm':is_mrm,'id':id})

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
        print("user_type",user_type)
        print("user_desc",user_desc)
        print("user_level",user_level)
        print("is_dept_head",is_dept_head)
        print("activate_status",activate_status)
        return render(request, 'newusercat.html',{ 'actPage':'Edit User Type','user_type':user_type,'user_level':user_level,'user_desc':user_desc,
                                                  'is_dept_head':is_dept_head,'activate_status':activate_status,'level':list(range(1, 6)),'id':id,'isDisabled':'disabled'})

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

class insertQtnAnsr(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:        
            mdl_id = request.data['mdl_id']
            qtn_id = request.data['qtn_id']
            Ansr = request.data['Ansr'] 
            objrmse.insertAnsr(mdl_id,qtn_id,str(request.data['uid']),Ansr)
            return JsonResponse({"is_taken":True}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class getQtnAns(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            mdl_id = request.data['mdl_id']
            qtn_id = request.data['qtn_id']  
            return JsonResponse({"is_taken":True,'ans':objrmse.getAnsr(mdl_id,qtn_id)}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class getTasks(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            all_data_lst=list()
            dict_data=dict()
            print('request.data ',request.data['uid'])
            alltasks=objrmse.getAllTasksByUser(request.data['uid'])
            print('alltasks ',alltasks)    
            for irow  in alltasks:       
                dict_data['start']= alltasks[irow]["end_date"]     
                dict_data['Task_Name']= alltasks[irow]["Task_Name"]  
                if alltasks[irow]["css"]=='text-danger':
                    dict_data['className']=alltasks[irow]["css"]
                    dict_data['title']= alltasks[irow]["Task_ID"] 
                    dict_data['description']=dict_data['Task_Name'] + " "+str(alltasks[irow]["datedif"])+" days overdue."        
                else:
                    dict_data['className']=alltasks[irow]["css"]
                    dict_data['title']=alltasks[irow]["Task_ID"] 
                    dict_data['description']=dict_data['Task_Name'] + " "+str(alltasks[irow]["datedif"])+" days to end."
                all_data_lst.append(dict_data.copy()) 
            context={'all_data_lst':json.dumps(all_data_lst)}    
            print('context ',context)
            return Response( context, status=status.HTTP_200_OK)
           
        except Exception as e: 
            print('stacktrace ',traceback.print_exc())
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class getIssues(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            print("rmse_calendar_issue",request.POST,request.GET)
            all_data_lst=list()
            dict_data=dict()
            allissues=objrmse.getAllIssuesByUser('9')
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


def modelfields(request): 
    fields_obj = ModelsFields.objects.all()
    return render(request, 'modelfields.html',{'actPage':'RMSE - Model Fields','fields_obj':fields_obj})

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
        overview_obj = MdlOverview.objects.get(mdl_id = id)
        print("overview_obj",overview_obj.func)
        if overview_obj.func != None:
            func = ModelFunctionMaster.objects.get(mdl_fncn_aid = overview_obj.func)
            func_label = func.mdl_fncn_label
            func_id = func.mdl_fncn_aid
        else: 
            func = ''
            func_label = ''
            func_id = ''
        department = Department.objects.get(dept_aid = overview_obj.department)
        model_source = ModelSourceMaster.objects.get(mdl_scr_aid = overview_obj.mdl_source)
        print("mdl_type",overview_obj.mdl_type)
        if overview_obj.mdl_type != 0:
            model_type = ModelTypeMaster.objects.get(mdl_type_aid = overview_obj.mdl_type)
        else:
            model_type = ''
        print("prdd master",overview_obj.prctaddr)
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
        print("mdl risk aid", model_risk_obj.mdl_risks)
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

        Upstr_Model=objreg.getMdlUpstrem(request.session['uid'])

        Dwstr_Model=objreg.getMdlUpstrem(request.session['uid']) #objreg.getMdlDwStream()
  
        Motr_Freq=objreg.getMontrFreq()  
    
        return render(request, 'editregistermodel.html',{ 'actPage':'Edit Model','department':department.dept_label,"func":func_label,"func_id":func_id,'Mdl_Func':Mdl_Func,'reg_date':overview_obj.reg_dt,'mdl_id':overview_obj.mdl_id,'overview_obj':overview_obj,'Mdl_Src':Mdl_Src,'mdl_source':model_source,'Mdl_Type':Mdl_Type,'model_type':model_type,'Prd_Addr':Prd_Addr,"prd_add":prd_addr,'Mdl_Usage_Frq':Mdl_Usage_Frq,'frequency':frequency,'Reliance':Reliance,
        'Materiality':Materiality,'Intrinsic':Intrinsic,'Mdl_Risk':Mdl_Risk,'model_risk_obj':model_risk_obj,'model_risk':model_risk,'intr_risk':intr_risk,'reliance':reliance,'materiality':materiality,'Mdl_Owners':Mdl_Owners,'Mdl_Devs':Mdl_Devs,'Mdl_Validators':Mdl_Validators,'Upstr_Model':Upstr_Model,'Dwstr_Model':Dwstr_Model,'upstream':upstream,'dwnstream':dwnstream,'Motr_Freq':Motr_Freq})
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
    instance = objdbops.insertRow("DELETE FROM Mdl_Relevant_personnel WHERE Mdl_Id='"+MdlId+"' and u_type='"+UType+"'")
    print("check instance",instance)
    for ids in UIds:
        rel_per_obj  = MdlRelevantPersonnel(mdl_id=MdlId,u_type=UType,u_id=ids,updatedby=updatedby,updatedate=datetime.now())
        rel_per_obj.save()
        print("save------------------")

def updateregmodel(request):
    print("update reg model")
    try:
        print("request",request.POST)
        request_data = {x:request.POST.get(x) for x in request.POST.keys()}
        print("request_data",request_data)   
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
        overview_obj = MdlOverview.objects.filter(mdl_id=request_data['mdl_id']).update(department=dept_obj.dept_aid,func=request_data['function'],mdl_id=request_data['mdl_id'],prm_name=request_data['prm_name'],sec_name=request_data['sec_name'],mdl_source=request_data['mdl_source'],mdl_type=request_data['Mdl_type'],mdl_absct=request_data['mdl_abstract'],mdl_objective=request_data['mdl_objective'],mdl_appl=request_data['mdl_app'],mdl_risk_anls=request_data['mdl_risk_anals'],prctaddr=request_data['pro_addr'],usgfreq=request_data['usage_freq'])
        print('--------------1')
        dict1_overview_obj = convrt_to_dictionary(MdlOverview,request_data['mdl_id'])
        print("overview_obj",dict1_overview_obj)
        overviewlistcolms = [key for key,val in dict1_overview.items() if key in dict1_overview_obj if dict1_overview_obj[key] != val]
        print("changed columns",overviewlistcolms)
        
        #Model Risk
        dict_mdlrisk = convrt_to_dictionary(MdlRisks,request_data['mdl_id'])
        print("mdlrisk",dict_mdlrisk)
        mdl_risk_obj = MdlRisks.objects.filter(mdl_id=request_data['mdl_id']).update(mdl_risks=request_data['mdl_risk'],intr_risk=request_data['intr_risk'],reliance=request_data['reliance'],materiality=request_data['materiality'],risk_mtgn=request_data['risk_miti'],fair_lndg=request_data['fair_lendg'])         
        dict_mdlrisk_obj = convrt_to_dictionary(MdlRisks,request_data['mdl_id'])
        print("mdlrisk",dict_mdlrisk)
        print('--------------2')
        modelriskcolms = [key for key,val in dict_mdlrisk.items() if key in dict_mdlrisk_obj if dict_mdlrisk_obj[key] != val]
        print("changed columns risk",modelriskcolms)
        #Relevent Personnal
        ddlOwner = request.POST.getlist('mdl_owner')
        print("ddlowner",ddlOwner)
        if len(ddlOwner) != 0:
            mdlrelv_personal(request_data['mdl_id'],'Owner',ddlOwner,request.session['uid'])
            print("owner save")
        
        ddldevloper = request.POST.getlist('mdl_devlpr')
        if len(ddldevloper) != 0:
            mdlrelv_personal(request_data['mdl_id'],'Devloper',ddldevloper,request.session['uid'])        

        ddluser = request.POST.getlist('mdl_user')
        if len(ddluser) != 0:
            mdlrelv_personal(request_data['mdl_id'],'User',ddluser,request.session['uid'])

        ddlprdxnsupp = request.POST.getlist('prdxn_support')
        if len(ddlprdxnsupp) != 0:
            mdlrelv_personal(request_data['mdl_id'],'PrdnSupport',ddlprdxnsupp,request.session['uid'])
        
        #Model Dependancies
        dependancy = convrt_to_dictionary(MdlDependencies,request_data['mdl_id'])
        print("dependancy",dependancy)
        mdl_depndncy_obj = MdlDependencies.objects.filter(mdl_id=request_data['mdl_id']).update(upstrmmdl=request_data['upstream'],dwstrmmdl=request_data['dwnstram'])
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
        print('--------------3')
        data = {"isvalid":"true"}
        return JsonResponse(data)
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc())

def issubmit(request): 
    
    request_data = {x:request.GET.get(x) for x in request.GET.keys()} 
    mrm_head=objmaster.getMRMHead()
    try:
        issub_obj = MdlOverview.objects.get(mdl_id = request_data['mdl_id'] )#, is_submit__isnull=True
        if issub_obj:             
            obj = MdlOverview.objects.filter(mdl_id = request_data['mdl_id']).update(is_submit=request_data['is_submit']) 
            print('inside 0 ',  request_data['is_submit'], str(request_data['is_submit'])=="0")        
            if(request_data['is_submit']==1):
                notification_trigger= "New Model registered - " +  request_data['mdl_id']
                objmaster.insert_notification(request.session['uid'],mrm_head,"Model",notification_trigger,1)
            elif(request_data['is_submit']==2):
                notification_trigger= "Edit request for - " +  request_data['mdl_id']
                objmaster.insert_notification(request.session['uid'],mrm_head,"Model",notification_trigger,1)
            elif(str(request_data['is_submit'])=="0"):
                notification_trigger= "Edit request approved - " +  request_data['mdl_id']
                
                print('inside 0 ',request.session['uid'],issub_obj.addedby,"Model",notification_trigger,1)
                objmaster.insert_notification(request.session['uid'],issub_obj.addedby,"Model",notification_trigger,1)
            return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print('issubmit is ',e)
        print('issubmit traceback is ', traceback.print_exc())
        return JsonResponse({"isvalid":"false"})
    
class save_OnlyQuestion_allocation(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):     
        try:
            mdlid =request.data['vt_mdl']
            question_ids = request.data['question_aid']
            users = request.data['users']
            end_date=request.data['end_date']
            strQ="delete from Question_Allocation where model_id='"+mdlid +"'"   
            objdbops.insertRow(strQ)
            # end_date = request_data['end_date'][6:] + "-" + request_data['end_date'][3:5] + "-" + request_data['end_date'][:2]
            for user, question_id in [(x,y) for x in users for y in question_ids]:
                strQ="INSERT INTO Question_Allocation(Question_AID,Allocated_to,AddedBy,AddDate,Model_Id)  VALUES ("
                strQ +=question_id+",'"+user+"',"+str(request.data['uid'])+",getdate(),'"+ mdlid +"')"
                objdbops.insertRow(strQ)
                #allocate_obj = QuestionAllocation(question_aid = question_id,allocated_to = user,end_date = None,model_id=mdlid)
                #allocate_obj.save()
            objvalidation.autoCreateTask(users,mdlid,request.data['uid'],request.data['uid'],end_date,request.data['dept'],"Model Validation Questions Assigned")
            return JsonResponse({"isvalid":"true"}, status=status.HTTP_200_OK)
        except Exception as e: 
            print(str(e))
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

def showrolesrespqtn(request):
    try: 
        qtnobj = RolesResponsibilityQuestion.objects.all()
        return render(request, 'rolesresponsibilityqtn.html',{'actPage' :'RMSE - Roles Responsibility Question','qtnobj':qtnobj})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())

def newrolesrespqtn(request):
    try:   
        return render(request, 'addrolesrespqtn.html',{'actPage':'RMSE - Add Task Function'})
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
        return render(request, 'auditregcompl.html',{'actPage' :'RMSE - Task Function','cmplobj':cmplobj})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())

def newauditregcompl(request):
    try:   
        return render(request, 'addauditregcompl.html',{'actPage':'RMSE - Add Audit Reg Compl'})
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
        return render(request, 'Audit_Allocation.html',{'actPage':'RMSE - Audit Reg Compl Response','obj':users,'questions':lst})
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

class newauditresponse(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:   
            # mdl_id = request.session['vt_mdl']
            lst = []
            users=[]
            selected_id="" 
            addedby = request.data['uid']
            if request.data['method'] == 'POST':   
                mdl_id = request.data['mdl_id'] 
                selected_id=mdl_id           
                
                
                strQ="select arc.* from Audit_Reg_Compl arc,"
                strQ +=" ( select Compl_AID from Audit_Reg_Compl_Allocation"
                strQ +=" where mdl_id='"+ mdl_id +"')a"
                strQ +=" where a.Compl_AID=arc.Compl_AID order by addedon"
                
                tableResult =objdbops.getTable(strQ)  
                users = tableResult.to_json(orient='index')
                users = json.loads(users) 
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
            
            
            allocation_obj = AuditRegComplAllocation.objects.filter(allocated_to=addedby).values_list('mdl_id',flat=True).distinct()       
            model_id = []
            for i in allocation_obj:
                print("i",i)
                model_id.append(i)
            

            
            return Response({'selected_id':selected_id,'obj':users,'questions':lst,'mdl_id':model_id}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

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

class saveauditresponse(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:     
            
            mdl_id = request.data['mdl_id']
            response_obj = AuditRegComplResp.objects.filter(Q(compl_aid = request.data['compl_id']) & Q(mdl_id =mdl_id))
            if response_obj:
                print('record exists')
                response_obj.update(question_resp = request.data['response'],addedby=request.data['uid'],addedon=datetime.now())
                return Response({"isvalid":"true"}, status=status.HTTP_200_OK)   
            else:
                print('record do not exists')
                obj = AuditRegComplResp(question_resp = request.data['response'],compl_aid=request.data['compl_id'],mdl_id = mdl_id,addedby=request.data['uid'],addedon=datetime.now())
                obj.save()
                return Response({"isvalid":"true"}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)



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
        return render(request, 'Question_Allocation.html',{'actPage':'RMSE - Responsibility Question Allocation','obj':users,'questions':lst})
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
    
class newquestionresponseapi(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:   
            print('inside newquestin')        
            lst = []
            users=[]
            mdl_id="" 
            addedby = request.data['uid']
            if request.data['method'] == 'POST':   
                mdl_id = request.data['mdl_id'] 
                strQ="select arc.* from Roles_Responsibility_Question arc,"
                strQ +=" (select Qtn_AID from Roles_Responsibility_Question "
                strQ += "where (Is_Active=1 and Is_Global=1) or (Is_Active=1 and addedby='"+str(addedby)+"')"
                strQ +=" except "  
                strQ +=" select Qtn_AID from Roles_Responsibility_Question_Allocation"
                strQ +=" where mdl_id='"+ mdl_id +"')a"
                strQ +=" where a.Qtn_AID=arc.Qtn_AID order by addedon"
            
                tableResult =objdbops.getTable(strQ)  
                users = tableResult.to_json(orient='index')
                users = json.loads(users)            
            
                strQ="  select   arc.Qtn_AID\
                        ,arc.[Mdl_Id]\
                        ,isNull(Qtn_Resp,'') Question_Resp,question_text from Roles_Responsibility_Question_Response arcr right join Roles_Responsibility_Question_Allocation arc\
                        on arc.[Qtn_AID]=arcr.[Qtn_AID],Roles_Responsibility_Question Audit_Reg_Compl where \
                        Audit_Reg_Compl.[Qtn_AID]=arc.[Qtn_AID] and\
                        arc.mdl_id='"+mdl_id+"' and arc.[Allocated_to]="+str(addedby)+" group by  arc.[Qtn_AID]      ,arc.[Mdl_Id]      , Qtn_Resp,question_text, arcr.[addedon]\
                        order by arcr.[addedon]"
                tableResult =objdbops.getTable(strQ)
                for index, row in  tableResult.iterrows():             
                    dict = {}             
                    dict['qtn_id'] = row['Qtn_AID']
                    dict['question_text'] = row['question_text']
                    dict['Question_Resp']= row['Question_Resp']
                    lst.append(dict) 

            allocation_obj = RolesResponsibilityQuestionAllocation.objects.filter(allocated_to=addedby).values_list('mdl_id',flat=True).distinct()       
            model_id = []
            for i in allocation_obj:
                print("i",i)
                model_id.append(i)

            return Response({'selected_id':mdl_id,'mdl_id':model_id,'obj':users,'questions':lst}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class savequestionresponse(APIView):    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:  
            mdl_id = request.data['mdl_id'] 
            qtn_respi_obj = RolesResponsibilityQuestionResponse.objects.filter(Q(qtn_aid = request.data['qtn_id']) & Q(mdl_id =mdl_id))
            if qtn_respi_obj:
                qtn_respi_obj.update(qtn_resp = request.data['response'],addedby=request.data['uid'],addedon=datetime.now())
            else:
                obj = RolesResponsibilityQuestionResponse(qtn_resp = request.data['response'],qtn_aid=request.data['qtn_id'],mdl_id = mdl_id,addedby=request.session['uid'],addedon=datetime.now())
                obj.save()
            return JsonResponse({"isvalid":"true"})
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

class save_activity_trail(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try: 
            refference_id=request.data['refference_id']
            activity_trigger=request.data['activity_trigger']
            activity_details=request.data['activity_details']
            addedby=request.data['addedby']
            if activity_trigger == '1':
                trigger = 'Model Created'
            elif activity_trigger == '2':
                trigger = 'Model Submitted'
            elif activity_trigger == '3':
                trigger = 'Edit Request submitted.'
            elif activity_trigger == '4':
                trigger = 'Edit Request Approved.'
            elif activity_trigger == '5':
                trigger = 'Decommission Requested.'
            elif activity_trigger == '6':
                trigger = 'Decommission Approved.'
            elif activity_trigger == '7':
                trigger = 'Task Created.'
            elif activity_trigger == '8':
                trigger = 'Task Updated.'
            elif activity_trigger == '9':
                trigger = 'Task Approved.'
            elif activity_trigger == '10':
                trigger = 'Issue Created.'
            elif activity_trigger == '11':
                trigger = 'Issue Updated.'
            elif activity_trigger == '12':
                trigger = 'Issue Approved.'
            elif activity_trigger == '13':
                trigger = 'Model Question(s) Updated.'
            elif activity_trigger == '14':
                trigger = 'Audit & Regulatory Compliance Question(s) Updated.'
            elif activity_trigger == '15':
                trigger = 'Roles Responsibility Question(s) Updated.'
            elif activity_trigger == '16':
                trigger = 'ICQ Question(s) Updated.'
            elif activity_trigger == '17':
                trigger = 'Model Data Imported.'
            elif activity_trigger == '18':
                trigger = 'Target Variable Set.'
            elif activity_trigger == '19':
                trigger = 'Data Updated.'
            elif activity_trigger == '20':
                trigger = 'Data Type Changed.'
            elif activity_trigger == '21':
                trigger = 'Data Visualization Done.'
            elif activity_trigger == '22':
                trigger = 'Data Preparation Done.'
            elif activity_trigger == '23':
                trigger = 'ML Modeling Done.'
            elif activity_trigger == '24':
                trigger = 'Model Validation Done.'
            elif activity_trigger == '25':
                trigger = 'Model Validation Report Generated.'
            elif activity_trigger == '26':
                trigger = 'Data Segement Created.'
            elif activity_trigger == '27':
                trigger = ''
            elif activity_trigger == '28':
                trigger = ''
            elif activity_trigger == '29':
                trigger = ''
            elif activity_trigger == '30':
                trigger = ''
            elif activity_trigger == '31':
                trigger = ''
            elif activity_trigger == '32':
                trigger = ''
            elif activity_trigger == '33':
                trigger = ''
            elif activity_trigger == '34':
                trigger = ''
            elif activity_trigger == '35':
                trigger = ''
            else:
                pass
            trail_obj = ActivityTrail(refference_id  = refference_id,activity_trigger = trigger,activity_details = activity_details,addedby=addedby,added_on=datetime.now(),)
            trail_obj.save()
            return Response({'msg':'Activity saved'}, status=status.HTTP_200_OK)
        except Department.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Department does not exist'}, status=status.HTTP_404_NOT_FOUND)


#jayesh api starts

class DepartmentAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            tasksub = Department.objects.get(dept_aid=id)
            serializer = DepartmentSerializer(tasksub)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        deptnmaster = Department.objects.all()
        serializer =  DepartmentSerializer(deptnmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_   data department",request.data)
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Department is created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
class updatedepartment(APIView):    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = Department.objects.get(dept_aid=id)

        except Department.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Department does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DepartmentSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Department is Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    




class TaskPriorityMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            taskfun = TaskPriorityMaster.objects.get(task_priority_aid=id)
            serializer = TaskPriorityMasterSerializer(taskfun)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        taskprioritymaster = TaskPriorityMaster.objects.all()
        serializer =  TaskPriorityMasterSerializer(taskprioritymaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = TaskPriorityMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'TaskPriorityMaster created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = TaskPriorityMaster.objects.get(task_priority_aid=id)

        except TaskPriorityMaster.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Task Priority does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskPriorityMasterSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Task Priority Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)



class TaskFunctionMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            taskfun = TaskFunctionMaster.objects.get(task_function_aid=id)
            serializer = TaskFunctionMasterSerializer(taskfun)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        taskfunctionmaster = TaskFunctionMaster.objects.all()
        serializer =  TaskFunctionMasterSerializer(taskfunctionmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = TaskFunctionMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'TaskFunctionMaster created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = TaskFunctionMaster.objects.get(task_function_aid=id)

        except TaskFunctionMaster.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Task Function does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskFunctionMasterSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Task Function Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)


class TaskTypeMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            tasktype = TaskTypeMaster.objects.get(task_type_aid=id)
            serializer = TaskTypeMasterSerializer(tasktype)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        tasktypemaster = TaskTypeMaster.objects.all()
        serializer =  TaskTypeMasterSerializer(tasktypemaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = TaskTypeMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'TaskTypeMaster created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = TaskTypeMaster.objects.get(task_type_aid=id)

        except TaskTypeMaster.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Task Type does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskTypeMasterSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Task Type Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

    


class TaskApprovalstatusMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            taskappr = TaskApprovalstatusMaster.objects.get(task_approvalstatus_aid=id)
            serializer = TaskApprovalstatusMasterSerializer(taskappr)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        taskapprovalstatusmaster = TaskApprovalstatusMaster.objects.all()
        serializer =  TaskApprovalstatusMasterSerializer(taskapprovalstatusmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = TaskApprovalstatusMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'TaskApprovalstatusMaster created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = TaskApprovalstatusMaster.objects.get(task_approvalstatus_aid=id)

        except TaskApprovalstatusMaster.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Task Approval Status does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskApprovalstatusMasterSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Task Approval Status Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class SubTasktypeMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            tasksub = SubTasktypeMaster.objects.get(sub_task_type_aid=id)
            serializer = SubTasktypeMasterSerializer(tasksub)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        subtasktypemaster = SubTasktypeMaster.objects.all()
        serializer = SubTasktypeMasterSerializer(subtasktypemaster,many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = SubTasktypeMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'SubTasktypeMaster created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = SubTasktypeMaster.objects.get(sub_task_type_aid=id)

        except SubTasktypeMaster.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Sub Task Type does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubTasktypeMasterSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Sub Task Type Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)


#jayesh api ends

## Nilesh sir's  code ##

class Save_Performance_Monitoring_Result(APIView):
    permission_classes=[IsAuthenticated]  
    def post(self,request):    
        try:
            strQ="delete from Performance_Monitoring_Result where Mdl_ID='"+str(request.data['Mdl_ID'])+"' and Metric="+ str(request.data['Metric']) + " and freq_idx="+ str(request.data['freq_idx'])
            objdbops.insertRow(strQ) 

            strQ="INSERT INTO Performance_Monitoring_Result(Mdl_ID,Metric,Prdn_Value,Metric_flag,Added_by,Added_On,freq_idx,freq_val)  VALUES ("
            strQ +="'"+str(request.data['Mdl_ID'])+"',"+request.data['Metric']+",'"+str(request.data['Prdn_Value'])+"','"+str(request.data['Metric_flag'])+"','"+str(request.data['addedby'])+"',getdate(),"+str(request.data['freq_idx'])+",getdate())"
            #print("strQ Insert ",strQ)
            objdbops.insertRow(strQ)
            return Response({'data':"",'msg':'Model Matrics Updated Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            print("error ",e, traceback.print_exc())
            return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class Save_Performance_Monitoring_Override_History(APIView):
    permission_classes=[IsAuthenticated]  
    def post(self,request):    
        try:   
            strQ="delete from Performance_Monitoring_Final_Result where Mdl_ID='"+str(request.data['Mdl_ID']) +"'  and Metric="+ str(request.data['Metric']) + " and freq_idx="+str(request.data['freq_idx'])
            objdbops.insertRow(strQ) 
   
            strQ="INSERT INTO Performance_Monitoring_Override_History(Mdl_ID,Metric,New_Value,Added_by,Added_On,freq_idx,freq_val)  VALUES ("
            strQ +="'"+str(request.data['Mdl_ID'])+"',"+str(request.data['Metric'])+",'"+str(request.data['New_Value'])+"','"+str(request.data['Added_by'])+"',getdate(),"+str(request.data['freq_idx'])+",getdate())"
             
            objdbops.insertRow(strQ)
            modelmetric=ModelMetricMaster.objects.get(mm_aid=request.data['Metric'])
            mrmheadId=objmaster.getMRMHead()
            # print('modelmetric ',modelmetric.mm_label)
            # userobj = objreg.getMdlOwnerById(request.data['Mdl_ID'],'Owner')   
            # for obj,val in userobj.items():
            #     notification_trigger= "Model  "+ request.data['Mdl_ID'] +" performance value overriden for "+modelmetric.mm_label
            #     objmaster.insert_notification(str(request.data['Added_by']),val['u_Aid'],"Peformance Overriden",notification_trigger,1)
             
            trail_obj = ActivityTrail(refference_id  = request.data['Mdl_ID'],activity_trigger = "Peformance Overriden.",activity_details = "Model performance value overriden for "+modelmetric.mm_label+ " from "+request.data['Old_Value']+ " to "+request.data['New_Value'],addedby=request.data['Added_by'],added_on=datetime.now(),)
            trail_obj.save()
            return Response({'data':"",'msg':'Model Matrics Updated Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            print("error ",e, traceback.print_exc())
            return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
        

class Update_Performance_Monitoring_Override_History(APIView):     
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            maxaid=objdbops.getscalar("select max(aid)   from Performance_Monitoring_Override_History where Mdl_ID='"+str(request.data['Mdl_ID']) +"'  and Metric="+ str(request.data['Metric']) + " and freq_idx="+str(request.data['freq_idx']))
            strQ="update Performance_Monitoring_Override_History set MO_Approval=1, MO_Approved_On=getdate() where aid="+ str(maxaid) +" and Mdl_ID='"+str(request.data['Mdl_ID']) +"'  and Metric="+ str(request.data['Metric']) + " and freq_idx="+str(request.data['freq_idx'])
            objdbops.insertRow(strQ) 
            return Response({'data':"",'msg':'Model Matrics Updated Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
        
class Save_Performance_Monitoring_Final_Result(APIView):
    permission_classes=[IsAuthenticated]  
    def post(self,request):    
        try:
            strQ="delete from Performance_Monitoring_Final_Result where Mdl_ID='"+str(request.data['Mdl_ID']) +"'  and Metric="+request.data['Metric'] + " and freq_idx="+request.data['freq_idx']
            objdbops.insertRow(strQ) 

            strQ="INSERT INTO Performance_Monitoring_Final_Result(Mdl_ID,Metric,Metric_flag,Added_by,Added_On,freq_idx,freq_val)  VALUES ("
            strQ +="'"+str(request.data['Mdl_ID'])+"',"+request.data['Metric']+",'"+str(request.data['New_Value'])+"','"+str(request.data['Added_by'])+"',getdate(),"+request.data['freq_idx']+"',getdate())"
            
            objdbops.insertRow(strQ)

            return Response({'data':"",'msg':'Model Matrics Updated Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            print("error ",e, traceback.print_exc())
            return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

## End ##

class Save_Data_Monitoring_Result(APIView):
    permission_classes=[IsAuthenticated]  
    def post(self,request):    
        try:
            strQ="delete from Data_Monitoring_Result where Mdl_ID='"+str(request.data['Mdl_ID'])+"' and Metric="+ str(request.data['Metric']) +" and Feature="+str(request.data['Feature']) +" and freq_idx="+ str(request.data['freq_idx'])
            objdbops.insertRow(strQ) 

            strQ="INSERT INTO Performance_Monitoring_Result(Mdl_ID,Metric,Feature,Prdn_Value,Metric_flag,Added_by,Added_On,freq_idx,freq_val)  VALUES ("
            strQ +="'"+str(request.data['Mdl_ID'])+"',"+request.data['Metric']+",'"+str(request.data['Feature'])+"','"+str(request.data['Prdn_Value'])+"','"+str(request.data['Metric_flag'])+"','"+str(request.data['addedby'])+"',getdate(),"+str(request.data['freq_idx'])+",getdate())"
            #print("strQ Insert ",strQ)
            objdbops.insertRow(strQ)
            return Response({'data':"",'msg':'Model Matrics Updated Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            print("error ",e, traceback.print_exc())
            return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class Save_Data_Monitoring_Override_History(APIView):
    permission_classes=[IsAuthenticated]  
    def post(self,request): 
        print("request data history",request.data)   
        try:   
            strQ="delete from Data_Monitoring_Final_Result where Mdl_ID='"+str(request.data['Mdl_ID']) +"'  and Metric="+ str(request.data['Metric']) +" and Feature="+str(request.data['Feature']) +" and freq_idx="+str(request.data['freq_idx'])
            objdbops.insertRow(strQ) 
   
            strQ="INSERT INTO Data_Monitoring_Override_History(Mdl_ID,Metric,Feature,Threshold,Warning,Actual,New_Value,old_Value,Added_by,Added_On,freq_idx,freq_val)  VALUES ("
            strQ +="'"+str(request.data['Mdl_ID'])+"',"+str(request.data['Metric'])+",'"+str(request.data['Feature'])+"','"+str(request.data['Threshold'])+"','"+str(request.data['Warning'])+"','"+str(request.data['Actual'])+"','"+str(request.data['New_Value'])+"','"+str(request.data['Old_Value'])+"','"+str(request.data['Added_by'])+"',getdate(),"+str(request.data['freq_idx'])+",getdate())"
             
            objdbops.insertRow(strQ)
            datametric=DataMetricMaster.objects.get(data_aid=request.data['Metric'])
            mrmheadId=objmaster.getMRMHead()
            # print('modelmetric ',modelmetric.mm_label)
            # userobj = objreg.getMdlOwnerById(request.data['Mdl_ID'],'Owner')   
            # for obj,val in userobj.items():
            #     notification_trigger= "Model  "+ request.data['Mdl_ID'] +" performance value overriden for "+modelmetric.mm_label
            #     objmaster.insert_notification(str(request.data['Added_by']),val['u_Aid'],"Peformance Overriden",notification_trigger,1)
            notification_trigger= "Model  "+ request.data['Mdl_ID'] +" Data Matric value overriden for "+datametric.data_label
            objmaster.insert_notification(str(request.data['Added_by']),mrmheadId,"Data Matric Overriden",notification_trigger,1)
            print("-------------------------Not TRig")
            trail_obj = ActivityTrail(refference_id  = request.data['Mdl_ID'],activity_trigger = "Data Matric Overriden.",activity_details = "Model Data Matric value overriden for "+datametric.data_label+ " from "+request.data['Old_Value']+ " to "+request.data['New_Value'],addedby=request.data['Added_by'],added_on=datetime.now(),)
            trail_obj.save()
            print("-------------------------Activity Trail")
            return Response({'data':"",'msg':'Model Matrics Updated Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            print("error ",e, traceback.print_exc())
            return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
        

class Update_Data_Monitoring_Override_History(APIView):     
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            print("request data-------------------1",request.data)
            maxaid=objdbops.getscalar("select max(AID)   from Data_Monitoring_Override_History where Mdl_ID='"+str(request.data['Mdl_ID']) +"'  and Metric="+ str(request.data['Metric']) +" and Feature='"+str(request.data['Feature']) +"' and freq_idx="+str(request.data['freq_idx']))
            strQ="update Data_Monitoring_Override_History set MO_Approval=1, MO_Approved_On=getdate() where AID="+ str(maxaid) +" and Mdl_ID='"+str(request.data['Mdl_ID']) +"'  and Metric="+ str(request.data['Metric']) + " and Feature='"+str(request.data['Feature']) +"' and freq_idx="+str(request.data['freq_idx'])
            print('strq check---------------',strQ)
            objdbops.insertRow(strQ) 

            datametric=DataMetricMaster.objects.get(data_aid=request.data['Metric'])
            mrmheadId=objmaster.getMRMHead()
            
            notification_trigger= "Model  "+ request.data['Mdl_ID'] +" Data Matric value overriden for "+datametric.data_label
            objmaster.insert_notification(str(request.data['Added_by']),mrmheadId,"Data Matric Overriden",notification_trigger,1)
            print("-------------------------Not TRig")
            trail_obj = ActivityTrail(refference_id  = request.data['Mdl_ID'],activity_trigger = "Data Matric Overriden.",activity_details = "Model Data Matric value overriden for "+datametric.data_label+ " from "+str(request.data['Old_Value'])+ " to "+str(request.data['New_Value']),addedby=request.data['Added_by'],added_on=datetime.now())
            trail_obj.save()
            print("-------------------------Activity Trail")
            return Response({'data':"",'msg':'Model Matrics Updated Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            print("error is-----",e)
            return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
        
class Save_Data_Monitoring_Final_Result(APIView):
    permission_classes=[IsAuthenticated]  
    def post(self,request):  
        print("request data final result",request.data)   
        try:
            strQ="delete from Data_Monitoring_Final_Result where Mdl_ID='"+str(request.data['Mdl_ID']) +"'  and Metric="+str(request.data['Metric']) + " and Feature='"+str(request.data['Feature']) +"' and freq_idx="+str(request.data['freq_idx'])
            objdbops.insertRow(strQ) 

            # strQ="INSERT INTO Data_Monitoring_Final_Result(Mdl_ID,Metric,Feature,Metric_flag,Added_by,Added_On,freq_idx,freq_val)  VALUES ("
            # strQ +="'"+str(request.data['Mdl_ID'])+"',"+request.data['Metric']+",'"+str(request.data['Feature'])+"','"+str(request.data['New_Value'])+"','"+str(request.data['Added_by'])+"',getdate(),"+request.data['freq_idx']+"',getdate())"

            strQ="INSERT INTO Data_Monitoring_Final_Result(Mdl_ID,Metric,Feature,Threshold,Warning,Actual,Added_by,Added_On,freq_idx,freq_val)  VALUES ("
            strQ +="'"+str(request.data['Mdl_ID'])+"',"+str(request.data['Metric'])+",'"+str(request.data['Feature'])+"','"+str(request.data['Threshold'])+"','"+str(request.data['Warning'])+"','"+str(request.data['Actual'])+"','"+str(request.data['Added_by'])+"',getdate(),"+str(request.data['freq_idx'])+",getdate())"
            
            objdbops.insertRow(strQ)

            datametric=DataMetricMaster.objects.get(data_aid=request.data['Metric'])
            mrmheadId=objmaster.getMRMHead()
            
            notification_trigger= "Model  "+ request.data['Mdl_ID'] +" Data Matric value overriden for "+datametric.data_label
            objmaster.insert_notification(str(request.data['Added_by']),mrmheadId,"Data Matric Overriden",notification_trigger,1)
            print("-------------------------Not TRig")
            trail_obj = ActivityTrail(refference_id  = request.data['Mdl_ID'],activity_trigger = "Data Matric Overriden.",activity_details = "Model Data Matric value overriden for "+datametric.data_label+ " from "+request.data['Old_Value']+ " to "+request.data['New_Value'],addedby=request.data['Added_by'],added_on=datetime.now(),)
            trail_obj.save()
            print("-------------------------Activity Trail")

            return Response({'data':"",'msg':'Model Matrics Updated Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            print("error ",e, traceback.print_exc())
            return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class getMaxFreqSeq(APIView):
    permission_classes=[IsAuthenticated]
    objdbops =None
    def __init__(self):
        self.objdbops=dbops()
    def get(self,request):
        strQ="select case ( SELECT   distinct Frequency   FROM  Performance_Monitoring_Setup where mdl_id='"+request.data['mdl_id']+"')"
        strQ+="    when 1 then case when  getdate() =  max(freq_val) then '0' else '1' end "
        strQ+="        when 2 then case when DATEPART(WEEK,getdate()) = DATEPART(WEEK, max(freq_val)) then '0' else '1' end "
        strQ+="        when 3 then case when Month(getdate()) = Month(max(freq_val)) then '0' else '1' end "
        strQ+="        when 4 then case when Month(getdate()) = Month(max(freq_val)) then '0' else '1' end else 'New'  end  'addorupdate', case ("
        strQ+="        SELECT   distinct Frequency   FROM  Performance_Monitoring_Setup where mdl_id='"+request.data['mdl_id']+"')"
        strQ+="        when 1 then case when  getdate() =  max(freq_val) then  max(isnull(freq_idx,0)) else  max(isnull(freq_idx,0))+1 end   when 2 then case when DATEPART(WEEK,getdate()) = DATEPART(WEEK, max(freq_val)) then max(isnull(freq_idx,0)) else  max(isnull(freq_idx,0)) +1 end "
        strQ+="        when 3 then case when Month(getdate()) = Month(max(freq_val)) then  max(isnull(freq_idx,0)) else  max(isnull(freq_idx,0))+1 end  when 4 then case when Month(getdate()) = Month(max(freq_val)) then  max(isnull(freq_idx,0)) else   max(isnull(freq_idx,0))+1 end "
        strQ+="        else 1 end 'freqidx'  from Performance_Monitoring_Result_file_info" 
        print("sql query",strQ)       
        tableResult=  self.objdbops.getTable(strQ)  
        freqData= tableResult.to_json(orient='index')   
        # print("freqData-----")
        return Response({'freqData':json.loads(freqData)})
    
class getMaxFreqSeqData(APIView):
    permission_classes=[IsAuthenticated]
    objdbops =None
    def __init__(self):
        self.objdbops=dbops()
    def get(self,request):
        strQ="select case ( SELECT   distinct Frequency   FROM  Data_Monitoring_Setup where mdl_id='"+request.data['mdl_id']+"')"
        strQ+="    when 1 then case when  getdate() =  max(freq_val) then '0' else '1' end "
        strQ+="        when 2 then case when DATEPART(WEEK,getdate()) = DATEPART(WEEK, max(freq_val)) then '0' else '1' end "
        strQ+="        when 3 then case when Month(getdate()) = Month(max(freq_val)) then '0' else '1' end "
        strQ+="        when 4 then case when Month(getdate()) = Month(max(freq_val)) then '0' else '1' end else 'New'  end  'addorupdate', case ("
        strQ+="        SELECT   distinct Frequency   FROM  Data_Monitoring_Setup where mdl_id='"+request.data['mdl_id']+"')"
        strQ+="        when 1 then case when  getdate() =  max(freq_val) then max(isnull(freq_idx,0)) when (select count(*)  from Data_Monitoring_Result_file_info where mdl_id='"+request.data['mdl_id']+"')=0 then 1 else  max(isnull(freq_idx,0))+1 end     when 2 then case when DATEPART(WEEK,getdate()) = DATEPART(WEEK, max(freq_val)) then max(isnull(freq_idx,0)) when (select count(*)  from Data_Monitoring_Result_file_info where mdl_id='"+request.data['mdl_id']+"')=0 then 1 else  max(isnull(freq_idx,0))+1  end "
        strQ+="        when 3 then case when Month(getdate()) = Month(max(freq_val)) then max(isnull(freq_idx,0)) when (select count(*)  from Data_Monitoring_Result_file_info where mdl_id='"+request.data['mdl_id']+"')=0 then 1 else   max(isnull(freq_idx,0))+1 end  when 4 then case when Month(getdate()) = Month(max(freq_val)) then max(isnull(freq_idx,0)) when (select count(*)  from Data_Monitoring_Result_file_info where mdl_id='"+request.data['mdl_id']+"')=0 then 1 else   max(isnull(freq_idx,0))+1 end "
        strQ+="        else 1 end 'freqidx'  from Data_Monitoring_Result_file_info where mdl_id='"+request.data['mdl_id']+"'"
        print("strQ-------------------",strQ)        
        tableResult=  self.objdbops.getTable(strQ)  
        freqData= tableResult.to_json(orient='index')   
          
        return Response({'freqData':json.loads(freqData)})

class getMaxFreqSeq_Buss(APIView):
    permission_classes=[IsAuthenticated]
    objdbops =None
    def __init__(self):
        self.objdbops=dbops()
    def get(self,request):
        strQ="select case ( SELECT   distinct Frequency   FROM  Buss_KPI_Monitoring_Setup where mdl_id='"+request.data['mdl_id']+"')"
        strQ+="    when 1 then case when  getdate() =  max(freq_val) then '0' else '1' end "
        strQ+="        when 2 then case when DATEPART(WEEK,getdate()) = DATEPART(WEEK, max(freq_val)) then '0' else '1' end "
        strQ+="        when 3 then case when Month(getdate()) = Month(max(freq_val)) then '0' else '1' end "
        strQ+="        when 4 then case when Month(getdate()) = Month(max(freq_val)) then '0' else '1' end else 'New'  end  'addorupdate', case ("
        strQ+="        SELECT   distinct Frequency   FROM  Buss_KPI_Monitoring_Setup where mdl_id='"+request.data['mdl_id']+"')"
        strQ+="        when 1 then case when  getdate() =  max(freq_val) then  max(isnull(freq_idx,0)) else  isnull(max(isnull(freq_idx,0)),0)+1 end   when 2 then case when DATEPART(WEEK,getdate()) = DATEPART(WEEK, max(freq_val)) then max(isnull(freq_idx,0)) else  max(isnull(freq_idx,0)) +1 end "
        strQ+="        when 3 then case when Month(getdate()) = Month(max(freq_val)) then  max(isnull(freq_idx,0)) else  max(isnull(freq_idx,0))+1 end  when 4 then case when Month(getdate()) = Month(max(freq_val)) then  max(isnull(freq_idx,0)) else   max(isnull(freq_idx,0))+1 end "
        strQ+="        else 1 end 'freqidx'  from Buss_KPI_Monitoring_Final_Result" 
        print("sql query",strQ)       
        tableResult=  self.objdbops.getTable(strQ)  
        freqData= tableResult.to_json(orient='index')   
        # print("freqData-----")
        return Response({'freqData':json.loads(freqData)})
    


class getTemplateData(APIView): 
    objdbops =None

    def __init__(self):
        self.objdbops=dbops()

    def get(self,request):   
        modeldata = PerformanceMonitoringSetup.objects.filter(mdl_id=request.data['mdl_id'])
        serializer_a = PerformanceMonitoringSetupSerializer(modeldata,many=True)  

        strQ = "select hist.metric,new_value from Performance_Monitoring_Override_History hist,("
        strQ += " select max(aid) aid,mdl_id,metric from Performance_Monitoring_Override_History"
        strQ += " group by mdl_id,metric  )maxids"
        strQ += " where maxids.aid=hist.aid and maxids.mdl_id=hist.mdl_id and maxids.metric=hist.metric"
        strQ += " and hist.mdl_id='"+request.data['mdl_id']+"' and freq_idx="+str(request.data['freq_idx'])# to be added later+" and MO_approval<>1"
        print(strQ)
        tableResult=  self.objdbops.getTable(strQ) 
        mdldata= tableResult.to_json(orient='index')  
        return Response({'overdata':json.loads(mdldata),'mmdata':serializer_a.data})


class Update_Performance_Monitoring_Override_History(APIView):     
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            maxaid=objdbops.getscalar("select max(aid)   from Performance_Monitoring_Override_History where Mdl_ID='"+str(request.data['Mdl_ID']) +"'  and Metric="+ str(request.data['Metric']) + " and freq_idx="+str(request.data['freq_idx']))
            strQ="update Performance_Monitoring_Override_History set MO_Approval=1, MO_Approved_On=getdate() where aid="+ str(maxaid) +" and Mdl_ID='"+str(request.data['Mdl_ID']) +"'  and Metric="+ str(request.data['Metric']) + " and freq_idx="+str(request.data['freq_idx'])
            objdbops.insertRow(strQ) 
            return Response({'data':"",'msg':'Model Matrics Updated Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

    
class Perm_Override_MRM(APIView): 
    def get(self,request,id=None): 
        if id:
            usr = ModelOverview.objects.get(u_aid=id)
            serializer = ModelOverviewSerializer(usr)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        modeldata = PerformanceMonitoringSetup.objects.order_by().values('mdl_id').distinct() 
        serializer = PerformanceMonitoringSetupSerializer(modeldata,many=True)
         
        freqmaster = FrequencyMaster.objects.all()
        freqerializer =  FrequencyMasterSerializer(freqmaster,many=True)

        matricsdeptdata = ModelMetricDept.objects.filter(dept_aid=request.data['dept_aid'])
        serializer_a =  ModelMetricDeptSerializer(matricsdeptdata,many=True)

        bmatricsdeptdata = BusinessMetricDept.objects.filter(dept_aid=request.data['dept_aid'])
        serializer_b =  BusinessMetricDeptSerializer(bmatricsdeptdata,many=True)

        dataMntrHstry = DataMonitoringOverrideHistory.objects.order_by().values('mdl_id').distinct()
        dmh_serializer = DataMonitoringOverrideHistorySerializer(dataMntrHstry,many=True)
        print("dataMntrHstry",dmh_serializer.data)
        
        return Response({'mdlids':serializer.data, 'frequency':freqerializer.data,'mdlmetric':serializer_a.data,'bussmetric':serializer_b.data,'dmh_mdlids':dmh_serializer.data}, status=status.HTTP_200_OK)
    

class ReportSectionMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            usr = RptSectionMaster.objects.get(rpt_section_aid=id)
            serializer = RptSectionMasterSerializer(usr)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        RptSection = RptSectionMaster.objects.all()
        serializer =  RptSectionMasterSerializer(RptSection,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        if RptSectionMaster.objects.filter(rpt_section_text = request.data['rpt_section_text']):
            return Response({'msg':'Section Already Exist'})
        else:
            serializer = RptSectionMasterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'msg':'Report Section created Successfully'},status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)

class FLReportSectionMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        print("request_data",request.data)
        if id:
            usr = FlRptSectionMaster.objects.get(fl_rpt_section_aid=id)
            serializer = FLRptSectionMasterSerializer(usr)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        RptSection = FlRptSectionMaster.objects.all()
        serializer =  FLRptSectionMasterSerializer(RptSection,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        if FlRptSectionMaster.objects.filter(rpt_section_text = request.data['rpt_section_text']):
            return Response({'msg':'Section Already Exist'})
        else:
            serializer = FLRptSectionMasterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'msg':'Report Section created Successfully'},status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
    

class ReportSubSectionMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        print("request data section",request.data)
        if request.data['is_taken'] == 'true':
            usr = ReportTemplateTemp.objects.filter(template_name = request.data['template_name'],rpt_section_aid=request.data['rpt_section_aid']).first()
            serializer_a = ReportTemplateTempSerializer(usr,)
            
            secdata = RptSubSectionMaster.objects.filter(rpt_section_aid = request.data['rpt_section_aid'])
            serializer =  RptSubSectionMasterSerializer(secdata,many=True)
            return Response({"status": "success", "data": serializer.data,"data2":serializer_a.data}, status=status.HTTP_200_OK)
        RptSection = RptSubSectionMaster.objects.all()
        serializer =  RptSubSectionMasterSerializer(RptSection,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = RptSubSectionMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Report Sub Section created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
    

class ReportSubSubSectionMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if request.data['is_taken'] == 'true':
            usr = ReportTemplateTemp.objects.filter(template_name = request.data['template_name'],rpt_sub_section_aid=request.data['rpt_sub_section_aid']).first()
            serializer_a = ReportTemplateTempSerializer(usr)

            secdata = RptSubSubSectionMaster.objects.filter(rpt_sub_section_aid = request.data['rpt_sub_section_aid'])
            serializer =  RptSubSubSectionMasterSerializer(secdata,many=True)
            return Response({"status": "success", "data": serializer.data,"data2":serializer_a.data}, status=status.HTTP_200_OK)
        RptSection = RptSubSubSectionMaster.objects.all()
        serializer =  RptSubSubSectionMasterSerializer(RptSection,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = RptSubSubSectionMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Report Sub Sub Section created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)

class ReportTemplateTempAPI(APIView):
    permission_classes=[IsAuthenticated]
    # def get(self,request,id=None):
    #     if request.data['is_taken'] == 'true':
    #         usr = RptSubSubSectionMaster.objects.get(rpt_sub_section_aid=request.data['rpt_sub_section_aid'])
    #         serializer = RptSubSubSectionMasterSerializer(usr)
    #         return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    #     RptSection = RptSubSubSectionMaster.objects.all()
    #     serializer =  RptSubSubSectionMasterSerializer(RptSection,many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data",request.data)
        request_data = request.data
        tempobj = ReportTemplateTemp.objects.filter(template_name = request_data['template_name'],rpt_section_aid = request_data['rpt_section_aid'],rpt_sub_section_aid = 0,rpt_sub_sub_section_aid = 0).first()
        mainobj = ReportTemplate.objects.filter(template_name = request_data['template_name'],rpt_section_aid = request_data['rpt_section_aid'],rpt_sub_section_aid = 0,rpt_sub_sub_section_aid = 0).first()
        if tempobj:
            if request_data['rpt_sub_section_aid'] != 0:
                pass
            else:
                return Response({'data':'','msg':'Template section Already Exist'},status=status.HTTP_201_CREATED)
        else:
            pass

        if mainobj:
            if request_data['rpt_sub_section_aid'] != 0:
                pass
            else:
                return Response({'data':'','msg':'Template section Already Exist'},status=status.HTTP_201_CREATED)
        else:
            pass


        tempobj1 = ReportTemplateTemp.objects.filter(template_name = request_data['template_name'],rpt_section_aid = request_data['rpt_section_aid'],rpt_sub_section_aid = request_data['rpt_sub_section_aid'],rpt_sub_sub_section_aid = 0).first()
        mainobj1 = ReportTemplate.objects.filter(template_name = request_data['template_name'],rpt_section_aid = request_data['rpt_section_aid'],rpt_sub_section_aid = request_data['rpt_sub_section_aid'],rpt_sub_sub_section_aid = 0).first()
        if tempobj1:
            if request_data['rpt_sub_sub_section_aid'] != 0:
                pass
            else:
                return Response({'data':'','msg':'Template sub section Already Exist'},status=status.HTTP_201_CREATED)
        else:
            pass

        if mainobj1:
            if request_data['rpt_sub_sub_section_aid'] != 0:
                pass
            else:
                return Response({'data':'','msg':'Template sub section Already Exist'},status=status.HTTP_201_CREATED)
        else:
            pass

        tempobj2 = ReportTemplateTemp.objects.filter(template_name = request_data['template_name'],rpt_section_aid = request_data['rpt_section_aid'],rpt_sub_section_aid = request_data['rpt_sub_section_aid'],rpt_sub_sub_section_aid = request_data['rpt_sub_sub_section_aid']).first()
        mainobj2 = ReportTemplateTemp.objects.filter(template_name = request_data['template_name'],rpt_section_aid = request_data['rpt_section_aid'],rpt_sub_section_aid = request_data['rpt_sub_section_aid'],rpt_sub_sub_section_aid = request_data['rpt_sub_sub_section_aid']).first()
        if tempobj2:
            return Response({'data':'','msg':'Template sub section Already Exist'},status=status.HTTP_201_CREATED)
        else:
            pass

        if mainobj2:
            return Response({'data':'','msg':'Template sub section Already Exist'},status=status.HTTP_201_CREATED)
        else:
            pass
        
        indxsec = ReportTemplateTemp.objects.filter(template_name = request_data['template_name']).last()
        print("indxsec new",indxsec)
        print("------------------1")
        if indxsec == None:
            request_data['index_section'] = 1
            if request_data['rpt_sub_section_aid'] == 0:
                request_data['index_sub_section'] = 0
            else:
                # request_data['index_sub_section'] = 11
                request_data['index_sub_section'] = 1
            if request_data['rpt_sub_sub_section_aid'] == 0:
                request_data['index_sub_sub_section'] = 0
            else:
                # request_data['index_sub_sub_section'] = 111
                request_data['index_sub_sub_section'] = 1
            # request_data['rpt_sub_section_aid'] = int(request.data['rpt_sub_section_aid'])
            # request_data['rpt_sub_sub_section_aid'] = int(request.data['rpt_sub_sub_section_aid'])
        else:
            sec_aid = ReportTemplateTemp.objects.filter(template_name = request_data['template_name'],rpt_section_aid = request_data['rpt_section_aid']).first()
            print("-------------2",sec_aid)
            
            if sec_aid == None:
                latest = ReportTemplateTemp.objects.latest("added_on")
                
                # max_value = ReportTemplateTemp.objects.aggregate(max_value=Max('template_name'))['max_value']
                max_value = ReportTemplateTemp.objects.filter(template_name = request_data['template_name']).aggregate(max_value=Max('index_section'))['max_value']
                request_data['index_section'] = max_value+1
                request_data['index_sub_section'] = 0
                request_data['index_sub_sub_section'] = 0
            else:
                print("--------------3","if")                
                request_data['index_section'] = sec_aid.index_section
                max_value = ReportTemplateTemp.objects.filter(template_name = request_data['template_name'],rpt_section_aid = request_data['rpt_section_aid']).aggregate(max_value=Max('index_sub_section'))['max_value']
                # request_data['index_sub_section'] = str(sec_aid.index_section)+str(1)
                request_data['index_sub_section'] = max_value+1
                indx_sub_sub_scn = ReportTemplateTemp.objects.filter(template_name = request_data['template_name'],rpt_section_aid = request_data['rpt_section_aid'],rpt_sub_sub_section_aid = request_data['rpt_sub_sub_section_aid']).aggregate(max_value=Max('index_sub_sub_section'))['max_value']
                print("indx_sub_sub_scn",indx_sub_sub_scn)
                if indx_sub_sub_scn == None:
                    request_data['index_sub_sub_section'] = 0
                else:
                    request_data['index_sub_sub_section'] = indx_sub_sub_scn
                
            if request_data['rpt_sub_sub_section_aid'] == 0:
                pass
            else:
                sub_sec_aid = ReportTemplateTemp.objects.filter(template_name = request_data['template_name'],rpt_section_aid = request_data['rpt_section_aid'],rpt_sub_section_aid = request_data['rpt_sub_section_aid']).first()
                if sub_sec_aid == None:
                    latest = ReportTemplateTemp.objects.latest("added_on")
                    max_value = ReportTemplateTemp.objects.filter(template_name =  request_data['template_name']).aggregate(max_value=Max('index_sub_section'))['max_value']
                    request_data['index_sub_section']  = max_value+1
                    # request_data['index_sub_sub_section'] = 111
                    request_data['index_sub_sub_section'] = 1
                else:
                    request_data['index_section'] = sub_sec_aid.index_section
                    request_data['index_sub_section'] = sub_sec_aid.index_sub_section
                    max_value = ReportTemplateTemp.objects.filter(template_name = request_data['template_name'],rpt_section_aid = request_data['rpt_section_aid'],rpt_sub_section_aid = request_data['rpt_sub_section_aid']).aggregate(max_value=Max('index_sub_sub_section'))['max_value']
                    if max_value == 0:
                        # request_data['index_sub_sub_section'] = str(sub_sec_aid.index_sub_section)+str(1)
                        request_data['index_sub_sub_section'] = 1
                    else:
                        request_data['index_sub_sub_section'] = int(max_value)+1

                # if sub_sec_aid.rpt_sub_section_aid == request_data['rpt_sub_section_aid']:
                #     request_data['index_sub_section'] = 11
                #     request_data['index_sub_sub_section'] = 111
                # else:
                #     KJB ='L'
                    


            # request_data['index_sub_section'] = indxsec.index_sub_section+1
            # if request_data['rpt_sub_sub_section_aid'] == 0:
            #     request_data['index_sub_sub_section'] = 0
            # else:
            #     # request_data['index_sub_sub_section'] = 1
            #     request_data['index_sub_sub_section'] = indxsec.index_sub_sub_section+1
        print("request data no 2",request_data)
        serializer = ReportTemplateTempSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Report Template created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)


class ReportTemplateAPI(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            print("request template data",request.data)
            tempquerysets = ReportTemplateTemp.objects.filter(template_name = request.data['template_name'])
            print("tempquerysets",tempquerysets)
            data_list = []
            for tempobj in tempquerysets:
                dict = {}
                dict['template_name'] = tempobj.template_name
                dict['department'] = tempobj.department
                dict['rpt_section_aid'] = tempobj.rpt_section_aid
                dict['rpt_sub_section_aid'] = tempobj.rpt_sub_section_aid
                dict['rpt_sub_sub_section_aid'] = tempobj.rpt_sub_sub_section_aid
                dict['index_section'] = tempobj.index_section
                dict['index_sub_section'] = tempobj.index_sub_section
                dict['index_sub_sub_section'] = tempobj.index_sub_sub_section
                dict['added_by'] = tempobj.added_by
                print("--------------1",dict)
                data_list.append(dict)
            print("--------------1",data_list)

            serializer = ReportTemplateSerializer(data=data_list, many=True)
            if serializer.is_valid():
                serializer.save()
                for obj in data_list:
                    obj_to_delete = ReportTemplateTemp.objects.filter(template_name = obj['template_name'])
                    obj_to_delete.delete()
                return Response({'data':serializer.data,'msg':'Report Template submitted Successfully'},status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("error is",e)
            return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)

class FLReportTemplateAPI(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            print("request template data",request.data)
            tempquerysets = FlReportTemplateTemp.objects.filter(template_name = request.data['template_name'])
            print("tempquerysets",tempquerysets)
            data_list = []
            for tempobj in tempquerysets:
                dict = {}
                dict['template_name'] = tempobj.template_name
                dict['department'] = tempobj.department
                dict['rpt_section_aid'] = tempobj.rpt_section_aid
                dict['rpt_sub_section_aid'] = tempobj.rpt_sub_section_aid
                dict['rpt_sub_sub_section_aid'] = tempobj.rpt_sub_sub_section_aid
                dict['index_section'] = tempobj.index_section
                dict['index_sub_section'] = tempobj.index_sub_section
                dict['index_sub_sub_section'] = tempobj.index_sub_sub_section
                dict['added_by'] = tempobj.added_by
                print("--------------1",dict)
                data_list.append(dict)
            print("--------------1",data_list)

            serializer = FLReportTemplateSerializer(data=data_list, many=True)
            if serializer.is_valid():
                serializer.save()
                for obj in data_list:
                    obj_to_delete = FlReportTemplateTemp.objects.filter(template_name = obj['template_name'])
                    obj_to_delete.delete()
                return Response({'data':serializer.data,'msg':'Report Template submitted Successfully'},status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("error is",e)
            return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)


class Fetch_Report_data(APIView):
    permission_classes=[IsAuthenticated]
    objdbops =None

    def __init__(self):
        self.objdbops=dbops()

    def get(self,request):
        print("request_data report---------------",request.data)
        strQ ="select isnull(Comment,'-') comment,case when  [Rpt_Sub_sub_section_text] is not null then [Rpt_Sub_sub_section_text]"
        strQ+="else case when  [Rpt_Sub_section_text] is not null then [Rpt_Sub_section_text]"
        strQ+="else case when  rpt_section_text is not null then rpt_section_text end end end lbl_txt,[Rpt_Sub_sub_section_text],[Rpt_Sub_section_text],rpt_section_text,"
        strQ+="case when  [Rpt_Sub_sub_section_text] is not null then 3 "
        strQ+="else case when  [Rpt_Sub_section_text] is not null then 2 "
        strQ+="else case when  rpt_section_text is not null then 1  end end end lbl_lvl,"
        strQ+="case when  [Rpt_Sub_sub_section_text] is not null then "
        strQ+="concat(cast ([Index_Section]  as varchar),'.',cast ([Index_Sub_Section]  as varchar),'.',"
        strQ+="cast ([Index_Sub_Sub_Section]  as varchar))else case when  [Rpt_Sub_section_text] is not null then "
        strQ+="concat(cast ([Index_Section]  as varchar),'.',cast ([Index_Sub_Section]  as varchar))else "
        strQ+="case when  rpt_section_text is not null then cast ([Index_Section]  as varchar) end end end lbl_idx,rep_temp.* "
        strQ+="from Report_Template_temp rep_temp  LEFT JOIN Report_Content "
        strQ+="on Report_Content.Report_Template_AID = rep_temp.Report_Template_Temp_AID "
        strQ+="inner join RPT_Section_Master sec_mst on rep_temp.Rpt_section_AID=sec_mst.[Rpt_section_AID] "
        strQ+="left outer join  RPT_sub_Section_Master sub_sec_mst on rep_temp.Rpt_sub_section_AID=sub_sec_mst.[Rpt_sub_section_AID] "
        strQ+="left outer join  RPT_sub_sub_Section_Master sub_sub_sec_mst on rep_temp.Rpt_sub_sub_section_AID=sub_sub_sec_mst.[Rpt_sub_sub_section_AID] "
        # strQ+="where rep_temp.template_name='new one temp' "
        strQ+="where rep_temp.template_name='"+request.data['template_name']+"' "
        strQ+="order by [Index_Section] ,[Index_Sub_Section] ,[Index_Sub_Sub_Section]"
        print("strq updated-----------",strQ)
        dtusers=  self.objdbops.getTable(strQ) 
        dtusers= dtusers.to_json(orient='records')
        d = json.loads(dtusers)
        print("data--------------",d)
    
        return Response({"df":d})

class Show_Report_data(APIView):
    permission_classes=[IsAuthenticated]
    objdbops =None

    def __init__(self):
        self.objdbops=dbops()

    def get(self,request):
        print()
        strQ ="select case when  [Rpt_Sub_sub_section_text] is not null then [Rpt_Sub_sub_section_text]"
        strQ+="else case when  [Rpt_Sub_section_text] is not null then [Rpt_Sub_section_text]"
        strQ+="else case when  rpt_section_text is not null then rpt_section_text end end end lbl_txt,[Rpt_Sub_sub_section_text],[Rpt_Sub_section_text],rpt_section_text,"
        strQ+="case when  [Rpt_Sub_sub_section_text] is not null then 3 "
        strQ+="else case when  [Rpt_Sub_section_text] is not null then 2 "
        strQ+="else case when  rpt_section_text is not null then 1  end end end lbl_lvl,"
        strQ+="case when  [Rpt_Sub_sub_section_text] is not null then "
        strQ+="concat(cast ([Index_Section]  as varchar),'.',cast ([Index_Sub_Section]  as varchar),'.',"
        strQ+="cast ([Index_Sub_Sub_Section]  as varchar))else case when  [Rpt_Sub_section_text] is not null then "
        strQ+="concat(cast ([Index_Section]  as varchar),'.',cast ([Index_Sub_Section]  as varchar))else "
        strQ+="case when  rpt_section_text is not null then cast ([Index_Section]  as varchar) end end end lbl_idx,rep_temp.* "
        strQ+="from Report_Template_temp rep_temp  "
        #strQ+="on Report_Content.Report_Template_AID = rep_temp.Report_Template_Temp_AID "
        strQ+="inner join RPT_Section_Master sec_mst on rep_temp.Rpt_section_AID=sec_mst.[Rpt_section_AID] "
        strQ+="left outer join  RPT_sub_Section_Master sub_sec_mst on rep_temp.Rpt_sub_section_AID=sub_sec_mst.[Rpt_sub_section_AID] "
        strQ+="left outer join  RPT_sub_sub_Section_Master sub_sub_sec_mst on rep_temp.Rpt_sub_sub_section_AID=sub_sub_sec_mst.[Rpt_sub_sub_section_AID] "
        # strQ+="where rep_temp.template_name='new one temp' "
        strQ+="where rep_temp.template_name='"+request.data['template_name']+"' "
        strQ+="order by [Index_Section] ,[Index_Sub_Section] ,[Index_Sub_Sub_Section]"
        print("strq updated-----------",strQ)
        dtusers=  self.objdbops.getTable(strQ) 
        dtusers= dtusers.to_json(orient='records')
        d = json.loads(dtusers)
        print("data--------------",d)
    
        return Response({"df":d})

class FLShow_Report_data(APIView):
    permission_classes=[IsAuthenticated]
    objdbops =None

    def __init__(self):
        self.objdbops=dbops()

    def get(self,request):
        print()
        strQ ="select case when  [Rpt_Sub_sub_section_text] is not null then [Rpt_Sub_sub_section_text]"
        strQ+="else case when  [Rpt_Sub_section_text] is not null then [Rpt_Sub_section_text]"
        strQ+="else case when  rpt_section_text is not null then rpt_section_text end end end lbl_txt,[Rpt_Sub_sub_section_text],[Rpt_Sub_section_text],rpt_section_text,"
        strQ+="case when  [Rpt_Sub_sub_section_text] is not null then 3 "
        strQ+="else case when  [Rpt_Sub_section_text] is not null then 2 "
        strQ+="else case when  rpt_section_text is not null then 1  end end end lbl_lvl,"
        strQ+="case when  [Rpt_Sub_sub_section_text] is not null then "
        strQ+="concat(cast ([Index_Section]  as varchar),'.',cast ([Index_Sub_Section]  as varchar),'.',"
        strQ+="cast ([Index_Sub_Sub_Section]  as varchar))else case when  [Rpt_Sub_section_text] is not null then "
        strQ+="concat(cast ([Index_Section]  as varchar),'.',cast ([Index_Sub_Section]  as varchar))else "
        strQ+="case when  rpt_section_text is not null then cast ([Index_Section]  as varchar) end end end lbl_idx,rep_temp.* "
        strQ+="from FL_Report_Template_Temp rep_temp  "
        #strQ+="on Report_Content.Report_Template_AID = rep_temp.Report_Template_Temp_AID "
        strQ+="inner join FL_RPT_Section_Master sec_mst on rep_temp.Rpt_section_AID=sec_mst.[Rpt_section_AID] "
        strQ+="left outer join  FL_RPT_sub_Section_Master sub_sec_mst on rep_temp.Rpt_sub_section_AID=sub_sec_mst.[Rpt_sub_section_AID] "
        strQ+="left outer join  FL_RPT_sub_sub_Section_Master sub_sub_sec_mst on rep_temp.Rpt_sub_sub_section_AID=sub_sub_sec_mst.[Rpt_sub_sub_section_AID] "
        # strQ+="where rep_temp.template_name='new one temp' "
        strQ+="where rep_temp.template_name='"+request.data['template_name']+"' "
        strQ+="order by [Index_Section] ,[Index_Sub_Section] ,[Index_Sub_Sub_Section]"
        print("strq updated-----------",strQ)
        dtusers=  self.objdbops.getTable(strQ) 
        dtusers= dtusers.to_json(orient='records')
        d = json.loads(dtusers)
        print("data--------------",d)
    
        return Response({"df":d})

    

class ReportContentAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        allocation_obj = ReportTemplateTemp.objects.all().values_list('template_name',flat=True).distinct()       
        temp_name = [i for i in allocation_obj]
        print("temp_name-------------",temp_name)
        # for i in allocation_obj:
        #     print("i",i)
        #     temp_name.append(i)
        rptcontentobj = ReportContent.objects.values('template_name')
        serializer =  ReportContentSerializer(rptcontentobj,many=True)
        return Response(temp_name, status=status.HTTP_200_OK)
    
    def post(self,request):
        obj = ReportContent.objects.filter(report_template_aid = request.data['report_template_aid'],template_name = request.data['template_name']).first()
        if obj:
            item = ReportContent.objects.get(report_template_aid = request.data['report_template_aid'],template_name = request.data['template_name'])
            data = ReportContentSerializer(instance=item, data=request.data)        
            if data.is_valid():
                data.save()
                return Response({'data':data.data,'msg':'Report Content Updated Successfully'},status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ReportContentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'msg':'Report Content Saved Successfully'},status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
        
class FindingsValElementsAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            find_val = FindingValElements.objects.get(element_aid=id)
            serializer = FindingValElementsSerializer(find_val)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        findvalmaster = FindingValElements.objects.all()
        serializer =  FindingValElementsSerializer(findvalmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data find val elements",request.data)
        serializer = FindingValElementsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Finding Val Element is created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = FindingValElements.objects.get(element_aid=id)

        except FindingValElements.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Finding val element does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = FindingValElementsSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Finding val Element is Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
class Elements(APIView):
    def get(self,request):
        obj = FindingValElements.objects.get(element_text=request.data['element'])
        serializer = FindingValElementsSerializer(obj)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class FindingsCategoryAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            find_cat = FindingsCategory.objects.get(category_aid=id)
            serializer = FindingsCategorySerializer(find_cat)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        findcatmaster = FindingsCategory.objects.all()
        serializer =  FindingsCategorySerializer(findcatmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data find val elements",request.data)
        serializer = FindingsCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Finding Category is created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = FindingsCategory.objects.get(category_aid=id)

        except FindingsCategory.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Finding val element does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = FindingsCategorySerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Finding Category is Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
class GetModelIdFindVal(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        print("request_data------------------",request.data)
        obj =  MdlRelevantPersonnel.objects.filter(u_id = request.data['uid'],u_type = 'Owner')
        print("obj---------------",obj)
        lst = []
        for i in obj:
            print("i-----------",i.mdl_id)
            find_valobj = ValidationFindings.objects.filter(mdl_id = i.mdl_id).first()
            if find_valobj:
                lst.append(find_valobj.mdl_id)
        # lst = [i.mdl_id for i in obj if find_valobj]
        print("lst--------------",lst)
        return Response({"Mdlids":lst}, status=status.HTTP_200_OK)


class FindingsValSubElementsAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            find_val = FindingValSubElements.objects.get(element_aid=id)
            serializer = FindingValSubElementsSerializer(find_val)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        findvalmaster = FindingValSubElements.objects.all()
        serializer =  FindingValSubElementsSerializer(findvalmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data find val elements",request.data)
        serializer = FindingValSubElementsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Finding Val sub Element is created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        print("request_data",request.data)
        try:
            id=request.data['id']
            smp = FindingValSubElements.objects.get(element_aid=id)

        except FindingValSubElements.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Finding val element does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = FindingValSubElementsSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Finding val sub Element is Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
        

class SectionApI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        question_master = QuestionSections.objects.all()
        serializer =  QuestionSectionsSerializer(question_master,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class Sections(APIView):
    def get(self,request):
        obj = QuestionSections.objects.get(section_label=request.data['section'])
        serializer = QuestionSectionsSerializer(obj)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class QuestionSectionAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            qtn_obj = QuestionMaster.objects.get(question_aid=id)
            serializer = QuestionMasterSerializer(qtn_obj)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        question_master = QuestionMaster.objects.all().order_by('section_aid')
        serializer =  QuestionMasterSerializer(question_master,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data question and section",request.data)
        serializer = QuestionMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Question and Section Added Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        print("request_data",request.data)
        try:
            id=request.data['id']
            smp = QuestionMaster.objects.get(question_aid=id)

        except QuestionMaster.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Questions does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionMasterSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Question and Sections Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)



class getIssuesByQtrOrMonth(APIView): 
    permission_classes=[IsAuthenticated] 
    def post(self,request):
        try: 
            objreg=Register()  
            issuesByQtrOrMonth=objreg.getIssuesByMonthOrQtr(request.data['ptype'],request.data['uid'],request.data['is_mrm'],request.data['issue_from_dt'],request.data['issue_to_dt'],request.data['issue_sts'])
            return JsonResponse({'issuesByQtrOrMonth':issuesByQtrOrMonth})
        except Exception as e:
            print('setuppycaret is ',e)
            print('setuppycaret traceback is ', traceback.print_exc())


class FiterIssue(APIView): 
    permission_classes=[IsAuthenticated] 
    def post(self,request):
        try: 
            objreg=Register()  
            issueList=objreg.getFilteredIssueListByUserId(request.data['uid'],request.data['type'],request.data['colval'],request.data['priority'])
            return Response({ 'issueList':issueList},
                                                    status=status.HTTP_200_OK)
           
        except Exception as e:
            print('setuppycaret is ',e)
            print('setuppycaret traceback is ', traceback.print_exc()) 
            error_saving(request,e)
    
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)     
        
class ValidationRatingsAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        master = ValidationRatingMaster.objects.all()
        serializer =  ValidationRatingMasterSerializer(master,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data validation Rating",request.data)
        temp_obj = ValidationRatingMasterTemp.objects.all()
        print("temp_obj",temp_obj)
        try:
            for i in temp_obj:
                filter_obj = ValidationRatingMaster.objects.filter(validation_rating = i.validation_rating,severity = i.severity)
                print("filter_obj",filter_obj)
                if filter_obj:
                    obj = ValidationRatingMaster.objects.filter(validation_rating = i.validation_rating,severity = i.severity).update(risk_type = i.risk_type,operator = i.operator,value = i.value)
                else:
                    obj = ValidationRatingMaster(validation_rating = i.validation_rating,severity = i.severity,risk_type = i.risk_type,operator = i.operator,value = i.value,addedby=i.addedby)
                    obj.save()
            print("check")
            ValidationRatingMasterTemp.objects.all().delete()
            return Response({'msg':'Validation Ratings Saved Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error':e,'msg':'Something Went Wrong'},status=status.HTTP_201_CREATED)

        # serializer = ValidationRatingMasterSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response({'data':serializer.data,'msg':'Validation Ratings Saved Successufully'},status=status.HTTP_201_CREATED)
        
    
class ValidationRatingsTempAPI(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):     
        print("request_data validation Rating",request.data)
        serializer = ValidationRatingMasterTempSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Validation Ratings Temp Saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)



class getReportTtlHdr(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try: 
            strQ="SELECT Z.template_name,"
            strQ+="   ttls = "
            strQ+="    STUFF ("
            strQ+="    (SELECT   "
            strQ+="    ',' +title_label  "
            strQ+="    FROM [report_title_template] X"
            strQ+="    Where X.template_name =Z.template_name"
            strQ+="    FOR XML PATH('')), 1, 1, ''"
            strQ+="   )"
            strQ+="    FROM [report_title_template] Z GROUP by Z.template_name"
            tableResult =objdbops.getTable(strQ)  
            ttlnheadrs = tableResult.to_json(orient='index')
            ttlnheadrs = json.loads(ttlnheadrs) 
            return Response({'ttlnheadrs':ttlnheadrs},status=status.HTTP_200_OK)
        except Exception as g:
            print('')

class FLgetReportTtlHdr(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try: 
            strQ="SELECT Z.template_name,"
            strQ+="   ttls = "
            strQ+="    STUFF ("
            strQ+="    (SELECT   "
            strQ+="    ',' +title_label  "
            strQ+="    FROM [FL_Report_title_template] X"
            strQ+="    Where X.template_name =Z.template_name"
            strQ+="    FOR XML PATH('')), 1, 1, ''"
            strQ+="   )"
            strQ+="    FROM [FL_Report_title_template] Z GROUP by Z.template_name"
            tableResult =objdbops.getTable(strQ)  
            ttlnheadrs = tableResult.to_json(orient='index')
            ttlnheadrs = json.loads(ttlnheadrs) 
            return Response({'ttlnheadrs':ttlnheadrs},status=status.HTTP_200_OK)
        except Exception as g:
            print('')


class save_model_report(APIView):
    def post(self,request): 
        try:
            title_id=request.data['title_id']
            title_or_heading=request.data['title_or_heading']
            added_by=request.data['added_by'] 
            title_label=request.data['title_label']
            template_name=request.data['tamplate_name']
            title_type=request.data['title_type'] 
            title_placeholder=request.data['title_placeholder']
            title_sort_idx=request.data['title_sort_idx'] 
            fontsize = request.data['fontsize'] 
            alignment = request.data['alignment']
            
            strQ="INSERT INTO  report_title_template \
                ( title_id,title_or_heading,title_label,added_by,added_on, template_name, fontsize,alignment,title_type, title_placeholder , title_sort_idx )\
                VALUES\
                ( "+str(title_id)+","+str(title_or_heading)+",'"+title_label+"',"+str(added_by)+",getdate(),'"+template_name+"','"+fontsize+"','"+alignment+"','"+title_type+"', '"+title_placeholder+"',"+str(title_sort_idx) +") " 
            objdbops.insertRow(strQ)
            return Response({'is_taken':True})
        except Exception as e:
            print('error is  ',e)


class insert_Report_Title_Table_contet(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            title_id=request.data['title_id']
            Template_Name=request.data['template_name']
            added_by=request.data['added_by'] 
            mdl_id=request.data['mdl_id']
            Header_1=request.data['comment_1']
            Header_2=request.data['comment_2'] 
            Header_3=request.data['comment_3']
            Header_4=request.data['comment_4'] 
            
            strQ="INSERT INTO  Report_Header_Table_Content \
                ( Template_Name , title_id  , mdl_id , Header_1 , Header_2, Header_3  , Header_4 , added_by  , added_on )\
                VALUES\
                ( '"+Template_Name +"'  , "+ str(title_id)  +", '"+mdl_id +"' , '"+Header_1+"' , '"+Header_2+"' , '"+Header_3+"' , '"+Header_4+"' , '"+str(added_by)+"' , getdate() )" 
           
            objdbops.insertRow(strQ)
            return Response({'is_taken':True},status=status.HTTP_200_OK)
        except Exception as e:
            print('setuppycaret is ',e)
            print('setuppycaret traceback is ', traceback.print_exc()) 

class FL_insert_Report_Title_Table_contet(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            title_id=request.data['title_id']
            Template_Name=request.data['template_name']
            added_by=request.data['added_by'] 
            mdl_id=request.data['mdl_id']
            Header_1=request.data['comment_1']
            Header_2=request.data['comment_2'] 
            Header_3=request.data['comment_3']
            Header_4=request.data['comment_4'] 
            
            strQ="INSERT INTO  FL_Report_Header_Table_Content \
                ( Template_Name , title_id  , mdl_id , Header_1 , Header_2, Header_3  , Header_4 , added_by  , added_on )\
                VALUES\
                ( '"+Template_Name +"'  , "+ str(title_id)  +", '"+mdl_id +"' , '"+Header_1+"' , '"+Header_2+"' , '"+Header_3+"' , '"+Header_4+"' , '"+str(added_by)+"' , getdate() )" 
           
            objdbops.insertRow(strQ)
            return Response({'is_taken':True},status=status.HTTP_200_OK)
        except Exception as e:
            print('setuppycaret is ',e)
            print('setuppycaret traceback is ', traceback.print_exc()) 


class get_Report_Title_Table_contet(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            title_id=request.data['title_id'] 
            strQ="SELECT  *  FROM  \
                Report_Header_Table_Content  where template_name='"+ request.data['temp_name']+ "' \
                and mdl_id='"+ request.data['mdl_id']+ "' and title_id="+str(title_id)+" order by Report_Header_Table_Content_AID"           
            tableResult =objdbops.getTable(strQ)  
            ttlnheadrs = tableResult.to_json(orient='index')
            ttlnheadrs = json.loads(ttlnheadrs) 
            return Response({'ttlnheadrs':ttlnheadrs},status=status.HTTP_200_OK)
        except Exception as e:
            print('setuppycaret is ',e)
            print('setuppycaret traceback is ', traceback.print_exc()) 


#Comment

def exportgraphImgPdf(pdf, graph, header, comments=""):
    # print('len(comments) ', len(comments))
    print(graph, header, comments)
    if(len(comments) > 0):
        x, y = 10, 10
        # print('get_y 1 ', pdf.get_y())
        pdf.set_font("Arial", size=15)
        pdf.set_xy(x, y)
        pdf.set_text_color(0.0, 0.0, 0.0)
        pdf.cell(0, 10, header, align='C')
        # print('get_y 2 ', pdf.get_y())
        if(len(comments) > 0):
            y = pdf.get_y()+10.0
            pdf.set_font("Arial", size=12)
            pdf.set_xy(x, y)
            pdf.set_text_color(0.0, 0.0, 0.0)
            pdf.multi_cell(0, 10, comments.encode(
                'latin-1', 'replace').decode('latin-1'), align='L')
        # print('get_y 3 ', pdf.get_y())
        y = pdf.get_y()+5.0
        pdf.set_xy(20, y)
        pdf.image(graph,  link='', type='', w=700/4, h=450/4)
    else:
        x, y = 10, 50
        # set style and size of font
        # that you want in the pdf
        pdf.set_font("Arial", size=15)
        pdf.set_xy(x, y)
        pdf.set_text_color(0.0, 0.0, 0.0)
        pdf.multi_cell(0, 10, header, align='C')

        y += 20.0
        pdf.set_xy(20, y)
        pdf.image(graph,  link='', type='', w=700/4, h=450/4)

    return pdf

def find_src_data(mdlid,dataset=''): 
        if mdlid=="":
            src_file_obj = collection_file_info.find()
        else:
            src_file_obj = collection_file_info.find({'Mdl_Id':mdlid})
        df =  pd.DataFrame(list(src_file_obj)) 
        if len(df)>0: 
            file_id=df['file_id'].max()
        else:
            file_id=1 #changed by nilesh on 11.4.23
        print('file_id' ,file_id) 

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

class save_desc_comments(APIView):
    def post(self,request):
        print("request_data------------------",request.data)

        added_by=request.data['Added_by']
        comment=request.data['comment']
        utility=request.data['utility']
        type_comm=request.data['type_comm']
        destination=request.data['destination']

        print("type_comm",type_comm)

        print("comment utility",comment,utility)

        VtUserComments.objects.create(mdl_id=request.data['mdl_id'],utility=request.data['utility'],sub_utility=request.data['sub_utility']
                                      ,comment=request.data['comment'],type_comment=type_comm,destination=destination,
                                      added_by=request.data['Added_by'],added_on=datetime.now())
        data = {'is_taken':True}
        print("saved")
        return Response(data)
    
class validation_comments(APIView):
    def get(self,request):
        print("request_data------------------",request.data)
        uid=request.data['uid']

        val_comm_obj=VtUserComments.objects.filter(added_by=uid)
        
        # distinct_queryset = MyModel.objects.values('field1', 'field2').distinct()

        distinct_values=val_comm_obj.values('mdl_id').distinct()

        print("distinct_values",distinct_values)

        return Response(distinct_values )


class get_val_comments_data(APIView):
    def get(self,request):
        print("request_data------------------",request.data)
        mdl_id=request.data['mdl_id']

        val_comm_obj=VtUserComments.objects.filter(mdl_id=mdl_id)

        values=val_comm_obj.values('mdl_id','utility','sub_utility','comment','type_comment','destination')

        print("values",values)

        return Response(values)


def saveChartViewd(chartType, xaxisval, yaxisval, imageName,vt_mdl,user_id,dataseg):
    print("saveChartViewd",chartType, xaxisval, yaxisval, imageName,vt_mdl,user_id,dataseg)

    data = [[chartType, xaxisval, yaxisval, imageName,vt_mdl,user_id,dataseg]]
    df = pd.DataFrame(
        data, columns=['chartType', 'xaxisval', 'yaxisval', 'imageName','Mdl_Id','user_id','data_segment'])
     
    if collection_chart_viewed.find_one({'xaxisval':xaxisval,'yaxisval':yaxisval,'Mdl_Id':vt_mdl,'user_id':int(user_id),'data_segment':dataseg,'chartType':chartType}):
        collection_chart_viewed.delete_many({'xaxisval':xaxisval,'yaxisval':yaxisval,'Mdl_Id':vt_mdl,'user_id':int(user_id),'data_segment':dataseg,'chartType':chartType})        
        collection_chart_viewed.insert_many(df.to_dict('records'))
    else:
        collection_chart_viewed.insert_many(df.to_dict('records'))


class Plotinsoccuvsincstate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request): 
        print("BASE_DIR",BASE_DIR)
        df=find_src_data(request.data['mdl_id'],request.data['dataset'])
       
        print("df",df)
        var1=request.data['var1']
        var2=request.data['var2']
        print("var1 2",var1,var2)
        username=request.data['username']
        print("username",username)
        cat_cols_temp = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] in [np.object]] 
        cat_cols=[]
        print("cat_cols",cat_cols)
        print("cat_cols_temp",cat_cols_temp)

        for x in cat_cols_temp:
            if len(df[x].value_counts())<25:
                cat_cols.append(x)
        print("cat_cols",cat_cols)       
        json_data = dict() 
        if(len(cat_cols)<1):
            cat_cols_check=1
            json_data['cat_cols_check']=cat_cols_check
            print("json_data",json_data)
            return JsonResponse(json_data)
            # return render(request, 'noCatVars.html')
        else:
            cat_cols_check=0

            if(var1 == False):
                var1 = cat_cols[0]
                var2 = cat_cols[1]

            print('varr1 ', var1)
            cat_bar = pd.crosstab(df[var1], df[var2])
            color = plt.cm.inferno(np.linspace(0, 1, 5))
            cat_bar.div(cat_bar.sum(1).astype(float), axis=0).plot(kind='bar', figsize=(10, 6),
                                                                stacked=False,
                                                                color=color)
            plt.title(var2, fontsize=14)
            plt.legend()
            plt.tight_layout()
            
            plt.savefig(os.path.join(
                BASE_DIR, plot_dir_view+username+'plotinsoccuvsincstate.png'))
            plt.close()
            del df  
            saveChartViewd('Bar chart', var1, var2, username +
                           'plotinsoccuvsincstate.png',request.data['mdl_id'],request.data['user_id'],
                           request.data['data_segment'])
            
            if os.path.exists(os.path.join(
                    BASE_DIR, plot_dir_view+username+'plotinsoccuvsincstate.png')):
                pdf = FPDF()
                pdf.add_page()
                pdf = exportgraphImgPdf(pdf, os.path.join(
                    BASE_DIR, plot_dir_view+username+'plotinsoccuvsincstate.png'), " Bar chart "+var1+" vs "+var2)
                pdf.output(os.path.join(
                    BASE_DIR, plot_dir_view+username+'Bar chart.pdf'))

            print("graphpath",plot_dir_view+username+'plotinsoccuvsincstate.png')
            print('pdfFile',plot_dir_view+username+'Bar chart.pdf')
            # BASE_DIR = Path(__file__).resolve().parent.parent
            pngDir = os.path.join(BASE_DIR, 'static\\media\\')
            savefile_name = pngDir + str(username+'plotinsoccuvsincstate.png')
            print("savefile_name",savefile_name)    


            file_stream = BytesIO()
            print("file_stream",file_stream)
            image_data = PIL.Image.open(savefile_name)
            print("image_data",image_data)
            image_data.save(file_stream,'png')
            # image_data.save(file_stream.png)
            print("image_data",image_data)
            print("image_data",type(image_data))
            file_stream.seek(0)
            base64_data = base64.b64encode(file_stream.getvalue()).decode('utf-8')
            
            json_data['report'] = base64_data
            print("type000",type(base64_data))
            json_data.update({'chartType': 'Bar chart', 'pdfFile': plot_dir_view+username+'Bar chart.pdf',
                    'ddlvar1': cat_cols, 'ddlvar2': cat_cols, 'var1': var1, 'var2': var2,'cat_cols_check':cat_cols_check})
            print("json data",json_data)
            return JsonResponse(json_data)


class plotinsoccuvsincstatestacked(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request): 
        df=find_src_data(request.data['mdl_id'],request.data['dataset'])
       
        print("df",df)
        var1=request.data['var1']
        var2=request.data['var2']
        print("var1 2",var1,var2)

        username=request.data['username']
        print("username",username)

        cat_cols_temp = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] in [np.object]]
        cat_cols=[]
        for x in cat_cols_temp:
            if len(df[x].value_counts())<25:
                cat_cols.append(x)
        print("cat_cols",cat_cols)
        print("len(cat_cols)",len(cat_cols))

        json_data = dict()
        if(len(cat_cols)<1):
            cat_cols_check=1
            json_data['cat_cols_check']=cat_cols_check
            print("json_data",json_data)
            return JsonResponse(json_data)
            # return render(request, 'noCatVars.html')
        else:
            cat_cols_check=0
        
            if(var1 == False):
                var1 = cat_cols[0]
                var2 = cat_cols[1]
            incident = pd.crosstab(df[var1], df[var2])
            # print('var1 ', var1, ' var2 ', var2)
            # occu = pd.crosstab(x_keep[var], df['fraud_reported'])
            colors = plt.cm.inferno(np.linspace(0, 1, 5))
            incident.div(incident.sum(1).astype(float), axis=0).plot(kind='bar',
                                                                    stacked=True,
                                                                    figsize=(
                                                                        10, 6),
                                                                    color=colors)

            plt.title(var2, fontsize=20)
            plt.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(
                BASE_DIR, plot_dir_view+request.data['username']+'plotinsoccuvsincstatestacked.png'))
            plt.close()
            del df
            saveChartViewd('Stacked Bar chart', var1, var2,
                           username+'plotinsoccuvsincstatestacked.png',request.data['mdl_id'],request.data['user_id'],
                           request.data['data_segment'])

            if os.path.exists(os.path.join(
                    BASE_DIR, plot_dir_view+request.data['username']+'plotinsoccuvsincstatestacked.png')):
                pdf = FPDF()
                pdf.add_page()
                pdf = exportgraphImgPdf(pdf, os.path.join(
                    BASE_DIR, plot_dir_view+request.data['username']+'plotinsoccuvsincstatestacked.png'), " Stacked Bar chart "+var1+" vs "+var2)
                pdf.output(os.path.join(
                    BASE_DIR, plot_dir_view+request.data['username']+'Stacked Bar chart.pdf'))

            pngDir = os.path.join(BASE_DIR, 'static\\media\\')
            savefile_name = pngDir + str(request.data['username']+'plotinsoccuvsincstatestacked.png')
            print("savefile_name",savefile_name)


            file_stream = BytesIO()
            print("file_stream",file_stream)
            image_data = PIL.Image.open(savefile_name)
            print("image_data",image_data)
            image_data.save(file_stream,'png')
            # image_data.save(file_stream.png)
            print("image_data",image_data)
            print("image_data",type(image_data))
            file_stream.seek(0)
            base64_data = base64.b64encode(file_stream.getvalue()).decode('utf-8')
            
            json_data['report'] = base64_data
            json_data.update({'chartType': 'Stacked Bar chart', 'pdfFile': plot_dir+user_name+'Stacked Bar chart.pdf',
                    'ddlvar1': cat_cols, 'ddlvar2': cat_cols, 'var1': var1, 'var2': var2,'cat_cols_check':cat_cols_check})
            print("json data",json_data)
            return JsonResponse(json_data)


class stripplot(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request): 
        import matplotlib.pyplot as pltstrip
        import seaborn as snsstrip

        df=find_src_data(request.data['mdl_id'],request.data['dataset'])
       
        print("df",df)
        var_cat=request.data['var_cat']
        var_num=request.data['var_num']
        print("var_cat var_num",var_cat,var_num)

        cat_cols_temp = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] in [np.object]]

        cat_cols=[]
        for x in cat_cols_temp:
            if len(df[x].value_counts())<25:
                cat_cols.append(x)
        print("cat_cols ",cat_cols)
        json_data = dict()
        if(len(cat_cols)<1):
            cat_cols_check=1
            json_data['cat_cols_check']=cat_cols_check
            print("json_data",json_data)
            return JsonResponse(json_data)
            # return render(request, 'noCatVars.html')
        else:
            cat_cols_check=0
            num_cols_temp = [c for i, c in enumerate(
                df.columns) if df.dtypes[i] not in [np.object]]
            print("num_cols_temp ",num_cols_temp)
            num_cols=[]
            for x in num_cols_temp:
                if len(df[x].value_counts())<25:
                    num_cols.append(x)
            print("num_cols",num_cols)
            if(var_num == False):
                var_num = num_cols[0]
                var_cat = cat_cols[1]

            fig = pltstrip.figure(figsize=(15, 8))
            pltstrip.style.use('fivethirtyeight')
            pltstrip.rcParams['figure.figsize'] = (15, 8)

            snsstrip.stripplot(x=df[var_cat],y=df[var_num],
                            palette='bone', figure=fig)
            pltstrip.title(var_num, fontsize=20)
            pltstrip.savefig(os.path.join(
                BASE_DIR, plot_dir_view+request.data['username']+'outputstripplot.png'))
            pltstrip.close()
            saveChartViewd('Strip Plot', var_num, var_cat,
                           request.data['username']+'outputstripplot.png',request.data['mdl_id'],request.data['user_id'],
                           request.data['data_segment'])
            del df
            if os.path.exists(os.path.join(
                    BASE_DIR, plot_dir_view+request.data['username']+'outputstripplot.png')):
                pdf = FPDF()
                pdf.add_page()
                pdf = exportgraphImgPdf(pdf, os.path.join(
                    BASE_DIR, plot_dir_view+request.data['username']+'outputstripplot.png'), " Strip Plot "+var_num+" vs "+var_cat)
                pdf.output(os.path.join(
                    BASE_DIR, plot_dir_view+request.data['username']+'Strip Plot.pdf'))

            pngDir = os.path.join(BASE_DIR, 'static\\media\\')
            savefile_name = pngDir + str(request.data['username']+'outputstripplot.png')
            print("savefile_name",savefile_name)


            file_stream = BytesIO()
            print("file_stream",file_stream)
            image_data = PIL.Image.open(savefile_name)
            print("image_data",image_data)
            image_data.save(file_stream,'png')
            # image_data.save(file_stream.png)
            print("image_data",image_data)
            print("image_data",type(image_data))
            file_stream.seek(0)
            base64_data = base64.b64encode(file_stream.getvalue()).decode('utf-8')
            json_data['report'] = base64_data
            json_data.update({'chartType': 'Strip Plot', 'pdfFile': plot_dir+request.data['username']+'Strip Plot.pdf',
                    'ddlvar1': num_cols, 'ddlvar2': cat_cols, 'var1': var_num, 'var2': var_cat, 'hideddl2': '','cat_cols_check':cat_cols_check})
            print("json data",json_data)
            return JsonResponse(json_data)


import joypy

class distribution(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request): 
       
        df=find_src_data(request.data['mdl_id'],request.data['dataset'])
       
        print("df",df)
        var_cat=request.data['var_cat']
        var_num=request.data['var_num']
        print("var_cat var_num",var_cat,var_num)

        cat_cols_temp = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] in [np.object]]

        cat_cols=[]
        for x in cat_cols_temp:
            if len(df[x].value_counts())<25:
                cat_cols.append(x)

        json_data = dict()
        if(len(cat_cols)<1):
            cat_cols_check=1
            json_data['cat_cols_check']=cat_cols_check
            print("json_data",json_data)
            return JsonResponse(json_data)
            # return render(request, 'noCatVars.html')
        else:
            cat_cols_check=0

            num_cols_temp = [c for i, c in enumerate(
                df.columns) if df.dtypes[i]   in ( [np.int64]or [np.float64])]
            num_cols=[]
            for x in num_cols_temp:
                if len(df[x].value_counts())<2500:
                    num_cols.append(x)

            if(var_num == False):
                var_num = num_cols[0]
                var_cat = cat_cols[1]
            fig, axes = joypy.joyplot(df,
                                    column=[var_num],
                                    by=var_cat,
                                    ylim='own',
                                    figsize=(20, 12),
                                    alpha=0.5,
                                    legend=True)

            plt.title(var_num, fontsize=20)
            plt.tight_layout()
            fig.savefig(os.path.join(
                BASE_DIR, plot_dir_view+request.data['username']+'distbyfraud2.png'))
            saveChartViewd('Distribution', var_num, var_cat,
                           request.data['username']+'distbyfraud2.png',request.data['mdl_id'],request.data['user_id'],
                           request.data['data_segment'])
            del df
            if os.path.exists(os.path.join(
                    BASE_DIR, plot_dir_view+request.data['username']+'distbyfraud2.png')):
                pdf = FPDF()
                pdf.add_page()
                pdf = exportgraphImgPdf(pdf, os.path.join(
                    BASE_DIR, plot_dir_view+request.data['username']+'distbyfraud2.png'), " Distribution "+var_num+" vs "+var_cat)
                pdf.output(os.path.join(
                    BASE_DIR, plot_dir_view +"/"+request.data['username']+"Distribution.pdf"))

            pngDir = os.path.join(BASE_DIR, 'static\\media\\')
            savefile_name = pngDir + str(request.data['username']+'distbyfraud2.png')
            print("savefile_name",savefile_name)
            file_stream = BytesIO()
            print("file_stream",file_stream)
            image_data = PIL.Image.open(savefile_name)
            print("image_data",image_data)
            image_data.save(file_stream,'png')
            # image_data.save(file_stream.png)
            print("image_data",image_data)
            print("image_data",type(image_data))
            file_stream.seek(0)
            base64_data = base64.b64encode(file_stream.getvalue()).decode('utf-8')
            json_data['report'] = base64_data
            json_data.update({'chartType': 'Distribution', 'pdfFile': plot_dir+request.data['username']+'Distribution.pdf',
                    'ddlvar1': num_cols, 'ddlvar2': cat_cols, 'var1': var_num, 'var2': var_cat, 'hideddl2': '','cat_cols_check':cat_cols_check})
            print("json data",json_data)
            return JsonResponse(json_data)


import matplotlib.pyplot as pltbox
import seaborn as snsbox

class box_plot(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request): 
        
        df=find_src_data(request.data['mdl_id'],request.data['dataset'])
       
        print("df",df)
        var_cat=request.data['var_cat']
        var_num=request.data['var_num']
        print("var_cat var_num",var_cat,var_num)

        username=request.data['username']

        cat_cols_temp = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] in [np.object]]

        cat_cols=[]
        for x in cat_cols_temp:
            if len(df[x].value_counts())<25:
                cat_cols.append(x)

        if(len(cat_cols)<1):
            return render(request, 'noCatVars.html')
        num_cols_temp = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] not in [np.object]] 

        num_cols=[]
        for x in num_cols_temp:
            if len(df[x].value_counts())<25:
                num_cols.append(x)

        print("num_cols",num_cols)
        print("cat_cols",cat_cols)

        if(var_num == False):
            var_num = num_cols[0]
            var_cat = cat_cols[1]
            # context = {'chartType': 'Box Plot', 'pdfFile': '', 'graphpath': '',
            #            'ddlvar1': num_cols, 'ddlvar2': cat_cols, 'var1': var_num, 'var2': var_cat, 'hideddl2': '', 'postAct': totalclaim_boxplot}
            # return render(request, 'showPlot.html', context)
        fig = pltbox.figure(figsize=(14, 8))
        pltbox.style.use('fivethirtyeight')
        pltbox.rcParams['figure.figsize'] = (20, 8)
        print("var_cat,var_num",df[var_cat],df[var_num])
        print("var_cat,var_num",var_cat,var_num)
        snsbox.boxenplot(x=df[var_cat],y=df[var_num], palette='pink', figure=fig)
        pltbox.title(var_num, fontsize=20)
        pltbox.savefig(os.path.join(
            BASE_DIR, plot_dir_view+username+'outputclaimboxplot.png'))
        pltbox.close()
        saveChartViewd('Box Plot', var_num, var_cat,
                       request.data['username']+'outputclaimboxplot.png',request.data['mdl_id'],request.data['user_id'],
                           request.data['data_segment'])
        del df
        if os.path.exists(os.path.join(
                BASE_DIR, plot_dir_view+username+'outputclaimboxplot.png')):
            pdf = FPDF()
            pdf.add_page()
            pdf = exportgraphImgPdf(pdf, os.path.join(
                BASE_DIR, plot_dir_view+username+'outputclaimboxplot.png'), " Box Plot "+var_num+" vs "+var_cat)
            pdf.output(os.path.join(
                BASE_DIR, plot_dir_view+username+'Box Plot.pdf'))

        pngDir = os.path.join(BASE_DIR, 'static\\media\\')
        savefile_name = pngDir + str(username+'outputclaimboxplot.png')
        print("savefile_name",savefile_name)
        file_stream = BytesIO()
        print("file_stream",file_stream)
        image_data = PIL.Image.open(savefile_name)
        print("image_data",image_data)
        image_data.save(file_stream,'png')
        # image_data.save(file_stream.png)
        print("image_data",image_data)
        print("image_data",type(image_data))
        file_stream.seek(0)
        base64_data = base64.b64encode(file_stream.getvalue()).decode('utf-8')
        json_data = dict()
        json_data['report'] = base64_data
        json_data.update({'chartType': 'Box Plot', 'pdfFile': plot_dir_view+username+'Box Plot.pdf',
                   'ddlvar1': num_cols, 'ddlvar2': cat_cols, 'var1': var_num, 'var2': var_cat, 'hideddl2': ''})
        print("json data",json_data)
        return JsonResponse(json_data)

class insert_VT_Discussion_Comments(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            strQ="INSERT INTO VT_User_Discussion  ( Mdl_Id , utility , sub_utility , comment, added_by , added_on  ,chat_data,file_pah) \
                VALUES           ( '"+request.data['mdl_id']+"' , '"+request.data['utility']+"' , '"+request.data['sub_utility']+"' , '"+str(request.data['comment']).replace("'","''")+"' , '"+str(request.data['Added_by'])+"' , getdate(),'"+request.data['chat_data']+"','"+request.data['destination_path'] + "')"
            objdbops.insertRow(strQ) 
            print(strQ)
            strQ = "select upper(concat(left(u.U_FName,1),left(u.U_LName,1))) uinitials,FORMAT (getdate(),'hh:mm tt  MMM dd, yyyy') createdt from users u where u_aid='"+str(request.data['Added_by'])+"'"
            tableResult= objdbops.getTable(strQ) 
            if tableResult.empty == False:
                mdldata= tableResult.to_json(orient='index')
                del tableResult 
            return Response({'is_taken':True,'data':mdldata,'fileinfo':request.data['destination_path']},status=status.HTTP_200_OK)
        except Exception as e:
            print('setuppycaret is ',e)
            return Response({'is_taken':False},status=status.HTTP_200_OK)
        
class Fetch_message(APIView):
    objdbops =None
    def __init__(self):
        self.objdbops=dbops()
    def get(self,request):
        try:
            strQ = "SELECT  [Comment_id],FORMAT (resp.[added_on],'hh:mm tt  MMM dd, yyyy') createdt ,[Comment],"
            strQ+=" concat(u.U_FName,' ',u.U_LName) addedby,upper(concat(left(u.U_FName,1),left(u.U_LName,1))) uinitials,case when resp.[added_by]="+str(request.data['addedby'].replace("'","''"))+" then 'S' else 'R' end msgcss ,chat_data,isnull(file_pah,'')  as 'filename'"
            strQ+=" from  [VT_User_Discussion] resp,users u"
            strQ+=" where u.U_AID=resp.[added_by] and [Mdl_Id]='"+request.data['mdl_id'].replace("'","''")+"'  and utility='"+str(request.data['utility']).replace('&','n')+"'  and sub_utility='"+request.data['sub_utility'].replace("'","''")+"' and chat_data='"+request.data['chat_data'].replace("'","''")+"'  order by [Comment_id]"
            
            tableResult=  self.objdbops.getTable(strQ)  
            commenthistory= tableResult.to_json(orient='index')
            strQ="SELECT  isnull( comment ,'')  comment,added_by    FROM  VT_User_Comments where    [Mdl_Id]='"+request.data['mdl_id'].replace("'","''")+"'  and utility='"+request.data['utility'].replace("'","''")+"'  and sub_utility='"+request.data['sub_utility'].replace("'","''")+"'"
        
            tableResult=  self.objdbops.getTable(strQ)  
            comment=tableResult.to_json(orient='index')
            return Response({'data':json.loads(commenthistory),'comment':json.loads(comment)}) 
        except Exception as e:
            print('setuppycaret is ',e)
            return Response({'is_taken':False},status=status.HTTP_200_OK)

class projectsInfo(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            ty =request.data['filterType']
            colnm =request.data['filterValue']#request.GET.get('colnm', 'False') 
            chartnm =request.data['filterColumn']#request.GET.get('chartnm', 'False') 
            canAdd="1" 
            # Authorization(request.data['ucaid'],'Model Inventory') 
            modelinfo=objreg.getModelInfoByFilter(request.data['uid'],ty,chartnm,colnm,'0')
            is_MrmHead=str(objmaster.checkMRMHead(str(request.data['uid'])))            
            return Response( {'modelinfo':modelinfo,'canAdd':canAdd, 'is_MrmHead':is_MrmHead},status=status.HTTP_200_OK)          
                
        except Exception as e:
           error_saving(request,e)
           return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)
  

class taskListByModel(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            mdl_id =request.data['mdl_id'] 
            uid =request.data['uid']   
            # Authorization(request.data['ucaid'],'Model Inventory') 
            task_list=objreg.getTaskListByMdl(mdl_id)    
            issue_list=objreg.getIssueListByModel(mdl_id)    
            mdlsts=objreg.getModelStsById(uid,mdl_id)  
            validationRatings=objreg.validationRatings(mdl_id)
            return Response( {'task_list':task_list,'issue_list':issue_list,'mdlsts':mdlsts,'validationRatings':validationRatings},status=status.HTTP_200_OK)          
                
        except Exception as e:
           error_saving(request,e)
           return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)
###############   
class FL_add_question(APIView):
    permission_classes=[IsAuthenticated] 
    # def get(self,request):
    #     fl_ques_obj=FlQuestionMaster.objects.all()
    #     values=fl_ques_obj.values('question_aid','question_label','section_type','section_aid','sub_section_aid',
    #                               'activestatus','addedby','adddate')
    #     print("values",values)
    #     return Response(values)
    
    def post(self,request):
        try:        
            added_by=request.data['uid']
            adddate=datetime.now()
            section=request.data['section']
            sub_section=request.data['sub_section']
            sub_sub_section=request.data['sub_sub_section']
            # sub_sub_sub_section=request.data['sub_sub_sub_section']
            question=request.data['question'] 
            sect_type=request.data['sect_type']
            if sub_section == '':
                sub_section=None
            if sub_sub_section == '':
                sub_sub_section =None
            # if sub_sub_sub_section == '':
            #     sub_sub_sub_section =None      
            question_obj=FlQuestionMaster.objects.create(question_label=question,section_aid=section,sub_section_aid=sub_section,sub_sub_section_aid=sub_sub_section,
                                                        section_type=sect_type,addedby=added_by,adddate=adddate)
            print("saved")
            return JsonResponse({'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)
        
class FL_addSub_Sub_Sub_Section(APIView):
    print()
    def post(self,request):
            sub_secid = request.data['sub_secid']
            section = request.data['section']
            sectiondesc = request.data['sectiondesc']
            activests = request.data['activests']
            user_id = request.data['user_id'] 
            sect_type = request.data['sect_type']           
            objmaster.FL_addSub_Sub_Sub_Section(sub_secid,section,sectiondesc,activests,user_id,sect_type)
            return JsonResponse({'msg':'FL sub sub sub section added succesfully'}, status=status.HTTP_200_OK)

class FLQtns(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try: 
            uid=request.data['uid'] 
            return Response({'canupdate':objmaster.FLcanUpdateRatings(uid),'sections':objmaster.getFLQtnSection(uid),
                           'Qtns':objmaster.getFLQtns(uid),'models':objmaster.getFLModels(str(uid))}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            print(traceback.print_exc())
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class submitFLRatings(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try: 
            objreg.submitRatings( objmaster.getmaxFLId())
            uid=request.data['uid']
            objmaster.insert_notification(str(uid),'MRM-Head','FL','Rating Submitted',1)    
            return JsonResponse({'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class saveFLRatings(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try: 
            colDataLst = request.data['colDataLst']
            print("colDataLst",colDataLst)
            uid=request.data['uid']
            json_colDataLst = json.loads(colDataLst)
            print("json_colDataLst",json_colDataLst)
            objreg=Register()
            for colval in json_colDataLst:
                print('col val is ',colval )
                # objreg.insertFLRatings(colval["qtnId"],colval["ddl_yesno_"],colval["ddl_doc_"],colval["txt_comment_"],uid,objmaster.getmaxFLId())
                obj = FlQuestionRatingData.objects.filter(review_id=objmaster.getmaxFLId(),question_aid=colval["qtnId"],addedby=uid)
                if obj:    
                    print("if")
                    FlQuestionRatingData.objects.filter(review_id=objmaster.getmaxFLId(),question_aid=colval["qtnId"],addedby=uid).update(rating_yes_no=colval["ddl_yesno_"],doc_yes_no=colval["ddl_doc_"],comments=colval["txt_comment_"],inherent_risk_rating = colval['ddl_InherentRisk_'],control_effectiveness_ratings = colval['ddl_ControllEffectiveness_'],residual_ratings = colval['ddl_Residual_'],control_description= colval['txt_control_desc_'],override_residual_ratings = colval['ddl_override_Residual_'],override_comments = colval['txt_override_comment_'])
                else: 
                    print("else")
                    try:   
                        print("review_id",objmaster.getmaxFLId(),"question_aid",colval["qtnId"])
                        save_obj = FlQuestionRatingData.objects.create(review_id=objmaster.getmaxFLId(),question_aid=colval["qtnId"],rating_yes_no=colval["ddl_yesno_"],doc_yes_no=colval["ddl_doc_"],comments=colval["txt_comment_"],inherent_risk_rating = colval['ddl_InherentRisk_'],control_effectiveness_ratings = colval['ddl_ControllEffectiveness_'],residual_ratings = colval['ddl_Residual_'],control_description= colval['txt_control_desc_'],override_residual_ratings = colval['ddl_override_Residual_'],override_comments = colval['txt_override_comment_'],addedby=uid)

                    except Exception as e:
                        print("error is",e.__traceback__)
            return Response({'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

# def check_columns():
#     file_path = 'C:/Jayesh/OwnProjects/forntendrmse/modelval/static/data.csv'
#     exceldf = pd.read_csv(file_path)
#     print("exceldf----------",len(exceldf.columns.tolist())) 

#     map_dtls = MappingDetails.objects.all()
#     queryset_list = list(map_dtls.values())
#     mappingdf = pd.DataFrame(queryset_list)
#     print("mapping_df",len(mappingdf['excel_fields'].tolist()))

#     # list1 = mappingdf['excel_fields'].tolist()
#     list1 = ['Name', 'Age', 'Departement']
#     print("list1",list1)
#     # list2 = exceldf.columns.tolist()
#     list2 = ['Departement', 'Age', 'Name']
#     print("list2",list2)
#     if len(list1) < len(list2):
#         print("additional columns")
#     elif len(list1) == len(list2):
#         print("columns length is same")
#         if sorted(list1) == sorted(list2):
#             print("column names are same")
#             pass
#         else:
#             print("columns are not same")
#     else:
#         print("Invalid file format")
#     print("data imported as it is")
# # check_columns()

# def latest():
#     list1 = ['Name','Age','Department']
#     list2 = ['Name','Age','Department','address']
#     if len(list1) < len(list2):
#         print("additional columns") 
#         for item in list1:
#             if item not in list2:
#                 # extra_colmns.append(item)
#                 print("Invalid Format") 
#                 err           
#             else:
#                 pass
#     print("data imported")
# latest()

class MappingAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        question_master = MappingDetails.objects.all()
        serializer =  MappingDetailsSerializer(question_master,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    objdbops =None

    def __init__(self):
        self.objdbops=dbops()
        
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data mapping details",request.data)

        excel_field = request.data['excel_fields']
        addedby = request.data['addedby']
        department = request.data['department']
        portfolio = request.data['portfolio']
        filepath = request.data['filepath']

        map_dtls = MappingDetails.objects.all()
        queryset_list = list(map_dtls.values())
        mappingdf = pd.DataFrame(queryset_list)
        print("mapping_df",mappingdf.columns.tolist())

        if mappingdf.empty:
            for index,excel in enumerate(excel_field):
                counter = index+1
                obj = MappingDetails(excel_fields = excel,database_fields = "field_"+str(counter),addedby = addedby,department = department,portfolio = portfolio)
                obj.save()
        else:
            list1 = mappingdf['excel_fields'].tolist() # mapping table field
            list2 = excel_field #excel file fields
            extra_colmns = []
            # for excel, database in [(x,y) for x in excel_field for y in database_field]:
            if len(list1) < len(list2):
                print("additional columns")
                for item in list1:
                    if item not in list2:
                        # extra_colmns.append(item)
                        print("Invalid Format")
                        return Response( {"isvalid":"true","msg":"Invalid File Format"}, status=status.HTTP_200_OK)
                    else:
                        pass

                # for index,excel in enumerate(extra_colmns):
                #     obj = MappingDetails.objects.all().last()
                #     num = obj.database_fields.split('_')
                #     print("num-------------------",num)
                #     counter = int(num[1])+1
                #     department = "MRM"
                #     portfolio = ""
                #     obj = MappingDetails(excel_fields = excel,database_fields = "field"+"_"+str(counter),addedby = addedby,department = department,portfolio = portfolio)
                #     obj.save()
                # pass
                # return Response( {"msg":"additional columns"}, status=status.HTTP_200_OK)
            elif len(list1) == len(list2):
                print("columns length is same")
                if sorted(list1) == sorted(list2):
                    print("column names are same")
                    pass
                else:
                    print("columns are not same")
                    return Response( {"isvalid":"true","msg":"Columns are not same"}, status=status.HTTP_200_OK)
            else:
                print("Invalid file format")
                return Response( {"isvalid":"true","msg":"Invalid file format"}, status=status.HTTP_200_OK)


        # file_path = 'C:/Jayesh/OwnProjects/forntendrmse/modelval/static/data.csv'
        # file_path = filepath
        exceldf = pd.read_csv(filepath)
        print("exceldf----------",exceldf)
        
        for id,excelrow in exceldf.iterrows():
            str1= " insert into Database_Fields ("
            strvalues=""
            for row in map_dtls:
                str1 += row.database_fields + ","
                strvalues +=  "'" + str(excelrow[row.excel_fields]) +"',"

            str1+=" addedby,adddate,Department,Portfolio"
            strvalues+= str(addedby)+",getdate()"+",'"+department+"','"+portfolio+"'"
            strQ=str1+") values ("+strvalues+")"
            self.objdbops.insertRow(strQ)
            print("str1",str1)
            print("strvalues",strvalues)
            print("strQ",strQ)
        return Response( {"isvalid":"true","msg":"File Imported Successfully"}, status=status.HTTP_200_OK)

class FLMappingAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        question_master = FlMappingDetails.objects.all()
        serializer =  FLMappingDetailsSerializer(question_master,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    objdbops =None

    def __init__(self):
        self.objdbops=dbops()
        
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data mapping details",request.data)

        excel_field = request.data['excel_fields']
        addedby = request.data['addedby']
        department = request.data['department']
        portfolio = request.data['portfolio']
        filepath = request.data['filepath']

        map_dtls = FlMappingDetails.objects.all()
        queryset_list = list(map_dtls.values())
        mappingdf = pd.DataFrame(queryset_list)
        print("mapping_df",mappingdf.columns.tolist())

        # db_field  = mappingdf['database_fields'].tolist()
        # print("database fields",db_field)

        if mappingdf.empty:
            for index,excel in enumerate(excel_field):
                counter = index+1
                obj = FlMappingDetails(excel_fields = excel,database_fields = "field_"+str(counter),addedby = addedby,department = department,portfolio = portfolio)
                obj.save()
        else:
            list1 = mappingdf['excel_fields'].tolist() # mapping table field
            list2 = excel_field #excel file fields
            print("list1",list1)
            print("list2",list2)
            extra_colmns = []
            # for excel, database in [(x,y) for x in excel_field for y in database_field]:
            if len(list1) < len(list2):
                print("additional columns")
                for item in list1:
                    if item not in list2:
                        # extra_colmns.append(item)
                        print("Invalid Format")
                        return Response( {"isvalid":"true","msg":"Invalid File Format"}, status=status.HTTP_200_OK)
                    else:
                        pass
                
                unique_col = list(set(list1) ^ set(list2)) #Symetric difference
                print(unique_col)   # ['Designation']
                db_field  = mappingdf['database_fields'].tolist()
                print("database fields",db_field)

                # for index,excel in enumerate(list2):
                #     counter = index+1
                #     obj = FlMappingDetails(excel_fields = excel,database_fields = "field_"+str(counter),addedby = addedby,department = department,portfolio = portfolio)
                #     obj.save()

                for index,excel in enumerate(unique_col):
                    obj = FlMappingDetails.objects.all().last()
                    num = obj.database_fields.split('_')
                    print("num-------------------",num)
                    counter = int(num[1])+1
                    department = "MRM"
                    portfolio = ""
                    obj = FlMappingDetails(excel_fields = excel,database_fields = "field"+"_"+str(counter),addedby = addedby,department = department,portfolio = portfolio)
                    obj.save()
                pass
                # return Response( {"msg":"additional columns imported"}, status=status.HTTP_200_OK)
            elif len(list1) == len(list2):
                print("columns length is same")
                if sorted(list1) == sorted(list2):
                    print("column names are same")
                    pass
                else:
                    print("columns are not same")
                    
                    return Response( {"isvalid":"true","msg":"Columns are not same"}, status=status.HTTP_200_OK)
            else:
                print("Invalid file format 1")
                return Response( {"isvalid":"true","msg":"Invalid file format"}, status=status.HTTP_200_OK)


        # file_path = 'C:/Jayesh/OwnProjects/forntendrmse/modelval/static/data.csv'
        # file_path = filepath
        exceldf = pd.read_csv(filepath)
        print("exceldf----------",exceldf)
        
        for id,excelrow in exceldf.iterrows():
            str1= " insert into FL_Data ("
            strvalues=""
            for row in map_dtls:
                str1 += row.database_fields + ","
                strvalues +=  "'" + str(excelrow[row.excel_fields]) +"',"

            str1+=" addedby,adddate,Department,Portfolio"
            strvalues+= str(addedby)+",getdate()"+",'"+department+"','"+portfolio+"'"
            strQ=str1+") values ("+strvalues+")"
            self.objdbops.insertRow(strQ)
            print("str1",str1)
            print("strvalues",strvalues)
            print("strQ",strQ)
        return Response( {"isvalid":"true","msg":"FL File Imported Successfully"}, status=status.HTTP_200_OK)


def diffdata():
    list1 = ['Name', 'Age', 'Location'] 
    list2 = ['Name', 'Age', 'Location', 'Designation','abc']
    diff = list(set(list2) ^ set(list1))
    print("new diff check---------------",diff)   # ['Designation']
diffdata()

class PerfMontrMappingAPI(APIView):
    objdbops =None

    def __init__(self):
        self.objdbops=dbops()
        
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data Perf Montr mapping details",request.data)

        excel_field = request.data['excel_fields']
        addedby = request.data['addedby']
        exceldf = request.data['exceldf']
        mdl_id = request.data['mdl_id']
        utility_type = request.data['datatype']
        # filepath = request.data['filepath']

        map_dtls = PerfMonitoringMappingDetails.objects.filter(mdl_id = mdl_id,datatype = utility_type)
        queryset_list = list(map_dtls.values())
        mappingdf = pd.DataFrame (queryset_list)
        print("mapping df all",mappingdf)
        print("Perf Montr mapping_df",mappingdf.columns.tolist())

        if mappingdf.empty:
            for index,excel in enumerate(excel_field):
                counter = index+1
                obj = PerfMonitoringMappingDetails(excel_fields = excel,database_fields = "Field_"+str(counter),addedby = addedby,adddate = datetime.now(),mdl_id = mdl_id,datatype = utility_type)
                obj.save()
        else:
            list1 = mappingdf['excel_fields'].tolist() # mapping table field
            list2 = excel_field #excel file fields
            print("list1 chk-----",list1)
            print("list2 chk-----",list2)
            extra_colmns = []

            if len(list1) < len(list2):
                print("additional columns")
                for item in list1:
                    if item not in list2:
                        # extra_colmns.append(item)
                        print("Invalid Format")
                        return Response( {"isvalid":"true","msg":"Invalid File Format"}, status=status.HTTP_200_OK)
                    else:
                        pass

            elif len(list1) == len(list2):
                print("columns length is same")
                if sorted(list1) == sorted(list2):
                    print("column names are same")
                    pass
                else:
                    print("columns are not same")
                    return Response( {"isvalid":"true","msg":"Columns are not same"}, status=status.HTTP_200_OK)
            else:
                print("Invalid file format")
                return Response( {"isvalid":"true","msg":"Invalid file format"}, status=status.HTTP_200_OK)


        # file_path = 'C:/Jayesh/OwnProjects/forntendrmse/modelval/static/data.csv'
        # file_path = filepath
        exceldf_a = exceldf#pd.read_csv(filepath)
        print("exceldf----------",exceldf_a)
        exceldf = pd.DataFrame(exceldf_a)

        for id,excelrow in exceldf.iterrows():
            print("excelrow")
            str1= " insert into Perf_Monitoring_Database_Fields ("
            strvalues=""
            for row in map_dtls:
                str1 += row.database_fields + ","
                strvalues +=  "'" + str(excelrow[row.excel_fields]) +"',"

            str1+=" addedby,adddate,datatype,mdl_id"
            # strvalues+= str(addedby)+",getdate()"+utility_type
            strvalues+= str(addedby)+",getdate()"+",'"+utility_type+"','"+mdl_id+"'"
            # strvalues+= str(addedby)+",getdate()"+",'"+utility_type+"'"
            strQ=str1+") values ("+strvalues+")"
            self.objdbops.insertRow(strQ)
            print("str1",str1)
        
            print("strvalues",strvalues)
            print("strQ",strQ)
        return Response( {"isvalid":"true","msg":"File Imported Successfully"}, status=status.HTTP_200_OK)



        # if serializer.is_valid():
        #     serializer.save()
        #     return Response({'data':serializer.data,'msg':'Mapping  Data Saved Successufully'},status=status.HTTP_201_CREATED)
        # return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class DatabaseFieldAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        question_master = DatabaseFields.objects.all()
        serializer =  DatabaseFieldsSerializer(question_master,many=True)

        empty_model_columns = {}
        table_name = DatabaseFields._meta.db_table  # Get the table name for the model

        # Step 3: Check if the table is empty
        if DatabaseFields.objects.count() == 0:  # If no records in the table
            # Step 4: Get the column names (fields) from the model
            field_names = [field.name for field in DatabaseFields._meta.fields]
            
            # Add the table name and its fields to the dictionary
            empty_model_columns[table_name] = field_names

        # Step 5: Output the empty models and their column names
        columns = []
        for table, columns in empty_model_columns.items():
            # columns.append(columns)
            print(f"Empty Model Table: {table}, Columns: {columns}")
        print("columns",json.dumps(columns))
        return Response({'columns':json.dumps(columns)}, status=status.HTTP_200_OK)

class FieldAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        print("request_data",request.data)
        try:
            department = request.data['department']
            portfolio = request.data['portfolio']
            
            if id:
                obj = FieldDetails.objects.get(field_aid=id)
                serializer = FieldsSerializer(obj)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            
            fieldmaster = FieldDetails.objects.filter(department = department,portfolio = portfolio)
            # fieldmaster = FieldDetails.objects.filter(Q(department='MRMedited') | Q(portfolio='MRM_1'))
            serializer =  FieldsSerializer(fieldmaster,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("error is",e)

    def put(self,request):
        try:
            request_data = request.data
            print("request data",request.data)
            id=request.data['field_aid']
            smp = FieldDetails.objects.get(field_aid=id)
            obj = FieldDetails.objects.filter(field_aid = id).update(excel_fields = request.data['Excel_Field'],addedby = request.data['added_by'],adddate = datetime.now())
            return Response({'msg':'Field is Updated Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            print("error is ",e)
            return Response({'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
        
class valueAPI(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data value",request.data)
        serializer = ValueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Value is Saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class ControllClassAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            obj = Controllclassmaster.objects.get(controllclass_aid=id)
            serializer = ControllclassmasterSerializer(obj)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        master = Controllclassmaster.objects.all()
        serializer =  ControllclassmasterSerializer(master,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data",request.data)
        serializer = ControllclassmasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Controll Class Master is created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:   
            id=request.data['id']
            smp = Controllclassmaster.objects.get(controllclass_aid=id)
        except Controllclassmaster.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'controll class does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ControllclassmasterSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Risk Master is Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
class RiskMasterAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            obj = Riskmaster.objects.get(risk_aid=id)
            serializer = RiskmasterSerializer(obj)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        master = Riskmaster.objects.all()
        serializer =  RiskmasterSerializer(master,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data",request.data)
        serializer = RiskmasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Risk Master is created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = Riskmaster.objects.get(risk_aid=id)
        except Riskmaster.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Risk Master does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RiskmasterSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Risk Master is Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    
# class FLReportContentAPI(APIView):
#     permission_classes=[IsAuthenticated]
#     def get(self,request,id=None):
#         allocation_obj = FlReportTemplateTemp.objects.all().values_list('template_name',flat=True).distinct()       
#         temp_name = [i for i in allocation_obj]
#         print("temp_name-------------",temp_name)
#         # for i in allocation_obj:
#         #     print("i",i)
#         #     temp_name.append(i)
#         rptcontentobj = FlReportContent.objects.values('template_name')
#         serializer =  FlReportContentSerializer(rptcontentobj,many=True)
#         return Response(temp_name, status=status.HTTP_200_OK)
    
#     def post(self,request):
#         obj = FlReportContent.objects.filter(fl_report_content_aid = request.data['report_template_aid'],template_name = request.data['template_name']).first()
#         if obj:
#             item = FlReportContent.objects.get(fl_report_content_aid = request.data['report_template_aid'],template_name = request.data['template_name'])
#             data = FlReportContentSerializer(instance=item, data=request.data)        
#             if data.is_valid():
#                 data.save()
#                 return Response({'data':data.data,'msg':'FL Report Content Updated Successfully'},status=status.HTTP_201_CREATED)
#             return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
#         else:
#             serializer = FlReportContentSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({'data':serializer.data,'msg':'FL Report Content Saved Successfully'},status=status.HTTP_201_CREATED)
#             return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
        
class GetUtilityAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if request.data['utility'] == 'None':
            obj = Riskmaster.objects.values('utility').distinct()
            utility_list = [value['utility'] for value in obj]

            mrmUsers=objmaster.getMRMUsers()

            utility_counts = Riskmaster.objects.values('utility').annotate(total_utility=Count('risk_aid'))
            max_utility = utility_counts.aggregate(max_count=Max('total_utility'))['max_count']

            return Response({"status": "success", "data": utility_list,'mrmUsers':mrmUsers,'utility_max_count':max_utility}, status=status.HTTP_200_OK)
        else:
            obj = Riskmaster.objects.filter(utility=request.data['utility'])
            serializer = RiskmasterSerializer(obj,many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

from django.db.models import Count, Max

class saveriskcomments(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data",request.data)  
        obj = RiskFactorComments.objects.get(risk_id = request.data['risk_id'])
        if obj:
            RiskFactorComments.objects.filter(risk_id = request.data['risk_id']).update(utility = request.data['utility'],comments = request.data['comments'],department = request.data['department'])
            return Response({'msg':'Risk Factor comment is Updated Successufully'},status=status.HTTP_201_CREATED)
        else:
            serializer = RiskFactorCommentsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'msg':'Risk Factor comment is created Successufully'},status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
#02262975526

class FLSettingAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        obj = FlSetting.objects.all()
        serializer = FlSettingSerializer(obj,many=True)
        return Response({"status":"success","data": serializer.data}, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data",request.data)
        serializer = FlSettingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'FL Setting is created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)


#Add Question
class add_question_ans(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):        
        question_text=request.data['question']
        answer_type=request.data['answer_type']
        # answer_text=request.data['answer_text']

        options_value=request.data['options_value']
        print("options_value",options_value)
        
        headers=request.data['headers']
        print("headers",headers)

        numRows=request.data['numRows']
        numCols=request.data['numCols']

        sub_question = request.data['sub_question']
        sub_answer_type= request.data['sub_answer_type']
        sub_options_value=request.data['sub_options_value']

        print("sub_question , sub_answer_type , sub_options_value",sub_question,sub_answer_type,sub_options_value)

        ##mongodb save

        # ques_ans_data={'Mdl_Id':(request.data['vt_mdl']),'question_text':question_text,'answer_type':answer_type,'options_value':options_value,
        #                     'headers':headers,'sub_question':sub_question,'sub_answer_type':sub_answer_type,'sub_options_value':sub_options_value,
        #                     'numRows':numRows,'numCols':numCols,'cycle':''}
        
        
        question_ans_id=QuestionAnswerMaster.objects.create(question_text=question_text,answer_type=answer_type)
        if options_value:
            for i in options_value:
                options_obj=QuestionOtionsMaster.objects.create(question=question_ans_id,question_option=i)

        ##table data save question
        if headers:
            for i in headers:
                table_obj=QuestionTableMaster.objects.create(question_tab=question_ans_id,table_header=i,table_row=numRows,
                table_column=numCols)
        
        ## Sub Question add
        sub_question_ans_id=SubQuestionAnswerMaster.objects.create(question_sub=question_ans_id,
                            sub_question_text=sub_question,sub_question_type=sub_answer_type)
                            
        if sub_options_value:
            for i in sub_options_value:
                sub_options_obj=SubQuestionOtionsMaster.objects.create(sub_question=sub_question_ans_id,sub_question_option=i)

        print("saved")
        return Response({'is_taken':False},status=status.HTTP_200_OK)

class MdlIdDataCheck(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        print("request_data",request.data)
        try:
            obj_chk =  PerfMonitoringMappingDetails.objects.filter(mdl_id=request.data['mdlid']).first()
            print("obj_chk----------",obj_chk)
            if obj_chk:
                print("inasadc------------------------")
                return Response({"status":"success","data_a": "Find"}, status=status.HTTP_200_OK)                
            else:
                return Response({"status":"success","data_a": None}, status=status.HTTP_200_OK)
        except Exception as e:
            print("error data is",e)
            return Response({"status":"Failure","data_a": None,'mdldata':None}, status=status.HTTP_200_OK)

class ModelMatricDataAPI(APIView): 
    objdbops =None

    def __init__(self):
        self.objdbops=dbops()

    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        print("request_data model",request.data)
        try:
            obj = PerfMonitoringMappingDetails.objects.get(mdl_id=request.data['mdlid'],excel_fields=request.data['model_matrics'],datatype=request.data['datatype'])
            print("obj------------",obj)
            db_field = obj.database_fields[0].lower() + obj.database_fields[1:] if obj.database_fields else obj.database_fields
            data = PerfMonitoringDatabaseFields.objects.filter(mdl_id = request.data['mdlid'],datatype = request.data['datatype']).values(db_field,'adddate')
            df = pd.DataFrame(list(data))
            print("df---",df)

            strQ = "WITH    nums AS (" 
            # strQ+=" concat(u.U_FName,' ',u.U_LName) addedby,upper(concat(left(u.U_FName,1),left(u.U_LName,1))) uinitials,case when resp.addedBy="+str(request.data['addedby'])+" then 'S' else 'R' end msgcss"
            strQ+="SELECT  TRY_CAST( "+obj.database_fields+" as float) colval, ROW_NUMBER() OVER (ORDER BY [AddDate]) AS rn"
            strQ+=" FROM    [Perf_Monitoring_Database_Fields] "
            strQ+=" where  mdl_id='"+request.data['mdlid']+"' and datatype='"+request.data['datatype']+"'"
            # strQ+=" where datatype='"+request.data['datatype']+"'"
            strQ+=" ) SELECT abs(tp.colval - tf.colval) colval "
            strQ+=" FROM nums tp "
            strQ+="JOIN    nums tf ON tf.rn = tp.rn + 1"
            print("asdf--------------------",strQ)
            tableResult=  self.objdbops.getTable(strQ) 
            
            # if tableResult.empty == False:
            mdldata=  list(tableResult['colval'])
            print("mdldata",mdldata)


            return Response({"status":"success","data": df,'mdldata':mdldata}, status=status.HTTP_200_OK)
        except Exception as e:
            print("error is in model----",e)
            return Response({"status":"Failure","data": None,'mdldata':None}, status=status.HTTP_200_OK)
    

class FlReportTitleCommentAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data title-------------",request.data)
        try:
            obj = FlReportTitleComment.objects.filter(portfolio=request.data['portfolio'],utility = request.data['utility'],department = request.data['department'],addedby=request.data['addedby']).first()
            if obj:
                update_obj = FlReportTitleComment.objects.filter(portfolio=request.data['portfolio'],utility = request.data['utility'],department = request.data['department'],addedby=request.data['addedby']).update(title = request.data['title'],comment = request.data['comment'])
                return Response({'msg':'FL Title and comment is Updated Successufully'},status=status.HTTP_201_CREATED)
            else:
                pass
            serializer = FlReportTitleCommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'msg':'FL Title and comment is Saved Successufully'},status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
        
class FlImportData(APIView): 
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data import-------------",request.data)
        try:
            # obj = FlReportTitleComment.objects.filter(portfolio=request.data['portfolio'],utility = request.data['utility'],department = request.data['department'],addedby=request.data['addedby']).first()
            df = request.data['df']
            print("dataframe check------------",df)
            serializer = FlRawDataSerializer(data=df[0])
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'msg':'Excel data import successfully'},status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class InherentRiskRatingAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops =dbops()

    def get(self,request,id=None):
        
        rating_1 = InherentRiskRating.objects.all()
        serializer_1 =  InherentRiskRatingSerializer(rating_1,many=True)

        rating_2 = ControlEffectivenessRating.objects.all()
        serializer_2 =  ControlEffectivenessRatingSerializer(rating_2,many=True)

        rating_3 = ResidualRating.objects.values('ratings').distinct().all()
        serializer_3 =  ResidualRatingSerializer(rating_3,many=True)
        print("serializer_3--------",serializer_3.data)

        strQ="SELECT Residual_Rating.*,concat('residual_val_',Control_Effectiveness_Rating_AID,'_',Inherent_Risk_Rating_AID) res_id"
        strQ+=" FROM Residual_Rating , Inherent_Risk_Rating,Control_Effectiveness_Rating where Residual_Rating.Inherent_risk_rating = Inherent_Risk_Rating.Ratings and Residual_Rating.Control_effectiveness_rating = Control_Effectiveness_Rating.Ratings"
        print("query strq",strQ)
        tableResult =self.objdbops.getTable(strQ)
        residual_lst = tableResult.to_json(orient='records')
        print("residual ratings result",json.loads(residual_lst))

        data = {'rating_1':serializer_1.data,'rating_2':serializer_2.data,'rating_3':json.loads(residual_lst),'rating_manual':serializer_3.data}
        return Response(data, status=status.HTTP_200_OK)

class ICQInherentRiskRatingAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops =dbops()

    def get(self,request,id=None):
        
        rating_1 = IcqInherentRiskRating.objects.all()
        serializer_1 =  IcqInherentRiskRatingSerializer(rating_1,many=True)

        rating_2 = IcqControlEffectivenessRating.objects.all()
        serializer_2 =  IcqControlEffectivenessRatingSerializer(rating_2,many=True)

        rating_3 = IcqResidualRating.objects.values('ratings').distinct().all()
        serializer_3 =  IcqResidualRatingSerializer(rating_3,many=True)
        print("serializer_3--------",serializer_3.data)

        strQ="SELECT DISTINCT ICQ_Residual_Rating.*,concat('residual_val_',ICQ_Control_Effectiveness_Rating_AID,'_',ICQ_Inherent_Risk_Rating_AID) res_id"
        strQ+=" FROM ICQ_Residual_Rating , ICQ_Inherent_Risk_Rating,ICQ_Control_Effectiveness_Rating where ICQ_Residual_Rating.Inherent_risk_rating = ICQ_Inherent_Risk_Rating.Ratings and ICQ_Residual_Rating.Control_effectiveness_rating = ICQ_Control_Effectiveness_Rating.Ratings"
        print("query strq",strQ)
        tableResult =self.objdbops.getTable(strQ)
        residual_lst = tableResult.to_json(orient='records')
        print("residual ratings result",json.loads(residual_lst))

        data = {'rating_1':serializer_1.data,'rating_2':serializer_2.data,'rating_3':json.loads(residual_lst),'rating_manual':serializer_3.data}
        return Response(data, status=status.HTTP_200_OK)
    

    
    
class FetchResidualRating(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        print("request_data------------------------ new",request.data)
        try:
            obj_chk =  ResidualRating.objects.filter(inherent_risk_rating=request.data['inherendRisk'],control_effectiveness_rating = request.data['controleffect']).first()
            print("obj_chk----------",obj_chk.ratings)

            # if obj_chk:
            #     print("inasadc------------------------")
            return Response({"status":"success","rating": obj_chk.ratings}, status=status.HTTP_200_OK)                
            # else:
            #     return Response({"status":"success","data_a": None}, status=status.HTTP_200_OK)
        except Exception as e:
            print("error data is",e)
            return Response({"status":"Failure","rating": None,'mdldata':None}, status=status.HTTP_200_OK)
    
class ICQFetchResidualRating(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        print("request_data------------------------ new",request.data)
        try:
            obj_chk =  IcqResidualRating.objects.filter(inherent_risk_rating=request.data['inherendRisk'],control_effectiveness_rating = request.data['controleffect']).first()
            print("obj_chk----------",obj_chk.ratings)

            # if obj_chk:
            #     print("inasadc------------------------")
            return Response({"status":"success","rating": obj_chk.ratings}, status=status.HTTP_200_OK)                
            # else:
            #     return Response({"status":"success","data_a": None}, status=status.HTTP_200_OK)
        except Exception as e:
            print("error data is",e)
            return Response({"status":"Failure","rating": None,'mdldata':None}, status=status.HTTP_200_OK)
    

class FLQuestionRatingDataAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        master = FlQuestionRatingData.objects.all()
        serializer =  FlQuestionRatingDataSerializer(master,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SaveResidualRatingsAPI(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data ratings",request.data)
        try:            
            obj_1 = InherentRiskRating.objects.get(inherent_risk_rating_aid = int(request.data['inherent_risk_rating']))
            inherent_risk_rating = obj_1.ratings
            print("inherent_risk_rating",inherent_risk_rating)
            obj_2 = ControlEffectivenessRating.objects.get(control_effectiveness_rating_aid = int(request.data['control_effective_rating']))
            control_eff_rating = obj_2.ratings
            print("control_eff_rating",control_eff_rating)
            obj_chk =  ResidualRating.objects.filter(inherent_risk_rating=inherent_risk_rating,control_effectiveness_rating = control_eff_rating).first()
            print("obj_chk",obj_chk)
            if obj_chk:
                obj_chk_1 =  ResidualRating.objects.filter(inherent_risk_rating=inherent_risk_rating,control_effectiveness_rating = control_eff_rating).update(ratings = request.data['residual_rating'],addedby = request.data['addedby'])
                return Response({'data':obj_chk_1,'msg':'Residual Rating added Successufully'},status=status.HTTP_201_CREATED)
            else:
                data = {
                    'ratings':request.data['residual_rating'],
                    'inherent_risk_rating':inherent_risk_rating,
                    'control_effectiveness_rating':control_eff_rating,
                    'addedby':request.data['addedby']
                }
                # obj_chk_1 =  ResidualRating.objects(ratings = request.data['residual_rating'],inherent_risk_rating =  inherent_risk_rating,control_effectiveness_rating = control_eff_rating, addedby = request.data['addedby'])
                # return Response({'data':obj_chk_1,'msg':'Residual Rating Save Successufully'},status=status.HTTP_201_CREATED)
                serializer = ResidualRatingSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                return Response({'data':serializer.data,'msg':'Residual Rating added Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'data':"",'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
 


class ALLInherentRatingAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            obj = InherentRiskRating.objects.get(inherent_risk_rating_aid=id)
            serializer = InherentRiskRatingSerializer(obj)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        obj = InherentRiskRating.objects.all()
        serializer = InherentRiskRatingSerializer(obj,many=True)
        return Response({"status":"success","data": serializer.data}, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data",request.data)
        
        serializer = InherentRiskRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Inherent Risk Rating is Saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = InherentRiskRating.objects.get(inherent_risk_rating_aid=id)

        except InherentRiskRating.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Inherent risk rating does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ControlEffectivenessRatingSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Inherent Risk Rating is Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
class ControlEffectiveRatingAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            obj = ControlEffectivenessRating.objects.get(control_effectiveness_rating_aid=id)
            serializer = ControlEffectivenessRatingSerializer(obj)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        obj = ControlEffectivenessRating.objects.all()
        serializer = ControlEffectivenessRatingSerializer(obj,many=True)
        return Response({"status":"success","data": serializer.data}, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data",request.data)
        
        serializer = ControlEffectivenessRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Control Effective Rating is Saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = ControlEffectivenessRating.objects.get(control_effectiveness_rating_aid=id)

        except ControlEffectivenessRating.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Inherent risk rating does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ControlEffectivenessRatingSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Control Effective Rating is Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    

class FLReportSubSectionMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        print("request data section",request.data)
        if request.data['is_taken'] == 'true':
            usr = FlReportTemplateTemp.objects.filter(template_name = request.data['template_name'],rpt_section_aid=request.data['rpt_section_aid']).first()
            serializer_a = FLReportTemplateTempSerializer(usr)
            
            secdata = FlRptSubSectionMaster.objects.filter(rpt_section_aid = request.data['rpt_section_aid'])
            serializer =  FLRptSubSectionMasterSerializer(secdata,many=True)
            return Response({"status": "success", "data": serializer.data,"data2":serializer_a.data}, status=status.HTTP_200_OK)
        RptSection = FlRptSubSectionMaster.objects.all()
        serializer =  FLRptSubSectionMasterSerializer(RptSection,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request sub section",request.data)
        serializer = FLRptSubSectionMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'FL Report Sub Section created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)


class FLReportTemplateTempAPI(APIView):
    permission_classes=[IsAuthenticated]
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data",request.data)
        request_data = request.data
        tempobj = FlReportTemplateTemp.objects.filter(template_name = request_data['template_name'],rpt_section_aid = request_data['rpt_section_aid'],rpt_sub_section_aid = 0,rpt_sub_sub_section_aid = 0).first()
        mainobj = FlReportTemplate.objects.filter(template_name = request_data['template_name'],rpt_section_aid = request_data['rpt_section_aid'],rpt_sub_section_aid = 0,rpt_sub_sub_section_aid = 0).first()
        if tempobj:
            if request_data['rpt_sub_section_aid'] != 0:
                pass
            else:
                return Response({'data':'','msg':'Template section Already Exist'},status=status.HTTP_201_CREATED)
        else:
            pass

        if mainobj:
            if request_data['rpt_sub_section_aid'] != 0:
                pass
            else:
                return Response({'data':'','msg':'Template section Already Exist'},status=status.HTTP_201_CREATED)
        else:
            pass


        tempobj1 = FlReportTemplateTemp.objects.filter(template_name = request_data['template_name'],rpt_section_aid = request_data['rpt_section_aid'],rpt_sub_section_aid = request_data['rpt_sub_section_aid'],rpt_sub_sub_section_aid = 0).first()
        mainobj1 = FlReportTemplate.objects.filter(template_name = request_data['template_name'],rpt_section_aid = request_data['rpt_section_aid'],rpt_sub_section_aid = request_data['rpt_sub_section_aid'],rpt_sub_sub_section_aid = 0).first()
        if tempobj1:
            if request_data['rpt_sub_sub_section_aid'] != 0:
                pass
            else:
                return Response({'data':'','msg':'Template sub section Already Exist'},status=status.HTTP_201_CREATED)
        else:
            pass

        if mainobj1:
            if request_data['rpt_sub_sub_section_aid'] != 0:
                pass
            else:
                return Response({'data':'','msg':'Template sub section Already Exist'},status=status.HTTP_201_CREATED)
        else:
            pass

        tempobj2 = FlReportTemplateTemp.objects.filter(template_name = request_data['template_name'],rpt_section_aid = request_data['rpt_section_aid'],rpt_sub_section_aid = request_data['rpt_sub_section_aid'],rpt_sub_sub_section_aid = request_data['rpt_sub_sub_section_aid']).first()
        mainobj2 = FlReportTemplateTemp.objects.filter(template_name = request_data['template_name'],rpt_section_aid = request_data['rpt_section_aid'],rpt_sub_section_aid = request_data['rpt_sub_section_aid'],rpt_sub_sub_section_aid = request_data['rpt_sub_sub_section_aid']).first()
        if tempobj2:
            return Response({'data':'','msg':'Template sub section Already Exist'},status=status.HTTP_201_CREATED)
        else:
            pass

        if mainobj2:
            return Response({'data':'','msg':'Template sub section Already Exist'},status=status.HTTP_201_CREATED)
        else:
            pass
        
        indxsec = FlReportTemplateTemp.objects.filter(template_name = request_data['template_name']).last()
        print("indxsec new",indxsec)
        print("------------------1")
        if indxsec == None:
            request_data['index_section'] = 1
            if request_data['rpt_sub_section_aid'] == 0:
                request_data['index_sub_section'] = 0
            else:
                # request_data['index_sub_section'] = 11
                request_data['index_sub_section'] = 1
            if request_data['rpt_sub_sub_section_aid'] == 0:
                request_data['index_sub_sub_section'] = 0
            else:
                # request_data['index_sub_sub_section'] = 111
                request_data['index_sub_sub_section'] = 1
            # request_data['rpt_sub_section_aid'] = int(request.data['rpt_sub_section_aid'])
            # request_data['rpt_sub_sub_section_aid'] = int(request.data['rpt_sub_sub_section_aid'])
        else:
            sec_aid = FlReportTemplateTemp.objects.filter(template_name = request_data['template_name'],rpt_section_aid = request_data['rpt_section_aid']).first()
            print("-------------2",sec_aid)
            
            if sec_aid == None:
                latest = FlReportTemplateTemp.objects.latest("added_on")
                
                # max_value = ReportTemplateTemp.objects.aggregate(max_value=Max('template_name'))['max_value']
                max_value = FlReportTemplateTemp.objects.filter(template_name = request_data['template_name']).aggregate(max_value=Max('index_section'))['max_value']
                request_data['index_section'] = max_value+1
                request_data['index_sub_section'] = 0
                request_data['index_sub_sub_section'] = 0
            else:
                print("--------------3","if")                
                request_data['index_section'] = sec_aid.index_section
                max_value = FlReportTemplateTemp.objects.filter(template_name = request_data['template_name'],rpt_section_aid = request_data['rpt_section_aid']).aggregate(max_value=Max('index_sub_section'))['max_value']
                # request_data['index_sub_section'] = str(sec_aid.index_section)+str(1)
                request_data['index_sub_section'] = max_value+1
                indx_sub_sub_scn = FlReportTemplateTemp.objects.filter(template_name = request_data['template_name'],rpt_section_aid = request_data['rpt_section_aid'],rpt_sub_sub_section_aid = request_data['rpt_sub_sub_section_aid']).aggregate(max_value=Max('index_sub_sub_section'))['max_value']
                print("indx_sub_sub_scn",indx_sub_sub_scn)
                if indx_sub_sub_scn == None:
                    request_data['index_sub_sub_section'] = 0
                else:
                    request_data['index_sub_sub_section'] = indx_sub_sub_scn
                
            if request_data['rpt_sub_sub_section_aid'] == 0:
                pass
            else:
                sub_sec_aid = FlReportTemplateTemp.objects.filter(template_name = request_data['template_name'],rpt_section_aid = request_data['rpt_section_aid'],rpt_sub_section_aid = request_data['rpt_sub_section_aid']).first()
                if sub_sec_aid == None:
                    latest = FlReportTemplateTemp.objects.latest("added_on")
                    max_value = FlReportTemplateTemp.objects.filter(template_name =  request_data['template_name']).aggregate(max_value=Max('index_sub_section'))['max_value']
                    request_data['index_sub_section']  = max_value+1
                    # request_data['index_sub_sub_section'] = 111
                    request_data['index_sub_sub_section'] = 1
                else:
                    request_data['index_section'] = sub_sec_aid.index_section
                    request_data['index_sub_section'] = sub_sec_aid.index_sub_section
                    max_value = FlReportTemplateTemp.objects.filter(template_name = request_data['template_name'],rpt_section_aid = request_data['rpt_section_aid'],rpt_sub_section_aid = request_data['rpt_sub_section_aid']).aggregate(max_value=Max('index_sub_sub_section'))['max_value']
                    if max_value == 0:
                        # request_data['index_sub_sub_section'] = str(sub_sec_aid.index_sub_section)+str(1)
                        request_data['index_sub_sub_section'] = 1
                    else:
                        request_data['index_sub_sub_section'] = int(max_value)+1

                # if sub_sec_aid.rpt_sub_section_aid == request_data['rpt_sub_section_aid']:
                #     request_data['index_sub_section'] = 11
                #     request_data['index_sub_sub_section'] = 111
                # else:
                #     KJB ='L'
                    


            # request_data['index_sub_section'] = indxsec.index_sub_section+1
            # if request_data['rpt_sub_sub_section_aid'] == 0:
            #     request_data['index_sub_sub_section'] = 0
            # else:
            #     # request_data['index_sub_sub_section'] = 1
            #     request_data['index_sub_sub_section'] = indxsec.index_sub_sub_section+1
        print("request data no 2",request_data)
        serializer = FLReportTemplateTempSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Report Template created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
    


class FLReportSubSubSectionMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if request.data['is_taken'] == 'true':
            usr = FlReportTemplateTemp.objects.filter(template_name = request.data['template_name'],rpt_sub_section_aid=request.data['rpt_sub_section_aid']).first()
            serializer_a = FLReportTemplateTempSerializer(usr)

            secdata = FlRptSubSubSectionMaster.objects.filter(rpt_sub_section_aid = request.data['rpt_sub_section_aid'])
            serializer =  FLRptSubSubSectionMasterSerializer(secdata,many=True)
            return Response({"status": "success", "data": serializer.data,"data2":serializer_a.data}, status=status.HTTP_200_OK)
        RptSection = FlRptSubSubSectionMaster.objects.all()
        serializer =  FLRptSubSubSectionMasterSerializer(RptSection,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = FLRptSubSubSectionMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Report Sub Sub Section created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
    
class ICQSaveResidualRatingsAPI(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data ratings",request.data)
        try:            
            obj_1 = IcqInherentRiskRating.objects.get(icq_inherent_risk_rating_aid = int(request.data['inherent_risk_rating']))
            inherent_risk_rating = obj_1.ratings
            print("inherent_risk_rating",inherent_risk_rating)
            obj_2 = IcqControlEffectivenessRating.objects.get(icq_control_effectiveness_rating_aid = int(request.data['control_effective_rating']))
            control_eff_rating = obj_2.ratings
            print("control_eff_rating",control_eff_rating)
            obj_chk =  IcqResidualRating.objects.filter(inherent_risk_rating=inherent_risk_rating,control_effectiveness_rating = control_eff_rating).first()
            print("obj_chk",obj_chk)
            if obj_chk:
                obj_chk_1 =  IcqResidualRating.objects.filter(inherent_risk_rating=inherent_risk_rating,control_effectiveness_rating = control_eff_rating).update(ratings = request.data['residual_rating'],addedby = request.data['addedby'])
                return Response({'data':obj_chk_1,'msg':'Residual Rating added Successufully'},status=status.HTTP_201_CREATED)
            else:
                data = {
                    'ratings':request.data['residual_rating'],
                    'inherent_risk_rating':inherent_risk_rating,
                    'control_effectiveness_rating':control_eff_rating,
                    'addedby':request.data['addedby']
                }
                # obj_chk_1 =  ResidualRating.objects(ratings = request.data['residual_rating'],inherent_risk_rating =  inherent_risk_rating,control_effectiveness_rating = control_eff_rating, addedby = request.data['addedby'])
                # return Response({'data':obj_chk_1,'msg':'Residual Rating Save Successufully'},status=status.HTTP_201_CREATED)
                serializer = IcqResidualRatingSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                return Response({'data':serializer.data,'msg':'ICQ Residual Rating added Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'data':"",'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
 
class ICQALLInherentRatingAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            obj = IcqInherentRiskRating.objects.get(icq_inherent_risk_rating_aid=id)
            serializer = IcqInherentRiskRatingSerializer(obj)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        obj = IcqInherentRiskRating.objects.all()
        serializer = IcqInherentRiskRatingSerializer(obj,many=True)
        return Response({"status":"success","data": serializer.data}, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data",request.data)
        
        serializer = IcqInherentRiskRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'ICQ Inherent Risk Rating is Saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = IcqInherentRiskRating.objects.get(icq_inherent_risk_rating_aid=id)

        except IcqInherentRiskRating.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'ICQ Inherent risk rating does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = IcqInherentRiskRatingSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'ICQ Inherent Risk Rating is Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
class ICQControlEffectiveRatingAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            obj = IcqControlEffectivenessRating.objects.get(icq_control_effectiveness_rating_aid=id)
            serializer = IcqControlEffectivenessRatingSerializer(obj)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        obj = IcqControlEffectivenessRating.objects.all()
        serializer = IcqControlEffectivenessRatingSerializer(obj,many=True)
        return Response({"status":"success","data": serializer.data}, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data",request.data)
        
        serializer = IcqControlEffectivenessRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'ICQ Control Effective Rating is Saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = IcqControlEffectivenessRating.objects.get(icq_control_effectiveness_rating_aid=id)

        except IcqControlEffectivenessRating.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Inherent risk rating does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = IcqControlEffectivenessRatingSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'ICQ Control Effective Rating is Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
class UdaapRatings(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:            
            context={'sections':objmaster.getUdaapSections(),'Qtns':objmaster.getAllUdaapQtnsAndRatings()}
            return Response( context, status=status.HTTP_200_OK)
        except Exception as e: 
            print(traceback.print_exc())  
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data",request.data)
        try:
            objmaster.Udaap_insertRatings(request.data['question_id'],request.data['ratings_yes'],request.data['ratings_no'],request.data['doc_na'])
            return Response({'msg':'rating saved successfully'}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST) 

class UdaapQtnsFinal(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:            
            context={'FLRating':objreg.getUdaapRatingsFinal(objmaster.getmaxFLId()), 
                                                        'sections':objmaster.getUdaaptnSectionFinal(),'Qtns':objmaster.getUdaapQtnsFinal()}
            return Response( context, status=status.HTTP_200_OK)
        except Exception as e: 
            print(traceback.print_exc())  
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class UdaapInherentRiskRatingAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops =dbops()

    def get(self,request,id=None):
        
        rating_1 = UdaapInherentRiskRating.objects.all()
        serializer_1 =  UdaapInherentRiskRatingSerializer(rating_1,many=True)

        rating_2 = UdaapControlEffectivenessRating.objects.all()
        serializer_2 =  UdaapControlEffectivenessRatingSerializer(rating_2,many=True)

        rating_3 = UdaapResidualRating.objects.values('ratings').distinct().all()
        serializer_3 =  UdaapResidualRatingSerializer(rating_3,many=True)

        strQ="SELECT Udaap_Residual_Rating.*,concat('residual_val_',Udaap_Control_Effectiveness_Rating_AID,'_',Udaap_Inherent_Risk_Rating_AID) res_id"
        strQ+=" FROM Udaap_Residual_Rating , Udaap_Inherent_Risk_Rating,Udaap_Control_Effectiveness_Rating where Udaap_Residual_Rating.Inherent_risk_rating = Udaap_Inherent_Risk_Rating.Ratings and Udaap_Residual_Rating.Control_effectiveness_rating = Udaap_Control_Effectiveness_Rating.Ratings"
        print("query strq udaap",strQ)
        tableResult =self.objdbops.getTable(strQ)
        residual_lst = tableResult.to_json(orient='records')
        print("residual ratings result",json.loads(residual_lst))

        data = {'rating_1':serializer_1.data,'rating_2':serializer_2.data,'rating_3':json.loads(residual_lst),'rating_manual':serializer_3.data}
        return Response(data, status=status.HTTP_200_OK)


class UdaapFetchResidualRating(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        print("request_data------------------------ new",request.data)
        try:
            obj_chk =  UdaapResidualRating.objects.filter(inherent_risk_rating=request.data['inherendRisk'],control_effectiveness_rating = request.data['controleffect']).first()
            print("obj_chk----------",obj_chk.ratings)

            # if obj_chk:
            #     print("inasadc------------------------")
            return Response({"status":"success","rating": obj_chk.ratings}, status=status.HTTP_200_OK)                
            # else:
            #     return Response({"status":"success","data_a": None}, status=status.HTTP_200_OK)
        except Exception as e:
            print("error data is",e)
            return Response({"status":"Failure","rating": None,'mdldata':None}, status=status.HTTP_200_OK)
    

class getUdaapSecQtnFinal(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:  
            return Response( {'sections':objmaster.getUdaapQtnsFinal()}, status=status.HTTP_200_OK)
        except Exception as e:
            print(traceback.print_exc()) 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class saveUdaapRatingsFinal(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:          
            colDataLst = request.data['colDataLst']
            print("colDataLst",colDataLst)
            uid=request.data['uid']
            json_colDataLst = json.loads(colDataLst)
            objreg=Register()
            maxid=objmaster.getmaxFLId()
            for colval in json_colDataLst: 
                objreg.updateUdaapRatingsFinal(colval["qtnId"],colval["ddl_yesno_"],colval["ddl_doc_"],colval["txt_comment_"],colval['ddl_InherentRisk_'],colval['ddl_ControllEffectiveness_'],colval['ddl_Residual_'],colval['txt_control_desc_'],colval['ddl_override_Residual_'], colval['txt_override_comment_'],uid,maxid)
 
            return Response( {'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class UdaapSaveResidualRatingsAPI(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data ratings",request.data)
        try:            
            obj_1 = UdaapInherentRiskRating.objects.get(udaap_inherent_risk_rating_aid = int(request.data['inherent_risk_rating']))
            inherent_risk_rating = obj_1.ratings
            print("inherent_risk_rating",inherent_risk_rating)
            obj_2 = UdaapControlEffectivenessRating.objects.get(udaap_control_effectiveness_rating_aid = int(request.data['control_effective_rating']))
            control_eff_rating = obj_2.ratings
            print("control_eff_rating",control_eff_rating)
            obj_chk =  UdaapResidualRating.objects.filter(inherent_risk_rating=inherent_risk_rating,control_effectiveness_rating = control_eff_rating).first()
            print("obj_chk",obj_chk)
            if obj_chk:
                obj_chk_1 =  UdaapResidualRating.objects.filter(inherent_risk_rating=inherent_risk_rating,control_effectiveness_rating = control_eff_rating).update(ratings = request.data['residual_rating'],addedby = request.data['addedby'])
                return Response({'data':obj_chk_1,'msg':'Residual Rating added Successufully'},status=status.HTTP_201_CREATED)
            else:
                data = {
                    'ratings':request.data['residual_rating'],
                    'inherent_risk_rating':inherent_risk_rating,
                    'control_effectiveness_rating':control_eff_rating,
                    'addedby':request.data['addedby']
                }
                # obj_chk_1 =  ResidualRating.objects(ratings = request.data['residual_rating'],inherent_risk_rating =  inherent_risk_rating,control_effectiveness_rating = control_eff_rating, addedby = request.data['addedby'])
                # return Response({'data':obj_chk_1,'msg':'Residual Rating Save Successufully'},status=status.HTTP_201_CREATED)
                serializer = UdaapResidualRatingSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                return Response({'data':serializer.data,'msg':'Udaap Residual Rating added Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'data':"",'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class UdaapALLInherentRatingAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            obj = UdaapInherentRiskRating.objects.get(udaap_inherent_risk_rating_aid=id)
            serializer = UdaapInherentRiskRatingSerializer(obj)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        obj = UdaapInherentRiskRating.objects.all()
        serializer = UdaapInherentRiskRatingSerializer(obj,many=True)
        return Response({"status":"success","data": serializer.data}, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data",request.data)
        
        serializer = UdaapInherentRiskRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Udaap Inherent Risk Rating is Saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = UdaapInherentRiskRating.objects.get(udaap_inherent_risk_rating_aid=id)

        except UdaapInherentRiskRating.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Udaap Inherent risk rating does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UdaapInherentRiskRatingSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Udaap Inherent Risk Rating is Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
 
class UdaapControlEffectiveRatingAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            obj = UdaapControlEffectivenessRating.objects.get(udaap_control_effectiveness_rating_aid=id)
            serializer = UdaapControlEffectivenessRatingSerializer(obj)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        obj = UdaapControlEffectivenessRating.objects.all()
        serializer = UdaapControlEffectivenessRatingSerializer(obj,many=True)
        return Response({"status":"success","data": serializer.data}, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data",request.data)
        
        serializer = UdaapControlEffectivenessRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Udaap Control Effective Rating is Saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = UdaapControlEffectivenessRating.objects.get(udaap_control_effectiveness_rating_aid=id)

        except UdaapControlEffectivenessRating.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Inherent risk rating does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UdaapControlEffectivenessRatingSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Udaap Control Effective Rating is Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)


class UdaapQtns(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try: 
            uid=request.data['uid'] 
            return Response({'canupdate':objmaster.UdaapcanUpdateRatings(uid),'sections':objmaster.getUdaapQtnSection(uid),
                           'Qtns':objmaster.getUdaapQtns(uid),'models':objmaster.getUdaapModels(str(uid))}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            print(traceback.print_exc())
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

############


class UdaapQuestions(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try: 
            
            return Response({'Qtns':objmaster.getAllUdaapQtns(),}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            print(traceback.print_exc())
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class addUdaapQtns(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:             
            return Response({'sections':objmaster.getUdaapSections()}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            print(traceback.print_exc())
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class getUdaapSub_Sections(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:             

            return Response({'subsections':objmaster.getUdaapSub_Sections(request.data['sub_secid'])}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            print(traceback.print_exc())
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)


class getUdaapSub_Sub_Sections(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:             
            return Response({'subsections':objmaster.getUdaapSub_Sub_Sections(request.data['sub_secid'])}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            print(traceback.print_exc())
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class getUdaapSub_Sub_Sub_Sections(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:             
            return Response({'subsections':objmaster.getUdaapSub_Sub_Sub_Sections(request.data['sub_secid'])}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            print(traceback.print_exc())
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class Udaap_add_question(APIView):
    permission_classes=[IsAuthenticated] 
    def post(self,request):
        try:   
            print("udaap api request_data",request.data)     
            added_by=request.data['uid']
            adddate=datetime.now()
            section=request.data['section']
            sub_section=request.data['sub_section']
            sub_sub_section=request.data['sub_sub_section']
            sub_sub_sub_section=request.data['sub_sub_sub_section']
            question=request.data['question'] 
            if sub_section == '':
                sub_section=None
            if sub_sub_section == '':
                sub_sub_section =None
            if sub_sub_sub_section == '':
                sub_sub_sub_section =None      
            question_obj=UdaapQuestionMaster(question_label=question,section_aid=section,sub_section_aid=sub_section,
                                                        sub_sub_section_aid=sub_sub_section,sub_sub_sub_section_aid=sub_sub_sub_section,
                                                        addedby=added_by,adddate=adddate)
            question_obj.save()
            print("saved")
            return JsonResponse({'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)
        

class addUdaapSection(APIView):
    permission_classes=[IsAuthenticated] 
    def post(self,request):
        try: 
            request_data = request.data
            obj = UdaapSections(section_label = request_data['text'],activestatus = request_data['activests'],section_description = request_data['desc'],addedby = request_data['uid'])
            obj.save()
            return JsonResponse({'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e:
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class addUdaapSubSection(APIView):
    permission_classes=[IsAuthenticated] 
    def post(self,request):
        try: 
            request_data = request.data
            obj = UdaapSubSections(sub_section_label = request_data['text'],section_aid = request_data['secid'],activestatus = request_data['activests'],sub_section_description = request_data['desc'],addedby = request_data['uid'])
            obj.save()
            return JsonResponse({'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e:
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class addUdaapSubSubSection(APIView):
    permission_classes=[IsAuthenticated] 
    def post(self,request):
        try: 
            request_data = request.data
            obj = UdaapSubSubSections(sub_sub_section_label = request_data['text'],sub_section_aid = request_data['sub_secid'],activestatus = request_data['activests'],sub_sub_section_description = request_data['desc'],addedby = request_data['uid'])
            obj.save()
            return JsonResponse({'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e:
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class addUdaapSubSubSubSection(APIView):
    permission_classes=[IsAuthenticated] 
    def post(self,request):
        try: 
            request_data = request.data
            obj = UdaapSubSubSubSections(sub_sub_sub_section_label = request_data['text'],sub_sub_section_aid = request_data['sub_secid'],activestatus = request_data['activests'],sub_sub_sub_section_description = request_data['desc'],addedby = request_data['uid'])
            obj.save()
            return JsonResponse({'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e:
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)


##############

class getUdaapSecQtn(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try: 
            uid=request.data['id'] 
            return Response({'Qtns':objmaster.getUdaapQtns(uid),}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            print(traceback.print_exc())
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class saveUdaapRatings(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try: 
            colDataLst = request.data['colDataLst']
            print("colDataLst",colDataLst)
            uid=request.data['uid']
            json_colDataLst = json.loads(colDataLst)
            print("json_colDataLst",json_colDataLst)
            objreg=Register()
            for colval in json_colDataLst:
                print('col val is ',colval )
                # objreg.insertFLRatings(colval["qtnId"],colval["ddl_yesno_"],colval["ddl_doc_"],colval["txt_comment_"],uid,objmaster.getmaxFLId())
                obj = UdaapQuestionRatingData.objects.filter(review_id=objmaster.getmaxFLId(),question_aid=colval["qtnId"],addedby=uid)
                if obj:    
                    print("if")
                    UdaapQuestionRatingData.objects.filter(review_id=objmaster.getmaxFLId(),question_aid=colval["qtnId"],addedby=uid).update(rating_yes_no=colval["ddl_yesno_"],doc_yes_no=colval["ddl_doc_"],comments=colval["txt_comment_"],inherent_risk_rating = colval['ddl_InherentRisk_'],control_effectiveness_ratings = colval['ddl_ControllEffectiveness_'],residual_ratings = colval['ddl_Residual_'],control_description= colval['txt_control_desc_'],override_residual_ratings = colval['ddl_override_Residual_'],override_comments = colval['txt_override_comment_'])
                else: 
                    print("else")
                    try:   
                        print("review_id",objmaster.getmaxFLId(),"question_aid",colval["qtnId"])
                        save_obj = UdaapQuestionRatingData.objects.create(review_id=objmaster.getmaxFLId(),question_aid=colval["qtnId"],rating_yes_no=colval["ddl_yesno_"],doc_yes_no=colval["ddl_doc_"],comments=colval["txt_comment_"],inherent_risk_rating = colval['ddl_InherentRisk_'],control_effectiveness_ratings = colval['ddl_ControllEffectiveness_'],residual_ratings = colval['ddl_Residual_'],control_description= colval['txt_control_desc_'],override_residual_ratings = colval['ddl_override_Residual_'],override_comments = colval['txt_override_comment_'],addedby=uid)

                    except Exception as e:
                        print("error is",e.__traceback__)
            return Response({'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class submitUdaapRatings1(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try: 
            print("check---------------------------",request.data)
            objreg.UdaapsubmitRatings(objmaster.getmaxFLId())
            uid=request.data['uid']
            objmaster.insert_notification(str(uid),'MRM-Head','FL','Rating Submitted',1)    
            return JsonResponse({'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e: 
            print("error is",e)
            error_saving(request,e)  
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)
    
class publishUdaap(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            objmaster.publishUdaap() 
            return Response( {"isvalid":"true"}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)


class UdaapSettingAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            obj = UdaapSetting.objects.get(fls_aid=id)
            serializer = UdaapSettingSerializer(obj)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        obj = UdaapSetting.objects.all()
        serializer = UdaapSettingSerializer(obj,many=True)
        return Response({"status":"success","users": serializer.data}, status=status.HTTP_200_OK)
        # return Response({"status":"success","users": users}, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data",request.data)
        
        # serializer = UdaapSettingSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        strQ="INSERT INTO Udaap_Setting (FLS_Text ,FLS_Remarks,FLS_EndDate,AddedBy,AddDate,publish) "
        strQ += " VALUES('"+ str(request.data['fls_text']).replace("'","''")+"','"+ str(request.data['fls_remarks']).replace("'","''")+"','"+ str(request.data['fls_enddate']) +"','"+ str(request.data['addedby']) +"',getdate(),0)"
        print(strQ)
        insertRow(strQ)
        return Response({'msg':'Udaap Setting is Saved Successufully'},status=status.HTTP_201_CREATED)
        # return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    # permission_classes=[IsAuthenticated]
    # def put(self,request):
    #     try:
    #         id=request.data['id']
    #         smp = UdaapInherentRiskRating.objects.get(udaap_inherent_risk_rating_aid=id)

    #     except UdaapInherentRiskRating.DoesNotExist:
    #         # msg = {'msg':'Department does not exist'}
    #         return Response({'msg':'Udaap Inherent risk rating does not exist'}, status=status.HTTP_404_NOT_FOUND)
    #     serializer = UdaapInherentRiskRatingSerializer(smp,data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'data':serializer.data,'msg':'Udaap Inherent Risk Rating is Updated Successufully'},status=status.HTTP_201_CREATED)
    #     return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    

class UdaapAllocation(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            section=request.data['section']
            sub_section=request.data=['sub_section']
            sub_sub_section=request.data['sub_sub_section']
            sub_sub_sub_section=request.data['sub_sub_sub_section']

            if sub_section == '' and sub_sub_section == '' and sub_sub_sub_section == '':
                print("session selected")
                question_obj_filter=UdaapQuestionMaster.objects.filter(section_aid=section)
            elif sub_sub_section == '' and sub_sub_sub_section == '':
                print("sub section selected")
                question_obj_filter=UdaapQuestionMaster.objects.filter(Q(sub_section_aid=sub_section) | Q(section_aid=section))
            elif sub_sub_sub_section == '':
                print("sub sub section selected")
                question_obj_filter=UdaapQuestionMaster.objects.filter(Q(sub_sub_section_aid=sub_sub_section) | Q(sub_section_aid=sub_section) | Q(section_aid=section))  
    
            else:
                print("else")
                question_obj_filter=UdaapQuestionMaster.objects.filter(section_aid=section,sub_section_aid=sub_section,
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
            return Response({"status":"success","data": dict_data}, status=status.HTTP_200_OK)    
            # return JsonResponse({'data':dict_data},safe=False)
	# #Jayesh Code 
            # userobj = Users.objects.all()
            # review_name = IcqQuestionRatingAllocation.objects.values('review_id','review_name').distinct()
            # print("review name",review_name)

        
            # return Response( {"isvalid":"true",'sections':objmaster.getSections(),'user':userobj,'review':objmaster.getICQIds()}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class getUdaapAllocation(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        userobj = Users.objects.all()
        serializer = UserSerializer(userobj,many=True)
        review_name = UdaapQuestionRatingAllocation.objects.values('review_id','review_name').distinct()
        # print("review name",review_name)
        return Response( {"isvalid":"true",'sections':objmaster.getUdaapSections(),'user':serializer.data,'review':objmaster.getUdaapIds()}, status=status.HTTP_200_OK)

class save_udaap_allocation(APIView):
    def post(self,request):  
        try:     
            section_aid = request.data['section_aid']
            users = request.data['users']
            # end_date = request_data['end_date'][6:] + "-" + request_data['end_date'][3:5] + "-" + request_data['end_date'][:2]
            if request.data['rv_id'] == "addnew":
                last_rvid_obj = UdaapQuestionRatingAllocation.objects.aggregate(max('review_id'))
                last_rvid = last_rvid_obj['review_id__max']
                splt_rvid = last_rvid.split('_')
                latest_rvid = int(splt_rvid[1]).__add__(1) #used magic method django
                for user, section_id in [(x,y) for x in users for y in section_aid]:
                    allocate_obj = UdaapQuestionRatingAllocation(review_id ="Rv_"+str(latest_rvid),review_name = request.data['rv_name'],section_aid = section_id,allocated_to = user,end_date = None)
                    allocate_obj.save()
                return Response( {"isvalid":"true"}, status=status.HTTP_200_OK) 
            else:
                for user, section_id in [(x,y) for x in users for y in section_aid]:
                    allocate_obj = UdaapQuestionRatingAllocation(review_id =request.data['rv_id'],review_name = request.data['rv_name'],section_aid = section_id,allocated_to = user,end_date = None)
                    allocate_obj.save() 
                return Response( {"isvalid":"true"}, status=status.HTTP_200_OK)
        except Exception as e: 
            print(traceback.print_exc())
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)
        
class FLDocsPoliciesProcedure(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            obj = FlPoliciesProcedureDocuments.objects.get(mdl_doc_id=id)
            serializer = FlPoliciesProcedureDocumentsSerializer(obj)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        obj = FlPoliciesProcedureDocuments.objects.all()
        serializer = FlPoliciesProcedureDocumentsSerializer(obj,many=True)
        return Response({"status":"success","users": serializer.data}, status=status.HTTP_200_OK)

    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data",request.data)
        
        serializer = FlPoliciesProcedureDocumentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'FL Docs Policies and Procedure is Saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)


class PrdnHistoryData(APIView): 
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try: 
            print("request data api",request.data)
            objreg=Register() 
            prdnData=objreg.getPrndHistoricalData(request.data['mdl_id'],request.data['mm_type']) 
            
            return Response({'prdnData':prdnData},status=status.HTTP_200_OK)
           
        except Exception as e:
            print('setuppycaret is ',e)
            print('setuppycaret traceback is ', traceback.print_exc()) 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class Save_Buss_KPI_Monitoring_Override_History(APIView):
    permission_classes=[IsAuthenticated]  
    def post(self,request):    
        try:      
            strQ="INSERT INTO Buss_KPI_Monitoring_Override_History(Mdl_ID,Metric,New_Value,Added_by,Added_On,freq_idx,freq_val)  VALUES ("
            strQ +="'"+str(request.data['Mdl_ID'])+"',"+request.data['Metric']+",'"+str(request.data['New_Value'])+"','"+str(request.data['Added_by'])+"',getdate(),"+str(request.data['freq_idx'])+", getdate())"
            print("strQ Insert History ",strQ)
            objdbops.insertRow(strQ)
            return Response({'data':"",'msg':'Model Matrics Updated Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            print("error ",e, traceback.print_exc())
            return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class Save_Buss_KPI_Monitoring_Final_Result(APIView):
    permission_classes=[IsAuthenticated]  
    def post(self,request):    
        try:
            strQ="delete from Buss_KPI_Monitoring_Final_Result where Mdl_ID='"+str(request.data['Mdl_ID']+"' and Metric="+ str(request.data['Metric']) + " and freq_idx="+str(request.data['freq_idx']))
            objdbops.insertRow(strQ) 

            strQ="INSERT INTO Buss_KPI_Monitoring_Final_Result(Mdl_ID,Metric,Metric_flag,Added_by,Added_On,freq_idx,freq_val)  VALUES ("
            strQ +="'"+str(request.data['Mdl_ID'])+"',"+request.data['Metric']+",'"+str(request.data['New_Value'])+"','"+str(request.data['Added_by'])+"',getdate(),"+str(request.data['freq_idx'])+",getdate())"
            print("strQ Insert Buss_KPI_Monitoring_Final_Result ",strQ)
            objdbops.insertRow(strQ)

            return Response({'data':"",'msg':'Model Matrics Updated Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            print("error ",e, traceback.print_exc())
            return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

            
class Save_Performance_Monitoring_Resolution(APIView):
    permission_classes=[IsAuthenticated]  
    def post(self,request):    
        try:  
            strQ="INSERT INTO Performance_Monitoring_Resolution(Mdl_ID,Resolution,Added_by,Added_On)  VALUES ("
            strQ +="'"+str(request.data['Mdl_ID'])+"','"+request.data['Resolution']+"','"+str(request.data['Added_by'])+"',getdate())"
            print("strQ Insert Performance_Monitoring_Resolution ",strQ)
            objdbops.insertRow(strQ)

            return Response({'data':"",'msg':'Model Matrics Updated Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            print("error ",e, traceback.print_exc())
            return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class Save_Buss_KPI_Monitoring_Resolution(APIView):
    permission_classes=[IsAuthenticated]  
    def post(self,request):    
        try:  
            print("save buss check",request.data)
            strQ="INSERT INTO Buss_KPI_Monitoring_Resolution(Mdl_ID,Resolution,Added_by,Added_On,freq_idx,freq_val)  VALUES ("
            strQ +="'"+str(request.data['Mdl_ID'])+"','"+request.data['Resolution']+"','"+str(request.data['Added_by'])+"',getdate(),"+str(request.data['Added_by'])+",getdate())"
            print("strQ Insert Buss_KPI_Monitoring_Resolution ",strQ)
            objdbops.insertRow(strQ)

            return Response({'data':"",'msg':'Model Matrics Updated Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            print("error ",e, traceback.print_exc())
            return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

def Convert_Date(date_str):
    # Parse the ISO format string
    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    # Convert to desired format
    formatted_date = dt.strftime("%m/%d/%Y")
    print(formatted_date)
    return formatted_date


class ValidationPlanningAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        print("request_data validation Planning",request.data)
        obj = ValidationPlanning.objects.filter(mdl_id = request.data['mdl_id'])
        serializer = ValidationPlanningSerializer(obj,many=True)
        print("serializer data check",json.loads(json.dumps(serializer.data)))
        if len(json.loads(json.dumps(serializer.data))) == 0:
            start_date = None
            end_date = None
            revised_date = None
        else:
            start_date = Convert_Date(json.loads(json.dumps(serializer.data))[0]['projected_start_date'])
            end_date = Convert_Date(json.loads(json.dumps(serializer.data))[0]['projected_end_date'])
            revised_date = (Convert_Date(json.loads(json.dumps(serializer.data))[0]['revised_end_date'])if json.loads(json.dumps(serializer.data))[0]['revised_end_date'] else None)
            
        print("dates",start_date," ",end_date," ",revised_date)
        curr_dates = {
            'start_date':start_date,
            'end_date':end_date,
            'revised_date':revised_date
        }
        

        strQ="select format(DATEADD(year,vfm.Val_Frequency,projected_start_date),'MM/dd/yyyy') next_projected_start_date, "
        strQ+="  format(DATEADD(year,vfm.Val_Frequency,projected_end_date),'MM/dd/yyyy') next_projected_end_date,  "
        strQ+=" cast( format(DATEADD(year,vfm.Val_Frequency,TRY_CONVERT(date, '01/' + validation_period, 103)),'MM/yyyy') as varchar ) next_val_period "
        strQ+=" from mdl_risks as mr left join Mdl_Risk_Master as mrm"
        strQ+="  on mr.mdl_risks= mrm.risk_val,Val_Frequency_Mst as vfm , validation_planning val_plan  where"
        strQ+=" lower(vfm.mdl_risk)=mdl_risk_label and val_plan.mdl_id=mr.mdl_id and  mr.mdl_id='"+str(request.data['mdl_id'])+"'"
        print("check updated date",strQ)
        tableResult =objdbops.getTable(strQ)  
        users = tableResult.to_json(orient='records')
        print("check users",users)
        if len(json.loads(users)) == 0:
            all_dates = None
        else:
            all_dates = json.loads(users)[0]
            # print("all dates-----------",json.loads(users)[0])
        print("all dates-----------",all_dates)

        return Response({"status":"success","data": serializer.data,"all_dates":all_dates,"curr_dates":curr_dates}, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):     
        print("request_data validation Planning",request.data)
        chk_val_obj = ValidationPlanning.objects.filter(mdl_id = request.data['mdl_id'] , validation_period = request.data['validation_period']).first()
        print("chk_val_obj",chk_val_obj)
        if chk_val_obj == None:
            serializer = ValidationPlanningSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'msg':'Validation Planning Saved Successufully'},status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                smp = ValidationPlanning.objects.get(mdl_id = request.data['mdl_id'] , validation_period = request.data['validation_period'])
                print("chk_val_obj",smp)
            except ValidationPlanning.DoesNotExist:
                # msg = {'msg':'Department does not exist'}
                return Response({'msg':'Validation Planning does not exist'}, status=status.HTTP_404_NOT_FOUND)
            serializer = ValidationPlanningSerializer(smp,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'msg':'Validation Planning Updated Successufully'},status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
            
class NextValidationPlanningAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        print("request_data Next validation Planning",request.data)
        obj = NextValidationPlanning.objects.filter(mdl_id = request.data['mdl_id'])
        serializer = NextValidationPlanningSerializer(obj,many=True)
        print("serializer data check",json.loads(json.dumps(serializer.data)))
        start_date = Convert_Date(json.loads(json.dumps(serializer.data))[0]['projected_start_date'])
        end_date = Convert_Date(json.loads(json.dumps(serializer.data))[0]['projected_end_date'])
        # revised_date = Convert_Date(json.loads(json.dumps(serializer.data))[0]['revised_end_date'])
        print("dates",start_date," ",end_date)
        Next_curr_dates = {
            'start_date':start_date,
            'end_date':end_date,
        }
        
        strQ="select format(DATEADD(year,vfm.Val_Frequency,projected_start_date),'MM/dd/yyyy') next_projected_start_date, "
        strQ+="  format(DATEADD(year,vfm.Val_Frequency,projected_end_date),'MM/dd/yyyy') next_projected_end_date,  "
        strQ+=" cast( format(DATEADD(year,vfm.Val_Frequency,TRY_CONVERT(date, '01/' + validation_period, 103)),'MM/yyyy') as varchar ) next_val_period "
        strQ+=" from mdl_risks as mr left join Mdl_Risk_Master as mrm"
        strQ+="  on mr.mdl_risks= mrm.risk_val,Val_Frequency_Mst as vfm , validation_planning val_plan  where"
        strQ+=" lower(vfm.mdl_risk)=mdl_risk_label and val_plan.mdl_id=mr.mdl_id and  mr.mdl_id='"+str(request.data['mdl_id'])+"'"
        print("check updated date",strQ)
        tableResult =objdbops.getTable(strQ)  
        users = tableResult.to_json(orient='records')
        print("all dates Next API-----------",json.loads(users)[0])

        return Response({"status":"success","data": serializer.data,"all_dates":json.loads(users)[0],"Next_curr_dates":Next_curr_dates}, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):     
        print("request_data Next validation Planning",request.data)
        chk_val_obj = NextValidationPlanning.objects.filter(mdl_id = request.data['mdl_id'] , validation_period = request.data['validation_period']).first()
        print("chk_val_obj",chk_val_obj)
        if chk_val_obj == None:
            serializer = NextValidationPlanningSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'msg':'Next Validation Planning Saved Successufully'},status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                smp = NextValidationPlanning.objects.get(mdl_id = request.data['mdl_id'] , validation_period = request.data['validation_period'])
                print("chk_val_obj",smp)
            except NextValidationPlanning.DoesNotExist:
                # msg = {'msg':'Department does not exist'}
                return Response({'msg':'Next Validation Planning does not exist'}, status=status.HTTP_404_NOT_FOUND)
            serializer = NextValidationPlanningSerializer(smp,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'msg':'Next Validation Planning Updated Successufully'},status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class Val_Period_Master(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        print()
        val_period_strt_date = ValPeriodMst.objects.get(val_period=1)
        print("projected start date",val_period_strt_date)
        return Response({"status":"success","projected_start_date": val_period_strt_date.val_period_start_dt.strftime("%m/%d/%Y"),}, status=status.HTTP_200_OK)
    
class Val_Frequency_Master_API(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        print()
        val_frequency = ValFrequencyMst.objects.filter(mdl_risk=request.data['mdl_risk']).first()
        print("val_frequency",val_frequency)
        return Response({"status":"success","val_frequency": val_frequency.val_frequency}, status=status.HTTP_200_OK)

class check_Validated_or_not(APIView):
    def get(self,request,id=None):
        request_data = request.data
        print("request_data",request_data)
        strQ="select   case when  cast(format(DATEADD(year,-1*Val_Frequency,getdate()),'yyyy') as int) > "+str(request.data['last_val_period_year'])+" "
        strQ+=" then  'not validated'  else 'validated' end valsts"
        strQ+=" FROM Val_Frequency_Mst where lower(Mdl_Risk)=lower('"+str(request.data['mdl_risk'])+"')"
        print("check valid query",strQ)
        tableResult =objdbops.getTable(strQ)  
        users = tableResult.to_json(orient='records')
        print("user-----------",json.loads(users)[0])
        if json.loads(users)[0]['valsts'] == 'validated':
            print()
            strQ="select cast(format(DATEADD(year,Val_Frequency,'"+str(request.data['last_val_period'])+"' ),'MM/yyyy') as varchar) "
            strQ+=" FROM Val_Frequency_Mst where lower(Mdl_Risk)=lower('"+str(request.data['mdl_risk'])+"')"
            print("validated query",strQ)
            tableResult =objdbops.getTable(strQ)  
            last_val_period = tableResult.to_json(orient='records')
            print("last_val_period 1-----------",json.loads(last_val_period)[0])
            return Response({"status":"success",'last_val_period':json.loads(last_val_period)[0][""]}, status=status.HTTP_200_OK)
        else:            
            val_period_strt_date = ValPeriodMst.objects.get(val_period=1)
            print("projected start curr date",val_period_strt_date.val_period_start_dt)
            a = str(val_period_strt_date.val_period_start_dt)
            b = a.split(" ")
            c = b[0].split("-")
            return Response({"status":"success",'last_val_period':c[1]+"/"+c[0]}, status=status.HTTP_200_OK)
        

class GetICQReportData(APIView):
    def get(self,request,id=None):
        request_data = request.data
        print("request_data",request_data)
        maxid=objmaster.getmaxICQId()
        strQ="SELECT c.response_id,c.section_id,isnull([ICQ_Report_Content].comment,concat('<b>',section_label,'</b><br>',c.comments)) comment,s.section_label,s.section_description FROM "
        strQ+=" Icq_section_comments c INNER JOIN ICQ_Sections s ON c.section_id = s.section_aid "
        strQ+=" left join [ICQ_Report_Content] on  c.section_id = ICQ_Report_Content.[ICQ_Section_ID] and ICQ_Report_Content.ICQ_Cycle_ID = "+maxid+"  where c.cycle_id = "+maxid+" "
        print("check valid query",strQ)
        tableResult =objdbops.getTable(strQ)  
        Icq_report = tableResult.to_json(orient='records')
        print("Icq_report-----------",json.loads(Icq_report))
        return Response({"status":"success","report_data":json.loads(Icq_report)}, status=status.HTTP_200_OK)


class ICQ_ReportContentAPI(APIView):
    # permission_classes=[IsAuthenticated]
    # def get(self,request,id=None):
    #     allocation_obj = FlReportTemplateTemp.objects.all().values_list('template_name',flat=True).distinct()       
    #     temp_name = [i for i in allocation_obj]
    #     print("FL temp_name-------------",temp_name)
    
    #     rptcontentobj = FlReportContent.objects.values('template_name')
    #     serializer =  FL_ReportContentSerializer(rptcontentobj,many=True)
    #     return Response(temp_name, status=status.HTTP_200_OK)

    permission_classes=[IsAuthenticated]
    def post(self,request):
        maxid=objmaster.getmaxICQId()
        request.data['icq_cycle_id'] = maxid
        print("icq report data",request.data)
        obj = IcqReportContent.objects.filter(icq_section_id = request.data['icq_section_id'],icq_cycle_id = maxid).first()
        print("obj",obj)
        if obj:
            # item = IcqReportContent.objects.filter(fl_report_template_aid = request.data['report_template_aid'],template_name = request.data['template_name']).first()
            data = ICQ_ReportContentSerializer(instance=obj, data=request.data)        
            if data.is_valid():
                data.save()
                return Response({'data':data.data,'msg':'ICQ Report Content Updated Successfully'},status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ICQ_ReportContentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'msg':'ICQ Report Content Saved Successfully'},status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)


class checkPendingTasks(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        strQ="select count(taskReg.Task_ID)  cnt  FROM  Task_Relevant_Personnel taskUsers,  Task_ApprovalStatus_Master apprlsts ,\
            Task_Registration taskReg  where taskReg.Task_ID=taskUsers.Task_ID \
            and taskReg.Approval_Status=apprlsts.task_ApprovalStatus_AID and Task_ApprovalStatus_Label <>'Approved' \
            and format(end_date,'yyyy-MM-dd')< format(getdate(),'yyyy-MM-dd') \
            and U_id=" + str(request.data['uid']) +" and (U_Type='Assignee' or U_Type='Approver')"
        tableResult=  self.objdbops.getscalar(strQ)
        print("strQ---------",strQ)
        print("tableResult----------",tableResult)
        if tableResult>0 :
            tableResult=1
        else:
            tableResult=0
        return Response({'data':tableResult},status=status.HTTP_200_OK)
    
###------------------------Ashok code----------------------------------------------###
env = environ.Env()
environ.Env.read_env()
BASE_URL = env("BASE_URL")

plot_dir='/static/media/'

app_url =BASE_URL 

mail_pwd="sxovbflfjwhgssvx"

def insert_data_notification(notification_from,notification_to,utility,notification_trigger,is_visible):
     
    create_date=datetime.now()
    notification_obj=NotificationDetails(notification_from=notification_from,notification_to=notification_to,utility=utility,
                                         notification_trigger=notification_trigger,is_visible=is_visible,create_date=create_date)
    notification_obj.save() 


def send_mrm_head_mail(email_id):
    print("send_mrm_head_mail")
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    mail_content = """Hello,
    This is a simple mail. There is only text, no attachments are there The mail is sent using Python SMTP library.
    Thank You
    """
    # The mail addresses and password
    sender_address = 'modvaladm@gmail.com'
    sender_pass = mail_pwd
    # receiver_address = 'kardeashok15@gmail.com'
    receiver_address = email_id

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    # The subject line
    message['Subject'] = 'A test mail sent by Python.'

    # The body and the attachments for the mail       
    message.attach(MIMEText(mail_content, 'plain'))

    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    # login with mail_id and password
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('MRM Mail Sent')


import smtplib

def send_owner_email(email_id):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    mail_content = """Hello,
    This is a simple mail. There is only text, no attachments are there The mail is sent using Python SMTP library.
    Thank You
    """
    # The mail addresses and password
    sender_address = 'modvaladm@gmail.com'
    sender_pass = mail_pwd
    # receiver_address = 'kardeashok15@gmail.com'
    receiver_address = email_id

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    # The subject line
    message['Subject'] = 'A test mail sent by Python.'

    # The body and the attachments for the mail       
    message.attach(MIMEText(mail_content, 'plain'))

    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    # login with mail_id and password
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


# class getTasks(APIView):
#     permission_classes=[IsAuthenticated]
#     def get(self,request):
#         try:
#             all_data_lst=list()
#             dict_data=dict()  
#             alltasks,taskcnt=objreg.getTaskListByUSerid(request.data['uid'],request.data['mdl_id'])  
#             for irow  in alltasks:       
#                 dict_data['start']= alltasks[irow]["end_date_cal"]     
#                 dict_data['Task_Name']= alltasks[irow]["Task_Name"]  
#                 if alltasks[irow]["css"]=='redEvent':
#                     # //dict_data['className']=alltasks[irow]["css"]
#                     dict_data['title']= alltasks[irow]["Task_ID"] 
#                     dict_data['description']=dict_data['Task_Name'] + " "+str(alltasks[irow]["datedif"])+" days overdue."  
#                     dict_data['textColor']='white'      
#                 else:
#                     # dict_data['className']=alltasks[irow]["css"]
#                     dict_data['title']=alltasks[irow]["Task_ID"] 
#                     dict_data['description']=dict_data['Task_Name'] + " "+str(alltasks[irow]["datedif"])+" days to end."
#                 dict_data['textColor']='white'
#                 dict_data['backgroundColor']= alltasks[irow]["css"] 
#                 dict_data['color']='white'
#                 all_data_lst.append(dict_data.copy())  
#             context={'all_data_lst':json.dumps(all_data_lst),'taskList':alltasks}     
#             return Response( context, status=status.HTTP_200_OK)
           
        # except Exception as e: 
        #     print('error ',traceback.print_exc(),e)
        #     error_saving(request,e)
        #     return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)


class getTasks(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            all_data_lst=list()
            dict_data=dict()  
            alltasks,taskcnt=objreg.getTaskListByUSerid(request.data['uid'],request.data['mdl_id']) 
            print("alltasks--------",alltasks) 
            for irow  in alltasks:       
                dict_data['start']= alltasks[irow]["end_date_cal"]     
                dict_data['Task_Name']= alltasks[irow]["Task_Name"]  
                if alltasks[irow]["css"]=='redEvent':
                    # //dict_data['className']=alltasks[irow]["css"]
                    dict_data['title']= alltasks[irow]["Task_ID"] 
                    dict_data['description']=str(dict_data['Task_Name']) + " "+str(alltasks[irow]["datedif"])+" days overdue."  
                    dict_data['textColor']='white'      
                else:
                    # dict_data['className']=alltasks[irow]["css"]
                    dict_data['title']=alltasks[irow]["Task_ID"] 
                    dict_data['description']=str(dict_data['Task_Name']) + " "+str(alltasks[irow]["datedif"])+" days to end."
                dict_data['textColor']='white'
                dict_data['backgroundColor']= alltasks[irow]["css"] 
                dict_data['color']='white'
                all_data_lst.append(dict_data.copy()) 
            print("dict_data---------",dict_data)
            print("all_data_lst----------",all_data_lst) 
            context={'all_data_lst':json.dumps(all_data_lst),'taskList':alltasks}     
            return Response( context, status=status.HTTP_200_OK)
           
        except Exception as e: 
            print('error ',traceback.print_exc(),e)
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)



class Find_Max_File_Id(APIView):
    
    def get(self,request,id):
        print("id",id)
        mdlid= id
        print("find_max_file_id ",mdlid)
        if(mdlid==""):
            src_file_obj = collection_file_info.find()
        else:
            src_file_obj = collection_file_info.find({'Mdl_Id':mdlid})
        df =  pd.DataFrame(list(src_file_obj)) 
        print(df)
        if len(df)>0: 
            file_id=df['file_id'].max()
            print('file_id 1 ',file_id)
        else:
            file_id=1 #changed by nilesh on 11.4.23
            print('file_id 2 ',file_id)

        return Response(file_id)


class Find_Src_Data(APIView):
    def post(self,request):
        print("request data",request.data)
        file_id=request.data['file_id']
        dataset=request.data['dataset']

        print('dataset is method is ',dataset,file_id)
        if(dataset==''):
            print('inside blank filter')
            src_file_obj = collection.find({"file_id":int(file_id)},{'_id':0})
        else:
            print('dataset ', str(dataset)) 
            dataset = dataset.replace("\'", "\"") 
            dataset=json.loads(dataset)    
            print('dataset is ',dataset)      
            src_file_obj = collection.find(dataset)

        df =  pd.DataFrame(list(src_file_obj))  
        print('len of ad ',len(df))  
        if len(df)>0:
            df.pop('file_id')
        print("src fn dataframe",len(df))
        return Response(df)  

        
class Find_Target_Value(APIView):
    def get(self,request,file_id): 

        print("find_target_value",file_id)    
        target_value_obj=collection_model_target_value.find({'file_id':int(file_id)},{'_id':0})
        target_value="None"
        if len(list(target_value_obj)):
            for j in target_value_obj:
                # print('j',j)
                print("target value data",j['column_name'])
            target_value= j['column_name']  
        return Response (target_value)        

class Dist_Numevari_Catvar(APIView):
    def post(self,request):
       
        print("request data",request.data)
        df_dict=request.data['df_dict']
        df=pd.DataFrame.from_dict(df_dict)
        print("df",df)
        var1=request.data['var1']
        var2=request.data['var2']
        print("var1 2",var1,var2)

        cat_cols = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] in [np.object]]
        noData=""
        if(len(cat_cols)<1):
            return Response({'msg':'No cat var'},status.HTTP_200_OK)
        num_cols = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] not in [np.object]]
        if(var1 != False):
            cat_var = var1  # cat_cols[i]
            num_var = var2  # num_cols[j]
        else:
            cat_var = cat_cols[0]  # cat_cols[i]
            num_var = num_cols[0]  # num_cols[j]
        dist_num_cat = df.groupby(cat_var)[num_var].describe()
        result = dist_num_cat.to_json(orient='index')
        result = json.loads(result)

        return Response({'msg':'','df': result, 'cat_var': cat_var, 'num_var': num_var, 
                         'colNames': dist_num_cat.columns, 'numCols': num_cols,
                           'catCols': cat_cols, 'divHeader': 'Distribution of ' + num_var + ' at ' + cat_var})

class Set_Cols(APIView):
    def post(self,request):
        print("request data",request.data)
        df_dict=request.data['df_dict']
        dff=pd.DataFrame.from_dict(df_dict)
        print("df",dff)
        targetVar =request.data['targetVar']
        print("targetVar",targetVar)
        gridDttypes = []
        if not(targetVar=="None"):
                dff = dff.drop(targetVar, axis=1)
        dttypes = dict(dff.dtypes)
        print("dttypes",dttypes)
        idx=1
        print("dff columns",dff.columns)
        for k in list(dff.columns):
            print("k",k)
        num_cols = [c for i, c in enumerate(
        dff.columns) if dff.dtypes[i] not in [np.object]] 
        print("num_cols",num_cols)
        for i in num_cols:
            gridDttypes.append({'colName': i, 'chkId': idx})
            idx = idx + 1
        print("gridDttypes",gridDttypes)
        del dff
        return Response(gridDttypes)


class downloadIm(APIView):
    from rest_framework.permissions import AllowAny    
    permission_classes = [AllowAny]
    def get(self,request): 
        try:     
            import base64
             
            with open("AUC.png", "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            from io import BytesIO
            from PIL import Image

            file_stream = BytesIO()
            imgpatj=r"D:/Projects/Python/RMSE_API/APIRMSE/app1/M080100_ROCAUC.png"
            image_data = Image.open(open(imgpatj,'rb'))
             
            image_data.save(file_stream,'png')
            file_stream.seek(0)
            base64_data = base64.b64encode(file_stream.getvalue()).decode('utf-8') 
            imgdata = base64.b64decode(base64_data) 
            filename = 'some_image_png.png'  # I assume you have a way of picking unique filenames
            with open(filename, 'wb') as f:
                f.write(imgdata)

            return Response({"status": "success", "base64Data": base64_data }, status=status.HTTP_200_OK)
        except Exception as e:
            print('error ',e,traceback.print_exc())
            return Response({"status": "success", "data": []}, status=status.HTTP_200_OK)



def find_src_data(mdlid,dataset=''): 
        if mdlid=="":
            src_file_obj = collection_file_info.find()
        else:
            src_file_obj = collection_file_info.find({'Mdl_Id':mdlid})
        df =  pd.DataFrame(list(src_file_obj)) 
        if len(df)>0: 
            file_id=df['file_id'].max()
        else:
            file_id=1 #changed by nilesh on 11.4.23
        print('file_id' ,file_id) 

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



class Plotinsoccuvsincstate(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request): 
        additional_param=request.data['additional_param'] 
        if additional_param == "DA":
            df=find_DA_src_data(request.data['mdl_id'],request.data['dataset'])
            
        else:

            df=find_src_data(request.data['mdl_id'],request.data['dataset'])
        
        var1=request.data['var1']
        var2=request.data['var2'] 
        username=request.data['username'] 
        cat_cols_temp = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] in [np.object]] 
        cat_cols=[]
        for x in cat_cols_temp:
            if len(df[x].value_counts())<25:
                cat_cols.append(x)
        if(len(cat_cols)<1):
            return Response({'msg':'No cat var'},status.HTTP_200_OK)
        if(var1 == False):
            var1 = cat_cols[0]
            var2 = cat_cols[1]

        cat_bar = pd.crosstab(df[var1].fillna('Null'), df[var2].fillna('Null'), dropna=True)
        print(var1 ,', ',df[var1].unique(),', null cnt ',df[var1].isnull().sum())
        print(var2 ,', ',df[var2].unique(),', null cnt ',df[var2].isnull().sum())
        print('cat_bar ')
        print(cat_bar.to_json())
        color = plt.cm.inferno(np.linspace(0, 1, 5))
        cat_bar.div(cat_bar.sum(1).astype(float), axis=0).plot(kind='bar', figsize=(10, 6),
                                                               stacked=False,
                                                               color=color)
        plt.title(var2, fontsize=14)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(
            BASE_DIR, plot_dir_view+username+'plotinsoccuvsincstate.png'))
        plt.close()
        del df 
        # saveChartViewd('Bar chart', var1, var2, user_name +
        #                'plotinsoccuvsincstate.png')
         
        # BASE_DIR = Path(__file__).resolve().parent.parent
        pngDir = os.path.join(BASE_DIR, 'static\\media\\')
        savefile_name = pngDir + str(username+'plotinsoccuvsincstate.png')
         


        file_stream = BytesIO() 
        image_data = PIL.Image.open(savefile_name) 
        image_data.save(file_stream,'png') 
        file_stream.seek(0)
        base64_data = base64.b64encode(file_stream.getvalue()).decode('utf-8')
        json_data = dict()
        json_data['report'] = base64_data
        json_data.update({'msg':'','chartType': 'Bar chart', 'pdfFile': plot_dir+username+'Bar chart.pdf',
                   'ddlvar1': cat_cols, 'ddlvar2': cat_cols, 'var1': var1, 'var2': var2,'msg':''})
         
        return JsonResponse(json_data)

def find_DA_src_data(mdlid,dataset=''): 
        print('mdlid ',mdlid)
        if mdlid=="":
            src_file_obj = collection_da_src_file_Info.find()
        else:
            src_file_obj = collection_da_src_file_Info.find({'Mdl_Id':mdlid})
       
        print(src_file_obj)
        df =  pd.DataFrame(list(src_file_obj)) 
        print(' file id ',len(df))
        if len(df)>0: 
            file_id=df['file_id'].max()
        else:
            file_id=1 #changed by nilesh on 11.4.23
        print('file_id' ,file_id) 

        if(dataset=='' or dataset == False):
            print('inside blank filter')
            src_file_obj = collection_da_src_data.find({"file_id":int(file_id)},{'_id':0})
        else:
            print('dataset ', str(dataset)) 
            dataset = dataset.replace("\'", "\"") 
            dataset=json.loads(dataset)    
            print('dataset is ',dataset)      
            src_file_obj = collection_da_src_data.find(dataset,{'_id':0})

        df =  pd.DataFrame(list(src_file_obj))   
        if len(df)>0: 
            df.pop('file_id') 
        return df     

 
class plotinsoccuvsincstatestacked(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request): 
        df=find_src_data(request.data['mdl_id'],request.data['dataset'])
       
        print("df",df)
        var1=request.data['var1']
        var2=request.data['var2']
        print("var1 2",var1,var2)

        username=request.data['username']

        cat_cols_temp = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] in [np.object]]
        cat_cols=[]
        for x in cat_cols_temp:
            if len(df[x].value_counts())<25:
                cat_cols.append(x)
        if(len(cat_cols)<1):
            return Response({'msg':'No cat var'},status.HTTP_200_OK)
            
         
        if(var1 == False):
            var1 = cat_cols[0]
            var2 = cat_cols[1]
        incident = pd.crosstab(df[var1], df[var2])
        # print('var1 ', var1, ' var2 ', var2)
        # occu = pd.crosstab(x_keep[var], df['fraud_reported'])
        colors = plt.cm.inferno(np.linspace(0, 1, 5))
        incident.div(incident.sum(1).astype(float), axis=0).plot(kind='bar',
                                                                 stacked=True,
                                                                 figsize=(
                                                                     10, 6),
                                                                 color=colors)

        plt.title(var2, fontsize=20)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(
            BASE_DIR, plot_dir_view+username+'plotinsoccuvsincstatestacked.png'))
        plt.close()
        del df
        # saveChartViewd('Stacked Bar chart', var1, var2,
        #                user_name+'plotinsoccuvsincstatestacked.png')

        if os.path.exists(os.path.join(
                BASE_DIR, plot_dir_view+username+'plotinsoccuvsincstatestacked.png')):
            pdf = FPDF()
            pdf.add_page()
            # pdf = exportgraphImgPdf(pdf, os.path.join(
            #     BASE_DIR, plot_dir_view+username+'plotinsoccuvsincstatestacked.png'), " Stacked Bar chart "+var1+" vs "+var2)
            pdf.output(os.path.join(
                BASE_DIR, plot_dir_view+username+'Stacked Bar chart.pdf'))

        pngDir = os.path.join(BASE_DIR, 'static\\media\\')
        savefile_name = pngDir + str(username+'plotinsoccuvsincstatestacked.png')
        print("savefile_name",savefile_name)


        file_stream = BytesIO()
        print("file_stream",file_stream)
        image_data = PIL.Image.open(savefile_name)
        print("image_data",image_data)
        image_data.save(file_stream,'png')
        # image_data.save(file_stream.png)
        print("image_data",image_data)
        print("image_data",type(image_data))
        file_stream.seek(0)
        base64_data = base64.b64encode(file_stream.getvalue()).decode('utf-8')
        json_data = dict()
        json_data['report'] = base64_data
        json_data.update({'msg':'','chartType': 'Stacked Bar chart', 'pdfFile': plot_dir+username+'Stacked Bar chart.pdf',
                   'ddlvar1': cat_cols, 'ddlvar2': cat_cols, 'var1': var1, 'var2': var2})
        print("json data",json_data)
        return JsonResponse(json_data)



class stripplot(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request): 
        import matplotlib.pyplot as pltstrip
        import seaborn as snsstrip

        df=find_src_data(request.data['mdl_id'],request.data['dataset'])
       
        print("df",df)
        var_cat=request.data['var_cat']
        var_num=request.data['var_num']
        print("var_cat var_num",var_cat,var_num)

        username=request.data['username']

        cat_cols_temp = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] in [np.object]]

        cat_cols=[]
        for x in cat_cols_temp:
            if len(df[x].value_counts())<25:
                cat_cols.append(x)
        print("cat_cols ",cat_cols)
        if(len(cat_cols)<1):
            return Response({'msg':'No cat var'},status.HTTP_200_OK)
        num_cols_temp = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] not in [np.object]]
        print("num_cols_temp ",num_cols_temp)
        num_cols=[]
        for x in num_cols_temp:
            if len(df[x].value_counts())<25:
                num_cols.append(x)
        print("num_cols",num_cols)
        if(var_num == False):
            var_num = num_cols[0]
            var_cat = cat_cols[1]

        fig = pltstrip.figure(figsize=(15, 8))
        pltstrip.style.use('fivethirtyeight')
        pltstrip.rcParams['figure.figsize'] = (15, 8)

        snsstrip.stripplot(df[var_cat], df[var_num],
                           palette='bone', figure=fig)
        pltstrip.title(var_num, fontsize=20)
        pltstrip.savefig(os.path.join(
            BASE_DIR, plot_dir_view+username+'outputstripplot.png'))
        pltstrip.close()
        # saveChartViewd('Strip Plot', var_num, var_cat,
        #                user_name+'outputstripplot.png',request.session['vt_mdl'],request.session['uid'],request.session['vt_datasetname'])
        del df
        if os.path.exists(os.path.join(
                BASE_DIR, plot_dir_view+username+'outputstripplot.png')):
            pdf = FPDF()
            pdf.add_page()
            # pdf = exportgraphImgPdf(pdf, os.path.join(
            #     BASE_DIR, plot_dir_view+username+'outputstripplot.png'), " Strip Plot "+var_num+" vs "+var_cat)
            pdf.output(os.path.join(
                BASE_DIR, plot_dir_view+username+'Strip Plot.pdf'))

        pngDir = os.path.join(BASE_DIR, 'static\\media\\')
        savefile_name = pngDir + str(username+'outputstripplot.png')
        print("savefile_name",savefile_name)


        file_stream = BytesIO()
        print("file_stream",file_stream)
        image_data = PIL.Image.open(savefile_name)
        print("image_data",image_data)
        image_data.save(file_stream,'png')
        # image_data.save(file_stream.png)
        print("image_data",image_data)
        print("image_data",type(image_data))
        file_stream.seek(0)
        base64_data = base64.b64encode(file_stream.getvalue()).decode('utf-8')
        json_data = dict()
        json_data['report'] = base64_data
        json_data.update({'msg':'', 'chartType': 'Strip Plot', 'pdfFile': plot_dir+username+'Strip Plot.pdf',
                   'ddlvar1': num_cols, 'ddlvar2': cat_cols, 'var1': var_num, 'var2': var_cat, 'hideddl2': ''})
        print("json data",json_data)
        return JsonResponse(json_data)

import joypy

class distribution(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request): 
       
        df=find_src_data(request.data['mdl_id'],request.data['dataset'])
       
        print("df",df)
        var_cat=request.data['var_cat']
        var_num=request.data['var_num']
        print("var_cat var_num",var_cat,var_num)

        username=request.data['username']

        cat_cols_temp = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] in [np.object]]

        cat_cols=[]
        for x in cat_cols_temp:
            if len(df[x].value_counts())<25:
                cat_cols.append(x)

        if(len(cat_cols)<1):
            return Response({'msg':'No cat var'},status.HTTP_200_OK)
        num_cols_temp = [c for i, c in enumerate(
            df.columns) if df.dtypes[i]   in ( [np.int64]or [np.float64])]
        num_cols=[]
        for x in num_cols_temp:
            if len(df[x].value_counts())<2500:
                num_cols.append(x)

        if(var_num == False):
            var_num = num_cols[0]
            var_cat = cat_cols[1]
        fig, axes = joypy.joyplot(df,
                                  column=[var_num],
                                  by=var_cat,
                                  ylim='own',
                                  figsize=(20, 12),
                                  alpha=0.5,
                                  legend=True)

        plt.title(var_num, fontsize=20)
        plt.tight_layout()
        fig.savefig(os.path.join(
            BASE_DIR, plot_dir_view+username+'distbyfraud2.png'))
        # saveChartViewd('Distribution', var_num, var_cat,
        #                user_name+'distbyfraud2.png')
        del df
        if os.path.exists(os.path.join(
                BASE_DIR, plot_dir_view+username+'distbyfraud2.png')):
            pdf = FPDF()
            pdf.add_page()
            # pdf = exportgraphImgPdf(pdf, os.path.join(
            #     BASE_DIR, plot_dir_view+username+'distbyfraud2.png'), " Distribution "+var_num+" vs "+var_cat)
            pdf.output(os.path.join(
                BASE_DIR, plot_dir_view +"/"+username+"Distribution.pdf"))

        pngDir = os.path.join(BASE_DIR, 'static\\media\\')
        savefile_name = pngDir + str(username+'distbyfraud2.png')
        print("savefile_name",savefile_name)
        file_stream = BytesIO()
        print("file_stream",file_stream)
        image_data = PIL.Image.open(savefile_name)
        print("image_data",image_data)
        image_data.save(file_stream,'png')
        # image_data.save(file_stream.png)
        print("image_data",image_data)
        print("image_data",type(image_data))
        file_stream.seek(0)
        base64_data = base64.b64encode(file_stream.getvalue()).decode('utf-8')
        json_data = dict()
        json_data['report'] = base64_data
        json_data.update({'msg':'', 'chartType': 'Distribution', 'pdfFile': plot_dir+username+'Distribution.pdf',
                   'ddlvar1': num_cols, 'ddlvar2': cat_cols, 'var1': var_num, 'var2': var_cat, 'hideddl2': ''})
        print("json data",json_data)
        return JsonResponse(json_data)


import matplotlib.pyplot as pltbox 
class box_plot(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request): 
        import seaborn as snsbox
        df=find_src_data(request.data['mdl_id'],request.data['dataset'])
       
        print("df",df)
        var_cat=request.data['var_cat']
        var_num=request.data['var_num']
        print("var_cat var_num",var_cat,var_num)

        username=request.data['username']

        cat_cols_temp = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] in [np.object]]

        cat_cols=[]
        for x in cat_cols_temp:
            if len(df[x].value_counts())<25:
                cat_cols.append(x)

        if(len(cat_cols)<1):
            return Response({'msg':'No cat var'},status.HTTP_200_OK)
        num_cols_temp = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] not in [np.object]] 

        num_cols=[]
        for x in num_cols_temp:
            if len(df[x].value_counts())<25:
                num_cols.append(x)

        print("num_cols",num_cols)
        print("cat_cols",cat_cols)

        if(var_num == False):
            var_num = num_cols[0]
            var_cat = cat_cols[1]
            # context = {'chartType': 'Box Plot', 'pdfFile': '', 'graphpath': '',
            #            'ddlvar1': num_cols, 'ddlvar2': cat_cols, 'var1': var_num, 'var2': var_cat, 'hideddl2': '', 'postAct': totalclaim_boxplot}
            # return render(request, 'showPlot.html', context)
        fig = pltbox.figure(figsize=(14, 8))
        pltbox.style.use('fivethirtyeight')
        pltbox.rcParams['figure.figsize'] = (20, 8)
        print("var_cat,var_num",df[var_cat],df[var_num])
        print("var_cat,var_num",var_cat,var_num)
        snsbox.boxenplot(df[var_cat], df[var_num], palette='pink', figure=fig)
        pltbox.title(var_num, fontsize=20)
        pltbox.savefig(os.path.join(
            BASE_DIR, plot_dir_view+username+'outputclaimboxplot.png'))
        pltbox.close()
        # saveChartViewd('Box Plot', var_num, var_cat,
        #                user_name+'outputclaimboxplot.png')
        del df
        if os.path.exists(os.path.join(
                BASE_DIR, plot_dir_view+username+'outputclaimboxplot.png')):
            pdf = FPDF()
            pdf.add_page()
            # pdf = exportgraphImgPdf(pdf, os.path.join(
            #     BASE_DIR, plot_dir_view+username+'outputclaimboxplot.png'), " Box Plot "+var_num+" vs "+var_cat)
            pdf.output(os.path.join(
                BASE_DIR, plot_dir_view+username+'Box Plot.pdf'))

        pngDir = os.path.join(BASE_DIR, 'static\\media\\')
        savefile_name = pngDir + str(username+'outputclaimboxplot.png')
        print("savefile_name",savefile_name)
        file_stream = BytesIO()
        print("file_stream",file_stream)
        image_data = PIL.Image.open(savefile_name)
        print("image_data",image_data)
        image_data.save(file_stream,'png')
        # image_data.save(file_stream.png)
        print("image_data",image_data)
        print("image_data",type(image_data))
        file_stream.seek(0)
        base64_data = base64.b64encode(file_stream.getvalue()).decode('utf-8')
        json_data = dict()
        json_data['report'] = base64_data
        json_data.update({ 'msg':'','chartType': 'Box Plot', 'pdfFile': plot_dir+username+'Box Plot.pdf',
                   'ddlvar1': num_cols, 'ddlvar2': cat_cols, 'var1': var_num, 'var2': var_cat, 'hideddl2': ''})
        print("json data",json_data)
        return JsonResponse(json_data)

import plotly.graph_objs as go
from plotly.offline import plot
from flask import Markup

class box_plot3d(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request): 
        
        df=find_src_data(request.data['mdl_id'],request.data['dataset'])
       
        print("df",df)
        var_cat=request.data['var_cat']
        var_num=request.data['var_num']
        print("var_cat var_num",var_cat,var_num)

        cat_cols_temp = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] in [np.object]]

        cat_cols=[]
        for x in cat_cols_temp:
            if len(df[x].value_counts())<25:
                cat_cols.append(x)
        if(len(cat_cols)<1):
            return Response({'msg':'No cat var'},status.HTTP_200_OK)
        num_cols_temp = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] not in [np.object]] 

        num_cols=[]
        for x in num_cols_temp:
            if len(df[x].value_counts())<25:
                num_cols.append(x)
        # x_keep = pd.read_csv(savefile_x_keep)
        if(var_cat == False):
            var_num = num_cols[0]
            var_cat = cat_cols[0]

        trace = go.Box(
            x=df[var_cat],
            y=df[var_num],
            opacity=0.7,
            marker=dict(
                color='rgb(215, 195, 5, 0.5)'
            )
        )
        data_boxplot = [trace]
        layout = go.Layout(title=var_num)
        fig = go.Figure(data=data_boxplot, layout=layout)
        plot_div = plot(fig, include_plotlyjs=False, output_type='div')
        # fig.write_image(os.path.join(BASE_DIR, 'static\media\outputvehclm.png'))
        print("plot_div",plot_div)

        json_data = dict()
        json_data['report'] = Markup(plot_div)
        json_data.update({'msg':'','var1': var_num,'var2': var_cat, 'ddlvar1': num_cols, 'ddlvar2': cat_cols,
                           'displayddl3': 'none', 'hideUnvar': 'none','pageHeader': 'Box Plot 3D'})
        print("json data",json_data)
        return JsonResponse(json_data)

class scattred3d(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request): 
        
        df=find_src_data(request.data['mdl_id'],request.data['dataset'])
       
        print("df",df)
        var1=request.data['var1']
        var2=request.data['var2']
        var3=request.data['var3']

        num_cols = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] not in [np.object]]
        cat_cols = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] in [np.object]]
        if(len(cat_cols)<1):
            return Response({'msg':'No cat var'},status.HTTP_200_OK)
        # x_keep = pd.read_csv(savefile_x_keep)
        if(var1 == False):
            var_cat1 = cat_cols[0]
            var_num1 = num_cols[0]
            var_num2 = num_cols[1]
            var1 = var_num1
            var2 = var_num2
            var3 = var_cat1

        trace = go.Scatter3d(x=df[var1], y=df[var2], z=df[var3],
                             mode='markers',  marker=dict(size=10, color=df[var1]))

        data_3d = [trace]

        layout = go.Layout(
            title=' ',
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0
            ),
            scene=dict(
                xaxis=dict(title=var1),
                yaxis=dict(title=var2),
                zaxis=dict(title=var3)
            )
        )
        fig = go.Figure(data=data_3d, layout=layout)
        # plot_div = fig.to_html()
        plot_div = plot(fig, include_plotlyjs=False, output_type='div')
        # fig.write_image(os.path.join(
        #     BASE_DIR, plot_dir_view+user_name+'outputscattred3d.png'))
        print("plot_div",plot_div)
        json_data = dict()
        json_data['report'] = Markup(plot_div)
        json_data.update({'msg':'','var1': var1,'var2': var2, 'var3': var3, 'ddlvar1': num_cols, 'ddlvar2': num_cols, 'ddlvar3': cat_cols,
                      'hideUnvar': 'none', 'displayddl3': '','pageHeader': 'Scattered 3D'})
        print("json data",json_data)
        return JsonResponse(json_data)
    


def getEmails():
    user_obj=Users.objects.all().values()
    user_obj_list=list(user_obj)
        
    print("user_obj_list",user_obj_list)    
    return user_obj_list


class confirmSrc(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request): 
        df=find_src_data(request.data['mdl_id'],request.data['dataset'])
       
        print("df",df)

        result= df.columns.tolist()   
        print(result)
        cnfirm_obj = collection_confirm_data_source.find({'Mdl_Id':request.data['mdl_id']},{'_id':0})
        # dfresp =  pd.DataFrame(list(cnfirm_obj))
        resultresp=list()
        for i in cnfirm_obj:
            print("i",i)
            resultresp.append(i)

        print("resultresp",resultresp)
        print("result",result)

        data_dict=dict()
        data_dict['resultresp']=resultresp
        data_dict['result']=result
        data_dict['emailLst']=getEmails()
        print("data",data_dict)
        return Response(data_dict)


def find_max_ds_id(Mdl_Id=""):
    print("find_max_ds_id")
    cnfirm_obj = collection_confirm_data_source.find()
    df =  pd.DataFrame(list(cnfirm_obj))
    print("dataframe is ",df)
    if df.empty:
        print('DataFrame is empty!')
        ds_id=1
        return ds_id
    else:
        print("dataframe max is",df['ds_id'].max())    
        ds_id=int(df['ds_id'].max())+1
        return ds_id

def sendGMail(emailId, srcId):
    print("sendGMail",emailId,srcId)
    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        mail_content = """Hello,
        Please click link below to confirm the datasource.
        """+app_url+"""cnfrmSrc/?srcID=""" + str(srcId) + """
        Thank You
        """
        # The mail addresses and password
        sender_address = 'modvaladm@gmail.com'
        sender_pass = mail_pwd
        receiver_address = emailId
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        # The subject line
        message['Subject'] = 'Confirm datasource for model validation.'

        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))

        # Create SMTP session for sending the mail
        # use gmail with port
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()  # enable security
        # login with mail_id and password
        session.login(sender_address, sender_pass)
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
    except Exception as e:
        print(e)
        print("Error: unable to send email")


class send_mail_confirmSrc(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request): 
   
        json_dictionary=request.data['json_dictionary']
        emailId=request.data['emailId']
        request_id=request.data['mdl_id']

        for colval in json_dictionary:
            for attribute, value in colval.items():
                colName = value
                print('colName ', colName)

                ds_id=find_max_ds_id(request_id)
                print("ds_id",ds_id)
                cnfirm_obj={"ColName":colName,"EmailId":emailId,"DataSource":"-","DataQuality":"-","ReqRessepon":"-","Comment":"-",
                            "Mdl_Id":request_id,"ds_id":int(ds_id)}
                
                myquery = { "Mdl_Id": request_id ,'ColName':colName}
                mydoc = collection_confirm_data_source.find(myquery)
                if collection_confirm_data_source.find_one(myquery):
                    for i in mydoc:                
                        cnfirm_obj['ds_id']=i['ds_id']
                        #print("cnfirm_obj",cnfirm_obj)
                        newvalues = { "$set":cnfirm_obj }
                        collection_confirm_data_source.update_one(myquery, newvalues)
                        for i in collection_confirm_data_source.find():
                            print("updated")
                else:
                    print("New Entry")
                    cnfirm_obj['ds_id']=cnfirm_obj['ds_id'] 
                    collection_confirm_data_source.insert_one(cnfirm_obj)
                    sendGMail(emailId,ds_id)
        
        data = {'is_taken': True}
        return Response(data)



class conceptualsoundness(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request): 

        data = {}
        result=[]
        resultDocumentation = []
        resultConcSnd = []
        modelFileExists = False
        
        # df=find_src_data(request.data['mdl_id'],request.data['dataset'])
       
         
        objvalidation=Validation()
        resultpROCESS =[]# df.to_json(orient="records")
        # resultpROCESS = json.loads(resultpROCESS)
        resultDocumentation = objvalidation.getModelDocs(request.data['mdl_id'])  
        data = {
            'selectedMdl':request.data['mdl_id'],
            'imgFiles': result,
            'pdfFile': "/static/media/ValidationReport.pdf",
            'modelDocs': resultDocumentation,
            'modelUsage': modelFileExists,
            'modelUsageFile': '',
            'df': resultpROCESS,
            'resultConcSnd': resultConcSnd,
            'occpae42' : "/static/reportTemplates/pub-ch-model-risk.pdf#page=42&zoom=100,0,400",
            'showQtnsIcon':'Yes'
        }

        return Response(data)


def find_max_cs_id():
    print("find_max_cs_id")
    cs_obj = collection_conceptual_soundness.find()
    df =  pd.DataFrame(list(cs_obj))
    print("dataframe is ",df)
    if df.empty:
        print('DataFrame is empty!')
        cs_id=0
        return cs_id
    else:
        print("dataframe max is",df['cs_id'].max())    
        cs_id=df['cs_id'].max()
        return cs_id


class save_CS_Data(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request): 
        try:
            request_id=request.data['mdl_id']
            comment=request.data['comment']
            title=request.data['title']
            titleIdx=request.data['titleIdx']
            reqId=request.data['reqId']

            cs_id=find_max_cs_id()
            print("cs_id",cs_id)
            
            cs_obj={'Title':title,'TitleIdx':int(titleIdx),'Comment':comment,'Img':'','ImgWidth':'','ImgHeight':'',
                            'ImgAlign':'','ImgTitle':'','TitleAlign':'','Mdl_Id':request_id,'cs_id':int(cs_id)}
            myquery = { "Mdl_Id": request_id ,'Title':title}
            mydoc = collection_conceptual_soundness.find(myquery)
            if collection_conceptual_soundness.find_one(myquery):
                for i in mydoc:
                    print("I",i['Mdl_Id'])
                    print("cs_id",i['cs_id'])
                    cs_obj['cs_id']=i['cs_id']
                    #print("cs_obj",cs_obj)
                    newvalues = { "$set":cs_obj }
                    collection_conceptual_soundness.update_one(myquery, newvalues)
                    for i in collection_conceptual_soundness.find():
                        print("updated")
            else:
                print("New Entry")
                cs_obj['cs_id']=cs_obj['cs_id'] + 1
                collection_conceptual_soundness.insert_one(cs_obj)
            
            data = {
                'is_taken': True,
                'reqId': str(reqId),
                'titleIdx': int(titleIdx)-1,
            }
            
            return Response(data)
        except Exception as e:
            print(e)
            print('stacktrace is ',traceback.print_exc())



class imp_ctrl(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request): 
    
        arrSection = ['Conform to Enterprise Production Policy', 
                        'Parallel Runs', 
                        'User Acceptance Testing',
                        'Integration within Production Systems',
                        'Model Approval Process',
                        'Contingency plans (Backup -on-site and off-site)',                       
                        'Change Controls',
                        'IT Security (Confirm)']
        enableReportBtn = "True"
        sectionType = []
        impCtrl_obj = collection_model_implementation_control.find({'Mdl_Id':request.data['mdl_id']})
        df =  pd.DataFrame(list(impCtrl_obj))
        print("dataframe is ",df)
        print("df len",len(df))
        if len(df) >1:
            dfcnt = df.loc[df['Response'] != '-']
            if len(dfcnt) == 8:
                enableReportBtn = "True"
            for isec in range(len(arrSection)):
                if (dfcnt["Section"] == arrSection[isec]).any():
                    sectionType.append(
                        {'secName': arrSection[isec], 'bgColor': 'green', 'color': 'white'})
                else:
                    sectionType.append(
                        {'secName': arrSection[isec], 'bgColor': 'white', 'color': 'black'})
        else:
            for isec in range(len(arrSection)):
                sectionType.append(
                    {'secName': arrSection[isec], 'bgColor': 'white', 'color': 'black'})
        
        objvalidation=Validation()
        req_id=request.data['mdl_id']
        print("req id",req_id)
        resultDocumentation = objvalidation.getModelDocs(req_id)
        data={'section': '',
            'validatorComment': '',
            'reqRessepon': '-',
            'recpComment': '',
            'enableReportBtn': enableReportBtn,
            'arrSection': sectionType,
            'emailLst': getEmails(),
            'modelDocs': resultDocumentation,
            "req_id":req_id,
            'selectedMdl':req_id,
            }

        return Response(data)


def find_max_impCtrl_id():
    print("find_max_impCtrl_id")
    impCtrl_obj = collection_model_implementation_control.find()
    df =  pd.DataFrame(list(impCtrl_obj))
    print("dataframe is ",df)
    if df.empty:
        print('DataFrame is empty!')
        impCtrl_id=0
        return impCtrl_id
    else:
        print("dataframe max is",df['impCtrl_id'].max())    
        impCtrl_id=df['impCtrl_id'].max()
        return impCtrl_id



def sendImpCtrlMail(emailId, impCtrl_id, comments, subjectline):
    print("EmailId",emailId)
    print("impCtrl_id",impCtrl_id)
    print("comments",comments)
    print("subjectline",subjectline)
    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        mail_content = """Hello,\n
        Please click link below to reply.
        """+app_url+"""cnfrmImpCtrlResp/?srcID=""" + str(impCtrl_id) + """
        Thank You
        """
        # The mail addresses and password
        sender_address = 'modvaladm@gmail.com'
        sender_pass = mail_pwd
        receiver_address = emailId
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        # The subject line
        message['Subject'] = subjectline

        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))

        # Create SMTP session for sending the mail
        # use gmail with port
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()  # enable security
        # login with mail_id and password
        session.login(sender_address, sender_pass)
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
    except Exception as e:
        print(e)
        print("Error: unable to send email")
  

class send_ImpCtrlCnfrm_Mail(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request): 
   
        request_id=request.data['mdl_id']
        emailId=request.data['emailId']
        validatorComment=request.data['validatorComment']
        section=request.data['section']

        impCtrl_id=find_max_impCtrl_id()
        print("impCtrl_id",impCtrl_id)
        
        impctrl_obj={"Mdl_Id":request_id,"ValidatorComment":validatorComment,"Section":section,"EmailId":emailId,"impCtrl_id":int(impCtrl_id),'Response':"","ResponseCheck":""}
        myquery={'impCtrl_id':int(impCtrl_id)}
        if collection_model_implementation_control.find_one(myquery):
            print("if true")
            myquery = { "Mdl_Id":request_id,'Section':section}
            mydoc = collection_model_implementation_control.find(myquery)
            if collection_model_implementation_control.find_one(myquery):
                for i in mydoc:
                    print("I",i['impCtrl_id'])
                    impctrl_obj['impCtrl_id']=i['impCtrl_id']
                    newvalues = { "$set":impctrl_obj }
                    collection_model_implementation_control.update_one(myquery, newvalues)
                    sendImpCtrlMail(emailId, impctrl_obj['impCtrl_id'], validatorComment, section + " - Model")
                    for i in collection_model_implementation_control.find():
                        print("updated",i)
            else:
                print("New Entry")
                impctrl_obj['impCtrl_id']=impctrl_obj['impCtrl_id'] + 1
                collection_model_implementation_control.insert_one(impctrl_obj)
                sendImpCtrlMail(emailId, impctrl_obj['impCtrl_id'], validatorComment, section + " - Model")
        else:
            print("first enrty")
            impctrl_obj['impCtrl_id']=impctrl_obj['impCtrl_id'] + 1
            collection_model_implementation_control.insert_one(impctrl_obj)
            sendImpCtrlMail(emailId, impctrl_obj['impCtrl_id'], validatorComment, section + " - Model")
        
        data = {
            'is_taken': True
        }

        return Response(data)
   

class get_Section_Resp(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request): 
   
        request_id=request.data['mdl_id']
        section=request.data['section']

        impCtrl_obj = collection_model_implementation_control.find({'Section': (section),'Mdl_Id':request_id},{'_id':0})
        data= {'Section': '',
                    'ValidatorComment': '',
                    'ResponseCheck': '-',
                    'Response': '',
                    'EmailId': ''
                    }  
        if impCtrl_obj:
            for i in impCtrl_obj:
                print("i",i)
                data = i
        else:
            data = {'Section': '',
                    'ValidatorComment': '',
                    'ResponseCheck': '-',
                    'Response': '',
                    'EmailId': ''
                    }      

        return Response(data)
 

class update_ImpCtrl_ReportComment(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request): 
   
        request_id=request.data['mdl_id']
        reportComment=request.data['reportComment']

        impCtrl_obj=collection_model_implementation_control.find({'Mdl_Id':request_id})
        df=pd.DataFrame(list(impCtrl_obj))
        print(df)
        impCtrl_id=df['impCtrl_id'].min()
        print("impCtrl_id",impCtrl_id)

        impctrl_comment_obj={'ReportComments':reportComment}
        myquery = { "impCtrl_id": int(impCtrl_id)}
        mydoc = collection_model_implementation_control.find(myquery)

        if collection_model_implementation_control.find_one(myquery):
            for i in mydoc:
                newvalues = { "$set":impctrl_comment_obj }
                collection_model_implementation_control.update_one(myquery, newvalues)
                for i in collection_model_implementation_control.find():
                    print("updated",i)

        data = {
        'is_taken': True
        }
        return Response(data)
  

class modelUsage(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request): 
        catLst = ['Business Requirement', 'Explanation of Model Output', 'Business Requirement Met', 'Model Performance Monitoring ',
                  'Model Maintenance (Frequency of Failure, Run-time etc)', 'Model Dependencies', 'Violations of Model Assumptions']
        
        data = {'emailLst': getEmails(), 'catLst': catLst}

        return Response(data)


def find_max_usage_id():
    print("find_max_usage_id")
    usage_obj = collection_model_usage.find()
    df =  pd.DataFrame(list(usage_obj))
    print("dataframe is ",df)
    if df.empty:
        print('DataFrame is empty!')
        usage_id=0
        return usage_id
    else:
        print("dataframe max is",df['usage_id'].max())    
        usage_id=df['usage_id'].max()
        return usage_id
    

def sendModelUsage(emailId,mdlid):
    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        mail_content = """Hello,
        Please click link below to responde the model usage.
        """+app_url + """modelUsageResp?id="""+mdlid +""""
        Thank You
        """
        # The mail addresses and password
        sender_address = 'modvaladm@gmail.com'
        sender_pass = mail_pwd
        receiver_address = emailId
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        # The subject line
        message['Subject'] = 'Model usage.'

        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))

        # Create SMTP session for sending the mail
        # use gmail with port
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()  # enable security
        # login with mail_id and password
        session.login(sender_address, sender_pass)
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
        data = {'is_taken': True}
    except Exception as e:
        print(e)
        print("Error: unable to send email")
        data = {'is_taken': False}
    return JsonResponse(data)


class save_model_usage(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request): 
   
        req_id=request.data['mdl_id']
        email=request.data['email']
        json_dictionary =request.data['categories']
        comment=request.data['comment']

        for colval in json_dictionary:
            for attribute, value in colval.items():
                colName = value
                print('colName ', colName)

        #collection_model_usage
                usage_id=find_max_usage_id()
                print("usage_id",usage_id)
                model_usage_obj={'Email':email,'Category':colName,'Comment':comment,'Mdl_Id':(req_id),'usage_id':int(usage_id),'Response':""}
                myquery = { "Mdl_Id": (req_id) ,'Category':colName}
                mydoc = collection_model_usage.find(myquery)
                if collection_model_usage.find_one(myquery):
                    for i in mydoc:
                        print("I",i['Mdl_Id'])
                        print("usage id",i['usage_id'])
                        model_usage_obj['usage_id']=i['usage_id']
                        #print("model_usage_obj",model_usage_obj)
                        newvalues = { "$set":model_usage_obj }
                        collection_model_usage.update_one(myquery, newvalues)
                        for i in collection_model_usage.find():
                            print("updated",i)
                else:
                    print("New Entry")
                    model_usage_obj['usage_id']=model_usage_obj['usage_id'] + 1
                    collection_model_usage.insert_one(model_usage_obj) 
        sendModelUsage(email,req_id)
        data = {
            'is_taken': True,
                }
        return Response(data)

class valFindings(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request): 
        
        today = date.today().strftime("%m/%d/%Y")  

        data = {'List': [], 'today': today, 'emailLst': getEmails(),'ValCatLst':get_Findings_Category(),'ValCatElm':get_Finding_val_elements()}

        return Response(data)


class save_valFindings(APIView):
    def __init__(self):
        self.objdbops=dbops()  
    permission_classes = [IsAuthenticated]
    def post(self,request):  
        request_id=request.data['request_id']
        validation_element=request.data['validation_element']
        validation_element_text=request.data['validation_element_text']
        sub_validation_element=request.data['sub_validation_element']
        ValCat=request.data['ValCat'] 
        Risk =request.data['Risk']
        Level=request.data['Level']
        Desc=request.data['Desc']
        Added_by=request.data['Added_by'] 
        added_on=datetime.now()
        letters="" 
        words = validation_element_text.split() 
        if(len(words)>1):
            for i in range(len(words)):
                if str(words[i][0]).isupper():
                    letters = letters + words[i][0]
        else:
            print('else')
            letters = validation_element_text[:2]

        # finding_element=letters[0] + letters[-1]
        print('letters is ',letters)

        findings_list=list()
        findings_id=""
        val_find_obj=ValidationFindings.objects.filter(mdl_id=request_id , validation_element=validation_element)
        print("len ",len(val_find_obj),val_find_obj)         
        findings_id=letters+ str(len(val_find_obj)+1)
        print("findings_id",findings_id)

        sql="select count(*) from validation_findings where Mdl_Id='"+request_id+"' and Validation_element="+str(validation_element)+" and Validation_Sub_element="+str(sub_validation_element)+" and category="+str(ValCat)
       
        if str(self.objdbops.getscalar(sql))=="0":    
            new_object = ValidationFindings.objects.create(mdl_id=request_id,validation_element=validation_element,
                                                        sub_validation_element=sub_validation_element,category=ValCat,risk=Risk,
                                                        risk_level=Level,finding_description=Desc,added_by=Added_by,added_on=added_on,
                                                        findings_id=findings_id)
        else:
            sql="update validation_findings set Finding_Description='"+str(Desc)+"',Updated_by="+str(Added_by)+",Updated_on=getdate() "
            sql+=" where Mdl_Id='"+request_id+"' and Validation_element="+str(validation_element)+" and Category="+str(ValCat)+"  and Validation_Sub_element="+str(sub_validation_element)
            self.objdbops.insertRow(sql) 
        insertValidationRating(request_id)
        
        data = {
                'is_taken': True,
                'findingsId': str(findings_id)
            }
        return Response(data)



class get_val_findings(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request): 
   
        findingsId=request.data['findingsId']
        validation_obj=collection_validation_findings.find({'FindingsId':findingsId},{'_id':0})
        df =  pd.DataFrame(validation_obj)
        print("df is",df)
        result=df.to_dict(orient="records")
        print("result",result)
        #result=json.loads(result)
        data={'findingData':result}

        return Response(data)


class send_Mail_valFindings(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request): 
        try:
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText

            request_id=request.data['request_id']
            emailId=request.data['emailId']

            
            objdbops=dbops() 
            sql="select count(*) from validation_findings where Mdl_Id='"+request_id+"'"
            df_old=  objdbops.getscalar(sql)
            objdbops=None 
            if str(df_old)=="0" and emailId != "False": 
                if ((df_old["EmailId"] == emailId)).any():
                    print('emailsent')
                    data = {'is_taken': True}
                else:
                    # # df_old.at[0, "EmailId"] = emailId
                    # validation_obj_update=collection_validation_findings.find({'Mdl_Id':request_id})
                    # if collection_validation_findings.find_one({'Mdl_Id':request_id}):
                    #     print("Update")      
                    #     for i in validation_obj_update:
                    #         newvalues = { "$set":{"EmailId":emailId} } 
                    #         collection_validation_findings.update_one({'Mdl_Id':request_id},newvalues)
                    mail_content = """Hello,
                    Please click link below to responde the model validation findings.
                    """+app_url + """valFindingsResp?id="""+ request_id +"""
                    Thank You
                    """
                    # The mail addresses and password
                    sender_address = 'modvaladm@gmail.com'
                    sender_pass = mail_pwd
                    receiver_address = emailId
                    # Setup the MIME
                    message = MIMEMultipart()
                    message['From'] = sender_address
                    message['To'] = receiver_address
                    # The subject line
                    message['Subject'] = 'Model validation findings.'

                    # The body and the attachments for the mail
                    message.attach(MIMEText(mail_content, 'plain'))

                    # Create SMTP session for sending the mail
                    # use gmail with port
                    session = smtplib.SMTP('smtp.gmail.com', 587)
                    session.starttls()  # enable security
                    # login with mail_id and password
                    session.login(sender_address, sender_pass)
                    text = message.as_string()
                    session.sendmail(sender_address, receiver_address, text)
                    session.quit()
                    print('Mail Sent',emailId)
                    data = {'is_taken': True}

                    return Response(data)
            else:
                data = {'is_taken': True}#added on 31.05.2024
        except Exception as e:
            print(e)
            print("Error: unable to send email")
            data = {'is_taken': False}
        return JsonResponse(data)      

class getvalFindings(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request):  
        request_id=request.data['request_id']
        Assessment=request.data['Assessment']
        ValCat=request.data['ValCat']

        objdbops=dbops() 
        sql="select * from validation_findings where Mdl_Id='"+request_id+"' and Validation_element="+Assessment+" and Category="+ValCat+""
        tableResult=  objdbops.getTable(sql)  
        objdbops=None
        mdldata= tableResult.to_json(orient='index')
        del tableResult
        return Response({'findingData':json.loads(mdldata)})


class valFindingsResp(APIView):
    
    # permission_classes = [IsAuthenticated]
    def post(self,request):  
        request_id=request.data['request_id']
        today = date.today().strftime("%m/%d/%Y")    
        data = {'today': today, 'ValCatLst':get_Findings_Category(),'ValCatElm':get_Finding_val_elements()}
        #print('ValCatLst : ',get_Findings_Category())
        return Response(data)
         
        
class save_valFindingsResp(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request): 
   
        request_id=request.data['request_id']
        Resp=request.data['Resp']        
        Assessment=request.data['Assessment']
        ValCat=request.data['ValCat']      
        Added_by=request.data['Added_by']   
        
        objdbops=dbops()         
        sql="update validation_findings set Response='"+str(Resp)+"',Updated_by="+str(Added_by)+",Updated_on=getdate() "
        sql+=" where Mdl_Id='"+request_id+"' and Validation_element="+str(Assessment)+" and Category="+str(ValCat)+""
        objdbops.insertRow(sql) 
        print('sql update : ',sql)
        objdbops=None

        data = {
                'is_taken': True,
                'findingsId': str(request_id)
            }
        return Response(data)


class get_ReportTtlData(APIView): 
    def __init__(self):
        self.objdbops=dbops()
    permission_classes=[IsAuthenticated]
    def post(self,request):
        strQ = "select * from Report_Header_Title_Content where template_name='"+request.data['template_name']+"' and mdl_id='"+request.data['mdl_id']+"'"        
        tableResult=  self.objdbops.getTable(strQ)  
        commenthistory= tableResult.to_json(orient='index')         
        return Response(json.loads(commenthistory))



def get_Findings_Category():   
    print('ValCatLst')
    objdbops=dbops() 
    strQ = "select Category_AID,Category_text from Findings_Category where ActiveStatus=1 order by Category_text"       
    Findings_Category_list=  objdbops.getTable(strQ)  
    Findings_Category_list=Findings_Category_list.to_json(orient='index')
    objdbops=None
    return json.loads(Findings_Category_list)


def get_Finding_val_elements():
    objdbops=dbops() 
    strQ = "select Element_AID,Element_text from Finding_val_elements where ActiveStatus=1 order by Element_text"       
    Finding_val_elements_list=  objdbops.getTable(strQ)  
    Finding_val_elements_list=Finding_val_elements_list.to_json(orient='index')
    objdbops=None
    return json.loads(Finding_val_elements_list)

        

def insertValidationRating(mdl_id):
    strQ="SELECT validation_rating,     STRING_AGG(CONCAT(case Severity when 'Low' then 'lowcnt' when 'Medium' then 'medcnt'\
        when 'High' then 'highcnt' end ,' ',operator,' ',value),' and ') condn\
        from   Validation_Rating_Master where operator is not null and value is not null \
        group by validation_rating order by 1"
    objdbops=dbops() 
    df=objdbops.getTable(strQ)
    strfail=df.values[0][1]
    strneedsimprovement=df.values[1][1]
    strsatisfactory=df.values[2][1]
    strQ="select highcnt,medcnt,lowcnt,\
    case when  "+ strfail +"  then 'Fail' else\
    case when "+ strneedsimprovement+" then 'Needs Improvement' else \
    case when "+strsatisfactory+" then 'Satisfactory' else '-' end\
    end  end   rating\
    from \
    (select case when exists(select count(*) lowcnt \
    from validation_findings where mdl_id='"+  mdl_id +"' and  risk=1 \
    group by mdl_id,Risk \
    ) then (select count(*) lowcnt \
    from validation_findings where mdl_id='"+  mdl_id +"' and  risk=1 group by mdl_id,Risk \
    )  else 0 end lowcnt) lowrating, \
    (select case when exists(select count(*) lowcnt \
    from validation_findings where mdl_id='"+  mdl_id +"'  and  risk=2 \
    group by mdl_id,Risk \
    ) then (select count(*) lowcnt \
    from validation_findings where mdl_id='"+  mdl_id +"'  and  risk=2 group by mdl_id,Risk \
    )  else 0 end medcnt) mediumrating  ,\
    (select case when exists(select count(*) lowcnt \
    from validation_findings where mdl_id='"+  mdl_id +"' and  risk=3 \
    group by mdl_id,Risk \
    ) then (select count(*) lowcnt \
    from validation_findings where mdl_id='"+  mdl_id +"'  and  risk=3 group by mdl_id,Risk \
    )  else 0  end highcnt) highrating   "
   
    df=objdbops.getTable(strQ) 
    print(mdl_id,' ratings is ',df.values[0][3])
    strQ="update Mdl_OverView set Validation_Rating='"+df.values[0][3]+"' where mdl_id='" + mdl_id + "' "
    objdbops.insertRow(strQ)

###---------------------------Ashok code rmse-----------------------------------###

class IssuePriorityMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            print("id",id)
            issuepriority = IssuePriorityMaster.objects.get(issue_priority_aid=id)
            serializer = IssuePriorityMasterSerializer(issuepriority)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        issueprioritymaster = IssuePriorityMaster.objects.all()
        serializer =  IssuePriorityMasterSerializer(issueprioritymaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = IssuePriorityMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Issue Priority created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
    

    permission_classes=[IsAuthenticated]
    def put(self,request):
        print("data",request.data)
        try:
            id=request.data['id']
            print("id",id)
            obj = IssuePriorityMaster.objects.get(issue_priority_aid=id)
        except IssuePriorityMaster.DoesNotExist:
            return Response({'msg':'Issue Priority does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = IssuePriorityMasterSerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Issue Priority Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class IssueFunctionMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            print("id",id)
            issuefunctionmaster = IssueFunctionMaster.objects.get(issue_function_aid=id)
            serializer = IssueFunctionMasterSerializer(issuefunctionmaster)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        issuefunctionmaster = IssueFunctionMaster.objects.all()
        serializer =  IssueFunctionMasterSerializer(issuefunctionmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = IssueFunctionMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'IssueFunctionMaster created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)


    permission_classes=[IsAuthenticated]
    def put(self,request):
        print("data",request.data)
        try:
            id=request.data['id']
            print("id",id)
            obj = IssueFunctionMaster.objects.get(issue_function_aid=id)
        except IssueFunctionMaster.DoesNotExist:
            return Response({'msg':'IssueFunctionMaster does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = IssueFunctionMasterSerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Issue Function Master Updated Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
    

class IssueApprovalstatusMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            print("id",id)
            issueapproval = IssueApprovalstatusMaster.objects.get(issue_approvalstatus_aid=id)
            serializer = IssueApprovalstatusMasterSerializer(issueapproval)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        issueapprovalstatusmaster = IssueApprovalstatusMaster.objects.all()
        serializer =  IssueApprovalstatusMasterSerializer(issueapprovalstatusmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = IssueApprovalstatusMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Issue Approval status created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)

    permission_classes=[IsAuthenticated]
    def put(self,request):
        print("data",request.data)
        try:
            id=request.data['id']
            print("id",id)
            obj = IssueApprovalstatusMaster.objects.get(issue_approvalstatus_aid=id)
        except IssueApprovalstatusMaster.DoesNotExist:
            return Response({'msg':'Issue Approval does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = IssueApprovalstatusMasterSerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Issue Approval Status Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST) 


class getIssues(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            print("rmse_calendar_issue")
            all_data_lst=list()
            dict_data=dict() 
            alltasks,issuecnt=objreg.getIssueListByUserId(request.data['uid'],request.data['mdl_id']) 
            for irow  in alltasks:       
                dict_data['start']= alltasks[irow]["end_date_cal"]
                dict_data['title']= alltasks[irow]["Issue_ID"]      
                if alltasks[irow]["css"]=='redEvent':                     
                    dict_data['description']=alltasks[irow]['Issue_ID'] + " "+str(alltasks[irow]["datedif"])+" days overdue."                         
                else: 
                    dict_data['description']=alltasks[irow]['Issue_ID'] + " "+str(alltasks[irow]["datedif"])+" days to end."
                dict_data['textColor']='white'
                dict_data['backgroundColor']= alltasks[irow]["css"] 
                dict_data['color']='white'
                all_data_lst.append(dict_data.copy())  
            context={'all_data_lst':json.dumps(all_data_lst),'mdldata':alltasks}  
            return Response( context, status=status.HTTP_200_OK)
        except Exception as e: 
            print('error ',traceback.print_exc())
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)


class getVRSubmResp(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:      
            enddate=''  
            mdl_id = request.data['mdl_id']
            if VrSubmissionAllocation.objects.filter(mdl_id=mdl_id):                 
                vrsuballoc = VrSubmissionAllocation.objects.filter(mdl_id=mdl_id) 
                enddate=vrsuballoc.aggregate(Max('enddate'))['enddate__max']               
                enddate=enddate.strftime('%m/%d/%Y')
            return Response({"Qtns":objrmse.getVRSubResp(mdl_id,str(request.data['uid'])),'enddate':enddate}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class insertVRSubResp(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:        
            mdl_id = request.data['mdl_id'] 
            comments = request.data['comments']
            isupdate = request.data['isupdate']
            Response_id = request.data['Response_id']
            objrmse.insertVRSubResp(mdl_id,str(request.data['uid']),comments,isupdate,Response_id)
            objmaster.saveActivity(mdl_id,38,'',str(request.data['uid'])) 
            return Response({"is_taken":True}, status=status.HTTP_200_OK)
        
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class getVRSubRespById(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:               
            Response_id = request.data['Response_id']        
            return Response({"is_taken":True,'comment':objrmse.getVRSubRespById(Response_id)}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)
        
class getVRSubRespByUid(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:               
            uid = request.data['uid']       
            respid = request.data['respid'] 
            mdl_id = request.data['mdl_id']  
            return Response({"is_taken":True,'comment':objrmse.getVRSubRespByUid(mdl_id,uid,respid)}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)
        
class getVRSubmCommentsCnt(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:               
            mdl_id = request.data['mdl_id']       
            return Response({"is_taken":True,'comment':objrmse.getVRSubmCommentsCnt(mdl_id)}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            print(e,traceback.print_exc())
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)


class GetMdlForClosure(APIView):
    def get(self,request): 
        try:  
            lst_mdl=[]      
            strQ=" select distinct refference_id from [Activity_Trail] where Activity_Trigger='Model Validation Report Submitted.'"   
            tableResult =objdbops.getTable(strQ) 
            actdata= tableResult.to_json(orient='records')
            del tableResult     
            return Response({"status": "success", "data": json.loads(actdata) }, status=status.HTTP_200_OK)
        except Exception as e:
            print('error ',e)
            return Response({"status": "success", "data": []}, status=status.HTTP_200_OK)


class InsertVRPublishingInfo(APIView):
    def post(self,request):
        try:
            mdl_id=request.data['mdl_id']
            uid=request.data['uid']
            objreg.insertVRPublishingInfo(mdl_id,uid)
            objmaster.saveActivity(mdl_id,'39','',uid)
            return Response({'msg':'Report published successfully.'},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class getMdlForVRSubmisionAllocation(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            uid=request.data['uid']
            is_mrm=request.data['is_mrm']
            return Response({"status":"success","mdl_id":objrmse.getMdlForVRSubmisionAllocation(uid,is_mrm)},status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
        
class GetMdlForPublish(APIView):
    def get(self,request): 
        try:     
            print('inside publish')
            lst_mdl=[]      
            strQ=" SELECT distinct Mdl_Id refference_id FROM  VR_Submission_Allocation  where enddate<getdate()  except  select  distinct Mdl_Id from VR_Publish_Info"   
            tableResult =objdbops.getTable(strQ) 
            actdata= tableResult.to_json(orient='records')
            del tableResult         
            return Response({"status": "success", "data": json.loads(actdata) }, status=status.HTTP_200_OK)
        except Exception as e:
            print('error ',e)
            return Response({"status": "success", "data": []}, status=status.HTTP_200_OK)


class getMdlQtnsBySec(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:     
            mdl_id = request.data['mdl_id']
            section =request.data['section']             
            return Response({"Qtns":objrmse.getMdlQtnsBySec(mdl_id,section),"end_date":objrmse.getmaxEndDate(mdl_id,section),"section_id":objrmse.getSecIDFromSectionText(mdl_id,section)}, status=status.HTTP_200_OK)
        except Exception as e: 
                error_saving(request,e)
                return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

        
class addUserQues_question(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:            
            added_by=request.data['uid']
            adddate=datetime.now()
            section=request.data['section']
            sub_section=""#request.data['sub_section']
            sub_sub_section=""#request.data['sub_sub_section']
            sub_sub_sub_section=""#request.data['sub_sub_sub_section']
            question=request.data['question'] 
            if sub_section == '':
                sub_section=None
            if sub_sub_section == '':
                sub_sub_section =None
            if sub_sub_sub_section == '':
                sub_sub_sub_section =None      
            question_obj=UserQuesQuestionMaster.objects.create(question_label=question,section_aid=section,sub_section_aid=sub_section,
                                                        sub_sub_section_aid=sub_sub_section,sub_sub_sub_section_aid=sub_sub_sub_section,
                                                        addedby=added_by,adddate=adddate)
            print("saved")
            return Response({'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST) 

class discardUpdate(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            mdlid = request.data.get("mdlId",'False')
            objreg.deleteupdateData(mdlid)
            # objmaster.saveActivity(mdlid,'41','Model changes discarded for model '+mdlid,request.data['uid']) 
            return Response({'istaken':'true'},status=status.HTTP_200_OK)
        except Exception as e:
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)



class Save_Buss_KPI_Monitoring_Result(APIView):
    permission_classes=[IsAuthenticated]  
    def post(self,request):    
        try:
            strQ="delete from Buss_KPI_Monitoring_Result where Mdl_ID='"+str(request.data['Mdl_ID'])+"'  and Metric="+ str(request.data['Metric']) + " and freq_idx="+str(request.data['freq_idx'])
            objdbops.insertRow(strQ) 

            strQ="INSERT INTO Buss_KPI_Monitoring_Result(Mdl_ID,Metric,Prdn_Value,Metric_flag,Added_by,Added_On,freq_idx,freq_val)  VALUES ("
            strQ +="'"+str(request.data['Mdl_ID'])+"',"+request.data['Metric']+",'"+str(request.data['Prdn_Value'])+"','"+str(request.data['Metric_flag'])+"','"+str(request.data['addedby'])+"',getdate(),"+str(request.data['freq_idx']) +", getdate())"
            #print("strQ Insert ",strQ)
            objdbops.insertRow(strQ)
            return Response({'data':"",'msg':'Model Matrics Updated Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            print("error ",e, traceback.print_exc())
            return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)


class Save_Performance_Monitoring_Resolution(APIView):
    permission_classes=[IsAuthenticated]  
    def post(self,request):    
        try:  
            strQ="INSERT INTO Performance_Monitoring_Resolution(Mdl_ID,Resolution,Added_by,Added_On)  VALUES ("
            strQ +="'"+str(request.data['Mdl_ID'])+"','"+request.data['Resolution']+"','"+str(request.data['Added_by'])+"',getdate())"
            print("strQ Insert Performance_Monitoring_Resolution ",strQ)
            objdbops.insertRow(strQ)

            return Response({'data':"",'msg':'Model Matrics Updated Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            print("error ",e, traceback.print_exc())
            return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)


class Update_Performance_Monitoring_Override_History(APIView):     
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            maxaid=objdbops.getscalar("select max(aid)   from Performance_Monitoring_Override_History where Mdl_ID='"+str(request.data['Mdl_ID']) +"'  and Metric="+ str(request.data['Metric']) + " and freq_idx="+str(request.data['freq_idx']))
            strQ="update Performance_Monitoring_Override_History set MO_Approval=1, MO_Approved_On=getdate() where aid="+ str(maxaid) +" and Mdl_ID='"+str(request.data['Mdl_ID']) +"'  and Metric="+ str(request.data['Metric']) + " and freq_idx="+str(request.data['freq_idx'])
            objdbops.insertRow(strQ) 
            return Response({'data':"",'msg':'Model Matrics Updated Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)


class getMdlIdforPerfMontr(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None): 
        if id:
            usr = ModelOverview.objects.get(u_aid=id)
            serializer = ModelOverviewSerializer(usr)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        modeldata = PerformanceMonitoringSetup.objects.order_by().values('mdl_id').distinct() 
        serializer = PerformanceMonitoringSetupSerializer(modeldata,many=True)
        
        freqmaster = FrequencyMaster.objects.all()
        freqerializer =  FrequencyMasterSerializer(freqmaster,many=True)

        matricsdeptdata = ModelMetricDept.objects.filter(dept_aid=request.data['dept_aid'])
        serializer_a =  ModelMetricDeptSerializer(matricsdeptdata,many=True)

        businessdata = BussKpiMonitoringSetup.objects.order_by().values('mdl_id').distinct() 
        serializer_b = BussKpiMonitoringSetupSerializer(businessdata,many=True)
        
        return Response({'mdlids':serializer.data, 'frequency':freqerializer.data,'mdlmetric':serializer_a.data,'bussmetric':serializer_b.data}, status=status.HTTP_200_OK)



class getIssuesByQtrOrMonth(APIView): 
    permission_classes=[IsAuthenticated] 
    def post(self,request):
        try: 
            objreg=Register()  
            issuesByQtrOrMonth=objreg.getIssuesByMonthOrQtr(request.data['ptype'],request.data['uid'],request.data['is_mrm'],request.data['issue_from_dt'],request.data['issue_to_dt'],request.data['issue_sts'])
            return JsonResponse({'issuesByQtrOrMonth':issuesByQtrOrMonth})
        except Exception as e:
            print('setuppycaret is ',e)
            print('setuppycaret traceback is ', traceback.print_exc())

class modelsByValPriority(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            ty =request.data['filterType']
            colnm =request.data['filterValue']#request.GET.get('colnm', 'False') 
            chartnm =request.data['filterColumn']#request.GET.get('chartnm', 'False') 
            valPriority =request.data['valPriority']
            element_txt =request.data['element_txt']
            category_txt =request.data['category_txt']

            canAdd="1" 
            # Authorization(request.data['ucaid'],'Model Inventory') 
            modelinfo=objreg.getModelInfoByValFindingsPriority(request.data['uid'],ty,chartnm,colnm,'0',valPriority,element_txt,category_txt)
            is_MrmHead=str(objmaster.checkMRMHead(str(request.data['uid'])))            
            return Response( {'modelinfo':modelinfo,'canAdd':canAdd, 'is_MrmHead':is_MrmHead},status=status.HTTP_200_OK)          
                
        except Exception as e:
           error_saving(request,e)
           return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)



class get_sub_valID(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        print("request_data------------------",request.data)

        result_dict = {}
        sub_val_obj=FindingValSubElements.objects.filter(element_aid=request.data['val_id'])
        for i in sub_val_obj:
            print("sub id",i.element_sub_aid)
            result_dict[i.element_sub_aid] = i.element_text

        print("result_dict",result_dict)

        return Response(result_dict, status=status.HTTP_200_OK)


class getfindings_ID(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        print("request_data------------------",request.data)
        findings_id_lst=list()

        find_valobj = ValidationFindings.objects.filter(mdl_id = request.data['mdlid'])

        for i in find_valobj:
            if i:
                print("findings id",i.findings_id)
                findings_id_lst.append(i.findings_id)

        print("lst",findings_id_lst)

        return Response(findings_id_lst, status=status.HTTP_200_OK)


class getfindings_Data(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        print("request_data------------------",request.data)       

        find_valobj = ValidationFindings.objects.get(mdl_id = request.data['mdlid'],findings_id= request.data['find_id'])

        print("desc",find_valobj.finding_description)  
        validation_element=list()      
        validation_category=list()
        val_find_obj=ValidationFindings.objects.filter(mdl_id= request.data['mdlid'],findings_id= request.data['find_id'])
        for i in val_find_obj:
            validation_element.append(i.validation_element)
            validation_category.append(i.category)

        return Response({'validation_element':find_valobj.validation_element,
                         'category':find_valobj.category,'risk':find_valobj.risk,
                         'risk_level':find_valobj.risk_level,'finding_description':find_valobj.finding_description,
                         'response':find_valobj.response,'validation_element':validation_element,
                         'validation_category':validation_category,'response':find_valobj.response}, status=status.HTTP_200_OK)
    
    
class update_response_findings(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data------------------",request.data)       

        find_valobj = ValidationFindings.objects.get(mdl_id = request.data['mdlid'],findings_id= request.data['find_id'])

        if find_valobj:
            find_valobj.response=request.data['response']
            find_valobj.save()

        return Response({"updated":True}, status=status.HTTP_200_OK)


class get_ValidationRating(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self,request):  
        request_id=request.data['mdl_id']
        strQ="SELECT validation_rating,     STRING_AGG(CONCAT(case Severity when 'Low' then 'isnull(max(lowcnt),'')'   when 'Medium' then 'isnull(max(medcnt),'')' \
        when 'High' then 'isnull(max(highcnt),'')' end ,' ',operator,' ',value),' and ') condn\
        from [Validation_Rating_Master] where operator is not null and value is not null \
        group by validation_rating order by 1"
        objdbops=dbops() 
        df=objdbops.getTable(strQ)
        strfail=df.values[0][1]
        strneedsimprovement=df.values[1][1]
        strsatisfactory=df.values[2][1]
        strQ="select elemetsdetails.*,isnull(ratingdata.rating,'-') rating from  ( \
        select   elements_mst.Element_text ,sub_elements_mst.Element_text sub_element_text, elements_mst.Element_AID \
        ,Element_Sub_AID,isnull(str(lowcnt),'') lowcnt,isnull(str(medcnt),'')medcnt  ,isnull(str(highcnt),'') highcnt \
        from Finding_val_elements elements_mst   left join \
        Finding_val_sub_elements sub_elements_mst on    sub_elements_mst.Element_AID= elements_mst.Element_AID  \
        left join   validation_findings vf \
        on vf.Validation_element= elements_mst.Element_AID and  vf.mdl_id='"+ request_id  +"'  \
        and vf.Validation_Sub_element=sub_elements_mst.Element_Sub_AID \
        left join  \
        ( select mdl_id ,Risk,count(*) lowcnt,Validation_element ,Validation_Sub_element \
        from validation_findings where mdl_id='"+ request_id  +"' and  risk=1 group by mdl_id,Risk,Validation_element,Validation_Sub_element \
        ) lowrating on vf.Mdl_Id=lowrating.Mdl_Id and vf.Risk=lowrating.Risk and vf.Validation_element=lowrating.Validation_element \
        and vf.Validation_Sub_element=lowrating.Validation_Sub_element left join  \
        ( select mdl_id,Risk,count(*) medcnt,Validation_element ,Validation_Sub_element \
        from validation_findings  \
        where  mdl_id='"+ request_id  +"' and risk=2 group by mdl_id,Risk,Validation_element,Validation_Sub_element \
        ) mediumrating  on vf.Mdl_Id=mediumrating.Mdl_Id and vf.Risk=mediumrating.Risk  \
        and vf.Validation_element=mediumrating.Validation_element \
        and vf.Validation_Sub_element=mediumrating.Validation_Sub_element  \
        left join \
        ( select mdl_id,Risk,count(*) highcnt,Validation_element ,Validation_Sub_element \
        from validation_findings  \
        where  mdl_id='"+ request_id  +"' and risk=3 group by mdl_id,Risk,Validation_element,Validation_Sub_element \
        ) highrating    on vf.Mdl_Id=highrating.Mdl_Id and vf.Risk=highrating.Risk \
        and vf.Validation_element=highrating.Validation_element and vf.Validation_Sub_element=highrating.Validation_Sub_element  )elemetsdetails  left join  \
        ( \
        select vf.mdl_id,vf.Validation_element ,isnull(max(lowcnt),'') lowcnt,isnull(max(medcnt),'') medcnt ,isnull( max(highcnt),'')highcnt, \
        case when  "+ strfail +" then 'Fail' else \
        case when "+ strneedsimprovement+" then 'Needs Improvement' else  \
        case when "+ strsatisfactory + " then 'Satisfactory' else '-' end \
        end  end   rating \
        from validation_findings vf left join \
        ( select mdl_id ,Risk,count(*) lowcnt,Validation_element  \
        from validation_findings where mdl_id='"+ request_id  +"' and  risk=1 group by mdl_id,Risk,Validation_element \
        ) lowrating on vf.Mdl_Id=lowrating.Mdl_Id and vf.Risk=lowrating.Risk  \
        and vf.Validation_element=lowrating.Validation_element  \
        left join  \
        (select mdl_id,Risk,count(*) medcnt,Validation_element  \
        from validation_findings  \
        where  mdl_id='"+ request_id  +"' and risk=2 group by mdl_id,Risk,Validation_element  \
        ) mediumrating  on vf.Mdl_Id=mediumrating.Mdl_Id and vf.Risk=mediumrating.Risk  \
        and vf.Validation_element=mediumrating.Validation_element  left join  \
        ( select mdl_id,Risk,count(*) highcnt,Validation_element  \
        from validation_findings  \
        where  mdl_id='"+ request_id  +"' and risk=3 group by mdl_id,Risk,Validation_element )  \
        highrating   on vf.Mdl_Id=highrating.Mdl_Id and vf.Risk=highrating.Risk \
        and vf.Validation_element=highrating.Validation_element   \
        where vf.mdl_id='"+ request_id  +"' \
        group by  vf.mdl_id,vf.Validation_element) ratingdata  \
        on ratingdata.Validation_element=elemetsdetails.Element_AID  "
        tableResult =objdbops.getTable(strQ)
        data = tableResult.to_json(orient='index')
        data = json.loads(data)
        return Response(data,status=status.HTTP_200_OK)


class fetch_model_report(APIView):
    def get(self,request):
        print("request_data------------------",request.data)
        template_obj=ReportTitleTemplate.objects.filter(template_name=request.data['tamplate_name'])
        title_data=dict()
        for i in template_obj:
            print("title_label",i.title_label)
            title_data[i.title_id]=i.title_label
        print("title_data",title_data)

        return Response(title_data)

class get_header_n_title(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            strQ="SELECT   title_id  , Header_or_Title , isnull(Comment,'')  Comment , Label , mdl_id  ,title_type,fontsize, \
                case alignment when 'center' then 'C' when 'left' then 'L' when 'right' then 'R' end alignment ,page_no    FROM  \
                Report_Header_Title_Content  where template_name='"+ request.data['temp_name']+ "' \
                and mdl_id='"+ request.data['mdl_id']+ "'  order by page_no,title_sort_idx"           
            tableResult =objdbops.getTable(strQ)  
            ttlnheadrs = tableResult.to_json(orient='index')
            ttlnheadrs = json.loads(ttlnheadrs) 
            maxlen=objdbops.getscalar("SELECT  isnull(max(len(Label)),0) maxlen FROM  Report_Header_Title_Content  where template_name='"+ request.data['temp_name']+"' and mdl_id='"+ request.data['mdl_id']+ "' and title_type='Header' ")
            return Response({'ttlnheadrs':ttlnheadrs,'maxlen':maxlen},status=status.HTTP_200_OK)
        except Exception as e:
            print('setuppycaret is ',e)
            print('setuppycaret traceback is ', traceback.print_exc()) 


class updateTempHeaderIdx(APIView):
    def post(self,request):
        
        try:
            title_id=request.data['title_id'] 
            page_no=request.data['page_no']
            title_sort_idx=request.data['title_sort_idx']  
            
            strQ="update temp_report_title_template set title_sort_idx="+str(title_sort_idx)+" where title_id="+str(title_id)+" and page_no="+str(page_no)
            objdbops.insertRow(strQ)
            return Response({'is_taken':True})
        except Exception as e:
            print('error is  ',e)



class deleteTempHeaderIdx(APIView):
    def post(self,request):
        
        try:
            title_id=request.data['title_id'] 
            page_no=request.data['page_no'] 
            
            strQ="delete from temp_report_title_template  where title_id="+str(title_id)+" and page_no="+str(page_no)
            objdbops.insertRow(strQ)
            return Response({'is_taken':True})
        except Exception as e:
            print('error is  ',e)

class insertFromTemp(APIView):
    def post(self,request):
        try:
            template_name=request.data['template_name']  
            
            strQ=" update temp_report_title_template set template_name='"+template_name +"'"
            objdbops.insertRow(strQ)
            strQ="INSERT INTO  report_title_template \
                ( title_id ,title_or_heading,title_label ,added_by ,added_on ,updated_by ,updated_on ,template_name ,title_type ,title_placeholder ,title_sort_idx,fontsize ,alignment,page_no)\
		        select  title_id ,title_or_heading,title_label ,added_by ,added_on ,updated_by ,updated_on ,template_name ,title_type ,title_placeholder ,title_sort_idx,fontsize ,alignment,page_no from temp_report_title_template "
            objdbops.insertRow(strQ)
            strQ="truncate table temp_report_title_template"
            objdbops.insertRow(strQ)
            return Response({'is_taken':True})
        except Exception as e:
            print('error is  ',e)     




class get_cat_cols(APIView): 
    permission_classes = [IsAuthenticated]
    def get(self,request): 
        try:
            df=find_DA_src_data(request.data['mdl_id'],request.data['dataset'] )
            print("df",df)
            cat_cols_temp = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] in [np.object]] 
            cat_cols=[]
            print("cat_cols",cat_cols)
            print("cat_cols_temp",cat_cols_temp)

            for x in cat_cols_temp:
                if len(df[x].value_counts())<25:
                    cat_cols.append(x)
            print("cat_cols",cat_cols) 

            return JsonResponse(cat_cols,safe=False )

        except Exception as e:
            print('error is ',e,traceback.print_exc()) 


class get_num_cols(APIView): 
    permission_classes = [IsAuthenticated]
    def get(self,request): 
        try:
            df=find_DA_src_data(request.data['mdl_id'],request.data['dataset'] )
            print("df",df)
            num_cols_temp = [c for i, c in enumerate(
                df.columns) if df.dtypes[i] not in [np.object]]
            print("num_cols_temp ",num_cols_temp)
            num_cols=[]
            for x in num_cols_temp:
                # if len(df[x].value_counts())<25:
                num_cols.append(x)
            print("num_cols",num_cols)

            return JsonResponse(num_cols,safe=False )

        except Exception as e:
            print('error is ',e,traceback.print_exc()) 

class get_da_data(APIView): 
    permission_classes = [IsAuthenticated]
    def post(self,request): 
        try:
            df=find_DA_src_data(request.data['mdl_id'],request.data['dataset'] )
            
            df = df.to_json(orient='index')
            df = json.loads(df)
            return JsonResponse({'da_data':df},safe=False )

        except Exception as e:
            print('error is ',e,traceback.print_exc()) 

 

class showcorrelation_da(APIView): 
    permission_classes = [IsAuthenticated]
    def post(self,request):
        
        # file_id=find_DA_max_file_id(request.data['user_id'])

        # x=find_DA_src_data(file_id,request.data['dataset']) 
        # print("df",x)

        x=find_DA_src_data(request.data['user_id'],request.data['dataset'])
        print("df",x)
    
        # dfcorr = x.corr().round(decimals=4) 
        dfcorr = x.select_dtypes(include='number').corr().round(decimals=4)
        # print(dfcorr.columns)
        result = dfcorr.to_json(orient='index')
        result = json.loads(result)

        fig = plt.figure(figsize=(14, 8))

        sns_plot = sns.heatmap(dfcorr, annot=False)
        fig = sns_plot.get_figure()
        plt.tight_layout()

        current_timestamp = datetime.now()

        formatted_timestamp = current_timestamp.strftime("%Y-%m-%d_%H-%M-%S")
        print("Formatted Timestamp:", formatted_timestamp)

        directory = os.path.join( 'static/media/DA/HeatMap', str(request.data['user_id']))
        if not os.path.exists(directory):
            os.makedirs(directory)

        image_path = os.path.join(directory, f"{request.data['username']}_outputcorrelation_{formatted_timestamp}.png")
        json_data=dict()

        fig.savefig(image_path, dpi=400)
        # (result)
        file_stream = BytesIO()
        print("file_stream",file_stream)
        image_data = PIL.Image.open(image_path)
        print("image_data",image_data)
        image_data.save(file_stream,'png')
        # image_data.save(file_stream.png)
        # print("image_data",image_data)
        print("image_data",type(image_data))
        file_stream.seek(0)
        base64_data = base64.b64encode(file_stream.getvalue()).decode('utf-8')
        
        json_data['report'] = base64_data 
          # if os.path.exists(os.path.join(
        #         BASE_DIR, 'static\media\outputcorrelation.png')):
        # pdf = FPDF()
        # pdf.add_page()
        # pdf = exportgraphImgPdf(pdf, os.path.join(
        #     BASE_DIR, plot_dir_view+user_name+'outputcorrelation.png'),  "Correlation on independent variables-Heat map", "")
        # pdf.output(os.path.join(
        #     BASE_DIR, plot_dir_view+user_name+'Heatmap.pdf'))

        return JsonResponse(json_data)




class Is_BackInfo_Exists(APIView):
    objdbops =None
    def __init__(self):
        self.objdbops=dbops()
    def get(self,request):
        strQ = "  select count(Bank_Domain_Name) from Bank_Details"        
        recordsCnt=  self.objdbops.getscalar(strQ)       
        tableResult=''
        if int (recordsCnt)> 0:
            strQ="Select * from Bank_Details "
            tableResult=  self.objdbops.getTable(strQ)  
            tableResult= tableResult.to_json(orient='index')
            tableResult=json.loads(tableResult)
        return Response({'data':recordsCnt,'bankInfo':tableResult}) 

class Add_BankInfo(APIView):
    objdbops =None
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        strQ = "  select count(Bank_Domain_Name) from Bank_Details"        
        tableResult=  self.objdbops.getscalar(strQ)   
        if str(tableResult)=="0" :
            strQ="INSERT INTO  Bank_Details ( Bank_Name , Bank_Domain_Name , Bank_Address  , Added_by , Added_On ,Bank_Logo,Bank_AI_Name,Fin_Inst)\
                VALUES ('"+request.data['bankName']+"' ,'"+request.data['domain']+"' ,'"+request.data['bankAddress']+"' ,"+str(request.data['addedby'])+" ,getdate(),'"+request.data['file_name']+"','"+request.data['bankAI']+"','"+request.data['FinInst']+"')"
            self.objdbops.insertRow(strQ)
        else:
            strQ="update Bank_Details set Bank_Name= '"+request.data['bankName']+"', Bank_Domain_Name= '"+request.data['domain']+"', Bank_Address='"+request.data['bankAddress']+"', Bank_AI_Name='"+request.data['bankAI']+"'  , Fin_Inst='"+request.data['FinInst']+"'  , Added_by="+str(request.data['addedby'])+" , Added_On=getdate()"       
            self.objdbops.insertRow(strQ)
        return Response({'data':tableResult}) 

class Get_UC_DEPT(APIView):
    objdbops =None
    def __init__(self):
        self.objdbops=dbops()
    def get(self,request):
        try:  
            tableResult = self.objdbops.getTable("SELECT   UC_AID  ,UC_Label  FROM User_Category where UC_Label <> 'Admin'  order by 2 ")
            users = tableResult.to_json(orient='index')
            users = json.loads(users)
            del tableResult
            

            tableResult =self.objdbops.getTable("SELECT Dept_AID,Dept_Label FROM Department") 
            dept = tableResult.to_json(orient='index')
            dept = json.loads(dept)
            del tableResult

            tableResult =objdbops.getTable("select * from Resources order by 1")  
            resources = tableResult.to_json(orient='index')
            resources = json.loads(resources)
            del tableResult
            return Response({'utype':users,'dept':dept,'resources':resources})
        except Exception as e:
            print('adduser is ',e)
            print('adduser traceback is ', traceback.print_exc()) 
     

class Update_Useraccess(APIView):
    objdbops =None
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            uc = request.data['uc'] 
            dept = request.data['dept']  
            colDataLst = request.data['datalist']   
            
            strQ="delete from User_Access where UC_AID="+str(uc) + " and ua_dept="+str(dept)
            objdbops.insertRow(strQ) 

            for colval in colDataLst: 
                strQ="INSERT INTO User_Access (R_AID,UA_Perm,UC_AID,AddDate,UA_Add,UA_Edit,UA_Delete,UA_Dept)  VALUES ("
                strQ +=colval['AID'] +",'"+colval['UA']+"',"+str(uc)+",getdate(),"+ str(colval['add']) +","+str(colval['edit']) +","+ str(colval['delete']) +","+ str(dept) +")"
                self.objdbops.insertRow(strQ)
            
            return JsonResponse({'istaken':'true'})
        except Exception as e:
            print('updateaccess ',e,traceback.print_exc())
            return JsonResponse({'istaken':'false'})
        
class Get_Useraccess(APIView):
    objdbops =None
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            uc = request.data['uc'] 
            dept = request.data['dept']     
            print("select ua.*,rs.R_Is_MRM,  from user_access ua ,Resources rs where rs.R_AID=ua.R_AID and  uc_aid="+ str(uc) + " and ua_dept="+ str(dept))
            tableResult =self.objdbops.getTable("select ua.*,rs.R_Is_MRM from user_access ua ,Resources rs where rs.R_AID=ua.R_AID and  uc_aid="+ str(uc) + " and ua_dept="+ str(dept))
            tableResult= tableResult.to_json(orient='index')
            tableResult=json.loads(tableResult)      
            is_MRM=self.objdbops.getscalar("select case dept_ismrm when 1 then 'true' else 'false' end from department where dept_AID="+ str(dept) +"")     
            print('is_MRM ',is_MRM)    
            return JsonResponse({'ucdata':tableResult,'is_MRM':is_MRM})
        except Exception as e:
            print('updateaccess ',e,traceback.print_exc())
            return JsonResponse({'ucdata':'false'}) 
       
class Get_User_Deatils(APIView):
    objdbops =None
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            utype=request.data['uc']
            dept=request.data['dept']
            strq= "select rs.r_aid,r_label, 'block' sts  ,UA_Perm 'AccessPerm' from user_access ua , Resources rs where rs.R_AID=ua.r_AID and  ua.uc_AID='"+str(utype)+"' and ua.UA_dept='"+str(dept)+"' "
            strq=strq + " union "
            strq=strq + " select *,'none' ,'' from( "
            strq=strq + " SELECT r_aid,r_label from Resources "
            strq=strq + " except "
            strq=strq + " select rs.r_aid,r_label   "
            strq=strq + " from user_access ua , Resources rs where rs.R_AID=ua.r_AID "
            strq=strq + " and  ua.uc_AID='"+ str(utype)+ "'  and ua.UA_dept='"+str(dept)+"')a " 
            strq=strq + " union "
            strq=strq + " select count(*),'Dept Head',case when count(*)=1 then 'block' else 'none' end,'' from user_category where uc_is_depthead=1 and uc_AID='"+ str(utype)+ "'"
            strq=strq + " union "
            strq=strq +  "select rs.r_aid,r_label, 'block' sts  ,UA_Perm 'AccessPerm'  from user_access ua , Resources rs where rs.R_AID=ua.r_AID and  ua.uc_AID='"+str(utype)+"' and ua.UA_dept='"+str(dept)+"' "
            print(strq)  

            tableResult =self.objdbops.getTable(strq)  
            tableResult= tableResult.to_json(orient='index') 
            tableResult=json.loads(tableResult)        
            ai_name=self.objdbops.getscalar("select Bank_AI_Name from bank_details")
            return JsonResponse({'ucdata':tableResult,'ai_name':ai_name})
        except Exception as e:
            print('updateaccess ',e,traceback.print_exc())
            return JsonResponse({'ucdata':'false'}) 

class Add_BankDoc(APIView):
    objdbops =None
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        strQ = "  select count(*) from Bank_Docs where Doc_Type='"+request.data['docType']+"'"        
        tableResult=  self.objdbops.getscalar(strQ)   
        if str(tableResult)=="0" :
            strQ="INSERT INTO Bank_Docs  ( Doc_Type , Doc_Desc , Doc_Name , Added_by , Added_On ) \
                VALUES ('"+request.data['docType']+"' ,'"+request.data['docDesc']+"' ,'"+request.data['docName']+"' ,"+str(request.data['addedby'])+" ,getdate())"
            self.objdbops.insertRow(strQ)
        else:
            strQ="update Bank_Details set Doc_Type= '"+request.data['docType']+"', Doc_Desc= '"+request.data['docDesc']+"', Doc_Name='"+request.data['docName']+"', Added_by="+str(request.data['addedby'])+" , Added_On=getdate()"       
            self.objdbops.insertRow(strQ)
        return Response({'data':tableResult}) 
    
class getModelQtnById(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:     
            mdl_id = request.data['mdl_id']
            ques = request.data['ques']
            return Response({"Qtns":objrmse.getModelQtnsById(mdl_id,ques)}, status=status.HTTP_200_OK)
        except Exception as e: 
                error_saving(request,e)
                return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)
        
class Fetch_Allmessage(APIView):
    objdbops =None
    def __init__(self):
        self.objdbops=dbops()
    def get(self,request):
        strQ = "SELECT utility, sub_utility, [Comment_id],FORMAT (resp.[added_on],'hh:mm tt  MMM dd, yyyy') createdt ,[Comment],"
        strQ+=" concat(u.U_FName,' ',u.U_LName) addedby,upper(concat(left(u.U_FName,1),left(u.U_LName,1))) uinitials ,chat_data,isnull(file_pah,'')  as 'filename'"
        strQ+=" from  [VT_User_Discussion] resp,users u"
        strQ+=" where u.U_AID=resp.[added_by] and [Mdl_Id]='"+request.data['mdl_id']+"'  order by [Comment_id]"
        
        tableResult=  self.objdbops.getTable(strQ)  
        commenthistory= tableResult.to_json(orient='index')         
        return Response(json.loads(commenthistory))



class GetDocsNameAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        try:
            master = MdlDocuments.objects.filter(mdl_id = request.data['mdl_id'],mdl_doc_type = request.data['mdl_doc_type'])
            serializer =  MdlDocumentsSerializer(master,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("docs error is",e)

class GetMdlDocumentsAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        try:
            master = MdlDocuments.objects.filter(mdl_id = request.data['mdl_id'])
            serializer =  MdlDocumentsSerializer(master,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("docs error is",e)


class generate_task_ID(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        model_id=request.data['model_id']
        task_Lbl=request.data['task_Lbl']
        task_type=request.data['task_type']

        task_id=get_latest_task(model_id,task_Lbl,task_type)
        print("final task Id",task_id)
        task_link_ID={}
        task_link_ID['task_id']=task_id
        task_link_ID['model_id']=model_id
        return Response(task_link_ID)

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


class update_summery_data(APIView):
    permission_classes=[IsAuthenticated]
    def put(self,request):
        task_id=request.data['task_id']
        print("task_id",task_id)
        assignee_comments=request.data['assignee_comments']
        completion_status=request.data['completion_status']
        approval=request.data['approval']
        updated_by=request.data['updated_by']
        update_date=datetime.now()
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
            approver_comments=request.data['approver_comments']
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
            objmaster.insertActivityTrail(task_id,"8","Task updated by approver - "+task_registration_obj.task_name,request.data['uid'],request.data['accessToken'])
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

            objmaster.insertActivityTrail(task_id,"8","Task updated by assignee - "+task_registration_obj.task_name,request.data['uid'],request.data['accessToken'])

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
        return Response({'updated':'true','task_assignee_lst':(task_assignee_lst),
                            'task_approver_lst':(task_approver_lst),'originatorid':int(updated_by),'task_id':task_id,
                            'task_approver_thread_lst':(task_approver_thread_lst),'task_assignee_thread_lst':(task_assignee_thread_lst)}) 



# class issue_registration(APIView):

#     permission_classes=[IsAuthenticated]
#     def get(self,request,id=None):
#         id=request.data['uid']
#         if id:
#             print("id",id)

#             ## one user Obj
#             usr = Users.objects.get(u_aid=id)
#             user_serializer = UserSerializer(usr)
#             user_obj=user_serializer.data
#             print("user_obj",user_obj)

#             added_by = user_obj['u_aid']
#             today_date=datetime.now()
#             originator_name=user_obj['u_fname']  +" " + user_obj['u_lname']

#             ## department obj
#             tasksub = Department.objects.get(dept_aid=user_obj['dept_aid'])
#             department_serializer = DepartmentSerializer(tasksub)
#             department_obj = department_serializer.data
#             print("department_obj",department_obj)

#             ##all users
#             usrmaster = Users.objects.all()
#             all_user_serializer =  UserSerializer(usrmaster,many=True)
#             users_obj=all_user_serializer.data
#             # print("users_obj",users_obj)
            
#             ## user category
#             usrmaster = UserCategory.objects.all()
#             user_cat_serializer =  UserCategorySerializer(usrmaster,many=True)

#             ## issue function
#             issuefunctionmaster = IssueFunctionMaster.objects.all()
#             issue_fun_serializer =  IssueFunctionMasterSerializer(issuefunctionmaster,many=True)

#             ##issue priority
#             issueprioritymaster = IssuePriorityMaster.objects.all()
#             issue_priority_serializer =  IssuePriorityMasterSerializer(issueprioritymaster,many=True)

#             ##issue approval status
#             issueapprovalstatusmaster = IssueApprovalstatusMaster.objects.all()
#             issue_status_serializer =  IssueApprovalstatusMasterSerializer(issueapprovalstatusmaster,many=True)

#             ## mdl overview
#             modeloverview =  ModelOverview.objects.all()
#             mdl_overview_serializer =  ModelOverviewSerializer(modeloverview,many=True)

#             ## issue type
#             issuetypemaster =  Issue_Type_Master.objects.all()
#             issue_type_serializer =  Issue_Type_MasterSerializer(issuetypemaster,many=True)

            
#             context={'added_by':added_by,'issue_function_obj':issue_fun_serializer.data,'issue_priority_obj':issue_priority_serializer.data,
#                      'issue_type_obj':issue_type_serializer.data,'issue_approval_master':issue_status_serializer.data,
#                      'originator_name':originator_name,'user_category_obj':user_cat_serializer.data,
#              'department_obj':department_obj,'users_obj':users_obj,'mdl_overview_obj':mdl_overview_serializer.data
#              }  

#             return Response(context, status=status.HTTP_200_OK)


class issue_registration(APIView):

    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        id=request.data['uid']
        if id:
            print("id",id)

            ## one user Obj
            usr = Users.objects.get(u_aid=id)
            user_serializer = UserSerializer(usr)
            user_obj=user_serializer.data
            print("user_obj",user_obj)

            added_by = user_obj['u_aid']
            today_date=datetime.now()
            originator_name=user_obj['u_fname']  +" " + user_obj['u_lname']

            ## department obj
            tasksub = Department.objects.get(dept_aid=user_obj['dept_aid'])
            department_serializer = DepartmentSerializer(tasksub)
            department_obj = department_serializer.data
            print("department_obj",department_obj)

            ##all users
            usrmaster = Users.objects.all()
            all_user_serializer =  UserSerializer(usrmaster,many=True)
            users_obj=all_user_serializer.data
            # print("users_obj",users_obj)
            
            ## user category
            usrmaster = UserCategory.objects.all()
            user_cat_serializer =  UserCategorySerializer(usrmaster,many=True)

            ## issue function
            issuefunctionmaster = IssueFunctionMaster.objects.all()
            issue_fun_serializer =  IssueFunctionMasterSerializer(issuefunctionmaster,many=True)

            ##issue priority
            issueprioritymaster = IssuePriorityMaster.objects.all()
            issue_priority_serializer =  IssuePriorityMasterSerializer(issueprioritymaster,many=True)

            ##issue approval status
            issueapprovalstatusmaster = IssueApprovalstatusMaster.objects.all()
            issue_status_serializer =  IssueApprovalstatusMasterSerializer(issueapprovalstatusmaster,many=True)

            ## mdl overview
            modeloverview =  ModelOverview.objects.all()
            mdl_overview_serializer =  ModelOverviewSerializer(modeloverview,many=True)

            ## issue type
            issuetypemaster =  Issue_Type_Master.objects.all()
            issue_type_serializer =  Issue_Type_MasterSerializer(issuetypemaster,many=True)

            
            context={'added_by':added_by,'issue_function_obj':issue_fun_serializer.data,'issue_priority_obj':issue_priority_serializer.data,
                     'issue_type_obj':issue_type_serializer.data,'issue_approval_master':issue_status_serializer.data,
                     'originator_name':originator_name,'user_category_obj':user_cat_serializer.data,
             'department_obj':department_obj,'users_obj':users_obj,'mdl_overview_obj':mdl_overview_serializer.data
             }  

            return Response(context, status=status.HTTP_200_OK)

    def post(self,request):
        print("issue_registration")
        issue_id = request.data['issue_id']
        department = request.data['department']
        originator = request.data['originator']
        issue_function = request.data['issue_function']
        issue_registration_date = request.data['registration_date']
        issue_type = request.data['issue_type']
        sub_issue_type = request.data['sub_issue_type']
        issue_priority = request.data['priority']
        issue_end_date = request.data['end_date']
        issue_completion_status = request.data['completion_status']
        issue_approval_status = request.data['approval_status']
        issue_major_ver = request.data['issue_major_ver']
        issue_minor_ver = request.data['issue_minor_ver']
        added_by = request.data['addedby']
        today_date = datetime.now()
        link_id = request.data['link_id']

        issue_relevant_personnel_check = request.data['issue_relevant_personnel_check']
        issue_summery_check = request.data['issue_summery_check']

        issue_assignee_lst=[]
        issue_approver_lst=[]
        issue_assignee_thread_lst=[]
        issue_approver_thread_lst=[]

        issue_registration_obj=IssueRegistration(issue_id=issue_id,department=department,originator=originator,issue_function=issue_function,
                                                registration_date=issue_registration_date,issue_type=issue_type,sub_issue_type=sub_issue_type,
                                                priority=issue_priority,end_date=issue_end_date,completion_status=issue_completion_status,
                                                approval_status=issue_approval_status,issue_major_ver=issue_major_ver,
                                                issue_minor_ver=issue_minor_ver,addedby=added_by,adddate=today_date,
                                                link_id=link_id
                                                )    

        issue_registration_obj.save()

        if issue_relevant_personnel_check == 'True':
            originator_relevant=request.data['issue_originator_relevant']
            issue_assigned_to=request.data['issue_assigned_to']
            issue_approved_by=request.data['issue_approved_by']
            print('issue_approved_by',issue_approved_by)
            print('issue_assigned_to',issue_assigned_to)
            # print('Relevant Personnel',relevant_personnel,originator_relevant,assigned_to,approved_by)
            if originator_relevant:
                issue_relevant_personnel_obj=IssueRelevantPersonnel(u_type="Originator",u_id=added_by,
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
            issue_summery=request.data['issue_summery_comments']
            issue_requirement=request.data['issue_requirements_comments']
            # issue_assignee_comments=request.data['issue_assignee_comments']
            # issue_approval=request_data['issue_approval']
            # issue_approver_comments=request.data['issue_approver_comments']
            # print("issue_approver_comments",issue_approver_comments)
            
            issue_summery_obj=IssueSummery(issue_summery=issue_summery,issue_requirement=issue_requirement,
                                                     issue=issue_registration_obj,addedby=added_by,adddate=today_date)
            issue_summery_obj.save() 
            print("saved summ data")
        print("saved")

        return Response(status=status.HTTP_200_OK)


class get_sub_issue_type(APIView):
    permission_classes=[IsAuthenticated] 
    def get(self,request):

        issue_type_aid=request.data['issue_type_aid']

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
        print("sub_issue_data",sub_issue_data)    
        
        return Response(sub_issue_data) 

class generate_issueID(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        model_id=request.data['model_id']
        issue_Lbl=request.data['issue_Lbl']
        issue_type=request.data['issue_type']

        issue_id=get_latest_issue(model_id,issue_Lbl,issue_type)
        print("final issue Id",issue_id)
        issue_link_ID={}
        issue_link_ID['issue_id']=issue_id
        issue_link_ID['model_id']=model_id
        return Response(issue_link_ID)

def get_latest_issue(modal_id,issue_Lbl,issue_type): 
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



class get_issue_ID_data(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        issue_id=request.data['id']
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

        return Response({'department':department,'originator':originator,'issue_function_label':issue_function_label,'reg_date':reg_date.strftime('%m-%d-%Y'),
                         'issue_type_label':issue_type_label,'sub_issue_type_label':sub_issue_type_label,'issue_priority_label':issue_priority_label,
                         'end_date':end_date.strftime('%m-%d-%Y'),'completion_status':completion_status,'issue_summery':issue_summery,
                         'issue_req':issue_req,'issue_approvalstatus_label':issue_approvalstatus_label,'approval_status':approval_status,'issue_dict':issue_dict,
                         'issue_assignee':issue_assignee,'approver_comments':approver_comments})

class issue_update_summery_data(APIView):
    permission_classes=[IsAuthenticated]
    def put(self,request):
        #notification code

        issue_id=request.data['issue_id']
        assignee_comments=request.data['assignee_comments']
        completion_status=request.data['completion_status']
        approval=request.data['approval']
        updated_by=request.data['updated_by']
        update_date=datetime.now()

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
            approver_comments=request.data['approver_comments']
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
            objmaster.insertActivityTrail(issue_id,"11","Issue updated by assignee", request.data['uid'],request.data['accessToken'])
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
            objmaster.insertActivityTrail(issue_id,"11","Issue updated by assignee", request.data['uid'],request.data['accessToken'])
        
        return Response({'updated':'true','issue_assignee_lst':(issue_assignee_lst),
                            'issue_approver_lst':(issue_approver_lst),'originatorid':int(updated_by),'issue_id':issue_id,'issue_assignee_thread_lst':(issue_assignee_thread_lst)})

class edit_issue(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        issue_id=request.data['id']

        issue_obj=IssueRegistration.objects.get(issue_id=issue_id)
        department=issue_obj.department
        originator=issue_obj.originator
        print("originator",originator)
        added_by=issue_obj.addedby
        issue_function=issue_obj.issue_function
        issue_function_obj=IssueFunctionMaster.objects.get(issue_function_aid=issue_function)
        issue_function_label=issue_function_obj.issue_function_label
        print("issue_function_label",issue_function_label)
        reg_date=issue_obj.registration_date
        reg_date=reg_date.strftime('%m-%d-%Y')
        issue_type=issue_obj.issue_type
        issue_type_obj=Issue_Type_Master.objects.get(issue_type_aid=issue_type)
        issue_type_label=issue_type_obj.issue_type_label
        issue_type_aid=issue_type_obj.issue_type_aid

        sub_issue_type_objs = list(Sub_Issue_Type_Master.objects.filter(issue_type_aid=issue_type_aid).values())

        
        sub_issue_type=issue_obj.sub_issue_type
        sub_issue_type_obj=Sub_Issue_Type_Master.objects.get(sub_issue_type_aid=sub_issue_type)
        sub_issue_type_label=sub_issue_type_obj.sub_issue_type_label

        priority=issue_obj.priority
        print('priority',priority)
        priority_obj=IssuePriorityMaster.objects.get(issue_priority_aid=priority)
        issue_priority_label=priority_obj.issue_priority_label
        print("issue_priority_label",issue_priority_label)
        end_date=issue_obj.end_date.strftime('%m-%d-%Y')
        completion_status=issue_obj.completion_status
        approval_status=issue_obj.approval_status
        approval_status_label=IssueApprovalstatusMaster.objects.get(issue_approvalstatus_aid=approval_status).issue_approvalstatus_label
        issue_summery_obj=IssueSummery.objects.get(issue=issue_id)
        issue_summery=issue_summery_obj.issue_summery
        print("issue_summery",issue_summery)
        issue_req=issue_summery_obj.issue_requirement

        assignee_user=list()
        relevant_personal_assignee=IssueRelevantPersonnel.objects.filter(issue=issue_id,u_type='Assignee')
        for i in relevant_personal_assignee:
            #print("relevant_personal_assignee",i.u_id)
            
            assignee_user_obj=Users.objects.filter(u_aid=i.u_id)
            for k in assignee_user_obj:
                assignee_user.append(k.u_aid)
        print("assignee_user",assignee_user)

        all_user=list()
        users_obj=Users.objects.all()
        dict_data=dict()
        
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

        print("assignee_user_lst",assignee_user_lst)
        print("dict_data",dict_data)
        
        approver_user=list()    
        relevant_personal_approver=IssueRelevantPersonnel.objects.filter(issue=issue_id,u_type='Approver')
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

            context={'issue_id':issue_id,'department':department,'originator':originator,'issue_function_label':issue_function_label,'issue_function':issue_function,'reg_date':reg_date,
                         'issue_type_label':issue_type_label,'sub_issue_type_label':sub_issue_type_label,'sub_issue_type':sub_issue_type,
                         'issue_priority_label':issue_priority_label,
                         'end_date':end_date ,'completion_status':completion_status,'issue_summery':issue_summery,'priority':priority,
                         'assignee_user_obj':assignee_user_lst,'approver_user_obj':approver_user_lst,
                         'issue_req':issue_req,'approval_status':approval_status,'approval_status_label':approval_status_label,
                         'sub_issue_type_objs':sub_issue_type_objs}

            return Response(context) 

    def put(self,request):
        issue_id = request.data['issue_id']
        department = request.data['department']
        originator = request.data['originator']
        issue_function = request.data['issue_function']
        registration_date = request.data['registration_date']
        issue_aid = request.data['issue_aid']
        sub_issue_type = request.data['sub_issue_type']
        priority = request.data['priority']
        end_date = request.data['end_date']
        completion_status = request.data['completion_status']
        approval_status = request.data['approval_status']
        issue_summery = request.data['issue_summery']
        issue_req = request.data['issue_req']

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
        
        print("saved")

        return Response(status=status.HTTP_200_OK)


class issue_assignee(APIView):
    def get(self,request):
     
        U_id=request.data['uid']
        issueid =request.data['issue_id']
        print('U_id',U_id)

        issue_approval_master=IssueApprovalstatusMaster.objects.all().values()
        issue_relevant_obj=IssueRelevantPersonnel.objects.filter(u_id=U_id,u_type="Assignee").values()

        issue_obj=IssueRegistration.objects.get(issue_id=issueid)

        originator=issue_obj.originator

        assignee_user=list()
        relevant_personal_assignee=IssueRelevantPersonnel.objects.filter(issue=issueid,u_type='Assignee')
        for i in relevant_personal_assignee:
            #print("relevant_personal_assignee",i.u_id)
            
            assignee_user_obj=Users.objects.filter(u_aid=i.u_id)
            for k in assignee_user_obj:
                assignee_user.append(k.u_aid)
        print("assignee_user",assignee_user)

        all_user=list()
        users_obj=Users.objects.all()
        dict_data=dict()
        
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

        print("assignee_user_lst",assignee_user_lst)
        print("dict_data",dict_data)
        
        approver_user=list()    
        relevant_personal_approver=IssueRelevantPersonnel.objects.filter(issue=issueid,u_type='Approver')
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
    

        context={"issue_relevant_obj":issue_relevant_obj,'issue_approval_master':issue_approval_master,'issueid':issueid,'originator':originator,
            'assignee_user_obj':assignee_user_lst,'approver_user_obj':approver_user_lst}

        return Response( context, status=status.HTTP_200_OK)



class issue_approver(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
       
        issueid = request.data['issue_id']
        uid = request.data['uid']
        
        issue_approval_master=IssueApprovalstatusMaster.objects.all().values()
        issue_relevant_obj=IssueRelevantPersonnel.objects.filter(u_id=uid,u_type="Approver").values()
        
        issue_obj=IssueRegistration.objects.get(issue_id=issueid)
        originator=issue_obj.originator

        assignee_user=list()
        relevant_personal_assignee=IssueRelevantPersonnel.objects.filter(issue=issueid,u_type='Assignee')
        for i in relevant_personal_assignee:
            #print("relevant_personal_assignee",i.u_id)
            
            assignee_user_obj=Users.objects.filter(u_aid=i.u_id)
            for k in assignee_user_obj:
                assignee_user.append(k.u_aid)
        print("assignee_user",assignee_user)

        all_user=list()
        users_obj=Users.objects.all()
        dict_data=dict()
        
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

        print("assignee_user_lst",assignee_user_lst)
        print("dict_data",dict_data)
        
        approver_user=list()    
        relevant_personal_approver=IssueRelevantPersonnel.objects.filter(issue=issueid,u_type='Approver')
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
 
        context={"issue_relevant_obj":issue_relevant_obj,'issue_approval_master':issue_approval_master,'issueid':issueid,'originator':originator,
            'assignee_user_obj':assignee_user_lst,'approver_user_obj':approver_user_lst}
        
        return Response( context, status=status.HTTP_200_OK)


class email_details(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        print("data",request.data)
        email_settings = Emailsettings.objects.values().first()  

        if email_settings:
            return JsonResponse(email_settings)


    def post(self,request):
        print("data",request.data)
        sender_address = request.data['sender_address']
        sender_password = request.data['sender_password']
        smtp_server = request.data['smtp_server']
        port = request.data['port']
        try:
            
            email_record = Emailsettings.objects.first()

            if email_record:
                #  Update existing record
                email_record.senderaddress = sender_address
                email_record.senderpassword = sender_password
                email_record.smtpserver = smtp_server
                email_record.port = port
                email_record.updatedat = datetime.now()
                email_record.save()
                action = 'updated'
            else:
                # Create new record
                Emailsettings.objects.create(
                    senderaddress=sender_address,
                    senderpassword=sender_password,
                    smtpserver=smtp_server,
                    port=port,
                    createdat=datetime.now()
                )
                action = 'created'

            return JsonResponse({'msg': f'Email settings {action} successfully.'})

        except Exception as e:
            return JsonResponse({'msg': f'Error: {str(e)}'}, status=500)


class scheduler_notification(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("data",request.data)
        Notificationschedule.objects.create(
            alert_type=request.data['alert_type'],
            frequency=request.data['frequency'],
            time=request.data['time'],
            day_of_week=request.data['day_of_week'] ,
            date_of_month=request.data['date_of_month'],
            notify_days_before=request.data['days_before'],
            is_active=request.data['is_active']
        )
        print("saved")

        return JsonResponse({'msg': f'Notification is scheduled successfully.'})


class get_alert_schedule_data(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        print("data",request.data)
        alert_type=request.data['alert_type']
        try:
            schedule = Notificationschedule.objects.get(alert_type=alert_type)
            return JsonResponse({
                'frequency': schedule.frequency,
                'time': schedule.time.strftime('%H:%M'),
                'day_of_week': schedule.day_of_week,
                'date_of_month': schedule.date_of_month,
                'notify_days_before': schedule.notify_days_before,
                'is_active': schedule.is_active
            })
        except Notificationschedule.DoesNotExist:
            return JsonResponse({'error': 'No schedule found for this alert.'}, status=404)



class save_comments_mdl_overview(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        uid=request.data['uid']
        print("save_comments_mdl_overview---   uid",uid)
        comments = DashboardComments.objects.filter(uid=uid)
        comments_dict = {}
        for c in comments:
            if c.section not in comments_dict:
                comments_dict[c.section] = {}
            comments_dict[c.section][c.field_name] = c.comment

        # response_data = {
        #     "comments": comments_dict
        # }

        return JsonResponse(comments_dict)


    def post(self,request):
        print("data",request.data)  
        # Example: loop and save to DB (pseudo-code)
        pane_name = request.data['pane_name']  # e.g. "Model Overview"
        comments = request.data['comments']   # dict of sections

        for section, section_comments in comments.items():
                for comment_obj in section_comments:
                    for field, comment_text in comment_obj.items():
                        if comment_text.strip():
                            # Update if exists, else create
                            DashboardComments.objects.update_or_create(
                                uid=request.data['uid'],
                                pane=pane_name,
                                section=section,
                                field_name=field,
                                defaults={
                                    "comment": comment_text.strip(),
                                    "created_at":datetime.now()
                                }
                            )
                        print("Saving:", pane_name, section, field, comment_text)

        return JsonResponse({"success": True})

ValidationFindings

class upload_findings(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        excel_field = request.data['excel_fields']
        exceldf_a = request.data['exceldf']
        print("df",exceldf_a)

        # exceldf = pd.DataFrame(exceldf_a)
        # for _, row in exceldf.iterrows():
        #         print("row",row)
        objects_insert = []
        for row in exceldf_a:
            def parse_date(date_str):
                return datetime.strptime(date_str, "%m/%d/%Y").date()

            # Look up ValidationCategory by name
            category_name = row.get("Validation Category")
            element_name=row.get("Validation Elements")
            print("category_name",category_name)
            category_obj = FindingsCategory.objects.get(category_text=category_name)
            print("category_obj",category_obj)
            print("element_name",element_name)
            val_element_obj = FindingValElements.objects.filter(element_text=row.get("Validation Elements")).first()
            print("validation element id",val_element_obj.element_aid)
            print("SUB validation element_text",row.get("Sub Validation Elements"))
            sub_val_element_obj = FindingValSubElements.objects.get(element_aid=val_element_obj.element_aid,element_text=row.get("Sub Validation Elements"))
            
            # if not val_element_obj:
            #     continue  # skip if element not found

            # if not category_obj:
            #     continue  # skip if element not found

            # if not sub_val_element_obj:
            #     continue  # skip if element not found

            obj = ValidationFindings(
                mdl_id=row.get("Model ID"),
                added_by=request.data['addedby'],
                # date=parse_date(row.get("Date")),
                validation_element=val_element_obj.element_aid,
                sub_validation_element=sub_val_element_obj.element_sub_aid,
                category=category_obj.category_aid,   
                risk=int(row.get("Severity")),
                risk_level=int(row.get("Level")),
                finding_description=row.get("Description"),
                # start_date=parse_date(row.get("Start Date")),
                # end_date=parse_date(row.get("End Date")),
            )
            print("obj",obj)
            objects_insert.append(obj)
            print("objects",(objects_insert))
            
        ValidationFindings.objects.bulk_create(objects_insert)

        return JsonResponse({
            "message": f"{len(objects_insert)} rows inserted successfully"
        })



class model_committee(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        print("data",request.data)
        if request.data:
            user_cat_obj = UserCategory.objects.filter(uc_is_depthead=1).values_list("uc_aid", flat=True)      
            print(user_cat_obj)
            user_obj = Users.objects.filter(uc_aid__in=user_cat_obj).values("u_aid","u_fname", "u_lname", "dept_aid")
            print("user_obj",user_obj)  

            dept_aids= [i["dept_aid"] for i in user_obj]

            dept_obj = dict(Department.objects.filter(dept_aid__in=dept_aids).values_list("dept_aid", "dept_label"))
            print("dept_obj",dept_obj)
            department_head = [
                {"u_aid":i["u_aid"] , "u_fname": i["u_fname"], "u_lname": i["u_lname"], "dept_label": dept_obj.get(i["dept_aid"])}
                for i in user_obj
            ]
            print("department_head",department_head)
            return JsonResponse(department_head,safe=False)
        else:
            print("else")
            mdl_gov_obj=ModelGovernanceCommittee.objects.all()
            selected_user_ids = list(mdl_gov_obj.values_list("user_id", flat=True)) if mdl_gov_obj else []
            print("selected_user_ids",selected_user_ids)
            return JsonResponse(selected_user_ids,safe=False)

    def post(self,request):
        print("data",request.data)
        members=request.data['members']
        for u_aid, choice in members.items():
            print("u_aid, choice",u_aid, choice)
            if choice == 'Yes':
                if not ModelGovernanceCommittee.objects.filter(user_id=u_aid).exists():
                    ModelGovernanceCommittee.objects.create(user_id=u_aid,
                                                        added_by=request.data['uid'],
                                                        added_on=datetime.now())
                    print("saved")
            elif choice == 'No':      
                if ModelGovernanceCommittee.objects.filter(user_id=u_aid).exists():
                    ModelGovernanceCommittee.objects.filter(user_id=u_aid).delete()                   
                

        return JsonResponse({"isvalid":"true"})



class perfMonitoring_email_send(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        print("data",request.data)
        metrictype=request.data['metrictype']
        print("metrictype",metrictype)
        if metrictype == "Warning" or metrictype == "Critical":
            ##mrm head
            mrm_head=objmaster.getMRMHead()
            print("mrm_head",mrm_head)
            mrm_mail_id=Users.objects.get(u_aid=mrm_head).u_email
            print("mrm_mail_id",mrm_mail_id)
            send_mrm_head_mail(mrm_mail_id)

            ##owner 
            relevanet_obj=MdlRelevantPersonnel.objects.filter(mdl_id=request.data['mdl_id'],u_type='Owner')
            print("relevanet_obj",relevanet_obj)
            for i in relevanet_obj:
                print("uid",i.u_id)
                user_email=Users.objects.get(u_aid=i.u_id).u_email
                print("user_email",user_email)
                send_owner_email(user_email)
                
        else:
            print("Normal")

        return JsonResponse({"isvalid":"true"})



from fpdf import FPDF
from django.http import HttpResponse
from django.conf import settings
from django.forms.models import model_to_dict

class pdf_request(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        print("data",request.data)
        req_data_obj = ModelChangeReqData.objects.get(request_id=request.data['req_id'])
        request_data = model_to_dict(req_data_obj)  
        print("req_data_obj",request_data)

        ##Initiator
        request_initiator=request_data.get('request_initiator')
        print("request_initiator",request_initiator)
        user_obj=Users.objects.get(u_aid=int(request_initiator))
        request_initiator_first_last = f"{user_obj.u_fname} {user_obj.u_lname}"
        print("request_initiator_first_last",request_initiator_first_last)

        ##Owner
        mdl_owner=request_data.get('mdl_owner')
        print("mdl_owner",type(mdl_owner))
        ids = [int(x) for x in mdl_owner.split(",")]
        print(ids)
        owner_list=list()
        for i in ids:
            try:
                user_obj = Users.objects.get(u_aid=i)
                owner_first_last=f"{user_obj.u_fname} {user_obj.u_lname}"
                owner_list.append(owner_first_last)
            except Users.DoesNotExist:
                print(f"Record with id {i} does not exist")

        print("owner_list",owner_list)

        ## Reviewers
        review_n_approval_reviewers=request_data.get('review_n_approval_reviewers')
        print("review_n_approval_reviewers",review_n_approval_reviewers)
        ids_reviews = [int(x) for x in review_n_approval_reviewers.split(",")]
        print(ids_reviews)
        
        reviews_list=list()
        for i in ids_reviews:
            try:
                user_obj = Users.objects.get(u_aid=i)
                reviews_first_last=f"{user_obj.u_fname} {user_obj.u_lname}"
                reviews_list.append(reviews_first_last)
            except Users.DoesNotExist:
                print(f"Record with id {i} does not exist")

        print("reviews_list",reviews_list)

        ##sign_off_by

        sign_off_by=request_data.get('sign_off_by')
        print("sign_off_by",sign_off_by)
        user_obj = Users.objects.get(u_aid=int(sign_off_by))
        sign_off_by_first_last=f"{user_obj.u_fname} {user_obj.u_lname}"
        print("sign_off_by_first_last",sign_off_by_first_last)

        ##update the data
        request_data['request_initiator'] = request_initiator_first_last
        request_data['mdl_owner']=" , ".join(owner_list)
        request_data['review_n_approval_reviewers']=" , ".join(reviews_list)
        request_data['sign_off_by']=sign_off_by_first_last
        # if request_initiator in request_data:
        #     print("ifffffff")
        #     request_data[request_initiator] = request_initiator_first_last
        print("request_initiator",request_data['request_initiator'])
        return JsonResponse(request_data)
        # return JsonResponse({"req_data_obj":req_data_obj})


class section_save_comment(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        print("fetch",request.data)

        data_comments = list(IcqSectionComments.objects.filter(section_id=request.data['section_id']).values('section_id','comments'))
        # data_discussion= list(IcqSectionDiscussion.objects.filter(section_id=request.data['section_id']).values('section_id','comments'))

        print("data_comments",data_comments)
        # print("data_discussion",data_discussion)

        return JsonResponse({
            "data_comments": data_comments,
        }, safe=False)

        


    def post(self,request):
        print("dataaa",request.data)
        rv_id=int(objmaster.getmaxICQId())
        print("rv_id",rv_id)
        obj = IcqSectionComments.objects.filter(section_id=request.data['section_aid'],review_id=rv_id).first()

        if obj:
            old_add_date = obj.adddate
            old_added_by = obj.addedby

            obj, created = IcqSectionComments.objects.update_or_create(
                section_id=request.data['section_aid'],
                defaults={
                    "section_id": request.data['section_aid'],
                    "comments":request.data['comment_text'],
                    "updatedby":request.data['addedby'],
                    "updatedate":datetime.now()
                },
            )

            # restore old values
            obj.adddate = old_add_date
            obj.addedby = old_added_by
            obj.save(update_fields=["adddate", "addedby"])

        else:
            obj, created = IcqSectionComments.objects.update_or_create(
                section_id=request.data['section_aid'],
                defaults={
                    "section_id": request.data['section_aid'],
                    "comments":request.data['comment_text'],
                    "addedby":request.data['addedby'],
                    "adddate":datetime.now(),
                    "review_id":objmaster.getmaxICQId(),
                }
            )
            
       
        
        return JsonResponse({"msg":"Section Comment saved successfully"})

class getsectionQtnResp(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        print("fetch",request.data) 
        try:        
            section_id = request.data['section_id']
            user_id = request.data['uid']

            return Response({"Qtns":objrmse.getsectionQtnResp(section_id,str(user_id))}, status=status.HTTP_200_OK)
        except Exception as e: 
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)
        

class section_save_discussion(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("dataaa",request.data)
        # objmaster.getmaxICQId()
        comment = IcqSectionDiscussion.objects.create(
                section_id=request.data['section_aid'],
                comments=request.data['comment_text'],
                addedby=request.data['addedby'],
                adddate=datetime.now(),
                review_id=objmaster.getmaxICQId(),
            )
        return JsonResponse({"msg":"Section Discussion saved successfully"})


class Task_Registration(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        id=request.data['uid']
        if id:
            print("id",id)
            ## one user data
            usr = Users.objects.get(u_aid=id)
            user_serializer = UserSerializer(usr)
            user_obj=user_serializer.data
            print("user_obj",user_obj)

            added_by = user_obj['u_aid']
            today_date=datetime.now()
            originator_name=user_obj['u_fname']  +" " + user_obj['u_lname']

            ## department obj
            tasksub = Department.objects.get(dept_aid=user_obj['dept_aid'])
            department_serializer = DepartmentSerializer(tasksub)
            department_obj = department_serializer.data
            print("department_obj",department_obj)
            ## all user
            usrmaster = Users.objects.all()
            all_user_serializer =  UserSerializer(usrmaster,many=True)
            users_obj=all_user_serializer.data
            print("users_obj",users_obj)
            
            ## user category
            usrmaster = UserCategory.objects.all()
            user_cat_serializer =  UserCategorySerializer(usrmaster,many=True)

            ## task function
            taskfunctionmaster = TaskFunctionMaster.objects.all()
            task_fun_serializer =  TaskFunctionMasterSerializer(taskfunctionmaster,many=True)

            ##task priority
            taskprioritymaster = TaskPriorityMaster.objects.all()
            task_priority_serializer =  TaskPriorityMasterSerializer(taskprioritymaster,many=True)

            ##task type
            tasktypemaster = TaskTypeMaster.objects.all()
            task_type_serializer =  TaskTypeMasterSerializer(tasktypemaster,many=True)

            ## task approval
            taskapprovalstatusmaster = TaskApprovalstatusMaster.objects.all()
            task_status_serializer =  TaskApprovalstatusMasterSerializer(taskapprovalstatusmaster,many=True)

            ## mdl overview
            modeloverview =  ModelOverview.objects.all()
            mdl_overview_serializer =  ModelOverviewSerializer(modeloverview,many=True)

            context={'added_by':added_by,'task_function_obj':task_fun_serializer.data,'task_priority_obj':task_priority_serializer.data,
                     'task_type_obj':task_type_serializer.data,'task_approval_master':task_status_serializer.data,
                     'originator_name':originator_name,'user_category_obj':user_cat_serializer.data,
             'department_obj':department_obj,'users_obj':users_obj,'mdl_overview_obj':mdl_overview_serializer.data}
            
            #  'assigned_to_arr':json.dumps(assigned_to),'approved_by':json.dumps(approved_by),
            #  'task_approver_thread_lst':json.dumps(task_approver_thread_lst),
            #  'task_assignee_thread_lst':json.dumps(task_assignee_thread_lst)}
            
            return Response(context, status=status.HTTP_200_OK)
            
    def post(self,request):
        print("Task_Registration")
        task_assignee_thread_lst=[]
        task_approver_thread_lst=[]
        adddate= datetime.now()

        task_id = request.data['task_id']
        department = request.data['department']
        originator = request.data['originator']
        task_function = request.data['task_function']
        registration_date = request.data['registration_date']
        task_type = request.data['task_type']
        sub_task_type = request.data['sub_task_type']
        priority = request.data['priority']
        end_date = request.data['end_date']
        completion_status = request.data['completion_status']
        approval_status = request.data['approval_status']
        task_Major_Ver = request.data['task_major_version']
        task_Minor_Ver = request.data['task_minor_version']
        added_by = request.data['addedby']
        today_date = adddate
        link_id = request.data['link_id']
        task_name = request.data['task_name']
        
        relevant_personnel=request.data['relevant_personnel']
        task_summery_check=request.data['task_summery_check']
        print("task_id",task_id)
        task_registration_obj=TaskRegistration(task_id=task_id,department=department,originator=originator,task_function=task_function,
                                               registration_date=registration_date,task_type=task_type,sub_task_type=sub_task_type,
                                               priority=priority,end_date=end_date,completion_status=completion_status,
                                               approval_status=approval_status,task_major_version=task_Major_Ver,
                                               task_minor_version=task_Minor_Ver,addedby=added_by,adddate=today_date,
                                               link_id=link_id,task_name=task_name
                                               )         
        
        task_registration_obj.save()

        if relevant_personnel == 'True':
            originator_relevant=request.data['originator_relevant']
            assigned_to=request.data['assigned_to']
            approved_by=request.data['approved_by']
            print('assigned_to',assigned_to)
            print('approved_by',approved_by)
            print('Relevant Personnel',relevant_personnel,originator_relevant,assigned_to,approved_by)
            if originator_relevant:
                relevant_personnel_obj=Task_Relevant_Personnel(u_type="Originator",u_id=added_by,
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
            task_summery=request.data['task_summery_comments']
            task_requirement=request.data['task_requirements_comments']
            # assignee_comments=request.data['task_assignee_comments']
            # approval=request_data['approval']
            # approver_comments=request.data['task_approver_comments']

            print("task_summery",task_summery)
            
            
            task_summery_obj=TaskSummery(task_summery=task_summery,task_requirement=task_requirement,
                                                     task_registration=task_registration_obj,addedby=added_by,adddate=today_date)
            task_summery_obj.save()

        print("saved")

        return Response(status=status.HTTP_200_OK)


class get_sub_task_type(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):

        task_type_aid=request.data['task_type_aid'] 
    
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
        
        return Response(sub_task_data)

class Sub_Category_MasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            print("id",id)
            sub_category = ModelSubCategory.objects.get(sub_category_aid=id)
            serializer = Sub_Cetegory_MasterSerializer(sub_category)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        sub_cat_master =  ModelSubCategory.objects.all()
        serializer =  Sub_Cetegory_MasterSerializer(sub_cat_master,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = Sub_Cetegory_MasterSerializer(data=request.data)
        print("request",request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Sub Category created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            print("request1",request.data)
            id=request.data['sub_category_aid']
            print("sub_category_aid",id)
            category_aid=request.data['category_aid']
            print("category_aid",category_aid)

            smp = ModelSubCategory.objects.get(sub_category_aid=id)
            print("request2",request.data)
        except ModelSubCategory.DoesNotExist:
            return Response({'msg':'Section does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = Sub_Cetegory_MasterSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Sub Category is Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)



class get_task_ID_data(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        task_id=request.data['id']

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

        context={'department':department,'originator':originator,'task_function_label':task_function_label,'reg_date':reg_date,
                         'task_type_label':task_type_label,'sub_task_type_label':sub_task_type_label,'task_priority_label':task_priority_label,
                         'end_date':end_date,'completion_status':completion_status,'task_summery':task_summery,'task_name':task_name,
                         'task_req':task_req,'task_approvalstatus_label':task_approvalstatus_label,'approval_status':approval_status,
                         'task_assignee':task_assignee,'approver_comments':approver_comments,'task_dict':task_dict,'task_name':task_name}

        return Response( context, status=status.HTTP_200_OK)



