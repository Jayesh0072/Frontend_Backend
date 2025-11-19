import re
from django.urls import path, re_path,include
# from matplotlib.cbook import report_memory
from pandas import read_parquet

# from . import viewviex
from . import views_db as views   
# from . import vaexPlots 
from . import rmseviews
from . import tasks_Issues
from . import masterdata
from .rmseviews import addUser
# from . import exportFromIpynb
from django.urls import path 
from .views import *
from .rmseviews import *

urlpatterns = [
    path('', rmseviews.login,name="login"),  # type: ignore
    # path('dashboard/', rmseviews.dashboard,name="dashboard"),
    # path('projectsDetails/', rmseviews.projectsDetails,name="projectsDetails"),
    # path('addmodel/',rmseviews.addmodel,name='addmodel'),
    # path('addtool/',rmseviews.addtool,name='addtool'),
    path('todolist/',rmseviews.todolist,name='todolist'),
    path('activity/',rmseviews.activity,name='activity'),
    path('blank/',rmseviews.blank,name='blank'),
    path('blankadmin/',rmseviews.blankadmin,name='blankadmin'),
    path('blankvalidationtool/',rmseviews.blankvalidationtool,name='blankvalidationtool'),
    path('validateUser/', rmseviews.validateUser,name="validateUser"),
    path('test/',rmseviews.test,name='test'),
    path('rmse_users/',rmseviews.user,name='rmse_users'),
    path('addUser/',rmseviews.addUser,name='addUser'),
    path('rmse_usercat/',rmseviews.showusercat,name='rmse_usercat'),
    path('addnewusercatv/',rmseviews.addnewusercat,name='addnewusercatv'),
    path('addusercat/',rmseviews.addusercat,name='addusercat'),
    path('addnewuser/',rmseviews.addnewuser,name='addnewuser'),
    path('checkValue/',rmseviews.checkValue,name='checkValue'),
    path('useraccess/',rmseviews.useraccess,name='useraccess'),
    path('updateuseraccess/',rmseviews.updateuseraccess,name='updateuseraccess'),
    path('getReportsTo/',rmseviews.getReportsTo,name='getReportsTo'),
    path('showdept/',rmseviews.showdept,name='showdept'),
    path('newdept/',rmseviews.newdept,name='newdept'),
    path('adddept/',rmseviews.adddept,name='adddept'),
    path('getUserDept/',rmseviews.getUserDept,name='getUserDept'),
    path('criteriaQtns/',rmseviews.criteriaQtns,name='criteriaQtns'),
    path('addQuestion/',rmseviews.addQuestion,name='addQuestion'),
    path('criteriaSetting/',rmseviews.criteriaSetting,name='criteriaSetting'),
    path('getQtnSecWise/',rmseviews.getQtnSecWise,name='getQtnSecWise'),
    path('saveCriteria/',rmseviews.saveCriteria,name='saveCriteria'),
    path('saveModelTool/',rmseviews.saveModelTool,name='saveModelTool'),
    # path('getCriteria/',rmseviews.getCriteria,name='getCriteria'),
    # path('getMdlInfoById/',rmseviews.getMdlInfoById,name='getMdlInfoById'),
    # path('updateMdlVersion/',rmseviews.updateMdlVersion,name='updateMdlVersion'),
    # path('GetIsModel/',rmseviews.GetIsModel,name='GetIsModel'),
    path('masterTbls/',rmseviews.masterTbls,name='masterTbls'), # type: ignore
    path('addMasterOpts/',rmseviews.addMasterOpts,name='addMasterOpts'),
    path('getMasterTblbyId/',rmseviews.getMasterTblbyId,name='getMasterTblbyId'),
    # path('getMdlDetailsById/',rmseviews.getMdlDetailsById,name='getMdlDetailsById'),
    path('getUCAccessData/',rmseviews.getUCAccessData,name='getUCAccessData'),
    path('userAddedBy/',rmseviews.userAddedBy,name='userAddedBy'),
    path('deptaddnewuser/',rmseviews.deptaddnewuser,name='deptaddnewuser'),
    path('deptuseraccess/',rmseviews.deptuseraccess,name='deptuseraccess'),
    path('getUCAccessDataDeptWise/',rmseviews.getUCAccessDataDeptWise,name='getUCAccessDataDeptWise'),
    path('updateDeptuseraccess/',rmseviews.updateDeptuseraccess,name='updateDeptuseraccess'),
    path('reqValidation/',rmseviews.reqValidation,name='reqValidation'),
    path('assignValidation/',rmseviews.assignValidation,name='assignValidation'), 
    path('getAssignedTo/',rmseviews.getAssignedTo,name='getAssignedTo'), 
    path('getnotifications/',rmseviews.getnotifications,name='getnotifications'), 
        path('addusrdashbcontent/', masterdata.addusrdashbcontent,name="addusrdashbcontent"),
#task function
    path('showtaskfun/',masterdata.showtaskfun,name='showtaskfun'),
#     path('redirectError/$',masterdata.redirectError,name='redirectError'),
    # path('redirectError/<str:pk>/', masterdata.redirectError, name='redirectError'),
    path('newtaskfun/',masterdata.newtaskfun,name='newtaskfun'),
    path('addtskfun/',masterdata.addtskfun,name='addtskfun'),
    #task type
    path('showtasktype/',masterdata.showtasktype,name='showtasktype'),
    path('newtasktype/',masterdata.newtasktype,name='newtasktype'),
    path('addtsktype/',masterdata.addtsktype,name='addtsktype'),
    #sub task type
    path('showsubtasktype/',masterdata.showsubtasktype,name='showsubtasktype'),
    path('newsubtasktype/',masterdata.newsubtasktype,name='newsubtasktype'),
    path('addsubtsktype/',masterdata.addsubtsktype,name='addsubtsktype'),
    #task priority
    path('showtaskpriority/',masterdata.showtaskpriority,name='showtaskpriority'),
    path('newtaskpriority/',masterdata.newtaskpriority,name='newtaskpriority'),
    path('addtskpriority/',masterdata.addtskpriority,name='addtskpriority'),
    #task approval status
    path('showtaskapprovalstatus/',masterdata.showtaskapprovalstatus,name='showtaskapprovalstatus'),
    path('newtaskapprovalstatus/',masterdata.newtaskapprovalstatus,name='newtaskapprovalstatus'),
    path('addtskapprovalstatus/',masterdata.addtskapprovalstatus,name='addtskapprovalstatus'),
    
    #Update Profile
    path('updateprofile/',masterdata.updateprofile,name='updateprofile'),
    path('updateprofilerecord/', masterdata.updateprofilerecord, name='updateprofilerecord'),
#     path('updateprofile1/', masterdata.updateprofile1,name='updateprofile1')
    #Dashboard content
    path('showdashboardcontent/',masterdata.showdashboardcontent,name='showdashboardcontent'),
    path('newdashboardcontent/',masterdata.newdashboardcontent,name='newdashboardcontent'),
    path('adddashboardcontent/',masterdata.adddashboardcontent,name='adddashboardcontent'),

        # path('task_registration/',tasks_Issues.task_registration,name='task_registration'),
    # path('get_sub_task_type/',tasks_Issues.get_sub_task_type,name='get_sub_task_type'),
    path('alert/',tasks_Issues.alert,name='alert'),
    path('show_alert/',tasks_Issues.show_alert,name='show_alert'),
    # path('issue_registrartion/',tasks_Issues.issue_registrartion,name='issue_registrartion'),
    # path('get_sub_issue_type/',tasks_Issues.get_sub_issue_type,name='get_sub_issue_type'),
    # path('generate_issueID/',tasks_Issues.generate_issueID,name='generate_issueID'),
    # path('generate_task_ID/',tasks_Issues.generate_task_ID,name='generate_task_ID'),
    # path('task_assignee/',tasks_Issues.task_assignee,name='task_assignee'),
    # path('get_task_ID_data/',tasks_Issues.get_task_ID_data,name='get_task_ID_data'),
    # path('update_summery_data/',tasks_Issues.update_summery_data,name='update_summery_data'),
    # path('task_approver/',tasks_Issues.task_approver,name='task_approver'),
    #     path('issue_assignee/',tasks_Issues.issue_assignee,name='issue_assignee'), 
    # path('get_issue_ID_data/',tasks_Issues.get_issue_ID_data,name='get_issue_ID_data'),
    # path('issue_update_summery_data/',tasks_Issues.issue_update_summery_data,name='issue_update_summery_data'),
        path('thread_creation/',rmseviews.thread_creation,name='thread_creation'),    
     path('addICQQtns/',rmseviews.addICQQtns,name='addICQQtns'),   
     path('addSection/',rmseviews.addSection,name='addSection'),   
path('addSub_Section/',rmseviews.addSub_Section,name='addSub_Section'),
path('addSub_Sub_Section/',rmseviews.addSub_Sub_Section,name='addSub_Sub_Section'),
path('getSub_Sections/',rmseviews.getSub_Sections,name='getSub_Sections'),
path('getSub_Sub_Sections/',rmseviews.getSub_Sub_Sections,name='getSub_Sub_Sections'),
path('addSub_Sub_Sub_Section/',rmseviews.addSub_Sub_Sub_Section,name='addSub_Sub_Sub_Section'),
path('ICQQtns/',rmseviews.ICQQtns,name='ICQQtns'),
# path('getICQSections/',rmseviews.getICQSections,name='getICQSections'),
path('getICQSecQtn/',rmseviews.getICQSecQtn,name='getICQSecQtn'),
path('saveICQRatings/',rmseviews.saveICQRatings,name='saveICQRatings'),
 path('show_task/',tasks_Issues.show_task,name='show_task'),
    # path('edit_task/<str:task_id>/',tasks_Issues.edit_task,name='edit_task'),
    # path('edit_issue/<str:issue_id>/',tasks_Issues.edit_issue,name='edit_issue'),
    path('show_issue/',tasks_Issues.show_issue,name='show_issue'),


    path('getSub_Sub_Sub_Sections/',rmseviews.getSub_Sub_Sub_Sections,name='getSub_Sub_Sub_Sections'),
    path('add_question/',rmseviews.add_question,name='add_question'),
    path('icq_ratings/',rmseviews.icq_ratings,name='icq_ratings'),
    path('save_ratings/',rmseviews.save_ratings,name='save_ratings'),
    path('submitICQRatings/',rmseviews.submitICQRatings,name='submitICQRatings'),
    # path('ICQQtnsFinal/',rmseviews.ICQQtnsFinal,name='ICQQtnsFinal'),
    # path('saveICQRatingsFinal/',rmseviews.saveICQRatingsFinal,name='saveICQRatingsFinal'),
    path('ICQQuestions/',rmseviews.ICQQuestions,name='ICQQuestions'),
    path('showICQSetting/',rmseviews.showICQSetting,name='showICQSetting'),
    path('newICQSetting/',rmseviews.newICQSetting,name='newICQSetting'),
    path('addICQSetting/',rmseviews.addICQSetting,name='addICQSetting'),
    path('get_parent_Sections/',tasks_Issues.get_parent_Sections,name='get_parent_Sections'),
# path('save_allocation/',tasks_Issues.save_allocation,name='save_allocation') ,
# path('allocate_icq/',tasks_Issues.allocate_icq,name='allocate_icq') ,
# path('getICQSecQtnFinal/',rmseviews.getICQSecQtnFinal,name='getICQSecQtnFinal'),
path('newquerybuilder/',rmseviews.newquerybuilder,name='newquerybuilder'),
path('query_filter/',rmseviews.query_filter,name='query_filter'),
 path('SpecificSong/', rmseviews.SpecificSong,name='SpecificSong'),
#  path('publushICQ/',rmseviews.publushICQ,name='publushICQ'),
 path('viewFiltredDataType/',views.viewFiltredDataType,name='viewFiltredDataType'),
 path('Query_builder_filter/',rmseviews.Query_builder_filter,name='Query_builder_filter'),
 path('getVTModelsSegments/',views.getVTModelsSegments,name='getVTModelsSegments'),
 path('PdfSummary/',rmseviews.PdfSummary,name='PdfSummary'),
 path('pdfsummaryresp/',rmseviews.pdfsummaryresp,name='pdfsummaryresp'),
 path('codereview/',rmseviews.codereview,name='codereview'),
  path('uploadDecommDoc/',rmseviews.uploadDecommDoc,name='uploadDecommDoc'),
  path('checkPendingTasksIssues/',rmseviews.checkPendingTasksIssues,name='checkPendingTasksIssues'),
path('getDecommDoc/',rmseviews.getDecommDoc,name='getDecommDoc'), 
path('savePDFResp/',rmseviews.savePDFResp,name='savePDFResp'),

#for model qtns
path('QtnsResp/',rmseviews.QtnsResp,name='QtnsResp'),
path('getModelQtnBySrc/',rmseviews.getModelQtnBySrc,name='getModelQtnBySrc'),
path('getQtnResp/',rmseviews.getQtnResp,name='getQtnResp'), 
path('insertQtnResp/',rmseviews.insertQtnResp,name='insertQtnResp'), 
path('getQtnRespById/',rmseviews.getQtnRespById,name='getQtnRespById'), 
path('mmrkasRead/',rmseviews.mmrkasRead,name='mmrkasRead'), 

path('Questions/',rmseviews.Questions,name='Questions') ,
path('addQtns/',rmseviews.addQtns,name='addQtns'),
path('addQuesSection/',rmseviews.addQuesSection,name='addQuesSection'),   
path('addQuesSub_Section/',rmseviews.addQuesSub_Section,name='addQuesSub_Section'),
path('addQuesSub_Sub_Section/',rmseviews.addQuesSub_Sub_Section,name='addQuesSub_Sub_Section'),
path('getQuesSub_Sections/',rmseviews.getQuesSub_Sections,name='getQuesSub_Sections'),
path('getQuesSub_Sub_Sections/',rmseviews.getQuesSub_Sub_Sections,name='getQuesSub_Sub_Sections'),
path('getQuesSub_Sub_Sub_Sections/',rmseviews.getQuesSub_Sub_Sub_Sections,name='getQuesSub_Sub_Sub_Sections'),
path('addQuesSub_Sub_Sub_Section/',rmseviews.addQuesSub_Sub_Sub_Section,name='addQuesSub_Sub_Sub_Section'),    
path('addQues_question/',rmseviews.addQues_question,name='addQues_question'),
path('allocate_questions/',rmseviews.allocate_questions,name='allocate_questions') ,
path('get_Qtn_Section/',rmseviews.get_Qtn_Section,name='get_Qtn_Section') ,
path('save_Question_allocation/',rmseviews.save_Question_allocation,name='save_Question_allocation'),
path('getQues_Sections/',rmseviews.getQues_Sections,name='getQues_Sections'),
path('QuestionsAllUsers/',rmseviews.QuestionsAllUsers,name='QuestionsAllUsers'),
path('addQtnsAllUsers/',rmseviews.addQtnsAllUsers,name='addQtnsAllUsers'),
path('edit_department/<str:id>/',rmseviews.edit_department,name='edit_department'),
    path('edit_user_cat/<str:id>/',rmseviews.edit_user_cat,name='edit_user_cat'),
    path('edit_user/<str:id>/',rmseviews.edit_user,name='edit_user'),
    path('insertQtnAnsr/',rmseviews.insertQtnAnsr,name='insertQtnAnsr'),
    path('getQtnAns/',rmseviews.getQtnAns,name='getQtnAns'),
    # path('getTasks/',rmseviews.rmse_calendar,name='getTasks'),
    #  path('checkUserRole/',tasks_Issues.checkUserRole,name='checkUserRole'),

    #  path('getIssues/',rmseviews.rmse_calendar_issue,name='getIssues'),
# path('checkUserRole_Issue/',tasks_Issues.checkUserRole_Issue,name='checkUserRole_Issue'),
path('showmasterTbls/',rmseviews.showmasterTbls,name='showmasterTbls'),
path('editmasterTbls/<str:id>/<str:page>/',rmseviews.editmasterTbls,name='editmasterTbls'),
path('modelfields/',rmseviews.modelfields,name='modelfields'),
path('updateFields/',rmseviews.updateFields,name='updateFields'), 
path('ModelArtifacts/',rmseviews.ModelArtifacts,name='ModelArtifacts'),
path('editregmodel/',rmseviews.editregmodel,name='editregmodel'),
path('updateregmodel/',rmseviews.updateregmodel,name='updateregmodel'),
# path('issubmit/',rmseviews.issubmit,name='issubmit'),
path('save_OnlyQuestion_allocation/',rmseviews.save_OnlyQuestion_allocation,name='save_OnlyQuestion_allocation'),
path('showrolesrespqtn/',rmseviews.showrolesrespqtn,name='showrolesrespqtn'),
path('newrolesrespqtn/',rmseviews.newrolesrespqtn,name='newrolesrespqtn'),
path('addrolesrespqtn/',rmseviews.addrolesrespqtn,name='addrolesrespqtn'),
path('editrolesrespqtn//<str:id>/',rmseviews.editrolesrespqtn,name='editrolesrespqtn'),
path('updaterolesrespqtn/',rmseviews.updaterolesrespqtn,name='updaterolesrespqtn'),

path('showauditregcompl/',rmseviews.showauditregcompl,name='showauditregcompl'),
path('newauditregcompl/',rmseviews.newauditregcompl,name='newauditregcompl'),
path('addauditregcompl/',rmseviews.addauditregcompl,name='addauditregcompl'),
path('editauditregcompl//<str:id>/',rmseviews.editauditregcompl,name='editauditregcompl'),
path('updateauditregcompl/',rmseviews.updateauditregcompl,name='updateauditregcompl'),
path('numtostring/',views.numtostring,name='dtTypeConversion'),  
path('updatenumtostring/',views.updatenumtostring,name='updatenumtostring'),  
path('newauditallocation/',rmseviews.newauditallocation,name='newauditallocation'),
path('saveauditallocation/',rmseviews.saveauditallocation,name='saveauditallocation'),
path('savemodalauditquestion/',rmseviews.savemodalauditquestion,name='savemodalauditquestion'),
path('newauditresponse/',rmseviews.newauditresponse,name='newauditresponse'),
path('saveauditresponse/',rmseviews.saveauditresponse,name='saveauditresponses'),
path('newquestionallocation/',rmseviews.newquestionallocation,name='newquestionallocation'),
path('savequestionallocation/',rmseviews.savequestionallocation,name='savequestionallocation'),
path('savemodalrespquestion/',rmseviews.savemodalrespquestion,name='savemodalrespquestion'),
path('newquestionresponse/',rmseviews.newquestionresponse,name='newquestionresponse'),
path('savequestionresponse/',rmseviews.savequestionresponse,name='savequestionresponse'),
path('convertDataType/',views.convertDataType,name='convertDataType'),
path('getAUditQtns/',rmseviews.getAUditQtns,name='getAUditQtns'),
path('getAuditQtnsAns/',rmseviews.getAuditQtnsAns,name='getAuditQtnsAns'),
path('BackupFor_userdetails/',rmseviews.BackupFor_userdetails,name='BackupFor_userdetails'),
# path('activitytrail/',rmseviews.activitytrail,name='activitytrail'), 
path('logout/',rmseviews.logout,name='logout'), 
path('tempdetails/',rmseviews.tempdetails,name='tempdetails'),
path('getTempMdlDetailsById/',rmseviews.getTempMdlDetailsById,name='getTempMdlDetailsById'),
path('ApproveEdit/',rmseviews.ApproveEdit,name='ApproveEdit'),

path('mdlselectionscreen/',rmseviews.mdlselectionscreen,name='mdlselectionscreen'),
path('checkutype/',rmseviews.checkutype,name='checkutype'),


path('vrsuballocationsave/',rmseviews.vrsuballocationsave,name='vrsuballocationsave'),
path('vrsuballocationscreen/',rmseviews.vrsuballocationscreen,name='vrsuballocationscreen'),
path('checkutype1/',rmseviews.checkutype1,name='checkutype1'),

path('showfrequency/',rmseviews.showfrequency,name='showfrequency'),
path('newfrequency/',rmseviews.newfrequency,name='newfrequency'),
path('addfrequency/',rmseviews.addfrequency,name='addfrequency'),
path('edit_frequency/<str:id>/',rmseviews.edit_frequency,name='edit_frequency'),
# path('addperfromancediscussion/',rmseviews.addperfromancediscussion,name='addperfromancediscussion'),
# path('PerfMontrSetup/',rmseviews.PerfMontrSetup,name='PerfMontrSetup'),
# path('gethistorymsg/',rmseviews.gethistorymsg,name='gethistorymsg'),
path('Fetchmodelmatrics/',rmseviews.Fetchmodelmatrics,name='Fetchmodelmatrics'),
# path('savemodelmatrics/',rmseviews.savemodelmatrics,name='savemodelmatrics'),

# path('UpdateModelMatricsData/',rmseviews.UpdateModelMatricsData,name='UpdateModelMatricsData'),
# path('PerfMontrPrdnData/',rmseviews.PerfMontrPrdnData,name='PerfMontrPrdnData'),
# path('mmlabeltoexcel/',rmseviews.mmlabeltoexcel,name='mmlabeltoexcel'),
# path('Perf_monitoring_file_upload/',rmseviews.Perf_monitoring_file_upload,name='Perf_monitoring_file_upload'),
path('PerfMontr/',rmseviews.PerfMontr,name='PerfMontr'),
# path('PerfMontrDataFetch/',rmseviews.PerfMontrDataFetch,name='PerfMontrDataFetch'),
# path('savemdlmetrics/',rmseviews.savemdlmetrics,name='savemdlmetrics'), //To be added
# Master code 0612
path('showModelMetrics/',rmseviews.showModelMetrics,name='showModelMetrics'),
path('addModelMetrics/',rmseviews.addModelMetrics,name='addModelMetrics'),
path('edit_ModelMetricsMaster/<str:id>/',rmseviews.edit_ModelMetricsMaster,name='edit_ModelMetricsMaster'),
path('savemodelmetrics/',rmseviews.savemodelmetrics,name='savemodelmetrics'),

  ##business metric
path('addBusinessMetrics/',rmseviews.addBusinessMetrics,name='addBusinessMetrics'),
path('savebusinessmetrics/',rmseviews.savebusinessmetrics,name='savebusinessmetrics'),
path('showbusinessmetrics/',rmseviews.showbusinessmetrics,name='showbusinessmetrics'),
path('edit_BusinessMetricsMaster/<str:id>/',rmseviews.edit_BusinessMetricsMaster,name='edit_BusinessMetricsMaster'),
path('getSubcat/',rmseviews.getSubcat,name='getSubcat'),

path('show_frequecy/',rmseviews.showfrequency,name='show_frequecy'),
path('new_frequecy/',rmseviews.newfrequency,name='new_frequecy'),

path('add_frequency/',rmseviews.addfrequency,name='add_frequency'),

path('edit_frequency_master/<str:id>/',rmseviews.edit_frequency,name='edit_frequency_master'),
# path('savebusinessmatrics/',rmseviews.savebusinessmatrics,name='savebusinessmatrics'),
# path('savebusmetrics/',rmseviews.savebusmetrics,name='savebusmetrics'),
path('gethistorymsgbus/',rmseviews.gethistorymsgbus,name='gethistorymsgbus'),
# path('mmlabeltoexcelforbus/',rmseviews.mmlabeltoexcelforbus,name='mmlabeltoexcelforbus'),
# path('Perf_monitoring_file_upload_bus/',rmseviews.Perf_monitoring_file_upload_bus,name='Perf_monitoring_file_upload_bus'),
# path('UpdatebusinessMatricsDatabus/',rmseviews.UpdatebusinessMatricsDatabus,name='UpdatebusinessMatricsDatabus'),
# path('PerfMontrSetupMRM/',rmseviews.PerfMontrSetupMRM,name='PerfMontrSetupMRM'),
# path('getMdlDataForMRM/',rmseviews.getMdlDataForMRM,name='getMdlDataForMRM'),
# path('getBusinessDataForMRM/',rmseviews.getBusinessDataForMRM,name='getBusinessDataForMRM'),
# path('ApproveModelMatricsData/',rmseviews.ApproveModelMatricsData,name='ApproveModelMatricsData'),
# path('ApproveBusinessMatricsData/',rmseviews.ApproveBusinessMatricsData,name='ApproveBusinessMatricsData'),

# path('datamatricsfeature/',rmseviews.datamatricsfeature,name='datamatricsfeature'),
# path('datamatricsfeatureMRM/',rmseviews.datamatricsfeatureMRM,name='datamatricsfeatureMRM'),
# path('SaveTempFeatureMatricData/',rmseviews.SaveTempFeatureMatricData,name='SaveTempFeatureMatricData'),
# path('selectdataMetric/',rmseviews.selectdataMetric,name='selectdataMetric'),
# path('savedatamatrics/',rmseviews.savedatamatrics,name='savedatamatrics'),

# path('home2/', views.home2, name="home2"),
# path('mmlabeltoexcelfordata/',rmseviews.mmlabeltoexcelfordata,name='mmlabeltoexcelfordata'),
# path('gethistorymsgdata/',rmseviews.gethistorymsgdata,name='gethistorymsgdata'),

# path('ApproveDataMatricsData/',rmseviews.ApproveDataMatricsData,name='ApproveDataMatricsData'),
path('prdn_data/',rmseviews.prdn_data,name='prdn_data'),
path('Save_Data_Monitoring_Override_History/',rmseviews.Save_Data_Monitoring_Override_History,name='Save_Data_Monitoring_Override_History'),
path('Save_Data_Monitoring_Final_Result/',rmseviews.Save_Data_Monitoring_Final_Result,name='Save_Data_Monitoring_Final_Result'),

# path('Update_Performance_Monitoring_Override_History/',rmseviews.Update_Performance_Monitoring_Override_History,name='Update_Performance_Monitoring_Override_History'),
# path('PerfMontrDataFetch_MRMApprl/',rmseviews.PerfMontrDataFetch_MRMApprl,name='PerfMontrDataFetch_MRMApprl'),

# path('PerfMontrMRM/',rmseviews.PerfMontrMRM,name='PerfMontrMRM'),
# path('DataMontrOverHistory/',rmseviews.DataMontrOverHistory,name='DataMontrOverHistory'),
# path('Update_Data_Monitoring_Override_History/',rmseviews.Update_Data_Monitoring_Override_History,name='Update_Data_Monitoring_Override_History'),

# path('Save_Performance_Monitoring_Resolution/',rmseviews.Save_Performance_Monitoring_Resolution,name='Save_Performance_Monitoring_Resolution'),
path('Save_Performance_Monitoring_Override_History/',rmseviews.Save_Performance_Monitoring_Override_History,name='Save_Performance_Monitoring_Override_History'),
path('Save_Performance_Monitoring_Final_Result/',rmseviews.Save_Performance_Monitoring_Final_Result,name='Save_Performance_Monitoring_Final_Result'),
 

  ## Issue Registration

    # path('issue_registrartion/',tasks_Issues.issue_registrartion,name='issue_registrartion'),
    # path('get_sub_issue_type/',tasks_Issues.get_sub_issue_type,name='get_sub_issue_type'),
    # path('generate_issueID/',tasks_Issues.generate_issueID,name='generate_issueID'),

    # path('getIssues/',rmseviews.rmse_calendar_issue,name='getIssues'),
     
    ## Issue Assignee 

    # path('issue_assignee/',tasks_Issues.issue_assignee,name='issue_assignee'),
    # path('get_issue_ID_data/',tasks_Issues.get_issue_ID_data,name='get_issue_ID_data'),
    # path('issue_update_summery_data/',tasks_Issues.issue_update_summery_data,name='issue_update_summery_data'),
    
    # ## Issue Approver
    # path('issue_approver/',tasks_Issues.issue_approver,name='issue_approver'),
 


    #Findings val and category
    path('showfindvalelement/',rmseviews.showfindvalelement,name='showfindvalelement'),
    path('newfindvalelement/',rmseviews.newfindvalelement,name='newfindvalelement'),
    path('addfindvalelement/',rmseviews.addfindvalelement,name='addfindvalelement'),
    path('edit_findvalelement/<str:id>/',rmseviews.edit_findvalelement,name='edit_findvalelement'),

    path('showfindcategory/',rmseviews.showfindcategory,name='showfindcategory'),
    path('newfindcategory/',rmseviews.newfindcategory,name='newfindcategory'),
    path('addfindcategory/',rmseviews.addfindcategory,name='addfindcategory'),
    path('edit_findcategory/<str:id>/',rmseviews.edit_findcategory,name='edit_findcategory'),
    path('GetModelIdFindVal/',rmseviews.GetModelIdFindVal,name='GetModelIdFindVal'),

  
#     path('edit_task_function/<str:id>/',tasks_Issues.edit_task_function,name='edit_task_function'),
#     path('edit_task_type/<str:id>/',tasks_Issues.edit_task_type,name='edit_task_type'),
#     path('edit_task_priority/<str:id>/',tasks_Issues.edit_task_priority,name='edit_task_priority'),
#     path('edit_task_approval/<str:id>/',tasks_Issues.edit_task_approval,name='edit_task_approval'),
#     path('edit_sub_task_type/<str:id>/',tasks_Issues.edit_sub_task_type,name='edit_sub_task_type')

    path('showfindvalsubelement/',rmseviews.showfindvalsubelement,name='showfindvalsubelement'),
    path('newfindvalsubelement/',rmseviews.newfindvalsubelement,name='newfindvalsubelement'),
    path('addfindvalsubelement/',rmseviews.addfindvalsubelement,name='addfindvalsubelement'),
    path('edit_findvalsubelement/<str:id>/',rmseviews.edit_findvalsubelement,name='edit_findvalsubelement'),

    path('CriteriaQuestionList/',rmseviews.CriteriaQuestionList,name='CriteriaQuestionList'),
    path('newCriteriaQuestion/',rmseviews.newCriteriaQuestion,name='newCriteriaQuestion'),
    path('addQuestionSection/',rmseviews.addQuestionSection,name='addQuestionSection'),
    path('edit_QuestionSection/<str:id>/',rmseviews.edit_QuestionSection,name='edit_QuestionSection'),
    # path('issueLst/',rmseviews.issueLst,name='issueLst'),
    # path('getIssuesByQtrOrMonth/',rmseviews.getIssuesByQtrOrMonth,name='getIssuesByQtrOrMonth'),
    
    path('showIssueTypesAssesment/',rmseviews.showIssueTypesAssesment,name='showIssueTypesAssesment'),
    path('SaveValidationRatings/',rmseviews.SaveValidationRatings,name='SaveValidationRatings'),
    path('ValidationRatingsdata/',rmseviews.ValidationRatingsdata,name='ValidationRatingsdata'),

    #val findings screen        
    # path('valFindings/',rmseviews.valFindings,name='valFindings'),
    path('validation_findings/',rmseviews.validation_findings,name='validation_findings'),
    path('generate_findings_pdf/', rmseviews.generate_findings_pdf, name='generate_findings_pdf'),
    # path('get_sub_valData/',rmseviews.get_sub_valData,name='get_sub_valData'),
    # path('savevalFindings/',rmseviews.savevalFindings,name='savevalFindings'),
    path('update_response/',rmseviews.update_response,name='update_response'), 
    path('getfindingsID/',rmseviews.getfindingsID,name='getfindingsID'),
    # path('savevalFindingsComment/',rmseviews.savevalFindingsComment,name='savevalFindingsComment'),

    path('Get_Title_Label/',rmseviews.Get_Title_Label,name='Get_Title_Label'),
    path('getReportTtlHdr/',rmseviews.getReportTtlHdr,name='getReportTtlHdr'), 
    path('save_desc_comments/',rmseviews.save_desc_comments,name='save_desc_comments'),
    path('validation_comments/',rmseviews.validation_comments,name='validation_comments'),
    path('get_val_comments_data/',rmseviews.get_val_comments_data,name='get_val_comments_data'), 
    path('insert_VT_Discussion_Comments/',rmseviews.insert_VT_Discussion_Comments,name='insert_VT_Discussion_Comments'),
    path('ValidationCommentHistory/',rmseviews.ValidationCommentHistory,name='ValidationCommentHistory'),
    # path('modelList/',rmseviews.modelList,name='modelList'),
    # path('modelDetails/',rmseviews.modelDetails,name='modelDetails'),
    path('multiple_data_import/',views.multiple_data_import,name='multiple_data_import'),

    path('is_primery_check/',views.is_primery_check,name='is_primery_check'),
    path('mergedfile2/',views.mergedfile2,name='mergedfile2'),
    path('mergedInfo/',views.mergedInfo,name='mergedInfo'),
    path('SaveModelData/',views.SaveModelData,name='SaveModelData'),

    # Mapping Urls Merged info 
   path('mapping/',views.mapping,name='mapping'),
   path('get_colums_mapping/',views.get_colums_mapping,name='get_colums_mapping'),
   path('get_columns_DV/',views.get_columns_DV,name='get_columns_DV'),
   path('save_mapping/',views.save_mapping,name='save_mapping'),

 
 
#    path('ModelMatricsData/',rmseviews.ModelMatricsData,name='ModelMatricsData'),

   path('edit_task_function/<str:id>/',rmseviews.edit_task_function,name='edit_task_function'), 
   path('edit_task_type/<str:id>/',rmseviews.edit_task_type,name='edit_task_type'),
   path('edit_task_priority/<str:id>/',rmseviews.edit_task_priority,name='edit_task_priority'),
   path('edit_task_approval/<str:id>/',rmseviews.edit_task_approval,name='edit_task_approval'),
   path('edit_sub_task_type/<str:id>/',rmseviews.edit_sub_task_type,name='edit_sub_task_type'),

   path('uploadfiles/',rmseviews.uploadfiles,name='uploadfiles'),

   path('show_issue_function/',rmseviews.show_issue_function,name='show_issue_function'),
    path('add_new_issue/',rmseviews.add_new_issue,name='add_new_issue'),
    path('save_issue_function/',rmseviews.save_issue_function,name='save_issue_function'),
        path('edit_issue_function/<str:id>/',rmseviews.edit_issue_function,name='edit_issue_function'), 
          path('bankDetails/',rmseviews.bankDetails,name='bankDetails'),
    path('email_details/',rmseviews.email_details,name='email_details'),
    path('scheduler_notification/', rmseviews.scheduler_notification, name='scheduler_notification'),
    path('get_alert_schedule_data/', rmseviews.get_alert_schedule_data, name='get_alert_schedule_data'),


path('addbank/',rmseviews.addbank,name='addbank'),
# path('getModelsByValFindingsPriority/', rmseviews.getModelsByValFindingsPriority,name="getModelsByValFindingsPriority"),
path('show_mdl_category',rmseviews.show_mdl_category,name='show_mdl_category'),
path('add_category',rmseviews.add_category,name='add_category'),
path('save_category/',rmseviews.save_category,name='save_category'),
path('edit_category/<str:id>/',rmseviews.edit_category,name='edit_category'),

path('show_sub_mdl_category',rmseviews.show_sub_mdl_category,name='show_sub_mdl_category'),
path('add_sub_category',rmseviews.add_sub_category,name='add_sub_category'),
path('save_sub_category/',rmseviews.save_sub_category,name='save_sub_category'),
path('edit_sub_category/<str:id>/',rmseviews.edit_sub_category,name='edit_sub_category'),
# path('ICQFetchResidualRating/',rmseviews.ICQFetchResidualRating,name='ICQFetchResidualRating'),
path('task_approver_data/',rmseviews.task_approver_data,name='task_approver_data'),
path('issue_approver_data/',rmseviews.issue_approver_data,name='issue_approver_data'),
path('getfindingsData/',rmseviews.getfindingsData,name='getfindingsData'),
path('show_issue_priority/',rmseviews.show_issue_priority,name='show_issue_priority'),
path('add_issue_priority/',rmseviews.add_issue_priority,name='add_issue_priority'),
path('save_issue_priority/',rmseviews.save_issue_priority,name='save_issue_priority'),
path('show_issue_approval_status/',rmseviews.show_issue_approval_status,name='show_issue_approval_status'),
path('add_issue_approval/',rmseviews.add_issue_approval,name='add_issue_approval'),
path('save_issue_approval_status/',rmseviews.save_issue_approval_status,name='save_issue_approval_status'),
path('show_issue_type/',rmseviews.show_issue_type,name='show_issue_type'),
path('add_issue_type/',rmseviews.add_issue_type,name='add_issue_type'),
path('save_issue_type/',rmseviews.save_issue_type,name='save_issue_type'),
path('show_sub_issue/',rmseviews.show_sub_issue,name='show_sub_issue'),
path('add_sub_issue_type/',rmseviews.add_sub_issue_type,name='add_sub_issue_type'),
path('save_sub_issue_type/',rmseviews.save_sub_issue_type,name='save_sub_issue_type'),

path('edit_issue_type/<str:id>/',rmseviews.edit_issue_type,name='edit_issue_type'),
path('edit_sub_issue_type/<str:id>/',rmseviews.edit_sub_issue_type,name='edit_sub_issue_type'),
path('edit_issue_priority/<str:id>/',rmseviews.edit_issue_priority,name='edit_issue_priority'),
path('edit_issue_approval_status/<str:id>/',rmseviews.edit_issue_approval_status,name='edit_issue_approval_status'),
path('df_to_pdf/',rmseviews.df_to_pdf,name='df_to_pdf'),
path('model_committee/',rmseviews.model_committee,name='model_committee'),


]
