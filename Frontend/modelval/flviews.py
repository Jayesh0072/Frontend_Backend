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
password = 'sqlAdm_18'
host = 'DESKTOP-NH98228\HCSPL18'
port = 1433
database = 'RMSE'
import environ
env = environ.Env()
# reading .env file
environ.Env.read_env()
# mongodb set up

 


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
collection_Chartimg=db['Chartimg']   

plot_dir='/static/media/'
plot_dir_view='static/media/'

def getAPIURL():
    api_url=os.environ['API_URL']
    return api_url

def getFLAPIURL():
    api_url=os.environ['FL_API_URL']
    return api_url

def getDistinct_Col_Val(request):
    api_url=getFLAPIURL()+"getDistinct_Col_Val/"       
    data_to_save={'colName':request.GET.get('colName','-'),
                  'activity_year':request.GET.get('activity_year','-'),
                  'Portfolio':'Mortgage',
                  'filterCol':request.GET.get('filterCol','-'),
                  'uid':request.session['uid']  , 
            'Dept':request.session['dept']} 
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
    return JsonResponse({'arrCols': api_data['distVals']})

def getDistinct_Col_Val_Map(request):
    api_url=getFLAPIURL()+"getDistinct_Col_Val_map/"       
    data_to_save={'colName':request.GET.get('colName','-'),
                  'activity_year':request.GET.get('activity_year','-'),
                  'Portfolio':'Mortgage',
            'Dept':request.session['dept']} 
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
    return JsonResponse({'arrCols': api_data['distVals']})

def updateCtrl_Class(request):
    try:
        colDataLst = request.GET['datalist']  
        selctedTab = request.GET['selctedTab']    
        json_colDataLst = json.loads(colDataLst) 
        api_url = getFLAPIURL()+'insert_Ctrl_Class_Criteria/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'datalist':json_colDataLst,
            'tabSelected':selctedTab, 
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json() 
        
        return JsonResponse({'istaken':api_data['istaken']})
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})
    
def get_AIR(request):
    try: 
        api_url = getFLAPIURL()+'get_AIR/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept']
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json() 
        
         
        return JsonResponse({'istaken':api_data['istaken'],'AIR':api_data['AIR'],'DOR':api_data['DOR'],'approved':api_data['approved'],'denied':api_data['denied'],'filterSelected':api_data['filterSelected']})
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})
    
def sqlqury(request):
    try:        
        
        api_url = getFLAPIURL()+'GET_FL_Data_Info/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year','2023'),
            'portfolio':'Mortgage',
            'dept':request.session['dept'],
            'utility':'Steering'
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()  
        return render(request, 'querybuilder_sql.html',{'columns':api_data['gridDttypes']})
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})
    
def query_filter_sql(request):
    # print("request only",request)
    request_data=request.GET.get('objectDataString',0)
    api_url = getFLAPIURL()+'GET_FL_Data_Filter_Cnt/' 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }       
    data_params={
        'filter_cndn':request_data , 
        'activity_year':request.GET.get('activity_year','2023'),
        'Portfolio':'Mortgage',
        'Dept':request.session['dept']
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data=response.json()  
    return JsonResponse({"isvalid":"true","all_count":api_data["all_count"],"filter_cnt":api_data["filter_cnt"]}) 

def query_filter_sql_map(request):
    # print("request only",request)
    request_data=request.GET.get('objectDataString',0)
    api_url = getFLAPIURL()+'GET_FL_Data_Filter_Cnt_Map/' 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }       
    data_params={
        'filter_cndn':request_data , 
        'activity_year':request.GET.get('activity_year','2023'),
        'Portfolio':'Mortgage',
        'Dept':request.session['dept']
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data=response.json()  
    return JsonResponse({"isvalid":"true","all_count":api_data["all_count"],"filter_cnt":api_data["filter_cnt"]}) 

def save_filter_sql(request):
    # print("request only",request)
    request_data=request.GET.get('objectDataString',0)
    utiltity=request.GET.get('utiltity','')
    api_url = getFLAPIURL()+'Save_FL_Data_Filter_Cndn/' 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }       
    data_params={
        'filter_cndn':request_data , 
        'uid':request.session['uid']  ,
        'activity_year':request.GET.get('activity_year','2023'),
        'portfolio':'Mortgage',
        'utiltity':utiltity,
        'dept':request.session['dept'],
        'segNm':request.GET.get('segNm',utiltity),
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data=response.json()  
    return JsonResponse({"isvalid":"true","is_taken":api_data["is_taken"],'filterSelected':api_data["filterSelected"]}) 

def fielddetails(request):
    try:
        third_party_api_url = getAPIURL()+'department/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        responseget = requests.get(third_party_api_url,headers=header)
        data=json.loads(responseget.content)
        print("department data",data)

        # third_party_api_url_a = getFLAPIURL()+'FieldAPI/'
        # header = {
        # "Content-Type":"application/json",
        # 'Authorization': 'Token '+request.session['accessToken']
        # }
        # responseget_dbfield = requests.get(third_party_api_url_a,data = json.dumps(data_to_get),headers=header)
        # data_A=json.loads(responseget_dbfield.content)
        # print("dbfield data",data_A)
        return render(request, 'field_details.html',{'department':data})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())


def saveexcelfields(request):
    print("request data databse field",request.GET)
    try: 
        datalist = json.loads(request.GET['datalist'])
        print("datalist",datalist)
        department = request.GET['department']
        print("department",department)
        portfolio = request.GET['portfolio']
        api_url=getFLAPIURL()+"FieldAPI/"  
        for i in datalist: 
            print("i",i)
            print("excel field",i['Excel_Field'])    
            data_to_update={ 
                'department': department,
                'field_aid':int(i['Field_AID']),
                'Excel_Field':i['Excel_Field'],
                'portfolio':portfolio,
                'added_by':request.session['uid']
            } 
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.put(api_url, data= json.dumps(data_to_update),headers=header)
            print("response---------",json.loads(response.content))
        data = json.loads(response.content)
        return JsonResponse({'istaken':'true','msg':data['msg']})
    except Exception as e:
        print('assignValidation ',e)
        print('assignValidation traceback is ', traceback.print_exc()) 
        return JsonResponse({'istaken':'false'})

def fetchfielddata(request):
    department = request.GET.get('department', 'False')
    portfolio = request.GET.get('portfolio','False')
    try:
        third_party_api_url_a = getFLAPIURL()+'FieldAPI/'
        print('third_party_api_url_a ',third_party_api_url_a)
        data_to_get={ 
            'department': department,
            'portfolio':portfolio,
        } 

        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        print('third_party_api_url_a ',third_party_api_url_a)
        responseget_dbfield = requests.get(third_party_api_url_a,data= json.dumps(data_to_get),headers=header)
        data_A=json.loads(responseget_dbfield.content)
        print("dbfield data",data_A)

        return JsonResponse({'database_field':data_A})
    except Exception as e:
        print("error is ",e)
        return JsonResponse({'error':e})

def getSteering_Dashb(request):
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
        'dept':str(request.session['dept']),
        'utility':'Steering'
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data=response.json()  
    return render(request, 'dashboard_fl_steering_indvl.html',{'arrCols':arrCols,'ctrl_cols':ctrl_class_data['ColumnName'],'filterSelected':api_data['filterSelected'],'querybldrcols':api_data['gridDttypes'],'peerlei':api_data['peerlei']})

def get_Steering_Dashb_Data(request):
    try: 
        api_url = getFLAPIURL()+'get_Steering_Dashb_Data/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept']
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'istaken':api_data['istaken'],'denied':[],'peergroupapps':api_data['peergroupapps'],'apps':api_data['apps'],'peergroupappsGov':api_data['peergroupappsGov'],'appsGov':api_data['appsGov']})
    except Exception as e:
        print('updateaccess ',e,traceback.print_exc())
        return JsonResponse({'istaken':'false'})
    
def get_Steering_Dashb_Data_apps(request):
    try: 
        api_url = getFLAPIURL()+'get_Steering_Dashb_Data_apps/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept']
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'istaken':api_data['istaken'], 'apps':api_data['apps'],'filterSelected':api_data['filterSelected'] })
    except Exception as e:
        print('updateaccess ',e,traceback.print_exc())
        return JsonResponse({'istaken':'false'})
  
def get_Steering_Dashb_Data_peergroupapps(request):
    try: 
        api_url = getFLAPIURL()+'get_Steering_Dashb_Data_peergroupapps/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept']
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'istaken':api_data['istaken'], 'peergroupapps':api_data['peergroupapps'] })
    except Exception as e:
        print('updateaccess ',e,traceback.print_exc())
        return JsonResponse({'istaken':'false'})
  
def get_Steering_Dashb_Data_appsGov(request):
    try: 
        api_url = getFLAPIURL()+'get_Steering_Dashb_Data_appsGov/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept']
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'istaken':api_data['istaken'], 'appsGov':api_data['appsGov'] })
    except Exception as e:
        print('updateaccess ',e,traceback.print_exc())
        return JsonResponse({'istaken':'false'})
  
def get_Steering_Dashb_Data_peergroupappsGov(request):
    try: 
        api_url = getFLAPIURL()+'get_Steering_Dashb_Data_peergroupappsGov/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept']
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'istaken':api_data['istaken'], 'peergroupappsGov':api_data['peergroupappsGov'] })
    except Exception as e:
        print('updateaccess ',e,traceback.print_exc())
        return JsonResponse({'istaken':'false'})
  
def updatePeerGroup(request):
    try:
        selctedTab = request.GET['selctedTab']  
        print('selctedTab ',selctedTab)
        peergroups = request.GET.getlist('peergroups[]')
        print('peergroups ',peergroups)
        peergroups=','.join(peergroups)
        print('peergroups 2 ',peergroups)
        
        api_url = getFLAPIURL()+'updatePeerGroups/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'tabSelected':selctedTab,
            'peergroups':peergroups
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json() 
        
        return JsonResponse({'istaken':api_data['istaken']})
    except Exception as e:
        print('updateaccess ',e,traceback.print_exc())
        return JsonResponse({'istaken':'false'})
    
def getMarketing_Dashb(request):
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
        'dept':str(request.session['dept']),
        'utility':'Marketing'
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data=response.json()  
    is_DA=request.GET.get('DA','block')
    if(is_DA =='false'):
        is_DA='none'

    return render(request, 'dashboard_fl_marketing.html',{'is_DA':is_DA,'arrCols':arrCols,'ctrl_cols':ctrl_class_data['ColumnName'],'filterSelected':api_data['filterSelected'],'querybldrcols':api_data['gridDttypes'],'peerlei':api_data['peerlei']})


def get_Marketing_Dashb_Data_apps(request):
    try: 
        api_url = getFLAPIURL()+'get_Marketing_Dashb_Data_apps/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept']
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'istaken':api_data['istaken'], 'apps':api_data['apps'],'filterSelected':api_data['filterSelected'] })
    except Exception as e:
        print('updateaccess ',e,traceback.print_exc())
        return JsonResponse({'istaken':'false'})
  
def get_Marketing_Dashb_Data_apps_IncomeGrp(request):
    try: 
        api_url = getFLAPIURL()+'get_Marketing_Dashb_Data_IncomeGrp/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'] 
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()         
        return JsonResponse({'istaken':api_data['istaken'], 'apps':api_data['apps'],'peergroupapps':api_data['peergroupapps'] })
    except Exception as e:
        print('updateaccess ',e,traceback.print_exc())
        return JsonResponse({'istaken':'false'})
    
def get_Marketing_Dashb_Data_peergroupapps(request):
    try: 
        api_url = getFLAPIURL()+'get_Marketing_Dashb_Data_peergroupapps/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept']
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'istaken':api_data['istaken'], 'peergroupapps':api_data['peergroupapps'] })
    except Exception as e:
        print('updateaccess ',e,traceback.print_exc())
        return JsonResponse({'istaken':'false'})
  
def Get_Utility(request):
    try: 
        utility =request.GET.get('utility', '')  
        prefix = list(utility)[0]

        api_url=getFLAPIURL()+"GetUtilityAPI/"       
        data_to_get={ 
            'utility':utility
            } 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_get),headers=header)
        api_data=response.json() 
        return render(request,'utility.html',{'data':api_data['data'],'prefix':prefix,'title':'Risk Factor','utility':utility,'department':json.loads(response.content)})
         
    except Exception as e:
        print('QtnsResp is ',e)
        print('QtnsResp traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})
        

def saveriskcomments(request): 
    comment =request.GET.get('comment', 'False') 
    risk_label =request.GET.get('risk_label', 'False') 
    risk_id =request.GET.get('risk_id', 'False') 
    utility = request.GET.get('utility', 'False')
    
    api_url=getFLAPIURL()+"saveriskcomments/"       
    data_to_save={ 
        'uid':request.session['uid'],
        'comments':comment,
        'risk_id':risk_id,
        'utility':"Pricing",
        'department':request.session['dept'],
        'added_by':request.session['uid']
    } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)         
    api_data=response.json() 
    return JsonResponse({"data":api_data})
 
def getriskfactorhistorymsg(request):
    try: 
        utility = request.GET.get('utility', 'False')  
        portfolio = request.GET.get('portfolio','False')
        risk_aid = request.GET.get('risk_aid','False')
        department= 'MRMedited'
        third_party_api_url = getFLAPIURL()+'GetRiskFactorHistoryMsg/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'risk_id':risk_aid,
            'group_id':department+"_"+portfolio+"_"+utility,
            'addedby':request.session['uid']
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        data=responseget.json()
        print("responseget history data--------------------------",data)    
        
        # return JsonResponse({'data':data['data'],'mmdata':data['mmdata'],'mo_approved':data['mo_approved']})
        return JsonResponse({'data':data['data'],'riskLbl':data['riskLbl']})

    except requests.exceptions.RequestException as e:
        print("error is",e)
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def addgetriskfactorhistorymsg(request):
    try: 
        risk_id = request.GET.get('risk_id','False') 
        group_id = request.GET.get('group_id', 'False') 
        utility = request.GET.get('utility', 'False') 
        portfolio = request.GET.get('portfolio','False')
        comments = request.GET.get('comment','False')

        third_party_api_url = getFLAPIURL()+'GetRiskFactorHistoryMsg/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_save = {
            'risk_id':risk_id,
            'group_id':group_id,
            'utility':utility,
            'department':request.session['dept'],
            'portfolio':portfolio,
            'added_by':request.session['uid'],
            'comments':comments
        }
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
        data=responseget.json() ,
        return JsonResponse({'data':data['data']})
    except Exception as e:
        print("error is",e)


def getPricing_Dashb(request):
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
        'dept':str(request.session['dept']),
        'utility':'Pricing'
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data=response.json()  
    return render(request, 'dashboard_fl_pricing.html',{'arrCols':arrCols,'ctrl_cols':ctrl_class_data['ColumnName'],'filterSelected':api_data['filterSelected'],'querybldrcols':api_data['gridDttypes'],'peerlei':api_data['peerlei']})

def get_Pricing_Dashb_Data_apps(request):
    try: 
        api_url = getFLAPIURL()+'get_Pricing_Dashb_Data_apps/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'ratespread':request.GET.get('ratespread',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept']
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'istaken':api_data['istaken'], 'apps':api_data['apps'],'filterSelected':api_data['filterSelected'] })
    except Exception as e:
        print('updateaccess ',e,traceback.print_exc())
        return JsonResponse({'istaken':'false'})
  
def get_Pricing_Dashb_Data_ratespread(request):
    try: 
        api_url = getFLAPIURL()+'get_Pricing_Dashb_Data_ratespread/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'ratespread':request.GET.get('ratespread',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept']
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'istaken':api_data['istaken'], 'apps':api_data['apps'] , 'denomCtrlCls':api_data['denomCtrlCls']  })
    except Exception as e:
        print('updateaccess ',e,traceback.print_exc())
        return JsonResponse({'istaken':'false'})


def addFL_question(request):
    try:
        
        return render(request, 'addFL_question.html',{'sections':objmaster.getFLSections()})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def FL_addSection(request):
    try:   
        sect_type=request.GET.get('stype', 'False') 
        section =request.GET.get('section', 'False') 
        sectiondesc =request.GET.get('sectiondesc', 'False') 
        activests =request.GET.get('activests', 'False')      
        sect_obj=FlSections.objects.create(section_type=sect_type,section_label=section,activestatus=activests,
                                           section_description=sectiondesc,addedby=request.session['uid'],adddate=date.today())
        # objmaster.addSection(section,sectiondesc,activests,str(request.session['uid']))
        return JsonResponse({'is_taken':True})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc())        

def FL_addSub_Section(request):
    try:  
        sect_type=request.GET.get('stype', 'False') 
        section =request.GET.get('section', 'False') 
        sectiondesc =request.GET.get('sectiondesc', 'False') 
        activests =request.GET.get('activests', 'False')     
        secid =request.GET.get('secid', 'False')      
        sect_obj=FlSubSections.objects.create(section_aid=secid,sub_section_type=sect_type,sub_section_label=section,activestatus=activests,
                                           sub_section_description=sectiondesc,addedby=request.session['uid'],adddate=date.today())
        

        # objmaster.addSub_Section(secid,section,sectiondesc,activests,str(request.session['uid']))
        return JsonResponse({'is_taken':True})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc())

  

def FL_addSub_Sub_Section(request):
    try:  
        sect_type=request.GET.get('stype', 'False') 
        section =request.GET.get('section', 'False') 
        sectiondesc =request.GET.get('sectiondesc', 'False') 
        activests =request.GET.get('activests', 'False')    
        sub_secid =request.GET.get('sub_secid', 'False')      

        sect_obj=FlSubSubSections.objects.create(sub_section_aid=sub_secid,sub_sub_section_type=sect_type,sub_sub_section_label=section,activestatus=activests,
                                           sub_sub_section_description=sectiondesc,addedby=request.session['uid'],adddate=date.today())
        # objmaster.addSub_Sub_Section(sub_secid,section,sectiondesc,activests,str(request.session['uid']))
        return JsonResponse({'is_taken':True})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 

def FL_getSub_Sections(request):
    try:       
        sub_secid =request.GET.get('secid', 'False')      
        
        return JsonResponse({'subsections':objmaster.FL_getSub_Sections(sub_secid)})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc())  



def FL_add_question(request):
    try:
        sect_type=request.GET.get('stype', 'False') 
        added_by=request.session['uid'] 
        section=request.GET.get('section','False')
        sub_section=request.GET.get('sub_section','False')
        # sub_sub_section=request.GET.get('sub_sub_section','False')
        # sub_sub_sub_section=request.GET.get('sub_sub_sub_section','False')
        question=request.GET.get('question','False')
        print("all data",sect_type,section,sub_section,question)
        api_url=getFLAPIURL()+"FL_add_question/"       
        params={'section':section,
            'sub_section':sub_section,
            'uid':added_by,
            # 'sub_sub_section':sub_sub_section,
            # 'sub_sub_sub_section':sub_sub_sub_section,
            'question':question,
            'sect_type':sect_type
            } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(params),headers=header)         
        api_data=response.json()
        print("api_data",api_data)
       
        return JsonResponse({'is_taken':api_data['is_taken']})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc())      


def FLQuestions(request):
    try: 
        
        return render(request, 'FLQuestions.html',{ 'Qtns':objmaster.getAllFLQtns()})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def fl_ratings(request):
    print("fl_ratings",fl_ratings)
    try:
        return render(request,'fl_ratings.html',{'sections':objmaster.getFLSections(),'Qtns':objmaster.getAllFLQtnsAndRatings()})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc())  



def fl_save_ratings(request):
    try:
        from datetime import datetime
        added_by=request.session['uid']
        adddate=datetime.now()
        question_id=request.GET.get('question_id')
        ratings_yes=request.GET.get('ratings_yes')
        ratings_no=request.GET.get('rating_no')
        doc_na=request.GET.get('doc_na')
        # doc_no=request.GET.get('doc_no')
        print("question_id is",question_id)
        if ratings_yes == '':
            ratings_yes="null"
        if ratings_no == '':
            ratings_no ="null"
        if doc_na == '':
            doc_na ="null"  
        objmaster.fl_insertRatings(question_id,ratings_yes,ratings_no,doc_na)
        print('saved')
        return JsonResponse({'is_taken':True})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 

def allocate_fl(request): 
    try:
        third_party_api_url = getFLAPIURL()+'Fl_sectionsAPI/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        responseget = requests.get(third_party_api_url,headers=header)
        print("--------------response section",json.loads(responseget.content)['data'])

        third_party_api_url_user = getFLAPIURL()+'UsersgetAPI/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        responseget_user = requests.get(third_party_api_url_user,headers=header)
        print("--------------response user",json.loads(responseget_user.content)['data'])

        return render(request,'allocate_fl.html',{'sections':json.loads(responseget.content)['data'],'user':json.loads(responseget_user.content)['data'],'review':''})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 

def save_flallocation(request):
    request_data = {x:request.GET.get(x) for x in request.GET.keys()}
    section_aid = request.GET.getlist('section_aid[]')
    users = request.GET.getlist('users[]')
    api_url=getFLAPIURL()+"save_flallocation/"       
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
    print("api data------------",api_data)
    return JsonResponse({"isvalid":api_data['isvalid']})

 
def getFLSecQtn(request):
    try: 
        # sectionid =request.GET.get('ddlSection', '0')  
        sectionid = request.session['uid']
        return JsonResponse({'sections':objmaster.getFLQtns(sectionid)})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def getRedlining_Dashb(request):
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
        'dept':request.session['dept'],
        'utility':'Redlining'
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data=response.json()   
    return render(request, 'dashboard_fl_redlining.html',{'arrCols':arrCols,'ctrl_cols':ctrl_class_data['ColumnName'],'querybldrcols':api_data['gridDttypes']})

def OnMap(request):
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
        'dept':request.session['dept'],
        'utility':'Steering'
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data=response.json()  
    print('api_data ',api_data)
    return render(request, 'fl_map.html',{'arrCols':arrCols,'ctrl_cols':ctrl_class_data['ColumnName'],'querybldrcols':api_data['gridDttypes']})

def get_State_Lat_long(request):
    try: 
        api_url = getFLAPIURL()+'get_State_Lat_long/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'peer':request.GET.get('peer','') 
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'StateLatLong':api_data['StateLatLong'],'BankBranches':api_data['BankBranches']})
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})

def get_County_Lat_long(request):
    try: 
        api_url = getFLAPIURL()+'get_County_Lat_long/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'State':request.GET.get('State',''),
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'peer':request.GET.get('peer','')         
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'CountyLatLong':api_data['CountyLatLong'],'BankBranches':api_data['BankBranches']})
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})

def get_Filter_State_Lat_long(request):
    try: 
        api_url = getFLAPIURL()+'get_Filter_State_Lat_long/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'peer':request.GET.get('peer',''),
            'filter_col':request.GET.get('filter_col','')    
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'FilterStateLatLong':api_data['FilterStateLatLong'],'BankBranches':api_data['BankBranches']})
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})

def get_Filter_County_Lat_long(request):
    try: 
        api_url = getFLAPIURL()+'get_Filter_County_Lat_long/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'State':request.GET.get('State',''),
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'peer':request.GET.get('peer',''),
            'filter_col':request.GET.get('filter_col','')            
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
        #print('get_Filter_County_Lat_lon api_data ',api_data)
        return JsonResponse({'FilterCountyLatLong':api_data['FilterCountyLatLong'],'BankBranches':api_data['BankBranches']})
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})

def showFLSetting(request):
    try: 
        third_party_api_url = getFLAPIURL()+'FLSettingAPI/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        responseget = requests.get(third_party_api_url,headers=header)
        data=responseget.json()
        print("responseget FL setting data--------------------------",data)
        return render(request, 'FLSettingLst.html',{ 'actPage':'Departments','data':data})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def newFLSetting(request):
    try:   
        print('inside addFLSetting')
        return render(request, 'addFLSetting.html')
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

from datetime import datetime

def addFLSetting(request):
    try: 
        flnameVal=request.GET['flname']  
        remarksVal=request.GET['remarks']  
        enddateVal=request.GET['enddate']
        date = datetime.strptime(enddateVal, '%d/%m/%Y').date()
        userid=str(request.session['uid'])

        third_party_api_url = getFLAPIURL()+'FLSettingAPI/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_save = {
            'fls_text':flnameVal,
            'fls_remarks':remarksVal,
            'fls_enddate':date.strftime('%Y-%m-%d') ,
            'addedby':userid
        }
        responseget = requests.post(third_party_api_url,data= json.dumps(data_to_save),headers=header)
        data=responseget.json()
        print("responseget FL setting data save--------------------------",data)
        
        return JsonResponse({"isvalid":"true","data":data})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})

def FLeanding(request):
    try:
        mdlLst= []
        segLst=[]
        if len(mdlLst)>0:              
            segLst=objvalidation.getVTModelsSegments(mdlLst['0']['Mdl_Id'])  
        generateReport_utility(request)
        return render(request, 'FLeanding.html',{'mdlLst':mdlLst,'segLst':segLst})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 


def getMatchedPair_Dashb(request):
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
        'dept':request.session['dept'],
        'utility':'MatchedPair'
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data=response.json()
    api_url = getFLAPIURL()+'get_DeniedRecordsMatchedPair/' 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }       
    data_params={
        'uid':request.session['uid']  , 
        'activity_year':request.GET.get('activity_year','2023'),
        'portfolio':'Mortgage',
        'dept':request.session['dept']
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data_denied=response.json()      
    print('approved records ',api_data_denied['approvedData'])
    return render(request, 'dashboard_fl_matchedpair.html',{'gridData':api_data_denied['gridData'],'approvedData':api_data_denied['approvedData'],'colListApproved':api_data_denied['colListApproved'],'arrCols':arrCols,'ctrl_cols':ctrl_class_data['ColumnName'],'querybldrcols':api_data['gridDttypes']})

def getMatchedPairs(request):
    try: 
        selectedId=request.GET['selectedId']    

        third_party_api_url = getFLAPIURL()+'Get_Similar_Records/' #'Get_MatchedPairs_Data/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_save = {
             'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year','2023'),
            'portfolio':'Mortgage',
            'dept':request.session['dept'],
            'selectedId':request.GET.get('selectedId',''),
            'colselection':request.GET.getlist('colselection[]',''),
            'WeightageVals':request.GET.getlist('WeightageVals[]',''),
            'sumWeg':request.GET.get('sumWeg',''),
            'offset':request.GET.get('offset',''),
            'tab':request.GET.get('tab',''),
        }
        
        responseget = requests.post(third_party_api_url,data= json.dumps(data_to_save),headers=header)
        data=responseget.json() 
        
        return JsonResponse({"isvalid":"true","data":data['gridData']})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})

