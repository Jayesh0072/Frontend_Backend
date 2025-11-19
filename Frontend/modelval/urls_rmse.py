import re
from django.urls import path, re_path
# from matplotlib.cbook import report_memory
from pandas import read_parquet
from pandas.core.dtypes.missing import na_value_for_dtype

# from . import viewviex  
from . import tasks_Issues as rmseviews 

urlpatterns = [
#path('show_issue_function/',rmseviews.show_issue_function,name='show_issue_function'),
# path('add_new_issue/',rmseviews.add_new_issue,name='add_new_issue'),
# path('save_issue_function/',rmseviews.save_issue_function,name='save_issue_function'),


#####Edit Issue master Edit Function,Type,Issue Type,Issue Priority,Issue Approval status

path('edit_issue_function/<str:id>/',rmseviews.edit_issue_function,name='edit_issue_function'),
path('edit_issue_type/<str:id>/',rmseviews.edit_issue_type,name='edit_issue_type'),
path('edit_sub_issue_type/<str:id>/',rmseviews.edit_sub_issue_type,name='edit_sub_issue_type'),
path('edit_issue_priority/<str:id>/',rmseviews.edit_issue_priority,name='edit_issue_priority'),
path('edit_issue_approval_status/<str:id>/',rmseviews.edit_issue_approval_status,name='edit_issue_approval_status'),
path('edit_task_function/<str:id>/',rmseviews.edit_task_function,name='edit_task_function'),
path('edit_task_type/<str:id>/',rmseviews.edit_task_type,name='edit_task_type'),
path('edit_task_priority/<str:id>/',rmseviews.edit_task_priority,name='edit_task_priority'),
path('edit_task_approval/<str:id>/',rmseviews.edit_task_approval,name='edit_task_approval'),
path('edit_sub_task_type/<str:id>/',rmseviews.edit_sub_task_type,name='edit_sub_task_type'),
]