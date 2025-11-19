from app1.DAL.dboperations import dbops
import json 
import pandas as pd
from app1.Adm_Utils.Masters import MasterTbls
from rest_framework import serializers

objmaster=MasterTbls()

class RegisterModel:
    objdbops =None

    def __init__(self):
        self.objdbops=dbops()

    def getMdlOwnerById(self,mdlId,UserType):
        
        strQ=" select concat(Users.U_FName ,' ', users.U_LName) uname ,users.u_Aid  from Mdl_Relevant_personnel mdl_users,Users where mdl_id='"+ mdlId +"'"
        strQ+=" and mdl_users.u_id= users.u_Aid and u_type='"+ UserType +"'"
        dtusers=  self.objdbops.getTable(strQ) 
        dtusers= dtusers.to_json(orient='index')
        return json.loads(dtusers)


    def getUsers(self,dept,utype):        
        tableResult =self.objdbops.getTable("select concat(U_FName,' ',U_LName) usernm,u_aid  from users where dept_aid='"+str(dept)+"'")# and UC_AID='"+str(utype)+"'
        userlst= tableResult.to_json(orient='index')
        return json.loads(userlst)
    
    def getUsersByType(self,utype):        
        tableResult =self.objdbops.getTable("select concat(U_FName,' ',U_LName) usernm,u_aid from User_Category uc,Users u where uc_label='"+utype+"' and uc.UC_AID=u.UC_AID")# and UC_AID='"+str(utype)+"'
        userlst= tableResult.to_json(orient='index')
        return json.loads(userlst)
    
    def getUserDeatils(self,utype,dept):
        strq= "select rs.r_aid,r_label, 'block' sts from user_access ua , Resources rs where rs.R_AID=ua.r_AID and  ua.uc_AID='"+str(utype)+"' "
        strq=strq + " union "
        strq=strq + " select *,'none' from( "
        strq=strq + " SELECT r_aid,r_label from Resources "
        strq=strq + " except "
        strq=strq + " select rs.r_aid,r_label   "
        strq=strq + " from user_access ua , Resources rs where rs.R_AID=ua.r_AID "
        strq=strq + " and  ua.uc_AID='"+ str(utype)+ "' )a " 
        strq=strq + " union "
        strq=strq + " select count(*),'Dept Head',case when count(*)=1 then 'block' else 'none' end from user_category where uc_is_depthead=1 and uc_AID='"+ str(utype)+ "' "
        strq=strq + " union "
        strq=strq +  "select rs.r_aid,r_label, 'block' sts from user_access ua , Resources rs where rs.R_AID=ua.r_AID and  ua.uc_AID='"+str(utype)+"' and ua.UA_dept='"+str(dept)+"' "
         
        tableResult =self.objdbops.getTable(strq)        
        return tableResult
    
    def getDeptNm(self,dept):
        return self.objdbops.getscalar("SELECT  Dept_Label   FROM  Department where Dept_AID ='"+str(dept)+"'")
    
    def getMdl_Src(self):
        tableResult =self.objdbops.getTable("SELECT Mdl_Scr_AID,Mdl_Src_Label FROM Model_Source_Master where ActiveStatus=1 ")
        Mdl_Src = tableResult.to_json(orient='index')
        return json.loads(Mdl_Src)
    
    def getMdl_Type(self):
        tableResult =self.objdbops.getTable("SELECT  Mdl_Type_AID,Mdl_Type_Label FROM Model_Type_Master where ActiveStatus=1")
        Mdl_Type = tableResult.to_json(orient='index')
        return json.loads(Mdl_Type)
    
    def getMdl_Usage_Fre(self):
        tableResult =self.objdbops.getTable("SELECT Mdl_Use_Freq_AID,Mdl_Use_Freq_Label FROM Model_Use_Freq_Master where ActiveStatus=1")
        Mdl_Usage_Frq= tableResult.to_json(orient='index')
        return json.loads(Mdl_Usage_Frq)
    
    def getPrd_Addr(self):
        tableResult =self.objdbops.getTable("SELECT Prd_Addr_AID,Prd_Addr_Label FROM Prd_Addr_Master where ActiveStatus=1")
        Prd_Addr= tableResult.to_json(orient='index')
        return json.loads(Prd_Addr)
    
    def getMdl_Risk(self):
        tableResult =self.objdbops.getTable("SELECT Mdl_Risk_AID,Mdl_Risk_Label FROM Mdl_Risk_Master where ActiveStatus=1")
        Mdl_Risk= tableResult.to_json(orient='index')
        return json.loads(Mdl_Risk)
    
    def getIntrinsic(self):
        tableResult =self.objdbops.getTable("SELECT Intrinsic_AID,Intrinsic_Label FROM Intrinsic_Master where ActiveStatus=1")
        Intrinsic= tableResult.to_json(orient='index')
        return json.loads(Intrinsic)
    
    def getMateriality(self):
        tableResult =self.objdbops.getTable("SELECT Materiality_AID,Materiality_Label FROM Materiality_Master where ActiveStatus=1")
        Materiality= tableResult.to_json(orient='index')
        return json.loads(Materiality)
    
    def getReliance(self):
        tableResult =self.objdbops.getTable("SELECT Reliance_AID,Reliance_Label FROM Reliance_Master where ActiveStatus=1")
        Reliance= tableResult.to_json(orient='index')
        return json.loads(Reliance)
    
    def getMdlUpstrem(self,uid):
        #tableResult =self.objdbops.getTable("select Mdl_Upstream_AID AID, Mdl_Upstream_Label opt , Mdl_Upstream_Description'desc' from  Mdl_Upstream  where ActiveStatus=1")
        tableResult =self.objdbops.getTable("select mdl_id from Mdl_OverView where AddedBy="+str(uid))
        Reliance= tableResult.to_json(orient='index')
        return json.loads(Reliance)
    
    def getMdlDwStream(self):
        tableResult =self.objdbops.getTable("Select Mdl_Dwstream_AID AID, Mdl_Dwstream_Label opt , Mdl_Dwstream_Description'desc' from  Mdl_Dwstream  where ActiveStatus=1")
        Reliance= tableResult.to_json(orient='index')
        return json.loads(Reliance)
    
    def getMontrFreq(self):
        tableResult =self.objdbops.getTable("SELECT Mdl_Montr_Freq_AID AID, Mdl_Montr_Freq_Label opt ,Mdl_Montr_Freq_Description'desc' from Mdl_Montr_Freq where ActiveStatus=1")
        Reliance= tableResult.to_json(orient='index')
        return json.loads(Reliance)
    
    def getMdlFunc(self):
        tableResult =self.objdbops.getTable(" select Mdl_Fncn_AID AID, Mdl_Fncn_Label opt ,Mdl_Fncn_Description 'desc' from Model_Function_Master  where ActiveStatus=1")
        Reliance= tableResult.to_json(orient='index')
        return json.loads(Reliance)

    def getModelsbyUserid(self,userId):
        tableResult =self.objdbops.getTable("select * from Mdl_OverView where addedby="+str(userId))
        mdldata= tableResult.to_json(orient='index')
        del tableResult
        return json.loads(mdldata)    
    
    def getMdlinfo(self,mdlId):
        return self.objdbops.getTable("select * from Mdl_OverView where Mdl_Id='"+str(mdlId) +"'")
    

    def updateMdlVersion(self,mdlId,isMinor):
        newmdlid=''
        if isMinor =="1":
            strQ="select  concat ( case when is_tool=0 then 'M' else 'T' end ,  format(mdl_cnt,'00'),"
            strQ+=" format(mdl_major_ver,'00') , format(mdl_minor_ver+1,'00'))"
            strQ+=" from Mdl_OverView where Mdl_Id='"+mdlId+"'"
            newmdlid=self.objdbops.getscalar(strQ)
        else:
            strQ="select  concat ( case when is_tool=0 then 'M' else 'T' end ,  format(mdl_cnt,'00'),"
            strQ+=" format(mdl_major_ver+1,'00') , format(mdl_minor_ver,'00'))"
            strQ+=" from Mdl_OverView where Mdl_Id='"+mdlId+"'"
            newmdlid=self.objdbops.getscalar(strQ)
        return newmdlid

    def getModelListByUSerid(self,userId,userLvl,istool): 
        # if userLvl=="1":
        #     strQ="select isnull(Mdl_Risk_Label,'') Mdl_Risk_Label,isnull(Intrinsic_Label,'') Intrinsic_Label,"
        #     strQ+=" isnull(Reliance_Label,'') Reliance_Label,isnull(Materiality_Label,'') Materiality_Label, mdl_overview.*,"
        #     strQ+=" isnull(mdl_risks.Risk_Mtgn,'') Risk_Mtgn,isnull(mdl_risks.Fair_Lndg,'') Fair_Lndg  from("
        #     strQ+=" select Mdl_Src_Label,Mdl_Use_Freq_Label,Prd_Addr_Label,mdl_oview.*,Mdl_Type_Label from  "
        #     strQ+=" Mdl_OverView mdl_oview,Model_Type_Master mdl_ty_mstr ,"
        #     strQ+=" Model_Source_Master mdl_src_mst ,Model_Use_Freq_Master mdl_use_freq_mst ,Prd_Addr_Master prd_addr_mst"
        #     strQ+=" where mdl_oview.addedby="+ str(userId)
        #     strQ+=" and mdl_oview.mdl_type=mdl_ty_mstr.Mdl_Type_AID"
        #     strQ+=" and Mdl_Scr_AID=Mdl_Source"
        #     strQ+=" and mdl_use_freq_mst.Mdl_Use_Freq_AID=usgFreq"
        #     strQ+=" and prd_addr_mst.Prd_Addr_AID=prctAddr and mdl_oview.is_tool=0 )mdl_overview left join"
        #     strQ+=" ("
        #     strQ+=" select isnull(Mdl_Risk_Label,'') Mdl_Risk_Label,isnull(Intrinsic_Label,'') Intrinsic_Label,isnull(Reliance_Label,'') Reliance_Label,isnull(Materiality_Label,'') Materiality_Label,mdl_risks.* from  Mdl_Risks mdl_risks left join  Mdl_Risk_Master mdl_risks_mst  "
        #     strQ+=" on Mdl_Risk_AID=mdl_risks left join Intrinsic_Master on Intrinsic_AID=Intr_Risk" 
        #     strQ+=" left join Reliance_Master on Reliance_AID=Reliance   left join Materiality_Master on Materiality_AID =Materiality"
        #     strQ+=" ) mdl_risks"
        #     strQ+=" on mdl_overview.Mdl_Id =mdl_risks.Mdl_Id"
        #     strQ+=" order by mdl_overview.adddate"
        # elif userLvl=="2": 
        if str(objmaster.checkMRMHead(str(userId)))=="1":
            strQ="select isnull(str(vtcnt),'') vtcnt,case   when  isnull(vtcnt,0) >0 then 'text-danger' else '' end Activity,isnull(Mdl_Risk_Label,'') Mdl_Risk_Label,isnull(Intrinsic_Label,'') Intrinsic_Label,"
            strQ+=" isnull(Reliance_Label,'') Reliance_Label,isnull(Materiality_Label,'') Materiality_Label, mdl_overview.*,"
            strQ+=" isnull(mdl_risks.Risk_Mtgn,'') Risk_Mtgn,isnull(mdl_risks.Fair_Lndg,'') Fair_Lndg ,Mdl_Use_Freq_Label,Prd_Addr_Label from("
            strQ+=" select Mdl_Src_Label,mdl_oview.*,Mdl_Type_Label from  "       
            strQ+=" Model_Source_Master mdl_src_mst, Mdl_OverView mdl_oview left join Model_Type_Master mdl_ty_mstr on mdl_type=mdl_ty_mstr.Mdl_Type_AID"
            strQ+=" where mdl_oview.addedby in ("+str(self.getSubOrdUsers(userId))+")"      
            strQ+=" and Mdl_Scr_AID=Mdl_Source" 
            strQ+=" and mdl_oview.is_tool="+ str(istool) +" and isnull(Is_Decommissioned,0)<>2 and isnull(is_submit,0)<>0) mdl_overview left join Model_Use_Freq_Master mdl_use_freq_mst on  mdl_use_freq_mst.Mdl_Use_Freq_AID=usgFreq"
            strQ+=" left join Prd_Addr_Master prd_addr_mst on  prd_addr_mst.Prd_Addr_AID=prctAddr left join"
            strQ+=" ("
            strQ+=" select isnull(Mdl_Risk_Label,'') Mdl_Risk_Label,isnull(Intrinsic_Label,'') Intrinsic_Label,isnull(Reliance_Label,'') Reliance_Label,isnull(Materiality_Label,'') Materiality_Label,mdl_risks.* from  Mdl_Risks mdl_risks left join  Mdl_Risk_Master mdl_risks_mst  "
            strQ+=" on Mdl_Risk_AID=mdl_risks left join Intrinsic_Master on Intrinsic_AID=Intr_Risk" 
            strQ+=" left join Reliance_Master on Reliance_AID=Reliance   left join Materiality_Master on Materiality_AID =Materiality"
            strQ+=" ) mdl_risks"
            strQ+=" on mdl_overview.Mdl_Id =mdl_risks.Mdl_Id"
            strQ+= " left join "
            strQ+= " (SELECT  mdl_id,count(*) vtcnt from  Validation_AssignTo "
            strQ+= " where  notify=1   and u_aid in ("+str(userId)+")"
            strQ+= " group by mdl_id  ) VTdata on VTdata.mdl_id=mdl_overview.Mdl_Id where isnull(Is_Decommissioned,0) <> 2"
            strQ+=" order by mdl_overview.adddate"   
        else:
            strQ="select isnull(str(vtcnt),'') vtcnt,case   when  isnull(vtcnt,0) >0 then 'text-danger' else '' end Activity,isnull(Mdl_Risk_Label,'') Mdl_Risk_Label,isnull(Intrinsic_Label,'') Intrinsic_Label,"
            strQ+=" isnull(Reliance_Label,'') Reliance_Label,isnull(Materiality_Label,'') Materiality_Label, mdl_overview.*,"
            strQ+=" isnull(mdl_risks.Risk_Mtgn,'') Risk_Mtgn,isnull(mdl_risks.Fair_Lndg,'') Fair_Lndg ,Mdl_Use_Freq_Label,Prd_Addr_Label from("
            strQ+=" select Mdl_Src_Label,mdl_oview.*,Mdl_Type_Label from  "       
            strQ+=" Model_Source_Master mdl_src_mst, Mdl_OverView mdl_oview left join Model_Type_Master mdl_ty_mstr on mdl_type=mdl_ty_mstr.Mdl_Type_AID"
            strQ+=" where mdl_oview.addedby in ("+str(self.getSubOrdUsers(userId))+")"      
            strQ+=" and Mdl_Scr_AID=Mdl_Source" 
            strQ+=" and mdl_oview.is_tool="+ str(istool) +" and isnull(Is_Decommissioned,0)<>2  ) mdl_overview left join Model_Use_Freq_Master mdl_use_freq_mst on  mdl_use_freq_mst.Mdl_Use_Freq_AID=usgFreq"
            strQ+=" left join Prd_Addr_Master prd_addr_mst on  prd_addr_mst.Prd_Addr_AID=prctAddr left join"
            strQ+=" ("
            strQ+=" select isnull(Mdl_Risk_Label,'') Mdl_Risk_Label,isnull(Intrinsic_Label,'') Intrinsic_Label,isnull(Reliance_Label,'') Reliance_Label,isnull(Materiality_Label,'') Materiality_Label,mdl_risks.* from  Mdl_Risks mdl_risks left join  Mdl_Risk_Master mdl_risks_mst  "
            strQ+=" on Mdl_Risk_AID=mdl_risks left join Intrinsic_Master on Intrinsic_AID=Intr_Risk" 
            strQ+=" left join Reliance_Master on Reliance_AID=Reliance   left join Materiality_Master on Materiality_AID =Materiality"
            strQ+=" ) mdl_risks"
            strQ+=" on mdl_overview.Mdl_Id =mdl_risks.Mdl_Id"
            strQ+= " left join "
            strQ+= " (SELECT  mdl_id,count(*) vtcnt from  Validation_AssignTo "
            strQ+= " where  notify=1   and u_aid in ("+str(userId)+")"
            strQ+= " group by mdl_id  ) VTdata on VTdata.mdl_id=mdl_overview.Mdl_Id where isnull(Is_Decommissioned,0)<>2"
            strQ+=" order by mdl_overview.adddate"  
        
        print('strQ ',strQ)
        tableResult =self.objdbops.getTable(strQ) 
        mdldata= tableResult.to_json(orient='index')
        del tableResult
        return json.loads(mdldata) 

    def getModelByFilter(self,userId,filterType,filterColumn,filterValue,istool):  
        strQ="select isnull(Mdl_Risk_Label,'') Mdl_Risk_Label,isnull(Intrinsic_Label,'') Intrinsic_Label,"
        strQ+=" isnull(Reliance_Label,'') Reliance_Label,isnull(Materiality_Label,'') Materiality_Label, mdl_overview.*,"
        strQ+=" isnull(mdl_risks.Risk_Mtgn,'') Risk_Mtgn,isnull(mdl_risks.Fair_Lndg,'') Fair_Lndg,case when "
        strQ+="   (( select count(*) from users u,department dept ,User_Category uc"
        strQ+="   where  isnull(Dept_IsMRM,0)=1 and u.Dept_AID=dept.Dept_AID and uc.UC_AID=u.UC_AID and UC_Is_DeptHead=1"
        strQ+="   and u.U_AID="+str(userId)+")=1 and isnull(Is_Decommissioned,0)=1)  or (   mdl_overview.addedby ="+str(userId)+" and isnull(Is_Decommissioned,0)=0 and isnull(is_submit,0)=1)  then 'Yes' else 'No' end canDecomm,case when "
        strQ+="   (( select count(*) from users u,department dept ,User_Category uc"
        strQ+="   where  isnull(Dept_IsMRM,0)=1 and u.Dept_AID=dept.Dept_AID and uc.UC_AID=u.UC_AID and UC_Is_DeptHead=1"
        strQ+="   and u.U_AID="+str(userId)+")=1 and isnull(is_submit,0)=2)  or (   mdl_overview.addedby ="+str(userId)+" and isnull(is_submit,0)=0)  then 'Yes' else 'No' end canEdit, case when (   mdl_overview.addedby ="+str(userId)+" and isnull(is_submit,0)=1)  then 'Yes' else 'No' end canReqEdit, "
        strQ+= " case isnull(Is_Decommissioned,0) when 1 then 'text-warning' when 2 then 'text-danger' else 'text-secondary' end decommcss ,isnull(Is_Decommissioned,0) Is_Decomm from("
        strQ+=" select Mdl_Src_Label,isnull(Mdl_Use_Freq_Label,'') Mdl_Use_Freq_Label,isnull(Prd_Addr_Label,'') Prd_Addr_Label,mdl_oview.*,isnull(Mdl_Type_Label ,'') Mdl_Type_Label from  "
        strQ+=" Mdl_OverView mdl_oview left join Model_Source_Master mdl_src_mst on  Mdl_Scr_AID=Mdl_Source\
                left join Model_Use_Freq_Master mdl_use_freq_mst on mdl_use_freq_mst.Mdl_Use_Freq_AID=usgFreq \
                left join Prd_Addr_Master prd_addr_mst on prd_addr_mst.Prd_Addr_AID=prctAddr \
                left join Model_Type_Master mdl_ty_mstr on mdl_oview.mdl_type=mdl_ty_mstr.Mdl_Type_AID "
        strQ+=" where mdl_oview.addedby in ("+str(self.getSubOrdUsers(userId))+")"
        if str(objmaster.checkMRMHead(str(userId)))=="1":
            strQ+=" and isnull(Is_Decommissioned,0)<>2 and isnull(is_submit,0)<>0 "
        else:
            strQ+=" and isnull(Is_Decommissioned,0)<>2 "
        strQ+=" and mdl_oview.is_tool="+ str(istool) +" ) mdl_overview left join"
        strQ+=" ("
        strQ+=" select isnull(Mdl_Risk_Label,'') Mdl_Risk_Label,isnull(Intrinsic_Label,'') Intrinsic_Label,isnull(Reliance_Label,'') Reliance_Label,isnull(Materiality_Label,'') Materiality_Label,mdl_risks.* from  Mdl_Risks mdl_risks left join  Mdl_Risk_Master mdl_risks_mst  "
        strQ+=" on Mdl_Risk_AID=mdl_risks left join Intrinsic_Master on Intrinsic_AID=Intr_Risk" 
        strQ+=" left join Reliance_Master on Reliance_AID=Reliance   left join Materiality_Master on Materiality_AID =Materiality"
        strQ+=" ) mdl_risks"
        strQ+=" on mdl_overview.Mdl_Id =mdl_risks.Mdl_Id"
        
        if(filterType=="bar" and filterColumn=="Model Risk Tier" and filterValue != "None"):
            strQ+=" where  isnull(Is_Decommissioned,0) <>2 and mdl_risks.Mdl_Risk_Label='"+filterValue+"'"
        elif(filterType=="bar" and filterColumn=="Model Risk Tier" and filterValue == "None"):
            strQ+=" where  isnull(Is_Decommissioned,0) <>2 and mdl_risks.Mdl_Risk_Label is null or mdl_risks.Mdl_Risk_Label =''"
        elif(filterType=="pie"):
            strQ+=" where isnull(Is_Decommissioned,0) <>2 and Mdl_Type_Label='"+filterValue+"'" 
        elif(filterType=="bar" and filterColumn=="Model Source" and filterValue != "None"):
            strQ+=" where isnull(Is_Decommissioned,0) <>2 and  Mdl_Src_Label='"+filterValue+"'"    
        else:
            strQ +=" where isnull(Is_Decommissioned,0) <>2"
        strQ+=" order by mdl_overview.adddate"
 
       
        tableResult =self.objdbops.getTable(strQ)
      
        mdldata= tableResult.to_json(orient='index')
        del tableResult
        return json.loads(mdldata)   

    def getModelRiskCntByUserid(self,userId,userLevel):
        # if userLevel=="1":
        #     strQ="select 'High' lbl ,count(*) cnt,1 from  Mdl_Risks mdl_risks  Where mdl_risks=1 and addedby="+str(userId)
        #     strQ+=" union"
        #     strQ+=" select 'Medium' Mdl_Risk_Label,count(*),2 from  Mdl_Risks mdl_risks  Where mdl_risks=2 and addedby="+str(userId)
        #     strQ+=" union"
        #     strQ+=" select 'Low' Mdl_Risk_Label,count(*),3 from  Mdl_Risks mdl_risks  Where mdl_risks=3   and addedby="+str(userId)
        #     strQ+=" union"
        #     strQ+=" select 'None' Mdl_Risk_Label,count(*),4 from Mdl_OverView mdl_overview left join Mdl_Risks mdl_risks on"
        #     strQ+=" mdl_overview.Mdl_Id =mdl_risks.Mdl_Id Where  (mdl_risks is null or mdl_risks='') and mdl_overview.is_tool=0 and mdl_overview.addedby="+str(userId)
        #     strQ+=" order by 3"
        # elif userLevel=="2": ("+str(self.getSubOrdUsers(userId))+")"
        if str(objmaster.checkMRMHead(str(userId)))=="1":
            strQ="select 'High' lbl ,count(*) cnt,1 from  Mdl_Risks mdl_risks ,Mdl_OverView where mdl_risks=1  and Mdl_OverView.Mdl_Id=mdl_risks.Mdl_Id   and  isnull(Is_Decommissioned,0) <>2 and isnull(is_submit,0)<>0 and mdl_risks=1 and Mdl_OverView.addedby in ("+str(self.getSubOrdUsers(userId))+")"
            strQ+=" union"
            strQ+=" select 'Medium' Mdl_Risk_Label,count(*),2 from  Mdl_Risks mdl_risks ,Mdl_OverView where mdl_risks=2  and Mdl_OverView.Mdl_Id=mdl_risks.Mdl_Id   and  isnull(Is_Decommissioned,0) <>2 and isnull(is_submit,0)<>0 and mdl_risks=2 and Mdl_OverView.addedby in ("+str(self.getSubOrdUsers(userId))+")"
            strQ+=" union"
            strQ+=" select 'Low' Mdl_Risk_Label,count(*),3 from  Mdl_Risks mdl_risks ,Mdl_OverView where mdl_risks=3  and Mdl_OverView.Mdl_Id=mdl_risks.Mdl_Id   and  isnull(Is_Decommissioned,0) <>2 and isnull(is_submit,0)<>0 and mdl_risks=3   and Mdl_OverView.addedby in ("+str(self.getSubOrdUsers(userId))+")"
            strQ+=" union"
            strQ+=" select 'None' Mdl_Risk_Label,count(*),4 from Mdl_OverView mdl_overview left join Mdl_Risks mdl_risks on"
            strQ+=" mdl_overview.Mdl_Id =mdl_risks.Mdl_Id Where  (mdl_risks is null or mdl_risks='') and  isnull(Is_Decommissioned,0) <>2 and isnull(is_submit,0)<>0 and mdl_overview.is_tool=0 and mdl_overview.addedby in ("+str(self.getSubOrdUsers(userId))+")"
            strQ+=" order by 3"
        else:
            strQ="select 'High' lbl ,count(*) cnt,1 from  Mdl_Risks mdl_risks ,Mdl_OverView where mdl_risks=1  and Mdl_OverView.Mdl_Id=mdl_risks.Mdl_Id   and  isnull(Is_Decommissioned,0) <>2 and mdl_risks=1 and Mdl_OverView.addedby in ("+str(self.getSubOrdUsers(userId))+")"
            strQ+=" union"
            strQ+=" select 'Medium' Mdl_Risk_Label,count(*),2 from  Mdl_Risks mdl_risks ,Mdl_OverView where mdl_risks=2  and Mdl_OverView.Mdl_Id=mdl_risks.Mdl_Id   and  isnull(Is_Decommissioned,0) <>2 and mdl_risks=2 and Mdl_OverView.addedby in ("+str(self.getSubOrdUsers(userId))+")"
            strQ+=" union"
            strQ+=" select 'Low' Mdl_Risk_Label,count(*),3 from  Mdl_Risks mdl_risks ,Mdl_OverView where mdl_risks=3  and Mdl_OverView.Mdl_Id=mdl_risks.Mdl_Id   and  isnull(Is_Decommissioned,0) <>2  and mdl_risks=3   and Mdl_OverView.addedby in ("+str(self.getSubOrdUsers(userId))+")"
            strQ+=" union"
            strQ+=" select 'None' Mdl_Risk_Label,count(*),4 from Mdl_OverView mdl_overview left join Mdl_Risks mdl_risks on"
            strQ+=" mdl_overview.Mdl_Id =mdl_risks.Mdl_Id Where  (mdl_risks is null or mdl_risks='') and  isnull(Is_Decommissioned,0) <>2  and mdl_overview.is_tool=0 and mdl_overview.addedby in ("+str(self.getSubOrdUsers(userId))+")"
            strQ+=" order by 3" 
        tableResult =self.objdbops.getTable(strQ)
                   
        return tableResult
        
    
    def getModelSrcCntByUserid(self,istool,userId): 
        if str(objmaster.checkMRMHead(str(userId)))=="1":
            strQ="select count(*) cnt,Mdl_Src_Label lbl from mdl_overview ,Model_Source_Master mdl_src"
            strQ+=" where Mdl_Scr_AID=Mdl_Source and  mdl_overview.is_tool="+ str(istool)+" and  isnull(Is_Decommissioned,0) <>2 and isnull(Is_submit,0)<>0  and mdl_overview.addedby in ("+str(self.getSubOrdUsers(userId))+")"
            strQ+=" group by Mdl_Src_Label"
            strQ+=" order by 2" 
        else:
            strQ="select count(*) cnt,Mdl_Src_Label lbl from mdl_overview ,Model_Source_Master mdl_src"
            strQ+=" where Mdl_Scr_AID=Mdl_Source and  mdl_overview.is_tool="+ str(istool)+" and  isnull(Is_Decommissioned,0) <>2 and mdl_overview.addedby in ("+str(self.getSubOrdUsers(userId))+")"
            strQ+=" group by Mdl_Src_Label"
            strQ+=" order by 2" 
         
        return self.objdbops.getTable(strQ)
   
    
    def getModelById(self,mdlId):        
        strQ="select isnull(Mdl_Risk_Label,'') Mdl_Risk_Label,isnull(Intrinsic_Label,'') Intrinsic_Label,"
        strQ+=" isnull(Reliance_Label,'') Reliance_Label,isnull(Materiality_Label,'') Materiality_Label, mdl_overview.*,"
        strQ+=" isnull(mdl_risks.Risk_Mtgn,'') Risk_Mtgn,isnull(mdl_risks.Fair_Lndg,'') Fair_Lndg ,format(mdl_overview.adddate,'MM/dd/yyyy') regdate from("
        strQ+=" select Mdl_Src_Label,Mdl_Use_Freq_Label,Prd_Addr_Label,mdl_oview.*,Mdl_Type_Label,Dept_Label from  Department dept, "         
        strQ+=" Model_Source_Master mdl_src_mst, Mdl_OverView mdl_oview left join Model_Type_Master mdl_ty_mstr on mdl_type=mdl_ty_mstr.Mdl_Type_AID\
                left join Model_Use_Freq_Master mdl_use_freq_mst on  mdl_use_freq_mst.Mdl_Use_Freq_AID=usgFreq\
                left join Prd_Addr_Master prd_addr_mst on  prd_addr_mst.Prd_Addr_AID=prctAddr "
        strQ+=" where   mdl_oview.mdl_id='"+ mdlId +"' and department=dept.Dept_AID and Mdl_Scr_AID=Mdl_Source" 
        strQ+=" )mdl_overview left join"
        strQ+=" ("
        strQ+=" select isnull(Mdl_Risk_Label,'') Mdl_Risk_Label,isnull(Intrinsic_Label,'') Intrinsic_Label,isnull(Reliance_Label,'') Reliance_Label,isnull(Materiality_Label,'') Materiality_Label,mdl_risks.* from  Mdl_Risks mdl_risks left join  Mdl_Risk_Master mdl_risks_mst  "
        strQ+=" on Mdl_Risk_AID=mdl_risks left join Intrinsic_Master on Intrinsic_AID=Intr_Risk" 
        strQ+=" left join Reliance_Master on Reliance_AID=Reliance   left join Materiality_Master on Materiality_AID =Materiality"
        strQ+=" ) mdl_risks"
        strQ+=" on mdl_overview.Mdl_Id =mdl_risks.Mdl_Id  where mdl_overview.mdl_id='"+ mdlId +"'"
        strQ+=" order by mdl_overview.adddate"
        
        tableResult =self.objdbops.getTable(strQ)
        mdldata= tableResult.to_json(orient='index')
        del tableResult
        return json.loads(mdldata)   

    def getTempModelById(self,mdlId):        
        strQ="select isnull(Mdl_Risk_Label,'') Mdl_Risk_Label,isnull(Intrinsic_Label,'') Intrinsic_Label,"
        strQ+=" isnull(Reliance_Label,'') Reliance_Label,isnull(Materiality_Label,'') Materiality_Label, mdl_overview.*,"
        strQ+=" isnull(mdl_risks.Risk_Mtgn,'') Risk_Mtgn,isnull(mdl_risks.Fair_Lndg,'') Fair_Lndg ,format(mdl_overview.adddate,'MM/dd/yyyy') regdate from("
        strQ+=" select Mdl_Src_Label,Mdl_Use_Freq_Label,Prd_Addr_Label,mdl_oview.*,Mdl_Type_Label,Dept_Label from  Department dept, "         
        strQ+=" Model_Source_Master mdl_src_mst, Temp_Mdl_OverView mdl_oview left join Model_Type_Master mdl_ty_mstr on mdl_type=mdl_ty_mstr.Mdl_Type_AID\
                left join Model_Use_Freq_Master mdl_use_freq_mst on  mdl_use_freq_mst.Mdl_Use_Freq_AID=usgFreq\
                left join Prd_Addr_Master prd_addr_mst on  prd_addr_mst.Prd_Addr_AID=prctAddr "
        strQ+=" where   mdl_oview.mdl_id='"+ mdlId +"' and department=dept.Dept_AID and Mdl_Scr_AID=Mdl_Source" 
        strQ+=" )mdl_overview left join"
        strQ+=" ("
        strQ+=" select isnull(Mdl_Risk_Label,'') Mdl_Risk_Label,isnull(Intrinsic_Label,'') Intrinsic_Label,isnull(Reliance_Label,'') Reliance_Label,isnull(Materiality_Label,'') Materiality_Label,mdl_risks.* from  Mdl_Risks mdl_risks left join  Mdl_Risk_Master mdl_risks_mst  "
        strQ+=" on Mdl_Risk_AID=mdl_risks left join Intrinsic_Master on Intrinsic_AID=Intr_Risk" 
        strQ+=" left join Reliance_Master on Reliance_AID=Reliance   left join Materiality_Master on Materiality_AID =Materiality"
        strQ+=" ) mdl_risks"
        strQ+=" on mdl_overview.Mdl_Id =mdl_risks.Mdl_Id  where mdl_overview.mdl_id='"+ mdlId +"'"
        strQ+=" order by mdl_overview.adddate"
        
        tableResult =self.objdbops.getTable(strQ)
        mdldata= tableResult.to_json(orient='index')
        del tableResult
        return json.loads(mdldata)   
    
    def getModelTypeByUserId(self,userId,userLevel):
        # if userLevel =="1":
        #     strQ=" select  Mdl_Type_Label ,count(*) cnt from  "
        #     strQ+=" Mdl_OverView mdl_oview,Model_Type_Master mdl_ty_mstr  "
        #     strQ+=" where mdl_oview.addedby="+str(userId)
        #     strQ+=" and mdl_oview.mdl_type=mdl_ty_mstr.Mdl_Type_AID and mdl_oview.is_tool=0"
        #     strQ+=" group by Mdl_Type_Label"
        # elif userLevel =="2":
        if str(objmaster.checkMRMHead(str(userId)))=="1":
            strQ=" select   isnull(Mdl_Type_Label,'NA') Mdl_Type_Label ,count(*) cnt from  "
            strQ+=" Mdl_OverView mdl_oview left join Model_Type_Master mdl_ty_mstr  on  mdl_oview.mdl_type=mdl_ty_mstr.Mdl_Type_AID where"
            strQ+="   mdl_oview.addedby in ("+str(self.getSubOrdUsers(userId))+")"
            strQ+=" and mdl_oview.is_tool=0 and  isnull(Is_Decommissioned,0) <>2 and isnull(is_submit,0)<>0 "
            strQ+=" group by Mdl_Type_Label" 
        else:
            strQ=" select   isnull(Mdl_Type_Label,'NA') Mdl_Type_Label ,count(*) cnt from  "
            strQ+=" Mdl_OverView mdl_oview left join Model_Type_Master mdl_ty_mstr  on  mdl_oview.mdl_type=mdl_ty_mstr.Mdl_Type_AID where"
            strQ+="   mdl_oview.addedby in ("+str(self.getSubOrdUsers(userId))+")"
            strQ+=" and mdl_oview.is_tool=0 and  isnull(Is_Decommissioned,0) <>2 "
            strQ+=" group by Mdl_Type_Label" 
        tableResult =self.objdbops.getTable(strQ) 
        
        data = {'color': ['info', 'info-300','warning-300','danger-300','success-300','primary']}

        df = pd.DataFrame(data)
        df=df.head(len(tableResult))
        tableResult = pd.concat([tableResult, df], axis=1)
        
        mdldata= tableResult.to_json(orient='index')
        del tableResult
        return json.loads(mdldata)  
    
    def getToolCntByUserId(self,userId,userLevel):
        strQ="" 
        # if userLevel=="1":
        #     strQ=" select   count(*) cnt from  "
        #     strQ+=" Mdl_OverView mdl_oview  "
        #     strQ+=" where mdl_oview.addedby="+str(userId) + " and mdl_oview.is_tool=1" 
        # elif userLevel=="2":
        strQ=" select   count(*) cnt from  "
        strQ+=" Mdl_OverView mdl_oview  "
        strQ+=" where mdl_oview.addedby in ("+str(self.getSubOrdUsers(userId))+") and mdl_oview.is_tool=1" 
        return self.objdbops.getscalar(strQ) 
    
    def getIsModel(self,criteria,qtnsIds):
        isModel=False 
        strQ=" select distinct criteria_aid from [Criteria_Setting] where question_aid in("+str(','.join([str(elem) for elem in qtnsIds ]))+")"        
        tableResult =self.objdbops.getTable(strQ) 
        for index, row in tableResult.iterrows(): 
            dfcriteria=self.objdbops.getTable("select case 	when operator='<>' and val='Yes' Then 'No' when operator='<>' and val='Yes' Then 'No' 	else val end rbval ,val,* from Criteria_Setting where criteria_aid='"+row["criteria_aid"]+"' ")
            logicaloptcnt= dict(dfcriteria['Logical_Opt'].value_counts())
            itrall=logicaloptcnt.get('And')
            for indexcr, rowcr in dfcriteria.iterrows():
                try: 
                    idx=qtnsIds.index(rowcr["Question_AID"])
                    print(itrall,',',rowcr["Question_AID"],',',rowcr["rbval"],',',criteria[idx])
                    if itrall == None and criteria[idx]==rowcr["rbval"]:
                       isModel=True
                       print('a ',rowcr["Criteria_AID"])
                       break 
                    elif criteria[idx]!=rowcr["rbval"]:
                        print('b ',rowcr["Criteria_AID"])
                        isModel=False  
                        break
                    elif criteria[idx]==rowcr["rbval"]:
                        isModel=True           
                        print('c ',rowcr["Criteria_AID"])    
                    
                except Exception as e:
                    print('error',rowcr["Question_AID"])
                    print(e) 
                    isModel=False  
            if isModel==True:
                break
            print('isModel ',isModel)
        return isModel

    def getPerfomanceMonitor(self,MdlId):
        strQ="select Mdl_Montr_Freq_Label ,perf_mon.* from Mdl_Performance_Monitor perf_mon left join Mdl_Montr_Freq freq_mst "
        strQ+=" on Mdl_Montr_Freq_AID=Monr_Freq where mdl_id='"+MdlId+"'"
        tableResult =self.objdbops.getTable(strQ)
        mdldata= tableResult.to_json(orient='index')
        del tableResult
        return json.loads(mdldata)  
    
    def getTempPerfomanceMonitor(self,MdlId):
        strQ="select Mdl_Montr_Freq_Label ,perf_mon.* from Temp_Mdl_Performance_Monitor perf_mon left join Mdl_Montr_Freq freq_mst "
        strQ+=" on Mdl_Montr_Freq_AID=Monr_Freq where mdl_id='"+MdlId+"'"
        tableResult =self.objdbops.getTable(strQ)
        mdldata= tableResult.to_json(orient='index')
        del tableResult
        return json.loads(mdldata)  
    
    def getSubOrdUsers(self,userId):
        if str(self.objdbops.getscalar(" select count(*)  cnt from users u,Department dept where dept.Dept_AID=u.dept_aid and dept.Dept_IsMRM=1 and U_AID='"+ str(userId) +"'"))=="0":
            strQ=" WITH cte ( U_AID, U_Reportto, U_FName)"
            strQ+=" AS"
            strQ+=" ("
            strQ+="     SELECT dept.U_AID, dept.U_Reportto, dept.U_FName "
            strQ+=" FROM  Users u,users dept "
            strQ+="     WHERE u.U_AID='"+ str(userId) +"' and u.Dept_AID=dept.Dept_AID "
            strQ+="   UNION ALL"
            strQ+="     SELECT  e.U_AID,e.U_Reportto, e.U_FName"
            strQ+="     FROM users AS e"
            strQ+="     JOIN cte ON e.U_Reportto = cte.U_AID"
            strQ+=" )"
            strQ+=" SELECT  U_AID "
            strQ+=" FROM cte  "
        else:
            strQ="select U_AID from users "
        tableResult =self.objdbops.getTable(strQ)
        mdlusers=tableResult['U_AID'].tolist()
        mdlusers=','.join([str(elem) for elem in mdlusers])
        del tableResult
        return mdlusers
    
    def getTaskListByUSerid(self,userId): 
         
        strQ="     select  distinct  case trp.U_Type when 'Assignee' then 'Assigned' when 'Approver' then 'For Approval' end 'U_Role', "
        strQ+="     format(end_date,'MM/dd/yyyy') end_dt,tr.*,Task_ApprovalStatus_Label,Task_Priority_Label,Task_Function_Label,Task_Type_label"
        strQ+="       from Task_Relevant_Personnel trp,Task_ApprovalStatus_Master apprlsts, "
        strQ+="     Task_Priority_Master tpm, Task_Function_Master tfm,Task_Type_Master ttm  ,"
        strQ+="     Task_Registration tr left join Mdl_OverView  on Mdl_OverView.Mdl_Id=Link_ID   "
        strQ+="     where tr.Task_ID=trp.Task_ID and (trp.U_Type='Assignee' or trp.U_Type='Approver')   "
        strQ+="     and tr.Approval_Status=apprlsts.Task_ApprovalStatus_AID and tr.Priority=cast(tpm.Task_Priority_AID as int) "
        strQ+="     and tfm.Task_Function_AID=task_function and Task_Type_AID =task_type "
        strQ+="     and u_id in ("+str(self.getSubOrdUsers(userId))+")  "
        strQ+="    and   isnull(Is_Decommissioned,0) <>2  "
        strQ+="     order by 3"
 
        tableResult =self.objdbops.getTable(strQ) 
        if tableResult.empty == False:
            mdldata= tableResult.to_json(orient='index')
            del tableResult
            return json.loads(mdldata) 
        else:
            return ''
        
    def getIssueListByUserId(self,userId):
        strQ="    select distinct  case trp.U_Type when 'Assignee' then 'Assigned' when 'Approver' then 'For Approval' end 'U_Role',format(end_date,'MM/dd/yyyy') end_dt,tr.*,"
        strQ+="   Issue_ApprovalStatus_Label,Issue_Priority_Label,Issue_Function_Label,Issue_Type_label"
        strQ+="   from  Issue_Relevant_Personnel trp,"
        strQ+="   Issue_ApprovalStatus_Master apprlsts, "
        strQ+="   Issue_Priority_Master tpm, issue_Function_Master tfm,Issue_Type_Master ttm ,"
        strQ+="   Issue_Registration tr ,  Mdl_OverView where Mdl_OverView.Mdl_Id=Link_ID and"
        strQ+="   tr.Issue_ID=trp.Issue_ID  and (trp.U_Type='Assignee'"
        strQ+="   or trp.U_Type='Approver')     "
        strQ+="   and tr.Approval_Status=apprlsts.Issue_ApprovalStatus_AID and tr.Priority=cast(tpm.Issue_Priority_AID as int)   "
        strQ+="   and tfm.issue_Function_AID=issue_function and Issue_Type_AID =Issue_type    "
        strQ+="   and u_id in  ("+str(self.getSubOrdUsers(userId))+") "
        strQ+="   and     isnull(Is_Decommissioned,0) <>2   order by 1"
        
        tableResult =self.objdbops.getTable(strQ) 
        if tableResult.empty == False:
            mdldata= tableResult.to_json(orient='index')
            del tableResult
            return json.loads(mdldata) 
        else:
            return ''
    
    def get_notifications(self,uid):
        strQ=" SELECT  Notification_Id ,Notification_From  ,Notification_To ,Utility ,Notification_Trigger ,Is_Visible, "
        strQ+=" concat( format(Create_Date,'hh:mm tt'),' ',DATENAME(MONTH, Create_Date) + ' ' + CAST(DAY(Create_Date) AS VARCHAR(2))"
        strQ+=" + ', ' + CAST(YEAR(Create_Date) AS VARCHAR(4)))  Create_Date  ,concat(u.U_FName,' ',u.U_LName) sentfrom ,concat(u2.U_FName,' ',u2.U_LName) sentto"
        strQ+=" FROM Notification_Details nd,Users u ,Users u2"
        strQ+=" where notification_from=u.U_AID and Notification_to=u2.U_AID and Is_Visible=1"
        strQ+=" and Notification_To="+str(uid)
        strQ+=" order by 1 desc"
        tableResult =self.objdbops.getTable(strQ) 
        if tableResult.empty == False:
            mdldata= tableResult.to_json(orient='index')
            del tableResult
            return json.loads(mdldata) 
        else:
            return 'None'
        
    def insertICQRatings(self,qtnid,yesno,doc,comments,uid,reviewid):
        if(str(self.objdbops.getscalar("select count(*) from ICQ_Question_Rating_Data where Review_id='"+reviewid+"' and Question_AID ='"+qtnid+"'"))=="0"):
            strQ=" INSERT INTO   ICQ_Question_Rating_Data "
            strQ+=" (  "
            strQ+="  Question_AID ,Review_id "
            strQ+=" , Rating_Yes_NO "
            strQ+=" , Doc_Yes_No "
            strQ+=" , Comments "
            strQ+=" , AddedBy "
            strQ+=" , AddDate )"
            strQ+=" VALUES("
            strQ+=" '"+qtnid+"' , '"+reviewid+"'"
            if(yesno!=""):
                strQ+=" ,'"+yesno+"'"
            else:
                strQ+=" ,null"
            if(doc!=""):
                strQ+=" ,'"+doc+"'"
            else:
                strQ+=" ,null"
            if(comments!=""):
                strQ+=" ,'"+comments+"'"
            else:
                strQ+=" ,null" 
            strQ+=" ,'"+str(uid)+"'"        
            strQ+=" ,GETDATE())" 
            self.objdbops.insertRow(strQ)
        else:
            strQ=" update ICQ_Question_Rating_Data set"              
            if(yesno!=""):
                strQ+=" Rating_Yes_NO='"+yesno+"'"
            else:
                strQ+=" Rating_Yes_NO=null"           
            if(doc!=""):
                strQ+=" ,Doc_Yes_No='"+doc+"'"
            else:
                strQ+=" ,Doc_Yes_No=null" 
            if(comments!=""):
                strQ+=" ,Comments='"+comments+"'"
            else:
                strQ+=" ,Comments=null" 
            strQ+=" ,  UpdatedBy='"+str(uid)+"'"  
            strQ+=" ,   UpdateDate=GETDATE() where  Review_id='"+reviewid+"' and Question_AID ='"+qtnid+"'"    
            self.objdbops.insertRow(strQ)

    def submitRatings(self,rvid):
        strQ="insert into ICQ_Question_Rating_Data_final  (Review_id"
        strQ+="  ,Question_AID"
        strQ+="   ,Rating_Yes_NO"
        strQ+="   ,Doc_Yes_No"
        strQ+="  ,Comments"
        strQ+="   ,AddedBy"
        strQ+="   ,AddDate"
        strQ+="   ,UpdatedBy"
        strQ+="   ,UpdateDate)"
        strQ+="   select   Review_id"
        strQ+="   ,Question_AID"
        strQ+="   ,Rating_Yes_NO"
        strQ+="   ,Doc_Yes_No"
        strQ+="   ,Comments"
        strQ+="   ,AddedBy"
        strQ+="   ,AddDate"
        strQ+="   ,UpdatedBy"
        strQ+="   ,UpdateDate from ICQ_Question_Rating_Data where Review_id='"+rvid+"'"
        self.objdbops.insertRow(strQ)

    def updateICQRatingsFinal(self,qtnid,yesno,doc,comments,uid,reviewid):
        if(str(self.objdbops.getscalar("select count(*) from ICQ_Question_Rating_Data_Final where Review_id='"+reviewid+"' and Question_AID ='"+qtnid+"'"))=="0"):
            strQ=" INSERT INTO   ICQ_Question_Rating_Data_Final "
            strQ+=" (  "
            strQ+="  Question_AID ,Review_id "
            strQ+=" , Rating_Yes_NO "
            strQ+=" , Doc_Yes_No "
            strQ+=" , Comments "
            strQ+=" , AddedBy "
            strQ+=" , AddDate )"
            strQ+=" VALUES("
            strQ+=" '"+qtnid+"' , '"+reviewid+"'"
            if(yesno!=""):
                strQ+=" ,'"+yesno+"'"
            else:
                strQ+=" ,null"
            if(doc!=""):
                strQ+=" ,'"+doc+"'"
            else:
                strQ+=" ,null"
            if(comments!=""):
                strQ+=" ,'"+comments+"'"
            else:
                strQ+=" ,null" 
            strQ+=" ,'"+str(uid)+"'"        
            strQ+=" ,GETDATE())" 
            self.objdbops.insertRow(strQ)
        else:
            strQ=" update ICQ_Question_Rating_Data_Final set"              
            if(yesno!=""):
                strQ+=" Rating_Yes_NO='"+yesno+"'"
            else:
                strQ+=" Rating_Yes_NO=null"           
            if(doc!=""):
                strQ+=" ,Doc_Yes_No='"+doc+"'"
            else:
                strQ+=" ,Doc_Yes_No=null" 
            if(comments!=""):
                strQ+=" ,Comments='"+comments+"'"
            else:
                strQ+=" ,Comments=null" 
            strQ+=" ,  UpdatedBy='"+str(uid)+"'"  
            strQ+=" ,   UpdateDate=GETDATE() where  Review_id='"+reviewid+"' and Question_AID ='"+qtnid+"'"   
        
            self.objdbops.insertRow(strQ)

    def getICQRatings(self,rvid):
        strQ="select case when Denominator =0 then 0 else  round((cast(Numerator as float)/cast(Denominator as float)) *100,0) end from (select sumRatingYes+sumDocYes Denominator from ("
        strQ+=" select sum([Rating_Yes]) sumRatingYes from ICQ_Question_Rating where question_aid not in("
        strQ+="  select question_aid from ICQ_Question_Rating_Data_Final where rating_yes_no='NA'"
        strQ+="  ))ratingyes,"
        strQ+="     (select sum([Doc_Yes]) sumDocYes from ICQ_Question_Rating where question_aid not in("
        strQ+="  select question_aid from ICQ_Question_Rating_Data_Final where Doc_yes_no='NA'"
        strQ+="  ))docyes)Denominator,"
        strQ+="  ("
        strQ+="  select sumYes+sumYesDoc-sumNo-sumNoDoc Numerator from"
        strQ+="  (select isnull( sum(case isnull(final.rating_yes_no,'No') when 'Yes' then [Rating_Yes] else 0 end),0) sumYes"
        strQ+=" from  ICQ_Question_Master qtnmst "
        strQ+=" left join ICQ_Question_Rating ratingmst"
        strQ+=" on qtnmst.question_aid=ratingmst.question_aid left join ICQ_Question_Rating_Data_Final final"
        strQ+=" on qtnmst.question_aid=final.question_aid "
        strQ+=" where isnull(final.rating_yes_no,'No')='Yes' and review_id='"+ rvid +"')sumYes,"
        strQ+="  (select sum(isnull(Rating_No,0)) sumNO from"
        strQ+=" (select question_aid from ICQ_Question_Master"
        strQ+=" except"
        strQ+=" select Question_aid from ICQ_Question_Rating_Data_Final where  review_id='"+ rvid +"'"
        strQ+=" and (rating_yes_no='Yes' or rating_yes_no='NA'))ratingNo left join ICQ_Question_Rating ratingmst"
        strQ+=" on ratingNo.question_aid=ratingmst.question_aid"
        strQ+=" )sumNo,"
        strQ+=" (select isnull(sum (case isnull(final.Doc_Yes_No,'No') when 'Yes' then Doc_Yes else 0 end),0) sumYesDoc"
        strQ+=" from  ICQ_Question_Master qtnmst "
        strQ+=" left join ICQ_Question_Rating ratingmst"
        strQ+=" on qtnmst.question_aid=ratingmst.question_aid left join ICQ_Question_Rating_Data_Final final"
        strQ+=" on qtnmst.question_aid=final.question_aid "
        strQ+=" where isnull(final.Doc_Yes_No,'No')='Yes'  and review_id='"+ rvid +"')sumYesDoc,"
        strQ+=" (select sum(isnull(Doc_No,0)) sumNoDoc from"
        strQ+=" (select question_aid from ICQ_Question_Master"
        strQ+=" except"
        strQ+=" select Question_aid from ICQ_Question_Rating_Data_Final where  review_id='"+ rvid +"'"
        strQ+=" and (doc_yes_no='Yes' or doc_yes_no='NA'))ratingNo left join ICQ_Question_Rating ratingmst"
        strQ+=" on ratingNo.question_aid=ratingmst.question_aid)sumNoDoc"
        strQ+=" )Numerator" 
       
        ratings=self.objdbops.getscalar(strQ) 
        if(ratings==None):
            ratings="-"
        return ratings
    
    def isICQPublished(self):
        ratings='-'
        maxid=   str(self.objdbops.getscalar("select ISNULL(max(ICQS_AID),0) review_id from  ICQ_Setting")) 
        if(str(self.objdbops.getscalar("select publish from ICQ_Setting where ICQS_AID= "+maxid))=="1"):            
            ratings=self.getICQRatings(maxid) 
        return ratings
    
    def deCommModel(self,mdl_id,comment,fileNm,sts): #to be updated on server
        if sts=="1":
            strQ="update Mdl_OverView set Is_Decommissioned="+str(sts)+" ,Decomm_Comment_Owner='"+comment+"',Decomm_FIle='"+fileNm+"' where Mdl_Id='"+mdl_id+"'"
        else:
            strQ="update Mdl_OverView set Is_Decommissioned="+str(sts)+" ,Decomm_Comment_Mrm='"+comment+"' where Mdl_Id='"+mdl_id+"'"
        
        return self.objdbops.insertRow(strQ)

    def checkPendingTaskIssue(self,mdl_id):
        strQ=" select case when  (select count(*) from Task_Registration  where Approval_Status<>2  and Link_ID ='"+mdl_id+"')>0 then 1 "
        strQ+=" when (select count(*) from Issue_Registration  where Approval_Status<>2  and Link_ID ='"+mdl_id+"')>0 then 1 "
        strQ+=" else 0 end 'pending_tasks'"
         
        return self.objdbops.getscalar(strQ)  
    
    def getDecommDoc(self,mdl_id):
        strQ=" select decomm_file,decomm_comment_owner from Mdl_OverView where Mdl_Id='"+mdl_id+"'"
        tableResult =self.objdbops.getTable(strQ) 
        if tableResult.empty == False:
            mdldata= tableResult.to_json(orient='index')
            del tableResult
            return json.loads(mdldata) 
        else:
            return 'None'
        
    def markasRead(self,id):
        strQ=" update Notification_Details set Is_Visible =0 where Notification_Id="+str(id)
        return self.objdbops.insertRow(strQ)

    def updateApprovedData(self,mdlId,tblName,colName):    
        if(tblName=='Temp_Mdl_OverView'):
            strQ="UPDATE A\
                SET "+colName+" = B."+colName+",[UpdatedBy]=b.[UpdatedBy],[UpdateDate]=getdate()\
                FROM Mdl_OverView A\
                JOIN Temp_Mdl_OverView B\
                    ON A.mdl_id = B.mdl_id\
                WHERE a.mdl_id='"+mdlId+"'"
            self.objdbops.insertRow(strQ) 
        elif(tblName=='Temp_Mdl_Performance_Monitor'):
            strQ="UPDATE A\
            SET "+colName+" = B."+colName+",[UpdatedBy]=b.[UpdatedBy],[UpdateDate]=getdate()\
            FROM Mdl_Performance_Monitor A\
            JOIN Temp_Mdl_Performance_Monitor B\
                ON A.mdl_id = B.mdl_id\
            WHERE a.mdl_id='"+mdlId+"'"
            self.objdbops.insertRow(strQ) 
        elif(tblName=='Temp_Mdl_Risks'):
            strQ="UPDATE A\
            SET [Mdl_Risks] = B.[Mdl_Risks] ,"+colName+"=b."+colName+",[UpdatedBy]=b.[UpdatedBy],[UpdateDate]=getdate()\
            FROM Mdl_Risks A\
            JOIN Temp_Mdl_Risks B\
                ON A.mdl_id = B.mdl_id\
            WHERE a.mdl_id='"+mdlId+"'"
            self.objdbops.insertRow(strQ) 
        elif(tblName=='Temp_Mdl_Dependencies'):
            strQ="UPDATE A\
            SET "+colName+" = B."+colName+",[UpdatedBy]=b.[UpdatedBy],[UpdateDate]=getdate()\
            FROM Mdl_Dependencies A\
            JOIN Temp_Mdl_Dependencies B\
                ON A.mdl_id = B.mdl_id\
            WHERE a.mdl_id='"+mdlId+"'"
            self.objdbops.insertRow(strQ) 
        
    def getIssuesByMonthOrQtr(self,intervaltype,uid,is_mrm,from_dt='',to_dt='',sts=''):  
        strQ="" 
        
        if intervaltype=="Qtr":   
            strQ="select   count(*) cnt, DATENAME(Quarter, End_Date) Qtr,FORMAT(End_Date,'yy') enddt_yr,tpm.Issue_Priority_Label  from "
            strQ+="     Issue_ApprovalStatus_Master apprlsts," 
            strQ+="      Issue_Priority_Master tpm, issue_Function_Master tfm,Issue_Type_Master ttm , "
            strQ+="      Issue_Registration tr ,  Mdl_OverView where Mdl_OverView.Mdl_Id=Link_ID "
            strQ+="      and tr.Approval_Status=apprlsts.Issue_ApprovalStatus_AID and tr.Priority=cast(tpm.Issue_Priority_AID as int) " 
            strQ+="      and tfm.issue_Function_AID=issue_function and Issue_Type_AID =Issue_type  "    
            if is_mrm == "No":
                strQ +=" and Mdl_OverView.addedby in ("+str(self.getSubOrdUsers(uid))+")"  
            if len(sts)>0:
                strQ +=" and Issue_ApprovalStatus_Label in ("+(','.join([ f"'{x}'" for x in sts]))+")" 
            if from_dt!='' and to_dt!='':
                    strQ+=" and End_Date between '"+from_dt+"' and '"+to_dt+"'"
            strQ+="       and     isnull(Is_Decommissioned,0) <>2"
            strQ+="      group by DATENAME(Quarter, End_Date),FORMAT(End_Date,'yy') ,tpm.Issue_Priority_Label"
            strQ+="      order by  DATENAME(Quarter, End_Date),FORMAT(End_Date,'yy')"
        elif intervaltype=="Week":   
            strQ="select   count(*) cnt, DATENAME(Week, End_Date) Qtr,FORMAT(End_Date,'yy') enddt_yr,tpm.Issue_Priority_Label  from "
            strQ+="     Issue_ApprovalStatus_Master apprlsts," 
            strQ+="      Issue_Priority_Master tpm, issue_Function_Master tfm,Issue_Type_Master ttm , "
            strQ+="      Issue_Registration tr ,  Mdl_OverView where Mdl_OverView.Mdl_Id=Link_ID "
            strQ+="      and tr.Approval_Status=apprlsts.Issue_ApprovalStatus_AID and tr.Priority=cast(tpm.Issue_Priority_AID as int) " 
            strQ+="      and tfm.issue_Function_AID=issue_function and Issue_Type_AID =Issue_type  "    
            if is_mrm == "No":
                strQ +=" and Mdl_OverView.addedby in ("+str(self.getSubOrdUsers(uid))+")"    
            strQ+="       and     isnull(Is_Decommissioned,0) <>2"
            if len(sts)>0:
                strQ +=" and Issue_ApprovalStatus_Label in ("+(','.join([ f"'{x}'" for x in sts]))+")" 
            if from_dt!='' and to_dt!='':
                    strQ+=" and End_Date between '"+from_dt+"' and '"+to_dt+"'"
            strQ+="      group by DATENAME(Week, End_Date),FORMAT(End_Date,'yy') ,tpm.Issue_Priority_Label"
            strQ+="      order by  DATENAME(Week, End_Date),FORMAT(End_Date,'yy')"
        else:
            strQ="select  count(*) cnt, DATENAME(mm, End_Date) enddt_mn,Month(end_date) Qtr,FORMAT(End_Date,'yy') enddt_yr,tpm.Issue_Priority_Label  from "
            strQ+="     Issue_ApprovalStatus_Master apprlsts," 
            strQ+="      Issue_Priority_Master tpm, issue_Function_Master tfm,Issue_Type_Master ttm , "
            strQ+="      Issue_Registration tr ,  Mdl_OverView where Mdl_OverView.Mdl_Id=Link_ID "
            strQ+="      and tr.Approval_Status=apprlsts.Issue_ApprovalStatus_AID and tr.Priority=cast(tpm.Issue_Priority_AID as int) " 
            strQ+="      and tfm.issue_Function_AID=issue_function and Issue_Type_AID =Issue_type  "   
            if is_mrm == "No":
                strQ +=" and Mdl_OverView.addedby in ("+str(self.getSubOrdUsers(uid))+")"     
            if from_dt!='' and to_dt!='':
                strQ+=" and End_Date between '"+from_dt+"' and '"+to_dt+"'"
            if len(sts)>0:
                strQ +=" and Issue_ApprovalStatus_Label in ("+(','.join([ f"'{x}'" for x in sts]))+")" 
            strQ+="       and     isnull(Is_Decommissioned,0) <>2"
            strQ+="      group by  DATENAME(mm, End_Date),FORMAT(End_Date,'yy') ,Month(end_date),tpm.Issue_Priority_Label"
            strQ+="      order by  Month(end_date),FORMAT(End_Date,'yy')"
        
        print("strq-------------",strQ)
        tableResult =self.objdbops.getTable(strQ) 
        arrQtrs=[]
        arrPriority=[] 
        if  tableResult.empty == False :
            tableResult['enddt_yr'] = tableResult['enddt_yr'].astype(int)
            tableResult['Qtr'] = tableResult['Qtr'].astype(int)
            if intervaltype=="Qtr":                 
                min_year=tableResult['enddt_yr'].min()  
                maxyear=tableResult['enddt_yr'].max() 
                arrHigh=[]
                arrMed=[]
                arrLow=[] 
                for iyear in range(int(min_year),int(maxyear)+1): 
                    for irow in range(1,5):
                        dfhigh=tableResult.loc[(tableResult['Qtr'] == irow) & (tableResult['enddt_yr'] == iyear) & (tableResult['Issue_Priority_Label'] == 'High')]
                        if dfhigh.empty: 
                            arrHigh.append(0)
                        else: 
                            cnt=int(dfhigh['cnt'].values[0]) 
                            arrHigh.append(cnt) 
                        dfmedium=tableResult.loc[(tableResult['Qtr'] == irow) & (tableResult['enddt_yr'] == iyear) & (tableResult['Issue_Priority_Label'] == 'Medium')]
                        if dfmedium.empty: 
                            arrMed.append(0)
                        else: 
                            cnt=int(dfmedium['cnt'].values[0]) 
                            arrMed.append(cnt) 

                        dflow=tableResult.loc[(tableResult['Qtr'] == irow) & (tableResult['enddt_yr'] == iyear) & (tableResult['Issue_Priority_Label'] == 'Low')]
                        if dflow.empty: 
                            arrLow.append(0)
                        else: 
                            cnt=int(dflow['cnt'].values[0]) 
                            arrLow.append(cnt) 
                        
                        arrQtrs.append("Q" +str(irow)+" "+str(str(iyear)))
            elif intervaltype=="Week":                 
                min_year=tableResult['enddt_yr'].min()  
                maxyear=tableResult['enddt_yr'].max() 
                arrHigh=[]
                arrMed=[]
                arrLow=[]
                for iyear in range(int(min_year),int(maxyear)+1): 
                    for irow in range(1,52):
                        dfhigh=tableResult.loc[(tableResult['Qtr'] == irow) & (tableResult['Issue_Priority_Label'] == 'High')]
                        if dfhigh.empty: 
                            arrHigh.append(0)
                        else: 
                            cnt=int(dfhigh['cnt'].values[0]) 
                            arrHigh.append(cnt) 
                        dfmedium=tableResult.loc[(tableResult['Qtr'] == irow) & (tableResult['Issue_Priority_Label'] == 'Medium')]
                        if dfmedium.empty: 
                            arrMed.append(0)
                        else: 
                            cnt=int(dfmedium['cnt'].values[0]) 
                            arrMed.append(cnt) 

                        dflow=tableResult.loc[(tableResult['Qtr'] == irow) & (tableResult['Issue_Priority_Label'] == 'Low')]
                        if dflow.empty: 
                            arrLow.append(0)
                        else: 
                            cnt=int(dflow['cnt'].values[0]) 
                            arrLow.append(cnt) 
                        
                        arrQtrs.append("Week" +str(irow)+" "+str(str(iyear)))
            
            else:
                import calendar  
                min_year=tableResult['enddt_yr'].min()  
                maxyear=tableResult['enddt_yr'].max()
                import numpy as np
                arrHigh=[]
                arrMed=[]
                arrLow=[]
                arrQtrs=[]
                arrPriority=[]
                for iyear in range(int(min_year),int(maxyear)+1): 
                    for irow in range(1,13):
                        dfhigh=tableResult.loc[(tableResult['Qtr'] == irow) & (tableResult['Issue_Priority_Label'] == 'High')]
                        if dfhigh.empty: 
                            arrHigh.append(0)
                        else: 
                            cnt=int(dfhigh['cnt'].values[0]) 
                            arrHigh.append(cnt) 
                        dfmedium=tableResult.loc[(tableResult['Qtr'] == irow) & (tableResult['Issue_Priority_Label'] == 'Medium')]
                        if dfmedium.empty: 
                            arrMed.append(0)
                        else: 
                            cnt=int(dfmedium['cnt'].values[0]) 
                            arrMed.append(cnt) 

                        dflow=tableResult.loc[(tableResult['Qtr'] == irow) & (tableResult['Issue_Priority_Label'] == 'Low')]
                        if dflow.empty: 
                            arrLow.append(0)
                        else: 
                            cnt=int(dflow['cnt'].values[0]) 
                            arrLow.append(cnt) 
                        
                        arrQtrs.append(calendar.month_abbr[irow]+" "+str(str(iyear)))
            arrPriority.append(arrHigh)  
            arrPriority.append(arrMed)  
            arrPriority.append(arrLow)         
        data={'data':arrPriority,'series':arrQtrs} 
        return data
    

    def getFindingsCntByElements(self):
        strQ=" select highcnt.element_text 'Validation_Element', highcnt.cntval 'High',medcnt.cntval 'Medium',lowcnt.cntval 'Low',\
            (highcnt.cntval+medcnt.cntval+lowcnt.cntval) Total from (select Element_text,Mdl_Risk_Label,count(risk) cntval  from Finding_val_elements\
            left join validation_findings on   Finding_val_elements.Element_AID=validation_element and risk=3\
            left join Mdl_Risk_Master on Mdl_Risk_Master.Risk_Val=validation_findings.Risk and   Risk_Val=3\
            group by Mdl_Risk_Label,Element_text) highcnt,\
            (select Element_text,Mdl_Risk_Label,count(risk) cntval from Finding_val_elements\
            left join validation_findings on   Finding_val_elements.Element_AID=validation_element and risk=2\
            left join Mdl_Risk_Master on Mdl_Risk_Master.Risk_Val=validation_findings.Risk and   Risk_Val=2\
            group by Mdl_Risk_Label,Element_text) medcnt,\
            (select Element_text,Mdl_Risk_Label,count(risk) cntval from Finding_val_elements\
            left join validation_findings on   Finding_val_elements.Element_AID=validation_element and risk=1\
            left join Mdl_Risk_Master on Mdl_Risk_Master.Risk_Val=validation_findings.Risk and   Risk_Val=1\
            group by Mdl_Risk_Label,Element_text) lowcnt\
            where highcnt.Element_text=medcnt.Element_text and medcnt.Element_text=lowcnt.Element_text\
            order by 1"
        tableResult =self.objdbops.getTable(strQ) 
      
        tableResult.loc[len(tableResult.index)] = ['Total', tableResult['High'].sum(), tableResult['Medium'].sum(),tableResult['Low'].sum(),(tableResult['High'].sum()+tableResult['Medium'].sum()+tableResult['Low'].sum())]
        mdldata= tableResult.to_json(orient='index')
        del tableResult
        return json.loads(mdldata) 
    
    def getFindingsCntByCategory(self):
        strQ=" select highcnt.Category_text 'Validation_Category', highcnt.cntval 'High',medcnt.cntval 'Medium',lowcnt.cntval 'Low',\
                (highcnt.cntval+medcnt.cntval+lowcnt.cntval) Total from \
                (select Category_text,Mdl_Risk_Label,count(risk) cntval  from Findings_Category\
                left join validation_findings on   Findings_Category.Category_AID=Category and risk=3\
                left join Mdl_Risk_Master on Mdl_Risk_Master.Risk_Val=validation_findings.Risk and   Risk_Val=3\
                group by Mdl_Risk_Label,Category_text) highcnt,\
                (select Category_text,Mdl_Risk_Label,count(risk) cntval  from Findings_Category\
                left join validation_findings on   Findings_Category.Category_AID=Category and risk=2\
                left join Mdl_Risk_Master on Mdl_Risk_Master.Risk_Val=validation_findings.Risk and   Risk_Val=2\
                group by Mdl_Risk_Label,Category_text) medcnt,\
                (select Category_text,Mdl_Risk_Label,count(risk) cntval from Findings_Category\
                left join validation_findings on   Findings_Category.Category_AID=Category and risk=1\
                left join Mdl_Risk_Master on Mdl_Risk_Master.Risk_Val=validation_findings.Risk and   Risk_Val=1\
                group by Mdl_Risk_Label,Category_text) lowcnt\
                where highcnt.Category_text=medcnt.Category_text and medcnt.Category_text=lowcnt.Category_text\
                order by 1"
        tableResult =self.objdbops.getTable(strQ)        
        tableResult.loc[len(tableResult.index)] = ['Total', tableResult['High'].sum(), tableResult['Medium'].sum(),tableResult['Low'].sum(),(tableResult['High'].sum()+tableResult['Medium'].sum()+tableResult['Low'].sum())]
        mdldata= tableResult.to_json(orient='index')
        del tableResult
        return json.loads(mdldata) 
    
    def getFilteredIssueListByUserId(self,userId,intervaltype,value,priority):
        strQ="    select distinct  case trp.U_Type when 'Assignee' then 'Assigned' when 'Approver' then 'For Approval' end 'U_Role',format(end_date,'MM/dd/yyyy') end_dt,tr.*,"
        strQ+="   Issue_ApprovalStatus_Label,Issue_Priority_Label,Issue_Function_Label,Issue_Type_label"
        strQ+="   from  Issue_Relevant_Personnel trp,"
        strQ+="   Issue_ApprovalStatus_Master apprlsts, "
        strQ+="   Issue_Priority_Master tpm, issue_Function_Master tfm,Issue_Type_Master ttm ,"
        strQ+="   Issue_Registration tr ,  Mdl_OverView where Mdl_OverView.Mdl_Id=Link_ID and"
        strQ+="   tr.Issue_ID=trp.Issue_ID  and (trp.U_Type='Assignee'"
        strQ+="   or trp.U_Type='Approver')     "
        strQ+="   and tr.Approval_Status=apprlsts.Issue_ApprovalStatus_AID and tr.Priority=cast(tpm.Issue_Priority_AID as int)   "
        strQ+="   and tfm.issue_Function_AID=issue_function and Issue_Type_AID =Issue_type    "
        strQ+="   and u_id in  ("+str(self.getSubOrdUsers(userId))+") "
        strQ+="   and Issue_Priority_Label='"+priority +"'"
        if(intervaltype =="Qtr"):
            strQ+="  and concat('Q',DATENAME(Quarter, End_Date),' ',FORMAT(End_Date,'yy'))='"+value+"'"
        else:
            strQ+="  and Format(End_Date,'MMM yy')='"+value+"'"
        strQ+="   and     isnull(Is_Decommissioned,0) <>2   order by 1" 
        tableResult =self.objdbops.getTable(strQ) 
        if tableResult.empty == False:
            mdldata= tableResult.to_json(orient='index')
            del tableResult
            return json.loads(mdldata) 
        else:
            return ''
  
    
