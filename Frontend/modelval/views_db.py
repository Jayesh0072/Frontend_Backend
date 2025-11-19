# import pymongo
from inspect import trace
import traceback
from pandas.core.frame import DataFrame
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import VotingClassifier, AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier, BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from statsmodels.stats.outliers_influence import variance_inflation_factor
from typing import Reversible
from sklearn import preprocessing
from sklearn.feature_selection import SelectPercentile, chi2, RFE
from sklearn.preprocessing import StandardScaler, label_binarize
from sklearn.model_selection import train_test_split, RandomizedSearchCV, GridSearchCV, StratifiedKFold
from sklearn.metrics import classification_report, roc_curve, auc, roc_auc_score, confusion_matrix, recall_score, precision_score, accuracy_score
from bubbly.bubbly import bubbleplot
# import plotly_express as px
import plotly.express as px

import joypy
from django.core.files.storage import FileSystemStorage
import math
from io import StringIO
from statsmodels import robust
import plotly.graph_objs as go
from plotly.offline import plot
import plotly.offline as py
from pandas.plotting import parallel_coordinates
from pandas import plotting
import matplotlib.pyplot as plt
from django.shortcuts import redirect, render
from django.http import JsonResponse
# from flask import Markup
from markupsafe import Markup

import pandas as pd
#import terality as pd
import numpy as np
from .models import descData, lstCnfrmSrc, lstOutlieranomalies, missingDataList, lstColFreq, lstOutlierGrubbs
import os
from pathlib import Path
import json
# for visualizations
import seaborn as sns
import matplotlib
import xgboost as xgb
# from outliers import smirnov_grubbs as grubbs
from fpdf import FPDF, HTMLMixin 
matplotlib.use('Agg')
# for modeling
# client = pymongo.MongoClient('127.0.0.1', 27017)
# dbname = client['modelval']
from .Validation.validation import Validation
from .RegModel.registermodel import MdlDocs
from pymongo import MongoClient
import datetime 
from datetime import date 
import requests
from rest_framework.response import Response
import environ
import base64
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

BASE_DIR = Path(__file__).resolve().parent.parent
# Create your views here.
user_name = "user1"
file_path = os.path.join(BASE_DIR, 'static/csv_files/')
file_path2 = os.path.join(BASE_DIR, 'static/document_files/')
file_name = "csvfile_"+user_name
# app_url = "http://3.131.88.246:8000/modelval/"
BASE_URL = env("BASE_URL")
app_url =BASE_URL 
processingFile_path='static/reportTemplates/processing.csv' 

plot_dir='/static/media/'
plot_dir_view='static/media/'
objvalidation=Validation()

src_files='static/cnfrmsrc_files/'
mail_pwd="sxovbflfjwhgssvx"

from .Adm_Utils.Masters import MasterTbls
objmaster=MasterTbls()
# comments for github test

def getAPIURL():
    api_url=os.environ['API_URL']
    return api_url

def vara(request):
    try:
        print("vara------id",vara,request.session['uid'])
        mdlLst= (objvalidation.getVTModels(request.session['uid']))#
        segLst=[]
        if len(mdlLst)>0:              
            segLst=objvalidation.getVTModelsSegments(mdlLst['0']['Mdl_Id'])
            print('segLst ,',segLst)
        return render(request, 'welcome.html',{'mdlLst':mdlLst,'segLst':segLst})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 


def selVTMdl(request):
    try:
        mdlLst=(objvalidation.getVTModels(request.session['uid']))#
        segLst=[]
        if len(mdlLst)>0:              
            segLst=objvalidation.getVTModelsSegments(mdlLst['0']['Mdl_Id'])
            print('segLst ,',segLst)
        return render(request, 'welcome2.html',{'mdlLst':mdlLst,'segLst':segLst})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 

def getVTModelsSegments(request):
    try:
        mdlId =request.GET.get('mdlId', 'False') 
        segLst=[]
              
        segLst=objvalidation.getVTModelsSegments(mdlId)
        
        return JsonResponse({'segLst':segLst})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
def index(request):
    return render(request, 'index.html')

# def setVTMdl(request):
#     mdlId =request.GET.get('mdlId', 'False') 
#     print("mdlId",mdlId)
#     dataset=request.GET.get('ddlDataset', 'False')
#     datasetName=request.GET.get('ddlDatasetName', 'False')
#     print('datasetName os ',datasetName)
#     dataset=json.loads(dataset)
#     print("dataset 1",dataset)   
#     request.session['vt_mdl']=mdlId
#     print("print 1")
#     request.session['vt_dataset']=dataset
#     print("print 2")
#     request.session['vt_datasetname']=datasetName
#     request.session['Data_Visualisation']="No"
#     request.session['Data_Preparation']="No"
#     request.session['ML_Modeling']="No"
#     request.session['Data_Preparation']="No"
#     request.session['Input_Data_Integrity']="No"
#     request.session['Conceptual_Soundness']="No"
#     request.session['Implementation_Controls']="No"
#     request.session['Model_Usage']="No"
#     request.session['Validation_Findings']="No"
#     request.session['Data_Import_Preprocessing']="No"
#     api_url=getAPIURL()+"getVTMenus/"       
#     data_to_save={ 
#         'mdlId':mdlId, 
#         'uid':request.session['uid'], 
#         } 
#     header = {
#     "Content-Type":"application/json",
#     'Authorization': 'Token '+request.session['accessToken']
#     }
#     response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
#     data=response.json() 
#     menudata=data['assignedTo']
#     jtopy=json.dumps(menudata)
#     json_object = json.loads(jtopy)
#     for key in json_object:        
#         print("The key ", (key['mdl_val_type_label']))
#         if key['mdl_val_type_label']=="Data Visualisation":
#             request.session['Data_Visualisation']="Yes"
#         elif key['mdl_val_type_label']=="Data Preparation":
#             request.session['Data_Preparation']="Yes"
#         elif key['mdl_val_type_label']=="ML Modeling":
#             request.session['ML_Modeling']="Yes"
#         elif key['mdl_val_type_label']=="Data Preparation":
#             request.session['Data_Preparation']="Yes"
#         elif key['mdl_val_type_label']=="Input & Data Integrity":
#             request.session['Input_Data_Integrity']="Yes"
#         elif key['mdl_val_type_label']=="Conceptual Soundness":
#             request.session['Conceptual_Soundness']="Yes"
#         elif key['mdl_val_type_label']=="Implementation & Controls":
#             request.session['Implementation_Controls']="Yes"
#         elif key['mdl_val_type_label']=="Model Usage":
#             request.session['Model_Usage']="Yes"
#         elif key['mdl_val_type_label']=="Validation Findings":
#             request.session['Validation_Findings']="Yes"
#         elif key['mdl_val_type_label']=="Data Import & Preprocessing":
#             request.session['Data_Import_Preprocessing']="Yes" 
          
       
#     return JsonResponse({'is_taken':True})


def setVTMdl(request):
    mdlId =request.GET.get('mdlId', 'False') 
    dataset=request.GET.get('ddlDataset', 'False')
    datasetName=request.GET.get('ddlDatasetName', 'False')
    print('datasetName os ',datasetName)
    dataset=json.loads(dataset)   
    request.session['vt_mdl']=mdlId
    request.session['validation_cycle']=1
    request.session['vt_dataset']=dataset
    request.session['vt_datasetname']=datasetName
    request.session['Data_Visualisation']="Yes"
    request.session['Data_Preparation']="Yes"
    request.session['ML_Modeling']="Yes"
    request.session['Data_Preparation']="Yes"
    request.session['Input_Data_Integrity']="No"
    request.session['Conceptual_Soundness']="No"
    request.session['Implementation_Controls']="No"
    request.session['Model_Usage']="No"
    request.session['Validation_Findings']="No"
    request.session['Data_Import_Preprocessing']="Yes"
    request.session['Model_Performance_Testing']="No"
    request.session['Governance_Oversight']="No"
    # request.session['is_mrm']="Yes"

    if request.session['is_mrm']=='Yes':
        request.session['Data_Visualisation']="Yes"
        request.session['Data_Preparation']="Yes"
        request.session['ML_Modeling']="Yes"
        request.session['Data_Preparation']="Yes"
        request.session['Input_Data_Integrity']="Yes"
        request.session['Conceptual_Soundness']="Yes"
        request.session['Implementation_Controls']="Yes"
        request.session['Model_Usage']="Yes"
        request.session['Validation_Findings']="Yes"
        request.session['Data_Import_Preprocessing']="Yes"
        request.session['Model_Performance_Testing']="Yes"
        request.session['Governance_Oversight']="Yes"
    else:
        api_url=getAPIURL()+"getVTMenus/"       
        data_to_save={ 
            'mdlId':mdlId, 
            'uid':request.session['uid'], 
            } 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
        data=response.json() 
        menudata=data['assignedTo']
        jtopy=json.dumps(menudata)
        json_object = json.loads(jtopy)
        for key in json_object:        
            print("The key ", (key['mdl_val_type_label']))
            if key['mdl_val_type_label']=="Data Visualisation":
                request.session['Data_Visualisation']="Yes"
            elif key['mdl_val_type_label']=="Data Preparation":
                request.session['Data_Preparation']="Yes"
            elif key['mdl_val_type_label']=="ML Modeling":
                request.session['ML_Modeling']="Yes"
            elif key['mdl_val_type_label']=="Data Preparation":
                request.session['Data_Preparation']="Yes"
            elif key['mdl_val_type_label']=="Input & Data Integrity":
                request.session['Input_Data_Integrity']="Yes"
            elif key['mdl_val_type_label']=="Conceptual Soundness":
                request.session['Conceptual_Soundness']="Yes"
            elif key['mdl_val_type_label']=="Implementation & Controls":
                request.session['Implementation_Controls']="Yes"
            elif key['mdl_val_type_label']=="Model Usage":
                request.session['Model_Usage']="Yes"
            elif key['mdl_val_type_label']=="Validation Findings":
                request.session['Validation_Findings']="Yes"
            elif key['mdl_val_type_label']=="Data Import & Preprocessing":
                request.session['Data_Import_Preprocessing']="Yes" 
            elif key['mdl_val_type_label']=="Model Performance & Testing":
                request.session['Model_Performance_Testing']="Yes" 
            elif key['mdl_val_type_label']=="Governance & Oversight":
                request.session['Governance_Oversight']="Yes" 
          
       
    return JsonResponse({'is_taken':True})


# def table(request): #current backup
#     try:
#         _isDisabled="disabled"
#         _xFiles=[".csv","_x_model.csv","_x_keep.csv","_x_dummy.csv","_x_scaled.csv","_x_final.csv"]
#         file_name = "csvfile_"+user_name
#         savefile_name = file_path + file_name + ".csv"  

#         if request.method == 'POST' and request.FILES['myfile']:
#             myfile = request.FILES['myfile']
#             fs = FileSystemStorage()
            
#             for f in _xFiles: 
#                 if os.path.exists(file_path + file_name +f):
#                     os.remove(file_path + file_name +f)

#             fs.save(savefile_name, myfile)

#             if os.path.exists(savefile_name):
#                 df = pd.read_csv(savefile_name, encoding='utf-8')
#                 # print('printing datatypes ')
                
#                 dttypes = dict(df.dtypes)
#                 file_id=find_max_file_id("") 

#                 data_model=df.to_dict('records')
#                 #print("data_model",data_model)
#                 for i in data_model:
#                         keys_data=list()
#                         keys_data.append(list(i.keys()))    ##column name
                
#                 uploaded_on=datetime.datetime.now()  ##uploaded on data
#                 file_info_data={'Mdl_Id':request.session['vt_mdl'],'file_id':int(file_id),'file_columns':keys_data,'file_name':file_name,'uploaded_by':"User","uploaded_on":uploaded_on}
                  
#                 if file_id==int(0):  
#                     file_info_data['file_id']=file_info_data['file_id'] + 1
#                     collection_file_info.insert_one(file_info_data)  
#                     # src_data_dict={}
#                     for i in data_model:                        
#                         src_data_dict=i
#                         src_data_dict.update({'file_id':file_info_data['file_id']}) 
#                         collection.insert_one(i)
#                 else:
               
#                     file_info_data['file_id']=file_info_data['file_id'] + 1
#                     collection_file_info.insert_one(file_info_data)  
                    
#                     for i in data_model: 
#                         src_data_dict=i
#                         src_data_dict.update({'file_id':file_info_data['file_id']}) 
#                         collection.insert_one(i)

#                 objmaster.insertActivityTrail(request.session['vt_mdl'],"17","Model source data imported.",request.session['uid'],request.session['accessToken'])


             

#             arrdescData = []
#             gridDttypes = []
#             result = ""
#             #file_name=myfile
            
#             for key, value in dttypes.items():
#                 gridDttypes.append({'colName': key, 'dataType': value})

#             dfdisplay = df.head(100)
#             result = dfdisplay.to_json(orient="records")
#             result = json.loads(result)
#             _isDisabled=""
#             return render(request, 'showdata.html', {'isDisabled':_isDisabled,'desc': arrdescData, 'dataTypes': gridDttypes, 'df': result})
#         else:
#             gridDttypes = []
#             _isDisabled=""

#             file_id=find_max_file_id(request.session['vt_mdl'])
#             dataset=request.session['vt_dataset'] 
#             df=find_src_data(file_id,dataset)
#             print('df is ',len(df))
#             if(len(df)==0):
#                 importMdlData(request.session['vt_mdl'])
#                 file_id=find_max_file_id(request.session['vt_mdl'])
#                 dataset=request.session['vt_dataset'] 
#                 df=find_src_data(file_id,dataset)
#                 objmaster.insertActivityTrail(request.session['vt_mdl'],"17","Model source data imported.",request.session['uid'],request.session['accessToken'])
#                 print('df ater import is ',len(df))
#             #dfdisplay=dfdisplay[["Show","file_id"]]
#             df = df.head(1000)
#             # Getting column name
#             dttypes = dict(df.dtypes) 
#             for key, value in dttypes.items():
#                 gridDttypes.append({'colName': key, 'dataType': value})

#             # Getting rows data
#             result = df.to_json(orient="records",default_handler=str)
#             result = json.loads(result) 
#             request.session['modelDocs'] = objvalidation.getModelDocs(request.session['vt_mdl'])
#             return render(request, 'showdata.html',{'isDisabled':_isDisabled,'df': result,'dataTypes': gridDttypes})
#     except Exception as e:
#         print(e)
#         print('traceback is ', traceback.print_exc())
#         return render(request, 'error.html')

def table(request):
    print("table test",request.GET,request.POST)
    try:
        print("table")
        # _isDisabled="disabled"
        # _xFiles=[".csv","_x_model.csv","_x_keep.csv","_x_dummy.csv","_x_scaled.csv","_x_final.csv"]
        # file_name = "csvfile_"+user_name
        # savefile_name = file_path + file_name + ".csv" 
        # processing = os.path.join(BASE_DIR, 'static/reportTemplates/processing.csv')
        # df_old_proc = pd.read_csv(processing) 
        # statusReq=df_old_proc.loc[df_old_proc.Idx == 1, "Status"] 
        # del df_old_proc
        # if(statusReq == "Not done").any():
        #     return render(request, 'processNotdone.html')

    
        if request.method == 'POST' and request.FILES['myfile']:
            print("if post ")
            
            if 'myfile' not in request.FILES:
                return JsonResponse({'error': 'No files uploaded.'}, status=400)

            # Retrieve the uploaded files
            files = request.FILES.getlist('myfile')

            print("files",files)
            print("files",len(files))
            # for i in range(len(files)):
            #     print(i)
                
            if not files:
                return JsonResponse({'error': 'No files uploaded.'}, status=400)
            fs = FileSystemStorage()
            columns_data=list()
            dataframes = []
            file_names_ids=dict()
            for file in files:

                # Assuming the files are CSV for this example
                df_combined = pd.read_csv(file)
                dataframes.append(df_combined)
                file_name = file.name
                
                savefile_name = file_path + file_name + ".csv" 
                print("file savefile_name",file,savefile_name)
                fs.save(savefile_name, file)
                df = pd.read_csv(savefile_name, encoding='utf-8')
                print("df",df)
                column_names = df.columns.to_list()
                print("List of all column names:")
                print(column_names)
                columns_data.append(column_names)
                dttypes = dict(df.dtypes)
                # file_id=int(find_max_file_id(""))+1 
                file_id=find_max_file_id("") 
                file_names_ids[int(file_id)]=file_name
                data_model=df.to_dict('records')
                print("data_model",data_model)
                for i in data_model:
                    i['file_id'] = int(file_id)
                    keys_data=list()
                    keys_data.append(list(i.keys()))    ##column name
                print("data_model",data_model)
                
                uploaded_on=datetime.datetime.now()  ##uploaded on data
                file_info_data={'Mdl_Id':request.session['vt_mdl'],'file_id':int(file_id),'file_columns':keys_data,'file_name':file_name,'uploaded_by':request.session['username'],"uploaded_on":uploaded_on,'validation_cycle':request.session['validation_cycle']}
                print("file_info_data-------------------",file_info_data)
                
                print("file_id",file_id)
                if file_id==int(1): 
                    print("initially when collection is empty") 
                    file_info_data['file_id']=file_info_data['file_id'] 
                    collection_file_info.insert_one(file_info_data)  

                    ## insert many Data SRC

                    result = collection.insert_many(data_model)

                    # src_data_dict={}
                    # for i in data_model:                        
                    #     src_data_dict=i
                    #     src_data_dict.update({'file_id':file_info_data['file_id']}) 
                    #     collection.insert_one(i)
                else:
                
                    file_info_data['file_id']=file_info_data['file_id'] 
                    collection_file_info.insert_one(file_info_data)  

                    ## insert many Data SRC

                    result = collection.insert_many(data_model)


                    # for i in data_model: 
                    #     src_data_dict=i
                    #     src_data_dict.update({'file_id':file_info_data['file_id']}) 
                    #     collection.insert_one(i)

                # objmaster.insertActivityTrail(request.session['vt_mdl'],"17","Model source data imported.",request.session['uid'],request.session['accessToken'])


                

                arrdescData = []
                gridDttypes = []
                result = ""
                #file_name=myfile
                
                for key, value in dttypes.items():
                    gridDttypes.append({'colName': key, 'dataType': value})

                dfdisplay = df.head(100)
                result = dfdisplay.to_json(orient="records")
                result = json.loads(result)
                
                print("columns_data",columns_data)

            print("file_names_ids",file_names_ids)
            # Concatenate all DataFrames (assuming they have the same structure)
            combined_file="file1" + "file2"
            final_df = pd.concat(dataframes, ignore_index=True)
            print("final_df",final_df)
            savefile_name = file_path + combined_file + ".csv"
            final_df.to_csv(savefile_name, index=False)

            return JsonResponse({'message': 'Files uploaded successfully.', 'file_names_ids': file_names_ids})

  
            # return render(request, 'showdata.html', {'isDisabled':_isDisabled,'desc': arrdescData, 'dataTypes': gridDttypes, 'df': result})
        else:
            gridDttypes = []
            _isDisabled=""

            file_id=find_max_file_id(request.session['vt_mdl'])
            dataset=request.session['vt_dataset'] 
            df=find_src_data(file_id,dataset)
            print('df is ',len(df))
            if(len(df)==0):
                importMdlData(request.session['vt_mdl'])
                file_id=find_max_file_id(request.session['vt_mdl'])
                dataset=request.session['vt_dataset'] 
                df=find_src_data(file_id,dataset)
                objmaster.insertActivityTrail(request.session['vt_mdl'],"17","Model source data imported.",request.session['uid'],request.session['accessToken'])
                print('df ater import is ',len(df))
            #dfdisplay=dfdisplay[["Show","file_id"]]
            df = df.head(1000)
            # Getting column name
            dttypes = dict(df.dtypes) 
            for key, value in dttypes.items():
                gridDttypes.append({'colName': key, 'dataType': value})

            # Getting rows data
            result = df.to_json(orient="records",default_handler=str)
            result = json.loads(result) 
            request.session['modelDocs'] = objvalidation.getModelDocs(request.session['vt_mdl'])
            return render(request, 'showdata.html',{'isDisabled':_isDisabled,'df': result,'dataTypes': gridDttypes})
    except Exception as e:
        print(e)
        print('traceback is ', traceback.print_exc())
        return render(request, 'error.html')




def is_primery_check(request):
    print("is_primery_check")
    print('is_primery_check',request.GET)  

    file_id=request.GET.get('key')
    file_name=request.GET.get('value')

    print("file_id file_name",file_id,file_name)

    # Define the filter query and update data
    filter_query = {'file_id': int(file_id)}
    update_data = {"$set": {"is_primery": 1}}

    print("filter_query",filter_query)
    print("update_data",update_data)

    # Update one document
    result = collection_file_info.update_one(filter_query, update_data)
    print(f"Matched count: {result.matched_count}")
    print(f"Modified count: {result.modified_count}")

    # Verify the update
    updated_document = collection_file_info.find_one(filter_query)
    print("updated docs",updated_document)
    data={'msg':"Preimery set and Data Imported Successfully"}
    return JsonResponse(data,safe=False)

     
def mergedFile():
    client = MongoClient('localhost',27017,connect=False)
    db = client['validation_tool']
    collection_file=db["SrcFileInfo"]
    collection=db["SrcData"]
    file_1 = collection_file.find_one({'file_name': 'file1.csv'})
    print("file_1-----------------",file_1)
    

    df1 = pd.DataFrame(file_1)
    print("df1--------",df1)

    # data = collection.find({'file_id': 4})
    # print("-------------data",data)
    # df = pd.DataFrame(data)
    # print("-----------df",df)

    file_2 = collection_file.find_one({'file_name': 'file2.csv'})
    print("file_2-----------------",file_2)

    df2 = pd.DataFrame(file_2)
    print("df2--------",df2)
    # for i in documents:
    #     print("documents----------------",i)

    # import pandas as pd

    df1 = pd.DataFrame({
        'key': ['A', 'B', 'C', 'D'],
        'value1': [1, 2, 3, 4]
    })

    df2 = pd.DataFrame({
        'key': ['B', 'D', 'E', 'F'],
        'value2': [5, 6, 7, 8]
    })

    outer_merge = pd.merge(df1, df2, on='key', how='outer')
    print("Outer Merge-----------------", outer_merge.T)

#mergedFile() 
def mergedInfo(request):
    client = MongoClient('localhost',27017,connect=False)
    db = client['validation_tool'] 
    merged_data = db['merged_data']
    merged_data_info = merged_data.find({"mdl_id":request.session['vt_mdl']},{'_id':0})
    print("merged data------------------------",merged_data_info)
    df_merged_data = pd.DataFrame(merged_data_info)
    print("df_merged_data-----------------------",df_merged_data.columns,"datatypes",df_merged_data.dtypes)

    gridDttypes = []
    dttypes = dict(df_merged_data.dtypes) 
    print("datatypes view",dttypes)
    irow=0
    for key, value in dttypes.items():
        if df_merged_data[key].dtypes=="int64" or df_merged_data[key].dtypes=="float64":   
            if len(df_merged_data[key].value_counts())<11:
                gridDttypes.append(
                    {'colName': key,'AID':irow ,'dataType': value, 'notnull': df_merged_data[key].count(),'null':len(df_merged_data)-df_merged_data[key].count()})
                irow+=1
        elif df_merged_data[key].dtypes=="object":
            try:
                print('string to num ',key , ' ',len(df_merged_data[key].fillna('0').astype(int)),  'notnull ', df_merged_data[key].count(),' null ',len(df_merged_data)-df_merged_data[key].count())
                if df_merged_data[key].count()>0:
                    gridDttypes.append(
                        {'colName': key,'AID':irow ,'dataType': value, 'notnull': df_merged_data[key].count(),'null':len(df_merged_data)-df_merged_data[key].count()})
                    irow+=1
                else:
                    gridDttypes.append(
                        {'colName': key,'AID':'' ,'dataType': value, 'notnull': df_merged_data[key].count(),'null':len(df_merged_data)-df_merged_data[key].count()})  
            except:
                gridDttypes.append(
                        {'colName': key,'AID':'' ,'dataType': value, 'notnull': df_merged_data[key].count(),'null':len(df_merged_data)-df_merged_data[key].count()})   
        else:
            gridDttypes.append(
                        {'colName': key,'AID':'' ,'dataType': value, 'notnull': df_merged_data[key].count(),'null':len(df_merged_data)-df_merged_data[key].count()})  
        # for key, value in dttypes.items():
        #     gridDttypes.append(
        #         {'colName': key, 'dataType': value, 'notnull': df[key].count(),'null':len(df)-df[key].count()})
        print("gridDttypes old---------------------",gridDttypes)

    return render(request, 'mergeinfo.html',{'dataTypes':gridDttypes})

def SaveModelData(request):
    client = MongoClient('localhost',27017,connect=False)
    db = client['validation_tool'] 
    model_data = db['model_data']
    merged_data = db['merged_data']
    datalist = request.GET['datalist'] 
    print("datalist------------------",json.loads(datalist))
    col_name = []
    for i in json.loads(datalist):
        print("i------------",i)
        col_name.append(str(i['Column Name']))
        col_name.append("mdl_id")
        col_name.append("validation_cycle")
    # merged_data_df = merged_data.find({"mdl_id":request.session['vt_mdl']})
    merged_data_df = pd.DataFrame(list(merged_data.find({"mdl_id":request.session['vt_mdl']},{'_id':0})))
    print("df",merged_data_df)
    model_data_df = merged_data_df[col_name]
    print("model_data_df-----------",model_data_df)
    data_dict = model_data_df.to_dict('records')
    model_data.insert_many(data_dict)
    return JsonResponse({"msg":"Saved Data Successfully"})

def check2():
    client = MongoClient('localhost',27017,connect=False)
    db = client['validation_tool'] 
    model_data = db['model_data']
    merged_data = db['merged_data']
    # datalist = request.GET['datalist'] 
    # print("datalist------------------",json.loads(datalist))
    merged_data_list = merged_data.find({"mdl_id":"M070101"},{'_id':0})
    print("List---------------------------",list(merged_data_list))
    merged_data_df = pd.DataFrame(list(merged_data.find({"mdl_id":"M070101"},{'_id':0})))
    print("df",merged_data_df)
    
check2()

from django.http import JsonResponse
def mergedfile2(request):
    client = MongoClient('localhost',27017,connect=False)
    db = client['validation_tool'] 
    collection_file=db["SrcFileInfo"]
    collection_file_data=db["SrcData"]
    # validator_collection=
    merged_data = db['merged_data']
    collection_merged_info = db['merged_info']
    # collection_merged_info.insert_one({ "primary_column": "N", "primary_filenm": "abc.csv", "secondary_column": "M","secondary_filenm":"xyz.csv","mdl_id":"M070101","validation_cycle":1 })
    
    df_mergeInfo = collection_merged_info.find()
    df_mergeInfo_data = pd.DataFrame(df_mergeInfo)
    print("df_mergeInfo------------",df_mergeInfo_data)
    # df_mergeInfo = pd.DataFrame([['A','E']],
    #     columns=['primary_col', 'Secondary_col']         
    # ) 

    file = collection_file.find()
    print("file----------",file)
    file_a = list(file)
    print("file_a---------------",file_a)
    for i in file_a:
        print("check file-------------------",i)
        if 'is_primery' in i:
            print("i-----------------",i)
            if i['is_primery'] == 1:
                print("i file_id---------------------",i['file_id'])
                #data1
                d1 = list(collection_file_data.find({"file_id":int(i['file_id'])},{'_id':0}))
                print("d1----------------",list(d1))
                # data = list(d1)
                # print("data new",data)
                df1 = pd.DataFrame(d1)
                print("dataframe1",df1)
                data_model=df1.to_dict('records') 
                # merged_data.insert_many(data_model)
                print("data_model",data_model)
        else:
            print("primary not------------------",i)
            # data_model=df1.to_dict('records') 
            # merged_data.insert_many(data_model)
            # print("data_model",data_model)

            #data2
            d2 = list(collection_file_data.find({"file_id":int(i['file_id'])},{'_id':0}))
            print("d2----------------",list(d2))
            df2 = pd.DataFrame(d2)  
            print("dataframe2",df2)

            df2_cols=df2.columns
            query=''
            for idx,irow in df2.iterrows():
                print("for loop")
                print("idx",idx,"irow",irow)
                df_mergeInfo_data_1 = df_mergeInfo_data.to_dict('records')
                # print("ok--------------------",df_mergeInfo_data_1,"next",irow[df_mergeInfo_data_1[0]["secondary_column"]])
                # primary_col =
                query=''
                col_list = []
                for merged_info in df_mergeInfo_data_1:
                    print("merged_info",merged_info,"row data",irow[merged_info["secondary_column"]])
                    query +='"'+ merged_info['primary_column']+'":"'+ irow[merged_info["secondary_column"]]+'",'                
                    print("query----------",query)
                    col_list.append(irow[merged_info["secondary_column"]])
                    #Define the new values
                print("col_list",col_list)   
                where_clause='{' +query+'"mdl_id":"M070101"    ,"validation_cycle":1} '  
                print("where_clause",where_clause)
                strsetvals=''
                new_values=''

                for col in df2_cols:     
                    print("col----------",col,":",str(irow[col]))     
                    # if col != 'E':
                    print("col_list_2",col_list)
                    if str(irow[col]) not in col_list:
                        strsetvals += '"' +col + '":"' + str(irow[col]) +'",' 
                print('strsetvals ',strsetvals)    

                new_values ='{"$set":{'+strsetvals +'}'  
                new_values +='}'
                import ast 
                print('fol loop under query ',where_clause,'new_values ',ast.literal_eval(new_values),"dict2",ast.literal_eval(new_values)['$set'])

            # Update the document   
                #####
                dict2 = ast.literal_eval(new_values)['$set']
                for key1, value1 in ast.literal_eval(where_clause).items():
                    # Find matching values in the second dictionary and remove the corresponding key
                    keys_to_remove = [key2 for key2, value2 in dict2.items() if value1 == value2]
                    for key in keys_to_remove:
                        del dict2[key]

                print("Updated dict2:", dict2)
                #####     
                result = merged_data.update_one(ast.literal_eval(where_clause) ,ast.literal_eval(new_values))
                print("result-------",result,result.modified_count)
            # # Check if the update was successful
            if result.modified_count > 0:
                print("Document updated successfully! chk")
                return JsonResponse({"msg":"Document Merged Successfully"})
            else:          
                print("No document was updated chk.")  
                return JsonResponse({"msg":"Document Not Merged Properly Please Try Again"})


    # # Select the collection #########################
    # collection = db['merged_data']    
    # df_mergeInfo = pd.DataFrame([['A','E']],
    #     columns=['primary_col', 'Secondary_col']         
    # )    
  
    # # Define the query to find the document
    # data1=[[1, 2, 3, 4,'M0101000','1','1',datetime.datetime.now()],[2, 4, 6, 8,'M0101000','1','1',datetime.datetime.now()]]
    # df1 = pd.DataFrame(data1,
    #      columns= ['A', 'B', 'C', 'D','mdl_id','validation_cycle','added_by','added_on']        
    # )

    # data_model=df1.to_dict('records') 
    # #collection.insert_many(data_model)

    # data2=[[1, 2, 3, 4],[2, 4, 6, 8]]
    # df2 = pd.DataFrame(data2,
    #      columns= ['E', 'F', 'G', 'H']        
    # )
    # # primary_col=
    # df2_cols=df2.columns
    # for idx,irow in df2.iterrows():
    #     print("idx_1",idx,"irow_1",irow)

    #     query = ''#{'df_mergeInfo["primary_col"]': irow['df_mergeInfo["secondary_col"]'],"mdl_id":"M010100","validation_cycle":1}

    # # Define the new values
    #     strsetvals=''
    #     new_values=''
    #     for col in df2_cols:
    #         if col != 'E':
    #             strsetvals += '{"' +col + '":' + str(irow[col]) +'},'
    #     new_values ='{"$set":{"F":4,"G":6,"H":8}' # '{"$set":'+strsetvals +'}'
    #     new_values +='}'
    #     import ast
    #     print('query ',query,'\n','new_values ',ast.literal_eval(new_values))

    # # Update the document
    #     result = collection.update_one({"mdl_id": "M0101000", "validation_cycle": "1"} ,{"$set": {"C":"40","F": "4", "G": "6", "H": "8"}})
    #     print("result-------",result)
    # # Check if the update was successful
    # if result.modified_count > 0:
    #     print("Document updated successfully!")
    # else:
    #     print("No document was updated.")
# mergedfile2()