def OnMapBanks(request):
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
        'dept':request.session['dept'],
        'utility':'Steering'
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data=response.json()  
    print('api_data ',api_data)
    return render(request, 'fl_map_bankbranches.html',{'arrCols':arrCols,'ctrl_cols':ctrl_class_data['ColumnName'],'querybldrcols':api_data['gridDttypes']})

def get_Bank_lat_long_state(request):
    try: 
        api_url = getFLAPIURL()+'get_Bank_lat_long_state/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'peer':request.GET.get('peer',''),
            'filter_col':request.GET.get('filter_col','')  
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'StateLatLong':api_data['StateLatLong'],'BankBranches':api_data['BankBranches'],'PeerBankBranches':api_data['PeerBankBranches']})
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})

def get_Bank_lat_long_county(request):
    try: 
        api_url = getFLAPIURL()+'get_Bank_lat_long_county/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'State':request.GET.get('State',''),
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'peer':request.GET.get('peer',''),
            'filter_col': request.GET.get('filter_col','')      
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'CountyLatLong':api_data['CountyLatLong'],'BankBranches':api_data['BankBranches'],'PeerBankBranches':api_data['PeerBankBranches']})
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})

def FLQtnsFinal(request):
    try: 
        sectionid =request.POST.get('ddlSection', '0') 
        api_url=getFLAPIURL()+"FLQtnsFinal/"       
         
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url,headers=header)
         
        api_data=response.json()
        print("api_data",api_data)

        api_url_a=getFLAPIURL()+"InherentRiskRatingAPI/"       
         
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response_a = requests.get(api_url_a,headers=header)
         
        api_data_a=response_a.json()
        print("api_data ratings-----------------",api_data_a)
        r1 = [i['ratings'] for i in api_data_a['rating_1']]
        print("r1",r1)
        r2 = [i['ratings'] for i in api_data_a['rating_2']]
        print("r2",r2)
        r3 = [i['ratings'] for i in api_data_a['rating_3']]
        print("r3",r3)
        
        return render(request, 'FLQtnsFinal.html',
                      {'FLRating':api_data['FLRating'],
                       'sectionid':sectionid,
                       'sections':api_data['sections'],'Qtns':api_data['Qtns'],'rating_1':r1,'rating_2':r2,
                                               'rating_3':r3})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def saveFLRatingsFinal(request):
    try:       
  
        colDataLst = request.POST['colDataLst']
        print("colDataLst-------",colDataLst)
        uid=request.session['uid']
        api_url=getFLAPIURL()+"saveFLRatingsFinal/"       
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
        print("api_data new-----------",api_data)   
        return JsonResponse({'is_taken':api_data['is_taken']})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())


def publishFL(request):
    try:
        # objmaster.publishICQ()
        api_url=getFLAPIURL()+"publishFL/"       
        
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }  
        response = requests.get(api_url,headers=header)
        
        api_data=response.json()
        print("Apii daata",api_data)
        return JsonResponse({"is_taken":"true"})
    except Exception as e:
        print('publushICQ is ',e)
        print('publushICQ traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})

def getFLSecQtnFinal(request):
    try:  
        api_url=getFLAPIURL()+"getFLSecQtnFinal/"       
         
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

 
def getUnderwriting_Dashb_Varwise(request):
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
        'dept':request.session['dept'],
        'utility':'Underwriting'
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data=response.json()   
    return render(request, 'dashboard_fl_underwriting_Varwise.html',{'arrCols':arrCols,'ctrl_cols':ctrl_class_data['ColumnName'],'querybldrcols':api_data['gridDttypes'],'filterSelected':api_data['filterSelected']})

def get_AIR_Varwise(request):
    try: 
        api_url = getFLAPIURL()+'get_AIR_Varwise/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'ClassVar':request.GET.get('prohb_cls',''),
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json() 
        
         
        return JsonResponse({'istaken':api_data['istaken'],'AIR':api_data['AIR'],'DOR':api_data['DOR'],'approved':api_data['approved'],'denied':api_data['denied'],'filterSelected':api_data['filterSelected']})
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})
    
def getPricing_Dashb_Varwise(request):
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
        'dept':str(request.session['dept']),
        'utility':'Pricing'
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data=response.json()  
    return render(request, 'dashboard_fl_pricing_Varwise.html',{'arrCols':arrCols,'ctrl_cols':ctrl_class_data['ColumnName'],'filterSelected':api_data['filterSelected'],'querybldrcols':api_data['gridDttypes'],'peerlei':api_data['peerlei']})

def get_Pricing_Dashb_Data_apps_Varwise(request):
    try: 
        api_url = getFLAPIURL()+'get_Pricing_Dashb_Data_apps_Varwise/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'ratespread':request.GET.get('ratespread',''),
            'Portfolio':'Mortgage',
            'ClassVar':request.GET.get('prohb_cls',''),
            'Dept':request.session['dept']
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'istaken':api_data['istaken'], 'apps':api_data['apps'],'filterSelected':api_data['filterSelected'] })
    except Exception as e:
        print('updateaccess ',e,traceback.print_exc())
        return JsonResponse({'istaken':'false'})
  
def get_Pricing_Dashb_Data_ratespread_Varwise(request):
    try: 
        api_url = getFLAPIURL()+'get_Pricing_Dashb_Data_ratespread_Varwise/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'ratespread':request.GET.get('ratespread',''),
            'Portfolio':'Mortgage',
            'ClassVar':request.GET.get('prohb_cls',''),
            'Dept':request.session['dept']
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'istaken':api_data['istaken'], 'apps':api_data['apps'] , 'denomCtrlCls':api_data['denomCtrlCls']  })
    except Exception as e:
        print('updateaccess ',e,traceback.print_exc())
        return JsonResponse({'istaken':'false'})

def getSteering_Dashb_Varwise(request):
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
        'dept':str(request.session['dept']),
        'utility':'Steering'
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data=response.json()  
    return render(request, 'dashboard_fl_steering_Varwise.html',{'arrCols':arrCols,'ctrl_cols':ctrl_class_data['ColumnName'],'filterSelected':api_data['filterSelected'],'querybldrcols':api_data['gridDttypes'],'peerlei':api_data['peerlei']})

def get_Steering_Dashb_Data_Varwise(request):
    try: 
        api_url = getFLAPIURL()+'get_Steering_Dashb_Data_apps_Varwise/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'ClassVar':request.GET.get('prohb_cls',''),
            'Dept':request.session['dept']
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'istaken':api_data['istaken'],'denied':[],'peergroupapps':api_data['peergroupapps'],'apps':api_data['apps'],'peergroupappsGov':api_data['peergroupappsGov'],'appsGov':api_data['appsGov']})
    except Exception as e:
        print('updateaccess ',e,traceback.print_exc())
        return JsonResponse({'istaken':'false'})
    

def getMatchedPair_Dashb_Varwise(request):
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
        'dept':request.session['dept'],
        'utility':'MatchedPair'
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data=response.json()
    api_url = getFLAPIURL()+'get_DeniedRecordsMatchedPair/' 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }       
    data_params={
        'uid':request.session['uid']  , 
        'activity_year':request.GET.get('activity_year','2023'),
        'portfolio':'Mortgage',
        'dept':request.session['dept']
    }

    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data_denied=response.json()   
    
    
    colCompare=['state_code','county_code','census_tract','derived_loan_product_type','derived_dwelling_category','purchaser_type','preapproval','loan_type','loan_purpose','lien_status','reverse_mortgage','open-end_line_of_credit','business_or_commercial_purpose','loan_amount','combined_loan_to_value_ratio','interest_rate','rate_spread','hoepa_status','total_loan_costs','total_points_and_fees','origination_charges','discount_points','lender_credits','loan_term','prepayment_penalty_term','intro_rate_period' 
,'negative_amortization','interest_only_payment','balloon_payment','other_nonamortizing_features','property_value','construction_method','occupancy_type','manufactured_home_secured_property_type','manufactured_home_land_property_interest','total_units','multifamily_affordable_units','income','debt_to_income_ratio','submission_of_application','initially_payable_to_institution', 
'tract_population','tract_minority_population_percent','ffiec_msa_md_median_family_income','tract_to_msa_income_percentage','tract_owner_occupied_units','tract_one_to_four_family_homes','tract_median_age_of_housing_units']
    return render(request, 'dashboard_fl_matchedpair_Varwise_LL.html',
                  {'colCompare':colCompare,'colList':api_data_denied['colList'],'gridData':api_data_denied['gridData'],
                   'filterSelected':api_data_denied['filterSelected'], 'arrCols':arrCols,'ctrl_cols':ctrl_class_data['ColumnName'],
                   'querybldrcols':api_data['gridDttypes'],'approvedData':api_data_denied['approvedData'],'colListApproved':api_data_denied['colListApproved']}) 

def getMatchedPairs_Varwise(request):
    try:   
        third_party_api_url = getFLAPIURL()+'Get_MatchedPairs_Data/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        } 
        data_to_save = {
           
             'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year','2023'),
            'portfolio':'Mortgage',
            'dept':request.session['dept'],
            'selectedId':request.GET.get('selectedId','')
        } 
        # responseget = requests.post(third_party_api_url,data= json.dumps(data_to_save),headers=header)
        # data=responseget.json() 
        data=[]
        return JsonResponse({"isvalid":"true","data":data['gridData']})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})


def getMarketing_Dashb_Varwise(request):
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
        'dept':str(request.session['dept']),
        'utility':'Marketing'
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data=response.json()  
    print("api_data",api_data)
    is_DA=request.GET.get('DA','block')
    if(is_DA =='false'):
        is_DA='none'

    return render(request, 'dashboard_fl_marketing_Varwise.html',{'is_DA':is_DA,'arrCols':arrCols,'ctrl_cols':ctrl_class_data['ColumnName'],'filterSelected':api_data['filterSelected'],'querybldrcols':api_data['gridDttypes'],'peerlei':api_data['peerlei']})



def get_Marketing_Dashb_Data_apps_Varwise(request):
    try: 
        api_url = getFLAPIURL()+'get_Marketing_Dashb_Data_ClassWise/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'ClassVar':request.GET.get('prohb_cls',''),
            'segNm':request.GET.get('segNm',''),
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()         
        return JsonResponse({'istaken':api_data['istaken'], 'apps':api_data['apps'],'peergroupapps':api_data['peergroupapps'] })
    except Exception as e:
        print('updateaccess ',e,traceback.print_exc())
        return JsonResponse({'istaken':'false'})
  

def getMatchedPairs_Denials(request):
    try:  
        third_party_api_url = getFLAPIURL()+'get_Denials_Varwise/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_save = {
             'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year','2023'),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'ClassVar':request.GET.get('prohb_cls',''),
        }
        responseget = requests.post(third_party_api_url,data= json.dumps(data_to_save),headers=header)
        data=responseget.json() 
        
        return JsonResponse({"isvalid":"true","data":data['apps']})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})


def get_DeniedRecordsMatchedPair(request):
    try:
        api_url = getFLAPIURL()+'get_DeniedRecordsMatchedPair/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year','2023'),
            'portfolio':'Mortgage',
            'dept':request.session['dept']
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data_denied=response.json()  
        return JsonResponse({'gridData':api_data_denied['gridData'],'filterSelected':api_data_denied['filterSelected']})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})


def BranchAnalysis(request):
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

    return render(request, 'fl_map_combined.html',{'arrCols':arrCols,'ctrl_cols':ctrl_class_data['ColumnName'],'querybldrcols':api_data['gridDttypes']})

def get_CountyMedianIncome(request):
    try: 
        api_url = getFLAPIURL()+'get_CountyMedianIncome/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept']
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'CountyLatLong':api_data['CountyLatLong'],'BankBranches':api_data['BankBranches'],'PeerBankBranches':api_data['PeerBankBranches']})
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})

def SaveChartImage(request):
    try: 
        # Extract image data from request
        import base64
        import os
        data = request.POST 
        image_data = data.get('image')
        filename=data.get('filename') 
        segNm=data.get('segNm') 
        if not image_data:
            return JsonResponse({'error': 'No image data provided'})

        # Decode the base64 image
        header, encoded_image = image_data.split(',', 1) 
        image_data = base64.b64decode(encoded_image)

        # Save the image to the static folder
        BASE_DIR = Path(__file__).resolve().parent.parent 
        static_folder = os.path.join(BASE_DIR, 'static/charts')
        os.makedirs(static_folder, exist_ok=True)
        image_filename = filename+'.png'
        image_path = os.path.join(static_folder, image_filename)

        with open(image_path, 'wb') as f:
            f.write(image_data)

        # Return the path to the saved image
        image_url = os.path.join('static/charts/', image_filename)
        
        api_url = getFLAPIURL()+'insert_FL_DA_ImageInfo/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'Img_Name':image_filename,
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'segNm':segNm
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data_denied=response.json()  

        return JsonResponse({'message': 'Image saved successfully!', 'image_url': image_url})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})

def FLDashboard(request):
    try: 
        api_url = getFLAPIURL()+'GET_FL_Data_Info/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year','2023'),
            'portfolio':'Mortgage',
            'dept':str(request.session['dept']),
            'utility':'Marketing'
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data_Filter=response.json() 

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
        api_url = getFLAPIURL()+'get_FLDashboardData/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_save = {
             'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year','2023'),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'ClassVar':request.GET.get('prohb_cls',''),
        }
        responseget = requests.post(api_url,data= json.dumps(data_to_save),headers=header)
        data=responseget.json()
        return render(request, 'dashboard_FLending.html',{'arrCols':arrCols,'ctrl_cols':ctrl_class_data['ColumnName'], 'apps':data['apps'],'orginated':data['orginated'],'denied':data['denied'],
                            'dropout':data['dropout'],'air':data['air'],'dor':data['dor'],'dorcolor':data['dorcolor'],'aircolor':data['aircolor']
                            ,'doi':data['doi'],'doicolor':data['doicolor'],'approved':data['approved'],'CreditModelCnt':data['CreditModelCnt'],
                            'FLRating':data['FLRating'],'querybldrcols':api_data_Filter['gridDttypes'],'CtrlClsSelected':api_data_Filter['CtrlClsSelected']})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def FLDashboard_Drilldown(request):
    try: 
        
        api_url = getFLAPIURL()+'get_FLDashboard_Drilldown_Data/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_save = {
             'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year','2023'),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'ClassVar':request.GET.get('prohb_cls',''),
            'ddType':request.GET.get('ddType',''),
        }
        responseget = requests.post(api_url,data= json.dumps(data_to_save),headers=header)
        data=responseget.json()
        api_url = getFLAPIURL()+'get_FLDashboard_Drilldown_Data_Pairwise/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_save = {
             'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year','2023'),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'ClassVar':request.GET.get('prohb_cls',''),
            'ddType':request.GET.get('ddType',''),
        }
        responseget = requests.post(api_url,data= json.dumps(data_to_save),headers=header)
        data_pair=responseget.json()
        
        return JsonResponse( { 'apps':data['apps'],'data_pair':data_pair['data_pair'] }) 
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def FLDashboard_Drilldown_Pairwise(request):
    try: 
        print('in pairwise')
        api_url = getFLAPIURL()+'get_FLDashboard_Drilldown_Data_Pairwise/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_save = {
             'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year','2023'),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'ClassVar':request.GET.get('prohb_cls',''),
            'ddType':request.GET.get('ddType',''),
        }
        responseget = requests.post(api_url,data= json.dumps(data_to_save),headers=header)
        data=responseget.json()
        return JsonResponse( { 'apps':data['apps'] })
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())


def FLDashboard_AIR_Drilldown(request):
    try:  
        api_url = getFLAPIURL()+'get_AIR_Drilldown_Data/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_save = {
             'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year','2023'),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'ClassVar':request.GET.get('prohb_cls',''),
            'ddType':request.GET.get('ddType',''),
        }
        responseget = requests.post(api_url,data= json.dumps(data_to_save),headers=header)
        data=responseget.json()
        api_url = getFLAPIURL()+'get_FLDashboard_Drilldown_Data_Pairwise/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_save = {
             'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year','2023'),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'ClassVar':request.GET.get('prohb_cls',''),
            'ddType':request.GET.get('ddType',''),
        }
        responseget = requests.post(api_url,data= json.dumps(data_to_save),headers=header)
        data_pair=responseget.json()
         
        return JsonResponse( { 'apps':data['ddData']  }) 
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def creditmodelList(request):
    try: 
        api_url=getFLAPIURL()+"Get_Credit_Mdl_List/"       
        data_to_save={ 
             } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)         
        api_data=response.json() 
        modelinfo=api_data['mdldata']#objreg.getModelByFilter(request.session['uid'],ty,chartnm,colnm,'0')
         
             
        # return render(request, 'addICQQtns.html',{'sections':objmaster.getSections(),'actPage':'RMSE','notifylen':str(len(objvalidation.getVTNotifications(request.session['uid'])))})
        return render(request, 'credit_modelList.html',{'actPage':'RMSE','modelinfo':modelinfo})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc())

def CompareOnMap(request):
    print('submitted')
    rb_Filter=''
    chkisPeer=''
    rb_Filter2=''
    chkisPeer2=''
    try:
        
        rb_Filter = request.POST.get('ddlFilter','TOT_MALE') 
        chkisPeer=request.POST.get('chkisPeer','n') 
        rb_Filter2 = request.POST.get('ddlFilter2','TOT_MALE') 
        chkisPeer2=request.POST.get('chkisPeer2','n')
        print('rb_Filter2 ',rb_Filter2)
    except Exception as e:
        print('CompareOnMap ',e,traceback.print_exc())
    
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
        'utility':'Dashboard-Map',
        'dept':str(request.session['dept'] )
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data=response.json()   

    api_url = getFLAPIURL()+'get_CountyMedianIncome/' 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }       
    data_params={
        'Portfolio':'Mortgage',
        'Dept':str(request.session['dept']),
        'uid':request.session['uid'],
        'filter_col':'Median',
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data_bank=response.json()        
         
        #return JsonResponse({'PeerBanks':api_data['PeerBanks'],'States':api_data['States'],'Counties':api_data['Counties']})

    return render(request, 'fl_map_jq.html',{'rb_Filter':rb_Filter,'chkisPeer':chkisPeer,'rb_Filter2':rb_Filter2,'chkisPeer2':chkisPeer2,'arrCols':arrCols,'ctrl_cols':ctrl_class_data['ColumnName'],'querybldrcols':api_data['gridDttypes'],'CountyLatLong':api_data_bank['CountyLatLong'],'peerlei':api_data['peerlei']})



def get_MedianIncomeForCounty(request):
    try: 
        api_url = getFLAPIURL()+'get_MedianIncomeForCounty/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'filter_col':request.GET.get('filter_col','')
        }
        #print("request.session['filter_col'] : ",request.session['filter_col'])
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'CountyLatLong':api_data['CountyLatLong']})
    except Exception as e:
        print('updateaccess ',e,traceback.print_exc())
        return JsonResponse({'istaken':'false'})

def get_QueryDataForCounty(request):
    try: 
        api_url = getFLAPIURL()+'get_QueryDataForCounty/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'State':request.GET.get('State',''),
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'peer':request.GET.get('peer',''),
            'filter_col': request.GET.get('filter_col','')      
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'CountyLatLong':api_data['CountyLatLong']})
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})
    

def generate_pdf(request):
    try:
        print('inside generate_pdf')
        pdf = FPDF(orientation = 'P', unit = 'mm', format='Legal')#PDF()
        title = "Overall Application Summary for {Name of Bank}"
        pdf.add_page()
        pdf.set_xy(10, 100)
        pdf.set_font("Arial", "B", 22)
        pdf.cell(0, 10,title, border=0, ln=1, align="C") 
        arrCLs=['derived_ethnicity','derived_race','derived_sex','applicant_age']
        for arr in arrCLs:
            api_url = getFLAPIURL()+'get_FL_Report_Data_Varwise/' 
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }       
            data_params={
                'uid':request.session['uid'],
                'activity_year':'2023',
                'ClassVar':arr,
                'Portfolio':'Mortgage',            
                'Dept':request.session['dept'],
            }
            response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
            rpt_data=response.json()    
            print('rpt_data')
            print(rpt_data['apps']['Originations'])
            # rpt_data= {'Dropout': {'0': {'ordCol': 1, 'ClsLbl': 'White:Male', 'ttlappl': 2462, 'Originations': 1153, 'Denied': 0, 'Dropped': 0}, '1': {'ordCol': 2, 'ClsLbl': 'Ethnicity Not Available', 'ttlappl': 1078, 'Originations': 562, 'Denied': 404, 'Dropped': 100}, '2': {'ordCol': 2, 'ClsLbl': 'Hispanic or Latino', 'ttlappl': 143, 'Originations': 37, 'Denied': 87, 'Dropped': 19}, '3': {'ordCol': 2, 'ClsLbl': 'Joint', 'ttlappl': 54, 'Originations': 28, 'Denied': 19, 'Dropped': 7}, '4': {'ordCol': 2, 'ClsLbl': 'Not Hispanic or Latino', 'ttlappl': 6191, 'Originations': 3421, 'Denied': 2225, 'Dropped': 508}}}
            list_data = []
        
            for i,j in rpt_data['apps']['Originations'].items():#api_data['apps']['Dropout'].items():
                x,y=5,50 
                if i != '0': 
                    #Add Header
                    utility = "Underwriting"
                    pdf.add_page()
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 10, "Analysis of Mortgage Portfolio - "+utility, border=0, ln=1, align="C")
                    pdf.ln(5)  # Add a small vertical space

                    #1 row
                    pdf.set_xy(x, y) 
                    pdf.set_font  ("Arial",  size=9)
                    pdf.set_fill_color(211, 211, 211)
                    y = pdf.get_y()#+10
                    pdf.set_xy(10, y)
                    pdf.multi_cell(25,5, j['ClsLbl'],
                            0, fill=False, align='C')

                    pdf.set_xy(35, y)
                    pdf.multi_cell(30, 5,  j['ClsLbl']+"\n Originations",
                            0, fill=False, align='C')
                    pdf.set_xy(65, y)
                    pdf.multi_cell(30, 5,  j['ClsLbl']+"\n Originations Rate",
                            0, fill=False, align='C')
                    pdf.set_xy(95, y)
                    pdf.multi_cell(30, 5,j['ClsLbl']+" Denials",
                            0, fill=False, align='C')
                    pdf.set_xy(125, y)
                    pdf.multi_cell(30, 5,j['ClsLbl']+" Denials Rate",
                            0, fill=False, align='C')
                    pdf.set_xy(155, y)
                    pdf.multi_cell(25, 5, j['ClsLbl']+" Dropouts", 0,
                            fill=False, align='C')
                    pdf.set_xy(180, y)
                    pdf.multi_cell(25, 5, j['ClsLbl']+" Dropout Rate", 0,
                            fill=False, align='C')
                    #11
                    y=pdf.get_y()
                    pdf.set_xy(x, y) 
                    pdf.set_font("Arial",  size=9)
                    pdf.set_fill_color(211, 211, 211)
                    y = pdf.get_y()#+10
                    pdf.set_xy(10, y)
                    pdf.cell(25, 5, str(j['ttlappl']),
                            0, fill=False, align='C')
                    pdf.set_xy(35, y)
                    pdf.cell(30, 5, str(j['Originations']),
                            0, fill=False, align='C')
                    pdf.set_xy(65, y)
                    if j['ttlappl'] == 0:
                        pdf.cell(30, 5,"-",
                                0, fill=False, align='C')
                    else:
                        pdf.cell(30, 5, str(round(j['Originations']/j['ttlappl'],2)*100),
                                0, fill=False, align='C')
                    pdf.set_xy(95, y)
                    pdf.cell(30, 5,str(j['Denied']),
                            0, fill=False, align='C')
                    pdf.set_xy(125, y)
                    if j['ttlappl'] == 0:
                        pdf.cell(30, 5,"-",
                                0, fill=False, align='C')
                    else: 
                        pdf.cell(30, 5,str(round(j['Denied']/j['ttlappl'],2)*100),
                                0, fill=False, align='C')
                    pdf.set_xy(155, y)
                    pdf.cell(25, 5, str(j['Dropped']), 0,
                            fill=False, align='C')
                    pdf.set_xy(180, y)
                    if j['ttlappl'] == 0:
                        pdf.cell(25, 5, "-", 0,
                                fill=False, align='C')
                    else:
                        pdf.cell(25, 5, str(round(j['Dropped']/j['ttlappl'],2)*100), 0,
                                fill=False, align='C')
                    y = pdf.get_y()+10

                    pdf.line(10, y, 210, y)
                    # 2 White:Male
                    ctrlCls=rpt_data['apps']['Originations']['0']
                    pdf.set_xy(x, y)
                    pdf.set_font("Arial",  size=9)
                    pdf.set_fill_color(211, 211, 211)
                    y = pdf.get_y()+10
                    pdf.set_xy(10, y)
                    pdf.multi_cell(25, 5, ctrlCls['ClsLbl'],
                            0, fill=False, align='C')

                    pdf.set_xy(35, y)
                    pdf.multi_cell(30, 5,  ctrlCls['ClsLbl']+"\n Originations",
                            0, fill=False, align='C')
                    pdf.set_xy(65, y)
                    pdf.multi_cell(30, 5,  ctrlCls['ClsLbl']+"\n Originations Rate",
                            0, fill=False, align='C')
                    pdf.set_xy(95, y)
                    pdf.multi_cell(30, 5,ctrlCls['ClsLbl']+" Denials",
                            0, fill=False, align='C')
                    pdf.set_xy(125, y)
                    pdf.multi_cell(30, 5,ctrlCls['ClsLbl']+" Denials Rate",
                            0, fill=False, align='C')
                    pdf.set_xy(155, y)
                    pdf.multi_cell(25, 5, ctrlCls['ClsLbl']+" Dropouts", 0, fill=False, align='C')
                    pdf.set_xy(180, y)
                    pdf.multi_cell(25, 5, ctrlCls['ClsLbl']+" Dropout Rate", 0, fill=False, align='C')
                    # # #21
                    y=pdf.get_y()
                    pdf.set_xy(x, y) 
                    pdf.set_font("Arial",  size=9)
                    pdf.set_fill_color(211, 211, 211)
                    y = pdf.get_y()#+10
                    pdf.set_xy(10, y)
                    pdf.multi_cell(25, 5, str(ctrlCls['ttlappl']),
                            0, fill=False, align='C')

                    pdf.set_xy(35, y)
                    pdf.multi_cell(30, 5, str(ctrlCls['Originations']),
                            0, fill=False, align='C')
                    pdf.set_xy(65, y) 
                    pdf.multi_cell(30, 5,  str(round(j['Originations']/j['ttlappl'],2)*100),
                            0, fill=False, align='C')
                    pdf.set_xy(95, y)
                    pdf.multi_cell(30, 5,str(ctrlCls['Denied']),
                            0, fill=False, align='C')
                    pdf.set_xy(125, y) 
                    pdf.multi_cell(30, 5, str(round(j['Denied']/j['ttlappl'],2)*100),
                            0, fill=False, align='C')
                    pdf.set_xy(155, y)
                    pdf.multi_cell(25, 5, str(ctrlCls['Dropped']), 0, fill=False, align='C')
                    pdf.set_xy(180, y)# str(round(j['Dropped']/j['ttlappl'],2)*100)
                    pdf.multi_cell(25, 5, str(ctrlCls['Dropped']/ctrlCls['ttlappl']), 0 ,
                            fill=False, align='C') 
                    y = pdf.get_y()+10
                    pdf.line(10, y, 210, y)

                    #Add Footer
                    pdf.set_xy(x, y)
                    y = pdf.get_y()+100
                    # pdf.image("logo.png", 10, 8, 33)  # Add logo (x=10, y=8, width=33)
                    pdf.set_font("Arial", "B", 12)
                    # pdf.cell(0, 10, "PDF Header with Logo", border=0, ln=1, align="C")
                    pdf.ln(215)
                    pdf.cell(0, 10, f"Page {pdf.page_no()} of {{nb}}", align="C")

                    #3 Comparison
                    # pdf.set_xy(x, y) 
                    # pdf.set_font("Arial",  size=9)
                    # pdf.set_fill_color(211, 211, 211)
                    # y = pdf.get_y()#+10
                    # pdf.set_xy(10, y)
                    # pdf.multi_cell(25, 5, "Outcome Comparison",
                    #         1, fill=True, align='C')
                    # pdf.set_xy(35, y)
                    # pdf.multi_cell(30, 5,  "",
                    #         1, fill=True, align='C')
                    # pdf.set_xy(65, y)
                    # pdf.multi_cell(30, 5,  "Origination Incidence Variance",
                    #         1, fill=True, align='C')
                    # pdf.set_xy(95, y)
                    # pdf.multi_cell(30, 5,"",
                    #         1, fill=True, align='C')
                    # pdf.set_xy(125, y)
                    # pdf.multi_cell(30, 5,"Daniel Incidence Variance",
                    #         1, fill=True, align='C')
                    # pdf.set_xy(155, y)
                    # pdf.multi_cell(25, 5, "", 1,
                    #         fill=True, align='C')
                    # pdf.set_xy(180, y)
                    # pdf.multi_cell(25, 5, "Dropout Incidence Variance", 1,
                    #         fill=True, align='C')
                    # # #31
                    # y=pdf.get_y()
                    # pdf.set_xy(x, y) 
                    # pdf.set_font("Arial",  size=9)
                    # pdf.set_fill_color(211, 211, 211)
                    # y = pdf.get_y()#+10
                    # pdf.set_xy(10, y)
                    # pdf.multi_cell(25, 5, "",
                    #         1, fill=True, align='C')

                    # pdf.set_xy(35, y)
                    # pdf.multi_cell(30, 5, "Negative Comparison",
                    #         1, fill=True, align='C')
                    # Hispanic_originate_rate = round(j['Originations']/j['ttlappl'],2)*100
                    # white_originate_rate = round(ctrlCls['Originations']/ctrlCls['ttlappl'],2)*100
                    # if white_originate_rate == 0:
                    #     originate_rate = str(0)
                    # else:
                    #     originate_rate = str(round(Hispanic_originate_rate/white_originate_rate,2)*100)
                    # pdf.set_xy(65, y)
                    # pdf.multi_cell(30, 5,  originate_rate,1, fill=True, align='C')
                    # pdf.set_xy(95, y)
                    # pdf.multi_cell(30, 5,"Positive Comparison",
                    #         1, fill=True, align='C')
                    # hispanic_daniel_rate = round(j['Denied']/j['ttlappl'],2)*100 
                    # white_daniel_rate = round(ctrlCls['Denied']/ctrlCls['ttlappl'],2)*100
                    # if white_daniel_rate == 0:
                    #     daniel_rate = str(0)
                    # else:
                    #     daniel_rate = str(round(hispanic_daniel_rate/white_daniel_rate,2)*100)
                    # pdf.set_xy(125, y)
                    # pdf.multi_cell(30, 5, daniel_rate,1, fill=True, align='C')
                    # pdf.set_xy(155, y)
                    # pdf.multi_cell(25, 5, "Negative Comparison", 1,
                    #         fill=True, align='C')
                    # hispanic_droupout_rate = round(j['Dropped']/j['ttlappl'],2)*100
                    # white_droupout_rate = round(ctrlCls['Dropped']/ctrlCls['ttlappl'],2)*100
                    # if white_droupout_rate == 0:
                    #     droupout_rate =str(0)
                    # else:
                    #     droupout_rate = str(round(hispanic_droupout_rate/white_droupout_rate,2)*100)
                    # pdf.set_xy(180, y)
                    # pdf.multi_cell(25, 5, droupout_rate, 1,fill=True, align='C')

        
        pdf.output(os.path.join( BASE_DIR, "static/media/"+str(request.session['uid'])+"_FairLendingReport.pdf"))
    
        
        return JsonResponse({'msg':"PDF Generated successfully"})    
    except Exception as e:
        print(e,traceback.print_exc())

