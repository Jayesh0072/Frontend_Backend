from django.urls import path


from .views import * #UserCategoryAPI,AddUser, Login, Logout,TaskRegistrationAPI,DepartmentAPI,Task_Relevant_PersonnelAPI,TaskSummeryAPI,AlertAPI,IssueRegistrationAPI,IssueRelevantPersonnelAPI
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
    path('task-type-master/',TaskTypeMasterAPI.as_view(),name="TaskTypeMasterView"),
    path('task-approval-status-master/',TaskApprovalstatusMasterAPI.as_view(),name='TaskApprovalstatusmasterView'),
    path('informaion/',InformationAPI.as_view(),name='InformationView'),
    path('sub-task-type-master/',SubTasktypeMasterAPI.as_view(),name='sub-task-type-masterView'),
    path('dashboard-content-master/',DashboardContentMasterAPI.as_view(),name='dashboard-content-masterview'),
    path('user-dashboard-conter-master/',UserDashboardContentMasterAPI.as_view(),name='user-dashboard-content-master'),
    path('intrensicmaster/',IntrinsicMasterAPI.as_view(),name='IntrinsicMasterView'),
    path('reliancemaster/',RelianceMasterAPI.as_view(),name='RelianceMasterView'),
    path('materilitymaster/',MaterialityMasterAPI.as_view(),name='MaterialityMasterView'),
    path('historyregister/',HistoryRegisterAPI.as_view(),name="HistoryRegisterView"),
    path('modelfunctionmaster/',ModelFunctionMasterAPI.as_view(),name="ModelFunctionMasterView"),
    path('modelsourcemaster/',ModelSourceMasterAPI.as_view(),name="ModelSourceMasterView"),
    path('modeltypemaster/',ModelTypeMasterAPI.as_view(),name="modeltypemasterView"),
    path('prdaddmaster/',PrdAddrMasterAPI.as_view(),name="PrdAddrMasterAPI"),
    path('mdldependencies/',MdlDependenciesAPI.as_view(),name="MdlDependenciesView"),
    path('mdlupstream/',MdlUpstreamAPI.as_view(),name="MdlUpstreamView"),
    path('mdldwstream/',MdlDwstreamAPI.as_view(),name="MdlDwstreamView"),
    path('thread/',ThreadAPI.as_view(),name="ThreadView"),
    path('chatmessage/',ChatmessageAPI.as_view(),name="ChatmessageView"),
    path('notificationdetails/',NotificationDetailsAPI.as_view(),name=' notificationdetailsview'),
    path('icqquestionmaster/',IcqQuestionMasterAPI.as_view(),name='IcqQuestionMasterView'),
    path('IcqSections/',IcqSectionsAPI.as_view(),name='IcqSectionsView'),
    path('Icqsubsubsections/',IcqSubSectionsAPI.as_view(),name="IcqSubSectionsAPI"),
    path('icqsubsubsections/',IcqSubSubSectionsAPI.as_view(),name="IcqSubSubSectionsAPI"),
    path('icqsubsubsubsections/',IcqSubSubSubSectionsAPI.as_view(),name="IcqSubSubSubSectionsView"),
    path('UserCategory/',UserCategoryAPI.as_view(),name='UserCategory'),
    path('addUser/', AddUser.as_view(), name="register"),
    path('addNewUser/',addNewUser.as_view(),name='addNewUser'),
    path('ResetPassword/',ResetPassword.as_view(),name='ResetPassword'),
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('dashboard/',Dashboard.as_view(),name="dashboard"),
    path('projectsDetails/',projectsDetails.as_view(),name="projectsDetails"),
    path('getMdlDetailsById/',getMdlDetailsById.as_view(),name='getMdlDetailsById'),
    path('checkPendingTasksIssues/',checkPendingTasksIssues.as_view(),name='checkPendingTasksIssues'), 
    path('task_approver/',task_approver.as_view(),name='task_approver'),
    path('task_assignee/',task_assignee.as_view(),name='task_assignee'),
    path('getIssues/',getIssues.as_view(),name='getIssues'),
    path('checkUserRole_Issue/',checkUserRole_Issue.as_view(),name='checkUserRole_Issue'),
    path('issue_assignee/',issue_assignee.as_view(),name='issue_assignee'),
    path('issue_approver/',issue_approver.as_view(),name='issue_approver'),
    path('ICQQtnsFinal/',ICQQtnsFinal.as_view(),name='ICQQtnsFinal'),
    path('getICQSecQtnFinal/',getICQSecQtnFinal.as_view(),name='getICQSecQtnFinal'),    
    path('publushICQ/',publushICQ.as_view(),name='publushICQ'),
    path('getICQSectionsFinal/',getICQSectionsFinal.as_view(),name='getICQSectionsFinal'),
    path('allocate_icq/',allocate_icq.as_view(),name='allocate_icq'),
    path('save_allocation/',save_allocation.as_view(),name='save_allocation'),
    path('reqValidation/',reqValidation.as_view(),name='reqValidation'),
    path('assignValidation/',assignValidation.as_view(),name='assignValidation'),
    path('getAssignedTo/',getAssignedTo.as_view(),name='getAssignedTo'),
    path('getModelQtnBySrc/',getModelQtnBySrc.as_view(),name='getModelQtnBySrc'),
    path('QtnsResp/',QtnsResp.as_view(),name='QtnsResp'),
    
    path('UpdateUser/', UpdateUser.as_view(), name="UpdateUser"),
    path('UpdateUser/<int:id>', UpdateUser.as_view(), name="UpdateUser"),
    path('MdlRelevantPersonnelAPI/', MdlRelevantPersonnelAPI.as_view(), name="MdlRelevantPersonnelAPI"),
    path('MdlRelevantPersonnelAPI/<str:id>', MdlRelevantPersonnelAPI.as_view(), name="MdlRelevantPersonnelAPI"),
    
    path('BackupForUserData/',BackupForUserData.as_view(), name="BackupForUserData"),

    path('VrSubmissionAllocationAPI/',VrSubmissionAllocationAPI.as_view(), name="VrSubmissionAllocationAPI"),
    path('VrSubmissionAllocationAPI/<str:id>/',VrSubmissionAllocationAPI.as_view(), name="VrSubmissionAllocationAPI"),
    path('checkutypeowner/',checkutypeowner.as_view(), name="checkutypeowner"),
    path('getutypeselection/',getutypeselection.as_view(), name="getutypeselection"),
    path('validationReviewFrequency/',validationReviewFrequency.as_view(), name="validationReviewFrequency"),
    path('validationReviewFrequency/<int:id>/',validationReviewFrequency.as_view(), name="validationReviewFrequency"),
    path('ConnectionMsgSave/',ConnectionMsgSave.as_view(), name="ConnectionMsgSave"),
    path('GetHistoryMsg/',GetHistoryMsg.as_view(), name="GetHistoryMsg"),
    path('Fetchmdlid/',Fetchmdlid.as_view(), name="Fetchmdlid"),
    path('Freqmasterdata/',Freqmasterdata.as_view(), name="Freqmasterdata"),
    path('FetchModelMatrics/',FetchModelMatrics.as_view(), name="FetchModelMatrics"),
    path('ModelMatricsAPI/',ModelMatricsAPI.as_view(), name="ModelMatricsAPI"),
    path('ModelMatricsTempData/',ModelMatricsTempData.as_view(), name="ModelMatricsTempData"),
    
    path('FetchPerfMonMdlId/',FetchPerfMonMdlId.as_view(), name="FetchPerfMonMdlId"),
    path('Fetchmmlabel/',Fetchmmlabel.as_view(), name="Fetchmmlabel"),
    path('perfMonitoringFileInfoAPI/',perfMonitoringFileInfoAPI.as_view(), name="perfMonitoringFileInfoAPI"),
    
    # path('AddModelMetrics/',AddModelMetrics.as_view(), name="AddModelMetrics"),
    # path('AddModelMetricsDept/',AddModelMetricsDept.as_view(), name="AddModelMetricsDept"),
    # # path('AddModelMetrics/<str:id>',AddModelMetrics.as_view(),name='AddModelMetrics'),
    # path('editmodelmetrics/<str:id>',editmodelmetrics.as_view(), name="editmodelmetrics"),
    # path('checkMetricDept/',checkMetricDept.as_view(),name='checkMetricDept'),
    # # Master code 0612
    # path('savemodelmetrics/',savemodelmetrics.as_view(),name='savemodelmetrics'),
    # path('savemodelmetrics/<str:id>',savemodelmetrics.as_view(), name="savemodelmetrics"),
    path('savemodeldepartment/',savemodeldepartment.as_view(),name='savemodeldepartment'),
    path('frequecy_master/',frequecy_master.as_view(),name='frequecy_master'),
    path('frequecy_master/<str:id>',frequecy_master.as_view(),name='frequecy_master'),

    path('BusinessMetricAPI/',BusinessMetricAPI.as_view(), name="BusinessMetricAPI"),
    path('AddBusinessMetricAPI/',AddBusinessMetricAPI.as_view(), name="AddBusinessMetricAPI"),
    path('AddBusinessMetricsDept/',AddBusinessMetricsDept.as_view(), name="AddBusinessMetricsDept"),
    path('BusinessMatricsTempData/',BusinessMatricsTempData.as_view(), name="BusinessMatricsTempData"),

    path('Fetchmdlid_MRM/',Fetchmdlid_MRM.as_view(), name="Fetchmdlid_MRM"),
    path('getMdlDataForMRM/',getMdlDataForMRM.as_view(), name="getMdlDataForMRM"),
    path('getBusinessDataForMRM/',getBusinessDataForMRM.as_view(), name="getBusinessDataForMRM"),
    path('getMdlIdforPerfMontr/',getMdlIdforPerfMontr.as_view(), name="getMdlIdforPerfMontr"),
    # path('getDataForMRM/',getDataForMRM.as_view(), name="getDataForMRM"),
    path('ApproveModelMatricsData/',ApproveModelMatricsData.as_view(), name="ApproveModelMatricsData"),
    path('ApproveBusinessMatricsData/',ApproveBusinessMatricsData.as_view(), name="ApproveBusinessMatricsData"),

    path('DataMatricsData/',DataMatricsData.as_view(), name="DataMatricsData"),
    path('SaveTempFeatureMatricSelection/',SaveTempFeatureMatricSelection.as_view(), name="SaveTempFeatureMatricSelection"),
    path('SelectdataMetrics/',SelectdataMetrics.as_view(), name="SelectdataMetrics"),
    path('calculatedatamatrics/',calculatedatamatrics.as_view(), name="calculatedatamatrics"),
    path('DataMetricAPI/',DataMetricAPI.as_view(), name="DataMetricAPI"),
    path('ApproveDataMatricsData/',ApproveDataMatricsData.as_view(), name="ApproveDataMatricsData"),
    
    #Data New Urls
    path('Save_Data_Monitoring_Result/',Save_Data_Monitoring_Result.as_view(), name="Save_Data_Monitoring_Result"),
    path('Save_Data_Monitoring_Override_History/',Save_Data_Monitoring_Override_History.as_view(), name="Save_Data_Monitoring_Result"),
    path('Update_Data_Monitoring_Override_History/',Update_Data_Monitoring_Override_History.as_view(), name="Update_Data_Monitoring_Override_History"),
    path('getMaxFreqSeqData/',getMaxFreqSeqData.as_view(), name="getMaxFreqSeqData"),
    path('getMaxFreqSeq_Buss/',getMaxFreqSeq_Buss.as_view(), name="getMaxFreqSeq_Buss"),
    path('DataMonitoringFileInfoAPI/',DataMonitoringFileInfoAPI.as_view(), name="DataMonitoringFileInfoAPI"),

    # Reports Urls
    path('ReportSectionMasterAPI/',ReportSectionMasterAPI.as_view(), name="ReportSectionMasterAPI"),
    path('ReportSubSectionMasterAPI/',ReportSubSectionMasterAPI.as_view(), name="ReportSubSectionMasterAPI"),
    path('ReportSubSubSectionMasterAPI/',ReportSubSubSectionMasterAPI.as_view(), name="ReportSubSubSectionMasterAPI"),
    path('ReportTemplateTempAPI/',ReportTemplateTempAPI.as_view(), name="ReportTemplateTempAPI"),
    path('ReportTemplateAPI/',ReportTemplateAPI.as_view(), name="ReportTemplateAPI"),
    path('Fetch_Report_data/',Fetch_Report_data.as_view(), name="Fetch_Report_data"),
    path('ReportContentAPI/',ReportContentAPI.as_view(), name="ReportContentAPI"),

    # Issues code sir # 

    path('getIssue/',getIssues.as_view(),name='getIssue'),
    path('issue_assignee/',issue_assignee.as_view(),name='issue_assignee'),
    path('issue_approver/',issue_approver.as_view(),name='issue_approver'),

    #Findings val and category
    path('FindingsValElementsAPI/',FindingsValElementsAPI.as_view(),name='FindingsValElementsAPI'),
    path('FindingsValElementsAPI/<int:id>',FindingsValElementsAPI.as_view(),name='FindingsValElementsAPI'),
    path('FindingsCategoryAPI/',FindingsCategoryAPI.as_view(),name='FindingsCategoryAPI'),
    path('FindingsCategoryAPI/<int:id>',FindingsCategoryAPI.as_view(),name='FindingsCategoryAPI'),

    path('GetModelIdFindVal/',GetModelIdFindVal.as_view(),name='GetModelIdFindVal'),

    path('FindingsValSubElementsAPI/',FindingsValSubElementsAPI.as_view(),name='FindingsValSubElementsAPI'),
    path('FindingsValSubElementsAPI/<int:id>',FindingsValSubElementsAPI.as_view(),name='FindingsValSubElementsAPI'),
    path('Elements/',Elements.as_view(),name='Elements'),

    path('QuestionSectionAPI/',QuestionSectionAPI.as_view(),name='QuestionSectionAPI'),
    path('QuestionSectionAPI/<int:id>',QuestionSectionAPI.as_view(),name='QuestionSectionAPI'),
    path('SectionApI/',SectionApI.as_view(),name='SectionApI'),
    path('Sections/',Sections.as_view(),name='Sections'),

    path('FiterIssue/',FiterIssue.as_view(),name='FiterIssue'),
    path('ValidationRatingsAPI/',ValidationRatingsAPI.as_view(),name='ValidationRatingsAPI'),
    path('ValidationRatingsTempAPI/',ValidationRatingsTempAPI.as_view(),name='ValidationRatingsTempAPI'),

    path('ValFindingConnectionMsgSave/',ValFindingConnectionMsgSave.as_view(),name='ValFindingConnectionMsgSave'),
    path('GetValFindHistoryMsg/',GetValFindHistoryMsg.as_view(),name='GetValFindHistoryMsg'),
    
    path('Show_Report_data/',Show_Report_data.as_view(),name='Show_Report_data'),

    path('Get_Title_Label/',Get_Title_Label.as_view(),name='Get_Title_Label'),
    path('get_template_name/',get_template_name.as_view(),name='get_template_name'),
    path('getReportTtlHdr/',getReportTtlHdr.as_view(),name='getReportTtlHdr'),
    path('RPT_Template_Header_API/',RPT_Template_Header_API.as_view(),name='RPT_Template_Header_API'),
    path('Fetch_Header_Details/',Fetch_Header_Details.as_view(),name='Fetch_Header_Details'),
    path('ReportHeaderTitleContentAPI/',ReportHeaderTitleContentAPI.as_view(),name='ReportHeaderTitleContentAPI'),

    path('save_model_report/',save_model_report.as_view(),name='save_model_report'),
    
    path('insert_Report_Title_Table_contet/',insert_Report_Title_Table_contet.as_view(),name='insert_Report_Title_Table_contet'),
    path('get_Report_Title_Table_contet/',get_Report_Title_Table_contet.as_view(),name='get_Report_Title_Table_contet'),

    #comment
    path('save_desc_comments/',save_desc_comments.as_view(), name="save_desc_comments"),
    path('validation_comments/',validation_comments.as_view(), name="validation_comments"),
    path('get_val_comments_data/',get_val_comments_data.as_view(), name="get_val_comments_data"),
    path('plotinsoccuvsincstate/',Plotinsoccuvsincstate.as_view(), name="plotinsoccuvsincstate"),

    path('Fetch_message/',Fetch_message.as_view(), name="Fetch_message"),
    path('projectsInfo/',projectsInfo.as_view(), name="projectsInfo"),
    path('taskListByModel/',taskListByModel.as_view(), name="taskListByModel"),

    path('FL_add_question/',FL_add_question.as_view(),name='FL_add_question'),
    path('Fl_sectionsAPI/',Fl_sectionsAPI.as_view(),name='Fl_sectionsAPI'),
    path('UsersgetAPI/',UsersgetAPI.as_view(),name='UsersgetAPI'),
    path('save_flallocation/',save_flallocation.as_view(),name='save_flallocation'),
    path('FLQtns/',FLQtns.as_view(),name='FLQtns'),
    path('FLQtnsFinal/',FLQtnsFinal.as_view(),name='FLQtnsFinal'),
    path('getFLSecQtnFinal/',getFLSecQtnFinal.as_view(),name='getFLSecQtnFinal'),
    path('saveFLRatingsFinal/',saveFLRatingsFinal.as_view(),name='saveFLRatingsFinal'),
    path('submitFLRatings/',submitFLRatings.as_view(),name='submitFLRatings'),
    path('submitFLRatings1/',submitFLRatings1.as_view(),name='submitFLRatings1'),
    path('saveFLRatings/',saveFLRatings.as_view(),name='saveFLRatings'),
    path('FetchResidualRating/',FetchResidualRating.as_view(),name='FetchResidualRating'),
    path('SaveResidualRatingsAPI/',SaveResidualRatingsAPI.as_view(),name='SaveResidualRatingsAPI'),


    path('FLQuestionRatingDataAPI/',FLQuestionRatingDataAPI.as_view(),name='FLQuestionRatingDataAPI'),
    path('MappingAPI/',MappingAPI.as_view(),name='MappingAPI'),
    path('DatabaseFieldAPI/',DatabaseFieldAPI.as_view(),name='DatabaseFieldAPI'),
    path('FieldAPI/',FieldAPI.as_view(),name='FieldAPI'),
    path('valueAPI/',valueAPI.as_view(),name='valueAPI'),

    path('ControllClassAPI/',ControllClassAPI.as_view(),name='ControllClassAPI'),
    path('ControllClassAPI/<int:id>',ControllClassAPI.as_view(),name='ControllClassAPI'),

    path('RiskMasterAPI/',RiskMasterAPI.as_view(),name='RiskMasterAPI'),
    path('RiskMasterAPI/<int:id>',RiskMasterAPI.as_view(),name='RiskMasterAPI'),
    path('GetUtilityAPI/',GetUtilityAPI.as_view(),name='GetUtilityAPI'),

    # path('FLReportContentAPI/',FLReportContentAPI.as_view(),name='FLReportContentAPI'),
    # path('FL_Fetch_Header_Details/',FL_Fetch_Header_Details.as_view(),name='FL_Fetch_Header_Details'),
    path('FLReportHeaderTitleContentAPI/',FLReportHeaderTitleContentAPI.as_view(),name='FLReportHeaderTitleContentAPI'),
    path('FL_insert_Report_Title_Table_contet/',FL_insert_Report_Title_Table_contet.as_view(),name='FL_insert_Report_Title_Table_contet'),

    path('saveriskcomments/',saveriskcomments.as_view(),name='saveriskcomments'),
    path('GetRiskFactorHistoryMsg/',GetRiskFactorHistoryMsg.as_view(), name="GetRiskFactorHistoryMsg"),
    path('GetRiskFactorComment/',GetRiskFactorComment.as_view(), name="GetRiskFactorComment"),
    
    path('FL_addSub_Sub_Sub_Section/',FL_addSub_Sub_Sub_Section.as_view(), name="FL_addSub_Sub_Sub_Section"),
    
    path('FLSettingAPI/',FLSettingAPI.as_view(), name="FLSettingAPI"),
    
    path('FL_ReportContentAPI/',FL_ReportContentAPI.as_view(),name='FL_ReportContentAPI'),
    path('FL_Fetch_Report_data/',FL_Fetch_Report_data.as_view(),name='FL_Fetch_Report_data'),
    path('FL_Fetch_Header_Details/',FL_Fetch_Header_Details.as_view(),name='FL_Fetch_Header_Details'),
    path('FL_ReportHeaderTitleContentAPI/',FL_ReportHeaderTitleContentAPI.as_view(),name='FL_ReportHeaderTitleContentAPI'),
    path('AssignRiskFactorAPI/',AssignRiskFactorAPI.as_view(), name="AssignRiskFactorAPI"),

    path('add_question_ans/',add_question_ans.as_view(),name='add_question_ans'),

    path('PerfMontrMappingAPI/',PerfMontrMappingAPI.as_view(),name='PerfMontrMappingAPI'),
    
    path('ModelMatricDataAPI/',ModelMatricDataAPI.as_view(),name='model_matric_data_API'),

    path('MdlIdDataCheck/',MdlIdDataCheck.as_view(),name='MdlIdDataCheck'),

    path('FlReportTitleCommentAPI/',FlReportTitleCommentAPI.as_view(),name='FlReportTitleCommentAPI'),
    
    path('FlImportData/',FlImportData.as_view(),name='FlImportData'),

    path('InherentRiskRatingAPI/',InherentRiskRatingAPI.as_view(),name='InherentRiskRatingAPI'),
    
    path('ALLInherentRatingAPI/',ALLInherentRatingAPI.as_view(),name='ALLInherentRatingAPI'),
    path('ALLInherentRatingAPI/<int:id>',ALLInherentRatingAPI.as_view(),name='ALLInherentRatingAPI'),

    path('ControlEffectiveRatingAPI/',ControlEffectiveRatingAPI.as_view(),name='ControlEffectiveRatingAPI'),
    path('ControlEffectiveRatingAPI/<int:id>',ControlEffectiveRatingAPI.as_view(),name='ControlEffectiveRatingAPI'),

    path('publishFL/',publishFL.as_view(),name='publishFL'),

    path('FLReportSectionMasterAPI/',FLReportSectionMasterAPI.as_view(),name='FLReportSectionMasterAPI'),
    path('FL_get_template_name/',FL_get_template_name.as_view(),name='FL_get_template_name'),
    path('FLReportSubSectionMasterAPI/',FLReportSubSectionMasterAPI.as_view(),name='FLReportSubSectionMasterAPI'),
    path('FLReportTemplateTempAPI/',FLReportTemplateTempAPI.as_view(),name='FLReportTemplateTempAPI'),
    path('FLReportSubSubSectionMasterAPI/',FLReportSubSubSectionMasterAPI.as_view(),name='FLReportSubSubSectionMasterAPI'),
    path('FLReportTemplateAPI/',FLReportTemplateAPI.as_view(),name='FLReportTemplateAPI'),
    path('FL_RPT_Template_Header_API/',FL_RPT_Template_Header_API.as_view(),name='FL_RPT_Template_Header_API'),
    path('FL_Get_Title_Label/',FL_Get_Title_Label.as_view(),name='FL_Get_Title_Label'),
    path('FLgetReportTtlHdr/',FLgetReportTtlHdr.as_view(),name='FLgetReportTtlHdr'),
    path('FLShow_Report_data/',FLShow_Report_data.as_view(),name='FLShow_Report_data'),

    path('ICQInherentRiskRatingAPI/',ICQInherentRiskRatingAPI.as_view(),name='ICQInherentRiskRatingAPI'),
    path('ICQFetchResidualRating/',ICQFetchResidualRating.as_view(),name='ICQFetchResidualRating'),
    path('ICQSaveResidualRatingsAPI/',ICQSaveResidualRatingsAPI.as_view(),name='ICQSaveResidualRatingsAPI'),

    path('ICQALLInherentRatingAPI/',ICQALLInherentRatingAPI.as_view(),name='ICQALLInherentRatingAPI'),
    path('ICQALLInherentRatingAPI/<int:id>',ICQALLInherentRatingAPI.as_view(),name='ICQALLInherentRatingAPI'),
    
    path('ICQControlEffectiveRatingAPI/',ICQControlEffectiveRatingAPI.as_view(),name='ICQControlEffectiveRatingAPI'),
    path('ICQControlEffectiveRatingAPI/<int:id>',ICQControlEffectiveRatingAPI.as_view(),name='ICQControlEffectiveRatingAPI'),

    path('UdaapRatings/',UdaapRatings.as_view(),name='UdaapRatings'),
    path('UdaapQtnsFinal/',UdaapQtnsFinal.as_view(),name='UdaapQtnsFinal'),
    path('UdaapInherentRiskRatingAPI/',UdaapInherentRiskRatingAPI.as_view(),name='UdaapInherentRiskRatingAPI'),
    path('UdaapFetchResidualRating/',UdaapFetchResidualRating.as_view(),name='UdaapFetchResidualRating'),
    path('getUdaapSecQtnFinal/',getUdaapSecQtnFinal.as_view(),name='getUdaapSecQtnFinal'),
    path('saveUdaapRatingsFinal/',saveUdaapRatingsFinal.as_view(),name='saveUdaapRatingsFinal'),
    path('publishUdaap/',publishUdaap.as_view(),name='publishUdaap'),

    path('UdaapQtns/',UdaapQtns.as_view(),name='UdaapQtns'),
    path('getUdaapSecQtn/',getUdaapSecQtn.as_view(),name='getUdaapSecQtn'),
    path('saveUdaapRatings/',saveUdaapRatings.as_view(),name='saveUdaapRatings'),
    path('submitUdaapRatings1/',submitUdaapRatings1.as_view(),name='submitUdaapRatings1'),
    
    path('UdaapSaveResidualRatingsAPI/',UdaapSaveResidualRatingsAPI.as_view(),name='UdaapSaveResidualRatingsAPI'),
    path('UdaapALLInherentRatingAPI/',UdaapALLInherentRatingAPI.as_view(),name='UdaapALLInherentRatingAPI'),
    path('UdaapALLInherentRatingAPI/<int:id>',UdaapALLInherentRatingAPI.as_view(),name='UdaapALLInherentRatingAPI'),

    path('UdaapControlEffectiveRatingAPI/',UdaapControlEffectiveRatingAPI.as_view(),name='UdaapControlEffectiveRatingAPI'),
    path('UdaapControlEffectiveRatingAPI/<int:id>',UdaapControlEffectiveRatingAPI.as_view(),name='UdaapControlEffectiveRatingAPI'),

    path('UdaapQuestions/',UdaapQuestions.as_view(),name='UdaapQuestions'),
    path('addUdaapQtns/',addUdaapQtns.as_view(),name='addUdaapQtns'),
    path('getUdaapSub_Sections/',getUdaapSub_Sections.as_view(),name='getUdaapSub_Sections'),
    path('getUdaapSub_Sub_Sections/',getUdaapSub_Sub_Sections.as_view(),name='getUdaapSub_Sub_Sections'),
    path('getUdaapSub_Sub_Sub_Sections/',getUdaapSub_Sub_Sub_Sections.as_view(),name='getUdaapSub_Sub_Sub_Sections'),
    path('Udaap_add_question/',Udaap_add_question.as_view(),name='Udaap_add_question'),    
    path('addUdaapSection/',addUdaapSection.as_view(),name='addUdaapSection'),    
    path('addUdaapSubSection/',addUdaapSubSection.as_view(),name='addUdaapSubSection'), 
    path('addUdaapSubSubSection/',addUdaapSubSubSection.as_view(),name='addUdaapSubSubSection'),
    path('addUdaapSubSubSubSection/',addUdaapSubSubSubSection.as_view(),name='addUdaapSubSubSubSection'), 

    path('UdaapSettingAPI/',UdaapSettingAPI.as_view(),name='UdaapSettingAPI'),
    path('getUdaapAllocation/',getUdaapAllocation.as_view(),name='getUdaapAllocation'),
    path('save_udaap_allocation/',save_udaap_allocation.as_view(),name='save_udaap_allocation'),
    
    path('FLDocsPoliciesProcedure/',FLDocsPoliciesProcedure.as_view(),name='FLDocsPoliciesProcedure'),

    path('category_master/',Category_MasterAPI.as_view(),name="category_master"),
    path('getSubCategory/<int:cat_id>', GetSubCategory.as_view(), name="getSubCategory"),

    path('DataMatricsTempData/',DataMatricsTempData.as_view(),name='DataMatricsTempData'),

    path('GetHistoryMsgBuss/',GetHistoryMsgBuss.as_view(),name='GetHistoryMsgBuss'),

    path('PrdnHistoryData/',PrdnHistoryData.as_view(),name='PrdnHistoryData'),
    
    path('Save_Performance_Monitoring_Result/',Save_Performance_Monitoring_Result.as_view(),name='Save_Performance_Monitoring_Result'),

    path('Save_Buss_KPI_Monitoring_Override_History/',Save_Buss_KPI_Monitoring_Override_History.as_view(),name='Save_Buss_KPI_Monitoring_Override_History'),

    path('Save_Buss_KPI_Monitoring_Resolution/',Save_Buss_KPI_Monitoring_Resolution.as_view(),name='Save_Buss_KPI_Monitoring_Resolution'),

    path('check_current_password/',check_current_password.as_view(),name='check_current_password'),
    
    
    ## add new

    path('AddModelMetrics/',AddModelMetrics.as_view(),name='AddModelMetrics'),
    path('editmodelmetrics/<str:id>',editmodelmetrics.as_view(), name="editmodelmetrics"),
    path('savemodelmetrics/',savemodelmetrics.as_view(),name='savemodelmetrics'),
    path('savemodeldepartment/',savemodeldepartment.as_view(),name='savemodeldepartment'),
    path('checkMetricDept/',checkMetricDept.as_view(),name='checkMetricDept'),
    path('get_model_cat_subcat/',get_model_cat_subcat.as_view(),name='get_model_cat_subcat'),

    path('savebusinessmetrics/', savebusinessmetrics.as_view(), name="savebusinessmetrics"),
    path('savebusinessdepartment/',savebusinessdepartment.as_view(),name='savebusinessdepartment'),
    path('AddBusinessMetrics/',AddBusinessMetrics.as_view(),name='AddBusinessMetrics'),
    path('editbusinessmetrics/<str:id>',editbusinessmetrics.as_view(),name='editbusinessmetrics'),
    path('get_business_cat_subcat/',get_business_cat_subcat.as_view(),name='get_business_cat_subcat'),
    path('checkBusinessDept/',checkBusinessDept.as_view(),name='checkBusinessDept'),
    path('fetch_mdl_document_name/',fetch_mdl_document_name.as_view(),name='fetch_mdl_document_name'),

    path('FLMappingAPI/',FLMappingAPI.as_view(),name='FLMappingAPI'),

    path('Fetchallmdlid/',Fetchallmdlid.as_view(),name='Fetchallmdlid'),
    path('ValidationPlanningAPI/',ValidationPlanningAPI.as_view(),name='ValidationPlanningAPI'),
    path('Val_Period_Master/',Val_Period_Master.as_view(),name='Val_Period_Master'),
    path('check_Validated_or_not/',check_Validated_or_not.as_view(),name='check_Validated_or_not'), 
    path('Val_Frequency_Master_API/',Val_Frequency_Master_API.as_view(),name='Val_Frequency_Master_API'),   

    path('NextValidationPlanningAPI/',NextValidationPlanningAPI.as_view(),name='NextValidationPlanningAPI'),

    path('GetICQReportData/',GetICQReportData.as_view(),name='GetICQReportData'),
    path('ICQ_ReportContentAPI/',ICQ_ReportContentAPI.as_view(),name='ICQ_ReportContentAPI'),
    path('checkPendingTasks/',checkPendingTasks.as_view(),name='checkPendingTasks') ,
    
    ###-------------------------Ashok code--------------------------------###
    # path('task-function-master/',TaskFunctionMasterAPI.as_view(),name='task_function_masterView'),
    path('getTasks/',getTasks.as_view(),name='getTasks'),
    path('find_max_file_id/<str:id>',Find_Max_File_Id.as_view(),name='find_max_file_id'),

    path('find_src_data/',Find_Src_Data.as_view(),name='find_src_data'),

    path('find_target_value/<str:file_id>',Find_Target_Value.as_view(),name='find_target_value'),

    path('dist_numevari_catvar/',Dist_Numevari_Catvar.as_view(),name='dist_numevari_catvar'),

    path('set_cols/',Set_Cols.as_view(),name='set_cols'),

    path('downloadIm/',downloadIm.as_view(),name='downloadIm'),

    path('plotinsoccuvsincstate/',Plotinsoccuvsincstate.as_view(),name='plotinsoccuvsincstate'),

    path('plotinsoccuvsincstatestacked/',plotinsoccuvsincstatestacked.as_view(),name='plotinsoccuvsincstatestacked'),

    path('stripplot/',stripplot.as_view(),name='stripplot'),

    path('distribution/',distribution.as_view(),name='distribution'),

    path('box_plot/',box_plot.as_view(),name='box_plot'),

    path('box_plot3d/',box_plot3d.as_view(),name='box_plot3d'),

    path('scattred3d/',scattred3d.as_view(),name='scattred3d'),

    path('confirmSrc/',confirmSrc.as_view(), name="confirmSrc"),

    path('send_mail_confirmSrc/',send_mail_confirmSrc.as_view(), name="send_mail_confirmSrc"),

    path('conceptualsoundness/',conceptualsoundness.as_view(), name="conceptualsoundness"),

    path('save_CS_Data/',save_CS_Data.as_view(), name="save_CS_Data"),

    path('imp_ctrl/',imp_ctrl.as_view(), name="imp_ctrl"),

    path('send_ImpCtrlCnfrm_Mail/',send_ImpCtrlCnfrm_Mail.as_view(), name="send_ImpCtrlCnfrm_Mail"),

    path('get_Section_Resp/',get_Section_Resp.as_view(), name="get_Section_Resp"),

    path('update_ImpCtrl_ReportComment/',update_ImpCtrl_ReportComment.as_view(), name="update_ImpCtrl_ReportComment"),

    path('modelUsage/',modelUsage.as_view(), name="modelUsage"),

    path('save_model_usage/',save_model_usage.as_view(), name="save_model_usage"),

    path('valFindings/',valFindings.as_view(), name="valFindings"),

    path('save_valFindings/',save_valFindings.as_view(), name="save_valFindings"),

    path('get_val_findings/',get_val_findings.as_view(), name="get_val_findings"),

    path('send_Mail_valFindings/',send_Mail_valFindings.as_view(), name="send_Mail_valFindings"),

    path('getvalFindings/',getvalFindings.as_view(),name='getvalFindings')        #Added by Shuvankar dated 2024.03.28

    , path('valFindingsResp/',valFindingsResp.as_view(), name="valFindingsResp")    #Added by Shuvankar dated 2024.03.28

    ,path('save_valFindingsResp/',save_valFindingsResp.as_view(), name="save_valFindingsResp"),



    path('get_ReportTtlData/',get_ReportTtlData.as_view(),name='get_ReportTtlData'),

    path('task_registration/',Task_Registration.as_view(),name='task_registration'),
    path('task_registration/<int:id>',Task_Registration.as_view(),name='task_registration'),
    path('get_sub_task_type/',get_sub_task_type.as_view(),name='get_sub_task_type'),

    path('sub_category_master/',Sub_Category_MasterAPI.as_view(),name="sub_category_master"),
    path('sub_category_master/<int:id>',Sub_Category_MasterAPI.as_view(),name="sub_category_master"),
    path('get_task_ID_data/',get_task_ID_data.as_view(),name='get_task_ID_data'),


    

    
    
]

