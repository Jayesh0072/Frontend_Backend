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

from fpdf import FPDF
from django.conf import settings

objreg=Register()  
objmaster=MasterTbls()
objvalidation=Validation()
objdbops=dbops()
objrmse=RMSEModel() 
from .models import *

def getAPIURL():
    api_url=os.environ['API_URL']
    return api_url


def modelList(request):
    try:
        ty =request.GET.get('ty', 'False') 
        colnm =request.GET.get('colnm', 'False') 
        chartnm =request.GET.get('chartnm', 'False') 
        mdlType =request.GET.get('mdlType', 'None') 
        canAdd=request.session['canAdd']
        # Authorization(request,request.session['ucaid'],'Model Inventory')
        api_url=getAPIURL()+"projectsInfo/"       
        data_to_save={ 
            'uid':request.session['uid'],
            'filterType':ty,
            'filterColumn':chartnm,
            'filterValue':colnm,
            'mdlType':mdlType,
            'istool':'0'} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)         
        api_data=response.json() 
        modelinfo=api_data['modelinfo']#objreg.getModelByFilter(request.session['uid'],ty,chartnm,colnm,'0')
        if ty=='pie' and chartnm=='Model Category':
            modeltype='Model Category - ' +colnm
        elif ty=='pie'  :
            modeltype='Model Type - ' +colnm
        elif ty =='bar':
            modeltype=chartnm +' - '+ colnm
        else:
            modeltype=''
             
        # return render(request, 'addICQQtns.html',{'sections':objmaster.getSections(),'actPage':'RMSE','notifylen':str(len(objvalidation.getVTNotifications(request.session['uid'])))})
        return render(request, 'modelList.html',{'actPage':'RMSE','modelinfo':modelinfo,'canAdd':canAdd,'modeltype':modeltype})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 


def getCriteria(request):
    try:   
        api_url=getAPIURL()+"getCriteria/"    
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, headers=header)         
        api_data=response.json()

        return render(request, 'criteria.html',{ 'actPage':'Select Model/Tool','criteria':api_data['criteria']})
    except Exception as e:
        print('criteriaQtns is ',e)
        print('criteriaQtns traceback is ', traceback.print_exc())


