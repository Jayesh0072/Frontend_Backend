from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import Users,UserCategory,TaskRegistration,Task_Relevant_Personnel,TaskSummery,Alert,IssueRegistration,IssueRelevantPersonnel
from .serializers import *
from rest_framework.views import APIView
from rest_framework import generics, permissions, status,serializers
 
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
from django.db.models import Max

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

from .RegModel.registermodel import RegisterModel as Register
from .RegModel.registermodel import MdlOverviewCls,ModelRisks,MdlRelevantPersonnelFuncs,MdlDependenciesCls,MdlPerformanceMonitoring,MdlDocs,UserDeatilsSerializers

from .Adm_Utils.Masters import MasterTbls
from .DAL.dboperations import dbops
from .models import *
from .UserInfo.user import UserInfo
from .Validation.validation import Validation
from .RMSE.RMSE import RMSEModel
# import chromadb 

objreg=Register()  
objmaster=MasterTbls()
objvalidation=Validation()
objdbops=dbops()
objrmse=RMSEModel()
from rest_framework.permissions import IsAuthenticated 

class get_AIR_Varwise(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
            prohb_cls=request.data['ClassVar']  
            filterCnd=''
            appovedCndn=getFilterCndn(self,dept,portfolio,'Approved')
            deniedCndn=getFilterCndn(self,dept,portfolio,'Denied')
            approved_and_denied=getFilterCndn(self,dept,portfolio,'Approved and Denied')
             
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']   
             
            filterCnd=getUserFilter(self,uid,portfolio,dept,'Underwriting') 
            leiValue=getFilterCndnNValue(self,dept,portfolio,'Bank ID') 
            if filterCnd !='':
                filterCnd="("+filterCnd +") and"
            filterCnd +=" "+leiValue +" and"
            strQ = "  select added_by,\
                ( SELECT  concat(col_nm,' ',col_oprtr,' ''',col_val,''' and ') \
                from FL_Ctrl_Class_Criteria where added_by="+ str(uid) +" \
                    and Tab_Selected ='Underwriting' FOR XML PATH ('')) as whereclause, \
                ( SELECT  concat(col_nm,' ,') \
                from FL_Ctrl_Class_Criteria where added_by="+ str(uid) +" \
                   and Tab_Selected ='Underwriting'  FOR XML PATH ('')) as colgroup  from FL_Ctrl_Class_Criteria  where added_by="+ str(uid) +" \
                    and Tab_Selected ='Underwriting' group by added_by"        
            tableResult=  self.objdbops.getTable(strQ)  
            arrCols=[]
            arrCols.append(prohb_cls)
            # arrCols=['derived_race','derived_sex','derived_ethnicity','applicant_age']
            arrCtrl_Class=tableResult.values[0][2].split(',')
            mydic=dict()
            dictDOR=dict()
            dictApproved=dict()
            dictDenied=dict()
            for irr in arrCols:
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                strQ="select AIRNum."+ i + " ClsLbl ,(airnum/airdenom)*100 AIR,ttlappl from  (select    ttlData."+ i+ ", \
                isnull(cast( appvd as decimal(7,2) )/ cast( (ttlappl) as decimal(7,2) ),0) \
                AIRNum,ttlappl from    \
                (select   "+ i+ ",count("+ Action_taken_Field+") ttlappl from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" in ("+approved_and_denied+") \
                group by  "+ i+ " )ttlData  left join   \
                ( select "+ i+ ",count("+ Action_taken_Field+") appvd from  FL_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" in ("+appovedCndn+")  \
                group by "+ i+ " ) apprvdData on \
                ttlData."+ i+ " =apprvdData."+ i+ " ) AIRNum, \
                (select   isnull(cast( appvd as decimal(7,2) )/ cast( (ttlappl) as decimal(7,2) ),0)\
                AIRDenom from    \
                ( select "+tableResult.values[0][2]+"count("+ Action_taken_Field+") appvd from  FL_data where "+tableResult.values[0][1]+" \
                 "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "'\
                and "+ Action_taken_Field+" in ("+appovedCndn+") \
                group by "+tableResult.values[0][2]+" "+ activity_year_Field +" ) apprvdData,\
                (select "+tableResult.values[0][2]+"count("+ Action_taken_Field+") ttlappl from FL_data where "+tableResult.values[0][1]+" \
                 "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" in ("+approved_and_denied +") \
                group by  "+tableResult.values[0][2]+" "+ activity_year_Field +" )ttlData \
                where " 
                for ctrlCls in range(0,len(arrCtrl_Class)-1):
                    if  ctrlCls != len(arrCtrl_Class)-2:
                        strQ +=" ttlData."+ arrCtrl_Class[ctrlCls] + " = apprvdData."+arrCtrl_Class[ctrlCls] +" and "
                    else:
                        strQ +=" ttlData."+ arrCtrl_Class[ctrlCls] + " = apprvdData."+arrCtrl_Class[ctrlCls] 
                strQ +=" )AIRDenom   " 
                
                tableResultAIR=  self.objdbops.getTable(strQ)  
                distVals= tableResultAIR.to_json(orient='index')
                distVals=json.loads(distVals)
                mydic['AIR'] = distVals
                del tableResultAIR

                strQ="select AIRNum."+ i+ " ClsLbl ,(airnum/airdenom)*100 DOR from  (select  ttlData."+ i+ ", \
                isnull(cast( denial as decimal(7,2) )/ cast( (appvd) as decimal(7,2) ),0) \
                AIRNum from    \
                (select   "+ i+ ",count("+ Action_taken_Field+") appvd from  FL_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" in ("+appovedCndn+") \
                group by  "+ i+" ,"+ activity_year_Field + " )ttlData left join   \
                ( select "+ i+ ",count("+ Action_taken_Field+") denial from  FL_data where  "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" in ("+deniedCndn+")  \
                group by "+ i+" ,"+ activity_year_Field + " ) apprvdData on \
                ttlData."+ i+ " =apprvdData."+ i+ " ) AIRNum, \
                (select   isnull(cast( denial as decimal(7,2) )/ cast( (appvd) as decimal(7,2) ),0)\
                AIRDenom from    \
                ( select "+tableResult.values[0][2]+"count("+ Action_taken_Field+") denial from  FL_data where "+tableResult.values[0][1]+" \
                 "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "'\
                and "+ Action_taken_Field+" in ("+deniedCndn+") \
                group by "+tableResult.values[0][2]+" "+ activity_year_Field +" ) apprvdData,\
                (select "+tableResult.values[0][2]+"count("+ Action_taken_Field+") appvd from FL_data where "+tableResult.values[0][1]+" \
                 "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" in ("+appovedCndn+") \
                group by  "+tableResult.values[0][2]+" "+ activity_year_Field +" )ttlData \
                where " 
                for ctrlCls in range(0,len(arrCtrl_Class)-1):
                    if  ctrlCls != len(arrCtrl_Class)-2:
                        strQ +=" ttlData."+ arrCtrl_Class[ctrlCls] + " = apprvdData."+arrCtrl_Class[ctrlCls] +" and "
                    else:
                        strQ +=" ttlData."+ arrCtrl_Class[ctrlCls] + " = apprvdData."+arrCtrl_Class[ctrlCls] 
                strQ +=" )AIRDenom   " 
                tableResultDOR=  self.objdbops.getTable(strQ)   
                distDOR= tableResultDOR.to_json(orient='index')
                distDOR=json.loads(distDOR)
                dictDOR['DOR'] = distDOR
                del tableResultDOR 

                strQ="select    ttlData."+ i+" ClsLbl, \
                round(isnull(cast( appvd as decimal(7,2) )/ cast( (ttlappl) as decimal(7,2) ),0)*100,2) \
                apprvd_rate,ttlappl,appvd from    \
                (select   "+ i+ ",count("+ Action_taken_Field+") ttlappl from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" in ("+approved_and_denied+") \
                group by  "+ i+ " )ttlData  left join   \
                ( select "+ i+ ",count("+ Action_taken_Field+") appvd from  FL_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" in ("+appovedCndn+")  \
                group by "+ i+ " ) apprvdData on \
                ttlData."+ i+ " =apprvdData."+ i
                tableResultApproved=  self.objdbops.getTable(strQ)   
                distApproved= tableResultApproved.to_json(orient='index')
                distApproved=json.loads(distApproved)
                dictApproved['AppApproved'] = distApproved
                del tableResultApproved 

                strQ="select    ttlData."+ i+" ClsLbl, \
                round(isnull(cast( denied as decimal(7,2) )/ cast( (ttlappl) as decimal(7,2) ),0)*100,2) \
                denied_rate,ttlappl,denied from    \
                (select   "+ i+ ",count("+ Action_taken_Field+") ttlappl from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" in ("+approved_and_denied+") \
                group by  "+ i+ " )ttlData  left join   \
                ( select "+ i+ ",count("+ Action_taken_Field+") denied from  FL_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" in ("+deniedCndn+")  \
                group by "+ i+ " ) apprvdData on \
                ttlData."+ i+ " =apprvdData."+ i
                tableResultDenied=  self.objdbops.getTable(strQ)   
                distDenied= tableResultDenied.to_json(orient='index')
                distDenied=json.loads(distDenied)
                dictDenied['AppDenied'] = distDenied
                del tableResultDenied 
 
            strFilter=getUserFilter(self,uid,portfolio,dept,'Steering') #"Field_4 = 'PA' or Field_4 = 'NC' and Field_1 = '2023'" 
            filterSelected=strFilter
            res = [i for i in range(len(strFilter)) if strFilter.startswith("Field_", i)]   
            for idx in res:
                startidx=6+idx
                endidx=startidx+2  
                filterSelected=filterSelected.replace("Field_"+str(strFilter[startidx:endidx]),getFLExcelCol(self,"Field_"+str(strFilter[startidx:endidx]),dept,portfolio))
                 

            return JsonResponse({'istaken':'true','AIR':mydic,'DOR':dictDOR,'approved':dictApproved,'denied':dictDenied,'filterSelected':filterSelected })
        except Exception as e:
            print('updateaccess ',e,traceback.print_exc())
            return JsonResponse({'istaken':'false'})
        

class get_Pricing_Dashb_Data_apps_Varwise(APIView): 
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            print("request_data",request.data)
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
            prohb_cls=request.data['ClassVar'] 
            segNm = str(request.data['segNm'])
            filterCnd='' 
            approved_and_denied=getFilterCndn(self,dept,portfolio,'Origination')             
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']    
            userfilterCnd=getUserFilter(self,uid,portfolio,dept,'Pricing_'+prohb_cls,segNm) 
            leiValue=getFilterCndnNValue(self,dept,portfolio,'Bank ID')     
            filterCnd=''     
            arrCols=[]#['derived_race','derived_sex','derived_ethnicity','applicant_age']
            arrCols.append(prohb_cls) 
            dictApplications=dict() 
            ctrlCLsQ,ctrlCLsCols=getUserCtrlClsQuery(self,uid,portfolio,dept,'Pricing_'+prohb_cls) 
            if prohb_cls !="tract_to_msa_income_percentage" and prohb_cls !="tract_minority_population_percent":
                for irr in arrCols: 
                    filterCnd=''
                    if userfilterCnd !='':
                        filterCnd="("+userfilterCnd +") and"
                    filterCnd +=" "+leiValue +" and" 
                    i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                    

                    strQ="select    2,ttlData."+ i+" ClsLbl , \
                    round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float ),0)*100,2) \
                    apprvd_rate,ttlappl,applconverted from    \
                    (select   "+ i+ ",count("+ Action_taken_Field+") ttlappl from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' and  CONCAT("+ctrlCLsCols+") not in( '"+ctrlCLsQ+"') group by  "+ i+ " )ttlData  left join   \
                    ( select "+ i+ ",count("+ Action_taken_Field+") applconverted from  FL_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                    and "+ Action_taken_Field+" in ("+approved_and_denied+")  and  CONCAT("+ctrlCLsCols+") not in( '"+ctrlCLsQ+"') \
                    group by "+ i+ " ) apprvdData on \
                    ttlData."+ i+ " =apprvdData."+ i  +"  union \
                    select    1, '"+ ctrlCLsQ +"' ClsLbl , \
                    round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float ),0)*100,2) \
                    apprvd_rate,ttlappl,applconverted from    \
                    (select  '"+ ctrlCLsQ +"' ClsLbl ,count("+ Action_taken_Field+") ttlappl from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' and  CONCAT("+ctrlCLsCols+")   in( '"+ctrlCLsQ+"')   )ttlData  ,   \
                    ( select '"+ ctrlCLsQ +"' ClsLbl ,count("+ Action_taken_Field+") applconverted from  FL_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                    and "+ Action_taken_Field+" in ("+approved_and_denied+")  and  CONCAT("+ctrlCLsCols+")   in( '"+ctrlCLsQ+"') \
                     ) apprvdData order by 1,2" 
                     
                    tableResultApproved=  self.objdbops.getTable(strQ)    
                    distApplications= tableResultApproved.to_json(orient='index')
                    distApplications=json.loads(distApplications)
                    dictApplications['apps'] = distApplications
                    del tableResultApproved
            elif prohb_cls =="tract_to_msa_income_percentage":
                irr="tract_to_msa_income_percentage"
                filterCnd=''
                if userfilterCnd !='':
                        filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+leiValue +" and"
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                    
                strQ="select  prohb_cls_data.ClsLbl, prohb_cls_data.ttlappl 'ttlappl',ctrl_cls_data.ttlappl 'ctrl_ttlappl',\
                    prohb_cls_data.applconverted 'applconverted',ctrl_cls_data.applconverted 'ctrl_applconverted',  \
                    prohb_cls_data.apprvd_rate 'apprvd_rate',ctrl_cls_data.apprvd_rate 'ctrl_apprvd_rate' from (select ttlapps.incomegrouop 'ClsLbl',ttlappl,isnull(applconverted,0) applconverted,\
                    round(isnull(cast( isnull(applconverted,0) as float)/ cast( (ttlappl) as float),0)*100,2) apprvd_rate from \
                    (select incomegrouop,count(*) ttlappl from ( \
                    select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                    when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                    when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                    when cast("+ i+ " as float)>= 120 then 'Upper' \
                    end incomegrouop from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' and  CONCAT("+ctrlCLsCols+") not in( '"+ctrlCLsQ+"')\
                    )   incomegroupdata group by incomegrouop)ttlapps left join \
                    (select incomegrouop,count(*) applconverted from ( \
                    select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                    when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                    when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                    when cast("+ i+ " as float)>= 120 then 'Upper' \
                    end incomegrouop from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                    and "+ Action_taken_Field+" in ("+approved_and_denied+")  and  CONCAT("+ctrlCLsCols+") not in( '"+ctrlCLsQ+"') )   incomegroupdata group by incomegrouop) convertedapps \
                    on ttlapps.incomegrouop=convertedapps.incomegrouop)  prohb_cls_data left join \
                     (select ttlapps.incomegrouop 'ClsLbl',ttlappl,isnull(applconverted,0) applconverted,\
                    round(isnull(cast( isnull(applconverted,0) as float)/ cast( (ttlappl) as float),0)*100,2) apprvd_rate from \
                    (select incomegrouop,count(*) ttlappl from ( \
                    select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                    when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                    when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                    when cast("+ i+ " as float)>= 120 then 'Upper' \
                    end incomegrouop from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' and  CONCAT("+ctrlCLsCols+")   in( '"+ctrlCLsQ+"')\
                    )   incomegroupdata group by incomegrouop)ttlapps left join \
                    (select incomegrouop,count(*) applconverted from ( \
                    select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                    when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                    when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                    when cast("+ i+ " as float)>= 120 then 'Upper' \
                    end incomegrouop from fl_data where "+filterCnd+"   "+ activity_year_Field +"='"+ activity_year + "' \
                    and "+ Action_taken_Field+" in ("+approved_and_denied+")   and  CONCAT("+ctrlCLsCols+")   in( '"+ctrlCLsQ+"') )   incomegroupdata group by incomegrouop) convertedapps \
                    on ttlapps.incomegrouop=convertedapps.incomegrouop)  ctrl_cls_data on prohb_cls_data.ClsLbl=ctrl_cls_data.ClsLbl "
                
                tableResultApproved=  self.objdbops.getTable(strQ)   
                distApplications= tableResultApproved.to_json(orient='index')
                distApplications=json.loads(distApplications)
                dictApplications['apps'] = distApplications
                del tableResultApproved 
            elif prohb_cls=="tract_minority_population_percent":
                irr="tract_minority_population_percent"
                filterCnd=''
                if userfilterCnd !='':
                        filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+leiValue +" and"
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                strQ="select  prohb_cls_data.ClsLbl, prohb_cls_data.ttlappl 'ttlappl',ctrl_cls_data.ttlappl 'ctrl_ttlappl',\
                    prohb_cls_data.applconverted 'applconverted',ctrl_cls_data.applconverted 'ctrl_applconverted',  \
                    prohb_cls_data.apprvd_rate 'apprvd_rate',ctrl_cls_data.apprvd_rate 'ctrl_apprvd_rate' from  (select ttlapps." + i +" 'ClsLbl',ttlappl,applconverted, \
                    round(isnull(cast( isnull(applconverted,0) as float)/ cast( (ttlappl) as float),0)*100,2) apprvd_rate from \
                    ( \
                    select " + i +", count(*) ttlappl,case   " + i +" when '10%'  then  1 \
                    when '>10% and <=25%'  then 2 \
                    when '>25% and <=50%' then 3 \
                    when   '>50% and <=75%'  then 4 \
                    when  '>75' then 5  \
                    else 6 end ordercol from ( \
                    select    case   when cast(" + i +" as float)<=10 then '10%'   \
                    when  cast(" + i +" as float)>10 and cast(" + i +" as float)<=25 then '>10% and <=25%'   \
                    when  cast(" + i +" as float)>25 and cast(" + i +" as float)<=50 then '>25% and <=50%' \
                    when  cast(" + i +" as float)>50 and cast(" + i +" as float)<=75 then '>50% and <=75%' \
                    when cast(" + i +" as float)>=75 then '>75'  end " + i +"  from \
                    (select " + i +" from fl_data where " + i +"<>'NA'  and "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' ) minortract) a \
                    group by " + i +" \
                    union \
                    select " + i +", count(*) cnt,6  from fl_data where " + i +"='NA' and  "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                    group by " + i +" \
                    ) ttlapps left join  \
                    ( \
                    select " + i +", count(*) applconverted,case   " + i +" when '10%'  then  1 \
                    when '>10% and <=25%'  then 2 \
                    when '>25% and <=50%' then 3 \
                    when   '>50% and <=75%'  then 4 \
                    when  '>75' then 5  \
                    else 6 end  ordercol from ( \
                    select    case   when cast(" + i +" as float)<=10 then '10%'   \
                    when  cast(" + i +" as float)>10 and cast(" + i +" as float)<=25 then '>10% and <=25%'   \
                    when  cast(" + i +" as float)>25 and cast(" + i +" as float)<=50 then '>25% and <=50%' \
                    when  cast(" + i +" as float)>50 and cast(" + i +" as float)<=75 then '>50% and <=75%' \
                    when cast(" + i +" as float)>=75 then '>75'  end " + i +"  from \
                    (select " + i +" from fl_data where " + i +"<>'NA' and  "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "'  and "+ Action_taken_Field+" in ("+approved_and_denied+") and  CONCAT("+ctrlCLsCols+") not in( '"+ctrlCLsQ+"') ) minortract) a \
                    group by " + i +" \
                    union \
                    select " + i +", count(*) cnt,6  from fl_data where " + i +"='NA' and  "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "'  and "+ Action_taken_Field+" in ("+approved_and_denied+") and  CONCAT("+ctrlCLsCols+") not in( '"+ctrlCLsQ+"') \
                    group by " + i +" \
                    ) convertedapps on  ttlapps." + i +"=convertedapps." + i +")  prohb_cls_data left join \
                    (select ttlapps." + i +" 'ClsLbl',ttlappl,applconverted, \
                    round(isnull(cast( isnull(applconverted,0) as float)/ cast( (ttlappl) as float),0)*100,2) apprvd_rate from \
                    ( \
                    select " + i +", count(*) ttlappl,case   " + i +" when '10%'  then  1 \
                    when '>10% and <=25%'  then 2 \
                    when '>25% and <=50%' then 3 \
                    when   '>50% and <=75%'  then 4 \
                    when  '>75' then 5  \
                    else 6 end ordercol from ( \
                    select    case   when cast(" + i +" as float)<=10 then '10%'   \
                    when  cast(" + i +" as float)>10 and cast(" + i +" as float)<=25 then '>10% and <=25%'   \
                    when  cast(" + i +" as float)>25 and cast(" + i +" as float)<=50 then '>25% and <=50%' \
                    when  cast(" + i +" as float)>50 and cast(" + i +" as float)<=75 then '>50% and <=75%' \
                    when cast(" + i +" as float)>=75 then '>75'  end " + i +"  from \
                    (select " + i +" from fl_data where " + i +"<>'NA'  and "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' and  CONCAT("+ctrlCLsCols+")   in( '"+ctrlCLsQ+"') ) minortract) a \
                    group by " + i +" \
                    union \
                    select " + i +", count(*) cnt,6  from fl_data where " + i +"='NA' and  "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' and  CONCAT("+ctrlCLsCols+")   in( '"+ctrlCLsQ+"') \
                    group by " + i +" \
                    ) ttlapps left join  \
                    ( \
                    select " + i +", count(*) applconverted,case   " + i +" when '10%'  then  1 \
                    when '>10% and <=25%'  then 2 \
                    when '>25% and <=50%' then 3 \
                    when   '>50% and <=75%'  then 4 \
                    when  '>75' then 5  \
                    else 6 end  ordercol from ( \
                    select    case   when cast(" + i +" as float)<=10 then '10%'   \
                    when  cast(" + i +" as float)>10 and cast(" + i +" as float)<=25 then '>10% and <=25%'   \
                    when  cast(" + i +" as float)>25 and cast(" + i +" as float)<=50 then '>25% and <=50%' \
                    when  cast(" + i +" as float)>50 and cast(" + i +" as float)<=75 then '>50% and <=75%' \
                    when cast(" + i +" as float)>=75 then '>75'  end " + i +"  from \
                    (select " + i +" from fl_data where " + i +"<>'NA' and  "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "'  and "+ Action_taken_Field+" in ("+approved_and_denied+") and  CONCAT("+ctrlCLsCols+")   in( '"+ctrlCLsQ+"') ) minortract) a \
                    group by " + i +" \
                    union \
                    select " + i +", count(*) cnt,6  from fl_data where " + i +"='NA' and  "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "'  and "+ Action_taken_Field+" in ("+approved_and_denied+") and  CONCAT("+ctrlCLsCols+")   in( '"+ctrlCLsQ+"') \
                    group by " + i +" \
                    ) convertedapps on  ttlapps." + i +"=convertedapps." + i +")      ctrl_cls_data on prohb_cls_data.ClsLbl=ctrl_cls_data.ClsLbl "
                
                tableResultApproved=  self.objdbops.getTable(strQ)   
                distApplications= tableResultApproved.to_json(orient='index')
                distApplications=json.loads(distApplications)
                dictApplications['apps'] = distApplications
                del tableResultApproved 
                
            strFilter=getUserFilter(self,uid,portfolio,dept,'Pricing_'+prohb_cls,segNm) #"Field_4 = 'PA' or Field_4 = 'NC' and Field_1 = '2023'" 
            filterSelected=strFilter
            res = [i for i in range(len(strFilter)) if strFilter.startswith("Field_", i)]   
            for idx in res:
                startidx=6+idx
                endidx=startidx+2  
                filterSelected=filterSelected.replace("Field_"+str(strFilter[startidx:endidx]),getFLExcelCol(self,"Field_"+str(strFilter[startidx:endidx]),dept,portfolio))
               
            return JsonResponse({'istaken':'true','apps':dictApplications,'filterSelected':filterSelected })
        except Exception as e:
            print('updateaccess ',e,traceback.print_exc())
            return JsonResponse({'istaken':'false'})
   