# def table(request):
    # print("table test")
    # try:
    #     print("table")
    #     _isDisabled="disabled"
    #     _xFiles=[".csv","_x_model.csv","_x_keep.csv","_x_dummy.csv","_x_scaled.csv","_x_final.csv"]
    #     file_name = "csvfile_"+user_name
    #     savefile_name = file_path + file_name + ".csv" 
    #     processing = os.path.join(BASE_DIR, 'static/reportTemplates/processing.csv')
    #     df_old_proc = pd.read_csv(processing) 
    #     statusReq=df_old_proc.loc[df_old_proc.Idx == 1, "Status"] 
    #     del df_old_proc
    #     if(statusReq == "Not done").any():
    #         return render(request, 'processNotdone.html')

    #     if request.method == 'POST' and request.FILES['myfile']:
    #         print("if post ")
    #         myfile = request.FILES['myfile']
    #         fs = FileSystemStorage()
            
    #         for f in _xFiles: 
    #             if os.path.exists(file_path + file_name +f):
    #                 os.remove(file_path + file_name +f)

    #         fs.save(savefile_name, myfile)
            
    #         if os.path.exists(savefile_name):
    #             print("savefile_name",savefile_name)
    #             print("myfile",myfile)
    #             print("myfile",type(myfile))
                
    #             api_url=getAPIURL()+"test_api/" 
    #             header = {
    #                 'Content-Type': 'multipart/form-data',
    #                 'Authorization': 'Token '+request.session['accessToken']
    #                 }
    #             with open(savefile_name, 'rb') as file:
    #                 file_content = file.read()

    #             print("file_content",file_content)
    #             print("file_content",type(file_content))

    #             files = {'file_data': ('file.csv', file_content, 'text/csv')}
    #             print("files",files)
                
    #             response = requests.post(api_url, data=file_content,headers=header)
    #             print("response",response)
                
    #             df = pd.read_csv(savefile_name, encoding='utf-8')
    #             # print('printing datatypes ')
                
    #             dttypes = dict(df.dtypes)
    #             file_id=find_max_file_id("") 

    #             data_model=df.to_dict('records')
    #             #print("data_model",data_model)
    #             for i in data_model:
    #                     keys_data=list()
    #                     keys_data.append(list(i.keys()))    ##column name
                
    #             uploaded_on=datetime.datetime.now()  ##uploaded on data
    #             file_info_data={'Mdl_Id':request.session['vt_mdl'],'file_id':int(file_id),'file_columns':keys_data,'file_name':file_name,'uploaded_by':"User","uploaded_on":uploaded_on}
                  
    #             if file_id==int(0):  
    #                 file_info_data['file_id']=file_info_data['file_id'] + 1
    #                 collection_file_info.insert_one(file_info_data)  
    #                 # src_data_dict={}
    #                 for i in data_model:                        
    #                     src_data_dict=i
    #                     src_data_dict.update({'file_id':file_info_data['file_id']}) 
    #                     collection.insert_one(i)
    #             else:
               
    #                 file_info_data['file_id']=file_info_data['file_id'] + 1
    #                 collection_file_info.insert_one(file_info_data)  
                    
    #                 for i in data_model: 
    #                     src_data_dict=i
    #                     src_data_dict.update({'file_id':file_info_data['file_id']}) 
    #                     collection.insert_one(i)

    #             objmaster.insertActivityTrail(request.session['vt_mdl'],"17","Model source data imported.",request.session['uid'],request.session['accessToken'])


             

    #         arrdescData = []
    #         gridDttypes = []
    #         result = ""
    #         #file_name=myfile
            
    #         for key, value in dttypes.items():
    #             gridDttypes.append({'colName': key, 'dataType': value})

    #         dfdisplay = df.head(100)
    #         result = dfdisplay.to_json(orient="records")
    #         result = json.loads(result)
    #         _isDisabled=""
    #         return render(request, 'showdata.html', {'isDisabled':_isDisabled,'desc': arrdescData, 'dataTypes': gridDttypes, 'df': result})
    #     else:
    #         gridDttypes = []
    #         _isDisabled=""

    #         file_id=find_max_file_id(request.session['vt_mdl'])
    #         dataset=request.session['vt_dataset'] 
    #         df=find_src_data(file_id,dataset)
    #         print('df is ',len(df))
    #         if(len(df)==0):
    #             importMdlData(request.session['vt_mdl'])
    #             file_id=find_max_file_id(request.session['vt_mdl'])
    #             dataset=request.session['vt_dataset'] 
    #             df=find_src_data(file_id,dataset)
    #             objmaster.insertActivityTrail(request.session['vt_mdl'],"17","Model source data imported.",request.session['uid'],request.session['accessToken'])
    #             print('df ater import is ',len(df))
    #         #dfdisplay=dfdisplay[["Show","file_id"]]
    #         df = df.head(1000)
    #         # Getting column name
    #         dttypes = dict(df.dtypes) 
    #         for key, value in dttypes.items():
    #             gridDttypes.append({'colName': key, 'dataType': value})

    #         # Getting rows data
    #         result = df.to_json(orient="records",default_handler=str)
    #         result = json.loads(result) 
    #         request.session['modelDocs'] = objvalidation.getModelDocs(request.session['vt_mdl'])
    #         return render(request, 'showdata.html',{'isDisabled':_isDisabled,'df': result,'dataTypes': gridDttypes})
    # except Exception as e:
    #     print(e)
    #     print('traceback is ', traceback.print_exc())
    #     return render(request, 'error.html')

def importMdlData(mdlId):
    mdldatafilenm=objvalidation.getMdlData(mdlId)
    if mdldatafilenm != None:
        mdldata_file_path = os.path.join(BASE_DIR, 'static/document_files/'+mdlId+'/'+mdldatafilenm)
        if os.path.exists(mdldata_file_path):
            df = pd.read_csv(mdldata_file_path, encoding='utf-8')
            # print('printing datatypes ')
            
            dttypes = dict(df.dtypes)
            file_id=find_max_file_id("") 

            data_model=df.to_dict('records') 
            #print("data_model",data_model)
            for i in data_model:
                    keys_data=list()
                    keys_data.append(list(i.keys()))    ##column name
            
            uploaded_on=datetime.datetime.now()  ##uploaded on data
            file_info_data={'Mdl_Id':mdlId,'file_id':int(file_id),'file_columns':keys_data,'file_name':mdldatafilenm,'uploaded_by':"User","uploaded_on":uploaded_on}
        
            if file_id==int(0):  
                file_info_data['file_id']=file_info_data['file_id'] + 1
                collection_file_info.insert_one(file_info_data)  
                # src_data_dict={}
                for i in data_model:                        
                    src_data_dict=i
                    src_data_dict.update({'file_id':file_info_data['file_id']}) 
                    collection.insert_one(i)
            else:
        
                file_info_data['file_id']=file_info_data['file_id'] + 1
                collection_file_info.insert_one(file_info_data)  
                
                for i in data_model: 
                    src_data_dict=i
                    src_data_dict.update({'file_id':file_info_data['file_id']}) 
                    collection.insert_one(i)

            

def testtree():
    csv_file_name = "csvfile_"+user_name
    savefile_x_final = file_path + csv_file_name + "_x_model.csv"
    df = pd.read_csv(savefile_x_final)
    targetVarFile = file_path + csv_file_name + "_targetVar.txt"
    file1 = open(targetVarFile, "r")  # write mode
    targetVar = file1.read()
    file1.close()
     
    dtree =df
    Y =  dtree[targetVar]
    X = dtree.drop(targetVar, axis=1)
    features = list(X.columns)

    hp = {
    'max_depth': 3,
    'min_samples_split': 50
    }
    root = Node(Y, X, **hp)
    root.grow_tree()
    root.print_tree()

def viewData(request):
    try:
        savefile_name = file_path + file_name + ".csv"
        if(not os.path.exists(savefile_name)):
            return render(request, 'processNotdone.html')
        df = pd.read_csv(savefile_name, na_values='?')
        gridDttypes = []
        dttypes = dict(df.dtypes)
        # print(dttypes)
        for key, value in dttypes.items():
            gridDttypes.append({'colName': key, 'dataType': value})
        result = df.to_json(orient="records")
        result = json.loads(result)
        desc = df.describe()
        arrdescData = []
        for recs, vals in dict(desc).items():
            objdescData = descData()
            objdescData.colName = recs
            objdescData.count_val = vals['count']
            objdescData.mean_val = vals['mean']
            objdescData.std_val = vals['std']
            objdescData.per25_val = vals['25%']
            objdescData.per50_val = vals['50%']
            objdescData.per75_val = vals['75%']
            objdescData.max_val = vals['max']
            objdescData.min_val = vals['min']
            arrdescData.append(objdescData)

        return render(request, 'viewData.html',  {'desc': arrdescData, 'dataTypes': gridDttypes, 'df': result})
    except Exception as e:
        print(e)
        return render(request, 'error.html')



def selCols(request):
    print("selCols")
    try:
        file_id=find_max_file_id(request.session['vt_mdl'])
        src_file_obj = collection_file_info.find({'file_id':int(file_id)})
        for i in src_file_obj:
            print("file_columns",i['file_columns'])

        column_data=i['file_columns']
        print("column_data",column_data) 
      
        target_value=find_target_value(file_id)
        # for i in column_data:
        #     print("i",i)
        # savefile_name = file_path + file_name + ".csv"
        # if(not os.path.exists(savefile_name)):
        #     return render(request, 'processNotdone.html')
        # df = pd.read_csv(savefile_name, na_values='?')
        gridDttypes = []
        # targetVarFile = file_path + file_name + "_targetVar.txt"
        # file1 = open(targetVarFile, "r")  # write mode
        # src_obj=collection.find({"file_id":int(file_id)},{'_id':0})
        # dff =  pd.DataFrame(list(src_obj))
        # print("dff",dff)
        dataset=request.session['vt_dataset']
        dff=find_src_data(file_id,dataset)
        targetVar = target_value
        print("target_value",targetVar)
        #file1.close()
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
        return render(request, 'selCols.html',  {'dataTypes': gridDttypes})
    except Exception as e:
        print(e)
        print('stacktrace iis ', traceback.print_exc())
        return render(request, 'error.html')


def viewDataType(request):
    try:
        # savefile_name = file_path + file_name + ".csv"
        # if(not os.path.exists(savefile_name)):
        #     return render(request, 'processNotdone.html')
        # df = pd.read_csv(savefile_name, na_values='?')
        file_id=find_max_file_id(request.session['vt_mdl'])
        dataset=request.session['vt_dataset']
        df=find_src_data(file_id,dataset) 
        gridDttypes = []
        dttypes = dict(df.dtypes) 
        print("datatypes view",dttypes)
        irow=0
        for key, value in dttypes.items():
            if df[key].dtypes=="int64" or df[key].dtypes=="float64":   
                if len(df[key].value_counts())<11:
                    gridDttypes.append(
                        {'colName': key,'AID':irow ,'dataType': value, 'notnull': df[key].count(),'null':len(df)-df[key].count()})
                    irow+=1
            elif df[key].dtypes=="object":
                try:
                    print('string to num ',key , ' ',len(df[key].fillna('0').astype(int)),  'notnull ', df[key].count(),' null ',len(df)-df[key].count())
                    if df[key].count()>0:
                        gridDttypes.append(
                            {'colName': key,'AID':irow ,'dataType': value, 'notnull': df[key].count(),'null':len(df)-df[key].count()})
                        irow+=1
                    else:
                        gridDttypes.append(
                            {'colName': key,'AID':'' ,'dataType': value, 'notnull': df[key].count(),'null':len(df)-df[key].count()})  
                except:
                    gridDttypes.append(
                            {'colName': key,'AID':'' ,'dataType': value, 'notnull': df[key].count(),'null':len(df)-df[key].count()})   
            else:
                gridDttypes.append(
                            {'colName': key,'AID':'' ,'dataType': value, 'notnull': df[key].count(),'null':len(df)-df[key].count()})  
        # for key, value in dttypes.items():
        #     gridDttypes.append(
        #         {'colName': key, 'dataType': value, 'notnull': df[key].count(),'null':len(df)-df[key].count()})
        print("gridDttypes old",gridDttypes)
        pdf = FPDF()
        pdf.add_page()

        pdf = exportDatatypenCnt(pdf, df, "")
        pdf.output(os.path.join(
            BASE_DIR, plot_dir_view +"/DatatypeCount.pdf"))
        del df
        return render(request, 'ViewDataType.html',  {'page':'ViewDataType','pdfFile': '\static\media\DatatypeCount.pdf', 'dataTypes': gridDttypes})
    except Exception as e:
        print(e)
        print('stacktrace iis ', traceback.print_exc())
        return render(request, 'error.html')


def numtostring(request):
    try:
       
        file_id=find_max_file_id(request.session['vt_mdl'])
        dataset=request.session['vt_dataset']
        df=find_src_data(file_id,dataset) 
        gridDttypes = []
        gridDttypesstr = []
        dttypes = dict(df.dtypes)
        irow=0
        irowstr=0
        for key, value in dttypes.items(): 
            if df[key].dtypes=="int64" or df[key].dtypes=="float64":   
               if len(df[key].value_counts())<11:
                    gridDttypes.append(
                        {'colName': key,'AID':irow ,'dataType': value, 'notnull': df[key].count(),'null':len(df)-df[key].count()})
                    irow+=1
            elif df[key].dtypes=="object":
                try:
                    print('string to num ',key , ' ',len(df[key].fillna('0').astype(int)),  'notnull ', df[key].count(),' null ',len(df)-df[key].count())
                    if df[key].count()>0:
                        gridDttypesstr.append(
                            {'colName': key,'AID':irow ,'dataType': "string", 'notnull': df[key].count(),'null':len(df)-df[key].count()})
                        irowstr+=1
                except:
                    print('could not convert string to num ',key )   
                    print('val cnt ',df[key].value_counts())              
       
        
        del df
        return render(request, 'numtostring.html',  {'page':'ViewDataType',  'dataTypes': gridDttypes,  'dataTypesStr': gridDttypesstr})
    except Exception as e:
        print(e)
        print('stacktrace iis ', traceback.print_exc())
        return render(request, 'error.html')

def updatenumtostring(request):
    try:
        colDataLst = request.GET['colList']  
        colDataLstStr = request.GET['colListStr']  
        json_colDataLst = json.loads(colDataLst)
        json_colDataLstStr = json.loads(colDataLstStr)
        print('json_colDataLstStr 1 ,',json_colDataLstStr)  
        for colval in json_colDataLst: 
            collection.update_many({}, [{'$set': {colval['colName']: {'$toString': '$'+colval['colName']}}}])

        print('json_colDataLstStr 2 ,',json_colDataLstStr)  

        for colval in json_colDataLstStr: 
            print('string col is ',colval['colName'])
            collection.update_many({}, [{'$set': {colval['colName']: {'$toDouble': '$'+colval['colName']}}}])
        
        return JsonResponse({'istaken':'true'})
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})
    
def convertDataType(request):
    try:
        colData = request.GET['colName']  
        colDataType = request.GET['colType'] 
        file_id=find_max_file_id(request.session['vt_mdl'])
         
        if colDataType=="int64" or colDataType=="float64":  
            collection.update_many({'file_id':int(file_id)}, [{'$set': {colData: {'$toString': '$'+colData}}}])

     

        if colDataType == "object":  
            collection.update_many({'file_id':int(file_id)}, [{'$set': {colData: {'$toDouble': '$'+colData}}}])
        
        return JsonResponse({'istaken':'true'})
    except Exception as e:
        print('updateaccess ',e)
        return JsonResponse({'istaken':'false'})

def exportDatatypenCnt(pdf, df, comments=""):
    x, y = 10, 25

    # y += 20.0

    pdf.set_xy(x, y)
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0.0, 0.0, 0.0)
    pdf.multi_cell(0, 10, "Variables by type and count", align='C')

    if(len(comments) > 0):
        y = pdf.get_y() + 10
        pdf.set_xy(x, y)
        pdf.set_font("Arial", size=12)
        pdf.set_text_color(0.0, 0.0, 0.0)
        pdf.multi_cell(0, 10, comments, align='L')

    pdf.set_font("Arial", size=10)
    pdf.set_text_color(255, 255, 255)
    y = pdf.get_y() + 10
    pdf.set_xy(20, y)
    pdf.cell(0, 5, "Column Name", 1, fill=True)
    pdf.set_xy(100, y)
    pdf.cell(0, 5, "Not-Null Count", 1)
    pdf.set_xy(130, y)
    pdf.cell(0, 5, "Column Data type", 1)
    # Start from the first cell. Rows and columns are zero indexed.

    result = dict(df.dtypes)
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0.0, 0.0, 0.0)
    for key, value in result.items():
        # gridDttypes.append(
        #     {'colName': key, 'dataType': value, 'notnull': df[key].count()})
        y += 5
        pdf.set_xy(20, y)
        pdf.cell(0, 5, key, 1)
        pdf.set_xy(100, y)
        pdf.cell(0, 5, str(df[key].count())+" non-null", 1)
        pdf.set_xy(130, y)
        pdf.cell(0, 5, str(value), 1)

    return pdf


def DatatypeComments(request):
    comments = request.GET['comments']
    UserCommentsFiles = file_path + "_DatatypeComments.csv"
    pdf = FPDF()
    if os.path.exists(UserCommentsFiles):
        df_old = pd.read_csv(UserCommentsFiles)
        if (df_old["Type"] == "Datatype").any():
            df_old.loc[df_old.Type ==
                       "Datatype", "comments"] = comments
            df_old.to_csv(UserCommentsFiles, index=False, encoding='utf-8')
        else:
            data = [["Datatype", comments]]
            df_new = pd.DataFrame(data, columns=['Type', 'comments'])
            df = pd.concat([df_old, df_new], axis=0)
            df.to_csv(UserCommentsFiles, index=False, encoding='utf-8')
            del df_new
            del df
        del df_old
    else:
        data = [["Datatype", comments]]
        df = pd.DataFrame(
            data, columns=['Type', 'comments'])
        df.to_csv(UserCommentsFiles, index=False, encoding='utf-8')
        del df

    savefile_name = file_path + file_name + ".csv"
    df = pd.read_csv(savefile_name, na_values='?')
    pdf.add_page()

    pdf = exportDatatypenCnt(pdf, df, comments)
    pdf.output(os.path.join(
        BASE_DIR, plot_dir_view +"/DatatypeCount.pdf"))
    del df
    data = {"is_taken": True}
    return JsonResponse(data)


def viewNumData(request):
    try:
        # savefile_name = file_path + file_name + ".csv"
        # if(not os.path.exists(savefile_name)):
        #     return render(request, 'processNotdone.html')
        # df = pd.read_csv(savefile_name, na_values='?')
        file_id=find_max_file_id(request.session['vt_mdl'])
        dataset=request.session['vt_dataset']
        df=find_src_data(file_id,dataset)
        desc = df.describe()
        arrdescData = []
        for recs, vals in dict(desc).items():
            objdescData = descData()
            objdescData.colName = recs
            objdescData.count_val = vals['count']
            objdescData.mean_val = vals['mean'].round(decimals=4)
            objdescData.std_val = vals['std'].round(decimals=4)
            objdescData.per25_val = vals['25%'].round(decimals=4)
            objdescData.per50_val = vals['50%'].round(decimals=4)
            objdescData.per75_val = vals['75%'].round(decimals=4)
            objdescData.max_val = vals['max'].round(decimals=4)
            objdescData.min_val = vals['min'].round(decimals=4)
            arrdescData.append(objdescData)

        num_cols = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] not in [np.object]]
        x_numeric = pd.DataFrame(df, columns=num_cols)
        mean_ad = x_numeric.mad().round(decimals=4)
        # print(mean_ad)
        mean_adresult = mean_ad.to_json(orient='index')
        mean_adresult = json.loads(mean_adresult)

        median_ad = x_numeric.apply(robust.mad).round(decimals=4)
        # print(mean_ad)
        median_adresult = median_ad.to_json(orient='index')
        median_adresult = json.loads(median_adresult)

        return render(request, 'ViewNumType.html',  {'desc': arrdescData, 'mean_adresult': mean_adresult, 'median_adresult': median_ad})
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def missingData(request):
    try:
        # csvfile = file_path + file_name + "_x.csv"
        # print('os.path.exists(csvfile) ',csvfile ,', ',os.path.exists(csvfile))
        # if(not os.path.exists(csvfile)):
        #     return render(request, 'processNotdone.html')
        # df = pd.read_csv(csvfile, na_values='?')

        # targetVarFile = file_path + file_name + "_targetVar.txt"
        # file1 = open(targetVarFile, "r")  # write mode
        # targetVar = file1.read()
        # file1.close()
        file_id=find_max_file_id(request.session['vt_mdl'])
        dataset=request.session['vt_dataset']
        df=find_src_data(file_id,dataset)
        targetVar=find_target_value(file_id)
        if not (targetVar=="None"):
            df = df.drop(targetVar, axis=1)

        # Change setting to display all columns and rows
        pd.set_option("display.max_columns", None)
        pd.set_option("display.max_rows", None)

        # Display column missingness
        # missing = 1 - df.count()/len(df.index)
        # print(missing)
        data = {'dataCount': df.count(),
                'Rows': len(df.index)}
        df2 = pd.DataFrame(data)

        # df3 = df2.loc[df2['dataCount'] != df2['Rows']]
        # print(df3)
        dfCatMissingValues = [{"value": "HFV", "text": "Highest Frequency Value"}, {"value": "Unknown", "text": "Unknown"}, {
            "value": "Yes", "text": "Yes"}, {"value": "No", "text": "No"}]
        dfNumMissingValues = [{"value": "mean", "text": "Mean"}, {
            "value": "median", "text": "Median"}, {"value": "ffill", "text": "Last Valid Value"}, {"value": "backfill", "text": "Next Valid Value"}]
        arrmissingData = []
        for i in range(0, len(df.columns)):
            if(df[df.columns[i]].count() != len(df.index)):
                # print(df.columns[i], '->', df[df.columns[i]].count())
                objmissingData = missingDataList()
                objmissingData.colName = df.columns[i]
                objmissingData.dtType = df.dtypes[df.columns[i]]
                objmissingData.count_rows = df[df.columns[i]].count()
                objmissingData.total_rows = len(df.index)
                objmissingData.missing_rows = len(
                    df.index) - df[df.columns[i]].count()
                arrmissingData.append(objmissingData)

        return render(request, 'missingData.html', {'desc': df, 'dataTypes': df, 'arrmissingData': arrmissingData, 'ddlCatMissingValues': dfCatMissingValues, 'ddlNumMissingValues': dfNumMissingValues})
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def update_missingval(request):
    # csvfile = file_path + file_name + "_x.csv"
    # df = pd.read_csv(csvfile, na_values='?')
    file_id=find_max_file_id(request.session['vt_mdl'])
    dataset=request.session['vt_dataset']
    df=find_src_data(file_id,dataset)
    content = request.GET['missing_vals']
    json_dictionary = json.loads(content)
    print("json_dictionary",json_dictionary)
    for colval in json_dictionary:
        for attribute, value in colval.items():
            print('attribute ', attribute, ' value ', value)
            colName = attribute

            if(value == "HFV"):
                idx = df[colName].value_counts(ascending=False)
                idx = dict(idx)
                # Getting first key in dictionary
                calValue = list(idx.keys())[0]
                # print('colName ', colName, ' maxval ', res)
            elif(value == "mean"):
                calValue = df[colName].mean()
            elif(value == "median"):
                calValue = df[colName].median()
            elif(value == "ffill"):
                calValue = "method='ffill'"
            elif(value == "backfill"):
                calValue = "method='backfill'"
            else:
                calValue = value
            print('colName ', colName, ' calValue ', value)
            df[colName].fillna(calValue, inplace=True)
            print("df updated",df.to_dict("records"))
            Updating_obj=df.to_dict("records")
            myquery = {'file_id':int(file_id) }
            mydoc = collection.find(myquery)
            if collection.find_one(myquery):
                for i in mydoc:
                    print("I",i[colName])
                    if i[colName] == None:
                        print("i[colName]",i[colName])
                        existing = {colName:i[colName]}
                        newvalues = { "$set":{colName:value} }
                        print("existing",existing)
                        print("newvalues",newvalues)
                        collection.update_one(existing,newvalues)
                        # db.collection.update(
                        #     {
                        #         "$or": [
                        #             { "name": { "$exists": False } }, 
                        #             { "name": null }
                        #         ]
                        #     }, 
                        #     { "$set": { "name": "test" } }
                        # )
            else:
                pass        
        #   print('colName ', colName, ' calValue ', calValue)

    # savefile_withoutnull = file_path + file_name + "_x.csv"
    # df.to_csv(savefile_withoutnull, index=False, encoding='utf-8')
    # processing = os.path.join(BASE_DIR, processingFile_path)
    # df_old_proc = pd.read_csv(processing)
    # df_old_proc.loc[df_old_proc.Idx == 5, "Status"] = "Done"
    # df_old_proc.to_csv(processing, index=False, encoding='utf-8')
    # del df_old_proc
    data = {
        'is_taken': True
    }
    return JsonResponse(data)

# def find_max_file_id(mdlid=""):
    
#     print("find_max_file_id",mdlid)
#     if mdlid=="":
#         src_file_obj = collection_file_info.find()
#     else:
#         src_file_obj = collection_file_info.find({'Mdl_Id':mdlid})
#     df =  pd.DataFrame(list(src_file_obj)) 
#     if len(df)>0: 
#         file_id=df['file_id'].max()
#     else:
#         file_id=1 #changed by nilesh on 11.4.23
#     print('file_id' ,file_id)
#     return file_id

def find_max_file_id(mdlid=""):
    
    print("find_max_file_id",mdlid)
    if mdlid=="":
        print("if")
        src_file_obj = collection_file_info.find()
    else:
        print("else")
        src_file_obj = collection_file_info.find({'Mdl_Id':mdlid})
    df =  pd.DataFrame(list(src_file_obj)) 
    print("df",df)
    print("length",len(df))
    if len(df)>0: 
        file_id=df['file_id'].max() + 1   ## +1 changed by ashok 26 07 24
    else:
        file_id=1 #changed by nilesh on 11.4.23
    print('file_id' ,file_id)
    return file_id

def find_target_value(file_id=0):
    print("find_target_value")    
    target_value_obj=collection_model_target_value.find({'file_id':int(file_id)},{'_id':0})
    
    for j in target_value_obj:
        print('j',j)
        print("target value data",j['column_name'])

    target_value=j['column_name']  
    return target_value

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

def dataCleaning(request):
    print("dataCleaning")

    try:
        file_id=find_max_file_id(request.session['vt_mdl'])
         
        src_file_obj = collection_file_info.find_one({'file_id':int(file_id)})
        
        column_data= src_file_obj['file_columns'][0]  
        gridDttypes=[]
        idx=0  
        for j in column_data:
            print("j is ",j,idx)
            gridDttypes.append({'colName': j,  'idx':str(idx)})
            idx=idx+1 
        _isDisabled="" 
         
        return render(request, 'dataCleaning.html', {'isDisabled':_isDisabled,'dataTypes': gridDttypes,'file_id':file_id})
    except Exception as e:
        print(e)
        return render(request, 'error.html')

def deleteColumns(request): 
    column_name_get = request.GET['delcolList']
    updated_column = request.GET['colDataLst']
    file_id=find_max_file_id(request.session['vt_mdl'])
    dataset=request.session['vt_dataset']
    df=find_src_data(file_id,dataset)  
        
    column_name = json.loads(column_name_get)
    parsed_obj = json.loads(updated_column)
    dict_obj={} 
    for i in parsed_obj:
        for key,val in i.items():
            #print("key value",key,val)
            dict_obj.update({key:val})
   
    for j in column_name:
        for k,v in j.items():
            column_name=v 
              
    class Data_SRC:
        def storing_src(self):         
            src_obj=collection.find({'file_id':int(file_id)})       
            for k,v in dict_obj.items():
                print("key value",column_name,k,v,df[column_name].dtypes)

                if k and v:
                    if df[column_name].dtypes=="int64":
                        myquery = { column_name: int(k),'file_id':int(file_id) }
                    elif df[column_name].dtypes=="float64":       
                         myquery = { column_name: float(k),'file_id':int(file_id) }
                    elif df[column_name].dtypes=="bool" or  (type(src_obj[column_name]).__name__=="bool"):                      
                        if(str(k)=="False"):
                            k=False
                        elif(str(k)=="True"):
                            k=True
                        myquery = { column_name: k,'file_id':int(file_id) }
                    else:
                        myquery = { column_name: k,'file_id':int(file_id) }
                    newvalues = { "$set": { column_name: v } }
                    print("myquery",myquery)
                    print("newvalues",newvalues)

                    collection.update_many(myquery, newvalues)
                    print("Update")
            return True
    
    class Data_Target:
        def storing_target(self):    
           
            target_obj={'column_name':column_name,'file_id':int(file_id)}
            myquery = { 'file_id':int(file_id) }
            mydoc = collection_model_target_value.find(myquery)
            if collection_model_target_value.find_one(myquery):
                for i in mydoc: 
                    newvalues = { "$set":target_obj }
                    collection_model_target_value.update_one(myquery, newvalues)
            else: 
                collection_model_target_value.insert_one(target_obj)
                return True
            objmaster.insertActivityTrail(request.session['vt_mdl'],"18","Target variable set.",request.session['uid'],request.session['accessToken'])
    src_obj=Data_SRC()
    src_obj.storing_src()    
    target_obj=Data_Target()
    target_obj.storing_target() 
    data = {
        'is_taken': True
    }
    return JsonResponse(data)

def showCatColFreq(request):
    try:
        # savefile_withoutnull = file_path + file_name + ".csv"
        # if(not os.path.exists(savefile_withoutnull)):
        #     return render(request, 'processNotdone.html')
        # df = pd.read_csv(savefile_withoutnull, na_values='?')
        # x = pd.read_csv(savefile_x, na_values='?')
        file_id=find_max_file_id(request.session['vt_mdl'])
        dataset=request.session['vt_dataset']
        df=find_src_data(file_id,dataset) 
        gridDttypes = []
        cat_cols = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] in [np.object]]
        noData=""
        if(len(cat_cols)<1):
            noData="Categorical variables not available to run this utility."
        x_categori = pd.DataFrame(df, columns=cat_cols)
        for col in x_categori.columns:
            objlstColFreq = lstColFreq()
            col_count = x_categori[col].value_counts()
            # print(dict(col_count))

            objlstColFreq.colName = col
            objlstColFreq.freqVal = dict(col_count)
            objlstColFreq.total_rows = x_categori[col].count()
            objlstColFreq.missing_rows = len(
                x_categori[col])-x_categori[col].count()
            gridDttypes.append(objlstColFreq)

        return render(request, 'showFreqData.html', {'dataTypes': gridDttypes,'noData':noData})
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def dropfeatures(request):
    try:
        # savefile_x = file_path + file_name + "_x.csv"
        _isDisabled="disabled"
        # savefile_withoutnull = file_path + file_name + "_x.csv"
        # savefile_x_keep = file_path + file_name + "_x_keep.csv"
        # if(not os.path.exists(savefile_withoutnull)):
        #     return render(request, 'processNotdone.html')

        # if(os.path.exists(savefile_x_keep)):
        #     _isDisabled=""
        # df = pd.read_csv(savefile_withoutnull, na_values='?')

        # targetVarFile = file_path + file_name + "_targetVar.txt"
        # file1 = open(targetVarFile, "r")  # write mode
        # targetVar = file1.read()
        # file1.close()
        file_id=find_max_file_id(request.session['vt_mdl'])
        dataset=request.session['vt_dataset']
        df=find_src_data(file_id,dataset) 
        targetVar=find_target_value(file_id)
        if(not (targetVar=="None")):
            df = df.drop(targetVar, axis=1)
        # x = pd.read_csv(savefile_x, na_values='?')
        gridDttypes = []
        cols = df.columns
        x_categori = pd.DataFrame(df, columns=cols)
        for col in x_categori.columns:
            objlstColFreq = lstColFreq()
            col_count = x_categori[col].value_counts()
            # print(dict(col_count))

            objlstColFreq.colName = col
            objlstColFreq.freqVal = dict(col_count)
            objlstColFreq.total_rows = x_categori[col].count()
            objlstColFreq.missing_rows = len(
                x_categori[col])-x_categori[col].count()
            gridDttypes.append(objlstColFreq)

        return render(request, 'dropfeatures.html', {'dataTypes': gridDttypes,'isDisabled':_isDisabled})
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def deleteColumnsFreqwise(request):
    savefile_x = file_path + file_name + "_x.csv"
    df = pd.read_csv(savefile_x, na_values='?')

    targetVarFile = file_path + file_name + "_targetVar.txt"
    file1 = open(targetVarFile, "r")  # write mode
    targetVar = file1.read()
    file1.close()
    if not (targetVar=='None'):
        y = df[targetVar]
        df = df.drop(targetVar, axis=1)

    content = request.GET['delcolList']
    json_dictionary = json.loads(content)
    delcolLst = []
    for colval in json_dictionary:
        for attribute, value in colval.items():
            if(attribute == 'column'):
                delcolLst.append(value)

    # print(delcolLst)
    # drop target and cust_id from the datset
    x1 = df.drop(delcolLst, axis=1)
    x = pd.concat([x1, y], axis=1)
    savefile_x_keep = file_path + file_name + "_x_keep.csv"
    x.to_csv(savefile_x_keep, index=False)
    processing = os.path.join(BASE_DIR, processingFile_path)
    df_old_proc = pd.read_csv(processing)
    df_old_proc.loc[df_old_proc.Idx == 6, "Status"] = "Done"
    df_old_proc.to_csv(processing, index=False)
    del df_old_proc
    data = {
        'is_taken': True
    }
    return JsonResponse(data)


