
from django.urls import path 

from . import issues

urlpatterns = [

    path('getIssues/',issues.rmse_calendar_issue,name='getIssues'),
    path('issue_registrartion/',issues.issue_registrartion,name='issue_registrartion'),
    path('get_sub_issue_type/',issues.get_sub_issue_type,name='get_sub_issue_type'),
    path('generate_issueID/',issues.generate_issueID,name='generate_issueID'),

    path('issue_assignee/',issues.issue_assignee,name='issue_assignee'),
    path('get_issue_ID_data/',issues.get_issue_ID_data,name='get_issue_ID_data'),
    path('issue_update_summery_data/',issues.issue_update_summery_data,name='issue_update_summery_data'),
    path('issue_approver/',issues.issue_approver,name='issue_approver'),
    path('edit_issue/<str:issue_id>/',issues.edit_issue,name='edit_issue'),

    

]