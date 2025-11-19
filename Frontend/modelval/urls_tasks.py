import re
from django.urls import path, re_path,include
# from matplotlib.cbook import report_memory
from pandas import read_parquet
from pandas.core.dtypes.missing import na_value_for_dtype

# from . import viewviex
from . import views_db as views   
# from . import vaexPlots 
from . import rmseviews
from . import tasks_Issues
from . import masterdata
from .rmseviews import addUser
# from . import exportFromIpynb
from django.urls import path 

from . import tasks

urlpatterns = [
    path('getTasks/',tasks.rmse_calendar,name='getTasks'),
    path('task_registration/',tasks.task_registration,name='task_registration'),
    path('get_sub_task_type/',tasks.get_sub_task_type,name='get_sub_task_type'),
    path('generate_task_ID/',tasks.generate_task_ID,name='generate_task_ID'),
    path('task_approver/',tasks.task_approver,name='task_approver'),
    path('get_task_ID_data/',tasks.get_task_ID_data,name='get_task_ID_data'),
    path('update_summery_data/',tasks.update_summery_data,name='update_summery_data'),
    path('edit_task/<str:task_id>/',tasks.edit_task,name='edit_task'),
    path('task_assignee/',tasks.task_assignee,name='task_assignee'),


]