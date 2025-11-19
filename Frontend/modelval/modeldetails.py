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
from .models import *

from fpdf import FPDF
from django.conf import settings

objreg=Register()  
objmaster=MasterTbls()
objvalidation=Validation()
objdbops=dbops()
objrmse=RMSEModel()


def getAPIURL():
    api_url=os.environ['API_URL']
    return api_url


def activityinfo(record):
    lst = []
    irow=1
    for activity_obj in record: 
        dict={}
        activity_trigger = activity_obj.activity_trigger
        refference_id = activity_obj.refference_id
        addon = activity_obj.added_on
        # print('addon ',addon)
        # addon = datetime.strptime(str(addon), '%y-%m-%d %I:%M %p')

        x = str(addon).split(" ") 
        userobj = Users.objects.get(u_aid = activity_obj.addedby)
        user = userobj.u_name
        f_name = userobj.u_fname
        f_n = f_name[:1].capitalize()
        l_name = userobj.u_lname
        l_n = l_name[:1].capitalize()
        dict['activity_trigger'] = activity_trigger
        dict['refference_id'] = refference_id
        dict['user'] = user
        dict['f_name'] = f_n
        dict['l_name'] = l_n
        dict['date'] = addon.strftime('%m/%d/%Y')
        dict['time'] = addon.strftime('%I:%M %p') 
        dict['activity_details'] =activity_obj.activity_details
        if irow== len(record):
            dict['is_last']='Yes'
        else:
            dict['is_last']='No'
            irow+=1
        lst.append(dict)
    return lst   


def modelDetails(request):
    try:
        print("check request",request.GET)
        mdlId =request.GET.get('mdlId', 'False') 
        api_url=getAPIURL()+"taskListByModel/"       
        data_to_save={ 
            'uid':request.session['uid'],             
            'mdl_id':mdlId} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)         
        api_data=response.json() 
        task_list=api_data['task_list']
        activityobj = ActivityTrail.objects.filter(refference_id = mdlId).order_by('-added_on')  
        activity_lst = activityinfo(activityobj)

        # Next Validation data
        api_url_a=getAPIURL()+"ValidationPlanningAPI/"       
        data_to_get={              
            'mdl_id':mdlId} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        next_val_response = requests.get(api_url_a, data= json.dumps(data_to_get),headers=header)         
        Next_val_api_data = next_val_response.json()
        print("Next_val_api_data ---",Next_val_api_data)
        
        if len(Next_val_api_data['data']) == 0:
            data = {
            'model_id':None,
            'validation_period':None
            }
        else:    
            data = {
                'model_id':Next_val_api_data['data'][0]['mdl_id'],
                'validation_period':Next_val_api_data['data'][0]['validation_period']
            }
        
        third_party_api_url = getAPIURL()+'addUser/'
        header = {      
        "Content-Type":"application/json",
         'Authorization': 'Token '+request.session['accessToken']
        }
        response_user = requests.get(third_party_api_url, headers=header)
        # print("response userlist",response_user.content)
        user_data = json.loads(response_user.content)
        print("user data",user_data)

        return render(request, 'modelDeatails.html',{'actPage':'RMSE','mdl_id':mdlId,'task_list':task_list,'mdlsts':api_data['mdlsts'],
                        'issue_list':api_data['issue_list'],'validationRatings':api_data['validationRatings'],'modelDocs':objvalidation.getModelDocs(mdlId),'activity_lst':activity_lst,'Next_val':data,'user_data':user_data})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
        return render(request, 'modelDeatails.html',{'actPage':'RMSE','mdl_id':mdlId,'task_list':task_list,'mdlsts':api_data['mdlsts'],
                        'issue_list':api_data['issue_list'],'validationRatings':api_data['validationRatings'],'modelDocs':'','activity_lst':activity_lst,'Next_val':data,'user_data':user_data})


def validation_planning(request):
    try:
        third_party_api_url = getAPIURL()+'Fetchallmdlid/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        responseget = requests.get(third_party_api_url,headers=header)
        data=json.loads(responseget.content)
        print("check data",data)

        third_party_api_url = getAPIURL()+'addUser/'
        header = {      
        "Content-Type":"application/json",
         'Authorization': 'Token '+request.session['accessToken']
        }
        response_user = requests.get(third_party_api_url, headers=header)
        # print("response userlist",response_user.content)
        user_data = json.loads(response_user.content)
        print("user data",user_data)

        # fetch projected start date
        third_party_api_url = getAPIURL()+'Val_Period_Master/'
        header = {      
        "Content-Type":"application/json",
         'Authorization': 'Token '+request.session['accessToken']
        }
        
        response_val_period_master_data = requests.get(third_party_api_url, headers=header)
        # print("response userlist",response_user.content)
        vel_period_master_data = json.loads(response_val_period_master_data.content)
        print("date",vel_period_master_data)

        return render(request, 'validation_planning.html',{ 'actPage':'validation_planning','mdlid':data['mdlids'],'user_data':user_data,'projected_start_date':vel_period_master_data})
    except Exception as e:
        print('validation_planning is ',e)
        print('validation_planning traceback is ', traceback.print_exc())