class MdlOverviewCls:
    Mdl_Id :str
    Mdl_Cnt :str
    Mdl_Major_Ver :str
    Mdl_Minor_Ver :str
    isnew :str
    is_tool :str
    Department :str
    Func :str
    Reg_Dt :str
    Prm_Name :str
    Sec_Name :str
    Mdl_Source :str
    Mdl_Type :str
    Mdl_Absct :str
    Mdl_objective :str
    Mdl_Appl :str
    Mdl_Risk_Anls :str
    PrctAddr :str
    UsgFreq :str
    AddedBy :str 
    objdbops =None

    def __init__(self,Mdl_Id,Mdl_Cnt ,Mdl_Major_Ver , Mdl_Minor_Ver ,isnew ,is_tool ,Department
                 ,Func,Prm_Name, Sec_Name,Mdl_Source,Mdl_Type,Mdl_Absct,Mdl_objective,Mdl_Appl,
                 Mdl_Risk_Anls,PrctAddr,UsgFreq,AddedBy):
        self.objdbops =dbops()
        self.Mdl_Id=Mdl_Id
        self.Mdl_Cnt =Mdl_Cnt
        self.Mdl_Major_Ver =Mdl_Major_Ver
        self.Mdl_Minor_Ver =Mdl_Minor_Ver
        self.isnew =isnew
        self.is_tool =is_tool
        self.Department =Department
        self.Func =Func 
        self.Prm_Name =Prm_Name
        self.Sec_Name =Sec_Name
        self.Mdl_Source =Mdl_Source
        self.Mdl_Type =Mdl_Type
        self.Mdl_Absct =Mdl_Absct
        self.Mdl_objective=Mdl_objective
        self.Mdl_Appl =Mdl_Appl
        self.Mdl_Risk_Anls =Mdl_Risk_Anls
        self.PrctAddr =PrctAddr
        self.UsgFreq =UsgFreq
        self.AddedBy =AddedBy

    def insertMdlOverview(self):       
        newcnt=0
        if(self.isnew=="1"):
            if self.is_tool=="1":
                newcnt=self.objdbops.getscalar("select format(isnull(max(mdl_cnt),0) +1,'00') newmdlcnt from  Mdl_OverView where Mdl_Major_Ver =1 and Mdl_Minor_Ver=0 and is_tool=1")
            
                self.Mdl_Id="T"+str(newcnt)+"0100"
            else:
                newcnt=self.objdbops.getscalar("select format(isnull(max(mdl_cnt),0) +1,'00') newmdlcnt from  Mdl_OverView where Mdl_Major_Ver =1 and Mdl_Minor_Ver=0 and is_tool=0")
                self.Mdl_Id="M"+str(newcnt)+"0100"
            self.Mdl_Major_Ver="1"
            self.Mdl_Minor_Ver="0" 

            
        strQ="insert into Mdl_OverView ( Mdl_Id "
        strQ+=" , Mdl_Cnt "
        strQ+=" , Mdl_Major_Ver "
        strQ+=" , Mdl_Minor_Ver "
        strQ+=" , isnewupdate "
        strQ+=" , is_tool "
        strQ+=" , Department "
        strQ+=" , Func "
        strQ+=" , Reg_Dt "
        strQ+=" , Prm_Name "
        strQ+=" , Sec_Name "
        strQ+=" , Mdl_Source "
        strQ+=" , Mdl_Type "
        strQ+=" , Mdl_Absct "
        strQ+=" , Mdl_objective "
        strQ+=" , Mdl_Appl "
        strQ+=" , Mdl_Risk_Anls "
        strQ+=" , PrctAddr "
        strQ+=" , UsgFreq "
        strQ+=" , AddedBy "
        strQ+="  , AddDate "
        strQ+=" )"
        strQ+=" values"
        strQ+="  ("
        strQ+=" '"+ self.Mdl_Id +"'"
        strQ+=" ,  "+str(newcnt)
        strQ+=" ,  "+ self.Mdl_Major_Ver
        strQ+=" ,  "+ self.Mdl_Minor_Ver
        strQ+=" , "+self.isnew
        strQ+=" ,  "+ self.is_tool
        strQ+=" ,  "+ str(self.Department)
        strQ+=" ,  "+"null" if str(self.Func)=="" else  str(self.Func)
        strQ+=" , getdate() " 
        strQ+=" , '"+ self.Prm_Name + "'"
        strQ+=" , '"+ self.Sec_Name +"'"
        strQ+=" , '"+ self.Mdl_Source +"'"
        strQ+=" , '"+ self.Mdl_Type +"'"
        strQ+=" , '"+ self.Mdl_Absct +"'"
        strQ+=" , '"+ self.Mdl_objective +"'"
        strQ+=" , '"+ self.Mdl_Appl +"'"
        strQ+=" , '"+ self.Mdl_Risk_Anls +"'"
        strQ+=" , '"+ self.PrctAddr +"'"
        strQ+=" , '"+ self.UsgFreq +"'"
        strQ+=" , '"+ str(self.AddedBy) +"'"
        strQ+=" ,getdate()"
        strQ+=" )" 
        self.objdbops.insertRow(strQ)
        return self.Mdl_Id
    
    
        