def showChartTypes(request):
    try:
        content = request.POST.get('rdoChart', False)
        print('content ', content)
        if(content == "barchart"):
            return redirect('plotinsoccuvsincstate')
        elif(content == "stackedbarchart"):
            return redirect('plotinsoccuvsincstatestacked')
        elif(content == "distChart"):
            print('inside distchart')
            return redirect('vardistbyfraud')
        elif(content == "stripplot"):
            return redirect('stripplot')
        elif(content == "boxChart"):
            return redirect('totalclaim_boxplot')
        elif(content == "box3dChart"):
            return redirect('vehicleclaim')
        elif(content == "scatteredChart"):
            return redirect('scattred3d')
        elif(content == "bubbleChart"):
            return redirect('bubblePlot3d')
        return render(request, 'showChartTypes.html')
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def showUniVarChartTypes(request):
    try:
        content = request.POST.get('rdoChart', False)
        print('content is :', content)
        if(content == "pieChart"):
            return redirect('showPieChart')
        elif(content == "DistPlot"):
            return redirect('showDistPlot')
        elif(content == "BoxPlot"):
            return redirect('showBoxPlot')
        elif(content == "CatCountPlot"):
            return redirect('showCatCountPlot')

        return render(request, 'showUniVarChartTypes.html')
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def showSNSChart(request):
    try: 
        content = request.POST.get('selCols', False) 
        selYCols = request.POST.get('selYCols', False) 
        # print('content is')
        # print(content)
        json_dictionary = json.loads(content)
        yaxis_dictionary = json.loads(selYCols)
        delcolLst = []
        colYaxisLst = []
        for colval in json_dictionary:
            for attribute, value in colval.items():
                if(attribute == 'column'):
                    delcolLst.append(value)
        
        for colval in yaxis_dictionary:
            for attribute, value in colval.items():
                if(attribute == 'column'):
                    colYaxisLst.append(value)

        print('json_dictionary is ',delcolLst)
        print('colYaxisLst is ',colYaxisLst)
        # savefile_x_keep = file_path + file_name + "_x.csv"
        # if(not os.path.exists(savefile_x_keep)):
        #     return render(request, 'processNotdone.html')
        # targetVarFile = file_path + file_name + "_targetVar.txt"
        # file1 = open(targetVarFile, "r")  # write mode
        # targetVar = file1.read()
        # file1.close()
        
        # print("dataframe is ",df)
        # print("dataframe max is",df['file_id'].max()) 
        file_id=find_max_file_id(request.session['vt_mdl']) 
        dataset=request.session['vt_dataset']
        x_keep=find_src_data(int(file_id),dataset)

          
        # x_keep = x_keep[delcolLst] 
        # sns_plot = sns.pairplot(x_keep)
        print('x_keep is ',x_keep.head(10))
        print('x_keep cols ',x_keep.columns)
        print('len(colYaxisLst),len(delcolLst) ',len(colYaxisLst),len(delcolLst)*2)
        plt.figure(figsize=(60,60))
        k=1
        for var in colYaxisLst:            
            for i in delcolLst:   
                plt.subplot(len(colYaxisLst),len(delcolLst),k)
                plt.scatter(x_keep[i], x_keep[var])
                plt.xlabel(i)
                plt.ylabel(var) 
                k=k+1
        plt.tight_layout()
        #plt.show()
        # sns_plot.savefig(os.path.join( BASE_DIR, plot_dir_view+user_name+'output.png'))
        plt.savefig(os.path.join(
            BASE_DIR, plot_dir_view+user_name+'output.png'))
        objmaster.insertActivityTrail(request.session['vt_mdl'],"21","Data visualization pair plot viewed.",request.session['uid'],request.session['accessToken'])
        return render(request, 'showSNSChart.html', {'graphpath': plot_dir+user_name+'output.png'}) 
    except Exception as e:
        print(e)
        print('stacktrace is ',traceback.print_exc())
        return render(request, 'error.html')


def showPieChart(request):
    try:
        file_id=find_max_file_id(request.session['vt_mdl'])
        dataset=request.session['vt_dataset'] 
        df=find_src_data(file_id,dataset)
        targetVar =  find_target_value(file_id)
        if(targetVar=='None'):
            return render(request, 'processNotdone.html')
         
        fraud = df[targetVar].value_counts()
        print('fraud ',fraud.index)
        label_fraud = fraud.index
        size_fraud = fraud.values
        colors = ['green', 'yellow']
        trace = go.Pie(labels=label_fraud, values=size_fraud,
                       marker=dict(colors=colors), name=targetVar)
        layout = go.Layout(title='Distribution of '+targetVar)
        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, include_plotlyjs=False, output_type='div')
        fig.write_image(os.path.join(
            BASE_DIR, plot_dir_view+user_name+'outputPieChart.png'))
        objmaster.insertActivityTrail(request.session['vt_mdl'],"21","Data visualization pie chart viewed.",request.session['uid'],request.session['accessToken'])
        context = {'graphpath': plot_dir+user_name+'outputPieChart.png',
                   'plot_div': Markup(plot_div), 'hideddls': 'none', 'hideUnvar': 'block', 'pageHeader': 'Pie Chart'}
        return render(request, 'show3dplot.html', context)
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def showDistPlot(request):
    file_id=find_max_file_id(request.session['vt_mdl'])
    dataset=request.session['vt_dataset'] 
    x_keep=find_src_data(file_id,dataset)
    targetVar =  find_target_value(file_id) 
    if not (targetVar=='None'):
        x_keep = x_keep.drop(targetVar, axis=1)
    # Retrieve all numerical variables from data
    # num_cols = [c for i, c in enumerate(
    #     x_keep.columns) if x_keep.dtypes[i] not in [np.object]]
    num_cols=x_keep.select_dtypes(include=np.number).columns.tolist()
    fig = plt.figure(figsize=(50, 50))
    k = 1
    for i in num_cols:
        plt.subplot(math.ceil(len(num_cols)/4), 4, k)
        sns.distplot(x_keep[i])
        k = k+1
    # plt.title('x_keep[i]', fontsize=10)
    plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.4)
    fig.savefig(os.path.join(BASE_DIR, plot_dir_view +
                user_name+'outputDistPlot.png'))
    
    objmaster.insertActivityTrail(request.session['vt_mdl'],"21","Data visualization dist plot for numeric features viewed.",request.session['uid'],request.session['accessToken'])

    context = {'graphpath': plot_dir+user_name+'outputDistPlot.png',
               'pageHeader': 'Distribution for all the numeric features Dist Plot'}
    return render(request, 'showDistPlot.html', context)


def showBoxPlot(request):
    try:
        file_id=find_max_file_id(request.session['vt_mdl'])
        dataset=request.session['vt_dataset'] 
        x_keep=find_src_data(file_id,dataset)
        targetVar =  find_target_value(file_id) 
        if not (targetVar=='None'):
            x_keep = x_keep.drop(targetVar, axis=1)
        # Retrieve all numerical variables from data
        # num_cols = [c for i, c in enumerate(
        #     x_keep.columns) if x_keep.dtypes[i] not in [np.object]]

        num_cols=x_keep.select_dtypes(include=np.number).columns.tolist()
        fig = plt.figure(figsize=(50, 50))
        k = 1
        for i in num_cols:
            plt.subplot(math.ceil(len(num_cols)/4), 4, k)
            sns.boxplot(x_keep[i])
            k = k+1
        plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.4)
        # plt.title('x_keep[i]', fontsize=10)
        fig.savefig(os.path.join(BASE_DIR, plot_dir_view +
                    user_name+'outputBoxPlot.png'))

        context = {'graphpath': plot_dir +
                   user_name+'outputBoxPlot.png', 'pageHeader': 'Distribution for all the numeric features Box Chart'}
        objmaster.insertActivityTrail(request.session['vt_mdl'],"21","Data visualization box chart for numeric features viewed.",request.session['uid'],request.session['accessToken'])
        return render(request, 'showBoxPlot.html', context)
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def showCatCountPlot(request):
    try:
        file_id=find_max_file_id(request.session['vt_mdl'])
        dataset=request.session['vt_dataset'] 
        x_keep=find_src_data(file_id,dataset)
        targetVar =  find_target_value(file_id) 
        if not (targetVar=='None'):
            x_keep = x_keep.drop(targetVar, axis=1)
        # Retrieve all text variables from data
        cat_cols = [c for i, c in enumerate(
            x_keep.columns) if x_keep.dtypes[i] in [np.object]]
        if(len(cat_cols)<1):
            return render(request, 'noCatVars.html')
        plt.style.use('fivethirtyeight')
        fig = plt.figure(figsize=(50, 50))
        k = 1
        for i in cat_cols:
            plt.subplot(math.ceil(len(cat_cols)/4), 4, k)
            sns.countplot(x_keep[i], palette='spring')
            k = k+1
        # plt.title('x_keep[i]', fontsize=10)
        plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.4)
        fig.savefig(os.path.join(
            BASE_DIR, plot_dir_view+user_name+'outputCatCntPlot.png'))

        context = {'graphpath': plot_dir +
                   user_name+'outputCatCntPlot.png', 'pageHeader': 'Text types histogram'}
        
        objmaster.insertActivityTrail(request.session['vt_mdl'],"21","Data visualization text types histogram viewed.",request.session['uid'],request.session['accessToken'])
        return render(request, 'showCatCntPlot.html', context)
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def plotinsured_occupations(request):
    try:
        var_cat = request.POST.get('ddlvar2', False)
        savefile_x_keep = file_path + file_name + "_x.csv"
        savefile_withoutnull = file_path + file_name + ".csv"
        if(not os.path.exists(savefile_withoutnull)):
            return render(request, 'processNotdone.html')
        df = pd.read_csv(savefile_withoutnull, na_values='?')
        x_keep = pd.read_csv(savefile_x_keep)
        cat_cols = [c for i, c in enumerate(
            x_keep.columns) if x_keep.dtypes[i] in [np.object]]
        if(len(cat_cols)<1):
            return render(request, 'noCatVars.html')
        if(var_cat == False):
            var = cat_cols[0]
        else:
            var = var_cat

        targetVarFile = file_path + file_name + "_targetVar.txt"
        file1 = open(targetVarFile, "r")  # write mode
        targetVar = file1.read()
        file1.close()
        occu = pd.crosstab(x_keep[var], df[targetVar])

        occu.div(occu.sum(1).astype(float), axis=0).plot(
            kind='bar', stacked=True, figsize=(15, 8))
        plt.title('Fraud', fontsize=20)
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(
            BASE_DIR, plot_dir_view+user_name+'plotinsured_occupations.png'))
        plt.close()
        context = {'graphpath': plot_dir+user_name+'plotinsured_occupations.png',
                   'ddlvar1': cat_cols, 'ddlvar2': cat_cols, 'var1': var_cat, 'var2': var, 'hideddl1': 'none', 'postAct': totalclaim_boxplot}
        return render(request, 'showPlot.html', context)
    except Exception as e:
        print(e)
        return render(request, 'error.html')


# def plotinsoccuvsincstate(request):
#     try:
#         var1 = request.POST.get('ddlvar1', False)
#         var2 = request.POST.get('ddlvar2', False)
        
#         file_id=find_max_file_id(request.session['vt_mdl'])
#         dataset=request.session['vt_dataset'] 
#         df=find_src_data(file_id,dataset)
#         # x_keep = pd.read_csv(savefile_x_keep)
#         cat_cols_temp = [c for i, c in enumerate(
#             df.columns) if df.dtypes[i] in [np.object]] 
#         cat_cols=[]
#         for x in cat_cols_temp:
#             if len(df[x].value_counts())<25:
#                 cat_cols.append(x)
#         if(len(cat_cols)<1):
#             return render(request, 'noCatVars.html')
#         print('cat_cols ',cat_cols)
#         if(var1 == False):
#             var1 = cat_cols[0]
#             var2 = cat_cols[1]

#         print('varr1 ', var1,var2)
#         cat_bar = pd.crosstab(df[var1].astype(str), df[var2].astype("string"))
#         color = plt.cm.inferno(np.linspace(0, 1, 5))
#         cat_bar.div(cat_bar.sum(1).astype(float), axis=0).plot(kind='bar', figsize=(10, 6),
#                                                                stacked=False,
#                                                                color=color)
#         plt.title(var2, fontsize=14)
#         plt.legend()
#         plt.tight_layout()
#         plt.savefig(os.path.join(
#             BASE_DIR, plot_dir_view+user_name+'plotinsoccuvsincstate.png'))
#         plt.close()
#         del df 

#         saveChartViewd('Bar chart', var1, var2, user_name +
#                        'plotinsoccuvsincstate.png',request.session['vt_mdl'],request.session['uid'],request.session['vt_datasetname'])
#         if os.path.exists(os.path.join(
#                 BASE_DIR, plot_dir_view+user_name+'plotinsoccuvsincstate.png')):
#             pdf = FPDF()
#             pdf.add_page()
#             pdf = exportgraphImgPdf(pdf, os.path.join(
#                 BASE_DIR, plot_dir_view+user_name+'plotinsoccuvsincstate.png'), " Bar chart "+var1+" vs "+var2)
#             pdf.output(os.path.join(
#                 BASE_DIR, plot_dir_view+user_name+'Bar chart.pdf'))

#         context = {'chartType': 'Bar chart', 'pdfFile': plot_dir+user_name+'Bar chart.pdf', 'graphpath': plot_dir+user_name+'plotinsoccuvsincstate.png',
#                    'ddlvar1': cat_cols, 'ddlvar2': cat_cols, 'var1': var1, 'var2': var2, 'postAct': plotinsoccuvsincstate}
#         objmaster.insertActivityTrail(request.session['vt_mdl'],"21","Data visualization bar chart viewed for "+ var1 + " vs  "+var2+".",request.session['uid'],request.session['accessToken'])
#         return render(request, 'showPlot.html', context)
#     except Exception as e:
#         print(e, ' stacktrace ',traceback.print_exc())
#         return render(request, 'error.html')
def plotinsoccuvsincstate(request):
    try:
        var1 = request.POST.get('ddlvar1', False)
        var2 = request.POST.get('ddlvar2', False)
        
        print("var1 var2",var1,var2)

        dataset=request.session['vt_dataset'] 
        user_id=int(request.session['uid'])
        data_segment=request.session['vt_datasetname']

        api_url=getAPIURL()+"plotinsoccuvsincstate/" 

        # third_party_api_url = api_url+'plotinsoccuvsincstate/'

        data_df={
            'mdl_id':request.session['vt_mdl'],
            'dataset':dataset,
            'var1':var1,
            'var2':var2,
            'username':request.session['username'],
            'user_id':user_id,
            'data_segment':data_segment
        }

        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url,data=json.dumps(data_df),headers=header)
        # print("response bar chart",response.content,response.status_code)
        context=json.loads(response.content)
        print("context",context)
        print("context['cat_cols_check']",context['cat_cols_check'])
        if context['cat_cols_check']==1:
            return render(request, 'noCatVars.html')
        else:
            print("report",context['report'])
            print("report",type(context['report']))
        
            image_path = os.path.join(BASE_DIR, 'static/media', request.session['username'] + 'plotinsoccuvsincstate.png')
            with open(image_path, "wb") as f:
                f.write(base64.b64decode(context['report']))
            print("Image downloaded successfully.")

        

        context = {'chartType': context['chartType'], 'pdfFile': plot_dir+user_name+'Bar chart.pdf', 'graphpath': plot_dir+request.session['username']+'plotinsoccuvsincstate.png',
                   'ddlvar1': context['ddlvar1'], 'ddlvar2': context['ddlvar2'], 'var1': context['var1'], 'var2': context['var2'], 'postAct': plotinsoccuvsincstate}
        return render(request, 'showPlot.html', context)
    except Exception as e:
        print(e,traceback.print_exc())
        return render(request, 'error.html')



# def plotinsoccuvsincstatestacked(request):
    try:
        var1 = request.POST.get('ddlvar1', False)
        var2 = request.POST.get('ddlvar2', False)
        savefile_withoutnull = file_path + file_name + ".csv"
        if(not os.path.exists(savefile_withoutnull)):
            return render(request, 'processNotdone.html')
        df = pd.read_csv(savefile_withoutnull, na_values='?')
        cat_cols_temp = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] in [np.object]]
        cat_cols=[]
        for x in cat_cols_temp:
            if len(df[x].value_counts())<25:
                cat_cols.append(x)
        if(len(cat_cols)<1):
            return render(request, 'noCatVars.html')
        if(len(cat_cols)<1):
            return render(request, 'noCatVars.html')
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
            BASE_DIR, plot_dir_view+user_name+'plotinsoccuvsincstatestacked.png'))
        plt.close()
        del df
        saveChartViewd('Stacked Bar chart', var1, var2,
                       user_name+'plotinsoccuvsincstatestacked.png',request.session['vt_mdl'],request.session['uid'],request.session['vt_datasetname'])

        if os.path.exists(os.path.join(
                BASE_DIR, plot_dir_view+user_name+'plotinsoccuvsincstatestacked.png')):
            pdf = FPDF()
            pdf.add_page()
            pdf = exportgraphImgPdf(pdf, os.path.join(
                BASE_DIR, plot_dir_view+user_name+'plotinsoccuvsincstatestacked.png'), " Stacked Bar chart "+var1+" vs "+var2)
            pdf.output(os.path.join(
                BASE_DIR, plot_dir_view+user_name+'Stacked Bar chart.pdf'))

        context = {'chartType': 'Stacked Bar chart', 'pdfFile': plot_dir+user_name+'Stacked Bar chart.pdf', 'graphpath': plot_dir+user_name+'plotinsoccuvsincstatestacked.png', 'ddlvar1': cat_cols,
                   'ddlvar2': cat_cols, 'var1': var1, 'var2': var2, 'postAct': plotinsoccuvsincstatestacked}
        objmaster.insertActivityTrail(request.session['vt_mdl'],"21","Data visualization stacked bar chart viewed for "+ var1 + " vs  "+var2+".",request.session['uid'],request.session['accessToken'])
        return render(request, 'showPlot.html', context)
    except Exception as e:
        print(e)
        return render(request, 'error.html')
def plotinsoccuvsincstatestacked(request):
    try:
        var1 = request.POST.get('ddlvar1', False)
        var2 = request.POST.get('ddlvar2', False)

        dataset=request.session['vt_dataset'] 
        user_id=int(request.session['uid'])
        data_segment=request.session['vt_datasetname']

        ## plotinsoccuvsincstatestacked 

        api_url=getAPIURL()+'plotinsoccuvsincstatestacked/'

        data_src={
            'mdl_id':request.session['vt_mdl'],
            'dataset':dataset,
            'var1':var1,
            'var2':var2,
            'username':request.session['username'],
            'user_id':user_id,
            'data_segment':data_segment
        }

        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url,data= json.dumps(data_src),headers=header)
        print("response stacked bar",response.content,response.status_code)

        context=json.loads(response.content)
        print("context",context)
        print("context['cat_cols_check']",context['cat_cols_check'])
        if context['cat_cols_check']==1:
            return render(request, 'noCatVars.html')
        else:
            print("report",context['report'])

            image_path = os.path.join(BASE_DIR, 'static/media', request.session['username'] + 'plotinsoccuvsincstatestacked.png')
            with open(image_path, "wb") as f:
                f.write(base64.b64decode(context['report']))
            print("Image downloaded successfully.")

        context = {'chartType': context['chartType'], 'pdfFile': plot_dir+user_name+'Stacked Bar chart.pdf', 'graphpath': plot_dir+request.session['username']+'plotinsoccuvsincstatestacked.png', 
                   'ddlvar1': context['ddlvar1'],
                   'ddlvar2': context['ddlvar2'], 'var1': context['var1'], 'var2': context['var2'], 'postAct': plotinsoccuvsincstatestacked}
        return render(request, 'showPlot.html', context)
    except Exception as e:
        print("e",e)
        return render(request, 'error.html')


def var_dist_by_fraud_old(request):
    try:
        var_num = request.POST.get('ddlvar1', False)

        savefile_withoutnull = file_path + file_name + ".csv"
        if(not os.path.exists(savefile_withoutnull)):
            return render(request, 'processNotdone.html')
        df = pd.read_csv(savefile_withoutnull, na_values='?')
        targetVarFile = file_path + file_name + "_targetVar.txt"
        file1 = open(targetVarFile, "r")  # write mode
        targetVar = file1.read()
        file1.close()
        # x_keep = pd.read_csv(savefile_x_keep)
        num_cols_temp = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] not in [np.object]]
        num_cols=[]
        for x in num_cols_temp:
            if len(df[x].value_counts())<25:
                num_cols.append(x)
        if(var_num == False):
            var_num = num_cols[0]

        fig, axes = joypy.joyplot(df,
                                  column=[var_num],
                                  by=targetVar,
                                  ylim='own',
                                  figsize=(10, 6),
                                  alpha=0.5,
                                  legend=True)

        plt.title(var_num, fontsize=20)
        plt.tight_layout()
        fig.savefig(os.path.join(
            BASE_DIR, plot_dir_view+user_name+'distbyfraud.png'))
        plt.close()
        context = {'graphpath':  plot_dir+user_name+'distbyfraud.png',
                   'ddlvar1': num_cols, 'var1': var_num, 'hideddl2': 'none', 'postAct': var_dist_by_fraud_old}
        return render(request, 'showPlot.html', context)
    except Exception as e:
        print(e)
        return render(request, 'error.html')
# Pairwise correlation


def pairwise_correlation(request):
    try:
        savefile_withoutnull = file_path + file_name + ".csv"
        if(not os.path.exists(savefile_withoutnull)):
            return render(request, 'processNotdone.html')
        df = pd.read_csv(savefile_withoutnull, na_values='?')
        var1 = "capital-gains"
        var2 = "total_claim_amount"
        targetVarFile = file_path + file_name + "_targetVar.txt"
        file1 = open(targetVarFile, "r")  # write mode
        targetVar = file1.read()
        file1.close()
        # plotting a correlation scatter plot
        fig1 = px.scatter_matrix(
            df, dimensions=[var1, var2], color=targetVar)
        # fig1.show()

        # plotting a 3D scatter plot
        fig2 = px.scatter(df, x=var1, y=var2, color=targetVar,
                          marginal_x='rug', marginal_y='histogram')
        # fig2.show()
        fig1.write_image(os.path.join(
            BASE_DIR, plot_dir_view+user_name+'pairwise_correlation_fig1.png'))

        fig2.write_image(os.path.join(
            BASE_DIR, plot_dir_view+user_name+'pairwise_correlation_fig2.png'))

        plot_div = plot(fig1, include_plotlyjs=False, output_type='div')
        plot_div2 = plot(fig2, include_plotlyjs=False, output_type='div')

        context = {'graphpath': Markup(plot_div),
                   'graphpath2': Markup(plot_div2)}
        del df
        return render(request, 'pairwise_correlation.html', context)
    except Exception as e:
        print(e)
        return render(request, 'error.html')


# def vardistbyfraud(request):
    try:
        var_cat = request.POST.get('ddlvar2', False)
        var_num = request.POST.get('ddlvar1', False)
        print('vardistbyfraud')
        savefile_withoutnull = file_path + file_name + ".csv"
        if(not os.path.exists(savefile_withoutnull)):
            return render(request, 'processNotdone.html')
        file_id=find_max_file_id(request.session['vt_mdl'])
        dataset=request.session['vt_dataset'] 
        df=find_src_data(file_id,dataset)
        cat_cols_temp = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] in [np.object]]

        cat_cols=[]
        for x in cat_cols_temp:
            if len(df[x].value_counts())<25:
                cat_cols.append(x)

        if(len(cat_cols)<1):
            return render(request, 'noCatVars.html')
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
            BASE_DIR, plot_dir_view+user_name+'distbyfraud2.png'))
        saveChartViewd('Distribution', var_num, var_cat,
                       user_name+'distbyfraud2.png',request.session['vt_mdl'],request.session['uid'],request.session['vt_datasetname'])
        del df
        if os.path.exists(os.path.join(
                BASE_DIR, plot_dir_view+user_name+'distbyfraud2.png')):
            pdf = FPDF()
            pdf.add_page()
            pdf = exportgraphImgPdf(pdf, os.path.join(
                BASE_DIR, plot_dir_view+user_name+'distbyfraud2.png'), " Distribution "+var_num+" vs "+var_cat)
            pdf.output(os.path.join(
                BASE_DIR, plot_dir_view +"/"+user_name+"Distribution.pdf"))

        context = {'chartType': 'Distribution', 'pdfFile': plot_dir+user_name+'Distribution.pdf', 'graphpath': plot_dir+user_name+'distbyfraud2.png',
                   'ddlvar1': num_cols, 'ddlvar2': cat_cols, 'var1': var_num, 'var2': var_cat, 'hideddl2': '', 'postAct': vardistbyfraud}
        
        objmaster.insertActivityTrail(request.session['vt_mdl'],"21","Data visualization distribution chart viewed for "+ var_num + " vs  "+var_cat+".",request.session['uid'],request.session['accessToken'])
        return render(request, 'showPlot.html', context)
    except Exception as e:
        print(e)
        return render(request, 'error.html')


# def stripplot(request):
    try:
        import matplotlib.pyplot as pltstrip
        import seaborn as snsstrip
        var_cat = request.POST.get('ddlvar2', False)
        var_num = request.POST.get('ddlvar1', False)
        savefile_withoutnull = file_path + file_name + ".csv"
        if(not os.path.exists(savefile_withoutnull)):
            return render(request, 'processNotdone.html')
        df = pd.read_csv(savefile_withoutnull, na_values='?')
        # x_keep = pd.read_csv(savefile_x_keep)
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
            BASE_DIR, plot_dir_view+user_name+'outputstripplot.png'))
        pltstrip.close()
        saveChartViewd('Strip Plot', var_num, var_cat,
                       user_name+'outputstripplot.png',request.session['vt_mdl'],request.session['uid'],request.session['vt_datasetname'])
        del df
        if os.path.exists(os.path.join(
                BASE_DIR, plot_dir_view+user_name+'outputstripplot.png')):
            pdf = FPDF()
            pdf.add_page()
            pdf = exportgraphImgPdf(pdf, os.path.join(
                BASE_DIR, plot_dir_view+user_name+'outputstripplot.png'), " Strip Plot "+var_num+" vs "+var_cat)
            pdf.output(os.path.join(
                BASE_DIR, plot_dir_view+user_name+'Strip Plot.pdf'))

        context = {'chartType': 'Strip Plot', 'pdfFile': plot_dir+user_name+'Strip Plot.pdf', 'graphpath': plot_dir+user_name+'outputstripplot.png',
                   'ddlvar1': num_cols, 'ddlvar2': cat_cols, 'var1': var_num, 'var2': var_cat, 'hideddl2': '', 'postAct': stripplot}
        objmaster.insertActivityTrail(request.session['vt_mdl'],"21","Data visualization strip plot viewed for "+ var_num + " vs  "+var_cat+".",request.session['uid'],request.session['accessToken'])
        return render(request, 'showPlot.html', context)
    except Exception as e:
        print(e)
        return render(request, 'error.html')
def stripplot(request):
    try:

        var_cat = request.POST.get('ddlvar2', False)
        var_num = request.POST.get('ddlvar1', False)
        print("var_cat",var_cat)
        print("var_num",var_num)
        
        dataset=request.session['vt_dataset'] 
        user_id=int(request.session['uid'])
        data_segment=request.session['vt_datasetname']

        api_url=getAPIURL()+'stripplot/'

        data_src={
            'mdl_id':request.session['vt_mdl'],
            'dataset':dataset,
            'var_cat':var_cat,
            'var_num':var_num,
            'username':request.session['username'],
            'user_id':user_id,
            'data_segment':data_segment
        }

        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url,data= json.dumps(data_src),headers=header)
        print("response strip plot ",response.content,response.status_code)

        context=json.loads(response.content)
        print("context",context)
        print("context['cat_cols_check']",context['cat_cols_check'])
        if context['cat_cols_check']==1:
            return render(request, 'noCatVars.html')
        else:
            print("report",context['report'])

            image_path = os.path.join(BASE_DIR, 'static/media', request.session['username'] + 'outputstripplot.png')
            with open(image_path, "wb") as f:
                f.write(base64.b64decode(context['report']))
            print("Image downloaded successfully.")

        context = {'chartType': context['chartType'], 'pdfFile': plot_dir+user_name+'Strip Plot.pdf', 'graphpath': plot_dir+request.session['username']+'outputstripplot.png',
                   'ddlvar1': context['ddlvar1'], 'ddlvar2': context['ddlvar2'], 'var1': context['var1'], 'var2': context['var2'], 'hideddl2': '', 'postAct': stripplot}
        return render(request, 'showPlot.html', context)
    except Exception as e:
        print(e)
        return render(request, 'error.html')



def vardistbyfraud(request):
    try:
        var_cat = request.POST.get('ddlvar2', False)
        var_num = request.POST.get('ddlvar1', False)
        print('vardistbyfraud')

        dataset=request.session['vt_dataset'] 
        user_id=int(request.session['uid'])
        data_segment=request.session['vt_datasetname']

        api_url=getAPIURL()+'distribution/'

        data_src={
            'mdl_id':request.session['vt_mdl'],
            'dataset':dataset,
            'var_cat':var_cat,
            'var_num':var_num,
            'username':request.session['username'],
            'user_id':user_id,
            'data_segment':data_segment
        }

        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url,data= json.dumps(data_src),headers=header)
        print("response distribution",response.content,response.status_code)

        context=json.loads(response.content)
        print("context",context)
        print("context['cat_cols_check']",context['cat_cols_check'])
        if context['cat_cols_check']==1:
            return render(request, 'noCatVars.html')
        else:
            print("report",context['report'])

            image_path = os.path.join(BASE_DIR, 'static/media', request.session['username'] + 'distbyfraud2.png')
            with open(image_path, "wb") as f:
                f.write(base64.b64decode(context['report']))
            print("Image downloaded successfully.")

        context = {'chartType': context['chartType'], 'pdfFile': plot_dir+user_name+'Distribution.pdf', 'graphpath': plot_dir+request.session['username']+'distbyfraud2.png',
                   'ddlvar1': context['ddlvar1'], 'ddlvar2': context['ddlvar2'], 'var1': context['var1'], 'var2': context['var2'], 'hideddl2': context['hideddl2'], 'postAct': vardistbyfraud}
        return render(request, 'showPlot.html', context)
    except Exception as e:
        print(e)
        return render(request, 'error.html')





def stripplot(request):
    try:

        var_cat = request.POST.get('ddlvar2', False)
        var_num = request.POST.get('ddlvar1', False)
        print("var_cat",var_cat)
        print("var_num",var_num)
        
        dataset=request.session['vt_dataset'] 
        user_id=int(request.session['uid'])
        data_segment=request.session['vt_datasetname']

        api_url=getAPIURL()+'stripplot/'

        data_src={
            'mdl_id':request.session['vt_mdl'],
            'dataset':dataset,
            'var_cat':var_cat,
            'var_num':var_num,
            'username':request.session['username'],
            'user_id':user_id,
            'data_segment':data_segment
        }

        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url,data= json.dumps(data_src),headers=header)
        print("response strip plot ",response.content,response.status_code)

        context=json.loads(response.content)
        print("context",context)
        print("context['cat_cols_check']",context['cat_cols_check'])
        if context['cat_cols_check']==1:
            return render(request, 'noCatVars.html')
        else:
            print("report",context['report'])

            image_path = os.path.join(BASE_DIR, 'static/media', request.session['username'] + 'outputstripplot.png')
            with open(image_path, "wb") as f:
                f.write(base64.b64decode(context['report']))
            print("Image downloaded successfully.")

        context = {'chartType': context['chartType'], 'pdfFile': plot_dir+user_name+'Strip Plot.pdf', 'graphpath': plot_dir+request.session['username']+'outputstripplot.png',
                   'ddlvar1': context['ddlvar1'], 'ddlvar2': context['ddlvar2'], 'var1': context['var1'], 'var2': context['var2'], 'hideddl2': '', 'postAct': stripplot}
        return render(request, 'showPlot.html', context)
    except Exception as e:
        print(e)
        return render(request, 'error.html')


