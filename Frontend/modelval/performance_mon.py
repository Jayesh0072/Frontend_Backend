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
import datetime
from datetime import date

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
from rest_framework.response import Response
from pymongo import MongoClient
import environ
env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent

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




def getAPIURL():
    api_url=os.environ['API_URL']
    return api_url

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
        print("check data pm-----",data)
        return render(request, 'PerfMontrSetup_MRM.html',{'data':data['mdlids'],'freqdata':data['frequency'],'ModelMatrics':data['mdlmetric'],'BusinessMetric':data['businessmetric'],'data_mdlids':data['data_mdlids']})
     
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())


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



# def savemodelmatrics(request):
#     print("request data model matrics",request.GET)
#     try: 
#         datalist = json.loads(request.GET['datalist'])
#         print("datalist",datalist)
#         mdlid = request.GET['mdlId']
#         print("mdlid",mdlid)
#         frequency = request.GET['frequency']
#         api_url=getAPIURL()+"ModelMatricsAPI/"  
#         for i in datalist:   
#             data_to_save={ 
#                 'mdl_id': mdlid,
#                 'metric':i['AID'],
#                 'threshold':int(i['Threshold']),
#                 'warning':int(i['Warning']),
#                 'frequency':frequency,
#                 'metric_value_type':i['Percentage'],
#                 'added_by':request.session['uid']
#             } 
#             header = {
#             "Content-Type":"application/json",
#             'Authorization': 'Token '+request.session['accessToken']
#             }
#             response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
            
#         return JsonResponse({'istaken':'true'})
#     except Exception as e:
#         print('assignValidation ',e)
#         print('assignValidation traceback is ', traceback.print_exc()) 
#         return JsonResponse({'istaken':'false'})



# def savebusinessmatrics(request):
#     print("request data business matrics",request.GET)
#     try: 
#         datalist = json.loads(request.GET['datalist'])
#         print("datalist",datalist)
#         mdlid = request.GET['mdlId']
#         print("mdlid",mdlid)
#         frequency = request.GET['frequency']
#         api_url=getAPIURL()+"BusinessMetricAPI/"  
#         for i in datalist: 
#             print("i",i)
#             print("threshold",str(i['Threshold']),"warning",str(i['Warning']))    
#             data_to_save={ 
#                 'mdl_id': mdlid,
#                 'metric':i['AID'],
#                 'threshold':int(i['Threshold']),
#                 'warning':int(i['Warning']),
#                 'frequency':frequency,
#                 'metric_value_type':i['Percentage'],
#                 'added_by':request.session['uid']
#             } 
#             header = {
#             "Content-Type":"application/json",
#             'Authorization': 'Token '+request.session['accessToken']
#             }
#             response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
#             print("response business metric",response.content)
#         return JsonResponse(json.loads(response.content))
#     except Exception as e:
#         print('assignValidation ',e)
#         print('assignValidation traceback is ', traceback.print_exc()) 
#         return JsonResponse({'istaken':'false'})



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

# def find_src_data(file_id,dataset=''): 
#     print('dataset is method is ',dataset)
#     if(dataset==''):
#         print('inside blank filter')
#         src_file_obj = collection.find({"file_id":int(file_id)},{'_id':0})
#     else:
#         print('dataset ', str(dataset)) 
#         dataset = dataset.replace("\'", "\"") 
#         dataset=json.loads(dataset)    
#         print('dataset is ',dataset)      
#         src_file_obj = collection.find(dataset,{'_id':0})

#     df =  pd.DataFrame(list(src_file_obj))   
#     if len(df)>0: 
#         df.pop('file_id')
#     print("src fn dataframe",len(df))
#     return df 


# def SaveTempFeatureMatricData(request):
#     try:
#         import statistics
#         mdl_id = request.GET.get('mdl_id', 'False') 
#         feature = request.GET.get('feature', 'False')
#         print("feature",feature)
#         data_matric = request.GET.get('data_matric', 'False') 

#         file_id=find_max_file_id(mdl_id)
#         dataset = ''
#         df=find_src_data(file_id,dataset)
#         print("feature column data",df[feature])
#         if data_matric == 'Null':
#             columndata = df[feature].isnull().sum()
#             print("isnull column",columndata/len(df[feature])*100)
#             percentage = columndata/len(df[feature])*100
#         elif data_matric == 'Mean':
#             columndata = df[feature].mean()
#             print("columndata mean",columndata)
#             percentage = columndata
#         elif data_matric == 'Median':
#             columndata = df[feature].to_list()
#             percentage = statistics.median(columndata)
#             print("Median",percentage)
#         elif data_matric == 'STD':
#             columndata = df[feature].std()
#             print("columndata Standard deviation",columndata)
#             percentage = columndata

#         third_party_api_url = getAPIURL()+'SaveTempFeatureMatricSelection/'
#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }

#         data_to_save = {
#             'mdl_id':mdl_id,
#             'feature':feature,
#             'datamatrics':data_matric,
#             'added_by':request.session['uid']
#         }
#         responseget = requests.get(third_party_api_url, data= json.dumps(data_to_save),headers=header)
        
#         data = json.loads(responseget.content)

#         print('response get',data['data'])

#         if len(data['data']) == 0:
#             responsesave = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
#             print('response save',responsesave.content)
#             data = json.loads(responsesave.content)
#             data['percentage'] = percentage
#             print("New Data",data)
#             return JsonResponse(data)
#             # return JsonResponse({'msg':'Feature Data created Successfully','null_percentage':null_percentage})
#         else:
#             return JsonResponse({'msg':'Data Already Exist','percentage':percentage})

#     except Exception as e:
#         print('adduser is ',e)
#         print('adduser traceback is ', traceback.print_exc())