def GetIsModel(request):
    try:
        colDataLst = request.GET['criteria'] 
        qtns = request.GET['qtns'] 
        api_url=getAPIURL()+"GetIsModel/"    
        params={'criteria':colDataLst,
            'qtns':qtns  } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(params),headers=header)        
        api_data=response.json()    
       
        return JsonResponse({'istaken':'true','isModel':api_data['isModel']})
    except Exception as e:
        print('saveModelTool is ',e)
        print('saveModelTool traceback is ', traceback.print_exc())


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
            txtMdlId =request.POST['txtMdlId']
            MdlVersion =request.POST['hdnMdlVersion'] 
            mdlCategory=request.POST['ddlCategory']
            ddlmdl_sub_category=request.POST['ddlmdl_sub_category']
            # ddlModelId
            mdlid= request.POST['mdlid']  
            txtPrdDt = request.POST['txtPrdDt'] 
            txtPrmName = request.POST['txtPrmName'] 
            txtSecName = request.POST['txtSecName'] 
            ddlSource = request.POST['ddlSource'] 
            ddlType = request.POST.get('ddlType','')
            txtMdlAbsct = request.POST['txtMdlAbsct'] 
            txtMdlObj = request.POST['txtMdlObj'] 
            txtMdlAppl = request.POST['txtMdlAppl'] 
            txtMdlRiskAnls = request.POST['txtMdlRiskAnls'] 
            ddlPrctAddr = request.POST.get('ddlPrctAddr','')
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
            txtApproach = '' #request.POST['txtApproach'] 
            ddlMonrFreq ='' # request.POST['ddlMonrFreq'] 
            txtTgrEvt = '' #request.POST['txtTgrEvt'] 
            txtLstTgrDt = '' #request.POST['txtLstTgrDt'] 
            txtLstTgrMtgnDt = '' #request.POST['txtLstTgrMtgnDt'] 
            txtTgrEvtMtgn ='' # request.POST['txtTgrEvtMtgn'] 
            txtMonrMtrcs=''#request.POST['txtMonrMtrcs'] 
            if str(rbisnewupdate)=="0": 
                mdlverInfo=MdlVersion.split('-') 
                objoverview=MdlOverviewCls(txtMdlId,mdlCategory,ddlmdl_sub_category,mdlverInfo[0],mdlverInfo[1],mdlverInfo[2],rbisnewupdate,'0',request.session['dept']
                                        ,ddlFunction,txtPrmName.replace("'","''"),txtSecName.replace("'","''"),ddlSource,ddlType,txtMdlAbsct.replace("'","''"),txtMdlObj.replace("'","''")
                                        ,txtMdlAppl.replace("'","''"),txtMdlRiskAnls.replace("'","''"),ddlPrctAddr,ddlUsgFreq,request.session['uid'],txtPrdDt)
            else:
                objoverview=MdlOverviewCls(txtMdlId,mdlCategory,ddlmdl_sub_category,'1','0','0',rbisnewupdate,'0',request.session['dept']
                                        ,ddlFunction,txtPrmName.replace("'","''"),txtSecName.replace("'","''"),ddlSource,ddlType,txtMdlAbsct.replace("'","''"),txtMdlObj.replace("'","''")
                                        ,txtMdlAppl.replace("'","''"),txtMdlRiskAnls.replace("'","''"),ddlPrctAddr,ddlUsgFreq,request.session['uid'],txtPrdDt)
            mdl_id=objoverview.insertMdlOverview()
            MdlOverview.objects.filter(mdl_id =mdl_id).update(is_submit=1)
 
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

            # objPerformMon=MdlPerformanceMonitoring(mdl_id,txtApproach.replace("'","''"),ddlMonrFreq,txtMonrMtrcs.replace("'","''"),txtTgrEvt.replace("'","''")
            #                                        ,txtLstTgrDt,txtLstTgrMtgnDt,txtTgrEvtMtgn.replace("'","''"),request.session['uid'])
            # objPerformMon.insertPerfomanceMonitor() 
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
            else:
                mdlid = mdlid
                api_data = getDocs(mdlid,'1',request)
                if api_data!="":
                    destination_path_old = os.path.join(BASE_DIR, 'static\\document_files\\'+mdlid+'\\')
                    fs = FileSystemStorage()
                    # savefile_name = destination_path_old + mdlid+'_'+'Laboratory Reports.pdf'
                    savefile_name = destination_path_old + api_data['mdl_doc_name']
                    if os.path.exists(savefile_name):
                        shutil.copy(savefile_name, destination_path)
                    objdocs.inserDocs(mdl_id,'1',api_data['mdl_doc_name'],str(request.session['uid']))

            fl_MD = request.FILES.get('txtUserManual', 'none')             
            if fl_MD != 'none':
                fs = FileSystemStorage()
                savefile_name = destination_path + mdl_id+'_'+fl_MD.name
                if os.path.exists(savefile_name):
                    os.remove(savefile_name)
                fs.save(savefile_name, fl_MD)
                objdocs.inserDocs(mdl_id,'2',mdl_id+'_'+fl_MD.name,str(request.session['uid']))
            else:
                mdlid = mdlid
                api_data = getDocs(mdlid,'2',request)
                if api_data!="":
                    destination_path_old = os.path.join(BASE_DIR, 'static\\document_files\\'+mdlid+'\\')
                    fs = FileSystemStorage()
                    # savefile_name = destination_path_old + mdlid+'_'+'Laboratory Reports.pdf'
                    savefile_name = destination_path_old + api_data['mdl_doc_name']
                    if os.path.exists(savefile_name):
                        shutil.copy(savefile_name, destination_path)
                    objdocs.inserDocs(mdl_id,'2',api_data['mdl_doc_name'],str(request.session['uid']))


            fl_MD = request.FILES.get('txtMdlData', 'none')             
            if fl_MD != 'none':
                fs = FileSystemStorage()
                savefile_name = destination_path + mdl_id+'_'+fl_MD.name
                if os.path.exists(savefile_name):
                    os.remove(savefile_name)
                fs.save(savefile_name, fl_MD)
                objdocs.inserDocs(mdl_id,'3',mdl_id+'_'+fl_MD.name,str(request.session['uid']))
            else:
                mdlid = mdlid
                api_data = getDocs(mdlid,'3',request)
                if api_data!="":
                    destination_path_old = os.path.join(BASE_DIR, 'static\\document_files\\'+mdlid+'\\')
                    fs = FileSystemStorage()
                    # savefile_name = destination_path_old + mdlid+'_'+'Laboratory Reports.pdf'
                    savefile_name = destination_path_old + api_data['mdl_doc_name']
                    if os.path.exists(savefile_name):
                        shutil.copy(savefile_name, destination_path)
                    objdocs.inserDocs(mdl_id,'3',api_data['mdl_doc_name'],str(request.session['uid']))

            fl_MD = request.FILES.get('txtMdlCode', 'none')             
            if fl_MD != 'none':
                fs = FileSystemStorage()
                savefile_name = destination_path + mdl_id+'_'+fl_MD.name
                if os.path.exists(savefile_name):
                    os.remove(savefile_name)
                fs.save(savefile_name, fl_MD)
                objdocs.inserDocs(mdl_id,'4',mdl_id+'_'+fl_MD.name,str(request.session['uid']))
            else:
                mdlid = mdlid
                api_data = getDocs(mdlid,'4',request)
                if api_data!="":
                    destination_path_old = os.path.join(BASE_DIR, 'static\\document_files\\'+mdlid+'\\')
                    fs = FileSystemStorage()
                    # savefile_name = destination_path_old + mdlid+'_'+'Laboratory Reports.pdf'
                    savefile_name = destination_path_old + api_data['mdl_doc_name']
                    if os.path.exists(savefile_name):
                        shutil.copy(savefile_name, destination_path)
                    objdocs.inserDocs(mdl_id,'4',api_data['mdl_doc_name'],str(request.session['uid']))

            
            fl_MD = request.FILES.get('txtUAT', 'none')             
            if fl_MD != 'none':
                fs = FileSystemStorage()
                savefile_name = destination_path + mdl_id+'_'+fl_MD.name
                if os.path.exists(savefile_name):
                    os.remove(savefile_name)
                fs.save(savefile_name, fl_MD)
                objdocs.inserDocs(mdl_id,'5',mdl_id+'_'+fl_MD.name,str(request.session['uid']))
            else:
                mdlid = mdlid
                api_data = getDocs(mdlid,'5',request)
                if api_data!="":
                    destination_path_old = os.path.join(BASE_DIR, 'static\\document_files\\'+mdlid+'\\')
                    fs = FileSystemStorage()
                    # savefile_name = destination_path_old + mdlid+'_'+'Laboratory Reports.pdf'
                    savefile_name = destination_path_old + api_data['mdl_doc_name']
                    if os.path.exists(savefile_name):
                        shutil.copy(savefile_name, destination_path)
                    objdocs.inserDocs(mdl_id,'5',api_data['mdl_doc_name'],str(request.session['uid']))


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
            else:
                mdlid = mdlid
                api_data = getDocs(mdlid,'7',request)
                if api_data!="":
                    destination_path_old = os.path.join(BASE_DIR, 'static\\document_files\\'+mdlid+'\\')
                    fs = FileSystemStorage()
                    # savefile_name = destination_path_old + mdlid+'_'+'Laboratory Reports.pdf'
                    savefile_name = destination_path_old + api_data['mdl_doc_name']
                    if os.path.exists(savefile_name):
                        shutil.copy(savefile_name, destination_path)
                    objdocs.inserDocs(mdl_id,'7',api_data['mdl_doc_name'],str(request.session['uid']))

                
            # print('txtMdlAppl ',txtMdlAppl, ' txtLstTgrMtgnDt ',txtLstTgrMtgnDt,' rbisnewupdate ',rbisnewupdate,request.session['dept'])
            objmaster.insertActivityTrail(mdl_id,"1","New model registered.",request.session['uid'],request.session['accessToken'])
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

        Mdl_Devs =objreg.getUsersByType('Developer')         

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

        third_party_api_url = getAPIURL()+'category_master/'
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response_cat = requests.get(third_party_api_url, headers=header)   
        return render(request, 'registermodel.html',{ 'actPage':'Model Registration','Mdl_Func':Mdl_Func,'Upstr_Model':Upstr_Model,
                    'Dwstr_Model':Dwstr_Model,'Motr_Freq':Motr_Freq,'mdl_id':mdl_id,
                    'mdlinfo':objreg.getModelsbyUserid(request.session['uid']),'Mdl_Devs':Mdl_Devs,
                'Mdl_Validators':Mdl_Validators,'Mdl_Owners':Mdl_Owners,'Reliance':Reliance,
                'Materiality':Materiality,'Intrinsic':Intrinsic,'Mdl_Risk':Mdl_Risk,'Prd_Addr':Prd_Addr,'Mdl_Usage_Frq':Mdl_Usage_Frq,
                'Mdl_Type':Mdl_Type,'Mdl_Src':Mdl_Src,'dept':dept,'regDate':today,'arrFields':arrFields,'category':json.loads(response_cat.content)})
    except Exception as e:
        print('addmodel is ',e)
        print('addmodel traceback is ', traceback.print_exc()) 
        error_saving(request,e)

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
                                    ,txtMdlAppl.replace("'","''"),txtMdlRiskAnls.replace("'","''"),ddlPrctAddr,ddlUsgFreq,request.session['uid'],str(datetime.now))
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


