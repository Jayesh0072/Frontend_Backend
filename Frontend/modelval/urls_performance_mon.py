from django.urls import path 

from . import performance_mon

urlpatterns = [
    #setup
    path('PerfMontrSetupMRM/',performance_mon.PerfMontrSetupMRM,name='PerfMontrSetupMRM'),
    path('savebusmetrics/',performance_mon.savebusmetrics,name='savebusmetrics'),
    path('addperfromancediscussion/',performance_mon.addperfromancediscussion,name='addperfromancediscussion'),
    path('savemodelmatrics/',performance_mon.savemodelmatrics,name='savemodelmatrics'),
    path('savebusinessmatrics/',performance_mon.savebusinessmatrics,name='savebusinessmatrics'),
    path('ApproveModelMatricsData/',performance_mon.ApproveModelMatricsData,name='ApproveModelMatricsData'),
    path('ApproveBusinessMatricsData/',performance_mon.ApproveBusinessMatricsData,name='ApproveBusinessMatricsData'),
    path('getMdlDataForMRM/',performance_mon.getMdlDataForMRM,name='getMdlDataForMRM'),
    path('getBusinessDataForMRM/',performance_mon.getBusinessDataForMRM,name='getBusinessDataForMRM'),
    path('datamatricsfeatureMRM/',performance_mon.datamatricsfeatureMRM,name='datamatricsfeatureMRM'),
    path('selectdataMetric/',performance_mon.selectdataMetric,name='selectdataMetric'),
    path('SaveTempFeatureMatricData/',performance_mon.SaveTempFeatureMatricData,name='SaveTempFeatureMatricData'),
    path('gethistorymsgdata/',performance_mon.gethistorymsgdata,name='gethistorymsgdata'),
    path('ApproveDataMatricsData/',performance_mon.ApproveDataMatricsData,name='ApproveDataMatricsData'),
    path('UpdateModelMatricsData/',performance_mon.UpdateModelMatricsData,name='UpdateModelMatricsData'),
    path('UpdatebusinessMatricsDatabus/',performance_mon.UpdatebusinessMatricsDatabus,name='UpdatebusinessMatricsDatabus'),
    path('gethistorymsgbus/',performance_mon.gethistorymsgbus,name='gethistorymsgbus'),
    path('datamatricsfeature/',performance_mon.datamatricsfeature,name='datamatricsfeature'),
    path('savedatamatrics/',performance_mon.savedatamatrics,name='savedatamatrics'),
    path('UpdateDataMatricsData/',performance_mon.UpdateDataMatricsData,name='UpdateDataMatricsData'),
    path('PerfMontrSetup/',performance_mon.PerfMontrSetup,name='PerfMontrSetup'),
    path('PerfMontr/',performance_mon.PerfMontr,name='PerfMontr'),
    path('SaveTempFeatureMatricData/',performance_mon.SaveTempFeatureMatricData,name='SaveTempFeatureMatricData'),
    path('PerfMontrDataFetch/',performance_mon.PerfMontrDataFetch,name='PerfMontrDataFetch'),
    path('PerfMontrDataFetchBuss/',performance_mon.PerfMontrDataFetchBuss,name='PerfMontrDataFetchBuss'),
    path('Save_Performance_Monitoring_Resolution/',performance_mon.Save_Performance_Monitoring_Resolution,name='Save_Performance_Monitoring_Resolution'),
    path('Save_Buss_KPI_Monitoring_Resolution/',performance_mon.Save_Buss_KPI_Monitoring_Resolution,name='Save_Buss_KPI_Monitoring_Resolution'),

    #upload data
    path('PerfMontrPrdnData/',performance_mon.PerfMontrPrdnData,name='PerfMontrPrdnData'),
    path('ModelMatricsData/',performance_mon.ModelMatricsData,name='ModelMatricsData'),
    path('mmlabeltoexcel/',performance_mon.mmlabeltoexcel,name='mmlabeltoexcel'),
    path('mmlabeltoexcelforbus/',performance_mon.mmlabeltoexcelforbus,name='mmlabeltoexcelforbus'),
    path('Perf_monitoring_file_upload/',performance_mon.Perf_monitoring_file_upload,name='Perf_monitoring_file_upload'),
    path('Perf_monitoring_file_upload_bus/',performance_mon.Perf_monitoring_file_upload_bus,name='Perf_monitoring_file_upload_bus'),
    path('gethistorymsg/',performance_mon.gethistorymsg,name='gethistorymsg'),
    path('home2/', performance_mon.home2, name="home2"),

    #Performance Monitoring
    path('PerfMontrMRM/',performance_mon.PerfMontrMRM,name='PerfMontrMRM'),
    path('PerfMontrDataFetch_MRMApprl/',performance_mon.PerfMontrDataFetch_MRMApprl,name='PerfMontrDataFetch_MRMApprl'),
    path('Update_Performance_Monitoring_Override_History/',performance_mon.Update_Performance_Monitoring_Override_History,name='Update_Performance_Monitoring_Override_History'),
    path('DataMontrOverHistory/',performance_mon.DataMontrOverHistory,name='DataMontrOverHistory'),
    path('Update_Data_Monitoring_Override_History/',performance_mon.Update_Data_Monitoring_Override_History,name='Update_Data_Monitoring_Override_History'),


]