class ModelRisks:
    Mdl_Id :str
    Mdl_Risks :str
    Intr_Risk :str
    Reliance :str
    Materiality :str
    Risk_Mtgn :str
    Fair_Lndg :str
    AddedBy :str

    def __init__(self,Mdl_Id,Mdl_Risks, Intr_Risk,Reliance,Materiality,Risk_Mtgn,Fair_Lndg,AddedBy):
        self.objdbops =dbops()
        self.Mdl_Id=Mdl_Id
        self.Mdl_Risks=Mdl_Risks
        self.Intr_Risk=Intr_Risk
        self.Reliance=Reliance
        self.Materiality=Materiality
        self.Risk_Mtgn=Risk_Mtgn
        self.Fair_Lndg=Fair_Lndg
        self.AddedBy=AddedBy

    def insertModelRisk(self):
        strQ="INSERT INTO Mdl_Risks "
        strQ +="   ( Mdl_Id "
        strQ +="     , Mdl_Risks "
        strQ +="      , Intr_Risk "
        strQ +="      , Reliance "
        strQ +="      , Materiality "
        strQ +="      , Risk_Mtgn "
        strQ +="   , Fair_Lndg "
        strQ +="      , AddedBy "
        strQ +="     , AddDate  )"
        strQ +="   VALUES"
        strQ +="      ('"+ self.Mdl_Id +"'"
        strQ +="      ,'"+ self.Mdl_Risks +"'"
        strQ +="      ,'"+ self.Intr_Risk +"'"
        strQ +="      ,'"+ self.Reliance +"'"
        strQ +="      ,'"+ self.Materiality +"'"
        strQ +="      ,'"+ self.Risk_Mtgn +"'"
        strQ +="      ,'"+ self.Fair_Lndg +"'"
        strQ +="      ,'"+ str(self.AddedBy) +"'"
        strQ +="   ,getdate())"
        self.objdbops.insertRow(strQ)
         