def SaveTempFeatureMatricData(request):
    try:
        mdl_id = request.GET.get('mdl_id', 'False') 
        feature = request.GET.get('feature', 'False')
        print("feature",feature)
        data_matric = request.GET.get('data_matric', 'False')  
        df=find_src_data(mdl_id,request.session['accessToken']) 
        print("feature column data",df[feature])
        if data_matric == 'Null':
            columndata = df[feature].isnull().sum()
            print("isnull column",columndata/len(df[feature])*100)
            # percentage = columndata/len(df[feature])*100
            percentage = (columndata / len(df[feature]) * 100) if len(df[feature]) != 0 else 0
        elif data_matric == 'Mean':
            columndata = df[feature].mean()
            print("columndata mean",columndata)
            percentage = columndata
        elif data_matric == 'Median':
            columndata = df[feature].to_list()
            import statistics
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
        print("responseget--------------------------",data['mmdata'])
        print('len of newval ',(data['overdata']) )
        for ir,val in data['overdata'].items():
                print('metric and newval ',val['metric'] , val['new_value'])

        exclfile = pd.read_excel(os.path.join(BASE_DIR, 'static/document_files/'+mdlid+'/'+'production_output/'+mdlid+'.xlsx'))
        print("exclfile-------",exclfile)
        
        arrMetricType=[]
        frequency=""

        for i in data['mmdata']:
            print("label check",i['mm_details']['mm_label'])
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

def Save_Performance_Monitoring_Resolution(request):
    try:
        #Mdl_ID,Metric,New_Value,Added_by,Added_On
        print("request_data",request.GET)
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


# def PerfMontrPrdnData(request):
#     try:  
#         third_party_api_url = getAPIURL()+'FetchPerfMonMdlId/'
#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }

#         data_to_get = {
#             'dept_aid':request.session['dept']
#         }
#         responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        
#         data=responseget.json() 

#         return render(request, 'PerfMontrPrdnData.html',{'data':data['data'],'buss_data':data['buss_data']})
#     except Exception as e:
#         print('adduser is ',e)
#         print('adduser traceback is ', traceback.print_exc())

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
        print("data------------123",data)
        
        return render(request, 'PerfMontrPrdnData.html',{'data':data['data'],'buss_data':data['buss_data']})
    except Exception as e:
        print('adduser is ',e)  
        print('adduser traceback is ', traceback.print_exc())

# def ModelMatricsData(request):
#     try:
#         print("request_data",request.GET)
#         modelmatrics = request.GET.get('modelmatrics','false')
#         mdlid = request.GET.get('mdlid','false')
#         datatype = request.GET.get('datatype','false')

#         third_party_api_url = getAPIURL()+'ModelMatricDataAPI/'
#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }
#         data_to_get = {
#             'model_matrics':modelmatrics,
#             'mdlid':mdlid,
#             'datatype':datatype
#         }
#         responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
#         data=json.loads(responseget.content)
#         print("responseget for model matrics updated new--------------------------",data['data'])
#         print("responseget for model matrics updated new moving--------------------------",data['mdldata'])

#         first_key = next(iter(data['data']))
#         print("first_key",first_key,data['data'][first_key])
#         chartData=[float(i) for i in data['data'][first_key]]

#         print('chartData ',chartData)
#         mean = np.mean(chartData)  
#         std_dev = np.std(chartData)  

#         # Control limits
#         UCL = mean + 3 * std_dev
#         LCL = mean - 3 * std_dev


#         #Moving data
#         mean_1 = np.mean(data['mdldata'])  
#         std_dev_1 = np.std(data['mdldata'])  

#         # Control limits
#         UCL_1 = mean_1 + 3 * std_dev_1
#         LCL_1 = mean_1 - 3 * std_dev_1

#         data = {
#             'data' : data['data'][first_key],
#             'mean' : mean,
#             'UCL' : UCL,
#             'LCL':LCL,
#             'date':data['data']['adddate'],
#             'data_1':data['mdldata'],
#             'mean_1':mean_1,
#             'std_dev_1':std_dev_1,
#             'UCL_1':UCL_1,
#             'LCL_1':LCL_1
#         }

#         print("data",data)

#         return JsonResponse({"data":data})
#     except Exception as e:
#         print("error is",e)

def ModelMatricsData(request):
    try:
        print("request_data ModelMatricsData",request.GET)
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

        third_party_api_url = getAPIURL()+'GetHistoryMsg/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        data_to_get = {
            'model_matrics':modelmatrics,
            'room_id':"Perfm_"+mdlid,
            'mdl_id':mdlid,
            'addedby':request.session['uid'],
            'datatype':datatype
        }
        responseget_a = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        print("response for warning",json.loads(responseget_a.content))
        if datatype != 'Business':
            filtered_data = [d for d in json.loads(responseget_a.content)['mmdata_a'] if d['mdl_id'] == mdlid and  d["mm_details"]["mm_label"] == modelmatrics]
            print("filtered_data------",filtered_data)
            warning = filtered_data[0]['warning']
        else:
            filtered_data_bussiness = [d for d in json.loads(responseget_a.content)['bmdata_b'] if d['mdl_id'] == mdlid and  d["bm_details"]["bm_label"] == modelmatrics]
            warning = filtered_data_bussiness[0]['warning']
        # for i in json.loads(responseget_a.content)['chartdata'] :
        #     print("check i--------",i)

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
            'LCL_1':LCL_1,
            'warning':warning
        }

        print("data-----------------------chk 1",data)

        return JsonResponse({"data":data})
    except Exception as e:
        print("error is",e)
        print('error traceback is ', traceback.print_exc())
        return JsonResponse({"data":None})


# def mmlabeltoexcel(request):
#     try:
#         third_party_api_url = getAPIURL()+'getMaxFreqSeq/'
#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }
#         freidx=1
#         is_new=0
#         data_to_save = {
#             'mdl_id':request.GET.get('mdlid', 'False')  
#         }
#         responseget = requests.get(third_party_api_url, data= json.dumps(data_to_save),headers=header)             
#         data=responseget.json() 
#         for ir,val in data['freqData'].items():
#             is_new=val['addorupdate']
#             freidx=val['freqidx']
#         mdlid =request.GET.get('mdlid', 'False') 

#         third_party_api_url = getAPIURL()+'getTemplateData/'
#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }

#         data_to_get = { 
#             'mdl_id':mdlid ,
#             'freq_idx':freidx
#         }
#         responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
#         # data=json.loads(responseget.content)
#         data=responseget.json()
#         # print("responseget--------------------------",data['mmdata']) 
#         lst = []
#         for i in data['mmdata']:
#             lst.append(i['mm_details']['mm_label'])
#         print("new label lst",lst)
#         dframe1 = pd.DataFrame(index = ['0'],columns = lst)  
#         print("dframe",dframe1)
#         BASE_DIR = Path(__file__).resolve().parent.parent 
               
#         destination_path = str(BASE_DIR)+'/static/document_files/'+ mdlid +'/templates/'     
#         # destination_path = os.path.join(BASE_DIR, 'static\\document_files\\'+mdlid+'\\')
#         if not os.path.exists(destination_path):
#             os.makedirs(destination_path)           
#         # dframe1.to_excel( str(BASE_DIR) + '/static/document_files/'+ mdlid + '/'+mdlid+'.xlsx',index=False)
#         dframe1.to_excel(destination_path + mdlid+'.xlsx',index=False)

#         modelmatrics = request.GET.get('modelmatrics','false')
#         mdlid = request.GET.get('mdlid','false')
#         datatype = request.GET.get('datatype','false')
#         try:
#             third_party_api_url = getAPIURL()+'MdlIdDataCheck/'
#             header = {
#             "Content-Type":"application/json",
#             'Authorization': 'Token '+request.session['accessToken']
#             }
#             data_to_get = {
#                 'mdlid':mdlid,
#             }
#             responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
#             data=json.loads(responseget.content)
#             print("responseget for model matrics updated new for hide--------------------------",data['data_a'])
#             data_check = data['data_a']
#         except Exception as e:
#             print("error data is",e)
#             data_check = 'None'
#         return JsonResponse({'file': '/static/document_files/'+ mdlid +'/templates/' +mdlid+'.xlsx','msg':"Excel Downloaded successfully",'model_matrics':lst,'data_check':data_check})
#     except Exception as e:
#         print('adduser is ',e)
#         print('adduser traceback is ', traceback.print_exc())

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
        print("responseget new api fetch mmlabel agains mdlid--------------------------",data['mmdata'])
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
        print('error is ',e)
        print('error traceback is ', traceback.print_exc())


# def mmlabeltoexcelforbus(request):
#     try:
#         print("request data-------------",request.GET.get)
#         mdlid =request.GET.get('mdlid', 'False') 

#         third_party_api_url = getAPIURL()+'GetHistoryMsg/'
#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }

#         data_to_get = {
#             'room_id':"",
#             'mdl_id':mdlid,
#             'addedby':request.session['uid']
#         }
#         responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
#         # data=json.loads(responseget.content)
#         data=responseget.json()
#         # print("responseget--------------------------",data['mmdata'])
#         print("responseget new api fetch bmlabel agains mdlid--------------------------",data['bmdata_b'])
#         lst = []
#         for i in data['bmdata_b']:
#             lst.append(i['bm_details']['bm_label'])
#         print("new label lst",lst)
#         dframe1 = pd.DataFrame(index = ['0'],columns = lst)  
#         BASE_DIR = Path(__file__).resolve().parent.parent      
#         destination_path = str(BASE_DIR)+'/static/document_files/'+mdlid +'/templates/'     
#         # destination_path = os.path.join(BASE_DIR, 'static\\document_files\\'+mdlid+'\\')
#         if not os.path.exists(destination_path):
#             os.makedirs(destination_path)           
#         # dframe1.to_excel( str(BASE_DIR) + '/static/document_files/'+ mdlid + '/'+mdlid+'.xlsx',index=False)
#         dframe1.to_excel(destination_path + 'Business_KPI_'+mdlid+'.xlsx',index=False)
#         return JsonResponse({'file': '/static/document_files/'+mdlid +'/templates/Business_KPI_'+mdlid+'.xlsx','msg':"Excel Downloaded successfully"})
#     except Exception as e:
#         print('error is ',e)
#         print('error traceback is ', traceback.print_exc())
 
def mmlabeltoexcelforbus(request):
    try:
        print("request data-------------bus",request.GET)
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
        return JsonResponse({'file': '/static/document_files/'+mdlid +'/templates/Business_KPI_'+mdlid+'.xlsx','msg':"Excel Downloaded successfully",'business_matrics':lst})
    except Exception as e:
        print('error is ',e)
        print('error traceback is ', traceback.print_exc())


 
# def Perf_monitoring_file_upload(request):
#     try:
#         mdl_id = request.POST.get('mdl_id','false')
        
#         filename_a = request.POST.get('filenm','none') 
#         historical = request.POST.get('historical','none')
#         print("historical",historical)
#         utility_type = request.POST.get('utility_type','none')
        
#         files = request.FILES
#         myfile = files.get('filename', None) 
#         df1 = pd.read_excel(myfile) 
#         ### Historical Condition
#         if historical == 'true':
#             print("historical")
#             third_party_api_url = getAPIURL()+'getMaxFreqSeq/'
#             header = {
#             "Content-Type":"application/json",
#             'Authorization': 'Token '+request.session['accessToken']
#             }
#             freidx=1
#             is_new=0
#             data_to_save = {
#                 'mdl_id':mdl_id  
#             }
#             responseget = requests.get(third_party_api_url, data= json.dumps(data_to_save),headers=header)             
#             data=responseget.json() 
#             for ir,val in data['freqData'].items():
#                 is_new=val['addorupdate']
#                 freidx=val['freqidx']
#             # mdlid =request.GET.get('mdlid', 'False') 