class get_Pricing_Dashb_Data_ratespread_Varwise(APIView): 
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept']) 
            ratespread = str(request.data['ratespread'])
            prohb_cls=request.data['ClassVar'] 
            segNm = str(request.data['segNm'])      
            filterCnd='' 
            approved_and_denied=getFilterCndn(self,dept,portfolio,'Origination')             
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']    
            userfilterCnd=getUserFilter(self,uid,portfolio,dept,'Pricing_'+prohb_cls,segNm) 
            
            leiValue=getFilterCndnNValue(self,dept,portfolio,'Bank ID') 
            strQ = "  select added_by,\
                ( SELECT  concat(col_nm,' ',col_oprtr,' ''',col_val,''' and ') \
                from FL_Ctrl_Class_Criteria where added_by="+ str(uid) +" \
                    and Tab_Selected ='Pricing' FOR XML PATH ('')) as whereclause, \
                ( SELECT  concat(col_nm,' ,') \
                from FL_Ctrl_Class_Criteria where added_by="+ str(uid) +" \
                   and Tab_Selected ='Pricing'  FOR XML PATH ('')) as colgroup  from FL_Ctrl_Class_Criteria  where added_by="+ str(uid) +" \
                    and Tab_Selected ='Pricing' group by added_by"        
            tableResult=  self.objdbops.getTable(strQ)  
            # arrCols=['derived_race','derived_sex','derived_ethnicity','applicant_age']
            arrCtrl_Class=tableResult.values[0][2].split(',')    
            filterCnd=''     
            arrCols=[]#['derived_race','derived_sex','derived_ethnicity','applicant_age']
            arrCols.append(prohb_cls)
            rate_spread_col=getFLDbCol(self,'rate_spread',dept,portfolio)
            dictApplications=dict() 
            strQ=" select  cast( aboveRateSpread as decimal(7,2))/cast( ctrlclsorg as decimal(7,2))*100 AIR  from   "                             
            strQ +=" ( select "+tableResult.values[0][2]+"count("+ Action_taken_Field+")  aboveRateSpread from  FL_data where "
            strQ +=" "+tableResult.values[0][1]+" "+filterCnd+ "  cast(case when "+rate_spread_col+"='NA' then Null else "+rate_spread_col+" end as float) >= "+ratespread + " and "+ activity_year_Field +"='"+ activity_year + "' "            
            strQ +=" and  "+ Action_taken_Field+" in ("+approved_and_denied +")               group by "+tableResult.values[0][2]+" "+ activity_year_Field +" ) AIRNum right join   "
            strQ +=" (  select "+tableResult.values[0][2]+"count("+ Action_taken_Field+")  ctrlclsorg from  FL_data where "+tableResult.values[0][1]+"   "             
            strQ +=" "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' and  "+ Action_taken_Field+" in ("+approved_and_denied +") "   
            strQ +=" group by "+tableResult.values[0][2]+" "+ activity_year_Field +" ) AIRDenom on    "

            for ctrlCls in range(0,len(arrCtrl_Class)-1):
                if  ctrlCls != len(arrCtrl_Class)-2:
                    strQ +=" AIRDenom."+ arrCtrl_Class[ctrlCls] + " = AIRNum."+arrCtrl_Class[ctrlCls] +" and "
                else:
                    strQ +=" AIRDenom."+ arrCtrl_Class[ctrlCls] + " = AIRNum."+arrCtrl_Class[ctrlCls] 
            denomCtrlCls= self.objdbops.getscalar(strQ) 
            ctrlCLsQ,ctrlCLsCols=getUserCtrlClsQuery(self,uid,portfolio,dept,'Pricing_'+prohb_cls) 
            if prohb_cls !="tract_to_msa_income_percentage" and   prohb_cls !="tract_minority_population_percent":
                for irr in arrCols: 
                    filterCnd=''
                    if userfilterCnd !='':
                        filterCnd="("+userfilterCnd +") and"
                    filterCnd +=" "+leiValue +" and"  
                    
                    i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                    

                    strQ="select   2, ttlData."+ i+" ClsLbl, \
                    round(isnull(cast( isnull(applconverted,0) as float)/ cast( (ttlappl) as float ),0)*100,2) \
                    apprvd_rate,ttlappl,isnull(applconverted,0) applconverted,isnull(fieldavg,0)fieldavg  from    \
                    (select   "+ i+ ",count("+ Action_taken_Field+") ttlappl from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "'\
                     and  CONCAT("+ctrlCLsCols+") not in( '"+ctrlCLsQ+"')   group by  "+ i+ " )ttlData  left join   \
                    ( select "+ i+ ",count("+ Action_taken_Field+") applconverted,avg( cast(case when "+rate_spread_col+"='NA' then Null else "+rate_spread_col+" end as float) ) fieldavg from  FL_data where "+filterCnd+ "  cast(case when "+rate_spread_col+"='NA' then Null else "+rate_spread_col+" end as float) >= "+ratespread + " and "+ activity_year_Field +"='"+ activity_year + "' \
                    and "+ Action_taken_Field+" in ("+approved_and_denied+")  and  CONCAT("+ctrlCLsCols+") not in( '"+ctrlCLsQ+"')  \
                    group by "+ i+ " ) apprvdData on \
                    ttlData."+ i+ " =apprvdData."+ i +" union \
                    select    1, '"+ ctrlCLsQ +"' ClsLbl, \
                    round(isnull(cast( isnull(applconverted,0) as float)/ cast( (ttlappl) as float ),0)*100,2) \
                    apprvd_rate,ttlappl,isnull(applconverted,0) applconverted,isnull(fieldavg,0)fieldavg  from    \
                    (select     '"+ ctrlCLsQ +"' ClsLbl ,count("+ Action_taken_Field+") ttlappl from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "'\
                     and  CONCAT("+ctrlCLsCols+")  in( '"+ctrlCLsQ+"')  )ttlData ,  \
                    ( select  '"+ ctrlCLsQ +"' ClsLbl ,count("+ Action_taken_Field+") applconverted,avg( cast(case when "+rate_spread_col+"='NA' then Null else "+rate_spread_col+" end as float) ) fieldavg from  FL_data where "+filterCnd+ "  cast(case when "+rate_spread_col+"='NA' then Null else "+rate_spread_col+" end as float) >= "+ratespread + " and "+ activity_year_Field +"='"+ activity_year + "' \
                    and "+ Action_taken_Field+" in ("+approved_and_denied+")  and  CONCAT("+ctrlCLsCols+")  in( '"+ctrlCLsQ+"')  \
                      ) apprvdData  order by 1,2 "
                    print("pricing query",strQ)
                    tableResultApproved=  self.objdbops.getTable(strQ)  
                    distApplications= tableResultApproved.to_json(orient='index')
                    distApplications=json.loads(distApplications)
                    dictApplications['apps'] = distApplications
                    del tableResultApproved      
                
            
            elif prohb_cls =="tract_to_msa_income_percentage":
                irr="tract_to_msa_income_percentage"
                filterCnd=''
                if userfilterCnd !='':
                        filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+leiValue +" and"
                
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                    
                strQ="select  prohb_cls_data.ClsLbl, prohb_cls_data.ttlappl 'ttlappl',ctrl_cls_data.ttlappl 'ctrl_ttlappl',\
                    prohb_cls_data.applconverted 'applconverted',ctrl_cls_data.applconverted 'ctrl_applconverted',  \
                    prohb_cls_data.apprvd_rate 'apprvd_rate',ctrl_cls_data.apprvd_rate 'ctrl_apprvd_rate',isnull(fieldavg,0)fieldavg ,isnull(ctrl_fieldavg,0) ctrl_fieldavg from (select ttlapps.incomegrouop 'ClsLbl',ttlappl,isnull(applconverted,0) applconverted,\
                    round(isnull(cast( isnull(applconverted,0) as float)/ cast( (ttlappl) as float),0)*100,2) apprvd_rate,fieldavg from \
                    (select incomegrouop,count(*) ttlappl from ( \
                    select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                    when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                    when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                    when cast("+ i+ " as float)>= 120 then 'Upper' \
                    end incomegrouop from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' and  CONCAT("+ctrlCLsCols+") not in( '"+ctrlCLsQ+"')\
                    )   incomegroupdata group by incomegrouop)ttlapps left join \
                    (select incomegrouop,count(*) applconverted, avg(isnull(fieldavg,0)) fieldavg from ( \
                    select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                    when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                    when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                    when cast("+ i+ " as float)>= 120 then 'Upper' \
                    end incomegrouop,cast(case when "+rate_spread_col+"='NA' then Null else "+rate_spread_col+" end as float) fieldavg from fl_data where "+filterCnd+"  cast(case when "+rate_spread_col+"='NA' then Null else "+rate_spread_col+" end as float) >= "+ratespread + " and "+ activity_year_Field +"='"+ activity_year + "' \
                    and "+ Action_taken_Field+" in ("+approved_and_denied+")  and  CONCAT("+ctrlCLsCols+") not in( '"+ctrlCLsQ+"') )   incomegroupdata group by incomegrouop) convertedapps \
                    on ttlapps.incomegrouop=convertedapps.incomegrouop)  prohb_cls_data left join \
                     (select ttlapps.incomegrouop 'ClsLbl',ttlappl,isnull(applconverted,0) applconverted,\
                    round(isnull(cast( isnull(applconverted,0) as float)/ cast( (ttlappl) as float),0)*100,2) apprvd_rate,ctrl_fieldavg from \
                    (select incomegrouop,count(*) ttlappl from ( \
                    select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                    when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                    when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                    when cast("+ i+ " as float)>= 120 then 'Upper' \
                    end incomegrouop from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' and  CONCAT("+ctrlCLsCols+")   in( '"+ctrlCLsQ+"')\
                    )   incomegroupdata group by incomegrouop)ttlapps left join \
                    (select incomegrouop,count(*) applconverted, avg(isnull(ctrl_fieldavg,0)) ctrl_fieldavg from ( \
                    select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                    when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                    when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                    when cast("+ i+ " as float)>= 120 then 'Upper' \
                    end incomegrouop,cast(case when "+rate_spread_col+"='NA' then Null else "+rate_spread_col+" end as float) ctrl_fieldavg from fl_data where "+filterCnd+"  cast(case when "+rate_spread_col+"='NA' then Null else "+rate_spread_col+" end as float) >= "+ratespread + " and "+ activity_year_Field +"='"+ activity_year + "' \
                    and "+ Action_taken_Field+" in ("+approved_and_denied+")   and  CONCAT("+ctrlCLsCols+")   in( '"+ctrlCLsQ+"') )   incomegroupdata group by incomegrouop) convertedapps \
                    on ttlapps.incomegrouop=convertedapps.incomegrouop)  ctrl_cls_data on prohb_cls_data.ClsLbl=ctrl_cls_data.ClsLbl "
           
                tableResultApproved=  self.objdbops.getTable(strQ)   
                distApplications= tableResultApproved.to_json(orient='index')
                distApplications=json.loads(distApplications)
                dictApplications['apps'] = distApplications
                del tableResultApproved  
            elif prohb_cls=="tract_minority_population_percent":
                irr="tract_minority_population_percent"
                filterCnd=''
                if userfilterCnd !='':
                        filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+leiValue +" and"
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                strQ="select  prohb_cls_data.ClsLbl, prohb_cls_data.ttlappl 'ttlappl',ctrl_cls_data.ttlappl 'ctrl_ttlappl',\
                    prohb_cls_data.applconverted 'applconverted',ctrl_cls_data.applconverted 'ctrl_applconverted',  \
                    prohb_cls_data.apprvd_rate 'apprvd_rate',ctrl_cls_data.apprvd_rate 'ctrl_apprvd_rate',fieldavg,ctrl_fieldavg from  (\
                    select ttlapps." + i +" 'ClsLbl',ttlappl,applconverted, \
                    round(isnull(cast( isnull(applconverted,0) as float)/ cast( (ttlappl) as float),0)*100,2) apprvd_rate, isnull(fieldavg,0) fieldavg from \
                    ( \
                    select " + i +", count(*) ttlappl,case   " + i +" when '10%'  then  1 \
                    when '>10% and <=25%'  then 2 \
                    when '>25% and <=50%' then 3 \
                    when   '>50% and <=75%'  then 4 \
                    when  '>75' then 5  \
                    else 6 end ordercol from ( \
                    select    case   when cast(" + i +" as float)<=10 then '10%'   \
                    when  cast(" + i +" as float)>10 and cast(" + i +" as float)<=25 then '>10% and <=25%'   \
                    when  cast(" + i +" as float)>25 and cast(" + i +" as float)<=50 then '>25% and <=50%' \
                    when  cast(" + i +" as float)>50 and cast(" + i +" as float)<=75 then '>50% and <=75%' \
                    when cast(" + i +" as float)>=75 then '>75'  end " + i +"  from \
                    (select * from fl_data where " + i +"<>'NA'  and "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' ) minortract) a \
                    group by " + i +" \
                    union \
                    select " + i +", count(*) cnt ,6  from fl_data where " + i +"='NA' and  "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                    group by " + i +" \
                    ) ttlapps left join  \
                    ( \
                    select " + i +", count(*) applconverted, avg(isnull(fieldavg,0)) fieldavg,case   " + i +" when '10%'  then  1 \
                    when '>10% and <=25%'  then 2 \
                    when '>25% and <=50%' then 3 \
                    when   '>50% and <=75%'  then 4 \
                    when  '>75' then 5  \
                    else 6 end  ordercol from ( \
                    select    case   when cast(" + i +" as float)<=10 then '10%'   \
                    when  cast(" + i +" as float)>10 and cast(" + i +" as float)<=25 then '>10% and <=25%'   \
                    when  cast(" + i +" as float)>25 and cast(" + i +" as float)<=50 then '>25% and <=50%' \
                    when  cast(" + i +" as float)>50 and cast(" + i +" as float)<=75 then '>50% and <=75%' \
                    when cast(" + i +" as float)>=75 then '>75'  end " + i +",cast(case when "+rate_spread_col+"='NA' then Null else "+rate_spread_col+" end as float)  fieldavg  from \
                    (select * from fl_data where " + i +"<>'NA' and  "+filterCnd+"  cast(case when "+rate_spread_col+"='NA' then Null else "+rate_spread_col+" end as float) >= "+ratespread + " and "+activity_year_Field +"='"+ activity_year + "'  and "+ Action_taken_Field+" in ("+approved_and_denied+") and  CONCAT("+ctrlCLsCols+") not in( '"+ctrlCLsQ+"') ) minortract) a \
                    group by " + i +" \
                    union \
                    select " + i +", count(*) cnt, isnull(avg (cast( "+rate_spread_col+" as float)),0)    fieldavg,6  from fl_data where " + i +"='NA' and  "+filterCnd+"  cast(case when "+rate_spread_col+"='NA' then Null else "+rate_spread_col+" end as float) >= "+ratespread + " and "+activity_year_Field +"='"+ activity_year + "'  and "+ Action_taken_Field+" in ("+approved_and_denied+") and  CONCAT("+ctrlCLsCols+") not in( '"+ctrlCLsQ+"') \
                    group by " + i +" \
                    ) convertedapps on  ttlapps." + i +"=convertedapps." + i +")  prohb_cls_data left join \
                    (select ttlapps." + i +" 'ClsLbl',ttlappl,applconverted, \
                    round(isnull(cast( isnull(applconverted,0) as float)/ cast( (ttlappl) as float),0)*100,2) apprvd_rate, isnull(ctrl_fieldavg,0) ctrl_fieldavg from \
                    ( \
                    select " + i +", count(*) ttlappl,case   " + i +" when '10%'  then  1 \
                    when '>10% and <=25%'  then 2 \
                    when '>25% and <=50%' then 3 \
                    when   '>50% and <=75%'  then 4 \
                    when  '>75' then 5  \
                    else 6 end ordercol from ( \
                    select    case   when cast(" + i +" as float)<=10 then '10%'   \
                    when  cast(" + i +" as float)>10 and cast(" + i +" as float)<=25 then '>10% and <=25%'   \
                    when  cast(" + i +" as float)>25 and cast(" + i +" as float)<=50 then '>25% and <=50%' \
                    when  cast(" + i +" as float)>50 and cast(" + i +" as float)<=75 then '>50% and <=75%' \
                    when cast(" + i +" as float)>=75 then '>75'  end " + i +"   from \
                    (select * from fl_data where " + i +"<>'NA'  and "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' and  CONCAT("+ctrlCLsCols+")   in( '"+ctrlCLsQ+"') ) minortract) a \
                    group by " + i +" \
                    union \
                    select " + i +", count(*) cnt,6  from fl_data where " + i +"='NA' and  "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' and  CONCAT("+ctrlCLsCols+")   in( '"+ctrlCLsQ+"') \
                    group by " + i +" \
                    ) ttlapps left join  \
                    ( \
                    select " + i +", count(*) applconverted, avg(isnull(ctrl_fieldavg,0)) ctrl_fieldavg,case   " + i +" when '10%'  then  1 \
                    when '>10% and <=25%'  then 2 \
                    when '>25% and <=50%' then 3 \
                    when   '>50% and <=75%'  then 4 \
                    when  '>75' then 5  \
                    else 6 end  ordercol from ( \
                    select    case   when cast(" + i +" as float)<=10 then '10%'   \
                    when  cast(" + i +" as float)>10 and cast(" + i +" as float)<=25 then '>10% and <=25%'   \
                    when  cast(" + i +" as float)>25 and cast(" + i +" as float)<=50 then '>25% and <=50%' \
                    when  cast(" + i +" as float)>50 and cast(" + i +" as float)<=75 then '>50% and <=75%' \
                    when cast(" + i +" as float)>=75 then '>75'  end " + i +" ,cast(case when "+rate_spread_col+"='NA' then Null else "+rate_spread_col+" end as float) ctrl_fieldavg from  (select * from fl_data "
                strQ+=" where " + i +"<>'NA'  and  "+filterCnd +"  cast(case when "+ rate_spread_col +"='NA' then Null else "+ rate_spread_col +" end as float) >= "+ratespread + " and "+ activity_year_Field +"='"+ activity_year + "'  and "+ Action_taken_Field+" in ("+approved_and_denied+") and  CONCAT("+ctrlCLsCols+")   in( '"+ctrlCLsQ+"') ) minortract) a \
                    group by " + i +" \
                    union \
                    select " + i +", count(*) cnt,isnull(avg (cast( "+rate_spread_col+" as float)),0)   ctrl_fieldavg,6  from fl_data where " + i +"='NA' and  "+filterCnd+"  cast(case when "+rate_spread_col+"='NA' then Null else "+rate_spread_col+" end as float) >= "+ratespread + " and "+ activity_year_Field +"='"+ activity_year + "'  and "+ Action_taken_Field+" in ("+approved_and_denied+") and  CONCAT("+ctrlCLsCols+")   in( '"+ctrlCLsQ+"') \
                    group by " + i +" \
                    ) convertedapps on  ttlapps." + i +"=convertedapps." + i +")      ctrl_cls_data on prohb_cls_data.ClsLbl=ctrl_cls_data.ClsLbl "
                print(strQ)
                tableResultApproved=  self.objdbops.getTable(strQ)   
                distApplications= tableResultApproved.to_json(orient='index')
                distApplications=json.loads(distApplications)
                dictApplications['apps'] = distApplications
                del tableResultApproved 
                
            
            return JsonResponse({'istaken':'true','apps':dictApplications,'denomCtrlCls':denomCtrlCls  })
        except Exception as e:
            print('updateaccess ',e,traceback.print_exc())
            return JsonResponse({'istaken':'false'})
 
