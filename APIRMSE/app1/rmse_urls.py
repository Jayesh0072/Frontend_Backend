from django.urls import path


from .views import *
from .rmseviews import *
from .tasks_Issues import task_approver,task_assignee,checkUserRole_Issue,issue_assignee,issue_approver,allocate_icq,save_allocation
urlpatterns = [
    path('task-registration/',TaskRegistrationAPI.as_view(),name="TaskRegistrationsView"),  
    path('department/',DepartmentAPI.as_view(),name='DepartmentView'),
    path('task-relevant/',Task_Relevant_PersonnelAPI.as_view(),name='TaskRelevantPersonnelView'),
    path('task-summery/',TaskSummeryAPI.as_view(),name="TaskSummeryView"),
    path('alert/',AlertAPI.as_view(),name='AlertView'),
    path('issue-registration/',IssueRegistrationAPI.as_view(),name="IssueRegistrationView"),
    path('issue-relevant-personnel/',IssueRelevantPersonnelAPI.as_view(),name="IssueRelevantPersonnelView"),
    path('issue-summery/',IssueSummeryAPI.as_view(),name="IssueSummeryView"),
    path('modelOverview/',ModelOverviewAPI.as_view(),name="ModelOverview"),
    path('issue-type-master/',Issue_Type_MasterAPI.as_view(),name="Issue_Type_MasterView"),
    path('sub-issue-type-master/',Sub_Issue_Type_MasterAPI.as_view(),name='Sub_Issue_Type_MasterView'),
    path('task-priority-master/',TaskPriorityMasterAPI.as_view(),name='task_priority_masterView'),
    path('task-function-master/',TaskFunctionMasterAPI.as_view(),name='task_function_masterView'),
    path('task-type-master/',TaskTypeMasterAPI.as_view(),name="TaskTypeMasterView"),
    path('task-approval-status-master/',TaskApprovalstatusMasterAPI.as_view(),name='TaskApprovalstatusmasterView'),
    path('informaion/',InformationAPI.as_view(),name='InformationView'),
    path('sub-task-type-master/',SubTasktypeMasterAPI.as_view(),name='sub-task-type-masterView'),
    path('dashboard-content-master/',DashboardContentMasterAPI.as_view(),name='dashboard-content-masterview'),
    path('user-dashboard-conter-master/',UserDashboardContentMasterAPI.as_view(),name='user-dashboard-content-master'),
    

    path('UserCategory/',UserCategoryAPI.as_view(),name='UserCategory'),
    path('addUser/', AddUser.as_view(), name="register"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),

    path('dashboard/',Dashboard.as_view(),name="dashboard"),
    path('projectsDetails/',projectsDetails.as_view(),name="projectsDetails"),
    path('getMdlDetailsById/',getMdlDetailsById.as_view(),name='getMdlDetailsById'),
    path('checkPendingTasksIssues/',checkPendingTasksIssues.as_view(),name='checkPendingTasksIssues'),
    path('getTasks/',getTasks.as_view(),name='getTasks'),
    path('task_approver/',task_approver.as_view(),name='task_approver'),
    path('task_assignee/',task_assignee.as_view(),name='task_assignee'),
    path('getIssues/',getIssues.as_view(),name='getIssues'),
    path('checkUserRole_Issue/',checkUserRole_Issue.as_view(),name='checkUserRole_Issue'),
    path('issue_assignee/',issue_assignee.as_view(),name='issue_assignee'),
    path('issue_approver/',issue_approver.as_view(),name='issue_approver'),
    path('ICQQtnsFinal/',ICQQtnsFinal.as_view(),name='ICQQtnsFinal'),
    path('getICQSecQtnFinal/',getICQSecQtnFinal.as_view(),name='getICQSecQtnFinal'),
    path('saveICQRatingsFinal/',saveICQRatingsFinal.as_view(),name='saveICQRatingsFinal'),
    path('publushICQ/',publushICQ.as_view(),name='publushICQ'),
    path('getICQSectionsFinal/',getICQSectionsFinal.as_view(),name='getICQSectionsFinal'),
    path('allocate_icq/',allocate_icq.as_view(),name='allocate_icq'),
    path('save_allocation/',save_allocation.as_view(),name='save_allocation'),
    path('reqValidation/',reqValidation.as_view(),name='reqValidation'), 
    path('getAssignedTo/',getAssignedTo.as_view(),name='getAssignedTo'),
    path('getModelQtnBySrc/',getModelQtnBySrc.as_view(),name='getModelQtnBySrc'),
    path('QtnsResp/',QtnsResp.as_view(),name='QtnsResp'),
    path('getQtnResp/',getQtnResp.as_view(),name='getQtnResp'),
    path('insertQtnResp/',insertQtnResp.as_view(),name='insertQtnResp'),
    path('getQtnRespById/',getQtnRespById.as_view(),name='getQtnRespById'),
    path('newauditresponse/',newauditresponse.as_view(),name='newauditresponse'),
    path('saveauditresponse/',saveauditresponse.as_view(),name='saveauditresponse'),
    path('newquestionresponseapi/',newquestionresponseapi.as_view(),name='newquestionresponseapi'),
    path('savequestionresponse/',savequestionresponse.as_view(),name='savequestionresponse'),
    path('ICQQtns/',ICQQtns.as_view(),name='ICQQtns'),
    path('getICQSecQtn/',ICQQtns.as_view(),name='getICQSecQtn'),
    path('saveICQRatings/',saveICQRatings.as_view(),name='saveICQRatings'),
    path('submitICQRatings/',submitICQRatings.as_view(),name='submitICQRatings'),
    path('getICQSections/',getICQSections.as_view(),name='getICQSections'),
    path('getCriteria/',getCriteria.as_view(),name='getCriteria'),
    path('GetIsModel/',GetIsModel.as_view(),name='GetIsModel'),
    path('getQtnAns/',getQtnAns.as_view(),name='getQtnAns'),
    path('insertQtnAnsr/',insertQtnAnsr.as_view(),name='insertQtnAnsr'),
    path('QuestionsAllUsers/',QuestionsAllUsers.as_view(),name='QuestionsAllUsers'),
    path('Questions/',Questions.as_view(),name='Questions'),
    path('add_question/',add_question.as_view(),name='add_question'),
    path('allocate_questions/',allocate_questions.as_view(),name='allocate_questions'),
    path('save_OnlyQuestion_allocation/',save_OnlyQuestion_allocation.as_view(),name='save_OnlyQuestion_allocation'),
    path('addQtnsAllUsers/',addQtnsAllUsers.as_view(),name='addQtnsAllUsers'),
    path('addQuesSub_Section/',addQuesSub_Section.as_view(),name='addQuesSub_Section'),
    path('addQuesSub_Sub_Section/',addQuesSub_Sub_Section.as_view(),name='addQuesSub_Sub_Section'),
    path('addQuesSub_Sub_Sub_Section/',addQuesSub_Sub_Sub_Section.as_view(),name='addQuesSub_Sub_Sub_Section'),
    path('addQues_question/',addQues_question.as_view(),name='addQues_question'),
    path('getQues_Sections/',getQues_Sections.as_view(),name='getQues_Sections'),
    path('getQuesSub_Sections/',getQuesSub_Sections.as_view(),name='getQuesSub_Sections'),
    path('getQuesSub_Sub_Sections/',getQuesSub_Sub_Sections.as_view(),name='getQuesSub_Sub_Sections'), 
    path('checkValue/',checkValue.as_view(),name='checkValue'), 
    path('save_activity_trail/',save_activity_trail.as_view(),name='save_activity_trail'),
    path('getVTMenus/',getVTMenus.as_view(),name='getVTMenus'),
    path('getTempMdlDetailsById/',getTempMdlDetailsById.as_view(),name='getTempMdlDetailsById'),
    path('ApproveEdit/',ApproveEdit.as_view(),name='ApproveEdit'),

    #jayesh api starts

    path('department/<int:id>',DepartmentAPI.as_view(),name='DepartmentView'),
    path('updatedepartment/',updatedepartment.as_view(),name='updatedepartment'),
   
    path('task-priority-master/<int:id>',TaskPriorityMasterAPI.as_view(),name='task_priority_masterView'),
 
    path('task-function-master/<int:id>',TaskFunctionMasterAPI.as_view(),name='task_function_masterView'),
    path('task-type-master/<int:id>',TaskTypeMasterAPI.as_view(),name="TaskTypeMasterView"),
    
    path('task-approval-status-master/<int:id>',TaskApprovalstatusMasterAPI.as_view(),name='TaskApprovalstatusmasterView'),
   
    path('sub-task-type-master/<int:id>',SubTasktypeMasterAPI.as_view(),name='sub-task-type-masterView'),
    path('dashboard-content-master/',DashboardContentMasterAPI.as_view(),name='dashboard-content-masterview'),
    path('user-dashboard-conter-master/',UserDashboardContentMasterAPI.as_view(),name='user-dashboard-content-master'),
     
    #jayesh api ends
    path('getMaxFreqSeq/',getMaxFreqSeq.as_view(),name='getMaxFreqSeq'),
    path('getTemplateData/',getTemplateData.as_view(),name='getTemplateData'),
    path('Update_Performance_Monitoring_Override_History,',Update_Performance_Monitoring_Override_History.as_view(),name='Update_Performance_Monitoring_Override_History'),
    path('Perm_Override_MRM/',Perm_Override_MRM.as_view(),name='Perm_Override_MRM'),

    path('getMaxFreqSeqData/',getMaxFreqSeqData.as_view(), name="getMaxFreqSeqData"),
    path('insert_VT_Discussion_Comments/',insert_VT_Discussion_Comments.as_view(),name='insert_VT_Discussion_Comments'),


    ###--------------------Ashok code--------------------------------------------###

    path('issue-priority-master/',IssuePriorityMasterAPI.as_view(),name='issue-priority-master'),

    path('issue-priority-master/<int:id>',IssuePriorityMasterAPI.as_view(),name='issue-priority-master'),

    path('issue-function-master/',IssueFunctionMasterAPI.as_view(),name='issue-function-master'),

    path('issue-function-master/<int:id>',IssueFunctionMasterAPI.as_view(),name='issue-function-master'),

    path('issue-approval-status-master/',IssueApprovalstatusMasterAPI.as_view(),name='issue-approval-status-master'),

    path('issue-approval-status-master/<int:id>/',IssueApprovalstatusMasterAPI.as_view(),name='issue-approval-status-master'),

    path('getIssue/',getIssues.as_view(),name='getIssue'),

    path('getVRSubmResp/',getVRSubmResp.as_view(),name='getVRSubmResp'),

    path('insertVRSubResp/',insertVRSubResp.as_view(),name='insertVRSubResp'),

    path('getVRSubRespById/',getVRSubRespById.as_view(),name='getVRSubRespById'),

    path('getVRSubmCommentsCnt/',getVRSubmCommentsCnt.as_view(),name='getVRSubmCommentsCnt'),

    path('getVRSubRespByUid/',getVRSubRespByUid.as_view(),name='getVRSubRespByUid'),

    path('GetMdlForClosure/',GetMdlForClosure.as_view(),name='GetMdlForClosure'),

    path('InsertVRPublishingInfo/',InsertVRPublishingInfo.as_view(),name='InsertVRPublishingInfo'),

    path('getMdlForVRSubmisionAllocation/',getMdlForVRSubmisionAllocation.as_view(),name='getMdlForVRSubmisionAllocation'),

    path('getMdlQtnsBySec/',getMdlQtnsBySec.as_view(),name='getMdlQtnsBySec'),

    path('addUserQues_question/',addUserQues_question.as_view(),name='addUserQues_question'),

    path('GetMdlForPublish/',GetMdlForPublish.as_view(),name='GetMdlForPublish'),

    path('discardUpdate/',discardUpdate.as_view(),name="discardUpdate"),

    path('Save_Buss_KPI_Monitoring_Result/',Save_Buss_KPI_Monitoring_Result.as_view(),name='Save_Buss_KPI_Monitoring_Result'), 

    path('Save_Performance_Monitoring_Resolution/',Save_Performance_Monitoring_Resolution.as_view(),name='Save_Performance_Monitoring_Resolution'),


    path('Update_Performance_Monitoring_Override_History/',Update_Performance_Monitoring_Override_History.as_view(),name='Update_Performance_Monitoring_Override_History'),

    path('getMdlIdforPerfMontr/',getMdlIdforPerfMontr.as_view(),name='getMdlIdforPerfMontr'), 

    path('getIssuesByQtrOrMonth/',getIssuesByQtrOrMonth.as_view(),name='getIssuesByQtrOrMonth'),

    path('modelsByValPriority/',modelsByValPriority.as_view(),name='modelsByValPriority'),

    path('get_sub_valID/',get_sub_valID.as_view(), name="get_sub_valID"), 

    path('getfindings_ID/',getfindings_ID.as_view(),name='getfindings_ID'),

    path('getfindings_Data/',getfindings_Data.as_view(),name='getfindings_Data'),

    path('update_response_findings/',update_response_findings.as_view(),name='update_response_findings'),

    path('get_ValidationRating/',get_ValidationRating.as_view(),name='get_ValidationRating'),

    path('fetch_model_report/',fetch_model_report.as_view(), name="fetch_model_report"),

    path('get_header_n_title/',get_header_n_title.as_view(),name='get_header_n_title'),

    path('updateTempHeaderIdx/',updateTempHeaderIdx.as_view(),name="updateTempHeaderIdx"),

    path('deleteTempHeaderIdx/',deleteTempHeaderIdx.as_view(),name='deleteTempHeaderIdx'),

    path('insertFromTemp/',insertFromTemp.as_view(),name='insertFromTemp'),

    

    path('get_cat_cols/',get_cat_cols.as_view(),name='get_cat_cols'),

    path('get_num_cols/',get_num_cols.as_view(),name='get_num_cols'),

    path('get_da_data/',get_da_data.as_view(),name='get_da_data'),

    path('showcorrelation_da/',showcorrelation_da.as_view(), name="showcorrelation_da"),


    path('Is_BackInfo_Exists/',Is_BackInfo_Exists.as_view(),name='Is_BackInfo_Exists'),

    path('Add_BankInfo/',Add_BankInfo.as_view(),name='Add_BankInfo'),

    path('Get_UC_DEPT/',Get_UC_DEPT.as_view(),name='Get_UC_DEPT'),

    path('Update_Useraccess/',Update_Useraccess.as_view(),name='Update_Useraccess'),

    path('Get_Useraccess/',Get_Useraccess.as_view(),name='Get_Useraccess'),

    path('Get_User_Deatils/',Get_User_Deatils.as_view(),name='Get_User_Deatils'),

    path('Add_BankDoc/',Add_BankDoc.as_view(),name='Add_BankDoc'),

    path('getModelQtnById/',getModelQtnById.as_view(),name="getModelQtnById"),

    path('Fetch_Allmessage/',Fetch_Allmessage.as_view(),name='Fetch_Allmessage'),

    path('GetDocsNameAPI/',GetDocsNameAPI.as_view(),name='GetDocsNameAPI'),

    path('GetMdlDocumentsAPI/',GetMdlDocumentsAPI.as_view(),name='GetMdlDocumentsAPI'),

    
    path('generate_task_ID/',generate_task_ID.as_view(),name='generate_task_ID'),

    path('update_summery_data/',update_summery_data.as_view(),name='update_summery_data'),

    path('issue_registration/',issue_registration.as_view(),name='issue_registration'),

    path('get_sub_issue_type/',get_sub_issue_type.as_view(),name='get_sub_issue_type'),

    path('generate_issueID/',generate_issueID.as_view(),name='generate_issueID'),

    path('issue_assignee/',issue_assignee.as_view(),name='issue_assignee'),

    path('issue_approver/',issue_approver.as_view(),name='issue_approver'),

    path('get_issue_ID_data/',get_issue_ID_data.as_view(),name='get_issue_ID_data'),

    path('issue_update_summery_data/',issue_update_summery_data.as_view(),name='issue_update_summery_data'),

    path('edit_issue/',edit_issue.as_view(),name='edit_issue'),



    path('email_details/',email_details.as_view(),name='email_details'),

    path('scheduler_notification/',scheduler_notification.as_view(),name='scheduler_notification'),

    path('get_alert_schedule_data/',get_alert_schedule_data.as_view(),name='get_alert_schedule_data'),

    path('save_comments_mdl_overview/',save_comments_mdl_overview.as_view(),name='save_comments_mdl_overview'),

    path('upload_findings/',upload_findings.as_view(),name='upload_findings'),

    path('model_committee/',model_committee.as_view(),name='model_committee'),

    path('perfMonitoring_email_send/',perfMonitoring_email_send.as_view(),name='perfMonitoring_email_send'),

    path('pdf_request/',pdf_request.as_view(),name='pdf_request'),

    path('section_save_comment/',section_save_comment.as_view(),name='section_save_comment'),

    path('getsectionQtnResp/',getsectionQtnResp.as_view(),name='getsectionQtnResp'),

    path('section_save_discussion/',section_save_discussion.as_view(),name='section_save_discussion'),

]

