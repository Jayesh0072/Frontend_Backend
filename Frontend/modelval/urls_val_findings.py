from django.urls import path 

from . import val_findings

urlpatterns = [
        path('valFindings/',val_findings.valFindings,name='valFindings'),
        path('valFindings_2/',val_findings.valFindings_2,name='valFindings_2'),
        path('get_sub_valData/',val_findings.get_sub_valData,name='get_sub_valData'),
        path('savevalFindings/',val_findings.savevalFindings,name='savevalFindings'),
        path('savevalFindingsComment/',val_findings.savevalFindingsComment,name='savevalFindingsComment'),
        path('upload_findings/',val_findings.upload_findings,name='upload_findings'),




]