from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import * #Users,UserCategory,TaskRegistration,Task_Relevant_Personnel,TaskSummery,Alert,IssueRegistration,IssueRelevantPersonnel,IssueSummery,ModelOverview,Issue_Type_Master,Sub_Issue_Type_Master, TaskPriorityMaster, Department,TaskFunctionMaster,TaskTypeMaster,TaskApprovalstatusMaster,information,SubTasktypeMaster,DashboardContentMaster,UserDashboardContentMaster
from .serializers import * #UserSerializer, UserLoginSerializer, UserLogoutSerializer,UserCategorySerializer,TaskRegistrationSerializer,DepartmentSerializer,Task_Relevant_PersonnelSerializer,TaskSummerySerializer,AlertSerializer,IssueRegistrationSerializer,IssueRelevantPersonnelSerializer,IssueSummerySerializer,ModelOverviewSerializer,Issue_Type_MasterSerializer,Sub_Issue_Type_MasterSerializer,TaskPriorityMasterSerializer,TaskFunctionMasterSerializer,TaskTypeMasterSerializer,TaskApprovalstatusMasterSerializer,InformationSerializer,SubTasktypeMasterSerializer,DashboardContentMasterSerializer,UserDashboardContentMasterSerializer
from rest_framework.views import APIView
from rest_framework import generics, permissions, status,serializers
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .Adm_Utils.Masters import MasterTbls
import datetime
import traceback


objmaster=MasterTbls()
User=get_user_model()

class UsersgetAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        data = User.objects.all()
        serializer = UserSerializer(data,many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class UserCategoryAPI(APIView):
    def get(self,request,id=None):
        if id:
            usr = UserCategory.objects.get(u_aid=id)
            serializer = UserCategorySerializer(usr)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        usrmaster = UserCategory.objects.all()
        serializer =  UserCategorySerializer(usrmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        serializer = UserCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'User Category is created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    




# class AddUser(generics.ListCreateAPIView):
#     # get method handler
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class Login(generics.GenericAPIView):
#     # get method handler
   
    
    
#     permission_classes = [AllowAny]
#     queryset = User.objects.all()
#     serializer_class = UserLoginSerializer
    
#     def post(self, request, *args, **kwargs):
#         serializer_class = UserLoginSerializer(data=request.data)
#         if serializer_class.is_valid(raise_exception=True):            
#             return Response(serializer_class.data, status=HTTP_200_OK)
#         return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


# class Logout(generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserLogoutSerializer
#     permission_classes=[IsAuthenticated]
#     def post(self, request, *args, **kwargs):
#         print('request.data ',request.data)
#         serializer_class = UserLogoutSerializer(data=request.data)
#         if serializer_class.is_valid(raise_exception=True):
#             return Response(serializer_class.data, status=HTTP_200_OK)
#         return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)

class AddUser(generics.ListCreateAPIView):
    # get method handler
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class Login(generics.GenericAPIView):
    # get method handler
    
    permission_classes = [AllowAny]
    queryset = Users.objects.all()
    serializer_class = UserLoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer_class = UserLoginSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):            
            return Response(serializer_class.validated_data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class Logout(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Users.objects.all()  # You can also use [IsAuthenticated]
    queryset = Users.objects.all()
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)




def index(request):
    return redirect('/api/login')


class ConnectionMsgSave(APIView):

    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = PerformanceMonitoringDiscussionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Message Saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    objdbops =None

    def __init__(self):
        self.objdbops=dbops()

    def get(self,request):
        print("new request--------------------------------",request.data)
        strQ = "select upper(concat(left(u.U_FName,1),left(u.U_LName,1))) uinitials,FORMAT (getdate(),'hh:mm tt  MMM dd, yyyy') createdt from users u where u_aid='"+str(request.data['addedby'])+"'"
        tableResult=  self.objdbops.getTable(strQ) 
        if tableResult.empty == False:
            mdldata= tableResult.to_json(orient='index')
            del tableResult
            return Response({'data':json.loads(mdldata)}) 

class GetHistoryMsg(APIView):
    print() 
    objdbops =None

    def __init__(self):
        self.objdbops=dbops()

    def get(self,request):
        print("new request--------------------------------",request.data)
        # strQ = "SELECT  [perf_mon_AID],FORMAT (resp.[addedon],'hh:mm tt  MMM dd, yyyy') createdt ,[Comment],"
        # strQ+=" concat(u.U_FName,' ',u.U_LName) addedby,upper(concat(left(u.U_FName,1),left(u.U_LName,1))) uinitials,case when resp.addedBy=9 then 'S' else 'R' end msgcss"
        # strQ+=" from  [performance_monitoring_discussion] resp,users u"
        # strQ+=" where u.U_AID=resp.AddedBy   and room_id='Perfm_M070100' order by [perf_mon_AID]"
        try:
            strQ = "SELECT  [perf_mon_AID],FORMAT (resp.[addedon],'hh:mm tt  MMM dd, yyyy') createdt ,[Comment],"
            strQ+=" concat(u.U_FName,' ',u.U_LName) addedby,upper(concat(left(u.U_FName,1),left(u.U_LName,1))) uinitials,case when resp.addedBy="+str(request.data['addedby'])+" then 'S' else 'R' end msgcss"
            strQ+=" from  [performance_monitoring_discussion] resp,users u"
            strQ+=" where u.U_AID=resp.AddedBy   and room_id='"+request.data['room_id']+"' order by [perf_mon_AID]"
            print("strQ",strQ)
            tableResult=  self.objdbops.getTable(strQ) 
            
            # if tableResult.empty == False:
            mdldata= tableResult.to_json(orient='index')
            print("mdldata",mdldata)


            # mdl_overview = ModelOverview.objects.filter(mdl_id=request.data['mdl_id']).first()
            # print("mdl_overview----------------",mdl_overview)

            # matricsdeptdata = ModelMetricDept.objects.filter(dept_aid=mdl_overview.department,model_category = mdl_overview.category,model_sub_category = mdl_overview.sub_category)
            # category_data =  ModelMetricDeptSerializer(matricsdeptdata,many=True)
            # print("category_data-------------------------------",category_data.data)

            strQ1 = "select distinct mmm.MM_Label,mmm.mm_aid, Isnull(cast(perf.Threshold as varchar), '') AS Threshold,Isnull(cast(perf.Warning as varchar), '') AS Warning,Frequency,Metric_Value_Type from Model_Metric_Master mmm inner join  Model_Metric_Dept mmd on"
            strQ1+=" mmm.MM_AID=mmd.MM_AID inner join Mdl_OverView mdl on mmd.category_aid=mdl.category"
            strQ1+=" and mmd.sub_category_aid=mdl.sub_category"
            strQ1+=" left join Performance_Monitoring_Setup_temp perf  on perf.mdl_id=mdl.mdl_id"
            strQ1+="  and perf.Metric=mmd.MM_AID where  Mdl.department=mmd.dept_aid and mdl.Mdl_Id='"+request.data['mdl_id']+"'"
            # strQ1+="  and perf.Metric=mmd.MM_AID where  Mdl.department=mmd.dept_aid and mdl.Mdl_Id='M470100'"
            # strQ1+="and perf.Metric=mmd.MM_AID where mdl.Mdl_Id='"+request.data['mdl_id']+"'"
            # and Mdl.department=mmd.dept_aid 
            print("mdl overview query category-----------------------------------",strQ1)
            tableResult1=  self.objdbops.getTable(strQ1) 
            
            # if tableResult.empty == False:
            mdlcatdata= tableResult1.to_json(orient='records')
            # print("mdlcat data",mdlcatdata)


            strQ1 = "select mmm.BM_Label,mmm.bm_aid,Isnull(cast(perf.Threshold as varchar), '') AS Threshold,Isnull(cast(perf.Warning as varchar), '') AS Warning,Frequency from Business_Metric_Master mmm inner join  Business_Metric_Dept mmd on"
            strQ1+=" mmm.BM_AID=mmd.BM_AID inner join Mdl_OverView mdl  on mmd.category_aid=mdl.category"
            strQ1+=" and mmd.sub_category_aid=mdl.sub_category"
            strQ1+=" left join Buss_KPI_Monitoring_Setup_temp perf  on perf.mdl_id=mdl.mdl_id"
            # strQ1+=" and perf.Metric=mmd.BM_AID where mdl.Mdl_Id='"+request.data['mdl_id']+"' and Mdl.department=mmd.dept_aid order by  mdl.Mdl_Id"
            strQ1+=" and perf.Metric=mmd.BM_AID where mdl.Mdl_Id='M300100' and Mdl.department=mmd.dept_aid order by  mdl.Mdl_Id"
            # strQ1+="and perf.Metric=mmd.MM_AID where mdl.Mdl_Id='"+request.data['mdl_id']+"'"
            print("mdl overview query category buss-----------------------------------",strQ1)
            tableResult1=  self.objdbops.getTable(strQ1) 
            
            # if tableResult.empty == False:
            mdlcatdatabus= tableResult1.to_json(orient='records')
            print("mdlcat data buss",mdlcatdatabus)


            chartdata = PerformanceMonitoringSetup.objects.filter(mdl_id=request.data['mdl_id'])
            chartdata_serializer = PerformanceMonitoringSetupSerializer(chartdata,many=True)
            print("chartdata--------------",chartdata_serializer.data)

            modeldata = PerformanceMonitoringSetupTemp.objects.filter(mdl_id=request.data['mdl_id'])
            serializer = PerformanceMonitoringSetupTempSerializer(modeldata,many=True)

            modeldata = PerformanceMonitoringSetup.objects.filter(mdl_id=request.data['mdl_id'])
            serializer_a = PerformanceMonitoringSetupSerializer(modeldata,many=True)

            modeldata = BussKpiMonitoringSetupTemp.objects.filter(mdl_id=request.data['mdl_id'])
            serializer_b_temp = BussKpiMonitoringSetupTempSerializer(modeldata,many=True)
            print("business data",serializer_b_temp)

            modeldata_a = BussKpiMonitoringSetup.objects.filter(mdl_id=request.data['mdl_id'])
            serializer_b = BussKpiMonitoringSetupSerializer(modeldata_a,many=True)
            print("business data now",serializer_b.data)

            modeldata = DataMonitoringSetupTemp.objects.filter(mdl_id=request.data['mdl_id'])
            serializer_d_temp = DataMonitoringSetupTempSerializer(modeldata,many=True)
            print("data for data",serializer_d_temp)

            if DataMonitoringSetupTemp.objects.filter(mdl_id=request.data['mdl_id']).first() :
                print("if")
                model_data = serializer_d_temp.data
            else:
                print("else")
                modeldata = DataMonitoringSetup.objects.filter(mdl_id=request.data['mdl_id'])
                serializer_d = DataMonitoringSetupSerializer(modeldata,many=True)
                model_data = serializer_d.data

            print("model data check---------",model_data)

            # modeldata = DataMonitoringSetup.objects.filter(mdl_id=request.data['mdl_id'])
            # serializer_d = DataMonitoringSetupSerializer(modeldata,many=True)
            # # serialized_data_list = list(serializer_d)
            # print("data model",serializer_d.data)

            dataMntrHstry = DataMonitoringOverrideHistory.objects.filter(mdl_id = request.data['mdl_id'])
            dmh_serializer = DataMonitoringOverrideHistorySerializer(dataMntrHstry,many=True)
            print("dataMntrHstry",dmh_serializer.data)            
            
            return Response({'data':json.loads(mdldata),'chartdata':chartdata_serializer.data,'mmdata':serializer.data,'mmdata_a':serializer_a.data,'bmdata':serializer_b_temp.data,'bmdata_b':serializer_b.data,'dmdata':model_data,'dataMntrHstry':dmh_serializer.data,'mdl_category_data':json.loads(mdlcatdata),'mdlcatdatabus':json.loads(mdlcatdatabus)})
        except Exception as e:
            print("Excpet")
            print('adduser is ',e)
            print('adduser traceback is ', traceback.print_exc())


class GetHistoryMsgBuss(APIView): 
    objdbops =None
    def __init__(self):
        self.objdbops=dbops()
    def get(self,request): 
        strQ = "SELECT  [perf_mon_AID],FORMAT (resp.[addedon],'hh:mm tt  MMM dd, yyyy') createdt ,[Comment],"
        strQ+=" concat(u.U_FName,' ',u.U_LName) addedby,upper(concat(left(u.U_FName,1),left(u.U_LName,1))) uinitials,case when resp.addedBy="+str(request.data['addedby'])+" then 'S' else 'R' end msgcss"
        strQ+=" from  [performance_monitoring_discussion] resp,users u"
        strQ+=" where u.U_AID=resp.AddedBy   and room_id='"+request.data['room_id']+"' order by [perf_mon_AID]"
        
        tableResult=  self.objdbops.getTable(strQ)  
        mdldata= tableResult.to_json(orient='index')

        modeldata = BussKpiMonitoringSetup.objects.filter(mdl_id=request.data['mdl_id'])
        # modeldata = BussKpiMonitoringSetup.objects.all()
        serializer = BussKpiMonitoringSetupSerializer(modeldata,many=True) 
        # del tableResult
        return Response({'data':json.loads(mdldata),'bmdata':serializer.data})

# def check():
#     modeldata = BussKpiMonitoringSetup.objects.filter(mdl_id="M570100")
#     serializer_b = BussKpiMonitoringSetupSerializer(modeldata,many=True)
#     print("business data",serializer_b.data)
# check()

class Fetchmdlid(APIView):
    print()
    def get(self,request,id=None):
        print("request data new-----------------",request.data)
        if id:
            usr = ModelOverview.objects.get(u_aid=id)
            serializer = ModelOverviewSerializer(usr)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        usrmaster = ModelOverview.objects.filter(addedby=request.data['addedby'],is_submit=1).exclude(is_decommissioned=2)
        serializer =  ModelOverviewSerializer(usrmaster,many=True)
        print("serializer-------------------------------",serializer.data)
        freqmaster = FrequencyMaster.objects.all()
        freqerializer =  FrequencyMasterSerializer(freqmaster,many=True)

        mdl_overview = ModelOverview.objects.filter(department=request.data['dept_aid'])
        print("mdl_overview----------------",mdl_overview)

        matricsdeptdata = ModelMetricDept.objects.filter(dept_aid=request.data['dept_aid'])
        serializer_a =  ModelMetricDeptSerializer(matricsdeptdata,many=True)
        print("serializer_a-------------------------------",serializer_a.data)

        bmatricsdeptdata = BusinessMetricDept.objects.filter(dept_aid=request.data['dept_aid'])
        serializer_b =  BusinessMetricDeptSerializer(bmatricsdeptdata,many=True)
        print("serializer_b-------------------------------",serializer_b.data)
        # lst = []
        # for i in matricsdeptdata:
        #     matricsmaster = ModelMetricMaster.objects.filter(mm_aid = i.mm_aid)
        #     serializer_a =  ModelMetricMasterSerializer(matricsmaster,many=True)
        #     lst.append(serializer_a.data[0])
        return Response({'mdlids':serializer.data,'frequency':freqerializer.data,'mdlmetric':serializer_a.data,'bussmetric':serializer_b.data}, status=status.HTTP_200_OK)

class Freqmasterdata(APIView):
    def get(self,request,id=None):
        freqmaster = FrequencyMaster.objects.all()
        serializer =  FrequencyMasterSerializer(freqmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class FetchModelMatrics(APIView):
    print()
    def get(self,request):
        matricsdeptdata = ModelMetricDept.objects.filter(dept_aid=3)
        lst = []
        for i in matricsdeptdata:
            matricsmaster = ModelMetricMaster.objects.filter(mm_aid = i.mm_aid)
            serializer =  ModelMetricMasterSerializer(matricsmaster,many=True)
            print("data check-------------",serializer.data[0])
            lst.append(serializer.data[0])
        print(lst)
        return Response(lst, status=status.HTTP_200_OK)


         
class getutypeselection(APIView):
    objdbops =None

    def __init__(self):
        self.objdbops=dbops()

    def get(self,request):
        print("new request--------------------------------",request.GET)
        strQ = "select * from users where dept_aid=3 and uc_aid in (select sublvl.uc_aid from  User_Category uclvl ,User_Category sublvl where uclvl.uc_level>=sublvl.uc_level and uclvl.uc_aid=10)"
        dtusers=  self.objdbops.getTable(strQ) 
        dtusers= dtusers.to_json(orient='records')
        return Response(json.loads(dtusers))


class TaskRegistrationAPI(APIView):

    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = TaskRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'data is created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    



# class DepartmentAPI(APIView):
#     permission_classes=[IsAuthenticated]
#     def post(self,request):
#         serializer = DepartmentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'data':serializer.data,'msg':'Department is created Successufully'},status=status.HTTP_201_CREATED)
#         return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    



class Task_Relevant_PersonnelAPI(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request):
        taskrelevant = Task_Relevant_Personnel.objects.all()
        serializer = Task_Relevant_PersonnelSerializer(taskrelevant,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = Task_Relevant_PersonnelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Task_Relevant_Personnel is created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    



class TaskSummeryAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        tasksummery = TaskSummery.objects.all()
        serializer = TaskSummerySerializer(tasksummery,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = TaskSummerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Task Summery is created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
class AlertAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        alerts = Alert.objects.all()
        serializer = AlertSerializer(alerts,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        data = request.data
        serializer = AlertSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Alert is created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)    

class IssueRegistrationAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        issueregistration = IssueRegistration.objects.all()
        serializer = IssueRegistrationSerializer(issueregistration,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = IssueRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Issue Registration created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    


class IssueRelevantPersonnelAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        issuerelevantpersonnel = IssueRelevantPersonnel.objects.all()
        serializer =  IssueRelevantPersonnelSerializer(issuerelevantpersonnel,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = IssueRelevantPersonnelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Issue RelevantPersonnel created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    

class IssueSummeryAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        issuesummery = IssueSummery.objects.all()
        serializer =  IssueSummerySerializer(issuesummery,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = IssueSummerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Issue Summery created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    

    


class ModelOverviewAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        modeloverview =  ModelOverview.objects.all()
        serializer =  ModelOverviewSerializer(modeloverview,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = ModelOverviewSerializer(data=request.data)
        if serializer.is_valid():   
            serializer.save()
            return Response({'data':serializer.data,'msg':'ModelOverview created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    

    

class Issue_Type_MasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        issuetypemaster =  Issue_Type_Master.objects.all()
        serializer =  Issue_Type_MasterSerializer(issuetypemaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = Issue_Type_MasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Issue_Type_Master created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)



class Sub_Issue_Type_MasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        subissuetypemaster =  Sub_Issue_Type_Master.objects.all()
        serializer =  Sub_Issue_Type_MasterSerializer(subissuetypemaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = Sub_Issue_Type_MasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Sub_Issue_Type_Master created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    




class TaskPriorityMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        taskprioritymaster = TaskPriorityMaster.objects.all()
        serializer =  TaskPriorityMasterSerializer(taskprioritymaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = TaskPriorityMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'TaskPriorityMaster created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
    
 
    

    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = TaskFunctionMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'TaskFunctionMaster created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
    


class TaskTypeMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        tasktypemaster = TaskTypeMaster.objects.all()
        serializer =  TaskTypeMasterSerializer(tasktypemaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = TaskTypeMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'TaskTypeMaster created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
    

 


class InformationAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        info = information.objects.all()
        serializer = InformationSerializer(info,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = InformationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Information created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
    


class SubTasktypeMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        subtasktypemaster = SubTasktypeMaster.objects.all()
        serializer = SubTasktypeMasterSerializer(subtasktypemaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = SubTasktypeMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'SubTasktypeMaster created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
    




class DashboardContentMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        dashboardcontentmaster = DashboardContentMaster.objects.all()
        serializer = DashboardContentMasterSerializer(dashboardcontentmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = DashboardContentMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'DashboardContentMaster created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
    

class UserDashboardContentMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        userdashboardcontentmaster = UserDashboardContentMaster.objects.all()
        serializer = UserDashboardContentMasterSerializer(userdashboardcontentmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = UserDashboardContentMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'UserDashboardContentMaster created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
    

class IssuePriorityMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            print("id",id)
            issuepriority = IssuePriorityMaster.objects.get(issue_priority_aid=id)
            serializer = IssuePriorityMasterSerializer(issuepriority)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        issueprioritymaster = IssuePriorityMaster.objects.all()
        serializer =  IssuePriorityMasterSerializer(issueprioritymaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = IssuePriorityMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Issue Priority created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
    

    permission_classes=[IsAuthenticated]
    def put(self,request):
        print("data",request.data)
        try:
            id=request.data['id']
            print("id",id)
            obj = IssuePriorityMaster.objects.get(issue_priority_aid=id)
        except IssuePriorityMaster.DoesNotExist:
            return Response({'msg':'Issue Priority does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = IssuePriorityMasterSerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Issue Priority Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class IssueFunctionMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            print("id",id)
            issuefunctionmaster = IssueFunctionMaster.objects.get(issue_function_aid=id)
            serializer = IssueFunctionMasterSerializer(issuefunctionmaster)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        issuefunctionmaster = IssueFunctionMaster.objects.all()
        serializer =  IssueFunctionMasterSerializer(issuefunctionmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = IssueFunctionMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'IssueFunctionMaster created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)


    permission_classes=[IsAuthenticated]
    def put(self,request):
        print("data",request.data)
        try:
            id=request.data['id']
            print("id",id)
            obj = IssueFunctionMaster.objects.get(issue_function_aid=id)
        except IssueFunctionMaster.DoesNotExist:
            return Response({'msg':'IssueFunctionMaster does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = IssueFunctionMasterSerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Issue Function Master Updated Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
    

class IssueApprovalstatusMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            print("id",id)
            issueapproval = IssueApprovalstatusMaster.objects.get(issue_approvalstatus_aid=id)
            serializer = IssueApprovalstatusMasterSerializer(issueapproval)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        issueapprovalstatusmaster = IssueApprovalstatusMaster.objects.all()
        serializer =  IssueApprovalstatusMasterSerializer(issueapprovalstatusmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = IssueApprovalstatusMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Issue Approval status created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)

    permission_classes=[IsAuthenticated]
    def put(self,request):
        print("data",request.data)
        try:
            id=request.data['id']
            print("id",id)
            obj = IssueApprovalstatusMaster.objects.get(issue_approvalstatus_aid=id)
        except IssueApprovalstatusMaster.DoesNotExist:
            return Response({'msg':'Issue Approval does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = IssueApprovalstatusMasterSerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Issue Approval Status Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST) 

class Issue_Type_MasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            print("id",id)
            issuetypemaster = Issue_Type_Master.objects.get(issue_type_aid=id)
            serializer = Issue_Type_MasterSerializer(issuetypemaster)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        issuetypemaster =  Issue_Type_Master.objects.all()
        serializer =  Issue_Type_MasterSerializer(issuetypemaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = Issue_Type_MasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Issue_Type created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

    permission_classes=[IsAuthenticated]
    def put(self,request):
        print("data",request.data)
        try:
            id=request.data['id']
            print("id",id)
            obj = Issue_Type_Master.objects.get(issue_type_aid=id)
        except Issue_Type_Master.DoesNotExist:
            return Response({'msg':'Issue Type_Master does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = Issue_Type_MasterSerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Issue_Type Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)


class Sub_Issue_Type_MasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            print("id",id)
            sub_issuetypemaster = Sub_Issue_Type_Master.objects.get(sub_issue_type_aid=id)
            serializer = Sub_Issue_Type_MasterSerializer(sub_issuetypemaster)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        subissuetypemaster =  Sub_Issue_Type_Master.objects.all()
        serializer =  Sub_Issue_Type_MasterSerializer(subissuetypemaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = Sub_Issue_Type_MasterSerializer(data=request.data)
        print("request",request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Sub Issue Type created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            print("request1",request.data)
            id=request.data['sub_issue_type_aid']
            print("sub_issue_type_aid",id)
            issue_type=request.data['issue_type_aid']
            print("issue_type",issue_type)

            smp = Sub_Issue_Type_Master.objects.get(sub_issue_type_aid=id)
            print("request2",request.data)
        except Sub_Issue_Type_Master.DoesNotExist:
            return Response({'msg':'Sub_Issue_Type_Master does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = Sub_Issue_Type_MasterSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Sub Issue Type is Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    


class UpdateUser(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            usr = Users.objects.get(u_aid=id)
            serializer = UserSerializer(usr)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        usrmaster = Users.objects.all()
        serializer =  UserSerializer(usrmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = Users.objects.get(u_aid=id)

        except Users.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'User is Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
class BackupForUserData(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        backup_user = Users.objects.filter(is_active = 1,U_AID_BackUpFor__isnull = True)
        serializer =  UserSerializer(backup_user,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

#-----------ajit added -------#


class IntrinsicMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        intrinsicmaster =  IntrinsicMaster.objects.all()
        serializer =  IntrinsicMasterSerializer(intrinsicmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = IntrinsicMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'IntrinsicMaster created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    


class RelianceMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        reliancemaster =  RelianceMaster.objects.all()
        serializer =  RelianceMasterSerializer(reliancemaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = RelianceMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'RelianceMaster created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    

class MaterialityMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        materialitymaster =  MaterialityMaster.objects.all()
        serializer =  MaterialityMasterSerializer(materialitymaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = MaterialityMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'MaterialityMaster created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    


class HistoryRegisterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        materialitymaster =  HistoryRegisterModel.objects.all()
        serializer = HistoryRegisterSerializer(materialitymaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = HistoryRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'HistoryRegisterModel created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    

class ModelFunctionMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        modelfunctionmaster = ModelFunctionMaster.objects.all()
        serializer = ModelFunctionMasterSerializer(modelfunctionmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = ModelFunctionMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'ModelFunctionMaster created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    



class ModelSourceMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        modelsourcemaster = ModelSourceMaster.objects.all()
        serializer = ModelSourceMasterSerializer(modelsourcemaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = ModelSourceMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'ModelSourceMaster created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    


class ModelTypeMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        modelsourcemaster = ModelTypeMaster.objects.all()
        serializer = ModelTypeMasterSerializer(modelsourcemaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = ModelTypeMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'ModelTypeMaster created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    



class PrdAddrMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        prdaddrmaster = PrdAddrMaster.objects.all()
        serializer = PrdAddrMasterSerializer(prdaddrmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = PrdAddrMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'PrdAddrMaster created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    


class MdlDependenciesAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        mdldependencies = MdlDependencies.objects.all()
        serializer = MdlDependenciesSerializer(mdldependencies,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = MdlDependenciesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'MdlDependencies created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    


class MdlUpstreamAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        mdlupstream = MdlUpstream.objects.all()
        serializer = MdlUpstreamSerializer(mdlupstream,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = MdlUpstreamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'MdlUpstream created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    


class MdlDwstreamAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        mdldwstream = MdlDwstream.objects.all()
        serializer = MdlDwstreamSerializer(mdldwstream,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = MdlDwstreamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'MdlDwstream created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    

class ThreadAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        thread = Thread.objects.all()
        serializer = ThreadSerializer(thread,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = ThreadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Thread created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    



class ChatmessageAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        chatmessage = Chatmessage.objects.all()
        serializer = ChatmessageSerializer(chatmessage,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = ChatmessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Chatmessage created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    


class NotificationDetailsAPI(APIView):
    # permission_classes=[IsAuthenticated]
    def get(self,request):
        notificationdetails = NotificationDetails.objects.all()
        serializer = NotificationDetailsSerializer(notificationdetails,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = NotificationDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'NotificationDetails created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    


class IcqQuestionMasterAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        icqquestionmaster = IcqQuestionMaster.objects.all()
        serializer = IcqQuestionMasterSerializer(icqquestionmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = IcqQuestionMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'IcqQuestionMaster created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    

class IcqSectionsAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        icqsections = IcqSections.objects.all()
        serializer = IcqSectionsSerializer(icqsections,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = IcqSectionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'IcqSections created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    

class IcqSubSectionsAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        icqsubsections = IcqSubSections.objects.all()
        serializer = IcqSubSectionsSerializer(icqsubsections,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = IcqSubSectionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'IcqSubSections created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    


class IcqSubSubSectionsAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        icqsubsubsections = IcqSubSubSections.objects.all()
        serializer = IcqSubSubSectionsSerializer(icqsubsubsections,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = IcqSubSubSectionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'IcqSubSubSections created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    


class IcqSubSubSubSectionsAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        icqsubsubsubsections = IcqSubSubSubSections.objects.all()
        serializer = IcqSubSubSubSectionsSerializer(icqsubsubsubsections,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = IcqSubSubSubSectionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'IcqSubSubSubSections created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class MdlRelevantPersonnelAPI(APIView): 
    permission_classes= [IsAuthenticated]   
    def get(self,request,id=None):
        if id:
            print('id is ',id)
            objmdl=MdlOverview.objects.get(mdl_id=id)
            # objusers=Users.objects.filter(dept_aid=objmdl.department)
            objusers=Users.objects.all()
            userser=UserSerializer(objusers,many=True)
            if VrSubmissionAllocation.objects.filter(mdl_id=id):
                print()
                vrsuballoc = VrSubmissionAllocation.objects.filter(mdl_id=id)
                serializer = VrSubmissionAllocationSerializer(vrsuballoc,many = True)
                val_data = ''
            else:
                usr = MdlRelevantPersonnel.objects.filter(mdl_id=id,u_type='Owner') 
                serializer = MdlRelevantPersonnelSerializer(usr,many=True)
                validator = ValidationAssignto.objects.filter(mdl_id=id)
                val_ser = ValidationAssigntoSerializer(validator,many=True)
                val_data = val_ser.data
            return Response({"status": "success", "owner": serializer.data,"users":userser.data,'validator':val_data}, status=status.HTTP_200_OK)

        # usrmaster = MdlRelevantPersonnel.objects.all()
        # serializer =  MdlRelevantPersonnelSerializer(usrmaster,many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
    
class VrSubmissionAllocationAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            allocation = VrSubmissionAllocation.objects.filter(mdl_id=id)
            serializer = VrSubmissionAllocationSerializer(allocation,many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        allocation = VrSubmissionAllocation.objects.all()
        serializer = VrSubmissionAllocationSerializer(allocation,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request data-------------------",request.data)
        if request.data['enddate'] == 'undefined':
            request.data['enddate'] = None
        else:
            request.data['enddate'] = request.data['enddate']
        obj = VrSubmissionAllocation.objects.filter(mdl_id = request.data['mdl_id'],u_aid = request.data['u_aid'])
        if obj:
            return Response({'msg':'VrSubmissionAllocation already Exist'},status=status.HTTP_201_CREATED)
        else:
            obj = VrSubmissionAllocation(mdl_id = request.data['mdl_id'],u_aid = request.data['u_aid'],enddate = request.data['enddate'],addedby  = request.data['addedby'])
            obj.save()
            return Response({'msg':'VrSubmissionAllocation created Successufully'},status=status.HTTP_201_CREATED)
            # serializer = VrSubmissionAllocationSerializer(data=request.data)
            # print("serializer",serializer)
            # if serializer.is_valid():
            #     serializer.save()
            #     return Response({'data':serializer.data,'msg':'VrSubmissionAllocation created Successufully'},status=status.HTTP_201_CREATED)
            # return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     if VrSubmissionAllocation.objects.get(mdl_id = request.data['mdl_id'],u_aid = request.data['u_aid']):
        #         # a = VrSubmissionAllocation.objects.filter(mdl_id = request.data['mdl_id']).update(u_aid = request.data['u_aid'],addedby = request.data['addedby'],enddate = enddate)
        #         return Response({'msg':'VrSubmissionAllocation already Exist'},status=status.HTTP_201_CREATED)            
        # except Exception as e:
        #     print("error is",e)
        #     serializer = VrSubmissionAllocationSerializer(data=request.data)
        #     print("serializer",serializer)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response({'data':serializer.data,'msg':'VrSubmissionAllocation created Successufully'},status=status.HTTP_201_CREATED)
        #     return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = VrSubmissionAllocation.objects.get(mdl_id=id)

        except VrSubmissionAllocation.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'VrSubmissionAllocation does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = VrSubmissionAllocationSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'VrSubmissionAllocation is Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    

import json
class checkutypeowner(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        vrsuballocobj = VrSubmissionAllocation.objects.all()
        owner = []
        for i in vrsuballocobj:
            # print(i.mdl_id)
            try:
                mdlrelobj = MdlRelevantPersonnel.objects.filter(mdl_id = i.mdl_id,u_type = 'Owner').first()
                print(mdlrelobj)
                owner.append(mdlrelobj.mdl_id)
            except Exception as e:
                print("error",e)
                owner.append("")
        print(owner)
        result = [x for x in owner if x != ""]
        print(result)
        return Response({'data':result})

from app1.DAL.dboperations import dbops
class getutypeselection(APIView):
    objdbops =None

    def __init__(self):
        self.objdbops=dbops()

    def get(self,request):
        print("new request--------------------------------",request.GET)
        strQ = "select * from users where dept_aid=3 and uc_aid in (select sublvl.uc_aid from  User_Category uclvl ,User_Category sublvl where uclvl.uc_level>=sublvl.uc_level and uclvl.uc_aid=10)"
        dtusers=  self.objdbops.getTable(strQ) 
        dtusers= dtusers.to_json(orient='records')
        return Response(json.loads(dtusers))

class validationReviewFrequency(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            allocation = ValidationReviewFrequency.objects.filter(frequency_aid=id)
            serializer = ValidationReviewFrequencySerializer(allocation,many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        allocation = ValidationReviewFrequency.objects.all()
        serializer = ValidationReviewFrequencySerializer(allocation,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request data-------------------",request.data)
        serializer = ValidationReviewFrequencySerializer(data=request.data)
        print("serializer",serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Frequency created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        print("data",request.data)
        try:
            id=request.data['id']
            print("id",id)
            obj = ValidationReviewFrequency.objects.get(frequency_aid=id)
        except ValidationReviewFrequency.DoesNotExist:
            return Response({'msg':'Frequency does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ValidationReviewFrequencySerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Frequency Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

# class VrSubmissionAllocationAPI(APIView): 
#     permission_classes= [IsAuthenticated]   
#     def get(self,request,id=None):
#         if id:
#             print('id is ',id)
#             objmdl=VrSubmissionAllocation.objects.get(mdl_id=id)
#             # objusers=Users.objects.filter(dept_aid=objmdl.department)
#             objusers=Users.objects.all()
#             userser=UserSerializer(objusers,many=True)
#             usr = MdlRelevantPersonnel.objects.filter(mdl_id=id,u_type='Owner') 
#             serializer = MdlRelevantPersonnelSerializer(usr,many=True)
#             validator = ValidationAssignto.objects.filter(mdl_id=id)
#             val_ser = ValidationAssigntoSerializer(validator,many=True)
#             return Response({"status": "success", "owner": serializer.data,"users":userser.data,'validator':val_ser.data}, status=status.HTTP_200_OK)

class ModelMatricsAPI(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("model matric request",request.data)
        try:
            obj = PerformanceMonitoringSetupTemp.objects.filter(mdl_id = request.data['mdl_id'],metric = request.data['metric'])
            if obj:
                obj.update(threshold = request.data['threshold'],warning = request.data['warning'],frequency = request.data['frequency'])
                return Response({'msg':'Model Matrics is updated Successufully'},status=status.HTTP_201_CREATED)
            else:
                serializer = PerformanceMonitoringSetupTempSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'data':serializer.data,'msg':'Model Matrics is saved Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
                print("what is error",e)
                return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
class BusinessMetricAPI(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        obj = BussKpiMonitoringSetupTemp.objects.filter(mdl_id = request.data['mdl_id'],metric = request.data['metric'])
        if obj:
            obj.update(threshold = request.data['threshold'],warning = request.data['warning'],frequency = request.data['frequency'])
            return Response({'msg':'Business Matrics is updated Successufully'},status=status.HTTP_201_CREATED)
        else:
            serializer = BussKpiMonitoringSetupTempSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'msg':'Business Matrics is saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class DataMetricAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        Datasetuptemp = DataMonitoringSetupTemp.objects.all()
        serializer = DataMonitoringSetupTempSerializer(Datasetuptemp,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request data for data",request.data)
        if DataMonitoringSetupTemp.objects.filter(mdl_id = request.data['mdl_id'],metric = request.data['Metric'],feature = request.data['feature']):
            print("inside if")
            datamontrsetuptmp = DataMonitoringSetupTemp.objects.filter(mdl_id = request.data['mdl_id'],metric = request.data['metric'],feature = request.data['feature']).update(mo_approval = 1,frequency = request.data['frequency'],threshold = request.data['threshold'],warning = request.data['warning'])
            return Response({'data':datamontrsetuptmp,'msg':'Data Matrics is Updated Successufully'},status=status.HTTP_201_CREATED)
        else:
            serializer = DataMonitoringSetupTempSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                datametric=DataMetricMaster.objects.get(data_aid=request.data['Metric'])
                mrmheadId=objmaster.getMRMHead()

                notification_trigger= "Model  "+ request.data['mdl_id'] +" Data Matric Saved "+datametric.data_label
                objmaster.insert_notification(str(request.data['added_by']),mrmheadId," Data Matric Saved",notification_trigger,1)
                print("-------------------------Not TRig")
                trail_obj = ActivityTrail(refference_id  = request.data['mdl_id'],activity_trigger = " Data Matric Saved",activity_details = "Model Data Matric Saved "+datametric.data_label,addedby=request.data['added_by'],added_on=datetime.datetime.now(),)
                trail_obj.save()
                print("-------------------------Activity Trail")
                return Response({'data':serializer.data,'msg':'Data Matrics is saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)


class AddBusinessMetricAPI(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = BusinessMetricMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Business Matrics is saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class AddBusinessMetricsDept(APIView):
    def post(self,request):
        serializer = BusinessMetricDeptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Business Metrics saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class ModelMatricsTempData(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        modeldata = PerformanceMonitoringSetupTemp.objects.filter(mdl_id=request.data['mdl_id'])
        serializer = PerformanceMonitoringSetupTempSerializer(modeldata,many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            print("-------------chk1")
            modeldata = PerformanceMonitoringSetupTemp.objects.filter(mdl_id=request.data['mdl_id']).update(mo_approval = 1)
            tempdata = PerformanceMonitoringSetupTemp.objects.filter(mdl_id=request.data['mdl_id'])
            print("setup_temp data",tempdata)
            del_obj = PerformanceMonitoringSetup.objects.filter(mdl_id=request.data['mdl_id']).delete()
            for i in tempdata:
                print("i---------",i)
                obj = PerformanceMonitoringSetup(mdl_id = i.mdl_id , metric = i.metric , metric_value_type = i.metric_value_type , threshold = i.threshold , warning = i.warning ,frequency = i.frequency ,added_by = i.added_by )
                obj.save()
            return Response({'data':modeldata,'msg':'Model Matrics Updated Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class DataMatricsTempData(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        modeldata = DataMonitoringSetupTemp.objects.filter(mdl_id=request.data['mdl_id'])
        serializer = DataMonitoringSetupTempSerializer(modeldata,many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            print("request data--------------------1",request.data)
            modeldata = DataMonitoringSetupTemp.objects.filter(mdl_id=request.data['mdl_id']).update(mo_approval = 1)

            tempdata = DataMonitoringSetupTemp.objects.filter(mdl_id=request.data['mdl_id'])
            print("setup_temp data",tempdata)
            del_obj = DataMonitoringSetup.objects.filter(mdl_id=request.data['mdl_id']).delete()
            for i in tempdata:
                print("i---------",i)
                obj = DataMonitoringSetup(mdl_id = i.mdl_id , metric = i.metric , threshold = i.threshold , warning = i.warning ,frequency = i.frequency ,added_by = i.added_by )
                obj.save()   

            return Response({'data':modeldata,'msg':'Data Matrics Updated Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            print("error is",e)
            return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
        
        
class BusinessMatricsTempData(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        modeldata = BussKpiMonitoringSetupTemp.objects.filter(mdl_id=request.data['mdl_id'])
        serializer = BussKpiMonitoringSetupTempSerializer(modeldata,many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            modeldata = BussKpiMonitoringSetupTemp.objects.filter(mdl_id=request.data['mdl_id']).update(mo_approval = 1)

            tempdata = BussKpiMonitoringSetupTemp.objects.filter(mdl_id=request.data['mdl_id'])
            print("setup_temp data",tempdata)
            del_obj = BussKpiMonitoringSetup.objects.filter(mdl_id=request.data['mdl_id']).delete()
            for i in tempdata:
                print("i---------",i)
                obj = BussKpiMonitoringSetup(mdl_id = i.mdl_id , metric = i.metric ,metric_value_type = i.metric_value_type , threshold = i.threshold , warning = i.warning ,frequency = i.frequency ,added_by = i.added_by )
                obj.save()  
            return Response({'data':modeldata,'msg':'Business Matrics Updated Successufully'},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)



from functools import reduce
def unique(list1):
    # Print directly by using * symbol
    ans = reduce(lambda re, x: re+[x] if x not in re else re, list1, [])
    print("unique ans",ans)
    return ans

class FetchPerfMonMdlId(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        print("request_data",request.data)
        mdlmatricdept = ModelMetricDept.objects.filter(dept_aid =request.data['dept_aid'])        
        lst = [i.mm_aid.mm_aid for i in mdlmatricdept ]
        print("lst chk",lst)
        groups = PerformanceMonitoringSetup.objects.filter(metric__in=lst) 
        lst1 = [x.mdl_id for x in groups]
        mdlid_data = unique(lst1)

        busmatricdept = BusinessMetricDept.objects.filter(dept_aid =request.data['dept_aid'])
        lst_b = [i.bm_aid.bm_aid for i in busmatricdept ]
        businessdata = BussKpiMonitoringSetup.objects.filter(metric__in=lst_b)  
        lstbuss = [x.mdl_id for x in businessdata]
        mdlid_buss_data = unique(lstbuss)
        print('mdlid_buss_data ',mdlid_buss_data)
        return Response({"status": "success", "data": mdlid_data,"buss_data":mdlid_buss_data}, status=status.HTTP_200_OK)
    

class Fetchmmlabel(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        mdlmatricmaster = ModelMetricMaster.objects.filter(mm_aid = request.data['metric'])
        serializer = ModelMetricMasterSerializer(mdlmatricmaster,many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    
class perfMonitoringFileInfoAPI(APIView):

    permission_classes=[IsAuthenticated]
    def get(self,request):
        print("request data file",request.data)
        mdlmatricmaster = PerformanceMonitoringResultFileInfo.objects.filter(mdl_id = request.data['mdl_id']).latest('added_on')
        print("latest",mdlmatricmaster)
        serializer = PerformanceMonitoringResultFileInfoSerializer(mdlmatricmaster)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = PerformanceMonitoringResultFileInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'file Info is saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

# class AddModelMetrics(APIView):
#     permission_classes=[IsAuthenticated]
#     def get(self,request):
#         mdlmatricmaster = ModelMetricMaster.objects.all()
#         print("mdlmatricmaster",mdlmatricmaster)
#         # serializer = ModelMetricMasterSerializer(mdlmatricmaster,many=True)
#         # print("mmm serializer",mdlmatricmaster)
#         lst=[]
#         for i in mdlmatricmaster:
#             dict = {}
#             dict['mm_aid'] = i.mm_aid
#             dict['mm_label'] = i.mm_label
#             dict['mm_descri ption'] = i.mm_description
#             lst_a = []
#             mdldept = ModelMetricDept.objects.filter(mm_aid = i.mm_aid)
#             # dict['departments'] = mdldept.dept_details.dept_label
#             print("mdldept-------------------",mdldept.values())
#             for j in mdldept:
#                 print("mdldept",j.dept_aid)
#                 lst_a.append(j.dept_aid.dept_label)
#             result = ', '.join(map(str, lst_a))
#             dict['departments'] = result
#             # serializer_a = ModelMetricDeptSerializer(mdldept,many=True)
#             # print("mmd serializer",serializer_a.data)
#             lst.append(dict)
#         print("list----------------",lst)
        
#         return Response({"status": "success", "data": lst}, status=status.HTTP_200_OK)

#     def post(self,request):
#         serializer = ModelMetricMasterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'data':serializer.data,'msg':'Model Metrics saved Successufully'},status=status.HTTP_201_CREATED)
#         return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
#     permission_classes=[IsAuthenticated]
#     def put(self,request):
#         try:
#             id=request.data['id']
#             smp = ModelMetricMaster.objects.get(frequency_aid=id)

#         except ModelMetricMaster.DoesNotExist:
#             # msg = {'msg':'Department does not exist'}
#             return Response({'msg':'Model Metric Master does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
#         print("request.data",request.data)
#         serializer = ModelMetricMasterSerializer(smp,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'data':serializer.data,'msg':'Model Metric Master Data Updated Successufully'},status=status.HTTP_201_CREATED)
#         return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)


# class editmodelmetrics(APIView):
#     permission_classes=[IsAuthenticated]
#     def get(self,request,id=None):
#         if id:
#             mmmaster = ModelMetricMaster.objects.get(mm_aid=id)
#             serializer = ModelMetricMasterSerializer(mmmaster)
#             dict = {}
#             dict['mm_aid'] = mmmaster.mm_aid
#             dict['mm_label'] = mmmaster.mm_label
#             dict['mm_description'] = mmmaster.mm_description
#             lst_a = []
#             mdldept = ModelMetricDept.objects.filter(mm_aid = mmmaster.mm_aid)
#             # dict['departments'] = mdldept.dept_details.dept_label
#             for j in mdldept:
#                 print("mdldept",j.dept_aid.dept_label)
#                 lst_a.append(j.dept_aid.dept_label)
#             result = ', '.join(map(str, lst_a))
#             dict['departments'] = result
#             dict['departments_list'] = lst_a
#             # mdlmatricmaster = ModelMetricMaster.objects.all()
#         # serializer = ModelMetricMasterSerializer(mdlmatricmaster,many=True)
#         # print("mmm serializer",mdlmatricmaster)
            
#             return Response({"status": "success", "data": dict}, status=status.HTTP_200_OK)

#         modelmetricnmaster = ModelMetricMaster.objects.all()
#         serializer =  ModelMetricMasterSerializer(modelmetricnmaster,many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)



# # def check():
# #     mdlmatricmaster = ModelMetricMaster.objects.all()
# #     serializer = ModelMetricMasterSerializer(mdlmatricmaster,many=True)
# #     print("mmm serializer",mdlmatricmaster)
# #     lst=[]
# #     for i in mdlmatricmaster:
# #         dict = {}
# #         dict['mm_aid'] = i.mm_aid
# #         dict['mm_label'] = i.mm_label
# #         dict['mm_description'] = i.mm_description
# #         lst_a = []
# #         mdldept = ModelMetricDept.objects.filter(mm_aid = i.mm_aid)
# #         # dict['departments'] = mdldept.dept_details.dept_label
# #         for j in mdldept:
# #             print("mdldept",j.dept_aid.dept_label)
# #             lst_a.append(j.dept_aid.dept_label)
# #         dict['departments'] = lst_a
# #         serializer_a = ModelMetricDeptSerializer(mdldept,many=True)
# #         # print("mmd serializer",serializer_a.data)
# #         lst.append(dict)
# #     print("list----------------",lst)
# # check()

# class AddModelMetricsDept(APIView):
#     def post(self,request):
#         serializer = ModelMetricDeptSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'data':serializer.data,'msg':'Model Metrics saved Successufully'},status=status.HTTP_201_CREATED)
#         return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
# # Master code 0612

# class savemodelmetrics(APIView): 
#     permission_classes=[IsAuthenticated]
#     def post(self,request):
#         print("request data",request.data)
#         serializer = ModelMetricMasterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'data':serializer.data,'msg':'Metric is created Successufully'},status=status.HTTP_201_CREATED)
#         return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
#     permission_classes=[IsAuthenticated]
#     def put(self,request):
#         try:
#             id=request.data['id']
#             smp = ModelMetricMaster.objects.get(mm_aid=id)

#         except ModelMetricMaster.DoesNotExist:
#             # msg = {'msg':'Department does not exist'}
#             return Response({'msg':'Model Metric Master does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
#         print("request.data",request.data)
#         serializer = ModelMetricMasterSerializer(smp,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'data':serializer.data,'msg':'Model Metric  Data Updated Successufully'},status=status.HTTP_201_CREATED)
#         return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

  

# class savemodeldepartment(APIView): 
#     permission_classes=[IsAuthenticated]
#     def post(self,request):
#         print("request data",request.data)
#         serializer = ModelMetricDeptSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'data':serializer.data,'msg':'Metric_Department is created Successufully'},status=status.HTTP_201_CREATED)
#         return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
#     permission_classes=[IsAuthenticated]
#     def put(self,request):
#         try:
#             id=request.data['id']
#             smp = ModelMetricDept.objects.get(mm_aid=id)

#         except ModelMetricDept.DoesNotExist:
#             # msg = {'msg':'Department does not exist'}
#             return Response({'msg':'Model Metric Master does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
#         print("request.data",request.data)
#         serializer = ModelMetricDeptSerializer(smp,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'data':serializer.data,'msg':'Metric_Department is Updated Successufully'},status=status.HTTP_201_CREATED)
#         return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

# class checkMetricDept(APIView):
#     permission_classes=[IsAuthenticated]
#     def get(self,request):
#         print("Metric dept check",request.data)
#         mdlmatricmaster = ModelMetricDept.objects.filter(mm_aid = request.data['mm_aid'],dept_aid = request.data['dept_aid'])
#         serializer = ModelMetricDeptSerializer(mdlmatricmaster,many=True)
#         return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    

class frequecy_master(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            freq = FrequencyMaster.objects.get(frequency_aid=id)
            serializer = FrequencyMasterSerializer(freq)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        frequencyfunctionmaster = FrequencyMaster.objects.all()
        serializer =  FrequencyMasterSerializer(frequencyfunctionmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request data",request.data)
        serializer = FrequencyMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Frequency Master Data created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = FrequencyMaster.objects.get(frequency_aid=id)

        except FrequencyMaster.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Frequency Master Function does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        print("request.data",request.data)
        serializer = FrequencyMasterSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Frequency Master Data Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

#######

class Fetchmdlid_MRM(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None): 
        if id:
            usr = ModelOverview.objects.get(u_aid=id)
            serializer = ModelOverviewSerializer(usr)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        usrmaster = ModelOverview.objects.all()
        mdlid_serializer =  ModelOverviewSerializer(usrmaster,many=True)
        print("mdl id serializer-------------------------------",mdlid_serializer.data)

        modeldata = PerformanceMonitoringSetupTemp.objects.order_by().values('mdl_id').distinct() 
        serializer = PerformanceMonitoringSetupTempSerializer(modeldata,many=True)
        print("serializer.data-------------------- ",serializer.data)
        freqmaster = FrequencyMaster.objects.all()
        freqerializer =  FrequencyMasterSerializer(freqmaster,many=True)

        matricsdeptdata = ModelMetricDept.objects.filter(dept_aid=request.data['dept_aid'])
        serializer_a =  ModelMetricDeptSerializer(matricsdeptdata,many=True)

        businessdata = BussKpiMonitoringSetupTemp.objects.order_by().values('mdl_id').distinct() 
        serializer_b = BussKpiMonitoringSetupTempSerializer(businessdata,many=True)
        print("serializer_b.data ",serializer_b.data)

        # Datasetuptemp = DataMonitoringSetupTemp.objects.all()
        # serializer_data = DataMonitoringSetupTempSerializer(Datasetuptemp,many=True)

        unique_values_data = DataMonitoringSetupTemp.objects.values('mdl_id').distinct()
        
        
        return Response({'mdlids':mdlid_serializer.data, 'data_mdlids': unique_values_data,'frequency':freqerializer.data,'mdlmetric':serializer_a.data,'businessmetric':serializer_b.data}, status=status.HTTP_200_OK)

class getMdlIdforPerfMontr(APIView): 
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None): 
        if id:
            usr = ModelOverview.objects.get(u_aid=id)
            serializer = ModelOverviewSerializer(usr)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        modeldata = PerformanceMonitoringSetup.objects.order_by().values('mdl_id').distinct() 
        serializer = PerformanceMonitoringSetupSerializer(modeldata,many=True)
        
        freqmaster = FrequencyMaster.objects.all()
        freqerializer =  FrequencyMasterSerializer(freqmaster,many=True)

        matricsdeptdata = ModelMetricDept.objects.filter(dept_aid=request.data['dept_aid'])
        serializer_a =  ModelMetricDeptSerializer(matricsdeptdata,many=True)

        businessdata = BussKpiMonitoringSetup.objects.order_by().values('mdl_id').distinct() 
        serializer_b = BussKpiMonitoringSetupSerializer(businessdata,many=True)
        
        return Response({'mdlids':serializer.data, 'frequency':freqerializer.data,'mdlmetric':serializer_a.data,'bussmetric':serializer_b.data}, status=status.HTTP_200_OK)



class getMdlDataForMRM(APIView):
    permission_classes=[IsAuthenticated]
    objdbops =None
    def __init__(self):
        self.objdbops=dbops()
    def get(self,request):
        strQ="SELECT   isnull(Metric,master_dt.mm_aid) metric,mm_label ,metric_value_type,threshold,warning ,frequency FROM \
            Performance_Monitoring_Setup_temp setup_temp right join \
            (select mmm.*,mdl_id from Model_Metric_Master mmm,Model_Metric_Dept mmd,Mdl_OverView mdl \
            where mmm.mm_aid=mmd.mm_aid and mmd.dept_aid=mdl.department and mdl_id='"+ request.data['mdl_id'] +"'  ) master_dt \
            on master_dt.mm_aid=setup_temp.Metric \
            and  setup_temp.mdl_id='"+ request.data['mdl_id'] +"'"

        tableResult=  self.objdbops.getTable(strQ)  
        mdldata= tableResult.to_json(orient='index')   

        strQ = "SELECT  [perf_mon_AID],FORMAT (resp.[addedon],'hh:mm tt  MMM dd, yyyy') createdt ,[Comment],"
        strQ+=" concat(u.U_FName,' ',u.U_LName) addedby,upper(concat(left(u.U_FName,1),left(u.U_LName,1))) uinitials,case when resp.addedBy="+str(request.data['addedby'])+" then 'S' else 'R' end msgcss"
        strQ+=" from  [performance_monitoring_discussion] resp,users u"
        strQ+=" where u.U_AID=resp.AddedBy   and room_id='"+request.data['room_id']+"' order by [perf_mon_AID]"
        
        tableResult=  self.objdbops.getTable(strQ)  
        chathistory= tableResult.to_json(orient='index')
        mo_approved=self.objdbops.getscalar("select count(*) from  Performance_Monitoring_Setup_temp where MO_approval=1 and mdl_id='"+request.data['mdl_id']+"'")

        strQ1 = "select mmm.MM_Label,mmm.mm_aid,Isnull(cast(perf.Threshold as varchar), '') AS Threshold,Isnull(cast(perf.Warning as varchar), '') AS Warning,MO_Approval,Frequency from Model_Metric_Master mmm inner join  Model_Metric_Dept mmd on"
        strQ1+=" mmm.MM_AID=mmd.MM_AID inner join Mdl_OverView mdl  on mmd.category_aid=mdl.category"
        strQ1+=" and mmd.sub_category_aid=mdl.sub_category"
        strQ1+=" left join Performance_Monitoring_Setup_temp perf  on perf.mdl_id=mdl.mdl_id"
        strQ1+=" and perf.Metric=mmd.MM_AID where mdl.Mdl_Id='"+request.data['mdl_id']+"' and Mdl.department=mmd.dept_aid order by  mdl.Mdl_Id"
        # strQ1+="and perf.Metric=mmd.MM_AID where mdl.Mdl_Id='"+request.data['mdl_id']+"'"
        print("mdl overview query category-----------------------------------",strQ1)
        tableResult1=  self.objdbops.getTable(strQ1) 
        
        # if tableResult.empty == False:
        mdlcatdata= tableResult1.to_json(orient='records')
        print("mdlcat data",mdlcatdata)


        return Response({'mmdata':json.loads(mdldata),'data':json.loads(chathistory),'mo_approved':mo_approved,'mdlcatdata':json.loads(mdlcatdata)})
    
class getBusinessDataForMRM(APIView):
    permission_classes=[IsAuthenticated]
    objdbops =None
    def __init__(self):
        self.objdbops=dbops()
    def get(self,request):
        strQ="SELECT   isnull(Metric,master_dt.bm_aid) metric,bm_label ,metric_value_type,threshold,warning ,frequency FROM \
            Buss_KPI_Monitoring_Setup_temp setup_temp right join \
            (select mmm.*,mdl_id from Business_Metric_Master mmm,Business_Metric_Dept mmd,Mdl_OverView mdl \
            where mmm.bm_aid=mmd.bm_aid and mmd.dept_aid=mdl.department and mdl_id='"+ request.data['mdl_id'] +"'  ) master_dt \
            on master_dt.bm_aid=setup_temp.Metric \
            and  setup_temp.mdl_id='"+ request.data['mdl_id'] +"'"
        print('query-------------------',strQ)
        tableResult=  self.objdbops.getTable(strQ)  
        businessdata= tableResult.to_json(orient='index')   
        strQ = "SELECT  [perf_mon_AID],FORMAT (resp.[addedon],'hh:mm tt  MMM dd, yyyy') createdt ,[Comment],"
        strQ+=" concat(u.U_FName,' ',u.U_LName) addedby,upper(concat(left(u.U_FName,1),left(u.U_LName,1))) uinitials,case when resp.addedBy="+str(request.data['addedby'])+" then 'S' else 'R' end msgcss"
        strQ+=" from  [performance_monitoring_discussion] resp,users u"
        strQ+=" where u.U_AID=resp.AddedBy   and room_id='"+request.data['room_id']+"'  order by [perf_mon_AID]"
        
        tableResult=  self.objdbops.getTable(strQ)  
        chathistory= tableResult.to_json(orient='index')
        mo_approved=self.objdbops.getscalar("select count(*) from  Buss_KPI_Monitoring_Setup_temp where MO_approval=1 and mdl_id='"+request.data['mdl_id']+"'")


        strQ1 = "select mmm.BM_Label,mmm.bm_aid,Isnull(cast(perf.Threshold as varchar), '') AS Threshold,Isnull(cast(perf.Warning as varchar), '') AS Warning,Frequency from Business_Metric_Master mmm inner join  Business_Metric_Dept mmd on"
        strQ1+=" mmm.BM_AID=mmd.BM_AID inner join Mdl_OverView mdl  on mmd.category_aid=mdl.category"
        strQ1+=" and mmd.sub_category_aid=mdl.sub_category"
        strQ1+=" left join Buss_KPI_Monitoring_Setup_temp perf  on perf.mdl_id=mdl.mdl_id"
        strQ1+=" and perf.Metric=mmd.BM_AID where mdl.Mdl_Id='"+request.data['mdl_id']+"' and Mdl.department=mmd.dept_aid order by  mdl.Mdl_Id"
        # strQ1+="and perf.Metric=mmd.MM_AID where mdl.Mdl_Id='"+request.data['mdl_id']+"'"
        print("mdl overview query category buss-----------------------------------",strQ1)
        tableResult1=  self.objdbops.getTable(strQ1) 
        
        # if tableResult.empty == False:
        mdlcatdatabus= tableResult1.to_json(orient='records')
        print("mdlcat data buss",mdlcatdatabus)

        return Response({'bmdata':json.loads(businessdata),'data':json.loads(chathistory),'mo_approved':mo_approved,'mdlcatdatabus':json.loads(mdlcatdatabus)})
    
# class getDataForMRM(APIView):
#     permission_classes=[IsAuthenticated]
#     objdbops =None
#     def __init__(self):
#         self.objdbops=dbops()
#     def get(self,request):
#         strQ="SELECT  isnull(Metric,master_dt.data_aid) metric,data_label ,metric_value_type,threshold,warning ,frequency FROM \
#             Data_Monitoring_Setup_temp setup_temp right join \
#             (select mmm.*,mdl_id from Data_Metric_Master mmm,Business_Metric_Dept mmd,Mdl_OverView mdl \
#             where mmm.bm_aid=mmd.bm_aid and mmd.dept_aid=mdl.department and mdl_id='"+ request.data['mdl_id'] +"'  ) master_dt \
#             on master_dt.bm_aid=setup_temp.Metric \
#             and  setup_temp.mdl_id='"+ request.data['mdl_id'] +"'"
#         print('query-------------------',strQ)
#         tableResult=  self.objdbops.getTable(strQ)  
#         businessdata= tableResult.to_json(orient='index')   
#         strQ = "SELECT  [perf_mon_AID],FORMAT (resp.[addedon],'hh:mm tt  MMM dd, yyyy') createdt ,[Comment],"
#         strQ+=" concat(u.U_FName,' ',u.U_LName) addedby,upper(concat(left(u.U_FName,1),left(u.U_LName,1))) uinitials,case when resp.addedBy="+str(request.data['addedby'])+" then 'S' else 'R' end msgcss"
#         strQ+=" from  [performance_monitoring_discussion] resp,users u"
#         strQ+=" where u.U_AID=resp.AddedBy   and room_id='"+request.data['room_id']+"' order by [perf_mon_AID]"
        
#         tableResult=  self.objdbops.getTable(strQ)  
#         chathistory= tableResult.to_json(orient='index')
#         mo_approved=self.objdbops.getscalar("select count(*) from  Buss_KPI_Monitoring_Setup_temp where MO_approval=1 and mdl_id='"+request.data['mdl_id']+"'")
#         return Response({'bmdata':json.loads(businessdata),'data':json.loads(chathistory),'mo_approved':mo_approved})
    
    
class ApproveModelMatricsData(APIView):
    objdbops =None
    def __init__(self):
        self.objdbops=dbops()
    permission_classes=[IsAuthenticated]  
    def post(self,request):
        try:
            # modeldata = PerformanceMonitoringSetupTemp.objects.filter(mdl_id=request.data['mdl_id']).update(mrm_approval = 1,mrm_approval_on=datetime.now())
            strQ="insert into Performance_Monitoring_Setup ([Mdl_Id] \
                ,[Metric]\
                ,[Metric_Value_Type]\
                ,[Threshold]\
                ,[Warning]\
                ,[Frequency] \
               , [MO_Approval] \
                ,[MO_Approval_On]  \
                ,[MRM_Approval] \
                ,[MRM_Approval_On] \
                ,[Added_by]\
                ,[Added_On] )\
                SELECT [Mdl_Id] \
                ,[Metric]\
                ,[Metric_Value_Type]\
                ,[Threshold]\
                ,[Warning]\
                ,[Frequency] \
                ,[MO_Approval] \
                ,[MO_Approval_On]  \
                ,[MRM_Approval] \
                ,[MRM_Approval_On] \
                ,[Added_by]\
                ,getdate() \
                FROM [Performance_Monitoring_Setup_temp] where mdl_id='"+request.data['mdl_id']+"'"
            self.objdbops.insertRow(strQ)
            print("----------11",strQ)
            self.objdbops.insertRow("delete from Performance_Monitoring_Setup_temp where mdl_id='"+request.data['mdl_id']+"'")
            return Response({'msg':'Model matrics approved.'},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
class ApproveBusinessMatricsData(APIView):
    objdbops =None
    def __init__(self):
        self.objdbops=dbops()
    permission_classes=[IsAuthenticated]  
    def post(self,request):
        try:
            modeldata = BussKpiMonitoringSetupTemp.objects.filter(mdl_id=request.data['mdl_id']).update(mrm_approval = 1,mrm_approval_on=datetime.datetime.now())
            # print("modeldata",modeldata)
            strQ="insert into Buss_KPI_Monitoring_Setup ([Mdl_Id] \
                ,[Metric]\
                ,[Metric_Value_Type]\
                ,[Threshold]\
                ,[Warning]\
                ,[Frequency] \
               , [MO_Approval] \
                ,[MO_Approval_On]  \
                ,[MRM_Approval] \
                ,[MRM_Approval_On] \
                ,[Added_by]\
                ,[Added_On] )\
                SELECT [Mdl_Id] \
                ,[Metric] \
                ,[Feature]\
                ,[Threshold]\
                ,[Warning]\
                ,[Frequency] \
                ,[MO_Approval] \
                ,[MO_Approval_On]  \
                ,[MRM_Approval] \
                ,[MRM_Approval_On] \
                ,[Added_by]\
                ,getdate() \
                FROM [Buss_KPI_Monitoring_Setup_temp] where mdl_id='"+request.data['mdl_id']+"'"
            self.objdbops.insertRow(strQ)
            print("----------11",strQ)
            self.objdbops.insertRow("delete from Buss_KPI_Monitoring_Setup_temp where mdl_id='"+request.data['mdl_id']+"'")
            return Response({'msg':'Business matrics approved.'},status=status.HTTP_201_CREATED)
        except Exception as e:
            print("busskpi error",e,traceback.print_exc())
            return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
        
class ApproveDataMatricsData(APIView):
    objdbops =None
    def __init__(self):
        self.objdbops=dbops()
    permission_classes=[IsAuthenticated]  
    def post(self,request):
        try:
            
            modeldata = DataMonitoringSetupTemp.objects.filter(mdl_id=request.data['mdl_id']).update(mrm_approval = 1,mrm_approval_on=datetime.datetime.now())
            # print("modeldata",modeldata)
            strQ="insert into Data_Monitoring_Setup ([Mdl_Id] \
                ,[Feature]\
                ,[Metric]\
                ,[Threshold]\
                ,[Warning]\
                ,[Frequency] \
               , [MO_Approval] \
                ,[MO_Approval_On]  \
                ,[MRM_Approval] \
                ,[MRM_Approval_On] \
                ,[Added_by]\
                ,[Added_On] )\
                SELECT [Mdl_Id] \
                ,[Metric]\
                ,[Metric_Value_Type]\
                ,[Threshold]\
                ,[Warning]\
                ,[Frequency] \
                ,[MO_Approval] \
                ,[MO_Approval_On]  \
                ,[MRM_Approval] \
                ,[MRM_Approval_On] \
                ,[Added_by]\
                ,getdate() \
                FROM [Data_Monitoring_Setup_temp] where mdl_id='"+request.data['mdl_id']+"'"
            self.objdbops.insertRow(strQ)
            print("----------11",strQ)
            self.objdbops.insertRow("delete from Data_Monitoring_Setup_temp where mdl_id='"+request.data['mdl_id']+"'")

            # datametric=DataMetricMaster.objects.get(data_aid=request.data['Metric'])
            mrmheadId=objmaster.getMRMHead()

            notification_trigger= "Model  "+ request.data['mdl_id'] +" Data Matric Signed Off"
            objmaster.insert_notification(str(request.data['Added_by']),mrmheadId,"Data Matric Signed Off",notification_trigger,1)
            print("-------------------------Not TRig")
            trail_obj = ActivityTrail(refference_id  = request.data['mdl_id'],activity_trigger = "Data Matric Signed Off",activity_details = "Model Data Matric Signed Off ",addedby=request.data['Added_by'],added_on=datetime.datetime.now(),)
            trail_obj.save()
            print("-------------------------Activity Trail")

            return Response({'msg':'Data matrics approved.'},status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Data Montr error",e,traceback.print_exc())
            return Response({'data':e,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
        
        
class DataMatricsData(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        data = DataMetricMaster.objects.all()
        serializer = DataMetricMasterSerializer(data,many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class SaveTempFeatureMatricSelection(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        data = TempFeatureMatricSelection.objects.filter(feature = request.data['feature'],datamatrics = request.data['datamatrics'])
        serializer = TempFeatureMatricSelectionSerializer(data,many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request data",request.data)
        serializer = TempFeatureMatricSelectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Feature Data created Successfully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)

    permission_classes=[IsAuthenticated]
    def delete(self, request):
        try:
            instance = TempFeatureMatricSelection.objects.filter(mdl_id=request.data['mdl_id'])
        except TempFeatureMatricSelection.DoesNotExist:
            return Response({'error': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response({'success': 'Object deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class SelectdataMetrics(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        values_to_filter1 = ['String','All']
        values_to_filter2 = ['Numeric','All']
        if request.data['type'] == 'object':
            # data = DataMetricMaster.objects.filter(data_types = 'String',data_types = 'All')
            data = DataMetricMaster.objects.filter(Q(data_types__in=values_to_filter1))
            serializer = DataMetricMasterSerializer(data,many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            # data = DataMetricMaster.objects.filter(data_types = 'Numeric',data_types = 'All')
            data = DataMetricMaster.objects.filter(Q(data_types__in=values_to_filter2))
            serializer = DataMetricMasterSerializer(data,many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

import pandas as pd    
class calculatedatamatrics(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        queryset = TempFeatureMatricSelection.objects.all()
        data = list(queryset.values())
        df = pd.DataFrame.from_records(data)
        print("df",df)
        datamatric_cnt = df[(df['datamatrics'] == 'Null') & (df['feature'] == 'Accuracy')]
        print("datamatric_cnt",len(datamatric_cnt)/100*100)
        # serializer = TempFeatureMatricSelectionSerializer(data,many=True)
        return Response({"status": "success", "datamatric_cnt": len(datamatric_cnt)/100*100}, status=status.HTTP_200_OK)
    

class DataMonitoringFileInfoAPI(APIView):

    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = DataMonitoringResultFileInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # datametric=DataMetricMaster.objects.get(data_aid=request.data['Metric'])
            mrmheadId=objmaster.getMRMHead()

            notification_trigger= "Model  "+ request.data['Mdl_ID'] +" Data Matric Imported File info "
            objmaster.insert_notification(str(request.data['Added_by']),mrmheadId," Data Matric Imported File info",notification_trigger,1)
            print("-------------------------Not TRig")
            trail_obj = ActivityTrail(refference_id  = request.data['Mdl_ID'],activity_trigger = "Data Matric Imported File info",activity_details = "Data Matric Imported File info ",addedby=request.data['Added_by'],added_on=datetime.datetime.now())
            trail_obj.save()
            print("-------------------------Activity Trail")
            return Response({'data':serializer.data,'msg':'file Info is saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)


#### issue code #########
def error_saving(request,data):
    print("data print",data)
    file = open('logs.txt', 'w')
    file.write(str(data))
    file.close()
    print("file save")


class ValFindingConnectionMsgSave(APIView):

    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = ValFindingsDiscussionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Message Saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    objdbops =None

    def __init__(self):
        self.objdbops=dbops()

    def get(self,request):
        print("new request--------------------------------",request.data)
        strQ = "select upper(concat(left(u.U_FName,1),left(u.U_LName,1))) uinitials,FORMAT (getdate(),'hh:mm tt  MMM dd, yyyy') createdt from users u where u_aid='"+str(request.data['addedby'])+"'"
        tableResult=  self.objdbops.getTable(strQ) 
        if tableResult.empty == False:
            mdldata= tableResult.to_json(orient='index')
            del tableResult
            return Response({'data':json.loads(mdldata)}) 


class GetValFindHistoryMsg(APIView):
    print() 
    objdbops =None

    def __init__(self):
        self.objdbops=dbops()

    def get(self,request):
        print("new request--------------------------------",request.data)
        # strQ = "SELECT  [perf_mon_AID],FORMAT (resp.[addedon],'hh:mm tt  MMM dd, yyyy') createdt ,[Comment],"
        # strQ+=" concat(u.U_FName,' ',u.U_LName) addedby,upper(concat(left(u.U_FName,1),left(u.U_LName,1))) uinitials,case when resp.addedBy=9 then 'S' else 'R' end msgcss"
        # strQ+=" from  [performance_monitoring_discussion] resp,users u"
        # strQ+=" where u.U_AID=resp.AddedBy   and room_id='Perfm_M070100' order by [perf_mon_AID]"
        try:
            strQ = "SELECT  [val_find_AID],FORMAT (resp.[addedon],'hh:mm tt  MMM dd, yyyy') createdt ,[Comment],"
            strQ+=" concat(u.U_FName,' ',u.U_LName) addedby,upper(concat(left(u.U_FName,1),left(u.U_LName,1))) uinitials,case when resp.addedBy="+str(request.data['addedby'])+" then 'S' else 'R' end msgcss"
            strQ+=" from  [val_findings_discussion] resp,users u"
            strQ+=" where u.U_AID=resp.AddedBy   and room_id='"+request.data['room_id']+"' and findings_id='"+request.data['findings_id']+"' order by [val_find_AID]"
            print(strQ)
            tableResult=  self.objdbops.getTable(strQ) 
            
            # if tableResult.empty == False:
            mdldata= tableResult.to_json(orient='index')
            print("mdldata",mdldata)

            modeldata = PerformanceMonitoringSetupTemp.objects.filter(mdl_id=request.data['mdl_id'])
            serializer = PerformanceMonitoringSetupTempSerializer(modeldata,many=True)

            # modeldata = PerformanceMonitoringSetup.objects.filter(mdl_id=request.data['mdl_id'])
            # serializer_a = PerformanceMonitoringSetupSerializer(modeldata,many=True)

            # modeldata = BussKpiMonitoringSetupTemp.objects.filter(mdl_id=request.data['mdl_id'])
            # serializer_b_temp = BussKpiMonitoringSetupTempSerializer(modeldata,many=True)
            # print("business data",serializer_b_temp)

            # modeldata = BussKpiMonitoringSetup.objects.filter(mdl_id=request.data['mdl_id'])
            # serializer_b = BussKpiMonitoringSetupSerializer(modeldata,many=True)
            # print("business data",serializer_b)

            # modeldata = DataMonitoringSetupTemp.objects.filter(mdl_id=request.data['mdl_id'])
            # serializer_d_temp = DataMonitoringSetupTempSerializer(modeldata,many=True)
            # print("data for data",serializer_d_temp)

            # modeldata = DataMonitoringSetup.objects.filter(mdl_id=request.data['mdl_id'])
            # serializer_d = DataMonitoringSetupSerializer(modeldata,many=True)
            # # serialized_data_list = list(serializer_d)
            # print("data model",serializer_d.data)

            # dataMntrHstry = DataMonitoringOverrideHistory.objects.filter(mdl_id = request.data['mdl_id'])
            # dmh_serializer = DataMonitoringOverrideHistorySerializer(dataMntrHstry,many=True)
            # print("dataMntrHstry",dmh_serializer.data)

            #  `` modeldata = BussKpiMonitoringSetup.objects.filter(mdl_id=request.data['mdl_id'])
    #     # modeldata = BussKpiMonitoringSetup.objects.all()
    #     serializer = BussKpiMonitoringSetupSerializer(modeldata,many=True)
            
            # del tableResult
            return Response({'data':json.loads(mdldata),'mmdata':serializer.data})
        except Exception as e:
            print("Excpet")
            print('adduser is ',e)
            print('adduser traceback is ', traceback.print_exc())


class Get_Title_Label(APIView):
    def get(self,request,id=None):
        request_data = request.data
        print("request_data",request_data)
        obj = ReportTitleTemplate.objects.filter(template_name = request.data['header_name']).order_by('title_id')
        serializer =  ReportTitleTemplateSerializer(obj,many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class FL_Get_Title_Label(APIView):
    def get(self,request,id=None):
        request_data = request.data
        print("request_data",request_data)
        obj = FlReportTitleTemplate.objects.filter(template_name = request.data['header_name']).order_by('title_id')
        serializer =  FlReportTitleTemplateSerializer(obj,many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class get_template_name(APIView):
    def get(self,request,id=None):
        obj = ReportTitleTemplate.objects.values('template_name').distinct()
        print("------------",obj)
        # serializer =  ReportTitleTemplateSerializer(obj,many=True)
        # print(serializer.data)
        lst = [i['template_name'] for i in obj]
        return Response({'data':lst}, status=status.HTTP_200_OK)

class FL_get_template_name(APIView):
    def get(self,request,id=None):
        obj = FlReportTitleTemplate.objects.values('template_name').distinct()
        print("------------",obj)
        # serializer =  ReportTitleTemplateSerializer(obj,many=True)
        # print(serializer.data)
        lst = [i['template_name'] for i in obj]
        return Response({'data':lst}, status=status.HTTP_200_OK)


class RPT_Template_Header_API(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data",request.data)
        serializer = ReportTemplateHeaderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Report Template Header Saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class FL_RPT_Template_Header_API(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data",request.data)
        serializer = FLReportTemplateHeaderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Report Template Header Saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)


class Fetch_Header_Details(APIView):
    def get(self,request,id=None):
        # template_name = 'new one temp'
        header_obj = ReportTemplateHeader.objects.filter(report_template_name = request.data['template_name']).first()
        header_name = header_obj.header_template_name
        print("header_name",header_name)
        header_data_obj = ReportTitleTemplate.objects.filter(template_name = header_name).order_by('title_id')
        serializer =  ReportTitleTemplateSerializer(header_data_obj,many=True)
        print("data 45-------------",serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class FL_Fetch_Header_Details(APIView):
#     def get(self,request,id=None):
#         # template_name = 'new one temp'
#         header_obj = FlReportTemplateHeader.objects.filter(fl_report_template_name = request.data['template_name']).first()
#         header_name = header_obj.header_template_name
#         print("header_name",header_name)
#         header_data_obj = FlReportTitleTemplate.objects.filter(template_name = header_name).order_by('title_id')
#         serializer =  FlReportTitleTemplateSerializer(header_data_obj,many=True)
#         print("data",serializer.data)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class ReportHeaderTitleContentAPI(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data",request.data)
        if request.data['type'] == 'update':
            print("request_data------------------------------------------------------s",request.data)    
            obj = ReportHeaderTitleContent.objects.filter(template_name=request.data['template_name'],mdl_id = request.data['mdl_id'],title_id = request.data['title_id']).update(comment=request.data['comment'])
            return Response({'msg':'Report Header Title Content Updated Successufully'},status=status.HTTP_201_CREATED)
        else:
            pass
        obj = ReportHeaderTitleContent.objects.filter(template_name=request.data['template_name'],title_id = request.data['title_id'],mdl_id = request.data['mdl_id']).first()
        if obj:
            return Response({'msg':'Data Already Exist'},status=status.HTTP_201_CREATED)
        else:
            serializer = ReportHeaderTitleContentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'msg':'Report Header Title Content Saved Successufully'},status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
class FLReportHeaderTitleContentAPI(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data",request.data)
        if request.data['type'] == 'update':
            print("request_data------------------------------------------------------s",request.data)    
            obj = FlReportHeaderTitleContent.objects.filter(template_name=request.data['template_name'],mdl_id = request.data['mdl_id'],title_id = request.data['title_id']).update(comment=request.data['comment'])
            return Response({'msg':'FL Report Header Title Content Updated Successufully'},status=status.HTTP_201_CREATED)
        else:
            pass
        obj = FlReportHeaderTitleContent.objects.filter(template_name=request.data['template_name'],title_id = request.data['title_id'],mdl_id = request.data['mdl_id']).first()
        if obj:
            return Response({'msg':'Data Already Exist'},status=status.HTTP_201_CREATED)
        else:
            serializer = FlReportHeaderTitleContentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'msg':'FL Report Header Title Content Saved Successufully'},status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    

class Fl_sectionsAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        data = FlSections.objects.all()
        serializer = FLSectionsSerializer(data,many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class FLAllocationAPI(APIView):
    def get(self,request,id=None):
        if id:
            usr = FlAllocation.objects.get(u_aid=id)
            serializer = FlallocationSerializer(usr)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        usrmaster = FlAllocation.objects.all()
        serializer =  FlallocationSerializer(usrmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        serializer = FlallocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'FL question Allocation is saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class save_flallocation(APIView):
    def post(self,request):  
        try:  
            print("request data-----------",request.data)   
            section_aid = request.data['section_aid']
            users = request.data['users']
            # end_date = request_data['end_date'][6:] + "-" + request_data['end_date'][3:5] + "-" + request_data['end_date'][:2]
            if request.data['rv_id'] == "addnew":
                print("if")
                last_rvid_obj = FlAllocation.objects.aggregate(max('review_id'))
                last_rvid = last_rvid_obj['review_id__max']
                splt_rvid = last_rvid.split('_')
                latest_rvid = int(splt_rvid[1]).__add__(1) #used magic method django
                for user, section_id in [(x,y) for x in users for y in section_aid]:
                    allocate_obj = FlAllocation(review_id ="Rv_"+str(latest_rvid),review_name = request.data['rv_name'],section_aid = section_id,allocated_to = user,end_date = None)
                    allocate_obj.save()
                return Response( {"isvalid":"true"}, status=status.HTTP_200_OK) 
            else:
                print("else")
                for user, section_id in [(x,y) for x in users for y in section_aid]:
                    allocate_obj = FlAllocation(review_id =request.data['rv_id'],review_name = request.data['rv_name'],section_aid = section_id,allocated_to = user,end_date = None)
                    allocate_obj.save() 
                return Response( {"isvalid":"true"}, status=status.HTTP_200_OK)
        except Exception as e: 
            print("error is",e)
            error_saving(request,e)
            return Response({'msg':'Error while processing request.'+ str(e)}, status=HTTP_400_BAD_REQUEST)

class GetRiskFactorHistoryMsg(APIView):
    print() 
    objdbops =None

    def __init__(self):
        self.objdbops=dbops()

    def get(self,request):
        print("new request--------------------------------",request.data)
        try:
            strQ = "SELECT  [Risk_Factor_Discussion_AID],FORMAT (resp.[Added_on],'hh:mm tt  MMM dd, yyyy') createdt ,[Comments],"
            strQ+=" concat(u.U_FName,' ',u.U_LName) Added_by,upper(concat(left(u.U_FName,1),left(u.U_LName,1))) uinitials,case when resp.Added_by="+str(request.data['addedby'])+" then 'S' else 'R' end msgcss"
            strQ+=" from  [Risk_Factor_Discussion] resp,users u"
            strQ+=" where u.U_AID=resp.Added_by and Group_Id='"+request.data['group_id']+"' and Risk_ID='"+request.data['risk_id']+"' order by [Risk_Factor_Discussion_AID]"
            print(strQ)
            tableResult=  self.objdbops.getTable(strQ) 
            
            # if tableResult.empty == False:
            data= tableResult.to_json(orient='index')
            print("data message-------------",data)

            data_a = RiskFactorComments.objects.get(risk_id=request.data['risk_id'])
            serializer = RiskFactorCommentsSerializer(data_a)
            print("comment data--------------",serializer.data)
            return Response({'data':json.loads(data),'comment':serializer.data})
        except Exception as e:
            print("Excpet")
            print('adduser is ',e)
            print('adduser traceback is ', traceback.print_exc())

    def post(self,request):
        serializer = RiskFactorDiscussionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response({'data':serializer.data,'msg':'Discussion Comments is saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)


class GetRiskFactorComment(APIView):
    
    def get(self,request):
        print("Comment mod")
        print("new request comment--------------------------------",request.data)
        data = RiskFactorComments.objects.get(risk_id=request.data['risk_id'])
        serializer = RiskFactorCommentsSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FL_ReportContentAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        allocation_obj = FlReportTemplateTemp.objects.all().values_list('template_name',flat=True).distinct()       
        temp_name = [i for i in allocation_obj]
        print("FL temp_name-------------",temp_name)
        # for i in allocation_obj:
        #     print("i",i)
        #     temp_name.append(i)
        rptcontentobj = FlReportContent.objects.values('template_name')
        serializer =  FL_ReportContentSerializer(rptcontentobj,many=True)
        return Response(temp_name, status=status.HTTP_200_OK)

    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("req data",request.data)
        obj = FlReportContent.objects.filter(fl_report_template_aid = request.data['report_template_aid'],template_name = request.data['template_name']).first()
        print("obj",obj)
        if obj:
            item = FlReportContent.objects.filter(fl_report_template_aid = request.data['report_template_aid'],template_name = request.data['template_name']).first()
            data = FL_ReportContentSerializer(instance=item, data=request.data)        
            if data.is_valid():
                data.save()
                return Response({'data':data.data,'msg':'Report Content Updated Successfully'},status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = FL_ReportContentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'msg':'Report Content Saved Successfully'},status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors,'msg':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)

class FL_Fetch_Report_data(APIView):
    print("FL_Fetch_Report_data")
    permission_classes=[IsAuthenticated]
    objdbops =None

    def __init__(self):
        self.objdbops=dbops()

    def get(self,request):
        print()
        strQ ="select isnull(Comment,'-') comment,case when  [Rpt_Sub_sub_section_text] is not null then [Rpt_Sub_sub_section_text]"
        strQ+="else case when  [Rpt_Sub_section_text] is not null then [Rpt_Sub_section_text]"
        strQ+="else case when  rpt_section_text is not null then rpt_section_text end end end lbl_txt,[Rpt_Sub_sub_section_text],[Rpt_Sub_section_text],rpt_section_text,"
        strQ+="case when  [Rpt_Sub_sub_section_text] is not null then 3 "
        strQ+="else case when  [Rpt_Sub_section_text] is not null then 2 "
        strQ+="else case when  rpt_section_text is not null then 1  end end end lbl_lvl,"
        strQ+="case when  [Rpt_Sub_sub_section_text] is not null then "
        strQ+="concat(cast ([Index_Section]  as varchar),'.',cast ([Index_Sub_Section]  as varchar),'.',"
        strQ+="cast ([Index_Sub_Sub_Section]  as varchar))else case when  [Rpt_Sub_section_text] is not null then "
        strQ+="concat(cast ([Index_Section]  as varchar),'.',cast ([Index_Sub_Section]  as varchar))else "
        strQ+="case when  rpt_section_text is not null then cast ([Index_Section]  as varchar) end end end lbl_idx,rep_temp.* "
        strQ+="from FL_Report_Template_Temp rep_temp  LEFT JOIN FL_Report_Content "
        strQ+="on FL_Report_Content.FL_Report_Template_AID = rep_temp.FL_Report_Template_Temp_AID "
        strQ+="inner join FL_RPT_Section_Master sec_mst on rep_temp.Rpt_section_AID=sec_mst.[FL_Rpt_section_AID] "
        strQ+="left outer join  FL_RPT_sub_Section_Master sub_sec_mst on rep_temp.Rpt_sub_section_AID=sub_sec_mst.[FL_Rpt_sub_section_AID] "
        strQ+="left outer join  FL_RPT_sub_sub_Section_Master sub_sub_sec_mst on rep_temp.Rpt_sub_sub_section_AID=sub_sub_sec_mst.[FL_Rpt_sub_sub_section_AID] "
        # strQ+="where rep_temp.template_name='new one temp' "
        strQ+="where rep_temp.template_name='"+request.data['template_name']+"' "
        strQ+="order by [Index_Section] ,[Index_Sub_Section] ,[Index_Sub_Sub_Section]"
        print("strq FLL updated-----------",strQ)
        dtusers=  self.objdbops.getTable(strQ) 
        dtusers= dtusers.to_json(orient='records')
        d = json.loads(dtusers)
        print("data--------------",d)
    
        return Response({"df":d})


class FL_Fetch_Header_Details(APIView):
    def get(self,request,id=None):
        # template_name = 'new one temp'
        print("template_name",request.data['template_name'] )
        header_obj = FlReportTemplateHeader.objects.filter(fl_report_template_name = request.data['template_name']).first()
        header_name = header_obj.header_template_name
        print("header_name",header_name)
        header_data_obj = FlReportTitleTemplate.objects.filter(template_name = header_name).order_by('title_id')
        serializer =  FL_ReportTitleTemplateSerializer(header_data_obj,many=True)
        print("data45",serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FL_ReportHeaderTitleContentAPI(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request_data",request.data)
        if request.data['type'] == 'update':
            print("request_data------------------------------------------------------s",request.data)    
            obj = FlReportHeaderTitleContent.objects.filter(template_name=request.data['template_name'],mdl_id = request.data['mdl_id'],title_id = int(request.data['title_id'])).update(comment=request.data['comment'])
            print("obj----------------------",obj)
            return Response({'msg':'Report Header Title Content Updated Successufully','data':obj},status=status.HTTP_201_CREATED)
        else:
            pass
        obj = FlReportHeaderTitleContent.objects.filter(template_name=request.data['template_name'],title_id = request.data['title_id'],mdl_id = request.data['mdl_id']).first()
        if obj:
            return Response({'msg':'Data Already Exist'},status=status.HTTP_201_CREATED)
        else:
            serializer = FLReportHeaderTitleContentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'msg':'Report Header Title Content Saved Successufully'},status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
        
class AssignRiskFactorAPI(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            print('in assignriskfactors ', request.data)
            try:
                serializer = AssignmentRiskFactorSerializer(data=request.data)
            except Exception as e:
                print(e,',',traceback.print_exc())
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'msg':'Risk Factor Assignment is saved Successufully'},status=status.HTTP_201_CREATED)
            return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("error is",traceback.print_exc())


class Category_MasterAPI(APIView):
    permission_classes=[IsAuthenticated]

    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            print("id",id)
            cat_master = ModelCategory.objects.get(category_aid=id)
            serializer = Cetegory_MasterSerializer(cat_master)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        catmaster =  ModelCategory.objects.all()
        serializer =  Cetegory_MasterSerializer(catmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = Cetegory_MasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Category created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

    permission_classes=[IsAuthenticated]
    def put(self,request):
        print("data",request.data)
        try:
            id=request.data['id']
            print("id",id)
            obj = ModelCategory.objects.get(category_aid=id)
        except ModelCategory.DoesNotExist:
            return Response({'msg':'Issue Type_Master does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = Cetegory_MasterSerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Category Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)


class GetSubCategory(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, cat_id=None):
        if cat_id is not None:
            print("cat_id", cat_id)
            sub_categories = ModelSubCategory.objects.filter(category_aid=cat_id)
            serializer = Sub_Cetegory_MasterSerializer(sub_categories, many=True)
            print("serializer",serializer.data)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    

def check_salt():
      
    raw_password = "MRM_user"
    custom_salt = "mysalt123"  # Use a securely generated salt in real applications

    hashed_password = make_password(password=raw_password, salt=custom_salt)

    print("0----------------01",hashed_password)
check_salt()

# new add

class AddModelMetrics(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        mdlmatricmaster = ModelMetricMaster.objects.all()
        # serializer = ModelMetricMasterSerializer(mdlmatricmaster,many=True)
        # print("mmm serializer",mdlmatricmaster)
        lst=[]
        for i in mdlmatricmaster:
            dict = {}
            dict['mm_aid'] = i.mm_aid
            dict['mm_label'] = i.mm_label
            dict['mm_description'] = i.mm_description
            lst_a = []
            mdldept = ModelMetricDept.objects.filter(mm_aid = i.mm_aid)
            # dict['departments'] = mdldept.dept_details.dept_label
            print('mdldept ',mdldept.values())
            for j in mdldept:
                cat=j.category_aid.category_label
                sub_cat=j.sub_category_aid.sub_category_label
                lst_a.append(j.dept_aid.dept_label)
                result = ', '.join(map(str, lst_a))
                dict['departments'] = result
                dict['model_category']=cat
                dict['model_sub_category']=sub_cat
                # print("dict",dict)
            # serializer_a = ModelMetricDeptSerializer(mdldept,many=True)
            # print("mmd serializer",serializer_a.data)
            lst.append(dict)
        print("listttttt----------------",lst)
        
        return Response({"status": "success", "data": lst}, status=status.HTTP_200_OK)

    def post(self,request):
        serializer = ModelMetricMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Model Metrics saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = ModelMetricMaster.objects.get(frequency_aid=id)

        except ModelMetricMaster.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Model Metric Master does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        print("request.data",request.data)
        serializer = ModelMetricMasterSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Model Metric Master Data Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)


class editmodelmetrics(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            mmmaster = ModelMetricMaster.objects.get(mm_aid=id)
            serializer = ModelMetricMasterSerializer(mmmaster)
            dict = {}
            dict['mm_aid'] = mmmaster.mm_aid
            dict['mm_label'] = mmmaster.mm_label
            dict['mm_description'] = mmmaster.mm_description
            dict['mm_status'] = mmmaster.mm_status
            dict['mm_is_global'] = mmmaster.mm_is_global
            lst_a = []
            mdldept = ModelMetricDept.objects.filter(mm_aid = mmmaster.mm_aid)
            # dict['departments'] = mdldept.dept_details.dept_label
            for j in mdldept:
                print("mdldept",j.dept_aid.dept_label)
                lst_a.append(j.dept_aid.dept_label)
            result = ', '.join(map(str, lst_a))
            dict['departments'] = result
            dict['departments_list'] = lst_a
            # mdlmatricmaster = ModelMetricMaster.objects.all()
        # serializer = ModelMetricMasterSerializer(mdlmatricmaster,many=True)
        # print("mmm serializer",mdlmatricmaster)
            
            return Response({"status": "success", "data": dict}, status=status.HTTP_200_OK)

        modelmetricnmaster = ModelMetricMaster.objects.all()
        serializer =  ModelMetricMasterSerializer(modelmetricnmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class savemodelmetrics(APIView): 
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request data",request.data)
        serializer = ModelMetricMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Metric is created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = ModelMetricMaster.objects.get(mm_aid=id)

        except ModelMetricMaster.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Model Metric Master does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        print("request.data",request.data)
        serializer = ModelMetricMasterSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Model Metric  Data Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class savemodeldepartment(APIView): 
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request data",request.data)
        mm_instance = ModelMetricMaster.objects.get(mm_aid=request.data['mm_aid'])
        dept_instance = Department.objects.get(dept_aid=request.data['dept_aid'])
        category_instance = ModelCategory.objects.get(category_aid=request.data['category_aid'])
        sub_category_instance = ModelSubCategory.objects.get(sub_category_aid=request.data['sub_category_aid'])

        model_obj = ModelMetricDept.objects.create(
            mm_aid=mm_instance,
            dept_aid=dept_instance,
            category_aid=category_instance,
            sub_category_aid=sub_category_instance,
            added_by_field=request.data.get('added_by_field')  # optional but included from your request.data
        )
        print("saved")

        return Response({'msg':'Model Department is created Successufully'})
        
        # print("request data",request.data)
        # serializer = ModelMetricDeptSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response({'data':serializer.data,'msg':'Metric_Department is created Successufully'},status=status.HTTP_201_CREATED)
        # return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = ModelMetricDept.objects.get(mm_aid=id)

        except ModelMetricDept.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Model Metric Master does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        print("request.data",request.data)
        serializer = ModelMetricDeptSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Metric_Department is Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)


class get_model_cat_subcat(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        mm_aid = request.GET.get('mm_aid')
        print("mm_aid",mm_aid)
        get_obj = ModelMetricDept.objects.filter(mm_aid=mm_aid).values('category_aid', 'sub_category_aid').distinct()

        print("get_obj",get_obj)
        model_category_val = get_obj[0]['category_aid']
        model_sub_category_val = get_obj[0]['sub_category_aid']
        print("model_category_val",model_category_val)
        print("model_sub_category_val",model_sub_category_val)

        category_label=ModelCategory.objects.get(category_aid=model_category_val).category_label
        print("category_label",category_label)
        sub_category_label=ModelSubCategory.objects.get(sub_category_aid=model_sub_category_val).sub_category_label
        print("sub_category_label",sub_category_label)
        return JsonResponse({'category_label':category_label,'sub_category_label':sub_category_label})

class checkMetricDept(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        print("Metric dept check",request.data)
        mm_aid = request.data['mm_aid']
        dept_labels = request.data.get('dept_label', [])
        added_by = request.data.get('added_by_field')

        # Step 1: Get existing category and sub-category info for this bm_aid
        existing = ModelMetricDept.objects.filter(mm_aid_id=mm_aid)
        category_aid = None
        sub_category_aid = None

        if existing.exists():
            first = existing.first()
            category_aid = first.category_aid_id
            sub_category_aid = first.sub_category_aid_id

        # Step 2: Delete existing dept_aid entries (filtered by bm_aid only)
        existing.delete()

        # Step 3: Create new entries using correct foreign key field names
        new_entries = [
            ModelMetricDept(
                mm_aid_id=mm_aid,
                dept_aid_id=int(dept),
                added_by_field=added_by,
                category_aid_id=category_aid,
                sub_category_aid_id=sub_category_aid
            )
            for dept in dept_labels
        ]

        # Step 4: Bulk insert
        ModelMetricDept.objects.bulk_create(new_entries)
        print("update done")
        return Response({'msg':"Business Department Updated Successfully"})

##business
class savebusinessmetrics(APIView): 
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request data",request.data)
        serializer = BusinessMetricMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Business Metric is created Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = BusinessMetricMaster.objects.get(bm_aid=id)

        except BusinessMetricMaster.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Model Metric Master does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        print("request.data",request.data)
        serializer = BusinessMetricMasterSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Business Metric Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class savebusinessdepartment(APIView): 
    permission_classes=[IsAuthenticated]
    def post(self,request):
        print("request data",request.data)
        bm_instance = BusinessMetricMaster.objects.get(bm_aid=request.data['bm_aid'])
        dept_instance = Department.objects.get(dept_aid=request.data['dept_aid'])
        category_instance = ModelCategory.objects.get(category_aid=request.data['category_aid'])
        sub_category_instance = ModelSubCategory.objects.get(sub_category_aid=request.data['sub_category_aid'])

        busines_obj = BusinessMetricDept.objects.create(
            bm_aid=bm_instance,
            dept_aid=dept_instance,
            category_aid=category_instance,
            sub_category_aid=sub_category_instance,
            added_by_field=request.data.get('added_by_field')  # optional but included from your request.data
        )
        print("saved")

        return Response({'msg':'Business Department is created Successufully'})

        
        # serializer = BusinessMetricDeptSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response({'data':serializer.data,'msg':'Business Department is created Successufully'},status=status.HTTP_201_CREATED)
        # return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = ModelMetricDept.objects.get(mm_aid=id)

        except ModelMetricDept.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Model Metric Master does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        print("request.data",request.data)
        serializer = ModelMetricDeptSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Metric_Department is Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)


          
class AddBusinessMetrics(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        busmatricmaster = BusinessMetricMaster.objects.all()
        # serializer = ModelMetricMasterSerializer(mdlmatricmaster,many=True)
        # print("mmm serializer",mdlmatricmaster)
        
        lst=[]
        for i in busmatricmaster:
            dict = {}
            print("busmatricmaster",i.bm_aid)
            dict['bm_aid'] = i.bm_aid
            dict['bm_label'] = i.bm_label
            dict['bm_description'] = i.bm_description
            lst_a = []
            cat=''
            sub_cat=''
            busdept = BusinessMetricDept.objects.filter(bm_aid = i.bm_aid)
            # dict['departments'] = mdldept.dept_details.dept_label
            print('busdept ',busdept.values())
            for j in busdept:
                cat=j.category_aid.category_label
                sub_cat=j.sub_category_aid.sub_category_label
                lst_a.append(j.dept_aid.dept_label)
            result = ', '.join(map(str, lst_a))
            dict['departments'] = result
            dict['model_category']=cat
            dict['model_sub_category']=sub_cat

            # serializer_a = ModelMetricDeptSerializer(mdldept,many=True)
            # print("mmd serializer",serializer_a.data)
            lst.append(dict)
        print("list----------------",lst)
        
        return Response({"status": "success", "data": lst}, status=status.HTTP_200_OK)

    def post(self,request):
        serializer = ModelMetricMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Model Metrics saved Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            id=request.data['id']
            smp = ModelMetricMaster.objects.get(frequency_aid=id)

        except ModelMetricMaster.DoesNotExist:
            # msg = {'msg':'Department does not exist'}
            return Response({'msg':'Model Metric Master does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        print("request.data",request.data)
        serializer = ModelMetricMasterSerializer(smp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg':'Model Metric Master Data Updated Successufully'},status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors,'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class editbusinessmetrics(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            bmmaster = BusinessMetricMaster.objects.get(bm_aid=id)
            serializer = BusinessMetricMasterSerializer(bmmaster)
            dict = {}
            dict['bm_aid'] = bmmaster.bm_aid
            dict['bm_label'] = bmmaster.bm_label
            dict['bm_description'] = bmmaster.bm_description
            dict['bm_status'] = bmmaster.bm_status
            dict['bm_is_global'] = bmmaster.bm_is_global
            lst_a = []
            bussdept = BusinessMetricDept.objects.filter(bm_aid = bmmaster.bm_aid)
            # dict['departments'] = mdldept.dept_details.dept_label
            for j in bussdept:
                print("bussdept",j.dept_aid.dept_label)
                lst_a.append(j.dept_aid.dept_label)
            result = ', '.join(map(str, lst_a))
            dict['departments'] = result
            dict['departments_list'] = lst_a
            # mdlmatricmaster = ModelMetricMaster.objects.all()
        # serializer = ModelMetricMasterSerializer(mdlmatricmaster,many=True)
        # print("mmm serializer",mdlmatricmaster)
            
            return Response({"status": "success", "data": dict}, status=status.HTTP_200_OK)

        businessmetricnmaster = BusinessMetricMaster.objects.all()
        serializer =  BusinessMetricMasterSerializer(businessmetricnmaster,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class get_business_cat_subcat(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        bm_aid = request.GET.get('bm_aid')
        print("bm_aid",bm_aid)
        get_obj = BusinessMetricDept.objects.filter(bm_aid=bm_aid).values('category_aid', 'sub_category_aid').distinct()

        print("get_obj",get_obj)
        model_category_val = get_obj[0]['category_aid']
        model_sub_category_val = get_obj[0]['sub_category_aid']
        print("model_category_val",model_category_val)
        print("model_sub_category_val",model_sub_category_val)

        category_label=ModelCategory.objects.get(category_aid=model_category_val).category_label
        print("category_label",category_label)
        sub_category_label=ModelSubCategory.objects.get(sub_category_aid=model_sub_category_val).sub_category_label
        print("sub_category_label",sub_category_label)
        return JsonResponse({'category_label':category_label,'sub_category_label':sub_category_label})


class checkBusinessDept(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        print("Business dept check",request.data)
        bm_aid = request.data['bm_aid']
        dept_labels = request.data.get('dept_label', [])
        added_by = request.data.get('added_by_field')

        # Step 1: Get existing category and sub-category info for this bm_aid
        existing = BusinessMetricDept.objects.filter(bm_aid_id=bm_aid)
        category_aid = None
        sub_category_aid = None

        if existing.exists():
            first = existing.first()
            category_aid = first.category_aid_id
            sub_category_aid = first.sub_category_aid_id

        # Step 2: Delete existing dept_aid entries (filtered by bm_aid only)
        existing.delete()

        # Step 3: Create new entries using correct foreign key field names
        new_entries = [
            BusinessMetricDept(
                bm_aid_id=bm_aid,
                dept_aid_id=int(dept),
                added_by_field=added_by,
                category_aid_id=category_aid,
                sub_category_aid_id=sub_category_aid
            )
            for dept in dept_labels
        ]

        # Step 4: Bulk insert
        BusinessMetricDept.objects.bulk_create(new_entries)
        print("update done")
        return Response({'msg':"Business Department Updated Successfully"})
        # serializer = BusinessMetricDeptSerializer(bussmatricmaster,many=True)
        # print("serializer.data",serializer.data)
        # return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class fetch_mdl_document_name(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        documents = MdlDocuments.objects.filter(mdl_id=request.data['mdlid'],mdl_doc_type = request.data['doc_type'])
        serializer = MdlDocumentsSerializer(documents, many=True)
        print("serializer",serializer.data)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    

class Fetchallmdlid(APIView):
    print()
    def get(self,request,id=None):
        usrmaster = ModelOverview.objects.all()
        serializer =  ModelOverviewSerializer(usrmaster,many=True)
        print("serializer-------------------------------",serializer.data)
        
        return Response({'mdlids':serializer.data}, status=status.HTTP_200_OK)