def issubmit(request): 
    
    request_data = {x:request.GET.get(x) for x in request.GET.keys()} 
    mrm_head=objmaster.getMRMHead()
    try:
        issub_obj = MdlOverview.objects.get(mdl_id = request_data['mdl_id'] )#, is_submit__isnull=True
        if issub_obj:       
            print(issub_obj.is_submit)      
            obj = MdlOverview.objects.filter(mdl_id = request_data['mdl_id']).update(is_submit=request_data['is_submit']) 
            print('inside 0 ',  request_data['is_submit'], str(request_data['is_submit'])=="0")        
            if(str(request_data['is_submit'])=="1"):
                notification_trigger= "New model Submitted - " +  request_data['mdl_id']
                objmaster.insert_notification(request.session['uid'],mrm_head,"Model",notification_trigger,1)
                objmaster.insertActivityTrail(request_data['mdl_id'],"2","New model submitted",request.session['uid'],request.session['accessToken'])
            elif(str(request_data['is_submit'])=="2"):
                notification_trigger= "Edit request for - " +  request_data['mdl_id']
                objmaster.insert_notification(request.session['uid'],mrm_head,"Model",notification_trigger,1)
                objmaster.insertActivityTrail(request_data['mdl_id'],"3","Model submitted",request.session['uid'],request.session['accessToken'])
            elif(str(request_data['is_submit'])=="0"):
                notification_trigger= "Edit request approved - " +  request_data['mdl_id']
                
                print('inside 0 ',request.session['uid'],issub_obj.addedby,"Model",notification_trigger,1)
                objmaster.insert_notification(request.session['uid'],issub_obj.addedby,"Model",notification_trigger,1)
                objmaster.insertActivityTrail(request_data['mdl_id'],"4","Model submitted",request.session['uid'],request.session['accessToken'])
            return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print('issubmit is ',e)
        print('issubmit traceback is ', traceback.print_exc())
        return JsonResponse({"isvalid":"false"})

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