def get_MedianIncomeForCountyN(request):
    try: 
        api_url = getFLAPIURL()+'get_MedianIncomeForCountyN/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'filter_col':request.GET.get('filter_col','')
        }
        #print("request.session['filter_col'] : ",request.session['filter_col'])
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'CountyLatLong':api_data['CountyLatLong'],'LoansCnt':api_data['LoansCnt']})
    except Exception as e:
        print('updateaccess ',e,traceback.print_exc())
        return JsonResponse({'istaken':'false'})

def get_QueryDataForCountyN(request):
    try: 
        api_url = getFLAPIURL()+'get_QueryDataForCountyN/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'State':request.GET.get('State',''),
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'peer':request.GET.get('peer',''),
            'filter_col': request.GET.get('filter_col','')      
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'CountyLatLong':api_data['CountyLatLong'],'LoansCnt':api_data['LoansCnt'],'maxCount': api_data['maxCount'],'minCount': api_data['minCount']})
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})

def get_PopulationDataForCounty(request):
    try: 
        api_url = getFLAPIURL()+'get_PopulationDataForCounty/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'State':request.GET.get('State',''),
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'peer':request.GET.get('peer',''),
            'filter_col': request.GET.get('filter_col',''),
            'OnlyBankStates':request.GET.get('OnlyBankStates','n')
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'CountyLatLong':api_data['CountyLatLong'],'LoansCnt':api_data['LoansCnt'],'maxCount': api_data['maxCount'],'minCount': api_data['minCount']})
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})


def FL_Data_Fields_Master(request):
    try: 
        return render(request, 'FL_Field_Master.html')
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc())

def add_FL_Data_Fields_Master(request):
    try: 
        return render(request, 'add_FL_Fields.html')
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc())

def insert_FL_Field_And_Valid_Value(request):
    try:
        api_url = getFLAPIURL()+'insert_FL_Field_And_Valid_Value/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'FL_Field_Label':request.GET.get('FL_Field_Label',''),
            'FL_Field_Valid_Value':request.GET.get('FL_Field_Valid_Value',''),
            'Added_By':request.session['uid']  , 
            'FL_Field_Description':request.GET.get('FL_Field_Description',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'FL_Field_IsNull':request.GET.get('FL_Field_IsNull',''), 
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()  
        return JsonResponse({'is_taken':api_data['is_taken']})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc())

def gettestCor(request):
    try: 
        api_url = getFLAPIURL()+'gettestCor/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'State':request.GET.get('State',''),
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'peer':request.GET.get('peer',''),
            'filter_col': request.GET.get('filter_col',''),
            'txtValPerc': request.GET.get('txtValPerc','0'),
            'ddlFilter': request.GET.get('ddlFilter',''),
            'ddlcolval': request.GET.get('Val_ddl1',''),
            'ddlFilter2': request.GET.get('ddlFilter2',''),
            'ddlcolval2': request.GET.get('Val_ddl2',''), 
            'ConmpareTypeVal': request.GET.get('ConmpareTypeVal','') ,
            'Filter_1':request.GET.get('Filter_1','Filter_1'), 
            'Filter_2':request.GET.get('Filter_2','Filter_2'), 
            
            'FillType': request.GET.get('FillType','Census'),
            'HazardType': request.GET.get('HazardType',''),
            'HazardCat':request.GET.get('HazardCat','')
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'testcor':api_data['testcor'],'loansGC':api_data['loansGC'],'loansGC2':api_data['loansGC2'],'banks':api_data['banks'],'peerbanks':api_data['peerbanks']})
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})


def fl_transmit_question(request):
    try:
        print("post data",request.body)
        if request.method == 'POST':
            data = json.loads(request.body)
            department = data.get('department')
            portfolio = data.get('portfolio')
            field_name = data.get('field_name')
            field_type = data.get('field_type') 


            api_url=getFLAPIURL()+"fl_transmit_question/"       
            params={'department':department,
                'portfolio':portfolio,
                'field_name':field_name,
                'field_type':field_type,
                } 
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(api_url, data= json.dumps(params),headers=header)         
            api_data=response.json()
            print("api_data",api_data)

            return JsonResponse(api_data)
            
        #department fetch
        Department

        depart_obj=Department.objects.all()
        context={'depart_obj':depart_obj}
        return render(request,'fl_transmit_question.html',context)
    except Exception as e:
        print('question_ans is ',e)
        print('question_ans traceback is ', traceback.print_exc())  


def fl_transmit_answer(request):
    print("data",request.session['uid'])

    api_url=getFLAPIURL()+"fl_transmit_answer/"       
    params={'uid':request.session['uid']
        } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.post(api_url, data= json.dumps(params),headers=header)         
    api_data=response.json()
    print("api_data",api_data)
    
    return render(request,'fl_transmit_answer.html',{'questions': api_data})



def process_portfolio(request):
    try:
        print('inside process')
        if request.method == 'POST':
        
            # Parse data from the POST request
            portfolio = request.POST.get('portfolio') 
            print("portfolio",portfolio)

            api_url=getFLAPIURL()+"process_portfolio/"       
            params={'portfolio':portfolio,
                    'uid':request.session['uid']
                } 
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(api_url, data= json.dumps(params),headers=header)         
            api_data=response.json()
            print("api_data",api_data)
            questions=api_data
            return JsonResponse(questions,safe=False)
            
        return render(request,'fl_transmit_answer.html')

    except Exception as e:
        print('question_ans is ',e)
        print('question_ans traceback is ', traceback.print_exc())         


from django.db import connection
from django.conf import settings

