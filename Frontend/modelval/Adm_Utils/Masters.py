from modelval.DAL.dboperations import dbops
from modelval.models import *  
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
        strQ+=" join User_Category uc on  sub.uc_aid=uc.uc_aid where sub.AddedBy='"+UId+"'"
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
    
      
    def insertFunctionOption(self,opt,desc,tbl,activests,userId,category):
        print("self,opt,desc,tbl,activests,userId,category",opt,desc,tbl,activests,userId,category)
        if(tbl=="1"):
            strQ="insert into Model_Function_Master ("
            strQ += " Mdl_Fncn_Label   ,"
            strQ += " Mdl_Fncn_Description  ,"
            strQ += " ActiveStatus ,"
            strQ += " AddedBy    ,"
            strQ += " AddDate  )"
            strQ += " values("
            strQ += " '"+opt+"'   ,"
            strQ += " '"+desc+"'  ,"
            strQ += " '"+activests+"' ,"
            strQ += " '"+userId +"'    ,"
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
            strQ += " '"+opt+"'   ,"
            strQ += " '"+desc+"'  ,"
            strQ += " '"+activests+"' ,"
            strQ += " '"+userId +"'    ,"
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
            strQ += " '"+opt+"'   ,"
            strQ += " '"+desc+"'  ,"
            strQ += " '"+activests+"' ,"
            strQ += " '"+userId +"'    ,"
            strQ += " GETDATE()  )	 "
            self.objdbops.insertRow(strQ) 
        elif(tbl=="4"):
            strQ="insert into Prd_Addr_Master ("
            strQ += " Prd_Addr_Label   ,"
            strQ += " Prd_Addr_Description  ,"
            strQ += " ActiveStatus ,"
            strQ += " AddedBy    ,"
            strQ += " AddDate    ,"
            strQ += " category_aid   )"
            strQ += " values("
            strQ += " '"+opt+"'   ,"
            strQ += " '"+desc+"'  ,"
            strQ += " '"+activests+"' ,"
            strQ += " '"+userId +"'    ,"
            strQ += " GETDATE()	 ,"
            strQ += str(category) + ")"
            
            self.objdbops.insertRow(strQ)  
        elif(tbl=="5"):
            strQ="insert into Model_Use_Freq_Master ("
            strQ += " Mdl_Use_Freq_Label   ,"
            strQ += " Mdl_Use_Freq_Description  ,"
            strQ += " ActiveStatus ,"
            strQ += " AddedBy    ,"
            strQ += " AddDate  )"
            strQ += " values("
            strQ += " '"+opt+"'   ,"
            strQ += " '"+desc+"'  ,"
            strQ += " '"+activests+"' ,"
            strQ += " '"+userId +"'    ,"
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
            strQ += " '"+opt+"'   ,"
            strQ += " '"+desc+"'  ,"
            strQ += " '"+activests+"' ,"
            strQ += " '"+userId +"'    ,"
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
            strQ += " '"+opt+"'   ,"
            strQ += " '"+desc+"'  ,"
            strQ += " '"+activests+"' ,"
            strQ += " '"+userId +"'    ,"
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
            strQ += " '"+opt+"'   ,"
            strQ += " '"+desc+"'  ,"
            strQ += " '"+activests+"' ,"
            strQ += " '"+userId +"'    ,"
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
            strQ += " '"+opt+"'   ,"
            strQ += " '"+desc+"'  ,"
            strQ += " '"+activests+"' ,"
            strQ += " '"+userId +"'    ,"
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
            strQ += " '"+opt+"'   ,"
            strQ += " '"+desc+"'  ,"
            strQ += " '"+activests+"' ,"
            strQ += " '"+userId +"'    ,"
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
            strQ += " '"+opt+"'   ,"
            strQ += " '"+desc+"'  ,"
            strQ += " '"+activests+"' ,"
            strQ += " '"+userId +"'    ,"
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
            strQ += " '"+opt+"'   ,"
            strQ += " '"+desc+"'  ,"
            strQ += " '"+activests+"' ,"
            strQ += " '"+userId +"'    ,"
            strQ += " GETDATE()  )	 "
            self.objdbops.insertRow(strQ)   

    def updateFunctionOption(self,optId,opt,desc,tbl,activests,userId):
        if(tbl=="1"):
            strQ="update Model_Function_Master set" 
            strQ += " Mdl_Fncn_Description = '"+desc+"'  ,"
            strQ += " ActiveStatus ='"+activests+"' ,"
            strQ += " UpdatedBy = '"+userId +"'  ,"
            strQ += " UpdateDate =GETDATE()  "   
            strQ += " where Mdl_Fncn_AID='"+optId +"' "
            self.objdbops.insertRow(strQ)
        elif(tbl=="2"):
            strQ="update Model_Source_Master set" 
            strQ += " Mdl_Src_Description = '"+desc+"'  ,"
            strQ += " ActiveStatus ='"+activests+"' ,"
            strQ += " UpdatedBy = '"+userId +"'  ,"
            strQ += " UpdateDate =GETDATE()  "  
            strQ += " where Mdl_Scr_AID='"+optId +"' "
            self.objdbops.insertRow(strQ) 
        elif(tbl=="3"):
            strQ=" update Model_Type_Master set" 
            strQ += " Mdl_Type_Description = '"+desc+"'  ,"
            strQ += " ActiveStatus ='"+activests+"' ,"
            strQ += " UpdatedBy = '"+userId +"'  ,"
            strQ += " UpdateDate =GETDATE()  "  
            strQ += " where Mdl_Type_AID='"+optId +"' "
            self.objdbops.insertRow(strQ) 
        elif(tbl=="4"):
            print("44444",activests)
            strQ="update Prd_Addr_Master set " 
            strQ += " Prd_Addr_Description  = '"+desc+"'  ,"
            strQ += " ActiveStatus ='"+activests+"' ,"
            strQ += " UpdatedBy = '"+userId +"'  ,"
            strQ += " UpdateDate =GETDATE()  "  
            strQ += " where Prd_Addr_AID='"+optId +"' "
            self.objdbops.insertRow(strQ)  
        elif(tbl=="5"):
            strQ="update Model_Use_Freq_Master set " 
            strQ += " Mdl_Use_Freq_Description  = '"+desc+"'  ,"
            strQ += " ActiveStatus ='"+activests+"' ,"
            strQ += " UpdatedBy = '"+userId +"'  ,"
            strQ += " UpdateDate =GETDATE()  "  
            strQ += " where Mdl_Use_Freq_AID='"+optId +"' "
            self.objdbops.insertRow(strQ)   
        elif(tbl=="6"):
            strQ="update Mdl_Risk_Master set " 
            strQ += " Mdl_Risk_Description  = '"+desc+"'  ,"
            strQ += " ActiveStatus  ='"+activests+"' ,"
            strQ += " UpdatedBy = '"+userId +"'  ,"
            strQ += " UpdateDate =GETDATE()  "  
            strQ += " where Mdl_Risk_AID='"+optId +"' "
            self.objdbops.insertRow(strQ)   
        elif(tbl=="7"):
            strQ="update Intrinsic_Master set " 
            strQ += " Intrinsic_Description= '"+desc+"'  ," 
            strQ += " ActiveStatus ='"+activests+"' ,"
            strQ += " UpdatedBy = '"+userId +"'  ,"
            strQ += " UpdateDate =GETDATE()  "  
            strQ += " where Intrinsic_AID='"+optId +"' "
            self.objdbops.insertRow(strQ)    
        elif(tbl=="9"):
            strQ="update Materiality_Master set " 
            strQ += " Materiality_Description  = '"+desc+"'  ," 
            strQ += " ActiveStatus ='"+activests+"' ,"
            strQ += " UpdatedBy = '"+userId +"'  ,"
            strQ += " UpdateDate =GETDATE()  "  
            strQ += " where Materiality_AID='"+optId +"' "
            self.objdbops.insertRow(strQ)   
        elif(tbl=="8"):
            strQ="update Reliance_Master set " 
            strQ += " Reliance_Description= '"+desc+"'  ," 
            strQ += " ActiveStatus ='"+activests+"' ,"
            strQ += " UpdatedBy = '"+userId +"'  ,"
            strQ += " UpdateDate =GETDATE()  "  
            strQ += " where Reliance_AID='"+optId +"' "
            self.objdbops.insertRow(strQ)    
        elif(tbl=="10"):
            strQ="update into Mdl_Upstream set " 
            strQ += " Mdl_Upstream_Description = '"+desc+"'  ," 
            strQ += " ActiveStatus ='"+activests+"' ,"
            strQ += " UpdatedBy = '"+userId +"'  ,"
            strQ += " UpdateDate =GETDATE()  "  
            strQ += " where Mdl_Upstream_AID='"+optId +"' "
            self.objdbops.insertRow(strQ) 
        elif(tbl=="11"):
            strQ="update into Mdl_Dwstream set " 
            strQ += " Mdl_Dwstream_Description = '"+desc+"'  ," 
            strQ += " ActiveStatus ='"+activests+"' ,"
            strQ += " UpdatedBy = '"+userId +"'  ,"
            strQ += " UpdateDate =GETDATE()  "  
            strQ += " where Mdl_Dwstream_AID='"+optId +"' "
            self.objdbops.insertRow(strQ)  
        elif(tbl=="12"):
            strQ="update into Mdl_Montr_Freq set " 
            strQ += " Mdl_Montr_Freq_Description= '"+ desc+"'  ," 
            strQ += " ActiveStatus ='"+activests+"' ,"
            strQ += " ActiveStatus ='"+activests+"' ,"
            strQ += " UpdatedBy = '"+userId +"'  ,"
            strQ += " UpdateDate =GETDATE()  "  
            strQ += " where Mdl_Montr_Freq_AID='"+optId +"' "
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
            tableResult = self.objdbops.getTable("""
                SELECT 
                    CASE P.ActiveStatus WHEN 1 THEN 'Active' ELSE 'Inactive' END AS sts,
                    P.Prd_Addr_AID AS AID,
                    P.Prd_Addr_Label AS opt,
                    P.Prd_Addr_Description AS [desc],
                    C.Category_AID,
                    C.Category_Label
                FROM Prd_Addr_Master P
                LEFT JOIN Model_Category C ON P.category_aid = C.Category_AID
                ORDER BY P.AddDate
            """)
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
        
        elif(tbl=="task_fun"):
            return self.objdbops.getscalar("select count(*) from Task_Function_Master where upper(Task_Function_Label)=upper('"+ val +"')")
        elif(tbl=="task_type"):
            return self.objdbops.getscalar("select count(*) from Task_Type_Master where upper(Task_Type_Label)=upper('"+ val +"')")
        elif(tbl=="sub_task_type"):
            return self.objdbops.getscalar("select count(*) from Sub_Tasktype_Master where upper(Sub_Task_Type_Label)=upper('"+ val +"')")
        elif(tbl=="prio"):
            return self.objdbops.getscalar("select count(*) from Task_Priority_Master where upper(Task_Priority_Label)=upper('"+ val +"')")
        elif(tbl=="task_appro"):
            return self.objdbops.getscalar("select count(*) from Task_ApprovalStatus_Master where upper(Task_ApprovalStatus_Label)=upper('"+ val +"')")

        elif(tbl=="issue_fun"):
            return self.objdbops.getscalar("select count(*) from Issue_Function_Master where upper(Issue_Function_Label)=upper('"+ val +"')")
        elif(tbl=="issue_type"):
            return self.objdbops.getscalar("select count(*) from Issue_Type_Master where upper(Issue_Type_Label)=upper('"+ val +"')")
        elif(tbl=="issue_sub_type"):
            return self.objdbops.getscalar("select count(*) from Sub_Issue_Type_Master where upper(Sub_Issue_Type_Label)=upper('"+ val +"')")
        elif(tbl=="issue_prio"):
            return self.objdbops.getscalar("select count(*) from Issue_Priority_Master where upper(Issue_Priority_Label)=upper('"+ val +"')")
        elif(tbl=="issue_status"):
            return self.objdbops.getscalar("select count(*) from Issue_ApprovalStatus_Master where upper(Issue_ApprovalStatus_Label)=upper('"+ val +"')")
        
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
        return self.objdbops.getscalar("select count(*) cnt from users u,department dept ,User_Category uc where  isnull(Dept_IsMRM,0)=1 and u.Dept_AID=dept.Dept_AID and uc.UC_AID=u.UC_AID and  UC_Level=3 and u_aid="+str(uid))
    
    def checkMRMUser(self,uid):
        return self.objdbops.getscalar("select count(*) cnt from users u,department dept ,User_Category uc where  isnull(Dept_IsMRM,0)=1 and u.Dept_AID=dept.Dept_AID and uc.UC_AID=u.UC_AID and u_aid="+str(uid))

    def getMRMHead(self):
        return self.objdbops.getscalar("select u_aid cnt from users u,department dept ,User_Category uc where  isnull(Dept_IsMRM,0)=1 and u.Dept_AID=dept.Dept_AID and uc.UC_AID=u.UC_AID and UC_Is_DeptHead=1")

    def getMdlOwner(self,mdlId):#to be updated on  server
        return self.objdbops.getscalar("select addedby from Mdl_OverView where mdl_id='"+mdlId+"'")
    

    def addSection(self,section,desc,activests,userId):  
        strQ="insert into ICQ_Sections ("
        strQ += " Section_Label   ,"
        strQ += " Section_Description  ,"
        strQ += " ActiveStatus ,"
        strQ += " AddedBy    ,"
        strQ += " AddDate  )"
        strQ += " values("
        strQ += " '"+section+"'   ,"
        strQ += " '"+desc+"'  ,"
        strQ += " '"+activests+"' ,"
        strQ += " '"+userId +"'    ,"
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
        strQ += " '"+section+"'   ,"
        strQ += " '"+desc+"'  ,"+id+", "
        strQ += " '"+activests+"' ,"
        strQ += " '"+userId +"'    ,"
        strQ += " GETDATE()  )	 "
        self.objdbops.insertRow(strQ)   

    def getSub_Sections(self,id):
        tableResult =self.objdbops.getTable("select  Sub_Section_Label , Sub_Section_AID  from  ICQ_Sub_Sections where Section_AID="+str(id)+" order by  Sub_Section_AID ")
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
        strQ += " '"+section+"'   ,"
        strQ += " '"+desc+"'  ,"+id+", "
        strQ += " '"+activests+"' ,"
        strQ += " '"+userId +"'    ,"
        strQ += " GETDATE()  )	 "
        self.objdbops.insertRow(strQ)   

    def getSub_Sub_Sections(self,id):
        tableResult =self.objdbops.getTable("select  Sub_Sub_Section_Label , Sub_Sub_Section_AID  from  ICQ_Sub_Sub_Sections where Sub_Section_AID="+str(id)+" order by  Sub_Section_AID ")
        print("tableResult ",tableResult)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    
    def getFLSub_Sub_Sections(self,id):
        tableResult =self.objdbops.getTable("select  Sub_Sub_Section_Label , Sub_Sub_Section_AID  from  FL_Sub_Sub_Sections where Sub_Section_AID="+str(id)+" order by  Sub_Section_AID ")
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
        strQ += " '"+section+"'   ,"
        strQ += " '"+desc+"'  ,"+id+", "
        strQ += " '"+activests+"' ,"
        strQ += " '"+userId +"'    ,"
        strQ += " GETDATE()  )	 "
        self.objdbops.insertRow(strQ)   

    def getICQQtns(self,sectionid):
        d2 = {}
        strQ="select distinct a.* from("
        strQ += " select '1' lvl,Section_AID,Section_Label,'-' Sub_Section_AID,'-' Sub_Section_Label,"
        strQ += " '-' Sub_Sub_Section_AID,'-' Sub_Sub_Section_Label,'-' Sub_Sub_Sub_Section_AID,'-' Sub_Sub_Sub_Section_Label "     
        strQ += " from ICQ_Sections  " 
        strQ += " )a ,ICQ_Question_Rating_Allocation alloc where alloc.section_aid=a.section_aid  and alloc.allocated_to='"+str(sectionid)+"'"
        strQ += " order by  a.Section_AID"#,cast(a.Sub_Section_AID as int),cast(a.Sub_Sub_Section_AID as int),cast(a.Sub_Sub_Sub_Section_AID as int)"
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
                strQtn+=" icq_question_master qtnmst left join ICQ_Sections sec on "
                strQtn+=" qtnmst.section_aid=sec.section_aid left join"
                strQtn+=" ICQ_Sub_Sections s_sec  on qtnmst.sub_section_aid=s_sec.sub_section_aid left join"
                strQtn+=" ICQ_Sub_Sub_Sections ss_sec on qtnmst.sub_sub_section_aid=ss_sec.sub_sub_section_aid "
                strQtn+=" left join ICQ_Question_Rating_Data   on qtnmst.Question_aid=ICQ_Question_Rating_Data.question_aid	"
                strQtn+=" where sec.section_aid="+str(tableResult['Section_AID'][ind])+" "
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
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i]
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
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i]
                                    } 
                    d2[arrayidx] = d
                    arrayidx+=1  
                del qtnResult
        
            del tableResult   
            # print(d2)
        return d2 # json.dumps(d2)  

    def getFLQtns(self,sectionid):
        d2 = {}
        strQ="select distinct a.* from("
        strQ += " select '1' lvl,Section_AID,Section_Label,'-' Sub_Section_AID,'-' Sub_Section_Label,"
        strQ += " '-' Sub_Sub_Section_AID,'-' Sub_Sub_Section_Label,'-' Sub_Sub_Sub_Section_AID,'-' Sub_Sub_Sub_Section_Label "     
        strQ += " from FL_Sections  " 
        strQ += " )a ,FL_Allocation alloc where alloc.section_aid=a.section_aid  and alloc.allocated_to='"+str(sectionid).replace("'","''")+"'"
        strQ += " order by  a.Section_AID"#,cast(a.Sub_Section_AID as int),cast(a.Sub_Sub_Section_AID as int),cast(a.Sub_Sub_Sub_Section_AID as int)"
        tableResult =self.objdbops.getTable(strQ)
        print("strQ",strQ)
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
                strQtn+=" FL_question_master qtnmst left join FL_Sections sec on "
                strQtn+=" qtnmst.section_aid=sec.section_aid left join"
                strQtn+=" FL_Sub_Sections s_sec  on qtnmst.sub_section_aid=s_sec.sub_section_aid left join"
                strQtn+=" FL_Sub_Sub_Sections ss_sec on qtnmst.sub_sub_section_aid=ss_sec.sub_sub_section_aid "
                strQtn+=" left join FL_Question_Rating_Data   on qtnmst.Question_aid=FL_Question_Rating_Data.question_aid	"
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
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i]
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
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i]
                                    } 
                    d2[arrayidx] = d
                    arrayidx+=1  
                del qtnResult
        
            del tableResult   
        print("d2 " ,d2)
        return d2 # json.dumps(d2)  
      
    
    def getICQModels(self,id):
        tableResult =self.objdbops.getTable("select distinct Model_Id from ICQ_Question_Rating_Allocation where Allocated_to ="+str(id)+" order by  1 ")
       
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    
    def getICQQtnSection(self,id):
        tableResult =self.objdbops.getTable("select distinct section_label,alloc.section_aid from ICQ_Sections icq,ICQ_Question_Rating_Allocation alloc where alloc.section_aid=icq.section_aid and Allocated_to ='"+str(id)+"' order by  1 ")
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    
    def getICQQtnSectionFinal(self):
        tableResult =self.objdbops.getTable("select distinct section_label,alloc.section_aid from ICQ_Sections icq,ICQ_Question_Rating_Allocation alloc where alloc.section_aid=icq.section_aid order by  1 ")
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    
    def getICQQtnsFinal(self):
        d2 = {}
        strQ="select distinct a.* from("
        strQ += " select '1' lvl,Section_AID,Section_Label,'-' Sub_Section_AID,'-' Sub_Section_Label,"
        strQ += " '-' Sub_Sub_Section_AID,'-' Sub_Sub_Section_Label,'-' Sub_Sub_Sub_Section_AID,'-' Sub_Sub_Sub_Section_Label "     
        strQ += " from ICQ_Sections   )a  ,ICQ_Question_Rating_Allocation alloc where alloc.section_aid=a.section_aid "# and a.section_aid='"+str(sectionid)+"'"
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
                strQtn+=" icq_question_master qtnmst left join ICQ_Sections sec on "
                strQtn+=" qtnmst.section_aid=sec.section_aid left join"
                strQtn+=" ICQ_Sub_Sections s_sec  on qtnmst.sub_section_aid=s_sec.sub_section_aid left join"
                strQtn+=" ICQ_Sub_Sub_Sections ss_sec on qtnmst.sub_sub_section_aid=ss_sec.sub_sub_section_aid "
                strQtn+=" left join ICQ_Question_Rating_Data_Final   on qtnmst.Question_aid=ICQ_Question_Rating_Data_Final.question_aid	"
                strQtn+=" where sec.section_aid="+str(tableResult['Section_AID'][ind])+" "
                strQtn+=" order by   qtnmst.Question_AID,qtnmst.section_aid"
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
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i]
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
                                    'Rating_Yes_NO':qtnResult['Rating_Yes_NO'][i],'Doc_Yes_No':qtnResult['Doc_Yes_No'][i],'comments':qtnResult['comments'][i]
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
    
    def canUpdateRatings(self,uid):
        return str(self.objdbops.getscalar("select count(*) from [ICQ_Question_Rating_Data_Final] where [Review_id] in ( \
                                        select max(ICQS_AID) review_id from  ICQ_Setting) and addedby='"+str(uid)+"'"))
    
    
    def insert_notification(self,from_user:str,to_user:str,utility:str,notification_trigger:str,is_visible): 
        create_date= datetime.now()
        notification_obj=NotificationDetails(notification_from=from_user,notification_to=to_user,utility=utility,
                                            notification_trigger=notification_trigger,is_visible=is_visible,create_date=create_date)
        notification_obj.save() 
      
    def publishICQ(self):
        maxid=   str(self.objdbops.getscalar("select max(ICQS_AID) review_id from  ICQ_Setting"))
        self.objdbops.insertRow("update ICQ_Setting set publish=1 where ICQS_AID="+maxid)

    def insertRatings(self,q_id,yes,no,doc_yes,doc_no):
        if(str(self.objdbops.getscalar("select count(*) from ICQ_Question_Rating where question_aid="+str(q_id)))=="0"):
            strQ="INSERT INTO   ICQ_Question_Rating \
            ( Question_AID \
            , Rating_Yes \
            , Rating_No \
            , Doc_Yes \
            , Doc_No , AddDate  )\
                VALUES\
            ("+str(q_id) +"\
            ,"+str(yes)+"\
            ,"+str(no)+"\
            ,"+str(doc_yes)+"\
            ,"+str(doc_no)+" ,getdate() )"
            self.objdbops.insertRow(strQ)
        else:
            strQ="update ICQ_Question_Rating set Rating_Yes="+str(yes)+",Rating_No="+str(no)+",Doc_Yes="+str(doc_yes)+",Doc_No="+str(doc_no)+" where   question_aid="+str(q_id)
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
                where mdl.Mdl_Source=mdlsrc.Mdl_Scr_AID and mdl.Mdl_Id ='"+ mdl_id +"')"         
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
                strQtn+=" where sec.section_aid="+str(tableResult['Section_AID'][ind])+" "
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
        tableResult =self.objdbops.getTable("select  Sub_Section_Label , Sub_Section_AID  from  Ques_Sub_Sections where Section_AID="+str(id)+" order by  Sub_Section_AID ")
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
        strQ += " '"+stype+"'   ,"
        strQ += " '"+section+"'   ,"
        strQ += " '"+desc+"'  ,"
        strQ += " '"+activests+"' ,"
        strQ += " '"+userId +"'    ,"
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
        strQ += " '"+section+"'   ,"
        strQ += " '"+desc+"'  ,"+id+", "
        strQ += " '"+activests+"' ,"
        strQ += " '"+userId +"'    ,"
        strQ += " GETDATE()  )	 "
        self.objdbops.insertRow(strQ)   

    def getQuesSub_Sections(self,id):
        tableResult =self.objdbops.getTable("select  Sub_Section_Label , Sub_Section_AID  from  Ques_Sub_Sections where Section_AID="+str(id)+" order by  Sub_Section_AID ")
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
        strQ += " '"+section+"'   ,"
        strQ += " '"+desc+"'  ,"+id+", "
        strQ += " '"+activests+"' ,"
        strQ += " '"+userId +"'    ,"
        strQ += " GETDATE()  )	 "
        self.objdbops.insertRow(strQ)   

    def getQuesSub_Sub_Sections(self,id):
        tableResult =self.objdbops.getTable("select  Sub_Sub_Section_Label , Sub_Sub_Section_AID  from  Ques_Sub_Sub_Sections where Sub_Section_AID="+str(id)+" order by  Sub_Section_AID ")
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
        strQ += " '"+section+"'   ,"
        strQ += " '"+desc+"'  ,"+id+", "
        strQ += " '"+activests+"' ,"
        strQ += " '"+userId +"'    ,"
        strQ += " GETDATE()  )	 "
        self.objdbops.insertRow(strQ)   

    def getSub_Sub_Sub_Sections(self,id):
        tableResult =self.objdbops.getTable("select  Sub_Sub_Sub_Section_Label , Sub_Sub_Sub_Section_AID  from  ICQ_Sub_Sub_Sub_Sections where Sub_Sub_Section_AID="+str(id)+" order by  Sub_Sub_Section_AID ")
        print("tableResult ",tableResult)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)

    def getQuesSub_Sub_Sub_Sections(self,id):
        tableResult =self.objdbops.getTable("select  Sub_Sub_Sub_Section_Label , Sub_Sub_Sub_Section_AID  from  Ques_Sub_Sub_Sub_Sections where Sub_Sub_Section_AID="+str(id)+" order by  Sub_Sub_Section_AID")
        print("tableResult ",tableResult)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)

    def get_Qtn_Section(self,mdl_id):
        strQuery="  select * from Ques_Sections where ModelTool_Type in(\
            select case Mdl_Src_Label when 'Internal' then '2' when 'Vendor' then '1' else '3' end qtntype  from [Model_Source_Master] mdlsrc, Mdl_OverView mdl\
            where mdl.Mdl_Source=mdlsrc.Mdl_Scr_AID and mdl.Mdl_Id ='"+ mdl_id +"'\
            ) order by 1"
        tableResult =self.objdbops.getTable(strQuery)
        print("tableResult ",tableResult)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult) 

    def getQues_Sections(self,id):
        tableResult =self.objdbops.getTable("select  Section_Label , Section_AID  from  Ques_Sections where modeltool_type="+str(id)+" order by Section_AID ")
        print("tableResult ",tableResult)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)
    
    def isAutherized(self,userCatId,rsrclbl):
        # print('user access ',self.objdbops.getscalar("select count(*) from User_Access where UC_AID ='"+str(userCatId)+"' and r_aid='"+rsrcId+"'"))
        # return str(self.objdbops.getscalar("select count(*) from User_Access where UC_AID ='"+str(userCatId)+"' and r_aid='"+rsrcId+"'"))
        return str(self.objdbops.getscalar("select count(*) from User_Access INNER JOIN Resources on User_Access.R_AID = Resources.R_AID where UC_AID = '"+str(userCatId)+"' and Resources.R_Label = '"+rsrclbl+"'"))
    
    def insertActivityTrail(self,refference_id,activity_trigger,activity_details,addedby,accessToken):         
        from rest_framework import generics, permissions, status,serializers
        import os
        import requests
        print('inside insertacitity')
        api_url=os.environ['API_URL']
        api_url=api_url+"save_activity_trail/"       
        params={  
            'refference_id': refference_id,
            'activity_trigger':activity_trigger,
            'addedby':addedby,
            'activity_details':activity_details,} 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+accessToken
            }
        response = requests.post(api_url, data= json.dumps(params),headers=header)  
        if response.status_code == status.HTTP_200_OK:       
            return response.json()
        
    ######FL########

    def getFLSections(self):
        tableResult =self.objdbops.getTable("select  Section_Label , Section_AID  from  FL_Sections  order by  Section_AID ")
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)


    def FL_getSub_Sections(self,id):
        tableResult =self.objdbops.getTable("select  Sub_Section_Label , Sub_Section_AID  from  FL_Sub_Sections where Section_AID="+str(id)+" order by  Sub_Section_AID ")
        print("tableResult ",tableResult)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)


    def getAllFLQtns(self):
        d2 = {}
        strQ="select a.* from("
        strQ += " select '1' lvl,Section_AID,Section_Label,'-' Sub_Section_AID,'-' Sub_Section_Label,"
        strQ += " '-' Sub_Sub_Section_AID,'-' Sub_Sub_Section_Label,'-' Sub_Sub_Sub_Section_AID,'-' Sub_Sub_Sub_Section_Label "     
        strQ += " from FL_Sections   "         
        strQ += " )a  order by  a.Section_AID"#,cast(a.Sub_Section_AID as int),cast(a.Sub_Sub_Section_AID as int),cast(a.Sub_Sub_Sub_Section_AID as int)"
        tableResult =self.objdbops.getTable(strQ) 

        arrayidx=0 
        d2 = {} 
        arrayidx=0 
        if tableResult.empty == False:
            for ind in tableResult.index:  
                strQtn="" 
                strQtn+="  select   sec.Section_AID, s_sec.Sub_Section_AID , convert( int, isnull(ss_sec.Sub_Sub_Section_AID,999)) "
                strQtn+="  Sub_Sub_Section_AID, isnull(sec.Section_Label,'') Section_Label, isnull(s_sec.Sub_Section_Label,'') Sub_Section_Label,isnull(ss_sec.Sub_Sub_Section_Label,'') Sub_Sub_Section_Label  "
                strQtn+="  from  fl_question_master qtnmst left join FL_Sections sec on  qtnmst.section_aid=sec.section_aid left join FL_Sub_Sections s_sec  on qtnmst.sub_section_aid=s_sec.sub_section_aid "
                strQtn +=" left join FL_Sub_Sub_Sections ss_sec on qtnmst.sub_sub_section_aid=ss_sec.sub_sub_section_aid  where sec.section_aid="+str(tableResult['Section_AID'][ind])+" "
                strQtn+="  group by   sec.Section_AID,s_sec.Sub_Section_AID,  ss_sec.Sub_Sub_Section_AID, Section_Label,   Sub_Section_Label, Sub_Sub_Section_Label " 
                strQtn+="  order by cast(sec.Section_AID as int),cast(s_sec.Sub_Section_AID  as int)  ,convert( int, isnull(ss_sec.Sub_Sub_Section_AID,999))"

                strQtn="SELECT Question_AID,Question_Label,\
                sec.Section_AID,\
                isnull(s_sec.sub_section_aid,0) Sub_Section_AID,isnull(ss_sec.sub_sub_section_aid,0) Sub_Sub_Section_AID,isnull(Sub_Sub_Sub_Section_AID,0) Sub_Sub_Sub_Section_AID ,\
                RANK() OVER (PARTITION BY sec.Section_AID,\
                s_sec.sub_section_aid ORDER BY qtnmst.adddate,sec.Section_AID,\
                s_sec.sub_section_aid,ss_sec.sub_sub_section_aid  ) AS Rank, isnull(sec.Section_Label,'') Section_Label, isnull(s_sec.Sub_Section_Label,'') Sub_Section_Label,isnull(ss_sec.Sub_Sub_Section_Label,'') Sub_Sub_Section_Label  \
                from fl_question_master qtnmst left join FL_Sections sec on  qtnmst.section_aid=sec.section_aid left join FL_Sub_Sections s_sec \
                on qtnmst.sub_section_aid=s_sec.sub_section_aid  left join FL_Sub_Sub_Sections ss_sec on \
                qtnmst.sub_sub_section_aid=ss_sec.sub_sub_section_aid   where sec.section_aid="+str(tableResult['Section_AID'][ind])
                 
                qtnResult =self.objdbops.getTable(strQtn)                 
                iLvlCurr=0
                iSecCurr=0
                iSubSecCurr=0
                iSubSubSecCurr=0
                iSubSubSecPrev=0 
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
                lstSubSec=[]
                lstSubSubSec=[]
                iSubSecPrev=""
                cntSubSec=0
                cntSubSubSec=0
                cntSubSubSubSec=0
                cntQtn=0
                
                for i in qtnResult.index:  
                    blnAlreadyIncreased = False 
                    strLevelText = ""
                    # iLvlCurr = int(qtnResult['lvl'][i])
                    iSecCurr = int(qtnResult['Section_AID'][i])
                    iSubSecCurr =int(qtnResult['Sub_Section_AID'][i])
                    iSubSubSecCurr =int(qtnResult['Sub_Sub_Section_AID'][i])   
                    strSectionText = qtnResult["Section_Label"][i]
                    strSubSectionText = qtnResult["Sub_Section_Label"][i]
                    strSubSectionText = strSubSectionText.replace("-", "")
                    strSubSubSectionText =qtnResult["Sub_Sub_Section_Label"][i]   
                    strQtn = qtnResult["Question_Label"][i]
                    strQtnIdx = qtnResult["Question_AID"][i]
                    if qtnResult["Sub_Section_AID"][i] != 0 and qtnResult["Sub_Sub_Section_AID"][i] != 0  and   qtnResult["Sub_Sub_Sub_Section_AID"][i] == 0 :
                        strLevelText='->->->'
                    elif qtnResult["Sub_Section_AID"][i] != 0 and (qtnResult["Sub_Sub_Section_AID"][i] == 0 ):
                        strLevelText='->->'
                    elif qtnResult["Sub_Section_AID"][i] == 0 :
                        strLevelText='->->' 
                    if (i == 0): 
                        d = {'Section_AID':str(qtnResult['Section_AID'][i]), 
                        'Section_Label':str(qtnResult['Section_Label'][i]), 
                        'Sub_Section_AID':"", 
                        'Sub_Section_Label':"", 
                        'Sub_Sub_Section_AID':'', 
                        'Sub_Sub_Section_Label':'', 
                        'qtnNo':"",
                        'qtnsArr':'',
                        'lvl': '->'} 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    #     if(strSubSectionText != ''):
                    #         lstSubSec.append(strSubSectionText)
                    #         cntSubSec +=1
                    #     if strSubSubSectionText!='':
                    #         lstSubSubSec.append(strSubSubSectionText) 
                    #         cntSubSubSec+=1

                    if not (strSubSectionText in lstSubSec): 
                        lstSubSec.append(strSubSectionText)
                        iSubSecPrev=strSubSectionText
                        cntSubSec +=1
                        cntSubSubSec=0
                        cntQtn=0
                        d = {'Section_AID':str(qtnResult['Section_AID'][i]), 
                        'Section_Label':'', 
                        'Sub_Section_AID':iSubSecCurr, 
                        'Sub_Section_Label':strSubSectionText, 
                        'Sub_Sub_Section_AID':'', 
                        'Sub_Sub_Section_Label':'', 
                        'qtnNo':str(chr(64+cntSubSec)),
                        'qtnsArr':'',
                        'lvl': strLevelText} 
                        d2[arrayidx] = d
                        arrayidx+=1  
 
                    elif strSubSubSectionText=='':
                        cntSubSubSec +=1
                        cntQtn=0 
                    if not (strSubSubSectionText in lstSubSubSec) and strSubSubSectionText !='':
                        lstSubSubSec.append(strSubSubSectionText)
                        iSubSubSecPrev=strSubSubSectionText
                        cntSubSubSec+=1
                        cntQtn=0
                        d = {'Section_AID':str(qtnResult['Section_AID'][i]), 
                        'Section_Label':'', 
                        'Sub_Section_AID':'', 
                        'Sub_Section_Label':'', 
                        'Sub_Sub_Section_AID':iSubSubSecCurr, 
                        'Sub_Sub_Section_Label':strSubSubSectionText, 
                        'qtnNo':str(cntSubSubSec),
                        'qtnsArr':'',
                        'lvl': strLevelText} 
                        d2[arrayidx] = d
                        arrayidx+=1  
                    # elif strSubSubSectionText =='':
                    #     d = {'Section_AID':str(qtnResult['Section_AID'][i]), 
                    #     'Section_Label':'', 
                    #     'Sub_Section_AID':iSubSecCurr, 
                    #     'Sub_Section_Label':strSubSectionText, 
                    #     'Sub_Sub_Section_AID':'', 
                    #     'Sub_Sub_Section_Label':'', 
                    #     'qtnNo':str(cntSubSubSec),
                    #     'qtnsArr':'',
                    #     'lvl': strLevelText} 
                    #     d2[arrayidx] = d
                    #     arrayidx+=1  
                        # print('sub ',str(cntSubSec),'.',cntSubSubSec,':',str(strQtnIdx))
                    cntQtn +=1
                    if(strSubSubSectionText !=''):
                        print('qtn no 1: ',str(chr(64+cntSubSec)),'.',str(cntSubSubSec),'.',str(chr(cntQtn+96)),',',str(strQtnIdx)) 
                        strQNo=str(chr(cntQtn+96))
                    elif strSubSubSectionText =='':
                        if cntSubSubSec==0:
                            cntSubSubSec+=1
                        strQNo=str(cntSubSubSec)
                        print('qtn no 2: ',str(chr(64+cntSubSec)),'.',str(cntSubSubSec),'.',str(chr(cntQtn+96)),',',str(strQtnIdx)) 
                    else:
                        print('qtn no 3: ',str(chr(64+cntSubSec)),'.',str(cntSubSubSec),'.',str(strQtnIdx)) 
                        strQNo=str(chr(cntQtn+64))

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
                        'qtnsArr':strQtn,
                        'qtn_aid':str(strQtnIdx), 
                        } 
                    d2[arrayidx] = d
                    arrayidx+=1  
                del qtnResult
                # print('Question ', lstSubSec,lstSubSubSec )
            del tableResult 
            # print(d2)
        return d2 # json.dumps(d2)  


    def getAllFLQtnsAndRatings(self):
        d2 = {}
        strQ="select a.* from("
        strQ += " select '1' lvl,Section_AID,Section_Label,'-' Sub_Section_AID,'-' Sub_Section_Label,"
        strQ += " '-' Sub_Sub_Section_AID,'-' Sub_Sub_Section_Label,'-' Sub_Sub_Sub_Section_AID,'-' Sub_Sub_Sub_Section_Label "     
        strQ += " from FL_Sections   "         
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
                strQtn+=" fl_question_master qtnmst left join FL_Sections sec on "
                strQtn+=" qtnmst.section_aid=sec.section_aid left join"
                strQtn+=" FL_Sub_Sections s_sec  on qtnmst.sub_section_aid=s_sec.sub_section_aid left join"
                strQtn+=" FL_Sub_Sub_Sections ss_sec on qtnmst.sub_sub_section_aid=ss_sec.sub_sub_section_aid left join FL_Question_Rating  ratings on qtnmst.Question_AID =ratings.Question_AID "
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


    def fl_insertRatings(self,q_id,yes,no,doc_na):
        if(str(self.objdbops.getscalar("select count(*) from FL_Question_Rating where question_aid="+str(q_id)))=="0"):
            strQ="INSERT INTO   FL_Question_Rating \
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
            strQ="update FL_Question_Rating set Rating_Yes="+str(yes)+",Rating_No="+str(no)+",NA="+str(doc_na)+" where   question_aid="+str(q_id)
            self.objdbops.insertRow(strQ)