# def totalclaim_boxplot(request):
    try:
        import matplotlib.pyplot as pltbox
        import seaborn as snsbox
        var_cat = request.POST.get('ddlvar2', False)
        var_num = request.POST.get('ddlvar1', False)
        savefile_withoutnull = file_path + file_name + ".csv"
        if(not os.path.exists(savefile_withoutnull)):
            return render(request, 'processNotdone.html')
        df = pd.read_csv(savefile_withoutnull, na_values='?')
        # x_keep = pd.read_csv(savefile_x_keep)
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

        if(var_num == False):
            var_num = num_cols[0]
            var_cat = cat_cols[1]
            # context = {'chartType': 'Box Plot', 'pdfFile': '', 'graphpath': '',
            #            'ddlvar1': num_cols, 'ddlvar2': cat_cols, 'var1': var_num, 'var2': var_cat, 'hideddl2': '', 'postAct': totalclaim_boxplot}
            # return render(request, 'showPlot.html', context)
        fig = pltbox.figure(figsize=(14, 8))
        pltbox.style.use('fivethirtyeight')
        pltbox.rcParams['figure.figsize'] = (20, 8)
        snsbox.boxenplot(df[var_cat], df[var_num], palette='pink', figure=fig)
        pltbox.title(var_num, fontsize=20)
        pltbox.savefig(os.path.join(
            BASE_DIR, plot_dir_view+user_name+'outputclaimboxplot.png'))
        pltbox.close()
        saveChartViewd('Box Plot', var_num, var_cat,
                       user_name+'outputclaimboxplot.png',request.session['vt_mdl'],request.session['uid'],request.session['vt_datasetname'])
        del df
        if os.path.exists(os.path.join(
                BASE_DIR, plot_dir_view+user_name+'outputclaimboxplot.png')):
            pdf = FPDF()
            pdf.add_page()
            pdf = exportgraphImgPdf(pdf, os.path.join(
                BASE_DIR, plot_dir_view+user_name+'outputclaimboxplot.png'), " Box Plot "+var_num+" vs "+var_cat)
            pdf.output(os.path.join(
                BASE_DIR, plot_dir_view+user_name+'Box Plot.pdf'))

        context = {'chartType': 'Box Plot', 'pdfFile': plot_dir+user_name+'Box Plot.pdf', 'graphpath': plot_dir+user_name+'outputclaimboxplot.png',
                   'ddlvar1': num_cols, 'ddlvar2': cat_cols, 'var1': var_num, 'var2': var_cat, 'hideddl2': '', 'postAct': totalclaim_boxplot}
        
        objmaster.insertActivityTrail(request.session['vt_mdl'],"21","Data visualization box chart viewed for "+ var_num + " vs  "+var_cat+".",request.session['uid'],request.session['accessToken'])
        return render(request, 'showPlot.html', context)
    except Exception as e:
        print("Error is ", e)
        return render(request, 'error.html')
def totalclaim_boxplot(request):
    try:
        print("totalclaim_boxplot",request.session['username'])
        var_cat = request.POST.get('ddlvar2', False)
        var_num = request.POST.get('ddlvar1', False)

        dataset=request.session['vt_dataset'] 


        # third_party_api_url = api_url+'box_plot/'

        api_url=getAPIURL()+'box_plot/'
        user_id=int(request.session['uid'])
        data_segment=request.session['vt_datasetname']

        data_src={
            'mdl_id':request.session['vt_mdl'],
            'dataset':dataset,
            'var_cat':var_cat,
            'var_num':var_num,
            'username':request.session['username'],
            'user_id':user_id,
            'data_segment':data_segment
        }

        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url,data= json.dumps(data_src),headers=header)
        print("response box plot",response.content,response.status_code)

        context=json.loads(response.content)
        print("context",context)
        print("report",context['report'])

        image_path = os.path.join(BASE_DIR, 'static/media', request.session['username'] + 'outputclaimboxplot.png')
        with open(image_path, "wb") as f:
            f.write(base64.b64decode(context['report']))
        print("Image downloaded successfully.")
        
        context = {'chartType': context['chartType'], 'pdfFile': plot_dir+user_name+'Box Plot.pdf', 'graphpath': plot_dir+request.session['username']+'outputclaimboxplot.png',
                   'ddlvar1': context['ddlvar1'], 'ddlvar2': context['ddlvar2'], 'var1': context['var1'], 'var2': context['var2'], 'hideddl2': context['hideddl2'], 'postAct': totalclaim_boxplot}
        return render(request, 'showPlot.html', context)
    except Exception as e:
        print("Error is ", e)
        return render(request, 'error.html')



def vehicle_claim(request):
    try:
        var_cat = request.POST.get('ddlvar2', False)
        var_num = request.POST.get('ddlvar1', False)

        savefile_withoutnull = file_path + file_name + ".csv"
        if(not os.path.exists(savefile_withoutnull)):
            return render(request, 'processNotdone.html')
        df = pd.read_csv(savefile_withoutnull, na_values='?')
        # x_keep = pd.read_csv(savefile_x_keep)
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
        context = {'plot_div': Markup(plot_div), 'var1': var_num,
                   'var2': var_cat, 'ddlvar1': num_cols, 'ddlvar2': cat_cols, 'displayddl3': 'none', 'hideUnvar': 'none', 'postAct': vehicle_claim,
                     'pageHeader': 'Box Plot 3D'}
        
        objmaster.insertActivityTrail(request.session['vt_mdl'],"21","Data visualization box plot 3D viewed for "+ var_num + " vs  "+var_cat+".",request.session['uid'],request.session['accessToken'])
        return render(request, 'show3dplot.html', context)
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def scattred3d(request):
    try:
        var2 = request.POST.get('ddlvar2', False)
        var1 = request.POST.get('ddlvar1', False)
        var3 = request.POST.get('ddlvar3', False)

        savefile_withoutnull = file_path + file_name + ".csv"
        if(not os.path.exists(savefile_withoutnull)):
            return render(request, 'processNotdone.html')
        df = pd.read_csv(savefile_withoutnull, na_values='?')
        # x_keep = pd.read_csv(savefile_x_keep)
        num_cols = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] not in [np.object]]
        cat_cols = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] in [np.object]]
        if(len(cat_cols)<1):
            return render(request, 'noCatVars.html')
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
        fig.write_image(os.path.join(
            BASE_DIR, plot_dir_view+user_name+'outputscattred3d.png'))
        context = {'graphpath': plot_dir+user_name+'outputscattred3d.png',
                   'plot_div': Markup(plot_div), 'var1': var1,
                   'var2': var2, 'var3': var3, 'ddlvar1': num_cols, 'ddlvar2': num_cols, 'ddlvar3': cat_cols, 'hideUnvar': 'none', 'displayddl3': '', 'postAct': scattred3d, 'pageHeader': 'Scattered 3D'}
        return render(request, 'show3dplot.html', context)
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def bubblePlot3d(request):
    try:
        var2 = request.POST.get('ddlvar2', False)
        var1 = request.POST.get('ddlvar1', False)

        savefile_withoutnull = file_path + file_name + ".csv"
        if(not os.path.exists(savefile_withoutnull)):
            return render(request, 'processNotdone.html')
        df = pd.read_csv(savefile_withoutnull, na_values='?')
        # x_keep = pd.read_csv(savefile_x_keep)
        num_cols = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] not in [np.object]]
        df = df.sort_values(by=['auto_year', 'months_as_customer'])
        # x_keep = pd.read_csv(savefile_x_keep)
        if(var1 == False):
            var1 = num_cols[0]
            var2 = num_cols[1]

        figure = bubbleplot(dataset=df, x_column=var1, y_column=var2,
                            bubble_column='fraud_reported', time_column='auto_year', size_column='months_as_customer',
                            color_column='fraud_reported',
                            x_title=var1, y_title=var2,
                            x_logscale=False, scale_bubble=3, height=650)

        # fig = py.plot(figure, config={'scrollzoom': True})

        plot_div = plot(figure, include_plotlyjs=False, output_type='div')
        # fig.write_image(os.path.join(
        #     BASE_DIR, 'static\media\outputscattred3d.png'))
        context = {'graphpath': plot_dir+user_name+'outputscattred3d.png',
                   'plot_div': Markup(plot_div), 'var1': var1,
                   'var2': var2, 'ddlvar1': num_cols, 'ddlvar2': num_cols, 'displayddl3': 'none', 'hideUnvar': 'none', 'postAct': bubblePlot3d, 'pageHeader': 'Bubble Plot'}
        return render(request, 'show3dplot.html', context)
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def file_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        savefile_name = file_path + file_name
        if os.path.exists(savefile_name):
            os.remove(savefile_name)
        else:
            print("Can not delete the file as it doesn't exists")

        filename = fs.save(savefile_name, myfile)
        df = pd.read_csv(savefile_name, na_values='?')

        gridDttypes = []
        dttypes = dict(df.dtypes)
        # print(dttypes)
        for key, value in dttypes.items():
            gridDttypes.append({'colName': key, 'dataType': value})
        result = df.to_json(orient="records")
        result = json.loads(result)
        desc = df.describe()
        arrdescData = []
        for recs, vals in dict(desc).items():
            objdescData = descData()
            print('key ', recs)
            objdescData.colName = recs
            objdescData.count_val = vals['count']
            objdescData.mean_val = vals['mean']
            objdescData.std_val = vals['std']
            objdescData.per25_val = vals['25%']
            objdescData.per50_val = vals['50%']
            objdescData.per75_val = vals['75%']
            objdescData.max_val = vals['max']
            objdescData.min_val = vals['min']
            arrdescData.append(objdescData)
        return render(request, 'FileUpload.html', {'desc': arrdescData, 'dataTypes': gridDttypes, 'df': result})

    return render(request, 'FileUpload.html')


def showCrossTab(request):
    try:
        savefile_x = file_path + file_name + "_x.csv"
        if(not os.path.exists(savefile_x)):
            return render(request, 'processNotdone.html')
        x = pd.read_csv(savefile_x)
        cat_cols = [c for i, c in enumerate(
            x.columns) if x.dtypes[i] in [np.object]]

        if(len(cat_cols)<1):
            return render(request, 'noCatVars.html')
        var1 = "insured_occupation"  # "cat_cols[i]
        var2 = "insured_relationship"  # cat_cols[j]
        dfCRossTab = pd.crosstab(x[var1], x[var2], rownames=[
            var1], colnames=[var2])

        # print(dfCRossTab.columns)
        # print(dttypes)
        result = dfCRossTab.to_json(orient='index')
        result = json.loads(result)
        return render(request, 'showCrossTab.html', {'df': result, 'ColNames': dfCRossTab.columns, 'rowname': var1, 'colname': var2, 'catCols': cat_cols})
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def updateCrossTab(request):
    try:
        var1 = request.POST.get('var1', False)
        var2 = request.POST.get('var2', False)
        savefile_x = file_path + file_name + "_x.csv"
        if(not os.path.exists(savefile_x)):
            return render(request, 'processNotdone.html')
        x = pd.read_csv(savefile_x)
        print('var1 is : ', var1)
        print('var2 is : ', var2)
        cat_cols = [c for i, c in enumerate(
            x.columns) if x.dtypes[i] in [np.object]]
        if(len(cat_cols)<1):
            return render(request, 'noCatVars.html')
        dfCRossTab = pd.crosstab(x[var1], x[var2], rownames=[
            var1], colnames=[var2])

        result = dfCRossTab.to_json(orient='index')
        result = json.loads(result)
        return render(request, 'showCrossTab.html', {'df': result, 'ColNames': dfCRossTab.columns, 'rowname': var1, 'colname': var2, 'catCols': cat_cols})
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def mean_ad(request):
    try:
        savefile_withoutnull = file_path + file_name + ".csv"
        if(not os.path.exists(savefile_withoutnull)):
            return render(request, 'processNotdone.html')
        df = pd.read_csv(savefile_withoutnull, na_values='?')
        num_cols = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] not in [np.object]]
        x_numeric = pd.DataFrame(df, columns=num_cols)
        mean_ad = x_numeric.mad().round(decimals=3)
        # print(mean_ad)
        result = mean_ad.to_json(orient='index')
        result = json.loads(result)
        return render(request, 'showMean_copy.html', {'df': result, 'divHeader': 'compute the mean absolute deviation'})
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def median_ad(request):
    try:
        savefile_withoutnull = file_path + file_name + ".csv"
        if(not os.path.exists(savefile_withoutnull)):
            return render(request, 'processNotdone.html')
        df = pd.read_csv(savefile_withoutnull, na_values='?')
        num_cols = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] not in [np.object]]
        x_numeric = pd.DataFrame(df, columns=num_cols)
        median_ad = x_numeric.apply(robust.mad).round(decimals=3)
        # print(mean_ad)
        result = median_ad.to_json(orient='index')
        result = json.loads(result)
        return render(request, 'showMean.html', {'df': result, 'divHeader': 'compute the median absolute deviation'})
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def showcorrelation(request):
    try:
        # savefile_x = file_path + file_name + "_x.csv"
        # if(not os.path.exists(savefile_x)):
        #     return render(request, 'processNotdone.html')
        # x = pd.read_csv(savefile_x)

        # targetVarFile = file_path + file_name + "_targetVar.txt"
        # file1 = open(targetVarFile, "r")  # write mode
        # targetVar = file1.read()
        # file1.close()
        file_id=find_max_file_id(request.session['vt_mdl'])
        dataset=request.session['vt_dataset']
        x=find_src_data(file_id,dataset) 
        targetVar=find_target_value(file_id)
        if not(targetVar=="None"):
            x = x.drop(targetVar, axis=1)

        dfcorr = x.corr().round(decimals=4) 
        # print(dfcorr.columns)
        result = dfcorr.to_json(orient='index')
        result = json.loads(result)

        fig = plt.figure(figsize=(14, 8))

        sns_plot = sns.heatmap(dfcorr, annot=False)
        fig = sns_plot.get_figure()
        plt.tight_layout()
        fig.savefig(os.path.join(
            BASE_DIR, plot_dir_view+user_name+'outputcorrelation.png'), dpi=400)
        # (result)

        saveChartViewd("Heatmap", "", "", user_name+'outputcorrelation.png',request.session['vt_mdl'],request.session['uid'],request.session['vt_datasetname'])
        # if os.path.exists(os.path.join(
        #         BASE_DIR, 'static\media\outputcorrelation.png')):
        pdf = FPDF()
        pdf.add_page()
        pdf = exportgraphImgPdf(pdf, os.path.join(
            BASE_DIR, plot_dir_view+user_name+'outputcorrelation.png'),  "Correlation on independent variables-Heat map", "")
        pdf.output(os.path.join(
            BASE_DIR, plot_dir_view+user_name+'Heatmap.pdf'))

        return render(request, 'showCorrelation1.html', {'pdfFile': plot_dir+user_name+'Heatmap.pdf', 'df': result, 'ColNames': dfcorr.columns, 'graphpath': plot_dir+user_name+'outputcorrelation.png'})
    except Exception as e:
        print(e, traceback.print_exc())
        return render(request, 'error.html')


def showSNScorrelation(request):
    try:
        savefile_x = file_path + file_name + "_x.csv"
        if(not os.path.exists(savefile_x)):
            return render(request, 'processNotdone.html')
        x = pd.read_csv(savefile_x)

        dfcorr = x.corr()

        fig = plt.figure(figsize=(14, 8))

        sns_plot = sns.heatmap(dfcorr, annot=True)
        fig = sns_plot.get_figure()
        plt.tight_layout()
        fig.savefig(os.path.join(
            BASE_DIR, plot_dir_view+user_name+'outputcorrelation.png'), dpi=400)
        return render(request, 'showSNSHeatMap1.html', {'graphpath': plot_dir_view+user_name+'outputcorrelation.png'})
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def dist_numevari_catvar(request):
    try:
        var1 = request.POST.get('var1', False)
        var2 = request.POST.get('var2', False) 
        file_id=find_max_file_id(request.session['vt_mdl'])
        dataset=request.session['vt_dataset']
        df=find_src_data(file_id,dataset)
        cat_cols = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] in [np.object]]
        noData=""
        if(len(cat_cols)<1):
            noData="Categorical variables not available to run this utility."
        num_cols = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] not in [np.object]]
        if(var1 != False):
            cat_var = var1  # cat_cols[i]
            num_var = var2  # num_cols[j]
        else:
            cat_var = cat_cols[0]  # cat_cols[i]
            num_var = num_cols[0]  # num_cols[j]
        dist_num_cat = df.groupby(cat_var)[num_var].describe().round(decimals=4)
        result = dist_num_cat.to_json(orient='index')
        result = json.loads(result)
        return render(request, 'showdistnumcat.html', {'noData':noData,'df': result, 'cat_var': cat_var, 'num_var': num_var, 'colNames': dist_num_cat.columns, 'numCols': num_cols, 'catCols': cat_cols, 'divHeader': 'Distribution of ' + num_var + ' at ' + cat_var})
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def create_dummy_variables(request):
    try:
        content = request.POST.get('rdoChart', False)
        # savefile_x_keep = file_path + file_name + "_x_keep.csv"
        # if(not os.path.exists(savefile_x_keep)):
        #     return render(request, 'processNotdone.html')
        gridDttypes = []
        result = ""
        _isDisabled="disabled"
        print('dummy var content is ', content)
        if(content == "NoData"):
            # if(os.path.exists(savefile_x_keep)):
            #     x_keep = pd.read_csv(savefile_x_keep, na_values='?')

            #     targetVarFile = file_path + file_name + "_targetVar.txt"
            #     file1 = open(targetVarFile, "r")  # write mode
            #     targetVar = file1.read()
            #     file1.close()
            file_id=find_max_file_id(request.session['vt_mdl'])
            dataset=request.session['vt_dataset']
            x_keep=find_src_data(file_id,dataset)
            cat_cols1=[] #get_cat_cols(x_keep)
            targetVar=find_target_value(file_id)
            y = x_keep[targetVar]
            print("y",y)
            if not(targetVar=="None"):
                x_keep = x_keep.drop(targetVar, axis=1)

            # cat_cols1 = [c for i, c in enumerate(
            #     x_keep.columns) if x_keep.dtypes[i] in [np.object]]

            x_dummy = pd.get_dummies(x_keep, columns=cat_cols1)

            dttypes = dict(x_dummy.dtypes)
            # print(dttypes)
            for key, value in dttypes.items():
                gridDttypes.append({'colName': key, 'dataType': value})

            savefile_x_dummy = file_path + file_name + "_x_dummy.csv"
            x = pd.concat([x_dummy, y], axis=1)
            x.to_csv(savefile_x_dummy, index=False)
            processing = os.path.join(
                BASE_DIR, processingFile_path)
            df_old_proc = pd.read_csv(processing)
            df_old_proc.loc[df_old_proc.Idx == 7, "Status"] = "Done"
            df_old_proc.to_csv(processing, index=False)
            del df_old_proc
            return render(request, 'stdFeaturesOpt.html')
        elif(content == "Data"):
            # if(os.path.exists(savefile_x_keep)):
            #     x_keep = pd.read_csv(savefile_x_keep, na_values='?')

            #     targetVarFile = file_path + file_name + "_targetVar.txt"
            #     file1 = open(targetVarFile, "r")  # write mode
            #     targetVar = file1.read()
            #     file1.close()
            file_id=find_max_file_id(request.session['vt_mdl'])
            dataset=request.session['vt_dataset']
            x_keep=find_src_data(file_id,dataset)
            
            cat_cols1=[] #get_cat_cols(x_keep)
            targetVar=find_target_value(file_id)

            if not(targetVar=="None"):
                y = x_keep[targetVar]
                x_keep = x_keep.drop(targetVar, axis=1)

            # cat_cols1 = [c for i, c in enumerate(
            #     x_keep.columns) if x_keep.dtypes[i] in [np.object]]

            if(len(cat_cols1)<1):
                return render(request, 'noCatVars.html')
            x_dummy = pd.get_dummies(x_keep, columns=cat_cols1)

            dttypes = dict(x_dummy.dtypes)
            # print(dttypes)
            for key, value in dttypes.items():
                gridDttypes.append({'colName': key, 'dataType': value})

            savefile_x_dummy = file_path + file_name + "_x_dummy.csv"
            x = pd.concat([x_dummy, y], axis=1)
            x.to_csv(savefile_x_dummy, index=False)
            result = x_dummy.to_json(orient='records')
            result = json.loads(result)
            processing = os.path.join(
                BASE_DIR, processingFile_path)
            df_old_proc = pd.read_csv(processing)
            df_old_proc.loc[df_old_proc.Idx == 7, "Status"] = "Done"
            df_old_proc.to_csv(processing, index=False)
            del df_old_proc
            return render(request, 'viewDummyData.html',  {'df': result, 'dataTypes': gridDttypes, 'tableHead': 'Create Dummy Variables'})
        elif(content == "Skip"):
            # if(os.path.exists(savefile_x_keep)):
            #     x_keep = pd.read_csv(savefile_x_keep, na_values='?')

            savefile_x_dummy = file_path + file_name + "_x_dummy.csv"
            x_keep.to_csv(savefile_x_dummy, index=False)
            processing = os.path.join(
                BASE_DIR, processingFile_path)
            df_old_proc = pd.read_csv(processing)
            df_old_proc.loc[df_old_proc.Idx == 7, "Status"] = "Done"
            df_old_proc.loc[df_old_proc.Idx == 7, "IsSkipped"] = "Yes"
            df_old_proc.to_csv(processing, index=False)
            del df_old_proc
            return render(request, 'stdFeaturesOpt.html')
        else:
            # savefile_x_dummy = file_path + file_name + "_x_dummy.csv"
            # if(os.path.exists(savefile_x_dummy)):
            #     _isDisabled=""
            return render(request, 'dummyVarOptions.html',{'isDisabled':_isDisabled})
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def std_features(request):
    try:
        content = request.POST.get('rdoChart', False)
        savefile_x_dummy = file_path + file_name + "_x_dummy.csv"
        if(not os.path.exists(savefile_x_dummy)):
            return render(request, 'processNotdone.html')
        gridDttypes = []
        result = ""
        _isDisabled="disabled"
        if(content == "NoData"):
            if os.path.exists(savefile_x_dummy):
                x_dummy = pd.read_csv(savefile_x_dummy, na_values='?')

                targetVarFile = file_path + file_name + "_targetVar.txt"
                file1 = open(targetVarFile, "r")  # write mode
                targetVar = file1.read()
                file1.close()
                y = x_dummy[targetVar]
                if not(targetVar=="None"):
                    x_dummy = x_dummy.drop(targetVar, axis=1)

                sc = StandardScaler()
                x_scaled = sc.fit_transform(x_dummy)
                x_scaled_df = pd.DataFrame(x_scaled, columns=x_dummy.columns)
                # print('x_scaled \n')
                # print(x_scaled_df)

                dttypes = dict(x_scaled_df.dtypes)
                # print(dttypes)
                for key, value in dttypes.items():
                    gridDttypes.append({'colName': key, 'dataType': value})

                savefile_x_scaled = file_path + file_name + "_x_scaled.csv"
                x = pd.concat([x_scaled_df, y], axis=1)
                x.to_csv(savefile_x_scaled, index=False)
                processing = os.path.join(
                    BASE_DIR, processingFile_path)
                df_old_proc = pd.read_csv(processing)
                df_old_proc.loc[df_old_proc.Idx == 8, "Status"] = "Done"
                df_old_proc.to_csv(processing, index=False)
                del df_old_proc
                # x_scaled_df.round(decimals=6).to_json(orient='records')
                result = x_scaled_df.to_json(orient='records')
                result = json.loads(result)
            return redirect('test_multicollinearity')
        elif(content == "Data"):
            if os.path.exists(savefile_x_dummy):
                x_dummy = pd.read_csv(savefile_x_dummy, na_values='?')

                targetVarFile = file_path + file_name + "_targetVar.txt"
                file1 = open(targetVarFile, "r")  # write mode
                targetVar = file1.read()
                file1.close()
                y = x_dummy[targetVar]
                if not(targetVar=="None"):
                    x_dummy = x_dummy.drop(targetVar, axis=1)

                sc = StandardScaler()
                x_scaled = sc.fit_transform(x_dummy)
                x_scaled_df = pd.DataFrame(x_scaled, columns=x_dummy.columns)
                # print('x_scaled \n')
                # print(x_scaled_df)

                dttypes = dict(x_scaled_df.dtypes)
                # print(dttypes)
                for key, value in dttypes.items():
                    gridDttypes.append({'colName': key, 'dataType': value})

                savefile_x_scaled = file_path + file_name + "_x_scaled.csv"
                x = pd.concat([x_scaled_df, y], axis=1)
                x.to_csv(savefile_x_scaled, index=False)
                processing = os.path.join(
                    BASE_DIR, processingFile_path)
                df_old_proc = pd.read_csv(processing)
                df_old_proc.loc[df_old_proc.Idx == 8, "Status"] = "Done"
                df_old_proc.to_csv(processing, index=False)
                del df_old_proc
                # x_scaled_df.round(decimals=6).to_json(orient='records')
                result = x_scaled_df.to_json(orient='records')
                result = json.loads(result)
            return render(request, 'viewDummyData.html',  {'df': result, 'dataTypes': gridDttypes, 'tableHead': 'Standardize the features'})
        elif(content == "Skip"):
            if(os.path.exists(savefile_x_dummy)):
                x_keep = pd.read_csv(savefile_x_dummy, na_values='?')

                savefile_x_scaled = file_path + file_name + "_x_scaled.csv"
                x_keep.to_csv(savefile_x_scaled, index=False)
                processing = os.path.join(
                    BASE_DIR, processingFile_path)
                df_old_proc = pd.read_csv(processing)
                df_old_proc.loc[df_old_proc.Idx == 8, "Status"] = "Done"
                df_old_proc.loc[df_old_proc.Idx == 8, "IsSkipped"] = "Yes"
                df_old_proc.to_csv(processing, index=False)
                del df_old_proc
            return redirect('test_multicollinearity')
        else:
            savefile_x_scaled = file_path + file_name + "_x_scaled.csv"
            if os.path.exists(savefile_x_scaled):
                _isDisabled=""
            return render(request, 'stdFeaturesOpt.html',{"isDisabled":_isDisabled})

    except Exception as e:
        print(e)
        print('error is ', traceback.print_exc())
        return render(request, 'error.html')

# Test Multicollinearity


def test_multicollinearity(request):
    try:
        _isDisabled="disabled"
        savefile_x_final = file_path + file_name + "_x_final.csv"
        if os.path.exists(savefile_x_final):
            savefile_x_scaled = savefile_x_final
        else:
            savefile_x_scaled = file_path + file_name + "_x_scaled.csv"
        savefile_x_keep = file_path + file_name + "_x_keep.csv"
        if(not os.path.exists(savefile_x_keep)):
            return render(request, 'processNotdone.html')
        gridFreqData = []
        x_scaledDttypes = []
        resultCrossTab = ""
        result = ""
        dfCRossTab = DataFrame()
        var1 = ""
        var2 = ""
        cat_cols = []
        result=[]
        gridDttypes = [{'colName': 'feature'}, {'colName': 'VIF'}]
        if os.path.exists(savefile_x_scaled):
            x_scaled_df = pd.read_csv(savefile_x_scaled, na_values='?')
            x_keep = pd.read_csv(savefile_x_keep, na_values='?')

            targetVarFile = file_path + file_name + "_targetVar.txt"
            file1 = open(targetVarFile, "r")  # write mode
            targetVar = file1.read()
            file1.close()
            if not(targetVar=="None"):
                x_keep = x_keep.drop(targetVar, axis=1)
                x_scaled_df = x_scaled_df.drop(targetVar, axis=1)

                
                
                vif_data = pd.DataFrame()
                vif_data["feature"] = x_scaled_df.columns

                # calculating VIF for each feature
                vif_data["VIF"] = [variance_inflation_factor(x_scaled_df.values, i)
                                for i in range(len(x_scaled_df.columns))]

                vif_data = vif_data.sort_values(
                    "VIF", ascending=False)  # json.loads(result)
                result = vif_data.to_json(orient='records')
                result = json.loads(result)
            # print(result)
            cat_cols1 = [c for i, c in enumerate(
                    x_keep.columns) if x_keep.dtypes[i] in [np.object]]
            x_categori = pd.DataFrame(x_keep, columns=cat_cols1)
            for col in x_categori.columns:
                objlstColFreq = lstColFreq()
                col_count = x_categori[col].value_counts()
                # print(dict(col_count))

                objlstColFreq.colName = col
                objlstColFreq.freqVal = dict(col_count)
                objlstColFreq.total_rows = x_categori[col].count()
                objlstColFreq.missing_rows = len(
                    x_categori[col])-x_categori[col].count()
                gridFreqData.append(objlstColFreq)

            if not(targetVar=="None"):
                savefile_withoutnull = file_path + file_name + ".csv"
                df = pd.read_csv(savefile_withoutnull)
                cat_cols = [c for i, c in enumerate(
                    df.columns) if df.dtypes[i] in [np.object]]
                if(len(cat_cols)>0): 
                    var1 = targetVar  # "cat_cols[i]
                    var2 = cat_cols[0]  # cat_cols[j]
                    dfCRossTab = pd.crosstab(df[var1], df[var2], rownames=[
                        var1], colnames=[var2])
                    resultCrossTab = dfCRossTab.to_json(orient='index')
                    resultCrossTab = json.loads(resultCrossTab)

            # dfx_scaled = pd.read_csv(savefile_x_scaled, na_values='?')

            dttypes = dict(x_scaled_df.dtypes)
            # print(dttypes)
            idx = 1
            for key, value in dttypes.items():
                x_scaledDttypes.append({'colName': key, 'chkId': idx})
                idx = idx + 1
        savefile_x_final = file_path + file_name + "_x_final.csv"
        if os.path.exists(savefile_x_final):
            _isDisabled=""
        return render(request, 'multicollinearity.html',  {'isDisabled':_isDisabled,'df': result, 'x_scaledDttypes': x_scaledDttypes, 'resultCrossTab': resultCrossTab, 'ColNames': dfCRossTab.columns, 'rowname': var1, 'colname': var2, 'catCols': cat_cols, 'dataTypes': gridDttypes, 'FreqData': gridFreqData, 'tableHead': 'Test Multicollinearity and Remove the High Correlated Feature'})
    except Exception as e:
        print(e)
        print(traceback.print_exc())
        return render(request, 'error.html')


def updateCT(request):
    csvfile = file_path + file_name + ".csv"
    df = pd.read_csv(csvfile, na_values='?')
    var1 = request.GET['var1']
    var2 = request.GET['var2']
    dfCRossTab = pd.crosstab(df[var1], df[var2], rownames=[
                             var1], colnames=[var2])
    resultCrossTab = dfCRossTab.to_json(orient='index')
    resultCrossTab = json.loads(resultCrossTab)

    data = {
        'ctData': resultCrossTab, 'rowname': var1, 'colname': var2
    }
    return JsonResponse(data)


def dropFinalColumns(request):
    savefile_x_scaled = file_path + file_name + "_x_scaled.csv"
    if os.path.exists(savefile_x_scaled):
        df = pd.read_csv(savefile_x_scaled, na_values='?')
        content = request.GET['delcolList']
        # print('content is')
        # print(content)
        json_dictionary = json.loads(content)
        delcolLst = []
        for colval in json_dictionary:
            for attribute, value in colval.items():
                if(attribute == 'column'):
                    delcolLst.append(value)

        # print(delcolLst)
        # drop target and cust_id from the datset
        
        x = df.drop(delcolLst, axis=1)
        savefile_x_final = file_path + file_name + "_x_final.csv"
        x.to_csv(savefile_x_final, index=False)
        processing = os.path.join(BASE_DIR, processingFile_path)
        df_old_proc = pd.read_csv(processing)
        df_old_proc.loc[df_old_proc.Idx == 9, "Status"] = "Done"
        df_old_proc.to_csv(processing, index=False)
        del df_old_proc
    data = {
        'is_taken': True
    }
    return JsonResponse(data)

# Detect outliers

# from .vaexPlots import get_cat_cols,get_num_cols

