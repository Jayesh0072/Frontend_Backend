
from django.urls import path 

from . import dashboard

urlpatterns = [

    path('dashboard/', dashboard.dashboard,name="dashboard"),
    path('getMdlDetailsById/',dashboard.getMdlDetailsById,name='getMdlDetailsById'),
    path('checkUserRole/',dashboard.checkUserRole,name='checkUserRole'),
    path('checkUserRole_Issue/',dashboard.checkUserRole_Issue,name='checkUserRole_Issue'),
    path('activitytrail/',dashboard.activitytrail,name='activitytrail'), 
    path('getIssuesByQtrOrMonth/',dashboard.getIssuesByQtrOrMonth,name='getIssuesByQtrOrMonth'),
    path('issueLst/',dashboard.issueLst,name='issueLst'),
    path('getModelsByValFindingsPriority/', dashboard.getModelsByValFindingsPriority,name="getModelsByValFindingsPriority"),
    path('modelList/',dashboard.modelList,name='modelList'),
    path("save_chart/", dashboard.save_chart, name="save_chart"),
    path("updateDashboardSetting/", dashboard.updateDashboardSetting, name="updateDashboardSetting"),
    path("save_comments_mdl_overview/", dashboard.save_comments_mdl_overview, name="save_comments_mdl_overview"),





]