class MdlRelevantPersonnelFuncs: 
    def __init__(self):
        self.objdbops =dbops()

    def getRelevantPersonal(self,mdlId,UserType):
        mdlusers=""
        strQ=" select concat(Users.U_FName ,' ', users.U_LName) uname from Mdl_Relevant_personnel mdl_users,Users where mdl_id='"+ mdlId +"'"
        strQ+=" and mdl_users.u_id= users.u_Aid and u_type='"+ UserType +"'"
        dtusers=  self.objdbops.getTable(strQ) 
        if dtusers.empty == False:
            mdlusers=dtusers['uname'].tolist()
            mdlusers=', '.join([str(elem) for elem in mdlusers])
        del dtusers
        return mdlusers

    def getTempRelevantPersonal(self,mdlId,UserType):
        mdlusers=""
        strQ=" select concat(Users.U_FName ,' ', users.U_LName) uname from temp_Mdl_Relevant_personnel mdl_users,Users where mdl_id='"+ mdlId +"'"
        strQ+=" and mdl_users.u_id= users.u_Aid and u_type='"+ UserType +"'"
        dtusers=  self.objdbops.getTable(strQ) 
        if dtusers.empty == False:
            mdlusers=dtusers['uname'].tolist()
            mdlusers=', '.join([str(elem) for elem in mdlusers])
        del dtusers
        return mdlusers

    
         

    def insertUsers(self,MdlId,UType,UIds,Addedby):
         
        for uid in UIds:
            strQ=" INSERT INTO  Mdl_Relevant_personnel "
            strQ+=" ( Mdl_Id "
            strQ+=" , U_Type "
            strQ+=" , U_ID "
            strQ+=" , AddedBy "
            strQ+=" , AddDate  )"
            strQ+=" VALUES"
            strQ+=" ('"+ MdlId +"'"
            strQ+=" ,'"+ UType +"'"
            strQ+=" ,'"+ uid+"'"
            strQ+=" ,'"+ str(Addedby) +"'"
            strQ+=" , getdate() )" 
            self.objdbops.insertRow(strQ)