def submit_answers(request):
    
    try:
        if request.method == 'POST':
            # Parse the submitted data
            answers = json.loads(request.POST.get('answers', '[]'))
            print("answers",answers)
            api_url=getFLAPIURL()+"submit_answers/"       
            params={'answers':answers,
                    'dept':request.session['dept'],
                } 
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(api_url, data= json.dumps(params),headers=header)         
            api_data=response.json()
            print("api_data",api_data)

            request.session['portf']='Mortgage'
            dept=str(request.session['dept'])
            port= request.session['portf'] 
            request_data = FlTransmittaAnswerSheet.objects.filter(department=dept,portfolio=port).values() 

            first_line = "|".join([entry['answer'] for entry in request_data])


            # # Fetch data from the SQL table
            # with connection.cursor() as cursor:
            #     cursor.execute("SELECT * FROM FL_Data")  # Replace `FL_Data` with your actual table name
            #     rows = cursor.fetchall()

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM FL_Data
                    WHERE Department = %s AND Portfolio = %s
                """, [dept, port])  # Use the dept and port values to filter the data
                rows = cursor.fetchall()
            # Prepare the content for the txt file
            content = first_line + "\n"  # Add the first line with answers
            # content += "\n".join(answer_lines) + "\n"  # Add detailed answers
            for row in rows:  # Add SQL data rows (pipe-separated)
                content += "|".join([str(value) if value is not None else "NULL" for value in row]) + "\n"

            # Define the path to save the txt file
            static_dir = os.path.join(settings.BASE_DIR, 'static/text_data')
            os.makedirs(static_dir, exist_ok=True)  # Ensure the directory exists
            file_path = os.path.join(static_dir, 'pipe_separated_data_with_answers.txt')

            # Write content to the file
            with open(file_path, 'w') as file:
                file.write(content)


            return JsonResponse(api_data)


    except Exception as e:
        print('question_ans is  ',e)
        print('question_ans traceback is ', traceback.print_exc())   


def file_raw_fl(request):
    request.session['portfolio']='port_credit_mortage'
    dept=request.session['dept']
    port= request.session['portfolio']
    if request.method == 'POST' and request.FILES['file']:
        upload_type = request.POST.get('upload_type')  # Get the parameter to differentiate tabs
        if upload_type == 'raw':
            folder = 'static/Fl/raw_data/'+str(dept)+'/Portfolio/'+port
        elif upload_type == 'fl':
            folder = 'static/FL/fl_data/'+str(dept)+'/Portfolio/'+port
        else:
            pass

        # Ensure the folder exists
        file_path = os.path.join(BASE_DIR, folder)
        os.makedirs(file_path, exist_ok=True)

        # Save the file
        file = request.FILES['file']
        file_full_path = os.path.join(file_path, file.name)
        with open(file_full_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        api_url=getFLAPIURL()+"fl_data_file_info/"       
        params={'type':upload_type,
                'dept':dept,
                'portfolio':port,
                'uploaded_by':request.session['uid'],
                'file_name':file.name
            } 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(params),headers=header)         
        api_data=response.json()
        print("api_data",api_data)


        # alert_message = "File uploaded and data saved successfully."

        return render(request, 'file_raw_fl.html', {'api_data': api_data})

    # Render the form with no file uploaded
    return render(request, 'file_raw_fl.html', {'tab': 'raw'})


def generatepdf(request):
    try: 
        return render(request, 'generatepdf.html',{ 'actPage':'Pdf Generation'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

from django.http import HttpResponse, Http404
from docx.enum.section import WD_ORIENT
from docx import Document

def generateReport_utility(request):
    try: 
        # a variable pdf
        pdf = FPDF(orientation = 'P', unit = 'mm', format='Legal')#PDF()
        document = Document()
        section = document.sections[0]
        # Changing the orientation to landscape
        section.orientation = WD_ORIENT.LANDSCAPE

        pdf = addheaderpages(pdf)
    
        pdf = generate_pdf_underwritting(pdf,request.session['accessToken'],request.session['uid'],request.session['dept'])

        # pdf = generate_pdf_pricing(pdf)

        pdf = generate_pdf_marketing(pdf)

        pdf.output(os.path.join(
            BASE_DIR, "static/UtilityReport.pdf"))

        document.save(os.path.join(
            BASE_DIR, "static/media/demo.docx"))

        reportFilepath = os.path.join(
            BASE_DIR, "static/UtilityReport.pdf")
        if os.path.exists(reportFilepath):
            
            return JsonResponse({'msg':"PDF Generated successfully"})
        raise Http404
    except Exception as e:
        print(e)
        print(traceback.print_exc())
        data = {"is_taken": True}
        return JsonResponse(data)

def addheaderpages(pdf):
    x,y = 25,50
    # pdf = FPDF(orientation = 'P', unit = 'mm', format='Legal')#PDF()
    bank_name = "ABC Bank"
    title = "Overall Application Summary for "+bank_name
    pdf.add_page()
    pdf.set_xy(10, 100)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10,title, border=0, ln=1, align="C")
    # pdf.line(5)

    y = pdf.get_y()#+10
    pdf.cell(0, 10,"Portfolio Name: Mortgage", border=0, ln=1, align="C") 

    y = pdf.get_y()#+10
    pdf.cell(0, 10,"Period: 2023", border=0, ln=1, align="C")

    y = pdf.get_y()#+10
    pdf.cell(0, 10,"Report Date:"+str(datetime.now().date()), border=0, ln=1, align="C") 

    ## Document Version History ##
    x,y=25,50 
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Document Version History", border=0, ln=1, align="C")
    # pdf.ln(1)  # Add a small vertical space
    
    #1 row
    # x,y=25,50 
    # y = pdf.get_y() 
    # pdf.set_font  ("Arial", "B", size=9)
    # pdf.set_fill_color(255, 255, 255)
    # pdf.set_xy(10, y)
    # pdf.multi_cell(35,10, "Period",
    #         1, fill=True, align='C')
    # pdf.set_xy(45, y)
    # pdf.multi_cell(35,10, "Date",
    #         1, fill=True, align='C')
    # pdf.set_xy(80, y)
    # pdf.multi_cell(35, 10,  "Author",
    #         1, fill=True, align='C')
    # pdf.set_xy(115, y)
    # pdf.multi_cell(35, 10,  "Approved By",
    #         1, fill=True, align='C')
    # pdf.set_xy(150, y)
    # pdf.multi_cell(45, 10,"Version Description",
    #         1, fill=True, align='C')
    
    # #11 
    # y=pdf.get_y()
    # pdf.set_xy(x, y) 
    # pdf.set_font("Arial", "B", size=9)
    # pdf.set_fill_color(255, 255, 255)
    # y = pdf.get_y()#+10    
    # pdf.set_font("Arial",size=9)
    # pdf.set_xy(10, y)
    # pdf.cell(35, 10, "",
    #         1, fill=True, align='C')
    # pdf.set_xy(45, y)
    # pdf.cell(35, 10, "",
    #         1, fill=True, align='C')
    # pdf.set_xy(80, y)   ##
    # pdf.multi_cell(35, 10, "",
    #         1, fill=True, align='C')
    # pdf.set_xy(115, y)
    # pdf.cell(35, 10,"",
    #         1, fill=True, align='C')
    # pdf.set_xy(150, y)
    # pdf.multi_cell(45, 10,"",
    #         1, fill=True, align='C')
    
    ##### segment
    # x,y = 25,50
    # pdf.add_page()
    # y = pdf.get_y()+10
    # pdf.set_xy(20, y)
    # pdf.set_font("Arial", "B", 12)
    # pdf.cell(0, 10,"1. Segment", border=0, ln=1, align="L")

    # y = pdf.get_y()
    # pdf.set_font("Arial",size=9)
    # pdf.set_xy(30, y)
    # pdf.cell(0, 10,"Mortgage", border=0, ln=1, align="L") 

    # y = pdf.get_y()
    # pdf.set_xy(30, y)
    # pdf.set_font("Arial",size=9)
    # pdf.cell(0, 10,"Department", border=0, ln=1, align="L") 

    # y = pdf.get_y()
    # pdf.set_xy(30, y)
    # pdf.set_font("Arial",size=9)
    # pdf.cell(0, 10,"Product", border=0, ln=1, align="L")

    # y = pdf.get_y()
    # pdf.set_xy(20, y)
    # pdf.set_font("Arial", "B", 12)
    # pdf.cell(0, 10,"2. Fair Lending Risk Assessment", border=0, ln=1, align="L") 
    return pdf
 
def generate_pdf_underwritting(pdf,accessToken,uid,dept):
    try:
        class_var = ['derived_race','derived_sex','derived_ethnicity','applicant_age']
        datalist = []
        for i in class_var:
            api_url = getFLAPIURL()+'get_FL_Report_Data_Varwise/' 
            header = {
            "Content-Type":"application/json", 
            'Authorization': 'Token '+accessToken
            }       
            data_params={
                'uid': uid,
                'activity_year':'2023',
                'ClassVar':i,
                'Portfolio':'Mortgage',            
                'Dept':dept
            }
            response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
            api_data=response.json()  
            if(api_data['apps']!=[]):
                datalist.append(api_data)
        # datalist.append(api_data['filterSelected'])
       
        # print('datalist ',datalist)
        for i,rpt_data in enumerate(datalist):
            
            # rpt_data['title_comment'] = {'title':'check new'+str(idx),'comment':'check new comment'+str(idx)}
            ### Minority Sum ###
            application_values = [j['ttlappl'] for i,j in rpt_data['apps']['Originations'].items() if i != '0']
            
            # Origination_values = [j['Originations'] for i,j in rpt_data['apps']['Dropout'].items() if i != '0' ]
            Origination_values = []
            for  i,j in rpt_data['apps']['Originations'].items():
                
                if i != '0':
                    if j['Originations'] == None:
                        Origination_values_2 = 0
                        a = Origination_values_2
                    else:
                        a = j['Originations']
                    Origination_values.append(a) 
            # OriginationRate_values = [round(j['Originations']/j['ttlappl'],2)*100 for i,j in rpt_data['Dropout'].items() if i != '0' ]
            OriginationRate_values = []
            for  i,j in rpt_data['apps']['Originations'].items():
                print(" i is ",i)
                print('(int(i) % 2) ',str(i),str((int(i) % 2)))
                if i != '0':
                    if j['Originations'] == None:
                        Origination_values_1 = 0
                        a = round(Origination_values_1/j['ttlappl'],2)*100
                    else: 
                        a = round(j['Originations']/j['ttlappl'],2)*100
                    OriginationRate_values.append(a)

            Denials_values = [j['Denied'] for i,j in rpt_data['apps']['Originations'].items() if i != '0']
            DenialsRate_values = [round(j['Denied']/j['ttlappl'],2)*100 for i,j in rpt_data['apps']['Originations'].items() if i != '0']
            Droupout_values = [j['Dropped'] for i,j in rpt_data['apps']['Originations'].items() if i != '0']
            DroupoutRate_values = [round(j['Dropped']/j['ttlappl'],2)*100 for i,j in rpt_data['apps']['Originations'].items() if i != '0']
            # air_values =  [j['AIR'] for i,j in  rpt_data['apps']['Originations'].items() if i != '0']
            # dor_values =  [j['DOR'] for i,j in  rpt_data['apps']['Originations'].items() if i != '0']
            # doi_values =  [j['DOI'] for i,j in  rpt_data['apps']['Originations'].items() if i != '0']

            x,y=25,50  
            utility =rpt_data['apps']['title']#rpt_data['apps']['title_comment']['title']
           
            pdf.add_page()
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, utility, border=0, ln=1, align="C")
            pdf.ln(5)  # Add a small vertical space

            filters = rpt_data['filterSelected']
            # print("filters",filters)
            filter_list ="Focal Points : "+ filters.replace(" and ",", ").replace(" And ",", ").replace(" or ",", ").replace(" Or ",", ").replace("=",":").replace("'","")
            # print("filter_list",filter_list)
            y=pdf.get_y() 
            pdf.set_xy(x, y) 
            pdf.set_font("Arial", "B", size=9)
            # pdf.set_fill_color(255, 255, 255)
            pdf.set_fill_color(211, 211, 211)
            y = pdf.get_y()#+10
            pdf.set_xy(10, y)
            pdf.multi_cell(200, 10, filter_list,
                    1, fill=True, align='L')
            
            #1 row
            x,y=25,50 
            pdf.set_xy(x, y) 
            pdf.set_font  ("Arial", "B", size=9)
            pdf.set_fill_color(255, 255, 255)
            y = pdf.get_y()#+10
            pdf.set_xy(10, y)
            pdf.multi_cell(35,10, "",
                    1, fill=True, align='C')
            pdf.set_xy(45, y)
            pdf.multi_cell(25,10, "Application",
                    1, fill=True, align='C')
            pdf.set_xy(70, y)
            pdf.multi_cell(25, 10,  "Originations",
                    1, fill=True, align='C')
            pdf.set_xy(95, y)
            pdf.multi_cell(25, 5,  "Originations Rate",
                    1, fill=True, align='C')
            pdf.set_xy(120, y)
            pdf.multi_cell(25, 10,"Denials",
                    1, fill=True, align='C')
            pdf.set_xy(145, y)
            pdf.multi_cell(25, 10,"Denials Rate",
                    1, fill=True, align='C')
            pdf.set_xy(170, y)
            pdf.multi_cell(20, 10, "Dropouts",1, fill=True, align='C')
            pdf.set_xy(190, y)
            pdf.multi_cell(20, 5, "Dropout Rate", 1, fill=True, align='C')
            
            #11 
            y=pdf.get_y()
            pdf.set_xy(x, y) 
            pdf.set_font("Arial", "B", size=9)
            pdf.set_fill_color(255, 255, 255)
            y = pdf.get_y()#+10
            a = "Minority"
            pdf.set_xy(10, y)
            if len(a) > 18:
                pdf.multi_cell(35, 5, "Minority",
                        1, fill=True, align='C')
            else:
                pdf.multi_cell(35, 10, "Minority",
                        1, fill=True, align='C')

            # pdf.set_xy(10, y)
            # pdf.multi_cell(35, 5, "Minority",
            #         1, fill=True, align='C')
            pdf.set_font("Arial",size=9)
            pdf.set_xy(45, y)
            pdf.cell(25, 10, str(sum(application_values)),
                    1, fill=True, align='C')
            pdf.set_xy(70, y) 
            pdf.cell(25, 10, str(sum(Origination_values)),
                    1, fill=True, align='C')
            pdf.set_xy(95, y)   ##
            if sum(application_values)==0:
                pdf.multi_cell(25, 10,"NA",
                        1, fill=True, align='C')
            else:
                pdf.multi_cell(25, 10, str(round((sum(Origination_values)/sum(application_values))*100,2)),
                    1, fill=True, align='C')
            pdf.set_xy(120, y)
            pdf.cell(25, 10,str(sum(Denials_values)),
                    1, fill=True, align='C')
            pdf.set_xy(145, y)
            if sum(application_values)==0:
                pdf.multi_cell(25, 10,"NA",
                        1, fill=True, align='C')
            else:
                pdf.multi_cell(25, 10,str(round((sum(Denials_values)/sum(application_values))*100,2)),
                    1, fill=True, align='C')
            pdf.set_xy(170, y)
            pdf.cell(20, 10, str(sum(Droupout_values)), 1, fill=True, align='C')
            pdf.set_xy(190, y)
            if sum(application_values)==0:
                pdf.multi_cell(20, 10, "NA", 1, fill=True, align='C')
            else:
                pdf.multi_cell(20, 10, str(round((sum(Droupout_values)/sum(application_values))*100,2)), 1, fill=True, align='C')
                                         
            
            # ### New White male
            ctrlCls=rpt_data['apps']['Originations']['0']  
            y=pdf.get_y()
            pdf.set_xy(x, y) 
            pdf.set_font("Arial", "B", size=9)
            pdf.set_fill_color(255, 255, 255)
            y = pdf.get_y()
            pdf.set_xy(10, y)
            pdf.multi_cell(35, 10, ctrlCls['ClsLbl'],
                    1,fill=True, align='C')
            pdf.set_xy(45, y)
            pdf.set_font("Arial",  size=9)
            pdf.multi_cell(25, 10, str(ctrlCls['ttlappl']),
                    1,fill=True, align='C')
            pdf.set_xy(70, y)
            pdf.multi_cell(25, 10, str(ctrlCls['Originations']),
                    1,fill=True, align='C')
            pdf.set_xy(95, y) 
            if ctrlCls['ttlappl']==0:
                pdf.multi_cell(25, 10,  "NA",
                    1,fill=True, align='C')
            else:
                pdf.multi_cell(25, 10,  str(round((ctrlCls['Originations']/ctrlCls['ttlappl'])*100,2)),
                        1,fill=True, align='C')
            pdf.set_xy(120, y)
            pdf.multi_cell(25, 10,str(ctrlCls['Denied']),
                    1,fill=True, align='C')
            pdf.set_xy(145, y) 
            if ctrlCls['ttlappl']==0:
                pdf.multi_cell(25, 10,  "NA",
                    1,fill=True, align='C')
            else:
                pdf.multi_cell(25, 10, str(round((ctrlCls['Denied']/ctrlCls['ttlappl'])*100,2)) ,
                        1,fill=True, align='C')
            pdf.set_xy(170, y)
            pdf.multi_cell(20, 10, str(ctrlCls['Dropped']), 1,fill=True, align='C')
            pdf.set_xy(190, y)# str(round(j['Dropped']/j['ttlappl'],2)*100)
            if ctrlCls['ttlappl']==0:
                pdf.multi_cell(20, 10,  "NA",
                    1,fill=True, align='C')
            else:
                pdf.multi_cell(20, 10,str(round((ctrlCls['Dropped']/ctrlCls['ttlappl'])*100,2)), 1,fill=True, align='C')
            
            # ###
            y=pdf.get_y()
            pdf.set_xy(x, y)
            pdf.set_font("Arial",  "B",size=9)
            pdf.set_fill_color(255, 255, 255)
            y = pdf.get_y()+10 
            pdf.set_xy(10, y)
            pdf.multi_cell(35,10, "",
                    1,fill=True, align='C')
            pdf.set_xy(45, y)
            pdf.multi_cell(25, 10, "AIR", 1,
                    fill=True, align='C')
            pdf.set_xy(70, y)
            pdf.multi_cell(25, 10, "DOR", 1,
                    fill=True, align='C')
            pdf.set_xy(95, y)
            pdf.multi_cell(25, 10, "DOI", 1,
                    fill=True, align='C') 
                    
            y=pdf.get_y()
            pdf.set_xy(x, y)
            pdf.set_font("Arial","B",size=9)
            pdf.set_fill_color(255, 255, 255)
            y = pdf.get_y()
            pdf.set_xy(10, y)
            if len(a) > 15:
                pdf.multi_cell(35, 5, a, 1,
                    fill=True, align='C')
            else:
                pdf.multi_cell(35, 10, a, 1,  #air_values dor_values doi_values
                    fill=True, align='C')
            pdf.set_font("Arial",size=9)
            pdf.set_xy(45, y)
            origin_val = sum(Origination_values)
            applc_val = sum(application_values)
            # print("Origination_values",origin_val,"application_values",applc_val,"solution",round(origin_val/applc_val*100))
            # print("Origination_values_wm",ctrlCls['Originations'],"application_values_wm",ctrlCls['ttlappl'],"solution",round(ctrlCls['Originations']/ctrlCls['ttlappl']*100))
            # print("proper_soln",round(origin_val/applc_val*100)/round(ctrlCls['Originations']/ctrlCls['ttlappl']*100)*100)
            if ctrlCls['ttlappl']==0:
                pdf.cell(25, 10,  "NA",
                    1,fill=True, align='C')
            else:
                pdf.cell(25, 10, str(round(round(origin_val/applc_val*100)/round(ctrlCls['Originations']/ctrlCls['ttlappl']*100)*100)),1,fill=True, align='C')
            pdf.set_xy(70, y)
            if ctrlCls['ttlappl']==0:
                pdf.cell(25, 10,  "NA",
                    1,fill=True, align='C')
            elif round(ctrlCls['Denied']/ctrlCls['ttlappl'],2)*100 == 0:
                pdf.cell(25, 10,"NA", 1,fill=True, align='C')
            else:
                pdf.cell(25, 10, str(round(sum(Denials_values)/sum(application_values),2)*100 / round(ctrlCls['Denied']/ctrlCls['ttlappl'],2)*100), 1,fill=True, align='C')
            pdf.set_xy(95, y)
            if ctrlCls['ttlappl']==0:
                pdf.cell(25, 10,  "NA",
                    1,fill=True, align='C')
            elif round(ctrlCls['Dropped']/ctrlCls['ttlappl'],2*100) == 0:
                pdf.cell(25, 10, "NA", 1, fill=True, align='C')
            else:
                pdf.cell(25, 10, str(round(sum(Droupout_values)/sum(application_values),2)*100 / ctrlCls['Dropped']/ctrlCls['ttlappl'],2*100), 1, fill=True, align='C')
             
            pdf.set_xy(x, y)
            y = pdf.get_y()    
            pdf.set_font("Arial", "B", 12)
            pdf.ln(190)
            pdf.cell(0, 10, f"Page {pdf.page_no()} of {{nb}}", align="C")
            #####

            for i,j in rpt_data['apps']['Originations'].items():
               
                x,y=25,50 
                if i != '0':    
                    #Add Header 
                    utility= rpt_data['apps']['title']# rpt_data['apps']['title_comment']['title'] to be uncommented
                    # print('(int(i) % 2) ',str(i),str((int(i) % 2)))
                    # if i ==0 or (int(i) % 2)==0:
                    pdf.add_page()
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 10, utility, border=0, ln=1, align="C")
                    y=pdf.get_y() 
                    # pdf.line(10, y, 210, y)
                    # pdf.ln(5) # Add a small vertical space
                    
                    # filters_1 = rpt_data['filterSelected']
                    # print("filters123",filters_1) 
                    # filter_list_1 = filters_1.split("and")
                    # print("filter_list123",filter_list_1)
                    y=pdf.get_y() 
                    pdf.set_xy(x, y) 
                    pdf.set_font("Arial", "B", size=9)
                    # pdf.set_fill_color(255, 255, 255)
                    pdf.set_fill_color(211, 211, 211)
                    y = pdf.get_y()#+10
                    pdf.set_xy(10, y)
                    pdf.multi_cell(200, 10,  filter_list,
                            1, fill=True, align='L')

                    #1 row
                    x,y=25,50
                    pdf.set_xy(x, y) 
                    pdf.set_font  ("Arial", "B", size=9)
                    pdf.set_fill_color(255, 255, 255)
                    y = pdf.get_y()#+10
                    pdf.set_xy(10, y)
                    pdf.multi_cell(35,10, "",
                            1, fill=True, align='C')
                    pdf.set_xy(45, y)
                    pdf.multi_cell(25,10, "Application",
                            1, fill=True, align='C')
                    pdf.set_xy(70, y)
                    pdf.multi_cell(25, 10,  "Originations",
                            1, fill=True, align='C')
                    pdf.set_xy(95, y)
                    pdf.multi_cell(25, 5,  "Originations Rate",
                            1, fill=True, align='C')
                    pdf.set_xy(120, y)
                    pdf.multi_cell(25, 10,"Denials",
                            1, fill=True, align='C')
                    pdf.set_xy(145, y)
                    pdf.multi_cell(25, 10,"Denials Rate",
                            1, fill=True, align='C')
                    pdf.set_xy(170, y)
                    pdf.multi_cell(20, 10, "Dropouts",1, fill=True, align='C')
                    pdf.set_xy(190, y)
                    pdf.multi_cell(20, 5, "Dropout Rate", 1, fill=True, align='C')
                    
                    #11 
                    y=pdf.get_y()
                    pdf.set_xy(x, y) 
                    pdf.set_font("Arial", "B", size=9)
                    pdf.set_fill_color(255, 255, 255)
                    y = pdf.get_y()#+10
                    pdf.set_xy(10, y) 
                    if len(str(j['ClsLbl'])) > 20:
                        pdf.multi_cell(35, 5, str(j['ClsLbl']),
                                1, fill=True, align='C')
                    else:
                        pdf.multi_cell(35, 10, str(j['ClsLbl']),
                                1, fill=True, align='C')
                    pdf.set_font("Arial",size=9)
                    pdf.set_xy(45, y)
                    pdf.cell(25, 10, str(j['ttlappl']),
                            1, fill=True, align='C')
                    pdf.set_xy(70, y)
                    pdf.cell(25, 10, str(j['Originations']),
                            1, fill=True, align='C')
                    pdf.set_xy(95, y)   ##
                    if j['ttlappl'] == 0:
                        pdf.multi_cell(25, 10,"-",
                                1, fill=True, align='C')
                    else:
                        if j['ttlappl']==0:
                            pdf.multi_cell(25, 10,  "NA",
                                1,fill=True, align='C')
                        elif j['Originations'] == None:                        
                            pdf.multi_cell(25, 10, '0',
                                1, fill=True, align='C')
                        else:
                            pdf.multi_cell(25, 10, str(round((j['Originations']/j['ttlappl'])*100,2)),
                                1, fill=True, align='C')
                    pdf.set_xy(120, y)
                    pdf.cell(25, 10,str(j['Denied']),
                            1, fill=True, align='C')
                    pdf.set_xy(145, y)
                    if j['ttlappl'] == 0:
                        pdf.multi_cell(25, 10,"-",
                                1, fill=True, align='C')
                    else: 
                        pdf.multi_cell(25, 10,str(round(j['Denied']/j['ttlappl'],2)*100),
                                1, fill=True, align='C')
                    pdf.set_xy(170, y)
                    pdf.cell(20, 10, str(j['Dropped']), 1, fill=True, align='C')
                    pdf.set_xy(190, y)
                    if j['ttlappl']==0:
                        pdf.multi_cell(25, 10,  "NA",
                                1,fill=True, align='C')
                    elif j['ttlappl'] == 0:
                        pdf.multi_cell(20, 10, "-", 1, fill=True, align='C')
                    else:
                        pdf.multi_cell(20, 10, str(round(j['Dropped']/j['ttlappl'],2)*100), 1, fill=True, align='C')
                    
                    ### New White male
                    ctrlCls=rpt_data['apps']['Originations']['0'] 
                    y=pdf.get_y()
                    pdf.set_xy(x, y) 
                    pdf.set_font("Arial", "B", size=9)
                    pdf.set_fill_color(255, 255, 255)
                    y = pdf.get_y()
                    pdf.set_xy(10, y)
                    pdf.multi_cell(35, 10, ctrlCls['ClsLbl'],
                            1,fill=True, align='C')
                    pdf.set_xy(45, y)
                    pdf.set_font("Arial",  size=9)
                    pdf.multi_cell(25, 10, str(ctrlCls['ttlappl']),
                            1,fill=True, align='C')
                    pdf.set_xy(70, y)
                    pdf.multi_cell(25, 10, str(ctrlCls['Originations']),
                            1,fill=True, align='C')
                    pdf.set_xy(95, y) 
                    if ctrlCls['ttlappl']==0:
                        pdf.multi_cell(25, 10,  "NA", 1,fill=True, align='C')
                    else:
                        pdf.multi_cell(25, 10,  str(round((ctrlCls['Originations']/ctrlCls['ttlappl'])*100,2)),
                                1,fill=True, align='C')
                    pdf.set_xy(120, y)
                    pdf.multi_cell(25, 10,str(ctrlCls['Denied']),
                            1,fill=True, align='C')
                    pdf.set_xy(145, y) 
                    if ctrlCls['ttlappl']==0:
                        pdf.multi_cell(25, 10,  "NA", 1,fill=True, align='C')
                    else:
                        pdf.multi_cell(25, 10, str(round(ctrlCls['Denied']/ctrlCls['ttlappl'],2)*100),
                            1,fill=True, align='C')
                    pdf.set_xy(170, y)
                    pdf.multi_cell(20, 10, str(ctrlCls['Dropped']), 1,fill=True, align='C')
                    pdf.set_xy(190, y)# str(round(j['Dropped']/j['ttlappl'],2)*100)
                    if ctrlCls['ttlappl']==0:
                        pdf.multi_cell(25, 10,  "NA", 1,fill=True, align='C')
                    else:
                        pdf.multi_cell(20, 10, str(ctrlCls['Dropped']/ctrlCls['ttlappl']), 1,fill=True, align='C')
                    
                    ###
                    y=pdf.get_y()
                    pdf.set_xy(x, y)
                    pdf.set_font("Arial",  "B",size=9)
                    pdf.set_fill_color(255, 255, 255)
                    y = pdf.get_y()+10 
                    pdf.set_xy(10, y)
                    pdf.multi_cell(35,10, "",
                            1,fill=True, align='C')
                    pdf.set_xy(45, y)
                    pdf.multi_cell(25, 10, "AIR", 1,
                            fill=True, align='C')
                    pdf.set_xy(70, y)
                    pdf.multi_cell(25, 10, "DOR", 1,
                            fill=True, align='C')
                    pdf.set_xy(95, y)
                    pdf.multi_cell(25, 10, "DOI", 1,
                            fill=True, align='C')            
                    y=pdf.get_y()
                    pdf.set_xy(x, y)
                    pdf.set_font("Arial","B",size=9)
                    pdf.set_fill_color(255, 255, 255)
                    y = pdf.get_y()
                    pdf.set_xy(10, y)
                    if len(str(j['ClsLbl'])) > 20:
                        pdf.multi_cell(35, 5, str(j['ClsLbl']), 1,
                            fill=True, align='C')
                    else:
                        pdf.multi_cell(35, 10, str(j['ClsLbl']), 1,
                            fill=True, align='C')
                    pdf.set_font("Arial",size=9)
                    pdf.set_xy(45, y)
                    if j['Originations'] == None:
                        if ctrlCls['ttlappl']==0:
                            pdf.cell(25, 10,  "NA", 1,fill=True, align='C')
                        else:
                            pdf.cell(25, 10, str(round(0/j['ttlappl'],2)*100 / round(ctrlCls['Originations']/ctrlCls['ttlappl'],2)*100),1,fill=True, align='C')
                    else: 
                        if ctrlCls['ttlappl']==0:
                            pdf.cell(25, 10,  "NA", 1,fill=True, align='C')
                        else:
                            
                            origin_val =   j['Originations']/j['ttlappl']*100  
                            origin_val_vm =  ctrlCls['Originations']/ctrlCls['ttlappl']*100   
                            pdf.cell(25, 10, str(round(origin_val/origin_val_vm*100)),1,
                                fill=True, align='C')
                    pdf.set_xy(70, y)
                    if ctrlCls['ttlappl']==0:
                        pdf.cell(25, 10,  "NA", 1,fill=True, align='C')
                    elif round(ctrlCls['Denied']/ctrlCls['ttlappl'],2)*100 == 0:
                        pdf.cell(25, 10, "NA", 1,
                            fill=True, align='C')
                    else:
                        pdf.cell(25, 10, str(round(j['Denied']/j['ttlappl'],2)*100 / round(ctrlCls['Denied']/ctrlCls['ttlappl'],2)*100), 1,
                                fill=True, align='C')
                    pdf.set_xy(95, y)
                    if ctrlCls['ttlappl']==0:
                        pdf.cell(25, 10,  "NA", 1,fill=True, align='C')
                    elif round(ctrlCls['Dropped']/ctrlCls['ttlappl'],2)*100 == 0:
                        pdf.cell(25, 10, "NA", 1,
                            fill=True, align='C')
                    else:
                        pdf.cell(25, 10, str(round(j['Dropped']/j['ttlappl'],2)*100 / round(ctrlCls['Dropped']/ctrlCls['ttlappl'],2)*100), 1,
                            fill=True, align='C')

                    
                    if int(i) == int(len(rpt_data['apps']['Originations'])-1): 
                    # if pdf.page_no() == int(len(rpt_data['Dropout']))+1:
                        y=pdf.get_y()
                        pdf.set_xy(x, y)
                        pdf.set_font("Arial",  "B",size=9)
                        pdf.set_fill_color(255, 255, 255)
                        y = pdf.get_y()+15
                        pdf.set_xy(10, y)
                        # pdf.cell(75, 10, "Comment: "+rpt_data['apps']['title_comment']['comment'], border=0, ln=1, align="C") to be uncommented
                        pdf.cell(210, 5, "Comments : " , border=0, ln=1, align="L")

                        y = pdf.get_y()
                        pdf.set_xy(10, y)
                        # pdf.cell(75, 10, "Comment: "+rpt_data['apps']['title_comment']['comment'], border=0, ln=1, align="C") to be uncommented
                        pdf.multi_cell(210, 5,rpt_data['apps']['comment'] , border=0, ln=1, align="L")
                    else:
                        print("inside else ",i,"length",len(rpt_data['apps']['Originations']), len(rpt_data['apps']['Originations'])-1)
                        pass

                    #Add Footer
                    pdf.set_xy(x, y)
                     
                    # pdf.image("logo.png", 10, 8, 33)  # Add logo (x=10, y=8, width=33)
                    pdf.set_font("Arial", "B", 12)
                    # pdf.cell(0, 10, "PDF Header with Logo", border=0, ln=1, align="C")
                    pdf.set_y(300)
                    pdf.cell(0, 10, f"Page {pdf.page_no()} of {{nb}}", align="C")

        return pdf   
    except Exception as e:
        print(e)
        print(traceback.print_exc())  
        return pdf   

def generate_pdf_pricing(pdf):

    datalist =[{'istaken': 'true', 'apps': {'Dropout': {'0': {'ordCol': 1, 'ClsLbl': 'Male:White', 'ttlappl': 2462, 'Originations': 1153.0, 'Origination_with_Rate_Spread': 0, 'perct_Origination_with_Rate_Spread': 0,'Rate_Spread_Disparity_Index':198,'Rate_Spread_Average':789}, 
                                            
    '1': {'ordCol': 2, 'ClsLbl': '2 or more minority races', 'ttlappl': 1, 'Originations': 4456, 'Origination_with_Rate_Spread': 1, 'perct_Origination_with_Rate_Spread': 0,'Rate_Spread_Disparity_Index':222,'Rate_Spread_Average':786},

    '2': {'ordCol': 2, 'ClsLbl': '2 or more minority races', 'ttlappl': 1, 'Originations': 6516, 'Origination_with_Rate_Spread': 1, 'perct_Origination_with_Rate_Spread': 0,'Rate_Spread_Disparity_Index':222,'Rate_Spread_Average':789}, 

    '3': {'ordCol': 2, 'ClsLbl': '2 or more minority races', 'ttlappl': 1, 'Originations': 6555, 'Origination_with_Rate_Spread': 1, 'perct_Origination_with_Rate_Spread': 0,'Rate_Spread_Disparity_Index':222,'Rate_Spread_Average':444}, 

    '4': {'ordCol': 2, 'ClsLbl': '2 or more minority races', 'ttlappl': 1, 'Originations': 7895, 'Origination_with_Rate_Spread': 1, 'perct_Origination_with_Rate_Spread': 0,'Rate_Spread_Disparity_Index':222,'Rate_Spread_Average':556}, 

    '5': {'ordCol': 2, 'ClsLbl': '2 or more minority races', 'ttlappl': 1, 'Originations': 3216, 'Origination_with_Rate_Spread': 1, 'perct_Origination_with_Rate_Spread': 0,'Rate_Spread_Disparity_Index':222,'Rate_Spread_Average':455}, 

    '6': {'ordCol': 2, 'ClsLbl': '2 or more minority races', 'ttlappl': 1, 'Originations': 5665, 'Origination_with_Rate_Spread': 1, 'perct_Origination_with_Rate_Spread': 0,'Rate_Spread_Disparity_Index':222,'Rate_Spread_Average':556}},
    
    'title_comment':{'title':'ICICI ','comment':'Analysis and porfolio of department is completed '}},'filterSelected': " Portfolio ='Mortgage' and department='MRMedited' "},

    {'istaken': 'true', 'apps': {'Dropout': {'0': {'ordCol': 1, 'ClsLbl': 'White:Male', 'ttlappl': 2462, 'Originations': 1153, 'Origination_with_Rate_Spread': 456, 'perct_Origination_with_Rate_Spread': 1112,'Rate_Spread_Disparity_Index':198,'Rate_Spread_Average':789}, 
                                            
    '1': {'ordCol': 2, 'ClsLbl': '2 or more minority races', 'ttlappl': 1, 'Originations': 5665, 'Origination_with_Rate_Spread': 1, 'perct_Origination_with_Rate_Spread': 0,'Rate_Spread_Disparity_Index':222,'Rate_Spread_Average':556}, 
    '2': {'ordCol': 2, 'ClsLbl': '2 or more minority races', 'ttlappl': 1, 'Originations': 5665, 'Origination_with_Rate_Spread': 1, 'perct_Origination_with_Rate_Spread': 0,'Rate_Spread_Disparity_Index':222,'Rate_Spread_Average':556}, 
    '3': {'ordCol': 2, 'ClsLbl': '2 or more minority races', 'ttlappl': 1, 'Originations': 5665, 'Origination_with_Rate_Spread': 1, 'perct_Origination_with_Rate_Spread': 0,'Rate_Spread_Disparity_Index':222,'Rate_Spread_Average':556}, 
    '4': {'ordCol': 2, 'ClsLbl': '2 or more minority races', 'ttlappl': 1, 'Originations': 5665, 'Origination_with_Rate_Spread': 1, 'perct_Origination_with_Rate_Spread': 0,'Rate_Spread_Disparity_Index':222,'Rate_Spread_Average':556}},'title_comment':{'title':'ICICI','comment':'Analysis and porfolio of department is completed'}}, 'filterSelected': " Portfolio ='Mortgage' and department='MRMedited' "}]

    # x,y = 25,50
    # # pdf = FPDF(orientation = 'P', unit = 'mm', format='Legal')#PDF()
    # bank_name = "ICICI Bank"
    # title = "Overall Application Summary for "+bank_name
    # pdf.add_page()
    # pdf.set_xy(10, 100)
    # pdf.set_font("Arial", "B", 12)
    # pdf.cell(0, 10,title, border=0, ln=1, align="C")
    # # pdf.line(5)

    # y = pdf.get_y()#+10
    # pdf.cell(0, 10,"Portfolio Name:", border=0, ln=1, align="C") 

    # y = pdf.get_y()#+10
    # pdf.cell(0, 10,"Period:", border=0, ln=1, align="C")

    # y = pdf.get_y()#+10
    # pdf.cell(0, 10,"Report Date:", border=0, ln=1, align="C") 

    # ## Document Version History ##
    # x,y=25,50 
    # pdf.add_page()
    # pdf.set_font("Arial", "B", 12)
    # pdf.cell(0, 10, "Document Version History", border=0, ln=1, align="C")
    # # pdf.ln(1)  # Add a small vertical space
    
    # #1 row
    # # x,y=25,50 
    # y = pdf.get_y() 
    # pdf.set_font  ("Arial", "B", size=9)
    # pdf.set_fill_color(255, 255, 255)
    # pdf.set_xy(10, y)
    # pdf.multi_cell(35,10, "Period",
    #         1, fill=True, align='C')
    # pdf.set_xy(45, y)
    # pdf.multi_cell(35,10, "Date",
    #         1, fill=True, align='C')
    # pdf.set_xy(80, y)
    # pdf.multi_cell(35, 10,  "Author",
    #         1, fill=True, align='C')
    # pdf.set_xy(115, y)
    # pdf.multi_cell(35, 10,  "Approved By",
    #         1, fill=True, align='C')
    # pdf.set_xy(150, y)
    # pdf.multi_cell(45, 10,"Version Description",
    #         1, fill=True, align='C')
    
    # #11 
    # y=pdf.get_y()
    # pdf.set_xy(x, y) 
    # pdf.set_font("Arial", "B", size=9)
    # pdf.set_fill_color(255, 255, 255)
    # y = pdf.get_y()#+10    
    # pdf.set_font("Arial",size=9)
    # pdf.set_xy(10, y)
    # pdf.cell(35, 10, "",
    #         1, fill=True, align='C')
    # pdf.set_xy(45, y)
    # pdf.cell(35, 10, "",
    #         1, fill=True, align='C')
    # pdf.set_xy(80, y)   ##
    # pdf.multi_cell(35, 10, "",
    #         1, fill=True, align='C')
    # pdf.set_xy(115, y)
    # pdf.cell(35, 10,"",
    #         1, fill=True, align='C')
    # pdf.set_xy(150, y)
    # pdf.multi_cell(45, 10,"",
    #         1, fill=True, align='C')
    
    # ##### segment
    # x,y = 25,50
    # pdf.add_page()
    # y = pdf.get_y()+10
    # pdf.set_xy(20, y)
    # pdf.set_font("Arial", "B", 12)
    # pdf.cell(0, 10,"1. Segment", border=0, ln=1, align="L")

    # y = pdf.get_y()
    # pdf.set_font("Arial",size=9)
    # pdf.set_xy(30, y)
    # pdf.cell(0, 10,"Mortgage", border=0, ln=1, align="L") 

    # y = pdf.get_y()
    # pdf.set_xy(30, y)
    # pdf.set_font("Arial",size=9)
    # pdf.cell(0, 10,"Department", border=0, ln=1, align="L") 

    # y = pdf.get_y()
    # pdf.set_xy(30, y)
    # pdf.set_font("Arial",size=9)
    # pdf.cell(0, 10,"Product", border=0, ln=1, align="L")

    # y = pdf.get_y()
    # pdf.set_xy(20, y)
    # pdf.set_font("Arial", "B", 12)
    # pdf.cell(0, 10,"2. Fair Lending Risk Assessment", border=0, ln=1, align="L") 
    ####
    for i,rpt_data in enumerate(datalist):
        # rpt_data['title_comment'] = {'title':'check new'+str(idx),'comment':'check new comment'+str(idx)}
        ### Minority Sum ###
        Origination_values = []
        for  i,j in rpt_data['apps']['Dropout'].items():
            if i != '0':
                if j['Originations'] == None:
                    Origination_values_2 = 0
                    a = Origination_values_2
                else:
                    a = j['Originations']
                Origination_values.append(a)
        print("Origination_values",Origination_values)
        # OriginationRate_values = [round(j['Originations']/j['ttlappl'],2)*100 for i,j in rpt_data['Dropout'].items() if i != '0' ]
        Origination_with_Rate_Spread = []
        for  i,j in rpt_data['apps']['Dropout'].items():
            print("j--------------",j)
            if i != '0':
                print("j['Origination_with_Rate_Spread']",j['Origination_with_Rate_Spread'])
                if j['Origination_with_Rate_Spread'] == None:
                    Origination_values_1 = 0
                    a = Origination_values_1
                else: 
                    a = j['Origination_with_Rate_Spread']
                Origination_with_Rate_Spread.append(a)
        print("Origination_with_Rate_Spread",Origination_with_Rate_Spread)

        perct_Origination_with_Rate_Spread_values = [j['perct_Origination_with_Rate_Spread'] for i,j in rpt_data['apps']['Dropout'].items() if i != '0']

        Rate_Spread_Disparity_Index_values = [j['Rate_Spread_Disparity_Index'] for i,j in rpt_data['apps']['Dropout'].items() if i != '0']
        Rate_Spread_Average_values = [j['Rate_Spread_Average'] for i,j in rpt_data['apps']['Dropout'].items() if i != '0']
        
        x,y=25,50 
        utility = rpt_data['apps']['title_comment']['title']
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, utility, border=0, ln=1, align="C")
        pdf.ln(5)  # Add a small vertical space

        filters = rpt_data['filterSelected']
        # print("filters",filters)
        filter_list = filters.split("and")
        # print("filter_list",filter_list)
        y=pdf.get_y() 
        pdf.set_xy(x, y) 
        pdf.set_font("Arial", "B", size=9)
        pdf.set_fill_color(255, 255, 255)
        y = pdf.get_y()#+10
        pdf.set_xy(70, y)
        pdf.multi_cell(85, 10,  filter_list[0]+" and "+filter_list[1],
                0, fill=False, align='C')
        
        #1 row
        x,y=25,50 
        pdf.set_xy(x, y) 
        pdf.set_font("Arial", "B", size=9)
        pdf.set_fill_color(255, 255, 255)
        y = pdf.get_y()#+10
        pdf.set_xy(10, y)
        pdf.multi_cell(25,10, "",
                1, fill=True, align='C')
        pdf.set_xy(35, y)
        pdf.multi_cell(35,10, "Originations",
                1, fill=True, align='C')
        pdf.set_xy(70, y)
        pdf.multi_cell(35, 5,  "Origination with Rate Spread",
                1, fill=True, align='C')
        pdf.set_xy(105, y)
        pdf.multi_cell(35, 5,  "% Origination with Rate Spread",
                1, fill=True, align='C')
        pdf.set_xy(140, y)
        pdf.multi_cell(35, 5,"Rate Spread Disparity Index",
                1, fill=True, align='C')
        pdf.set_xy(175, y)
        pdf.multi_cell(35, 10,"Rate Spread Average",
                1, fill=True, align='C')
    
        #11 
        y=pdf.get_y()
        pdf.set_xy(x, y) 
        pdf.set_font("Arial", "B", size=9)
        pdf.set_fill_color(255, 255, 255)
        y = pdf.get_y()#+10
        a = "Minority"
        pdf.set_xy(10, y)
        if len(a) > 18:
            pdf.multi_cell(25, 5, "Minority",
                    1, fill=True, align='C')
        else:
            pdf.multi_cell(25, 10, "Minority",
                    1, fill=True, align='C')
        pdf.set_font("Arial",size=9)
        pdf.set_xy(35, y)
        pdf.cell(35, 10, str(sum(Origination_values)),
                1, fill=True, align='C')
        pdf.set_xy(70, y)    
        pdf.cell(35, 10, str(sum(Origination_with_Rate_Spread)),
                1, fill=True, align='C')
        pdf.set_xy(105, y)   ##
        pdf.multi_cell(35, 10, str(sum(perct_Origination_with_Rate_Spread_values)),
                1, fill=True, align='C')
        pdf.set_xy(140, y)
        pdf.cell(35, 10,str(sum(Rate_Spread_Disparity_Index_values)),
                1, fill=True, align='C')
        pdf.set_xy(175, y)
        pdf.multi_cell(35, 10,str(sum(Rate_Spread_Average_values)),
                1, fill=True, align='C')
        
        # ### New White male
        ctrlCls=rpt_data['apps']['Dropout']['0']  
        y=pdf.get_y()
        pdf.set_xy(x, y) 
        pdf.set_font("Arial", "B", size=9)
        pdf.set_fill_color(255, 255, 255)
        y = pdf.get_y()
        pdf.set_xy(10, y)
        pdf.multi_cell(25, 10, ctrlCls['ClsLbl'],
                1,fill=True, align='C')
        pdf.set_xy(35, y)
        pdf.set_font("Arial",  size=9)
        pdf.multi_cell(35, 10, str(ctrlCls['Originations']),
                1,fill=True, align='C')
        pdf.set_xy(70, y)
        pdf.multi_cell(35, 10, str(ctrlCls['Origination_with_Rate_Spread']),
                1,fill=True, align='C')
        pdf.set_xy(105, y) 
        pdf.multi_cell(35, 10,  str(ctrlCls['perct_Origination_with_Rate_Spread']),
                1,fill=True, align='C')
        pdf.set_xy(140, y)
        pdf.multi_cell(35, 10,str(ctrlCls['Rate_Spread_Disparity_Index']),
                1,fill=True, align='C')
        pdf.set_xy(175, y) 
        pdf.multi_cell(35, 10, str(ctrlCls['Rate_Spread_Average']),
                1,fill=True, align='C')
        
        #Add Footer
        pdf.set_xy(x, y)
        y = pdf.get_y()    
        pdf.set_font("Arial", "B", 12)
        pdf.ln(190)
        pdf.cell(0, 10, f"Page {pdf.page_no()} of {{nb}}", align="C")
        #####

        for i,j in rpt_data['apps']['Dropout'].items():
            print("i-------------------",i)
            print("length of dict",len(rpt_data['apps']['Dropout']))
            x,y=25,50 
            if i != '0':    
                #Add Header                
                utility = rpt_data['apps']['title_comment']['title']
                pdf.add_page()
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, utility, border=0, ln=1, align="C")
                pdf.ln(5) # Add a small vertical space

                
                y=pdf.get_y() 
                pdf.set_xy(x, y) 
                pdf.set_font("Arial", "B", size=9)
                pdf.set_fill_color(255, 255, 255)
                y = pdf.get_y()#+10
                pdf.set_xy(70, y)
                pdf.cell(75, 10,  filter_list[0]+" and "+filter_list[1],
                        0, fill=False, align='C')

                #1 row
                
                x,y=25,50
                pdf.set_xy(x, y) 
                pdf.set_font  ("Arial", "B", size=9)
                pdf.set_fill_color(255, 255, 255)
                y = pdf.get_y()#+10
                pdf.set_xy(10, y)
                pdf.multi_cell(35,10, "",
                        1, fill=True, align='C')
                pdf.set_xy(45, y)
                pdf.multi_cell(25,10, "Originations",
                        1, fill=True, align='C')
                pdf.set_xy(70, y)
                pdf.multi_cell(35, 5,  "Origination with Rate Spread",
                        1, fill=True, align='C')
                pdf.set_xy(105, y)
                pdf.multi_cell(35, 5,  "% Origination with Rate Spread",
                        1, fill=True, align='C')
                pdf.set_xy(140, y)
                pdf.multi_cell(35, 5,"Rate Spread Disparity Index",
                        1, fill=True, align='C')
                pdf.set_xy(175, y)
                pdf.multi_cell(35, 10,"Rate Spread Average",
                        1, fill=True, align='C')
                
                #11 
                print("j val--------------",j)
                y=pdf.get_y()
                pdf.set_xy(x, y) 
                pdf.set_font("Arial", "B", size=9)
                pdf.set_fill_color(255, 255, 255)
                y = pdf.get_y()#+10
                pdf.set_xy(10, y) 
                pdf.multi_cell(35, 5, str(j['ClsLbl']), 1, fill=True, align='C')
            
                pdf.set_font("Arial",size=9)
                pdf.set_xy(45, y)
                pdf.cell(25, 10, str(j['Originations']),
                        1, fill=True, align='C')
                pdf.set_xy(70, y)
                pdf.cell(35, 10, str(j['Origination_with_Rate_Spread']),
                        1, fill=True, align='C')
                pdf.set_xy(105, y)   
                pdf.multi_cell(35, 10, str(j['perct_Origination_with_Rate_Spread']),1, fill=True, align='C')
            
                pdf.set_xy(140, y)
                pdf.cell(35, 10,str(j['Rate_Spread_Disparity_Index']),
                        1, fill=True, align='C')
                pdf.set_xy(175, y)
                pdf.cell(35, 10,str(j['Rate_Spread_Average']),
                        1, fill=True, align='C')
                
                ### New White male
                x,y = 25,50
                ctrlCls=rpt_data['apps']['Dropout']['0'] 
                y=pdf.get_y()
                pdf.set_xy(x, y) 
                pdf.set_font("Arial", "B", size=9)
                pdf.set_fill_color(255, 255, 255)
                y = pdf.get_y()+10
                pdf.set_xy(10, y)
                pdf.multi_cell(35, 10, ctrlCls['ClsLbl'],
                        1,fill=True, align='C')
                pdf.set_xy(45, y)
                pdf.set_font("Arial",  size=9)
                pdf.multi_cell(25, 10, str(ctrlCls['Originations']),
                        1,fill=True, align='C')
                pdf.set_xy(70, y)
                pdf.multi_cell(35, 10, str(ctrlCls['Origination_with_Rate_Spread']),
                        1,fill=True, align='C')
                pdf.set_xy(105, y) 
                pdf.multi_cell(35, 10,  str(ctrlCls['perct_Origination_with_Rate_Spread']),
                        1,fill=True, align='C')
                pdf.set_xy(140, y)
                pdf.multi_cell(35, 10,str(ctrlCls['Rate_Spread_Disparity_Index']),
                        1,fill=True, align='C')
                pdf.set_xy(175, y) 
                pdf.multi_cell(35, 10, str(ctrlCls['Rate_Spread_Average']),
                        1,fill=True, align='C')
            
                
                # ###
                # pdf.line(15, y, 310, y)
                if int(i) == int(len(rpt_data['apps']['Dropout'])-1):
                    print("inside if",i,"length",len(rpt_data['apps']['Dropout']))
                    print("pdf.get_y()",pdf.get_y())
                # if pdf.page_no() == int(len(rpt_data['Dropout']))+1:
                    y=pdf.get_y()
                    pdf.set_xy(x, y)
                    pdf.set_font("Arial",  "B",size=9)
                    pdf.set_fill_color(255, 255, 255)
                    y = pdf.get_y()+10 
                    pdf.set_xy(50, y)
                    pdf.cell(75, 10, "Comment: "+rpt_data['apps']['title_comment']['comment'], border=0, ln=1, align="C")
                else:
                    print("inside else ",i,"length",len(rpt_data['apps']['Dropout']), len(rpt_data['apps']['Dropout'])-1)
                    pass

                #Add Footer
                pdf.set_xy(x, y)
                y = pdf.get_y()
                # pdf.image("logo.png", 10, 8, 33)  # Add logo (x=10, y=8, width=33)
                pdf.set_font("Arial", "B", 12)
                # pdf.cell(0, 10, "PDF Header with Logo", border=0, ln=1, align="C")
                pdf.ln(190)
                pdf.cell(0, 10, f"Page {pdf.page_no()} of {{nb}}", align="C")

    return pdf    
    # pdf.output(os.path.join(
    #         BASE_DIR, "static/medtable_from_dict_pricing.pdf"))    
    # return JsonResponse({'msg':"PDF Generated successfully"})  
     
def generate_pdf_marketing(pdf):

    datalist =[{'istaken': 'true', 'apps': {'Dropout': {'0': {'ordCol': 1, 'ClsLbl': 'Male:White', 'Applications': 2462, 'Applications_Rate': 1153.0, 'Peer_Applications': 4560, 'Peer_Applications_Rate': 0,'Differene_in_perct':198,'Application_Deficit_perct':789}, 
                                            
    '1': {'ordCol': 2, 'ClsLbl': 'Hispanic or more', 'Applications': 4566, 'Applications_Rate': 4456, 'Peer_Applications': 1, 'Peer_Applications_Rate': 0,'Differene_in_perct':222,'Application_Deficit_perct':786},
 
    '2': {'ordCol': 2, 'ClsLbl': '2 or more minority races', 'Applications': 5556, 'Applications_Rate': 6516, 'Peer_Applications': 1, 'Peer_Applications_Rate': 0,'Differene_in_perct':222,'Application_Deficit_perct':789}, 

    '3': {'ordCol': 2, 'ClsLbl': 'ethnicity valueable', 'Applications': 4896, 'Applications_Rate': 4786, 'Peer_Applications': 7553, 'Peer_Applications_Rate': 5555,'Differene_in_perct':78,'Application_Deficit_perct':123}},
    
    'title_comment':{'title':'HDFC ','comment':'Analysis and porfolio of department is completed '}},'filterSelected': "Control Class : derived_race = 'White' and derived_sex = 'Male' , Filter : Portfolio ='Mortgage' and department='1'"},

    {'istaken': 'true', 'apps': {'Dropout': {'0': {'ordCol': 1, 'ClsLbl': 'Male:White', 'Applications': 2462, 'Applications_Rate': 1153.0, 'Peer_Applications': 4560, 'Peer_Applications_Rate': 0,'Differene_in_perct':198,'Application_Deficit_perct':789}, 
                                            
    '1': {'ordCol': 2, 'ClsLbl': 'Hispanic or more', 'Applications': 2366, 'Applications_Rate': 7896, 'Peer_Applications': 2233, 'Peer_Applications_Rate': 1566,'Differene_in_perct':2333,'Application_Deficit_perct':5236}, 

    '2': {'ordCol': 2, 'ClsLbl': 'Hispanic or more', 'Applications': 3232, 'Applications_Rate': 5623, 'Peer_Applications': 7523, 'Peer_Applications_Rate': 1222,'Differene_in_perct':888,'Application_Deficit_perct':2113}, 

    '3':  {'ordCol': 2, 'ClsLbl': 'Hispanic or more', 'Applications': 3232, 'Applications_Rate': 5623, 'Peer_Applications': 7523, 'Peer_Applications_Rate': 1222,'Differene_in_perct':888,'Application_Deficit_perct':2113}},'title_comment':{'title':'ICICI','comment':'Analysis and porfolio of department is completed'}}, 'filterSelected': " Control Class : derived_race = 'White' and derived_sex = 'Male' , Filter : Portfolio ='Mortgage' and department='1'"}]

    # x,y = 25,50
    # # pdf = FPDF(orientation = 'P', unit = 'mm', format='Legal')#PDF()
    # bank_name = "ICICI Bank"
    # title = "Overall Application Summary for "+bank_name
    # pdf.add_page()
    # pdf.set_xy(10, 100)
    # pdf.set_font("Arial", "B", 12)
    # pdf.cell(0, 10,title, border=0, ln=1, align="C")
    # # pdf.line(5)

    # y = pdf.get_y()#+10
    # pdf.cell(0, 10,"Portfolio Name:", border=0, ln=1, align="C") 

    # y = pdf.get_y()#+10
    # pdf.cell(0, 10,"Period:", border=0, ln=1, align="C")

    # y = pdf.get_y()#+10
    # pdf.cell(0, 10,"Report Date:", border=0, ln=1, align="C") 

    # ## Document Version History ##
    # x,y=25,50 
    # pdf.add_page()
    # pdf.set_font("Arial", "B", 12)
    # pdf.cell(0, 10, "Document Version History", border=0, ln=1, align="C")
    # # pdf.ln(1)  # Add a small vertical space
    
    # #1 row
    # # x,y=25,50 
    # y = pdf.get_y() 
    # pdf.set_font  ("Arial", "B", size=9)
    # pdf.set_fill_color(255, 255, 255)
    # pdf.set_xy(10, y)
    # pdf.multi_cell(35,10, "Period",
    #         1, fill=True, align='C')
    # pdf.set_xy(45, y)
    # pdf.multi_cell(35,10, "Date",
    #         1, fill=True, align='C')
    # pdf.set_xy(80, y)
    # pdf.multi_cell(35, 10,  "Author",
    #         1, fill=True, align='C')
    # pdf.set_xy(115, y)
    # pdf.multi_cell(35, 10,  "Approved By",
    #         1, fill=True, align='C')
    # pdf.set_xy(150, y)
    # pdf.multi_cell(45, 10,"Version Description",
    #         1, fill=True, align='C')
    
    # #11 
    # y=pdf.get_y()
    # pdf.set_xy(x, y) 
    # pdf.set_font("Arial", "B", size=9)
    # pdf.set_fill_color(255, 255, 255)
    # y = pdf.get_y()#+10    
    # pdf.set_font("Arial",size=9)
    # pdf.set_xy(10, y)
    # pdf.cell(35, 10, "",
    #         1, fill=True, align='C')
    # pdf.set_xy(45, y)
    # pdf.cell(35, 10, "",
    #         1, fill=True, align='C')
    # pdf.set_xy(80, y)   ##
    # pdf.multi_cell(35, 10, "",
    #         1, fill=True, align='C')
    # pdf.set_xy(115, y)
    # pdf.cell(35, 10,"",
    #         1, fill=True, align='C')
    # pdf.set_xy(150, y)
    # pdf.multi_cell(45, 10,"",
    #         1, fill=True, align='C')
    
    # ##### segment
    # x,y = 25,50
    # pdf.add_page()
    # y = pdf.get_y()+10
    # pdf.set_xy(20, y)
    # pdf.set_font("Arial", "B", 12)
    # pdf.cell(0, 10,"1. Segment", border=0, ln=1, align="L")

    # y = pdf.get_y()
    # pdf.set_font("Arial",size=9)
    # pdf.set_xy(30, y)
    # pdf.cell(0, 10,"Mortgage", border=0, ln=1, align="L") 

    # y = pdf.get_y()
    # pdf.set_xy(30, y)
    # pdf.set_font("Arial",size=9)
    # pdf.cell(0, 10,"Department", border=0, ln=1, align="L") 

    # y = pdf.get_y()
    # pdf.set_xy(30, y)
    # pdf.set_font("Arial",size=9)
    # pdf.cell(0, 10,"Product", border=0, ln=1, align="L")

    # y = pdf.get_y()
    # pdf.set_xy(20, y)
    # pdf.set_font("Arial", "B", 12)
    # pdf.cell(0, 10,"2. Fair Lending Risk Assessment", border=0, ln=1, align="L") 
    ####
    for i,rpt_data in enumerate(datalist):
        # rpt_data['title_comment'] = {'title':'check new'+str(idx),'comment':'check new comment'+str(idx)}
        ### Minority Sum ###
        Applications = []
        for  i,j in rpt_data['apps']['Dropout'].items():
            if i != '0':
                if j['Applications'] == None:
                    Origination_values_2 = 0
                    a = Origination_values_2
                else:
                    a = j['Applications']
                Applications.append(a)
        print("Applications",Applications)
        Applications_Rate = []
        for  i,j in rpt_data['apps']['Dropout'].items():
            if i != '0':
                if j['Applications_Rate'] == None:
                    Origination_values_2 = 0
                    a = Origination_values_2
                else:
                    a = j['Applications_Rate']
                Applications_Rate.append(a)
        print("Applications_Rate",Applications_Rate)
        # OriginationRate_values = [round(j['Originations']/j['ttlappl'],2)*100 for i,j in rpt_data['Dropout'].items() if i != '0' ]
        Peer_Applications = []
        for  i,j in rpt_data['apps']['Dropout'].items():
            print("j--------------",j)
            if i != '0':
                print("j['Peer Applications']",j['Peer_Applications'])
                if j['Peer_Applications'] == None:
                    Origination_values_1 = 0
                    a = Origination_values_1
                else: 
                    a = j['Peer_Applications']
                Peer_Applications.append(a)
        print("Origination_with_Rate_Spread",Peer_Applications)

        Peer_Applications_Rate = [j['Peer_Applications_Rate'] for i,j in rpt_data['apps']['Dropout'].items() if i != '0']

        Differene_in_perct = [j['Differene_in_perct'] for i,j in rpt_data['apps']['Dropout'].items() if i != '0']
        Application_Deficit_perct = [j['Application_Deficit_perct'] for i,j in rpt_data['apps']['Dropout'].items() if i != '0']
        
        x,y=25,50 
        utility = rpt_data['apps']['title_comment']['title']
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, utility, border=0, ln=1, align="C")
        pdf.ln(5)  # Add a small vertical space

        filters = rpt_data['filterSelected']
        # print("filters",filters)
        filter_list = filters.split("and")
        # print("filter_list",filter_list)
        y=pdf.get_y() 
        pdf.set_xy(x, y) 
        pdf.set_font("Arial", "B", size=9)
        pdf.set_fill_color(255, 255, 255)
        y = pdf.get_y()#+10
        pdf.set_xy(70, y)
        pdf.multi_cell(85, 10,  filter_list[0]+" and "+filter_list[1],
                0, fill=False, align='C')
        
        #1 row
        x,y=25,50 
        pdf.set_xy(x, y) 
        pdf.set_font("Arial", "B", size=9)
        pdf.set_fill_color(255, 255, 255)
        y = pdf.get_y()#+10
        pdf.set_xy(5, y)
        pdf.multi_cell(25,10, "",
                1, fill=True, align='C')
        pdf.set_xy(30, y)
        pdf.multi_cell(25,10, "Applications",
                1, fill=True, align='C')
        pdf.set_xy(55, y)
        pdf.multi_cell(35, 10,  "Applications Rate",
                1, fill=True, align='C')
        pdf.set_xy(90, y)
        pdf.multi_cell(35, 10,  "Peer Applications",
                1, fill=True, align='C')
        pdf.set_xy(125, y)
        pdf.multi_cell(35, 5,"Peer Applications Rate",
                1, fill=True, align='C')
        pdf.set_xy(160, y)
        pdf.multi_cell(25, 10,"Differene in %",
                1, fill=True, align='C')
        pdf.set_xy(185, y)
        pdf.multi_cell(25, 5,"Application Deficit %",
                1, fill=True, align='C')
            
    
        #11 
        y=pdf.get_y()
        pdf.set_xy(x, y) 
        pdf.set_font("Arial", "B", size=9)
        pdf.set_fill_color(255, 255, 255)
        y = pdf.get_y()#+10
        a = "Minority"
        pdf.set_xy(5, y)
        if len(a) > 18:
            pdf.multi_cell(25, 5, "Minority",
                    1, fill=True, align='C')
        else:
            pdf.multi_cell(25, 10, "Minority",
                    1, fill=True, align='C')
        pdf.set_font("Arial",size=9)
        pdf.set_xy(30, y)
        pdf.cell(25, 10, str(sum(Applications)),
                1, fill=True, align='C')
        pdf.set_xy(55, y)    
        pdf.cell(35, 10, str(sum(Applications_Rate)),
                1, fill=True, align='C')
        pdf.set_xy(90, y)   ##
        pdf.multi_cell(35, 10, str(sum(Peer_Applications)),
                1, fill=True, align='C')
        pdf.set_xy(125, y)
        pdf.cell(35, 10,str(sum(Peer_Applications_Rate)),
                1, fill=True, align='C')
        pdf.set_xy(160, y)
        pdf.multi_cell(25, 10,str(sum(Differene_in_perct)),
                1, fill=True, align='C')
        pdf.set_xy(185, y)
        pdf.multi_cell(25, 10,str(sum(Application_Deficit_perct)),
                1, fill=True, align='C')
        
        # ### New White male
        ctrlCls=rpt_data['apps']['Dropout']['0']  
        y=pdf.get_y()
        pdf.set_xy(x, y) 
        pdf.set_font("Arial", "B", size=9)
        pdf.set_fill_color(255, 255, 255)
        y = pdf.get_y()
        pdf.set_xy(5, y)
        pdf.multi_cell(25, 10, ctrlCls['ClsLbl'],
                1,fill=True, align='C')
        pdf.set_xy(30, y)
        pdf.set_font("Arial",  size=9)
        pdf.multi_cell(25, 10, str(ctrlCls['Applications']),
                1,fill=True, align='C')
        pdf.set_xy(55, y)
        pdf.multi_cell(35, 10, str(ctrlCls['Applications_Rate']),
                1,fill=True, align='C')
        pdf.set_xy(90, y) 
        pdf.multi_cell(35, 10,  str(ctrlCls['Peer_Applications']),
                1,fill=True, align='C')
        pdf.set_xy(125, y)
        pdf.multi_cell(35, 10,str(ctrlCls['Peer_Applications_Rate']),
                1,fill=True, align='C')
        pdf.set_xy(160, y) 
        pdf.multi_cell(25, 10, str(ctrlCls['Differene_in_perct']),
                1,fill=True, align='C')
        pdf.set_xy(185, y) 
        pdf.multi_cell(25, 10, str(ctrlCls['Application_Deficit_perct']),
                1,fill=True, align='C')
        
        #Add Footer
        pdf.set_xy(x, y)
        y = pdf.get_y()    
        pdf.set_font("Arial", "B", 12)
        pdf.ln(190)
        pdf.cell(0, 10, f"Page {pdf.page_no()} of {{nb}}", align="C")
        #####

        for i,j in rpt_data['apps']['Dropout'].items():
            print("i-------------------",i)
            print("length of dict",len(rpt_data['apps']['Dropout']))
            x,y=25,50 
            if i != '0':    
                #Add Header                
                utility = rpt_data['apps']['title_comment']['title']
                pdf.add_page()
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, utility, border=0, ln=1, align="C")
                pdf.ln(5) # Add a small vertical space

                
                y=pdf.get_y() 
                pdf.set_xy(x, y) 
                pdf.set_font("Arial", "B", size=9)
                pdf.set_fill_color(255, 255, 255)
                y = pdf.get_y()#+10
                pdf.set_xy(70, y)
                pdf.cell(75, 10,  filter_list[0]+" and "+filter_list[1],
                        0, fill=False, align='C')

                #1 row
                
                x,y=25,50
                pdf.set_xy(x, y) 
                pdf.set_font  ("Arial", "B", size=9)
                pdf.set_fill_color(255, 255, 255)
                y = pdf.get_y()#+10
                pdf.set_xy(5, y)
                pdf.multi_cell(25,10, "",
                        1, fill=True, align='C')
                pdf.set_xy(30, y)
                pdf.multi_cell(25,10, "Applications",
                        1, fill=True, align='C')
                pdf.set_xy(55, y)
                pdf.multi_cell(35, 10,  "Applications Rate",
                        1, fill=True, align='C')
                pdf.set_xy(90, y)
                pdf.multi_cell(35, 10,  "Peer Applications",
                        1, fill=True, align='C')
                pdf.set_xy(125, y)
                pdf.multi_cell(35, 5,"Peer Applications Rate",
                        1, fill=True, align='C')
                pdf.set_xy(160, y)
                pdf.multi_cell(25, 10,"Differene in %",
                        1, fill=True, align='C')
                pdf.set_xy(185, y)
                pdf.multi_cell(25, 5,"Application Deficit %",
                        1, fill=True, align='C')
                
                #11 
                print("j val--------------",j)
                y=pdf.get_y()
                pdf.set_xy(x, y) 
                pdf.set_font("Arial", "B", size=9)
                pdf.set_fill_color(255, 255, 255)
                y = pdf.get_y()#+10
                pdf.set_xy(5, y) 
                pdf.multi_cell(25, 5, str(j['ClsLbl']), 1, fill=True, align='C')
            
                pdf.set_font("Arial",size=9)
                pdf.set_xy(30, y)
                pdf.cell(25, 10, str(j['Applications']),
                        1, fill=True, align='C')
                pdf.set_xy(55, y)
                pdf.cell(35, 10, str(j['Applications_Rate']),
                        1, fill=True, align='C')
                pdf.set_xy(90, y)   
                pdf.multi_cell(35, 10, str(j['Peer_Applications']),1, fill=True, align='C')
            
                pdf.set_xy(125, y)
                pdf.cell(35, 10,str(j['Peer_Applications_Rate']),
                        1, fill=True, align='C')
                pdf.set_xy(160, y)
                pdf.cell(25, 10,str(j['Differene_in_perct']),
                        1, fill=True, align='C')
                pdf.set_xy(185, y)
                pdf.cell(25, 10,str(j['Application_Deficit_perct']),
                        1, fill=True, align='C')
                
                ### New White male
                x,y = 25,50
                ctrlCls=rpt_data['apps']['Dropout']['0'] 
                y=pdf.get_y()
                pdf.set_xy(x, y) 
                pdf.set_font("Arial", "B", size=9)
                pdf.set_fill_color(255, 255, 255)
                y = pdf.get_y()+10
                pdf.set_xy(5, y)
                pdf.multi_cell(25, 10, ctrlCls['ClsLbl'],
                        1,fill=True, align='C')
                pdf.set_xy(30, y)
                pdf.set_font("Arial",  size=9)
                pdf.multi_cell(25, 10, str(ctrlCls['Applications']),
                        1,fill=True, align='C')
                pdf.set_xy(55, y)
                pdf.multi_cell(35, 10, str(ctrlCls['Applications_Rate']),
                        1,fill=True, align='C')
                pdf.set_xy(90, y) 
                pdf.multi_cell(35, 10,  str(ctrlCls['Peer_Applications']),
                        1,fill=True, align='C')
                pdf.set_xy(125, y)
                pdf.multi_cell(35, 10,str(ctrlCls['Peer_Applications_Rate']),
                        1,fill=True, align='C')
                pdf.set_xy(160, y) 
                pdf.multi_cell(25, 10, str(ctrlCls['Differene_in_perct']),
                        1,fill=True, align='C')
                pdf.set_xy(185, y) 
                pdf.multi_cell(25, 10, str(ctrlCls['Application_Deficit_perct']),
                        1,fill=True, align='C')
            
                
                # ###
                # pdf.line(15, y, 310, y)
                if int(i) == int(len(rpt_data['apps']['Dropout'])-1):
                    print("inside if",i,"length",len(rpt_data['apps']['Dropout']))
                    print("pdf.get_y()",pdf.get_y())
                # if pdf.page_no() == int(len(rpt_data['Dropout']))+1:
                    y=pdf.get_y()
                    pdf.set_xy(x, y)
                    pdf.set_font("Arial",  "B",size=9)
                    pdf.set_fill_color(255, 255, 255)
                    y = pdf.get_y()+10 
                    pdf.set_xy(50, y)
                    pdf.cell(75, 10, "Comment: "+rpt_data['apps']['title_comment']['comment'], border=0, ln=1, align="C")
                else:
                    print("inside else ",i,"length",len(rpt_data['apps']['Dropout']), len(rpt_data['apps']['Dropout'])-1)
                    pass

                #Add Footer
                pdf.set_xy(x, y)
                y = pdf.get_y()
                # pdf.image("logo.png", 10, 8, 33)  # Add logo (x=10, y=8, width=33)
                pdf.set_font("Arial", "B", 12)
                # pdf.cell(0, 10, "PDF Header with Logo", border=0, ln=1, align="C")
                pdf.ln(190)
                pdf.cell(0, 10, f"Page {pdf.page_no()} of {{nb}}", align="C")

    return pdf  

def get_Filter_Selected(request):
    try: 
        api_url = getFLAPIURL()+'get_Filter_Selected/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year','2003'),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'utility':request.GET.get('utility',''),
            'segNm':request.GET.get('segNm',''),
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'istaken':api_data['istaken'], 'filters':api_data['filters'],'CtrlClsSelected':api_data['CtrlClsSelected'] ,'segNm':api_data['segNm']})
    except Exception as e:
        print('updateaccess ',e,traceback.print_exc())
        return JsonResponse({'istaken':'false'})

def delete_Filter_Selected(request):
    try: 
        api_url = getFLAPIURL()+'delete_Filter_Selected/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  ,  
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'utility':request.GET.get('utility',''),
            'segNm':request.GET.get('segNm',''),
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'istaken':api_data['istaken']})
    except Exception as e:
        print('updateaccess ',e,traceback.print_exc())
        return JsonResponse({'istaken':'false'})

def Fl_titleCommentSave(request):
    print("request data title",request.GET)
    title = request.GET.get('title','false')
    comments = request.GET.get('comments','false')
    utility = request.GET.get('utility','false')

    api_url=getFLAPIURL()+"FlReportTitleCommentAPI/"       
    data_to_save={ 
        'comment':comments,
        'title':title,
        'utility':utility,
        'portfolio':'Mortgage',
        'department':request.session['dept'],
        'addedby':request.session['uid']
    } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)         
    api_data=response.json() 
    return JsonResponse({"data":api_data})
 
def Redlining_Map(request):
    print('submitted')
    rb_Filter=''
    chkisPeer=''
    rb_Filter2=''
    chkisPeer2=''
    try:
        
        rb_Filter = request.POST.get('ddlFilter','TOT_MALE') 
        chkisPeer=request.POST.get('chkisPeer','n') 
        rb_Filter2 = request.POST.get('ddlFilter2','TOT_MALE') 
        chkisPeer2=request.POST.get('chkisPeer2','n')
        print('rb_Filter2 ',rb_Filter2)
    except Exception as e:
        print('CompareOnMap ',e,traceback.print_exc())
    
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
        'utility':'Dashboard-Map',
        'dept':str(request.session['dept'] )
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data=response.json()   

    api_url = getFLAPIURL()+'get_CountyMedianIncome/' 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }       
    data_params={
        'Portfolio':'Mortgage',
        'Dept':str(request.session['dept']),
        'uid':request.session['uid'],
        'filter_col':'Median',
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data_bank=response.json()        
         
        #return JsonResponse({'PeerBanks':api_data['PeerBanks'],'States':api_data['States'],'Counties':api_data['Counties']})

    return render(request, 'fl_map_jq-redlining.html',{'rb_Filter':rb_Filter,'chkisPeer':chkisPeer,'rb_Filter2':rb_Filter2,'chkisPeer2':chkisPeer2,'arrCols':arrCols,'ctrl_cols':ctrl_class_data['ColumnName'],'querybldrcols':api_data['gridDttypes'],'CountyLatLong':api_data_bank['CountyLatLong'],'peerlei':api_data['peerlei']})


def Marketing_Map(request):
    print('submitted')
    rb_Filter=''
    chkisPeer=''
    rb_Filter2=''
    chkisPeer2=''
    try:
        
        rb_Filter = request.POST.get('ddlFilter','TOT_MALE') 
        chkisPeer=request.POST.get('chkisPeer','n') 
        rb_Filter2 = request.POST.get('ddlFilter2','TOT_MALE') 
        chkisPeer2=request.POST.get('chkisPeer2','n')
        print('rb_Filter2 ',rb_Filter2)
    except Exception as e:
        print('Marketing_Map ',e,traceback.print_exc())
    
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
        'utility':'Dashboard-Map',
        'dept':str(request.session['dept'] )
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data=response.json()   

    api_url = getFLAPIURL()+'get_CountyMedianIncome/' 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }       
    data_params={
        'Portfolio':'Mortgage',
        'Dept':str(request.session['dept']),
        'uid':request.session['uid'],
        'filter_col':'Median',
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data_bank=response.json()        
         
        #return JsonResponse({'PeerBanks':api_data['PeerBanks'],'States':api_data['States'],'Counties':api_data['Counties']})

    return render(request, 'fl_map_jq-marketing.html',{'rb_Filter':rb_Filter,'chkisPeer':chkisPeer,'rb_Filter2':rb_Filter2,'chkisPeer2':chkisPeer2,'arrCols':arrCols,'ctrl_cols':ctrl_class_data['ColumnName'],'querybldrcols':api_data['gridDttypes'],'CountyLatLong':api_data_bank['CountyLatLong'],'peerlei':api_data['peerlei']})


def question_ans(request):
    try:
        print("post data",request.POST)
        if request.method == 'POST':
            # Initialize an empty dictionary to store form data
            form_data = {}

            # Get data from request.POST or request.FILES if files are included
            question = request.POST.get('question')
            questionNumber = request.POST.get('questionNumber')
            answer_type= request.POST.get('answer_type')
            
            sub_question = request.POST.get('sub_question')
            sub_answer_type= request.POST.get('sub_answer_type')
            sub_options_value=request.POST.getlist('sub_options_value[]')

            print("sub_question , sub_answer_type , sub_options_value",sub_question,sub_answer_type,sub_options_value)

            # form_data['textarea_input'] = request.POST.get('textareaInput')
            # form_data['dropdown_input'] = request.POST.get('dropdownInput')
            # form_data['radio_input'] = request.POST.get('radioInput')

            print("data",question,answer_type)
            if answer_type =='options':
                options_value=request.POST.getlist('options_value[]')
                print("options_value",options_value)
                headers=None
                numRows=None
                numCols=None
            elif answer_type == 'radio':
                options_value=request.POST.getlist('options_value[]')
                headers=None
                numRows=None
                numCols=None
            elif answer_type == 'paragraph':
                answer_type= answer_type    
                options_value=None
                headers=None
                numRows=None
                numCols=None
            elif answer_type == 'text':
                answer_type= answer_type
                options_value=None
                headers=None
                numRows=None
                numCols=None
            elif answer_type == 'table':
                headers=request.POST.getlist('headers[]')
                numRows=request.POST.get('numRows')
                numCols=request.POST.get('numCols')
                options_value=None
            elif answer_type == 'sub_question':
                answer_type= answer_type
                options_value=None
                headers=None
                numRows=None
                numCols=None
            else:
                pass

            if sub_answer_type =='options':
                sub_options_value=request.POST.getlist('sub_options_value[]')
                print("sub_options_value",sub_options_value)
            elif sub_answer_type == 'radio':
                sub_options_value=request.POST.getlist('sub_options_value[]')
            elif sub_answer_type == 'paragraph':
                sub_answer_type= sub_answer_type    
                sub_options_value=None
            elif sub_answer_type == 'text':
                sub_answer_type= sub_answer_type
                sub_options_value=None
            else:
                pass

            api_url=getFLAPIURL()+"add_question_ans/"       
            params={'question':question,
                    'questionNumber':questionNumber,                    
                'answer_type':answer_type,
                'options_value':options_value,
                'sub_question':sub_question,
                'sub_answer_type':sub_answer_type,
                'sub_options_value':sub_options_value,
                'headers':headers,
                'numRows':numRows,
                'numCols':numCols,
                'uid':request.session['uid']
                } 
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(api_url, data= json.dumps(params),headers=header)         
            api_data=response.json()
            print("api_data",api_data)

            return JsonResponse(api_data)
            

        return render(request,'question_ans.html')
    except Exception as e:
        print('question_ans is ',e)
        print('question_ans traceback is ', traceback.print_exc())  


def question_list(request):
    print("post data",request.POST)

    if request.method == 'POST':
        data = json.loads(request.body)
        print("data",data)
        
        # questions = data.get('questions', {})
        # sub_questions = data.get('sub_questions', {})
        # print("questions",questions)
        # print("sub_questions",sub_questions)
        
        # # Loop through the POST data
        # for key, value in request.POST.items():
        #     # Filter only keys that start with 'form_data['
        #     if key.startswith('form_data['):
        #         # Extract the number inside the brackets, e.g., 'form_data[3]' -> 3
        #         index = key.split('[')[1].split(']')[0]  # Get the number inside '[]'
        #         form_data[index] = value  # Store the value by index

        # # Debugging: See the processed form data
        # print("Processed form data:", form_data)

        # for question_id, answer in form_data.items():
        #     # Skipping undefined and csrfmiddlewaretoken
        #     # if key != 'csrfmiddlewaretoken' and key != 'undefined':
        #     #     print(f"Key: {key}, Value: {value}")
        #     #     question = Question_Answer_Master.objects.get(id=question_id)
        #     if answer and question_id != 'csrfmiddlewaretoken' and question_id != 'undefined':  # Check if the answer is not empty
        #         question_obj = QuestionAnswerMaster.objects.get(question_id=int(question_id))
        #         question_obj.answer_text=answer
        #         question_obj.save()
        # print("saved")

        api_url=getFLAPIURL()+"question_list/"       
        params={'questions_ans':data,
                'uid':request.session['uid']
                } 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url,data=json.dumps(params),headers=header)       
        api_data=response.json()
        print("api_data",api_data)
        return JsonResponse(api_data)
    
    api_url=getFLAPIURL()+"question_list/"       
    
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url,headers=header)       
    api_data=response.json()
    print("api_data",api_data)

    api_url=getFLAPIURL()+"get_question_options/"       
    
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url,headers=header)       
    api_data_options=response.json()
    print("api_data options",api_data_options)


    ## get question table

    api_url=getFLAPIURL()+"get_question_table/"       
    
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url,headers=header)       
    api_data_table=response.json()
    
    # number_of_columns = 0
    # number_of_rows = 0

    # for item in api_data_table:
    #     if item.question_tab == question_id:
    #         number_of_columns = item.number_of_columns
    #         number_of_rows = item.number_of_rows
    #         break  # Stop after finding the first matching item
    
    # for table in api_data_table:
    #     table['table_row'] = table['table_row'] if table['table_row'] is not None else 0
    #     table['table_column'] = table['table_column'] if table['table_column'] is not None else 0
    #     # Generate range objects now that table_row and table_column are guaranteed to be integers
    #     table['row_range'] = range(table['table_row'])
    #     table['col_range'] = range(table['table_column'])


    # for entry in api_data_table:
    #     entry['row_range'] = range(entry['table_row'])
    #     entry['column_range'] = range(entry['table_column'])

    # for table in api_data_table:
    #     table["row_range"] = range(table["table_row"] + int(1))
    #     table["column_range"] = range(table["table_column"])

    # row_data=[
    # {'question_table_id': 1033, 'table_header': 'test200', 'table_row': 3, 'table_column': 2, 'question_tab': 3074},
    # {'question_table_id': 1037, 'table_header': 'A', 'table_row': 3, 'table_column': 4, 'question_tab': 3076},
    # ]
    print("api_data_table",api_data_table)    

    # Extract unique question_tab values from the data
    question_tab_values = list(set(item['question_tab'] for item in api_data_table))
    print("question_tab_values:", question_tab_values)

    # Get only one entry for each unique question_tab
    seen_tabs = set()
    row_data = []
    for item in api_data_table:
        if item['question_tab'] not in seen_tabs:
            row_data.append(item)
            seen_tabs.add(item['question_tab'])

    print("row_data:", row_data)

    ##sub question
    api_url=getFLAPIURL()+"sub_question_list/"       
    
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url,headers=header)       
    sub_question_list=response.json()
    print("sub_question_list",sub_question_list)

    api_url=getFLAPIURL()+"get_sub_question_options/"       
    
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url,headers=header)       
    get_sub_question_options=response.json()
    print("get_sub_question_options",get_sub_question_options)

    # times=times()
    # print("times",times)
    return render(request, 'question_list.html', {'questions': api_data,'options':api_data_options,
                    'sub_question_list':sub_question_list,'get_sub_question_options':get_sub_question_options,'table':api_data_table,
                    'row_data':row_data})


def pair_class(request):
    try:
        Protected_class_id=UserCategory.objects.get(uc_label='Protected Class Tester')
        Prohibited_class_id=UserCategory.objects.get(uc_label='Prohibited Class Tester')

        print("Protected_class_id",Protected_class_id)
        print("Prohibited_class_id",Prohibited_class_id)
        protected_obj=Users.objects.filter(uc_aid=Protected_class_id.uc_aid)
        print("protected_obj",protected_obj)
        Prohibited_obj=Users.objects.filter(uc_aid=Prohibited_class_id.uc_aid)
        print("Prohibited_obj",Prohibited_obj)
        context={'protected_obj':protected_obj,'Prohibited_obj':Prohibited_obj}
        return render(request, 'pair_class.html',context)
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc()) 


def save_pairs(request):
    try:
       if request.method == 'POST':
        data = json.loads(request.body)
        pairs = data.get('pairs', [])
        print("pairs",pairs)
        for pair in pairs:
            # Extract values from the request
            pair_label = pair.get('pair_label')  # e.g., "Pair 1"
            protected_class = pair.get('protected_class')
            prohibited_class = pair.get('prohibited_class')
            rv_id="rv_1"
            Pairmodel.objects.create(
                pair_label=pair_label,
                protected_class=protected_class,
                prohibited_class=prohibited_class,
                rv_id=rv_id
            )
            print("saved")
        return JsonResponse({'message': 'Data saved successfully!'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc()) 
        


def fl_addnewuser(request):
    try: 
        
        return render(request, 'fl_addnewuser.html')
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc()) 



def fl_addUser(request):
    try:

        uname =request.GET.get('uname', 'False') 
        lname=request.GET.get('lname', 'False')   
        fname=request.GET.get('fname', 'False')     
        email=request.GET.get('email', 'False')   
    
        utype=request.GET.get('class')
        print("utype",utype)

        api_url=getFLAPIURL()+"fl_addUser/"       
        params={
                'uname':uname,
                'lname':lname,
                'fname':fname,
                'email':email,
                'utype':utype,
                'uid':request.session['uid']
            } 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(params),headers=header)         
        api_data=response.json()
        print("api_data",api_data)
       


        return JsonResponse({"api_data":api_data})
 
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc()) 


def fl_User_list(request):
    try:
        Protected_class_id=UserCategory.objects.get(uc_label='Protected Class Tester')
        Prohibited_class_id=UserCategory.objects.get(uc_label='Prohibited Class Tester')

        print("Protected_class_id",Protected_class_id)
        print("Prohibited_class_id",Prohibited_class_id)
        protected_obj=Users.objects.filter(uc_aid=Protected_class_id.uc_aid)
        Prohibited_obj=Users.objects.filter(uc_aid=Prohibited_class_id.uc_aid)
        user_obj = protected_obj | Prohibited_obj

        print("user_obj", user_obj)
        context={'users':user_obj}
        return render(request, 'fl_User_list.html',context)
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc()) 



def fetch_review_cycle_data(request):
    api_url=getFLAPIURL()+"fetch_review_cycle_data/"       
    
    params={
                'review_cycle':'rv_1' 
            } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(params),headers=header)     
    api_data=response.json()
    print("api_data",type(api_data['questions']))
            
    # answer_range = range(api_data['max_answers'])
    # print("answer_range",answer_range)
    

    context = {"questions": api_data['questions'],'user_ids':api_data['user_ids']}
    return render(request, "fetch_review_cycle_data.html", context)
def RegressionAnalysis(request):
    print('submitted')   
    
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
        'utility':'Regression_Analysis',
        'dept':str(request.session['dept'] )
    }
    response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
    api_data=response.json()   
        #return JsonResponse({'PeerBanks':api_data['PeerBanks'],'States':api_data['States'],'Counties':api_data['Counties']})

    return render(request, 'regression_analysis.html',{'arrCols':arrCols,'ctrl_cols':ctrl_class_data['ColumnName'],'filterSelected':api_data['filterSelected'],'querybldrcols':api_data['gridDttypes']})

def GetRegressionAnalysis(request): 
    try: 
        api_url = getFLAPIURL()+'GetRegressionAnalysis/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'State':request.GET.get('State',''),
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year',''),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept']           
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'testcor':api_data['testcor']})
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})

def GetRegressionResult(request):
    try:
        print(' independentVar',request.GET.getlist('independentVar[]',''))
        api_url = getFLAPIURL()+'GetRegressionResult/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        
        print('REGRESSION VALS :',request.GET.get('v_ddlRegType',''))
        print(request.GET.get('v_ddlModel',''))
        print(request.GET.get('v_txtSegment',''))
        print(request.GET.get('dependentVar',''))
        print(request.GET.getlist('ddlTar[]',''))
        print(request.GET.get('v_ddlProhibitedClass',''))
        print(request.GET.get('v_ddlProhibited',''))
        print(request.GET.get('v_ddlControlClass',''))
        print(request.GET.get('v_ddlControlValue',''))
        print(request.GET.get('v_ddlOrdinalFeatures',''))
        data_params={
            'independentVar':request.GET.getlist('independentVar[]',''),
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year','2023'),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept'],
            'v_ddlRegType':request.GET.get('v_ddlRegType',''),
            'v_ddlModel':request.GET.get('v_ddlModel',''),           
            'v_txtSegment':request.GET.get('v_txtSegment',''),
            'v_ddlDependent':request.GET.get('dependentVar',''),
            'v_ddlTarget':request.GET.getlist('ddlTar[]',''),
            'v_ddlProhibitedClass':request.GET.get('v_ddlProhibitedClass',''),
            'v_ddlProhibited':request.GET.get('v_ddlProhibited',''),
            'v_ddlControlClass':request.GET.get('v_ddlControlClass',''),
            'v_ddlControlValue':request.GET.get('v_ddlControlValue',''),
            'v_ddlOrdinalFeatures':request.GET.get('v_ddlOrdinalFeatures','')
        }
        
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'dataresult':api_data['dataresult']})
    except Exception as e:
        print('updateaccess ',e,traceback.print_exc())
        return JsonResponse({'istaken':'false'})

def GetRegressionData(request):
    try:
        api_url = getFLAPIURL()+'GetRegressionData/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'independentVar':request.GET.getlist('independentVar[]',''),
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year','2023'),
            'Portfolio':'Mortgage',
            'Dept':request.session['dept']           
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()        
         
        return JsonResponse({'dataresult':api_data['RegressionData']})
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})



def SMD(request):
    try:
        api_url = getFLAPIURL()+'get_SMD/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year','2023'),
            'portfolio':'Mortgage',
            'dept':request.session['dept']
        }

        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data_SMD=response.json()   
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
            'dept':request.session['dept'],
            'utility':'MatchedPair'
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()
         
        
        
        colCompare=['state_code','county_code','census_tract','derived_loan_product_type','derived_dwelling_category','purchaser_type','preapproval','loan_type','loan_purpose','lien_status','reverse_mortgage','open-end_line_of_credit','business_or_commercial_purpose','loan_amount','combined_loan_to_value_ratio','interest_rate','rate_spread','hoepa_status','total_loan_costs','total_points_and_fees','origination_charges','discount_points','lender_credits','loan_term','prepayment_penalty_term','intro_rate_period' 
                    ,'negative_amortization','interest_only_payment','balloon_payment','other_nonamortizing_features','property_value','construction_method','occupancy_type','manufactured_home_secured_property_type','manufactured_home_land_property_interest','total_units','multifamily_affordable_units','income','debt_to_income_ratio','submission_of_application','initially_payable_to_institution', 
                    'tract_population','tract_minority_population_percent','ffiec_msa_md_median_family_income','tract_to_msa_income_percentage','tract_owner_occupied_units','tract_one_to_four_family_homes','tract_median_age_of_housing_units']
        return render(request, 'SMD.html',{'SMD_Data':api_data_SMD['SMD'],'colCompare':colCompare, 
                     'arrCols':arrCols,'ctrl_cols':ctrl_class_data['ColumnName'],
                    'querybldrcols':api_data['gridDttypes']}) 

         
         
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})
    
def get_SMD(request):
    try:
        api_url = getFLAPIURL()+'get_SMD/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  , 
            'activity_year':request.GET.get('activity_year','2023'),
            'portfolio':'Mortgage',
            'dept':request.session['dept']
        }

        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data_SMD=response.json()   
        print('smd ',api_data_SMD['SMD'])
        return JsonResponse({'istaken':'true','SMD_Data':json.dumps(api_data_SMD['SMD'])})
         
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})


def FLQtns(request):
    try: 
        sectionid =request.POST.get('ddlSection', '0')  
        api_url=getFLAPIURL()+"FLQtns/"       
        data_to_save={ 
            'uid':request.session['uid'],} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        print("api_data-----------------",api_data)

        api_url_a=getFLAPIURL()+"InherentRiskRatingAPI/"       
         
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response_a = requests.get(api_url_a,headers=header)
         
        api_data_a=response_a.json()
        print("api_data ratings-----------------",api_data_a)
        r1 = [i['ratings'] for i in api_data_a['rating_1']]
        print("r1",r1)
        r2 = [i['ratings'] for i in api_data_a['rating_2']]
        print("r2",r2)
        r3 = [i['ratings'] for i in api_data_a['rating_3']]
        print("r3",r3)
        
        return render(request, 'flQtns.html',{'canupdate':api_data['canupdate'],
                                               'sectionid':sectionid,'sections':api_data['sections'],
                                               'Qtns':api_data['Qtns'],'models':api_data['models'],
                                               'rating_1':r1,'rating_2':r2,
                                               'rating_3':r3})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())


def saveFLRatings(request):
    try:
        print('insied saveFLRatings') 
        colDataLst = request.POST['colDataLst']
        uid=request.session['uid']
        api_url=getFLAPIURL()+"saveFLRatings/"       
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

def submitFLRatings(request):
    try: 
        # objreg.submitRatings( objmaster.getmaxICQId())
        # uid=request.session['uid']
        api_url=getFLAPIURL()+"submitFLRatings1/"       
        data_to_save={        
            'uid':request.session['uid'], } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        print("API data",api_data)
        # objmaster.insert_notification(str(uid),'MRM-Head','ICQ','Rating Submitted',1)    
        return JsonResponse({'is_taken':api_data['is_taken']})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def FetchResidualRating(request):
    print()
    inherendRisk =request.GET.get('inherendRisk', 'False')
    controleffect =request.GET.get('controleffect', 'False')
    api_url=getFLAPIURL()+"FetchRessidualRating_1/"       
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


def residualratingslist(request):
    try:  
        print() 
        third_party_api_url = getFLAPIURL()+'InherentRiskRatingAPI/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        data = json.loads(response.content)
        print("residual ratings data",data)
        r1 = json.dumps(data['rating_1'])#['High','Moderate','Low']   
        r2 = json.dumps(data['rating_2'])#['Effective','Partially Effective','Ineffective','NA']
        r3 = json.dumps(data['rating_3'])
        return render(request, 'residualratingslist.html',{'ratings_1':json.loads(r1),'ratings_2':json.loads(r2),'ratings_3':r3})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 


def GetResidualRatings(request):
    print()
    try:
        third_party_api_url = getFLAPIURL()+'InherentRiskRatingAPI/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        data = json.loads(response.content)
        print("residual ratings data",data)
        return JsonResponse({"data":data})  
    except Exception as e:
        print("error is ",e)  
        return JsonResponse({"data":""})
    
def saveresidualrating(request):
    print("request_data_rating",request.GET)
    api_url=getFLAPIURL()+"SaveResidualRatingsAPI/"       
    data_to_save={ 
        'control_effective_rating':request.GET.get('ctrl_eff_rating_id','false'),
        'inherent_risk_rating':request.GET.get('inherent_rsk_rating','false'),
        'residual_rating':request.GET.get('residual_rating','false'),
        'addedby':request.session['uid']
    } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)         
    api_data=response.json() 
    print("api_data",api_data)
    return JsonResponse({"data":api_data})

def showinherentristrating(request):
    try: 
        #new
        third_party_api_url = getFLAPIURL()+'ALLInherentRatingAPI/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        } 
        response = requests.get(third_party_api_url, headers=header)
        print("response inherent risk  rating",response.content)

        return render(request, 'linherentriskratinglist.html',{ 'actPage':'Inherent Risk Rating','ratings':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def newinherentristrating(request):
    try:   
        return render(request, 'addinherentriskrating.html',{ 'actPage':'Add Inherent Risk Rating'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

@api_view(['POST','PUT'])
def addinherentristrating(request):
    try:
        print("request_data",request.POST)
        third_party_api_url = getFLAPIURL()+'ALLInherentRatingAPI/'

        updated_id = request.POST.get('update_id','False')
        rating = request.POST.get('rating', 'False')

        print("request------------------------",updated_id)
        if updated_id != 'undefined':
            # third_party_api_url = getFLAPIURL()+'ALLInherentRatingAPI/'
            print("third_party_api_url",third_party_api_url)
            data_to_update = {
                'ratings':rating,
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
            # third_party_api_url = getFLAPIURL()+'ALLInherentRatingAPI/'
            data_to_save = {
                'ratings':rating,
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


def edit_inherentristrating(request,id): 
    try:
        print("check id",id)
        # finddval_obj=Department.objects.get(dept_aid=id) 
        third_party_api_url = getFLAPIURL()+'ALLInherentRatingAPI/'+str(id)
        header = {
        "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response--------------------------rating",json.loads(response.content))  
        find_val_obj = json.loads(response.content)
        label=find_val_obj['data']['ratings']
        
        return render(request, 'addinherentriskrating.html',{ 'actPage':'Edit Inherent Risk Rating','label':label,'id':id})

    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())

def showcontroleffectiverating(request):
    try: 
        #new
        third_party_api_url = getFLAPIURL()+'ControlEffectiveRatingAPI/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        } 
        response = requests.get(third_party_api_url, headers=header)
        print("response control effective rating",response.content)

        return render(request, 'controleffectiveratinglist.html',{ 'actPage':'Inherent Risk Rating','ratings':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def newcontroleffectiverating(request):
    try:   
        return render(request, 'addcontroleffectiverating.html',{ 'actPage':'Add Inherent Risk Rating'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())


@api_view(['POST','PUT'])
def addcontroleffectiverating(request):
    try:
        print("request_data",request.POST)
        third_party_api_url = getFLAPIURL()+'ControlEffectiveRatingAPI/'

        updated_id = request.POST.get('update_id','False')
        rating = request.POST.get('rating', 'False')

        print("request------------------------",updated_id)
        if updated_id != 'undefined':
            # third_party_api_url = getFLAPIURL()+'ALLInherentRatingAPI/'
            print("third_party_api_url",third_party_api_url)
            data_to_update = {
                'ratings':rating,
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
            # third_party_api_url = getFLAPIURL()+'ALLInherentRatingAPI/'
            data_to_save = {
                'ratings':rating,
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

def edit_controleffectiverating(request,id): 
    try:
        print("check id",id)
        # finddval_obj=Department.objects.get(dept_aid=id) 
        third_party_api_url = getFLAPIURL()+'ControlEffectiveRatingAPI/'+str(id)
        header = {
        "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response--------------------------rating",json.loads(response.content))  
        find_val_obj = json.loads(response.content)
        label=find_val_obj['data']['ratings']
        
        return render(request, 'addcontroleffectiverating.html',{ 'actPage':'Edit Inherent Risk Rating','label':label,'id':id})

    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())



def FL_Report(request):
    print("FL_Report")
    try: 
        gridHeaders=["Assessment Area","Question / Request","MDD References","Request Document Name","Request Date","Response Date","Responsible Party","Status","Notes / Comments from Varo MO","Follow-up/New Questions","Request Date_Follow-up","Response Date_Follow-up"]
        data = {}
        resultDocumentation = []
        result = [] 
        api_url = getFLAPIURL()+'get_FL_DA_ImageInfo/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uid':request.session['uid']  ,  
            'Portfolio':'Mortgage',
            'Dept':request.session['dept']
        }
        responseimg = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        result=responseimg.json()  
        lstTbl = []
        
        modelFileExists = "true" 
        newTitles=[]
        # template_name = 'new check'
        # savedData,newTitles = getSavedReportDataNew(request.session['accessToken'],template_name)
        resultpROCESS =[] 
        qtnresult=[]
        rows=[]
        
        
        tblFile = file_path + user_name+"_Tables.csv"
        if os.path.exists(tblFile):
            df_tbl = pd.read_csv(tblFile)
            resultTbl = df_tbl.to_json(orient="records")
            lstTbl = json.loads(resultTbl)
            resultTbl = ""
            del df_tbl
        outputfiles = []
        replication_files = os.path.join(
            BASE_DIR, 'static/replicationFiles/')
        if os.path.exists(replication_files):
            dir_list = os.listdir(os.path.join(
                BASE_DIR, 'static/replicationoutput/'))
            # prints all files
            outputfiles = dir_list

        scnfiles = []
        scn_files = os.path.join(
            BASE_DIR, 'static/scenarioOutput/')
        if os.path.exists(scn_files):
            dir_list = os.listdir(os.path.join(
                BASE_DIR, 'static/scenarioOutput'))
            # prints all files
            scnfiles = dir_list 

           
        #     DocumentationData = file_path + file_name + "_DocumentationData.csv"
        #     if os.path.exists(DocumentationData):
        #         df_old = pd.read_csv(DocumentationData, encoding='utf-8')
        #         idxLst = [*range(1, len(df_old)+1, 1)]
        #         print('idxLst ', idxLst) 
        #         df_new = pd.DataFrame(
        #             idxLst, columns=['docIdx'])
        #         df = pd.concat([df_old, df_new], axis=1)
        #         resultDocumentation = df.to_json(orient="records")
        #         resultDocumentation = json.loads(resultDocumentation)
        resultDocumentation=  []
        #Get Template Names
        api_url = getFLAPIURL()+'FL_ReportContentAPI/'
        header = {
        "Content-Type":"application/json",
         'Authorization': 'Token '+request.session['accessToken']
        }
        response_user = requests.get(api_url, headers=header)
        # print("response userlist",response_user.content)
        Rpt_content_data = json.loads(response_user.content) 
        data = {
            'imgFiles': result,
            'imgReplication': outputfiles,
            'imgScn': scnfiles,
            'pdfFile': "/static/media/FLAnalysisReport_"+str(request.session['dept'])+".pdf",
            'policiesLst': [],
            'modelDocs': resultDocumentation,
            'ismodelUsage': modelFileExists, 
            'df': resultpROCESS,
            # 'savedReportData': savedData,
            'lstTables': lstTbl,
            'newTitles':newTitles,
            'headers':  gridHeaders,
            'qtnresult':qtnresult,
            'selectedMdl':request.session['dept'],
            'Report_Template':Rpt_content_data
        }
        
        report_file_path = os.path.join(BASE_DIR, plot_dir_view)
        report_file_name = "temp_report_"+user_name
        cnfrmsrcFiles = report_file_path + report_file_name + ".csv"
        if os.path.exists(cnfrmsrcFiles):
            os.remove(cnfrmsrcFiles)

        
        return render(request, 'FL_exportReportTxtEdV.html', data)
    except Exception as e:
        print('Error is', e)
        print('Error is', traceback.print_exc())
        return render(request, 'error.html')

def FLgenerateReportTxtEd(request):

    try: 
        print("request_data _report",request.GET)
        mdl_id=request.session['dept']
        template_name = request.GET.get('template_name')
        print("template_name",template_name)
        # a variable pdf
        pdf = MyFPDF()
        document = Document()
        section = document.sections[0]
        # Changing the orientation to landscape
        section.orientation = WD_ORIENT.LANDSCAPE

        # Printing the new orientation.
        columnPageIdx = -1  
        edaPageIdx = -1
        modelsPageIdx = -1

        # pdf.add_page('P')
        # pdf = addTitlenComments(pdf, document,mdl_id)

        pdf.add_page('P')
        FLaddDocumentVesrionHistory(pdf, document,request.session['accessToken'],request.session['dept'],template_name)

        # #pdf = addCommentsnImgs(pdf)

        pdf, columnPageIdx, edaPageIdx, modelsPageIdx = FLaddSummarynCommentsHTMLNew(
            pdf, document, columnPageIdx, edaPageIdx, modelsPageIdx,mdl_id,request.session['accessToken'],template_name)
        # pdf = addReferences(pdf)
        # pdf.add_page('P')
        # document.add_page_break()
        # pdf = addDocumentationComments(pdf, document,mdl_id)

        # pdf.add_page('P')
        # document.add_page_break()
        # pdf = addDataQuality(pdf, document,mdl_id)

        pdf.output(os.path.join(
            BASE_DIR, "static/media/FLValidationReport_"+mdl_id+".pdf"))

        document.save(os.path.join(
            BASE_DIR, "static/media/demo.docx"))

        reportFilepath = os.path.join(
            BASE_DIR, "static/media/ValidationReport_"+mdl_id+".pdf")
        if os.path.exists(reportFilepath):
            # with open(reportFilepath, 'rb') as fh:
            #     response = HttpResponse(
            #         fh.read(), content_type="application/force-download")
            #     response['Content-Disposition'] = 'attachment; filename=' + \
            #         os.path.basename(reportFilepath)
            #     return response
            # from django.utils.encoding import smart_str

            # # mimetype is replaced by content_type for django 1.7
            # response = HttpResponse(content_type="application/force-download")
            # response['Content-Disposition'] = 'attachment; filename=' + \
            #     os.path.basename(reportFilepath)
            # response['X-Sendfile'] = smart_str(reportFilepath)
            # return response
            data = {"is_taken": True}
            return JsonResponse(data)
        raise Http404
    except Exception as e:
        print(e)
        print(traceback.print_exc())
        data = {"is_taken": False}
        return JsonResponse(data)
    
font_files = os.path.join(BASE_DIR, 'static/fonts/')

def FLaddSummarynCommentsHTMLNew(pdf, document, columnPageIdx, edaPageIdx, modelsPageIdx,mdl_id,accessToken,template_name):
    print("template_name-------",template_name)
    # SummaryDataFiles = file_path + file_name + "_SummaryData.csv"
    ####
    try:
        third_party_api_url = getFLAPIURL()+'FL_Fetch_Report_data/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+accessToken
        }

        data_to_get = {
                'template_name':template_name,            
            }
        
        responseget = requests.get(third_party_api_url,data=json.dumps(data_to_get),headers=header)
        # print("responseget------------------ ",responseget.content)
        data = json.loads(responseget.content)
        # df = pd.DataFrame(data['df'])
        df = pd.json_normalize(data['df'])
        print("df-------------",df)
        ###
        
        for index, row in df.iterrows():
            print("row-------",row)

            x, y = 10, pdf.get_y()
            if(str(row["comment"]) != "-"):
                
                y = pdf.get_y()
                # print('y at start is ',y)
                pdf.set_xy(x, y)
                pdf.add_font("ArialUnicodeMS", "",
                                font_files + "ARIALUNI.ttf", uni=True)
                pdf.set_font('ArialUnicodeMS', '', 9)
                # ##pdf.set_font("Arial",  size=9)
                pdf.set_text_color(0.0, 0.0, 0.0)
                pdf.set_left_margin(10)
                # pdf.set_link(linkArr[index], y, pdf.page_no())
                encdStr = str(row["comment"]).replace(
                    'src="/static', 'src="static').replace('height="24"', 'height="20"')
                
                encdStr=encdStr.replace('\\','/')
                encdStr=encdStr.replace('/static','static')
                encdStr = str(encdStr.encode('utf-8'), 'utf-8')
                commentstr = ""
                import re
                tblLst = re.findall(
                    '<div class="appTblsss" id="', encdStr) 
                for match in re.finditer('<div class="appTblsss" id="', encdStr):
                    print('match is ', match)

                tbl_index = -1
                # print('encdStr is ',encdStr)
                if '<div class="appTblsss" id="'.lower() in encdStr.lower():
                    tbl_index = encdStr.index(
                        '<div class="appTblsss" id="')
                    print('tbl_index is ',tbl_index)
                    try:
                        tblid_index = encdStr.index('"><table style=', tbl_index)
                    except Exception as e:
                        tblid_index = encdStr.index('"><table width=', tbl_index)
                    # print('tblid_index ', tblid_index)
                    # print(' tableId is ', encdStr[(tbl_index+27):tblid_index])
                    table_ID = encdStr[(tbl_index+27):tblid_index]
                    tblend_index = encdStr.index(table_ID+'End"')
                    tblend_index = tblend_index+17+len(table_ID)
                # print('tblend_index is ', tblend_index)
                itr = 0
                # print('coment after replacing the table is ',
                #       encdStr[:tbl_index] + "" + encdStr[tblend_index:])
                # print('len of encdStr ', len(encdStr))
                while itr < len(encdStr):
                    # for itr in range(len(encdStr)):
                    # print('itr is ', itr)
                    if tbl_index == itr:
                        y = pdf.get_y()
                        x = 10
                        pdf.set_xy(x, y)
                        pdf.set_font('Arial', '', 9)
                        pdf.write_html(commentstr) 
                        commentstr = ""
                        print('table_ID is ',table_ID)
                        # addTabletoRpt(pdf, table_ID)
                        itr = tblend_index
                        print('added here  1', commentstr)
                    elif(checkSymbol(encdStr[itr:itr+1]) == False):
                        commentstr += encdStr[itr:itr+1]

                    else:
                        # print('commentstr ', commentstr)
                        pdf.set_font('Arial', '', 9)
                        pdf.write_html(commentstr)
                        y = pdf.get_y()
                        x = pdf.get_x()
                        # print('x before cell', pdf.get_x(), pdf.get_y())
                        pdf.set_xy(x, y)
                        pdf.set_font('ArialUnicodeMS', '', 9)
                        pdf.cell(2, 5, encdStr[itr:itr+1])
                        y = pdf.get_y()
                        x = pdf.get_x()
                        # print('x,y  ', pdf.get_x(), pdf.get_y())
                        # print('added here  2',commentstr)
                        commentstr = ""
                    itr += 1
                if len(encdStr) == itr and commentstr != "":
                    # print('commentst at end is ', commentstr)
                    # print('y at srite html is ',y)                        
                    pdf.set_font('Arial', '', 9)
                    pdf.write_html(commentstr)
                    y = pdf.get_y()
                    x = pdf.get_x()
                    # print('added here  3',commentstr,' y is ',y)
                    commentstr = "" 
                y = pdf.get_y()+5
                pdf.set_xy(x, y)
                pdf.multi_cell(0, 5, "", align='L')
            else:
                y = pdf.get_y()
                # print('y at start is ',y)
                pdf.set_xy(x, y)
                pdf.add_font("ArialUnicodeMS", "",
                                font_files + "ARIALUNI.ttf", uni=True)
                pdf.set_font('ArialUnicodeMS', '', 9)
                # ##pdf.set_font("Arial",  size=9)
                pdf.set_text_color(0.0, 0.0, 0.0)
                pdf.set_left_margin(10)
                # pdf.set_link(linkArr[index], y, pdf.page_no())
                commentstr = "<b>"+ str(row["lbl_idx"]) + ' '+ str(row["lbl_txt"]).replace(
                    'src="/static', 'src="static').replace('height="24"', 'height="20"') +"</b>"                               
                pdf.set_font('Arial', '', 9)
                pdf.write_html(commentstr)
                y = pdf.get_y()
                x = pdf.get_x()
                # print('added here  3',commentstr,' y is ',y)
                commentstr = "" 
                y = pdf.get_y()+5
                pdf.set_xy(x, y)
                pdf.multi_cell(0, 5, "", align='L')
        return pdf, columnPageIdx, edaPageIdx, modelsPageIdx
    except Exception as e:
        print("report error is",e)

def checkSymbol(charStr):
    try:
        a = charStr.encode('latin-1')
        return False
    except Exception as e:
        return True
    
def FL_Reportdata(request):
    print("FL_Reportdata")
    newTitles=[]
    template_name = request.GET.get('template_name', 'False')
    savedData,newTitles = FL_getSavedReportDataNew(request.session['accessToken'],template_name)
    # resultpROCESS = df.to_json(orient="records")
    # resultpROCESS = json.loads(resultpROCESS) 
    third_party_api_url = getFLAPIURL()+'FL_Fetch_Header_Details/'
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }  
    data_to_get = {
            'template_name':template_name,
    }
    responseget_header_data = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
    print("responseget_header_data ",json.loads(responseget_header_data.content))

    for i in json.loads(responseget_header_data.content):
        print("----------------------------",i)
        third_party_api_url = getFLAPIURL()+'FL_ReportHeaderTitleContentAPI/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_save = {
            'template_name':i['template_name'],
            'title_id':i['title_id'], 
            'label':i['title_label'],
            'header_or_title':i['title_or_heading'],
            'title_type':i['title_type'],
            'title_placeholder':i['title_placeholder'],
            'title_sort_idx':i['title_sort_idx'],
            'fontsize':i['fontsize'],
            'alignment':i['alignment'],
            'mdl_id':request.session['dept'],
            'added_by':request.session['uid'],
            'type':'save'
        }
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
        print("responseget save header content FLLLLLLLL",responseget.content)
    data = {
        'df':savedData,
        'header_data':json.loads(responseget_header_data.content)
    }
    return JsonResponse(data)


def FL_getSavedReportDataNew(accessToken,template_name,template="General"): 
    # SummaryDataFiles = file_path + file_name + "_SummaryData.csv" 
    print("FL_getSavedReportDataNew")
    ####
    third_party_api_url = getFLAPIURL()+'FL_Fetch_Report_data/'
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+accessToken
    }
    data_to_get = {
            'template_name':template_name, 
        }
    
    responseget = requests.get(third_party_api_url,data= json.dumps(data_to_get),headers=header)
    print("responseget show------------------ ",json.loads(responseget.content))
    data = json.loads(responseget.content)
    # df = pd.DataFrame(data['df'])
    df = pd.json_normalize(data['df'])
    # print("df FLL-------------",df)
    ###

    temp_report_file_path = os.path.join(BASE_DIR, plot_dir_view)
    temp_report_file_name = "temp_report_"+user_name    
    temp_cnfrmsrcFiles = temp_report_file_path + temp_report_file_name + ".csv"
    divMain = ""
    newTitles=[]
    divSection = ""
    report_file_path = os.path.join(BASE_DIR, plot_dir_view)
    staticTitles='"Executive Summary" ,"Model Assessment","Model Performance & Testing","Implementation and Controls","Governance and Oversight"'
    report_file_name = "report_"+user_name
    cnfrmsrcFiles = report_file_path + report_file_name + ".csv"
    print('os.path.exists(temp_cnfrmsrcFiles) is ',temp_cnfrmsrcFiles ,',',os.path.exists(temp_cnfrmsrcFiles))
    if os.path.exists(temp_cnfrmsrcFiles):
        if not os.path.exists(cnfrmsrcFiles):
            # os.remove(cnfrmsrcFiles)
        # os.rename(temp_cnfrmsrcFiles, cnfrmsrcFiles)
            shutil.copyfile(temp_cnfrmsrcFiles, cnfrmsrcFiles)
    ms_report_file_path = os.path.join(BASE_DIR, 'static/reportTemplates/')
    ms_report_file_name = "report_master.csv"
    df_ms = pd.read_csv(ms_report_file_path+ms_report_file_name, encoding='utf-8')
    print('os.path.exists(cnfrmsrcFiles) ',cnfrmsrcFiles,os.path.exists(cnfrmsrcFiles))
     
    for index, row in df.iterrows(): 
        if str(row["lbl_idx"]) =="Executive Summary":
            ExeSummId=str(row["Report_Template_Temp_AID"]) 
        if str(row['comment']) == "-": 
            divSection = divSection+"<div style='display: flex; justify-content: flex-start;'><div style='width:17px;'><i id='tggl_" + str(row["FL_Report_Template_Temp_AID"]) + "' class='bi bi-plus-square'' style='margin-right:5px;cursor:pointer;' onclick='toggleHeight("+str(row["FL_Report_Template_Temp_AID"]) +",this.id)'></i></div><div style='width:20px;'><i class='bi bi-pencil-square' style='margin-right:5px;cursor:pointer;'  title='Edit comment' onclick='getData("+str(row["FL_Report_Template_Temp_AID"]) +")'></i> </div><div id='div_" + str(row["FL_Report_Template_Temp_AID"]) + "' style='height:20px;overflow:hidden;'><b>"+ str(row["lbl_idx"]) + ' '+ str(row["lbl_txt"]).replace("\t", "\u0020\u0020\u0020\u0020") +"</b></div></div>"
            #divSection = divSection+"</br>" 
        else:
            divSection = divSection+"<div style='display: flex; justify-content: flex-start;'><div style='width:17px;'><i id='tggl_" + str(row["FL_Report_Template_Temp_AID"]) + "' class='bi bi-plus-square'' style='margin-right:5px;cursor:pointer;' onclick='toggleHeight("+str(row["FL_Report_Template_Temp_AID"]) +",this.id)'></i></div><div style='width:20px;'><i class='bi bi-pencil-square' style='margin-right:5px;cursor:pointer;'  title='Edit comment' onclick='getData("+str(row["FL_Report_Template_Temp_AID"]) +")'></i> </div><div id='div_" + str(row["FL_Report_Template_Temp_AID"]) + "' style='height:20px;overflow:hidden;'>"+ str(row["comment"])+"</div></div>"
            # divSection = divSection+"<br>" 
        #Report_Template_Temp_AID     
    return divSection,newTitles


def FL_savereportcontent(request): 
    print("FL_savereportcontent")
    comments =request.POST.get('comments', 'False') 
    template_name = request.POST.get('template_name','False')
    report_template_aid = request.POST.get('report_template_aid','False') 
    print("comments",comments)
    print("template_name",template_name)
    print("report_template_aid",report_template_aid)
    third_party_api_url = getFLAPIURL()+'FL_ReportContentAPI/'
    data_to_save = {
        'report_template_aid':report_template_aid,
        'template_name':template_name,
        'comment':comments,
        'mdl_id':request.session['dept'],
        'added_by':request.session['uid']
    }
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
    data=json.loads(response.content) 
    print("data",data)
    savedData,newTtl = FL_getSavedReportDataNew(request.session['accessToken'],template_name,request.session['dept'])
    print('savedData ', savedData)
    data = {
        'is_taken': True,
        'reqId': str(report_template_aid), 
        'savedReportData': savedData,
    }
    return JsonResponse(data)

def getPolicies():
    contactFile = file_path + user_name + "_Policies.csv"
    result = []
    if os.path.exists(contactFile):
        df = pd.read_csv(contactFile)
        result = df.to_json(orient="records")
        result = json.loads(result)

    return result

def FLaddDocumentVesrionHistory(pdf, document,accessToken="",mdl_id="",template_name=""):
    x, y = 10, 10
    api_url=getFLAPIURL()+"get_header_n_title/"       
    data_to_save={ 
        'temp_name':template_name,
        'mdl_id':mdl_id } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+ accessToken
    }
    response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)         
    api_data=response.json()  
    page_no=0
    if len(api_data)>0: 
        dfsorted = api_data['ttlnheadrs']  
        for testdata,val in dfsorted.items():  
            if page_no==0:
                page_no= val["page_no"]
            elif page_no!=val["page_no"]:
                page_no=val["page_no"]
                pdf.add_page('P')
                x, y = 10, 10
            if(str(val["Header_or_Title"])=="1"):
                pdf.set_xy(10, y)
                pdf.set_font("Arial", 'B', size=val["fontsize"])
                pdf.multi_cell(200, 10, val["Comment"], align=val["alignment"])
                y += 5
            else:
                if(str(val["title_type"])=="Label"):
                    pdf.set_xy(10, y)
                    pdf.set_font("Arial", 'B', size=val["fontsize"])
                    pdf.multi_cell(200, 10, val["Label"], align=val["alignment"]) 
                elif(val["title_type"]=="Header"):
                    pdf.set_xy(10, y)
                    pdf.set_font("Arial", 'B',  size=val["fontsize"])
                    pdf.multi_cell( 200, 10, val["Label"]+ val["Comment"], align=val["alignment"])
                    # x = pdf.get_x()+5
                    # pdf.set_xy(x, y)
                    # pdf.set_font("Arial" , size=10)
                    # pdf.multi_cell(100, 10, val["Comment"], align='L') 
                elif(val["title_type"]=="Table"): 
                    hdrLen=len(str(val["Label"]).split(','))                     
                    cellWidth=190/len(str(val["Label"]).split(','))                    
                    y += 5
                    cellx = 10
                    for hdr in str(val["Label"]).split(','):                    
                        pdf.set_font("Arial", 'B', size=9)
                        pdf.set_fill_color(211, 211, 211)
                        pdf.set_xy(cellx, y)
                        pdf.cell(cellWidth, 5,hdr, 1, fill=True, align='C')       
                        cellx =cellWidth+cellx                 
                    api_url=getFLAPIURL()+"get_Report_Title_Table_contet/"       
                    data_to_save={ 
                        'temp_name':template_name,
                        'mdl_id':mdl_id,
                        'title_id':val["title_id"] } 
                    header = {
                    "Content-Type":"application/json",
                    'Authorization': 'Token '+ accessToken
                    }
                    response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)         
                    api_data_tbl=response.json() 
                    if len(api_data_tbl)>0: 
                        dftbldt = api_data_tbl['ttlnheadrs']
                        for testdata,valtbl in dftbldt.items():   
                            cellx=10     
                            y += 5                    
                            for ir in range(1,(hdrLen+1)):
                                print('tbl Header_',str(ir),' ', valtbl["Header_"+str(ir)]) 
                                pdf.set_font("Arial", 'B', size=9)
                                pdf.set_fill_color(211, 211, 211)
                                pdf.set_xy(cellx, y)
                                pdf.cell(cellWidth, 5,valtbl["Header_"+str(ir)], 1, fill=False, align='C')       
                                cellx =cellWidth+cellx       
            y += 5
    return pdf



def FLaddReports(request):
    try: 
        # department
        third_party_api_url = getAPIURL()+'department/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }    
        responseget_department = requests.get(third_party_api_url, headers=header)
        print("responseget_department ",json.loads(responseget_department.content))

        # Section
        third_party_api_url = getFLAPIURL()+'FLReportSectionMasterAPI/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }    
        responseget_sections = requests.get(third_party_api_url, headers=header)
        print("responseget_sections ",json.loads(responseget_sections.content))

        # Template name
        third_party_api_url = getFLAPIURL()+'FL_get_template_name/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }    
        data_to_save = {
            'template_name':request.session['uid']
        }
        responseget_tmpname = requests.get(third_party_api_url, headers=header)
        print("responseget_tmpname ",json.loads(responseget_tmpname.content))

        return render(request, 'fladdReports.html',{'departments':json.loads(responseget_department.content),'sections':json.loads(responseget_sections.content),'template_names':json.loads(responseget_tmpname.content)})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc()) 


def FLSave_Report(request):
    try:
        print("request save report",request.GET)
        if request.GET['sub_section'] == '':
            sub_section = 0
        else:
            sub_section =  request.GET['sub_section']
        
        if request.GET['sub_sub_section'] == '':
            sub_sub_section = 0
        else:
            sub_sub_section = request.GET['sub_sub_section'] 

        third_party_api_url = getFLAPIURL()+'FLReportTemplateTempAPI/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        
        data_to_save = {
            'template_name':request.GET['template_name'],
            'department':request.GET['department'],
            'rpt_section_aid':request.GET['section'],
            'rpt_sub_section_aid':sub_section,
            'rpt_sub_sub_section_aid': sub_sub_section,
            'added_by':request.session['uid']
        }
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
        print("responseget report",responseget.content)
        
        return JsonResponse(json.loads(responseget.content))    
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())


def FLgetRptSub_Sections(request):
    try:       
        secid =request.GET.get('secid', 'False')  
        template_name = request.GET.get('template_name','False')
        third_party_api_url = getFLAPIURL()+'FLReportSubSectionMasterAPI/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_get = {
            'is_taken':'true',
            'rpt_section_aid':secid,
            'template_name':template_name
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        print("responseget ",responseget.content)
        return JsonResponse({'subsections':json.loads(responseget.content)})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 


def FLgetRptSub_Sub_Sections(request):
    try:       
        secid =request.GET.get('secid', 'False')  
        template_name = request.GET.get('template_name','False')
        third_party_api_url = getFLAPIURL()+'FLReportSubSubSectionMasterAPI/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_get = {
            'is_taken':'true',
            'rpt_sub_section_aid':secid,
            'template_name':template_name
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        print("responseget ",responseget.content)
        return JsonResponse({'subsections':json.loads(responseget.content)})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 


def FLSubmit_Report(request):
    try:
        print("Request template data",request.GET)
        third_party_api_url = getFLAPIURL()+'FLReportTemplateAPI/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_save = {
            'template_name':request.GET['template_name'],
        }
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
        print("responseget report submit data",responseget.content)

        header_name = request.GET.get('header_name','False')
        print("header name",header_name)
        if header_name != '':
            third_party_api_url_a = getFLAPIURL()+'FL_RPT_Template_Header_API/'
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }    
            data_to_save = {
                'header_template_name':header_name,
                'report_template_name':request.GET['template_name'],
                'added_by':request.session['uid']
            }
            response_save_header = requests.post(third_party_api_url_a, data= json.dumps(data_to_save),headers=header)
            print("response_save_header ",json.loads(response_save_header.content))
        else:
            pass
            
        return JsonResponse(json.loads(responseget.content))    
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())


def FLSave_Report_Section(request):
    try:
        print("request data get",request.GET)
        third_party_api_url = getFLAPIURL()+'FLReportSectionMasterAPI/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_save = {
            'rpt_section_text':request.GET['section'],
            'rpt_section_description':request.GET['sectiondesc'], 
            'added_by':request.session['uid'],
            'activestatus':request.GET['activests']
        }
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
        print("responseget ",responseget)
        
        return JsonResponse(json.loads(responseget.content))    
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())


def FLSave_Report_Sub_Section(request):
    try:
        third_party_api_url = getFLAPIURL()+'FLReportSubSectionMasterAPI/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_save = {
            'rpt_section_aid':request.GET['secid'],
            'rpt_sub_section_text':request.GET['section'],
            'rpt_sub_section_description':request.GET['sectiondesc'], 
            'added_by':request.session['uid'],
            'activestatus':request.GET['activests']
        }
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
        print("responseget ",responseget.content)
        
        return JsonResponse(json.loads(responseget.content))    
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())


def FLSave_Report_Sub_Sub_Section(request):
    try:
        third_party_api_url = getFLAPIURL()+'FLReportSubSubSectionMasterAPI/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_save = {
            'rpt_section_aid':request.GET['section_id'],
            'rpt_sub_section_aid':request.GET['sub_secid'],
            'rpt_sub_sub_section_text':request.GET['sectiontext'], 
            'rpt_sub_sub_section_description':request.GET['sectiondesc'],
            'added_by':request.session['uid'],
            'activestatus':request.GET['activests']
        }
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
        print("responseget sub sub section ",responseget.content)
        
        return JsonResponse(json.loads(responseget.content))    
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())


def FL_Get_Title_Label(request):
    try:
        # Title_Label
        header_name = request.GET.get('header_name','False')
        template_name = request.GET.get('template_name','False') 
        print("Template name",template_name)
        third_party_api_url = getFLAPIURL()+'FL_Get_Title_Label/'
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


def FLgetReportTtlHdr(request):
    api_url = getFLAPIURL()+'FLgetReportTtlHdr/'
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


def FLShowReportdata(request):
    newTitles=[]
    template_name = request.GET.get('template_name', 'False')
    savedData,newTitles = FLgetShowReportDataNew(request.session['accessToken'],template_name)
    # resultpROCESS = df.to_json(orient="records")
    # resultpROCESS = json.loads(resultpROCESS) 
    data = {
        'df':savedData
    }
    return JsonResponse(data)


def FLgetShowReportDataNew(accessToken,template_name,template="General"): 
    
    third_party_api_url = getFLAPIURL()+'FLShow_Report_data/'
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+accessToken
    }
    data_to_get = {
            'template_name':template_name, 
        }
    
    responseget = requests.get(third_party_api_url,data= json.dumps(data_to_get),headers=header)
    
    data = json.loads(responseget.content)
    
    df = pd.json_normalize(data['df'])
    
    newTitles=[]
    divSection = ""

    for index, row in df.iterrows(): 
        print("row",row)
        # if str(row['Report_Template_Temp_AID']) == str(row['Report_Template_Temp_AID']): 
        divSection = divSection+"<div style='display: flex; justify-content: flex-start;'><div style='width:17px;'><i id='tggl_" + str(row["Report_Template_Temp_AID"]) + "' class='far fa-plus-square' style='margin-right:5px;cursor:pointer;' onclick='toggleHeight("+str(row["Report_Template_Temp_AID"]) +",this.id)'></i></div><div style='width:20px;'><i class='fa fa-edit' style='margin-right:5px;cursor:pointer;'  title='Edit comment' onclick='getData("+str(row["Report_Template_Temp_AID"]) +")'></i> </div><div id='div_" + str(row["Report_Template_Temp_AID"]) + "' style='height:20px;overflow:hidden;'><b>"+ str(row["lbl_idx"]) + ' '+ str(row["lbl_txt"]).replace("\t", "\u0020\u0020\u0020\u0020") +"</b></br></div></div>"
        print("1")
        divSection = divSection+"<br>" 
     
    return divSection,newTitles


def udaap_ratings(request):
    print("udaap_ratings",udaap_ratings)
    try:
        api_url=getFLAPIURL()+"UdaapRatings/"       
         
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url,headers=header)                      
        api_data=response.json()
        print("api_data",api_data)

        return render(request,'Udaap_ratings.html',{'sections':api_data['sections'],'Qtns':api_data['Qtns']})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc())  

def Udaap_save_ratings(request):
    try:
        from datetime import datetime
        added_by=request.session['uid']
        adddate=datetime.now()
        question_id=request.GET.get('question_id')
        ratings_yes=request.GET.get('ratings_yes')
        ratings_no=request.GET.get('rating_no')
        doc_na=request.GET.get('doc_na')
        # doc_no=request.GET.get('doc_no')
        print("question_id",question_id)
        if ratings_yes == '':
            ratings_yes="null"
        if ratings_no == '':
            ratings_no ="null"
        if doc_na == '':
            doc_na ="null" 
        

        api_url=getFLAPIURL()+"UdaapRatings/"       
        data_to_save={ 
            'question_id':question_id,
            'ratings_yes':ratings_yes,
            'ratings_no':ratings_no,
            'doc_na':doc_na,
            'istool':'0'} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)         
        api_data=response.json() 
        print("udaap api data",api_data)

        # objmaster.fl_insertRatings(question_id,ratings_yes,ratings_no,doc_na)
        # print('saved')
        return JsonResponse({'is_taken':True})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 



def UdaapQtnsFinal(request):
    try: 
        sectionid =request.POST.get('ddlSection', '0') 
        api_url=getFLAPIURL()+"UdaapQtnsFinal/"       

        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url,headers=header)
         
        api_data=response.json()
        print("api_data",api_data)

        api_url_a=getFLAPIURL()+"UdaapInherentRiskRatingAPI/"       
         
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response_a = requests.get(api_url_a,headers=header)
         
        api_data_a=response_a.json()
        print("api_data ratings-----------------",api_data_a)
        r1 = [i['ratings'] for i in api_data_a['rating_1']]
        print("r1",r1)
        r2 = [i['ratings'] for i in api_data_a['rating_2']]
        print("r2",r2)
        r3 = [i['Ratings'] for i in api_data_a['rating_3']]
        print("r3",r3)
        
        return render(request, 'UdaapQtnsFinal.html',
                      {'FLRating':api_data['FLRating'],
                       'sectionid':sectionid,
                       'sections':api_data['sections'],'Qtns':api_data['Qtns'],'rating_1':r1,'rating_2':r2,
                                               'rating_3':r3})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def UdaapFetchResidualRating(request):
    print()
    inherendRisk =request.GET.get('inherendRisk', 'False')
    controleffect =request.GET.get('controleffect', 'False')
    api_url=getFLAPIURL()+"UdaapFetchResidualRating/"       
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

def getUdaapSecQtnFinal(request):
    try:  
        api_url=getFLAPIURL()+"getUdaapSecQtnFinal/"       
         
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

def saveUdaapRatingsFinal(request):
    try:         
        colDataLst = request.POST['colDataLst']
        print("colDataLst-------",colDataLst)
        uid=request.session['uid']
        api_url=getFLAPIURL()+"saveUdaapRatingsFinal/"       
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
        print("api_data new-----------",api_data)   
        return JsonResponse({'is_taken':api_data['is_taken']})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())


def Udaapresidualratingslist(request):
    try:  
        print() 
        third_party_api_url = getFLAPIURL()+'UdaapInherentRiskRatingAPI/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        data = json.loads(response.content)
        print("residual ratings data",data)
        r1 = json.dumps(data['rating_1'])#['High','Moderate','Low']   
        r2 = json.dumps(data['rating_2'])#['Effective','Partially Effective','Ineffective','NA']
        r3 = json.dumps(data['rating_3'])

        print("ratings 3",r3)
        
        return render(request, 'Udaapresidualratingslist.html',{'ratings_1':json.loads(r1),'ratings_2':json.loads(r2),'ratings_3':r3})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 


def UdaapGetResidualRatings(request):
    print()
    try:
        third_party_api_url = getFLAPIURL()+'UdaapInherentRiskRatingAPI/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        data = json.loads(response.content)
        print("Udaao residual ratings data",data)
        return JsonResponse({"data":data})  
    except Exception as e:
        print("error is ",e)  
        return JsonResponse({"data":""})

def Udaapsaveresidualrating(request):
    print("request_data_rating",request.GET)
    api_url=getFLAPIURL()+"UdaapSaveResidualRatingsAPI/"       
    data_to_save={ 
        'control_effective_rating':request.GET.get('ctrl_eff_rating_id','false'),
        'inherent_risk_rating':request.GET.get('inherent_rsk_rating','false'),
        'residual_rating':request.GET.get('residual_rating','false'),
        'addedby':request.session['uid']
    } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)         
    api_data=response.json() 
    print("api_data",api_data)
    return JsonResponse({"data":api_data})

def Udaapshowinherentristrating(request):
    try: 
        #new
        third_party_api_url = getFLAPIURL()+'UdaapALLInherentRatingAPI/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        } 
        response = requests.get(third_party_api_url, headers=header)
        print("response inherent risk  rating",response.content)

        return render(request, 'Udaaplinherentriskratinglist.html',{ 'actPage':'Inherent Risk Rating','ratings':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def Udaapnewinherentristrating(request):
    try:   
        return render(request, 'Udaapaddinherentriskrating.html',{ 'actPage':'Add Inherent Risk Rating'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())


@api_view(['POST','PUT'])
def Udaapaddinherentristrating(request):
    try:
        print("request_data",request.POST)
        third_party_api_url = getFLAPIURL()+'UdaapALLInherentRatingAPI/'

        updated_id = request.POST.get('update_id','False')
        rating = request.POST.get('rating', 'False')
        
        print("request------------------------",updated_id)
        if updated_id != 'undefined':
            # third_party_api_url = getFLAPIURL()+'ALLInherentRatingAPI/'
            print("third_party_api_url",third_party_api_url)
            data_to_update = {
                'ratings':rating,
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
            # third_party_api_url = getFLAPIURL()+'ALLInherentRatingAPI/'
            data_to_save = {
                'ratings':rating,
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

def Udaapedit_inherentristrating(request,id): 
    try:
        print("check id",id)
        # finddval_obj=Department.objects.get(dept_aid=id) 
        third_party_api_url = getFLAPIURL()+'UdaapALLInherentRatingAPI/'+str(id)
        header = {
        "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response--------------------------rating",json.loads(response.content))  
        find_val_obj = json.loads(response.content)
        label=find_val_obj['data']['ratings']
        
        return render(request, 'Udaapaddinherentriskrating.html',{ 'actPage':'Edit Inherent Risk Rating','label':label,'id':id})

    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())


def Udaapshowcontroleffectiverating(request):
    try: 
        #new
        third_party_api_url = getFLAPIURL()+'UdaapControlEffectiveRatingAPI/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        } 
        response = requests.get(third_party_api_url, headers=header)
        print("response control effective rating",response.content)

        return render(request, 'Udaapcontroleffectiveratinglist.html',{ 'actPage':'Inherent Risk Rating','ratings':json.loads(response.content)})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def Udaapnewcontroleffectiverating(request):
    try:   
        return render(request, 'Udaapaddcontroleffectiverating.html',{ 'actPage':'Add Control effective Rating'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

@api_view(['POST','PUT'])
def Udaapaddcontroleffectiverating(request):
    try:
        print("request_data",request.POST)
        third_party_api_url = getFLAPIURL()+'UdaapControlEffectiveRatingAPI/'

        updated_id = request.POST.get('update_id','False')
        rating = request.POST.get('rating', 'False')

        print("request------------------------",updated_id)
        if updated_id != 'undefined':
            # third_party_api_url = getFLAPIURL()+'ALLInherentRatingAPI/'
            print("third_party_api_url",third_party_api_url)
            data_to_update = {
                'ratings':rating,
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
            # third_party_api_url = getFLAPIURL()+'ALLInherentRatingAPI/'
            data_to_save = {
                'ratings':rating,
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

def Udaapedit_controleffectiverating(request,id): 
    try:
        print("check id",id)
        # finddval_obj=Department.objects.get(dept_aid=id) 
        third_party_api_url = getFLAPIURL()+'UdaapControlEffectiveRatingAPI/'+str(id)
        header = {
        "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(third_party_api_url, headers=header)
        print("response--------------------------rating",json.loads(response.content))  
        find_val_obj = json.loads(response.content)
        label=find_val_obj['data']['ratings']
        
        return render(request, 'Udaapaddcontroleffectiverating.html',{ 'actPage':'Edit Inherent Risk Rating','label':label,'id':id})

    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())

def UdaapQtns(request):
    try: 
        sectionid =request.POST.get('ddlSection', '0')  
        api_url=getFLAPIURL()+"UdaapQtns/"       
        data_to_save={ 
            'uid':request.session['uid'],} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        print("api_data-----------------",api_data)

        api_url_a=getFLAPIURL()+"UdaapInherentRiskRatingAPI/"       
         
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response_a = requests.get(api_url_a,headers=header)
         
        api_data_a=response_a.json()
        print("api_data ratings-----------------",api_data_a)
        r1 = [i['ratings'] for i in api_data_a['rating_1']]
        print("r1",r1)
        r2 = [i['ratings'] for i in api_data_a['rating_2']]
        print("r2",r2)
        r3 = [i['Ratings'] for i in api_data_a['rating_3']]
        print("r3",r3)
        
        return render(request, 'UdaapQtns.html',{'canupdate':api_data['canupdate'],
                                               'sectionid':sectionid,'sections':api_data['sections'],
                                               'Qtns':api_data['Qtns'],'models':api_data['models'],
                                               'rating_1':r1,'rating_2':r2,
                                               'rating_3':r3})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def getUdaapSecQtn(request):
    try:
        modelid =request.GET.get('ddlModel', 'False')  
        # sectionid =request.GET.get('ddlSection', '0')  
        sectionid = request.session['uid']

        data_to_get = {
            'id':sectionid
        }

        api_url_a=getFLAPIURL()+"getUdaapSecQtn/"       
         
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        
        response_a = requests.get(api_url_a,data= json.dumps(data_to_get),headers=header)
        api_data=response_a.json()
        return JsonResponse({'sections':api_data['Qtns']})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())


def saveUdaapRatings(request):
    try:
        print('insied saveFLRatings') 
        colDataLst = request.POST['colDataLst']
        uid=request.session['uid']
        api_url=getFLAPIURL()+"saveUdaapRatings/"       
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

def submitUdaapRatings(request):
    try: 
        # objreg.submitRatings( objmaster.getmaxICQId())
        # uid=request.session['uid']
        api_url=getFLAPIURL()+"submitUdaapRatings1/"       
        data_to_save={        
            'uid':request.session['uid'], } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        print("API data",api_data)
        # objmaster.insert_notification(str(uid),'MRM-Head','ICQ','Rating Submitted',1)    
        return JsonResponse({'is_taken':api_data['is_taken']})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def UdaapQuestions(request):
    try: 
        sectionid =request.POST.get('ddlSection', '0') 
        api_url=getFLAPIURL()+"UdaapQuestions/"       
        
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url,headers=header)
         
        api_data=response.json()
        print("api_data-----------------",api_data)
 
        return render(request, 'UdaapQuestions.html',{ 'Qtns':api_data['Qtns']})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def addUdaapQtns(request):
    try:
        api_url=getFLAPIURL()+"addUdaapQtns/"       
        
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url,headers=header)
         
        api_data=response.json()
        print("api_data-----------------",api_data)
        return render(request, 'addUdaapQtns.html',{'sections':api_data['sections']})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc()) 


def getUdaapSub_Sections(request):
    try:       
        sub_secid =request.GET.get('secid', 'False')      
        api_url=getFLAPIURL()+"getUdaapSub_Sections/"       
        
        data_to_get={        
            'sub_secid':sub_secid, } 

        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url,data= json.dumps(data_to_get),headers=header)
         
        api_data=response.json()
        print("api_data-----------------",api_data)
        return JsonResponse({'subsections':api_data['subsections']})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 

def getUdaapSub_Sub_Sections(request):
    try:       
        sub_secid =request.GET.get('secid', 'False') 

        api_url=getFLAPIURL()+"getUdaapSub_Sub_Sections/"       

        data_to_get={        
            'sub_secid':sub_secid, } 

        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url,data= json.dumps(data_to_get),headers=header)
         
        api_data=response.json()
        print("api_data-----------------",api_data)     
        
        return JsonResponse({'subsections':api_data['subsections']})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 


def getUdaapSub_Sub_Sub_Sections(request):
    print("getSub_Sub_Sub_Sections")
    try:       
        sub_secid =request.GET.get('secid', 'False')      
        print("sub_secid",sub_secid)

        api_url=getFLAPIURL()+"getUdaapSub_Sub_Sub_Sections/"       

        data_to_get={        
            'sub_secid':sub_secid, } 

        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url,data= json.dumps(data_to_get),headers=header)
         
        api_data=response.json()
        print("api_data-----------------",api_data) 


        return JsonResponse({'subsections':api_data['subsections']})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 


def Udaap_add_question(request):
    try:
        print('udaap request',request.GET)
        added_by=request.session['uid'] 
        section=request.GET.get('section','False')
        sub_section=request.GET.get('sub_section','False')
        sub_sub_section=request.GET.get('sub_sub_section','False')
        sub_sub_sub_section=request.GET.get('sub_sub_sub_section','False')
        question=request.GET.get('question','False')
        api_url=getFLAPIURL()+"Udaap_add_question/"       
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
        print("api data udaap",api_data)
        return JsonResponse({'is_taken':api_data['is_taken']})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc())     

def addUdaapSection(request):
    try:   
        section =request.GET.get('section', 'False') 
        sectiondesc =request.GET.get('sectiondesc', 'False') 
        activests =request.GET.get('activests', 'False') 

        api_url=getFLAPIURL()+"addUdaapSection/"       

        data_to_save={        
            'text':section, 
            'desc':sectiondesc,
            'activests':activests,
            'uid':request.session['uid']} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url,data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        print("api_data-----------------",api_data)      
        # objmaster.addSection(section,sectiondesc,activests,str(request.session['uid']))
        return JsonResponse({'is_taken':True})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc())  

def addUdaapSub_Section(request):
    try:   
        section =request.GET.get('section', 'False') 
        sectiondesc =request.GET.get('sectiondesc', 'False') 
        activests =request.GET.get('activests', 'False')     
        secid =request.GET.get('secid', 'False')    

        api_url=getFLAPIURL()+"addUdaapSubSection/"       

        data_to_save={        
            'text':section, 
            'desc':sectiondesc,
            'activests':activests,
            'secid':secid,
            'uid':request.session['uid']} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url,data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        print("api_data-----------------",api_data)     
        # objmaster.addSub_Section(secid,section,sectiondesc,activests,str(request.session['uid']))
        return JsonResponse({'is_taken':True})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 

def addUdaapSub_Sub_Section(request):
    try:   
        section =request.GET.get('section', 'False') 
        sectiondesc =request.GET.get('sectiondesc', 'False') 
        activests =request.GET.get('activests', 'False')    
        sub_secid =request.GET.get('sub_secid', 'False') 

        api_url=getFLAPIURL()+"addUdaapSubSubSection/"       

        data_to_save={        
            'text':section, 
            'desc':sectiondesc,
            'activests':activests,
            'sub_secid':sub_secid,
            'uid':request.session['uid']} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url,data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        print("api_data-----------------",api_data)      
        # objmaster.addSub_Sub_Section(sub_secid,section,sectiondesc,activests,str(request.session['uid']))
        return JsonResponse({'is_taken':True})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 


def addUdaapSub_Sub_Sub_Section(request):
    try:   
        section =request.GET.get('section', 'False') 
        sectiondesc =request.GET.get('sectiondesc', 'False') 
        activests =request.GET.get('activests', 'False')    
        sub_secid =request.GET.get('sub_secid', 'False')  

        api_url=getFLAPIURL()+"addUdaapSubSubSubSection/"       

        data_to_save={        
            'text':section, 
            'desc':sectiondesc,
            'activests':activests,
            'sub_secid':sub_secid,
            'uid':request.session['uid']} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url,data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        print("api_data-----------------",api_data)     
        # objmaster.addSub_Sub_Sub_Section(sub_secid,section,sectiondesc,activests,str(request.session['uid']))
        return JsonResponse({'is_taken':True})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 


def showUdaapSetting(request):
    try: 
        api_url=getFLAPIURL()+"UdaapSettingAPI/"       
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url,headers=header)         
        api_data=response.json()
        print("api_data-----------------",api_data) 
        return render(request, 'UdaapSettingLst.html',{ 'actPage':'Departments','users':api_data['users']})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())


def newUdaapSetting(request):
    try:   
        print('inside newUdaapSetting')
        return render(request, 'addUdaapSetting.html',{ 'actPage':'Add Department'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())

def addUdaapSetting(request):
    try: 
        icqnameVal=request.GET['icqname']  
        remarksVal=request.GET['remarks']  
        enddateVal=request.GET['enddate']
        userid=str(request.session['uid'])
        # strQ="INSERT INTO ICQ_Setting (ICQS_Text ,ICQS_Remarks,ICQS_EndDate,AddedBy,AddDate,publish) "
        # strQ += " VALUES('"+ icqnameVal.replace("'","''")+"','"+ remarksVal.replace("'","''")+"','"+ enddateVal +"','"+ userid +"',getdate(),0)"
        # print(strQ)
        # insertRow(strQ)

        api_url=getFLAPIURL()+"UdaapSettingAPI/"       

        data_to_save={        
            'fls_text':icqnameVal, 
            'fls_remarks':remarksVal,
            'fls_enddate':enddateVal,
            'addedby':request.session['uid']} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url,data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()
        print("api_data-----------------",api_data)
        return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})


def allocate_udaap(request): 
    try:
        if request.method=="POST":
            section=request.POST.get('section','False')
            sub_section=request.POST.get('sub_section','False')
            sub_sub_section=request.POST.get('sub_sub_section','False')
            sub_sub_sub_section=request.POST.get('sub_sub_sub_section','False')

            
            print(section,sub_section,sub_sub_section,sub_sub_sub_section)


        
            api_url=getFLAPIURL()+"UdaapAllocation/"       

            data_to_get={        
                'section':section,
                'sub_section':sub_section ,
                'sub_sub_section':sub_sub_section,
                'sub_sub_section':sub_sub_section,
                'sub_sub_sub_section':sub_sub_sub_section
            }


            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.get(api_url,data= json.dumps(data_to_get),headers=header)
            
            api_data=response.json()
            print("api_data udaap setting-----------------",api_data) 
            return JsonResponse(api_data,safe=False)
        

        api_url=getFLAPIURL()+"getUdaapAllocation/"       

        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url,headers=header)
         
        api_data=response.json()
        print("api_data-----------------",api_data)

        # return render(request,'allocate_udaap.html',{'sections':objmaster.getSections(),'user':userobj,'review':objmaster.getICQIds()})
        return render(request,'allocate_udaap.html',{'sections':api_data['sections'],'user':api_data['user'],'review':api_data['review']})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 


def save_Udaap_allocation(request):
    request_data = {x:request.GET.get(x) for x in request.GET.keys()}
    section_aid = request.GET.getlist('section_aid[]')
    users = request.GET.getlist('users[]')
    api_url=getFLAPIURL()+"save_udaap_allocation/"       
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

from fpdf import FPDF, HTMLMixin

class MyFPDF(FPDF, HTMLMixin):
    pass

