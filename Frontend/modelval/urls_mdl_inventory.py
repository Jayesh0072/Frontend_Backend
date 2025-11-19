from django.urls import path 

from . import mdl_inventory

urlpatterns = [

    path('modelList/',mdl_inventory.modelList,name='modelList'),
    path('getCriteria/',mdl_inventory.getCriteria,name='getCriteria'),
    path('GetIsModel/',mdl_inventory.GetIsModel,name='GetIsModel'),
    path('addmodel/',mdl_inventory.addmodel,name='addmodel'),
    path('addtool/',mdl_inventory.addtool,name='addtool'),
    path('issubmit/',mdl_inventory.issubmit,name='issubmit'),
    path('getMdlInfoById/',mdl_inventory.getMdlInfoById,name='getMdlInfoById'),
    path('updateMdlVersion/',mdl_inventory.updateMdlVersion,name='updateMdlVersion'),
    path('getSubcat/',mdl_inventory.getSubcat,name='getSubcat'),
    path('projectsDetails/', mdl_inventory.projectsDetails,name="projectsDetails"),
    path('pdf_request/', mdl_inventory.pdf_request,name="pdf_request"),
    path('data_show/', mdl_inventory.data_show, name='data_show'),









]   