class get_Steering_Dashb_Data_apps_Varwise(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
            prohb_cls=request.data['ClassVar'] 
            segNm = str(request.data['segNm'])  
            filterCnd='' 
            approved_and_denied=getFilterCndn(self,dept,portfolio,'Approved and Denied')             
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']    
            userfilterCnd=getUserFilter(self,uid,portfolio,dept,'Steering',segNm) 
            leiValue=getFilterCndnNValue(self,dept,portfolio,'Bank ID')    
            peerGroupLei=getFilterCndnNValue(self,dept,portfolio,'Peer Group')    
            filterCnd=''     
            arrCols=[]#['derived_race','derived_sex','derived_ethnicity','applicant_age']
            arrCols.append(prohb_cls)
            dictApplications=dict() 
            if prohb_cls !="tract_to_msa_income_percentage":
                for irr in arrCols: 
                    filterCnd=''
                    if userfilterCnd !='':
                        filterCnd="("+userfilterCnd +") and"
                    filterCnd +=" "+leiValue +" and" 
                    i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                    

                    strQ="select    ttlData."+ i+" ClsLbl, \
                    round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float ),0)*100,2) \
                    apprvd_rate,ttlappl,applconverted from    \
                    (select   "+ i+ ",count("+ Action_taken_Field+") ttlappl from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' group by  "+ i+ " )ttlData  left join   \
                    ( select "+ i+ ",count("+ Action_taken_Field+") applconverted from  FL_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                    and "+ Action_taken_Field+" in ("+approved_and_denied+")  \
                    group by "+ i+ " ) apprvdData on \
                    ttlData."+ i+ " =apprvdData."+ i 
                    
                    tableResultApproved=  self.objdbops.getTable(strQ)  
                    distApplications= tableResultApproved.to_json(orient='index')
                    distApplications=json.loads(distApplications)
                    dictApplications['apps'] = distApplications
                    del tableResultApproved     
            elif prohb_cls =="tract_to_msa_income_percentage":
                irr="tract_to_msa_income_percentage"
                filterCnd=''
                if userfilterCnd !='':
                        filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+leiValue +" and"
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                    
                strQ="select ttlapps.incomegrouop 'ClsLbl',ttlappl,applconverted,\
                    round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float),0)*100,2) apprvd_rate from \
                    (select incomegrouop,count(*) ttlappl from ( \
                    select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                    when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                    when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                    when cast("+ i+ " as float)>= 120 then 'Upper' \
                    end incomegrouop from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                    )   incomegroupdata group by incomegrouop)ttlapps left join \
                    (select incomegrouop,count(*) applconverted from ( \
                    select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                    when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                    when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                    when cast("+ i+ " as float)>= 120 then 'Upper' \
                    end incomegrouop from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                    and "+ Action_taken_Field+" in ("+approved_and_denied+")   )   incomegroupdata group by incomegrouop) convertedapps \
                    on ttlapps.incomegrouop=convertedapps.incomegrouop" 
                
                tableResultApproved=  self.objdbops.getTable(strQ)  
                distApplications= tableResultApproved.to_json(orient='index')
                distApplications=json.loads(distApplications)
                dictApplications['apps'] = distApplications
                del tableResultApproved 

            strFilter=getUserFilter(self,uid,portfolio,dept,'Steering',segNm) #"Field_4 = 'PA' or Field_4 = 'NC' and Field_1 = '2023'" 
            filterSelected=strFilter
            res = [i for i in range(len(strFilter)) if strFilter.startswith("Field_", i)]   
            for idx in res:
                startidx=6+idx
                endidx=startidx+2  
                filterSelected=filterSelected.replace("Field_"+str(strFilter[startidx:endidx]),getFLExcelCol(self,"Field_"+str(strFilter[startidx:endidx]),dept,portfolio))

            dictPeerApplications=dict() 
            if prohb_cls !="tract_to_msa_income_percentage":
                for irr in arrCols:  
                    i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                    
                    filterCnd=''
                    userfilterCnd=getUserFilterPeerApplication(self,uid,portfolio,dept,'Steering') 
                    
                    if userfilterCnd !='':
                        filterCnd="("+userfilterCnd +") and"
                    filterCnd +=" "+peerGroupLei +" and"
                    strQ="select    ttlData."+ i+" ClsLbl, \
                    round(isnull(cast( peerconverted as float)/ cast( (peerapps) as  float),0)*100,2) \
                    conversion_rate,peerapps,peerconverted from    \
                    (select   "+ i+ ",count("+ Action_taken_Field+") peerapps from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' group by  "+ i+ " )ttlData  left join   \
                    ( select "+ i+ ",count("+ Action_taken_Field+") peerconverted from  FL_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                    and "+ Action_taken_Field+" in ("+approved_and_denied+")  \
                    group by "+ i+ " ) apprvdData on \
                    ttlData."+ i+ " =apprvdData."+ i  
                    tableResultDenied=  self.objdbops.getTable(strQ)   
                    distDenied= tableResultDenied.to_json(orient='index')
                    distDenied=json.loads(distDenied)
                    dictPeerApplications['peergroupapps'] = distDenied
                    del tableResultDenied 
            elif prohb_cls =="tract_to_msa_income_percentage":
                irr="tract_to_msa_income_percentage"
                
                filterCnd=''
                userfilterCnd=getUserFilterPeerApplication(self,uid,portfolio,dept,'Steering') 
                if userfilterCnd !='':
                        filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+peerGroupLei +" and"
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                    
                strQ="select ttlapps.incomegrouop 'ClsLbl',ttlappl,applconverted 'peerconverted',\
                    round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float),0)*100,2) conversion_rate  from \
                    (select incomegrouop,count(*) ttlappl from ( \
                    select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                    when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                    when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                    when cast("+ i+ " as float)>= 120 then 'Upper' \
                    end incomegrouop from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                    )   incomegroupdata group by incomegrouop)ttlapps left join \
                    (select incomegrouop,count(*) applconverted from ( \
                    select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                    when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                    when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                    when cast("+ i+ " as float)>= 120 then 'Upper' \
                    end incomegrouop from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                    and "+ Action_taken_Field+" in ("+approved_and_denied+")   )   incomegroupdata group by incomegrouop) convertedapps \
                    on ttlapps.incomegrouop=convertedapps.incomegrouop" 
                 
                tableResultApproved=  self.objdbops.getTable(strQ)   
                distApplications= tableResultApproved.to_json(orient='index')
                distApplications=json.loads(distApplications)
                dictPeerApplications['peergroupapps'] = distApplications
                del tableResultApproved 

            governmentApps=getFilterCndnNValue(self,dept,portfolio,'Government Application')     
            filterCnd=''             
            dictGovApplications=dict() 
            if prohb_cls !="tract_to_msa_income_percentage":
                for irr in arrCols: 
                    
                    i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                    
                    #Goverment apps query
                    filterCnd=''
                    userfilterCnd=userfilterCnd=getUserFilter(self,uid,portfolio,dept,'Steering',segNm) 
                    if userfilterCnd !='':
                        filterCnd="("+userfilterCnd +") and"
                    filterCnd +=" "+leiValue +" and "  
                    strQ="select    ttlData."+ i+" ClsLbl , \
                    round(isnull(cast( govApps as decimal(7,2) )/ cast( (ttlappl) as decimal(7,2) ),0)*100,2) \
                    apprvd_rate,ttlappl,govApps from    \
                    (select   "+ i+ ",count("+ Action_taken_Field+") ttlappl from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' group by  "+ i+ " )ttlData  left join   \
                    ( select "+ i+ ",count("+ Action_taken_Field+") govApps from  FL_data where "+filterCnd+" " +governmentApps+ " and  "+ activity_year_Field +"='"+ activity_year + "' \
                    and "+ Action_taken_Field+" in ("+approved_and_denied+")  \
                    group by "+ i+ " ) apprvdData on \
                    ttlData."+ i+ " =apprvdData."+ i  
                    tableResultApproved=  self.objdbops.getTable(strQ)   
                    distGovApplications= tableResultApproved.to_json(orient='index')
                    distGovApplications=json.loads(distGovApplications)
                    dictGovApplications['appsGov'] = distGovApplications
                    del tableResultApproved 
    
            elif prohb_cls =="tract_to_msa_income_percentage":
                irr="tract_to_msa_income_percentage"   
                filterCnd=''
                userfilterCnd=userfilterCnd=getUserFilter(self,uid,portfolio,dept,'Steering',segNm) 
                if userfilterCnd !='':
                        filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+leiValue +" and  " +governmentApps+ " and "
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                    
                strQ="select ttlapps.incomegrouop 'ClsLbl',ttlappl,applconverted 'govApps',\
                    round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float),0)*100,2) apprvd_rate  from \
                    (select incomegrouop,count(*) ttlappl from ( \
                    select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                    when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                    when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                    when cast("+ i+ " as float)>= 120 then 'Upper' \
                    end incomegrouop from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                    )   incomegroupdata group by incomegrouop)ttlapps left join \
                    (select incomegrouop,count(*) applconverted from ( \
                    select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                    when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                    when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                    when cast("+ i+ " as float)>= 120 then 'Upper' \
                    end incomegrouop from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                    and "+ Action_taken_Field+" in ("+approved_and_denied+")   )   incomegroupdata group by incomegrouop) convertedapps \
                    on ttlapps.incomegrouop=convertedapps.incomegrouop" 
                
                tableResultApproved=  self.objdbops.getTable(strQ)   
                distApplications= tableResultApproved.to_json(orient='index')
                distApplications=json.loads(distApplications)
                dictGovApplications['appsGov'] = distApplications
                del tableResultApproved 

            dictGovPeerApplications=dict() 
            if prohb_cls !="tract_to_msa_income_percentage":
                for irr in arrCols:               
                    i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                    filterCnd=''
                    userfilterCnd=getUserFilterPeerApplication(self,uid,portfolio,dept,'Steering') 
                    if userfilterCnd !='':
                        filterCnd="("+userfilterCnd +") and"
                    filterCnd +=" "+peerGroupLei +" and "
                    strQ="select    ttlData."+ i+" ClsLbl, \
                    round(isnull(cast( peerappsGov as float )/ cast( (peerapps) as float ),0)*100,2) \
                    conversion_rate,peerapps,peerappsGov from    \
                    (select   "+ i+ ",count("+ Action_taken_Field+") peerapps from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' group by  "+ i+ " )ttlData  left join   \
                    ( select "+ i+ ",count("+ Action_taken_Field+") peerappsGov from  FL_data where "+filterCnd+" " +governmentApps+ " and    "+ activity_year_Field +"='"+ activity_year + "' \
                    and "+ Action_taken_Field+" in ("+approved_and_denied+")  \
                    group by "+ i+ " ) apprvdData on \
                    ttlData."+ i+ " =apprvdData."+ i 
                    tableResultDenied=  self.objdbops.getTable(strQ)   
                    distGovPeerGroup= tableResultDenied.to_json(orient='index')
                    distGovPeerGroup=json.loads(distGovPeerGroup)
                    dictGovPeerApplications['peergroupappsGov'] = distGovPeerGroup
                    del tableResultDenied  
            elif prohb_cls =="tract_to_msa_income_percentage":    
                irr="tract_to_msa_income_percentage" 
                filterCnd=''
                userfilterCnd=getUserFilterPeerApplication(self,uid,portfolio,dept,'Steering') 
                if userfilterCnd !='':
                        filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+peerGroupLei +" and  " +governmentApps+ " and "
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                    
                strQ="select ttlapps.incomegrouop 'ClsLbl',ttlappl,applconverted 'govApps',\
                    round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float),0)*100,2) apprvd_rate  from \
                    (select incomegrouop,count(*) ttlappl from ( \
                    select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                    when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                    when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                    when cast("+ i+ " as float)>= 120 then 'Upper' \
                    end incomegrouop from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                    )   incomegroupdata group by incomegrouop)ttlapps left join \
                    (select incomegrouop,count(*) applconverted from ( \
                    select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                    when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                    when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                    when cast("+ i+ " as float)>= 120 then 'Upper' \
                    end incomegrouop from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                    and "+ Action_taken_Field+" in ("+approved_and_denied+")   )   incomegroupdata group by incomegrouop) convertedapps \
                    on ttlapps.incomegrouop=convertedapps.incomegrouop"  
                tableResultApproved=  self.objdbops.getTable(strQ)   
                distApplications= tableResultApproved.to_json(orient='index')
                distApplications=json.loads(distApplications)
                dictGovPeerApplications['peergroupappsGov'] = distApplications
                del tableResultApproved  
 
            return JsonResponse({'istaken':'true','apps':dictApplications,'filterSelected':filterSelected , 'peergroupapps':dictPeerApplications, 'appsGov':dictGovApplications , 'peergroupappsGov':dictGovPeerApplications  })
        except Exception as e:
            print('updateaccess ',e,traceback.print_exc())
            return JsonResponse({'istaken':'false'})

class get_Denials_Varwise(APIView): 
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
            prohb_cls=request.data['ClassVar']     
            filterCnd='' 
            
            deniedCndn=getFilterCndn(self,dept,portfolio,'Denied')         
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']    
            userfilterCnd=getUserFilter(self,uid,portfolio,dept,'Pricing') 
            
            leiValue=getFilterCndnNValue(self,dept,portfolio,'Bank ID')  
            arrColsRatio=['combined_loan_to_value_ratio']#,'debt_to_income' 
            arrColsVals=['income','loan_amount']#'denial_reason_1',
            arrcolsDdlvals=['denial_reason_1','loan_purpose']   
            filterCnd=''   
            dictApplications=dict()  
            if prohb_cls in arrColsVals:
                irr= prohb_cls 
                filterCnd=''
                if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+leiValue +" and"  
                
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                
                if prohb_cls =='loan_amount': 
                    strQ=" select incomegrouop 'ClsLbl',count(*) denied,ordcol from ( "
                    strQ+="    select  case   when cast("+ i+ " as float)/1000<=100 then '<=100  K' "
                    strQ+="    when  cast("+ i+ " as float)/1000 > 100 and cast("+ i+ " as float)/1000<= 250 then '>100 and <=250  K' "
                    strQ+="   when  cast("+ i+ " as float)/1000 > 250 and cast("+ i+ " as float)/1000<= 500 then '>250 and <=500  K'  "
                    strQ+="   when  cast("+ i+ " as float)/1000 > 500 and cast("+ i+ " as float)/1000<= 750 then '>500 and <=750  K'  "
                    strQ+="     when  cast("+ i+ " as float)/1000 > 750 and cast("+ i+ " as float)/1000<= 1000 then '>750 and <1000  K'  "
                    strQ+="    when cast("+ i+ " as float)/1000> 1000 then '>1000  K'  end incomegrouop ,"
                    strQ+="    case   when cast("+ i+ " as float)/1000<=100 then 0 when  cast("+ i+ " as float)/1000> 100 and cast("+ i+ " as float)/1000<= 250 then 1 "          
                    strQ+="    when  cast("+ i+ " as float)/1000 > 250 and cast("+ i+ " as float)/1000<= 500 then 2   "
                    strQ+="    when  cast("+ i+ " as float)/1000 >  500 and cast("+ i+ " as float)/1000<= 750 then 3 "
                    strQ+="    when  cast("+ i+ " as float)/1000 > 750 and cast("+ i+ " as float)/1000<= 1000 then 4  " 
                    strQ+="    when cast("+ i+ " as float)/1000> 1000 then 5  "   
                    strQ+="    end  ordcol  from fl_data where "+filterCnd+"     "+ activity_year_Field +"='"+ activity_year + "'   and  "+i+"<>'NA'  "
                    strQ+="    and "+ Action_taken_Field+" in ("+deniedCndn+")   )   incomegroupdata group by incomegrouop ,ordcol"
                    strQ+="    union          select 'NA' ,count(*),10 from fl_data where  "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' and  "
                    strQ+=    i+"<>'NA' and "+ Action_taken_Field+" in ("+deniedCndn+")  order by 3 "   
                else:
                    strQ=" select incomegrouop 'ClsLbl',count(*) denied,ordcol from ( "
                    strQ+="    select  case   when cast("+ i+ " as float)<=100 then '<=100 K'"
                    strQ+="    when  cast("+ i+ " as float)> 100 and cast("+ i+ " as float)<= 250 then '>100 and <=250 K' "
                    strQ+="   when  cast("+ i+ " as float)> 250 and cast("+ i+ " as float)<= 500 then '>250 and <=500 K'  "
                    strQ+="   when  cast("+ i+ " as float)> 500 and cast("+ i+ " as float)<= 750 then '>500 and <=750 K'  "
                    strQ+="     when  cast("+ i+ " as float)> 750 and cast("+ i+ " as float)<= 1000 then '>750 and <1000 K'  "
                    strQ+="    when cast("+ i+ " as float)> 1000 then '>1000 K'  end incomegrouop ,"
                    strQ+="    case   when cast("+ i+ " as float)<=100 then 0 when  cast("+ i+ " as float)> 100 and cast("+ i+ " as float)<= 250 then 1 "          
                    strQ+="    when  cast("+ i+ " as float)> 250 and cast("+ i+ " as float)<= 500 then 2   "
                    strQ+="    when  cast("+ i+ " as float)> 500 and cast("+ i+ " as float)<= 750 then 3 "
                    strQ+="    when  cast("+ i+ " as float)> 750 and cast("+ i+ " as float)<= 1000 then 4  " 
                    strQ+="    when cast("+ i+ " as float)> 1000 then 5  "   
                    strQ+="    end  ordcol  from fl_data where "+filterCnd+"     "+ activity_year_Field +"='"+ activity_year + "'   and  "+i+"<>'NA'  "
                    strQ+="    and "+ Action_taken_Field+" in ("+deniedCndn+")   )   incomegroupdata group by incomegrouop ,ordcol"
                    strQ+="    union          select 'NA' ,count(*),10 from fl_data where  "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' and  "
                    strQ+=    i+"<>'NA' and "+ Action_taken_Field+" in ("+deniedCndn+")  order by 3 "   
            
                tableResultApproved=  self.objdbops.getTable(strQ)   
                distApplications= tableResultApproved.to_json(orient='index')
                distApplications=json.loads(distApplications)
                dictApplications['denials'] = distApplications
                del tableResultApproved      
                
            
            elif prohb_cls in arrColsRatio:
                irr=prohb_cls
                filterCnd=''
                if userfilterCnd !='':
                        filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+leiValue +" and"
                
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                    
                strQ=" select incomegrouop 'ClsLbl',count(*) denied,ordrcol   from ( \
                    select  case   when cast("+ i+ " as float)<=25 then '<=25' \
                    when  cast("+ i+ " as float)> 25 and cast("+ i+ " as float)<= 50 then '>25 and <=50' \
                    when  cast("+ i+ " as float)> 50 and cast("+ i+ " as float)<= 75 then '>50 and <=75'  \
                     when  cast("+ i+ " as float)> 75 and cast("+ i+ " as float)<= 100 then '>75 and <=100'  \
                    when cast("+ i+ " as float)> 100 then '>100' \
                    end incomegrouop ,  case   when cast("+ i+ " as float)<=25 then 1\
                    when  cast("+ i+ " as float)> 25 and cast("+ i+ " as float)<= 50 then 2 \
                    when  cast("+ i+ " as float)> 50 and cast("+ i+ " as float)<= 75 then 3 \
                     when  cast("+ i+ " as float)> 75 and cast("+ i+ " as float)<= 100 then 4  \
                    when cast("+ i+ " as float)> 100 then 5 \
                    end ordrcol from fl_data where "+filterCnd+"     "+ activity_year_Field +"='"+ activity_year + "'   and  "+i+"<>'NA'  \
                    and "+ Action_taken_Field+" in ("+deniedCndn+")   )   incomegroupdata group by incomegrouop ,ordrcol \
                    union          select 'NA' ,count(*) ,10 from fl_data where  "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' and  "+i+"<>'NA' and "+ Action_taken_Field+" in ("+deniedCndn+")  order by 3  "               
                 
                tableResultApproved=  self.objdbops.getTable(strQ)   
                distApplications= tableResultApproved.to_json(orient='index')
                distApplications=json.loads(distApplications)
                dictApplications['denials'] = distApplications
                del tableResultApproved  
            elif prohb_cls in arrcolsDdlvals:
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+prohb_cls+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                if prohb_cls=='denoal_reason_1':
                    strQ=" select   \
                        case  "+ i+ " when   1 then 'Debt-to-income ratio'\
                        when   2 then  'Employment history'\
                        when   3 then  'Credit history'\
                        when  4 then  'Collateral'\
                        when   5 then  'Insufficient cash (downpayment, closing costs)'\
                        when   6 then  'Unverifiable information'\
                        when  7 then  'Credit application incomplete'\
                        when   8 then  'Mortgage insurance denied'\
                        when  9 then  'Other'\
                        when   10 then  'Not applicable'\
                            else  "+ i+ "  end 'ClsLbl' ,count("+ Action_taken_Field+") denied from  FL_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                     and "+ Action_taken_Field+" in ("+deniedCndn+")  \
                    group by "+ i
                else:
                    strQ=" select   \
                        case  "+ i+ " when   1 then 'Debt-to-income ratio'\
                        when   2 then  'Home purchase'\
                        when   31 then  'Home improvement'\
                        when  4 then  'Other purpose'\
                        when   5 then  'Not applicable'\
                        when  32 then  ' Cash-out refinancing' else "+ i+ " end 'ClsLbl' ,count("+ Action_taken_Field+") denied from  FL_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                     and "+ Action_taken_Field+" in ("+deniedCndn+")  \
                    group by "+ i 
                 
                tableResultApproved=  self.objdbops.getTable(strQ)   
                distApplications= tableResultApproved.to_json(orient='index')
                distApplications=json.loads(distApplications)
                dictApplications['denials'] = distApplications
                del tableResultApproved  
            return JsonResponse({'istaken':'true','apps':dictApplications   })
        except Exception as e:
            print('updateaccess ',e,traceback.print_exc())
            return JsonResponse({'istaken':'false'})
 

def getFLDbCol(self,excelcol,dept,portfolio):     
    return  self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Mapping_Details fl_map_dtl where  lower(Excel_Fields)=lower('"+excelcol+"') and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'")  
    # self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+excelcol+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 

def getFLExcelCol(self,dbcol,dept,portfolio):     
    return  self.objdbops.getscalar("select fl_map_dtl.Excel_Fields from FL_Mapping_Details fl_map_dtl where  lower(Database_Fields)=lower('"+dbcol+"') and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'")  
   
def getFilterCndn(self,dept,portfolio,cndn):
    return str(self.objdbops.getscalar("SELECT  Value filter_cndn FROM  FL_Value_Details where portfolio='"+ portfolio +"' and department='"+ str(dept) +"' and filter_condition='"+ cndn +"'"))

def getFilterCndnNValue(self,dept,portfolio,cndn):
    return str(self.objdbops.getscalar("SELECT  concat(Database_Fields,' ',Operator,' ',Value) filter_cndn FROM  FL_Value_Details where portfolio='"+ portfolio +"' and department='"+ str(dept) +"' and filter_condition='"+ cndn +"'"))

# def getUserFilter(self,uid,portfolio,dept,utility):
#     # strQ="select isnull(max(filter_Condn),'') filter_Condn from FL_Filter_Criteria where added_by="+ str(uid) +" and portfolio='"+ portfolio +"' and department='"+ str(dept) +"'"
#     strCnt="select  count(*) filter_Condn from FL_Filter_Criteria where \
#             added_by="+ str(uid) +" and portfolio='"+ portfolio +"' and department='"+ str(dept) +"' and utility='"+utility+"'"    
    
    
#     if str(self.objdbops.getscalar(strCnt))=="0":
#         return  " Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"' "
#     else:
#         strQ="select  isnull((filter_Condn),'')  filter_Condn from FL_Filter_Criteria where \
#             added_by="+ str(uid) +" and portfolio='"+ portfolio +"' and department='"+ str(dept) +"' and utility='"+utility+"'"    
#         return  "Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"' and " +self.objdbops.getscalar(strQ) 

def getUserFilter(self,uid,portfolio,dept,utility,segNm="",forDisplay="False"):
    # strQ="select isnull(max(filter_Condn),'') filter_Condn from FL_Filter_Criteria where added_by="+ str(uid) +" and portfolio='"+ portfolio +"' and department='"+ str(dept) +"'"
    strCnt="select  count(*) filter_Condn from FL_Filter_Criteria where \
            added_by="+ str(uid) +" and portfolio='"+ portfolio +"' and department='"+ str(dept) +"' and utility='"+utility+"'"    
    print(segNm,',',segNm != "")
    if str(self.objdbops.getscalar(strCnt))=="0":
        return  " Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"' "
    else:

        strQ="select  isnull((filter_Condn),'')  filter_Condn from FL_Filter_Criteria where \
            added_by="+ str(uid) +" and portfolio='"+ portfolio +"' and department='"+ str(dept) +"' and utility='"+utility+"'"  
        if segNm != "":
            strQ +=" and segment_name='"+segNm+"'"
        print(strQ)
        if (forDisplay == 'True'):
            return   self.objdbops.getscalar(strQ)  
        else:
            return  "Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"' and (" +self.objdbops.getscalar(strQ) +")" 



def getUserFilterPeerApplication(self,uid,portfolio,dept,utility):
    # strQ="select isnull(max(filter_Condn),'') filter_Condn from FL_Filter_Criteria where added_by="+ str(uid) +" and portfolio='"+ portfolio +"' and department='"+ str(dept) +"'"
    strQ="select  isnull((filter_Condn),'') +' '+ case when lei_selected is null then ''else 'and '+lei_selected end  filter_Condn from FL_Filter_Criteria where \
          added_by="+ str(uid) +" and portfolio='"+ portfolio +"' and department='"+ str(dept) +"' and utility='"+utility+"'"
    return self.objdbops.getscalar(strQ) 

 
def getUserCtrlCls(self,uid,portfolio,dept,utilty):
    strCnt=" select count(*) colgroup  from FL_Ctrl_Class_Criteria  where added_by="+ str(uid) +" \
                    and Tab_Selected ='"+ utilty +"' "  
    if str(self.objdbops.getscalar(strCnt))=="0":
        return pd.DataFrame()
    else:
        strQ = "  select added_by,\
                    ( SELECT  concat(col_nm,' ',col_oprtr,' ''',col_val,''' and ') \
                    from FL_Ctrl_Class_Criteria where added_by="+ str(uid) +" \
                        and Tab_Selected ='"+ utilty +"' FOR XML PATH ('')) as whereclause, \
                    ( SELECT  concat(col_nm,' ,') \
                    from FL_Ctrl_Class_Criteria where added_by="+ str(uid) +" \
                    and Tab_Selected ='"+ utilty +"'  FOR XML PATH ('')) as colgroup  from FL_Ctrl_Class_Criteria  where added_by="+ str(uid) +" \
                        and Tab_Selected ='"+ utilty +"' group by added_by"    
        tableResult=  self.objdbops.getTable(strQ)  
        return tableResult 
    
def getUserCtrlClsQuery(self,uid,portfolio,dept,utilty):
    strCnt=" select count(*) colgroup  from FL_Ctrl_Class_Criteria  where added_by="+ str(uid) +" \
                    and Tab_Selected ='"+ utilty +"' "  
    ctrlCLsQ=""
    ctrlCLsCols=""
    print(strCnt)
    if str(self.objdbops.getscalar(strCnt))=="0":
        return ctrlCLsQ,ctrlCLsCols
    else:
        strQ = "  select added_by,\
                    ( SELECT  concat(col_val,':')  \
                    from FL_Ctrl_Class_Criteria where added_by="+ str(uid) +" \
                        and Tab_Selected ='"+ utilty +"' FOR XML PATH ('')) as whereclause, \
                    ( SELECT  concat(col_nm,','':'',')  \
                    from FL_Ctrl_Class_Criteria where added_by="+ str(uid) +" \
                    and Tab_Selected ='"+ utilty +"'  FOR XML PATH ('')) as colgroup  from FL_Ctrl_Class_Criteria  where added_by="+ str(uid) +" \
                        and Tab_Selected ='"+ utilty +"' group by added_by"  
        
        strCtrlCls=  self.objdbops.getTable(strQ)   
        if   strCtrlCls.empty  ==False:
            ctrlCLsQ=strCtrlCls.values[0][1]
            ctrlCLsQ = ctrlCLsQ[:-1]
            ctrlCLsCols=strCtrlCls.values[0][2]
            ctrlCLsCols = ctrlCLsCols[:-5] 
        return ctrlCLsQ ,ctrlCLsCols
    