def detect_outliers(request):
    try:
        # savefile_x_keep = file_path + file_name + "_x_keep.csv"
        # if(not os.path.exists(savefile_x_keep)):
        #     return render(request, 'processNotdone.html')
        # x_keep = pd.read_csv(savefile_x_keep, na_values='?')
        
        file_id=find_max_file_id(request.session['vt_mdl'])
        dataset=request.session['vt_dataset']
        x_keep=find_src_data(file_id,dataset)
      
       
        # num_cols1 = [c for i, c in enumerate(
        #     x_keep.columns) if x_keep.dtypes[i] not in [np.object]]
        num_cols1= [c for i, c in enumerate(
             x_keep.columns) if x_keep.dtypes[i] not in [np.object]]
        # i = 1
        arrlstOutlierGrubbs = []
        # for i in range(len(num_cols1)):
        #     num_var = num_cols1[i]
        #     objlstOutlierGrubbs = lstOutlierGrubbs()
        #     # print('outlier detected for', num_var, 'the location is')
        #     objlstOutlierGrubbs.colName = num_var
        #     objlstOutlierGrubbs.min_location = grubbs.min_test_indices(
        #         x_keep[num_var], alpha=.05)
        #     # print(grubbs.min_test_indices(x_keep[num_var], alpha=.05))
        #     objlstOutlierGrubbs.max_location = grubbs.max_test_indices(
        #         x_keep[num_var], alpha=.05)
        #     # print(grubbs.max_test_indices(x_keep[num_var], alpha=.05))
        #     # print('outlier detected for ', num_var, ' the values is')
        #     objlstOutlierGrubbs.min_value = grubbs.min_test_outliers(
        #         x_keep[num_var], alpha=.05)
        #     # print(grubbs.min_test_outliers(x_keep[num_var], alpha=.05))
        #     objlstOutlierGrubbs.max_value = grubbs.max_test_outliers(
        #         x_keep[num_var], alpha=.05)
        #     # print(grubbs.max_test_outliers(x_keep[num_var], alpha=.05))
        #     # print('\n')
        #     arrlstOutlierGrubbs.append(objlstOutlierGrubbs)
        #     i = i+1

        k = 1
        arrlstOutlieranomalies = []
        for k in range(len(num_cols1)):
            var = num_cols1[k]
            # print('outlier detected for', var)
            # find_anomalies(x_keep[var])
            objlstOutlieranomalies = lstOutlieranomalies()
            anomalies = []
            objlstOutlieranomalies.colName = var
            # Set upper and lower limit to 3 standard deviation
            random_data_std = np.std(x_keep[var])
            random_data_mean = np.mean(x_keep[var])
            anomaly_cut_off = random_data_std * 3

            lower_limit = random_data_mean - anomaly_cut_off
            upper_limit = random_data_mean + anomaly_cut_off
            objlstOutlieranomalies.lower_limit = lower_limit
            objlstOutlieranomalies.upper_limit = upper_limit
            # print('the lower limit is: ', lower_limit,'the upper limit is: ', upper_limit)
            # Generate outliers
            for outlier in x_keep[var]:
                if outlier > upper_limit or outlier < lower_limit:
                    anomalies.append(outlier)
        #     return anomalies
            # print(anomalies)

            objlstOutlieranomalies.arr_anomalies = len(anomalies)
            arrlstOutlieranomalies.append(objlstOutlieranomalies)
            k = k+1

        # print(arrlstOutlieranomalies)
        return render(request, 'ViewOutliers.html',  {'tableHead': 'View Outliers', 'arrlstOutlierGrubbs': arrlstOutlierGrubbs, 'arrlstOutlieranomalies': arrlstOutlieranomalies})
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def setScheduler(request):
    return render(request, 'shedular.html')


def setScheduler1(request):
    return render(request, 'shedular1.html')


def setProfile(request):
    return render(request, 'profile.html')


def evaluate_model(val_pred, val_probs, train_pred, train_probs, fileName):
    # """Compare machine learning model to baseline performance.
    # Computes statistics and shows ROC curve."""
    savefile_x_final = file_path + file_name + "_x_final.csv"
    x_final = pd.read_csv(savefile_x_final, na_values='?')
    savefile_name = file_path + file_name + ".csv"
    df = pd.read_csv(savefile_name)
    # split the dastaset into train, validation and test with the ratio 0.7, 0.2 and 0.1
    y = df['fraud_reported'].replace(('Y', 'N'), (1, 0))
    X_train, X_test, y_train, y_test = train_test_split(
        x_final, y, test_size=0.1, random_state=321)  # Predictor and target variables
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.22222222222222224, random_state=321)

    # baseline, ROC=0.5 with equal chance to classify for any randome selected target account
    baseline = {}
    baseline['recall'] = recall_score(y_val, [1 for _ in range(len(y_val))])
    baseline['precision'] = precision_score(
        y_val, [1 for _ in range(len(y_val))])
    baseline['roc'] = 0.5

    # Calculate ROC on validation dataset
    val_results = {}
    val_results['recall'] = recall_score(y_val, val_pred)
    val_results['precision'] = precision_score(y_val, val_pred)
    val_results['roc'] = roc_auc_score(y_val, val_probs)

    # Calculate ROC on training dataset
    train_results = {}
    train_results['recall'] = recall_score(y_train, train_pred)
    train_results['precision'] = precision_score(y_train, train_pred)
    train_results['roc'] = roc_auc_score(y_train, train_probs)

    for metric in ['recall', 'precision', 'roc']:
        print(
            f'{metric.capitalize()} Baseline: {round(baseline[metric], 2)} Validation: {round(val_results[metric], 2)} Training: {round(train_results[metric], 2)}')

    # Calculate false positive rates and true positive rates
    base_fpr, base_tpr, _ = roc_curve(y_val, [1 for _ in range(len(y_val))])
    model_fpr, model_tpr, _ = roc_curve(y_val, val_probs)

    plt.figure(figsize=(8, 6))
    plt.rcParams['font.size'] = 16

    # Plot both curves
    plt.plot(base_fpr, base_tpr, 'b', label='baseline')
    plt.plot(model_fpr, model_tpr, 'r', label='model')
    plt.legend()
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves')
    plt.savefig(os.path.join(
        BASE_DIR, plot_dir_view, fileName))
    plt.close()


def randomForest_defSettings_Tests(request):

    savefile_x_final = file_path + file_name + "_x_final.csv"
    x_final = pd.read_csv(savefile_x_final, na_values='?')
    savefile_name = file_path + file_name + ".csv"
    df = pd.read_csv(savefile_name)
    # split the dastaset into train, validation and test with the ratio 0.7, 0.2 and 0.1
    y = df['fraud_reported'].replace(('Y', 'N'), (1, 0))
    X_train, X_test, y_train, y_test = train_test_split(
        x_final, y, test_size=0.1, random_state=321)  # Predictor and target variables
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.22222222222222224, random_state=321)
    rf_model = RandomForestClassifier(n_estimators=100, criterion="gini",
                                      random_state=50,
                                      max_features='sqrt',
                                      n_jobs=-1, verbose=1)
    rf_model.fit(X_train, y_train)
    RandomForestClassifier(max_features='sqrt', n_jobs=-1, random_state=50,
                           verbose=1)
    # check the average of the nodes and depth.
    n_nodes = []
    max_depths = []
    for ind_tree in rf_model.estimators_:
        n_nodes.append(ind_tree.tree_.node_count)
        max_depths.append(ind_tree.tree_.max_depth)

    print(f'Average number of nodes {int(np.mean(n_nodes))}')
    print(f'Average maximum depth {int(np.mean(max_depths))}')
    # Test the model
    pred_rf_val = rf_model.predict(X_val)
    pred_rf_prob_val = rf_model.predict_proba(X_val)[:, 1]

    pred_rf_train = rf_model.predict(X_train)
    pred_rf_prob_train = rf_model.predict_proba(X_train)[:, 1]

    # Get the model performance
    print('classification report on training data')
    print(classification_report(y_train, pred_rf_train))
    print('\n')
    print('classification report on validation data')
    print(classification_report(y_val, pred_rf_val))
    evaluate_model(y_val, pred_rf_prob_val, y_train,
                   pred_rf_prob_train, "Random_Forest.png")
    # baseline, ROC=0.5 with equal chance to classify for any randome selected target account
    # show the confusion matrix for training data

    cnf_matrix = confusion_matrix(y_train, pred_rf_train, labels=[0, 1])
    sns.heatmap(pd.DataFrame(cnf_matrix), annot=True,
                cmap="YlGnBu", fmt='g')
    plt.tight_layout()
    plt.title('Confusion matrix: Training data')
    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')
    plt.savefig(os.path.join(
        BASE_DIR, 'static\media\RF_Con_mat_train_data.png'))
    plt.close()
    # show the confusion matrix for validation data

    cnf_matrix2 = confusion_matrix(y_val, pred_rf_val, labels=[0, 1])
    sns.heatmap(pd.DataFrame(cnf_matrix2), annot=True,
                cmap="YlGnBu", fmt='g')
    plt.tight_layout()
    plt.title('Confusion matrix: Validation data')
    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')
    plt.savefig(os.path.join(
        BASE_DIR, 'static\media\RF_Con_mat_val_data.png'))
    plt.close()
    context = {'graphpath':   '\static\media\Random_Forest.png',
               'graphConfMat1': '\static\media\RF_Con_mat_train_data.png', 'graphConfMat2': '\static\media\RF_Con_mat_val_data.png'}
    return render(request, 'showRandomForest.html', context)


def random_forest_tune_Paras(request):
    from sklearn.model_selection import RandomizedSearchCV
    savefile_x_final = file_path + file_name + "_x_final.csv"
    x_final = pd.read_csv(savefile_x_final, na_values='?')
    savefile_name = file_path + file_name + ".csv"
    df = pd.read_csv(savefile_name)
    # split the dastaset into train, validation and test with the ratio 0.7, 0.2 and 0.1
    y = df['fraud_reported'].replace(('Y', 'N'), (1, 0))
    X_train, X_test, y_train, y_test = train_test_split(
        x_final, y, test_size=0.1, random_state=321)  # Predictor and target variables
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.22222222222222224, random_state=321)
    # Hyperparameter grid
    param_grid = {'criterion': ['entropy', 'gini'],
                  'max_features': ['auto', 'sqrt', 'log2', None] + list(np.arange(0.5, 1, 0.1).astype('float')),
                  'max_depth': [None] + list(np.linspace(5, 200, 50).astype('float')),
                  'min_samples_leaf': list(np.linspace(2, 20, 10).astype('float')),
                  'min_samples_split': [2, 5, 7, 10, 12, 15],
                  'n_estimators': np.linspace(10, 200, 50).astype('float'),
                  'max_features': ['auto', 'sqrt', None] + list(np.arange(0.5, 1, 0.1).astype('float')),
                  'max_leaf_nodes': [None] + list(np.linspace(10, 50, 500).astype('float')),
                  'bootstrap': [True, False]
                  }

    # Estimator for use in random search
    model = RandomForestClassifier()

    # Create the random search model
    rs_search = RandomizedSearchCV(model, param_grid, n_jobs=-1,
                                   scoring='roc_auc', cv=10,
                                   n_iter=100, verbose=1, random_state=50)

    # Fit
    rs_search.fit(X_train, y_train)
    return render(request, 'profile.html')


def XGBoost_Model(request):
    savefile_x_final = file_path + file_name + "_x_final.csv"
    x_final = pd.read_csv(savefile_x_final, na_values='?')
    savefile_name = file_path + file_name + ".csv"
    df = pd.read_csv(savefile_name)
    # split the dastaset into train, validation and test with the ratio 0.7, 0.2 and 0.1
    y = df['fraud_reported'].replace(('Y', 'N'), (1, 0))
    X_train, X_test, y_train, y_test = train_test_split(
        x_final, y, test_size=0.1, random_state=321)  # Predictor and target variables
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.22222222222222224, random_state=321)

    # Fit XGRegressor to the Training set
    xg_clf = xgb.XGBClassifier(objective='binary:logistic', colsample_bytree=0.3,
                               learning_rate=0.01, max_depth=5, reg_lambda=10, n_estimators=1000)
    xg_clf.fit(X_train, y_train)
    pred_xgb_val = xg_clf.predict(X_val)
    pred_xgb_prob_val = xg_clf.predict_proba(X_val)[:, 1]

    pred_xgb_train = xg_clf.predict(X_train)
    pred_xgb_prob_train = xg_clf.predict_proba(X_train)[:, 1]

    # Get the model performance
    print(classification_report(y_train, pred_xgb_train))
    print(classification_report(y_val, pred_xgb_val))
    evaluate_model(pred_xgb_val, pred_xgb_prob_val,
                   pred_xgb_train, pred_xgb_prob_train, "XGBoost.png")
    cnf_matrix = confusion_matrix(y_train, pred_xgb_train, labels=[0, 1])

    sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu", fmt='g')
    plt.tight_layout()
    plt.title('Confusion matrix: Training data')
    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')
    plt.savefig(os.path.join(
        BASE_DIR, 'static\media\XGBoost_Con_mat_train_data.png'))
    plt.close()

    cnf_matrix = confusion_matrix(y_val, pred_xgb_val, labels=[0, 1])
    sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu", fmt='g')
    plt.tight_layout()
    plt.title('Confusion matrix: Training data')
    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')
    plt.savefig(os.path.join(
        BASE_DIR, 'static\media\XGBoost_Con_mat_val_data.png'))
    plt.close()

    context = {'graphpath':   '\static\media\XGBoost.png',
               'graphConfMat1': '\static\media\XGBoost_Con_mat_train_data.png',
               'graphConfMat2': '\static\media\XGBoost_Con_mat_val_data.png'}
    return render(request, 'showRandomForest.html', context)


def XGBoost_Optimization_RS(request):
    savefile_x_final = file_path + file_name + "_x_final.csv"
    x_final = pd.read_csv(savefile_x_final, na_values='?')
    savefile_name = file_path + file_name + ".csv"
    df = pd.read_csv(savefile_name)
    # split the dastaset into train, validation and test with the ratio 0.7, 0.2 and 0.1
    y = df['fraud_reported'].replace(('Y', 'N'), (1, 0))
    X_train, X_test, y_train, y_test = train_test_split(
        x_final, y, test_size=0.1, random_state=321)  # Predictor and target variables
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.22222222222222224, random_state=321)

    parameters = {'objective': ['binary:logistic'],
                  'colsample_bytree': [0.3, 0.5, 0.7, 0.9],
                  'learning_rate': [0.001, 0.003, 0.005, 0.007, 0.009, 0.01, 0.03, 0.05,  0.07, 0.09],
                  'max_depth': list(np.linspace(3, 20).astype(int)),
                  'lambda': list(np.linspace(3, 10).astype(int)),
                  'n_estimators': [100, 200, 500, 700, 1000],
                  'missing': [-999],
                  'seed': [1337]}

    # Estimator for use in random search
    estimator = xgb.XGBClassifier(random_state=50)

    # Create the random search model
    xgb_random = RandomizedSearchCV(estimator, parameters, n_jobs=-1,
                                    scoring='roc_auc', cv=10,
                                    n_iter=100, verbose=1, random_state=50)

    # Fit
    xgb_random.fit(X_train, y_train)
    xgb_random.best_params_

    parameters = {'objective': ['binary:logistic'],
                  'colsample_bytree':  [0.9],
                  'learning_rate':  [0.006],
                  'max_depth': [5],
                  'lambda': [8],
                  'n_estimators': [1000],
                  'missing': [-999],
                  'seed': [1337]}

    # Estimator for use in random search
    estimator = xgb.XGBClassifier(random_state=50)

    # Create the random search model
    xgb_grid = GridSearchCV(estimator, parameters, n_jobs=-1,
                            scoring='roc_auc', cv=10, verbose=1)

    # Fit
    xgb_grid.fit(X_train, y_train)
    xgb_grid.best_params_

    best_model_xgb = xgb_grid.best_estimator_
    best_model_xgb

    # Test the model
    pred_xgb_val1 = best_model_xgb.predict(X_val)
    pred_xgb_prob_val1 = best_model_xgb.predict_proba(X_val)[:, 1]

    pred_xgb_train1 = best_model_xgb.predict(X_train)
    pred_xgb_prob_train1 = best_model_xgb.predict_proba(X_train)[:, 1]

    # Get the model performance
    print(classification_report(y_train, pred_xgb_train1))
    print(classification_report(y_val, pred_xgb_val1))

    evaluate_model(y_val, pred_xgb_prob_val1, y_train,
                   pred_xgb_prob_train1, "XGBoost_Opt_RS.png")

    cnf_matrix = confusion_matrix(y_train, pred_xgb_train1, labels=[0, 1])
    sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu", fmt='g')
    plt.tight_layout()
    plt.title('Confusion matrix: Training data')
    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')
    plt.savefig(os.path.join(
        BASE_DIR, 'static\media\XGBoost_Opt_RS_Con_mat_train_data.png'))
    plt.close()

    cnf_matrix = confusion_matrix(y_val, pred_xgb_val1, labels=[0, 1])
    sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu", fmt='g')
    plt.tight_layout()
    plt.title('Confusion matrix: Training data')
    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')
    plt.savefig(os.path.join(
        BASE_DIR, 'static\media\XGBoost_Opt_RS_Con_mat_train_data.png'))
    plt.close()

    context = {'graphpath':   '\static\media\XGBoost_Opt_RS.png',
               'graphConfMat1': '\static\media\XGBoost_Opt_RS_Con_mat_train_data.png',
               'graphConfMat2': '\static\media\XGBoost_Con_mat_val_data.png'}
    return render(request, 'showRandomForest.html', context)


def getTargetColVals(request):
    print("getTargetColVals")
    target = request.GET['colName']
    print('colName ', target)
    file_id=request.GET['file_id']
    print('file_id ', file_id)
    dataset=request.session['vt_dataset']
    dataframe=find_src_data(file_id,dataset) 
    # filtered_column_data=dataframe.loc[:,str(target)]
    # print("filtered_column_data",type(filtered_column_data))

    # df1_list=list(filtered_column_data)        
    # print("filtered_column_data",df1_list)
    # x=np.array(df1_list)
    # print(np.unique(x))
    # unique_list=list(np.unique(x))
    # print("unique_list",unique_list)
    # # print(type(unique_list))
    # # print("unique_list",unique_list)
    # df = pd.DataFrame(unique_list)
    # # result=df.to_dict('record')
    # print("df is",df)
    # result=df.to_json(orient='index')
    # result = json.loads(result)
    # print('result ', result)
    # result_dict={}
    # for i in result:
    #     print("i",i)
    #     for key,val in i.items():
    #         result_dict.update({key:val})
    # print("result_dict",result_dict)        

    # # savefile_withoutnull = file_path + file_name + "_withoutnull.csv"
    # savefile_withoutnull = file_path + file_name + ".csv"
    # df = pd.read_csv(savefile_withoutnull, na_values='?')
    # target = request.GET['colName']
    # # print('colName ', target)
    count_target = dataframe[target].value_counts()
    # print(count_target)
    # print('missing value is:', len(df[target])-df[target].count())
    print('count_target is ',count_target)
    result = count_target.to_json(orient='index')
    result = json.loads(result)
    print('result ', result)
    data = {
        'ctData':result # unique_list
    }
    print("data",data)
    return JsonResponse(data)


def updateData(request):
    print("updateData")
    try:
        _isDisabled="disabled"
        file_id=find_max_file_id(request.session['vt_mdl'])
         
        src_file_obj = collection_file_info.find_one({'file_id':int(file_id)})
        
        column_data= src_file_obj['file_columns'][0]  
        gridDttypes=[]
        idx=0  
        for j in column_data:
            print("j is ",j,idx)
            gridDttypes.append({'colName': j,  'idx':str(idx)})
            idx=idx+1 
        _isDisabled="" 
      
        
 
         

        return render(request, 'updateData.html', {'dataTypes': gridDttypes,'isDisabled':_isDisabled,'file_id':file_id})
    except Exception as e:
        print(e)
        return render(request, 'error.html')

def skipUpdateData(request):
    try:
        content = request.GET['name']
        print('form name is ',content)
        if(content=='targetVar'):
            processing = os.path.join(BASE_DIR, processingFile_path)
            df_old_proc = pd.read_csv(processing)
            df_old_proc.loc[df_old_proc.Idx == 3, "Status"] = "Done"
            df_old_proc.to_csv(processing, index=False, encoding='utf-8')
            del df_old_proc
            # savefile_y = file_path + file_name + "_y.csv"
            # y.to_csv(savefile_y, index=False, encoding='utf-8')
            targetVar = file_path + file_name + "_targetVar.txt"
            if os.path.exists(targetVar):
                file1 = open(targetVar, "w")  # write mode
                file1.write("None")
                file1.close()
            else:
                file1 = open(targetVar, "w+")  # write mode
                file1.write("None")
                file1.close()
            savefile  =  file_path + file_name + ".csv"
            df = pd.read_csv(savefile, na_values='?')           
            savefile_x = file_path + file_name + "_x.csv"
            df.to_csv(savefile_x, index=False)
            return redirect('updateData')
        elif(content=='missingvals'):
            processing = os.path.join(BASE_DIR, processingFile_path)
            df_old_proc = pd.read_csv(processing)
            df_old_proc.loc[df_old_proc.Idx == 4, "Status"] = "Done"
            df_old_proc.to_csv(processing, index=False)
            del df_old_proc
            return redirect('viewDataType')
        elif(content=='dropfeatures'):
             
            processing = os.path.join(BASE_DIR, processingFile_path)
            df_old_proc = pd.read_csv(processing)
            df_old_proc.loc[df_old_proc.Idx == 5, "Status"] = "Done"
            df_old_proc.to_csv(processing, index=False, encoding='utf-8')
            del df_old_proc
            return redirect('dropfeatures')
        elif(content=='dummy_var'):
            savefile_x = file_path + file_name + "_x.csv"
            df = pd.read_csv(savefile_x, na_values='?')           
            savefile_x_keep = file_path + file_name + "_x_keep.csv"
            df.to_csv(savefile_x_keep, index=False)
            processing = os.path.join(BASE_DIR, processingFile_path)
            df_old_proc = pd.read_csv(processing)
            df_old_proc.loc[df_old_proc.Idx == 6, "Status"] = "Done"
            df_old_proc.to_csv(processing, index=False)
            del df_old_proc
            return redirect('dummy_vars')     
        elif(content=='renameCols'):
            savefile_x_scaled = file_path + file_name + "_x_scaled.csv"
            if os.path.exists(savefile_x_scaled):
                df = pd.read_csv(savefile_x_scaled, na_values='?')               
                savefile_x_final = file_path + file_name + "_x_final.csv"
                df.to_csv(savefile_x_final, index=False)
                processing = os.path.join(BASE_DIR, processingFile_path)
                df_old_proc = pd.read_csv(processing)
                df_old_proc.loc[df_old_proc.Idx == 9, "Status"] = "Done"
                df_old_proc.to_csv(processing, index=False)
                del df_old_proc,df
            return redirect('renameCols')    
        elif(content=='resample'):
            processing = os.path.join(BASE_DIR, processingFile_path)
            df_old_proc = pd.read_csv(processing)
            df_old_proc.loc[df_old_proc.Idx == 10, "Status"] = "Done"
            df_old_proc.to_csv(processing, index=False)
            del df_old_proc
            return redirect('resample')                   
        else:
            return render(request, 'error.html')
    except Exception as e:
        print(e)
        print('traceback is ',traceback.print_exc())
        return render(request, 'error.html')

def getUpdatedColVals(request):
    print("getUpdatedColVals")
    target = request.GET['colName']
    print('colName ', target)
    file_id=request.GET['file_id']
    print('file_id ', file_id)

    dataset=request.session['vt_dataset']
    dataframe=find_src_data(file_id,dataset)
    count_target = dataframe[target].value_counts()
    result = count_target.to_json(orient='index')
    result = json.loads(result)
    # print('result ', result)
    data = {
        'ctData': result
    }
    return JsonResponse(data)


def updateColData(request):
    print("updateColData")
    column_name_get = request.GET['delcolList']
    updated_column = request.GET['colDataLst']
    file_id=find_max_file_id(request.session['vt_mdl'])
    dataset=request.session['vt_dataset']
    df=find_src_data(file_id,dataset)          
    column_name =  column_name_get 
    parsed_obj = json.loads(updated_column)
    dict_obj={} 
    for i in parsed_obj:
        for key,val in i.items():
            #print("key value",key,val)
            dict_obj.update({key:val})   
      
    class Data_SRC:
        def storing_src(self):
         
            src_obj=collection.find_one({'file_id':int(file_id)})
            for k,v in dict_obj.items():
                print("key value",column_name,k,v,df[column_name].dtypes)

                if k and v:
                     
                    print(column_name, type(src_obj[column_name]).__name__, (type(src_obj[column_name]).__name__=="bool"))
                    if df[column_name].dtypes=="int64":
                        print('inside int')
                        myquery = { column_name: int(k),'file_id':int(file_id) }
                    elif df[column_name].dtypes=="float64":
                         print('inside float')                       
                         myquery = { column_name: float(k),'file_id':int(file_id) }
                    elif df[column_name].dtypes=="bool" or  (type(src_obj[column_name]).__name__=="bool"):
                        print('inside bool')
                        if(str(k)=="False"):
                            k=False
                        elif(str(k)=="True"):
                            k=True
                        myquery = { column_name: k,'file_id':int(file_id) }
                    else:
                        print('inside default')
                        myquery = { column_name: k,'file_id':int(file_id) }
                    newvalues = { "$set": { column_name: v } }
                    print("myquery",myquery)
                    print("newvalues",newvalues)

                    collection.update_many(myquery, newvalues)
                    print("Update")
            return True
    
     
            
    src_obj=Data_SRC()
    src_obj.storing_src()     
    data = {
        'is_taken': True
    }
    return JsonResponse(data)


def renameCols(request):
    try:
        savefile_withoutnull = file_path + file_name + "_x_final.csv"
        if(not os.path.exists(savefile_withoutnull)):
            return render(request, 'processNotdone.html')
        gridDttypes = []

        if os.path.exists(savefile_withoutnull):
            df = pd.read_csv(savefile_withoutnull, na_values='?')
            dttypes = dict(df.dtypes)
            # print(dttypes)
            irow = 1
            for key, value in dttypes.items():
                gridDttypes.append({'colName': key, 'irow': irow})
                irow = irow + 1
        return render(request, 'renameCols.html', {'dataTypes': gridDttypes})
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def renameColNames(request):
    # savefile_withoutnull = file_path + file_name + "_withoutnull.csv"
    savefile_withoutnull = file_path + file_name + "_x_final.csv"
    df = pd.read_csv(savefile_withoutnull, na_values='?')
    colDataLst = request.GET['colDataLst']
    json_colDataLst = json.loads(colDataLst)
    # print(json_colDataLst)

    colLst = []
    valLst = []
    for colval in json_colDataLst:
        for attribute, value in colval.items():
            print(attribute, value)
            if(value != ""):
                df = df.rename(columns={attribute: value})

    savefile_x = file_path + file_name + "_x_final.csv"
    df.to_csv(savefile_x, index=False)
    processing = os.path.join(BASE_DIR, processingFile_path)
    df_old_proc = pd.read_csv(processing)
    df_old_proc.loc[df_old_proc.Idx == 10, "Status"] = "Done"
    df_old_proc.to_csv(processing, index=False)
    del df_old_proc
    data = {
        'is_taken': True
    }
    return JsonResponse(data)


def showTargetColFreq(request):
    try:
        csvfile = file_path + file_name + "_x_final.csv"
        if(not os.path.exists(csvfile)):
            return render(request, 'processNotdone.html')
        gridDttypes = []
        _isDisabled="disabled"
        if os.path.exists(csvfile):
            df = pd.read_csv(csvfile, na_values='?')

            targetVarFile = file_path + file_name + "_targetVar.txt"
            file1 = open(targetVarFile, "r")  # write mode
            targetVar = file1.read()
            file1.close()
            if not(targetVar=="None"):
                x_categori = df
                # for col in x_categori.columns:
                objlstColFreq = lstColFreq()
                col_count = x_categori[targetVar].value_counts()
                objlstColFreq.colName = targetVar
                objlstColFreq.freqVal = dict(col_count)
                objlstColFreq.total_rows = x_categori[targetVar].count()
                objlstColFreq.missing_rows = len(
                    x_categori[targetVar])-x_categori[targetVar].count()
                gridDttypes.append(objlstColFreq)
        savefile_withoutnull = file_path + file_name + "_x_model.csv"
        if os.path.exists(savefile_withoutnull):
            _isDisabled=""
        return render(request, 'resamplingData.html', {'isDisabled':_isDisabled,'dataTypes': gridDttypes})
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def resamplingData(request):
    csvfile = file_path + file_name + "_x_final.csv"
    df = pd.read_csv(csvfile, na_values='?')
    targetVarFile = file_path + file_name + "_targetVar.txt"
    file1 = open(targetVarFile, "r")  # write mode
    targetVar = file1.read()
    file1.close()
    content = request.GET['dataPerc']
    json_dictionary = json.loads(content)
    df_new = pd.DataFrame()

    for colval in json_dictionary:
        for attribute, value in colval.items():
            colName = attribute
            df_sampl = df[(df[targetVar] == int(colName))].sample(frac=value)
            df_new = pd.concat(
                [df_new, df_sampl], axis=0)

    savefile_withoutnull = file_path + file_name + "_x_model.csv"
    df_new.to_csv(savefile_withoutnull, index=False)
    processing = os.path.join(BASE_DIR, processingFile_path)
    df_old_proc = pd.read_csv(processing)
    df_old_proc.loc[df_old_proc.Idx == 11, "Status"] = "Done"
    df_old_proc.loc[df_old_proc.Idx == 10, "Status"] = "Done"
    df_old_proc.to_csv(processing, index=False)
    del df_old_proc
    data = {
        'is_taken': True
    }
    return JsonResponse(data)


def confirmSrc(request):
    try:
        file_id=find_max_file_id(request.session['vt_mdl'])    
        dataset=request.session['vt_dataset'] 
        df=find_src_data(file_id,dataset) 
        
        result= df.columns.tolist()   
        print(result)
        cnfirm_obj = collection_confirm_data_source.find({'Mdl_Id':request.session['vt_mdl']})
        # dfresp =  pd.DataFrame(list(cnfirm_obj))
        resultresp=list()
        for i in cnfirm_obj:
            print("i",i)
            resultresp.append(i)
        return render(request, 'confirmSource3.html', {'dfresp':resultresp,'txtList': result, 'emailLst': getEmails(),'occpae32' : "/static/reportTemplates/pub-ch-model-risk.pdf#page=32&zoom=100,0,400"})
    except Exception as e:
        print(e, traceback.print_exc())
        return render(request, 'error.html')

def sendCnfrmMail(request):
    emailId = request.GET['emailId']
    colName = request.GET['colName']
    print('srcName', colName, 'emailId', emailId)

    cnfrmsrc_file_path = os.path.join(BASE_DIR, src_files)
    cnfrmsrc_file_name = "cnfrmsrc_"+user_name
    cnfrmsrcFiles = cnfrmsrc_file_path + cnfrmsrc_file_name + ".csv"
    if os.path.exists(cnfrmsrcFiles):
        df_old = pd.read_csv(cnfrmsrcFiles)
        if (df_old["colName"] == colName).any():
            print('already exists')
        else:
            maxid = df_old["reqID"].max()+1
            data = [['-', colName, emailId, maxid, '-', '-']]
            df_new = pd.DataFrame(
                data, columns=['srcName', 'colName', 'emailId', 'reqID', 'dataQuality', 'comment'])
            df = pd.concat([df_old, df_new], axis=0)
            df.to_csv(cnfrmsrcFiles, index=False)
        sendGMail(emailId, maxid)
    else:
        data = [['-', colName, emailId, '1', '-', '-']]
        df = pd.DataFrame(
            data, columns=['srcName', 'colName', 'emailId', 'reqID', 'dataQuality', 'comment'])
        df.to_csv(cnfrmsrcFiles, index=False)
        sendGMail(emailId, '1')
    data = {
        'is_taken': True
    }
    return JsonResponse(data)

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


def sendCnfrmMail2(request):
    print("sendCnfrmMail2")
    emailId = request.GET['emailId']
    colNamearr = request.GET['colName']
    json_dictionary = json.loads(colNamearr)
    print("json_dictionary",json_dictionary)

    request_id=request.session['vt_mdl']
    print("emailId",emailId)
    collection_confirm_data_source
    
    

    for colval in json_dictionary:
        for attribute, value in colval.items():
            colName = value
            print('colName ', colName)

            ds_id=find_max_ds_id(request.session['vt_mdl'])
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
    
    # cnfirm_obj={"reqId":int(request_id),"EmailId":emailId,"ds_id":int(ds_id),"ColName":colName}
    # myquery={'impCtrl_id':int(impCtrl_id)}

    # cnfrmsrc_file_path = os.path.join(BASE_DIR, src_files)
    # cnfrmsrc_file_name = "cnfrmsrc_"+user_name
    # cnfrmsrcFiles = cnfrmsrc_file_path + cnfrmsrc_file_name + ".csv"
    # if os.path.exists(cnfrmsrcFiles):
    #     for colval in json_dictionary:
    #         for attribute, value in colval.items():
    #             df_old = pd.read_csv(cnfrmsrcFiles)
    #             maxid = df_old["reqID"].max()+1
    #             colName = value
    #             if (df_old["colName"] == colName).any():
    #                 print('already exists')
    #             else:
    #                 data = [['-', colName, emailId, maxid, '-', '-', '-']]
    #                 df_new = pd.DataFrame(
    #                     data, columns=['srcName', 'colName', 'emailId', 'reqID', 'reqRessepon', 'dataQuality', 'comment'])
    #                 df = pd.concat([df_old, df_new], axis=0)
    #                 df.to_csv(cnfrmsrcFiles, index=False)
    #                 sendGMail(emailId, maxid)
    #                 maxid += 1
    # else:
    #     maxid = 1
    #     for colval in json_dictionary:
    #         for attribute, value in colval.items():
    #             colName = value
    #             if os.path.exists(cnfrmsrcFiles):
    #                 df_old = pd.read_csv(cnfrmsrcFiles)
    #                 data = [['-', colName, emailId, maxid, '-', '-', '-']]
    #                 df_new = pd.DataFrame(
    #                     data, columns=['srcName', 'colName', 'emailId', 'reqID', 'reqRessepon', 'dataQuality', 'comment'])
    #                 df = pd.concat([df_old, df_new], axis=0)
    #                 df.to_csv(cnfrmsrcFiles, index=False)
    #                 sendGMail(emailId, maxid)
    #                 maxid += 1
    #             else:
    #                 data = [['-', colName, emailId, maxid, '-', '-', '-']]
    #                 df = pd.DataFrame(
    #                     data, columns=['srcName', 'colName', 'emailId', 'reqID', 'reqRessepon', 'dataQuality', 'comment'])
    #                 df.to_csv(cnfrmsrcFiles, index=False)
    #                 sendGMail(emailId, maxid)
    #                 maxid += 1

    data = {
        'is_taken': True
    }
    return JsonResponse(data)