#             third_party_api_url = getAPIURL()+'getTemplateData/'
#             header = {
#             "Content-Type":"application/json",
#             'Authorization': 'Token '+request.session['accessToken']
#             }
#             data_to_get = { 
#                 'mdl_id':mdl_id ,
#                 'freq_idx':freidx
#             }
#             responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
#             # data=json.loads(responseget.content)
#             data=responseget.json()
#             # print("responseget--------------------------",data['mmdata'])
#             print("responseget new api fetch mmlabel agains mdlid--------------------------",data['mmdata'])
#             lst = []
#             for i in data['mmdata']:
#                 lst.append(i['mm_details']['mm_label'])
#             print("new label lst",lst)
#             dframe1 = pd.DataFrame(index = ['0'],columns = lst)
#             exceldf = dframe1.to_json(orient="records")
#             print("df2 columns",dframe1.columns.to_list())
#             excel_fields = df1.columns.to_list()
#             excel_fields_1  = df1.to_json(orient="records")
#             print("df1 columns",df1.columns.to_list())

#             if list(dframe1.columns.values) == list(df1.columns.values): 
#                 third_party_api_url  = getAPIURL()+'PerfMontrMappingAPI/'
#                 data_to_save={ 
#                     'addedby':request.session['uid'],
#                     'excel_fields':excel_fields,
#                     'department':"MRM",
#                     'portfolio':"MRM",
#                     'exceldf':json.loads(excel_fields_1),
#                     'mdl_id':mdl_id,
#                     'datatype':utility_type
#                     } 
#                 header = {
#                 "Content-Type":"application/json",
#                 'Authorization': 'Token '+request.session['accessToken']
#                 }
#                 responsepost = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)    
#                 api_data=responsepost.json()
#                 print("api data perf montr mapping------------",api_data)
#                 return JsonResponse(api_data)
#             else:
#                 print("false only")
#                 return JsonResponse({'isvalid':'false'})
#         else:
#             pass
#         ###
#         filename = filename_a.split('.')
#         BASE_DIR = Path(__file__).resolve().parent.parent
            
#         file_check_path = str(BASE_DIR)+'/static/document_files/'+ mdl_id + '/' +'templates/' +mdl_id+".xlsx" 
#         df2 = pd.read_excel(file_check_path) 
#         if list(df1.columns.values) == list(df2.columns.values): 
#             if filename_a != None and myfile != None:
#                 fs = FileSystemStorage() 
#                 filePath=os.path.join(BASE_DIR, 'static/document_files/'+mdl_id+'/'+'production_output/'+filename_a)
#                 if os.path.exists(filePath): 
#                     os.remove(filePath)
#                     print("remove filename",filePath)
#                 fs.save(os.path.join(BASE_DIR, 'static/document_files/'+mdl_id+'/'+'production_output/'+filename_a), myfile) 

#                 third_party_api_url = getAPIURL()+'getMaxFreqSeq/'
#                 header = {
#                 "Content-Type":"application/json",
#                 'Authorization': 'Token '+request.session['accessToken']
#                 }
#                 freidx=1
#                 is_new=0
#                 data_to_save = {
#                     'mdl_id':mdl_id, 
#                 }
#                 responseget = requests.get(third_party_api_url, data= json.dumps(data_to_save),headers=header)             
#                 data=responseget.json() 
#                 for ir,val in data['freqData'].items():
#                     is_new=val['addorupdate']
#                     freidx=val['freqidx']
#                 if historical == 'true':
#                     print("historical")
#                 else:
#                     pass
#                 third_party_api_url = getAPIURL()+'perfMonitoringFileInfoAPI/'
#                 header = {
#                 "Content-Type":"application/json",
#                 'Authorization': 'Token '+request.session['accessToken']
#                 }