from datetime import datetime, timezone
def mmddyyyy_to_iso_z(date_str: str) -> str:
    # date_str: "04/27/2025"
    dt = datetime.strptime(date_str, "%m/%d/%Y")
    dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()  # -> "2025-04-27T00:00:00+00:00"


def SaveValidationPlanning(request):
    try:
        print("check request",request.POST)
        model_id = request.POST.get('model_id', 'False') 
        validation_period = request.POST.get('validation_period','False')
        validation_scope = request.POST.get('validation_scope','False')

        validator = request.POST.get('validator','False')
        internal_validator = request.POST.get('internal_validator','False')
        external_validator = request.POST.get('external_validator','False')

        projected_start_date = request.POST.get('projected_start_date', 'False')
        projected_start_date_cnvrt = mmddyyyy_to_iso_z(projected_start_date)
        projected_end_date = request.POST.get('projected_end_date','False')
        projected_end_date_cnvrt = mmddyyyy_to_iso_z(projected_end_date)
        revised_end_date = request.POST.get('revised_end_date','False')
        if revised_end_date == 'False':
            revised_end_date_cnvrt = None
        else:
            revised_end_date_cnvrt = mmddyyyy_to_iso_z(revised_end_date)

        previous_total_fees = request.POST.get('previous_total_fees',None)
        estimated_total_fees = request.POST.get('estimated_total_fees',None)
        actual_total_fees = request.POST.get('actual_total_fees',None) 

        validation_status = request.POST.get('validation_status','False')
        validation_progress = request.POST.get('validation_progress','False')

        destination_path = os.path.join(BASE_DIR, 'static\\document_files\\'+model_id+'\\')
        objdocs=MdlDocs()
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        today = date.today()
        fs = FileSystemStorage()
        print("date--------",str(today))

        objdocs=MdlDocs()
        #Validation template
        validation_template_filename = request.POST.get('validation_template_filename','none')
        if validation_template_filename != 'none':
            print(' validation_template_filename ',validation_template_filename)
            validation_template_file = request.FILES.get('validation_template_file', None)
            print('validation_template_file ',validation_template_file,' validation_template_filename ',validation_template_filename)
            flNm,flExt=os.path.splitext(validation_template_file.name)
            print("check filename",flNm+'_'+str(today),flExt)
            savefile_name_VT = destination_path +flNm+'_'+str(today)+flExt
            fs.save(savefile_name_VT, validation_template_file)
            objdocs.inserDocs(model_id,'1',model_id+'_'+validation_template_file.name,str(request.session['uid']))

        if external_validator != '':
            #detailed validation scope
            detailed_validation_filename = request.POST.get('detailed_validation_filename','none')
            if detailed_validation_filename != 'none':
                detailed_validation_file = request.FILES.get('detailed_validation_file', None)
                print('detailed_validation_file ',detailed_validation_file,' detailed_validation_filename ',detailed_validation_filename)
                flNm_a,flExt_a=os.path.splitext(detailed_validation_file.name)
                savefile_name_dvc = destination_path + flNm_a+'_'+str(today)+flExt_a
                fs.save(savefile_name_dvc, detailed_validation_file)
                objdocs.inserDocs(model_id,'2',model_id+'_'+detailed_validation_file.name,str(request.session['uid']))

            #Validation Contract
            validation_contract_filename = request.POST.get('validation_contract_filename','none')
            if validation_contract_filename != 'none':
                validation_contract_file = request.FILES.get('validation_contract_file', None)
                print('validation_contract_file ',validation_contract_file,' validation_contract_filename ',validation_contract_filename)
                flNm_b,flExt_b=os.path.splitext(validation_contract_file.name)
                savefile_name_vc = destination_path + flNm_b+'_'+str(today)+flExt_b
                fs.save(savefile_name_vc, validation_contract_file)
                objdocs.inserDocs(model_id,'3',model_id+'_'+validation_contract_file.name,str(request.session['uid']))


        comment = request.POST.get('comment','False')
        response = request.POST.get('response','False')
                
        # third_party_api_url = getAPIURL()+'ValidationRatingsTempAPI/'
        third_party_api_url = getAPIURL()+'ValidationPlanningAPI/'
        data_to_save = {
            'mdl_id':model_id,
            'validation_period':validation_period,
            'validation_scope':validation_scope,
            'validator':validator,
            'internal_validator':internal_validator,
            'external_validator':external_validator,
            'projected_start_date':projected_start_date_cnvrt,
            'projected_end_date':projected_end_date_cnvrt,
            'revised_end_date':revised_end_date_cnvrt,
            'previous_total_fees':None if previous_total_fees==''else previous_total_fees ,
            'estimated_total_fees':None if estimated_total_fees==''else estimated_total_fees,
            'actual_total_fees':actual_total_fees,
            'validation_status':validation_status,
            'validation_progress':validation_progress,
            'comment':comment,
            'response':response,
            'addedby':request.session['uid']
        }
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response_data = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
        print("check response",json.loads(response_data.content))
        return JsonResponse(json.loads(response_data.content))
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def SaveNextValidationPlanning(request):
    try:
        print("check request Next Validation",request.POST)
        model_id = request.POST.get('model_id', 'False') 
        validation_period = request.POST.get('validation_period','False')
        validation_scope = request.POST.get('validation_scope','False')

        validator = request.POST.get('validator','False')
        internal_validator = request.POST.get('internal_validator','False')
        external_validator = request.POST.get('external_validator','False')

        projected_start_date = request.POST.get('projected_start_date', 'False')
        projected_start_date_cnvrt = mmddyyyy_to_iso_z(projected_start_date)
        projected_end_date = request.POST.get('projected_end_date','False')
        projected_end_date_cnvrt = mmddyyyy_to_iso_z(projected_end_date)
        
        previous_total_fees = request.POST.get('previous_total_fees',None)
        estimated_total_fees = request.POST.get('estimated_total_fees',None)

        comment = request.POST.get('comment','False')
        response = request.POST.get('response','False')
                
        third_party_api_url = getAPIURL()+'NextValidationPlanningAPI/'
        data_to_save = {
            'mdl_id':model_id,
            'validation_period':validation_period,
            'validation_scope':validation_scope,
            'validator':validator,
            'internal_validator':internal_validator,
            'external_validator':external_validator,
            'projected_start_date':projected_start_date_cnvrt,
            'projected_end_date':projected_end_date_cnvrt,
            'previous_total_fees':None if previous_total_fees==''else previous_total_fees ,
            'estimated_total_fees':None if estimated_total_fees==''else estimated_total_fees,
            'comment':comment,
            'response':response,
            'addedby':request.session['uid']
        }
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response_data = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
        print("check response",json.loads(response_data.content))
        return JsonResponse(json.loads(response_data.content))
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def check_validated_or_not(request):
    try:
        mdl_risk = request.GET.get('mdl_risk', 'False')
        last_val_period = request.GET.get('last_val_period', 'False')
        last_val_period_year = request.GET.get('last_val_period_year', 'False')
        third_party_api_url = getAPIURL()+'check_Validated_or_not/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }

        data_to_get = {
            'mdl_risk':mdl_risk,
            'last_val_period':last_val_period,
            'last_val_period_year': last_val_period_year
        }
        responseget = requests.get(third_party_api_url, data= json.dumps(data_to_get),headers=header)
        data=json.loads(responseget.content)
        print("check data",data)

        return JsonResponse(json.loads(responseget.content))
    except Exception as e:
        print('validation_planning is ',e)
        print('validation_planning traceback is ', traceback.print_exc())
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def CurrentValidation(request):
    mdlId =request.GET.get('mdl_id', 'False') 
    mdl_risk = request.GET.get('mdl_risk','False')
    print("mdl_risk check",mdl_risk)
    api_url_a=getAPIURL()+"ValidationPlanningAPI/"       
    data_to_get={              
        'mdl_id':mdlId} 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    next_val_response = requests.get(api_url_a, data= json.dumps(data_to_get),headers=header)         
    Next_val_api_data = next_val_response.json()
    print("Next_val_api_data",Next_val_api_data)

    # Next Validation API
    try:
        api_url_a=getAPIURL()+"NextValidationPlanningAPI/"       
        data_to_get={              
            'mdl_id':mdlId} 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        next_val_response_new = requests.get(api_url_a, data= json.dumps(data_to_get),headers=header)         
        Next_val_api_data_new = next_val_response_new.json()
        print("Next_val_api_data_New",Next_val_api_data_new)
        # data = {
        #     'model_id':Next_val_api_data['data'][0]['mdl_id'],
        #     'validation_period':Next_val_api_data['data'][0]['validation_period']
        # }
    except Exception as e:
        print("error in next validation",e)
        Next_val_api_data_new = None

        
    return JsonResponse({'data': Next_val_api_data['data'][0],'updated_dates':Next_val_api_data['all_dates'],'curr_dates':Next_val_api_data['curr_dates'],'Next_val_new':Next_val_api_data_new,'isvalid':'true'})


def fetch_val_freq(request):
    mdl_risk = request.GET.get('mdl_risk','False')
    api_url_b=getAPIURL()+"Val_Frequency_Master_API/"       
    data_to_get_a={              
        'mdl_risk':mdl_risk} 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    freq_val_response = requests.get(api_url_b, data= json.dumps(data_to_get_a),headers=header)         
    freq_val_api_data = freq_val_response.json()
    print("freq_val_api_data",freq_val_api_data['val_frequency'])
    return JsonResponse({'data': freq_val_api_data['val_frequency'],'isvalid':'true'})