class MdlDependenciesCls:
    def __init__(self):
        self.objdbops =dbops()

    def insertMdlDepencies(self,MdlId,UpstrmMdl,DwstrmMdl,Addedby):
        self.objdbops =dbops()
        strQ=" INSERT INTO  Mdl_Dependencies "
        strQ+=" ( Mdl_Id "
        strQ+=" , UpstrmMdl "
        strQ+=" , DwstrmMdl "
        strQ+=" , AddedBy "
        strQ+=" , AddDate  )"
        strQ+=" VALUES"
        strQ+=" ('"+ MdlId +"'"
        strQ+=" ,'"+ UpstrmMdl +"'"
        strQ+=" ,'"+ DwstrmMdl+"'"
        strQ+=" ,'"+ str(Addedby) +"'"
        strQ+=" , getdate() )" 
        self.objdbops.insertRow(strQ)

    def getMdlDependencies(self,MdlId):
        # strQ="select Mdl_Dwstream_Label,Mdl_Upstream_Label  from Mdl_Dependencies mdl_depn left join Mdl_Dwstream mdl_dwstr  on"
        # strQ+=" DwstrmMdl= Mdl_Dwstream_AID left join Mdl_Upstream    on"
        # strQ+=" Mdl_Upstream_AID=DwstrmMdl where mdl_id='" + MdlId + "' "
        strQ =" select DwstrmMdl Mdl_Dwstream_Label,UpstrmMdl Mdl_Upstream_Label  from Mdl_Dependencies mdl_depn where mdl_id='" + MdlId + "' "
        tableResult =self.objdbops.getTable(strQ) 
        if tableResult.empty == False:
            mdldata= tableResult.to_json(orient='index')
            del tableResult
            return json.loads(mdldata) 
        else:
            return '' 
        
    def getTempMdlDependencies(self,MdlId):
        # strQ="select Mdl_Dwstream_Label,Mdl_Upstream_Label  from Mdl_Dependencies mdl_depn left join Mdl_Dwstream mdl_dwstr  on"
        # strQ+=" DwstrmMdl= Mdl_Dwstream_AID left join Mdl_Upstream    on"
        # strQ+=" Mdl_Upstream_AID=DwstrmMdl where mdl_id='" + MdlId + "' "
        strQ =" select DwstrmMdl Mdl_Dwstream_Label,UpstrmMdl Mdl_Upstream_Label  from Temp_Mdl_Dependencies mdl_depn where mdl_id='" + MdlId + "' "
        tableResult =self.objdbops.getTable(strQ) 
        if tableResult.empty == False:
            mdldata= tableResult.to_json(orient='index')
            del tableResult
            return json.loads(mdldata) 
        else:
            return '' 