def updateMdlVersion(request):
    try:
        mdlid =request.GET.get('mdlid', 'False')
        isMinor =request.GET.get('isMinor', 'False')
        api_url=getAPIURL()+"getMdlDetailsById/"       
        data_to_save={
            'mdl_id':mdlid} 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header) 
        api_data=response.json()  
        newMdlId,mdlVersion = objreg.updateMdlVersion(mdlid,isMinor)
        return JsonResponse({'newMdlId':newMdlId,'mdlVersion':mdlVersion,'regmdldata':api_data})
    except Exception as e:
        print('getMdlInfoById is ',e)
        print('getMdlInfoById traceback is ', traceback.print_exc())

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


from datetime import date, datetime
from dateutil import parser

def generate_request_pdf(request,req_id):
    # req_data_obj = ModelChangeReqData.objects.get(request_id=req_id)

    api_url=getAPIURL()+"pdf_request/"       
    data_to_save={ 
            'uid':request.session['uid'],
            'req_id':req_id} 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url,data= json.dumps(data_to_save),headers=header)         
    req_data_obj=response.json() 
    print("req_data_obj",req_data_obj)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    textarea_fields = {
        "Detailed Description",
        "Rationale for the Change",
        "Intended Benefits",
        "Impact on the Model",
        "Potential Risks",
        "Affected Systems and Processes",
        "Implementation Plan Summary",
        "Testing Plan",
        "Back-out Plan",
        "Resources Required",
        "Conditions/Comments",
        "PIR Findings",
        "Validation Requirement",
        "Completion Sign-off",
    }

    def add_section(title, fields):
        
        # Section header
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 8, title, ln=True, align="L")
        pdf.set_draw_color(0, 0, 0)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)

        # Fields
        for label, value in fields:
            value = str(value) if value else ""
            if label in textarea_fields:
                pdf.set_font("Arial", 'B', 10)

                # Label
                label_text = f"{label}:"
                label_w = 60   
                pdf.cell(label_w, 8, label_text, border=0, ln=0)

                pdf.set_font("Arial", size=10)
                box_w = pdf.w - pdf.r_margin - pdf.get_x()  # remaining width
                line_h = 6
                   
                pdf.multi_cell(box_w, line_h, value if value else " ", border=0, align="L")
                pdf.ln(1)
            else:
                # Normal inline field
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(60, 8, f"{label}:", border=0)
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(130, 8, value, border=0)
                pdf.ln(1)

        pdf.ln(4)

    

    def format_date(value):
        if not value:
            return ""
        if isinstance(value, (date, datetime)):
            return value.strftime("%Y-%m-%d")  
        if isinstance(value, str):
            try:
                print("value data",value)
                dt = parser.parse(value)  
                return dt.strftime("%Y-%m-%d")
            except (ValueError, OverflowError):
                return value.split("T")[0] if "T" in value else value
        print(str(value))
        return str(value)

    # Change Request Details ---
    last_val_dt=format_date( req_data_obj.get("mdl_last_validation"))
    print("dt",last_val_dt)
    dt_obj = datetime.strptime(last_val_dt, "%Y-%m-%d")
    section1 = [
        ("Request ID", req_data_obj.get("request_id")),
        ("Request Date", format_date(req_data_obj.get("request_date"))),
        ("Request Initiator", req_data_obj.get("request_initiator")),
        ("Model Name", req_data_obj.get("mdl_nm")),
        ("Model ID/Version", req_data_obj.get("mdl_id")),
        ("Model Owner", req_data_obj.get("mdl_owner")),
        ("Date of Last Validation",dt_obj.strftime("%m-%Y")),
    ]
    add_section("Change Request Details", section1)

    # Description of Change ---
    section2 = [
        ("Description of Change", req_data_obj.get("desc_change_change_type")),
        ("Detailed Description", req_data_obj.get("desc_change_detailed_desc")),
        ("Rationale for the Change", req_data_obj.get("desc_change_rationale_for_change")),
        ("Intended Benefits", req_data_obj.get("desc_change_intended_benefits")),
    ]
    add_section("Description of Change", section2)

    # Impact and Risk Assessment ---
    section3 = [
        ("Impact on the Model", req_data_obj.get("impact_n_risk_assmnt_impac_on_model")),
        ("Risk Level of the Change", req_data_obj.get("impact_n_risk_assmnt_risk_level_of_change")),
        ("Potential Risks", req_data_obj.get("impact_n_risk_assmnt_potential_risks")),
        ("Affected Systems and Processes", req_data_obj.get("impact_n_risk_assmnt_affected_sys_n_processes")),
    ]
    add_section("Impact and Risk Assessment", section3)

    # Implementation and Testing ---
    section4 = [
        ("Implementation Plan Summary", req_data_obj.get("implementation_and_testing_implementation_plan_summary")),
        ("Testing Plan", req_data_obj.get("implementation_and_testing_testing_plan")),
        ("Back-out Plan", req_data_obj.get("implementation_and_testing_back_out_plan")),
        ("Resources Required", req_data_obj.get("implementation_and_testing_resources_required")),
    ]
    add_section("Implementation and Testing", section4)

    # Review and Approval ---
    section5 = [
        ("Reviewers", req_data_obj.get("review_n_approval_reviewers")),
        ("Review Date",format_date(req_data_obj.get("review_n_approval_review_date"))),
        ("Decision", req_data_obj.get("review_n_approval_decision")),
        ("Conditions/Comments", req_data_obj.get("review_n_approval_conditions_comments")),
    ]
    add_section("Review and Approval", section5)

    # Post-Implementation Review ---
    section6 = [
        ("Date of Implementation",format_date(req_data_obj.get("post_implementation_review_date_of_implementation"))),
        ("PIR Date",format_date(req_data_obj.get("post_implementation_review_pir_date"))),
        ("PIR Findings", req_data_obj.get("post_implementation_review_pir_findings")),
        ("Validation Requirement", req_data_obj.get("post_implementation_review_validation_requirement")),
        ("Signed Off By", req_data_obj.get("sign_off_by")),
        ("Signed Off On",format_date( req_data_obj.get("sign_off_on"))),

    ]
    add_section("Post-Implementation Review", section6)

    # Save 
    folder_path = os.path.join(settings.BASE_DIR, "static", "req_data")
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f"{ req_data_obj.get('request_id')}.pdf")
    pdf.output(file_path)

    return file_path



