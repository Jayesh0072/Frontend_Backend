from app1.DAL.dboperations import dbops
import json 
from app1.Adm_Utils.Masters import MasterTbls
from app1.models import *
objmaster=MasterTbls()

class Validation:
    objdbops =None

    def __init__(self):
        self.objdbops=dbops()

    def assignValidation(self,validationType,assignTo,mdlId,addedBy,department_aid,originator_id,priorityLbl="High"):
        task_id_lst = []
        
        for colval in validationType: 
            dept_obj = Department.objects.get(dept_aid=department_aid)
            department = dept_obj.dept_label
            user_obj = Users.objects.get(u_aid = originator_id)
            originator = user_obj.u_fname + " " + user_obj.u_lname
            task_function= None
            task_type_obj = TaskTypeMaster.objects.get(task_type_label = "Model")
            task_type=task_type_obj.task_type_aid
            task_type_lbl = ModelValidationTypeMaster.objects.get(mdl_val_type_aid = colval['AID'])
            req_for_name = task_type_lbl.mdl_val_type_label
            SubTasktype = SubTasktypeMaster.objects.filter(sub_task_type_label=req_for_name).first()
            if  SubTasktype == None:
                sub_task_type =None
            else:
                sub_task_type = SubTasktype.sub_task_type_aid

            task_registration_count=TaskRegistration.objects.filter(link_id=mdlId,task_major_version="1",task_minor_version="0").count()
            
            task_max=task_registration_count + 1
            task_id=mdlId +"T"+ str(task_max) +"0100"
            task_id_dict = {}
            task_id_dict['AID'] = colval['AID']
            task_id_dict['task_id'] = task_id
            task_id_lst.append(task_id_dict)
            link_id=mdlId
            priority_obj=TaskPriorityMaster.objects.get(task_priority_label=priorityLbl)
            priority=priority_obj.task_priority_aid    
            end_date=colval['End_date']
            import datetime
            from datetime import date
            end_date= datetime.datetime.strptime(end_date, '%m/%d/%Y') 
            
             
            completion_status=0
            approval_obj = TaskApprovalstatusMaster.objects.get(task_approvalstatus_label = "Pending")
            approval_status= approval_obj.task_approvalstatus_aid  

            task_registration_obj=TaskRegistration(task_id=task_id,task_name="Model Validation",department=department,originator=originator,task_function=None,
                                               registration_date=date.today(),task_type=task_type,sub_task_type=sub_task_type,
                                               priority=priority,end_date=end_date,completion_status=completion_status,
                                               approval_status=approval_status,task_major_version="1",
                                               task_minor_version="0",addedby=addedBy,adddate=date.today(),
                                               link_id=link_id
                                               )
            task_registration_obj.save() 
            relevant_personnel_obj=Task_Relevant_Personnel(u_type="Originator",u_id=addedBy,
                                                                task=task_registration_obj,addedby=addedBy,adddate=date.today())
            relevant_personnel_obj.save()
            relevant_personnel_obj=Task_Relevant_Personnel(u_type="Approver",u_id=addedBy,
                                                                task=task_registration_obj,addedby=addedBy,adddate=date.today())
            relevant_personnel_obj.save() 

            task_summery_obj=TaskSummery(task_summery="Model validation "+task_type_lbl.mdl_val_type_label+" assigned." ,
                                                     task_registration=task_registration_obj,addedby=addedBy,adddate=date.today())
            task_summery_obj.save()
            
            task_assignee_thread_lst = []
                
            for user in assignTo:                 
                strQ="INSERT INTO Validation_AssignTo "
                strQ+=" ( Mdl_Id "
                strQ+=" , Validation_Task_Type  "
                strQ+=" , U_AID  "
                strQ+=" , Notify  "
                strQ+=" , AddedBy  "
                strQ+=" , AddDate   ) "
                strQ+=" VALUES ( "
                strQ+=" '"+mdlId+"' "
                strQ+=" ,'"+str(colval["AID"])+"' "
                strQ+=" ,'"+str(user["UID"])+"' "
                strQ+=" ,1 "
                strQ+=" ,'"+str(addedBy)+"' "
                strQ+=" ,getdate() ) "
                self.objdbops.insertRow(strQ)

                relevant_personnel_obj=Task_Relevant_Personnel(u_type="Assignee",u_id=user["UID"],
                                                     task=task_registration_obj,addedby=addedBy,adddate=date.today())
                relevant_personnel_obj.save() 
                #notification code
                notification_trigger="New task registered - "+task_id
                objmaster.insert_notification(addedBy,user["UID"],"Task",notification_trigger,1) 
                thread_id=objmaster.thread_creation(addedBy,user["UID"])
                task_assignee_thread_lst.append({"from": str(addedBy), "to": str(user["UID"]),"thread_id":str(thread_id)})               
        return task_id_lst
    
    def getAssiged(self,mdlId):
        strQ="SELECT mdl_id,Validation_Task_Type,STRING_AGG( ISNULL(concat(U_FName ,' ', U_LName), ' '), ',') As users  ,	 format(end_date,'MM/dd/yyyy')  End_Date,tr.Task_ID "
        strQ+=" From  Validation_AssignTo va, Users, Task_Registration tr ,Model_Validation_Type_Master mvtm ,   Sub_Tasktype_Master stm   where users.U_AID =va.u_aid and mdl_id='"+mdlId+"'"
        strQ+=" and tr.Link_ID=va.Mdl_Id  and va.Validation_Task_Type=mvtm.Mdl_Val_Type_AID and mvtm.Mdl_Val_Type_Label=stm.Sub_Task_Type_Label  and stm.Sub_Task_Type_AID=tr.Sub_Task_Type "
        strQ+=" group by  mdl_id,Validation_Task_Type ,tr.End_Date,tr.Task_ID"
        
        tableResult =self.objdbops.getTable(strQ)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult)   
    
    def getVTMenus(self,mdlId,uid):
        strQ="select mdl_val_type_label from Validation_AssignTo va,Model_Validation_Type_Master mvtm,"
        strQ+=" Sub_Tasktype_Master stm where  mdl_id='"+mdlId+"'  and  U_AID="+str(uid)
        strQ+=" and   mvtm.Mdl_Val_Type_AID=va.Validation_Task_Type"
        strQ+=" and mvtm.Mdl_Val_Type_Label=stm.Sub_Task_Type_Label "
        
        tableResult =self.objdbops.getTable(strQ)
        tableResult= tableResult.to_json(orient='records')
        return json.loads(tableResult)   
    
    def getVTNotifications(self,uid):        
        strQ=" SELECT  FORMAT (va.AddDate,'hh:mm tt  MMM dd, yyyy') createdt ,[Mdl_Val_Type_Label] from  [Validation_AssignTo] va,"
        strQ+=" Model_Validation_Type_Master mvtm where mvtm.Mdl_Val_Type_AID = va.Validation_Task_Type and u_aid='"+str(uid)+"'"
        strQ+=" order by va.adddate desc"
        tableResult =self.objdbops.getTable(strQ)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult) 
    
    def getVTModels(self,uid):        
        strQ=" SELECT   distinct Mdl_Id from  Validation_AssignTo  where  u_AID='"+str(uid)+"'"  
        tableResult =self.objdbops.getTable(strQ)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult) 

    def getVTModelsSegments(self,mdlid):        
        strQ="select Rulename,Query_Rule from Query_Builder_Filter where model_id='"+ mdlid +"'"  
        tableResult =self.objdbops.getTable(strQ)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult) 
    
    def getSelectedModel(self,uid): 
        return self.objdbops.getscalar("SELECT [Mdl_Id] FROM [Validation_Model_Selection] where   [U_AID]="+str(uid)+"")
    
    def getModelDocs(self,mdlId):
        strQ="select   case Mdl_Doc_Type  when 1 then 'Model Development'"
        strQ+="    when 2 then 'User Manual'"
        strQ+="    when 3 then 'Model Data'"
        strQ+="    when 4 then 'Model Code'"
        strQ+="    when 5 then 'User Acceptance Testing'"
        strQ+="    when 6 then 'Technical Manual'"
        strQ+="    when 7 then 'Onboarding Documents' "
        strQ+="    when 8 then 'Conform to Enterprise Production Policy'" 
        strQ+="    when 9 then 'Parallel Runs'"
        strQ+="    when 10 then 'User Acceptance Testing'"
        strQ+="    when 11 then 'Integration within Production Systems'" 
        strQ+="    when 12 then 'Model Approval Process'" 
        strQ+="    when 13 then 'Contingency plans (Backup -on-site and off-site)'"
        strQ+="   when 14 then 'Change Controls'"
        strQ+="    when 15 then 'IT Security (Confirm)'"
        strQ+="    end Mdl_Doc_Type,Mdl_Doc_Name  from Mdl_Documents where mdl_id='" + mdlId + "' "  
        tableResult =self.objdbops.getTable(strQ)
        tableResult= tableResult.to_json(orient='index')
        return json.loads(tableResult) 
    
    def getMdlData(self,mdlId):        
        return self.objdbops.getscalar("SELECT  Mdl_Doc_Name  FROM Mdl_Documents where Mdl_Id='"+mdlId+"' and Mdl_Doc_Type=3")
    
    def getMdlCode(self,mdlId):
        return self.objdbops.getscalar("SELECT  Mdl_Doc_Name  FROM Mdl_Documents where Mdl_Id='"+mdlId+"' and Mdl_Doc_Type=4")
    
    def autoCreateTask(self,assignTo,mdlId,addedBy,originator_id,end_date,dept_id,task_name="",priority="High"):
        task_id_lst = []
        dept_obj = Department.objects.get(dept_aid=dept_id)
        department = dept_obj.dept_label
        user_obj = Users.objects.get(u_aid = originator_id)
        originator = user_obj.u_fname + " " + user_obj.u_lname
      
        task_type_obj = TaskTypeMaster.objects.get(task_type_label = "Model")
        task_type=task_type_obj.task_type_aid    
        sub_task_type =None
        

        task_registration_count=TaskRegistration.objects.filter(link_id=mdlId,task_major_version="1",task_minor_version="0").count()
        
        task_max=task_registration_count + 1
        task_id=mdlId +"T"+ str(task_max) +"0100"
     
        link_id=mdlId
        priority_obj=TaskPriorityMaster.objects.get(task_priority_label=priority)
        priority=priority_obj.task_priority_aid       
        end_date=end_date
        import datetime
        from datetime import date
        end_date= datetime.datetime.strptime(end_date, '%m/%d/%Y') 
        
            
        completion_status=0
        approval_obj = TaskApprovalstatusMaster.objects.get(task_approvalstatus_label = "Pending")
        approval_status= approval_obj.task_approvalstatus_aid  

        task_registration_obj=TaskRegistration(task_id=task_id,task_name=task_name,department=department,originator=originator,task_function=None,
                                            registration_date=date.today(),task_type=task_type,sub_task_type=sub_task_type,
                                            priority=priority,end_date=end_date,completion_status=completion_status,
                                            approval_status=approval_status,task_major_version="1",
                                            task_minor_version="0",addedby=addedBy,adddate=date.today(),
                                            link_id=link_id
                                            )
        task_registration_obj.save() 
        relevant_personnel_obj=Task_Relevant_Personnel(u_type="Originator",u_id=addedBy,
                                                            task=task_registration_obj,addedby=addedBy,adddate=date.today())
        relevant_personnel_obj.save()
        relevant_personnel_obj=Task_Relevant_Personnel(u_type="Approver",u_id=addedBy,
                                                            task=task_registration_obj,addedby=addedBy,adddate=date.today())
        relevant_personnel_obj.save() 
        
        task_assignee_thread_lst = []
            
        for user in assignTo:    
            relevant_personnel_obj=Task_Relevant_Personnel(u_type="Assignee",u_id=user,
                                                    task=task_registration_obj,addedby=addedBy,adddate=date.today())
            relevant_personnel_obj.save() 
            #notification code
            notification_trigger="New task registered - "+task_id
            objmaster.insert_notification(addedBy,user,"Task",notification_trigger,1) 
            thread_id=objmaster.thread_creation(addedBy,user)
            task_assignee_thread_lst.append({"from": str(addedBy), "to": str(user),"thread_id":str(thread_id)})               
        return task_id_lst
    