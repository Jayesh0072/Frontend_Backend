from django.urls import path


from .views import *
from .flView import * 
from .flDashb import *
from .tasks_Issues import task_approver,task_assignee,checkUserRole_Issue,issue_assignee,issue_approver,allocate_icq,save_allocation
urlpatterns = [ 
    path('getFL_Tbl_Cols/',getFL_Tbl_Cols.as_view(),name='getFL_Tbl_Cols'),
    path('getDistinct_Col_Val/',getDistinct_Col_Val.as_view(),name='getDistinct_Col_Val'),
    path('insert_Ctrl_Class_Criteria/',insert_Ctrl_Class_Criteria.as_view(),name='insert_Ctrl_Class_Criteria'),
    path('get_AIR/',get_AIR.as_view(),name="get_AIR"),
    path('GET_FL_Data_Info/',GET_FL_Data_Info.as_view(),name='GET_FL_Data_Info'),
    path('GET_FL_Data_Filter_Cnt/',GET_FL_Data_Filter_Cnt.as_view(),name='GET_FL_Data_Filter_Cnt'),
    path('Save_FL_Data_Filter_Cndn/',Save_FL_Data_Filter_Cndn.as_view(),name='Save_FL_Data_Filter_Cndn'),
    path('FieldAPI/',FieldAPI.as_view(),name='FieldAPI'),
    path('getFL_Ctrl_Class_Cols/',getFL_Ctrl_Class_Cols.as_view(),name='getFL_Ctrl_Class_Cols'),
    path('get_Steering_Dashb_Data/',get_Steering_Dashb_Data.as_view(),name='get_Steering_Dashb_Data'),
    path('get_Steering_Dashb_Data_peergroupappsGov/',get_Steering_Dashb_Data_peergroupappsGov.as_view(),name='get_Steering_Dashb_Data_peergroupappsGov'),
    path('get_Steering_Dashb_Data_peergroupapps/',get_Steering_Dashb_Data_peergroupapps.as_view(),name='get_Steering_Dashb_Data_peergroupapps'),
    path('get_Steering_Dashb_Data_appsGov/',get_Steering_Dashb_Data_appsGov.as_view(),name='get_Steering_Dashb_Data_appsGov'),
    path('get_Steering_Dashb_Data_apps/',get_Steering_Dashb_Data_apps.as_view(),name='get_Steering_Dashb_Data_apps'),
    path('updatePeerGroups/',updatePeerGroups.as_view(),name='updatePeerGroups'),
    path('get_Marketing_Dashb_Data_apps/',get_Marketing_Dashb_Data_apps.as_view(),name='get_Marketing_Dashb_Data_apps'),
    path('get_Marketing_Dashb_Data_peergroupapps/',get_Marketing_Dashb_Data_peergroupapps.as_view(),name='get_Marketing_Dashb_Data_peergroupapps'),
    path('get_Pricing_Dashb_Data_apps/',get_Pricing_Dashb_Data_apps.as_view(),name='get_Pricing_Dashb_Data_apps'),
    path('get_Pricing_Dashb_Data_ratespread/',get_Pricing_Dashb_Data_ratespread.as_view(),name='get_Pricing_Dashb_Data_ratespread'),
    path('saveriskcomments/',saveriskcomments.as_view(),name='saveriskcomments'),
    path('GetRiskFactorHistoryMsg/',GetRiskFactorHistoryMsg.as_view(), name="GetRiskFactorHistoryMsg"),    
    path('GetUtilityAPI/',GetUtilityAPI.as_view(),name='GetUtilityAPI'),
    path('FL_add_question/',FL_add_question.as_view(),name='FL_add_question'),
    path('Fl_sectionsAPI/',Fl_sectionsAPI.as_view(),name='Fl_sectionsAPI'),
    path('UsersgetAPI/',UsersgetAPI.as_view(),name='UsersgetAPI'),
    path('save_flallocation/',save_flallocation.as_view(),name='save_flallocation'),
    path('FLQtns/',FLQtns.as_view(),name='FLQtns'),
    path('submitFLRatings/',submitFLRatings.as_view(),name='submitFLRatings'),
    path('saveFLRatings/',saveFLRatings.as_view(),name='saveFLRatings'),
    path('get_State_Lat_long/',get_State_Lat_long.as_view(),name="get_State_Lat_long"),
    path('get_County_Lat_long/',get_County_Lat_long.as_view(),name="get_County_Lat_long"),
    path('get_Filter_State_Lat_long/',get_Filter_State_Lat_long.as_view(),name="get_Filter_State_Lat_long"),
    path('get_Filter_County_Lat_long/',get_Filter_County_Lat_long.as_view(),name="get_Filter_County_Lat_long"),
    path('FLSettingAPI/',FLSettingAPI.as_view(), name="FLSettingAPI"),
    path('get_DeniedRecordsMatchedPair/',get_DeniedRecordsMatchedPair.as_view(),name='get_DeniedRecordsMatchedPair'),
    path('Get_MatchedPairs_Data/',Get_MatchedPairs_Data.as_view(),name='Get_MatchedPairs_Data'),
    path('get_Bank_lat_long_state/',get_Bank_lat_long_state.as_view(),name="get_Bank_lat_long_state"),
    path('get_Bank_lat_long_county/',get_Bank_lat_long_county.as_view(),name="get_Bank_lat_long_county"),
    path('get_Marketing_Dashb_Data_ClassWise/',get_Marketing_Dashb_Data_ClassWise.as_view(),name="get_Marketing_Dashb_Data_ClassWise"),
    path('FLQtnsFinal/',FLQtnsFinal.as_view(),name='FLQtnsFinal'),
    path('getFLSecQtnFinal/',getFLSecQtnFinal.as_view(),name='getFLSecQtnFinal'),
    path('saveFLRatingsFinal/',saveFLRatingsFinal.as_view(),name='saveFLRatingsFinal'),
    path('get_Marketing_Dashb_Data_IncomeGrp/',get_Marketing_Dashb_Data_IncomeGrp.as_view(),name='get_Marketing_Dashb_Data_IncomeGrp'),
    path('get_AIR_Varwise/',get_AIR_Varwise.as_view(),name='get_AIR_Varwise'),
    path('get_Pricing_Dashb_Data_apps_Varwise/',get_Pricing_Dashb_Data_apps_Varwise.as_view(),name='get_Pricing_Dashb_Data_apps_Varwise'),
    path('get_Pricing_Dashb_Data_ratespread_Varwise/',get_Pricing_Dashb_Data_ratespread_Varwise.as_view(),name='get_Pricing_Dashb_Data_ratespread_Varwise'),
    path('get_Steering_Dashb_Data_apps_Varwise/',get_Steering_Dashb_Data_apps_Varwise.as_view(),name='get_Steering_Dashb_Data_apps_Varwise') ,
    path('get_Denials_Varwise/',get_Denials_Varwise.as_view(),name='get_Denials_Varwise')     ,
    path('get_CountyMedianIncome/',get_CountyMedianIncome.as_view(),name="get_CountyMedianIncome"),       
    path('saveimagedata/',saveimagedata.as_view(),name="saveimagedata"), 
    path('get_FL_Report_Data_Varwise/',get_FL_Report_Data_Varwise.as_view(),name="get_FL_Report_Data_Varwise"), 
    ##Ashok code
    path('fl_data_file_info/',fl_data_file_info.as_view(),name='fl_data_file_info'),
    path('get_Filter_Selected/',get_Filter_Selected.as_view(),name='get_Filter_Selected'),
    path('delete_Filter_Selected/',delete_Filter_Selected.as_view(),name='delete_Filter_Selected'),
    
 
     
]