class MdlPerformanceMonitoring:
    Mdl_Id :str
    Approach :str
    Monr_Freq :str
    Mon_Mtrcs :str
    Tgr_Evt :str
    Lst_Tgr_Dt :str
    Lst_Tgr_Mtgn_Dt :str
    Tgr_Evt_Mtgn :str
    AddedBy :str

    def __init__(self,Mdl_Id,Approach,Monr_Freq,Mon_Mtrcs,Tgr_Evt,Lst_Tgr_Dt,Lst_Tgr_Mtgn_Dt,Tgr_Evt_Mtgn,AddedBy) -> None:
        self.objdbops =dbops()
        self.Mdl_Id=Mdl_Id
        self.Approach=Approach
        self.Monr_Freq=Monr_Freq
        self.Mon_Mtrcs=Mon_Mtrcs
        self.Tgr_Evt=Tgr_Evt
        self.Lst_Tgr_Dt=Lst_Tgr_Dt
        self.Lst_Tgr_Mtgn_Dt=Lst_Tgr_Mtgn_Dt
        self.Tgr_Evt_Mtgn=Tgr_Evt_Mtgn
        self.AddedBy=AddedBy
        
    def insertPerfomanceMonitor(self):
        strQ=" INSERT INTO   Mdl_Performance_Monitor"
        strQ+="   ( Mdl_Id "
        strQ+="   , Approach "
        strQ+="   , Monr_Freq "
        strQ+="   , Monr_Mtrcs "
        strQ+="   , Tgr_Evt "
        strQ+="   , Lst_Tgr_Dt "
        strQ+="   , Lst_Tgr_Mtgn_Dt "
        strQ+="   , Tgr_Evt_Mtgn "
        strQ+="   , AddedBy "
        strQ+="   , AddDate )"
        strQ+=" VALUES ("
        strQ+="  '"+ self.Mdl_Id +"'"
        strQ+="   ,'"+ self.Approach +"'"
        strQ+="   ,'"+ self.Monr_Freq +"'"
        strQ+="   ,'"+ self.Mon_Mtrcs +"'"
        strQ+="   ,'"+ self.Tgr_Evt +"'"
        strQ+="   ,'"+ self.Lst_Tgr_Dt +"'"
        strQ+="   ,'"+ self.Lst_Tgr_Mtgn_Dt +"'"
        strQ+="   ,'"+ self.Tgr_Evt_Mtgn +"'"
        strQ+="   ,'"+ str(self.AddedBy) +"'"
        strQ+="   ,getdate())"
        self.objdbops.insertRow(strQ)