#                 data_to_save = {
#                     'mdl_id':mdl_id,
#                     'file_nm':filename_a,
#                     'added_by':request.session['uid'],
#                     'freq_idx':freidx,
#                     'is_new':is_new
#                 }
#                 responseget = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
#                 # data=json.loads(responseget.content)
#                 print("response--------------------------",json.loads(responseget.content))
#                 return JsonResponse({"isvalid":"true"})
#             else:
#                 return JsonResponse({"isvalid":"false"})
#         else:
#             print("columns are not same")
#             return JsonResponse({"isvalid":"false"})
#     except Exception as e:
#         print("file error is ",e)

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
        print("df1",df1)

        ##email send code to owner and mrm_head
        BASE_DIR = Path(__file__).resolve().parent.parent
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
        third_party_api_url = getAPIURL()+'getTemplateData/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'room_id':"",
            'mdl_id':mdl_id,
            'addedby':request.session['uid'],
            'freq_idx':freidx
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        # data=json.loads(responseget.content)
        data=responseget.json()
        print("responseget--------------------------",data['mmdata'])
        print('len of newval ',(data['overdata']) )
        for ir,val in data['overdata'].items():
                print('metric and newval ',val['metric'] , val['new_value'])

        exclfile = pd.read_excel(os.path.join(BASE_DIR, 'static/document_files/'+mdl_id+'/'+'production_output/'+mdl_id+'.xlsx'))
        print("exclfile-------",exclfile)
        
        arrMetricType=[]
        frequency=""
        try:
            for i in data['mmdata']:
                print("label check",i['mm_details']['mm_label'])
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
        except Exception as e:
            print("check error is---",e,e.__traceback__)   
        print("metrictype",metrictype)

        third_party_api_url = getAPIURL()+'perfMonitoring_email_send/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        
        data_to_save = {
            'metrictype':metrictype, 
            'mdl_id':mdl_id,
        }
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)             
        data_email=responseget.json()
        print("data_email",data_email)
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
            lst.append('date')
            dframe1 = pd.DataFrame(index = ['0'],columns = lst)
            exceldf = dframe1.to_json(orient="records")
            print("df2 columns",dframe1.columns.to_list())
            excel_fields = df1.columns.to_list()
            excel_fields_1 = df1.to_json(orient="records")
            print("df1 columns",df1.columns.to_list())
            model_matrics_df = df1.to_dict(orient="records")
            print("df1 dataframe",model_matrics_df)

            if list(dframe1.columns.values) == list(df1.columns.values): 
                third_party_api_url  = getAPIURL()+'PerfMontrMappingAPI/'
                data_to_save={ 
                    'addedby':request.session['uid'],
                    'excel_fields':excel_fields,
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
                api_data['model_matrics'] = dframe1.columns.to_list()
                api_data['model_matrics_data'] = model_matrics_df
                print("api data perf montr mapping------------",api_data)
                print("correct historical")
                return JsonResponse(api_data)
            else:
                print("false only")
                return JsonResponse({'isvalid':'false','msg':'something went wrong'})
        else:
            pass
        ###
        filename = filename_a.split('.')
        BASE_DIR = Path(__file__).resolve().parent.parent
            
        file_check_path = str(BASE_DIR)+'/static/document_files/'+ mdl_id + '/' +'templates/' +mdl_id+".xlsx" 
        df2 = pd.read_excel(file_check_path) 
        print("df2",df2)
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
                print("response check perfMonitoringFileInfoAPI--------------------------",json.loads(responseget.content))

                return JsonResponse({"isvalid":"true","msg":json.loads(responseget.content)['msg']})
            else:
                return JsonResponse({"isvalid":"false"})
        else:
            print("columns are not same")
            return JsonResponse({"isvalid":"false"})
    except Exception as e:
        print("file error is ",e)




# def Perf_monitoring_file_upload_bus(request):
#     mdl_id = request.POST.get('mdl_id','false')
    
#     historical = request.POST.get('historical','none')
#     print("historical",historical)
#     utility_type = request.POST.get('utility_type','none')
#     filename_a = request.POST.get('filenm','none')
    
#     files = request.FILES
#     myfile = files.get('filename', None) ####

#     df1 = pd.read_excel(myfile)
#     print("df1-----------",list(df1.columns.values))
#     ####
#     if historical == 'true':        
#         third_party_api_url = getAPIURL()+'GetHistoryMsg/'
#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }
#         data_to_get = {
#             'room_id':"",
#             'mdl_id':mdl_id,
#             'addedby':request.session['uid']
#         }
#         responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
#         # data=json.loads(responseget.content)
#         data=responseget.json()
#         # print("responseget--------------------------",data['mmdata'])
#         print("responseget new api fetch bmlabel agains mdlid--------------------------",data['bmdata_b'])
#         lst = []
#         for i in data['bmdata_b']:
#             lst.append(i['bm_details']['bm_label'])
#         print("new label lst",lst)
#         dframe1 = pd.DataFrame(index = ['0'],columns = lst)
#         print("--------------------Business---------------------------")
#         exceldf = dframe1.to_json(orient="records")
#         print("df2 columns",dframe1.columns.to_list())
#         excel_fields = df1.columns.to_list()
#         excel_fields_1  = df1.to_json(orient="records")
#         print("df1 columns",df1.columns.to_list())

#         if list(dframe1.columns.values) == list(df1.columns.values): 
#             third_party_api_url  = getAPIURL()+'PerfMontrMappingAPI/'
#             data_to_save={ 
#                 'addedby':request.session['uid'],
#                 'excel_fields':excel_fields,
#                 'department':"MRM",
#                 'portfolio':"MRM",
#                 'exceldf':json.loads(excel_fields_1),
#                 'mdl_id':mdl_id,
#                 'datatype':utility_type
#                 } 
#             header = {
#             "Content-Type":"application/json",
#             'Authorization': 'Token '+request.session['accessToken']
#             }
#             responsepost = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)    
#             api_data=responsepost.json()
#             print("api data perf montr mapping business------------",api_data)
#             return JsonResponse(api_data)
#     else:
#         print("false only")
#         return JsonResponse({'isvalid':'false'})
#     ####
#     filename = filename_a.split('.')
#     print("filename",filename[0])
#     BASE_DIR = Path(__file__).resolve().parent.parent        
#     file_check_path = str(BASE_DIR)+'/static/document_files/'+ mdl_id + '/' +'templates/' +filename_a
#     print("file_check_path",file_check_path)
#     df2 = pd.read_excel(file_check_path)
#     print("df2------------",list(df2.columns.values))
#     if list(df1.columns.values) == list(df2.columns.values):
#         print("columns are same")
#         if filename_a != None and myfile != None:
#             fs = FileSystemStorage() 
#             filePath=os.path.join(BASE_DIR, 'static/document_files/'+mdl_id+'/'+'production_output/'+filename_a)
#             if os.path.exists(filePath): 
#                 os.remove(filePath)
#                 print("remove filename",filePath)
#             fs.save(os.path.join(BASE_DIR, 'static/document_files/'+mdl_id+'/'+'production_output/'+filename_a), myfile) 

#             third_party_api_url = getAPIURL()+'getMaxFreqSeq_Buss/'
#             header = {
#             "Content-Type":"application/json",
#             'Authorization': 'Token '+request.session['accessToken']
#             }
#             freidx=1
#             is_new=0
#             data_to_save = {
#                 'mdl_id':mdl_id, 
#             }
#             responseget = requests.get(third_party_api_url, data= json.dumps(data_to_save),headers=header)             
#             data_maxfreq=responseget.json() 
#             for ir,val in data_maxfreq['freqData'].items():
#                 is_new=val['addorupdate']
#                 freidx=val['freqidx']

#             third_party_api_url = getAPIURL()+'perfMonitoringFileInfoAPI/'
#             header = {
#             "Content-Type":"application/json",
#             'Authorization': 'Token '+request.session['accessToken']
#             }

#             data_to_save = {
#                 'mdl_id':mdl_id,
#                 'file_nm':filename_a,
#                 'added_by':request.session['uid'],
#                 'freq_idx':freidx,
#                 'is_new':is_new
#             }
#             responseget = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
#             # data=json.loads(responseget.content)
#             print("response--------------------------",json.loads(responseget.content))
#             return JsonResponse({"isvalid":"true"})
#         else:
#             return JsonResponse({"isvalid":"false"})
#     else:
#         print("columns are not same")
#         return JsonResponse({"isvalid":"false"})

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
        # return JsonResponse({'isvalid':'false'})
        pass
    ####
    filename = filename_a.split('.')
    print("filename",filename[0])
    BASE_DIR = Path(__file__).resolve().parent.parent        
    file_check_path = str(BASE_DIR)+'/static/document_files/'+ mdl_id + '/' +'templates/' +'Business_KPI_'+mdl_id+".xlsx"
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
            return JsonResponse({"isvalid":"true","msg":json.loads(responseget.content)['msg']})
        else:
            return JsonResponse({"isvalid":"false","msg":"something went wrong"})
    else:
        print("columns are not same")
        return JsonResponse({"isvalid":"false"})

user_name = "user1"

 
# def home2(request):
#     print("in home2")
#     try:
#         mdlId =request.POST.get('mdlid', 'False')
#         _isDisabled="disabled"
#         _xFiles=[".csv","_x_model.csv","_x_keep.csv","_x_dummy.csv","_x_scaled.csv","_x_final.csv"]
#         file_name = mdlId+'_'+"csvfile_"+user_name
#         filepath1 = os.path.join(BASE_DIR, 'static/document_files/'+mdlId+'/'+'production_output/')
#         savefile_name = filepath1 + file_name + ".csv" 
#         print("savefile_name",savefile_name)
#         processing = os.path.join(BASE_DIR, 'static/reportTemplates/processing.csv')
#         df_old_proc = pd.read_csv(processing) 
#         statusReq=df_old_proc.loc[df_old_proc.Idx == 1, "Status"] 
#         del df_old_proc


#         print("if post ")
#         filename_a = request.POST.get('filenm','none')
#         print(' filename ',filename_a)
#         files = request.FILES
#         myfile = files.get('filename', None)
#         print('myfile ',myfile,' filename ',filename_a)

#         fs = FileSystemStorage()
#         print("myfile",myfile)
#         for f in _xFiles: 
#             if os.path.exists(filepath1 + file_name +f):
#                 os.remove(filepath1 + file_name +f)

#         file_name = mdlId+'_'+str(myfile)
#         savefile_name = filepath1 + file_name
#         print("savefile_name",savefile_name)
#         fs.save(savefile_name, myfile)
        
#         if os.path.exists(savefile_name):
#             df = pd.read_csv(savefile_name, encoding='utf-8')
#             # print('printing datatypes ')
#             print("DF new",df)
#             dttypes = dict(df.dtypes)
#             file_id=find_max_prdn_file_id("") 
#             print("file_id",file_id)
#             data_model=df.to_dict('records')
#             #print("data_model",data_model)
#             for i in data_model:
#                     keys_data=list()
#                     keys_data.append(list(i.keys()))    ##column name
#             Freq_Idx=1
#             uploaded_on=datetime.datetime.now()  ##uploaded on data
#             file_info_data={'Mdl_Id':mdlId,'Freq_Idx':Freq_Idx,'file_id':int(file_id),'file_columns':keys_data,'file_name':file_name,'uploaded_by':"User","uploaded_on":uploaded_on}
                
#             if file_id==int(0):  
#                 file_info_data['file_id']=file_info_data['file_id'] + 1
#                 collection_prdn_file_info.insert_one(file_info_data)  
#                 # src_data_dict={}
#                 for i in data_model:                        
#                     src_data_dict=i
#                     src_data_dict.update({'file_id':file_info_data['file_id']}) 
#                     collection_prdn_src_data.insert_one(i)
#             else:
            
#                 file_info_data['file_id']=file_info_data['file_id'] + 1
#                 collection_prdn_file_info.insert_one(file_info_data)  
                
#                 for i in data_model: 
#                     src_data_dict=i
#                     src_data_dict.update({'file_id':file_info_data['file_id']}) 
#                     collection_prdn_src_data.insert_one(i)

#             objmaster.insertActivityTrail(mdlId,"17","Model source data imported.",request.session['uid'],request.session['accessToken'])

#         arrdescData = []
#         gridDttypes = []
#         result = ""
#         #file_name=myfile
        
#         for key, value in dttypes.items():
#             gridDttypes.append({'colName': key, 'dataType': value})
#         print("gridDttypes",gridDttypes)
#         dfdisplay = df.head(100)
#         result = dfdisplay.to_json(orient="records")
#         result = json.loads(result)
#         print("result",result)
#         _isDisabled=""
#         # return JsonResponse({'isDisabled':_isDisabled,'desc': arrdescData, 'dataTypes': gridDttypes, 'df': result})
#         third_party_api_url = getAPIURL()+'getMaxFreqSeqData/'
#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }
#         freidx=1
#         is_new=0
#         data_to_save = {
#             'mdl_id':mdlId, 
#         }
#         responseget = requests.get(third_party_api_url, data= json.dumps(data_to_save),headers=header)             
#         data=responseget.json() 
#         for ir,val in data['freqData'].items():
#             is_new=val['addorupdate']
#             freidx=val['freqidx']


#         third_party_api_url = getAPIURL()+'DataMonitoringFileInfoAPI/'
#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }

#         data_to_save = {
#             'mdl_id':mdlId,
#             'file_nm':filename_a,
#             'added_by':request.session['uid'],
#             'freq_idx':freidx,
#             'is_new':is_new
#         }
#         responseget = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
#         # data=json.loads(responseget.content)
#         print("response--------------------------",json.loads(responseget.content))
#         return JsonResponse({'isvalid':'true'})
        
#     except Exception as e:
#         print(e)
#         print('traceback is ', traceback.print_exc())
#         return render(request, 'error.html')

cluster=MongoClient('localhost',27017,connect=False)
 
db=cluster["ModelValidation"]
collection_prdn_file_info=db['Prdn_File_Info']
collection_prdn_src_data=db['Prdn_Src_Data']




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



def home2(request):
    print("in home2----------------------------")
    try:
        mdlId =request.POST.get('mdlid', 'False')
        print("mdlid------------------",mdlId)
        _isDisabled="disabled"
        _xFiles=[".csv","_x_model.csv","_x_keep.csv","_x_dummy.csv","_x_scaled.csv","_x_final.csv"]
        file_name = mdlId+'_'+"csvfile_"+user_name
        filepath1 = os.path.join(BASE_DIR, 'static/document_files/'+mdlId+'/'+'production_output/')
        savefile_name = filepath1 + file_name + ".csv" 
        print("savefile_name",savefile_name)
        processing = os.path.join(BASE_DIR, 'static/reportTemplates/processing.csv')
        df_old_proc = pd.read_csv(processing) 
        statusReq=df_old_proc.loc[df_old_proc.Idx == 1, "Status"] 
        del df_old_proc


        print("if post ")
        filename_a = request.POST.get('filenm','none')
        print(' filename ',filename_a)
        files = request.FILES
        myfile = files.get('filename', None)
        print('myfile ',myfile,' filename ',filename_a)

        fs = FileSystemStorage()
        print("myfile",myfile)
        for f in _xFiles: 
            if os.path.exists(filepath1 + file_name +f):
                os.remove(filepath1 + file_name +f)

        file_name = mdlId+'_'+str(myfile)
        savefile_name = filepath1 + file_name
        print("savefile_name",savefile_name)
        fs.save(savefile_name, myfile)
        
        if os.path.exists(savefile_name):
            print("if exist")
            df = pd.read_excel(savefile_name)
            # print('printing datatypes ')
            print("DF new",df)
            dttypes = dict(df.dtypes)
            file_id=find_max_prdn_file_id("") 
            print("file_id",file_id)
            data_model=df.to_dict('records')
            print("data_model",data_model)
            for i in data_model:
                    keys_data=list()
                    keys_data.append(list(i.keys()))    ##column name
            Freq_Idx=1
            uploaded_on=datetime.now()  ##uploaded on data
            file_info_data={'Mdl_Id':mdlId,'Freq_Idx':Freq_Idx,'file_id':int(file_id),'file_columns':keys_data,'file_name':file_name,'uploaded_by':"User","uploaded_on":uploaded_on}
                
            if file_id==int(0):  
                file_info_data['file_id']=file_info_data['file_id'] + 1
                collection_prdn_file_info.insert_one(file_info_data)  
                # src_data_dict={}
                for i in data_model:                        
                    src_data_dict=i
                    src_data_dict.update({'file_id':file_info_data['file_id']}) 
                    collection_prdn_src_data.insert_one(i)
            else:
            
                file_info_data['file_id']=file_info_data['file_id'] + 1
                collection_prdn_file_info.insert_one(file_info_data)  
                
                for i in data_model: 
                    src_data_dict=i
                    src_data_dict.update({'file_id':file_info_data['file_id']}) 
                    collection_prdn_src_data.insert_one(i)

            objmaster.insertActivityTrail(mdlId,"17","Model source data imported.",request.session['uid'],request.session['accessToken'])

        arrdescData = []
        gridDttypes = []
        result = ""
        #file_name=myfile
        
        for key, value in dttypes.items():
            gridDttypes.append({'colName': key, 'dataType': value})
        print("gridDttypes",gridDttypes)
        dfdisplay = df.head(100)
        result = dfdisplay.to_json(orient="records")
        result = json.loads(result)
        print("result",result)
        _isDisabled=""
        # return JsonResponse({'isDisabled':_isDisabled,'desc': arrdescData, 'dataTypes': gridDttypes, 'df': result})
        third_party_api_url = getAPIURL()+'getMaxFreqSeqData/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        freidx=1
        is_new=0
        data_to_save = {
            'mdl_id':mdlId, 
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_save),headers=header)             
        data=responseget.json() 
        for ir,val in data['freqData'].items():
            is_new=val['addorupdate']
            freidx=val['freqidx']


        third_party_api_url = getAPIURL()+'DataMonitoringFileInfoAPI/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_save = {
            'Mdl_ID':mdlId,
            'file_nm':filename_a,
            'Added_by':request.session['uid'],
            'freq_idx':freidx,
            'is_new':is_new
        }
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
        # data=json.loads(responseget.content)
        print("response--------------------------",json.loads(responseget.content))
        print("in home2----------------------------end")
        return JsonResponse({'isvalid':'true'})
        
    except Exception as e:
        print(e)
        print('traceback is ', traceback.print_exc())
        return render(request, 'error.html')