def find_max_title_idx():
    print("find_max_cs_id")
    cs_obj = collection_conceptual_soundness.find()
    df =  pd.DataFrame(list(cs_obj))
    print("dataframe is ",df)
    if df.empty:
        print('DataFrame is empty!')
        TitleIdx=0
        return TitleIdx
    else:
        print("dataframe max is",df['TitleIdx'].max())    
        TitleIdx=df['TitleIdx'].max()
        return TitleIdx
    
def getSubTitleCS(request):
    print("getSubTitleCS")
    title = request.GET['title']
    titleTxt = request.GET['titleTxt']
    print("title",title)
    print("titleTxt",titleTxt)
    # titleIdx=find_max_title_idx()
    #print("titleIdx",titleIdx)
    myquery = { "Title": titleTxt}
    mydoc = collection_conceptual_soundness.find(myquery)
    if collection_conceptual_soundness.find_one(myquery):
        print("update")
        for i in mydoc:
            print("TitleIdx",i['TitleIdx'])
            titleIdx=i['TitleIdx'] -1
            print("titleidx",titleIdx)
    else:
        print("else")
        titleIdx=find_max_title_idx()         
        print("titleidx",titleIdx) 
    # data = {}
    # report_file_path = os.path.join(BASE_DIR, 'static/csv_files/')
    # report_file_name = "CS_"+user_name
    # cnfrmsrcFiles = report_file_path + report_file_name + ".csv"
    # titleIdx = 0
    # if os.path.exists(cnfrmsrcFiles):
    #     df = pd.read_csv(cnfrmsrcFiles, encoding='utf-8')
    #     dffilter = df.query("title == '" + titleTxt + "'")
    #     if(len(dffilter) > 0):
    #         titleIdx = dffilter["titleIdx"].max()-1
    #     else:
    #         titleIdx = df["titleIdx"].max()
    #     del dffilter, df
    #     print('titleIdx ', titleIdx)
    #     titleIdx = str(titleIdx)

    data = {'titleIdx': int(titleIdx)}
    return JsonResponse(data)

def find_max_title_idx_DI():
    print("find_max_title_idx_DI")
    di_obj = collection_data_integrity.find()
    df =  pd.DataFrame(list(di_obj))
    print("dataframe is ",df)
    if df.empty:
        print('DataFrame is empty!')
        TitleIdx=0
        return TitleIdx
    else:
        print("dataframe max is",df['TitleIdx'].max())    
        TitleIdx=df['TitleIdx'].max()
        return TitleIdx


def getSubTitleDI(request):
    print("getSubTitleDI")
    title = request.GET['title']
    titleTxt = request.GET['titleTxt']
    print("title",title)
    print("titleTxt",titleTxt)
    myquery = { "Title": titleTxt}

    mydoc = collection_data_integrity.find(myquery)
    if collection_data_integrity.find_one(myquery):
        print("update")
        for i in mydoc:
            print("TitleIdx",i['TitleIdx'])
            titleIdx=i['TitleIdx'] -1
            print("titleidx",titleIdx)
    else:
        print("else")
        titleIdx=find_max_title_idx_DI()         
        print("titleidx",titleIdx) 
    # data = {}
    # report_file_path = os.path.join(BASE_DIR, 'static/csv_files/')
    # report_file_name = "DI_"+user_name
    # cnfrmsrcFiles = report_file_path + report_file_name + ".csv"
    # titleIdx = 0
    # if os.path.exists(cnfrmsrcFiles):
    #     df = pd.read_csv(cnfrmsrcFiles, encoding='utf-8')
    #     dffilter = df.query("title == '" + titleTxt + "'")
    #     if(len(dffilter) > 0):
    #         titleIdx = dffilter["titleIdx"].max()-1
    #     else:
    #         titleIdx = df["titleIdx"].max()
    #     del dffilter, df
    #     print('titleIdx ', titleIdx)
    #     titleIdx = str(titleIdx)

    data = {'titleIdx': int(titleIdx)}
    return JsonResponse(data)


def getSubTitle(request):
    title = request.GET['title']
    titleTxt = request.GET['titleTxt']
    data = {}
    report_file_path = os.path.join(BASE_DIR, plot_dir_view)
    report_file_name = "temp_report_"+user_name
    cnfrmsrcFiles = report_file_path + report_file_name + ".csv"

    report_file_name = "report_"+user_name
    savedReport = report_file_path + report_file_name + ".csv"
    if(os.path.exists(savedReport)):
        cnfrmsrcFiles = savedReport
    newSubTitles=[]
    titleIdx = 0
    comment = ""
    if os.path.exists(cnfrmsrcFiles):
        df = pd.read_csv(cnfrmsrcFiles, encoding='utf-8')
        # print('titleTxt is ',titleTxt)
        dffilter = df.query("title == '" + titleTxt + "' ") #and subtitleIdx==0
        # print('dffilter ', dffilter, len(dffilter))
        # print('df ', df, len(df))
        if(len(dffilter) > 0):
            titleIdx = dffilter["titleIdx"].max()-1
            df_sorted = dffilter.sort_values(
                by=['titleIdx', 'subtitleIdx', 'subsubtitleIdx', 'reqID'], ascending=True)
            print('df_sorted ', df_sorted["subtitleIdx"])
            for index, row in df_sorted.iterrows():
                if row["section"] == "Comment":                    
                    if(str(row["subtitleIdx"])=="0.0"):
                        comment = comment+str(row["comment"])+"\n"
                    if not (str(row["subtitle"])=="nan"):
                        newSubTitles.append(str(row["subtitle"]))
            del df_sorted
            print(' comment is ', comment)
        else:
            if(len(df) > 0):
                titleIdx = df["titleIdx"].max()
        del dffilter, df
        print('main titleIdx ', titleIdx)
        titleIdx = str(titleIdx)
    exeSumm = ['Model Purpose and Use',
               'Model Description',
               'Model Risk Tier',
               'Validation Scope and Approach',
               'Validation Outcome',
               'Validation Findings']
    if(titleTxt == "Executive Summary"):
        difference_1=[]
        difference_1 = list(set(newSubTitles).difference(set(exeSumm))) 
        print('exeSumm+difference_1',exeSumm,difference_1)
        data = {'subTtl':exeSumm+difference_1, 'titleIdx': titleIdx, 'savedComments': comment}   
        
    elif(title == "-1"):
        data = {'subTtl': [], 'titleIdx': titleIdx, 'savedComments': comment}
    elif(titleTxt == "Model Assessment"):
        subTtlLst=['Development Overview', 'Development Documentation',
                           'Input and Data Integrity', 'Conceptual Soundness']
        difference_1=[]
        difference_1 = list(set(newSubTitles).difference(set(subTtlLst))) 
        data = {'subTtl':subTtlLst+difference_1, 'titleIdx': titleIdx, 'savedComments': comment}    
    elif(titleTxt == "Model Performance & Testing"):
        subTtlLst=['Model Diagnostic Testing', 'Outcome Analysis / Back-testing',
                           'Benchmarking', 'Sensitivity, Stability, and Robustness']
        difference_1=[]
        difference_1 = list(set(newSubTitles).difference(set(subTtlLst))) 
        data = {'subTtl':subTtlLst+difference_1, 'titleIdx': titleIdx, 'savedComments': comment}
    elif(titleTxt == "Implementation and Controls"):
        subTtlLst =  [
            'Production Platform, Data, and Code', 'Implementation Plan'] 
        difference_1=[]
        difference_1 = list(set(newSubTitles).difference(set(subTtlLst))) 
        data = {'subTtl':subTtlLst+difference_1, 'titleIdx': titleIdx, 'savedComments': comment}    
    elif(titleTxt == "Governance and Oversight"):
        subTtlLst=['Performance and Risk Monitoring', 'Change Management',
                           'Tuning and Calibration', 'Model Reference Tables']
        difference_1=[]
        difference_1 = list(set(newSubTitles).difference(set(subTtlLst))) 
        data = {'subTtl':subTtlLst+difference_1, 'titleIdx': titleIdx, 'savedComments': comment}   
    else:
        subTtlLst=[]
        difference_1=[]
        difference_1 = list(set(newSubTitles).difference(set(subTtlLst))) 
        data = {'subTtl':subTtlLst+difference_1, 'titleIdx': titleIdx, 'savedComments': comment}
    print('data is ',data)
    return JsonResponse(data)


def getSubSubTitle(request):
    title = request.GET['title']
    titleTxt = request.GET['titleTxt']
    subtitleTxt = request.GET['subtitleTxt']
    data = {}
    report_file_path = os.path.join(BASE_DIR, plot_dir_view)
    report_file_name = "temp_report_"+user_name
    cnfrmsrcFiles = report_file_path + report_file_name + ".csv"

    report_file_name1 = "report_"+user_name
    savedReport = report_file_path + report_file_name1 + ".csv"
    if(os.path.exists(savedReport)):
        cnfrmsrcFiles = savedReport
    titleIdx = 0
    newSubTitles=[]
    data={}
    comment = ""
    print('subtitleTxt ', subtitleTxt)
    print('titleTxt ', titleTxt)
    if os.path.exists(cnfrmsrcFiles):
        df = pd.read_csv(cnfrmsrcFiles, encoding='utf-8')
        print('df ', df)
        dffilter = df.query("title =='" + titleTxt +
                            "' and subtitle=='" + subtitleTxt + "' ")
        print('dffilter ', dffilter)
        if(len(dffilter) > 0):
            titleIdx = dffilter["subtitleIdx"].max()
            titleIdx = str(titleIdx).split(".")[1]
            titleIdx = int(titleIdx)-1
            df_sorted = dffilter.sort_values(
                by=['titleIdx', 'subtitleIdx', 'subsubtitleIdx', 'reqID'], ascending=True)
            print('df_sorted ', df_sorted["subsubtitleIdx"])
            for index, row in df_sorted.iterrows():
                if row["section"] == "Comment":
                    if(str(row["subsubtitleIdx"])=="0.0" or str(row["subsubtitleIdx"])=="0"):
                        comment = comment+str(row["comment"])+"\n"
                    if not (str(row["subsubtitle"])=="nan"):
                        newSubTitles.append(str(row["subsubtitle"]))
            del df_sorted
            
        else:
            dffilter = df.query("title == '" + titleTxt + "'")
            if(len(dffilter) > 0):
                titleIdx = dffilter["subtitleIdx"].max()
                if(int(titleIdx) > 0):
                    print('titleIdx is ', titleIdx)
                    titleIdx = str(titleIdx).split(".")[1]
        del dffilter, df
        print('titleIdx ', titleIdx)
        titleIdx = str(titleIdx)
    if(titleTxt == "Conceptual Soundness"):
        subTtlLst=['Methodology', 'Suitability', 'Variable Selection and Segmentation',
                              'Development Platform and Code', 'Assumptions', 'Limitations']
        difference_1=[]
        difference_1 = list(set(newSubTitles).difference(set(subTtlLst))) 
        data = {'subsubTtl':subTtlLst+difference_1, 'titleIdx': titleIdx, 'savedComments': comment}
        
    elif(titleTxt == "Input and Data Integrity"):
        subTtlLst=['Input Data Source', 'Data Transformation, Cleaning', 'Final Model Development Dataset']
        difference_1=[]
        difference_1 = list(set(newSubTitles).difference(set(subTtlLst))) 
        data = {'subsubTtl':subTtlLst+difference_1, 'titleIdx': titleIdx, 'savedComments': comment}        
    else:
        subTtlLst=[]
        difference_1=[]
        difference_1 = list(set(newSubTitles).difference(set(subTtlLst))) 
        data = {'subsubTtl':subTtlLst+difference_1, 'titleIdx': titleIdx, 'savedComments': comment}
       

    return JsonResponse(data)


def getSubSubTitleIdx(request):
    titleTxt = request.GET['titleTxt']
    subtitleTxt = request.GET['subtitleTxt']
    subsubtitleTxt = request.GET['subsubtitleTxt']
    data = {}
    report_file_path = os.path.join(BASE_DIR, plot_dir_view)
    report_file_name = "temp_report_"+user_name
    cnfrmsrcFiles = report_file_path + report_file_name + ".csv"
    report_file_name1 = "report_"+user_name
    savedReport = report_file_path + report_file_name1 + ".csv"
    if(os.path.exists(savedReport)):
        cnfrmsrcFiles = savedReport
    titleIdx = 0
    comment=""
    print('subtitleTxt ', subtitleTxt)
    print('titleTxt ', titleTxt)
    if os.path.exists(cnfrmsrcFiles):
        df = pd.read_csv(cnfrmsrcFiles, encoding='utf-8')
        dffilter = df.query("title =='" + titleTxt +
                            "' and subtitle=='" + subtitleTxt + "' and subsubtitle=='" + subsubtitleTxt + "'")
        print('subsubtitleIdx ',dffilter["subsubtitleIdx"])
        if(len(dffilter) > 0):
            titleIdx = dffilter["subsubtitleIdx"].max()
            titleIdx = str(titleIdx).split(".")[2]
            titleIdx = int(titleIdx)-1
            for index, row in dffilter.iterrows():
                if row["section"] == "Comment":
                    comment = comment+str(row["comment"])+"\n"
        else:
            dffilter = df.query("title == '" + titleTxt +
                                "'  and subtitle=='" + subtitleTxt + "'")
            if(len(dffilter) > 0):
                titleIdx = dffilter["subsubtitleIdx"].max()

                # if(int(titleIdx) > 0):
                print('titleIdx is ', titleIdx)
                titleIdx = str(titleIdx).split(".")[2]
        del dffilter, df
        titleIdx = str(titleIdx)
    print('titleIdx ', titleIdx)
    data = {'titleIdx': titleIdx ,'savedComments': comment}

    return JsonResponse(data)


def cnfrmSrc(request):
    print("cnfrmSrc")
    try:
        req_id = request.GET['srcID']
        req_id=int(req_id)
        print("req_id",req_id)
        confirm_obj=collection_confirm_data_source.find({'ds_id':int(req_id)},{'_id':0})
        result=list()
        for i in confirm_obj:  
            confirm_obj2=collection_confirm_data_source.find({'EmailId':i["EmailId"]},{'_id':0}) 
            for j in confirm_obj2:  
                result.append(j)   
        # cnfrmsrc_file_path = os.path.join(BASE_DIR, src_files)
        # cnfrmsrc_file_name = "cnfrmsrc_"+user_name
        # cnfrmsrcFiles = cnfrmsrc_file_path + cnfrmsrc_file_name + ".csv"
        # if os.path.exists(cnfrmsrcFiles):
        #     df = pd.read_csv(cnfrmsrcFiles)
        #     # df.loc[df['reqID'] == srcName]
        #     dfemail = df.query('reqID == ' + srcName)
        #     email = dfemail['emailId'].values[0]
        #     dfData = df.loc[df.emailId == email]

        #     result = dfData.to_json(orient="records")
        #     result = json.loads(result)
        #     del dfemail, dfData
        return render(request, 'confirmSourceResp2.html', {'df': result})
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def dataQuality(request):
    try:
        srcLst = []
        userResp = request.POST.get('userResp', False)
        print('userResp ', userResp)
        if userResp == False:
            userResp = "showDialog"
        cnfrmsrc_file_path = os.path.join(BASE_DIR, src_files)
        cnfrmsrc_file_name = "cnfrmsrc_"+user_name
        cnfrmsrcFiles = cnfrmsrc_file_path + cnfrmsrc_file_name + ".csv"
        if os.path.exists(cnfrmsrcFiles):
            df = pd.read_csv(cnfrmsrcFiles)
            if userResp == "Yes":
                dffilter = df.query("reqRessepon == '1'")
            elif userResp == "No":
                dffilter = df.query("reqRessepon == '0'")
            else:
                dffilter = df

            for idx, row in dffilter.iterrows():
                objlstCnfrmSrc = lstCnfrmSrc()
                objlstCnfrmSrc.colId = row['reqID']
                objlstCnfrmSrc.colName = row['colName']
                objlstCnfrmSrc.srcName = row['srcName']
                objlstCnfrmSrc.emailId = row['emailId']
                objlstCnfrmSrc.dataQlt = row['dataQuality']
                if str(row['reqRessepon']) != "-":
                    objlstCnfrmSrc.reqResp = "Yes"
                else:
                    objlstCnfrmSrc.reqResp = "-"
                srcLst.append(objlstCnfrmSrc)
        return render(request, 'dataQuality.html', {'txtList': srcLst, 'userResp': userResp})
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def updateResp(request):
    ds_id = request.GET['reqId']
    dataQlt = request.GET['dataQlt']
    src = request.GET['src']

    print("ds_id",ds_id)
    print("dataQlt",dataQlt)
    print("src",src) 

    confirm_obj = collection_confirm_data_source.find({'ds_id':int(ds_id)},{'_id':0})
    for i in confirm_obj:
        print("i",i)
        myquery=i
        # model_usage_obj['usage_id']=i['usage_id']
        # print("model_usage_obj",model_usage_obj)
        newvalues = { "$set":{'DataSource':src,'DataQuality':dataQlt,"ReqRessepon":"replied"} }
        collection_confirm_data_source.update_one(myquery, newvalues)
        for i in collection_confirm_data_source.find():
            print("updated")
 
     
    data = {
        'is_taken': True
    }
    return JsonResponse(data)


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


def saveChartViewd(chartType, xaxisval, yaxisval, imageName,vt_mdl="",user_id="",dataseg="", comments=""):
    
    data = [[chartType, xaxisval, yaxisval, imageName, comments,vt_mdl,user_id,dataseg]]
    df = pd.DataFrame(
        data, columns=['chartType', 'xaxisval', 'yaxisval', 'imageName', 'comments','Mdl_Id','user_id','data_segment'])
     
    if collection_chart_viewed.find_one({'xaxisval':xaxisval,'yaxisval':yaxisval,'Mdl_Id':vt_mdl,'user_id':int(user_id),'data_segment':dataseg,'chartType':chartType}):
        collection_chart_viewed.delete_many({'xaxisval':xaxisval,'yaxisval':yaxisval,'Mdl_Id':vt_mdl,'user_id':int(user_id),'data_segment':dataseg,'chartType':chartType})        
        collection_chart_viewed.insert_many(df.to_dict('records'))
    else:
        collection_chart_viewed.insert_many(df.to_dict('records'))
     


def saveChartComments(request):
    try:
        comments = request.GET['comments']
        chartType = request.GET['chartType']
        xaxis= request.GET['xaxisval'] 
        yaxis= request.GET['yaxisval']
        file_id=find_max_file_id(request.session['vt_mdl'])
      
        print("comments","chartType",comments,chartType)
        chartImg=request.session['vt_mdl']+'_'+chartType+'_'+xaxis+'_'+yaxis+'_'+date.today().strftime("%m.%d.%Y") +'.png'  
        chart_image_obj={'mdl_id':request.session['vt_mdl'],'chartImg':chartImg,"user_id":int(request.session['uid']),'Chart_Type':chartType,'Comments':comments}
        
        myquery = {'mdl_id':request.session['vt_mdl'],'chartImg':chartImg,"user_id":int(request.session['uid']),'Chart_Type':chartType }
        mydoc = collection_model_chart_image.find(myquery) 
        if collection_model_chart_image.find_one(myquery):
            for i in mydoc: 
                newvalues = { "$set":chart_image_obj }
                collection_model_chart_image.update_one(myquery, newvalues)
        else: 
            collection_model_chart_image.insert_one(chart_image_obj)
 
        data = {"is_taken": True}
        return JsonResponse(data)
    except Exception as e:
        print(e)
        print("error is ", traceback.print_exc())
        data = {'is_taken': False}
        return JsonResponse(data)


def saveChartImage(request):
    import shutil
    user_name="Dir_"+str(request.session['uid'])
    chartImg = request.GET['chartImg']
    chartType = request.GET['chartType'] 
    xaxis= request.GET['xaxisval'] 
    yaxis= request.GET['yaxisval']


    directory = os.path.join(BASE_DIR, plot_dir_view+user_name+'_Chartimgs')   
    chartImg=request.session['vt_mdl']+'_'+chartType+'_'+xaxis+'_'+yaxis+'_'+date.today().strftime("%m.%d.%Y") +'.png'  
    destination = plot_dir_view+user_name+'_Chartimgs/'+chartImg+'.png'
    print("destination",destination, " chartType ",chartType," xaxis ",xaxis," yaxis ",yaxis)

    if not os.path.exists(directory):
            os.makedirs(directory)

    objImg= collection_chart_viewed.find({'xaxisval':xaxis,'yaxisval':yaxis,'Mdl_Id':request.session['vt_mdl'],"user_id":int(request.session['uid']),'data_segment':request.session['vt_datasetname'],'chartType':chartType})
    dffilter =  pd.DataFrame(list(objImg))
    if len(dffilter) >0:
        print('chart saved',dffilter)          
        for index, row in dffilter.iterrows():
            print('row["imageName"]) ',row["imageName"], ',',os.path.exists(os.path.join(
                    BASE_DIR, 'static\\media\\'+row["imageName"])))
            if os.path.exists(os.path.join(
                    BASE_DIR, 'static\\media\\'+row["imageName"])):
                # Source path
                source = os.path.join(
                    BASE_DIR, 'static\\media\\'+row["imageName"])

                # Destination path
                destination = os.path.join(
                    BASE_DIR,destination)
                shutil.copyfile(source, destination)
                print("File copied successfully.")  

    destination = plot_dir_view+user_name+'_Chartimgs/'+chartImg+'.png'
    chart_image_obj={'chartType':chartType,'chartImg':chartImg,'destination':destination,'mdl_id':request.session['vt_mdl'],"user_id":int(request.session['uid']),"comments":""}
     

    myquery = {'mdl_id':request.session['vt_mdl'],'chartImg':chartImg,"user_id":int(request.session['uid']),'data_segment':request.session['vt_datasetname'],'Chart_Type':chartType }
    mydoc = collection_model_chart_image.find(myquery)
    if collection_model_chart_image.find_one(myquery):
        for i in mydoc: 
            newvalues = { "$set":chart_image_obj }
            collection_model_chart_image.update_one(myquery, newvalues)
    else: 
        collection_model_chart_image.insert_one(chart_image_obj)
         
     
    data = {"is_taken": True}
    return JsonResponse(data)


def saveHeatmapImage():
    import shutil
    chartImg = "Heatmap"
    chartType = "Heatmap"
    UserChartFile = file_path + "_Chartimg.csv"
    UserCommentsFiles = file_path + "_ChartViewd.csv"
    directory = os.path.join(BASE_DIR, plot_dir_view+user_name+'Chartimgs')

    if os.path.exists(UserChartFile):
        df2 = pd.read_csv(UserChartFile)
        df = pd.read_csv(UserCommentsFiles)

        if not os.path.exists(directory):
            os.makedirs(directory)
            if (df2["chartType"] == chartType).any():
                df2.loc[df.chartType ==
                        chartType, "chartImg"] = chartImg
                destination = plot_dir_view+user_name+'Chartimgs/'+chartImg+'.png'
                df2.loc[df.chartType ==
                        chartType, "destination"] = destination
                df2.to_csv(UserChartFile, index=False)
            else:
                dffilter = df.query("chartType== '"+chartType+"'")
                destination = plot_dir_view+user_name+'Chartimgs/'+chartImg+'.png'
                data = [[chartType, chartImg, destination,
                        dffilter["comments"].values[0]]]
                dfnew = pd.DataFrame(
                    data, columns=['chartType', 'chartImg', 'destination', 'comments'])
                dfmerged = pd.concat([df2, dfnew], axis=0)
                dfmerged.to_csv(UserChartFile, index=False, encoding='utf-8')
                del dfmerged
                del dffilter
        if (df["chartType"] == chartType).any():
            dffilter = df.query("chartType== '"+chartType+"'")
            for index, row in dffilter.iterrows():
                if os.path.exists(os.path.join(
                        BASE_DIR, plot_dir_view+row["imageName"])):
                    # Source path
                    source = os.path.join(
                        BASE_DIR, plot_dir_view+row["imageName"])

                    # Destination path
                    destination = os.path.join(
                        BASE_DIR, plot_dir_view+user_name+'Chartimgs/'+chartImg+'.png')
                    shutil.copyfile(source, destination)
                    print("File copied successfully.")
            del dffilter
        del df
        del df2
    else:
        df = pd.read_csv(UserCommentsFiles)
        dffilter = df.query("chartType== '"+chartType+"'")
        destination = plot_dir_view+user_name+'Chartimgs/'+chartImg+'.png'
        data = [[chartType, chartImg, destination,
                 dffilter["comments"].values[0]]]
        del dffilter
        dfnew = pd.DataFrame(
            data, columns=['chartType', 'chartImg', 'destination', 'comments'])
        dfnew.to_csv(UserChartFile, index=False, encoding='utf-8')
        del dfnew

        if not os.path.exists(directory):
            os.makedirs(directory)

        if (df["chartType"] == chartType).any():
            dffilter = df.query("chartType== '"+chartType+"'")
            for index, row in dffilter.iterrows():
                if os.path.exists(os.path.join(
                        BASE_DIR, plot_dir_view+row["imageName"])):
                    # Source path
                    source = os.path.join(
                        BASE_DIR, plot_dir_view+row["imageName"])

                    # Destination path
                    destination = os.path.join(
                        BASE_DIR, plot_dir_view+user_name+'Chartimgs/'+chartImg+'.png')
                    shutil.copyfile(source, destination)
                    print("File copied successfully.")
            del dffilter
    if os.path.exists(os.path.join(BASE_DIR, plot_dir_view+user_name+chartType+'.pdf')):
        print('copy and rename pdf')
        # Source path
        source = os.path.join(
            BASE_DIR, plot_dir_view+user_name+chartType+'.pdf')

        # Destination path
        destination = os.path.join(
            BASE_DIR, plot_dir_view+user_name+'Chartimgs/'+chartImg+'.pdf')
        shutil.copyfile(source, destination)
        print("PDF File copied successfully.")
    data = {"is_taken": True}
    return JsonResponse(data)


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


def impCtrl(request):
    print("impCtrl")
    try:
        cnfrmsrc_file_path = os.path.join(BASE_DIR, src_files)
        cnfrmsrc_file_name = "ImpCtrl_"+user_name
        cnfrmsrcFiles = cnfrmsrc_file_path + cnfrmsrc_file_name + ".csv"
        enableReportBtn = "True"
        arrSection = ['Conform to Enterprise Production Policy', 
                      'Parallel Runs', 
                      'User Acceptance Testing',
                      'Integration within Production Systems',
                      'Model Approval Process',
                      'Contingency plans (Backup -on-site and off-site)',                       
                      'Change Controls',
                      'IT Security (Confirm)']
        sectionType = []
        if os.path.exists(cnfrmsrcFiles):
            df = pd.read_csv(cnfrmsrcFiles)
            dfcnt = df.loc[df['reqRessepon'] != '-']
            if len(dfcnt) == 8:
                enableReportBtn = "True"
            for isec in range(len(arrSection)):
                if (dfcnt["section"] == arrSection[isec]).any():
                    sectionType.append(
                        {'secName': arrSection[isec], 'bgColor': 'green', 'color': 'white'})
                else:
                    sectionType.append(
                        {'secName': arrSection[isec], 'bgColor': 'white', 'color': 'black'})
        else:
            for isec in range(len(arrSection)):
                sectionType.append(
                    {'secName': arrSection[isec], 'bgColor': 'white', 'color': 'black'})
         
        req_id=request.session['vt_mdl']
        print("req id",req_id)
        resultDocumentation = objvalidation.getModelDocs(req_id) #collection_model_documents.find({'Mdl_Id':req_id},{'_id':0})
         
 
        #print("result",resultDocumentation)
        return render(request, 'ImpCtrl.html', {'section': '',
                                                'validatorComment': '',
                                                'reqRessepon': '-',
                                                'recpComment': '',
                                                'enableReportBtn': enableReportBtn,
                                                'arrSection': sectionType,
                                                'emailLst': getEmails(),
                                                'modelDocs': resultDocumentation,
                                                "req_id":req_id,
                                                'selectedMdl':req_id,
                                                })
    except Exception as e:
        print(e)
        print('stacktrace is ',traceback.print_exc())
        return render(request, 'error.html')


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
 
def sendImpCtrlCnfrmMail(request):
    validatorComment = request.GET['validatorComment']
    emailId = request.GET['emailId']
    section = request.GET['section']
   
    print('validatorComment', validatorComment)
    print('section', section)
    print("emailId",emailId)
    collection_model_implementation_control
    impCtrl_id=find_max_impCtrl_id()
    print("impCtrl_id",impCtrl_id)
    
    impctrl_obj={"Mdl_Id":request.session['vt_mdl'],"ValidatorComment":validatorComment,"Section":section,"EmailId":emailId,"impCtrl_id":int(impCtrl_id),'Response':"","ResponseCheck":""}
    myquery={'impCtrl_id':int(impCtrl_id)}
    if collection_model_implementation_control.find_one(myquery):
        print("if true")
        myquery = { "Mdl_Id":request.session['vt_mdl'],'Section':section}
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
    return JsonResponse(data)


def cnfrmImpCtrlResp(request):
    print("cnfrmImpCtrlResp")
    try:
        srcName = request.GET['srcID']
        print("srcName",type(srcName))
        #print("srcName",srcName[:1])
        impCtrl_id=int(srcName[:1])
        #
        print("impCtrl_id",impCtrl_id,type(impCtrl_id))
         
        impCtrl_obj=collection_model_implementation_control.find({'impCtrl_id':impCtrl_id})
        for i in impCtrl_obj:
            print("i",i)
        # cnfrmsrc_file_path = os.path.join(BASE_DIR, src_files)
        # cnfrmsrc_file_name = "ImpCtrl_"+user_name
        # cnfrmsrcFiles = cnfrmsrc_file_path + cnfrmsrc_file_name + ".csv"
        # if os.path.exists(cnfrmsrcFiles):
        #     df = pd.read_csv(cnfrmsrcFiles)
        #     # df.loc[df['reqID'] == srcName]
        #     dfemail = df.query('reqID == ' + srcName)
        #     validatorComment = dfemail['validatorComment'].values[0]
        #     section = dfemail['section'].values[0]
        section=i['Section']
        validatorComment=i['ValidatorComment']
        return render(request, 'ImpCtrlResp.html', {'section': section, 'validatorComment': validatorComment, 'srcName':impCtrl_id })
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def updateImpCtrlResp(request):
    print("updateImpCtrlResp")
    reqID = request.POST['reqId']
    Resp = request.POST['Resp']
    recpComment = request.POST['recpComment'] 

     
    impCtrl_obj = collection_model_implementation_control.find({'impCtrl_id':int(reqID)},{'_id':0})
    mdl_id=''
    sec=''
    for i in impCtrl_obj:
        print("i",i)
        myquery=i
        mdl_id=i["Mdl_Id"]
        sec=i["Section"]
        # model_usage_obj['usage_id']=i['usage_id']
        # print("model_usage_obj",model_usage_obj)
        newvalues = { "$set":{'Response':recpComment,'ResponseCheck':Resp} }
        collection_model_implementation_control.update_one(myquery, newvalues)
        for i in collection_model_implementation_control.find():
            print("updated")
    dict = {
        'Conform to Enterprise Production Policy': 8,
        'Parallel Runs':9,
        'User Acceptance Testing':10,
        'Integration within Production Systems':11,
        'Model Approval Process':12,
        'Contingency plans (Backup -on-site and off-site)':13,
        'Change Controls':14,
        'IT Security (Confirm)':15
    } 
    section = dict[sec] 
    # New Code
    if request.method == 'POST':  
        filename = request.POST.get('filenm','none')
       
        files = request.FILES
        # print("files",files)
        myfile = files.get('filename', None)
  
        if myfile != None:
            destination_path = os.path.join(BASE_DIR, 'static\\document_files\\'+mdl_id+'\\')
            objdocs=MdlDocs()
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)
            fs = FileSystemStorage()
            savefile_name = destination_path + mdl_id+'_'+filename
            if os.path.exists(savefile_name):
                os.remove(savefile_name)
            fs.save(savefile_name, myfile)
            objdocs.inserDocs(mdl_id,section,mdl_id+'_'+myfile.name,'null')

    data = {
        'is_taken': True
    }
    return JsonResponse(data)