def pdf_request(request):
    try:

        req_id='M480100Req0002'
        print("req_id",req_id)
        req_pdf_path=generate_request_pdf(request,req_id)
        print("req_pdf_path",req_pdf_path)
     
        return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 


import pandas as pd
import plotly.express as px
import plotly
from django.shortcuts import render
import json

def data_fig_show():
    
    data = {
        'Task': ['Task A', 'Task B', 'Task C', 'Task D', 'Task E'],
        'Start_Baseline': ['2025-01-01', '2025-01-10', '2025-01-20', '2025-02-05', '2025-02-15'],
        'End_Baseline':   ['2025-01-15', '2025-01-25', '2025-02-10', '2025-02-20', '2025-02-28'],
        'Start_Revised':  ['2025-01-01', '2025-01-12', '2025-01-22', '2025-02-08', '2025-02-14'],
        'End_Revised':    ['2025-01-14', '2025-01-28', '2025-02-15', '2025-02-25', '2025-03-05']
    }
    df = pd.DataFrame(data)

    # Baseline (gray bars)
    fig = px.timeline(
        df,
        x_start="Start_Baseline",
        x_end="End_Baseline",
        y="Task",
        color_discrete_sequence=['#cccccc'],
        title="Project Schedule: Baseline vs Revised"
    )

    # Revised (blue bars)
    fig.add_traces(
        px.timeline(
            df,
            x_start="Start_Revised",
            x_end="End_Revised",
            y="Task",
            color_discrete_sequence=['#4285F4']
        ).data
    )

    fig.update_layout(
        showlegend=False,
        plot_bgcolor="#fff0e8",    # background inside chart
        paper_bgcolor="#ffffff",   #outer background
        # title_font=dict(size=18, color="#333333"),
        font=dict(size=12, color="#222222"),
        # width=1000,   # pixels
        # height=500, 
    )

    # Reverse Y axis so Task A is at top
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(showlegend=False)

    return fig


def data_show(request):
    fig = data_fig_show()
    
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render(request, "chart.html", {"fig_json": fig_json})