# def gethistorymsg(request):
#     try:
#         room_id = request.GET.get('room_id', 'False') 
#         mdl_id = request.GET.get('mdl_id', 'False') 
#         print("mdl_id--------",mdl_id)
#         third_party_api_url = getAPIURL()+'GetHistoryMsg/'
#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }
#         data_to_get = {
#             'room_id':room_id,
#             'mdl_id':mdl_id,
#             'addedby':request.session['uid']
#         }
#         responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
#         data=responseget.json()
#         print("responseget--------------------------2",data['mmdata'])

#         print("responseget history data--------------------------",data['data'])
        
#         # return JsonResponse({'data':data['data'],'mmdata':data['mmdata'],'mo_approved':data['mo_approved']})
#         return JsonResponse({'data':data['data'],'mmdata':data['mmdata'],'mdl_category_data':data['mdl_category_data']})
#         # return JsonResponse(data['data'])
#     except requests.exceptions.RequestException as e:
#         return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 



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


# def gethistorymsg(request):
#     try:
#         room_id = request.GET.get('room_id', 'False') 
#         mdl_id = request.GET.get('mdl_id', 'False') 
#         print("mdl_id--------",mdl_id)
#         third_party_api_url = getAPIURL()+'GetHistoryMsg/'
#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }
#         data_to_get = {
#             'room_id':room_id,
#             'mdl_id':mdl_id,
#             'addedby':request.session['uid']
#         }
#         responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
#         data=responseget.json()
#         print("responseget--------------------------2",data['mmdata'])

