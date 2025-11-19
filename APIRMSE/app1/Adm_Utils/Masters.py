from app1.DAL.dboperations import dbops
from app1.models import *  
from datetime import datetime
import json
class MasterTbls:
    objdbops =None

    def __init__(self):
        self.objdbops=dbops()

    def getdbUsers(self):
        strQ="SELECT "
        strQ+=" sub.*,isnull(sup.u_name,'-') 'reportto',UC_Label ,case sub.activestatus when 1 then 'Active' else 'Inactive' end sts"
        strQ+=" FROM Users sub"
        strQ+=" left JOIN Users sup"
        strQ+=" ON sub.U_reportto = sup.U_AID"
        strQ+=" join User_Category uc on  sub.uc_aid=uc.uc_aid"
        strQ+=" ORDER BY sub.U_reportto"
        tableResult =self.objdbops.getTable(strQ)
        return tableResult
    
    def getdbUsersAddedBy(self,UId):
        strQ="SELECT "
        strQ+=" sub.*,isnull(sup.u_name,'-') 'reportto',UC_Label ,case sub.activestatus when 1 then 'Active' else 'Inactive' end sts"
        strQ+=" FROM Users sub"
        strQ+=" left JOIN Users sup"
        strQ+=" ON sub.U_reportto = sup.U_AID"
        strQ+=" join User_Category uc on  sub.uc_aid=uc.uc_aid where sub.AddedBy='"+UId.replace("'","''")+"'"
        strQ+=" ORDER BY sub.U_reportto"
        tableResult =self.objdbops.getTable(strQ)
        return tableResult
    
    def getQtnSections(self):
        strQ="SELECT Section_AID,Section_Label FROM Question_Sections order by Section_AID"
        tableResult =self.objdbops.getTable(strQ)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    
    def insertQuestion(self,section,qtn):
        
        if(str(self.objdbops.getscalar("SELECT  count(Section_AID) cnt   FROM Question_Sections where Section_Label='"+section +"'"))=="0"):
            
            self.objdbops.insertRow("INSERT INTO Question_Sections  (Section_Label ,ActiveStatus ,AddDate ) VALUES ('"+section +"' ,1 ,getdate())")

        sectionid=self.objdbops.getscalar("SELECT Section_AID cnt   FROM Question_Sections where Section_Label='"+section +"'")
        strQ="INSERT INTO Question_Master (Question_Label ,Section_AID,AddDate) "
        strQ += " VALUES  ('"+ qtn+"','"+ str(sectionid)+"',getdate())" 
        self.objdbops.insertRow(strQ)
      
    def getQtn(self,section,userId):
        strQ="SELECT Question_AID,Question_Label FROM Question_Master where Section_AID="+ str(section) 
        strQ +=" and Question_AID not in(select  Question_AID from Criteria_Setting_Temp where AddedBy ="+  str(userId )+") order by Question_AID"
        
        tableResult =self.objdbops.getTable(strQ)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    
    def insertTempCriteria(self,section,qtnId,Opt,Val,userID):
        strQ="INSERT INTO Criteria_Setting_Temp (Section_AID ,Question_AID ,Operator ,Val ,AddedBy)"
        strQ += " VALUES ( "+ str(section)+", "+ str(qtnId) +", '"+ Opt+"', '"+ Val+"', "+  str(userID )+")"
        print('strQ ',strQ)
        self.objdbops.insertRow(strQ)
    
    def getTempCriteria(self,userID):
        strQ="select ROW_NUMBER() over(order by ROwidx) rownum  , cst.*,qm.Question_Label qtn,Section_Label Section from  Criteria_Setting_Temp cst,Question_Master qm,"
        strQ += " Question_Sections qs "
        strQ += " where cst.Question_AID=qm.Question_AID and qs.Section_AID=cst.Section_AID and qm.Section_AID=qs.Section_AID and cst.AddedBy="+ str(userID)    +" order by ROwidx"     
        tableResult =self.objdbops.getTable(strQ)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    
    def getNewCriteriaId(self):
        strQ="select count(distinct Criteria_AID)+1 crid from [Criteria_Setting]"
        return self.objdbops.getscalar(strQ)
    
    def insertCriteria(self,criteriaId,userId,isModelTool,json_dictionary):
        strQ="INSERT INTO  Criteria_Setting (Criteria_AID  ,Is_Model_Tool ,Section_AID ,Question_AID  ,Operator ,Val, ROwidx,AddedBy ,AddDate) "
        strQ += " select '"+ criteriaId +"'  ,'"+ isModelTool +"' ,Section_AID ,Question_AID ,Operator ,Val ,ROwidx,AddedBy ,getdate() from Criteria_Setting_temp where AddedBy='"+ str(userId) +"' "
        self.objdbops.insertRow(strQ)
        for colval in json_dictionary:
            for attribute, value in colval.items():              
                strQ="update Criteria_Setting set Logical_Opt='"+ value +"' where AddedBy='"+ str(userId) +"' and  ROwidx="+str(attribute)
                self.objdbops.insertRow(strQ)
        self.objdbops.insertRow("delete from Criteria_Setting_temp where AddedBy='"+ str(userId) +"'")

    def getCriteria(self):
        strQ="select case when rownum=1 then 'add' "
        strQ += " when lead_section_aid is not null and lead_section_aid != section_aid then 'add' "
        strQ += " else '' end addseclbl, * from("
        strQ += " select ROW_NUMBER() over(order by question_aid) rownum, lag(qm.section_aid) OVER(ORDER BY qm.section_aid) as lead_section_aid,"
        strQ += " sm.section_label, qm.* from  Question_Master qm,Question_Sections sm where qm.section_aid=sm.section_aid"
        strQ += " ) crdata"
        strQ += " order by section_aid,question_aid"
        tableResult =self.objdbops.getTable(strQ)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    
    def insertFunctionOption(self,opt,desc,tbl,activests,userId):
        if(tbl=="1"):
            strQ="insert into Model_Function_Master ("
            strQ += " Mdl_Fncn_Label   ,"
            strQ += " Mdl_Fncn_Description  ,"
            strQ += " ActiveStatus ,"
            strQ += " AddedBy    ,"
            strQ += " AddDate  )"
            strQ += " values("
            strQ += " '"+opt.replace("'","''")+"'   ,"
            strQ += " '"+desc.replace("'","''")+"'  ,"
            strQ += " '"+activests.replace("'","''")+"' ,"
            strQ += " '"+userId.replace("'","''") +"'    ,"
            strQ += " GETDATE()  )	 "
            self.objdbops.insertRow(strQ)
        elif(tbl=="2"):
            strQ="insert into Model_Source_Master ("
            strQ += " Mdl_Src_Label   ,"
            strQ += " Mdl_Src_Description  ,"
            strQ += " ActiveStatus ,"
            strQ += " AddedBy    ,"
            strQ += " AddDate  )"
            strQ += " values("
            strQ += " '"+opt.replace("'","''")+"'   ,"
            strQ += " '"+desc.replace("'","''")+"'  ,"
            strQ += " '"+activests.replace("'","''")+"' ,"
            strQ += " '"+userId.replace("'","''") +"'    ,"
            strQ += " GETDATE()  )	 "
            self.objdbops.insertRow(strQ) 
        elif(tbl=="3"):
            strQ="insert into Model_Type_Master ("
            strQ += " Mdl_Type_Label   ,"
            strQ += " Mdl_Type_Description  ,"
            strQ += " ActiveStatus ,"
            strQ += " AddedBy    ,"
            strQ += " AddDate  )"
            strQ += " values("
            strQ += " '"+opt.replace("'","''")+"'   ,"
            strQ += " '"+desc.replace("'","''")+"'  ,"
            strQ += " '"+activests.replace("'","''")+"' ,"
            strQ += " '"+userId.replace("'","''") +"'    ,"
            strQ += " GETDATE()  )	 "
            self.objdbops.insertRow(strQ) 
        elif(tbl=="4"):
            strQ="insert into Prd_Addr_Master ("
            strQ += " Prd_Addr_Label   ,"
            strQ += " Prd_Addr_Description  ,"
            strQ += " ActiveStatus ,"
            strQ += " AddedBy    ,"
            strQ += " AddDate  )"
            strQ += " values("
            strQ += " '"+opt.replace("'","''")+"'   ,"
            strQ += " '"+desc.replace("'","''")+"'  ,"
            strQ += " '"+activests.replace("'","''")+"' ,"
            strQ += " '"+userId.replace("'","''") +"'    ,"
            strQ += " GETDATE()  )	 "
            self.objdbops.insertRow(strQ)  
        elif(tbl=="5"):
            strQ="insert into Model_Use_Freq_Master ("
            strQ += " Mdl_Use_Freq_Label   ,"
            strQ += " Mdl_Use_Freq_Description  ,"
            strQ += " ActiveStatus ,"
            strQ += " AddedBy    ,"
            strQ += " AddDate  )"
            strQ += " values("
            strQ += " '"+opt.replace("'","''")+"'   ,"
            strQ += " '"+desc.replace("'","''")+"'  ,"
            strQ += " '"+activests.replace("'","''")+"' ,"
            strQ += " '"+userId.replace("'","''") +"'    ,"
            strQ += " GETDATE()  )	 "
            self.objdbops.insertRow(strQ)   
        elif(tbl=="6"):
            strQ="insert into Mdl_Risk_Master ("
            strQ += " Mdl_Risk_Label   ,"
            strQ += " Mdl_Risk_Description  ,"
            strQ += " ActiveStatus ,"
            strQ += " AddedBy    ,"
            strQ += " AddDate  )"
            strQ += " values("
            strQ += " '"+opt.replace("'","''")+"'   ,"
            strQ += " '"+desc.replace("'","''")+"'  ,"
            strQ += " '"+activests.replace("'","''")+"' ,"
            strQ += " '"+userId.replace("'","''") +"'    ,"
            strQ += " GETDATE()  )	 "
            self.objdbops.insertRow(strQ)   
        elif(tbl=="7"):
            strQ="insert into Intrinsic_Master ("
            strQ += " Intrinsic_Label   ,"
            strQ += " Intrinsic_Description,"
            strQ += " ActiveStatus ,"
            strQ += " AddedBy    ,"
            strQ += " AddDate  )"
            strQ += " values("
            strQ += " '"+opt.replace("'","''")+"'   ,"
            strQ += " '"+desc.replace("'","''")+"'  ,"
            strQ += " '"+activests.replace("'","''")+"' ,"
            strQ += " '"+userId.replace("'","''") +"'    ,"
            strQ += " GETDATE()  )	 "
            self.objdbops.insertRow(strQ)    
        elif(tbl=="9"):
            strQ="insert into Materiality_Master ("
            strQ += " Materiality_Label   ,"
            strQ += " Materiality_Description  ,"
            strQ += " ActiveStatus ,"
            strQ += " AddedBy    ,"
            strQ += " AddDate  )"
            strQ += " values("
            strQ += " '"+opt.replace("'","''")+"'   ,"
            strQ += " '"+desc.replace("'","''")+"'  ,"
            strQ += " '"+activests.replace("'","''")+"' ,"
            strQ += " '"+userId.replace("'","''") +"'    ,"
            strQ += " GETDATE()  )	 "
            self.objdbops.insertRow(strQ)   
        elif(tbl=="8"):
            strQ="insert into Reliance_Master ("
            strQ += " Reliance_Label   ,"
            strQ += " Reliance_Description  ,"
            strQ += " ActiveStatus ,"
            strQ += " AddedBy    ,"
            strQ += " AddDate  )"
            strQ += " values("
            strQ += " '"+opt.replace("'","''")+"'   ,"
            strQ += " '"+desc.replace("'","''")+"'  ,"
            strQ += " '"+activests.replace("'","''")+"' ,"
            strQ += " '"+userId.replace("'","''") +"'    ,"
            strQ += " GETDATE()  )	 "
            self.objdbops.insertRow(strQ)    
        elif(tbl=="10"):
            strQ="insert into Mdl_Upstream ("
            strQ += " Mdl_Upstream_Label   ,"
            strQ += " Mdl_Upstream_Description  ,"
            strQ += " ActiveStatus ,"
            strQ += " AddedBy    ,"
            strQ += " AddDate  )"
            strQ += " values("
            strQ += " '"+opt.replace("'","''")+"'   ,"
            strQ += " '"+desc.replace("'","''")+"'  ,"
            strQ += " '"+activests.replace("'","''")+"' ,"
            strQ += " '"+userId.replace("'","''") +"'    ,"
            strQ += " GETDATE()  )	 "
            self.objdbops.insertRow(strQ) 
        elif(tbl=="11"):
            strQ="insert into Mdl_Dwstream ("
            strQ += " Mdl_Dwstream_Label   ,"
            strQ += " Mdl_Dwstream_Description  ,"
            strQ += " ActiveStatus ,"
            strQ += " AddedBy    ,"
            strQ += " AddDate  )"
            strQ += " values("
            strQ += " '"+opt.replace("'","''")+"'   ,"
            strQ += " '"+desc.replace("'","''")+"'  ,"
            strQ += " '"+activests.replace("'","''")+"' ,"
            strQ += " '"+userId.replace("'","''") +"'    ,"
            strQ += " GETDATE()  )	 "
            self.objdbops.insertRow(strQ)  
        elif(tbl=="12"):
            strQ="insert into Mdl_Montr_Freq ("
            strQ += " Mdl_Montr_Freq_Label   ,"
            strQ += " Mdl_Montr_Freq_Description  ,"
            strQ += " ActiveStatus ,"
            strQ += " AddedBy    ,"
            strQ += " AddDate  )"
            strQ += " values("
            strQ += " '"+opt.replace("'","''")+"'   ,"
            strQ += " '"+desc.replace("'","''")+"'  ,"
            strQ += " '"+activests.replace("'","''")+"' ,"
            strQ += " '"+userId.replace("'","''") +"'    ,"
            strQ += " GETDATE()  )	 "
            self.objdbops.insertRow(strQ)   

    def updateFunctionOption(self,optId,opt,desc,tbl,activests,userId):
        if(tbl=="1"):
            strQ="update Model_Function_Master set" 
            strQ += " Mdl_Fncn_Description = '"+desc.replace("'","''")+"'  ,"
            strQ += " ActiveStatus ='"+activests.replace("'","''")+"' ,"
            strQ += " UpdatedBy = '"+userId.replace("'","''") +"'  ,"
            strQ += " UpdateDate =GETDATE()  "   
            strQ += " where Mdl_Fncn_AID='"+optId.replace("'","''") +"' "
            self.objdbops.insertRow(strQ)
        elif(tbl=="2"):
            strQ="update Model_Source_Master set" 
            strQ += " Mdl_Src_Description = '"+desc.replace("'","''")+"'  ,"
            strQ += " ActiveStatus ='"+activests.replace("'","''")+"' ,"
            strQ += " UpdatedBy = '"+userId.replace("'","''") +"'  ,"
            strQ += " UpdateDate =GETDATE()  "  
            strQ += " where Mdl_Scr_AID='"+optId.replace("'","''") +"' "
            self.objdbops.insertRow(strQ) 
        elif(tbl=="3"):
            strQ=" update Model_Type_Master set" 
            strQ += " Mdl_Type_Description = '"+desc.replace("'","''")+"'  ,"
            strQ += " ActiveStatus ='"+activests.replace("'","''")+"' ,"
            strQ += " UpdatedBy = '"+userId.replace("'","''") +"'  ,"
            strQ += " UpdateDate =GETDATE()  "  
            strQ += " where Mdl_Type_AID='"+optId.replace("'","''") +"' "
            self.objdbops.insertRow(strQ) 
        elif(tbl=="4"):
            strQ="update Prd_Addr_Master set " 
            strQ += " Prd_Addr_Description  = '"+desc.replace("'","''")+"'  ,"
            strQ += " ActiveStatus ='"+activests.replace("'","''")+"' ,"
            strQ += " UpdatedBy = '"+userId.replace("'","''") +"'  ,"
            strQ += " UpdateDate =GETDATE()  "  
            strQ += " where Prd_Addr_AID='"+optId.replace("'","''") +"' "
            self.objdbops.insertRow(strQ)  
        elif(tbl=="5"):
            strQ="update Model_Use_Freq_Master set " 
            strQ += " Mdl_Use_Freq_Description  = '"+desc.replace("'","''")+"'  ,"
            strQ += " ActiveStatus ='"+activests.replace("'","''")+"' ,"
            strQ += " UpdatedBy = '"+userId.replace("'","''") +"'  ,"
            strQ += " UpdateDate =GETDATE()  "  
            strQ += " where Mdl_Use_Freq_AID='"+optId.replace("'","''") +"' "
            self.objdbops.insertRow(strQ)   
        elif(tbl=="6"):
            strQ="update Mdl_Risk_Master set " 
            strQ += " Mdl_Risk_Description  = '"+desc.replace("'","''")+"'  ,"
            strQ += " ActiveStatus  ='"+activests.replace("'","''")+"' ,"
            strQ += " UpdatedBy = '"+userId.replace("'","''") +"'  ,"
            strQ += " UpdateDate =GETDATE()  "  
            strQ += " where Mdl_Risk_AID='"+optId.replace("'","''") +"' "
            self.objdbops.insertRow(strQ)   
        elif(tbl=="7"):
            strQ="update Intrinsic_Master set " 
            strQ += " Intrinsic_Description= '"+desc.replace("'","''")+"'  ," 
            strQ += " ActiveStatus ='"+activests.replace("'","''")+"' ,"
            strQ += " UpdatedBy = '"+userId.replace("'","''") +"'  ,"
            strQ += " UpdateDate =GETDATE()  "  
            strQ += " where Intrinsic_AID='"+optId.replace("'","''") +"' "
            self.objdbops.insertRow(strQ)    
        elif(tbl=="9"):
            strQ="update Materiality_Master set " 
            strQ += " Materiality_Description  = '"+desc.replace("'","''")+"'  ," 
            strQ += " ActiveStatus ='"+activests.replace("'","''")+"' ,"
            strQ += " UpdatedBy = '"+userId.replace("'","''") +"'  ,"
            strQ += " UpdateDate =GETDATE()  "  
            strQ += " where Materiality_AID='"+optId.replace("'","''") +"' "
            self.objdbops.insertRow(strQ)   
        elif(tbl=="8"):
            strQ="update Reliance_Master set " 
            strQ += " Reliance_Description= '"+desc.replace("'","''")+"'  ," 
            strQ += " ActiveStatus ='"+activests.replace("'","''")+"' ,"
            strQ += " UpdatedBy = '"+userId.replace("'","''") +"'  ,"
            strQ += " UpdateDate =GETDATE()  "  
            strQ += " where Reliance_AID='"+optId.replace("'","''") +"' "
            self.objdbops.insertRow(strQ)    
        elif(tbl=="10"):
            strQ="update into Mdl_Upstream set " 
            strQ += " Mdl_Upstream_Description = '"+desc.replace("'","''")+"'  ," 
            strQ += " ActiveStatus ='"+activests.replace("'","''")+"' ,"
            strQ += " UpdatedBy = '"+userId.replace("'","''") +"'  ,"
            strQ += " UpdateDate =GETDATE()  "  
            strQ += " where Mdl_Upstream_AID='"+optId.replace("'","''") +"' "
            self.objdbops.insertRow(strQ) 
        elif(tbl=="11"):
            strQ="update into Mdl_Dwstream set " 
            strQ += " Mdl_Dwstream_Description = '"+desc.replace("'","''")+"'  ," 
            strQ += " ActiveStatus ='"+activests.replace("'","''")+"' ,"
            strQ += " UpdatedBy = '"+userId.replace("'","''") +"'  ,"
            strQ += " UpdateDate =GETDATE()  "  
            strQ += " where Mdl_Dwstream_AID='"+optId.replace("'","''") +"' "
            self.objdbops.insertRow(strQ)  
        elif(tbl=="12"):
            strQ="update into Mdl_Montr_Freq set " 
            strQ += " Mdl_Montr_Freq_Description= '"+ desc.replace("'","''")+"'  ," 
            strQ += " ActiveStatus ='"+activests.replace("'","''")+"' ,"
            strQ += " ActiveStatus ='"+activests.replace("'","''")+"' ,"
            strQ += " UpdatedBy = '"+userId.replace("'","''") +"'  ,"
            strQ += " UpdateDate =GETDATE()  "  
            strQ += " where Mdl_Montr_Freq_AID='"+optId.replace("'","''") +"' "
            self.objdbops.insertRow(strQ)   


    def getMasterTblData(self,tbl):
        if(tbl=="1"):
            tableResult =self.objdbops.getTable("select case ActiveStatus when 1 then 'Active' else 'Inactive' end sts, Mdl_Fncn_AID AID, Mdl_Fncn_Label opt ,Mdl_Fncn_Description 'desc' from Model_Function_Master order by AddDate")
            tableResult= tableResult.to_json(orient='index')
            return json.loads(tableResult)
        elif(tbl=="2"):
            tableResult =self.objdbops.getTable("select case ActiveStatus when 1 then 'Active' else 'Inactive' end sts, Mdl_Scr_AID AID,Mdl_Src_Label opt ,Mdl_Src_Description 'desc' from Model_Source_Master order by AddDate")
            tableResult= tableResult.to_json(orient='index')
            return json.loads(tableResult)
        elif(tbl=="3"):
            tableResult =self.objdbops.getTable("select case ActiveStatus when 1 then 'Active' else 'Inactive' end sts,Mdl_Type_AID AID,Mdl_Type_Label opt ,Mdl_Type_Description 'desc' from Model_Type_Master order by AddDate")
            tableResult= tableResult.to_json(orient='index')
            return json.loads(tableResult)
        elif(tbl=="4"):
            tableResult =self.objdbops.getTable("select case ActiveStatus when 1 then 'Active' else 'Inactive' end sts, Prd_Addr_AID AID, Prd_Addr_Label opt ,Prd_Addr_Description 'desc' from Prd_Addr_Master order by AddDate")
            tableResult= tableResult.to_json(orient='index')
            return json.loads(tableResult)
        elif(tbl=="5"):
            tableResult =self.objdbops.getTable("select case ActiveStatus when 1 then 'Active' else 'Inactive' end sts, Mdl_Use_Freq_AID AID, Mdl_Use_Freq_Label opt , Mdl_Use_Freq_Description 'desc' from Model_Use_Freq_Master order by AddDate")
            tableResult= tableResult.to_json(orient='index')
            return json.loads(tableResult)
        elif(tbl=="6"):
            tableResult =self.objdbops.getTable("select case ActiveStatus when 1 then 'Active' else 'Inactive' end sts, Mdl_Risk_AID AID, Mdl_Risk_Label opt ,Mdl_Risk_Description  'desc' from Mdl_Risk_Master order by AddDate")
            tableResult= tableResult.to_json(orient='index')
            return json.loads(tableResult) 
        elif(tbl=="7"):
            tableResult =self.objdbops.getTable("select case ActiveStatus when 1 then 'Active' else 'Inactive' end sts, Intrinsic_AID AID, Intrinsic_Label opt , Intrinsic_Description  'desc' from Intrinsic_Master order by AddDate")
            tableResult= tableResult.to_json(orient='index')
            return json.loads(tableResult)
        elif(tbl=="9"):
            tableResult =self.objdbops.getTable("select case ActiveStatus when 1 then 'Active' else 'Inactive' end sts, Materiality_AID AID, Materiality_Label opt ,Materiality_Description  'desc' from Materiality_Master order by AddDate")
            tableResult= tableResult.to_json(orient='index')
            return json.loads(tableResult) 
        elif(tbl=="8"):
            tableResult =self.objdbops.getTable("select  case ActiveStatus when 1 then 'Active' else 'Inactive' end sts,Reliance_AID AID, Reliance_Label opt ,  Reliance_Description'desc' from Reliance_Master order by AddDate")
            tableResult= tableResult.to_json(orient='index')
            return json.loads(tableResult)  
        elif(tbl=="10"):
            tableResult =self.objdbops.getTable("select case ActiveStatus when 1 then 'Active' else 'Inactive' end sts, Mdl_Upstream_AID AID, Mdl_Upstream_Label opt , Mdl_Upstream_Description'desc' from  Mdl_Upstream  order by AddDate")
            tableResult= tableResult.to_json(orient='index')
            return json.loads(tableResult)  
        elif(tbl=="11"):
            tableResult =self.objdbops.getTable("select case ActiveStatus when 1 then 'Active' else 'Inactive' end sts, Mdl_Dwstream_AID AID, Mdl_Dwstream_Label opt , Mdl_Dwstream_Description'desc' from  Mdl_Dwstream  order by AddDate")
            tableResult= tableResult.to_json(orient='index')
            return json.loads(tableResult) 
        elif(tbl=="12"):
            tableResult =self.objdbops.getTable("select case ActiveStatus when 1 then 'Active' else 'Inactive' end sts, Mdl_Montr_Freq_AID AID, Mdl_Montr_Freq_Label opt ,Mdl_Montr_Freq_Description'desc' from Mdl_Montr_Freq order by AddDate")
            tableResult= tableResult.to_json(orient='index')
            return json.loads(tableResult)  
 
    def checkUniqueVal(self,tbl,val,dept="",ucid=""):
        if tbl =="UC":
            return self.objdbops.getscalar("select count(*) from User_Category where upper(UC_Label)=upper('"+ val +"') ")
        elif tbl =="users":
            return self.objdbops.getscalar("select count(*) from Users where upper(U_Name)=upper('"+ val +"') ")
        elif tbl =="dept":
            return self.objdbops.getscalar("select count(*) from Department where upper(Dept_Label)=upper('"+ val +"') ")
        elif tbl =="email": 
            return self.objdbops.getscalar("select count(*) from Users where U_Email='"+val+"' and Dept_AID="+str(dept)+" and UC_AID="+str(ucid))
        elif(tbl=="1"):
            return self.objdbops.getscalar("select count(*) from Model_Function_Master where upper(Mdl_Fncn_Label)=upper('"+ val +"') ")             
        elif(tbl=="2"):
            return self.objdbops.getscalar("select count(*) from Model_Source_Master where upper(Mdl_Src_Label)=upper('"+ val +"')")             
        elif(tbl=="3"):
            return self.objdbops.getscalar("select count(*) from Model_Type_Master where upper(Mdl_Type_Label)=upper('"+ val +"')")
        elif(tbl=="4"):
            return self.objdbops.getscalar("select count(*) from Prd_Addr_Master where upper(Prd_Addr_Label)=upper('"+ val +"')")          
        elif(tbl=="5"):
            return self.objdbops.getscalar("select count(*) from Model_Use_Freq_Master where upper(Mdl_Use_Freq_Label)=upper('"+ val +"')")            
        elif(tbl=="6"):
            return self.objdbops.getscalar("select count(*) from Mdl_Risk_Master where upper(Mdl_Risk_Label)=upper('"+ val +"')")            
        elif(tbl=="7"):
            return self.objdbops.getscalar("select count(*) from Intrinsic_Master  where uper(Intrinsic_Label)=upper('"+ val +"')")           
        elif(tbl=="9"):
            return self.objdbops.getscalar("select count(*) from Materiality_Master where upper(Materiality_Label)=upper('"+ val +"')")            
        elif(tbl=="8"):
            return self.objdbops.getscalar("select count(*) from Reliance_Master where upper(Reliance_Label)=upper('"+ val +"')" )           
        elif(tbl=="10"):
            return self.objdbops.getscalar("select  count(*) from  Mdl_Upstream  where upper(Mdl_Upstream_Label)=upper('"+ val +"')")            
        elif(tbl=="11"):
            return self.objdbops.getscalar("select count(*) from  Mdl_Dwstream where upper(Mdl_Dwstream_Label)=upper('"+ val +"')")             
        elif(tbl=="12"):
            return self.objdbops.getscalar("select count(*) from Mdl_Montr_Freq where upper(Mdl_Montr_Freq_Label)=upper('"+ val +"')")
            

    # def isAutherized(self,userCatId,rsrcId):
    #     # print('user access ',self.objdbops.getscalar("select count(*) from User_Access where UC_AID ='"+str(userCatId)+"' and r_aid='"+rsrcId+"'"))
    #     return str(self.objdbops.getscalar("select count(*) from User_Access where UC_AID ='"+str(userCatId)+"' and r_aid='"+rsrcId+"'"))
        

    def isReadOnly(self,userCatId,rsrcId,deptID):
        return str(self.objdbops.getscalar("Select count(*) cnt from User_Access where UC_AID ='"+str(userCatId)+"' and UA_dept='"+str(deptID)+"' and r_aid='"+rsrcId+"'and UA_Perm='rw'"))
        

    def getUCAccess(self,userCatId):
        tableResult =self.objdbops.getTable("select * from user_access where uc_aid="+userCatId)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)   

    def getUCAccess(self,userCatId):
        tableResult =self.objdbops.getTable("select * from user_access where uc_aid="+userCatId)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)    

    def getUCAccessDeptWise(self,userCatId,deptId):
        tableResult =self.objdbops.getTable("select * from user_access where uc_aid="+userCatId +" and UA_dept='"+str(deptId)+"'")
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)  
    
    def isDeptHead(self,ucId):
        return self.objdbops.getscalar("select count(*) from User_Category where UC_AID='"+str(ucId)+"' and UC_Is_DeptHead =1")    
    
    def getValidationTypes(self):
        tableResult =self.objdbops.getTable("select * from Model_Validation_Type_Master where activestatus=1")
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)  
    
    def getMRMUsers(self):
        tableResult =self.objdbops.getTable("select u_aid, concat(U_FName ,' ', U_LName) uname from users u,department dept where  isnull(Dept_IsMRM,0)=1 and u.Dept_AID=dept.Dept_AID")
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)  
    
    def checkMRMHead(self,uid):
        return self.objdbops.getscalar("select count(*) cnt from users u,department dept ,User_Category uc where  isnull(Dept_IsMRM,0)=1 and u.Dept_AID=dept.Dept_AID and uc.UC_AID=u.UC_AID and UC_Is_DeptHead=1 and u_aid="+str(uid).replace("'","''"))

    def checkMRMMgr(self,uid):
        return self.objdbops.getscalar("select count(*) cnt from users u,department dept ,User_Category uc where  isnull(Dept_IsMRM,0)=1 and u.Dept_AID=dept.Dept_AID and uc.UC_AID=u.UC_AID and  UC_Level=3 and u_aid="+str(uid).replace("'","''"))
    
    def getMRMHead(self):
        return self.objdbops.getscalar("select u_aid cnt from users u,department dept ,User_Category uc where  isnull(Dept_IsMRM,0)=1 and u.Dept_AID=dept.Dept_AID and uc.UC_AID=u.UC_AID and UC_Is_DeptHead=1")

    def getMdlOwner(self,mdlId):#to be updated on  server
        return self.objdbops.getscalar("select addedby from Mdl_OverView where mdl_id='"+mdlId.replace("'","''")+"'")
    

    def addSection(self,section,desc,activests,userId):  
        strQ="insert into ICQ_Sections ("
        strQ += " Section_Label   ,"
        strQ += " Section_Description  ,"
        strQ += " ActiveStatus ,"
        strQ += " AddedBy    ,"
        strQ += " AddDate  )"
        strQ += " values("
        strQ += " '"+section.replace("'","''")+"'   ,"
        strQ += " '"+desc.replace("'","''")+"'  ,"
        strQ += " '"+activests.replace("'","''")+"' ,"
        strQ += " '"+userId.replace("'","''")+"'    ,"
        strQ += " GETDATE()  )	 "
        self.objdbops.insertRow(strQ)   

    def getSections(self):
        tableResult =self.objdbops.getTable("select  Section_Label , Section_AID  from  ICQ_Sections  order by  Section_AID ")
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
        
    def addSub_Section(self,id,section,desc,activests,userId):  
        strQ="insert into ICQ_Sub_Sections ("
        strQ += " Sub_Section_Label   ,"
        strQ += " Sub_Section_Description  ,Section_AID, "
        strQ += " ActiveStatus ,"
        strQ += " AddedBy    ,"
        strQ += " AddDate  )"
        strQ += " values("
        strQ += " '"+section.replace("'","''")+"'   ,"
        strQ += " '"+desc.replace("'","''")+"'  ,"+id.replace("'","''")+", "
        strQ += " '"+activests.replace("'","''")+"' ,"
        strQ += " '"+userId.replace("'","''") +"'    ,"
        strQ += " GETDATE()  )	 "
        self.objdbops.insertRow(strQ)   

    def getSub_Sections(self,id):
        tableResult =self.objdbops.getTable("select  Sub_Section_Label , Sub_Section_AID  from  ICQ_Sub_Sections where Section_AID="+str(id).replace("'","''")+" order by  Sub_Section_AID ")
        print("tableResult ",tableResult)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    
    def addSub_Sub_Section(self,id,section,desc,activests,userId):  
        strQ="insert into ICQ_Sub_Sub_Sections ("
        strQ += " Sub_Sub_Section_Label   ,"
        strQ += " Sub_Sub_Section_Description  ,Sub_Section_AID, "
        strQ += " ActiveStatus ,"
        strQ += " AddedBy    ,"
        strQ += " AddDate  )"
        strQ += " values("
        strQ += " '"+section.replace("'","''")+"'   ,"
        strQ += " '"+desc.replace("'","''")+"'  ,"+id.replace("'","''")+", "
        strQ += " '"+activests.replace("'","''")+"' ,"
        strQ += " '"+userId.replace("'","''") +"'    ,"
        strQ += " GETDATE()  )	 "
        self.objdbops.insertRow(strQ)   

    def getSub_Sub_Sections(self,id):
        tableResult =self.objdbops.getTable("select  Sub_Sub_Section_Label , Sub_Sub_Section_AID  from  ICQ_Sub_Sub_Sections where Sub_Section_AID="+str(id).replace("'","''")+" order by  Sub_Section_AID ")
        print("tableResult ",tableResult)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    
    
    
    def addSub_Sub_Sub_Section(self,id,section,desc,activests,userId):  
        strQ="insert into ICQ_Sub_Sub_Sub_Sections ("
        strQ += " Sub_Sub_Sub_Section_Label   ,"
        strQ += " Sub_Sub_Sub_Section_Description  ,Sub_Sub_Section_AID, "
        strQ += " ActiveStatus ,"
        strQ += " AddedBy    ,"
        strQ += " AddDate  )"
        strQ += " values("
        strQ += " '"+section.replace("'","''")+"'   ,"
        strQ += " '"+desc.replace("'","''")+"'  ,"+id.replace("'","''")+", "
        strQ += " '"+activests.replace("'","''")+"' ,"
        strQ += " '"+userId.replace("'","''") +"'    ,"
        strQ += " GETDATE()  )	 "
        self.objdbops.insertRow(strQ)   

    def getICQQtns(self,sectionid):
        d2 = {}
        strQ="select distinct a.* from("
        strQ += " select '1' lvl,Section_AID,Section_Label,'-' Sub_Section_AID,'-' Sub_Section_Label,"
        strQ += " '-' Sub_Sub_Section_AID,'-' Sub_Sub_Section_Label,'-' Sub_Sub_Sub_Section_AID,'-' Sub_Sub_Sub_Section_Label "     
        strQ += " from ICQ_Sections  " 
        strQ += " )a ,ICQ_Question_Rating_Allocation alloc where alloc.section_aid=a.section_aid  and alloc.allocated_to='"+str(sectionid).replace("'","''")+"'"
        strQ += " order by  a.Section_AID"#,cast(a.Sub_Section_AID as int),cast(a.Sub_Sub_Section_AID as int),cast(a.Sub_Sub_Sub_Section_AID as int)"
        tableResult =self.objdbops.getTable(strQ)
        print("qtns query",strQ)
        arrayidx=0 
        if tableResult.empty == False:
            for ind in tableResult.index: 
                strQtn=""
                strQtn+=" select Rating_Yes_NO ,Doc_Yes_No,Inherent_Risk_Rating,Control_Effectiveness_Ratings,Residual_Ratings,Control_Description,override_residual_ratings,override_comments,isnull(comments,'')comments,case when  len(qtnmst.Section_AID )<>  0 and  (qtnmst.Sub_Section_AID) is null then 1 "
                strQtn+=" when  len(qtnmst.Sub_Section_AID)<>  0 and  (qtnmst.Sub_Sub_Section_AID) is null then 2"
                strQtn+=" when len(qtnmst.Sub_Sub_Section_AID)<>0 and  (qtnmst.Sub_Sub_Sub_Section_AID)  is null then 3 "
                strQtn+=" when len(qtnmst.Sub_Sub_Sub_Section_AID)<>  0 then 4  else 0 end lvl,  sec.Section_AID,isnull(s_sec.Sub_Section_AID,'0') Sub_Section_AID,"
                strQtn+=" isnull(ss_sec.Sub_Sub_Section_AID,'0') Sub_Sub_Section_AID,qtnmst.Question_AID ,"
                strQtn+=" qtnmst.Question_Label ,isnull(sec.Section_Label,'') Section_Label, isnull(s_sec.Sub_Section_Label,'') Sub_Section_Label,isnull(ss_sec.Sub_Sub_Section_Label,'') Sub_Sub_Section_Label    from "
                strQtn+=" icq_question_master qtnmst left join ICQ_Sections sec on "
                strQtn+=" qtnmst.section_aid=sec.section_aid left join"
                strQtn+=" ICQ_Sub_Sections s_sec  on qtnmst.sub_section_aid=s_sec.sub_section_aid left join"
                strQtn+=" ICQ_Sub_Sub_Sections ss_sec on qtnmst.sub_sub_section_aid=ss_sec.sub_sub_section_aid "
                strQtn+=" left join ICQ_Question_Rating_Data   on qtnmst.Question_aid=ICQ_Question_Rating_Data.question_aid	"
                strQtn+=" where sec.section_aid="+str(tableResult['Section_AID'][ind]).replace("'","''")+" "
                strQtn+=" order by   qtnmst.Question_AID,qtnmst.section_aid"
                strQtn+=" ,cast(qtnmst.Sub_Section_AID as int),cast(qtnmst.Sub_Sub_Section_AID as int) " 
                qtnResult =self.objdbops.getTable(strQtn) 
                           
               
                qtnNo=0 
                iLvlCurr=0
                iSecCurr=0
                iSubSecCurr=0
                iSubSubSecCurr=0
                iSubSubSecPrev=0
                iCnt_L1=0
                strQues=""
                strSectionText=""
                strSubSectionText=""
                strSubSubSectionText=""
                iQuesID=0
                iCnt_L1 = 0                #//Q No
                iCnt_Section = 0              # //Q No
                iCnt_SubSection = 0              #  //Q No
                iCnt_SubSubSection = 0              # //Q No 
                strQNo = ""  #//Q No
                blnAlreadyIncreased = False
                for i in qtnResult.index: 
                    blnAlreadyIncreased = False 
                    strLevelText = ""
                    iLvlCurr = int(qtnResult['lvl'][i])
                    iSecCurr = int(qtnResult['Section_AID'][i])
                    iSubSecCurr =int(qtnResult['Sub_Section_AID'][i])
                    iSubSubSecCurr =int(qtnResult['Sub_Sub_Section_AID'][i])
                   
                    
                    iQuesID=int(qtnResult['Question_AID'][i])

                    strQues = qtnResult["Question_Label"][i]
                    strSectionText = qtnResult["Section_Label"][i]
                    strSubSectionText = qtnResult["Sub_Section_Label"][i]
                    strSubSectionText = strSubSectionText.replace("-", "")
                    strSubSubSectionText =qtnResult["Sub_Sub_Section_Label"][i]

                    for j in range(iLvlCurr):
                        strLevelText += "->"

                    if (i == 0): 
                        iCnt_L1 = 0
                        iCnt_Section = 0
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0

                        iLvlPrev = iLvlCurr
                        iSecPrev = iSecCurr
                        iSubSecPrev = iSubSecCurr
                        iSubSubSecCurr = iSubSubSecPrev

                    if (i > 0 and iSecCurr != iSecPrev):
                        iSecPrev = iSecCurr
                        iCnt_L1 = 0
                        iCnt_Section = 0
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0
                    elif (i > 0):
                        strSectionText = ""

                    if (i > 0 and iSubSecCurr != iSubSecPrev):
                        iSubSecPrev = iSubSecCurr
                        if (strSectionText == ""):
                            blnAlreadyIncreased = True
                            iCnt_L1+=1
                        iCnt_Section = 0
                        iCnt_SubSection = 0    
                        iCnt_SubSubSection = 0 
                    elif (i > 0):
                        strSubSectionText = ""

                    if (i > 0 and iSubSubSecCurr>0 and iSubSubSecCurr != iSubSubSecPrev):
                        iSubSubSecPrev = iSubSubSecCurr
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0
                        iCnt_Section+=1
                    elif(i > 0 and iSubSubSecCurr > 0):
                        strSubSubSectionText = ""

                    #   //Increase Question Nos Starts
                    iCnt_L1 =1 if strSectionText != "" and strSubSectionText != "" and iCnt_L1 == 0  else iCnt_L1
                    if (iLvlCurr == 1): 
                        if (blnAlreadyIncreased == False):
                            iCnt_L1 +=1        
                    elif (iLvlCurr == 2):
                        iCnt_Section+=1
                    elif (iLvlCurr == 3): 
                        iCnt_SubSection+=1 
                    elif (iLvlCurr == 4):
                        iCnt_SubSubSection+=1
                    # //Increase Question Nos Ends 

                     
                   
                    if (iLvlCurr == 1):                  
                        strQNo = str(iCnt_L1 )
                    elif (iLvlCurr == 2): 
                        strQNo = str(iCnt_L1) + "." + str(iCnt_Section)
                    elif (iLvlCurr == 3): 
                        strQNo = str(iCnt_L1) + "." + str(iCnt_Section) + "." + str(iCnt_SubSection) 
                    elif (iLvlCurr == 4): 
                        strQNo = str(iCnt_L1) + "." +str( iCnt_Section) + "." + str(iCnt_SubSection) + "." + str(iCnt_SubSubSection)
                     
                    if i == 0:  
                        if(str(qtnResult['lvl'][i]) !="1"): 
                            d = {'Section_AID':str(qtnResult['Section_AID'][i]), 
                            'Section_Label':str(qtnResult['Section_Label'][i]), 
                            'Sub_Section_AID':iSubSecPrev, 
                            'Sub_Section_Label':"", 
                            'Sub_Sub_Section_AID':'', 
                            'Sub_Sub_Section_Label':'', 
                            'qtnNo':"",
                            'qtnsArr':'',
                            'lvl': str('->') } 
                            d2[arrayidx] = d
                            arrayidx+=1  

                    if(strSectionText!=""):
                        # dtFinalValues.Rows.Add(strSectionText, 
                        #                        strSubSectionText, 
                        #                        strSubSubSectionText, "", "", 
                        #                        iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0],
                                    'qtnsArr':"",
                                    'qtn_aid':"",
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i],
                                    'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                    'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                    'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                    'Control_Description':qtnResult['Control_Description'][i],
                                    'override_residual_ratings':qtnResult['override_residual_ratings'][i],
                                    'override_comments':qtnResult['override_comments'][i]
                                    
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    elif (strSubSectionText != ""):
                        # dtFinalValues.Rows.Add(strSectionText, 
                        #                        strSubSectionText, 
                        #                        strSubSubSectionText, "", 
                        #                        strQNo.Split('.')[0], iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0],
                                    'qtnsArr':"",
                                    'qtn_aid':str(iQuesID),
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i],
                                    'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                    'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                    'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                    'Control_Description':qtnResult['Control_Description'][i],
                                    'override_residual_ratings':qtnResult['override_residual_ratings'][i],
                                    'override_comments':qtnResult['override_comments'][i]
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    elif (strSubSubSectionText != ""):
                        # dtFinalValues.Rows.Add(strSectionText, strSubSectionText, 
                        #                        strSubSubSectionText, "", 
                        #                        strQNo.Split('.')[0] + "." + 
                        #                        strQNo.Split('.')[1], iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0]+ "." +str(strQNo).split('.')[1] ,
                                    'qtnsArr':"",
                                    'qtn_aid':str(iQuesID),
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i],
                                    'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                    'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                    'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                    'Control_Description':qtnResult['Control_Description'][i],
                                    'override_residual_ratings':qtnResult['override_residual_ratings'][i],
                                    'override_comments':qtnResult['override_comments'][i]
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  

                    # dtFinalValues.Rows.Add("", "", "", strLevelText + "    " + strQues, 
                    #                        strQNo, iLvlCurr.ToString());
                    d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':"", 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':"", 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':"", 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo)  ,
                                    'qtnsArr':strQues,
                                    'qtn_aid':str(iQuesID),
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i],
                                    'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                    'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                    'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                    'Control_Description':qtnResult['Control_Description'][i],
                                    'override_residual_ratings':qtnResult['override_residual_ratings'][i],
                                    'override_comments':qtnResult['override_comments'][i]
                                    } 
                    d2[arrayidx] = d
                    arrayidx+=1  
                del qtnResult
        
            del tableResult   
        print("d2 " ,d2)
        return d2 # json.dumps(d2)   

    def getFLQtns(self,sectionid):
        d2 = {}
        strQ="select distinct a.* from("
        strQ += " select '1' lvl,Section_AID,Section_Label,'-' Sub_Section_AID,'-' Sub_Section_Label,"
        strQ += " '-' Sub_Sub_Section_AID,'-'     Sub_Sub_Section_Label,'-' Sub_Sub_Sub_Section_AID,'-' Sub_Sub_Sub_Section_Label "     
        strQ += " from FL_Sections" 
        strQ += " )a ,FL_Allocation alloc where alloc.section_aid=a.section_aid  and alloc.allocated_to='"+str(sectionid).replace("'","''")+"'"
        strQ += " order by  a.Section_AID"#,cast(a.Sub_Section_AID as int),cast(a.Sub_Sub_Section_AID as int),cast(a.Sub_Sub_Sub_Section_AID as int)"
        print("Strq------",strQ) 
        tableResult =self.objdbops.getTable(strQ)
        print("tableResult",tableResult) 
        arrayidx=0 
        if tableResult.empty == False:
            for ind in tableResult.index: 
                strQtn=""
                strQtn+=" select Rating_Yes_NO ,Doc_Yes_No, Inherent_Risk_Rating,Control_Effectiveness_Ratings,Residual_Ratings,Control_Description,override_residual_ratings,override_comments,isnull(comments,'')comments,case when  len(qtnmst.Section_AID )<>  0 and  (qtnmst.Sub_Section_AID) is null then 1 "
                strQtn+=" when  len(qtnmst.Sub_Section_AID)<>  0 and  (qtnmst.Sub_Sub_Section_AID) is null then 2"
                strQtn+=" when len(qtnmst.Sub_Sub_Section_AID)<>0 and  (qtnmst.Sub_Sub_Sub_Section_AID)  is null then 3 "
                strQtn+=" when len(qtnmst.Sub_Sub_Sub_Section_AID)<>  0 then 4  else 0 end lvl,  sec.Section_AID,isnull(s_sec.Sub_Section_AID,'0') Sub_Section_AID,"
                strQtn+=" isnull(ss_sec.Sub_Sub_Section_AID,'0') Sub_Sub_Section_AID,qtnmst.Question_AID ,"
                strQtn+=" qtnmst.Question_Label ,isnull(sec.Section_Label,'') Section_Label, isnull(s_sec.Sub_Section_Label,'') Sub_Section_Label,isnull(ss_sec.Sub_Sub_Section_Label,'') Sub_Sub_Section_Label    from "
                strQtn+=" FL_question_master qtnmst left join FL_Sections sec on "
                strQtn+=" qtnmst.section_aid=sec.section_aid left join"
                strQtn+=" FL_Sub_Sections s_sec  on qtnmst.sub_section_aid=s_sec.sub_section_aid left join"
                strQtn+=" FL_Sub_Sub_Sections ss_sec on qtnmst.sub_sub_section_aid=ss_sec.sub_sub_section_aid "
                strQtn+=" left join FL_Question_Rating_Data   on qtnmst.Question_aid=FL_Question_Rating_Data.question_aid	"
                strQtn+=" where sec.section_aid="+str(tableResult['Section_AID'][ind]).replace("'","''")+" "
                strQtn+=" order by   qtnmst.Question_AID,qtnmst.section_aid"
                strQtn+=" ,cast(qtnmst.Sub_Section_AID as int),cast(qtnmst.Sub_Sub_Section_AID as int) " 
                qtnResult =self.objdbops.getTable(strQtn) 
                           
                print("qtnResult---------------",qtnResult['override_residual_ratings'])
                qtnNo=0 
                iLvlCurr=0
                iSecCurr=0
                iSubSecCurr=0
                iSubSubSecCurr=0
                iSubSubSecPrev=0
                iCnt_L1=0
                strQues=""
                strSectionText=""
                strSubSectionText=""
                strSubSubSectionText=""
                iQuesID=0
                iCnt_L1 = 0                #//Q No
                iCnt_Section = 0              # //Q No
                iCnt_SubSection = 0              #  //Q No
                iCnt_SubSubSection = 0              # //Q No 
                strQNo = ""  #//Q No
                blnAlreadyIncreased = False
                for i in qtnResult.index: 
                    blnAlreadyIncreased = False 
                    strLevelText = ""
                    iLvlCurr = int(qtnResult['lvl'][i])
                    iSecCurr = int(qtnResult['Section_AID'][i])
                    iSubSecCurr =int(qtnResult['Sub_Section_AID'][i])
                    iSubSubSecCurr =int(qtnResult['Sub_Sub_Section_AID'][i])
                   
                    
                    iQuesID=int(qtnResult['Question_AID'][i])

                    strQues = qtnResult["Question_Label"][i]
                    strSectionText = qtnResult["Section_Label"][i]
                    strSubSectionText = qtnResult["Sub_Section_Label"][i]
                    strSubSectionText = strSubSectionText.replace("-", "")
                    strSubSubSectionText =qtnResult["Sub_Sub_Section_Label"][i]

                    for j in range(iLvlCurr):
                        strLevelText += "->"

                    if (i == 0): 
                        iCnt_L1 = 0
                        iCnt_Section = 0
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0

                        iLvlPrev = iLvlCurr
                        iSecPrev = iSecCurr
                        iSubSecPrev = iSubSecCurr
                        iSubSubSecCurr = iSubSubSecPrev

                    if (i > 0 and iSecCurr != iSecPrev):
                        iSecPrev = iSecCurr
                        iCnt_L1 = 0
                        iCnt_Section = 0
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0
                    elif (i > 0):
                        strSectionText = ""

                    if (i > 0 and iSubSecCurr != iSubSecPrev):
                        iSubSecPrev = iSubSecCurr
                        if (strSectionText == ""):
                            blnAlreadyIncreased = True
                            iCnt_L1+=1
                        iCnt_Section = 0
                        iCnt_SubSection = 0    
                        iCnt_SubSubSection = 0 
                    elif (i > 0):
                        strSubSectionText = ""

                    if (i > 0 and iSubSubSecCurr>0 and iSubSubSecCurr != iSubSubSecPrev):
                        iSubSubSecPrev = iSubSubSecCurr
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0
                        iCnt_Section+=1
                    elif(i > 0 and iSubSubSecCurr > 0):
                        strSubSubSectionText = ""

                    #   //Increase Question Nos Starts
                    iCnt_L1 =1 if strSectionText != "" and strSubSectionText != "" and iCnt_L1 == 0  else iCnt_L1
                    if (iLvlCurr == 1): 
                        if (blnAlreadyIncreased == False):
                            iCnt_L1 +=1        
                    elif (iLvlCurr == 2):
                        iCnt_Section+=1
                    elif (iLvlCurr == 3): 
                        iCnt_SubSection+=1 
                    elif (iLvlCurr == 4):
                        iCnt_SubSubSection+=1
                    # //Increase Question Nos Ends 

                     
                   
                    if (iLvlCurr == 1):                  
                        strQNo = str(iCnt_L1 )
                    elif (iLvlCurr == 2): 
                        strQNo = str(iCnt_L1) + "." + str(iCnt_Section)
                    elif (iLvlCurr == 3): 
                        strQNo = str(iCnt_L1) + "." + str(iCnt_Section) + "." + str(iCnt_SubSection) 
                    elif (iLvlCurr == 4): 
                        strQNo = str(iCnt_L1) + "." +str( iCnt_Section) + "." + str(iCnt_SubSection) + "." + str(iCnt_SubSubSection)
                     
                    if i == 0:  
                        if(str(qtnResult['lvl'][i]) !="1"): 
                            d = {'Section_AID':str(qtnResult['Section_AID'][i]), 
                            'Section_Label':str(qtnResult['Section_Label'][i]), 
                            'Sub_Section_AID':iSubSecPrev, 
                            'Sub_Section_Label':"", 
                            'Sub_Sub_Section_AID':'', 
                            'Sub_Sub_Section_Label':'', 
                            'qtnNo':"",
                            'qtnsArr':'',
                            'lvl': str('->') } 
                            d2[arrayidx] = d
                            arrayidx+=1  

                    if(strSectionText!=""):
                        # dtFinalValues.Rows.Add(strSectionText, 
                        #                        strSubSectionText, 
                        #                        strSubSubSectionText, "", "", 
                        #                        iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0],
                                    'qtnsArr':"",
                                    'qtn_aid':"",
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],
                                    'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],
                                    'comments':qtnResult['comments'][i],
                                    'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                    'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                    'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                    'Control_Description':qtnResult['Control_Description'][i],
                                    'override_residual_ratings':qtnResult['override_residual_ratings'][i],
                                    'override_comments':qtnResult['override_comments'][i]
                                    
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    elif (strSubSectionText != ""):
                        # dtFinalValues.Rows.Add(strSectionText, 
                        #                        strSubSectionText, 
                        #                        strSubSubSectionText, "", 
                        #                        strQNo.Split('.')[0], iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0],
                                    'qtnsArr':"",
                                    'qtn_aid':str(iQuesID),
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i],
                                    'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                    'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                    'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                    'Control_Description':qtnResult['Control_Description'][i],
                                    'override_residual_ratings':qtnResult['override_residual_ratings'][i],
                                    'override_comments':qtnResult['override_comments'][i]
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    elif (strSubSubSectionText != ""):
                        # dtFinalValues.Rows.Add(strSectionText, strSubSectionText, 
                        #                        strSubSubSectionText, "", 
                        #                        strQNo.Split('.')[0] + "." + 
                        #                        strQNo.Split('.')[1], iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0]+ "." +str(strQNo).split('.')[1] ,
                                    'qtnsArr':"",
                                    'qtn_aid':str(iQuesID),
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i],
                                    'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                    'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                    'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                    'Control_Description':qtnResult['Control_Description'][i],
                                    'override_residual_ratings':qtnResult['override_residual_ratings'][i],
                                    'override_comments':qtnResult['override_comments'][i]
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  

                    # dtFinalValues.Rows.Add("", "", "", strLevelText + "    " + strQues, 
                    #                        strQNo, iLvlCurr.ToString());
                    d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':"", 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':"", 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':"", 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo)  ,
                                    'qtnsArr':strQues,
                                    'qtn_aid':str(iQuesID),
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i],
                                    'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                    'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                    'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                    'Control_Description':qtnResult['Control_Description'][i],
                                    'override_residual_ratings':qtnResult['override_residual_ratings'][i],
                                    'override_comments':qtnResult['override_comments'][i]
                                    } 
                    d2[arrayidx] = d
                    arrayidx+=1  
                del qtnResult
        
            del tableResult   
        print("d2 " ,d2)
        return d2 # json.dumps(d2)  
    
    def getICQModels(self,id):
        tableResult =self.objdbops.getTable("select distinct Model_Id from ICQ_Question_Rating_Allocation where Allocated_to ="+str(id).replace("'","''")+" order by  1 ")
       
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)

    def getFLModels(self,id):
        tableResult =self.objdbops.getTable("select distinct Model_Id from FL_Allocation where Allocated_to ="+str(id).replace("'","''")+" order by  1 ")
       
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    
    def getICQQtnSection(self,id):
        tableResult =self.objdbops.getTable("select distinct section_label,alloc.section_aid from ICQ_Sections icq,ICQ_Question_Rating_Allocation alloc where alloc.section_aid=icq.section_aid and Allocated_to ='"+str(id).replace("'","''")+"' order by  1 ")
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)

    def getFLQtnSection(self,id):
        tableResult =self.objdbops.getTable("select distinct section_label,alloc.section_aid from FL_Sections fl,FL_Allocation alloc where alloc.section_aid=fl.section_aid and Allocated_to ='"+str(id).replace("'","''")+"' order by  1 ")
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    
    def getICQQtnSectionFinal(self):
        tableResult =self.objdbops.getTable("select distinct section_label,alloc.section_aid from ICQ_Sections icq,ICQ_Question_Rating_Allocation alloc where alloc.section_aid=icq.section_aid order by  1 ")
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    
    # def getICQQtnSectionFinal(self):
    #     tableResult =self.objdbops.getTable("select distinct section_label,alloc.section_aid from ICQ_Sections icq,ICQ_Question_Rating_Allocation alloc where alloc.section_aid=icq.section_aid order by  1 ")
    #     tableResult= tableResult.to_json(orient='index')
    #     return json.loads(tableResult)
    
    def getFLtnSectionFinal(self):
        tableResult =self.objdbops.getTable("select distinct section_label,alloc.section_aid from FL_Sections fl,FL_Allocation alloc where alloc.section_aid=fl.section_aid order by  1 ")
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    

    def getICQQtnsFinal(self):
        d2 = {}
        strQ="select distinct a.* from("
        strQ += " select '1' lvl,Section_AID,Section_Label,'-' Sub_Section_AID,'-' Sub_Section_Label,"
        strQ += " '-' Sub_Sub_Section_AID,'-' Sub_Sub_Section_Label,'-' Sub_Sub_Sub_Section_AID,'-' Sub_Sub_Sub_Section_Label "     
        strQ += " from ICQ_Sections   )a  ,ICQ_Question_Rating_Allocation alloc where alloc.section_aid=a.section_aid "# and a.section_aid='"+str(sectionid)+"'"
        strQ += " order by  a.Section_AID"
        print("query1--",strQ)
        tableResult =self.objdbops.getTable(strQ) 
        arrayidx=0 
        if tableResult.empty == False:
            for ind in tableResult.index: 
                strQtn=""     
                strQtn+=" select Rating_Yes_NO ,Doc_Yes_No,Inherent_Risk_Rating,Control_Effectiveness_Ratings,Residual_Ratings,Control_Description,override_residual_ratings,override_comments,isnull(comments,'')comments,case when  len(qtnmst.Section_AID )<>  0 and  (qtnmst.Sub_Section_AID) is null then 1 "
                strQtn+=" when  len(qtnmst.Sub_Section_AID)<>  0 and  (qtnmst.Sub_Sub_Section_AID) is null then 2"
                strQtn+=" when len(qtnmst.Sub_Sub_Section_AID)<>0 and  (qtnmst.Sub_Sub_Sub_Section_AID)  is null then 3 "
                strQtn+=" when len(qtnmst.Sub_Sub_Sub_Section_AID)<>  0 then 4  else 0 end lvl,  sec.Section_AID,isnull(s_sec.Sub_Section_AID,'0') Sub_Section_AID,"
                strQtn+=" isnull(ss_sec.Sub_Sub_Section_AID,'0') Sub_Sub_Section_AID,qtnmst.Question_AID ,"
                strQtn+=" qtnmst.Question_Label ,isnull(sec.Section_Label,'') Section_Label, isnull(s_sec.Sub_Section_Label,'') Sub_Section_Label,isnull(ss_sec.Sub_Sub_Section_Label,'') Sub_Sub_Section_Label    from "
                strQtn+=" icq_question_master qtnmst left join ICQ_Sections sec on "
                strQtn+=" qtnmst.section_aid=sec.section_aid left join"
                strQtn+=" ICQ_Sub_Sections s_sec  on qtnmst.sub_section_aid=s_sec.sub_section_aid left join"
                strQtn+=" ICQ_Sub_Sub_Sections ss_sec on qtnmst.sub_sub_section_aid=ss_sec.sub_sub_section_aid "
                strQtn+=" left join ICQ_Question_Rating_Data_Final   on qtnmst.Question_aid=ICQ_Question_Rating_Data_Final.question_aid	"
                strQtn+=" where sec.section_aid="+str(tableResult['Section_AID'][ind])+" "
                strQtn+=" order by   qtnmst.Question_AID,qtnmst.section_aid"
                strQtn+=" ,cast(qtnmst.Sub_Section_AID as int),cast(qtnmst.Sub_Sub_Section_AID as int) " 
                qtnResult =self.objdbops.getTable(strQtn)                 
                print("query------",strQtn)
                
                iLvlCurr=0
                iSecCurr=0
                iSubSecCurr=0
                iSubSubSecCurr=0
                iSubSubSecPrev=0
                iCnt_L1=0
                strQues=""
                strSectionText=""
                strSubSectionText=""
                strSubSubSectionText=""
                iQuesID=0
                iCnt_L1 = 0                #//Q No
                iCnt_Section = 0              # //Q No
                iCnt_SubSection = 0              #  //Q No
                iCnt_SubSubSection = 0              # //Q No 
                strQNo = ""  #//Q No
                blnAlreadyIncreased = False
                for i in qtnResult.index: 
                    blnAlreadyIncreased = False 
                    strLevelText = ""
                    iLvlCurr = int(qtnResult['lvl'][i])
                    iSecCurr = int(qtnResult['Section_AID'][i])
                    iSubSecCurr =int(qtnResult['Sub_Section_AID'][i])
                    iSubSubSecCurr =int(qtnResult['Sub_Sub_Section_AID'][i])
                   
                    
                    iQuesID=int(qtnResult['Question_AID'][i])

                    strQues = qtnResult["Question_Label"][i]
                    strSectionText = qtnResult["Section_Label"][i]
                    strSubSectionText = qtnResult["Sub_Section_Label"][i]
                    strSubSectionText = strSubSectionText.replace("-", "")
                    strSubSubSectionText =qtnResult["Sub_Sub_Section_Label"][i]

                    for j in range(iLvlCurr):
                        strLevelText += "->"

                    if (i == 0): 
                        iCnt_L1 = 0
                        iCnt_Section = 0
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0

                        iLvlPrev = iLvlCurr
                        iSecPrev = iSecCurr
                        iSubSecPrev = iSubSecCurr
                        iSubSubSecCurr = iSubSubSecPrev

                    if (i > 0 and iSecCurr != iSecPrev):
                        iSecPrev = iSecCurr
                        iCnt_L1 = 0
                        iCnt_Section = 0
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0
                    elif (i > 0):
                        strSectionText = ""

                    if (i > 0 and iSubSecCurr != iSubSecPrev):
                        iSubSecPrev = iSubSecCurr
                        if (strSectionText == ""):
                            blnAlreadyIncreased = True
                            iCnt_L1+=1
                        iCnt_Section = 0
                        iCnt_SubSection = 0    
                        iCnt_SubSubSection = 0 
                    elif (i > 0):
                        strSubSectionText = ""

                    if (i > 0 and iSubSubSecCurr>0 and iSubSubSecCurr != iSubSubSecPrev):
                        iSubSubSecPrev = iSubSubSecCurr
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0
                        iCnt_Section+=1
                    elif(i > 0 and iSubSubSecCurr > 0):
                        strSubSubSectionText = ""

                    #   //Increase Question Nos Starts
                    iCnt_L1 =1 if strSectionText != "" and strSubSectionText != "" and iCnt_L1 == 0  else iCnt_L1
                    if (iLvlCurr == 1): 
                        if (blnAlreadyIncreased == False):
                            iCnt_L1 +=1        
                    elif (iLvlCurr == 2):
                        iCnt_Section+=1
                    elif (iLvlCurr == 3): 
                        iCnt_SubSection+=1 
                    elif (iLvlCurr == 4):
                        iCnt_SubSubSection+=1
                    # //Increase Question Nos Ends 

                     
                   
                    if (iLvlCurr == 1):                  
                        strQNo = str(iCnt_L1 )
                    elif (iLvlCurr == 2): 
                        strQNo = str(iCnt_L1) + "." + str(iCnt_Section)
                    elif (iLvlCurr == 3): 
                        strQNo = str(iCnt_L1) + "." + str(iCnt_Section) + "." + str(iCnt_SubSection) 
                    elif (iLvlCurr == 4): 
                        strQNo = str(iCnt_L1) + "." +str( iCnt_Section) + "." + str(iCnt_SubSection) + "." + str(iCnt_SubSubSection)
                     
                    if i == 0:  
                        if(str(qtnResult['lvl'][i]) !="1"): 
                            d = {'Section_AID':str(qtnResult['Section_AID'][i]), 
                            'Section_Label':str(qtnResult['Section_Label'][i]), 
                            'Sub_Section_AID':iSubSecPrev, 
                            'Sub_Section_Label':"", 
                            'Sub_Sub_Section_AID':'', 
                            'Sub_Sub_Section_Label':'', 
                            'qtnNo':"",
                            'qtnsArr':'',
                            'lvl': str('->') } 
                            d2[arrayidx] = d
                            arrayidx+=1  

                    if(strSectionText!=""):
                        # dtFinalValues.Rows.Add(strSectionText, 
                        #                        strSubSectionText, 
                        #                        strSubSubSectionText, "", "", 
                        #                        iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0],
                                    'qtnsArr':"",
                                    'qtn_aid':"",
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i],
                                    'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                    'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                    'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                    'Control_Description':qtnResult['Control_Description'][i]
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    elif (strSubSectionText != ""):
                        # dtFinalValues.Rows.Add(strSectionText, 
                        #                        strSubSectionText, 
                        #                        strSubSubSectionText, "", 
                        #                        strQNo.Split('.')[0], iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0],
                                    'qtnsArr':"",
                                    'qtn_aid':str(iQuesID),
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i],
                                    'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                    'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                    'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                    'Control_Description':qtnResult['Control_Description'][i]
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    elif (strSubSubSectionText != ""):
                        # dtFinalValues.Rows.Add(strSectionText, strSubSectionText, 
                        #                        strSubSubSectionText, "", 
                        #                        strQNo.Split('.')[0] + "." + 
                        #                        strQNo.Split('.')[1], iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0]+ "." +str(strQNo).split('.')[1] ,
                                    'qtnsArr':"",
                                    'qtn_aid':str(iQuesID),
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i]
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  

                    # dtFinalValues.Rows.Add("", "", "", strLevelText + "    " + strQues, 
                    #                        strQNo, iLvlCurr.ToString());
                    d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':"", 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':"", 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':"", 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo)  ,
                                    'qtnsArr':strQues,
                                    'qtn_aid':str(iQuesID),
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i],
                                    'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                    'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                    'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                    'Control_Description':qtnResult['Control_Description'][i]
                                    } 
                    d2[arrayidx] = d
                    arrayidx+=1  
                del qtnResult
        
            del tableResult 
        return d2 # json.dumps(d2)    
    
    def getFLQtnsFinal(self):
        d2 = {}
        strQ="select distinct a.* from("
        strQ += " select '1' lvl,Section_AID,Section_Label,'-' Sub_Section_AID,'-' Sub_Section_Label,"
        strQ += " '-' Sub_Sub_Section_AID,'-' Sub_Sub_Section_Label,'-' Sub_Sub_Sub_Section_AID,'-' Sub_Sub_Sub_Section_Label "     
        strQ += " from FL_Sections   )a  ,FL_Allocation alloc where alloc.section_aid=a.section_aid "# and a.section_aid='"+str(sectionid)+"'"
        strQ += " order by  a.Section_AID"
        tableResult =self.objdbops.getTable(strQ) 
        arrayidx=0 
        if tableResult.empty == False:
            for ind in tableResult.index: 
                strQtn=""
                strQtn+=" select Rating_Yes_NO ,Doc_Yes_No,Inherent_Risk_Rating,Control_Effectiveness_Ratings,Residual_Ratings,Control_Description,override_residual_ratings,override_comments,isnull(comments,'')comments,case when  len(qtnmst.Section_AID )<>  0 and  (qtnmst.Sub_Section_AID) is null then 1 "
                strQtn+=" when  len(qtnmst.Sub_Section_AID)<>  0 and  (qtnmst.Sub_Sub_Section_AID) is null then 2"
                strQtn+=" when len(qtnmst.Sub_Sub_Section_AID)<>0 and  (qtnmst.Sub_Sub_Sub_Section_AID)  is null then 3 "
                strQtn+=" when len(qtnmst.Sub_Sub_Sub_Section_AID)<>  0 then 4  else 0 end lvl,  sec.Section_AID,isnull(s_sec.Sub_Section_AID,'0') Sub_Section_AID,"
                strQtn+=" isnull(ss_sec.Sub_Sub_Section_AID,'0') Sub_Sub_Section_AID,qtnmst.Question_AID ,"
                strQtn+=" qtnmst.Question_Label ,isnull(sec.Section_Label,'') Section_Label, isnull(s_sec.Sub_Section_Label,'') Sub_Section_Label,isnull(ss_sec.Sub_Sub_Section_Label,'') Sub_Sub_Section_Label    from "
                strQtn+=" FL_question_master qtnmst left join FL_Sections sec on "
                strQtn+=" qtnmst.section_aid=sec.section_aid left join"
                strQtn+=" FL_Sub_Sections s_sec  on qtnmst.sub_section_aid=s_sec.sub_section_aid left join"
                strQtn+=" FL_Sub_Sub_Sections ss_sec on qtnmst.sub_sub_section_aid=ss_sec.sub_sub_section_aid "
                strQtn+=" left join FL_Question_Rating_Data_Final on qtnmst.Question_aid=FL_Question_Rating_Data_Final.Question_AID	"
                strQtn+=" where sec.section_aid="+str(tableResult['Section_AID'][ind])+" "
                strQtn+=" order by qtnmst.Question_AID,qtnmst.section_aid"
                strQtn+=" ,cast(qtnmst.Sub_Section_AID as int),cast(qtnmst.Sub_Sub_Section_AID as int) " 
                qtnResult =self.objdbops.getTable(strQtn)                 
                print(strQtn)
                print("qtnResult",qtnResult)
                iLvlCurr=0
                iSecCurr=0
                iSubSecCurr=0
                iSubSubSecCurr=0
                iSubSubSecPrev=0
                iCnt_L1=0
                strQues=""
                strSectionText=""
                strSubSectionText=""
                strSubSubSectionText=""
                iQuesID=0
                iCnt_L1 = 0                #//Q No
                iCnt_Section = 0              # //Q No
                iCnt_SubSection = 0              #  //Q No
                iCnt_SubSubSection = 0              # //Q No 
                strQNo = ""  #//Q No
                blnAlreadyIncreased = False
                for i in qtnResult.index: 
                    blnAlreadyIncreased = False 
                    strLevelText = ""
                    iLvlCurr = int(qtnResult['lvl'][i])
                    iSecCurr = int(qtnResult['Section_AID'][i])
                    iSubSecCurr =int(qtnResult['Sub_Section_AID'][i])
                    iSubSubSecCurr =int(qtnResult['Sub_Sub_Section_AID'][i])
                   
                    
                    iQuesID=int(qtnResult['Question_AID'][i])

                    strQues = qtnResult["Question_Label"][i]
                    strSectionText = qtnResult["Section_Label"][i]
                    strSubSectionText = qtnResult["Sub_Section_Label"][i]
                    strSubSectionText = strSubSectionText.replace("-", "")
                    strSubSubSectionText =qtnResult["Sub_Sub_Section_Label"][i]

                    for j in range(iLvlCurr):
                        strLevelText += "->"

                    if (i == 0): 
                        iCnt_L1 = 0
                        iCnt_Section = 0
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0

                        iLvlPrev = iLvlCurr
                        iSecPrev = iSecCurr
                        iSubSecPrev = iSubSecCurr
                        iSubSubSecCurr = iSubSubSecPrev

                    if (i > 0 and iSecCurr != iSecPrev):
                        iSecPrev = iSecCurr
                        iCnt_L1 = 0
                        iCnt_Section = 0
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0
                    elif (i > 0):
                        strSectionText = ""

                    if (i > 0 and iSubSecCurr != iSubSecPrev):
                        iSubSecPrev = iSubSecCurr
                        if (strSectionText == ""):
                            blnAlreadyIncreased = True
                            iCnt_L1+=1
                        iCnt_Section = 0
                        iCnt_SubSection = 0    
                        iCnt_SubSubSection = 0 
                    elif (i > 0):
                        strSubSectionText = ""

                    if (i > 0 and iSubSubSecCurr>0 and iSubSubSecCurr != iSubSubSecPrev):
                        iSubSubSecPrev = iSubSubSecCurr
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0
                        iCnt_Section+=1
                    elif(i > 0 and iSubSubSecCurr > 0):
                        strSubSubSectionText = ""

                    #   //Increase Question Nos Starts
                    iCnt_L1 =1 if strSectionText != "" and strSubSectionText != "" and iCnt_L1 == 0  else iCnt_L1
                    if (iLvlCurr == 1): 
                        if (blnAlreadyIncreased == False):
                            iCnt_L1 +=1        
                    elif (iLvlCurr == 2):
                        iCnt_Section+=1
                    elif (iLvlCurr == 3): 
                        iCnt_SubSection+=1 
                    elif (iLvlCurr == 4):
                        iCnt_SubSubSection+=1
                    # //Increase Question Nos Ends 

                     
                   
                    if (iLvlCurr == 1):                  
                        strQNo = str(iCnt_L1 )
                    elif (iLvlCurr == 2): 
                        strQNo = str(iCnt_L1) + "." + str(iCnt_Section)
                    elif (iLvlCurr == 3): 
                        strQNo = str(iCnt_L1) + "." + str(iCnt_Section) + "." + str(iCnt_SubSection) 
                    elif (iLvlCurr == 4): 
                        strQNo = str(iCnt_L1) + "." +str( iCnt_Section) + "." + str(iCnt_SubSection) + "." + str(iCnt_SubSubSection)
                     
                    if i == 0:  
                        if(str(qtnResult['lvl'][i]) !="1"): 
                            d = {'Section_AID':str(qtnResult['Section_AID'][i]), 
                            'Section_Label':str(qtnResult['Section_Label'][i]), 
                            'Sub_Section_AID':iSubSecPrev, 
                            'Sub_Section_Label':"", 
                            'Sub_Sub_Section_AID':'', 
                            'Sub_Sub_Section_Label':'', 
                            'qtnNo':"",
                            'qtnsArr':'',
                            'lvl': str('->') } 
                            d2[arrayidx] = d
                            arrayidx+=1  

                    if(strSectionText!=""):
                        # dtFinalValues.Rows.Add(strSectionText, 
                        #                        strSubSectionText, 
                        #                        strSubSubSectionText, "", "", 
                        #                        iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0],
                                    'qtnsArr':"",
                                    'qtn_aid':"",
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i]
                                    ,
                                    'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                    'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                    'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                    'Control_Description':qtnResult['Control_Description'][i],
                                    'override_residual_ratings':qtnResult['override_residual_ratings'][i],
                                    'override_comments':qtnResult['override_comments'][i]
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    elif (strSubSectionText != ""):
                        # dtFinalValues.Rows.Add(strSectionText, 
                        #                        strSubSectionText, 
                        #                        strSubSubSectionText, "", 
                        #                        strQNo.Split('.')[0], iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0],
                                    'qtnsArr':"",
                                    'qtn_aid':str(iQuesID),
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i],
                                    'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                    'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                    'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                    'Control_Description':qtnResult['Control_Description'][i],
                                    'override_residual_ratings':qtnResult['override_residual_ratings'][i],
                                    'override_comments':qtnResult['override_comments'][i]
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    elif (strSubSubSectionText != ""):
                        # dtFinalValues.Rows.Add(strSectionText, strSubSectionText, 
                        #                        strSubSubSectionText, "", 
                        #                        strQNo.Split('.')[0] + "." + 
                        #                        strQNo.Split('.')[1], iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0]+ "." +str(strQNo).split('.')[1] ,
                                    'qtnsArr':"",
                                    'qtn_aid':str(iQuesID),
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i]
                                    ,
                                    'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                    'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                    'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                    'Control_Description':qtnResult['Control_Description'][i],
                                    'override_residual_ratings':qtnResult['override_residual_ratings'][i],
                                    'override_comments':qtnResult['override_comments'][i]
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  

                    # dtFinalValues.Rows.Add("", "", "", strLevelText + "    " + strQues, 
                    #                        strQNo, iLvlCurr.ToString());
                    d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':"", 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':"", 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':"", 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo)  ,
                                    'qtnsArr':strQues,
                                    'qtn_aid':str(iQuesID),
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i]
                                    ,
                                    'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                    'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                    'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                    'Control_Description':qtnResult['Control_Description'][i],
                                    'override_residual_ratings':qtnResult['override_residual_ratings'][i],
                                    'override_comments':qtnResult['override_comments'][i]
                                    } 
                    d2[arrayidx] = d
                    arrayidx+=1  
                del qtnResult
        
            del tableResult 
        return d2 # json.dumps(d2)    
    

    def getAllICQQtns(self):
        d2 = {}
        strQ="select a.* from("
        strQ += " select '1' lvl,Section_AID,Section_Label,'-' Sub_Section_AID,'-' Sub_Section_Label,"
        strQ += " '-' Sub_Sub_Section_AID,'-' Sub_Sub_Section_Label,'-' Sub_Sub_Sub_Section_AID,'-' Sub_Sub_Sub_Section_Label "     
        strQ += " from ICQ_Sections   "         
        strQ += " )a  order by  a.Section_AID"#,cast(a.Sub_Section_AID as int),cast(a.Sub_Sub_Section_AID as int),cast(a.Sub_Sub_Sub_Section_AID as int)"
        tableResult =self.objdbops.getTable(strQ) 
        
        arrayidx=0  
        if tableResult.empty == False:
            for ind in tableResult.index: 
                # print(tableResult['Section_AID'][ind],tableResult['Sub_Section_AID'][ind], tableResult['Sub_Sub_Section_AID'][ind], tableResult['Sub_Sub_Sub_Section_AID'][ind])
                # strQtn=" select qtnmst.Question_AID,qtnmst.Question_Label,Rating_Yes_NO ,Doc_Yes_No,isnull(comments,'')comments from icq_question_master qtnmst left join ICQ_Question_Rating_Data_Final "
                # strQtn+="     on qtnmst.Question_aid=ICQ_Question_Rating_Data_Final.question_aid where section_aid='"+str(tableResult['Section_AID'][ind])+"'  and isnull(Sub_Section_AID,'-') ='"+str(tableResult['Sub_Section_AID'][ind]) +"' and "
                # strQtn+=" isnull(Sub_Sub_Section_AID,'-')= '"+str(tableResult['Sub_Sub_Section_AID'][ind])+"' and isnull(Sub_Sub_Sub_Section_AID,'-')='"+str(tableResult['Sub_Sub_Sub_Section_AID'][ind]) +"' "
                # strQtn+=" order by qtnmst.Question_AID,cast(Sub_Section_AID as int),cast(Sub_Sub_Section_AID as int),cast(Sub_Sub_Sub_Section_AID as int)"
                strQtn=""
                strQtn+=" select case when  len(qtnmst.Section_AID )<>  0 and  (qtnmst.Sub_Section_AID) is null then 1 "
                strQtn+=" when  len(qtnmst.Sub_Section_AID)<>  0 and  (qtnmst.Sub_Sub_Section_AID) is null then 2"
                strQtn+=" when len(qtnmst.Sub_Sub_Section_AID)<>0 and  (qtnmst.Sub_Sub_Sub_Section_AID)  is null then 3 "
                strQtn+=" when len(qtnmst.Sub_Sub_Sub_Section_AID)<>  0 then 4  else 0 end lvl,  sec.Section_AID,isnull(s_sec.Sub_Section_AID,'0') Sub_Section_AID,"
                strQtn+=" isnull(ss_sec.Sub_Sub_Section_AID,'0') Sub_Sub_Section_AID,Question_AID ,"
                strQtn+=" qtnmst.Question_Label ,isnull(sec.Section_Label,'') Section_Label, isnull(s_sec.Sub_Section_Label,'') Sub_Section_Label,isnull(ss_sec.Sub_Sub_Section_Label,'') Sub_Sub_Section_Label    from "
                strQtn+=" icq_question_master qtnmst left join ICQ_Sections sec on "
                strQtn+=" qtnmst.section_aid=sec.section_aid left join"
                strQtn+=" ICQ_Sub_Sections s_sec  on qtnmst.sub_section_aid=s_sec.sub_section_aid left join"
                strQtn+=" ICQ_Sub_Sub_Sections ss_sec on qtnmst.sub_sub_section_aid=ss_sec.sub_sub_section_aid "
                strQtn+=" where sec.section_aid="+str(tableResult['Section_AID'][ind]).replace("'","''")+" "
                strQtn+=" order by   Question_AID,qtnmst.section_aid"
                strQtn+=" ,cast(qtnmst.Sub_Section_AID as int),cast(qtnmst.Sub_Sub_Section_AID as int) " 
                qtnResult =self.objdbops.getTable(strQtn)                 
                iLvlCurr=0
                iSecCurr=0
                iSubSecCurr=0
                iSubSubSecCurr=0
                iSubSubSecPrev=0
                iCnt_L1=0
                strQues=""
                strSectionText=""
                strSubSectionText=""
                strSubSubSectionText=""
                iQuesID=0
                iCnt_L1 = 0                #//Q No
                iCnt_Section = 0              # //Q No
                iCnt_SubSection = 0              #  //Q No
                iCnt_SubSubSection = 0              # //Q No 
                strQNo = ""  #//Q No
                blnAlreadyIncreased = False
                for i in qtnResult.index: 
                    blnAlreadyIncreased = False 
                    strLevelText = ""
                    iLvlCurr = int(qtnResult['lvl'][i])
                    iSecCurr = int(qtnResult['Section_AID'][i])
                    iSubSecCurr =int(qtnResult['Sub_Section_AID'][i])
                    iSubSubSecCurr =int(qtnResult['Sub_Sub_Section_AID'][i])
                   
                    
                    iQuesID=int(qtnResult['Question_AID'][i])

                    strQues = qtnResult["Question_Label"][i]
                    strSectionText = qtnResult["Section_Label"][i]
                    strSubSectionText = qtnResult["Sub_Section_Label"][i]
                    strSubSectionText = strSubSectionText.replace("-", "")
                    strSubSubSectionText =qtnResult["Sub_Sub_Section_Label"][i]

                    for j in range(iLvlCurr):
                        strLevelText += "->"

                    if (i == 0): 
                        iCnt_L1 = 0
                        iCnt_Section = 0
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0

                        iLvlPrev = iLvlCurr
                        iSecPrev = iSecCurr
                        iSubSecPrev = iSubSecCurr
                        iSubSubSecCurr = iSubSubSecPrev

                    if (i > 0 and iSecCurr != iSecPrev):
                        iSecPrev = iSecCurr
                        iCnt_L1 = 0
                        iCnt_Section = 0
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0
                    elif (i > 0):
                        strSectionText = ""

                    if (i > 0 and iSubSecCurr != iSubSecPrev):
                        iSubSecPrev = iSubSecCurr
                        if (strSectionText == ""):
                            blnAlreadyIncreased = True
                            iCnt_L1+=1
                        iCnt_Section = 0
                        iCnt_SubSection = 0    
                        iCnt_SubSubSection = 0 
                    elif (i > 0):
                        strSubSectionText = ""

                    if (i > 0 and iSubSubSecCurr>0 and iSubSubSecCurr != iSubSubSecPrev):
                        iSubSubSecPrev = iSubSubSecCurr
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0
                        iCnt_Section+=1
                    elif(i > 0 and iSubSubSecCurr > 0):
                        strSubSubSectionText = ""

                    #   //Increase Question Nos Starts
                    iCnt_L1 =1 if strSectionText != "" and strSubSectionText != "" and iCnt_L1 == 0  else iCnt_L1
                    if (iLvlCurr == 1): 
                        if (blnAlreadyIncreased == False):
                            iCnt_L1 +=1        
                    elif (iLvlCurr == 2):
                        iCnt_Section+=1
                    elif (iLvlCurr == 3): 
                        iCnt_SubSection+=1 
                    elif (iLvlCurr == 4):
                        iCnt_SubSubSection+=1
                    # //Increase Question Nos Ends 

                     
                   
                    if (iLvlCurr == 1):                  
                        strQNo = str(iCnt_L1 )
                    elif (iLvlCurr == 2): 
                        strQNo = str(iCnt_L1) + "." + str(iCnt_Section)
                    elif (iLvlCurr == 3): 
                        strQNo = str(iCnt_L1) + "." + str(iCnt_Section) + "." + str(iCnt_SubSection) 
                    elif (iLvlCurr == 4): 
                        strQNo = str(iCnt_L1) + "." +str( iCnt_Section) + "." + str(iCnt_SubSection) + "." + str(iCnt_SubSubSection)
                     
                    if i == 0:  
                        if(str(qtnResult['lvl'][i]) !="1"): 
                            d = {'Section_AID':str(qtnResult['Section_AID'][i]), 
                            'Section_Label':str(qtnResult['Section_Label'][i]), 
                            'Sub_Section_AID':iSubSecPrev, 
                            'Sub_Section_Label':"", 
                            'Sub_Sub_Section_AID':'', 
                            'Sub_Sub_Section_Label':'', 
                            'qtnNo':"",
                            'qtnsArr':'',
                            'lvl': str('->') } 
                            d2[arrayidx] = d
                            arrayidx+=1  

                    if(strSectionText!=""):
                        # dtFinalValues.Rows.Add(strSectionText, 
                        #                        strSubSectionText, 
                        #                        strSubSubSectionText, "", "", 
                        #                        iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0],
                                    'qtnsArr':"",
                                    'qtn_aid':"", 
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    elif (strSubSectionText != ""):
                        # dtFinalValues.Rows.Add(strSectionText, 
                        #                        strSubSectionText, 
                        #                        strSubSubSectionText, "", 
                        #                        strQNo.Split('.')[0], iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0],
                                    'qtnsArr':"",
                                    'qtn_aid':str(iQuesID), 
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    elif (strSubSubSectionText != ""):
                        # dtFinalValues.Rows.Add(strSectionText, strSubSectionText, 
                        #                        strSubSubSectionText, "", 
                        #                        strQNo.Split('.')[0] + "." + 
                        #                        strQNo.Split('.')[1], iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0]+ "." +str(strQNo).split('.')[1] ,
                                    'qtnsArr':"",
                                    'qtn_aid':str(iQuesID), 
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  

                    # dtFinalValues.Rows.Add("", "", "", strLevelText + "    " + strQues, 
                    #                        strQNo, iLvlCurr.ToString());
                    d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':"", 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':"", 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':"", 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo)  ,
                                    'qtnsArr':strQues,
                                    'qtn_aid':str(iQuesID), 
                                    } 
                    d2[arrayidx] = d
                    arrayidx+=1  
                del qtnResult
        
            del tableResult
        return d2 # json.dumps(d2)    
    

    def getAllICQQtnsAndRatings(self):
        d2 = {}
        strQ="select a.* from("
        strQ += " select '1' lvl,Section_AID,Section_Label,'-' Sub_Section_AID,'-' Sub_Section_Label,"
        strQ += " '-' Sub_Sub_Section_AID,'-' Sub_Sub_Section_Label,'-' Sub_Sub_Sub_Section_AID,'-' Sub_Sub_Sub_Section_Label "     
        strQ += " from ICQ_Sections   "         
        strQ += " )a  order by  a.Section_AID"#,cast(a.Sub_Section_AID as int),cast(a.Sub_Sub_Section_AID as int),cast(a.Sub_Sub_Sub_Section_AID as int)"
        tableResult =self.objdbops.getTable(strQ) 
        
        arrayidx=0 
        if tableResult.empty == False:
            for ind in tableResult.index: 
                # print(tableResult['Section_AID'][ind],tableResult['Sub_Section_AID'][ind], tableResult['Sub_Sub_Section_AID'][ind], tableResult['Sub_Sub_Sub_Section_AID'][ind])
                # strQtn=" select qtnmst.Question_AID,qtnmst.Question_Label,Rating_Yes_NO ,Doc_Yes_No,isnull(comments,'')comments from icq_question_master qtnmst left join ICQ_Question_Rating_Data_Final "
                # strQtn+="     on qtnmst.Question_aid=ICQ_Question_Rating_Data_Final.question_aid where section_aid='"+str(tableResult['Section_AID'][ind])+"'  and isnull(Sub_Section_AID,'-') ='"+str(tableResult['Sub_Section_AID'][ind]) +"' and "
                # strQtn+=" isnull(Sub_Sub_Section_AID,'-')= '"+str(tableResult['Sub_Sub_Section_AID'][ind])+"' and isnull(Sub_Sub_Sub_Section_AID,'-')='"+str(tableResult['Sub_Sub_Sub_Section_AID'][ind]) +"' "
                # strQtn+=" order by qtnmst.Question_AID,cast(Sub_Section_AID as int),cast(Sub_Sub_Section_AID as int),cast(Sub_Sub_Sub_Section_AID as int)"
                strQtn=""
                strQtn+=" select isnull(cast([Rating_Yes] as varchar),'')[Rating_Yes],isnull(cast([Rating_No] as varchar),'')[Rating_No], "
                strQtn+=" isnull(cast([Doc_Yes] as varchar),'')[Doc_Yes],isnull(cast([Doc_no] as varchar),'')[Doc_no] , case when  len(qtnmst.Section_AID )<>  0 and  (qtnmst.Sub_Section_AID) is null then 1 "
                strQtn+=" when  len(qtnmst.Sub_Section_AID)<>  0 and  (qtnmst.Sub_Sub_Section_AID) is null then 2"
                strQtn+=" when len(qtnmst.Sub_Sub_Section_AID)<>0 and  (qtnmst.Sub_Sub_Sub_Section_AID)  is null then 3 "
                strQtn+=" when len(qtnmst.Sub_Sub_Sub_Section_AID)<>  0 then 4  else 0 end lvl,  sec.Section_AID,isnull(s_sec.Sub_Section_AID,'0') Sub_Section_AID,"
                strQtn+=" isnull(ss_sec.Sub_Sub_Section_AID,'0') Sub_Sub_Section_AID,qtnmst.Question_AID ,"
                strQtn+=" qtnmst.Question_Label ,isnull(sec.Section_Label,'') Section_Label, isnull(s_sec.Sub_Section_Label,'') Sub_Section_Label,isnull(ss_sec.Sub_Sub_Section_Label,'') Sub_Sub_Section_Label    from "
                strQtn+=" icq_question_master qtnmst left join ICQ_Sections sec on "
                strQtn+=" qtnmst.section_aid=sec.section_aid left join"
                strQtn+=" ICQ_Sub_Sections s_sec  on qtnmst.sub_section_aid=s_sec.sub_section_aid left join"
                strQtn+=" ICQ_Sub_Sub_Sections ss_sec on qtnmst.sub_sub_section_aid=ss_sec.sub_sub_section_aid left join ICQ_Question_Rating  ratings on qtnmst.Question_AID =ratings.Question_AID "
                strQtn+=" where sec.section_aid="+str(tableResult['Section_AID'][ind]).replace("'","''")+" "
                strQtn+=" order by   Question_AID,qtnmst.section_aid"
                strQtn+=" ,cast(qtnmst.Sub_Section_AID as int),cast(qtnmst.Sub_Sub_Section_AID as int) " 
                qtnResult =self.objdbops.getTable(strQtn)        
                   
                iLvlCurr=0
                iSecCurr=0
                iSubSecCurr=0
                iSubSubSecCurr=0
                iSubSubSecPrev=0
                iCnt_L1=0
                strQues=""
                strSectionText=""
                strSubSectionText=""
                strSubSubSectionText=""
                iQuesID=0
                iCnt_L1 = 0                #//Q No
                iCnt_Section = 0              # //Q No
                iCnt_SubSection = 0              #  //Q No
                iCnt_SubSubSection = 0              # //Q No 
                strQNo = ""  #//Q No
                blnAlreadyIncreased = False
                for i in qtnResult.index: 
                    blnAlreadyIncreased = False 
                    strLevelText = ""
                    iLvlCurr = int(qtnResult['lvl'][i])
                    iSecCurr = int(qtnResult['Section_AID'][i])
                    iSubSecCurr =int(qtnResult['Sub_Section_AID'][i])
                    iSubSubSecCurr =int(qtnResult['Sub_Sub_Section_AID'][i])
                   
                    
                    iQuesID=int(qtnResult['Question_AID'][i])

                    strQues = qtnResult["Question_Label"][i]
                    strSectionText = qtnResult["Section_Label"][i]
                    strSubSectionText = qtnResult["Sub_Section_Label"][i]
                    strSubSectionText = strSubSectionText.replace("-", "")
                    strSubSubSectionText =qtnResult["Sub_Sub_Section_Label"][i]

                    for j in range(iLvlCurr):
                        strLevelText += "->"

                    if (i == 0): 
                        iCnt_L1 = 0
                        iCnt_Section = 0
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0

                        iLvlPrev = iLvlCurr
                        iSecPrev = iSecCurr
                        iSubSecPrev = iSubSecCurr
                        iSubSubSecCurr = iSubSubSecPrev

                    if (i > 0 and iSecCurr != iSecPrev):
                        iSecPrev = iSecCurr
                        iCnt_L1 = 0
                        iCnt_Section = 0
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0
                    elif (i > 0):
                        strSectionText = ""

                    if (i > 0 and iSubSecCurr != iSubSecPrev):
                        iSubSecPrev = iSubSecCurr
                        if (strSectionText == ""):
                            blnAlreadyIncreased = True
                            iCnt_L1+=1
                        iCnt_Section = 0
                        iCnt_SubSection = 0    
                        iCnt_SubSubSection = 0 
                    elif (i > 0):
                        strSubSectionText = ""

                    if (i > 0 and iSubSubSecCurr>0 and iSubSubSecCurr != iSubSubSecPrev):
                        iSubSubSecPrev = iSubSubSecCurr
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0
                        iCnt_Section+=1
                    elif(i > 0 and iSubSubSecCurr > 0):
                        strSubSubSectionText = ""

                    #   //Increase Question Nos Starts
                    iCnt_L1 =1 if strSectionText != "" and strSubSectionText != "" and iCnt_L1 == 0  else iCnt_L1
                    if (iLvlCurr == 1): 
                        if (blnAlreadyIncreased == False):
                            iCnt_L1 +=1        
                    elif (iLvlCurr == 2):
                        iCnt_Section+=1
                    elif (iLvlCurr == 3): 
                        iCnt_SubSection+=1 
                    elif (iLvlCurr == 4):
                        iCnt_SubSubSection+=1
                    # //Increase Question Nos Ends 

                     
                   
                    if (iLvlCurr == 1):                  
                        strQNo = str(iCnt_L1 )
                    elif (iLvlCurr == 2): 
                        strQNo = str(iCnt_L1) + "." + str(iCnt_Section)
                    elif (iLvlCurr == 3): 
                        strQNo = str(iCnt_L1) + "." + str(iCnt_Section) + "." + str(iCnt_SubSection) 
                    elif (iLvlCurr == 4): 
                        strQNo = str(iCnt_L1) + "." +str( iCnt_Section) + "." + str(iCnt_SubSection) + "." + str(iCnt_SubSubSection)
                     
                    if i == 0:  
                        if(str(qtnResult['lvl'][i]) !="1"): 
                            d = {'Section_AID':str(qtnResult['Section_AID'][i]), 
                            'Section_Label':str(qtnResult['Section_Label'][i]), 
                            'Sub_Section_AID':iSubSecPrev, 
                            'Sub_Section_Label':"", 
                            'Sub_Sub_Section_AID':'', 
                            'Sub_Sub_Section_Label':'', 
                            'qtnNo':"",
                            'qtnsArr':'',
                            'lvl': str('->') } 
                            d2[arrayidx] = d
                            arrayidx+=1  

                    if(strSectionText!=""):
                        # dtFinalValues.Rows.Add(strSectionText, 
                        #                        strSubSectionText, 
                        #                        strSubSubSectionText, "", "", 
                        #                        iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0],
                                    'qtnsArr':"",
                                    'qtn_aid':"", 
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    elif (strSubSectionText != ""):
                        # dtFinalValues.Rows.Add(strSectionText, 
                        #                        strSubSectionText, 
                        #                        strSubSubSectionText, "", 
                        #                        strQNo.Split('.')[0], iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0],
                                    'qtnsArr':"",
                                    'qtn_aid':str(iQuesID), 
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    elif (strSubSubSectionText != ""):
                        # dtFinalValues.Rows.Add(strSectionText, strSubSectionText, 
                        #                        strSubSubSectionText, "", 
                        #                        strQNo.Split('.')[0] + "." + 
                        #                        strQNo.Split('.')[1], iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0]+ "." +str(strQNo).split('.')[1] ,
                                    'qtnsArr':"",
                                    'qtn_aid':str(iQuesID), 
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  

                    # dtFinalValues.Rows.Add("", "", "", strLevelText + "    " + strQues, 
                    #                        strQNo, iLvlCurr.ToString());
                    d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':"", 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':"", 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':"", 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo)  ,
                                    'qtnsArr':strQues,
                                    'qtn_aid':str(iQuesID), 
                                     'Rating_Yes':qtnResult['Rating_Yes'][i],
                                     'Rating_No':qtnResult['Rating_No'][i],
                                     'Doc_Yes':qtnResult['Doc_Yes'][i],
                                     'Doc_No':qtnResult['Doc_no'][i]
                                    } 
                    d2[arrayidx] = d
                    arrayidx+=1  
                del qtnResult
        
            del tableResult
        return d2 # json.dumps(d2)    
    

    def getICQIds(self):
        tableResult =self.objdbops.getTable("select max(ICQS_AID) review_id,ICQS_text review_name from  ICQ_Setting group by ICQS_text")
       
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    
    def getmaxICQId(self):
        return  str(self.objdbops.getscalar("select max(ICQS_AID) review_id from  ICQ_Setting"))

    def getmaxFLId(self):
        return  str(self.objdbops.getscalar("select max(FLS_AID) review_id from  FL_Setting"))
    
    def canUpdateRatings(self,uid):
        return str(self.objdbops.getscalar("select count(*) from [ICQ_Question_Rating_Data_Final] where [Review_id] in ( \
                                        select max(ICQS_AID) review_id from  ICQ_Setting) and addedby='"+str(uid).replace("'","''")+"'"))

    def FLcanUpdateRatings(self,uid):
        return str(self.objdbops.getscalar("select count(*) from [FL_Question_Rating_Data] where [Review_id] in ( \
                                        select max(FLS_AID) review_id from  FL_Setting) and addedby='"+str(uid).replace("'","''")+"'"))
    
    
    def insert_notification(self,from_user:str,to_user:str,utility:str,notification_trigger:str,is_visible): 
        create_date= datetime.now()
        notification_obj=NotificationDetails(notification_from=from_user,notification_to=to_user,utility=utility,
                                            notification_trigger=notification_trigger,is_visible=is_visible,create_date=create_date)
        notification_obj.save() 
      
    def publishICQ(self):
        maxid=   str(self.objdbops.getscalar("select max(ICQS_AID) review_id from  ICQ_Setting"))
        self.objdbops.insertRow("update ICQ_Setting set publish=1 where ICQS_AID="+maxid.replace("'","''"))

    def publishFL(self):
        maxid=   str(self.objdbops.getscalar("select max(FLS_AID) review_id from  FL_Setting"))
        self.objdbops.insertRow("update FL_Setting set publish=1 where FLS_AID="+maxid.replace("'","''"))

    def insertRatings(self,q_id,yes,no,doc_yes,doc_no):
        if(str(self.objdbops.getscalar("select count(*) from ICQ_Question_Rating where question_aid="+str(q_id)))=="0"):
            strQ="INSERT INTO   ICQ_Question_Rating \
            ( Question_AID \
            , Rating_Yes \
            , Rating_No \
            , Doc_Yes \
            , Doc_No , AddDate  )\
                VALUES\
            ("+str(q_id).replace("'","''") +"\
            ,"+str(yes).replace("'","''")+"\
            ,"+str(no).replace("'","''")+"\
            ,"+str(doc_yes).replace("'","''")+"\
            ,"+str(doc_no).replace("'","''")+" ,getdate() )"
            self.objdbops.insertRow(strQ)
        else:
            strQ="update ICQ_Question_Rating set Rating_Yes="+str(yes).replace("'","''")+",Rating_No="+str(no).replace("'","''")+",Doc_Yes="+str(doc_yes).replace("'","''")+",Doc_No="+str(doc_no).replace("'","''")+" where   question_aid="+str(q_id).replace("'","''")
            self.objdbops.insertRow(strQ)
    

    
    def thread_creation(self,send_by,send_to):  
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
    
    def getQuesSections(self):
        tableResult =self.objdbops.getTable("select  Section_Label , Section_AID  from  Ques_Sections  order by  Section_AID ")
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)       
      
    def getAllQtns(self,mdl_id=''):
        d2 = {}
        strQ="select a.* from("
        strQ += " select '1' lvl,Section_AID,Section_Label,'-' Sub_Section_AID,'-' Sub_Section_Label,"
        strQ += " '-' Sub_Sub_Section_AID,'-' Sub_Sub_Section_Label,'-' Sub_Sub_Sub_Section_AID,'-' Sub_Sub_Sub_Section_Label "     
        strQ += " from Ques_Sections "   
        if(mdl_id !=''):
            strQ+=" where modeltool_type in (select case Mdl_Src_Label when 'Internal' then '2' when 'Vendor' then '1' else '3' end qtntype  from Model_Source_Master mdlsrc, Mdl_OverView mdl\
                where mdl.Mdl_Source=mdlsrc.Mdl_Scr_AID and mdl.Mdl_Id ='"+ mdl_id.replace("'","''") +"')"         
        strQ += " )a  order by  a.Section_AID"
        tableResult =self.objdbops.getTable(strQ) 
        
        arrayidx=0 
        if tableResult.empty == False:
            for ind in tableResult.index: 
                strQtn=""
                strQtn+=" select case when  len(qtnmst.Section_AID )<>  0 and  (qtnmst.Sub_Section_AID) is null then 1 "
                strQtn+=" when  len(qtnmst.Sub_Section_AID)<>  0 and  (qtnmst.Sub_Sub_Section_AID) is null then 2"
                strQtn+=" when len(qtnmst.Sub_Sub_Section_AID)<>0 and  (qtnmst.Sub_Sub_Sub_Section_AID)  is null then 3 "
                strQtn+=" when len(qtnmst.Sub_Sub_Sub_Section_AID)<>  0 then 4  else 0 end lvl,  sec.Section_AID,isnull(s_sec.Sub_Section_AID,'0') Sub_Section_AID,"
                strQtn+=" isnull(ss_sec.Sub_Sub_Section_AID,'0') Sub_Sub_Section_AID,Question_AID ,"
                strQtn+=" qtnmst.Question_Label ,isnull(sec.Section_Label,'') Section_Label, isnull(s_sec.Sub_Section_Label,'') Sub_Section_Label,isnull(ss_sec.Sub_Sub_Section_Label,'') Sub_Sub_Section_Label    from "
                strQtn+=" Question_Ques_Master qtnmst left join Ques_Sections sec on "
                strQtn+=" qtnmst.section_aid=sec.section_aid left join"
                strQtn+=" Ques_Sub_Sections s_sec  on qtnmst.sub_section_aid=s_sec.sub_section_aid left join"
                strQtn+=" Ques_Sub_Sub_Sections ss_sec on qtnmst.sub_sub_section_aid=ss_sec.sub_sub_section_aid "
                strQtn+=" where sec.section_aid="+str(tableResult['Section_AID'][ind]).replace("'","''")+" "
                strQtn+=" order by qtnmst.section_aid"
                strQtn+=" ,cast(qtnmst.Sub_Section_AID as int),cast(qtnmst.Sub_Sub_Section_AID as int) " 
                qtnResult =self.objdbops.getTable(strQtn)                 
               
                iLvlCurr=0
                iSecCurr=0
                iSubSecCurr=0
                iSubSubSecCurr=0
                iSubSubSecPrev=0
                iCnt_L1=0
                strQues=""
                strSectionText=""
                strSubSectionText=""
                strSubSubSectionText=""
                iQuesID=0
                iCnt_L1 = 0                #//Q No
                iCnt_Section = 0              # //Q No
                iCnt_SubSection = 0              #  //Q No
                iCnt_SubSubSection = 0              # //Q No 
                strQNo = ""  #//Q No
                blnAlreadyIncreased = False
                for i in qtnResult.index: 
                    blnAlreadyIncreased = False 
                    strLevelText = ""
                    iLvlCurr = int(qtnResult['lvl'][i])
                    iSecCurr = int(qtnResult['Section_AID'][i])
                    iSubSecCurr =int(qtnResult['Sub_Section_AID'][i])
                    iSubSubSecCurr =int(qtnResult['Sub_Sub_Section_AID'][i])
                   
                    
                    iQuesID=int(qtnResult['Question_AID'][i])

                    strQues = qtnResult["Question_Label"][i]
                    strSectionText = qtnResult["Section_Label"][i]
                    strSubSectionText = qtnResult["Sub_Section_Label"][i]
                    strSubSectionText = strSubSectionText.replace("-", "")
                    strSubSubSectionText =qtnResult["Sub_Sub_Section_Label"][i]

                    for j in range(iLvlCurr):
                        strLevelText += "->"

                    if (i == 0): 
                        iCnt_L1 = 0
                        iCnt_Section = 0
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0

                        iLvlPrev = iLvlCurr
                        iSecPrev = iSecCurr
                        iSubSecPrev = iSubSecCurr
                        iSubSubSecCurr = iSubSubSecPrev

                    if (i > 0 and iSecCurr != iSecPrev):
                        iSecPrev = iSecCurr
                        iCnt_L1 = 0
                        iCnt_Section = 0
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0
                    elif (i > 0):
                        strSectionText = ""

                    if (i > 0 and iSubSecCurr != iSubSecPrev):
                        iSubSecPrev = iSubSecCurr
                        if (strSectionText == ""):
                            blnAlreadyIncreased = True
                            iCnt_L1+=1
                        iCnt_Section = 0
                        iCnt_SubSection = 0    
                        iCnt_SubSubSection = 0 
                    elif (i > 0):
                        strSubSectionText = ""

                    if (i > 0 and iSubSubSecCurr>0 and iSubSubSecCurr != iSubSubSecPrev):
                        iSubSubSecPrev = iSubSubSecCurr
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0
                        iCnt_Section+=1
                    elif(i > 0 and iSubSubSecCurr > 0):
                        strSubSubSectionText = ""

                    #   //Increase Question Nos Starts
                    iCnt_L1 =1 if strSectionText != "" and strSubSectionText != "" and iCnt_L1 == 0  else iCnt_L1
                    if (iLvlCurr == 1): 
                        if (blnAlreadyIncreased == False):
                            iCnt_L1 +=1        
                    elif (iLvlCurr == 2):
                        iCnt_Section+=1
                    elif (iLvlCurr == 3): 
                        iCnt_SubSection+=1 
                    elif (iLvlCurr == 4):
                        iCnt_SubSubSection+=1
                    # //Increase Question Nos Ends 

                     
                   
                    if (iLvlCurr == 1):                  
                        strQNo = str(iCnt_L1 )
                    elif (iLvlCurr == 2): 
                        strQNo = str(iCnt_L1) + "." + str(iCnt_Section)
                    elif (iLvlCurr == 3): 
                        strQNo = str(iCnt_L1) + "." + str(iCnt_Section) + "." + str(iCnt_SubSection) 
                    elif (iLvlCurr == 4): 
                        strQNo = str(iCnt_L1) + "." +str( iCnt_Section) + "." + str(iCnt_SubSection) + "." + str(iCnt_SubSubSection)
                     
                    if i == 0:  
                        if(str(qtnResult['lvl'][i]) !="1"): 
                            d = {'Section_AID':str(qtnResult['Section_AID'][i]), 
                            'Section_Label':str(qtnResult['Section_Label'][i]), 
                            'Sub_Section_AID':iSubSecPrev, 
                            'Sub_Section_Label':"", 
                            'Sub_Sub_Section_AID':'', 
                            'Sub_Sub_Section_Label':'', 
                            'qtnNo':"",
                            'qtnsArr':'',
                            'lvl': str('->') } 
                            d2[arrayidx] = d
                            arrayidx+=1  

                    if(strSectionText!=""):
                        # dtFinalValues.Rows.Add(strSectionText, 
                        #                        strSubSectionText, 
                        #                        strSubSubSectionText, "", "", 
                        #                        iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0],
                                    'qtnsArr':"",
                                    'qtn_aid':"", 
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    elif (strSubSectionText != ""):
                        # dtFinalValues.Rows.Add(strSectionText, 
                        #                        strSubSectionText, 
                        #                        strSubSubSectionText, "", 
                        #                        strQNo.Split('.')[0], iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0],
                                    'qtnsArr':"",
                                    'qtn_aid':str(iQuesID), 
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    elif (strSubSubSectionText != ""):
                        # dtFinalValues.Rows.Add(strSectionText, strSubSectionText, 
                        #                        strSubSubSectionText, "", 
                        #                        strQNo.Split('.')[0] + "." + 
                        #                        strQNo.Split('.')[1], iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0]+ "." +str(strQNo).split('.')[1] ,
                                    'qtnsArr':"",
                                    'qtn_aid':str(iQuesID), 
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  

                    # dtFinalValues.Rows.Add("", "", "", strLevelText + "    " + strQues, 
                    #                        strQNo, iLvlCurr.ToString());
                    d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':"", 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':"", 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':"", 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo)  ,
                                    'qtnsArr':strQues,
                                    'qtn_aid':str(iQuesID), 
                                    } 
                    d2[arrayidx] = d
                    arrayidx+=1  
                del qtnResult
        
            del tableResult
        return d2 # json.dumps(d2)   
    
    def getQues_Sub_Sections(self,id):
        tableResult =self.objdbops.getTable("select  Sub_Section_Label , Sub_Section_AID  from  Ques_Sub_Sections where Section_AID="+str(id).replace("'","''")+" order by  Sub_Section_AID ")
        print("tableResult ",tableResult)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)

    def addQuesSection(self,stype,section,desc,activests,userId):  
        strQ="insert into Ques_Sections ("
        strQ += " ModelTool_Type, "
        strQ += " Section_Label   ,"
        strQ += " Section_Description  ,"
        strQ += " ActiveStatus ,"
        strQ += " AddedBy    ,"
        strQ += " AddDate  )"
        strQ += " values("
        strQ += " '"+stype.replace("'","''")+"'   ,"
        strQ += " '"+section.replace("'","''")+"'   ,"
        strQ += " '"+desc.replace("'","''")+"'  ,"
        strQ += " '"+activests.replace("'","''")+"' ,"
        strQ += " '"+userId.replace("'","''")+"'    ,"
        strQ += " GETDATE()  )	 "
        self.objdbops.insertRow(strQ)   
        
    def addQuesSub_Section(self,id,section,desc,activests,userId):  
        strQ="insert into Ques_Sub_Sections ("
        strQ += " Sub_Section_Label   ,"
        strQ += " Sub_Section_Description  ,Section_AID, "
        strQ += " ActiveStatus ,"
        strQ += " AddedBy    ,"
        strQ += " AddDate  )"
        strQ += " values("
        strQ += " '"+section.replace("'","''")+"'   ,"
        strQ += " '"+desc.replace("'","''")+"'  ,"+id.replace("'","''")+", "
        strQ += " '"+activests.replace("'","''")+"' ,"
        strQ += " '"+userId.replace("'","''")+"'    ,"
        strQ += " GETDATE()  )	 "
        self.objdbops.insertRow(strQ)   

    def getQuesSub_Sections(self,id):
        tableResult =self.objdbops.getTable("select  Sub_Section_Label , Sub_Section_AID  from  Ques_Sub_Sections where Section_AID="+str(id).replace("'","''")+" order by  Sub_Section_AID ")
        print("tableResult ",tableResult)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    
    def addQuesSub_Sub_Section(self,id,section,desc,activests,userId):  
        strQ="insert into Ques_Sub_Sub_Sections ("
        strQ += " Sub_Sub_Section_Label   ,"
        strQ += " Sub_Sub_Section_Description  ,Sub_Section_AID, "
        strQ += " ActiveStatus ,"
        strQ += " AddedBy    ,"
        strQ += " AddDate  )"
        strQ += " values("
        strQ += " '"+section.replace("'","''")+"'   ,"
        strQ += " '"+desc.replace("'","''")+"'  ,"+id.replace("'","''")+", "
        strQ += " '"+activests.replace("'","''")+"' ,"
        strQ += " '"+userId.replace("'","''") +"'    ,"
        strQ += " GETDATE()  )	 "
        self.objdbops.insertRow(strQ)   

    def getQuesSub_Sub_Sections(self,id):
        tableResult =self.objdbops.getTable("select  Sub_Sub_Section_Label , Sub_Sub_Section_AID  from  Ques_Sub_Sub_Sections where Sub_Section_AID="+str(id).replace("'","''")+" order by  Sub_Section_AID ")
        print("tableResult ",tableResult)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)  
    
    def addQuesSub_Sub_Sub_Section(self,id,section,desc,activests,userId):  
        strQ="insert into Ques_Sub_Sub_Sub_Sections ("
        strQ += " Sub_Sub_Sub_Section_Label   ,"
        strQ += " Sub_Sub_Sub_Section_Description  ,Sub_Sub_Section_AID, "
        strQ += " ActiveStatus ,"
        strQ += " AddedBy    ,"
        strQ += " AddDate  )"
        strQ += " values("
        strQ += " '"+section.replace("'","''")+"'   ,"
        strQ += " '"+desc.replace("'","''")+"'  ,"+id.replace("'","''")+", "
        strQ += " '"+activests.replace("'","''")+"' ,"
        strQ += " '"+userId.replace("'","''") +"'    ,"
        strQ += " GETDATE()  )	 "
        self.objdbops.insertRow(strQ)   

    def getSub_Sub_Sub_Sections(self,id):
        tableResult =self.objdbops.getTable("select  Sub_Sub_Sub_Section_Label , Sub_Sub_Sub_Section_AID  from  ICQ_Sub_Sub_Sub_Sections where Sub_Sub_Section_AID="+str(id).replace("'","''")+" order by  Sub_Sub_Section_AID ")
        print("tableResult ",tableResult)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)

    def getQuesSub_Sub_Sub_Sections(self,id):
        tableResult =self.objdbops.getTable("select  Sub_Sub_Sub_Section_Label , Sub_Sub_Sub_Section_AID  from  Ques_Sub_Sub_Sub_Sections where Sub_Sub_Section_AID="+str(id).replace("'","''")+" order by  Sub_Sub_Section_AID")
        print("tableResult ",tableResult)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)

    def get_Qtn_Section(self,mdl_id):
        strQuery="  select * from Ques_Sections where ModelTool_Type in(\
            select case Mdl_Src_Label when 'Internal' then '2' when 'Vendor' then '1' else '3' end qtntype  from [Model_Source_Master] mdlsrc, Mdl_OverView mdl\
            where mdl.Mdl_Source=mdlsrc.Mdl_Scr_AID and mdl.Mdl_Id ='"+ mdl_id.replace("'","''") +"'\
            ) order by 1"
        tableResult =self.objdbops.getTable(strQuery)
        print("tableResult ",tableResult)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult) 
  
    def getQues_Sections(self,id):
        tableResult =self.objdbops.getTable("select  Section_Label , Section_AID  from  Ques_Sections where modeltool_type="+str(id).replace("'","''")+" order by Section_AID ")
        print("tableResult ",tableResult)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    
    def isAutherized(self,userCatId,rsrclbl):
        # print('user access ',self.objdbops.getscalar("select count(*) from User_Access where UC_AID ='"+str(userCatId)+"' and r_aid='"+rsrcId+"'"))
        # return str(self.objdbops.getscalar("select count(*) from User_Access where UC_AID ='"+str(userCatId)+"' and r_aid='"+rsrcId+"'"))
        return str(self.objdbops.getscalar("select count(*) from User_Access INNER JOIN Resources on User_Access.R_AID = Resources.R_AID where UC_AID = '"+str(userCatId).replace("'","''")+"' and Resources.R_Label = '"+rsrclbl.replace("'","''")+"'"))
    

    def FL_addSub_Sub_Sub_Section(self,id,section,desc,activests,userId,sect_type):  
        strQ="insert into FL_Sub_Sub_Sub_Sections ("
        strQ += " Sub_Sub_Sub_Section_Label   ,"
        strQ += " Sub_Sub_Sub_Section_Description  ,Sub_Sub_Section_AID ,Sub_Sub_Sub_Section_Type "
        strQ += " ActiveStatus ,"
        strQ += " AddedBy    ,"
        strQ += " AddDate  )"
        strQ += " values("
        strQ += " '"+section.replace("'","''")+"'   ,"
        strQ += " '"+desc.replace("'","''")+"'  ,"+id.replace("'","''")+", "+sect_type.replace("'","''")+", "
        strQ += " '"+activests.replace("'","''")+"' ,"
        strQ += " '"+userId.replace("'","''") +"'    ,"
        strQ += " GETDATE()  )	 "
        self.objdbops.insertRow(strQ)   

    def getUdaapSections(self):
            tableResult =self.objdbops.getTable("select  Section_Label , Section_AID  from  Udaap_Sections  order by  Section_AID ")
            tableResult= tableResult.to_json(orient='index')
            return json.loads(tableResult) 

    def getAllUdaapQtnsAndRatings(self):
            d2 = {}
            strQ="select a.* from("
            strQ += " select '1' lvl,Section_AID,Section_Label,'-' Sub_Section_AID,'-' Sub_Section_Label,"
            strQ += " '-' Sub_Sub_Section_AID,'-' Sub_Sub_Section_Label,'-' Sub_Sub_Sub_Section_AID,'-' Sub_Sub_Sub_Section_Label "     
            strQ += " from Udaap_Sections   "         
            strQ += " )a  order by  a.Section_AID"#,cast(a.Sub_Section_AID as int),cast(a.Sub_Sub_Section_AID as int),cast(a.Sub_Sub_Sub_Section_AID as int)"
            tableResult =self.objdbops.getTable(strQ) 

            arrayidx=0 
            if tableResult.empty == False:
                for ind in tableResult.index: 
                    # print(tableResult['Section_AID'][ind],tableResult['Sub_Section_AID'][ind], tableResult['Sub_Sub_Section_AID'][ind], tableResult['Sub_Sub_Sub_Section_AID'][ind])
                    # strQtn=" select qtnmst.Question_AID,qtnmst.Question_Label,Rating_Yes_NO ,Doc_Yes_No,isnull(comments,'')comments from icq_question_master qtnmst left join ICQ_Question_Rating_Data_Final "
                    # strQtn+="     on qtnmst.Question_aid=ICQ_Question_Rating_Data_Final.question_aid where section_aid='"+str(tableResult['Section_AID'][ind])+"'  and isnull(Sub_Section_AID,'-') ='"+str(tableResult['Sub_Section_AID'][ind]) +"' and "
                    # strQtn+=" isnull(Sub_Sub_Section_AID,'-')= '"+str(tableResult['Sub_Sub_Section_AID'][ind])+"' and isnull(Sub_Sub_Sub_Section_AID,'-')='"+str(tableResult['Sub_Sub_Sub_Section_AID'][ind]) +"' "
                    # strQtn+=" order by qtnmst.Question_AID,cast(Sub_Section_AID as int),cast(Sub_Sub_Section_AID as int),cast(Sub_Sub_Sub_Section_AID as int)"
                    strQtn=""
                    strQtn+=" select isnull(cast([Rating_Yes] as varchar),'')[Rating_Yes],isnull(cast([Rating_No] as varchar),'')[Rating_No], "
                    strQtn+=" isnull(cast([NA] as varchar),'')[NA], case when  len(qtnmst.Section_AID )<>  0 and  (qtnmst.Sub_Section_AID) is null then 1 "
                    strQtn+=" when  len(qtnmst.Sub_Section_AID)<>  0 and  (qtnmst.Sub_Sub_Section_AID) is null then 2"
                    strQtn+=" when len(qtnmst.Sub_Sub_Section_AID)<>0 and  (qtnmst.Sub_Sub_Sub_Section_AID)  is null then 3 "
                    strQtn+=" when len(qtnmst.Sub_Sub_Sub_Section_AID)<>  0 then 4  else 0 end lvl,  sec.Section_AID,isnull(s_sec.Sub_Section_AID,'0') Sub_Section_AID,"
                    strQtn+=" isnull(ss_sec.Sub_Sub_Section_AID,'0') Sub_Sub_Section_AID,qtnmst.Question_AID ,"
                    strQtn+=" qtnmst.Question_Label ,isnull(sec.Section_Label,'') Section_Label, isnull(s_sec.Sub_Section_Label,'') Sub_Section_Label,isnull(ss_sec.Sub_Sub_Section_Label,'') Sub_Sub_Section_Label    from "
                    strQtn+=" Udaap_question_master qtnmst left join Udaap_Sections sec on "
                    strQtn+=" qtnmst.section_aid=sec.section_aid left join"
                    strQtn+=" Udaap_Sub_Sections s_sec  on qtnmst.sub_section_aid=s_sec.sub_section_aid left join"
                    strQtn+=" Udaap_Sub_Sub_Sections ss_sec on qtnmst.sub_sub_section_aid=ss_sec.sub_sub_section_aid left join Udaap_Question_Rating  ratings on qtnmst.Question_AID =ratings.Question_AID "
                    strQtn+=" where sec.section_aid="+str(tableResult['Section_AID'][ind])+" "
                    strQtn+=" order by   Question_AID,qtnmst.section_aid"
                    strQtn+=" ,cast(qtnmst.Sub_Section_AID as int),cast(qtnmst.Sub_Sub_Section_AID as int) " 
                    qtnResult =self.objdbops.getTable(strQtn)        
                        
                    iLvlCurr=0
                    iSecCurr=0
                    iSubSecCurr=0
                    iSubSubSecCurr=0
                    iSubSubSecPrev=0
                    iCnt_L1=0
                    strQues=""
                    strSectionText=""
                    strSubSectionText=""
                    strSubSubSectionText=""
                    iQuesID=0
                    iCnt_L1 = 0                #//Q No
                    iCnt_Section = 0              # //Q No
                    iCnt_SubSection = 0              #  //Q No
                    iCnt_SubSubSection = 0              # //Q No 
                    strQNo = ""  #//Q No
                    blnAlreadyIncreased = False
                    for i in qtnResult.index: 
                        blnAlreadyIncreased = False 
                        strLevelText = ""
                        iLvlCurr = int(qtnResult['lvl'][i])
                        iSecCurr = int(qtnResult['Section_AID'][i])
                        iSubSecCurr =int(qtnResult['Sub_Section_AID'][i])
                        iSubSubSecCurr =int(qtnResult['Sub_Sub_Section_AID'][i])
                        
                        
                        iQuesID=int(qtnResult['Question_AID'][i])

                        strQues = qtnResult["Question_Label"][i]
                        strSectionText = qtnResult["Section_Label"][i]
                        strSubSectionText = qtnResult["Sub_Section_Label"][i]
                        strSubSectionText = strSubSectionText.replace("-", "")
                        strSubSubSectionText =qtnResult["Sub_Sub_Section_Label"][i]

                        for j in range(iLvlCurr):
                            strLevelText += "->"

                        if (i == 0): 
                            iCnt_L1 = 0
                            iCnt_Section = 0
                            iCnt_SubSection = 0
                            iCnt_SubSubSection = 0

                            iLvlPrev = iLvlCurr
                            iSecPrev = iSecCurr
                            iSubSecPrev = iSubSecCurr
                            iSubSubSecCurr = iSubSubSecPrev

                        if (i > 0 and iSecCurr != iSecPrev):
                            iSecPrev = iSecCurr
                            iCnt_L1 = 0
                            iCnt_Section = 0
                            iCnt_SubSection = 0
                            iCnt_SubSubSection = 0
                        elif (i > 0):
                            strSectionText = ""

                        if (i > 0 and iSubSecCurr != iSubSecPrev):
                            iSubSecPrev = iSubSecCurr
                            if (strSectionText == ""):
                                blnAlreadyIncreased = True
                                iCnt_L1+=1
                            iCnt_Section = 0
                            iCnt_SubSection = 0    
                            iCnt_SubSubSection = 0 
                        elif (i > 0):
                            strSubSectionText = ""

                        if (i > 0 and iSubSubSecCurr>0 and iSubSubSecCurr != iSubSubSecPrev):
                            iSubSubSecPrev = iSubSubSecCurr
                            iCnt_SubSection = 0
                            iCnt_SubSubSection = 0
                            iCnt_Section+=1
                        elif(i > 0 and iSubSubSecCurr > 0):
                            strSubSubSectionText = ""

                        #   //Increase Question Nos Starts
                        iCnt_L1 =1 if strSectionText != "" and strSubSectionText != "" and iCnt_L1 == 0  else iCnt_L1
                        if (iLvlCurr == 1): 
                            if (blnAlreadyIncreased == False):
                                iCnt_L1 +=1        
                        elif (iLvlCurr == 2):
                            iCnt_Section+=1
                        elif (iLvlCurr == 3): 
                            iCnt_SubSection+=1 
                        elif (iLvlCurr == 4):
                            iCnt_SubSubSection+=1
                        # //Increase Question Nos Ends 

                            
                        
                        if (iLvlCurr == 1):                  
                            strQNo = str(iCnt_L1 )
                        elif (iLvlCurr == 2): 
                            strQNo = str(iCnt_L1) + "." + str(iCnt_Section)
                        elif (iLvlCurr == 3): 
                            strQNo = str(iCnt_L1) + "." + str(iCnt_Section) + "." + str(iCnt_SubSection) 
                        elif (iLvlCurr == 4): 
                            strQNo = str(iCnt_L1) + "." +str( iCnt_Section) + "." + str(iCnt_SubSection) + "." + str(iCnt_SubSubSection)
                            
                        if i == 0:  
                            if(str(qtnResult['lvl'][i]) !="1"): 
                                d = {'Section_AID':str(qtnResult['Section_AID'][i]), 
                                'Section_Label':str(qtnResult['Section_Label'][i]), 
                                'Sub_Section_AID':iSubSecPrev, 
                                'Sub_Section_Label':"", 
                                'Sub_Sub_Section_AID':'', 
                                'Sub_Sub_Section_Label':'', 
                                'qtnNo':"",
                                'qtnsArr':'',
                                'lvl': str('->') } 
                                d2[arrayidx] = d
                                arrayidx+=1  

                        if(strSectionText!=""):
                            # dtFinalValues.Rows.Add(strSectionText, 
                            #                        strSubSectionText, 
                            #                        strSubSubSectionText, "", "", 
                            #                        iLvlCurr.ToString());
                            d = {'lvl': strLevelText,
                                        'Section_AID':iSecCurr, 
                                        'Section_Label':strSectionText, 
                                        'Sub_Section_AID':iSubSecPrev, 
                                        'Sub_Section_Label':strSubSectionText, 
                                        'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                        'Sub_Sub_Section_Label':strSubSubSectionText, 
                                        # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                        # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                        'qtnNo':str(strQNo).split('.')[0],
                                        'qtnsArr':"",
                                        'qtn_aid':"", 
                                        } 
                            d2[arrayidx] = d
                            arrayidx+=1  
                        elif (strSubSectionText != ""):
                            # dtFinalValues.Rows.Add(strSectionText, 
                            #                        strSubSectionText, 
                            #                        strSubSubSectionText, "", 
                            #                        strQNo.Split('.')[0], iLvlCurr.ToString());
                            d = {'lvl': strLevelText,
                                        'Section_AID':iSecCurr, 
                                        'Section_Label':strSectionText, 
                                        'Sub_Section_AID':iSubSecPrev, 
                                        'Sub_Section_Label':strSubSectionText, 
                                        'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                        'Sub_Sub_Section_Label':strSubSubSectionText, 
                                        # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                        # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                        'qtnNo':str(strQNo).split('.')[0],
                                        'qtnsArr':"",
                                        'qtn_aid':str(iQuesID), 
                                        } 
                            d2[arrayidx] = d
                            arrayidx+=1  
                        elif (strSubSubSectionText != ""):
                            # dtFinalValues.Rows.Add(strSectionText, strSubSectionText, 
                            #                        strSubSubSectionText, "", 
                            #                        strQNo.Split('.')[0] + "." + 
                            #                        strQNo.Split('.')[1], iLvlCurr.ToString());
                            d = {'lvl': strLevelText,
                                        'Section_AID':iSecCurr, 
                                        'Section_Label':strSectionText, 
                                        'Sub_Section_AID':iSubSecPrev, 
                                        'Sub_Section_Label':strSubSectionText, 
                                        'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                        'Sub_Sub_Section_Label':strSubSubSectionText, 
                                        # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                        # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                        'qtnNo':str(strQNo).split('.')[0]+ "." +str(strQNo).split('.')[1] ,
                                        'qtnsArr':"",
                                        'qtn_aid':str(iQuesID), 
                                        } 
                            d2[arrayidx] = d
                            arrayidx+=1  

                        # dtFinalValues.Rows.Add("", "", "", strLevelText + "    " + strQues, 
                        #                        strQNo, iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                        'Section_AID':iSecCurr, 
                                        'Section_Label':"", 
                                        'Sub_Section_AID':iSubSecPrev, 
                                        'Sub_Section_Label':"", 
                                        'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                        'Sub_Sub_Section_Label':"", 
                                        # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                        # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                        'qtnNo':str(strQNo)  ,
                                        'qtnsArr':strQues,
                                        'qtn_aid':str(iQuesID), 
                                            'Rating_Yes':qtnResult['Rating_Yes'][i],
                                            'Rating_No':qtnResult['Rating_No'][i],
                                            'NA':qtnResult['NA'][i],
                                        } 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    del qtnResult

                del tableResult
            return d2 # json.dumps(d2) 

    def Udaap_insertRatings(self,q_id,yes,no,doc_na):
        if(str(self.objdbops.getscalar("select count(*) from Udaap_Question_Rating where question_aid="+str(q_id)))=="0"):
            strQ="INSERT INTO  Udaap_Question_Rating \
            ( Question_AID \
            , Rating_Yes \
            , Rating_No \
            , NA \
            , AddDate  )\
                VALUES\
            ("+str(q_id) +"\
            ,"+str(yes)+"\
            ,"+str(no)+"\
            ,"+str(doc_na)+"\
            ,getdate() )"
            self.objdbops.insertRow(strQ)
        else:
            strQ="update Udaap_Question_Rating set Rating_Yes="+str(yes)+",Rating_No="+str(no)+",NA="+str(doc_na)+" where   question_aid="+str(q_id)
            self.objdbops.insertRow(strQ)

    def getUdaaptnSectionFinal(self):
        tableResult =self.objdbops.getTable("select distinct section_label,alloc.section_aid from Udaap_Sections udaap,Udaap_Allocation alloc where alloc.section_aid=udaap.section_aid order by  1 ")
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    
    def getUdaapQtnsFinal(self):
        d2 = {}
        strQ="select distinct a.* from("
        strQ += " select '1' lvl,Section_AID,Section_Label,'-' Sub_Section_AID,'-' Sub_Section_Label,"
        strQ += " '-' Sub_Sub_Section_AID,'-' Sub_Sub_Section_Label,'-' Sub_Sub_Sub_Section_AID,'-' Sub_Sub_Sub_Section_Label "     
        strQ += " from Udaap_Sections   )a  ,Udaap_Allocation alloc where alloc.section_aid=a.section_aid "# and a.section_aid='"+str(sectionid)+"'"
        strQ += " order by  a.Section_AID"
        tableResult =self.objdbops.getTable(strQ) 
        arrayidx=0 
        if tableResult.empty == False:
            for ind in tableResult.index: 
                strQtn=""
                strQtn+=" select Rating_Yes_NO ,Doc_Yes_No,isnull(comments,'')comments,case when  len(qtnmst.Section_AID )<>  0 and  (qtnmst.Sub_Section_AID) is null then 1 "
                strQtn+=" when  len(qtnmst.Sub_Section_AID)<>  0 and  (qtnmst.Sub_Sub_Section_AID) is null then 2"
                strQtn+=" when len(qtnmst.Sub_Sub_Section_AID)<>0 and  (qtnmst.Sub_Sub_Sub_Section_AID)  is null then 3 "
                strQtn+=" when len(qtnmst.Sub_Sub_Sub_Section_AID)<>  0 then 4  else 0 end lvl,  sec.Section_AID,isnull(s_sec.Sub_Section_AID,'0') Sub_Section_AID,"
                strQtn+=" isnull(ss_sec.Sub_Sub_Section_AID,'0') Sub_Sub_Section_AID,qtnmst.Question_AID ,"
                strQtn+=" qtnmst.Question_Label ,isnull(sec.Section_Label,'') Section_Label, isnull(s_sec.Sub_Section_Label,'') Sub_Section_Label,isnull(ss_sec.Sub_Sub_Section_Label,'') Sub_Sub_Section_Label    from "
                strQtn+=" Udaap_question_master qtnmst left join Udaap_Sections sec on "
                strQtn+=" qtnmst.section_aid=sec.section_aid left join"
                strQtn+=" Udaap_Sub_Sections s_sec  on qtnmst.sub_section_aid=s_sec.sub_section_aid left join"
                strQtn+=" Udaap_Sub_Sub_Sections ss_sec on qtnmst.sub_sub_section_aid=ss_sec.sub_sub_section_aid "
                strQtn+=" left join Udaap_Question_Rating_Data_Final on qtnmst.Question_aid=Udaap_Question_Rating_Data_Final.Question_AID	"
                strQtn+=" where sec.section_aid="+str(tableResult['Section_AID'][ind])+" "
                strQtn+=" order by qtnmst.Question_AID,qtnmst.section_aid"
                strQtn+=" ,cast(qtnmst.Sub_Section_AID as int),cast(qtnmst.Sub_Sub_Section_AID as int) " 
                qtnResult =self.objdbops.getTable(strQtn)                 
                print(strQtn)
                print("qtnResult",qtnResult)
                iLvlCurr=0
                iSecCurr=0
                iSubSecCurr=0
                iSubSubSecCurr=0
                iSubSubSecPrev=0
                iCnt_L1=0
                strQues=""
                strSectionText=""
                strSubSectionText=""
                strSubSubSectionText=""
                iQuesID=0
                iCnt_L1 = 0                #//Q No
                iCnt_Section = 0              # //Q No
                iCnt_SubSection = 0              #  //Q No
                iCnt_SubSubSection = 0              # //Q No 
                strQNo = ""  #//Q No
                blnAlreadyIncreased = False
                for i in qtnResult.index: 
                    blnAlreadyIncreased = False 
                    strLevelText = ""
                    iLvlCurr = int(qtnResult['lvl'][i])
                    iSecCurr = int(qtnResult['Section_AID'][i])
                    iSubSecCurr =int(qtnResult['Sub_Section_AID'][i])
                    iSubSubSecCurr =int(qtnResult['Sub_Sub_Section_AID'][i])
                   
                    
                    iQuesID=int(qtnResult['Question_AID'][i])

                    strQues = qtnResult["Question_Label"][i]
                    strSectionText = qtnResult["Section_Label"][i]
                    strSubSectionText = qtnResult["Sub_Section_Label"][i]
                    strSubSectionText = strSubSectionText.replace("-", "")
                    strSubSubSectionText =qtnResult["Sub_Sub_Section_Label"][i]

                    for j in range(iLvlCurr):
                        strLevelText += "->"

                    if (i == 0): 
                        iCnt_L1 = 0
                        iCnt_Section = 0
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0

                        iLvlPrev = iLvlCurr
                        iSecPrev = iSecCurr
                        iSubSecPrev = iSubSecCurr
                        iSubSubSecCurr = iSubSubSecPrev

                    if (i > 0 and iSecCurr != iSecPrev):
                        iSecPrev = iSecCurr
                        iCnt_L1 = 0
                        iCnt_Section = 0
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0
                    elif (i > 0):
                        strSectionText = ""

                    if (i > 0 and iSubSecCurr != iSubSecPrev):
                        iSubSecPrev = iSubSecCurr
                        if (strSectionText == ""):
                            blnAlreadyIncreased = True
                            iCnt_L1+=1
                        iCnt_Section = 0
                        iCnt_SubSection = 0    
                        iCnt_SubSubSection = 0 
                    elif (i > 0):
                        strSubSectionText = ""

                    if (i > 0 and iSubSubSecCurr>0 and iSubSubSecCurr != iSubSubSecPrev):
                        iSubSubSecPrev = iSubSubSecCurr
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0
                        iCnt_Section+=1
                    elif(i > 0 and iSubSubSecCurr > 0):
                        strSubSubSectionText = ""

                    #   //Increase Question Nos Starts
                    iCnt_L1 =1 if strSectionText != "" and strSubSectionText != "" and iCnt_L1 == 0  else iCnt_L1
                    if (iLvlCurr == 1): 
                        if (blnAlreadyIncreased == False):
                            iCnt_L1 +=1        
                    elif (iLvlCurr == 2):
                        iCnt_Section+=1
                    elif (iLvlCurr == 3): 
                        iCnt_SubSection+=1 
                    elif (iLvlCurr == 4):
                        iCnt_SubSubSection+=1
                    # //Increase Question Nos Ends 

                     
                   
                    if (iLvlCurr == 1):                  
                        strQNo = str(iCnt_L1 )
                    elif (iLvlCurr == 2): 
                        strQNo = str(iCnt_L1) + "." + str(iCnt_Section)
                    elif (iLvlCurr == 3): 
                        strQNo = str(iCnt_L1) + "." + str(iCnt_Section) + "." + str(iCnt_SubSection) 
                    elif (iLvlCurr == 4): 
                        strQNo = str(iCnt_L1) + "." +str( iCnt_Section) + "." + str(iCnt_SubSection) + "." + str(iCnt_SubSubSection)
                     
                    if i == 0:  
                        if(str(qtnResult['lvl'][i]) !="1"): 
                            d = {'Section_AID':str(qtnResult['Section_AID'][i]), 
                            'Section_Label':str(qtnResult['Section_Label'][i]), 
                            'Sub_Section_AID':iSubSecPrev, 
                            'Sub_Section_Label':"", 
                            'Sub_Sub_Section_AID':'', 
                            'Sub_Sub_Section_Label':'', 
                            'qtnNo':"",
                            'qtnsArr':'',
                            'lvl': str('->') } 
                            d2[arrayidx] = d
                            arrayidx+=1  

                    if(strSectionText!=""):
                        # dtFinalValues.Rows.Add(strSectionText, 
                        #                        strSubSectionText, 
                        #                        strSubSubSectionText, "", "", 
                        #                        iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0],
                                    'qtnsArr':"",
                                    'qtn_aid':"",
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i]
                                    # ,
                                    # 'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                    # 'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                    # 'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                    # 'Control_Description':qtnResult['Control_Description'][i],
                                    # 'override_residual_ratings':qtnResult['override_residual_ratings'][i],
                                    # 'override_comments':qtnResult['override_comments'][i]
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    elif (strSubSectionText != ""):
                        # dtFinalValues.Rows.Add(strSectionText, 
                        #                        strSubSectionText, 
                        #                        strSubSubSectionText, "", 
                        #                        strQNo.Split('.')[0], iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0],
                                    'qtnsArr':"",
                                    'qtn_aid':str(iQuesID),
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i]
                                # ,
                                #     'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                #     'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                #     'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                #     'Control_Description':qtnResult['Control_Description'][i],
                                #     'override_residual_ratings':qtnResult['override_residual_ratings'][i],
                                #     'override_comments':qtnResult['override_comments'][i]
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    elif (strSubSubSectionText != ""):
                        # dtFinalValues.Rows.Add(strSectionText, strSubSectionText, 
                        #                        strSubSubSectionText, "", 
                        #                        strQNo.Split('.')[0] + "." + 
                        #                        strQNo.Split('.')[1], iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0]+ "." +str(strQNo).split('.')[1] ,
                                    'qtnsArr':"",
                                    'qtn_aid':str(iQuesID),
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i]
                                    # ,
                                    # 'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                    # 'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                    # 'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                    # 'Control_Description':qtnResult['Control_Description'][i],
                                    # 'override_residual_ratings':qtnResult['override_residual_ratings'][i],
                                    # 'override_comments':qtnResult['override_comments'][i]
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  

                    # dtFinalValues.Rows.Add("", "", "", strLevelText + "    " + strQues, 
                    #                        strQNo, iLvlCurr.ToString());
                    d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':"", 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':"", 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':"", 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo)  ,
                                    'qtnsArr':strQues,
                                    'qtn_aid':str(iQuesID),
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i]
                                    # ,
                                    # 'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                    # 'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                    # 'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                    # 'Control_Description':qtnResult['Control_Description'][i],
                                    # 'override_residual_ratings':qtnResult['override_residual_ratings'][i],
                                    # 'override_comments':qtnResult['override_comments'][i]
                                    } 
                    d2[arrayidx] = d
                    arrayidx+=1  
                del qtnResult
        
            del tableResult 
        return d2 # json.dumps(d2)    

    def UdaapcanUpdateRatings(self,uid):
        return str(self.objdbops.getscalar("select count(*) from [Udaap_Question_Rating_Data] where [Review_id] in ( \
                                        select max(FLS_AID) review_id from  Udaap_Setting) and addedby='"+str(uid).replace("'","''")+"'"))  

    def getUdaapQtnSection(self,id):
        tableResult =self.objdbops.getTable("select distinct section_label,alloc.section_aid from Udaap_Sections udaap,Udaap_Allocation alloc where alloc.section_aid=udaap.section_aid and Allocated_to ='"+str(id).replace("'","''")+"' order by  1 ")
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)  
    
    def getUdaapQtns(self,sectionid):
        d2 = {}
        strQ="select distinct a.* from("
        strQ += " select '1' lvl,Section_AID,Section_Label,'-' Sub_Section_AID,'-' Sub_Section_Label,"
        strQ += " '-' Sub_Sub_Section_AID,'-'     Sub_Sub_Section_Label,'-' Sub_Sub_Sub_Section_AID,'-' Sub_Sub_Sub_Section_Label "     
        strQ += " from Udaap_Sections" 
        strQ += " )a ,Udaap_Allocation alloc where alloc.section_aid=a.section_aid  and alloc.allocated_to='"+str(sectionid).replace("'","''")+"'"
        strQ += " order by  a.Section_AID"#,cast(a.Sub_Section_AID as int),cast(a.Sub_Sub_Section_AID as int),cast(a.Sub_Sub_Sub_Section_AID as int)"
        print("Strq------",strQ) 
        tableResult =self.objdbops.getTable(strQ)
        print("tableResult",tableResult) 
        arrayidx=0 
        if tableResult.empty == False:
            for ind in tableResult.index: 
                strQtn=""
                strQtn+=" select Rating_Yes_NO ,Doc_Yes_No, Inherent_Risk_Rating,Control_Effectiveness_Ratings,Residual_Ratings,Control_Description,override_residual_ratings,override_comments,isnull(comments,'')comments,case when  len(qtnmst.Section_AID )<>  0 and  (qtnmst.Sub_Section_AID) is null then 1 "
                strQtn+=" when  len(qtnmst.Sub_Section_AID)<>  0 and  (qtnmst.Sub_Sub_Section_AID) is null then 2"
                strQtn+=" when len(qtnmst.Sub_Sub_Section_AID)<>0 and  (qtnmst.Sub_Sub_Sub_Section_AID)  is null then 3 "
                strQtn+=" when len(qtnmst.Sub_Sub_Sub_Section_AID)<>  0 then 4  else 0 end lvl,  sec.Section_AID,isnull(s_sec.Sub_Section_AID,'0') Sub_Section_AID,"
                strQtn+=" isnull(ss_sec.Sub_Sub_Section_AID,'0') Sub_Sub_Section_AID,qtnmst.Question_AID ,"
                strQtn+=" qtnmst.Question_Label ,isnull(sec.Section_Label,'') Section_Label, isnull(s_sec.Sub_Section_Label,'') Sub_Section_Label,isnull(ss_sec.Sub_Sub_Section_Label,'') Sub_Sub_Section_Label    from "
                strQtn+=" Udaap_question_master qtnmst left join Udaap_Sections sec on "
                strQtn+=" qtnmst.section_aid=sec.section_aid left join"
                strQtn+=" Udaap_Sub_Sections s_sec  on qtnmst.sub_section_aid=s_sec.sub_section_aid left join"
                strQtn+=" Udaap_Sub_Sub_Sections ss_sec on qtnmst.sub_sub_section_aid=ss_sec.sub_sub_section_aid "
                strQtn+=" left join Udaap_Question_Rating_Data   on qtnmst.Question_aid=Udaap_Question_Rating_Data.question_aid	"
                strQtn+=" where sec.section_aid="+str(tableResult['Section_AID'][ind]).replace("'","''")+" "
                strQtn+=" order by   qtnmst.Question_AID,qtnmst.section_aid"
                strQtn+=" ,cast(qtnmst.Sub_Section_AID as int),cast(qtnmst.Sub_Sub_Section_AID as int) " 
                qtnResult =self.objdbops.getTable(strQtn) 
                           
               
                qtnNo=0 
                iLvlCurr=0
                iSecCurr=0
                iSubSecCurr=0
                iSubSubSecCurr=0
                iSubSubSecPrev=0
                iCnt_L1=0
                strQues=""
                strSectionText=""
                strSubSectionText=""
                strSubSubSectionText=""
                iQuesID=0
                iCnt_L1 = 0                #//Q No
                iCnt_Section = 0              # //Q No
                iCnt_SubSection = 0              #  //Q No
                iCnt_SubSubSection = 0              # //Q No 
                strQNo = ""  #//Q No
                blnAlreadyIncreased = False
                for i in qtnResult.index: 
                    blnAlreadyIncreased = False 
                    strLevelText = ""
                    iLvlCurr = int(qtnResult['lvl'][i])
                    iSecCurr = int(qtnResult['Section_AID'][i])
                    iSubSecCurr =int(qtnResult['Sub_Section_AID'][i])
                    iSubSubSecCurr =int(qtnResult['Sub_Sub_Section_AID'][i])
                   
                    
                    iQuesID=int(qtnResult['Question_AID'][i])

                    strQues = qtnResult["Question_Label"][i]
                    strSectionText = qtnResult["Section_Label"][i]
                    strSubSectionText = qtnResult["Sub_Section_Label"][i]
                    strSubSectionText = strSubSectionText.replace("-", "")
                    strSubSubSectionText =qtnResult["Sub_Sub_Section_Label"][i]

                    for j in range(iLvlCurr):
                        strLevelText += "->"

                    if (i == 0): 
                        iCnt_L1 = 0
                        iCnt_Section = 0
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0

                        iLvlPrev = iLvlCurr
                        iSecPrev = iSecCurr
                        iSubSecPrev = iSubSecCurr
                        iSubSubSecCurr = iSubSubSecPrev

                    if (i > 0 and iSecCurr != iSecPrev):
                        iSecPrev = iSecCurr
                        iCnt_L1 = 0
                        iCnt_Section = 0
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0
                    elif (i > 0):
                        strSectionText = ""

                    if (i > 0 and iSubSecCurr != iSubSecPrev):
                        iSubSecPrev = iSubSecCurr
                        if (strSectionText == ""):
                            blnAlreadyIncreased = True
                            iCnt_L1+=1
                        iCnt_Section = 0
                        iCnt_SubSection = 0    
                        iCnt_SubSubSection = 0 
                    elif (i > 0):
                        strSubSectionText = ""

                    if (i > 0 and iSubSubSecCurr>0 and iSubSubSecCurr != iSubSubSecPrev):
                        iSubSubSecPrev = iSubSubSecCurr
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0
                        iCnt_Section+=1
                    elif(i > 0 and iSubSubSecCurr > 0):
                        strSubSubSectionText = ""

                    #   //Increase Question Nos Starts
                    iCnt_L1 =1 if strSectionText != "" and strSubSectionText != "" and iCnt_L1 == 0  else iCnt_L1
                    if (iLvlCurr == 1): 
                        if (blnAlreadyIncreased == False):
                            iCnt_L1 +=1        
                    elif (iLvlCurr == 2):
                        iCnt_Section+=1
                    elif (iLvlCurr == 3): 
                        iCnt_SubSection+=1 
                    elif (iLvlCurr == 4):
                        iCnt_SubSubSection+=1
                    # //Increase Question Nos Ends 

                     
                   
                    if (iLvlCurr == 1):                  
                        strQNo = str(iCnt_L1 )
                    elif (iLvlCurr == 2): 
                        strQNo = str(iCnt_L1) + "." + str(iCnt_Section)
                    elif (iLvlCurr == 3): 
                        strQNo = str(iCnt_L1) + "." + str(iCnt_Section) + "." + str(iCnt_SubSection) 
                    elif (iLvlCurr == 4): 
                        strQNo = str(iCnt_L1) + "." +str( iCnt_Section) + "." + str(iCnt_SubSection) + "." + str(iCnt_SubSubSection)
                     
                    if i == 0:  
                        if(str(qtnResult['lvl'][i]) !="1"): 
                            d = {'Section_AID':str(qtnResult['Section_AID'][i]), 
                            'Section_Label':str(qtnResult['Section_Label'][i]), 
                            'Sub_Section_AID':iSubSecPrev, 
                            'Sub_Section_Label':"", 
                            'Sub_Sub_Section_AID':'', 
                            'Sub_Sub_Section_Label':'', 
                            'qtnNo':"",
                            'qtnsArr':'',
                            'lvl': str('->') } 
                            d2[arrayidx] = d
                            arrayidx+=1  

                    if(strSectionText!=""):
                        # dtFinalValues.Rows.Add(strSectionText, 
                        #                        strSubSectionText, 
                        #                        strSubSubSectionText, "", "", 
                        #                        iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0],
                                    'qtnsArr':"",
                                    'qtn_aid':"",
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],
                                    'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],
                                    'comments':qtnResult['comments'][i],
                                    'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                    'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                    'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                    'Control_Description':qtnResult['Control_Description'][i],
                                    'override_residual_ratings':qtnResult['override_residual_ratings'][i],
                                    'override_comments':qtnResult['override_comments'][i]
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    elif (strSubSectionText != ""):
                        # dtFinalValues.Rows.Add(strSectionText, 
                        #                        strSubSectionText, 
                        #                        strSubSubSectionText, "", 
                        #                        strQNo.Split('.')[0], iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0],
                                    'qtnsArr':"",
                                    'qtn_aid':str(iQuesID),
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i],
                                    'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                    'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                    'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                    'Control_Description':qtnResult['Control_Description'][i],
                                    'override_residual_ratings':qtnResult['override_residual_ratings'][i],
                                    'override_comments':qtnResult['override_comments'][i]
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    elif (strSubSubSectionText != ""):
                        # dtFinalValues.Rows.Add(strSectionText, strSubSectionText, 
                        #                        strSubSubSectionText, "", 
                        #                        strQNo.Split('.')[0] + "." + 
                        #                        strQNo.Split('.')[1], iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0]+ "." +str(strQNo).split('.')[1] ,
                                    'qtnsArr':"",
                                    'qtn_aid':str(iQuesID),
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i],
                                    'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                    'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                    'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                    'Control_Description':qtnResult['Control_Description'][i],
                                    'override_residual_ratings':qtnResult['override_residual_ratings'][i],
                                    'override_comments':qtnResult['override_comments'][i]
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  

                    # dtFinalValues.Rows.Add("", "", "", strLevelText + "    " + strQues, 
                    #                        strQNo, iLvlCurr.ToString());
                    d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':"", 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':"", 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':"", 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo)  ,
                                    'qtnsArr':strQues,
                                    'qtn_aid':str(iQuesID),
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i],
                                    'Inherent_Risk_Rating':qtnResult['Inherent_Risk_Rating'][i],
                                    'Control_Effectiveness_Ratings':qtnResult['Control_Effectiveness_Ratings'][i],
                                    'Residual_Ratings':qtnResult['Residual_Ratings'][i],
                                    'Control_Description':qtnResult['Control_Description'][i],
                                    'override_residual_ratings':qtnResult['override_residual_ratings'][i],
                                    'override_comments':qtnResult['override_comments'][i]
                                    } 
                    d2[arrayidx] = d
                    arrayidx+=1  
                del qtnResult
        
            del tableResult   
        print("d2 " ,d2)
        return d2 # json.dumps(d2)  
    
    def getUdaapModels(self,id):
        tableResult =self.objdbops.getTable("select distinct Model_Id from Udaap_Allocation where Allocated_to ="+str(id).replace("'","''")+" order by  1 ")
       
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    
    def publishUdaap(self):
        maxid=   str(self.objdbops.getscalar("select max(FLS_AID) review_id from  Udaap_Setting"))
        self.objdbops.insertRow("update Udaap_Setting set publish=1 where FLS_AID="+maxid.replace("'","''"))

    
    def getAllUdaapQtns(self):
        d2 = {}
        strQ="select a.* from("
        strQ += " select '1' lvl,Section_AID,Section_Label,'-' Sub_Section_AID,'-' Sub_Section_Label,"
        strQ += " '-' Sub_Sub_Section_AID,'-' Sub_Sub_Section_Label,'-' Sub_Sub_Sub_Section_AID,'-' Sub_Sub_Sub_Section_Label "     
        strQ += " from Udaap_Sections   "         
        strQ += " )a  order by  a.Section_AID"#,cast(a.Sub_Section_AID as int),cast(a.Sub_Sub_Section_AID as int),cast(a.Sub_Sub_Sub_Section_AID as int)"
        tableResult =self.objdbops.getTable(strQ) 
        
        arrayidx=0 
        if tableResult.empty == False:
            for ind in tableResult.index: 
                # print(tableResult['Section_AID'][ind],tableResult['Sub_Section_AID'][ind], tableResult['Sub_Sub_Section_AID'][ind], tableResult['Sub_Sub_Sub_Section_AID'][ind])
                # strQtn=" select qtnmst.Question_AID,qtnmst.Question_Label,Rating_Yes_NO ,Doc_Yes_No,isnull(comments,'')comments from icq_question_master qtnmst left join ICQ_Question_Rating_Data_Final "
                # strQtn+="     on qtnmst.Question_aid=ICQ_Question_Rating_Data_Final.question_aid where section_aid='"+str(tableResult['Section_AID'][ind])+"'  and isnull(Sub_Section_AID,'-') ='"+str(tableResult['Sub_Section_AID'][ind]) +"' and "
                # strQtn+=" isnull(Sub_Sub_Section_AID,'-')= '"+str(tableResult['Sub_Sub_Section_AID'][ind])+"' and isnull(Sub_Sub_Sub_Section_AID,'-')='"+str(tableResult['Sub_Sub_Sub_Section_AID'][ind]) +"' "
                # strQtn+=" order by qtnmst.Question_AID,cast(Sub_Section_AID as int),cast(Sub_Sub_Section_AID as int),cast(Sub_Sub_Sub_Section_AID as int)"
                strQtn=""
                strQtn+=" select case when  len(qtnmst.Section_AID )<>  0 and  (qtnmst.Sub_Section_AID) is null then 1 "
                strQtn+=" when  len(qtnmst.Sub_Section_AID)<>  0 and  (qtnmst.Sub_Sub_Section_AID) is null then 2"
                strQtn+=" when len(qtnmst.Sub_Sub_Section_AID)<>0 and  (qtnmst.Sub_Sub_Sub_Section_AID)  is null then 3 "
                strQtn+=" when len(qtnmst.Sub_Sub_Sub_Section_AID)<>  0 then 4  else 0 end lvl,  sec.Section_AID,isnull(s_sec.Sub_Section_AID,'0') Sub_Section_AID,"
                strQtn+=" isnull(ss_sec.Sub_Sub_Section_AID,'0') Sub_Sub_Section_AID,Question_AID ,"
                strQtn+=" qtnmst.Question_Label ,isnull(sec.Section_Label,'') Section_Label, isnull(s_sec.Sub_Section_Label,'') Sub_Section_Label,isnull(ss_sec.Sub_Sub_Section_Label,'') Sub_Sub_Section_Label    from "
                strQtn+=" Udaap_Question_Master qtnmst left join Udaap_Sections sec on "
                strQtn+=" qtnmst.section_aid=sec.section_aid left join"
                strQtn+=" Udaap_Sub_Sections s_sec  on qtnmst.sub_section_aid=s_sec.sub_section_aid left join"
                strQtn+=" Udaap_Sub_Sub_Sections ss_sec on qtnmst.sub_sub_section_aid=ss_sec.sub_sub_section_aid "
                strQtn+=" where sec.section_aid="+str(tableResult['Section_AID'][ind])+" "
                strQtn+=" order by   Question_AID,qtnmst.section_aid"
                strQtn+=" ,cast(qtnmst.Sub_Section_AID as int),cast(qtnmst.Sub_Sub_Section_AID as int) " 
                qtnResult =self.objdbops.getTable(strQtn)                 
                iLvlCurr=0
                iSecCurr=0
                iSubSecCurr=0
                iSubSubSecCurr=0
                iSubSubSecPrev=0
                iCnt_L1=0
                strQues=""
                strSectionText=""
                strSubSectionText=""
                strSubSubSectionText=""
                iQuesID=0
                iCnt_L1 = 0                #//Q No
                iCnt_Section = 0              # //Q No
                iCnt_SubSection = 0              #  //Q No
                iCnt_SubSubSection = 0              # //Q No 
                strQNo = ""  #//Q No
                blnAlreadyIncreased = False
                for i in qtnResult.index: 
                    blnAlreadyIncreased = False 
                    strLevelText = ""
                    iLvlCurr = int(qtnResult['lvl'][i])
                    iSecCurr = int(qtnResult['Section_AID'][i])
                    iSubSecCurr =int(qtnResult['Sub_Section_AID'][i])
                    iSubSubSecCurr =int(qtnResult['Sub_Sub_Section_AID'][i])
                   
                    
                    iQuesID=int(qtnResult['Question_AID'][i])

                    strQues = qtnResult["Question_Label"][i]
                    strSectionText = qtnResult["Section_Label"][i]
                    strSubSectionText = qtnResult["Sub_Section_Label"][i]
                    strSubSectionText = strSubSectionText.replace("-", "")
                    strSubSubSectionText =qtnResult["Sub_Sub_Section_Label"][i]

                    for j in range(iLvlCurr):
                        strLevelText += "->"

                    if (i == 0): 
                        iCnt_L1 = 0
                        iCnt_Section = 0
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0

                        iLvlPrev = iLvlCurr
                        iSecPrev = iSecCurr
                        iSubSecPrev = iSubSecCurr
                        iSubSubSecCurr = iSubSubSecPrev

                    if (i > 0 and iSecCurr != iSecPrev):
                        iSecPrev = iSecCurr
                        iCnt_L1 = 0
                        iCnt_Section = 0
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0
                    elif (i > 0):
                        strSectionText = ""

                    if (i > 0 and iSubSecCurr != iSubSecPrev):
                        iSubSecPrev = iSubSecCurr
                        if (strSectionText == ""):
                            blnAlreadyIncreased = True
                            iCnt_L1+=1
                        iCnt_Section = 0
                        iCnt_SubSection = 0    
                        iCnt_SubSubSection = 0 
                    elif (i > 0):
                        strSubSectionText = ""

                    if (i > 0 and iSubSubSecCurr>0 and iSubSubSecCurr != iSubSubSecPrev):
                        iSubSubSecPrev = iSubSubSecCurr
                        iCnt_SubSection = 0
                        iCnt_SubSubSection = 0
                        iCnt_Section+=1
                    elif(i > 0 and iSubSubSecCurr > 0):
                        strSubSubSectionText = ""

                    #   //Increase Question Nos Starts
                    iCnt_L1 =1 if strSectionText != "" and strSubSectionText != "" and iCnt_L1 == 0  else iCnt_L1
                    if (iLvlCurr == 1): 
                        if (blnAlreadyIncreased == False):
                            iCnt_L1 +=1        
                    elif (iLvlCurr == 2):
                        iCnt_Section+=1
                    elif (iLvlCurr == 3): 
                        iCnt_SubSection+=1 
                    elif (iLvlCurr == 4):
                        iCnt_SubSubSection+=1
                    # //Increase Question Nos Ends 

                     
                   
                    if (iLvlCurr == 1):                  
                        strQNo = str(iCnt_L1 )
                    elif (iLvlCurr == 2): 
                        strQNo = str(iCnt_L1) + "." + str(iCnt_Section)
                    elif (iLvlCurr == 3): 
                        strQNo = str(iCnt_L1) + "." + str(iCnt_Section) + "." + str(iCnt_SubSection) 
                    elif (iLvlCurr == 4): 
                        strQNo = str(iCnt_L1) + "." +str( iCnt_Section) + "." + str(iCnt_SubSection) + "." + str(iCnt_SubSubSection)
                     
                    if i == 0:  
                        if(str(qtnResult['lvl'][i]) !="1"): 
                            d = {'Section_AID':str(qtnResult['Section_AID'][i]), 
                            'Section_Label':str(qtnResult['Section_Label'][i]), 
                            'Sub_Section_AID':iSubSecPrev, 
                            'Sub_Section_Label':"", 
                            'Sub_Sub_Section_AID':'', 
                            'Sub_Sub_Section_Label':'', 
                            'qtnNo':"",
                            'qtnsArr':'',
                            'lvl': str('->') } 
                            d2[arrayidx] = d
                            arrayidx+=1  

                    if(strSectionText!=""):
                        # dtFinalValues.Rows.Add(strSectionText, 
                        #                        strSubSectionText, 
                        #                        strSubSubSectionText, "", "", 
                        #                        iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0],
                                    'qtnsArr':"",
                                    'qtn_aid':"", 
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    elif (strSubSectionText != ""):
                        # dtFinalValues.Rows.Add(strSectionText, 
                        #                        strSubSectionText, 
                        #                        strSubSubSectionText, "", 
                        #                        strQNo.Split('.')[0], iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0],
                                    'qtnsArr':"",
                                    'qtn_aid':str(iQuesID), 
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    elif (strSubSubSectionText != ""):
                        # dtFinalValues.Rows.Add(strSectionText, strSubSectionText, 
                        #                        strSubSubSectionText, "", 
                        #                        strQNo.Split('.')[0] + "." + 
                        #                        strQNo.Split('.')[1], iLvlCurr.ToString());
                        d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':strSectionText, 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':strSubSectionText, 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':strSubSubSectionText, 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo).split('.')[0]+ "." +str(strQNo).split('.')[1] ,
                                    'qtnsArr':"",
                                    'qtn_aid':str(iQuesID), 
                                    } 
                        d2[arrayidx] = d
                        arrayidx+=1  

                    # dtFinalValues.Rows.Add("", "", "", strLevelText + "    " + strQues, 
                    #                        strQNo, iLvlCurr.ToString());
                    d = {'lvl': strLevelText,
                                    'Section_AID':iSecCurr, 
                                    'Section_Label':"", 
                                    'Sub_Section_AID':iSubSecPrev, 
                                    'Sub_Section_Label':"", 
                                    'Sub_Sub_Section_AID':iSubSubSecPrev, 
                                    'Sub_Sub_Section_Label':"", 
                                    # 'Sub_Sub_Sub_Section_AID':str(qtnResult['Sub_Sub_Sub_Section_AID'][ind]), 
                                    # 'Sub_Sub_Sub_Section_Label':qtnResult['Sub_Sub_Sub_Section_Label'][ind],
                                    'qtnNo':str(strQNo)  ,
                                    'qtnsArr':strQues,
                                    'qtn_aid':str(iQuesID), 
                                    } 
                    d2[arrayidx] = d
                    arrayidx+=1  
                del qtnResult
        
            del tableResult
        return d2 # json.dumps(d2)    
    
    def getUdaapSections(self):
        tableResult =self.objdbops.getTable("select  Section_Label , Section_AID  from  Udaap_Sections order by  Section_AID ")
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)

    def getUdaapSub_Sections(self,id):
        tableResult =self.objdbops.getTable("select  Sub_Section_Label , Sub_Section_AID  from  Udaap_Sub_Sections where Section_AID="+str(id)+" order by  Sub_Section_AID ")
        print("tableResult ",tableResult)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    
    def getUdaapSub_Sub_Sections(self,id):
        tableResult =self.objdbops.getTable("select  Sub_Sub_Section_Label , Sub_Sub_Section_AID  from  Udaap_Sub_Sub_Sections where Sub_Section_AID="+str(id).replace("'","''")+" order by  Sub_Section_AID ")
        print("tableResult ",tableResult)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    
    def getUdaapSub_Sub_Sub_Sections(self,id):
        tableResult =self.objdbops.getTable("select  Sub_Sub_Sub_Section_Label , Sub_Sub_Sub_Section_AID  from  Udaap_Sub_Sub_Sub_Sections where Sub_Sub_Section_AID="+str(id).replace("'","''")+" order by  Sub_Sub_Section_AID ")
        print("tableResult ",tableResult)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    

    def getUdaapIds(self):
        tableResult =self.objdbops.getTable("select max(FLS_AID) review_id,FLS_text review_name from  Udaap_Setting group by FLS_text")
       
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