def updateImpCtrlReportComment(request):
    print("updateImpCtrlReportComment")
    reqID = request.GET['reqId']
    reportComment = request.GET['reportComment']
    print('reqID', reqID, 'recpComment', reportComment)
    impCtrl_obj=collection_model_implementation_control.find({'Mdl_Id':(reqID)})
    df=pd.DataFrame(list(impCtrl_obj))
    impCtrl_id=df['impCtrl_id'].min()
    print("impCtrl_id",impCtrl_id)

    impctrl_comment_obj={'ReportComments':reportComment}
    myquery = { "impCtrl_id": int(impCtrl_id)}
    mydoc = collection_model_implementation_control.find(myquery)

    if collection_model_implementation_control.find_one(myquery):
        for i in mydoc:
            print("I",i['Mdl_Id'])
            newvalues = { "$set":impctrl_comment_obj }
            collection_model_implementation_control.update_one(myquery, newvalues)
            for i in collection_model_implementation_control.find():
                print("updated",i)

    # cnfrmsrc_file_path = os.path.join(BASE_DIR, src_files)
    # cnfrmsrc_file_name = "ImpCtrl_"+user_name
    # cnfrmsrcFiles = cnfrmsrc_file_path + cnfrmsrc_file_name + ".csv"
    # if os.path.exists(cnfrmsrcFiles):
    #     df_old = pd.read_csv(cnfrmsrcFiles)

    #     if (df_old.reqID.astype(str) == str(reqID)).any():
    #         df_old.loc[df_old.reqID.astype(str) == str(
    #             reqID), "reportComment"] = reportComment
    #         df_old.to_csv(cnfrmsrcFiles, index=False, encoding='utf-8')

    data = {
        'is_taken': True
    }
    return JsonResponse(data)


def getSecResp(request):
    print("getSecResp")
    section = request.GET['section']
    print("section",section)
    impCtrl_obj = collection_model_implementation_control.find({'Section': (section),'Mdl_Id':request.session['vt_mdl']},{'_id':0})
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

    return JsonResponse(data)


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



def processStatus(request):
    # savefile_withoutnull = file_path + file_name + "_withoutnull.csv"
    try:
        processing = os.path.join(BASE_DIR, processingFile_path)
        df = pd.read_csv(processing, na_values='?')

        result = df.to_json(orient="records")
        result = json.loads(result)
        del df

        return render(request, 'processStatus.html', {'df': result})
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def contacts(request):
    contactFile = file_path + user_name + "_Contacts.csv"
    data = {
        'contactLst': '',
    }
    if os.path.exists(contactFile):
        df = pd.read_csv(contactFile)
        result = df.to_json(orient="records")
        result = json.loads(result)
        data = {
            'contactLst': getEmails(),
        }
    return render(request, 'contacts.html', data)


def updateContacts(request):
    firstName = request.GET['firstName']
    lastName = request.GET['lastName']
    email = request.GET['email']
    contactIdx = request.GET['contactIdx']
    contactFile = file_path + user_name + "_Contacts.csv"
    print('contactIdx ', contactIdx)
    if os.path.exists(contactFile):
        df_old = pd.read_csv(contactFile)
        dffilter = df_old.query("contact== '"+str(contactIdx)+"'")
        if len(dffilter) > 0:
            print('email is ', email)
            df_old.loc[(df_old["contact"] ==
                       contactIdx), "firstName"] = firstName
            df_old.loc[(df_old["contact"] ==
                       contactIdx), "lastName"] = lastName
            df_old.loc[(df_old["contact"] ==
                       contactIdx), "email"] = email
            print('df_old ', df_old)
            df_old.to_csv(contactFile, index=False, encoding='utf-8')
            del df_old, dffilter
        else:
            maxidx = df_old['contactIdx'].max()+1
            data = [[maxidx, 'Con-' + str(maxidx), firstName, lastName, email]]
            df_new = pd.DataFrame(
                data, columns=['contactIdx', 'contact', 'firstName', 'lastName', 'email'])
            df = pd.concat([df_old, df_new], axis=0)
            df.to_csv(contactFile, index=False, encoding='utf-8')
            del df_old, df_new, df, dffilter

    else:
        data = [[1, 'Con-1', firstName, lastName, email]]
        df = pd.DataFrame(
            data, columns=['contactIdx', 'contact',  'firstName', 'lastName', 'email'])
        df.to_csv(contactFile, index=False, encoding='utf-8')
        del df

    if os.path.exists(contactFile):
        df = pd.read_csv(contactFile)
        result = df.to_json(orient="records")
        result = json.loads(result)
    data = {
        'paramVals': result,
        'is_taken': True
    }
    return JsonResponse(data)


def policies(request):
    data = {
        'contactLst': getPolicies(),
    }
    return render(request, 'policies.html', data)


def addRptRef(request):
    policy = request.GET['policy']
    reference = request.GET['reference']
    contactFile = file_path + user_name + "_RptRef.csv"
    maxidx = 0
    if os.path.exists(contactFile):
        df_old = pd.read_csv(contactFile)
        maxidx = df_old['Srno'].max()+1
        data = [[maxidx,  policy, reference]]
        df_new = pd.DataFrame(
            data, columns=['Srno', 'policy', 'reference'])
        df = pd.concat([df_old, df_new], axis=0)
        df.to_csv(contactFile, index=False, encoding='utf-8')
        del df_old, df_new, df
    else:
        maxidx = 1
        data = [[1, policy, reference]]
        df = pd.DataFrame(
            data, columns=['Srno', 'policy', 'reference'])
        df.to_csv(contactFile, index=False, encoding='utf-8')
        del df

    data = {
        'is_taken': True,
        'refNo': maxidx
    }
    return JsonResponse(data)


def updatePolicy(request):
    policy = request.GET['policy']
    reference = request.GET['reference']
    policyIdx = request.GET['policyIdx']
    contactFile = file_path + user_name + "_Policies.csv"
    if os.path.exists(contactFile):
        df_old = pd.read_csv(contactFile)
        dffilter = df_old.query("policyIdx== '"+str(policyIdx)+"'")
        if len(dffilter) > 0:
            df_old.loc[(df_old["policyIdx"] ==
                       policyIdx), "policy"] = policy
            df_old.loc[(df_old["policyIdx"] ==
                       policyIdx), "reference"] = reference
            print('df_old ', df_old)
            df_old.to_csv(contactFile, index=False, encoding='utf-8')
            del df_old, dffilter
        else:
            maxidx = df_old['Srno'].max()+1
            data = [[maxidx, 'Pol-' + str(maxidx), policy, reference]]
            df_new = pd.DataFrame(
                data, columns=['Srno', 'policyIdx', 'policy', 'reference'])
            df = pd.concat([df_old, df_new], axis=0)
            df.to_csv(contactFile, index=False, encoding='utf-8')
            del df_old, df_new, df, dffilter

    else:
        data = [[1, 'Pol-1', policy, reference]]
        df = pd.DataFrame(
            data, columns=['Srno', 'policyIdx',  'policy', 'reference'])
        df.to_csv(contactFile, index=False, encoding='utf-8')
        del df

    data = {
        'is_taken': True
    }
    return JsonResponse(data)


def getEmails():
    contactFile = file_path + user_name + "_Contacts.csv"
    result = {
        '': '',
    }
    if os.path.exists(contactFile):
        df = pd.read_csv(contactFile)
        result = df.to_json(orient="records")
        result = json.loads(result)

    return result


def getPolicies():
    contactFile = file_path + user_name + "_Policies.csv"
    result = {
        '': '',
    }
    if os.path.exists(contactFile):
        df = pd.read_csv(contactFile)
        result = df.to_json(orient="records")
        result = json.loads(result)

    return result


def WIP(request):
    # from inspect import getmembers, isfunction
    # functions_list = getmembers(sns, isfunction)
    # print(functions_list)
    # html = """
    #     <H1 align="center">html2fpdf</H1>
    #     <h2>Basic usage</h2>
    #     <p>You can now easily print text mixing different
    #     styles : <B>bold</B>, <I>italic</I>, <U>underlined</U>, or
    #     <B><I><U>all at once</U></I></B>!<BR>You can also insert links
    #     on text, such as <A HREF="http://www.fpdf.org">www.fpdf.org</A>,
    #     or on an image: click on the logo.<br>
    #     <center>
    #     <img src=plot_dir_view +"/user1KNN_NT_roc1.png" width="600" height="200">
    #     </center>
    #     <h3>Sample List</h3>
    #     <ul><li>option 1</li>
    #     <ol><li>option 2</li></ol>
    #     <li>option 3</li></ul>

    #     <table border="0" align="center" width="50%">
    #     <thead><tr><th width="30%">Header 1</th><th width="70%">header 2</th></tr></thead>
    #     <tbody>
    #     <tr><td>cell 1</td><td>cell 2</td></tr>
    #     <tr><td>cell 2</td><td>cell 3</td></tr>
    #     </tbody>
    #     </table>
    #     """
    # pdf = MyFPDF()
    # pdf.add_page()
    # pdf.write_html(html)
    # pdf.output(os.path.join(
    #     BASE_DIR, plot_dir_view +"/htmltest.pdf"), 'F')
    # return render(request, 'test.html')
    return render(request, 'comingsoon.html')


def testPdf(request):
    return render(request, 'userImages.html')

def getProcessDone(request):
    try:
        processing = os.path.join(BASE_DIR, 'static/reportTemplates/processing.csv')
        df_old_proc = pd.read_csv(processing)
        maxid=0
       
        dfDone=df_old_proc.loc[df_old_proc.Status == "Done"] 
        if(len(dfDone)>0): 
            maxid = dfDone["Idx"].max() 
        
        print('process maxid is ',maxid)
        del df_old_proc,dfDone
        context = {'idx':str(maxid)}
    except Exception as e:
        print(e)
        print(traceback.print_exc())
        print("Error: unable to send email")
        context = {'idx':'0'}
    return JsonResponse(context)
     

def TestHIST(request):
    try: 
        selCol = request.GET['selCol'] 
        selCol2 = request.GET['selCol2'] 
        chartType = request.GET['chartType'] 
        print('selCol ',selCol,' chartType ',chartType)
        savefile_x_keep = file_path + "labeled_"+ file_name + ".csv"
       
        x_keep = pd.read_csv(savefile_x_keep)
 
        
        plt.style.use('fivethirtyeight')
        fig = plt.figure(figsize=(10,6))
        chartName=""
        result=[]
        if(chartType=="Data"):
            x_keep=x_keep.head(1000)
            result = x_keep.to_json(orient="records")
            result = json.loads(result)
        elif(chartType=="Hist"):
            sns.countplot(x_keep[selCol], palette='spring')
            chartName='static/replicationoutput/'+file_name+'_'+selCol+'_Histogram.png'
        else:
            sns.scatterplot(data=x_keep, x=x_keep[selCol], y=x_keep[selCol2])
            chartName='static/replicationoutput/'+file_name+'_'+selCol+'_'+selCol2+'_Scattered.png'
        # chart.set_xticklabels(chart.get_xticklabels(), rotation=45 , horizontalalignment='right') 
        # plt.title('x_keep[i]', fontsize=10)
        plt.xticks(rotation=45) 
        plt.tight_layout()
        fig.savefig(os.path.join(
            BASE_DIR, chartName))

        context = {'is_taken':True,'graphpath': '/' + chartName,'csvdata':result}
        
        return JsonResponse(context)
    except Exception as e:
        print(e)
        print('traceback is ',traceback.print_exc())
        context = {'is_taken':False,'graphpath': ''}
        return JsonResponse(context)

class MyFPDF(FPDF, HTMLMixin):
    pass



# Data wrangling 
import pandas as pd 

# Array math
import numpy as np 

# Quick value count calculator
from collections import Counter


class Node: 
    """
    Class for creating the nodes for a decision tree 
    """
    def __init__(
        self, 
        Y: list,
        X: pd.DataFrame,
        min_samples_split=None,
        max_depth=None,
        depth=None,
        node_type=None,
        rule=None
    ):
        # Saving the data to the node 
        self.Y = Y 
        self.X = X

        # Saving the hyper parameters
        self.min_samples_split = min_samples_split if min_samples_split else 20
        self.max_depth = max_depth if max_depth else 5

        # Default current depth of node 
        self.depth = depth if depth else 0

        # Extracting all the features
        self.features = list(self.X.columns)

        # Type of node 
        self.node_type = node_type if node_type else 'root'

        # Rule for spliting 
        self.rule = rule if rule else ""

        # Calculating the counts of Y in the node 
        self.counts = Counter(Y)

        # Getting the GINI impurity based on the Y distribution
        self.gini_impurity = self.get_GINI()

        # Sorting the counts and saving the final prediction of the node 
        counts_sorted = list(sorted(self.counts.items(), key=lambda item: item[1]))

        # Getting the last item
        yhat = None
        if len(counts_sorted) > 0:
            yhat = counts_sorted[-1][0]

        # Saving to object attribute. This node will predict the class with the most frequent class
        self.yhat = yhat 

        # Saving the number of observations in the node 
        self.n = len(Y)

        # Initiating the left and right nodes as empty nodes
        self.left = None 
        self.right = None 

        # Default values for splits
        self.best_feature = None 
        self.best_value = None 

    @staticmethod
    def GINI_impurity(y1_count: int, y2_count: int) -> float:
        """
        Given the observations of a binary class calculate the GINI impurity
        """
        # Ensuring the correct types
        if y1_count is None:
            y1_count = 0

        if y2_count is None:
            y2_count = 0

        # Getting the total observations
        n = y1_count + y2_count
        
        # If n is 0 then we return the lowest possible gini impurity
        if n == 0:
            return 0.0

        # Getting the probability to see each of the classes
        p1 = y1_count / n
        p2 = y2_count / n
        
        # Calculating GINI 
        gini = 1 - (p1 ** 2 + p2 ** 2)
        
        # Returning the gini impurity
        return gini

    @staticmethod
    def ma(x: np.array, window: int) -> np.array:
        """
        Calculates the moving average of the given list. 
        """
        return np.convolve(x, np.ones(window), 'valid') / window

    def get_GINI(self):
        """
        Function to calculate the GINI impurity of a node 
        """
        # Getting the 0 and 1 counts
        y1_count, y2_count = self.counts.get(0, 0), self.counts.get(1, 0)

        # Getting the GINI impurity
        return self.GINI_impurity(y1_count, y2_count)

    def best_split(self) -> tuple:
        """
        Given the X features and Y targets calculates the best split 
        for a decision tree
        """
        # Creating a dataset for spliting
        df = self.X.copy()
        df['Y'] = self.Y

        # Getting the GINI impurity for the base input 
        GINI_base = self.get_GINI()

        # Finding which split yields the best GINI gain 
        max_gain = 0

        # Default best feature and split
        best_feature = None
        best_value = None

        for feature in self.features:
            # Droping missing values
            Xdf = df.dropna().sort_values(feature)

            # Sorting the values and getting the rolling average
            xmeans = self.ma(Xdf[feature].unique(), 2)

            for value in xmeans:
                # Spliting the dataset 
                left_counts = Counter(Xdf[Xdf[feature]<value]['Y'])
                right_counts = Counter(Xdf[Xdf[feature]>=value]['Y'])

                # Getting the Y distribution from the dicts
                y0_left, y1_left, y0_right, y1_right = left_counts.get(0, 0), left_counts.get(1, 0), right_counts.get(0, 0), right_counts.get(1, 0)

                # Getting the left and right gini impurities
                gini_left = self.GINI_impurity(y0_left, y1_left)
                gini_right = self.GINI_impurity(y0_right, y1_right)

                # Getting the obs count from the left and the right data splits
                n_left = y0_left + y1_left
                n_right = y0_right + y1_right

                # Calculating the weights for each of the nodes
                w_left = n_left / (n_left + n_right)
                w_right = n_right / (n_left + n_right)

                # Calculating the weighted GINI impurity
                wGINI = w_left * gini_left + w_right * gini_right

                # Calculating the GINI gain 
                GINIgain = GINI_base - wGINI

                # Checking if this is the best split so far 
                if GINIgain > max_gain:
                    best_feature = feature
                    best_value = value 

                    # Setting the best gain to the current one 
                    max_gain = GINIgain

        return (best_feature, best_value)

    def grow_tree(self):
        """
        Recursive method to create the decision tree
        """
        # Making a df from the data 
        df = self.X.copy()
        df['Y'] = self.Y

        # If there is GINI to be gained, we split further 
        if (self.depth < self.max_depth) and (self.n >= self.min_samples_split):

            # Getting the best split 
            best_feature, best_value = self.best_split()

            if best_feature is not None:
                # Saving the best split to the current node 
                self.best_feature = best_feature
                self.best_value = best_value

                # Getting the left and right nodes
                left_df, right_df = df[df[best_feature]<=best_value].copy(), df[df[best_feature]>best_value].copy()

                # Creating the left and right nodes
                left = Node(
                    left_df['Y'].values.tolist(), 
                    left_df[self.features], 
                    depth=self.depth + 1, 
                    max_depth=self.max_depth, 
                    min_samples_split=self.min_samples_split, 
                    node_type='left_node',
                    rule=f"{best_feature} <= {round(best_value, 3)}"
                    )

                self.left = left 
                self.left.grow_tree()

                right = Node(
                    right_df['Y'].values.tolist(), 
                    right_df[self.features], 
                    depth=self.depth + 1, 
                    max_depth=self.max_depth, 
                    min_samples_split=self.min_samples_split,
                    node_type='right_node',
                    rule=f"{best_feature} > {round(best_value, 3)}"
                    )

                self.right = right
                self.right.grow_tree()

    def print_info(self, width=4):
        """
        Method to print the infromation about the tree
        """
        # Defining the number of spaces 
        const = int(self.depth * width ** 1.5)
        spaces = "-" * const
        
        if self.node_type == 'root':
            print("Root")
        else:
            print(f"|{spaces} Split rule: {self.rule}")
        print(f"{' ' * const}   | GINI impurity of the node: {round(self.gini_impurity, 2)}")
        print(f"{' ' * const}   | Class distribution in the node: {dict(self.counts)}")
        print(f"{' ' * const}   | Predicted class: {self.yhat}")   

    def print_tree(self):
        """
        Prints the whole tree from the current node to the bottom
        """
        self.print_info() 
        
        if self.left is not None: 
            self.left.print_tree()
        
        if self.right is not None:
            self.right.print_tree()

    def predict(self, X:pd.DataFrame):
        """
        Batch prediction method
        """
        predictions = []

        for _, x in X.iterrows():
            values = {}
            for feature in self.features:
                values.update({feature: x[feature]})
        
            predictions.append(self.predict_obs(values))
        
        return predictions

    def predict_obs(self, values: dict) -> int:
        """
        Method to predict the class given a set of features
        """
        cur_node = self
        while cur_node.depth < cur_node.max_depth:
            # Traversing the nodes all the way to the bottom
            best_feature = cur_node.best_feature
            best_value = cur_node.best_value

            if cur_node.n < cur_node.min_samples_split:
                break 

            if (values.get(best_feature) < best_value):
                if self.left is not None:
                    cur_node = cur_node.left
            else:
                if self.right is not None:
                    cur_node = cur_node.right
            
        return cur_node.yhat

#to be changed
def saveTableInfo(request):
    try:
        tableType = request.GET['tableType']
        tableName = request.GET['tableName']
        comments = request.GET['comments']
        var1 = request.GET['var1']
        var2 = request.GET['var2']
        tblFile = file_path + user_name+"_Tables.csv"
        if os.path.exists(tblFile):
            df_old = pd.read_csv(tblFile)
            if ((df_old["tableName"] == tableName) & (df_old["tableType"] == tableType)).any():
                if(len(comments) > 0):
                    df_old.loc[(df_old["tableName"] == tableName) & (
                        df_old["tableType"] == tableType), "comments"] = comments
                df_old.to_csv(tblFile, index=False)
            else:
                data = [[tableType, tableName, comments, var1, var2]]
                df_new = pd.DataFrame(
                    data, columns=['tableType', 'tableName', 'comments', 'var1', 'var2'])
                df = pd.concat([df_old, df_new], axis=0)
                df.to_csv(tblFile, index=False)
            del df_old
        else:
            data = [[tableType, tableName, comments, var1, var2]]
            df = pd.DataFrame(
                data, columns=['tableType', 'tableName', 'comments', 'var1', 'var2'])
            df.to_csv(tblFile, index=False)
            del df
        data = {'is_taken': True}
        return JsonResponse(data)
    except Exception as e:
        print(e)
        print("error is ", traceback.print_exc())
        data = {'is_taken': False}
        return JsonResponse(data)



def getTableInfo(request):
    try:
        tableType = request.GET['tableType']
        tableName = request.GET['tableName']
        print('tableType is ', tableType)
        data = {'is_taken': False}
        if(tableType == "DataTypenCnt"):
            data = {'is_taken': True, 'tblCode': getDatatypenCnt()}
        elif (tableType == "DataDesc"):
            data = {'is_taken': True, 'tblCode': viewNumData2(tableType)}
        elif (tableType == "DataMean"):
            data = {'is_taken': True, 'tblCode': viewNumData2(tableType)}
        elif (tableType == "DataMedian"):
            data = {'is_taken': True, 'tblCode': viewNumData2(tableType)}
        elif(tableType == "NumVarDIst"):
            data = {'is_taken': True,
                    'tblCode': dist_numevari_catvar2(tableName)}
        elif(tableType == "VIFData"):
            data = {'is_taken': True,
                    'tblCode': getVIFData()}
        elif(tableType == "TarvsCat"):
            data = {'is_taken': True,
                    'tblCode': getCT(tableName)}
        elif(tableType == "ValFindings"):
            data = {'is_taken': True,
                    'tblCode': getValFindingsttbl()}
        return JsonResponse(data)
    except Exception as e:
        print(e)
        print("error is ", traceback.print_exc())
        data = {'is_taken': False}
        return JsonResponse(data)

def testTable(request):
    tableCode = '''<table border="0" color="black" width="100%">
                        <thead>
                            <tr>
                                <th align="left" width="40%">Column Name</th>
                                <th width="30%">Not-Null Count</th>
                                <th width="30%">Column Data type &nbsp;&nbsp;&nbsp;&nbsp;</th>
                            </tr>
                        </thead>
                        <tbody border="1" > <tr border="1" ><td border="1">months_as_customer</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">age</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">policy_number</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">policy_bind_date</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">policy_state</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">policy_csl</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">policy_deductable</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid
                        # eee;">policy_annual_premium</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">float64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">umbrella_limit</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">insured_zip</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">insured_sex</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">insured_education_level</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">insured_occupation</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">insured_hobbies</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">insured_relationship</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">capital-gains</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">capital-loss</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">incident_date</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">incident_type</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">collision_type</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">822 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">incident_severity</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">authorities_contacted</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">incident_state</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">incident_city</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000
                        non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">incident_location</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">incident_hour_of_the_day</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">number_of_vehicles_involved</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">property_damage</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">640 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">bodily_injuries</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">witnesses</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">police_report_available</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">657 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">total_claim_amount</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">injury_claim</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null
                        </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">property_claim</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">vehicle_claim</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px
                        5px 0px 5px;border: 1px solid #eee;">auto_make</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">auto_model</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">auto_year</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">fraud_reported</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr></tbody></table>'''

    pdf = MyFPDF()
    pdf.add_page('P')
    pdf.set_font('Arial', '', 9)
    pdf.write_html(tableCode)
    pdf.output(os.path.join(
        BASE_DIR, "static\\media\\tabletest1.pdf"))
    return JsonResponse({'data': True})


def getDatatypenCnt():
    try:
        savefile_name = file_path + file_name + ".csv"
        df = pd.read_csv(savefile_name, na_values='?')
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


def testTable(request):
    tableCode = '''<table border="0" color="black" width="100%">
                        <thead>
                            <tr>
                                <th align="left" width="40%">Column Name</th>
                                <th width="30%">Not-Null Count</th>
                                <th width="30%">Column Data type &nbsp;&nbsp;&nbsp;&nbsp;</th>
                            </tr>
                        </thead>
                        <tbody border="1" > <tr border="1" ><td border="1">months_as_customer</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">age</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">policy_number</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">policy_bind_date</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">policy_state</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">policy_csl</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">policy_deductable</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid
                        # eee;">policy_annual_premium</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">float64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">umbrella_limit</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">insured_zip</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">insured_sex</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">insured_education_level</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">insured_occupation</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">insured_hobbies</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">insured_relationship</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">capital-gains</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">capital-loss</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">incident_date</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">incident_type</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">collision_type</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">822 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">incident_severity</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">authorities_contacted</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">incident_state</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">incident_city</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000
                        non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">incident_location</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">incident_hour_of_the_day</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">number_of_vehicles_involved</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">property_damage</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">640 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">bodily_injuries</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">witnesses</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">police_report_available</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">657 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">total_claim_amount</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">injury_claim</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null
                        </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">property_claim</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">vehicle_claim</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px
                        5px 0px 5px;border: 1px solid #eee;">auto_make</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">auto_model</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">auto_year</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">int64</td></tr><tr><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">fraud_reported</td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">1000 non-null </td><td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">object</td></tr></tbody></table>'''

    pdf = MyFPDF()
    pdf.add_page('P')
    pdf.set_font('Arial', '', 9)
    pdf.write_html(tableCode)
    pdf.output(os.path.join(
        BASE_DIR, "static\\media\\tabletest1.pdf"))
    return JsonResponse({'data': True})


def viewNumData2(strType):
    from statsmodels import robust
    savefile_name = file_path + file_name + ".csv"
    df = pd.read_csv(savefile_name, na_values='?')
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


def dist_numevari_catvar2(tableName):
    tblFile = file_path + user_name+"_Tables.csv"
    arrdescData = ''

    if os.path.exists(tblFile):
        df = pd.read_csv(tblFile)
        dffilter = df.query("tableName== '"+tableName +
                            "' and tableType== 'NumVarDIst'")
        if(len(dffilter) > 0):
            var1 = dffilter["var1"].values[0]
            var2 = dffilter["var2"].values[0]
        savefile_withoutnull = file_path + file_name + ".csv"

        df = pd.read_csv(savefile_withoutnull, na_values='?')
        cat_cols = [c for i, c in enumerate(
            df.columns) if df.dtypes[i] in [np.object]]
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
        print('colNames ', dist_num_cat.columns)
        arrdescData = ''' <div class="appTblsss" id="'''+tableName + '''"><table width="100%"  border="1" style="border: 1px solid #eee;border-collapse: collapse;">
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
                        </table></div><div class="'''+tableName + '''End">&nbsp;</div>'''
    return arrdescData


def getVIFData():
    arrdescData = ""
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    savefile_x_final = file_path + file_name + "_x_final.csv"
    if os.path.exists(savefile_x_final):
        savefile_x_scaled = savefile_x_final
    else:
        savefile_x_scaled = file_path + file_name + "_x_scaled.csv"
    savefile_x_keep = file_path + file_name + "_x_keep.csv"

    if os.path.exists(savefile_x_scaled):
        x_scaled_df = pd.read_csv(savefile_x_scaled, na_values='?')
        x_keep = pd.read_csv(savefile_x_keep, na_values='?')

        targetVarFile = file_path + file_name + "_targetVar.txt"
        file1 = open(targetVarFile, "r")  # write mode
        targetVar = file1.read()
        file1.close()
        x_keep = x_keep.drop(targetVar, axis=1)
        x_scaled_df = x_scaled_df.drop(targetVar, axis=1)

        vif_data = pd.DataFrame()
        vif_data["feature"] = x_scaled_df.columns

        # calculating VIF for each feature
        vif_data["VIF"] = [variance_inflation_factor(x_scaled_df.values, i)
                           for i in range(len(x_scaled_df.columns))]

        vif_data = vif_data.sort_values(
            "VIF", ascending=False)  # json.loads(result)
        print('vif_data df is')
        print(vif_data)
        # result = vif_data.to_json(orient='records')
        # result = json.loads(result)
        # print('result is ', result)
        arrdescData = '<div class="appTblsss" id="VIFData"><table width="100%" border="1" style="border: 1px solid #eee;border-collapse: collapse;">'
        arrdescData += ' <thead> <tr>'
        arrdescData += ' <th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="60%">Column</th>'
        arrdescData += ' <th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="40%">VIF</th>'
        arrdescData += ' </tr>'
        arrdescData += ' </thead>'
        arrdescData += ' <tbody>  '
        for index, row in vif_data.iterrows():
            # for key in result:
            # print('key is ', key)
            # value = result[key]
            arrdescData += '<tr>  <td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">' + \
                row["feature"]+'</td>'
            # if(value == None):
            arrdescData += '<td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">' + \
                str(row["VIF"]) + '</td></tr>'
            # else:
            # arrdescData += '''<td>''' + str(value)+'''</td>'''
        arrdescData += '''</tbody></table></div><div class="VIFDataEnd">&nbsp;</div>'''

        return arrdescData


def getCT(tableName):
    tblFile = file_path + user_name+"_Tables.csv"
    arrdescData = ''

    if os.path.exists(tblFile):
        df = pd.read_csv(tblFile)
        dffilter = df.query("tableName== '"+tableName +
                            "' and tableType== 'TarvsCat'")
        if(len(dffilter) > 0):
            var1 = dffilter["var1"].values[0]
            var2 = dffilter["var2"].values[0]
    csvfile = file_path + file_name + ".csv"
    df = pd.read_csv(csvfile, na_values='?')
    dfCRossTab = pd.crosstab(df[var1], df[var2], rownames=[
                             var1], colnames=[var2])
    resultCrossTab = dfCRossTab.to_json(orient='index')
    resultCrossTab = json.loads(resultCrossTab)
    appendHeaderData1 = '<div class="appTblsss" id="'+tableName + \
        '"><table width="100%" border="1" style="border: 1px solid #eee;border-collapse: collapse;">'
    appendHeaderData1 += '<thead><tr><th style="padding-top:0px;padding-bottom:0px;background-color:#eee;" width="20%">' + var1 + '</th>'
    appendHeaderData2 = '<tr><th style="padding-top:0px;padding-bottom:0px;background-color:#eee;" width="20%">' + var2 + '</th>'
    appendBodyData = '<tbody>'
    for key in resultCrossTab:
        value = resultCrossTab[key]
        # arrdescData += '''
        #             <tr>
        #                 <td>''' + str(key)+'''</td>'''
        for key2 in value:
            appendHeaderData1 = appendHeaderData1 + \
                '<th style="padding-top:0px;padding-bottom:0px;background-color:#eee;" width="10%">' + \
                str(key2) + '</th>'
            appendHeaderData2 = appendHeaderData2 + \
                '<th style="padding-top:0px;padding-bottom:0px;background-color:#eee;" width="10%"></th>'
        appendHeaderData1 = appendHeaderData1+'</tr>'
        appendHeaderData2 = appendHeaderData2+'</tr></thead>'
        break
    for key in resultCrossTab:
        value = resultCrossTab[key]
        appendBodyData = appendBodyData+'<tr>'
        appendBodyData = appendBodyData + \
            '<td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">'+key+'</td>'
        for key2 in value:
            val1 = value[key2]
            appendBodyData = appendBodyData + \
                '<td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">' + \
                str(val1)+'</td>'
        appendBodyData = appendBodyData+'</tr>'
    appendBodyData = appendBodyData + \
        '</tbody></table></div><div class="'+tableName+'End">&nbsp;</div>'
    # $('#crosstabData').append(appendHeaderData1+appendHeaderData2+appendBodyData);
    arrdescData = appendHeaderData1+appendHeaderData2+appendBodyData
    # print('arrdescData is ', arrdescData)
    return arrdescData