class MdlDocs:
    def __init__(self):
        self.objdbops =dbops()

    def inserDocs(self,Mdl_Id,Doc_Type,Doc_Name,AddedBy):
        strQ="insert into Mdl_Documents ("
        strQ+=" Mdl_Id  , "
        strQ+=" Mdl_Doc_Type ,"
        strQ+=" Mdl_Doc_Name   ,"
        strQ+=" AddedBy  ,"
        strQ+=" AddDate "
        strQ+=" ) "
        strQ+=" values("
        strQ+=" '"+Mdl_Id+"', "
        strQ+=" '"+str(Doc_Type)+"' ,"
        strQ+=" '"+Doc_Name+"'   ,"
        strQ+=" "+AddedBy+"  ,"
        strQ+=" getdate()" 
        strQ+=" )" 
        self.objdbops.insertRow(strQ)


    def getMdlDocs(self,Mdl_Id):
        strQ="select   case Mdl_Doc_Type  when 1 then 'Model Development'"
        strQ+="    when 2 then 'User Manual'"
        strQ+="    when 3 then 'Model Data'"
        strQ+="    when 4 then 'Model Code'"
        strQ+="    when 5 then 'User Acceptance Testing'"
        strQ+="    when 6 then 'Technical Manual'"
        strQ+="    when 7 then 'Onboarding Documents' "
        strQ+="    when 8 then 'Conform to Enterprize Production Policy'" 
        strQ+="    when 9 then 'Parellel Runs'"
        strQ+="    when 10 then 'User Acceptance Testing'"
        strQ+="    when 11 then 'Integration within Production Systems'" 
        strQ+="    when 12 then 'Model Approval Process'" 
        strQ+="    when 13 then 'Contingency plans(Backup-on-site and off-site)'"
        strQ+="   when 14 then 'Change Controls'"
        strQ+="    when 15 then 'IT Security(Confirm)'"
        strQ+="    end Mdl_Doc_Type,Mdl_Doc_Name  from Mdl_Documents where mdl_id='" + Mdl_Id + "' "
        tableResult =self.objdbops.getTable(strQ)  
        return tableResult