#         print("responseget history data--------------------------",data['data'])
        
#         # return JsonResponse({'data':data['data'],'mmdata':data['mmdata'],'mo_approved':data['mo_approved']})
#         return JsonResponse({'data':data['data'],'mmdata':data['mmdata'],'mdl_category_data':data['mdl_category_data']})
#         # return JsonResponse(data['data'])
#     except requests.exceptions.RequestException as e:
#         return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            print("response check model matrics",json.loads(response.content))
        return JsonResponse({'istaken':'true'})
    except Exception as e:
        print('assignValidation ',e)
        print('assignValidation traceback is ', traceback.print_exc()) 
        return JsonResponse({'istaken':'false'})



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
        # data=json.loads(responseget.content)
        print("responseget for check data model matrics--------------------------",json.loads(responseget.content))
    
        return JsonResponse(json.loads(responseget.content))
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())



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


# def gethistorymsgbus(request):
#     try:
#         room_id = request.GET.get('room_id', 'False') 
#         mdl_id = request.GET.get('mdl_id', 'False') 
#         third_party_api_url = getAPIURL()+'GetHistoryMsg/'
#         header = {
#         "Content-Type":"application/json",
#         'Authorization': 'Token '+request.session['accessToken']
#         }

#         data_to_get = {
#             'room_id':room_id,
#             'mdl_id':mdl_id,
#             'addedby':request.session['uid']
#         }
#         responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
#         data=responseget.json()
#         print("responseget business--------------------------",data['bmdata'])
        
