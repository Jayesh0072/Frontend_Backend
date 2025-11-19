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


def valFindings_2(request):
    print("valFindings_2")
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

        if request.method == "POST":
            data = json.loads(request.body)
            
            mdlid = data.get('mdlid', [])
            validation_element = data.get('validation_element', [])
            optValCat = data.get('optValCat', [])

            print("Model IDs:", mdlid)
            print("Validation Elements:", validation_element)
            print("Validation Categories:", optValCat)


            return JsonResponse({"status": "success"})
    
        data = {'List': data['List'], 'today': data['today'], 'emailLst': data['emailLst'],'ValCatLst':data['ValCatLst'],'ValCatElm':data['ValCatElm'],'mdlid':data_a['mdlids']}
        return render(request, 'valFindings_2.html', data)
    except Exception as e:
        print(e, traceback.print_exc())
        return render(request, 'error.html')
    

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

import csv

def upload_findings(request):
    if request.method == "POST":
        file = request.FILES.get("fileprdxn")
        print("file",file)
        if file and file.name.endswith(".csv"):
            print("if")
            # Save file first
            fs = FileSystemStorage(location="static/media/findings/")
            filename = fs.save(file.name, file)
            file_path = fs.path(filename)
            print("file_path",file_path)
            # Use Pandas to read CSV
            df1 = pd.read_csv(file_path)
            print("df1",df1)

            excel_fields = df1.columns.to_list()
            excel_fields_1  = df1.to_json(orient="records")
            print("df1 columns",excel_fields)
            print("excel_fields_1",excel_fields_1)
            # Iterate rows and save to DB
            if list(df1.columns.values): 
                third_party_api_url  = getAPIURL()+'upload_findings/'
                data_to_save={ 
                    'addedby':request.session['uid'],
                    'excel_fields':excel_fields,
                    'exceldf':json.loads(excel_fields_1),
                    } 
                header = {
                "Content-Type":"application/json",
                'Authorization': 'Token '+request.session['accessToken']
                }
                responsepost = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)    
                api_data=responsepost.json()
                print("api",api_data)
                return JsonResponse(api_data)
            
            
        return JsonResponse({
            "message": f"File {filename} uploaded and saved into DB successfully",
        })