class UserDeatilsSerializers(serializers.ModelSerializer):
    # to accept either username or email
    utype = serializers.CharField()
    dept = serializers.CharField()
    def getUserDeatils(self,data):
        utype=data.get("utype", None)
        dept=data.get("dept", None)
        strq= "select rs.r_aid,r_label, 'block' sts from user_access ua , Resources rs where rs.R_AID=ua.r_AID and  ua.uc_AID='"+str(utype)+"' "
        strq=strq + " union "
        strq=strq + " select *,'none' from( "
        strq=strq + " SELECT r_aid,r_label from Resources "
        strq=strq + " except "
        strq=strq + " select rs.r_aid,r_label   "
        strq=strq + " from user_access ua , Resources rs where rs.R_AID=ua.r_AID "
        strq=strq + " and  ua.uc_AID='"+ str(utype)+ "' )a " 
        strq=strq + " union "
        strq=strq + " select count(*),'Dept Head',case when count(*)=1 then 'block' else 'none' end from user_category where uc_is_depthead=1 and uc_AID='"+ str(utype)+ "' "
        strq=strq + " union "
        strq=strq +  "select rs.r_aid,r_label, 'block' sts from user_access ua , Resources rs where rs.R_AID=ua.r_AID and  ua.uc_AID='"+str(utype)+"' and ua.UA_dept='"+str(dept)+"' "
        
        tableResult =self.objdbops.getTable(strq)     
        return tableResult