#         return JsonResponse({'data':data['data'],'bmdata':data['bmdata'],'mdlcatdatabus':data['mdlcatdatabus']})
#         # return JsonResponse(data['data'])
#     except requests.exceptions.RequestException as e:
#         return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


def savebusinessmatrics(request):
    print("request data business matrics",request.GET)
    try: 
        datalist = json.loads(request.GET['datalist'])
        print("datalist",datalist)
        mdlid = request.GET['mdlId']
        print("mdlid",mdlid)
        frequency = request.GET['frequency']
        if frequency == 'None':
            a = 0
        else:
            a = frequency
        api_url=getAPIURL()+"BusinessMetricAPI/"  
        for i in datalist: 
            print("i",i)
            print("threshold",str(i['Threshold']),"warning",str(i['Warning']))    
            data_to_save={ 
                'mdl_id': mdlid,
                'metric':i['AID'],
                'threshold':int(i['Threshold']),
                'warning':int(i['Warning']),
                'frequency':int(a),
                'metric_value_type':i['Percentage']    ,
                'added_by':request.session['uid']
            } 
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
            print("response business metric",response.content)
            if str(i['Threshold']) == '' and str(i['Warning']) == '':
                pass
        return JsonResponse({"istaken":"true"})
    except Exception as e:
        print('assignValidation ',e)
        print('assignValidation traceback is ', traceback.print_exc()) 
        return JsonResponse({'istaken':'false'})

def find_src_data(mdlid,accessToken): 
    # print('dataset is method is ',dataset)
    # if(dataset==''):
    #     print('inside blank filter')
    #     src_file_obj = collection.find({"file_id":int(file_id)},{'_id':0})
    # else:
    #     print('dataset ', str(dataset)) 
    #     dataset = dataset.replace("\'", "\"") 
    #     dataset=json.loads(dataset)    
    #     print('dataset is ',dataset)      
    #     src_file_obj = collection.find(dataset,{'_id':0})

    # df =  pd.DataFrame(list(src_file_obj))   
    # if len(df)>0: 
    #     df.pop('file_id')
    # print("src fn dataframe",len(df))

    try:
        third_party_api_url = getAPIURL()+'fetch_mdl_document_name/'
        data_to_update = {
            'mdlid':mdlid,
            'doc_type':3,
        }
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+accessToken
        }
        response = requests.get(third_party_api_url, data= json.dumps(data_to_update),headers=header)
        resp_data=json.loads(response.content)
        print("Document details---------------",resp_data)
    except Exception as e:
        print("Error EE",e)
    BASE_DIR = Path(__file__).resolve().parent.parent 
    try:
        destination_path = os.path.join(BASE_DIR, 'static\\document_files\\'+mdlid+'\\')
        savefile_name = destination_path + resp_data['data'][0]['mdl_doc_name']
        # destination_path = str(BASE_DIR)+'/static/document_files/'+ mdlid + '/' +resp_data['data'][0]['mdl_doc_name']+'.xlsx'
        print("file----------",savefile_name) 
        # df = pd.read_excel(savefile_name)
        df = pd.read_excel(savefile_name)
        print("df",df)
    except Exception as e:
        print("file error is---------",e)
        df = pd.DataFrame()
    # print("df----------",df.columns.to_list())
    # cols = df.columns.to_list()
    return df 
     

def find_max_req_id(Mdl_Id=""):
    print("find_max_req_id")
    model_info_obj = collection_model_information.find({'Mdl_Id':Mdl_Id},{'_id':0})
    df =  pd.DataFrame(list(model_info_obj))
    #print("dataframe is ",df)
    print("dataframe max is",df['reqId'].max())    
    req_id=df['reqId'].max()
    return req_id

def datamatricsfeature(request):
    try: 
        print("datamatricsfeature") 
        mdlid =request.GET.get('mdl_id', 'False')
        print("mdlid",mdlid) 
        dataset = ''
        df=find_src_data(mdlid,request.session['accessToken']) 
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
            print("threshold",i['Threshold'],"warning",i['Warning'],'feature',i['feature'])  
            print("only warning",i['Warning'])  
            data_to_save={ 
                'mdl_id': mdlid,
                'Metric':i['AID'],
                'feature':i['feature'],
                'threshold':i['Threshold'],
                'mo_approval':1,
                'warning':i['Warning'],
                # 'warning':0,
                'frequency':frequency,
                'added_by':request.session['uid']
            } 
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
            print("response Data metric",response.content)
        return JsonResponse(json.loads(response.content))
    except Exception as e:
        print('assignValidation ',e)
        print('assignValidation traceback is ', traceback.print_exc()) 
        return JsonResponse({'istaken':'false'})


def UpdateDataMatricsData(request):
    try:
        mdl_id = request.GET.get('mdl_id', 'False') 
        third_party_api_url = getAPIURL()+'DataMatricsTempData/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_update = {
            'mdl_id':mdl_id
        }
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_update),headers=header)
        # data=json.loads(responseget.content)
        print("responseget for check data matrics data--------------------------",json.loads(responseget.content))
    
        return JsonResponse(json.loads(responseget.content))
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())
    

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



