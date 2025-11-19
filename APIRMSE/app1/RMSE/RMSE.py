from app1.DAL.dboperations import dbops
import json 
import pandas as pd

class RMSEModel:
    objdbops =None

    def __init__(self):
        self.objdbops=dbops()

    def insertPdfFileData(self,doc,uid):        
        strQ="INSERT INTO   Pdf_Summary_Documents ( Doc_Name, AddedBy,AddDate)  VALUES    ( '"+doc+"'  , '"+str(uid)+"'  ,getdate() )"
        return self.objdbops.insertRow(strQ)
    
    def getDocById(self,uid):        
        tableResult =self.objdbops.getTable("select * from Pdf_Summary_Documents where addedby='"+str(uid)+"'")# and UC_AID='"+str(utype)+"'
        userlst= tableResult.to_json(orient='index')
        return json.loads(userlst)
    
    def insertPdfResp(self,doc,uid,respLbl,resp,query):
        strQ="INSERT INTO  Pdf_Summary_Response ( Doc_Id, Resp_Label, AddedBy, AddDate,Pdf_Resp,Query)  VALUES ( '"+doc+"'  , '"+respLbl+"'  , '"+str(uid)+"'  ,getdate() , '"+resp+"','"+ query + "')"
       
        return self.objdbops.insertRow(strQ)
    
    def getModelsbyId(self,uid):
        if str(self.objdbops.getscalar("select count(*) cnt from users u,department dept ,User_Category uc where  isnull(Dept_IsMRM,0)=1 and u.Dept_AID=dept.Dept_AID and uc.UC_AID=u.UC_AID and UC_Is_DeptHead=1 and u_aid="+str(uid)))=="1":
            strQ="select distinct model_id from  Question_Allocation "# and UC_AID='"+str(utype)+"'  
        else:
            strQ="select distinct model_id from  Question_Allocation where allocated_to='"+str(uid)+"'"
        tableResult =self.objdbops.getTable(strQ)# and UC_AID='"+str(utype)+"'
        userlst= tableResult.to_json(orient='index')
        return json.loads(userlst)
        
    def getModelQtns(self,mdl_id):
        d2 = {}
        strQ="select distinct a.* from("
        strQ += " select '1' lvl,Section_AID,Section_Label,'-' Sub_Section_AID,'-' Sub_Section_Label,"
        strQ += " '-' Sub_Sub_Section_AID,'-' Sub_Sub_Section_Label,'-' Sub_Sub_Sub_Section_AID,'-' Sub_Sub_Sub_Section_Label "     
        strQ += " from Ques_Sections "
        strQ += " )a ,Question_Allocation alloc ,Question_Ques_Master qqm where qqm.section_aid=a.section_aid and alloc.question_aid=qqm.Question_AID  and model_id='"+mdl_id+"'"# and a.section_aid='"+str(sectionid)+"'"
        strQ += " order by  a.Section_AID"#,cast(a.Sub_Section_AID as int),cast(a.Sub_Sub_Section_AID as int),cast(a.Sub_Sub_Sub_Section_AID as int)"
        tableResult =self.objdbops.getTable(strQ)
          
        arrayidx=0 
        if tableResult.empty == False:
            for ind in tableResult.index: 
                strQtn=""
                strQtn+=" select  case when  len(qtnmst.Section_AID )<>  0 and  (qtnmst.Sub_Section_AID) is null then 1 "
                strQtn+=" when  len(qtnmst.Sub_Section_AID)<>  0 and  (qtnmst.Sub_Sub_Section_AID) is null then 2"
                strQtn+=" when len(qtnmst.Sub_Sub_Section_AID)<>0 and  (qtnmst.Sub_Sub_Sub_Section_AID)  is null then 3 "
                strQtn+=" when len(qtnmst.Sub_Sub_Sub_Section_AID)<>  0 then 4  else 0 end lvl,  sec.Section_AID,isnull(s_sec.Sub_Section_AID,'0') Sub_Section_AID,"
                strQtn+=" isnull(ss_sec.Sub_Sub_Section_AID,'0') Sub_Sub_Section_AID,qtnmst.Question_AID ,"
                strQtn+=" qtnmst.Question_Label ,isnull(sec.Section_Label,'') Section_Label, isnull(s_sec.Sub_Section_Label,'') Sub_Section_Label,isnull(ss_sec.Sub_Sub_Section_Label,'') Sub_Sub_Section_Label    from "
                strQtn+=" Question_Allocation alloc,Question_Ques_Master qtnmst left join Ques_Sections sec on "
                strQtn+=" qtnmst.section_aid=sec.section_aid left join"
                strQtn+=" Ques_Sub_Sections s_sec  on qtnmst.sub_section_aid=s_sec.sub_section_aid left join"
                strQtn+=" Ques_Sub_Sub_Sections ss_sec on qtnmst.sub_sub_section_aid=ss_sec.sub_sub_section_aid " 
                strQtn+=" where sec.section_aid="+str(tableResult['Section_AID'][ind])+" and alloc.question_aid=qtnmst.Question_AID  and model_id='"+mdl_id+"'"
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
            # print(d2)
        return d2 # json.dumps(d2)    
    

    def getQtnResp(self,mdl_id,qtn_id,uid):
        strQ=" SELECT  Response_id,FORMAT (resp.AddDate,'hh:mm tt  MMM dd, yyyy') createdt ,[Comments],\
            concat(u.U_FName,' ',u.U_LName) addedby,upper(concat(left(u.U_FName,1),left(u.U_LName,1))) uinitials, case when resp.AddedBy="+ str(uid) +" then 'S' else 'R' end msgcss\
            from  Question_Ques_Response resp,users u\
            where u.U_AID=resp.AddedBy and [Mdl_id]='"+mdl_id+"' and [Question_AID]="+str(qtn_id)+"\
            order by [Response_id]"   
        tableResult =self.objdbops.getTable(strQ)
        userlst= tableResult.to_json(orient='index')
        return json.loads(userlst)
    
    def insertResp(self,mdl_id,qtn_id,uid,comment,isupdate,resp_id):
        strQ=""
        if(str(isupdate)=="0"):
            strQ=" INSERT INTO  Question_Ques_Response ( Mdl_id, Question_AID, Comments , AddedBy , AddDate) VALUES  ( '"+mdl_id+"' ,"+str(qtn_id)+"  , '"+comment.replace("'","''")+"' , "+ str(uid) +" , getdate())"
        else:
            strQ="update Question_Ques_Response set Comments= '"+comment.replace("'","''")+"' , UpdatedBy = "+ str(uid) +" , UpdateDate =getdate()  where Response_id="+str(resp_id)
      
        return self.objdbops.insertRow(strQ)
    
    def getQtnRespById(self,resp_id):
        return self.objdbops.getscalar("select Comments from Question_Ques_Response where Response_id="+str(resp_id))
    
    def insertAnsr(self,mdl_id,qtn_id,uid,comment):
        strQ=""   
        if str(self.objdbops.getscalar("select count(*) from  Question_Ques_Answer where  Mdl_id= '"+mdl_id+"' and Question_AID="+str(qtn_id)))=="0":    
            strQ=" INSERT INTO  Question_Ques_Answer ( Mdl_id, Question_AID, Answer , AddedBy , AddDate) VALUES  ( '"+mdl_id+"' ,"+str(qtn_id)+"  , '"+comment.replace("'","''")+"' , "+ str(uid) +" , getdate())"        
        else:
            strQ=" update  Question_Ques_Answer  set Answer = '"+comment.replace("'","''")+"' UpdatedBy = "+ str(uid) +" , UpdateDate =getdate()  where Mdl_id= '"+mdl_id+"' and Question_AID="+str(qtn_id)
        return self.objdbops.insertRow(strQ)
    
    def getAnsr(self,mdl_id,qtn_id):
        strQ=""   
        return self.objdbops.getscalar("select Answer from  Question_Ques_Answer where  Mdl_id= '"+mdl_id+"' and Question_AID="+str(qtn_id))
    
    def getAllTasksByUser(self,uid):
        strQ="SELECT   distinct case when end_date<getdate() then  format(getdate(),'yyyy-MM-dd')  else format(end_date,'yyyy-MM-dd') end end_date,"
        strQ +="    case  when format(end_date,'yyyy-MM-dd')< format(getdate(),'yyyy-MM-dd') then  'text-danger'   when datediff(d,getdate(),end_date) <8 then 'text-warning'" 
        strQ +="     when datediff(d,getdate(),end_date) >7 then 'text-success' end css,abs(datediff(d,getdate(),end_date))datedif,taskReg.Task_ID,Task_Name  FROM  Task_Relevant_Personnel taskUsers,"
        strQ +="     Task_Registration taskReg  where taskReg.Task_ID=taskUsers.Task_ID and U_id="+str(uid)
        tableResult =self.objdbops.getTable(strQ)
        taskLst=  tableResult.to_json(orient='index')
        return json.loads(taskLst)
    
    def checkUserRole(self,uid,task_id):
        return self.objdbops.getscalar("select min(u_type) from Task_Relevant_Personnel where U_id="+ str(uid)+" and task_id='"+ str(task_id)+"' group by  task_id  ")
     
    def getAllIssuesByUser(self,uid):
        tableResult =self.objdbops.getTable("SELECT   distinct format(end_date,'yyyy-MM-dd') end_date,issueReg.Issue_ID  FROM  Issue_Relevant_Personnel issueUsers,\
                                            Issue_Registration issueReg  where issueReg.Issue_ID=issueUsers.Issue_ID and U_id="+str(uid))
        issueLst=  tableResult.to_json(orient='index')
        print("issueLst",issueLst)
        return json.loads(issueLst)

    def checkUserRole_Issue(self,uid,issue_id):
        return self.objdbops.getscalar("select min(u_type) from Issue_Relevant_Personnel where U_id="+ str(uid)+" and issue_id='"+ str(issue_id)+"' group by  issue_id  ")
    

    def insertAuditChatResp(self,mdl_id,qtn_id,uid,comment,isupdate,resp_id):
        strQ=""
        if(str(isupdate)=="0"):
            strQ=" INSERT INTO  Audit_Reg_Compl_Chat ( Mdl_id, Compl_AID, Comment , AddedBy , AddDate) VALUES  ( '"+mdl_id+"' ,"+str(qtn_id)+"  , '"+comment.replace("'","''")+"' , "+ str(uid) +" , getdate())"
        else:
            strQ="update Audit_Reg_Compl_Chat set Comment= '"+comment.replace("'","''")+"' , UpdatedBy = "+ str(uid) +" , UpdateDate =getdate()  where Compl_Resp_AID="+str(resp_id)
      
        return self.objdbops.insertRow(strQ)