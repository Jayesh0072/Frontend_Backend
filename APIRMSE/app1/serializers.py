from django.db.models import Q # for queries
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import * #Users,UserCategory,TaskRegistration,Department,Task_Relevant_Personnel,TaskSummery,Alert,IssueRegistration,IssueRelevantPersonnel,IssueSummery,ModelOverview,Issue_Type_Master,Sub_Issue_Type_Master,TaskPriorityMaster,TaskFunctionMaster,TaskTypeMaster,TaskApprovalstatusMaster,information,SubTasktypeMaster,DashboardContentMaster,UserDashboardContentMaster
from django.core.exceptions import ValidationError
from uuid import uuid4
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password,check_password



class UserCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCategory
        fields = '__all__'


# class UserSerializer(serializers.ModelSerializer):
#     uc_details = UserCategorySerializer(source='uc_aid', read_only=True)
#     u_email = serializers.EmailField(
#         required=True,
#         validators=[UniqueValidator(queryset=Users.objects.all())]
#         )
#     u_name = serializers.CharField(
#         required=True,
#         validators=[UniqueValidator(queryset=Users.objects.all())]
#         )
#     u_password = serializers.CharField(max_length=8)
    
#     class Meta:
#         model = Users
#         fields = (
#             'u_aid',
#             'u_name',
#             'u_password',
#             'u_email',
#             'u_fname',
#             'u_lname',
#             # 'u_profilepic',
#             'uc_aid',
#             'uc_details',
#             # 'u_description',
#             # 'u_extra1',
#             # 'u_extra2',
#             'is_active',
#             'addedby',
#             'adddate',
#             'updatedby',
#             'updatedate',
#             'dept_aid',
#             'u_reportto',
#             'U_AID_BackUpFor',
#         )


class UserSerializer(serializers.ModelSerializer):
   # uc_details = UserCategorySerializer(source='uc_aid', read_only=True)
    u_email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Users.objects.all())]
        )
    u_name = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Users.objects.all())]
        )
    u_password = serializers.CharField(write_only=True,max_length=8)

    def create(self, validated_data):
        validated_data['u_password'] = make_password(validated_data['u_password'],"mysalt123")
        return super(UserSerializer, self).create(validated_data)

    
    class Meta:
        model = Users
        fields = (
            'u_aid',
            'u_name',
            'u_password',
            'u_email',
            'u_fname',
            'u_lname',
            # 'u_profilepic',
            'uc_aid',
            #'uc_details',
            # 'u_description',
            # 'u_extra1',
            # 'u_extra2',
            'is_active',
            'addedby',
            'adddate',
            'updatedby',
            'updatedate',
            'dept_aid',
            'u_reportto',
            #'U_AID_BackUpFor',
        )


# class UserLoginSerializer(serializers.ModelSerializer):
#     # to accept either username or email
#     u_name = serializers.CharField()
#     u_password = serializers.CharField()
#     token = serializers.CharField(required=False, read_only=True)

#     def validate(self, data):
#         # user,email,password validator
#         u_name = data.get("u_name", None)
#         u_password = data.get("u_password", None)
#         if not u_name and not u_password:
#             raise ValidationError("Details not entered.")
#         user = None
#         # if the email has been passed
#         if '@' in u_name:
#             user = Users.objects.filter(
#                 Q(u_email=u_name) &
#                 Q(u_password=u_password)
#                 ).distinct()
#             if not user.exists():
#                 raise ValidationError("Invalid username or password.")
#             user = Users.objects.get(u_email=u_name)
#         else:
#             user = Users.objects.filter(
#                 Q(u_name=u_name) &
#                 Q(u_password=u_password)
#             ).distinct()
#             if not user.exists():
#                 raise ValidationError("Invalid username or password.")
#             user = Users.objects.get(u_name=u_name)
#         # if user.if_logged:
#         #     raise ValidationError("User already logged in.")
#         user.if_logged = True 
#         token, created = Token.objects.get_or_create(user=user)
#         print('print token ',token.key)
#         data['token'] = token.key#uuid4()
#         user.token = data['token']
#         data['u_password']=""
#         user.save()
#         return data

#     class Meta:
#         model = Users
#         fields = (
#             'u_name',
#             'u_password',
#             'token', 
#         )

#         read_only_fields = (
#             'token',
#         )

