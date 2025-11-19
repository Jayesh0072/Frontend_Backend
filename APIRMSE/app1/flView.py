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

objreg=Register()  
objmaster=MasterTbls()
objvalidation=Validation()
objdbops=dbops()
objrmse=RMSEModel()
from rest_framework.permissions import IsAuthenticated 
# import chromadb 
 
class getFL_Tbl_Cols(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def get(self,request):
        strQ = " SELECT  Column_Name ColumnName FROM INFORMATION_SCHEMA.COLUMNS wHERE TABLE_NAME ='FL_data'"
        
        tableResult=  self.objdbops.getTable(strQ)  
        commenthistory= tableResult.to_json(orient='index')   
        return Response(json.loads(commenthistory))

class getFL_Ctrl_Class_Cols(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def get(self,request):
        portfolio = request.data['Portfolio']  
        dept = str(request.data['Dept']) 
        strQ = "SELECT Ctrl_Label ColumnName ,Database_Fields FROM FL_Control_class_Master  ctrl_cls_mst,FL_Field_Details fl_fld_dtl \
                where Excel_Fields=Ctrl_Label and  ctrl_cls_mst.Portfolio ='"+ portfolio +"' and ctrl_cls_mst.department='"+ str(dept) +"'" 
        print(strQ)
        tableResult=  self.objdbops.getTable(strQ)  
        commenthistory= tableResult.to_json(orient='index')   
        return Response({'ColumnName':json.loads(commenthistory)})


class getDistinct_Col_Val(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def get(self,request):
        portfolio = request.data['Portfolio']  
        dept = str(request.data['Dept'])  
        activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
        strQ = " select distinct("+ request.data['colName']+") distVals from   FL_data where "+ activity_year_Field +"='"+ request.data['activity_year']+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'"        
        tableResult=  self.objdbops.getTable(strQ)  
        if len(tableResult)<=50:
            distVals= tableResult.to_json(orient='index')
            distVals=json.loads(distVals)
                
        else:
            import ast                        
            distVals=ast.literal_eval("{'0': {'distVals': 'UserInput'}}")
        print(type(distVals))     
        return Response({'distVals':distVals})


class insert_Ctrl_Class_Criteria(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            uid = request.data['uid'] 
            tabSelected = request.data['tabSelected']  
            colDataLst = request.data['datalist']   
            
            strQ="delete from FL_Ctrl_Class_Criteria where Tab_Selected ='"+ tabSelected +"' and Added_By="+str(uid) 
            objdbops.insertRow(strQ) 

            for colval in colDataLst: 
                print(colval)
                strQ="INSERT INTO FL_Ctrl_Class_Criteria ( Col_Nm , Col_Oprtr , Col_Val , Added_By , Added_On ,Tab_Selected) \
                VALUES ('"+ colval['Col_Nm']+"' ,'"+ colval['Col_Oprtr']+"' ,'"+colval['Col_Val']+"' ,'"+ str(uid) +"' ,getdate(),'"+ tabSelected +"')"
                self.objdbops.insertRow(strQ)
            return JsonResponse({'istaken':'true'})
        except Exception as e:
            print('updateaccess ',e,traceback.print_exc())
            return JsonResponse({'istaken':'false'})

class get_AIR(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
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
            arrCols=['derived_race','derived_sex','derived_ethnicity','applicant_age']
            arrCtrl_Class=tableResult.values[0][2].split(',')
            mydic=dict()
            dictDOR=dict()
            dictApproved=dict()
            dictDenied=dict()
            for irr in arrCols:
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                strQ="select AIRNum."+ i + " "+irr+" ,(airnum/airdenom)*100 AIR,ttlappl from  (select    ttlData."+ i+ ", \
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
                # print('col ',i )
                # print(tableResultAIR)
                distVals= tableResultAIR.to_json(orient='index')
                distVals=json.loads(distVals)
                mydic[irr] = distVals
                del tableResultAIR

                strQ="select AIRNum."+ i+ " "+irr+" ,(airnum/airdenom)*100 DOR from  (select  ttlData."+ i+ ", \
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
                # print('col ',i )
                # print(tableResultAIR) 
                distDOR= tableResultDOR.to_json(orient='index')
                distDOR=json.loads(distDOR)
                dictDOR[irr] = distDOR
                del tableResultDOR 

                strQ="select    ttlData."+ i+" "+irr+ ", \
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
                # print('col ',i )
                # print(tableResultAIR) 
                distApproved= tableResultApproved.to_json(orient='index')
                distApproved=json.loads(distApproved)
                dictApproved[irr] = distApproved
                del tableResultApproved 

                strQ="select    ttlData."+ i+" "+irr+ ", \
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
                # print('col ',i )
                # print(tableResultAIR) 
                distDenied= tableResultDenied.to_json(orient='index')
                distDenied=json.loads(distDenied)
                dictDenied[irr] = distDenied
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


class GET_FL_Data_Info(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        dept=request.data['dept']
        portfolio=request.data['portfolio']
        utility=request.data.get('utility','Steering')
        uid=request.data['uid']
        from pandas.api.types import is_numeric_dtype,is_float_dtype,is_integer_dtype,is_string_dtype,is_number  
        strFilter=getUserFilter(self,uid,portfolio,dept,utility,"",'True') #"Field_4 = 'PA' or Field_4 = 'NC' and Field_1 = '2023'" 
        if strFilter !="":
            filterSelected=strFilter
            res = [i for i in range(len(strFilter)) if strFilter.startswith("Field_", i)]   
            for idx in res:
                startidx=6+idx
                endidx=startidx+2  
                filterSelected=filterSelected.replace("Field_"+str(strFilter[startidx:endidx]),getFLExcelCol(self,"Field_"+str(strFilter[startidx:endidx]),dept,portfolio))
        else:
            filterSelected='Not selected.'
        strCtrlCls=getUserCtrlCls(self,uid,portfolio,dept,utility) 
        if   strCtrlCls.empty  ==False:
            strCtrlCls=strCtrlCls.values[0][1]
            strCtrlCls = strCtrlCls[:-4]
            strCtrlClsSel=strCtrlCls
            res = [i for i in range(len(strCtrlCls)) if strCtrlCls.startswith("Field_", i)]   
            for idx in res:
                startidx=6+idx
                endidx=startidx+2  
                strCtrlClsSel=strCtrlClsSel.replace("Field_"+str(strCtrlCls[startidx:endidx]),getFLExcelCol(self,"Field_"+str(strCtrlCls[startidx:endidx]),dept,portfolio))
        else:
            strCtrlClsSel="Not set"
        filterSelected="Control Class : "+strCtrlClsSel+" , Filter : "   +filterSelected  
        strQ = " SELECT Excel_Fields  ,Database_Fields  ,Field_datatype  FROM FL_Field_Details  where portfolio='"+ request.data['portfolio']+"' and department='"+str(request.data['dept'])+"'"        
         

        df=  self.objdbops.getTable(strQ)  
        gridDttypes=[] 
        for index, row in  df.iterrows():   
            minmax=[]         
            valueLst=[]      
            if row['Field_datatype']=="number": 
                # print("select concat(isnull(min(cast("+row['Database_Fields']+" as float)),0)  ,'-',isnull(max(cast("+row['Database_Fields']+" as float)),0) ) minmaxval from fl_data  where portfolio='"+ request.data['portfolio']+"' and department='"+str(request.data['dept'])+"'" )
                # minmaxvals=self.objdbops.getscalar("select concat(isnull(min(cast("+row['Database_Fields']+" as float)),0)  ,'-',isnull(max(cast("+row['Database_Fields']+" as float)),0) ) minmaxval from fl_data  where portfolio='"+ request.data['portfolio']+"' and department='"+str(request.data['dept'])+"'" )
                minmax=[]
                value="integer"  
            elif  row['Field_datatype']=="bool":
                value="boolean"
                valueLst=['True','False','Null']
            else:
                value="string"
                dfDistinctVals=self.objdbops.getTable("select  distinct("+row['Database_Fields']+") stringCol from fl_data  where portfolio='"+ request.data['portfolio']+"' and department='"+str(request.data['dept'])+"'" )
                if len(dfDistinctVals)<=200: 
                    valueLst=dfDistinctVals["stringCol"].astype(str).unique().tolist() 
                del dfDistinctVals        
         
            gridDttypes.append({'colName': row["Excel_Fields"],'dbColName':row['Database_Fields'] ,'dataType': str(value),'valueLst':valueLst,'minmax':minmax})  
        
        peergrouplei=getFilterCndnNValue(self,dept,portfolio,'Peer Group')   
        dbfield=getFLDbCol(self,'lei',dept,portfolio) 
        strQ = " SELECT distinct  "+ str(dbfield)+" peerlei  FROM FL_data  where "+ peergrouplei+ " and portfolio='"+ request.data['portfolio']+"' and department='"+ str(request.data['dept'])+"'"     
        print(strQ)     
        df=  self.objdbops.getTable(strQ)  
        dfresult= df.to_json(orient='index')
        dfresult=json.loads(dfresult)
        del df
        return JsonResponse({'gridDttypes':gridDttypes,'peerlei':dfresult,'filterSelected':filterSelected})
       
class GET_FL_Data_Filter_Cnt(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        from pandas.api.types import is_numeric_dtype,is_float_dtype,is_integer_dtype,is_string_dtype,is_number 
        print(request.data)
        portfolio = request.data['Portfolio']  
        dept = str(request.data['Dept'])
        activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
        Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")  
        strQ = " select  count(*) from   FL_data where "+ activity_year_Field +"='"+ request.data['activity_year']+"' and "+ Action_taken_Field+" in (1,3) "     
        ttlCnt=  self.objdbops.getscalar(strQ)  

        strQ = " select  count(*) from   FL_data where "+ activity_year_Field +"='"+ request.data['activity_year']+"' and "+ Action_taken_Field+" in (1,3)  and ("+ request.data['filter_cndn']+")"     
        filterCnt=  self.objdbops.getscalar(strQ)  
         
        return JsonResponse({"all_count":ttlCnt,"filter_cnt":filterCnt})
       
class Save_FL_Data_Filter_Cndn(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request): 
        dept=str(request.data['dept'])
        portfolio=request.data['portfolio']
        utility=request.data['utiltity']
        segNm=request.data['segNm']
        strQ = " delete from FL_Filter_Criteria  where Added_By = '"+ str(request.data['uid'])+"' and portfolio='"+portfolio+"' and department='"+dept+"' and utility='"+utility+"' and segment_name='"+segNm+"'"     
        self.objdbops.insertRow(strQ)

        strQ = " INSERT INTO    FL_Filter_Criteria  ( Filter_Condn , Added_By  , Added_On,portfolio,department,utility,segment_name )  VALUES ('"+ request.data['filter_cndn'].replace("'","''")+"','"+ str(request.data['uid'])+"',getdate(),'"+portfolio+"','"+dept+"','"+utility+"','"+segNm+"')"     
        self.objdbops.insertRow(strQ)
        strFilter=getUserFilter(self,str(request.data['uid']),portfolio,dept,utility) #"Field_4 = 'PA' or Field_4 = 'NC' and Field_1 = '2023'" 
        filterSelected=strFilter
        res = [i for i in range(len(strFilter)) if strFilter.startswith("Field_", i)]   
        for idx in res:
            startidx=6+idx
            endidx=startidx+2  
            filterSelected=filterSelected.replace("Field_"+str(strFilter[startidx:endidx]),getFLExcelCol(self,"Field_"+str(strFilter[startidx:endidx]),dept,portfolio))
             
        return JsonResponse({"is_taken":"true",'filterSelected':filterSelected})
 
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
        
class get_Steering_Dashb_Data(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
            filterCnd='' 
            approved_and_denied=getFilterCndn(self,dept,portfolio,'Approved and Denied')
             
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']    
            userfilterCnd=getUserFilter(self,uid,portfolio,dept,'Steering') 
            leiValue=getFilterCndnNValue(self,dept,portfolio,'Bank ID')  
            peerGroupLei=getFilterCndnNValue(self,dept,portfolio,'Peer Group')  
            governmentApps=getFilterCndnNValue(self,dept,portfolio,'Government Application')     
              
            arrCols=['derived_race','derived_sex','derived_ethnicity','applicant_age']
            dictApplications=dict()
            dictPeerApplications=dict()
            dictGovApplications=dict()
            dictGovPeerApplications=dict() 
            for irr in arrCols: 
                filterCnd=''
                if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+leiValue +" and" 
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                 

                strQ="select    ttlData."+ i+" "+irr+ ", \
                round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float ),0)*100,2) \
                apprvd_rate,ttlappl,applconverted from    \
                (select   "+ i+ ",count("+ Action_taken_Field+") ttlappl from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' group by  "+ i+ " )ttlData  left join   \
                ( select "+ i+ ",count("+ Action_taken_Field+") applconverted from  FL_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" in ("+approved_and_denied+")  \
                group by "+ i+ " ) apprvdData on \
                ttlData."+ i+ " =apprvdData."+ i 
                
                tableResultApproved=  self.objdbops.getTable(strQ)  
                # print('col ',i )
                # print(tableResultAIR) 
                distApplications= tableResultApproved.to_json(orient='index')
                distApplications=json.loads(distApplications)
                dictApplications[irr] = distApplications
                del tableResultApproved 

                filterCnd=''
                userfilterCnd=getUserFilterPeerApplication(self,uid,portfolio,dept,'Steering') 
                if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+peerGroupLei +" and"
                strQ="select    ttlData."+ i+" "+irr+ ", \
                round(isnull(cast( peerconverted as float)/ cast( (peerapps) as  float),0)*100,2) \
                conversion_rate,peerapps,peerconverted from    \
                (select   "+ i+ ",count("+ Action_taken_Field+") peerapps from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' group by  "+ i+ " )ttlData  left join   \
                ( select "+ i+ ",count("+ Action_taken_Field+") peerconverted from  FL_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" in ("+approved_and_denied+")  \
                group by "+ i+ " ) apprvdData on \
                ttlData."+ i+ " =apprvdData."+ i  
                tableResultDenied=  self.objdbops.getTable(strQ)  
                # print('col ',i )
                # print(tableResultAIR) 
                distDenied= tableResultDenied.to_json(orient='index')
                distDenied=json.loads(distDenied)
                dictPeerApplications[irr] = distDenied
                del tableResultDenied 

                #Goverment apps query
                filterCnd=''
                if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+leiValue +" and " 

                strQ="select    ttlData."+ i+" "+irr+ ", \
                round(isnull(cast( govApps as decimal(7,2) )/ cast( (ttlappl) as decimal(7,2) ),0)*100,2) \
                apprvd_rate,ttlappl,govApps from    \
                (select   "+ i+ ",count("+ Action_taken_Field+") ttlappl from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' group by  "+ i+ " )ttlData  left join   \
                ( select "+ i+ ",count("+ Action_taken_Field+") govApps from  FL_data where "+filterCnd+" " +governmentApps+ " and  "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" in ("+approved_and_denied+")  \
                group by "+ i+ " ) apprvdData on \
                ttlData."+ i+ " =apprvdData."+ i 
                
                tableResultApproved=  self.objdbops.getTable(strQ)  
                # print('col ',i )
                # print(tableResultAIR) 
                distGovApplications= tableResultApproved.to_json(orient='index')
                distGovApplications=json.loads(distGovApplications)
                dictGovApplications[irr] = distGovApplications
                del tableResultApproved 

                filterCnd=''
                userfilterCnd=getUserFilterPeerApplication(self,uid,portfolio,dept,'Steering') 
                if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+peerGroupLei +" and "
                strQ="select    ttlData."+ i+" "+irr+ ", \
                round(isnull(cast( peerappsGov as float )/ cast( (peerapps) as float ),0)*100,2) \
                conversion_rate,peerapps,peerappsGov from    \
                (select   "+ i+ ",count("+ Action_taken_Field+") peerapps from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' group by  "+ i+ " )ttlData  left join   \
                ( select "+ i+ ",count("+ Action_taken_Field+") peerappsGov from  FL_data where "+filterCnd+" " +governmentApps+ " and    "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" in ("+approved_and_denied+")  \
                group by "+ i+ " ) apprvdData on \
                ttlData."+ i+ " =apprvdData."+ i
                
                tableResultDenied=  self.objdbops.getTable(strQ)  
                # print('col ',i )
                # print(tableResultAIR) 
                distGovPeerGroup= tableResultDenied.to_json(orient='index')
                distGovPeerGroup=json.loads(distGovPeerGroup)
                dictGovPeerApplications[irr] = distGovPeerGroup
                del tableResultDenied  
            
            irr="tract_to_msa_income_percentage"
            filterCnd=''
            if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
            filterCnd +=" "+leiValue +" and"
            i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                
            strQ="select ttlapps.incomegrouop 'incomegroup',ttlappl,applconverted,\
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
            # print('col ',i )
            # print(tableResultAIR) 
            distApplications= tableResultApproved.to_json(orient='index')
            distApplications=json.loads(distApplications)
            dictApplications[irr] = distApplications
            del tableResultApproved 

            filterCnd=''
            userfilterCnd=getUserFilterPeerApplication(self,uid,portfolio,dept,'Steering') 
            if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
            filterCnd +=" "+peerGroupLei +" and"
            i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                
            strQ="select ttlapps.incomegrouop 'incomegroup',ttlappl,applconverted 'peerconverted',\
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
            # print('col ',i )
            # print(tableResultAIR) 
            distApplications= tableResultApproved.to_json(orient='index')
            distApplications=json.loads(distApplications)
            dictPeerApplications[irr] = distApplications
            del tableResultApproved 

           
            filterCnd=''
            if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
            filterCnd +=" "+leiValue +" and  " +governmentApps+ " and "
            i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                
            strQ="select ttlapps.incomegrouop 'incomegroup',ttlappl,applconverted 'govApps',\
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
            # print('col ',i )
            # print(tableResultAIR) 
            distApplications= tableResultApproved.to_json(orient='index')
            distApplications=json.loads(distApplications)
            dictGovApplications[irr] = distApplications
            del tableResultApproved 

            filterCnd=''
            userfilterCnd=getUserFilterPeerApplication(self,uid,portfolio,dept,'Steering') 
            if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
            filterCnd +=" "+peerGroupLei +" and  " +governmentApps+ " and "
            i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                
            strQ="select ttlapps.incomegrouop 'incomegroup',ttlappl,applconverted 'govApps',\
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
            # print('col ',i )
            # print(tableResultAIR) 
            distApplications= tableResultApproved.to_json(orient='index')
            distApplications=json.loads(distApplications)
            dictGovPeerApplications[irr] = distApplications
            del tableResultApproved 
            return JsonResponse({'istaken':'true','apps':dictApplications,'peergroupapps':dictPeerApplications,'appsGov':dictGovApplications,'peergroupappsGov':dictGovPeerApplications })
        except Exception as e:
            print('updateaccess ',e,traceback.print_exc())
            return JsonResponse({'istaken':'false'})
    
class get_Steering_Dashb_Data_apps(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
            filterCnd='' 
            approved_and_denied=getFilterCndn(self,dept,portfolio,'Approved and Denied')             
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']    
            userfilterCnd=getUserFilter(self,uid,portfolio,dept,'Steering') 
            leiValue=getFilterCndnNValue(self,dept,portfolio,'Bank ID')     
            filterCnd=''     
            arrCols=['derived_race','derived_sex','derived_ethnicity','applicant_age']
            dictApplications=dict() 
            for irr in arrCols: 
                filterCnd=''
                if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+leiValue +" and" 
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                 

                strQ="select    ttlData."+ i+" "+irr+ ", \
                round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float ),0)*100,2) \
                apprvd_rate,ttlappl,applconverted from    \
                (select   "+ i+ ",count("+ Action_taken_Field+") ttlappl from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' group by  "+ i+ " )ttlData  left join   \
                ( select "+ i+ ",count("+ Action_taken_Field+") applconverted from  FL_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" in ("+approved_and_denied+")  \
                group by "+ i+ " ) apprvdData on \
                ttlData."+ i+ " =apprvdData."+ i 
                
                tableResultApproved=  self.objdbops.getTable(strQ)  
                # print('col ',i )
                # print(tableResultAIR) 
                distApplications= tableResultApproved.to_json(orient='index')
                distApplications=json.loads(distApplications)
                dictApplications[irr] = distApplications
                del tableResultApproved          
            irr="tract_to_msa_income_percentage"
            filterCnd=''
            if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
            filterCnd +=" "+leiValue +" and"
            i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                
            strQ="select ttlapps.incomegrouop 'incomegroup',ttlappl,applconverted,\
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
            # print('col ',i )
            # print(tableResultAIR) 
            distApplications= tableResultApproved.to_json(orient='index')
            distApplications=json.loads(distApplications)
            dictApplications[irr] = distApplications
            del tableResultApproved 

            strFilter=getUserFilter(self,uid,portfolio,dept,'Steering') #"Field_4 = 'PA' or Field_4 = 'NC' and Field_1 = '2023'" 
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
     
class get_Steering_Dashb_Data_peergroupapps(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
            filterCnd='' 
            approved_and_denied=getFilterCndn(self,dept,portfolio,'Approved and Denied')
             
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']    
            userfilterCnd=getUserFilter(self,uid,portfolio,dept,'Steering')           
            peerGroupLei=getFilterCndnNValue(self,dept,portfolio,'Peer Group')   
            filterCnd=''     
            arrCols=['derived_race','derived_sex','derived_ethnicity','applicant_age']
          
            dictPeerApplications=dict() 
            for irr in arrCols:  
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                 
 

                filterCnd=''
                userfilterCnd=getUserFilterPeerApplication(self,uid,portfolio,dept,'Steering') 
                print('userfilterCnd ',userfilterCnd)
                if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+peerGroupLei +" and"
                strQ="select    ttlData."+ i+" "+irr+ ", \
                round(isnull(cast( peerconverted as float)/ cast( (peerapps) as  float),0)*100,2) \
                conversion_rate,peerapps,peerconverted from    \
                (select   "+ i+ ",count("+ Action_taken_Field+") peerapps from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' group by  "+ i+ " )ttlData  left join   \
                ( select "+ i+ ",count("+ Action_taken_Field+") peerconverted from  FL_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" in ("+approved_and_denied+")  \
                group by "+ i+ " ) apprvdData on \
                ttlData."+ i+ " =apprvdData."+ i  
                tableResultDenied=  self.objdbops.getTable(strQ)  
                # print('col ',i )
                # print(tableResultAIR) 
                distDenied= tableResultDenied.to_json(orient='index')
                distDenied=json.loads(distDenied)
                dictPeerApplications[irr] = distDenied
                del tableResultDenied 

            irr="tract_to_msa_income_percentage"
             
            filterCnd=''
            userfilterCnd=getUserFilterPeerApplication(self,uid,portfolio,dept,'Steering') 
            if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
            filterCnd +=" "+peerGroupLei +" and"
            i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                
            strQ="select ttlapps.incomegrouop 'incomegroup',ttlappl,applconverted 'peerconverted',\
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
            # print('col ',i )
            # print(tableResultAIR) 
            distApplications= tableResultApproved.to_json(orient='index')
            distApplications=json.loads(distApplications)
            dictPeerApplications[irr] = distApplications
            del tableResultApproved 

                 
            return JsonResponse({'istaken':'true', 'peergroupapps':dictPeerApplications })
        except Exception as e:
            print('updateaccess ',e,traceback.print_exc())
            return JsonResponse({'istaken':'false'})

class get_Steering_Dashb_Data_appsGov(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
            filterCnd='' 
            approved_and_denied=getFilterCndn(self,dept,portfolio,'Approved and Denied')
             
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']   
            userfilterCnd=getUserFilter(self,uid,portfolio,dept,'Steering') 
            leiValue=getFilterCndnNValue(self,dept,portfolio,'Bank ID')  
            peerGroupLei=getFilterCndnNValue(self,dept,portfolio,'Peer Group')  
            governmentApps=getFilterCndnNValue(self,dept,portfolio,'Government Application')     
            filterCnd=''     
            arrCols=['derived_race','derived_sex','derived_ethnicity','applicant_age']             
            dictGovApplications=dict() 
            for irr in arrCols: 
                 
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                  
                #Goverment apps query
                filterCnd=''
                if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+leiValue +" and " 

                strQ="select    ttlData."+ i+" "+irr+ ", \
                round(isnull(cast( govApps as decimal(7,2) )/ cast( (ttlappl) as decimal(7,2) ),0)*100,2) \
                apprvd_rate,ttlappl,govApps from    \
                (select   "+ i+ ",count("+ Action_taken_Field+") ttlappl from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' group by  "+ i+ " )ttlData  left join   \
                ( select "+ i+ ",count("+ Action_taken_Field+") govApps from  FL_data where "+filterCnd+" " +governmentApps+ " and  "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" in ("+approved_and_denied+")  \
                group by "+ i+ " ) apprvdData on \
                ttlData."+ i+ " =apprvdData."+ i 
                
                tableResultApproved=  self.objdbops.getTable(strQ)  
                # print('col ',i )
                # print(tableResultAIR) 
                distGovApplications= tableResultApproved.to_json(orient='index')
                distGovApplications=json.loads(distGovApplications)
                dictGovApplications[irr] = distGovApplications
                del tableResultApproved 
 
            
            irr="tract_to_msa_income_percentage"            

             
            filterCnd=''
            if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
            filterCnd +=" "+leiValue +" and  " +governmentApps+ " and "
            i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                
            strQ="select ttlapps.incomegrouop 'incomegroup',ttlappl,applconverted 'govApps',\
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
            # print('col ',i )
            # print(tableResultAIR) 
            distApplications= tableResultApproved.to_json(orient='index')
            distApplications=json.loads(distApplications)
            dictGovApplications[irr] = distApplications
            del tableResultApproved 

           
            return JsonResponse({'istaken':'true', 'appsGov':dictGovApplications })
        except Exception as e:
            print('updateaccess ',e,traceback.print_exc())
            return JsonResponse({'istaken':'false'})

class get_Steering_Dashb_Data_peergroupappsGov(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
            filterCnd='' 
            approved_and_denied=getFilterCndn(self,dept,portfolio,'Approved and Denied')
             
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']    
            userfilterCnd=getUserFilter(self,uid,portfolio,dept,'Steering') 
            peerGroupLei=getFilterCndnNValue(self,dept,portfolio,'Peer Group')  
            governmentApps=getFilterCndnNValue(self,dept,portfolio,'Government Application')     
            filterCnd=''     
            arrCols=['derived_race','derived_sex','derived_ethnicity','applicant_age'] 
            dictGovPeerApplications=dict() 
            for irr in arrCols:               
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                filterCnd=''
                userfilterCnd=getUserFilterPeerApplication(self,uid,portfolio,dept,'Steering') 
                if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+peerGroupLei +" and "
                strQ="select    ttlData."+ i+" "+irr+ ", \
                round(isnull(cast( peerappsGov as float )/ cast( (peerapps) as float ),0)*100,2) \
                conversion_rate,peerapps,peerappsGov from    \
                (select   "+ i+ ",count("+ Action_taken_Field+") peerapps from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' group by  "+ i+ " )ttlData  left join   \
                ( select "+ i+ ",count("+ Action_taken_Field+") peerappsGov from  FL_data where "+filterCnd+" " +governmentApps+ " and    "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" in ("+approved_and_denied+")  \
                group by "+ i+ " ) apprvdData on \
                ttlData."+ i+ " =apprvdData."+ i 
                tableResultDenied=  self.objdbops.getTable(strQ)  
                # print('col ',i )
                # print(tableResultAIR) 
                distGovPeerGroup= tableResultDenied.to_json(orient='index')
                distGovPeerGroup=json.loads(distGovPeerGroup)
                dictGovPeerApplications[irr] = distGovPeerGroup
                del tableResultDenied  
            
            irr="tract_to_msa_income_percentage" 
            filterCnd=''
            userfilterCnd=getUserFilterPeerApplication(self,uid,portfolio,dept,'Steering') 
            if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
            filterCnd +=" "+peerGroupLei +" and  " +governmentApps+ " and "
            i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                
            strQ="select ttlapps.incomegrouop 'incomegroup',ttlappl,applconverted 'govApps',\
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
            # print('col ',i )
            # print(tableResultAIR) 
            distApplications= tableResultApproved.to_json(orient='index')
            distApplications=json.loads(distApplications)
            dictGovPeerApplications[irr] = distApplications
            del tableResultApproved 
            return JsonResponse({'istaken':'true', 'peergroupappsGov':dictGovPeerApplications })
        except Exception as e:
            print('updateaccess ',e,traceback.print_exc())
            return JsonResponse({'istaken':'false'})
        
class updatePeerGroups(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            uid =str(request.data['uid'])
            tabSelected = request.data['tabSelected']  
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])   
            peergroups =request.data['peergroups']
            peergroups=peergroups.replace("'","''") 
            dbfield=getFLDbCol(self,'lei',dept,portfolio) 
            strQ="UPDATE FL_Filter_Criteria SET   Lei_Selected ='"+dbfield+" in ("+peergroups+")' WHERE  Department ='"+dept+"' and Portfolio ='"+portfolio+"' \
                and Utility = '"+tabSelected+"' and Added_By ='"+uid+"'"
            self.objdbops.insertRow(strQ)
            return JsonResponse({'istaken':'true'})
        except Exception as e:
            print('updateaccess ',e,traceback.print_exc())
            return JsonResponse({'istaken':'false'})

class get_Marketing_Dashb_Data_apps(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            print("request_data",request.data)
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
            filterCnd='' 
            approved_and_denied=getFilterCndn(self,dept,portfolio,'Approved and Denied')             
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']    
            userfilterCnd=getUserFilter(self,uid,portfolio,dept,'Marketing') 
            leiValue=getFilterCndnNValue(self,dept,portfolio,'Bank ID')     
            filterCnd=''     
            arrCols=['derived_race','derived_sex','derived_ethnicity','applicant_age']
            dictApplications=dict() 
            for irr in arrCols: 
                filterCnd=''
                if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+leiValue +" and" 
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                 

                strQ="select    apprvdData."+ i+" "+irr+ ", \
                round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float ),0)*100,2) \
                apprvd_rate, applconverted 'ttlappl'from    \
                (select  count("+ Action_taken_Field+") ttlappl from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "'  )ttlData , \
                ( select "+ i+ ",count("+ Action_taken_Field+") applconverted from  FL_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "'  group by "+ i+ " ) apprvdData "                
                tableResultApproved=  self.objdbops.getTable(strQ)  
                
                # print(tableResultAIR) 
                distApplications= tableResultApproved.to_json(orient='index')
                distApplications=json.loads(distApplications)
                dictApplications[irr] = distApplications
                del tableResultApproved      

            irr="tract_to_msa_income_percentage"
            filterCnd=''
            if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
            filterCnd +=" "+leiValue +" and"
            i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                
            strQ="select convertedapps.incomegrouop 'incomegroup',ttlappl,applconverted,\
                round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float),0)*100,2) apprvd_rate from \
                (select count(*) ttlappl from  fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                )ttlapps ,\
                (select incomegrouop,count(*) applconverted from ( \
                select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                when cast("+ i+ " as float)>= 120 then 'Upper' \
                end incomegrouop from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                )   incomegroupdata group by incomegrouop) convertedapps " 
            
            tableResultApproved=  self.objdbops.getTable(strQ)  
            # print('col ',i )
            # print(tableResultAIR) 
            distApplications= tableResultApproved.to_json(orient='index')
            distApplications=json.loads(distApplications)
            dictApplications[irr] = distApplications
            del tableResultApproved 

            strFilter=getUserFilter(self,uid,portfolio,dept,'Steering') #"Field_4 = 'PA' or Field_4 = 'NC' and Field_1 = '2023'" 
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

class get_Marketing_Dashb_Data_ClassWise(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            print("request_data classwise",request.data)
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
            classVar = str(request.data['ClassVar'])    
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
            classVar = str(request.data['ClassVar'])    
            segNm = str(request.data['segNm'])    
            filterCnd='' 
            approved_and_denied=getFilterCndn(self,dept,portfolio,'Approved and Denied')             
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']    
            userfilterCnd=getUserFilter(self,uid,portfolio,dept,'Marketing_'+classVar,segNm) 
            leiValue=getFilterCndnNValue(self,dept,portfolio,'Bank ID')     
            filterCnd=''     
            arrCols=[]
            arrCols.append(classVar)
            dictApplications=dict() 
            ctrlCLsQ,ctrlCLsCols=getUserCtrlClsQuery(self,uid,portfolio,dept,'Marketing_'+classVar) 
            for irr in arrCols: 
                filterCnd=''
                strCtrlClsQ=''
                if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+leiValue +" and"  
                i=self.objdbops.getscalar("select Database_Fields from FL_Mapping_Details where lower(Excel_Fields)=lower('"+irr+"') and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                 
                if ctrlCLsCols  !="":
                    strCtrlClsQ="select    1, '"+ ctrlCLsQ +"'  ClsLbl, \
                round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float ),0)*100,2) \
                apprvd_rate, applconverted 'ttlappl'from    \
                (select  count("+ Action_taken_Field+") ttlappl from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "'  and  CONCAT("+ctrlCLsCols+")   in ( '"+ctrlCLsQ+"') )ttlData , \
                ( select  'Control Class' 'Control Class' ,count("+ Action_taken_Field+") applconverted from  FL_data where  "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "'  and  CONCAT("+ctrlCLsCols+")   in( '"+ctrlCLsQ+"')) apprvdData union "                
                
                strQ="select   2, apprvdData."+ i+" ClsLbl, \
                round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float ),0)*100,2) \
                apprvd_rate, applconverted 'ttlappl'from    \
                (select  count("+ Action_taken_Field+") ttlappl from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' and  CONCAT("+ctrlCLsCols+") not  in ( '"+ctrlCLsQ+"')  )ttlData , \
                ( select "+ i+ ",count("+ Action_taken_Field+") applconverted from  FL_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "'  and  CONCAT("+ctrlCLsCols+") not in( '"+ctrlCLsQ+"') group by "+ i+ " ) apprvdData order by 1 "                
                    
                tableResultApproved=  self.objdbops.getTable(strCtrlClsQ+strQ)  
                
                # print(tableResultAIR) 
                distApplications= tableResultApproved.to_json(orient='index')
                distApplications=json.loads(distApplications)
                dictApplications['apps'] = distApplications
                del tableResultApproved       
            peerGroupLei=getFilterCndnNValue(self,dept,portfolio,'Peer Group')   
            filterCnd=''     
            
            dictPeerApplications=dict() 
            for irr in arrCols:  
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                filterCnd=''
                strCtrlClsQ=''
                userfilterCnd=getUserFilterPeerApplication(self,uid,portfolio,dept,'Marketing') 
                if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+peerGroupLei +" and"
                if ctrlCLsCols  !="":
                    strCtrlClsQ="select    1 ordercol, '"+ ctrlCLsQ +"'  ClsLbl, \
               round(isnull(cast( peerconverted as float)/ cast( (peerapps) as  float),0)*100,2) \
                conversion_rate, peerconverted  from    \
                (select  count("+ Action_taken_Field+") peerapps from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' and  CONCAT("+ctrlCLsCols+")   in ( '"+ctrlCLsQ+"')  )ttlData , \
                ( select  'Control Class' 'Control Class' ,count("+ Action_taken_Field+") peerconverted from  FL_data where  "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "'  and  CONCAT("+ctrlCLsCols+")   in ( '"+ctrlCLsQ+"')) apprvdData union "   
                
                strQ="select   2, apprvdData."+ i +" ClsLbl, \
                round(isnull(cast( peerconverted as float)/ cast( (peerapps) as  float),0)*100,2) \
                conversion_rate, peerconverted   from    \
                (select   count("+ Action_taken_Field+") peerapps from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "'    and  CONCAT("+ctrlCLsCols+")  not in ( '"+ctrlCLsQ+"'))ttlData , \
                ( select "+ i+ ",count("+ Action_taken_Field+") peerconverted from  FL_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "'   and  CONCAT("+ctrlCLsCols+")   not in( '"+ctrlCLsQ+"')\
                  group by "+ i+ " ) apprvdData order by 1"
                
                tableResultDenied=  self.objdbops.getTable(strCtrlClsQ+strQ)  
                # print('col ',i )
                # print(tableResultAIR) 
                distDenied= tableResultDenied.to_json(orient='index')
                distDenied=json.loads(distDenied)
                dictPeerApplications['peergroupapps'] = distDenied
                del tableResultDenied 

             
             
            return JsonResponse({'istaken':'true','apps':dictApplications, 'peergroupapps':dictPeerApplications})
        except Exception as e:
            print('updateaccess ',e,traceback.print_exc())
            return JsonResponse({'istaken':'false'})

class get_Marketing_Dashb_Data_IncomeGrp(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
            filterCnd=''             
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            # //Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']    
            userfilterCnd=getUserFilter(self,uid,portfolio,dept,'Marketing') 
            leiValue=getFilterCndnNValue(self,dept,portfolio,'Bank ID')     
            filterCnd=''  
            dictApplications=dict() 
            dictPeerApplications=dict()
            irr="tract_to_msa_income_percentage"
            ctrlCLsQ,ctrlCLsCols=getUserCtrlClsQuery(self,uid,portfolio,dept,'Marketing_'+irr) 
            
            filterCnd=''
            if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
            filterCnd +=" "+leiValue +" and"
            i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 

            if ctrlCLsCols  !="":
                strQ="select prohbcls.ClsLbl,prohbcls.ttlappl,prohbcls.applconverted,prohbcls.apprvd_rate, \
                    controlcls.ttlappl 'ctrl_ttlappl',controlcls.applconverted 'ctrl_applconverted',controlcls.apprvd_rate 'ctrl_apprvd_rate' from (select convertedapps.incomegrouop 'ClsLbl',ttlappl,applconverted,\
                round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float),0)*100,2) apprvd_rate from \
                (select count(*) ttlappl from  fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' and  CONCAT("+ctrlCLsCols+") not in( '"+ctrlCLsQ+"')\
                )ttlapps ,\
                (select incomegrouop,count(*) applconverted from ( \
                select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                when cast("+ i+ " as float)>= 120 then 'Upper' \
                end incomegrouop from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "'  and  CONCAT("+ctrlCLsCols+") not in( '"+ctrlCLsQ+"')  \
                )   incomegroupdata group by incomegrouop) convertedapps) prohbcls left join  (select convertedapps.incomegrouop 'ClsLbl',ttlappl,applconverted,\
                round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float),0)*100,2) apprvd_rate from \
                (select count(*) ttlappl from  fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' and  CONCAT("+ctrlCLsCols+")  in( '"+ctrlCLsQ+"')\
                )ttlapps ,\
                (select incomegrouop,count(*) applconverted from ( \
                select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                when cast("+ i+ " as float)>= 120 then 'Upper' \
                end incomegrouop from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "'  and  CONCAT("+ctrlCLsCols+")  in( '"+ctrlCLsQ+"')  \
                )   incomegroupdata group by incomegrouop) convertedapps) controlcls on controlcls.ClsLbl=prohbcls.ClsLbl"      
            else:
                strQ="select convertedapps.incomegrouop 'ClsLbl',ttlappl,applconverted,\
                    round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float),0)*100,2) apprvd_rate from \
                    (select count(*) ttlappl from  fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                    )ttlapps ,\
                    (select incomegrouop,count(*) applconverted from ( \
                    select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                    when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                    when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                    when cast("+ i+ " as float)>= 120 then 'Upper' \
                    end incomegrouop from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "'  \
                    )   incomegroupdata group by incomegrouop) convertedapps "   
            tableResultApproved=  self.objdbops.getTable(strQ)  
            # print('col ',i )
            # print(tableResultAIR) 
            distApplications= tableResultApproved.to_json(orient='index')
            distApplications=json.loads(distApplications)
            dictApplications['apps'] = distApplications
            del tableResultApproved 
            peerGroupLei=getFilterCndnNValue(self,dept,portfolio,'Peer Group')   
            filterCnd=''
            userfilterCnd=getUserFilterPeerApplication(self,uid,portfolio,dept,'Steering') 
            if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
            filterCnd +=" "+peerGroupLei +" and"
            i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 

            if ctrlCLsCols  !="":
                strQ="select prohbcls.ClsLbl,prohbcls.ttlappl,prohbcls.applconverted 'peerconverted',prohbcls.apprvd_rate 'conversion_rate', \
                    controlcls.ttlappl 'ctrl_ttlappl',controlcls.applconverted 'ctrl_peerconverted',controlcls.apprvd_rate 'ctrl_conversion_rate' from (select convertedapps.incomegrouop 'ClsLbl',ttlappl,applconverted,\
                round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float),0)*100,2) apprvd_rate from \
                (select count(*) ttlappl from  fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' and  CONCAT("+ctrlCLsCols+") not in( '"+ctrlCLsQ+"')\
                )ttlapps ,\
                (select incomegrouop,count(*) applconverted from ( \
                select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                when cast("+ i+ " as float)>= 120 then 'Upper' \
                end incomegrouop from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "'  and  CONCAT("+ctrlCLsCols+") not in( '"+ctrlCLsQ+"')  \
                )   incomegroupdata group by incomegrouop) convertedapps) prohbcls left join  (select convertedapps.incomegrouop 'ClsLbl',ttlappl,applconverted,\
                round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float),0)*100,2) apprvd_rate from \
                (select count(*) ttlappl from  fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' and  CONCAT("+ctrlCLsCols+")  in( '"+ctrlCLsQ+"')\
                )ttlapps ,\
                (select incomegrouop,count(*) applconverted from ( \
                select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                when cast("+ i+ " as float)>= 120 then 'Upper' \
                end incomegrouop from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "'  and  CONCAT("+ctrlCLsCols+")  in( '"+ctrlCLsQ+"')  \
                )   incomegroupdata group by incomegrouop) convertedapps) controlcls on controlcls.ClsLbl=prohbcls.ClsLbl" 
            else:    
                strQ="select convertedapps.incomegrouop 'ClsLbl',applconverted 'peerconverted',\
                    round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float),0)*100,2) conversion_rate  from \
                    (select count(*) ttlappl from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                    )ttlapps ,\
                    (select incomegrouop,count(*) applconverted from ( \
                    select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                    when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                    when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                    when cast("+ i+ " as float)>= 120 then 'Upper' \
                    end incomegrouop from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                    )   incomegroupdata group by incomegrouop) convertedapps "  
             
            tableResultApproved=  self.objdbops.getTable(strQ)  
            # print('col ',i )
            # print(tableResultAIR) 
            distApplications= tableResultApproved.to_json(orient='index')
            distApplications=json.loads(distApplications)
            dictPeerApplications['peergroupapps'] = distApplications
            del tableResultApproved 


                      
            return JsonResponse({'istaken':'true','apps':dictApplications , 'peergroupapps':dictPeerApplications})
        except Exception as e:
            print('updateaccess ',e,traceback.print_exc())
            return JsonResponse({'istaken':'false'})

class get_Marketing_Dashb_Data_peergroupapps(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
            filterCnd=''  
             
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']    
            userfilterCnd=getUserFilter(self,uid,portfolio,dept,'Marketing')           
            peerGroupLei=getFilterCndnNValue(self,dept,portfolio,'Peer Group')   
            filterCnd=''     
            arrCols=['derived_race','derived_sex','derived_ethnicity','applicant_age']
          
            dictPeerApplications=dict() 
            for irr in arrCols:  
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                filterCnd=''
                userfilterCnd=getUserFilterPeerApplication(self,uid,portfolio,dept,'Marketing') 
                if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+peerGroupLei +" and"
                strQ="select    apprvdData."+ i+" "+irr+ ", \
                round(isnull(cast( peerconverted as float)/ cast( (peerapps) as  float),0)*100,2) \
                conversion_rate, peerconverted   from    \
                (select   count("+ Action_taken_Field+") peerapps from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "'  )ttlData , \
                ( select "+ i+ ",count("+ Action_taken_Field+") peerconverted from  FL_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                  group by "+ i+ " ) apprvdData "
               
                tableResultDenied=  self.objdbops.getTable(strQ)  
                # print('col ',i )
                # print(tableResultAIR) 
                distDenied= tableResultDenied.to_json(orient='index')
                distDenied=json.loads(distDenied)
                dictPeerApplications[irr] = distDenied
                del tableResultDenied 

            irr="tract_to_msa_income_percentage"
             
            filterCnd=''
            userfilterCnd=getUserFilterPeerApplication(self,uid,portfolio,dept,'Steering') 
            if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
            filterCnd +=" "+peerGroupLei +" and"
            i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                
            strQ="select convertedapps.incomegrouop 'incomegroup',applconverted 'peerconverted',\
                round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float),0)*100,2) conversion_rate  from \
                (select count(*) ttlappl from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                )ttlapps ,\
                (select incomegrouop,count(*) applconverted from ( \
                select  case   when cast("+ i+ " as float)< 50 then 'Low' \
                when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
                when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
                when cast("+ i+ " as float)>= 120 then 'Upper' \
                end incomegrouop from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                 )   incomegroupdata group by incomegrouop) convertedapps "  
             
            tableResultApproved=  self.objdbops.getTable(strQ)  
            # print('col ',i )
            # print(tableResultAIR) 
            distApplications= tableResultApproved.to_json(orient='index')
            distApplications=json.loads(distApplications)
            dictPeerApplications[irr] = distApplications
            del tableResultApproved 

                 
            return JsonResponse({'istaken':'true', 'peergroupapps':dictPeerApplications })
        except Exception as e:
            print('updateaccess ',e,traceback.print_exc())
            return JsonResponse({'istaken':'false'})


class GetRiskFactorHistoryMsg(APIView):
    print() 
    objdbops =None

    def __init__(self):
        self.objdbops=dbops()

    def get(self,request):
        print("new request--------------------------------",request.data)
        try:
            strQ = "SELECT  [Risk_Factor_Discussion_AID],FORMAT (resp.[Added_on],'hh:mm tt  MMM dd, yyyy') createdt ,[Comments],"
            strQ+=" concat(u.U_FName,' ',u.U_LName) Added_by,upper(concat(left(u.U_FName,1),left(u.U_LName,1))) uinitials,case when resp.Added_by="+str(request.data['addedby'])+" then 'S' else 'R' end msgcss"
            strQ+=" from  [Risk_Factor_Discussion] resp,users u"
            strQ+=" where u.U_AID=resp.Added_by and Group_Id='"+request.data['group_id']+"' and Risk_ID='"+request.data['risk_id']+"' order by [Risk_Factor_Discussion_AID]"
             
            tableResult=  self.objdbops.getTable(strQ) 
            
            # if tableResult.empty == False:
            data= tableResult.to_json(orient='index') 

            return Response({'data':json.loads(data)})
        except Exception as e:
            print("Excpet")
            print('adduser is ',e)
            print('adduser traceback is ', traceback.print_exc())

    def post(self,request):
        serializer = RiskFactorDiscussionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response({'data':serializer.data,'msg':'Discussion Comments is saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class GetUtilityAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        obj = Risk_Factor_Master.objects.filter(utility=request.data['utility'])
        serializer = Risk_Factor_MasterSerializer(obj,many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class saveriskcomments(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data",request.data)  
        obj = RiskFactorComments.objects.filter(risk_id = request.data['risk_id'])
        if obj:
            RiskFactorComments.objects.filter(risk_id = request.data['risk_id']).update(utility = request.data['utility'],comments = request.data['comments'],department = request.data['department'])
            return Response({'msg':'Risk Factor comment is Updated Successufully'},status=status.HTTP_201_CREATED)
        else:
            serializer = RiskFactorCommentsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'msg':'Risk Factor comment is created Successufully'},status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class get_Pricing_Dashb_Data_apps(APIView): 
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
            filterCnd='' 
            approved_and_denied=getFilterCndn(self,dept,portfolio,'Origination')             
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']    
            userfilterCnd=getUserFilter(self,uid,portfolio,dept,'Pricing') 
            leiValue=getFilterCndnNValue(self,dept,portfolio,'Bank ID')     
            filterCnd=''     
            arrCols=['derived_race','derived_sex','derived_ethnicity','applicant_age']
            dictApplications=dict() 
            for irr in arrCols: 
                filterCnd=''
                if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+leiValue +" and" 
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                 

                strQ="select    ttlData."+ i+" "+irr+ ", \
                round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float ),0)*100,2) \
                apprvd_rate,ttlappl,applconverted from    \
                (select   "+ i+ ",count("+ Action_taken_Field+") ttlappl from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' group by  "+ i+ " )ttlData  left join   \
                ( select "+ i+ ",count("+ Action_taken_Field+") applconverted from  FL_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" in ("+approved_and_denied+")  \
                group by "+ i+ " ) apprvdData on \
                ttlData."+ i+ " =apprvdData."+ i  
                tableResultApproved=  self.objdbops.getTable(strQ)  
                # print('col ',i )
                # print(tableResultAIR) 
                distApplications= tableResultApproved.to_json(orient='index')
                distApplications=json.loads(distApplications)
                dictApplications[irr] = distApplications
                del tableResultApproved          
            irr="tract_to_msa_income_percentage"
            filterCnd=''
            if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
            filterCnd +=" "+leiValue +" and"
            i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                
            strQ="select ttlapps.incomegrouop 'incomegroup',ttlappl,applconverted,\
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
            # print('col ',i )
            # print(tableResultAIR) 
            distApplications= tableResultApproved.to_json(orient='index')
            distApplications=json.loads(distApplications)
            dictApplications[irr] = distApplications
            del tableResultApproved 

            strFilter=getUserFilter(self,uid,portfolio,dept,'Pricing') #"Field_4 = 'PA' or Field_4 = 'NC' and Field_1 = '2023'" 
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
   
class get_Pricing_Dashb_Data_ratespread(APIView): 
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept']) 
            ratespread = str(request.data['ratespread'])   
            filterCnd='' 
            approved_and_denied=getFilterCndn(self,dept,portfolio,'Origination')             
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']    
            userfilterCnd=getUserFilter(self,uid,portfolio,dept,'Pricing') 
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
            arrCols=['derived_race','derived_sex','derived_ethnicity','applicant_age']
            arrCtrl_Class=tableResult.values[0][2].split(',')    
            filterCnd=''     
            arrCols=['derived_race','derived_sex','derived_ethnicity','applicant_age']
            rate_spread_col=getFLDbCol(self,'rate_spread',dept,portfolio)
            dictApplications=dict() 
            for irr in arrCols: 
                filterCnd=''
                if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+leiValue +" and"  
                
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                 

                strQ="select    ttlData."+ i+" "+irr+ ", \
                round(isnull(cast( isnull(applconverted,0) as float)/ cast( (ttlappl) as float ),0)*100,2) \
                apprvd_rate,ttlappl,isnull(applconverted,0) applconverted,isnull(fieldavg,0)fieldavg  from    \
                (select   "+ i+ ",count("+ Action_taken_Field+") ttlappl from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "'\
                      group by  "+ i+ " )ttlData  left join   \
                ( select "+ i+ ",count("+ Action_taken_Field+") applconverted,avg( cast(case when "+rate_spread_col+"='NA' then Null else "+rate_spread_col+" end as float) ) fieldavg from  FL_data where "+filterCnd+ "  cast(case when "+rate_spread_col+"='NA' then Null else "+rate_spread_col+" end as float) >= "+ratespread + " and "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" in ("+approved_and_denied+")  \
                group by "+ i+ " ) apprvdData on \
                ttlData."+ i+ " =apprvdData."+ i 
                tableResultApproved=  self.objdbops.getTable(strQ)   
                # print(tableResultAIR) 
                distApplications= tableResultApproved.to_json(orient='index')
                distApplications=json.loads(distApplications)
                dictApplications[irr] = distApplications
                del tableResultApproved      
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
            irr="tract_to_msa_income_percentage"
            filterCnd=''
            if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
            filterCnd +=" "+leiValue +" and"
             
            i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                
            strQ="select ttlapps.incomegrouop 'incomegroup',ttlappl,isnull(applconverted,0) applconverted,\
                round(isnull(cast( isnull(applconverted,0) as float)/ cast( (ttlappl) as float),0)*100,2) apprvd_rate from \
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
                end incomegrouop from fl_data where "+filterCnd+"  cast(case when "+rate_spread_col+"='NA' then Null else "+rate_spread_col+" end as float) >= "+ratespread + " and "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" in ("+approved_and_denied+")   )   incomegroupdata group by incomegrouop) convertedapps \
                on ttlapps.incomegrouop=convertedapps.incomegrouop" 
            
            tableResultApproved=  self.objdbops.getTable(strQ)  
            # print('col ',i )
            # print(tableResultAIR) 
            distApplications= tableResultApproved.to_json(orient='index')
            distApplications=json.loads(distApplications)
            dictApplications[irr] = distApplications
            del tableResultApproved  
            
            return JsonResponse({'istaken':'true','apps':dictApplications,'denomCtrlCls':denomCtrlCls  })
        except Exception as e:
            print('updateaccess ',e,traceback.print_exc())
            return JsonResponse({'istaken':'false'})
   
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
            # sub_sub_section=request.data['sub_sub_section']
            # sub_sub_sub_section=request.data['sub_sub_sub_section']
            question=request.data['question'] 
            sect_type=request.data['sect_type']
            if sub_section == '':
                sub_section=None
            # if sub_sub_section == '':
            #     sub_sub_section =None
            # if sub_sub_sub_section == '':
            #     sub_sub_sub_section =None      
            question_obj=FlQuestionMaster.objects.create(question_label=question,section_aid=section,sub_section_aid=sub_section,
                                                        section_type=sect_type,addedby=added_by,adddate=adddate)
            print("saved")
            return JsonResponse({'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e: 
            #error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class Fl_sectionsAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        data = FlSections.objects.all()
        serializer = FLSectionsSerializer(data,many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class UsersgetAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        from django.contrib.auth import get_user_model
        User=get_user_model()
        data = User.objects.all()
        serializer = UserSerializer(data,many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class save_flallocation(APIView):
    def post(self,request):  
        try:  
            print("request data-----------",request.data)   
            section_aid = request.data['section_aid']
            users = request.data['users']
            # end_date = request_data['end_date'][6:] + "-" + request_data['end_date'][3:5] + "-" + request_data['end_date'][:2]
            if request.data['rv_id'] == "addnew":
                print("if")
                last_rvid_obj = FlAllocation.objects.aggregate(max('review_id'))
                last_rvid = last_rvid_obj['review_id__max']
                splt_rvid = last_rvid.split('_')
                latest_rvid = int(splt_rvid[1]).__add__(1) #used magic method django
                for user, section_id in [(x,y) for x in users for y in section_aid]:
                    allocate_obj = FlAllocation(review_id ="Rv_"+str(latest_rvid),review_name = request.data['rv_name'],section_aid = section_id,allocated_to = user,end_date = None)
                    allocate_obj.save()
                return Response( {"isvalid":"true"}, status=status.HTTP_200_OK) 
            else:
                print("else")
                for user, section_id in [(x,y) for x in users for y in section_aid]:
                    allocate_obj = FlAllocation(review_id =request.data['rv_id'],review_name = request.data['rv_name'],section_aid = section_id,allocated_to = user,end_date = None)
                    allocate_obj.save() 
                return Response( {"isvalid":"true"}, status=status.HTTP_200_OK)
        except Exception as e: 
            #error_saving(request,e)
            print(traceback.print_exc())
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)
        
class FLQtns(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try: 
            uid=request.data['uid'] 
            return Response({'canupdate':objmaster.FLcanUpdateRatings(uid),'sections':objmaster.getFLQtnSection(uid),
                           'Qtns':objmaster.getFLQtns(uid),'models':objmaster.getFLModels(str(uid))}, status=status.HTTP_200_OK)
        except Exception as e: 
            ##error_saving(request,e)
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
            #error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class saveFLRatings(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try: 
            colDataLst = request.data['colDataLst']
            print("colDataLst",colDataLst)
            uid=request.data['uid']
            json_colDataLst = json.loads(colDataLst)
            objreg=Register()
            for colval in json_colDataLst:
                print('col val is ',colval )
                # objreg.insertFLRatings(colval["qtnId"],colval["ddl_yesno_"],colval["ddl_doc_"],colval["txt_comment_"],uid,objmaster.getmaxFLId())
                obj = FlQuestionRatingData.objects.filter(review_id=objmaster.getmaxFLId(),question_aid=colval["qtnId"],addedby=uid)
                if obj:    
                    print("if")
                    FlQuestionRatingData.objects.filter(review_id=objmaster.getmaxFLId(),question_aid=colval["qtnId"],addedby=uid).update(rating_yes_no=colval["ddl_yesno_"],comments=colval["txt_comment_"])
                else: 
                    print("else")
                    try:   
                        print("review_id",objmaster.getmaxFLId(),"question_aid",colval["qtnId"])
                        save_obj = FlQuestionRatingData.objects.create(review_id=objmaster.getmaxFLId(),question_aid=colval["qtnId"],rating_yes_no=colval["ddl_yesno_"],comments=colval["txt_comment_"],addedby=uid)

                    except Exception as e:
                        print("error is",e)
            return Response({'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e: 
            print(traceback.print_exc(),e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class get_State_Lat_long(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
            peer = request.data['peer'] 
            peergrouplei=getFilterCndnNValue(self,dept,portfolio,'Peer Group')   
            filterCnd=''
            appovedCndn=getFilterCndn(self,dept,portfolio,'Approved')
            deniedCndn=getFilterCndn(self,dept,portfolio,'Denied')
            approved_and_denied=getFilterCndn(self,dept,portfolio,'Approved and Denied')
             
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ dept +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ dept +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']   
            strQ="select isnull(max(filter_Condn),'') filter_Condn from FL_Filter_Criteria where added_by="+ str(uid) 
            filterCnd=self.objdbops.getscalar(strQ) 
            if peer=='n':
                leiValue=getFilterCndnNValue(self,dept,portfolio,'Bank ID')
            elif peer=='y':
                leiValue=getFilterCndnNValue(self,dept,portfolio,'Peer Group')
            print('leiValue is ',leiValue)
            
            if filterCnd !='':
                filterCnd="("+filterCnd +") and"
            filterCnd +=" "+leiValue +" and"    
           
            
            i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='state_code' and  Portfolio ='"+ portfolio +"' and department='"+ dept +"'") 
            strQ="select dt."+i+" state,count(*) RowCnt,max(st.lat) lat,max(st.lng) long  \
                from FL_Data dt join FL_State_Lat_Lng st \
                on dt."+i+"=st.state_id where "+filterCnd +" " + activity_year_Field +"='"+ request.data['activity_year']+"' group by dt."+i+""
            tableResultAIR=  self.objdbops.getTable(strQ)   
            # print('col ',i )
            # print(tableResultAIR)
            distVals= tableResultAIR.to_json(orient='index')
            distVals=json.loads(distVals) 
            del tableResultAIR

            strQ="select B_address,b_city,b_state,b_zip,B_Lat,B_Long from Bank_Branches "  
            tableResultBranch=  self.objdbops.getTable(strQ)   
            # print('col ',i )
            print('StateLatLong Branch',tableResultBranch)
            print(strQ)
            distBranch= tableResultBranch.to_json(orient='index')
            distBranch=json.loads(distBranch) 
            del tableResultBranch
                
            return JsonResponse({'StateLatLong':distVals, 'BankBranches':distBranch })
        except Exception as e:
            print('StateLatLong ',e,traceback.print_exc())
            return JsonResponse({'StateLatLong':'false'})

class get_County_Lat_long(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
            State = request.data['State'] 
            peer = request.data['peer'] 
            filterCnd=''
            appovedCndn=getFilterCndn(self,dept,portfolio,'Approved')
            deniedCndn=getFilterCndn(self,dept,portfolio,'Denied')
            approved_and_denied=getFilterCndn(self,dept,portfolio,'Approved and Denied')

            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ dept +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ dept +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']   
            strQ="select isnull(max(filter_Condn),'') filter_Condn from FL_Filter_Criteria where added_by="+ str(uid) 
            filterCnd=self.objdbops.getscalar(strQ) 
            if peer=='n':
                leiValue=getFilterCndnNValue(self,dept,portfolio,'Bank ID')
            elif peer=='y':
                leiValue=getFilterCndnNValue(self,dept,portfolio,'Peer Group')
            print('leiValue is ',leiValue)
            
            if filterCnd !='':
                filterCnd="("+filterCnd +") and"
            filterCnd +=" "+leiValue +" and"    
           
            
            st=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='state_code' and  Portfolio ='"+ portfolio +"' and department='"+ dept +"'") 
            i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='county_code' and  Portfolio ='"+ portfolio +"' and department='"+ dept +"'")             
            strQ="select max(county) CountyName,dt."+i+" ,count(*) RowCnt,max(cy.lat) lat,max(cy.lng) long  \
                from FL_Data dt join FL_County_Lat_Lng cy \
                on dt."+i+"=cy.county_fips where "+filterCnd +" " + activity_year_Field +"='"+ request.data['activity_year']+"' and dt."+st+"='"+ State +"' group by dt."+i+""
            tableResultAIR=  self.objdbops.getTable(strQ)   
            # print('col ',i )
            print('CountyLatLong StateName',State)
            print(strQ)
            distVals= tableResultAIR.to_json(orient='index')
            distVals=json.loads(distVals) 
            del tableResultAIR

            strQ="select B_address,b_city,b_state,b_zip,B_Lat,B_Long from Bank_Branches where trim(B_STATE)='"+State+"'"
            tableResultBranch=  self.objdbops.getTable(strQ)   
            # print('col ',i )
            print('CountyLatLong Branch',tableResultBranch)
            print(strQ)
            distBranch= tableResultBranch.to_json(orient='index')
            distBranch=json.loads(distBranch) 
            del tableResultBranch
                
            return JsonResponse({'CountyLatLong':distVals, 'BankBranches':distBranch })  
        except Exception as e:
            print('CountyLatLong ',e,traceback.print_exc())
            return JsonResponse({'CountyLatLong':'false'})

class get_Filter_State_Lat_long(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
            peer = request.data['peer'] 
            filter_col=request.data['filter_col']
            peergrouplei=getFilterCndnNValue(self,dept,portfolio,'Peer Group')   
            filterCnd=''
            appovedCndn=getFilterCndn(self,dept,portfolio,'Approved')
            deniedCndn=getFilterCndn(self,dept,portfolio,'Denied')
            approved_and_denied=getFilterCndn(self,dept,portfolio,'Approved and Denied')
             
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ dept +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ dept +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']   
            strQ="select isnull(max(filter_Condn),'') filter_Condn from FL_Filter_Criteria where added_by="+ str(uid) 
            filterCnd=self.objdbops.getscalar(strQ) 
            if peer=='n':
                leiValue=getFilterCndnNValue(self,dept,portfolio,'Bank ID')
            elif peer=='y':
                leiValue=getFilterCndnNValue(self,dept,portfolio,'Peer Group')
            print('leiValue is ',leiValue)
            
            if filterCnd !='':
                filterCnd="("+filterCnd +") and"
            filterCnd +=" "+leiValue +" and"    

            ## select Field_10, dt.Field_4 state,count(field_4) RowCnt,max(st.lat) lat,max(st.lng) long
            ## from fl_data dt join FL_State_Lat_Lng st on dt.Field_4=st.state_id
            ## where Field_2='N8T7HW55LK5D2ORCKP39' group by Field_10,Field_4 order by 2,1   

            ## select Field_10, dt.Field_4 state,count(field_4) RowCnt,max(st.lat) lat,max(st.lng) long
            ## from fl_data dt join FL_State_Lat_Lng st on dt.Field_4=st.state_id
            ## where Field_2='N8T7HW55LK5D2ORCKP39' group by Field_10,Field_4
            ## order by row_number() over (partition by dt.Field_4 order by dt.Field_4,count(field_4) desc), dt.Field_4         

            i=getFLDbCol(self,"state_code",dept,portfolio)    ##self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='state_code' and  Portfolio ='"+ portfolio +"' and department='"+ dept +"'") 
            FilterColName=getFLDbCol(self,filter_col,dept,portfolio)          ##getFLDbCol(self,excelcol,dept,portfolio)
            print('get_Filter_State_Lat_long ',i,':',filter_col,':',FilterColName,':')
            strQ="select dt."+FilterColName+" FilVal,dt."+i+" state,count(*) RowCnt,max(st.lat) lat,max(st.lng) long  \
                from FL_Data dt join FL_State_Lat_Lng st \
                on dt."+i+"=st.state_id where "+filterCnd +" " + activity_year_Field +"='"+ request.data['activity_year']+"' group by dt."+FilterColName+",dt."+i+" \
                order by row_number() over (partition by dt."+i+" order by dt."+i+",count("+i+") desc), dt."+i+""  
            print('get_Filter_State_Lat_long ',strQ)
            tableResultAIR=  self.objdbops.getTable(strQ)   
             
            # print(tableResultAIR)
            distVals= tableResultAIR.to_json(orient='index')
            distVals=json.loads(distVals) 
            del tableResultAIR
# ##irr="tract_to_msa_income_percentage"
#             filterCnd=''
#             if userfilterCnd !='':
#                     filterCnd="("+userfilterCnd +") and"
#             filterCnd +=" "+leiValue +" and"
             
#             i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ dept +"'") 
                
#             strQ="select ttlapps.incomegrouop 'incomegroup',ttlappl,isnull(applconverted,0) applconverted,\
#                 round(isnull(cast( isnull(applconverted,0) as float)/ cast( (ttlappl) as float),0)*100,2) apprvd_rate from \
#                 (select incomegrouop,count(*) ttlappl from ( \
#                 select  case   when cast("+ i+ " as float)< 50 then 'Low' \
#                 when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
#                 when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
#                 when cast("+ i+ " as float)>= 120 then 'Upper' \
#                 end incomegrouop from fl_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
#                 )   incomegroupdata group by incomegrouop)ttlapps left join \
#                 (select incomegrouop,count(*) applconverted from ( \
#                 select  case   when cast("+ i+ " as float)< 50 then 'Low' \
#                 when  cast("+ i+ " as float)>= 50 and cast("+ i+ " as float)< 80 then 'MOD' \
#                 when  cast("+ i+ " as float)>= 80 and cast("+ i+ " as float)< 120 then 'Middle' \
#                 when cast("+ i+ " as float)>= 120 then 'Upper' \
#                 end incomegrouop from fl_data where "+filterCnd+"  cast(case when "+rate_spread_col+"='NA' then Null else "+rate_spread_col+" end as float) >= "+ratespread + " and "+ activity_year_Field +"='"+ activity_year + "' \
#                 and "+ Action_taken_Field+" in ("+approved_and_denied+")   )   incomegroupdata group by incomegrouop) convertedapps \
#                 on ttlapps.incomegrouop=convertedapps.incomegrouop" 
            
#             ###tableResultApproved=  self.objdbops.getTable(strQ)  
#             #### print('col ',i )
#             #### print(tableResultAIR) 
#             ###distApplications= tableResultApproved.to_json(orient='index')
#             ###distApplications=json.loads(distApplications)
#             ###dictApplications[irr] = distApplications
#             ###
            strQ="select B_address,b_city,b_state,b_zip,B_Lat,B_Long from Bank_Branches "  
            tableResultBranch=  self.objdbops.getTable(strQ)   
            # print('col ',i )
            print('StateLatLong Branch',tableResultBranch)
            print(strQ)
            distBranch= tableResultBranch.to_json(orient='index')
            distBranch=json.loads(distBranch) 
            del tableResultBranch
                
            return JsonResponse({'FilterStateLatLong':distVals, 'BankBranches':distBranch })
        except Exception as e:
            print('StateLatLong ',e,traceback.print_exc())
            return JsonResponse({'StateLatLong':'false'})

class get_Filter_County_Lat_long(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
            State = request.data['State'] 
            peer = request.data['peer'] 
            filter_col=request.data['filter_col']
            peergrouplei=getFilterCndnNValue(self,dept,portfolio,'Peer Group')   
            filterCnd=''
            appovedCndn=getFilterCndn(self,dept,portfolio,'Approved')
            deniedCndn=getFilterCndn(self,dept,portfolio,'Denied')
            approved_and_denied=getFilterCndn(self,dept,portfolio,'Approved and Denied')
              
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ dept +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ dept +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']   
            strQ="select isnull(max(filter_Condn),'') filter_Condn from FL_Filter_Criteria where added_by="+ str(uid) 
            filterCnd=self.objdbops.getscalar(strQ) 
            if peer=='n':
                leiValue=getFilterCndnNValue(self,dept,portfolio,'Bank ID')
            elif peer=='y':
                leiValue=getFilterCndnNValue(self,dept,portfolio,'Peer Group')
            print('leiValue is ',leiValue)
            
            if filterCnd !='':
                filterCnd="("+filterCnd +") and"
            filterCnd +=" "+leiValue +" and"    

            ## select Field_10, max(county) CountyName,dt.Field_5 ,count(*) RowCnt,max(cy.lat) lat,max(cy.lng) long 
            ## from FL_Data dt join FL_County_Lat_Lng cy on dt.Field_5=cy.county_fips
            ## where Field_2='N8T7HW55LK5D2ORCKP39' group by Field_10,Field_5 order by 2,1
           
            i=getFLDbCol(self,"county_code",dept,portfolio)    
            FilterColName=getFLDbCol(self,filter_col,dept,portfolio)
            st=getFLDbCol(self,"state_code",dept,portfolio)   
            print('get_Filter_County_Lat_long : ',i,':',filter_col,':',FilterColName,':')
            strQ="select dt."+FilterColName+" FilVal,cy.county CountyName,count(*) RowCnt,max(cy.lat) lat,max(cy.lng) long  \
                from FL_Data dt join FL_County_Lat_Lng cy on dt."+i+"=cy.county_fips \
                where "+filterCnd +" " + activity_year_Field +"='"+ request.data['activity_year']+"' and dt."+st+"='"+State+"' group by dt."+FilterColName+",cy.county \
                order by row_number() over (partition by cy.county order by cy.county,count(cy.county) desc), cy.county"  
            print('get_Filter_County_Lat_long ',strQ)
            tableResultAIR=  self.objdbops.getTable(strQ)   
             
            # print(tableResultAIR)
            distVals= tableResultAIR.to_json(orient='index')
            distVals=json.loads(distVals) 
            del tableResultAIR

            strQ="select B_address,b_city,b_state,b_zip,B_Lat,B_Long from Bank_Branches where trim(B_STATE)='"+State+"'"
            tableResultBranch=  self.objdbops.getTable(strQ)   
            # print('col ',i )
            print('StateLatLong Branch',tableResultBranch)
            print(strQ)
            distBranch= tableResultBranch.to_json(orient='index')
            distBranch=json.loads(distBranch) 
            del tableResultBranch
                
            return JsonResponse({'FilterCountyLatLong':distVals, 'BankBranches':distBranch })
        except Exception as e:
            print('StateLatLong ',e,traceback.print_exc())
            return JsonResponse({'StateLatLong':'false'})

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

class get_DeniedRecordsMatchedPair(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            portfolio = request.data['portfolio']  
            dept = str(request.data['dept'])   
            filterCnd='' 
            deniedCndn=getFilterCndn(self,dept,portfolio,'Denied')              
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ dept +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ dept +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']   
           
            userfilterCnd=getUserFilter(self,uid,portfolio,dept,'MatchedPair') 
             
            leiValue=getFilterCndnNValue(self,dept,portfolio,'Bank ID') 
            if userfilterCnd !='':
                filterCnd="("+userfilterCnd +") and"
            filterCnd +=" "+leiValue +" and"   
            uidcol=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from  FL_Mapping_Details fl_map_dtl where  upper(Excel_Fields)='UID' and  Portfolio ='"+ portfolio +"' and department='"+ dept +"'")   
            strQ="select Database_Fields,Excel_Fields from FL_mapping_Details where  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'"
            dfResultDenied=self.objdbops.getTable(strQ) 
            strQ="Select "+uidcol+" 'unique_id', "
            for index, row in dfResultDenied.iterrows():
                strQ+=" "+ row['Database_Fields']+ " "+row['Excel_Fields']+" ," 
            strQ=strQ[:-2]
            strQ+="  from FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "'  and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'  and "+ Action_taken_Field+" in ("+deniedCndn+")  " 
            
            del dfResultDenied
            mdldata="{}"
            colList=[]
            tableResult=  self.objdbops.getTable(strQ) 
            if tableResult.empty == False:
                tableResult=tableResult.head(50)
                mdldata= tableResult.to_json(orient='records')
                colList=list(tableResult.columns.values)
            del tableResult
            
            strFilter=getUserFilter(self,uid,portfolio,dept,'MatchedPair') #"Field_4 = 'PA' or Field_4 = 'NC' and Field_1 = '2023'" 
            filterSelected=strFilter
            res = [i for i in range(len(strFilter)) if strFilter.startswith("Field_", i)]   
            for idx in res:
                startidx=6+idx
                endidx=startidx+2  
                filterSelected=filterSelected.replace("Field_"+str(strFilter[startidx:endidx]),getFLExcelCol(self,"Field_"+str(strFilter[startidx:endidx]),dept,portfolio))
                 
            return Response({'gridData':json.loads(mdldata),'filterSelected':filterSelected,'colList':colList})  
        except Exception as e:
            print('StateLatLong ',e,traceback.print_exc())
            return JsonResponse({'StateLatLong':'false'})


class Get_MatchedPairs_Data(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            # client = chromadb.PersistentClient("./data/") 
            # collection = client.get_or_create_collection(name="lar")
            # documents = [] 
            # ids = []
            # count = 0
            # portfolio = request.data['portfolio']  
            # dept = str(request.data['dept'])   
            # selected_id= request.data['selectedId']  
            # arrCols= request.data['colselection']   
            # filterCnd='' 
            # deniedCndn=getFilterCndn(self,dept,portfolio,'Denied')            
            # approvedCndn=getFilterCndn(self,dept,portfolio,'Approved')              
            # activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ dept +"'")   
            # Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ dept +"'")   
            # uid = request.data['uid']  
            # activity_year = request.data['activity_year']    
            # filterCnd=getUserFilter(self,uid,portfolio,dept,'MatchedPair') 
                
            # leiValue=getFilterCndnNValue(self,dept,portfolio,'Bank ID') 
            # if filterCnd !='':
            #     filterCnd="("+filterCnd +") and"
            # filterCnd +=" "+leiValue +" and"  
            # # arrCols=['derived_race','derived_sex','derived_ethnicity','applicant_age','uid'] 
            # strQ = "  select added_by,\
            #         ( SELECT  concat(col_nm,' ',col_oprtr,' ''',col_val,'''  and ') \
            #         from FL_Ctrl_Class_Criteria where added_by="+ str(uid) +" \
            #             and Tab_Selected ='MatchedPair' FOR XML PATH ('')) as whereclause, \
            #         ( SELECT  concat(col_nm,' ,') \
            #         from FL_Ctrl_Class_Criteria where added_by="+ str(uid) +" \
            #         and Tab_Selected ='MatchedPair'  FOR XML PATH ('')) as colgroup  from FL_Ctrl_Class_Criteria  where added_by="+ str(uid) +" \
            #             and Tab_Selected ='MatchedPair' group by added_by"        
            # tableResult=  self.objdbops.getTable(strQ)  
            
            # strQ="Select "
            # selected_rec_id=''
            # arrCols.append('uid')
            # for irr in arrCols:
            #     i=self.objdbops.getscalar("select Database_Fields from FL_mapping_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
            #     if irr=='uid': 
            #         selected_rec_id =" and  "+i+" = '"+selected_id +"'"
                      
            #     strQ+=" "+ i + " "+irr+" ,"
            # strQ=strQ[:-2]
            # strQ+="   from FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "'  and "+ Action_taken_Field+" in ("+deniedCndn+") and  Portfolio ='"+ portfolio +"' and department='"+ dept +"'"   
            # mdldata="{}"   
            # searchdata=  self.objdbops.getTable(strQ+selected_rec_id)  
            # strQ="Select "
            # for irr in arrCols:
            #     i=self.objdbops.getscalar("select Database_Fields from FL_mapping_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
            #     strQ+=" "+ i + " "+irr+" ," 
            # strQ=strQ[:-2]
            # strQ+="   from FL_data where "+tableResult.values[0][1]+" "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "'  and "+ Action_taken_Field+" in ("+approvedCndn+") and  Portfolio ='"+ portfolio +"' and department='"+ dept +"'"   
             
            # df=  self.objdbops.getTable(strQ) 
            # # client = chromadb.PersistentClient("./data/")
            # # collection = client.get_or_create_collection(name="lar")
            # # documents = []
            # # ids = []
            # # index_columns = ["uid"]
            # # for row in df.iterrows():
            # #     index = str(row[1][index_columns].values)
                
            # #     d = row[1].to_dict() 
            # #     for c in index_columns:
            # #         d.pop(c) 
            # #     ids.append(index)
            # #     documents.append(str(d)) 
            # #     if count == 250:
            # #         print('count ',count)
            # #         collection.add(documents = documents, ids = ids)
            # #         count = 0
            # #         documents = []
            # #         ids=[]
            # #     count+=1
            # del df
            # print('searchdata ',searchdata)
            # matchedPairs=similar_record(self,searchdata.loc[0, :],portfolio,dept)
            return Response({'gridData':""})  
        except Exception as e:
            print('Matched pair ',e,traceback.print_exc())
            return JsonResponse({'gridData':'false'})

class get_Bank_lat_long_state(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
            peer = request.data['peer'] 
            filter_col=request.data['filter_col']
            peergrouplei=getFilterCndnNValue(self,dept,portfolio,'Peer Group')   
            filterCnd=''
         
             
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ dept +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ dept +"'")   
            uid = request.data['uid']   
            strQ="select isnull(max(filter_Condn),'') filter_Condn from FL_Filter_Criteria where added_by="+ str(uid) 
            filterCnd=self.objdbops.getscalar(strQ) 
            if peer=='n':
                leiValue=getFilterCndnNValue(self,dept,portfolio,'Bank ID')
            elif peer=='y':
                leiValue=getFilterCndnNValue(self,dept,portfolio,'Peer Group')
            print('leiValue is ',leiValue)
            
            if filterCnd !='':
                filterCnd="("+filterCnd +") and"
            filterCnd +=" "+leiValue +" and"    

            ## select Field_10, max(county) CountyName,dt.Field_5 ,count(*) RowCnt,max(cy.lat) lat,max(cy.lng) long 
            ## from FL_Data dt join FL_County_Lat_Lng cy on dt.Field_5=cy.county_fips
            ## where Field_2='N8T7HW55LK5D2ORCKP39' group by Field_10,Field_5 order by 2,1    

            #i=getFLDbCol(self,"county_code",dept,portfolio)
            #st=getFLDbCol(self,"state_code",dept,portfolio)  
            
            i=getFLDbCol(self,"state_code",dept,portfolio)
            if filter_col=='':
                # i=getFLDbCol(self,"state_code",dept,portfolio)
                strQ="select dt."+i+" state,count(*) RowCnt,max(st.lat) lat,max(st.lng) long  \
                    from FL_Data dt join FL_State_Lat_Lng st \
                    on dt."+i+"=st.state_id where "+filterCnd +" " + activity_year_Field +"='"+ request.data['activity_year']+"' group by dt."+i+""
            elif filter_col=="tract_to_msa_income_percentage":
                #irr="tract_to_msa_income_percentage"                 
                incperc=getFLDbCol(self,"tract_to_msa_income_percentage",dept,portfolio)
                # i=getFLDbCol(self,"state_code",dept,portfolio)               

                # strQ="select case when cast(incomegrp as float)< 50 then 'Low' \
                #     when cast(incomegrp as float)>= 50 and cast(incomegrp as float)< 80 then 'MOD' \
                #     when cast(incomegrp as float)>= 80 and cast(incomegrp as float)< 120 then 'Middle' \
                #     when cast(incomegrp as float)>= 120 then 'Upper' end incomegrouop    ,field_4 from( \
                #     select  field_4,max(Field_96) incomegrp  from fl_data \
                #     where  Field_2 <> 'N8T7HW55LK5D2ORCKP39' and  Field_1='2023' group by field_4 ) incomegrpdata"

                strQ="select case when cast(incomegrp as float)< 50 then 'Low' when cast(incomegrp as float)>= 50 and cast(incomegrp as float)< 80 then 'MOD' \
                    when cast(incomegrp as float)>= 80 and cast(incomegrp as float)< 120 then 'Middle' when cast(incomegrp as float)>= 120 then 'Upper' end incomegroup, \
                    "+i+",cnt,st.lat lat,st.lng long from ( select  "+i+",max("+incperc+") incomegrp,count(*) cnt  from fl_data \
                    where  "+filterCnd +" " + activity_year_Field +"='"+ request.data['activity_year']+"' group by "+i+" ) incomegrpdata join FL_State_Lat_Lng st on "+i+"=st.state_id "
                
                # tableResultApproved=  self.objdbops.getTable(strQ)  
                # # print('col ',i )
                # # print(tableResultAIR) 
                # distApplications= tableResultApproved.to_json(orient='index')
                # distApplications=json.loads(distApplications)
                # dictApplications[irr] = distApplications
                # del tableResultApproved 
            else:
                FilterColName=getFLDbCol(self,filter_col,dept,portfolio)
                strQ="select dt."+FilterColName+" FilVal,dt."+i+" state,count(*) RowCnt,max(st.lat) lat,max(st.lng) long  \
                    from FL_Data dt join FL_State_Lat_Lng st \
                    on dt."+i+"=st.state_id where "+filterCnd +" " + activity_year_Field +"='"+ request.data['activity_year']+"' group by dt."+FilterColName+",dt."+i+" \
                    order by row_number() over (partition by dt."+i+" order by dt."+i+",count("+i+") desc), dt."+i+""  
            
            print('get_Bank_lat_long_state ',strQ)
            
            tableResultAIR=  self.objdbops.getTable(strQ)   
             
            #print(tableResultAIR)
            distVals= tableResultAIR.to_json(orient='index')
            distVals=json.loads(distVals) 
            del tableResultAIR

            strQ="select B_address,b_city,b_state,b_zip,B_Lat,B_Long from Bank_Branches"
            tableResultBranch=  self.objdbops.getTable(strQ)   
            ## print('col ',i )
            #print('StateLatLong Branch',tableResultBranch)
            print(strQ)
            distBranch= tableResultBranch.to_json(orient='index')
            distBranch=json.loads(distBranch) 
            del tableResultBranch

            strQ="select PB_Bank,replace(replace(PB_Branch,PB_Bank,''),',','') PB_Branch,PB_BranchType,PB_Address,PB_City,PB_State,PB_Zip,PB_Lat,PB_Long \
                from FL_Peer_Bank_Branches order by PB_State"
            tableResultPeerBranch=  self.objdbops.getTable(strQ)   
            ## print('col ',i )
            #print('PeerBank Branch',tableResultPeerBranch)
            print(strQ)
            distPeerBranch= tableResultPeerBranch.to_json(orient='index')
            distPeerBranch=json.loads(distPeerBranch) 
            del tableResultPeerBranch
                
            return JsonResponse({'StateLatLong':distVals, 'BankBranches':distBranch, 'PeerBankBranches':distPeerBranch  })
        except Exception as e:
            print('StateLatLong ',e,traceback.print_exc())
            return JsonResponse({'StateLatLong':'false'})

class get_Bank_lat_long_county(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
            peer = request.data['peer'] 
            filter_col=request.data['filter_col']
            State = request.data['State'] 
            peergrouplei=getFilterCndnNValue(self,dept,portfolio,'Peer Group')   
            filterCnd=''
            appovedCndn=getFilterCndn(self,dept,portfolio,'Approved')
            deniedCndn=getFilterCndn(self,dept,portfolio,'Denied')
            approved_and_denied=getFilterCndn(self,dept,portfolio,'Approved and Denied')
             
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ dept +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ dept +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']   
            strQ="select isnull(max(filter_Condn),'') filter_Condn from FL_Filter_Criteria where added_by="+ str(uid) 
            filterCnd=self.objdbops.getscalar(strQ) 
            if peer=='n':
                leiValue=getFilterCndnNValue(self,dept,portfolio,'Bank ID')
            elif peer=='y':
                leiValue=getFilterCndnNValue(self,dept,portfolio,'Peer Group')
            print('leiValue is ',leiValue)
            
            if filterCnd !='':
                filterCnd="("+filterCnd +") and"
            filterCnd +=" "+leiValue +" and"    

            ## select Field_10, max(county) CountyName,dt.Field_5 ,count(*) RowCnt,max(cy.lat) lat,max(cy.lng) long 
            ## from FL_Data dt join FL_County_Lat_Lng cy on dt.Field_5=cy.county_fips
            ## where Field_2='N8T7HW55LK5D2ORCKP39' group by Field_10,Field_5 order by 2,1
           
            # strQ="select dt."+i+" state,count(*) RowCnt,max(st.lat) lat,max(st.lng) long  \
            #     from FL_Data dt join FL_State_Lat_Lng st \
            #     on dt."+i+"=st.state_id where "+filterCnd +" " + activity_year_Field +"='"+ request.data['activity_year']+"' group by dt."+i+""

            i=getFLDbCol(self,"county_code",dept,portfolio)                
            st=getFLDbCol(self,"state_code",dept,portfolio)   

            if filter_col=='':
                strQ="select dt."+i+" CountyName,count(*) RowCnt,max(cy.lat) lat,max(cy.lng) long  \
                from FL_Data dt join FL_County_Lat_Lng cy on dt."+i+"=cy.county_fips \
                where "+filterCnd +" " + activity_year_Field +"='"+ request.data['activity_year']+"' and "+st+"='"+State+"' group by dt."+i+""

            elif filter_col=="tract_to_msa_income_percentage":                           
                incperc=getFLDbCol(self,"tract_to_msa_income_percentage",dept,portfolio)
                i=getFLDbCol(self,"county_code",dept,portfolio) 
                strQ="select case when cast(incomegrp as float)< 50 then 'Low' when cast(incomegrp as float)>= 50 and cast(incomegrp as float)< 80 then 'MOD' \
                    when cast(incomegrp as float)>= 80 and cast(incomegrp as float)< 120 then 'Middle' when cast(incomegrp as float)>= 120 then 'Upper' end incomegroup, \
                    cy.county CountyName,RowCnt,cy.lat lat,cy.lng long from ( select  "+i+",max("+incperc+") incomegrp,count(*) RowCnt from fl_data \
                    where  "+filterCnd +" " + activity_year_Field +"='"+ request.data['activity_year']+"' and "+st+"='"+State+"' group by "+i+" ) incomegrpdata join FL_County_Lat_Lng cy on "+i+"=cy.county_fips"
            else:
                FilterColName=getFLDbCol(self,filter_col,dept,portfolio)
                print('get_Filter_County_Lat_long : ',i,':',filter_col,':',FilterColName,':')
                strQ="select dt."+FilterColName+" FilVal,cy.county CountyName,count(*) RowCnt,max(cy.lat) lat,max(cy.lng) long  \
                    from FL_Data dt join FL_County_Lat_Lng cy on dt."+i+"=cy.county_fips \
                    where "+filterCnd +" " + activity_year_Field +"='"+ request.data['activity_year']+"' and dt."+st+"='"+State+"' group by dt."+FilterColName+",cy.county \
                    order by row_number() over (partition by cy.county order by cy.county,count(cy.county) desc), cy.county"  
            print('get_Filter_County_Lat_long ',strQ)
            tableResultAIR=  self.objdbops.getTable(strQ)   
             
            # print(tableResultAIR)
            distVals= tableResultAIR.to_json(orient='index')
            distVals=json.loads(distVals) 
            del tableResultAIR

            strQ="select B_address,b_city,b_state,b_zip,B_Lat,B_Long from Bank_Branches where trim(B_STATE)='"+State+"'"
            tableResultBranch=  self.objdbops.getTable(strQ)   
            # print('col ',i )
            print('StateLatLong Branch',tableResultBranch)
            print(strQ)
            distBranch= tableResultBranch.to_json(orient='index')
            distBranch=json.loads(distBranch) 
            del tableResultBranch

            strQ="select PB_Bank,replace(replace(PB_Branch,PB_Bank,''),',','') PB_Branch,PB_BranchType,PB_Address,PB_City,PB_State,PB_Zip,PB_Lat,PB_Long \
                from FL_Peer_Bank_Branches where trim(PB_STATE)='"+State+"' order by PB_State"
            tableResultPeerBranch=  self.objdbops.getTable(strQ)   
            # print('col ',i )
            print('PeerBank Branch',tableResultPeerBranch)
            print(strQ)
            distPeerBranch= tableResultPeerBranch.to_json(orient='index')
            distPeerBranch=json.loads(distPeerBranch) 
            del tableResultPeerBranch
                
            return JsonResponse({'CountyLatLong':distVals, 'BankBranches':distBranch, 'PeerBankBranches':distPeerBranch  })
        except Exception as e:
            print('StateLatLong ',e,traceback.print_exc())
            return JsonResponse({'StateLatLong':'false'})
        
class FLQtnsFinal(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
        
            context={'FLRating':objmaster.getFLRatings(objmaster.getmaxFLId()), 
                                                        'sections':objmaster.getFLtnSectionFinal(),'Qtns':objmaster.getFLQtnsFinal()}
            return Response( context, status=status.HTTP_200_OK)
        except Exception as e: 
            print(traceback.print_exc()) 
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)


class getFLSecQtnFinal(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:  
            return Response( {'sections':objmaster.getFLQtnsFinal()}, status=status.HTTP_200_OK)
        except Exception as e:
            print(traceback.print_exc())  
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class saveFLRatingsFinal(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:          
            colDataLst = request.data['colDataLst']
            uid=request.data['uid']
            json_colDataLst = json.loads(colDataLst)
            objreg=Register()
            maxid=objmaster.getmaxFLId()
            for colval in json_colDataLst: 
                objreg.updateFLRatingsFinal(colval["qtnId"],colval["ddl_yesno_"],colval["ddl_doc_"],colval["txt_comment_"],uid,maxid)
 
            return Response( {'is_taken':True}, status=status.HTTP_200_OK)
        except Exception as e:  
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)
         
class get_CountyMedianIncome(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        try:
            portfolio = request.data['Portfolio']  
            dept = str(request.data['Dept'])  
            #peer = request.data['peer'] 
            #filter_col=request.data['filter_col']
            #State = request.data['State'] 
            
            
            i=getFLDbCol(self,"county_code",dept,portfolio)                
            st=getFLDbCol(self,"state_code",dept,portfolio)   
           
            strQ="select case when cast(groupinf.infval as float)<=50000 then 'level1' \
                when cast(groupinf.infval as float)>50000 and cast(groupinf.infval as float)<=80000 then 'level2' \
                when cast(groupinf.infval as float)>80000 and cast(groupinf.infval as float)<=110000 then 'level3' \
                when cast(groupinf.infval as float)>110000 and cast(groupinf.infval as float)<=140000 then 'level4' \
                when cast(groupinf.infval as float)>140000 then 'level5' end incomegrp,cy.county CountyName,cy.lat lat,cy.lng long from \
                (select REPLACE(place,' County, '+statename,'') county,max(statename) state,max(infvalue) infval from FL_Param_Info \
                where placetype='county' group by  REPLACE(place,' County, '+statename,'')) groupinf \
                join FL_County_Lat_Lng cy on groupinf.county=cy.county and groupinf.state=cy.state_id \
                order by cy.county"
             
            tableResultAIR=  self.objdbops.getTable(strQ)    
            distVals= tableResultAIR.to_json(orient='index')
            distVals=json.loads(distVals) 
            del tableResultAIR

            strQ="select PB_Bank,replace(replace(PB_Branch,PB_Bank,''),',','') PB_Branch,PB_BranchType,PB_Address,PB_City,PB_State,PB_Zip,PB_Lat,PB_Long \
                from FL_Peer_Bank_Branches where trim(PB_Bank) in ('Comerica Bank') order by PB_State"
            tableResultBranch=  self.objdbops.getTable(strQ)   
            # print('col ',i ) 
            distBranch= tableResultBranch.to_json(orient='index')
            distBranch=json.loads(distBranch) 
            del tableResultBranch

            strQ="select PB_Bank,replace(replace(PB_Branch,PB_Bank,''),',','') PB_Branch,PB_BranchType,PB_Address,PB_City,PB_State,PB_Zip,PB_Lat,PB_Long \
                from FL_Peer_Bank_Branches where trim(PB_Bank) not in ('Comerica Bank') order by PB_State"
            tableResultPeerBranch=  self.objdbops.getTable(strQ)   
            # print('col ',i ) 
            distPeerBranch= tableResultPeerBranch.to_json(orient='index')
            distPeerBranch=json.loads(distPeerBranch) 
            del tableResultPeerBranch
                
            return JsonResponse({'CountyLatLong':distVals, 'BankBranches':distBranch, 'PeerBankBranches':distPeerBranch  })
        except Exception as e:
            print('StateLatLong ',e,traceback.print_exc())
            return JsonResponse({'StateLatLong':'false'})
 

class get_Filter_Selected(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        uid=request.data['uid']
        portfolio=request.data['Portfolio']
        dept=request.data['Dept']
        utility=request.data['utility']
        segNm=request.data['segNm']
        # strQ="select isnull(max(filter_Condn),'') filter_Condn from FL_Filter_Criteria where added_by="+ str(uid) +" and portfolio='"+ portfolio +"' and department='"+ str(dept) +"'"
        strCnt="select  count(*) filter_Condn from FL_Filter_Criteria where \
                added_by="+ str(uid) +" and portfolio='"+ portfolio +"' and department='"+ str(dept) +"' and utility='"+utility+"'"    
        tableResultJson=""
        strCnt=" select count(*) colgroup  from FL_Ctrl_Class_Criteria  where added_by="+ str(uid) +" \
                    and Tab_Selected ='"+ utility +"' "   
        if str(self.objdbops.getscalar(strCnt))=="0":
            tableResultJson =  "{}"
        else:
            strQ = "SELECT  col_nm,col_oprtr,col_val from FL_Ctrl_Class_Criteria where added_by="+ str(uid) +"   and Tab_Selected ='"+ utility +"'"    
            tableResult=  self.objdbops.getTable(strQ)
            tableResult= tableResult.to_json(orient='index')
            tableResultJson=json.loads(tableResult)   
            del tableResult 
        if str(self.objdbops.getscalar(strCnt))=="0":
            return  JsonResponse({'istaken':'true','filters':  "-",'CtrlClsSelected':tableResultJson,'segNm':[]})
        else:
            strQ="select  isnull((filter_Condn),'')  filter_Condn from FL_Filter_Criteria where \
                added_by="+ str(uid) +" and portfolio='"+ portfolio +"' and department='"+ str(dept) +"' and utility='"+utility+"'"    
            if segNm !="":
                strQ +=" and segment_name='"+segNm+"'"
            strQ +=" order by Added_On desc"
            filterSegNm=getUserFilterSegments(self,uid,portfolio,dept,utility) 
            return  JsonResponse({'istaken':'true','filters':   self.objdbops.getscalar(strQ) ,'CtrlClsSelected':tableResultJson,'segNm':filterSegNm})

class delete_Filter_Selected(APIView):
    objdbops =None
    permission_classes=[IsAuthenticated]
    def __init__(self):
        self.objdbops=dbops()
    def post(self,request):
        uid=request.data['uid']
        portfolio=request.data['Portfolio']
        dept=request.data['Dept']
        utility=request.data['utility']
        segNm=request.data['segNm']
        # strQ="select isnull(max(filter_Condn),'') filter_Condn from FL_Filter_Criteria where added_by="+ str(uid) +" and portfolio='"+ portfolio +"' and department='"+ str(dept) +"'"
        strCnt="delete from FL_Filter_Criteria where \
                added_by="+ str(uid) +" and portfolio='"+ portfolio +"' and department='"+ str(dept) +"' and utility='"+utility+"' and segment_name='"+segNm +"'"  
        self.objdbops.insertRow(strCnt)
        return  JsonResponse({'istaken':'true'})


def getUserFilterSegments(self,uid,portfolio,dept,utility):
    # strQ="select isnull(max(filter_Condn),'') filter_Condn from FL_Filter_Criteria where added_by="+ str(uid) +" and portfolio='"+ portfolio +"' and department='"+ str(dept) +"'"
    strCnt="select  count(*) filter_Condn from FL_Filter_Criteria where \
            added_by="+ str(uid) +" and portfolio='"+ portfolio +"' and department='"+ str(dept) +"' and utility='"+utility+"'"    
    if str(self.objdbops.getscalar(strCnt))=="0":
        return  "[]"
    else:
        strQ="select   isnull(segment_name,utility) segNm  from FL_Filter_Criteria where \
            added_by="+ str(uid) +" and portfolio='"+ portfolio +"' and department='"+ str(dept) +"' and utility='"+utility+"' group by segment_name,utility order by  max(Added_On) desc"    
        tableResult=  self.objdbops.getTable(strQ)
        tableResultJson=  tableResult['segNm'].tolist() 
        del tableResult
        return tableResultJson    



def getFLDbCol(self,excelcol,dept,portfolio):     
    return  self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Mapping_Details fl_map_dtl where  lower(Excel_Fields)=lower('"+excelcol+"') and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'")  
    # self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+excelcol+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 

def getFLExcelCol(self,dbcol,dept,portfolio):     
    return  self.objdbops.getscalar("select fl_map_dtl.Excel_Fields from FL_Mapping_Details fl_map_dtl where  lower(Database_Fields)=lower('"+dbcol+"') and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'")  
   
def getFilterCndn(self,dept,portfolio,cndn):
    return str(self.objdbops.getscalar("SELECT  Value filter_cndn FROM  FL_Value_Details where portfolio='"+ portfolio +"' and department='"+ str(dept) +"' and filter_condition='"+ cndn +"'"))

def getFilterCndnNValue(self,dept,portfolio,cndn):
    # print(("SELECT  concat(Database_Fields,' ',Operator,' ',Value) filter_cndn FROM  FL_Value_Details where portfolio='"+ portfolio +"' and department='"+ str(dept) +"' and filter_condition='"+ cndn +"'"))
    return str(self.objdbops.getscalar("SELECT  concat(Database_Fields,' ',Operator,' ',Value) filter_cndn FROM  FL_Value_Details where portfolio='"+ portfolio +"' and department='"+ str(dept) +"' and filter_condition='"+ cndn +"'"))

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
    
def getUserFilterPeerApplication(self,uid,portfolio,dept,utility):
    # strQ="select isnull(max(filter_Condn),'') filter_Condn from FL_Filter_Criteria where added_by="+ str(uid) +" and portfolio='"+ portfolio +"' and department='"+ str(dept) +"'"
    strCnt="  select  count(*) from FL_Filter_Criteria where \
            added_by="+ str(uid) +" and portfolio='"+ portfolio +"' and department='"+ str(dept) +"' and utility='"+utility+"' "  
    if str(self.objdbops.getscalar(strCnt))=="0":
        return ""
    else:
        strQ="select  isnull((filter_Condn),'') +' '+ case when lei_selected is null then ''else 'and '+lei_selected end  filter_Condn from FL_Filter_Criteria where \
            added_by="+ str(uid) +" and portfolio='"+ portfolio +"' and department='"+ str(dept) +"' and utility='"+utility+"'"
        return self.objdbops.getscalar(strQ) 


def similar_record(self,record,portfolio,dept):
    import ast
    try:
        client = chromadb.PersistentClient("./data/")
        collection = client.get_collection(name="lar")
        # d = record.to_ict()
        # ?d.pop("Unnamed: 0")
        result = collection.query(query_texts = [str(record.to_dict())])
        selIds= ''
        arr=[]
        arrayDT=[]
        arrRowdt=[]   
        for  val in result['ids'][0]:  
            selIds +="'"+(ast.literal_eval(val.replace('[','').replace(']','')))+"',"
        selIds=selIds[:-1] 
        # for i in result['documents'][0]:
        #     arrRowdt=[]  
        #     d = i.replace("nan", "'NaN'")  
        
        #     # using ast.literal_eval()
        #     # convert dictionary string to dictionary
        #     res = ast.literal_eval(d)
        #     # print result  
        #     for key,val in res.items(): 
        #         arrRowdt.append(val)
        #     arr.append(res)
        #     # arrayDT.append(arrRowdt) my_string = ','.join(my_list)
        uidcol=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from  FL_Mapping_Details fl_map_dtl where  upper(Excel_Fields)='UID' and  Portfolio ='"+ portfolio +"' and department='"+ dept +"'")   
        strQ="select Database_Fields,Excel_Fields from FL_mapping_Details where  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'"
        dfResultDenied=self.objdbops.getTable(strQ) 
        strQ="Select  "
        for index, row in dfResultDenied.iterrows():
            strQ+=" "+ row['Database_Fields']+ " "+row['Excel_Fields']+" ," 
        strQ=strQ[:-2]
        strQ+="  from FL_data where "+ uidcol + " in ("+ selIds +  ")" 
        del dfResultDenied
        mdldata="{}"
        colList=[]
        print(strQ)
        tableResult=  self.objdbops.getTable(strQ)  
        matchedPairs=""
        if tableResult.empty == False:
            tableResult=tableResult.head(50)
            matchedPairs= tableResult.to_json(orient='index')
            matchedPairs=json.loads(matchedPairs)
        del tableResult
        return matchedPairs
    except Exception as e:
        print(e, traceback.print_exc())
        return []

def getUserCtrlClsQuery(self,uid,portfolio,dept,utilty):
    strCnt=" select count(*) colgroup  from FL_Ctrl_Class_Criteria  where added_by="+ str(uid) +" \
                    and Tab_Selected ='"+ utilty +"' "  
    ctrlCLsQ=""
    ctrlCLsCols="" 
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
    
class saveimagedata(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data",request.data)
        serializer = FlDataanalysisImagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Image Data is created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

    
class get_FL_Report_Data_Varwise(APIView): 
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
            filterCnd='' 
            approved_and_denied=getFilterCndn(self,dept,portfolio,'Origination')  
            
            approved= getFilterCndn(self,dept,portfolio,'Approved')   
            denied= getFilterCndn(self,dept,portfolio,'Denied')         
            droppedout= getFilterCndn(self,dept,portfolio,'Dropout')
            activity_year_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and upper(fl_fld_dtl.Excel_Fields)='ACTIVITY_YEAR' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            Action_taken_Field=self.objdbops.getscalar("select fl_map_dtl.Database_Fields from FL_Field_Details fl_fld_dtl,FL_Mapping_Details fl_map_dtl where  fl_fld_dtl.Excel_Fields=fl_map_dtl.Excel_Fields and lower(fl_fld_dtl.Excel_Fields)='action_taken' and  fl_fld_dtl.Portfolio ='"+ portfolio +"' and fl_fld_dtl.department='"+ str(dept) +"'")   
            uid = request.data['uid']  
            activity_year = request.data['activity_year']    
            userfilterCnd=getUserFilter(self,uid,portfolio,dept,'Pricing_'+prohb_cls) 
            leiValue=getFilterCndnNValue(self,dept,portfolio,'Bank ID')     
            filterCnd=''     
            arrCols=[]#['derived_race','derived_sex','derived_ethnicity','applicant_age']
            arrCols.append(prohb_cls) 
            dictApplications=dict() 
            ctrlCLsQ,ctrlCLsCols=getUserCtrlClsQuery(self,uid,portfolio,dept,'Pricing_'+prohb_cls) 
             
            for irr in arrCols: 
                filterCnd=''
                if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+leiValue +" and" 
                print("irr----------------",irr)
                print("portfolio----------",portfolio)
                print("dept---------",str(dept))
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                print("i---------",i)
 
                filterCnd=''
                if userfilterCnd !='':
                    filterCnd="("+userfilterCnd +") and"
                filterCnd +=" "+leiValue +" and" 
                i=self.objdbops.getscalar("select Database_Fields from FL_Field_Details where lower(Excel_Fields)='"+irr+"' and  Portfolio ='"+ portfolio +"' and department='"+ str(dept) +"'") 
                strQ="select orginationData.ordCol,  orginationData.ClsLbl , orginationData.ttlappl,Originations,isnull(Denied,0) Denied,isnull(Dropped,0) Dropped from \
                (select    2 ordCol,ttlData."+ i+" ClsLbl , \
                round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float ),0)*100,2) \
                apprvd_rate,ttlappl,applconverted 'Originations'  from    \
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
                    ) dataa ) orginationData full join (select    2 ordCol,ttlData."+ i+" ClsLbl , \
                round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float ),0)*100,2) \
                apprvd_rate,ttlappl,applconverted 'Denied' from    \
                (select   "+ i+ ",count("+ Action_taken_Field+") ttlappl from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' and  CONCAT("+ctrlCLsCols+") not in( '"+ctrlCLsQ+"') group by  "+ i+ " )ttlData  left join   \
                ( select "+ i+ ",count("+ Action_taken_Field+") applconverted from  FL_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" in ("+denied+")  and  CONCAT("+ctrlCLsCols+") not in( '"+ctrlCLsQ+"') \
                group by "+ i+ " ) apprvdData on \
                ttlData."+ i+ " =apprvdData."+ i  +") deniedData on orginationData.ClsLbl=deniedData.ClsLbl full join (select    2 ordcol,ttlData."+ i+" ClsLbl , \
                round(isnull(cast( applconverted as float)/ cast( (ttlappl) as float ),0)*100,2) \
                apprvd_rate,ttlappl,applconverted   'Dropped' from    \
                (select   "+ i+ ",count("+ Action_taken_Field+") ttlappl from  FL_data where "+filterCnd+" "+ activity_year_Field +"='"+ activity_year + "' and  CONCAT("+ctrlCLsCols+") not in( '"+ctrlCLsQ+"') group by  "+ i+ " )ttlData  left join   \
                ( select "+ i+ ",count("+ Action_taken_Field+") applconverted from  FL_data where "+filterCnd+"  "+ activity_year_Field +"='"+ activity_year + "' \
                and "+ Action_taken_Field+" not in ("+droppedout+")  and  CONCAT("+ctrlCLsCols+") not in( '"+ctrlCLsQ+"') \
                group by "+ i+ " ) apprvdData on \
                ttlData."+ i+ " =apprvdData."+ i  +"   ) dropoutData on orginationData.ClsLbl=dropoutData.ClsLbl order by 1,2" 
                 
                tableResultApproved=  self.objdbops.getTable(strQ)    
                distApplications= tableResultApproved.to_json(orient='index')
                distApplications=json.loads(distApplications)
                dictApplications['Dropout'] = distApplications
                del tableResultApproved
                
            strFilter=getUserFilter(self,uid,portfolio,dept,'Pricing_'+prohb_cls) #"Field_4 = 'PA' or Field_4 = 'NC' and Field_1 = '2023'" 
            filterSelected=strFilter
            res = [i for i in range(len(strFilter)) if strFilter.startswith("Field_", i)]   
            for idx in res:
                startidx=6+idx
                endidx=startidx+2  
                filterSelected=filterSelected.replace("Field_"+str(strFilter[startidx:endidx]),getFLExcelCol(self,"Field_"+str(strFilter[startidx:endidx]),dept,portfolio))

            print('dictApplications ',dictApplications) 
            
              
            return JsonResponse({'istaken':'true','apps':dictApplications,'filterSelected':filterSelected })
        except Exception as e:
            print('updateaccess ',e,traceback.print_exc())
            return JsonResponse({'istaken':'false'})
   

class fl_data_file_info(APIView):
    permission_classes=[IsAuthenticated]    
    def post(self,request):
        print("req data",request.data)
        fl_data=FlDataFileInfo.objects.create(type_file=request.data['type'],department=request.data['dept'],portfolio=request.data['portfolio'],
        uploaded_by=request.data['uploaded_by'],uploaded_on=datetime.now(),upload_file_name=request.data['file_name'])

        return Response({'msg':"File Uploaded and Data Saved Successfully"})

