from django.db import models
import datetime
from datetime import datetime

# Create your models here.
class UserCategory(models.Model):
    uc_aid = models.AutoField(db_column='UC_AID', primary_key=True)  # Field name made lowercase.
    uc_label = models.CharField(db_column='UC_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    uc_description = models.CharField(db_column='UC_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    uc_level = models.IntegerField(db_column='UC_Level', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'User_Category'



from django.contrib.auth.models import AbstractUser
class Users(AbstractUser):
    REQUIRED_FIELDS = ('u_password',)
     
    is_staff = None
    is_superuser = None
    # is_active = None
    date_joined=None
    last_name=None
    password=None
    last_login=None
    first_name=None
    email=None
    username=None
    u_aid = models.AutoField(db_column='U_AID', primary_key=True)  # Field name made lowercase.
    u_name = models.CharField(db_column='U_Name', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS',unique=True)  # Field name made lowercase.
    u_password = models.TextField(db_column='U_Password', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    u_email = models.CharField(db_column='U_Email', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    u_fname = models.CharField(db_column='U_FName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    u_lname = models.CharField(db_column='U_LName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    u_profilepic = models.CharField(db_column='U_ProfilePic', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    # uc_aid = models.IntegerField(db_column='UC_AID')  # Field name made lowercase.
    uc_aid = models.ForeignKey('UserCategory', models.DO_NOTHING, db_column='UC_AID', blank=True, null=True)
    u_description = models.CharField(db_column='U_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    u_extra1 = models.CharField(db_column='U_Extra1', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    u_extra2 = models.CharField(db_column='U_Extra2', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    is_active = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    dept_aid = models.IntegerField(db_column='Dept_AID', blank=True, null=True)  # Field name made lowercase.
    u_reportto = models.IntegerField(db_column='U_Reportto', blank=True, null=True)  # Field name made lowercase.
    # if_logged = models.BooleanField(db_column='IfLogged', blank=True, null=True)
    token = models.CharField(db_column='Token', max_length=500, blank=True, null=True)
    U_AID_BackUpFor = models.IntegerField(db_column='U_AID_BackUpFor', blank=True, null=True) 
    USERNAME_FIELD = 'u_name'

    class Meta:
        managed = False
        db_table = 'Users'
        



class TaskRegistration(models.Model):
    task_id = models.CharField(db_column='Task_ID', primary_key=True,max_length=300)  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    originator = models.CharField(db_column='Originator', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    task_function = models.CharField(db_column='Task_Function', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    registration_date = models.DateField(db_column='Registration_Date', blank=True, null=True)  # Field name made lowercase.
    task_type = models.CharField(db_column='Task_Type', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sub_task_type = models.CharField(db_column='Sub_Task_Type', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    priority = models.CharField(db_column='Priority', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    end_date = models.DateField(db_column='End_Date', blank=True, null=True)  # Field name made lowercase.
    completion_status = models.CharField(db_column='Completion_Status', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    approval_status = models.CharField(db_column='Approval_Status', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    task_major_version=models.CharField(db_column='Task_Major_Ver', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    task_minor_version=models.CharField(db_column='Task_Minor_Ver', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    task_count=models.CharField(db_column='Task_Count', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercas
    link_id = models.CharField(db_column='Link_ID',max_length=300)  # Field name made lowercase.
    task_name= models.CharField(db_column='Task_Name',max_length=300)

    class Meta:
        managed = False
        db_table = 'Task_Registration'
    def __str__(self):
        return f"{self.department}"
    




class Department(models.Model):
    dept_aid = models.AutoField(db_column='Dept_AID', primary_key=True)  # Field name made lowercase.
    dept_label = models.CharField(db_column='Dept_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    dept_description = models.CharField(db_column='Dept_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    dept_ismrm = models.IntegerField(db_column='Dept_IsMRM', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Department'



class Task_Relevant_Personnel(models.Model):
    relevant_personnel_id = models.AutoField(db_column='Relevant_Personnel_id', primary_key=True)  # Field name made lowercase.
    u_type = models.CharField(db_column='U_Type', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    u_id = models.CharField(db_column='U_Id', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    task = models.ForeignKey('TaskRegistration', models.DO_NOTHING, db_column='Task_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Task_Relevant_Personnel'



class TaskSummery(models.Model):
    task_summery_id = models.AutoField(db_column='Task_Summery_id', primary_key=True)  # Field name made lowercase.
    task_summery = models.CharField(db_column='Task_Summery', max_length=350, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    task_requirement = models.CharField(db_column='Task_Requirement', max_length=350, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    assignee_comments = models.CharField(db_column='Assignee_Comments', max_length=350, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    approval = models.CharField(db_column='Approval', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    approver_comments = models.CharField(db_column='Approver_Comments', max_length=350, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    task_registration = models.ForeignKey('TaskRegistration', models.DO_NOTHING, db_column='Task_ID', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase
    
    class Meta:
        managed = False
        db_table = 'Task_Summery'    


#Alert models not work 


class Alert(models.Model):
    alert_id = models.AutoField(db_column='Alert_ID', primary_key=True)  # Field name made lowercase.
    author = models.CharField(db_column='Author', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    recipient = models.CharField(db_column='Recipient', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    alert_date = models.DateTimeField(db_column='Alert_Date', blank=True, null=True)  # Field name made lowercase.
    days_prior = models.CharField(db_column='Days_Prior', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    period = models.CharField(db_column='Period', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    comments = models.CharField(db_column='Comments', max_length=350, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    u_aid=models.ForeignKey('Users', models.DO_NOTHING, db_column='U_AID', blank=True, null=True)
    

    class Meta:
        managed = False
        db_table = 'Alert' 



class IssueRegistration(models.Model):
    issue_id = models.CharField(db_column='Issue_ID', primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    originator = models.CharField(db_column='Originator', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    issue_function = models.CharField(db_column='Issue_Function', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    registration_date = models.DateTimeField(db_column='Registration_Date', blank=True, null=True)  # Field name made lowercase.
    issue_type = models.CharField(db_column='Issue_Type', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sub_issue_type = models.CharField(db_column='Sub_Issue_Type', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    priority = models.CharField(db_column='Priority', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    end_date = models.DateTimeField(db_column='End_Date', blank=True, null=True)  # Field name made lowercase.
    completion_status = models.CharField(db_column='Completion_Status', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    approval_status = models.CharField(db_column='Approval_Status', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    issue_major_ver = models.CharField(db_column='Issue_Major_Ver', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    issue_minor_ver = models.CharField(db_column='Issue_Minor_Ver', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    issue_count = models.CharField(db_column='Issue_Count', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase
    link_id = models.CharField(db_column='Link_ID',max_length=300)  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'Issue_Registration'



class IssueRelevantPersonnel(models.Model):
    relevant_personnel_id = models.AutoField(db_column='Relevant_Personnel_id', primary_key=True)  # Field name made lowercase.
    u_type = models.CharField(db_column='U_Type', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    u_id = models.CharField(db_column='U_Id', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    issue = models.ForeignKey(IssueRegistration, models.DO_NOTHING, db_column='Issue_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Issue_Relevant_Personnel'



class IssueSummery(models.Model):
    issue_summery_id = models.AutoField(db_column='Issue_Summery_id', primary_key=True)  # Field name made lowercase.
    issue_summery = models.CharField(db_column='Issue_Summery', max_length=350, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    issue_requirement = models.CharField(db_column='Issue_Requirement', max_length=350, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    assignee_comments = models.CharField(db_column='Assignee_Comments', max_length=350, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    approval = models.CharField(db_column='Approval', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    approver_comments = models.CharField(db_column='Approver_Comments', max_length=350, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    issue = models.ForeignKey(IssueRegistration, models.DO_NOTHING, db_column='Issue_ID', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Issue_Summery'


class ModelOverview(models.Model):
    mdl_id = models.CharField(db_column='Mdl_Id', primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    mdl_cnt = models.IntegerField(db_column='Mdl_Cnt')  # Field name made lowercase.
    mdl_major_ver = models.IntegerField(db_column='Mdl_Major_Ver')  # Field name made lowercase.
    mdl_minor_ver = models.IntegerField(db_column='Mdl_Minor_Ver')  # Field name made lowercase.
    isnewupdate = models.BooleanField(blank=True, null=True)
    is_tool = models.BooleanField(blank=True, null=True)
    department = models.IntegerField(db_column='Department')  # Field name made lowercase.
    func = models.IntegerField(db_column='Func', blank=True, null=True)  # Field name made lowercase.
    reg_dt = models.DateTimeField(db_column='Reg_Dt', blank=True, null=True)  # Field name made lowercase.
    prm_name = models.CharField(db_column='Prm_Name', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    sec_name = models.CharField(db_column='Sec_Name', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mdl_source = models.IntegerField(db_column='Mdl_Source')  # Field name made lowercase.
    mdl_type = models.IntegerField(db_column='Mdl_Type')  # Field name made lowercase.
    mdl_absct = models.CharField(db_column='Mdl_Absct', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mdl_objective = models.CharField(db_column='Mdl_objective', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mdl_appl = models.CharField(db_column='Mdl_Appl', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mdl_risk_anls = models.CharField(db_column='Mdl_Risk_Anls', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    prctaddr = models.IntegerField(db_column='PrctAddr', blank=True, null=True)  # Field name made lowercase.
    usgfreq = models.IntegerField(db_column='UsgFreq', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    is_decommissioned = models.IntegerField(db_column='Is_Decommissioned', blank=True, null=True)  # Field name made lowercase.
    is_submit = models.IntegerField(db_column='Is_submit', blank=True, null=True)  # Field name made lowercase.
    prd_dt = models.DateTimeField(db_column='Prd_Dt', blank=True, null=True)  # Field name made lowercase.
    validation_rating = models.CharField(db_column='Validation_Rating', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    sub_category = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Mdl_OverView'



class Issue_Type_Master(models.Model):
    issue_type_aid = models.AutoField(db_column='Issue_Type_AID', primary_key=True)  # Field name made lowercase.
    issue_type_label = models.CharField(db_column='Issue_Type_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    issue_type_description = models.CharField(db_column='Issue_Type_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Issue_Type_Master'


class Sub_Issue_Type_Master(models.Model):
    sub_issue_type_aid = models.AutoField(db_column='Sub_Issue_Type_AID', primary_key=True)  # Field name made lowercase.
    sub_issue_type_label = models.CharField(db_column='Sub_Issue_Type_Label', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sub_issue_type_description = models.CharField(db_column='Sub_Issue_Type_Description', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.CharField(db_column='AddedBy', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    issue_type_aid = models.ForeignKey('Issue_Type_Master', models.DO_NOTHING, db_column='Issue_Type_AID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sub_Issue_Type_Master'






class TaskPriorityMaster(models.Model):
    task_priority_aid = models.AutoField(db_column='Task_Priority_AID', primary_key=True)  # Field name made lowercase.
    task_priority_label = models.CharField(db_column='Task_Priority_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    task_priority_description = models.CharField(db_column='Task_Priority_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Task_Priority_Master'


class TaskFunctionMaster(models.Model):
    task_function_aid = models.AutoField(db_column='Task_Function_AID', primary_key=True)  # Field name made lowercase.
    task_function_label = models.CharField(db_column='Task_Function_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    task_function_description = models.CharField(db_column='Task_Function_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Task_Function_Master'



class TaskTypeMaster(models.Model):
    task_type_aid = models.AutoField(db_column='Task_Type_AID', primary_key=True)  # Field name made lowercase.
    task_type_label = models.CharField(db_column='Task_Type_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    task_type_description = models.CharField(db_column='Task_Type_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Task_Type_Master'



class TaskApprovalstatusMaster(models.Model):
    task_approvalstatus_aid = models.AutoField(db_column='Task_ApprovalStatus_AID', primary_key=True)  # Field name made lowercase.
    task_approvalstatus_label = models.CharField(db_column='Task_ApprovalStatus_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    task_approvalstatus_description = models.CharField(db_column='Task_ApprovalStatus_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Task_ApprovalStatus_Master'



class information(models.Model):
    name=models.CharField(max_length=200)
    address = models.CharField(max_length=255)


class SubTasktypeMaster(models.Model):
    sub_task_type_aid = models.AutoField(db_column='Sub_Task_Type_AID', primary_key=True)  # Field name made lowercase.
    sub_task_type_label = models.CharField(db_column='Sub_Task_Type_Label', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sub_task_type_description = models.CharField(db_column='Sub_Task_Type_Description', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.CharField(db_column='AddedBy', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    task_type_aid = models.ForeignKey('TaskTypeMaster', models.DO_NOTHING, db_column='Task_Type_AID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sub_Tasktype_Master'



class DashboardContentMaster(models.Model):
    dashboard_content_aid = models.AutoField(db_column='Dashboard_Content_AID', primary_key=True)  # Field name made lowercase.
    display_type = models.CharField(db_column='Display_Type', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sorting_index = models.IntegerField(db_column='Sorting_index', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dashboard_Content_Master'



class UserDashboardContentMaster(models.Model):
    user_dashboard_content_aid = models.AutoField(db_column='User_Dashboard_Content_AID', primary_key=True)  # Field name made lowercase.
    user_id = models.IntegerField(db_column='User_Id', blank=True, null=True)  # Field name made lowercase.
    display_type = models.CharField(db_column='Display_Type', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sorting_index = models.IntegerField(db_column='Sorting_index', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'User_Dashboard_Content_Master'



class MdlRisks(models.Model):
    mdl_id = models.CharField(db_column='Mdl_Id', primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    mdl_risks = models.CharField(db_column='Mdl_Risks', max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    intr_risk = models.CharField(db_column='Intr_Risk', max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    reliance = models.CharField(db_column='Reliance', max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    materiality = models.CharField(db_column='Materiality', max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    risk_mtgn = models.CharField(db_column='Risk_Mtgn', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    fair_lndg = models.CharField(db_column='Fair_Lndg', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mdl_Risks'

class MdlOverview(models.Model):
    mdl_id = models.CharField(db_column='Mdl_Id', primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    mdl_cnt = models.IntegerField(db_column='Mdl_Cnt')  # Field name made lowercase.
    mdl_major_ver = models.IntegerField(db_column='Mdl_Major_Ver')  # Field name made lowercase.
    mdl_minor_ver = models.IntegerField(db_column='Mdl_Minor_Ver')  # Field name made lowercase.
    isnewupdate = models.BooleanField(blank=True, null=True)
    is_tool = models.BooleanField(blank=True, null=True)
    department = models.IntegerField(db_column='Department')  # Field name made lowercase.
    func = models.IntegerField(db_column='Func')  # Field name made lowercase.
    reg_dt = models.DateTimeField(db_column='Reg_Dt', blank=True, null=True)  # Field name made lowercase.
    prm_name = models.CharField(db_column='Prm_Name', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    sec_name = models.CharField(db_column='Sec_Name', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mdl_source = models.IntegerField(db_column='Mdl_Source')  # Field name made lowercase.
    mdl_type = models.IntegerField(db_column='Mdl_Type')  # Field name made lowercase.
    mdl_absct = models.CharField(db_column='Mdl_Absct', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mdl_objective = models.CharField(db_column='Mdl_objective', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mdl_appl = models.CharField(db_column='Mdl_Appl', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mdl_risk_anls = models.CharField(db_column='Mdl_Risk_Anls', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    prctaddr = models.IntegerField(db_column='PrctAddr')  # Field name made lowercase.
    usgfreq = models.IntegerField(db_column='UsgFreq')  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    is_submit = models.IntegerField(db_column='Is_submit', blank=True, null=True)  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'Mdl_OverView'

class MdlRiskMaster(models.Model):
    mdl_risk_aid = models.AutoField(db_column='Mdl_Risk_AID', primary_key=True)  # Field name made lowercase.
    mdl_risk_label = models.CharField(db_column='Mdl_Risk_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    mdl_risk_description = models.CharField(db_column='Mdl_Risk_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    risk_val = models.IntegerField(db_column='Risk_Val', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mdl_Risk_Master'

class IntrinsicMaster(models.Model):
    intrinsic_aid = models.AutoField(db_column='Intrinsic_AID', primary_key=True)  # Field name made lowercase.
    intrinsic_label = models.CharField(db_column='Intrinsic_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    intrinsic_description = models.CharField(db_column='Intrinsic_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    intrinsic_val = models.IntegerField(db_column='Intrinsic_Val', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Intrinsic_Master'

class RelianceMaster(models.Model):
    reliance_aid = models.AutoField(db_column='Reliance_AID', primary_key=True)  # Field name made lowercase.
    reliance_label = models.CharField(db_column='Reliance_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    reliance_description = models.CharField(db_column='Reliance_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    reliance_val = models.IntegerField(db_column='Reliance_Val', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Reliance_Master'

class MaterialityMaster(models.Model):
    materiality_aid = models.AutoField(db_column='Materiality_AID', primary_key=True)  # Field name made lowercase.
    materiality_label = models.CharField(db_column='Materiality_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    materiality_description = models.CharField(db_column='Materiality_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    materiality_val = models.IntegerField(db_column='Materiality_Val', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Materiality_Master'

class HistoryRegisterModel(models.Model):
    history_register_model_id = models.AutoField(db_column='History_Register_Model_ID', primary_key=True)  # Field name made lowercase.
    column_name = models.CharField(db_column='Column_name', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'History_Register_Model'

class ModelFunctionMaster(models.Model):
    mdl_fncn_aid = models.AutoField(db_column='Mdl_Fncn_AID', primary_key=True)  # Field name made lowercase.
    mdl_fncn_label = models.CharField(db_column='Mdl_Fncn_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    mdl_fncn_description = models.CharField(db_column='Mdl_Fncn_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Model_Function_Master'

class ModelSourceMaster(models.Model):
    mdl_scr_aid = models.AutoField(db_column='Mdl_Scr_AID', primary_key=True)  # Field name made lowercase.
    mdl_src_label = models.CharField(db_column='Mdl_Src_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    mdl_src_description = models.CharField(db_column='Mdl_Src_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Model_Source_Master'

class ModelTypeMaster(models.Model):
    mdl_type_aid = models.AutoField(db_column='Mdl_Type_AID', primary_key=True)  # Field name made lowercase.
    mdl_type_label = models.CharField(db_column='Mdl_Type_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    mdl_type_description = models.CharField(db_column='Mdl_Type_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Model_Type_Master'

class PrdAddrMaster(models.Model):
    prd_addr_aid = models.IntegerField(db_column='Prd_Addr_AID', primary_key=True)  # Field name made lowercase.
    prd_addr_label = models.CharField(db_column='Prd_Addr_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    prd_addr_description = models.CharField(db_column='Prd_Addr_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Prd_Addr_Master'

class MdlDependencies(models.Model):
    mdl_id = models.CharField(db_column='Mdl_Id',primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    upstrmmdl = models.CharField(db_column='UpstrmMdl', max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    dwstrmmdl = models.CharField(db_column='DwstrmMdl', max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mdl_Dependencies'

class MdlUpstream(models.Model):
    mdl_upstream_aid = models.AutoField(db_column='Mdl_Upstream_AID', primary_key=True)  # Field name made lowercase.
    mdl_upstream_label = models.CharField(db_column='Mdl_Upstream_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    mdl_upstream_description = models.CharField(db_column='Mdl_Upstream_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mdl_Upstream'

class MdlDwstream(models.Model):
    mdl_dwstream_aid = models.AutoField(db_column='Mdl_Dwstream_AID', primary_key=True)  # Field name made lowercase.
    mdl_dwstream_label = models.CharField(db_column='Mdl_Dwstream_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    mdl_dwstream_description = models.CharField(db_column='Mdl_Dwstream_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mdl_Dwstream'

#chat models
class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        print("kwargs user",kwargs.get('user'))
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs

class Thread(models.Model):
    thread_id = models.AutoField(primary_key=True)
    first_person = models.ForeignKey('Users', models.DO_NOTHING, db_column='first_person', related_name='thread_first_person',blank=True, null=True)
    second_person = models.ForeignKey('Users', models.DO_NOTHING, db_column='second_person', related_name='thread_second_person',blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Thread'
        unique_together = ['first_person', 'second_person']

class Chatmessage(models.Model):
    chat_id = models.AutoField(primary_key=True)
    thread = models.ForeignKey('Thread', models.DO_NOTHING, db_column='thread', blank=True, null=True)
    chat_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='chat_user', blank=True, null=True)
    message = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ChatMessage'

class NotificationDetails(models.Model):
    notification_id = models.AutoField(db_column='Notification_Id', primary_key=True)  # Field name made lowercase.
    notification_from = models.CharField(db_column='Notification_From', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    notification_to = models.CharField(db_column='Notification_To', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    utility = models.CharField(db_column='Utility', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    notification_trigger = models.CharField(db_column='Notification_Trigger', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    is_visible = models.BooleanField(db_column='Is_Visible', blank=True, null=True)  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='Create_Date',default=datetime.now(), blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Notification_Details'




class IcqQuestionMaster(models.Model):
    question_aid = models.AutoField(db_column='Question_AID', primary_key=True)  # Field name made lowercase.
    question_label = models.CharField(db_column='Question_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    section_aid = models.IntegerField(db_column='Section_AID')  # Field name made lowercase.
    sub_section_aid = models.IntegerField(db_column='Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    sub_sub_section_aid = models.IntegerField(db_column='Sub_Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    sub_sub_sub_section_aid = models.IntegerField(db_column='Sub_Sub_Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ICQ_Question_Master'


class IcqSections(models.Model):
    section_aid = models.AutoField(db_column='Section_AID', primary_key=True)  # Field name made lowercase.
    section_label = models.CharField(db_column='Section_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    section_description = models.TextField(db_column='Section_Description', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ICQ_Sections'


class IcqSubSections(models.Model):
    sub_section_aid = models.AutoField(db_column='Sub_Section_AID', primary_key=True)  # Field name made lowercase.
    sub_section_label = models.CharField(db_column='Sub_Section_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    section_aid = models.ForeignKey(IcqSections, models.DO_NOTHING, db_column='Section_AID')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    sub_section_description = models.CharField(db_column='Sub_Section_Description', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ICQ_Sub_Sections'


class IcqSubSubSections(models.Model):
    sub_sub_section_aid = models.AutoField(db_column='Sub_Sub_Section_AID', primary_key=True)  # Field name made lowercase.
    sub_sub_section_label = models.CharField(db_column='Sub_Sub_Section_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    sub_section_aid = models.ForeignKey(IcqSubSections, models.DO_NOTHING, db_column='Sub_Section_AID')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    sub_sub_section_description = models.CharField(db_column='Sub_Sub_Section_Description', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ICQ_Sub_Sub_Sections'


class IcqSubSubSubSections(models.Model):
    sub_sub_sub_section_aid = models.AutoField(db_column='Sub_Sub_Sub_Section_AID', primary_key=True)  # Field name made lowercase.
    sub_sub_sub_section_label = models.CharField(db_column='Sub_Sub_Sub_Section_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    sub_sub_section_aid = models.ForeignKey(IcqSubSubSections, models.DO_NOTHING, db_column='Sub_Sub_Section_AID')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    sub_sub_sub_section_description = models.CharField(db_column='Sub_Sub_Sub_Section_Description', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ICQ_Sub_Sub_Sub_Sections'


class IcqQuestionRating(models.Model):
    rating_id = models.AutoField(db_column='Rating_id', primary_key=True)  # Field name made lowercase.
    question_aid = models.ForeignKey(IcqQuestionMaster, models.DO_NOTHING, db_column='Question_AID')  # Field name made lowercase.
    rating_yes = models.IntegerField(db_column='Rating_Yes', blank=True, null=True)  # Field name made lowercase.
    rating_no = models.IntegerField(db_column='Rating_No', blank=True, null=True)  # Field name made lowercase.
    doc_yes = models.IntegerField(db_column='Doc_Yes', blank=True, null=True)  # Field name made lowercase.
    doc_no = models.IntegerField(db_column='Doc_No', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ICQ_Question_Rating'


class IcqQuestionRatingAllocation(models.Model):
    allocation_aid = models.AutoField(db_column='Allocation_Aid', primary_key=True)  # Field name made lowercase.
    review_id = models.CharField(db_column='Review_id', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    review_name = models.CharField(db_column='Review_Name', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    section_aid = models.IntegerField(db_column='Section_AID')  # Field name made lowercase.
    sub_section_aid = models.IntegerField(db_column='Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    sub_sub_section_aid = models.IntegerField(db_column='Sub_Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    sub_sub_sub_section_aid = models.IntegerField(db_column='Sub_Sub_Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    allocated_to = models.IntegerField(db_column='Allocated_to')  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    model_id = models.CharField(db_column='Model_Id', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ICQ_Question_Rating_Allocation' 

class QueryBuilderFilter(models.Model):
    query_builder_filter_aid = models.AutoField(db_column='Query_Builder_Filter_AID', primary_key=True)  # Field name made lowercase.
    rule = models.CharField(db_column='Query_Rule', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    addon = models.DateTimeField(db_column='AddOn', blank=True, null=True)  # Field name made lowercase.
    file_id = models.IntegerField(db_column='File_id', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    rulename = models.CharField(db_column='Rulename', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    model_id = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Query_Builder_Filter'


class SavedModels(models.Model):
    ml_model_data_id = models.AutoField(db_column='ML_Model_Data_ID', primary_key=True)  # Field name made lowercase.
    model_id = models.CharField(db_column='Model_id', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    selected_model = models.CharField(db_column='Selected_Model', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ml_model_name = models.CharField(db_column='ML_model_name', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    user_id = models.IntegerField(blank=True, null=True)
    dataset = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Saved_Models'


class QuesQuestionMaster(models.Model):
    question_aid = models.AutoField(db_column='Question_AID', primary_key=True)  # Field name made lowercase.
    question_label = models.CharField(db_column='Question_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    section_aid = models.IntegerField(db_column='Section_AID')  # Field name made lowercase.
    sub_section_aid = models.IntegerField(db_column='Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    sub_sub_section_aid = models.IntegerField(db_column='Sub_Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    sub_sub_sub_section_aid = models.IntegerField(db_column='Sub_Sub_Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    question_seq = models.IntegerField(db_column='Question_seq', blank=True, null=True) 

    class Meta:
        managed = False
        db_table = 'Question_Ques_Master'

class QuestionSectionAllocation(models.Model):
    allocation_aid = models.AutoField(db_column='Allocation_Aid', primary_key=True)  # Field name made lowercase.    
    section_aid = models.IntegerField(db_column='Section_AID')  # Field name made lowercase.
    sub_section_aid = models.IntegerField(db_column='Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    sub_sub_section_aid = models.IntegerField(db_column='Sub_Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    sub_sub_sub_section_aid = models.IntegerField(db_column='Sub_Sub_Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    allocated_to = models.IntegerField(db_column='Allocated_to')  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    model_id = models.CharField(db_column='Model_Id', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Question_Section_Allocation'

class IssueFunctionMaster(models.Model):
    issue_function_aid = models.AutoField(db_column='Issue_Function_AID', primary_key=True)  # Field name made lowercase.
    issue_function_label = models.CharField(db_column='Issue_Function_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    issue_function_description = models.CharField(db_column='Issue_Function_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Issue_Function_Master'


class IssuePriorityMaster(models.Model):
    issue_priority_aid = models.AutoField(db_column='Issue_Priority_AID', primary_key=True)  # Field name made lowercase.
    issue_priority_label = models.CharField(db_column='Issue_Priority_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    issue_priority_description = models.CharField(db_column='Issue_Priority_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Issue_Priority_Master'
        
class IssueApprovalstatusMaster(models.Model):
    issue_approvalstatus_aid = models.AutoField(db_column='Issue_ApprovalStatus_AID', primary_key=True)  # Field name made lowercase.
    issue_approvalstatus_label = models.CharField(db_column='Issue_ApprovalStatus_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    issue_approvalstatus_description = models.CharField(db_column='Issue_ApprovalStatus_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Issue_ApprovalStatus_Master'

class ModelsFields(models.Model):
    field_id = models.AutoField(db_column='Field_ID', primary_key=True)  # Field name made lowercase.
    fields_name = models.CharField(db_column='Fields_name', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field_label = models.CharField(db_column='Field_Label', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    is_mandatory = models.BooleanField(db_column='Is_Mandatory', blank=True, null=True)  # Field name made lowercase.
    is_visible = models.BooleanField(db_column='Is_Visible', blank=True, null=True)  # Field name made lowercase.
    field_addedby = models.IntegerField(db_column='[AddedBy', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Models_Fields'

class ModelValidationTypeMaster(models.Model):
    mdl_val_type_aid = models.AutoField(db_column='Mdl_Val_Type_AID', primary_key=True)  # Field name made lowercase.
    mdl_val_type_label = models.CharField(db_column='Mdl_Val_Type_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    mdl_val_type_description = models.CharField(db_column='Mdl_Val_Type_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Model_Validation_Type_Master'

class RolesResponsibilityQuestion(models.Model):
    qtn_aid = models.AutoField(db_column='Qtn_AID', primary_key=True)  # Field name made lowercase.
    question_text = models.CharField(db_column='Question_Text', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    is_active = models.IntegerField(db_column='Is_Active', blank=True, null=True)  # Field name made lowercase.
    is_global = models.IntegerField(db_column='Is_Global', blank=True, null=True)  # Field name made lowercase.
    approved_on = models.DateTimeField(db_column='Approved_On', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(blank=True, null=True)
    addedon = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Roles_Responsibility_Question'

class AuditRegCompl(models.Model):
    compl_aid = models.AutoField(db_column='Compl_AID', primary_key=True)  # Field name made lowercase.
    question_text = models.CharField(db_column='Question_Text', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    is_active = models.IntegerField(db_column='Is_Active', blank=True, null=True)  # Field name made lowercase.
    is_global = models.IntegerField(db_column='Is_Global', blank=True, null=True)  # Field name made lowercase.
    approved_on = models.DateTimeField(db_column='Approved_On', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(blank=True, null=True)
    addedon = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Audit_Reg_Compl'

class AuditRegComplResp(models.Model):
    compl_resp_aid = models.AutoField(db_column='Compl_Resp_AID', primary_key=True)  # Field name made lowercase.
    compl_aid = models.IntegerField(db_column='Compl_AID')  # Field name made lowercase.
    mdl_id = models.CharField(db_column='Mdl_Id', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    question_resp = models.CharField(db_column='Question_Resp', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(blank=True, null=True)
    addedon = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Audit_Reg_Compl_Resp'


class AuditRegComplAllocation(models.Model):
    allocation_aid = models.AutoField(db_column='Allocation_AID', primary_key=True)  # Field name made lowercase.
    compl_aid = models.IntegerField(db_column='Compl_AID')  # Field name made lowercase.
    mdl_id = models.CharField(db_column='Mdl_Id', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(blank=True, null=True)
    addedon = models.DateTimeField(blank=True, null=True)
    allocated_to = models.IntegerField(db_column='Allocated_to', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Audit_Reg_Compl_Allocation'

class RolesResponsibilityQuestionAllocation(models.Model):
    question_allocation_aid = models.AutoField(db_column='Question_Allocation_AID', primary_key=True)  # Field name made lowercase.
    qtn_aid = models.IntegerField(db_column='Qtn_AID')  # Field name made lowercase.
    mdl_id = models.CharField(db_column='Mdl_Id', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(blank=True, null=True)
    addedon = models.DateTimeField(blank=True, null=True)
    allocated_to = models.IntegerField(db_column='Allocated_to', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Roles_Responsibility_Question_Allocation'


class RolesResponsibilityQuestionResponse(models.Model):
    question_response_aid = models.AutoField(db_column='Question_Response_AID', primary_key=True)  # Field name made lowercase.
    qtn_aid = models.IntegerField(db_column='Qtn_AID')  # Field name made lowercase.
    mdl_id = models.CharField(db_column='Mdl_Id', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    qtn_resp = models.CharField(db_column='Qtn_Resp', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(blank=True, null=True)
    addedon = models.DateTimeField(blank=True, null=True)
    allocated_to = models.IntegerField(db_column='Allocated_to', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Roles_Responsibility_Question_Response'

class ActivityTrail(models.Model):
    activity_aid = models.AutoField(db_column='Activity_AID', primary_key=True)  # Field name made lowercase.
    refference_id = models.CharField(db_column='Refference_Id', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activity_trigger = models.CharField(db_column='Activity_Trigger', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    activity_details = models.CharField(db_column='Activity_Details', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_On', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Activity_Trail'

class MdlRelevantPersonnel(models.Model):
    mdl_id = models.CharField(db_column='Mdl_Id', primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    u_type = models.CharField(db_column='U_Type', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    u_id = models.CharField(db_column='U_ID', max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mdl_Relevant_personnel' 

class ValidationAssignto(models.Model):
    mdl_id = models.CharField(db_column='Mdl_Id', primary_key=True,max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    validation_task_type = models.CharField(db_column='Validation_Task_Type', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    u_aid = models.CharField(db_column='U_AID', max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    notify = models.IntegerField(db_column='Notify', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Validation_AssignTo'

# class VrSubmissionAllocation(models.Model):
#     mdl_id = models.CharField(db_column='Mdl_Id', primary_key=True,max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
#     u_aid = models.IntegerField(db_column='U_AID')  # Field name made lowercase.
#     enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
#     addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
#     adddate = models.DateTimeField(db_column='AddDate',blank=True, null=True)  # Field name made lowercase.
#     updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
#     updatedate = models.DateTimeField(db_column='UpdateDate', default=datetime.datetime.now(),blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = 'VR_Submission_Allocation'
class VrSubmissionAllocation(models.Model):
    allocate_aid = models.AutoField(db_column='Allocate_AID', primary_key=True)  # Field name made lowercase.
    mdl_id = models.CharField(db_column='Mdl_Id', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    u_aid = models.IntegerField(db_column='U_AID')  # Field name made lowercase.
    enddate = models.DateField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VR_Submission_Allocation'

class ValidationReviewFrequency(models.Model):
    frequency_aid = models.AutoField(db_column='Frequency_AID', primary_key=True)  # Field name made lowercase.
    model_risk = models.CharField(db_column='Model_Risk', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    annual_review_frequency = models.IntegerField(db_column='Annual_Review_Frequency', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(blank=True, null=True)
    addedon = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'validation_review_frequency'

class PerformanceMonitoringDiscussion(models.Model):
    perf_mon_aid = models.AutoField(db_column='perf_mon_AID', primary_key=True)  # Field name made lowercase.
    room_id = models.CharField(db_column='Room_id', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    addedby = models.IntegerField(blank=True, null=True,)
    addedon = models.DateTimeField(blank=True,default=datetime.now(),null=True)

    class Meta:
        managed = False
        db_table = 'performance_monitoring_discussion'

# class FrequencyMaster(models.Model):
#     frequency_aid = models.AutoField(db_column='Frequency_AID', primary_key=True)  # Field name made lowercase.
#     frequency_label = models.CharField(db_column='Frequency_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
#     frequency_description = models.CharField(db_column='Frequency_Description', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     active_status = models.IntegerField(db_column='Active_Status', blank=TquencyMastrue, null=True)  # Field name made lowercase.
#     added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
#     added_on = models.DateTimeField(db_column='Added_on', blank=True, null=True)  # Field name made lowercase.
#     updated_by = models.IntegerField(db_column='Updated_by', blank=True, null=True)  # Field name made lowercase.
#     updated_on = models.DateTimeField(db_column='Updated_on', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = 'Frequency_Master'

class FrequencyMaster(models.Model):
    frequency_aid = models.AutoField(db_column='Frequency_AID', primary_key=True)  # Field name made lowercase.
    frequency_label = models.CharField(db_column='Frequency_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    frequency_description = models.CharField(db_column='Frequency_Description', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    active_status = models.IntegerField(db_column='Active_Status', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', default=datetime.now, blank=True, null=True)  # Field name made lowercase.
    updated_by = models.IntegerField(db_column='Updated_by', blank=True, null=True)  # Field name made lowercase.
    updated_on = models.DateTimeField(db_column='Updated_on', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Frequency_Master'


# class ModelMetricDept(models.Model):
#     aid = models.AutoField(db_column='AID',primary_key=True)  # Field name made lowercase.
#     # mm_aid = models.IntegerField(db_column='MM_AID', blank=True, null=True)  # Field name made lowercase.
#     mm_aid = models.ForeignKey('ModelMetricMaster', models.DO_NOTHING, db_column='MM_AID', blank=True, null=True)
#     # dept_aid = models.IntegerField(db_column='Dept_AiD', blank=True, null=True)  # Field name made lowercase.
#     dept_aid = models.ForeignKey('Department', models.DO_NOTHING, db_column='Dept_AID', blank=True, null=True)
#     added_by_field = models.IntegerField(db_column='Added_by_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
#     added_on = models.DateTimeField(db_column='Added_on', default=datetime.now, blank=True, null=True)  # Field name made lowercase.
#     updated_by = models.IntegerField(db_column='Updated_by', blank=True, null=True)  # Field name made lowercase.
#     updated_on = models.DateTimeField(db_column='Updated_on', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = 'Model_Metric_Dept'

# class ModelMetricDept(models.Model):
#     aid = models.AutoField(db_column='AID',primary_key=True)  # Field name made lowercase.
#     mm_aid = models.ForeignKey('ModelMetricMaster', models.DO_NOTHING, db_column='MM_AID', blank=True, null=True) # Field name made lowercase.
#     dept_aid = models.ForeignKey('Department', models.DO_NOTHING, db_column='Dept_AID', blank=True, null=True)
#     added_by_field = models.IntegerField(db_column='Added_by_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
#     added_on = models.DateTimeField(db_column='Added_on', blank=True, null=True)  # Field name made lowercase.
#     updated_by = models.IntegerField(db_column='Updated_by', blank=True, null=True)  # Field name made lowercase.
#     updated_on = models.DateTimeField(db_column='Updated_on', blank=True, null=True)  # Field name made lowercase.
#     model_category = models.IntegerField(db_column='Model_category', blank=True, null=True)  # Field name made lowercase.
#     model_sub_category = models.IntegerField(db_column='Model_sub_category', blank=True, null=True)  # Field name made lowercase.
    
#     class Meta:
#         managed = False
#         db_table = 'Model_Metric_Dept'


class ModelMetricDept(models.Model):
    aid = models.AutoField(db_column='AID',primary_key=True)  # Field name made lowercase.
    mm_aid = models.ForeignKey('ModelMetricMaster', models.DO_NOTHING, db_column='MM_AID', blank=True, null=True) # Field name made lowercase.
    dept_aid = models.ForeignKey('Department', models.DO_NOTHING, db_column='Dept_AID', blank=True, null=True)
    added_by_field = models.IntegerField(db_column='Added_by_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    added_on = models.DateTimeField(db_column='Added_on', blank=True, null=True)  # Field name made lowercase.
    updated_by = models.IntegerField(db_column='Updated_by', blank=True, null=True)  # Field name made lowercase.
    updated_on = models.DateTimeField(db_column='Updated_on', blank=True, null=True)  # Field name made lowercase.
    category_aid = models.ForeignKey('ModelCategory', models.DO_NOTHING, db_column='category_aid', blank=True, null=True)
    sub_category_aid = models.ForeignKey('ModelSubCategory', models.DO_NOTHING, db_column='sub_category_aid', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'Model_Metric_Dept'


class ModelMetricMaster(models.Model):
    mm_aid = models.AutoField(db_column='MM_AID',primary_key=True)  # Field name made lowercase.
    # mm_aid = models.ForeignKey('ModelMetricDept', models.DO_NOTHING, db_column='MM_AID', blank=True, null=True)
    mm_label = models.CharField(db_column='MM_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    mm_description = models.CharField(db_column='MM_Description', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mm_status = models.IntegerField(db_column='MM_status', blank=True, null=True)  # Field name made lowercase.
    mm_is_global = models.IntegerField(db_column='MM_Is_Global', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', default=datetime.now, blank=True, null=True)  # Field name made lowercase.
    updated_by = models.IntegerField(db_column='Updated_by', blank=True, null=True)  # Field name made lowercase.
    updated_on = models.DateTimeField(db_column='Updated_on', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Model_Metric_Master'

class PerformanceMonitoringSetupTemp(models.Model):
    mdl_id = models.CharField(db_column='Mdl_Id', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    aid = models.AutoField(db_column='AID',primary_key=True)  # Field name made lowercase.
    # metric = models.IntegerField(db_column='Metric', blank=True, null=True)  # Field name made lowercase.
    metric = models.ForeignKey('ModelMetricMaster', models.DO_NOTHING, db_column='Metric', blank=True, null=True)
    metric_value_type = models.CharField(db_column='Metric_Value_Type', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    threshold = models.FloatField(db_column='Threshold', blank=True, null=True)  # Field name made lowercase.
    warning = models.FloatField(db_column='Warning', blank=True, null=True)  # Field name made lowercase.
    frequency = models.IntegerField(db_column='Frequency', blank=True, null=True)  # Field name made lowercase.
    mo_approval = models.IntegerField(db_column='MO_Approval', blank=True, null=True)  # Field name made lowercase.
    mo_approval_on = models.DateTimeField(db_column='MO_Approval_On', blank=True, null=True)  # Field name made lowercase.
    mrm_approval = models.IntegerField(db_column='MRM_Approval', blank=True, null=True)  # Field name made lowercase.
    mrm_approval_on = models.DateTimeField(db_column='MRM_Approval_On', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_On', blank=True, null=True)  # Field name made lowercase.
    updated_by = models.IntegerField(db_column='Updated_by', blank=True, null=True)  # Field name made lowercase.
    updated_on = models.DateTimeField(db_column='Updated_On', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Performance_Monitoring_Setup_temp'

class PerformanceMonitoringSetup(models.Model):
    mdl_id = models.CharField(db_column='Mdl_Id', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    aid = models.AutoField(db_column='AID',primary_key=True)  # Field name made lowercase.
    # metric = models.IntegerField(db_column='Metric', blank=True, null=True)  # Field name made lowercase.
    metric = models.ForeignKey('ModelMetricMaster', models.DO_NOTHING, db_column='Metric', blank=True, null=True)
    metric_value_type = models.CharField(db_column='Metric_Value_Type', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    threshold = models.FloatField(db_column='Threshold', blank=True, null=True)  # Field name made lowercase.
    warning = models.FloatField(db_column='Warning', blank=True, null=True)  # Field name made lowercase.
    frequency = models.IntegerField(db_column='Frequency', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_On', blank=True, null=True)  # Field name made lowercase.
    updated_by = models.IntegerField(db_column='Updated_by', blank=True, null=True)  # Field name made lowercase.
    updated_on = models.DateTimeField(db_column='Updated_On', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Performance_Monitoring_Setup'

class PerformanceMonitoringResultFileInfo(models.Model):
    aid = models.AutoField(db_column='AID',primary_key=True)  # Field name made lowercase.
    mdl_id = models.CharField(db_column='Mdl_ID', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    file_nm = models.CharField(db_column='file_Nm', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_On', default=datetime.now(),blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Performance_Monitoring_Result_file_info'

# class BusinessMetricDept(models.Model):
#     aid = models.AutoField(db_column='AID',primary_key=True)  # Field name made lowercase.
#     # bm_aid = models.IntegerField(db_column='BM_AID', blank=True, null=True)  # Field name made lowercase.
#     bm_aid = models.ForeignKey('BusinessMetricMaster', models.DO_NOTHING, db_column='BM_AID', blank=True, null=True)
#     # dept_aid = models.IntegerField(db_column='Dept_AiD', blank=True, null=True)  # Field name made lowercase.
#     dept_aid = models.ForeignKey('Department', models.DO_NOTHING, db_column='Dept_AID', blank=True, null=True)
#     added_by_field = models.IntegerField(db_column='Added_by_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
#     added_on = models.DateTimeField(db_column='Added_on', blank=True, null=True)  # Field name made lowercase.
#     updated_by = models.IntegerField(db_column='Updated_by', blank=True, null=True)  # Field name made lowercase.
#     updated_on = models.DateTimeField(db_column='Updated_on', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = 'Business_Metric_Dept'

class BusinessMetricDept(models.Model):
    aid = models.AutoField(db_column='AID',primary_key=True)  # Field name made lowercase.
    # bm_aid = models.IntegerField(db_column='BM_AID', blank=True, null=True)  # Field name made lowercase.
    bm_aid = models.ForeignKey('BusinessMetricMaster', models.DO_NOTHING, db_column='BM_AID', blank=True, null=True)
    # dept_aid = models.IntegerField(db_column='Dept_AiD', blank=True, null=True)  # Field name made lowercase.
    dept_aid = models.ForeignKey('Department', models.DO_NOTHING, db_column='Dept_AID', blank=True, null=True)
    added_by_field = models.IntegerField(db_column='Added_by_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    added_on = models.DateTimeField(db_column='Added_on', blank=True, null=True)  # Field name made lowercase.
    updated_by = models.IntegerField(db_column='Updated_by', blank=True, null=True)  # Field natetimme made lowercase.
    updated_on = models.DateTimeField(db_column='Updated_on', blank=True, null=True)  # Field name made lowercase.
    # model_category = models.IntegerField(db_column='Model_category', blank=True, null=True)  # Field name made lowercase.
    category_aid = models.ForeignKey('ModelCategory', models.DO_NOTHING, db_column='category_aid', blank=True, null=True)
    # model_sub_category = models.IntegerField(db_column='Model_sub_category', blank=True, null=True)  # Field name made lowercase.
    sub_category_aid = models.ForeignKey('ModelSubCategory', models.DO_NOTHING, db_column='sub_category_aid', blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'Business_Metric_Dept'




class BusinessMetricMaster(models.Model):
    bm_aid = models.AutoField(db_column='BM_AID',primary_key=True)  # Field name made lowercase.
    bm_label = models.CharField(db_column='BM_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    bm_description = models.CharField(db_column='BM_Description', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    bm_status = models.IntegerField(db_column='BM_status', blank=True, null=True)  # Field name made lowercase.
    bm_is_global = models.IntegerField(db_column='BM_Is_Global', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', blank=True, null=True)  # Field name made lowercase.
    updated_by = models.IntegerField(db_column='Updated_by', blank=True, null=True)  # Field name made lowercase.
    updated_on = models.DateTimeField(db_column='Updated_on', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Business_Metric_Master'


class BussKpiMonitoringSetup(models.Model):
    mdl_id = models.CharField(db_column='Mdl_Id', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    aid = models.AutoField(db_column='AID',primary_key=True)  # Field name made lowercase.
    # metric = models.IntegerField(db_column='Metric', blank=True, null=True)  # Field name made lowercase.
    metric = models.ForeignKey('BusinessMetricMaster', models.DO_NOTHING, db_column='Metric', blank=True, null=True)
    metric_value_type = models.CharField(db_column='Metric_Value_Type', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    threshold = models.FloatField(db_column='Threshold', blank=True, null=True)  # Field name made lowercase.
    warning = models.FloatField(db_column='Warning', blank=True, null=True)  # Field name made lowercase.
    frequency = models.IntegerField(db_column='Frequency', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_On', blank=True, null=True)  # Field name made lowercase.
    updated_by = models.IntegerField(db_column='Updated_by', blank=True, null=True)  # Field name made lowercase.
    updated_on = models.DateTimeField(db_column='Updated_On', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Buss_KPI_Monitoring_Setup'


class BussKpiMonitoringSetupTemp(models.Model):
    mdl_id = models.CharField(db_column='Mdl_Id', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    aid = models.AutoField(db_column='AID',primary_key=True)  # Field name made lowercase.
    # metric = models.IntegerField(db_column='Metric', blank=True, null=True)  # Field name made lowercase.
    metric = models.ForeignKey('BusinessMetricMaster', models.DO_NOTHING, db_column='Metric', blank=True, null=True)
    metric_value_type = models.CharField(db_column='Metric_Value_Type', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    threshold = models.FloatField(db_column='Threshold', blank=True, null=True)  # Field name made lowercase.
    warning = models.FloatField(db_column='Warning', blank=True, null=True)  # Field name made lowercase.
    frequency = models.IntegerField(db_column='Frequency', blank=True, null=True)  # Field name made lowercase.
    mo_approval = models.IntegerField(db_column='MO_Approval', blank=True, null=True)  # Field name made lowercase.
    mo_approval_on = models.DateTimeField(db_column='MO_Approval_On', blank=True, null=True)  # Field name made lowercase.
    mrm_approval = models.IntegerField(db_column='MRM_Approval', blank=True, null=True)  # Field name made lowercase.
    mrm_approval_on = models.DateTimeField(db_column='MRM_Approval_On', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_On', blank=True, null=True)  # Field name made lowercase.
    updated_by = models.IntegerField(db_column='Updated_by', blank=True, null=True)  # Field name made lowercase.
    updated_on = models.DateTimeField(db_column='Updated_On', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Buss_KPI_Monitoring_Setup_temp'

class DataMetricMaster(models.Model):
    data_aid = models.AutoField(db_column='Data_AID',primary_key=True)  # Field name made lowercase.
    data_label = models.CharField(db_column='Data_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    data_description = models.CharField(db_column='Data_Description', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    data_status = models.IntegerField(db_column='Data_status', blank=True, null=True)  # Field name made lowercase.
    data_is_global = models.IntegerField(db_column='Data_Is_Global', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', blank=True, null=True)  # Field name made lowercase.
    updated_by = models.IntegerField(db_column='Updated_by', blank=True, null=True)  # Field name made lowercase.
    updated_on = models.DateTimeField(db_column='Updated_on', blank=True, null=True)  # Field name made lowercase.
    data_types = models.CharField(db_column='Data_Types', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Data_Metric_Master'

class DataMonitoringSetup(models.Model):
    mdl_id = models.CharField(db_column='Mdl_Id', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    aid = models.AutoField(db_column='AID',primary_key=True)  # Field name made lowercase.
    feature = models.CharField(db_column='Feature', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    # metric = models.IntegerField(db_column='Metric', blank=True, null=True)  # Field name made lowercase.
    metric = models.ForeignKey('DataMetricMaster', models.DO_NOTHING, db_column='Metric', blank=True, null=True)
    threshold = models.FloatField(db_column='Threshold', blank=True, null=True)  # Field name made lowercase.
    warning = models.FloatField(db_column='Warning', blank=True, null=True)  # Field name made lowercase.
    frequency = models.IntegerField(db_column='Frequency', blank=True, null=True)  # Field name made lowercase.
    mo_approval = models.IntegerField(db_column='MO_Approval', blank=True, null=True)  # Field name made lowercase.
    mo_approval_on = models.DateTimeField(db_column='MO_Approval_On', blank=True, null=True)  # Field name made lowercase.
    mrm_approval = models.IntegerField(db_column='MRM_Approval', blank=True, null=True)  # Field name made lowercase.
    mrm_approval_on = models.DateTimeField(db_column='MRM_Approval_On', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_On', blank=True, null=True)  # Field name made lowercase.
    updated_by = models.IntegerField(db_column='Updated_by', blank=True, null=True)  # Field name made lowercase.
    updated_on = models.DateTimeField(db_column='Updated_On', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Data_Monitoring_Setup'

class DataMonitoringSetupTemp(models.Model):
    mdl_id = models.CharField(db_column='Mdl_Id', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    aid = models.AutoField(db_column='AID',primary_key=True)  # Field name made lowercase.
    feature = models.CharField(db_column='Feature', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    # metric = models.IntegerField(db_column='Metric', blank=True, null=True)  # Field name made lowercase.
    metric = models.ForeignKey('DataMetricMaster', models.DO_NOTHING, db_column='Metric', blank=True, null=True)
    threshold = models.FloatField(db_column='Threshold', blank=True, null=True)  # Field name made lowercase.
    warning = models.FloatField(db_column='Warning', blank=True, null=True)  # Field name made lowercase.
    frequency = models.IntegerField(db_column='Frequency', blank=True, null=True)  # Field name made lowercase.
    mo_approval = models.IntegerField(db_column='MO_Approval', blank=True, null=True)  # Field name made lowercase.
    mo_approval_on = models.DateTimeField(db_column='MO_Approval_On',default=datetime.now(), blank=True, null=True)  # Field name made lowercase.
    mrm_approval = models.IntegerField(db_column='MRM_Approval', blank=True, null=True)  # Field name made lowercase.
    mrm_approval_on = models.DateTimeField(db_column='MRM_Approval_On', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_On', default=datetime.now(),blank=True, null=True)  # Field name made lowercase.
    updated_by = models.IntegerField(db_column='Updated_by', blank=True, null=True)  # Field name made lowercase.
    updated_on = models.DateTimeField(db_column='Updated_On', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Data_Monitoring_Setup_temp'


        
class TempFeatureMatricSelection(models.Model):
    mdl_id = models.CharField(db_column='Mdl_Id', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    aid = models.AutoField(db_column='AID',primary_key=True)  # Field name made lowercase.
    feature = models.CharField(db_column='Feature', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    datamatrics = models.CharField(db_column='DataMatrics', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_On', blank=True, null=True)  # Field name made lowercase.
    updated_by = models.IntegerField(db_column='Updated_by', blank=True, null=True)  # Field name made lowercase.
    updated_on = models.DateTimeField(db_column='Updated_On', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Temp_Feature_Matric_Selection'

class DataMonitoringOverrideHistory(models.Model):
    aid = models.AutoField(db_column='AID',primary_key=True)  # Field name made lowercase.
    mdl_id = models.CharField(db_column='Mdl_ID', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    # metric = models.IntegerField(db_column='Metric', blank=True, null=True)  # Field name made lowercase.
    metric = models.ForeignKey('DataMetricMaster', models.DO_NOTHING, db_column='Metric', blank=True, null=True)
    feature = models.CharField(db_column='Feature', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    old_value = models.CharField(db_column='old_Value', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    new_value = models.CharField(db_column='New_Value', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mo_approval = models.IntegerField(db_column='MO_approval', blank=True, null=True)  # Field name made lowercase.
    mrm_approval = models.IntegerField(db_column='MRM_Approval', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_On', blank=True, null=True)  # Field name made lowercase.
    freq_idx = models.IntegerField(db_column='Freq_Idx', blank=True, null=True)  # Field name made lowercase.
    freq_val = models.DateTimeField(db_column='Freq_Val', blank=True, null=True)  # Field name made lowercase.
    mo_approved_on = models.DateTimeField(db_column='MO_Approved_On', blank=True, null=True)  # Field name made lowercase.
    mrm_approved_on = models.DateTimeField(db_column='MRM_Approved_On', blank=True, null=True)  # Field name made lowercase.
    threshold = models.FloatField(db_column='Threshold', blank=True, null=True)  # Field name made lowercase.
    warning = models.FloatField(db_column='Warning', blank=True, null=True)  # Field name made lowercase.
    actual = models.FloatField(db_column='Actual', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Data_Monitoring_Override_History'

class DataMonitoringResultFileInfo(models.Model):
    aid = models.AutoField(db_column='AID',primary_key=True)  # Field name made lowercase.
    mdl_id = models.CharField(db_column='Mdl_ID', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    file_nm = models.CharField(db_column='file_Nm', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', blank=True, null=True)  # Field name made lowercase.
    freq_idx = models.IntegerField(blank=True, null=True)
    freq_val = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Data_Monitoring_Result_file_info'

# Reports Models
class RptSectionMaster(models.Model):
    rpt_section_aid = models.AutoField(db_column='Rpt_section_AID',primary_key=True)  # Field name made lowercase.
    rpt_section_text = models.CharField(db_column='Rpt_section_text', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    rpt_section_description = models.CharField(db_column='Rpt_section_Description', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on',default=datetime.now() ,blank=True, null=True)  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'RPT_Section_Master'

class RptSubSectionMaster(models.Model):
    rpt_sub_section_aid = models.AutoField(db_column='Rpt_Sub_section_AID',primary_key=True)  # Field name made lowercase.
    rpt_section_aid = models.IntegerField(db_column='Rpt_section_AID', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_section_text = models.CharField(db_column='Rpt_Sub_section_text', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_section_description = models.CharField(db_column='Rpt_Sub_section_Description', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', default=datetime.now(),blank=True, null=True)  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RPT_Sub_Section_Master'


class RptSubSubSectionMaster(models.Model):
    rpt_sub_sub_section_aid = models.AutoField(db_column='Rpt_Sub_Sub_section_AID',primary_key=True)  # Field name made lowercase.
    rpt_section_aid = models.IntegerField(db_column='Rpt_section_AID', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_section_aid = models.IntegerField(db_column='Rpt_Sub_section_AID', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_sub_section_text = models.CharField(db_column='Rpt_Sub_Sub_section_text', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_sub_section_description = models.CharField(db_column='Rpt_Sub_Sub_section_Description', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', default=datetime.now() ,blank=True, null=True)  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RPT_Sub_Sub_Section_Master'


class ReportTemplate(models.Model):
    report_template_aid = models.AutoField(db_column='Report_Template_AID',primary_key=True)  # Field name made lowercase.
    template_name = models.CharField(db_column='Template_Name', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    department = models.IntegerField(db_column='Department', blank=True, null=True)  # Field name made lowercase.
    rpt_section_aid = models.IntegerField(db_column='Rpt_section_AID', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_section_aid = models.IntegerField(db_column='Rpt_Sub_section_AID', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_sub_section_aid = models.IntegerField(db_column='Rpt_Sub_Sub_section_AID', blank=True, null=True)  # Field name made lowercase.
    index_section = models.IntegerField(db_column='Index_Section', blank=True, null=True)  # Field name made lowercase.
    index_sub_section = models.IntegerField(db_column='Index_Sub_Section', blank=True, null=True)  # Field name made lowercase.
    index_sub_sub_section = models.IntegerField(db_column='Index_Sub_Sub_Section', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', default=datetime.now(),blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Report_Template'


class ReportTemplateTemp(models.Model):
    report_template_temp_aid = models.AutoField(db_column='Report_Template_Temp_AID',primary_key=True)  # Field name made lowercase.
    template_name = models.CharField(db_column='Template_Name', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    department = models.IntegerField(db_column='Department', blank=True, null=True)  # Field name made lowercase.
    rpt_section_aid = models.IntegerField(db_column='Rpt_section_AID', blank=True, null=True)  # Field name made lowercase.
    # rpt_section_aid = models.ForeignKey('RptSectionMaster', models.DO_NOTHING, db_column='Rpt_section_AID', blank=True, null=True)
    rpt_sub_section_aid = models.IntegerField(db_column='Rpt_Sub_section_AID', blank=True, null=True)  # Field name made lowercase.
    # rpt_sub_section_aid = models.ForeignKey('RptSubSectionMaster', models.DO_NOTHING, db_column='Rpt_Sub_section_AID', blank=True, null=True)
    rpt_sub_sub_section_aid = models.IntegerField(db_column='Rpt_Sub_Sub_section_AID', blank=True, null=True)  # Field name made lowercase.
    # rpt_sub_sub_section_aid = models.ForeignKey('RptSubSubSectionMaster', models.DO_NOTHING, db_column='Rpt_Sub_Sub_section_AID', blank=True, null=True)
    index_section = models.IntegerField(db_column='Index_Section', blank=True, null=True)  # Field name made lowercase.
    index_sub_section = models.IntegerField(db_column='Index_Sub_Section', blank=True, null=True)  # Field name made lowercase.
    index_sub_sub_section = models.IntegerField(db_column='Index_Sub_Sub_Section', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', default=datetime.now(),blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Report_Template_Temp'

class ReportContent(models.Model):
    report_content_aid = models.AutoField(db_column='Report_Content_AID',primary_key=True)  # Field name made lowercase.
    report_template_aid = models.IntegerField(db_column='Report_Template_AID', blank=True, null=True)  # Field name made lowercase.
    template_name = models.CharField(db_column='Template_Name', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', default=datetime.now(),blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Report_Content'


class FindingValElements(models.Model):
    element_aid = models.AutoField(db_column='Element_AID', primary_key=True)  # Field name made lowercase.
    element_text = models.CharField(db_column='Element_text', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    element_description = models.CharField(db_column='Element_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    addedon = models.DateTimeField(db_column='Addedon', default=datetime.now(),blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Finding_val_elements'


class FindingsCategory(models.Model):
    category_aid = models.AutoField(db_column='Category_AID', primary_key=True)  # Field name made lowercase.
    category_text = models.CharField(db_column='Category_text', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    category_description = models.CharField(db_column='Category_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    addedon = models.DateTimeField(db_column='Addedon',default=datetime.now(),blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Findings_Category'

class ValidationFindings(models.Model):
    findings_aid = models.AutoField(db_column='Findings_AId',primary_key=True)  # Field name made lowercase.
    mdl_id = models.CharField(db_column='Mdl_Id', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    validation_element = models.IntegerField(db_column='Validation_element', blank=True, null=True)  # Field name made lowercase.
    category = models.IntegerField(db_column='Category', blank=True, null=True)  # Field name made lowercase.
    risk = models.IntegerField(db_column='Risk', blank=True, null=True)  # Field name made lowercase.
    risk_level = models.IntegerField(db_column='Risk_Level', blank=True, null=True)  # Field name made lowercase.
    finding_description = models.CharField(db_column='Finding_Description', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    response = models.CharField(db_column='Response', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    emailid = models.CharField(db_column='EmailId', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(db_column='Updated_by', blank=True, null=True)  # Field name made lowercase.
    updated_on = models.DateTimeField(db_column='Updated_on', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'validation_findings'

class FindingValSubElements(models.Model):
    element_sub_aid = models.AutoField(db_column='Element_Sub_AID', primary_key=True)  # Field name made lowercase.
    # element_aid = models.IntegerField(db_column='Element_AID', blank=True, null=True)  # Field name made lowercase.
    element_aid = models.ForeignKey('FindingValElements', models.DO_NOTHING, db_column='Element_AID', blank=True, null=True)
    element_text = models.CharField(db_column='Element_text', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    element_description = models.CharField(db_column='Element_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    addedon = models.DateTimeField(db_column='Addedon', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Finding_val_sub_elements'

class QuestionMaster(models.Model):
    question_aid = models.AutoField(db_column='Question_AID', primary_key=True)  # Field name made lowercase.
    question_label = models.CharField(db_column='Question_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    # section_aid = models.IntegerField(db_column='Section_AID')  # Field name made lowercase.
    section_aid = models.ForeignKey('QuestionSections', models.DO_NOTHING, db_column='Section_AID', blank=True, null=True)
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Question_Master'


class QuestionSections(models.Model):
    section_aid = models.AutoField(db_column='Section_AID', primary_key=True)  # Field name made lowercase.
    section_label = models.CharField(db_column='Section_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Question_Sections'

class ValidationRatingMaster(models.Model):
    validation_ratings_master_aid = models.AutoField(db_column='Validation_Ratings_Master_AID' ,primary_key=True)  # Field name made lowercase.
    validation_rating = models.CharField(db_column='Validation_Rating', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    severity = models.CharField(db_column='Severity', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    risk_type = models.CharField(db_column='Risk_Type', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    value = models.IntegerField(db_column='Value', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(blank=True, null=True)
    addedon = models.DateTimeField(blank=True, default=datetime.now(),null=True)

    class Meta:
        managed = False
        db_table = 'Validation_Rating_Master'

class ValidationRatingMasterTemp(models.Model):
    validation_ratings_master_temp_aid = models.AutoField(db_column='Validation_Ratings_Master_Temp_AID',primary_key=True)  # Field name made lowercase.
    validation_rating = models.CharField(db_column='Validation_Rating', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    severity = models.CharField(db_column='Severity', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    risk_type = models.CharField(db_column='Risk_Type', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    value = models.IntegerField(db_column='Value', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(blank=True, null=True)
    addedon = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Validation_Rating_Master_Temp'

class ValFindingsDiscussion(models.Model):
    val_find_aid = models.AutoField(db_column='val_find_AID', primary_key=True)  # Field name made lowercase.
    room_id = models.CharField(db_column='Room_id', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    addedby = models.IntegerField(blank=True, null=True)
    addedon = models.DateTimeField(blank=True, null=True,default=datetime.now())
    findings_id = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'val_findings_discussion'


class UserAccess(models.Model):
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    ua_add = models.IntegerField(db_column='UA_Add', blank=True, null=True)  # Field name made lowercase.
    ua_edit = models.IntegerField(db_column='UA_Edit', blank=True, null=True)  # Field name made lowercase.
    ua_delete = models.IntegerField(db_column='UA_Delete', blank=True, null=True)  # Field name made lowercase.
    ua_dept = models.IntegerField(db_column='UA_dept', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'User_Access'

class ReportTitleTemplate(models.Model):
    title_aid = models.AutoField(db_column='title_aid',primary_key=True)
    title_id = models.IntegerField(db_column='title_id',blank=True, null=True)
    title_or_heading = models.IntegerField(db_column='title_or_heading',blank=True, null=True)
    title_label = models.CharField(db_column='title_label',max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    added_by = models.IntegerField(db_column='added_by',blank=True, null=True)
    added_on = models.DateTimeField(db_column='added_on',blank=True, null=True)
    updated_by = models.IntegerField(db_column='updated_by',blank=True, null=True)
    updated_on = models.DateTimeField(db_column='updated_on',blank=True, null=True)
    template_name = models.CharField(db_column='template_name',max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    title_type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    title_placeholder = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    title_sort_idx = models.IntegerField(blank=True, null=True)
    fontsize = models.IntegerField(blank=True, null=True)
    alignment = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'report_title_template'

class ReportTemplateHeader(models.Model):
    report_template_header_aid = models.AutoField(db_column='Report_Template_Header_aid',primary_key=True)  # Field name made lowercase.
    report_template_name = models.CharField(db_column='Report_Template_Name', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    header_template_name = models.CharField(db_column='Header_Template_Name', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(blank=True, null=True)
    added_on = models.DateTimeField(blank=True, default=datetime.now(),null=True)

    class Meta:
        managed = False
        db_table = 'Report_Template_Header'

class ReportHeaderTitleContent(models.Model):
    report_header_title_content_aid = models.AutoField(db_column='Report_Header_Title_Content_aid',primary_key=True)  # Field name made lowercase.
    template_name = models.CharField(db_column='Template_Name', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    title_id = models.IntegerField(blank=True, null=True)
    header_or_title = models.IntegerField(db_column='Header_or_Title', blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    label = models.CharField(db_column='Label', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mdl_id = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    added_by = models.IntegerField(blank=True, null=True)
    added_on = models.DateTimeField(blank=True, null=True)
    title_placeholder = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    title_sort_idx = models.IntegerField(blank=True, null=True)
    fontsize = models.IntegerField(blank=True, null=True)
    alignment = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    title_type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Report_Header_Title_Content'




class VtUserComments(models.Model):
    mdl_id = models.CharField(db_column='Mdl_Id', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    utility = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    sub_utility = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    comment = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    added_by = models.IntegerField(blank=True, null=True)
    added_on = models.DateTimeField(blank=True, null=True)
    type_comment = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    destination = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'VT_User_Comments' 

class VtUserDiscussion(models.Model):
    comment_id = models.AutoField(db_column='Comment_id',primary_key=True)  # Field name made lowercase.
    mdl_id = models.CharField(db_column='Mdl_Id', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    utility = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    sub_utility = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    comment = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    added_by = models.IntegerField(blank=True, null=True)
    added_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'VT_User_Discussion'

class FlQuestionMaster(models.Model):
    question_aid = models.AutoField(db_column='Question_AID', primary_key=True)  # Field name made lowercase.
    question_label = models.CharField(db_column='Question_Label', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    section_type = models.IntegerField(db_column='Section_Type', blank=True, null=True)  # Field name made lowercase.
    section_aid = models.IntegerField(db_column='Section_AID')  # Field name made lowercase.
    sub_section_aid = models.IntegerField(db_column='Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    sub_sub_section_aid = models.IntegerField(db_column='Sub_Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    sub_sub_sub_section_aid = models.IntegerField(db_column='Sub_Sub_Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    sort_idx = models.IntegerField(db_column='Sort_Idx', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FL_Question_Master'

class FlSections(models.Model):
    section_aid = models.AutoField(db_column='Section_AID', primary_key=True)  # Field name made lowercase.
    section_type = models.IntegerField(db_column='Section_Type', blank=True, null=True)  # Field name made lowercase.
    section_label = models.CharField(db_column='Section_Label', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    section_description = models.TextField(db_column='Section_Description', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sort_idx = models.IntegerField(db_column='Sort_Idx', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FL_Sections'

class FlAllocation(models.Model):
    allocation_aid = models.AutoField(db_column='Allocation_Aid', primary_key=True)  # Field name made lowercase.
    review_id = models.CharField(db_column='Review_id', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    review_name = models.CharField(db_column='Review_Name', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    section_aid = models.IntegerField(db_column='Section_AID')  # Field name made lowercase.
    sub_section_aid = models.IntegerField(db_column='Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    sub_sub_section_aid = models.IntegerField(db_column='Sub_Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    sub_sub_sub_section_aid = models.IntegerField(db_column='Sub_Sub_Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    allocated_to = models.IntegerField(db_column='Allocated_to')  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    model_id = models.CharField(db_column='Model_Id', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FL_allocation'



class FlQuestionRatingData(models.Model):
    rating_id = models.AutoField(db_column='Rating_id', primary_key=True)  # Field name made lowercase.
    review_id = models.CharField(db_column='Review_id', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    question_aid = models.IntegerField(db_column='Question_AID')  # Field name made lowercase.
    rating_yes_no = models.CharField(db_column='Rating_Yes_NO', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    doc_yes_no = models.CharField(db_column='Doc_Yes_No', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.CharField(db_column='AddedBy', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    inherent_risk_rating = models.CharField(db_column='Inherent_Risk_Rating', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    control_effectiveness_ratings = models.CharField(db_column='Control_Effectiveness_Ratings', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    residual_ratings = models.CharField(db_column='Residual_Ratings', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    control_description = models.CharField(db_column='Control_description', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    override_residual_ratings = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    override_comments = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FL_Question_Rating_Data'


class FlQuestionRatingDataFinal(models.Model):
    rating_id = models.AutoField(db_column='Rating_id', primary_key=True)  # Field name made lowercase.
    review_id = models.CharField(db_column='Review_id', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    question_aid = models.IntegerField(db_column='Question_AID')  # Field name made lowercase.
    rating_yes_no = models.CharField(db_column='Rating_Yes_NO', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    doc_yes_no = models.CharField(db_column='Doc_Yes_No', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    inherent_risk_rating = models.CharField(db_column='Inherent_Risk_Rating', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    control_effectiveness_ratings = models.CharField(db_column='Control_Effectiveness_Ratings', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    residual_ratings = models.CharField(db_column='Residual_Ratings', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    control_description = models.CharField(db_column='Control_Description', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.CharField(db_column='AddedBy', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    override_residual_ratings = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    override_comments = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FL_Question_Rating_Data_Final'

class MappingDetails(models.Model):
    mapping_aid = models.AutoField(db_column='Mapping_AID', primary_key=True)  # Field name made lowercase.
    excel_fields = models.CharField(db_column='Excel_Fields', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    database_fields = models.CharField(db_column='Database_Fields', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    portfolio = models.CharField(db_column='Portfolio', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mapping_Details'

class FlMappingDetails(models.Model):
    mapping_aid = models.AutoField(db_column='Mapping_AID', primary_key=True)  # Field name made lowercase.
    excel_fields = models.CharField(db_column='Excel_Fields', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    database_fields = models.CharField(db_column='Database_Fields', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    portfolio = models.CharField(db_column='Portfolio', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FL_Mapping_Details'

class PerfMonitoringMappingDetails(models.Model):
    mapping_aid = models.AutoField(db_column='Mapping_AID', primary_key=True)  # Field name made lowercase.
    excel_fields = models.CharField(db_column='Excel_Fields', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    database_fields = models.CharField(db_column='Database_Fields', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    mdl_id = models.CharField(db_column='Mdl_id', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    datatype = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Perf_Monitoring_Mapping_Details'

class PerfMonitoringDatabaseFields(models.Model):
    field_1 = models.CharField(db_column='Field_1', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field_2 = models.CharField(db_column='Field_2', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field_3 = models.CharField(db_column='Field_3', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field_4 = models.CharField(db_column='Field_4', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field_5 = models.CharField(db_column='Field_5', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field_6 = models.CharField(db_column='Field_6', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field_7 = models.CharField(db_column='Field_7', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field_8 = models.CharField(db_column='Field_8', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field_9 = models.CharField(db_column='Field_9', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field_10 = models.CharField(db_column='Field_10', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field_11 = models.CharField(db_column='Field_11', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field_12 = models.CharField(db_column='Field_12', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field_13 = models.CharField(db_column='Field_13', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field_14 = models.CharField(db_column='Field_14', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field_15 = models.CharField(db_column='Field_15', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field_16 = models.CharField(db_column='Field_16', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field_17 = models.CharField(db_column='Field_17', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field_18 = models.CharField(db_column='Field_18', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field_19 = models.CharField(db_column='Field_19', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field_20 = models.CharField(db_column='Field_20', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    datatype = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    mdl_id = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Perf_Monitoring_Database_Fields'

class FieldDetails(models.Model):
    field_aid = models.AutoField(db_column='Field_AID', primary_key=True)  # Field name made lowercase.
    excel_fields = models.CharField(db_column='Excel_Fields', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    database_fields = models.CharField(db_column='Database_Fields', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    portfolio = models.CharField(db_column='Portfolio', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Field_Details'


class DatabaseFields(models.Model):
    fields_aid = models.AutoField(db_column='Fields_AID', primary_key=True)  # Field name made lowercase.
    field1 = models.CharField(db_column='Field1', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field2 = models.CharField(db_column='Field2', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field3 = models.CharField(db_column='Field3', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field4 = models.CharField(db_column='Field4', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field5 = models.CharField(db_column='Field5', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field6 = models.CharField(db_column='Field6', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field7 = models.CharField(db_column='Field7', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field8 = models.CharField(db_column='Field8', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field9 = models.CharField(db_column='Field9', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field10 = models.CharField(db_column='Field10', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field11 = models.CharField(db_column='Field11', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field12 = models.CharField(db_column='Field12', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field13 = models.CharField(db_column='Field13', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field14 = models.CharField(db_column='Field14', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field15 = models.CharField(db_column='Field15', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field16 = models.CharField(db_column='Field16', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field17 = models.CharField(db_column='Field17', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field18 = models.CharField(db_column='Field18', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field19 = models.CharField(db_column='Field19', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field20 = models.CharField(db_column='Field20', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field21 = models.CharField(db_column='Field21', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field22 = models.CharField(db_column='Field22', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field23 = models.CharField(db_column='Field23', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field24 = models.CharField(db_column='Field24', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field25 = models.CharField(db_column='Field25', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field26 = models.CharField(db_column='Field26', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field27 = models.CharField(db_column='Field27', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field28 = models.CharField(db_column='Field28', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field29 = models.CharField(db_column='Field29', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field30 = models.CharField(db_column='Field30', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field31 = models.CharField(db_column='Field31', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field32 = models.CharField(db_column='Field32', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field33 = models.CharField(db_column='Field33', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field34 = models.CharField(db_column='Field34', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field35 = models.CharField(db_column='Field35', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field36 = models.CharField(db_column='Field36', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field37 = models.CharField(db_column='Field37', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field38 = models.CharField(db_column='Field38', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field39 = models.CharField(db_column='Field39', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field40 = models.CharField(db_column='Field40', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field41 = models.CharField(db_column='Field41', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field42 = models.CharField(db_column='Field42', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field43 = models.CharField(db_column='Field43', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field44 = models.CharField(db_column='Field44', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field45 = models.CharField(db_column='Field45', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field46 = models.CharField(db_column='Field46', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field47 = models.CharField(db_column='Field47', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field48 = models.CharField(db_column='Field48', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field49 = models.CharField(db_column='Field49', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field50 = models.CharField(db_column='Field50', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Database_Fields'

class FieldDetails(models.Model):
    field_aid = models.AutoField(db_column='Field_AID', primary_key=True)  # Field name made lowercase.
    excel_fields = models.CharField(db_column='Excel_Fields', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    database_fields = models.CharField(db_column='Database_Fields', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    portfolio = models.CharField(db_column='Portfolio', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    datatypes = models.CharField(db_column='DataTypes', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Field_Details'

class ValueDetails(models.Model):
    value_aid = models.AutoField(db_column='Value_AID', primary_key=True)  # Field name made lowercase.
    database_fields = models.CharField(db_column='Database_Fields', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    value = models.CharField(db_column='Value', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    portfolio = models.CharField(db_column='Portfolio', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate',default=datetime.now(), blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Value_Details'

class Controllclassmaster(models.Model):
    controllclass_aid = models.AutoField(db_column='ControllClass_AID', primary_key=True)  # Field name made lowercase.
    label = models.CharField(db_column='Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', default=datetime.now(),blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ControllClassMaster'

class Riskmaster(models.Model):
    risk_aid = models.AutoField(db_column='Risk_AID', primary_key=True)  # Field name made lowercase.
    label = models.CharField(db_column='Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', default=datetime.now(),blank=True, null=True)  # Field name made lowercase.
    utility = models.CharField(db_column='Utility', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RiskMaster'

class RiskFactorDiscussion(models.Model):
    risk_factor_discussion_aid = models.AutoField(db_column='Risk_Factor_Discussion_AID',primary_key=True)  # Field name made lowercase.
    risk_id = models.IntegerField(db_column='Risk_ID', blank=True, null=True)  # Field name made lowercase.
    group_id = models.TextField(db_column='Group_Id', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    utility = models.CharField(db_column='Utility', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    portfolio = models.CharField(db_column='Portfolio', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Risk_Factor_Discussion'


class RiskFactorComments(models.Model):
    rrisk_factor_comments_aid = models.AutoField(db_column='RRisk_Factor_Comments_AID',primary_key=True)  # Field name made lowercase.
    risk_id = models.IntegerField(db_column='Risk_ID', blank=True, null=True)  # Field name made lowercase.
    utility = models.CharField(db_column='Utility', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    portfolio = models.CharField(db_column='Portfolio', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', default=datetime.now(),blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Risk_Factor_Comments'

class FlReportTemplate(models.Model):
    fl_report_template_aid = models.AutoField(db_column='FL_Report_Template_AID',primary_key=True)  # Field name made lowercase.
    template_name = models.CharField(db_column='Template_Name', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    department = models.IntegerField(db_column='Department', blank=True, null=True)  # Field name made lowercase.
    rpt_section_aid = models.IntegerField(db_column='Rpt_section_AID', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_section_aid = models.IntegerField(db_column='Rpt_Sub_section_AID', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_sub_section_aid = models.IntegerField(db_column='Rpt_Sub_Sub_section_AID', blank=True, null=True)  # Field name made lowercase.
    index_section = models.IntegerField(db_column='Index_Section', blank=True, null=True)  # Field name made lowercase.
    index_sub_section = models.IntegerField(db_column='Index_Sub_Section', blank=True, null=True)  # Field name made lowercase.
    index_sub_sub_section = models.IntegerField(db_column='Index_Sub_Sub_Section', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FL_Report_Template'


class FlReportContent(models.Model):
    fl_report_content_aid = models.AutoField(db_column='FL_Report_Content_AID',primary_key=True)  # Field name made lowercase.
    fl_report_template_aid = models.IntegerField(db_column='FL_Report_Template_AID', blank=True, null=True)  # Field name made lowercase.
    template_name = models.CharField(db_column='Template_Name', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FL_Report_Content'


class FlReportHeaderTableContent(models.Model):
    fl_report_header_table_content_aid = models.AutoField(db_column='FL_Report_Header_Table_Content_AID',primary_key=True)  # Field name made lowercase.
    template_name = models.CharField(db_column='Template_Name', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    title_id = models.IntegerField(blank=True, null=True)
    mdl_id = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    header_1 = models.CharField(db_column='Header_1', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    header_2 = models.CharField(db_column='Header_2', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    header_3 = models.CharField(db_column='Header_3', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    header_4 = models.CharField(db_column='Header_4', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    header_5 = models.CharField(db_column='Header_5', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(blank=True, null=True)
    added_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FL_Report_Header_Table_Content'


class FlReportHeaderTitleContent(models.Model):
    fl_report_header_title_content_aid = models.AutoField(db_column='FL_Report_Header_Title_Content_aid',primary_key=True)  # Field name made lowercase.
    template_name = models.CharField(db_column='Template_Name', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    title_id = models.IntegerField(blank=True, null=True)
    header_or_title = models.IntegerField(db_column='Header_or_Title', blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    label = models.CharField(db_column='Label', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mdl_id = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    added_by = models.IntegerField(blank=True, null=True)
    added_on = models.DateTimeField(blank=True, null=True)
    title_placeholder = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    title_sort_idx = models.IntegerField(blank=True, null=True)
    fontsize = models.IntegerField(blank=True, null=True)
    alignment = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    title_type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FL_Report_Header_Title_Content'


class FlReportTemplateHeader(models.Model):
    fl_report_template_header_aid = models.AutoField(db_column='FL_Report_Template_Header_aid',primary_key=True)  # Field name made lowercase.
    fl_report_template_name = models.CharField(db_column='FL_Report_Template_Name', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    header_template_name = models.CharField(db_column='Header_Template_Name', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(blank=True, null=True)
    added_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FL_Report_Template_Header'


class FlReportTemplateTemp(models.Model):
    fl_report_template_temp_aid = models.AutoField(db_column='FL_Report_Template_Temp_AID',primary_key=True)  # Field name made lowercase.
    template_name = models.CharField(db_column='Template_Name', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    department = models.IntegerField(db_column='Department', blank=True, null=True)  # Field name made lowercase.
    rpt_section_aid = models.IntegerField(db_column='Rpt_section_AID', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_section_aid = models.IntegerField(db_column='Rpt_Sub_section_AID', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_sub_section_aid = models.IntegerField(db_column='Rpt_Sub_Sub_section_AID', blank=True, null=True)  # Field name made lowercase.
    index_section = models.IntegerField(db_column='Index_Section', blank=True, null=True)  # Field name made lowercase.
    index_sub_section = models.IntegerField(db_column='Index_Sub_Section', blank=True, null=True)  # Field name made lowercase.
    index_sub_sub_section = models.IntegerField(db_column='Index_Sub_Sub_Section', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FL_Report_Template_Temp'


class FlReportTitleTemplate(models.Model):
    title_aid = models.AutoField(primary_key=True)
    title_id = models.IntegerField(blank=True, null=True)
    title_or_heading = models.IntegerField(blank=True, null=True)
    title_label = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    added_by = models.IntegerField(blank=True, null=True)
    added_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    template_name = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    title_type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    title_placeholder = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    title_sort_idx = models.IntegerField(blank=True, null=True)
    fontsize = models.IntegerField(blank=True, null=True)
    alignment = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    fill_color = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    font_color = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FL_Report_title_template'

class FlSetting(models.Model):
    fls_aid = models.AutoField(db_column='FLS_AID',primary_key=True)  # Field name made lowercase.
    fls_text = models.CharField(db_column='FLS_Text', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    fls_remarks = models.CharField(db_column='FLS_Remarks', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    fls_enddate = models.DateField(db_column='FLS_EndDate', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy')  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate',default=datetime.now())  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    publish = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FL_Setting'

class AssignmentRiskFactor(models.Model):
    assignment_risk_factor_aid = models.AutoField(db_column='Assignment_Risk_Factor_AID', primary_key=True)  # Field name made lowercase.
    risk_factor_label = models.CharField(db_column='Risk_Factor_Label', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    assign_to = models.IntegerField(db_column='Assign_to', blank=True, null=True)  # Field name made lowercase.
    end_date = models.DateField(db_column='End_Date', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    risk_aid = models.CharField(db_column='Risk_AID', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Assignment_Risk_Factor'

# Add Question
class QuestionAnswerMaster(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_text = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')  # This field type is a guess.
    answer_type = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    answer_text = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Question_Answer_Master'

class QuestionOtionsMaster(models.Model):
    question_otions_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(QuestionAnswerMaster, on_delete=models.CASCADE)
    question_option = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Question_Otions_Master'


class SubQuestionAnswerMaster(models.Model):
    sub_question_id = models.AutoField(primary_key=True)
    question_sub= models.ForeignKey('QuestionAnswerMaster', models.DO_NOTHING, db_column='question_id', blank=True, null=True)  # Field name made lowercase.
    sub_question_text = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')  # This field type is a guess.
    sub_question_type = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    sub_answer_text = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Sub_Question_Answer_Master'


class SubQuestionOtionsMaster(models.Model):
    sub_question_otions_id = models.AutoField(primary_key=True)
    sub_question = models.ForeignKey(SubQuestionAnswerMaster, on_delete=models.CASCADE)
    sub_question_option = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Sub_Question_Otions_Master'

class QuestionTableMaster(models.Model):
    question_table_id = models.AutoField(db_column='Question_Table_id', primary_key=True)  # Field name made lowercase.
    question_tab =  models.ForeignKey('QuestionAnswerMaster', models.DO_NOTHING, db_column='question_id', blank=True, null=True) 
    table_header = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')  # This field type is a guess.
    table_row = models.IntegerField()
    table_column = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Question_Table_Master'

class FlDataanalysisImages(models.Model):
    fl_dataanalysis_images_aid = models.AutoField(db_column='Fl_DataAnalysis_Images_AID',primary_key=True)  # Field name made lowercase.
    image_name = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    utility = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    chart_type = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    variable = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    department = models.IntegerField(blank=True, null=True)
    portfolio = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on',default=datetime.now(), blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Fl_DataAnalysis_Images'


class FlReportTitleComment(models.Model):
    fl_report_title_comment_aid = models.AutoField(db_column='Fl_Report_Title_Comment_AID',primary_key=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    portfolio = models.CharField(db_column='Portfolio', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    utility = models.CharField(db_column='Utility', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', default=datetime.now(),blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Fl_Report_Title_Comment'

class FlDataFileInfo(models.Model):
    fl_id = models.AutoField(db_column='fl_ID', primary_key=True)  # Field name made lowercase.
    type_file = models.CharField(db_column='Type_file', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.   
    department = models.CharField(db_column='Department', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    portfolio = models.CharField(db_column='Portfolio', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    uploaded_by = models.CharField(db_column='Uploaded_By', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    uploaded_on = models.DateTimeField(db_column='Uploaded_On', blank=True, null=True)  # Field name made lowercase.
    upload_file_name = models.CharField(db_column='upload_File_name', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'fl_data_File_Info'

class FlRawData(models.Model):
    fields_aid = models.AutoField(db_column='Fields_AID', primary_key=True)  # Field name made lowercase.
    record_identifier = models.CharField(db_column='Record_Identifier', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    legal_entity_identifier = models.CharField(db_column='Legal_Entity_Identifier', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    universal_loan_identifier_or_non_universal_loan_identifier = models.CharField(db_column='Universal_Loan_Identifier_or_Non_Universal_Loan_Identifier', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    application_date = models.CharField(db_column='Application_Date', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    loan_type = models.CharField(db_column='Loan_Type', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    loan_purpose = models.CharField(db_column='Loan_Purpose', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    preapproval = models.CharField(db_column='Preapproval', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    construction_method = models.CharField(db_column='Construction_Method', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    occupancy_type = models.CharField(db_column='Occupancy_Type', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    loan_amount = models.CharField(db_column='Loan_Amount', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    action_taken = models.CharField(db_column='Action_Taken', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    action_taken_date = models.CharField(db_column='Action_Taken_Date', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    street_address = models.CharField(db_column='Street Address', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    city = models.CharField(db_column='City', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    zip_code = models.CharField(db_column='ZIP_Code', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    county = models.CharField(db_column='County', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    census_tract = models.CharField(db_column='Census_Tract', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ethnicity_of_applicant_or_borrower_1 = models.CharField(db_column='Ethnicity_of_Applicant_or_Borrower_1', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ethnicity_of_applicant_or_borrower_2 = models.CharField(db_column='Ethnicity_of_Applicant_or_Borrower_2', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ethnicity_of_applicant_or_borrower_3 = models.CharField(db_column='Ethnicity_of_Applicant_or_Borrower_3', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ethnicity_of_applicant_or_borrower_4 = models.CharField(db_column='Ethnicity_of_Applicant_or_Borrower_4', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ethnicity_of_applicant_or_borrower_5 = models.CharField(db_column='Ethnicity_of_Applicant_or_Borrower_5', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ethnicity_of_applicant_or_borrower_free_form_text_field_for_other_hispanic_or_latino = models.CharField(db_column='Ethnicity_of_Applicant_or_Borrower_Free_Form_Text_Field_for_Other_Hispanic_or_Latino', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ethnicity_of_co_applicant_or_co_borrower_1 = models.CharField(db_column='Ethnicity_of_Co_Applicant_or_Co_Borrower_1', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ethnicity_of_co_applicant_or_co_borrower_2 = models.CharField(db_column='Ethnicity_of_Co_Applicant_or_Co_Borrower_2', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ethnicity_of_co_applicant_or_co_borrower_3 = models.CharField(db_column='Ethnicity_of_Co_Applicant_or_Co_Borrower_3', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ethnicity_of_co_applicant_or_co_borrower_4 = models.CharField(db_column='Ethnicity_of_Co_Applicant_or_Co_Borrower_4', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ethnicity_of_co_applicant_or_co_borrower_5 = models.CharField(db_column='Ethnicity_of_Co_Applicant_or_Co_Borrower_5', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ethnicity_of_co_applicant_or_co_borrower_free_form_text_field_for_other_hispanic_or_latino = models.CharField(db_column='Ethnicity_of_Co_Applicant_or_Co_Borrower_Free_Form_Text_Field_for_Other_Hispanic_or_Latino', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ethnicity_of_applicant_or_borrower_collected_on_the_basis_of_visual_observation_or_surname = models.CharField(db_column='Ethnicity of Applicant or Borrower Collected on the Basis of Visual Observation or Surname', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ethnicity_of_co_applicant_or_co_borrower_collected_on_the_basis_of_visual_observation_or_surname = models.CharField(db_column='Ethnicity_of_Co_Applicant_or_Co_Borrower_Collected_on_the_Basis_of_Visual_Observation_or_Surname', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    race_of_applicant_or_borrower_1 = models.CharField(db_column='Race_of_Applicant_or_Borrower_1', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    race_of_applicant_or_borrower_2 = models.CharField(db_column='Race_of_Applicant_or_Borrower_2', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    race_of_applicant_or_borrower_3 = models.CharField(db_column='Race_of_Applicant_or_Borrower_3', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    race_of_applicant_or_borrower_4 = models.CharField(db_column='Race_of_Applicant_or_Borrower_4', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    race_of_applicant_or_borrower_5 = models.CharField(db_column='Race_of_Applicant_or_Borrower_5', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    race_of_applicant_or_borrower_free_form_text_field_for_american_indian_or_alaska_native_enrolled_or_principal_tribe = models.CharField(db_column='Race_of_Applicant_or_Borrower_Free_Form_Text_Field_for_American_Indian_or_Alaska_Native_Enrolled_or_Principal_Tribe', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    race_of_applicant_or_borrower_free_form_text_field_for_other_asian = models.CharField(db_column='Race_of_Applicant_or_Borrower_Free_Form_Text_Field_for_Other_Asian', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    race_of_applicant_or_borrower_free_form_text_field_for_other_pacific_islander = models.CharField(db_column='Race_of_Applicant_or_Borrower_Free_Form_Text_Field_for_Other_Pacific_Islander', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    race_of_co_applicant_or_co_borrower_1 = models.CharField(db_column='Race_of_Co_Applicant_or_Co_Borrower_1', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    race_of_co_applicant_or_co_borrower_2 = models.CharField(db_column='Race_of_Co_Applicant_or_Co_Borrower_2', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    race_of_co_applicant_or_co_borrower_3 = models.CharField(db_column='Race_of_Co_Applicant_or_Co_Borrower_3', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    race_of_co_applicant_or_co_borrower_4 = models.CharField(db_column='Race_of_Co_Applicant_or_Co_Borrower_4', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    race_of_co_applicant_or_co_borrower_5 = models.CharField(db_column='Race_of_Co_Applicant_or_Co_Borrower_5', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    race_of_co_applicant_or_co_borrower_free_form_text_field_for_american_indian_or_alaska_native_enrolled_or_principal_tribe = models.CharField(db_column='Race_of_Co_Applicant_or_Co_Borrower_Free_Form_Text_Field_for_American_Indian_or_Alaska_Native_Enrolled_or_Principal_Tribe', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    race_of_co_applicant_or_co_borrower_free_form_text_field_for_other_asian = models.CharField(db_column='Race_of_Co_Applicant_or_Co_Borrower_Free_Form_Text_Field_for_Other_Asian', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    race_of_co_applicant_or_co_borrower_free_form_text_field_for_other_pacific_islander = models.CharField(db_column='Race_of_Co_Applicant_or_Co_Borrower_Free_Form_Text_Field_for_Other_Pacific_Islander', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    race_of_applicant_or_borrower_collected_on_the_basis_of_visual_observation_or_surname = models.CharField(db_column='Race_of_Applicant_or_Borrower_Collected_on_the_Basis_of_Visual_Observation_or_Surname', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    race_of_co_applicant_or_co_borrower_collected_on_the_basis_of_visual_observation_or_surname = models.CharField(db_column='Race_of_Co_Applicant_or_Co_Borrower_Collected_on_the_Basis_of_Visual_Observation_or_Surname', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sex_of_applicant_or_borrower = models.CharField(db_column='Sex_of_Applicant_or_Borrower', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sex_of_co_applicant_or_co_borrower = models.CharField(db_column='Sex_of_Co_Applicant_or_Co_Borrower', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sex_of_applicant_or_borrower_collected_on_the_basis_of_visual_observation_or_surname = models.CharField(db_column='Sex_of_Applicant_or_Borrower_Collected_on_the_Basis_of_Visual_Observation_or_Surname', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sex_of_co_applicant_or_co_borrower_collected_on_the_basis_of_visual_observation_or_surname = models.CharField(db_column='Sex_of_Co_Applicant_or_Co_Borrower_Collected_on_the_Basis_of_Visual_Observation_or_Surname', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    age_of_applicant_or_borrower = models.CharField(db_column='Age_of_Applicant_or_Borrower', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    age_of_co_applicant_or_co_borrower = models.CharField(db_column='Age of Co-Applicant or Co-Borrower', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    income = models.CharField(db_column='Income', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    type_of_purchaser = models.CharField(db_column='Type_of_Purchaser', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    rate_spread = models.CharField(db_column='Rate_Spread', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    hoepa_status = models.CharField(db_column='HOEPA_Status', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    lien_status = models.CharField(db_column='Lien_Status', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    credit_score_of_applicant_or_borrower = models.CharField(db_column='Credit_Score_of_Applicant_or_Borrower', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    credit_score_of_co_applicant_or_co_borrower = models.CharField(db_column='Credit_Score_of_Co_Applicant_or_Co_Borrower', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    applicant_or_borrower_name_and_version_of_credit_scoring_model = models.CharField(db_column='Applicant_or_Borrower_Name_and_Version_of_Credit_Scoring_Model', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    applicant_or_borrower_name_and_version_of_credit_scoring_model_conditional_free_form_text_field_for_code_8 = models.CharField(db_column='Applicant_or_Borrower_Name_and_Version_of_Credit_Scoring_Model_Conditional_Free_Form_Text_Field_for_Code_8', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    co_applicant_or_co_borrower_name_and_version_of_credit_scoring_model = models.CharField(db_column='Co_Applicant_or_Co_Borrower_Name_and_Version_of_Credit_Scoring_Model', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    co_applicant_or_co_borrower_name_and_version_of_credit_scoring_model_conditional_free_form_text_field_for_code_8 = models.CharField(db_column='Co_Applicant_or_Co_Borrower_Name_and_Version_of_Credit_Scoring_Model_Conditional_Free_Form_Text_Field_for_Code_8', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    reason_for_denial_1 = models.CharField(db_column='Reason_for_Denial_1', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    reason_for_denial_2 = models.CharField(db_column='Reason_for_Denial_2', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    reason_for_denial_3 = models.CharField(db_column='Reason_for_Denial_3', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    reason_for_denial_4 = models.CharField(db_column='Reason_for_Denial_4', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    reason_for_denial_conditional_free_form_text_field_for_code_9 = models.CharField(db_column='Reason_for_Denial_Conditional_Free_Form_Text_Field_for_Code_9', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    total_loan_costs = models.CharField(db_column='Total_Loan_Costs', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    total_points_and_fees = models.CharField(db_column='Total_Points_and_Fees', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    origination_charges = models.CharField(db_column='Origination_Charges', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    discount_points = models.CharField(db_column='Discount_Points', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    lender_credits = models.CharField(db_column='Lender_Credits', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    interest_rate = models.CharField(db_column='Interest_Rate', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    prepayment_penalty_term = models.CharField(db_column='Prepayment_Penalty_Term', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    debt_to_income_ratio = models.CharField(db_column='Debt_to_Income_Ratio', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    combined_loan_to_value_ratio = models.CharField(db_column='Combined_Loan_to_Value_Ratio', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    loan_term = models.CharField(db_column='Loan_Term', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    introductory_rate_period = models.CharField(db_column='Introductory_Rate_Period', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    balloon_payment = models.CharField(db_column='Balloon_Payment', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    interest_only_payments = models.CharField(db_column='Interest_Only_Payments', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    negative_amortization = models.CharField(db_column='Negative_Amortization', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    other_non_amortizing_features = models.CharField(db_column='Other_Non_Amortizing_Features', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    property_value = models.CharField(db_column='Property_Value', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    manufactured_home_secured_property_type = models.CharField(db_column='Manufactured_Home_Secured_Property_Type', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    manufactured_home_land_property_interest = models.CharField(db_column='Manufactured_Home_Land_Property_Interest', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    total_units = models.CharField(db_column='Total_Units', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    multifamily_affordable_units = models.CharField(db_column='Multifamily_Affordable_Units', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    submission_of_application = models.CharField(db_column='Submission_of_Application', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    initially_payable_to_your_institution = models.CharField(db_column='Initially_Payable_to_Your_Institution', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mortgage_loan_originator_nmlsr_identifier = models.CharField(db_column='Mortgage_Loan_Originator_NMLSR_Identifier', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    automated_underwriting_system_1 = models.CharField(db_column='Automated_Underwriting_System_1', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    automated_underwriting_system_2 = models.CharField(db_column='Automated_Underwriting_System_2', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    automated_underwriting_system_3 = models.CharField(db_column='Automated_Underwriting_System_3', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    automated_underwriting_system_4 = models.CharField(db_column='Automated_Underwriting_System_4', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    automated_underwriting_system_5 = models.CharField(db_column='Automated_Underwriting_System_5', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    automated_underwriting_system_conditional_free_form_text_field_for_code_5 = models.CharField(db_column='Automated_Underwriting_System_Conditional_Free_Form_Text_Field_for_Code_5', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    automated_underwriting_system_result_1 = models.CharField(db_column='Automated_Underwriting_System_Result_1', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    automated_underwriting_system_result_2 = models.CharField(db_column='Automated_Underwriting_System_Result_2', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    automated_underwriting_system_result_3 = models.CharField(db_column='Automated_Underwriting_System_Result_3', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    automated_underwriting_system_result_4 = models.CharField(db_column='Automated_Underwriting_System_Result_4', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    automated_underwriting_system_result_5 = models.CharField(db_column='Automated_Underwriting_System_Result_5', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    automated_underwriting_system_result_conditional_free_form_text_field_for_code_16 = models.CharField(db_column='Automated_Underwriting_System_Result_Conditional_Free_Form_Text_Field_for_Code_16', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    reverse_mortgage = models.CharField(db_column='Reverse_Mortgage', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    open_end_line_of_credit = models.CharField(db_column='Open_End_Line_of_Credit', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    business_or_commercial_purpose = models.CharField(db_column='Business_or_Commercial_Purpose', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', default=12,blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate',default=datetime.now(), blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FL_RAW_DATA'

class InherentRiskRating(models.Model):
    inherent_risk_rating_aid = models.AutoField(db_column='Inherent_Risk_Rating_AID', primary_key=True)  # Field name made lowercase.
    ratings = models.CharField(db_column='Ratings', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_On', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Inherent_Risk_Rating'


class ControlEffectivenessRating(models.Model):
    control_effectiveness_rating_aid = models.AutoField(db_column='Control_Effectiveness_Rating_AID', primary_key=True)  # Field name made lowercase.
    ratings = models.CharField(db_column='Ratings', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_On', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Control_Effectiveness_Rating'


class ResidualRating(models.Model):
    residual_rating_aid = models.AutoField(db_column='Residual_Rating_AID', primary_key=True)  # Field name made lowercase.
    ratings = models.CharField(db_column='Ratings', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_On', default=datetime.now(),blank=True, null=True)  # Field name made lowercase.
    inherent_risk_rating = models.CharField(db_column='Inherent_risk_rating', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    control_effectiveness_rating = models.CharField(db_column='Control_effectiveness_rating', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Residual_Rating'

class FlRptSectionMaster(models.Model):
    fl_rpt_section_aid = models.AutoField(db_column='FL_Rpt_section_AID',primary_key=True)  # Field name made lowercase.
    rpt_section_text = models.CharField(db_column='Rpt_section_text', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    rpt_section_description = models.CharField(db_column='Rpt_section_Description', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on',default=datetime.now(), blank=True, null=True)  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FL_RPT_Section_Master'


class FlReportTitleTemplate(models.Model):
    title_aid = models.AutoField(primary_key=True)
    title_id = models.IntegerField(blank=True, null=True)
    title_or_heading = models.IntegerField(blank=True, null=True)
    title_label = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    added_by = models.IntegerField(blank=True, null=True)
    added_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    template_name = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    title_type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    title_placeholder = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    title_sort_idx = models.IntegerField(blank=True, null=True)
    fontsize = models.IntegerField(blank=True, null=True)
    alignment = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    fill_color = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    font_color = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FL_Report_title_template'


class FlRptSubSectionMaster(models.Model):
    fl_rpt_sub_section_aid = models.AutoField(db_column='FL_Rpt_Sub_section_AID',primary_key=True)  # Field name made lowercase.
    rpt_section_aid = models.IntegerField(db_column='Rpt_section_AID', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_section_text = models.CharField(db_column='Rpt_Sub_section_text', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_section_description = models.CharField(db_column='Rpt_Sub_section_Description', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', default=datetime.now(),blank=True, null=True)  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FL_RPT_Sub_Section_Master'

class FlRptSubSubSectionMaster(models.Model):
    fl_rpt_sub_sub_section_aid = models.AutoField(db_column='FL_Rpt_Sub_Sub_section_AID',primary_key=True)  # Field name made lowercase.
    rpt_section_aid = models.IntegerField(db_column='Rpt_section_AID', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_section_aid = models.IntegerField(db_column='Rpt_Sub_section_AID', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_sub_section_text = models.CharField(db_column='Rpt_Sub_Sub_section_text', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_sub_section_description = models.CharField(db_column='Rpt_Sub_Sub_section_Description', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on',default=datetime.now(), blank=True, null=True)  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FL_RPT_Sub_Sub_Section_Master'

class IcqControlEffectivenessRating(models.Model):
    icq_control_effectiveness_rating_aid = models.AutoField(db_column='ICQ_Control_Effectiveness_Rating_AID', primary_key=True)  # Field name made lowercase.
    ratings = models.CharField(db_column='Ratings', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_On', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ICQ_Control_Effectiveness_Rating'


class IcqInherentRiskRating(models.Model):
    icq_inherent_risk_rating_aid = models.AutoField(db_column='ICQ_Inherent_Risk_Rating_AID', primary_key=True)  # Field name made lowercase.
    ratings = models.CharField(db_column='Ratings', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_On', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ICQ_Inherent_Risk_Rating'


class IcqResidualRating(models.Model):
    icq_residual_rating_aid = models.AutoField(db_column='ICQ_Residual_Rating_AID', primary_key=True)  # Field name made lowercase.
    ratings = models.CharField(db_column='Ratings', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_On', blank=True, null=True)  # Field name made lowercase.
    inherent_risk_rating = models.CharField(db_column='Inherent_risk_rating', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    control_effectiveness_rating = models.CharField(db_column='Control_effectiveness_rating', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ICQ_Residual_Rating'


class IcqQuestionRatingData(models.Model):
    rating_id = models.AutoField(db_column='Rating_id', primary_key=True)  # Field name made lowercase.
    review_id = models.CharField(db_column='Review_id', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    question_aid = models.IntegerField(db_column='Question_AID')  # Field name made lowercase.
    rating_yes_no = models.CharField(db_column='Rating_Yes_NO', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    doc_yes_no = models.CharField(db_column='Doc_Yes_No', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.CharField(db_column='AddedBy', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    inherent_risk_rating = models.CharField(db_column='Inherent_Risk_Rating', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    control_effectiveness_ratings = models.CharField(db_column='Control_Effectiveness_Ratings', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    residual_ratings = models.CharField(db_column='Residual_Ratings', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    control_description = models.CharField(db_column='Control_description', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    override_residual_ratings = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    override_comments = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ICQ_Question_Rating_Data'

class IcqQuestionRatingDataFinal(models.Model):
    rating_id = models.AutoField(db_column='Rating_id', primary_key=True)  # Field name made lowercase.
    review_id = models.CharField(db_column='Review_id', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    question_aid = models.IntegerField(db_column='Question_AID')  # Field name made lowercase.
    rating_yes_no = models.CharField(db_column='Rating_Yes_NO', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    doc_yes_no = models.CharField(db_column='Doc_Yes_No', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.CharField(db_column='AddedBy', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    inherent_risk_rating = models.CharField(db_column='Inherent_Risk_Rating', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    control_effectiveness_ratings = models.CharField(db_column='Control_Effectiveness_Ratings', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    residual_ratings = models.CharField(db_column='Residual_Ratings', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    control_description = models.CharField(db_column='Control_description', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    override_residual_ratings = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    override_comments = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ICQ_Question_Rating_Data_Final'

class UdaapInherentRiskRating(models.Model):
    udaap_inherent_risk_rating_aid = models.AutoField(db_column='Udaap_Inherent_Risk_Rating_AID', primary_key=True)  # Field name made lowercase.
    ratings = models.CharField(db_column='Ratings', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_On', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Udaap_Inherent_Risk_Rating'


class UdaapControlEffectivenessRating(models.Model):
    udaap_control_effectiveness_rating_aid = models.AutoField(db_column='Udaap_Control_Effectiveness_Rating_AID', primary_key=True)  # Field name made lowercase.
    ratings = models.CharField(db_column='Ratings', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_On', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Udaap_Control_Effectiveness_Rating'


class UdaapResidualRating(models.Model):
    udaap_residual_rating_aid = models.AutoField(db_column='Udaap_Residual_Rating_AID', primary_key=True)  # Field name made lowercase.
    ratings = models.CharField(db_column='Ratings', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_On', blank=True, null=True)  # Field name made lowercase.
    inherent_risk_rating = models.CharField(db_column='Inherent_risk_rating', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    control_effectiveness_rating = models.CharField(db_column='Control_effectiveness_rating', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Udaap_Residual_Rating'


class UdaapQuestionRatingData(models.Model):
    rating_id = models.AutoField(db_column='Rating_id', primary_key=True)  # Field name made lowercase.
    review_id = models.CharField(db_column='Review_id', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    question_aid = models.IntegerField(db_column='Question_AID')  # Field name made lowercase.
    rating_yes_no = models.CharField(db_column='Rating_Yes_NO', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    doc_yes_no = models.CharField(db_column='Doc_Yes_No', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.CharField(db_column='AddedBy', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    inherent_risk_rating = models.CharField(db_column='Inherent_Risk_Rating', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    control_effectiveness_ratings = models.CharField(db_column='Control_Effectiveness_Ratings', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    residual_ratings = models.CharField(db_column='Residual_Ratings', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    control_description = models.CharField(db_column='Control_description', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    override_residual_ratings = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    override_comments = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Udaap_Question_Rating_Data'


class UdaapQuestionRatingDataFinal(models.Model):
    rating_id = models.AutoField(db_column='Rating_id', primary_key=True)  # Field name made lowercase.
    review_id = models.CharField(db_column='Review_id', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    question_aid = models.IntegerField(db_column='Question_AID')  # Field name made lowercase.
    rating_yes_no = models.CharField(db_column='Rating_Yes_NO', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    doc_yes_no = models.CharField(db_column='Doc_Yes_No', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    inherent_risk_rating = models.CharField(db_column='Inherent_Risk_Rating', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    control_effectiveness_ratings = models.CharField(db_column='Control_Effectiveness_Ratings', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    residual_ratings = models.CharField(db_column='Residual_Ratings', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    control_description = models.CharField(db_column='Control_Description', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.CharField(db_column='AddedBy', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    override_residual_ratings = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    override_comments = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Udaap_Question_Rating_Data_Final'

class UdaapQuestionMaster(models.Model):
    question_aid = models.AutoField(db_column='Question_AID', primary_key=True)  # Field name made lowercase.
    question_label = models.CharField(db_column='Question_Label', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    section_type = models.IntegerField(db_column='Section_Type', blank=True, null=True)  # Field name made lowercase.
    section_aid = models.IntegerField(db_column='Section_AID')  # Field name made lowercase.
    sub_section_aid = models.IntegerField(db_column='Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    sub_sub_section_aid = models.IntegerField(db_column='Sub_Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    sub_sub_sub_section_aid = models.IntegerField(db_column='Sub_Sub_Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    sort_idx = models.IntegerField(db_column='Sort_Idx', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Udaap_Question_Master'

class UdaapSections(models.Model):
    section_aid = models.AutoField(db_column='Section_AID', primary_key=True)  # Field name made lowercase.
    section_type = models.IntegerField(db_column='Section_Type', blank=True, null=True)  # Field name made lowercase.
    section_label = models.CharField(db_column='Section_Label', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', default=datetime.now(),blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    section_description = models.TextField(db_column='Section_Description', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sort_idx = models.IntegerField(db_column='Sort_Idx', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Udaap_Sections'


class UdaapSubSections(models.Model):
    sub_section_aid = models.AutoField(db_column='Sub_Section_AID', primary_key=True)  # Field name made lowercase.
    sub_section_type = models.IntegerField(db_column='Sub_Section_Type', blank=True, null=True)  # Field name made lowercase.
    sub_section_label = models.CharField(db_column='Sub_Section_Label', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    section_aid = models.IntegerField(db_column='Section_AID')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    sub_section_description = models.CharField(db_column='Sub_Section_Description', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sort_idx = models.IntegerField(db_column='Sort_Idx', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Udaap_Sub_Sections'


class UdaapSubSubSections(models.Model):
    sub_sub_section_aid = models.AutoField(db_column='Sub_Sub_Section_AID', primary_key=True)  # Field name made lowercase.
    sub_sub_section_type = models.IntegerField(db_column='Sub_Sub_Section_Type', blank=True, null=True)  # Field name made lowercase.
    sub_sub_section_label = models.CharField(db_column='Sub_Sub_Section_Label', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    sub_section_aid = models.IntegerField(db_column='Sub_Section_AID')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    sub_sub_section_description = models.CharField(db_column='Sub_Sub_Section_Description', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sort_idx = models.IntegerField(db_column='Sort_Idx', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Udaap_Sub_Sub_Sections'


class UdaapSubSubSubSections(models.Model):
    sub_sub_sub_section_aid = models.AutoField(db_column='Sub_Sub_Sub_Section_AID', primary_key=True)  # Field name made lowercase.
    sub_sub_sub_section_label = models.CharField(db_column='Sub_Sub_Sub_Section_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    sub_sub_section_aid = models.IntegerField(db_column='Sub_Sub_Section_AID')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    sub_sub_sub_section_description = models.CharField(db_column='Sub_Sub_Sub_Section_Description', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Udaap_Sub_Sub_Sub_Sections'

class UdaapSetting(models.Model):
    fls_aid = models.AutoField(db_column='FLS_AID',primary_key=True)  # Field name made lowercase.
    fls_text = models.CharField(db_column='FLS_Text', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    fls_remarks = models.CharField(db_column='FLS_Remarks', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    fls_enddate = models.DateField(db_column='FLS_EndDate', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy')  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate')  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    publish = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Udaap_Setting'

class UdaapQuestionRatingAllocation(models.Model):
    allocation_aid = models.AutoField(db_column='Allocation_Aid', primary_key=True)  # Field name made lowercase.
    review_id = models.CharField(db_column='Review_id', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    review_name = models.CharField(db_column='Review_Name', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    section_aid = models.IntegerField(db_column='Section_AID')  # Field name made lowercase.
    sub_section_aid = models.IntegerField(db_column='Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    sub_sub_section_aid = models.IntegerField(db_column='Sub_Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    sub_sub_sub_section_aid = models.IntegerField(db_column='Sub_Sub_Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    allocated_to = models.IntegerField(db_column='Allocated_to')  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    model_id = models.CharField(db_column='Model_Id', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Udaap_Question_Rating_Allocation'

class FlPoliciesProcedureDocuments(models.Model):
    mdl_id = models.CharField(db_column='Mdl_Id', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mdl_doc_id = models.AutoField(db_column='Mdl_Doc_Id',primary_key=True)  # Field name made lowercase.
    mdl_doc_type = models.CharField(db_column='Mdl_Doc_Type', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mdl_doc_name = models.CharField(db_column='Mdl_Doc_Name', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', default=datetime.now(),blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    department = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    portfolio = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FL_Policies_Procedure_Documents'

class ModelCategory(models.Model):
    category_aid = models.AutoField(db_column='Category_AID', primary_key=True)  # Field name made lowercase.
    category_label = models.CharField(db_column='Category_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    category_description = models.CharField(db_column='Category_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Model_Category'


class ModelSubCategory(models.Model):
    sub_category_aid = models.AutoField(db_column='Sub_Category_AID', primary_key=True)  # Field name made lowercase.
    sub_category_label = models.CharField(db_column='Sub_Category_Label', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sub_category_description = models.CharField(db_column='Sub_Category_Description', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.CharField(db_column='AddedBy', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    category_aid = models.ForeignKey('ModelCategory', models.DO_NOTHING, db_column='Category_AID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Model_Sub_Category'

class MdlDocuments(models.Model):
    mdl_id = models.CharField(db_column='Mdl_Id', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    mdl_doc_id = models.AutoField(db_column='Mdl_Doc_Id',primary_key=True)  # Field name made lowercase.
    mdl_doc_type = models.CharField(db_column='Mdl_Doc_Type', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    mdl_doc_name = models.CharField(db_column='Mdl_Doc_Name', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mdl_Documents'
        
class ValidationPlanning(models.Model):
    validation_planning_aid = models.AutoField(db_column='Validation_Planning_AID', primary_key=True)  # Field name made lowercase.
    mdl_id = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    validation_period = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    validation_scope = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    validator = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    internal_validator = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    external_validator = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    projected_start_date = models.DateTimeField(blank=True, null=True)
    projected_end_date = models.DateTimeField(blank=True, null=True)
    revised_end_date = models.DateTimeField(blank=True, null=True)
    previous_total_fees = models.IntegerField(db_column='Previous_total_fees', blank=True, null=True)  # Field name made lowercase.
    estimated_total_fees = models.IntegerField(blank=True, null=True)
    actual_total_fees = models.IntegerField(blank=True, null=True)
    comment = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    response = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    validation_status = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    validation_progress = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'validation_planning'

class NextValidationPlanning(models.Model):
    next_validation_planning_aid = models.AutoField(db_column='Next_Validation_Planning_AID', primary_key=True)  # Field name made lowercase.
    mdl_id = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    validation_period = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    validation_scope = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    validator = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    internal_validator = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    external_validator = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    projected_start_date = models.DateTimeField(blank=True, null=True)
    projected_end_date = models.DateTimeField(blank=True, null=True)
    revised_end_date = models.DateTimeField(blank=True, null=True)
    previous_total_fees = models.IntegerField(db_column='Previous_total_fees', blank=True, null=True)  # Field name made lowercase.
    estimated_total_fees = models.IntegerField(blank=True, null=True)
    actual_total_fees = models.IntegerField(blank=True, null=True)
    validation_status = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    validation_progress = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    comment = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    response = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Next_Validation_Planning'


class ValPeriodMst(models.Model):
    # id = models.AutoField(db_column='id', primary_key=True)  # Field name made lowercase.
    val_period = models.IntegerField(db_column='Val_Period', primary_key=True,blank=True)  # Field name made lowercase.
    val_period_start_dt = models.DateTimeField(db_column='Val_Period_Start_Dt', blank=True, null=True)  # Field name made lowercase.
    remark = models.TextField(db_column='Remark', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_By', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Val_Period_Mst'

class ValFrequencyMst(models.Model):
    mdl_risk = models.CharField(db_column='Mdl_Risk', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    val_frequency = models.IntegerField(db_column='Val_Frequency', blank=True,primary_key=True)  # Field name made lowercase.
    remark = models.TextField(db_column='Remark', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_By', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Val_Frequency_Mst'

class IcqSetting(models.Model):
    icqs_aid = models.AutoField(db_column='ICQS_AID',primary_key=True)  # Field name made lowercase.
    icqs_text = models.CharField(db_column='ICQS_Text', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    icqs_remarks = models.CharField(db_column='ICQS_Remarks', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    icqs_enddate = models.DateField(db_column='ICQS_EndDate', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy')  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate')  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    publish = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ICQ_Setting'


class IcqSectionComments(models.Model):
    response_id = models.AutoField(primary_key=True)
    section_id = models.IntegerField(blank=True, null=True)
    # section_id = models.ForeignKey(IcqSections, models.DO_NOTHING, db_column='Section_AID',blank=True, null=True) 
    comments = models.TextField(db_column='Comments', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.CharField(db_column='AddedBy', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    cycle_id = models.IntegerField(blank=True, null=True)
    # cycle_id = models.ForeignKey(IcqSetting, models.DO_NOTHING, db_column='icqs_aid',blank=True, null=True) 

    class Meta:
        managed = False
        # db_table = 'Icq_section_comments'

class IcqReportContent(models.Model):
    icq_report_content_aid = models.AutoField(db_column='ICQ_Report_Content_AID',primary_key=True)  # Field name made lowercase.
    icq_section_id = models.IntegerField(db_column='ICQ_Section_ID', blank=True, null=True)  # Field name made lowercase.
    icq_cycle_id = models.IntegerField(db_column='ICQ_Cycle_ID', blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ICQ_Report_Content'

###---------------------Ashok models-------------------------------###

class UserQuesQuestionMaster(models.Model):
    question_aid = models.AutoField(db_column='Question_AID', primary_key=True)  # Field name made lowercase.
    question_label = models.CharField(db_column='Question_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    section_aid = models.IntegerField(db_column='Section_AID')  # Field name made lowercase.
    sub_section_aid = models.IntegerField(db_column='Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    sub_sub_section_aid = models.IntegerField(db_column='Sub_Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    sub_sub_sub_section_aid = models.IntegerField(db_column='Sub_Sub_Sub_Section_AID', blank=True, null=True)  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    question_seq = models.IntegerField(db_column='Question_seq', blank=True, null=True) 

    class Meta:
        managed = False
        db_table = 'User_Question_Ques_Master'


class Notificationschedule(models.Model):
    alert_type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    frequency = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    time = models.TimeField()
    day_of_week = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    date_of_month = models.SmallIntegerField(blank=True, null=True)
    notify_days_before = models.SmallIntegerField()
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'NotificationSchedule'



class DashboardComments(models.Model):
    uid = models.IntegerField()
    pane = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    section = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    field_name = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    comment = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dashboard_Comments'
        
#added on 11.04.25 ends


class ModelGovernanceCommittee(models.Model):
    mgc_id = models.AutoField(db_column='MGC_Id', primary_key=True)  # Field name made lowercase.
    user_id = models.IntegerField()
    added_by = models.IntegerField()
    added_on = models.DateField()

    class Meta:
        managed = False
        db_table = 'Model_Governance_Committee'

class ModelChangeReqData(models.Model):
    request_id = models.CharField(db_column='Request_ID',primary_key=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    request_date = models.DateTimeField(db_column='Request_Date', blank=True, null=True)  # Field name made lowercase.
    request_initiator = models.IntegerField(db_column='Request_Initiator', blank=True, null=True)  # Field name made lowercase.
    mdl_nm = models.CharField(db_column='Mdl_Nm', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mdl_id = models.CharField(db_column='Mdl_Id', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mdl_owner = models.CharField(db_column='Mdl_Owner', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mdl_last_validation = models.DateTimeField(db_column='Mdl_Last_Validation', blank=True, null=True)  # Field name made lowercase.
    desc_change_change_type = models.CharField(db_column='Desc_Change_Change_type', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    desc_change_detailed_desc = models.TextField(db_column='Desc_Change_Detailed_Desc', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    desc_change_rationale_for_change = models.TextField(db_column='Desc_Change_Rationale_for_Change', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    desc_change_intended_benefits = models.TextField(db_column='Desc_Change_Intended_Benefits', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    impact_n_risk_assmnt_impac_on_model = models.TextField(db_column='Impact_n_Risk_Assmnt_Impac_on_Model', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    impact_n_risk_assmnt_risk_level_of_change = models.IntegerField(db_column='Impact_n_Risk_Assmnt_Risk_Level_of_Change', blank=True, null=True)  # Field name made lowercase.
    impact_n_risk_assmnt_potential_risks = models.TextField(db_column='Impact_n_Risk_Assmnt_Potential_Risks', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    impact_n_risk_assmnt_affected_sys_n_processes = models.TextField(db_column='Impact_n_Risk_Assmnt_Affected_Sys_n_Processes', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    implementation_and_testing_implementation_plan_summary = models.TextField(db_column='Implementation_and_Testing_Implementation_Plan_Summary', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    implementation_and_testing_testing_plan = models.TextField(db_column='Implementation_and_Testing_Testing_Plan', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    implementation_and_testing_back_out_plan = models.TextField(db_column='Implementation_and_Testing_Back_out_Plan', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.       
    implementation_and_testing_resources_required = models.TextField(db_column='Implementation_and_Testing_Resources_Required', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    review_n_approval_reviewers = models.TextField(db_column='Review_n_Approval_Reviewers', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    review_n_approval_review_date = models.DateTimeField(db_column='Review_n_Approval_Review_Date', blank=True, null=True)  # Field name made lowercase.
    review_n_approval_decision = models.IntegerField(db_column='Review_n_Approval_Decision', blank=True, null=True)  # Field name made lowercase.
    review_n_approval_conditions_comments = models.TextField(db_column='Review_n_Approval_Conditions_Comments', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    post_implementation_review_date_of_implementation = models.DateTimeField(db_column='Post_Implementation_Review_Date_of_Implementation', blank=True, null=True)  # Field name made lowercase.
    post_implementation_review_pir_date = models.DateTimeField(db_column='Post_Implementation_Review_PIR_Date', blank=True, null=True)  # Field name made lowercase.
    post_implementation_review_pir_findings = models.TextField(db_column='Post_Implementation_Review_PIR_Findings', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    post_implementation_review_validation_requirement = models.TextField(db_column='Post_Implementation_Review_Validation_Requirement', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    post_implementation_review_completion_sign_off = models.TextField(db_column='Post_Implementation_Review_Completion_Sign_off', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(blank=True, null=True)
    added_on = models.DateTimeField(blank=True, null=True)
    sign_off_by = models.IntegerField(db_column='Sign_Off_By', blank=True, null=True)  # Field name made lowercase.
    sign_off_on = models.DateTimeField(db_column='Sign_Off_On', blank=True, null=True)  # Field name made lowercase.
    update_by = models.IntegerField(db_column='Update_By', blank=True, null=True)  # Field name made lowercase.    updated_on = models.DateTimeField(db_column='Updated_On', blank=True, null=True)  # Field name made lowercase.
    request_sts = models.CharField(db_column='Request_Sts', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Model_change_req_data'
        

class IcqSectionDiscussion(models.Model):
    response_id = models.AutoField(primary_key=True)
    section_id = models.IntegerField(blank=True, null=True)
    comments = models.TextField(db_column='Comments', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.CharField(db_column='AddedBy', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    review_id = models.IntegerField(db_column='Review_id', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'Icq_section_Discussion'




class Emailsettings(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    senderaddress = models.CharField(db_column='SenderAddress', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    senderpassword = models.CharField(db_column='SenderPassword', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    smtpserver = models.CharField(db_column='SmtpServer', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    port = models.IntegerField(db_column='Port')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='UpdatedAt', blank=True, null=True)  # Field name made lowercase.
 
    class Meta:
        managed = False
        db_table = 'EmailSettings'