class UserLoginSerializer(serializers.ModelSerializer):
    u_name = serializers.CharField()
    u_password = serializers.CharField(write_only=True)
    token = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        u_name = data.get("u_name")
        u_password = data.get("u_password")
        user = None

        if not u_name or not u_password:
            raise ValidationError("Details not entered.")

        try:
            user = Users.objects.get(Q(u_email=u_name) | Q(u_name=u_name))
        except Users.DoesNotExist:
            raise ValidationError("Invalid username or password.")

        if not check_password(u_password, user.u_password):
            raise ValidationError("Invalid username or password.")

        user.if_logged = True
        token, created = Token.objects.get_or_create(user=user)
        data['token'] = token.key
        user.token = token.key
        data['u_password'] = ""
        user.save()
        return data

    class Meta:
        model = Users
        fields = ('u_name', 'u_password', 'token')
        read_only_fields = ('token',)




class UserLogoutSerializer(serializers.ModelSerializer):
    u_name = serializers.CharField()
    is_active = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        u_name = data.get("u_name", None)
        print(u_name)
        user = None
        try:
            user = Users.objects.get(u_name=u_name)
            if not user.if_logged:
                raise ValidationError("User is not logged in.")
        except Exception as e:
            raise ValidationError(str(e))
        user.if_logged = False
        user.token = ""
        user.save()
        data['is_active'] = "User is logged out."
        return data    

    class Meta:
        model = Users
        fields = (
            'u_name',
            'is_active',
        )











class TaskRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRegistration
        fields = ('task_id','department','originator','task_function','registration_date','task_type','sub_task_type','priority','end_date','completion_status','approval_status','task_major_version','task_minor_version','task_count','addedby','adddate','updatedby','updatedate','link_id')




class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('dept_aid','dept_label','dept_description','dept_ismrm','activestatus','addedby','adddate','updatedby','updatedate')


class Task_Relevant_PersonnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task_Relevant_Personnel
        fields = ('u_type','u_id','addedby','adddate','updatedby','updatedate','task')

class TaskSummerySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSummery
        fields = ('task_summery','task_requirement','assignee_comments','approval','approver_comments','task_registration','addedby','adddate','updatedby','updatedate')



class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ('author','recipient','alert_date','days_prior','period','comments','u_aid')



class IssueRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueRegistration
        fields = '__all__'





class IssueRelevantPersonnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueRelevantPersonnel
        fields = ('u_type','u_id','addedby','adddate','updatedby','updatedate','issue')



class IssueSummerySerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueSummery
        fields = ('issue_summery','issue_requirement','assignee_comments','approval','approver_comments','issue','addedby','adddate','updatedby','updatedate')


class ModelOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelOverview
        fields = "__all__"

class FrequencyMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrequencyMaster
        fields = "__all__"

class ModelMetricMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelMetricMaster
        fields = ('mm_aid','mm_label','mm_description','mm_status','mm_is_global','added_by')

class PerformanceMonitoringSetupTempSerializer(serializers.ModelSerializer):
    mm_details = ModelMetricMasterSerializer(source='metric', read_only=True)
    class Meta:
        model = PerformanceMonitoringSetupTemp
        fields = ('mdl_id','threshold','warning','frequency','metric','mm_details','metric_value_type','added_by','added_on')



class ModelMetricDeptSerializer(serializers.ModelSerializer):
    mm_details = ModelMetricMasterSerializer(source='mm_aid', read_only=True)
    dept_details = DepartmentSerializer(source='dept_aid',read_only =True )
    class Meta:
        model = ModelMetricDept
        fields = ('mm_aid','dept_aid','added_by_field','mm_details','dept_details','category_aid','sub_category_aid') 

class Issue_Type_MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue_Type_Master
        fields = ('issue_type_label','issue_type_description','activestatus','addedby','adddate','updatedby','updatedate')

class PerformanceMonitoringSetupSerializer(serializers.ModelSerializer):
    mm_details = ModelMetricMasterSerializer(source='metric', read_only=True)
    class Meta:
        model = PerformanceMonitoringSetup
        fields = ('mdl_id','threshold','warning','frequency','metric','mm_details','metric_value_type','added_by','added_on')


class Sub_Issue_Type_MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sub_Issue_Type_Master
        fields = ('sub_issue_type_label','sub_issue_type_description','activestatus','addedby','adddate','updatedby','updatedate','issue_type_aid')


class TaskPriorityMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model =  TaskPriorityMaster
        fields = ('task_priority_aid','task_priority_label','task_priority_description','activestatus','addedby','adddate','updatedby','updatedate')



class TaskFunctionMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model =  TaskFunctionMaster
        fields = ('task_function_aid','task_function_label','task_function_description','activestatus','addedby','adddate','updatedby','updatedate')


class TaskTypeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTypeMaster
        fields = ('task_type_aid','task_type_label','task_type_description','activestatus','addedby','adddate','updatedby','updatedate')



class TaskApprovalstatusMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskApprovalstatusMaster
        fields = ('task_approvalstatus_aid','task_approvalstatus_label','task_approvalstatus_description','activestatus','addedby','adddate','updatedby','updatedate')


class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = information
        fields = '__all__'

class SubTasktypeMasterSerializer(serializers.ModelSerializer):
    task_type_details = TaskTypeMasterSerializer(source='task_type_aid', read_only=True)
    class Meta:
        model = SubTasktypeMaster
        fields = ('sub_task_type_aid','sub_task_type_label','sub_task_type_description','activestatus','addedby','adddate','updatedby','updatedate','task_type_aid','task_type_details')




class DashboardContentMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardContentMaster
        fields = ('display_type','source','sorting_index')

class UserDashboardContentMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDashboardContentMaster
        fields = ('user_id','display_type','source','sorting_index')



class Issue_Type_MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue_Type_Master
        fields = ('issue_type_aid','issue_type_label','issue_type_description','activestatus','addedby','adddate','updatedby','updatedate')


class Sub_Issue_Type_MasterSerializer(serializers.ModelSerializer):
    issue_type_details = Issue_Type_MasterSerializer(source='issue_type_aid', read_only=True)
    class Meta: 
        model = Sub_Issue_Type_Master
        fields = ('sub_issue_type_aid','sub_issue_type_label','sub_issue_type_description','activestatus','addedby','adddate','updatedby','updatedate','issue_type_aid','issue_type_details')


class IssuePriorityMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model =  IssuePriorityMaster
        fields = ('issue_priority_aid','issue_priority_label','issue_priority_description','activestatus','addedby','adddate','updatedby','updatedate')


class IssueFunctionMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model =  IssueFunctionMaster
        fields = ('issue_function_aid','issue_function_label','issue_function_description','activestatus','addedby','adddate','updatedby','updatedate')

class IssueApprovalstatusMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueApprovalstatusMaster
        fields = ('issue_approvalstatus_aid','issue_approvalstatus_label','issue_approvalstatus_description','activestatus','addedby','adddate','updatedby','updatedate')


class IntrinsicMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntrinsicMaster
        fields = "__all__"


class RelianceMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelianceMaster
        fields = '__all__'


class MaterialityMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialityMaster
        fields = '__all__'


   

class HistoryRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryRegisterModel
        fields = '__all__'



class ModelFunctionMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelFunctionMaster
        fields = '__all__'




class ModelSourceMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelSourceMaster
        fields = '__all__'



class ModelTypeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelTypeMaster
        fields = '__all__'



class PrdAddrMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrdAddrMaster
        fields = '__all__'



class MdlDependenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MdlDependencies
        fields = '__all__'



class MdlUpstreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = MdlUpstream
        fields = '__all__'



class MdlDwstreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = MdlDwstream
        fields = '__all__'




class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ('first_person','second_person','updated','timestamp')



class ChatmessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatmessage
        fields = ('thread','chat_user','message','timestamp')



class NotificationDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationDetails
        fields = ('notification_from','notification_to','utility','notification_trigger','is_visible','create_date')




class IcqQuestionMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = IcqQuestionMaster
        fields = ('question_label','section_aid','sub_section_aid','sub_sub_section_aid','sub_sub_sub_section_aid','activestatus','addedby','adddate','updatedby','updatedate')


class IcqSectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IcqSections
        fields = ('section_label','activestatus','addedby','adddate','updatedby','updatedate','section_description')


class IcqSubSectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IcqSubSections
        fields = ('sub_section_label','section_aid','activestatus','addedby','adddate','updatedby','updatedate','sub_section_description')



class IcqSubSubSectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IcqSubSubSections
        fields = ('sub_sub_section_label','sub_section_aid','activestatus','addedby','adddate','updatedby','updatedate','sub_sub_section_description')



class IcqSubSubSubSectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IcqSubSubSubSections
        fields = ('sub_sub_sub_section_label','sub_sub_section_aid','activestatus','addedby','adddate','updatedby','updatedate','sub_sub_sub_section_description')

class MdlRelevantPersonnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MdlRelevantPersonnel
        fields = '__all__'

class ValidationAssigntoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidationAssignto
        fields = '__all__'

class VrSubmissionAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VrSubmissionAllocation
        # fields = '__all__'
        fields = ('mdl_id','u_aid','enddate','addedby')

class ValidationReviewFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidationReviewFrequency
        # fields = '__all__'
        fields = ('frequency_aid','model_risk','annual_review_frequency','addedby')

class PerformanceMonitoringDiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceMonitoringDiscussion
        fields = ('perf_mon_aid','room_id','comment','addedby','addedon')
        extra_kwargs = {
            'addedon': {'format': 'hh:mm tt  MMM dd, yyyy'}
        }
    
class PerformanceMonitoringResultFileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceMonitoringResultFileInfo
        fields = ('mdl_id','file_nm','added_by')

class DataMonitoringResultFileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataMonitoringResultFileInfo
        fields = ('mdl_id','file_nm','added_by','freq_idx','freq_val')

class BusinessMetricMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessMetricMaster
        fields = ('bm_aid','bm_label','bm_description','bm_status','bm_is_global','added_by')

class DataMetricMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataMetricMaster
        fields = ('data_aid','data_label','data_description','data_status','data_is_global','added_by')

class BusinessMetricDeptSerializer(serializers.ModelSerializer):
    bm_details = BusinessMetricMasterSerializer(source='bm_aid', read_only=True)
    dept_details = DepartmentSerializer(source='dept_aid',read_only =True )
    class Meta:
        model = BusinessMetricDept
        fields = ('bm_aid','dept_aid','added_by_field','bm_details','dept_details')

class BussKpiMonitoringSetupTempSerializer(serializers.ModelSerializer):
    bm_details = BusinessMetricMasterSerializer(source='metric', read_only=True)
    class Meta:
        model = BussKpiMonitoringSetupTemp
        fields = ('mdl_id','threshold','warning','frequency','metric','bm_details','metric_value_type','added_by','added_on','mo_approval')

class DataMonitoringSetupSerializer(serializers.ModelSerializer):
    dm_details = DataMetricMasterSerializer(source='metric', read_only=True)
    class Meta:
        model = DataMonitoringSetup
        fields = ('mdl_id','threshold','warning','feature','frequency','metric','dm_details','added_by','added_on','mo_approval')

class DataMonitoringSetupTempSerializer(serializers.ModelSerializer):
    dm_details = DataMetricMasterSerializer(source='metric', read_only=True)
    class Meta:
        model = DataMonitoringSetupTemp
        fields = ('mdl_id','threshold','feature','warning','frequency','metric','dm_details','added_by','added_on','mo_approval')

class BussKpiMonitoringSetupSerializer(serializers.ModelSerializer):
    bm_details = BusinessMetricMasterSerializer(source='metric', read_only=True)
    class Meta:
        model = BussKpiMonitoringSetup
        fields = ('mdl_id','threshold','warning','frequency','metric','bm_details','metric_value_type','added_by','added_on')

class DataMetricMasterSerializer(serializers.ModelSerializer):
    class Meta :
        model = DataMetricMaster
        fields = "__all__"

class TempFeatureMatricSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempFeatureMatricSelection
        fields = ('mdl_id','feature','datamatrics','added_by','added_on')

class DataMonitoringOverrideHistorySerializer(serializers.ModelSerializer):
    dm_details = DataMetricMasterSerializer(source='metric', read_only=True)
    class Meta:
        model = DataMonitoringOverrideHistory
        fields = ('mdl_id','metric','feature','old_value','new_value','threshold','warning','actual','added_by','dm_details')

class RptSectionMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RptSectionMaster
        fields = ('rpt_section_aid','rpt_section_text','rpt_section_description','added_by','added_on','activestatus')

class RptSubSectionMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RptSubSectionMaster
        fields = ('rpt_sub_section_aid','rpt_section_aid','rpt_sub_section_text','rpt_sub_section_description','added_by','added_on','activestatus')

class FLRptSubSectionMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlRptSubSectionMaster
        fields = ('fl_rpt_sub_section_aid','rpt_section_aid','rpt_sub_section_text','rpt_sub_section_description','added_by','added_on','activestatus')

class RptSubSubSectionMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RptSubSubSectionMaster
        fields = ('rpt_sub_sub_section_aid','rpt_sub_section_aid','rpt_section_aid','rpt_sub_sub_section_text','rpt_sub_sub_section_description','added_by','added_on','activestatus')

class FLRptSubSubSectionMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlRptSubSubSectionMaster
        fields = ('fl_rpt_sub_sub_section_aid','rpt_sub_section_aid','rpt_section_aid','rpt_sub_sub_section_text','rpt_sub_sub_section_description','added_by','added_on','activestatus')


class ReportTemplateTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTemplateTemp
        fields = ('report_template_temp_aid','template_name','department','rpt_section_aid','rpt_sub_section_aid','rpt_sub_sub_section_aid','index_section','index_sub_section','index_sub_sub_section','added_by')

class FLReportTemplateTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlReportTemplateTemp
        fields = ('fl_report_template_temp_aid','template_name','department','rpt_section_aid','rpt_sub_section_aid','rpt_sub_sub_section_aid','index_section','index_sub_section','index_sub_sub_section','added_by')

class ReportTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTemplate
        fields = ('report_template_aid','template_name','department','rpt_section_aid','rpt_sub_section_aid','rpt_sub_sub_section_aid','index_section','index_sub_section','index_sub_sub_section')

class FLReportTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlReportTemplate
        fields = ('fl_report_template_aid','template_name','department','rpt_section_aid','rpt_sub_section_aid','rpt_sub_sub_section_aid','index_section','index_sub_section','index_sub_sub_section')

class ReportContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportContent
        fields = ('report_content_aid','report_template_aid','template_name','comment','added_by')

class FindingValElementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FindingValElements
        fields = ('element_aid','element_text','element_description','activestatus','addedby','addedon')

class FindingsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FindingsCategory
        fields = ('category_aid','category_text','category_description','activestatus','addedby','addedon')

class FindingValSubElementsSerializer(serializers.ModelSerializer):
    element_details = FindingValElementsSerializer(source='element_aid', read_only=True)
    class Meta:
        model = FindingValSubElements
        fields = ('element_sub_aid','element_aid','element_text','element_description','activestatus','addedby','addedon','element_details')

class QuestionSectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionSections
        fields = ('section_aid','section_label')
    
class QuestionMasterSerializer(serializers.ModelSerializer):
    section_details = QuestionSectionsSerializer(source='section_aid', read_only=True)
    class Meta:
        model = QuestionMaster
        fields = ('question_aid','question_label','section_aid','activestatus','addedby','adddate','updatedby','updatedate','section_details')    

class ValidationRatingMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidationRatingMaster
        fields = ('validation_ratings_master_aid','validation_rating','severity','risk_type','operator','value','addedby')

class ValidationRatingMasterTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidationRatingMasterTemp
        fields = ('validation_ratings_master_temp_aid','validation_rating','severity','risk_type','operator','value','addedby')

class ValFindingsDiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValFindingsDiscussion
        fields = ('val_find_aid','room_id','comment','addedby','addedon','findings_id')
        extra_kwargs = {
            'addedon': {'format': 'hh:mm tt  MMM dd, yyyy'}
        }

class ReportTitleTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTitleTemplate
        fields = ('title_aid','title_id','title_or_heading','title_label','template_name','added_by','added_on','title_type','title_placeholder','title_sort_idx','fontsize','alignment')

class ReportTemplateHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTemplateHeader
        fields = ('report_template_header_aid','report_template_name','header_template_name','added_by','added_on')

class FLReportTemplateHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlReportTemplateHeader
        fields = ('fl_report_template_header_aid','report_template_name','header_template_name','added_by','added_on')


class ReportHeaderTitleContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportHeaderTitleContent
        fields = ('report_header_title_content_aid','template_name','title_id','header_or_title','comment','label','mdl_id','added_by','added_on')

class VtUserDiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VtUserDiscussion
        fields = ('comment_id','mdl_id','utility','sub_utility','comment','added_by','added_on')

class FLSectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlSections
        fields = '__all__'

class FlallocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlAllocation
        fields = '__all__'

class MappingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MappingDetails
        fields = ('excel_fields','database_fields','addedby','adddate')

class FLMappingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlMappingDetails
        fields = ('excel_fields','database_fields','addedby','adddate')

class DatabaseFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseFields
        fields = '__all__'

class FieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldDetails
        fields = ('field_aid','excel_fields','database_fields','department','portfolio','addedby','adddate','description','datatypes')

class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValueDetails
        fields = ('value_aid','database_fields','value','operator','department','portfolio','addedby','adddate')

class ControllclassmasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Controllclassmaster
        fields = '__all__'

class RiskmasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Riskmaster
        fields = '__all__'

class FlReportContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlReportContent
        fields = ('fl_report_content_aid','fl_report_template_aid','template_name','comment','added_by')

class FlReportTitleTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlReportTitleTemplate
        fields = ('title_aid','title_id','title_or_heading','title_label','template_name','added_by','added_on','title_type','title_placeholder','title_sort_idx','fontsize','alignment')

class FlReportHeaderTitleContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlReportHeaderTitleContent
        fields = ('report_header_title_content_aid','template_name','title_id','header_or_title','comment','label','mdl_id','added_by','added_on')

class RiskFactorCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskFactorComments
        fields = '__all__'

class RiskFactorDiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskFactorDiscussion
        fields = '__all__'

class FlSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlSetting
        fields = '__all__'
        
class FL_ReportTitleTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlReportTitleTemplate
        fields = ('title_aid','title_id','title_or_heading','title_label','template_name','added_by','added_on','title_type','title_placeholder','title_sort_idx','fontsize','alignment')

class FLReportHeaderTitleContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlReportHeaderTitleContent
        fields = ('fl_report_header_title_content_aid','template_name','title_id','header_or_title','comment','label','mdl_id','added_by','added_on')


class FL_ReportContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlReportContent
        fields = ('fl_report_content_aid','fl_report_template_aid','template_name','comment','added_by')

class AssignmentRiskFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentRiskFactor
        fields = ('assignment_risk_factor_aid','risk_factor_label','assign_to','end_date','addedby','risk_aid')

class FlDataanalysisImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlDataanalysisImages
        fields = ('fl_dataanalysis_images_aid','image_name','utility','chart_type','variable','department','portfolio','added_by','added_on')

class FlReportTitleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlReportTitleComment
        fields = '__all__'

class FlRawDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlRawData
        fields = '__all__'

class InherentRiskRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = InherentRiskRating
        fields = '__all__'

class ControlEffectivenessRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlEffectivenessRating
        fields = '__all__'

class ResidualRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidualRating
        fields = '__all__'

class FlQuestionRatingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlQuestionRatingData
        fields = '__all__'

class FLRptSectionMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlRptSectionMaster
        fields = ('fl_rpt_section_aid','rpt_section_text','rpt_section_description','added_by','added_on','activestatus')

class IcqInherentRiskRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = IcqInherentRiskRating
        fields = '__all__'

class IcqControlEffectivenessRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = IcqControlEffectivenessRating
        fields = '__all__'

class IcqResidualRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = IcqResidualRating
        fields = '__all__'

class UdaapInherentRiskRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UdaapInherentRiskRating
        fields = '__all__'

class UdaapControlEffectivenessRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UdaapControlEffectivenessRating
        fields = '__all__'

class UdaapResidualRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UdaapResidualRating
        fields = '__all__'


class UdaapQuestionRatingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UdaapQuestionRatingData
        fields = '__all__'

class UdaapSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UdaapSetting
        fields = '__all__'

class FlPoliciesProcedureDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlPoliciesProcedureDocuments
        fields = '__all__'

class Cetegory_MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelCategory
        fields = ('category_aid','category_label','category_description','activestatus','addedby','adddate','updatedby','updatedate')

class Sub_Cetegory_MasterSerializer(serializers.ModelSerializer):
    category_details = Cetegory_MasterSerializer(source='category_aid', read_only=True)
    class Meta:
        model = ModelSubCategory
        fields = ('sub_category_aid','sub_category_label','sub_category_description','activestatus','addedby','adddate','updatedby','updatedate','category_aid','category_details')


class Sub_Cetegory_MasterSerializer(serializers.ModelSerializer):
    category_details = Cetegory_MasterSerializer(source='category_aid', read_only=True)
    class Meta:
        model = ModelSubCategory
        fields = ('sub_category_aid','sub_category_label','sub_category_description','activestatus','addedby','adddate','updatedby','updatedate','category_aid','category_details')

class MdlDocumentsSerializer(serializers.ModelSerializer):
    class Meta :
        model = MdlDocuments
        fields = "__all__"

class ValidationPlanningSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ValidationPlanning
        fields = '__all__'

class NextValidationPlanningSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NextValidationPlanning
        fields = '__all__'


class ICQ_ReportContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IcqReportContent
        fields = '__all__'