def getValFindingsttbl():
    validationFindings = file_path + user_name + "_validationFindings.csv"
    arrdescData =""
    if os.path.exists(validationFindings):
        print('val findings exists')
        df = pd.read_csv(validationFindings)
        df = df.sort_values(by="reqId", ascending=True)

        arrdescData = '<div class="appTblsss" id="ValFinding"><table width="100%" border="1" style="border: 1px solid #eee;border-collapse: collapse;">'
        arrdescData += ' <thead> <tr>'
        arrdescData += ' <th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="10%">Finding ID#</th>'
        arrdescData += ' <th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="30%">Assessment Area</th>'
        arrdescData += ' <th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="40%">Description</th>'
        arrdescData += ' <th style="padding: 5px 0px 5px 5px;border: 1px solid #eee;background-color:#eee;" width="20%">Risk Level</th>'
        arrdescData += ' </tr>'
        arrdescData += ' </thead>'
        arrdescData += ' <tbody>  '
  
         
        for index, row in df.iterrows():
            arrdescData += '<tr>  <td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">' + \
               str(row["findingsId"])+'</td>' 
            arrdescData += '<td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">' + \
                str(row["Assessment"]).encode('latin-1', 'replace').decode('latin-1')+ '</td>'
            
            arrdescData += ' <td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">' + \
               str(row["Desc"]).encode('latin-1', 'replace').decode('latin-1')+'</td>' 
            arrdescData += '<td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">' + \
                str(row["Risk_Level"]).encode('latin-1', 'replace').decode('latin-1')+ '</td></tr>'

         
            if(len(str(row["Response"])) > 0 and str(row["Response"]) != "-"):
                arrdescData += '<tr>  <td style="padding: 0px 5px 0px 5px;border: 1px solid #eee;">' + \
                                str(row["Response"])+'</td></tr>'  

        arrdescData += '''</tbody></table></div><div class="ValFindingEnd">&nbsp;</div>'''
    print('valfindings data is ',arrdescData)
    return arrdescData 


def getModels(request):
    try:
        modelfile=file_path+ "Modelinfo.csv"  
        result=[]
        if os.path.exists(modelfile):
            df = pd.read_csv(modelfile, na_values='?')

            result = df.to_json(orient="records")
            result = json.loads(result)    
        return render(request, 'setModel.html',{'modelinfo':result})
    except Exception as e:
        print(e)
        print('traceback is ', traceback.print_exc())
        return render(request, 'error.html')

def setModel(request):
    
    try:
        model = request.GET['model']
        modelfile=file_path+ "Modelinfo.csv"  
        print('model is ',model)
        if os.path.exists(modelfile):
            df = pd.read_csv(modelfile, na_values='?')

            df["IsSelected"] = "No"
            df.loc[df.Process_Name == model, "IsSelected"] = "Yes"
            df.to_csv(modelfile, index=False, encoding='utf-8')
        return  JsonResponse({'msg':'success'})
    except Exception as e:
        print(e)
        print('traceback is ', traceback.print_exc())
        return render(request, 'error.html')
    
def viewFiltredDataType(request):
    try: 
        request_data=request.GET.get('objectDataString',0)
        data=json.loads(request_data)
        print("req data---",type(data)) 
        confirm_obj=collection.find(json.loads(data))
        
        df =  pd.DataFrame(list(confirm_obj))
        df.pop('file_id')
        gridDttypes = []
        dttypes = dict(df.dtypes)
        # print(dttypes)
        for key, value in dttypes.items():
            gridDttypes.append(
                {'colName': key, 'dataType': value, 'notnull': df[key].count()})
        pdf = FPDF()
        pdf.add_page()

        pdf = exportDatatypenCnt(pdf, df, "")
        pdf.output(os.path.join(
            BASE_DIR, plot_dir_view +"/DatatypeCount.pdf"))
        del df
        return render(request, 'ViewDataType.html',  {'page':'ViewDataType','pdfFile': '\static\media\DatatypeCount.pdf', 'dataTypes': gridDttypes})
    except Exception as e:
        print(e)
        print('stacktrace iis ', traceback.print_exc())
        return render(request, 'error.html')

def dataIntegrity(request):
    try:
        UserChartFile = file_path + "_Chartimg.csv"
        data = {}
        resultDocumentation = []
        DocumentationData = file_path + file_name + "_DocumentationData.csv"
        if os.path.exists(DocumentationData):
            df_old = pd.read_csv(DocumentationData)
            idxLst = [*range(1, len(df_old)+1, 1)]
            df_new = pd.DataFrame(
                idxLst, columns=['docIdx'])
            df = pd.concat([df_old, df_new], axis=1)
            resultDocumentation = df.to_json(orient="records")
            resultDocumentation = json.loads(resultDocumentation)
        data = {
            'modelDocs': resultDocumentation,
        }
        return render(request, 'dataIntegrity.html', data)
    except Exception as e:
        print('Error is', e,' , ',traceback.print_exc)
        return render(request, 'error.html')

def saveDIData(request):
    comment = request.GET['comment']
    reqId = request.GET['reqId']
    title = request.GET['title']
    titleIdx = request.GET['titleIdx']
    print("reqId",reqId)
    print("title",title)
    print("titleIdx",titleIdx)
    collection_data_integrity
    request_id=find_max_req_id()

    di_id=find_max_id()
    print("di_id",di_id)
    
    di_obj={'Title':title,'TitleIdx':int(titleIdx),'Comment':comment,'Img':'','ImgWidth':'','ImgHeight':'',
                     'ImgAlign':'','ImgTitle':'','TitleAlign':'','reqId':int(request_id),'di_id':int(di_id)}
    myquery = { "reqId": int(request_id) ,'Title':title}
    mydoc = collection_data_integrity.find(myquery)
    if collection_data_integrity.find_one(myquery):
        for i in mydoc:
            print("I",i['reqId'])
            print("di_id",i['di_id'])
            di_obj['di_id']=i['di_id']
            #print("cs_obj",cs_obj)
            newvalues = { "$set":di_obj }
            collection_data_integrity.update_one(myquery, newvalues)
            for i in collection_data_integrity.find():
                print("updated")
    else:
        print("New Entry")
        di_obj['di_id']=di_obj['di_id'] + 1
        collection_data_integrity.insert_one(di_obj) 
    data = {
        'is_taken': True,
        'reqId': str(reqId),
        'titleIdx': int(titleIdx)-1,
    }
    return JsonResponse(data)

def conceptualsoundness(request):
    try:
        UserChartFile = file_path + "_Chartimg.csv"
        data = {}
        result=[]
        resultDocumentation = []
        resultConcSnd = []
        modelFileExists = False
        processing = os.path.join(BASE_DIR, processingFile_path)
        df = pd.read_csv(processing, na_values='?')

        resultpROCESS = df.to_json(orient="records")
        resultpROCESS = json.loads(resultpROCESS)
        del df 
        
        resultDocumentation = objvalidation.getModelDocs(request.session['vt_mdl']) #collection_model_documents.find({'Mdl_Id':request.session['vt_mdl']},{'_id':0})
        # df =  pd.DataFrame(list(model_document_obj))
        # print("df",df)
        
        # resultDocumentation = df.to_json(orient="index")
        # resultDocumentation = json.loads(resultDocumentation)
        print('resultDocumentation is ',resultDocumentation)
        data = {
            'selectedMdl':request.session['vt_mdl'],
            'imgFiles': result,
            'pdfFile': "/static/media/ValidationReport.pdf",
            'modelDocs': resultDocumentation,
            'modelUsage': modelFileExists,
            'modelUsageFile': plot_dir + file_name + "_ModelUsage.pdf",
            'df': resultpROCESS,
            'resultConcSnd': resultConcSnd,
            'occpae42' : "/static/reportTemplates/pub-ch-model-risk.pdf#page=42&zoom=100,0,400",
        }
        return render(request, 'conceptualsoundness.html', data)
    except Exception as e: 
        print('Error is', e,' , ',traceback.print_exc)
        return render(request, 'error.html')

def saveCSData(request):
    comment = request.GET['comment']
    reqId = request.GET['reqId']
    title = request.GET['title']
    titleIdx = request.GET['titleIdx']
    print("Comment",comment)
    print("reqId",reqId)
    print("title",title)
    print("titleIdx",titleIdx)
    collection_conceptual_soundness
    request_id=request.session['vt_mdl']

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
    return JsonResponse(data)

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
 
def saveModelUsageReq(request):
    print("saveModelUsageReq")
    email = request.GET['email']
    categories = request.GET['categories']
    comment= ""
    print("email",email)
    print('comment',comment)
    print("categories",categories)
    json_dictionary = json.loads(categories)
    #print("json_dictonary",json_dictionary)
    req_id= request.session['vt_mdl'] 
    #modelUsageReq = file_path + file_name + "_modelUsageReq.csv"
    for colval in json_dictionary:
        for attribute, value in colval.items():
            colName = value
            print('colName ', colName)

    #collection_model_usage
            usage_id=find_max_usage_id()
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
    return JsonResponse(data)

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


def modelUsageResp(request):
    try:
        req_id = request.GET['id']
        
        model_usage_obj = collection_model_usage.find({'Mdl_Id':(req_id)},{'_id':0})
        df =  pd.DataFrame(list(model_usage_obj))       
        
        result = df.to_json(orient="records")
        result = json.loads(result)
        
        # modelUsageReq = file_path + file_name + "_modelUsageReq.csv"
        # data = {'List': ''}
        # if os.path.exists(modelUsageReq):
        #     df = pd.read_csv(modelUsageReq)
        #     result = df.to_json(orient="records")
        #     result = json.loads(result)
        data = {'List': result}
        print("result",result)    
        return render(request, 'modelUsageResp.html', data)
    except Exception as e:
        print(e)
        return render(request, 'error.html')


def saveModelUsageResp(request):
    feqModel = request.GET['feqModel']
    comments = request.GET['comments']
    users = request.GET['users']
    comments_dictionary = json.loads(comments)
    print("comments_dictionary",comments_dictionary)
    mdl_id=""
    for colval in comments_dictionary:
            print("colval",colval)
            for usage_id, resp in colval.items():
                # print("usage_id",type(usage_id))
                # print("resp",resp)
                 
                model_usage_obj = collection_model_usage.find({'usage_id':int(usage_id) },{'_id':0})
                for i in model_usage_obj:
                    mdl_id=i['Mdl_Id']
                    myquery=i
                    # model_usage_obj['usage_id']=i['usage_id']
                    # print("model_usage_obj",model_usage_obj)
                    newvalues = { "$set":{'Response':resp} }
                    collection_model_usage.update_one(myquery, newvalues)
                    
    exportModelUsage(mdl_id)
    data = {
        'is_taken': True,
    }
    return JsonResponse(data)


def exportModelUsage(mdl_id=""): 
    usage_obj = collection_model_usage.find({'Mdl_Id':mdl_id },{'_id':0})
    df =  pd.DataFrame(list(usage_obj))
    pdf = FPDF()
    pdf.add_page()
    x, y = 10, 10
    if len(df)>0: 
        df = df.sort_values(by="usage_id", ascending=True)
        pdf.set_xy(x, y)
        pdf.set_font("Arial", "B", size=9)
        pdf.set_text_color(0.0, 0.0, 0.0)
        pdf.cell(
            0, 5, "Model Usage", align='L')
        pdf.set_font("Arial",  size=9)
        pdf.set_fill_color(211, 211, 211)
        y = pdf.get_y()+10
        pdf.set_xy(20, y)
        pdf.cell(60, 5, "Section",
                 1, fill=True, align='L')

        pdf.set_xy(80, y)
        pdf.cell(100, 5, "Comments",
                 1, fill=True, align='L')
        y = pdf.get_y()+5
        cellHeight = 0
        pdf.set_font("Arial",  size=8)
        for index, row in df.iterrows():
            pdf.set_xy(20, y)
            pdf.multi_cell(60, 4, str(
                row["Category"]), 0, fill=False)
            cellHeight = pdf.get_y()
            pdf.set_xy(80, y)
            pdf.multi_cell(100, 4, str(row["Response"]).encode(
                'latin-1', 'replace').decode('latin-1'), 0, fill=False)
            if(pdf.get_y() > cellHeight):
                cellHeight = pdf.get_y()
            pdf.rect(20, y, 60, cellHeight-y)
            pdf.rect(80, y, 100, cellHeight-y)
            y = cellHeight
            print(' y is ', y, ' cellHeight ', cellHeight)
    pdf.output(os.path.join(
        BASE_DIR, plot_dir_view + mdl_id + "_ModelUsage.pdf"))

def valFindings(request):
    print("valFindings")
    try:
        today = date.today().strftime("%m/%d/%Y")
        request_id=request.session['vt_mdl'] #find_max_req_id()
        validation_obj=collection_validation_findings.find({'Mdl_Id': (request_id)},{'_id':0})
  
        result=list()
        for i in validation_obj:
            print(i)
            if (str(i["Response"]) != "-"):
                result.append(
                    {'val': i["FindingsId"], 'bgColor': 'green', 'color': 'white'})
            else:
                result.append(
                    {'val': i["FindingsId"], 'bgColor': 'white', 'color': 'black'}) 

        data = {'List': result, 'today': today, 'emailLst': getEmails(),'model_id':request_id}
        return render(request, 'valFindings.html', data)
    except Exception as e:
        print(e)
        return render(request, 'error.html')


# def valFindingsResp(request):
#     try:
#         validationFindings = file_path + file_name + "_validationFindings.csv"
#         data = {'List': ''}
#         if os.path.exists(validationFindings):
#             df = pd.read_csv(validationFindings)
#             df = df["findingsId"]
#             result = df.to_json(orient="records")
#             result = json.loads(result)
#             data = {'List': result}
#         return render(request, 'valFindingsResp.html', data)
#     except Exception as e:
#         print(e)
#         return render(request, 'error.html')


def getvalFindings(request):
    #validationFindings = file_path + file_name + "_validationFindings.csv"
    findingsId = request.GET['findingsId']
    
    validation_obj=collection_validation_findings.find({'FindingsId':findingsId},{'_id':0})
    df =  pd.DataFrame(validation_obj)
    print("df is",df)
    result=df.to_dict(orient="records")
    print("result",result)
    #result=json.loads(result)
    data={'findingData':result}
     
    return JsonResponse(data)

def savevalFindings(request):
    Desc = request.GET['Desc']
    Risk = request.GET['Risk_Level']
    Assessment = request.GET['Assessment']
    findingsId = request.GET['findingsId']
    Level = request.GET['Lvl'] 
    letters = ""
    words = Assessment.split()
    if(len(words)>1):
        for i in range(2):
            letters = letters + words[i][0]
    else:
        letters = Assessment[:2]
    print('letters is ',letters)
    #validationFindings = file_path + file_name + "_validationFindings.csv"
    today = date.today().strftime("%m/%d/%Y")
    #collection_validation_findings
    request_id=request.session['vt_mdl'] # find_max_req_id()
    #findingsId = letters + str(len(df_old)+1)
    documents_obj={"Assessment":Assessment,"Risk":Risk,"Risk_Level":Level,"Description":Desc,
                    "Response":'-',"EmailId":'-',"FindingsId":'-',"Finding_RequestId":'',"Date":today,"Mdl_Id":(request_id)}
    
    myquery={'Mdl_Id':(request_id)}
    validation_obj=collection_validation_findings.find(myquery)
    if collection_validation_findings.find_one(myquery):
        print("if true")
        myquery={'FindingsId':findingsId}
        validation_obj_update=collection_validation_findings.find(myquery)
        if collection_validation_findings.find_one(myquery):
            print("Update")      
            for i in validation_obj_update:
                print("i",i)
                FindingsId_update=i['FindingsId']
                Finding_RequestId_update=i['Finding_RequestId']
                
                newvalues = { "$set":documents_obj }
                documents_obj['FindingsId']=FindingsId_update
                documents_obj['Finding_RequestId']=Finding_RequestId_update
                print("documents_obj",documents_obj)
                collection_validation_findings.update_one(myquery,newvalues)
        else:    
            print("Insert if entry > 0")    
            for i in validation_obj:
                #print("i",i['Finding_RequestId'])
                max_finding_requestId=i['Finding_RequestId']
        
            Finding_RequestId=int(max_finding_requestId+1)

            FindingsId = letters + str(Finding_RequestId)
            print("Findings",FindingsId)
            documents_obj['FindingsId']=FindingsId
            documents_obj['Finding_RequestId']=Finding_RequestId
            print("documents_obj",documents_obj)
            collection_validation_findings.insert_one(documents_obj)
            data = {
                'is_taken': True,
                'findingsId': FindingsId
            }
            return JsonResponse(data)
    else:
        print("First Entry")
        max_finding_requestId =0
        Finding_RequestId=int(max_finding_requestId+1)
        FindingsId = letters + str(Finding_RequestId)
        documents_obj['FindingsId']=FindingsId
        documents_obj['Finding_RequestId']=Finding_RequestId
        print("documents_obj",documents_obj)
        collection_validation_findings.insert_one(documents_obj)
        data = {
            'is_taken': True,
            'findingsId': FindingsId
        }
        return JsonResponse(data) 
    data = {
        'is_taken': True,
    }
    return JsonResponse(data)

def sendDevloperMail(request):
    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        emailId = request.GET.get('emailId', 'False') 
        validation_obj=collection_validation_findings.find({'Mdl_Id':request.session['vt_mdl']},{'_id':0})
        df_old =  pd.DataFrame(validation_obj)
        if len(df_old)>0 and emailId != "False": 
            if ((df_old["EmailId"] == emailId)).any():
                print('emailsent')
                data = {'is_taken': True}
            else:
                # df_old.at[0, "EmailId"] = emailId
                validation_obj_update=collection_validation_findings.find({'Mdl_Id':request.session['vt_mdl']})
                if collection_validation_findings.find_one({'Mdl_Id':request.session['vt_mdl']}):
                    print("Update")      
                    for i in validation_obj_update:
                        newvalues = { "$set":{"EmailId":emailId} } 
                        collection_validation_findings.update_one({'Mdl_Id':request.session['vt_mdl']},newvalues)
                mail_content = """Hello,
                Please click link below to responde the model validation findings.
                """+app_url + """valFindingsResp?id="""+ request.session['vt_mdl'] +"""
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
                print('Mail Sent')
                data = {'is_taken': True}
    except Exception as e:
        print(e)
        print("Error: unable to send email")
        data = {'is_taken': False}
    return JsonResponse(data)

def valFindingsResp(request):
    try:
        mdlid=request.GET['id']
        validation_obj=collection_validation_findings.find({'Mdl_Id':mdlid},{'_id':0})
        df =  pd.DataFrame(validation_obj)
        mdl_id = request.session['vt_mdl']
        print("mdl id------------------",mdl_id)
        data = {'List': '','model_id':mdl_id}
        if len(df)>0:
            
            df = df["FindingsId"]
            result = df.to_json(orient="records")
            result = json.loads(result)
            
            data = {'List': result,'model_id':mdl_id}
        return render(request, 'valFindingsResp.html', data)
    except Exception as e:
        print(e)
        return render(request, 'error.html')
    
def savevalFindingsResp(request):
    Resp = request.GET['Resp']
    findingsId = request.GET['findingsId']
    validation_obj=collection_validation_findings.find({'FindingsId':findingsId})
    df =  pd.DataFrame(validation_obj)
    print('len(df) ',len(df),' ',findingsId,',',Resp)
    
    if len(df) >0: #collection_validation_findings.find_one({'FindingsId':findingsId}):
        newvalues ={ "$set":{"Response":Resp} }  
        collection_validation_findings.update_one({'FindingsId':findingsId},newvalues)   
        del df 
    data = {
        'is_taken': True
    }
    return JsonResponse(data)

def viewModelUsage(request): 
    resultConcSnd = []
    model_usage_obj = collection_model_usage.find({'Mdl_Id':request.session['vt_mdl']},{'_id':0})
    df =  pd.DataFrame(list(model_usage_obj))       
    
    resultConcSnd = df.to_json(orient="records")
    resultConcSnd = json.loads(resultConcSnd)
    
    
    del df

    data = {
        'resultConcSnd': resultConcSnd,
    }
    return render(request, 'viewModelUsage.html', data)

def viewConcSnd(request):
    cs_obj = collection_conceptual_soundness.find({'Mdl_Id':request.session['vt_mdl']},{'_id':0})
    df =  pd.DataFrame(list(cs_obj))
    resultConcSnd = []
    resultConcSnd = df.to_json(orient="records")
    resultConcSnd = json.loads(resultConcSnd)
    del df
    data = {
        'resultConcSnd': resultConcSnd, 'header': 'Conceptual Soundness'
    }
    return render(request, 'viewConSnd.html', data)

class MyFPDF(FPDF, HTMLMixin):
    pass


##########Ashok  Code############
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


def home2(request):
    print("in home2")
    try:
        mdlId =request.POST.get('mdlid', 'False')
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
            df = pd.read_csv(savefile_name, encoding='utf-8')
            # print('printing datatypes ')
            print("DF new",df)
            dttypes = dict(df.dtypes)
            file_id=find_max_prdn_file_id("") 
            print("file_id",file_id)
            data_model=df.to_dict('records')
            #print("data_model",data_model)
            for i in data_model:
                    keys_data=list()
                    keys_data.append(list(i.keys()))    ##column name
            Freq_Idx=1
            uploaded_on=datetime.datetime.now()  ##uploaded on data
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
            'mdl_id':mdlId,
            'file_nm':filename_a,
            'added_by':request.session['uid'],
            'freq_idx':freidx,
            'is_new':is_new
        }
        responseget = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
        # data=json.loads(responseget.content)
        print("response--------------------------",json.loads(responseget.content))
        return JsonResponse({'isvalid':'true'})
        
    except Exception as e:
        print(e)
        print('traceback is ', traceback.print_exc())
        return render(request, 'error.html')

#-------------------------------Ashok Code--------------------

collection_validator_data_file_Info=db['validator_dataSrcFileInfo']
collection_validator_data_src_data=db['validator_dataSrcData']



def find_validator_data_max_file_id(mdlid=""):
    
    print("find_max_file_id",mdlid)
    if mdlid=="":
        print("if")
        src_file_obj = collection_validator_data_file_Info.find()
    else:
        print("else")
        src_file_obj = collection_validator_data_file_Info.find({'Mdl_Id':mdlid})
    df =  pd.DataFrame(list(src_file_obj)) 
    print("df",df)
    print("length",len(df))
    if len(df)>0: 
        file_id=df['file_id'].max()
    else:
        file_id=1 #changed by nilesh on 11.4.23
    print('file_id' ,file_id)
    return file_id

file_path_validator_data = os.path.join(BASE_DIR, 'static/csv_files_validator_data/')

def multiple_data_import(request):
    _xFiles=[".csv","_x_model.csv","_x_keep.csv","_x_dummy.csv","_x_scaled.csv","_x_final.csv"]
    file_name = "csvfile_"+ request.session['username']
    

    if request.method == 'POST' and request.FILES['myfile']:
        print("if post ")
        
        if 'myfile' not in request.FILES:
            return JsonResponse({'error': 'No files uploaded.'}, status=400)

        # Retrieve the uploaded files
        files = request.FILES.getlist('myfile')

        print("files",files)
        print("files",len(files))
        # for i in range(len(files)):
        #     print(i)
            
        if not files:
            return JsonResponse({'error': 'No files uploaded.'}, status=400)
        fs = FileSystemStorage()
        columns_data=list()
        dataframes = []
        for file in files:

            # Assuming the files are CSV for this example
            df_combined = pd.read_csv(file)
            dataframes.append(df_combined)

            file_name = file.name
            savefile_name = file_path_validator_data + file_name + ".csv" 
            print("file savefile_name",file,savefile_name)
            fs.save(savefile_name, file)
            df = pd.read_csv(savefile_name, encoding='utf-8')
            print("df",df)
            column_names = df.columns.to_list()
            print("List of all column names:")
            print(column_names)
            columns_data.append(column_names)
            dttypes = dict(df.dtypes)
            file_id=find_validator_data_max_file_id("") 

            data_model=df.to_dict('records')
            print("data_model",data_model)
            for i in data_model:
                keys_data=list()
                keys_data.append(list(i.keys()))    ##column name
            
            uploaded_on=datetime.datetime.now()  ##uploaded on data
            file_info_data={'Mdl_Id':int(request.session['uid']),'file_id':int(file_id),'file_columns':keys_data,'file_name':file_name,'uploaded_by':request.session['username'],"uploaded_on":uploaded_on,'validation_cycle':request.session['validation_cycle']}
                
            if file_id==int(0):  
                file_info_data['file_id']=file_info_data['file_id'] + 1
                collection_validator_data_file_Info.insert_one(file_info_data)  
                # src_data_dict={}

                ## insert many validator Data SRC

                result = collection_validator_data_src_data.insert_many(data_model)
                
                # for i in data_model:                        
                #     src_data_dict=i
                #     src_data_dict.update({'file_id':file_info_data['file_id']}) 
                #     collection_validator_data_src_data.insert_one(i)
            else:
            
                file_info_data['file_id']=file_info_data['file_id'] + 1
                collection_validator_data_file_Info.insert_one(file_info_data)  
                
                ## insert many validator Data SRC

                result = collection_validator_data_src_data.insert_many(data_model)

                # for i in data_model: 
                #     src_data_dict=i
                #     src_data_dict.update({'file_id':file_info_data['file_id']}) 
                #     collection_validator_data_src_data.insert_one(i)

            # objmaster.insertActivityTrail(request.session['vt_mdl'],"17","Model source data imported.",request.session['uid'],request.session['accessToken'])


             

            arrdescData = []
            gridDttypes = []
            result = ""
            #file_name=myfile
            
            for key, value in dttypes.items():
                gridDttypes.append({'colName': key, 'dataType': value})

            dfdisplay = df.head(100)
            result = dfdisplay.to_json(orient="records")
            result = json.loads(result)
            
            print("columns_data",columns_data)

        # Concatenate all DataFrames (assuming they have the same structure)
        combined_file="file1" + "file2"
        final_df = pd.concat(dataframes, ignore_index=True)
        print("final_df",final_df)
        savefile_name = file_path_validator_data + combined_file + ".csv"
        final_df.to_csv(savefile_name, index=False)

        return JsonResponse({'message': 'Files uploaded successfully.', 'file_paths': savefile_name})

    return render(request, 'multiple_data_import.html')


### Mapping code Merged Info 
client = MongoClient('localhost',27017,connect=False)
dbs = client['validation_tool'] 
collection_mergeinfo=dbs['merged_info']


def mapping(request):
    # query = { 'validation_cycle':1,'is_primery':1}
    
    ## is primery =1
    query1 = {'validation_cycle':1}
    query2 = {'is_primery':1}


    combined_query = {"$and": [query1, query2]}

    src_file_obj = list(collection_file_info.find(combined_query,{'_id':0}))

    print("src_file_obj",src_file_obj)
    df=pd.DataFrame(list(src_file_obj))
    print("check DF",df)

    data_src_obj=collection.find()
    data_list=list(data_src_obj)
    for i in data_list:
        print("i",i['file_id'])
        query2 = {'file_id':i['file_id']}
        # combined_query = {"$and": [query1, query2]}
        src_obj_check = list(collection.find(query2,{'_id':0}))
        print("src_obj_check",src_obj_check)
        df=pd.DataFrame(list(src_obj_check))
        print("check Data src",df)

    ## Normal data import and validators file data

    query11 = {'validation_cycle':1}
    query22 = {"is_primery": {"$ne": 1}}

    combined_query_11 = {"$and": [query11, query22]}

    src_file_obj_combined = list(collection_file_info.find(combined_query_11,{'_id':0}))
    
    file_names = [item['file_name'] for item in src_file_obj_combined]

    print('file_names',file_names)


    # flat_list = file_columns[0]

    query111 = {'validation_cycle':1}

    src_file_obj_validator = list(collection_validator_data_file_Info.find(query111,{'_id':0}))


    file_names_in_validator = [item['file_name'] for item in src_file_obj_validator if item['file_name'] in file_names]
    print("check",file_names_in_validator)
    if file_names_in_validator:
        for i in file_names_in_validator:
            filter_query = {'file_name': i}
            update_data_srcfile= {"$set": {"data_import": i }}

            update_data_validator={"$set": {"data_validator": i }}

            print("filter_query",filter_query)
            print("update_data",update_data_srcfile)

            # Update one document
            result = collection_file_info.update_one(filter_query, update_data_srcfile)

            result = collection_validator_data_file_Info.update_one(filter_query, update_data_validator)

    print("src_file_obj_combined",src_file_obj_combined)
    print("src_file_obj_validator",src_file_obj_validator)
 
    src_file_obj_combined.extend(src_file_obj_validator)
    print("final list",src_file_obj_combined)
    return render(request, 'mapping.html',{'doc':src_file_obj,'doc2':src_file_obj_combined})

def get_colums_mapping(request):
    print("get_colums_mapping")
    print('file name',request.GET.get('file_name'))    
    query1 = {'validation_cycle':1}
    query2 = {'file_name':request.GET.get('file_name')}

    # Combine the queries using $and
    combined_query = {"$and": [query1, query2]}
    # query = { 'validation_cycle':1,'file_name':request.GET.get('file_name')}

    columns_obj = list(collection_file_info.find(combined_query,{'_id':0}))   

    print("columns_obj",columns_obj)
    file_columns = columns_obj[0]['file_columns']
    print('file_columns',file_columns)
    # column_data=list()
    # for i in columns_obj:
    #     for j in i.file_columns:
    #         column_data.append(j)

    # print("column_data",column_data)
    flat_list = file_columns[0]

    print(flat_list)
    return JsonResponse(flat_list,safe=False)




def get_columns_DV(request):
    print("get_columns_DV")
    print('file name',request.GET.get('file_name'))    

    file_name=request.GET.get('file_name')
    flat_dict=dict()
    # flat_list=[]
    if file_name.startswith("DI"):
        print("DI")
        file_name=file_name[3:]
        print("file_name",file_name)
        query1 = {'validation_cycle':1}
        query2 = {'file_name':file_name}

        combined_query = {"$and": [query1, query2]}

        columns_obj = list(collection_file_info.find(combined_query,{'_id':0}))   

        print("columns_obj",columns_obj)
        file_columns = columns_obj[0]['file_columns']
        print('file_columns',file_columns)
        
        columns_data = file_columns[0]
        file_id = columns_obj[0]['file_id']

        flat_dict['columns_data']=columns_data
        flat_dict['file_id']=file_id
    
        print("flat_dict",flat_dict)
        
    elif file_name.startswith("Val") :
        print("Val")
        file_name=file_name[4:]
        print("file_name",file_name)
        query1 = {'validation_cycle':1}
        query2 = {'file_name':file_name}

        combined_query = {"$and": [query1, query2]}

        columns_obj = list(collection_validator_data_file_Info.find(combined_query,{'_id':0}))   

        print("columns_obj",columns_obj)
        file_columns = columns_obj[0]['file_columns']
        print('file_columns',file_columns)
        
        columns_data = file_columns[0]
        file_id = columns_obj[0]['file_id']

        flat_dict['columns_data']=columns_data
        flat_dict['file_id']=file_id
    
        print("flat_dict",flat_dict)
    else:
        print("else")

        print("file_name",file_name)
        query1 = {'validation_cycle':1}
        query2 = {'file_name':file_name}

        combined_query = {"$and": [query1, query2]}

        columns_obj = list(collection_validator_data_file_Info.find(combined_query,{'_id':0}))   

        print("columns_obj",columns_obj)

        if len(columns_obj)> 0:
            file_columns = columns_obj[0]['file_columns']
            print('file_columns',file_columns)
            
            columns_data = file_columns[0]
            file_id = columns_obj[0]['file_id']

            flat_dict['columns_data']=columns_data
            flat_dict['file_id']=file_id
        
            print("flat_dict",flat_dict)
            # flat_list = file_columns[0]

        print("file_name",file_name)
        query1 = {'validation_cycle':1}
        query2 = {'file_name':file_name}

        combined_query = {"$and": [query1, query2]}

        columns_obj_file = list(collection_file_info.find(combined_query,{'_id':0}))   

        print("columns_obj_file",columns_obj_file)

        if len(columns_obj_file)> 0:
            file_columns = columns_obj_file[0]['file_columns']
            print('file_columns',file_columns)
            
            columns_data = file_columns[0]
            file_id = columns_obj_file[0]['file_id']

            flat_dict['columns_data']=columns_data
            flat_dict['file_id']=file_id
        
            print("flat_dict",flat_dict)

    return JsonResponse(flat_dict)


def save_mapping(request):
    print("getlist",request.GET.getlist)
    selectedData1 = request.GET.getlist('selectedData1[]')
    selectedData2 = request.GET.getlist('selectedData2[]')
    primery_file=request.GET.get('primery_file')
    secondarey_file=request.GET.get('secondarey_file')
    # file_id=request.GET.get('file_id')

    # Process the options as needed
    # For example, you can save them to the database or perform other operations
    print('Received options:', selectedData1)
    print('Received options:', selectedData2)
    print('primery', primery_file)
    print('second:', secondarey_file)
    # print('file_id', file_id)

    collection_mergeinfo

    for i in selectedData1:
        print(i)
        for j in selectedData2:
            file_info_data={'Mdl_Id':request.session['vt_mdl'],'primery_column':i,'primery_file_name':primery_file,
                            'secondarey_column':j,'secondarey_file_name':secondarey_file,'validation_cycle':request.session['validation_cycle']}
    
            collection_mergeinfo.insert_one(file_info_data) 
    print("saved")

    data={'msg':"Mapping Done"}
    return JsonResponse(data,safe=False)



    

