from re import T
from django.db import models

# Create your models here.


# Create your models here.
class Users:     
	U_AID: str
	U_Name: str
	U_Password: str
	U_Email: str
	U_FName: str
	U_LName: str
	U_ProfilePic: str
	UC_AID: str
	U_Description: str
	U_Extra1: str
	U_Extra2: str
	ActiveStatus: str
	AddedBy: str


class UA:     
	li_1: str="none"
	li_2: str="none"
	li_3: str="none"
	li_4: str="none"
	li_5: str="none"
	li_6: str="none"
	li_7: str="none"
	li_8: str="none"
	li_9: str="none"
	li_10: str="none"
	li_11: str="none"
	li_12: str="none"
	li_13: str="none"
	li_vmtool: str="none"
	li_expmnt: str="none"
	li_sgnoffmodel: str="none"
	li_revmod: str="none"
	li_crrpt: str="none"
	li_reqdoc: str="none"
	reqmodinfo: str="none"
	li_upcod: str="none"
	li_updoc: str="none"
	li_reqcng: str="none"
	li_subdoc: str="none"
	li_reqval: str="none"
	li_idmod: str="none"
	li_task: str="none"
	li_todo: str="none"
	li_modinv: str="none"
	li_policies: str="none"
	li_contacts: str="none"
	li_profile: str="none"
	li_shdl: str="none"
	li_mrmadm: str="none"
	li_cr: str="none"
	li_qv: str="none"
	li_mrm: str="none"
	li_prdaprvl: str="none"
	li_knpol: str="none"

class Users(models.Model):
    u_aid = models.AutoField(db_column='U_AID', primary_key=True)  # Field name made lowercase.
    u_name = models.CharField(db_column='U_Name', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.        
    u_password = models.CharField(db_column='U_Password', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    u_email = models.CharField(db_column='U_Email', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    u_fname = models.CharField(db_column='U_FName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    u_lname = models.CharField(db_column='U_LName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    u_profilepic = models.CharField(db_column='U_ProfilePic', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    # uc_aid = models.IntegerField(db_column='UC_AID')  # Field name made lowercase.
    uc_aid = models.ForeignKey('UserCategory', models.DO_NOTHING, db_column='UC_AID', blank=True, null=True)
    u_description = models.CharField(db_column='U_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    u_extra1 = models.CharField(db_column='U_Extra1', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    u_extra2 = models.CharField(db_column='U_Extra2', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    dept_aid = models.IntegerField(db_column='Dept_AID', blank=True, null=True)  # Field name made lowercase.
    u_reportto = models.IntegerField(db_column='U_Reportto', blank=True, null=True)  # Field name made lowercase.
    is_logged_in = models.BooleanField(blank=True, null=True)
    token = models.CharField(db_column='Token', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    u_aid_backupfor = models.IntegerField(db_column='U_AID_BackUpFor', blank=True, null=True)  # Field name made lowercase.
    backup_aid = models.IntegerField(db_column='BackUp_AID', blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Users'

from datetime import datetime

class ValidationFindings(models.Model):
    findings_aid = models.AutoField(db_column='Findings_AId',primary_key=True)  # Field name made lowercase.
    mdl_id = models.CharField(db_column='Mdl_Id', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    validation_element = models.IntegerField(db_column='Validation_element', blank=True, null=True)  # Field name made lowercase.
    sub_validation_element = models.IntegerField(db_column='Validation_Sub_element',blank=True, null=True)
    category = models.IntegerField(db_column='Category', blank=True, null=True)  # Field name made lowercase.
    risk = models.IntegerField(db_column='Risk', blank=True, null=True)  # Field name made lowercase.
    risk_level = models.IntegerField(db_column='Risk_Level', blank=True, null=True)  # Field name made lowercase.
    finding_description = models.CharField(db_column='Finding_Description', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    response = models.CharField(db_column='Response', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    emailid = models.CharField(db_column='EmailId', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(blank=True, default=datetime.now(),null=True)
    updated_by = models.IntegerField(db_column='Updated_by', blank=True, null=True)  # Field name made lowercase.
    updated_on = models.DateTimeField(db_column='Updated_on', blank=True, null=True)  # Field name made lowercase.
    findings_id=models.CharField(db_column='Findings_ID', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase

    class Meta:
        managed = False
        db_table = 'validation_findings'  

class CSVData:
    months_as_customer: str
    age: str
    policy_number: str
    policy_bind_date: str
    policy_state: str
    policy_csl: str
    policy_deductable:   str
    policy_annual_premium:   float
    umbrella_limit:      str
    insured_zip: str
    insured_sex: str
    insured_education_level:   str
    insured_occupation:      str
    insured_hobbies:     str
    insured_relationship:    str
    capital_gains:       str
    capital_loss: str
    incident_date:       str
    incident_type:      str
    collision_type:    str
    incident_severity:   str
    authorities_contacted:   str
    incident_state:      str
    incident_city:       str
    incident_location:   str
    incident_hour_of_the_day:    str
    number_of_vehicles_involved: str
    property_damage: str
    bodily_injuries:     str
    witnesses: str
    police_report_available: str
    total_claim_amount:      str
    injury_claim: str
    property_claim:      str
    vehicle_claim:      str
    auto_make: str
    auto_model: str
    auto_year: str
    fraud_reported: str


class descData:
    colName: str
    count_val: str
    mean_val: str
    std_val: str
    min_val: str
    per25_val: str
    per50_val: str
    per75_val: str
    max_val: str


class missingDataList:
    colName: str
    dtType: str
    count_rows: int
    total_rows: int
    missing_rows: int


class lstColFreq:
    colName: str
    freqVal: dict
    total_rows: int
    missing_rows: int


class lstOutlierGrubbs:
    colName: str
    min_location: str
    max_location: str
    min_value: str
    max_value: str


class lstOutlieranomalies:
    colName: str
    lower_limit: str
    upper_limit: str
    arr_anomalies: str


class lstTestModelPerf:
    testName: str
    testResult: str
    testResult_dict: dict

class lstCnfrmSrc:
    colId: str
    colName: str
    srcName: str
    emailId: str
    reqResp: str
    dataQlt: str
    comment: str  
      
    
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
    completion_status = models.IntegerField(db_column='Completion_Status', blank=True, null=True)  # Field name made lowercase.
    approval_status = models.CharField(db_column='Approval_Status', max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    task_major_version=models.CharField(db_column='Task_Major_Ver', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    task_minor_version=models.CharField(db_column='Task_Minor_Ver', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    task_count=models.CharField(db_column='Task_Count', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercas
    link_id = models.CharField(db_column='Link_ID',max_length=300)  # Field name made lowercase.
    task_name = models.CharField(db_column='Task_Name', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True) 
    class Meta:
        managed = False
        db_table = 'Task_Registration'
    def __str__(self):
        return f"{self.department}"
    
class UserAccess(models.Model):
    ua_aid = models.AutoField(db_column='UA_AID', primary_key=True)  # Field name made lowercase.
    r_aid = models.IntegerField(db_column='R_AID')  # Field name made lowercase.
    ua_perm = models.CharField(db_column='UA_Perm', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    uc_aid = models.CharField(db_column='UC_AID', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
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
    title_aid = models.AutoField(db_column='title_aid', primary_key=True)
    title_id = models.IntegerField(blank=True, null=True)
    title_or_heading = models.IntegerField(blank=True, null=True)
    title_label = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    added_by = models.IntegerField(blank=True, null=True)
    added_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    template_name = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report_title_template' 


    
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
    is_dept_head = models.IntegerField(db_column='UC_Is_DeptHead', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'User_Category'

class Department(models.Model):
    dept_aid = models.AutoField(db_column='Dept_AID', primary_key=True)  # Field name made lowercase.
    dept_label = models.CharField(db_column='Dept_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    dept_description = models.CharField(db_column='Dept_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

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
    completion_status = models.IntegerField(db_column='Completion_Status', blank=True, null=True)  # Field name made lowercase.
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
    is_decomm = models.IntegerField(db_column='Is_Decommissioned')  

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

# class Users(models.Model):
#     u_aid = models.AutoField(db_column='U_AID', primary_key=True)  # Field name made lowercase.
#     u_name = models.CharField(db_column='U_Name', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
#     u_password = models.TextField(db_column='U_Password', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     u_email = models.CharField(db_column='U_Email', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     u_fname = models.CharField(db_column='U_FName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     u_lname = models.CharField(db_column='U_LName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     u_profilepic = models.CharField(db_column='U_ProfilePic', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     # uc_aid = models.IntegerField(db_column='UC_AID')  # Field name made lowercase.
#     uc_aid = models.ForeignKey('UserCategory', models.DO_NOTHING, db_column='UC_AID', blank=True, null=True)
#     u_description = models.CharField(db_column='U_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     u_extra1 = models.CharField(db_column='U_Extra1', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     u_extra2 = models.CharField(db_column='U_Extra2', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
#     addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
#     adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
#     updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
#     updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
#     dept_aid = models.IntegerField(db_column='Dept_AID', blank=True, null=True)  # Field name made lowercase.
#     u_reportto = models.IntegerField(db_column='U_Reportto', blank=True, null=True)  # Field name made lowercase.
#     U_AID_BackUpFor = models.IntegerField(db_column='U_AID_BackUpFor', blank=True, null=True)  # Field name made lowercase.
#     class Meta:
#         managed = False
#         db_table = 'Users'

class Department(models.Model):
    dept_aid = models.AutoField(db_column='Dept_AID', primary_key=True)  # Field name made lowercase.
    dept_label = models.CharField(db_column='Dept_Label', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    dept_description = models.CharField(db_column='Dept_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    is_mrm = models.IntegerField(db_column='Dept_IsMRM', blank=True, null=True) 
    class Meta:
        managed = False
        db_table = 'Department'


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
    # def __str__(self):
    #     return f"{self.sub_task_type_label}"

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
    txtPrdDt=models.DateTimeField(db_column='Prd_Dt', blank=True, null=True) 
    


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
    create_date = models.DateTimeField(db_column='Create_Date', blank=True, null=True)  # Field name made lowercase.

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

class TempMdlDependencies(models.Model):
    temp_mdl_dependencies_id = models.CharField(db_column='Temp_Mdl_Dependencies_ID', primary_key=True,max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    mdl_id = models.CharField(db_column='Mdl_Id', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    upstrmmdl = models.CharField(db_column='UpstrmMdl', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    dwstrmmdl = models.CharField(db_column='DwstrmMdl', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Temp_Mdl_Dependencies'

class TempMdlOverview(models.Model):
    temp_mdl_overview_id = models.CharField(db_column='Temp_Mdl_OverView_id', primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    mdl_id = models.CharField(db_column='Mdl_Id',max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
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
    is_submit = models.BooleanField(db_column='Is_submit', blank=True, null=True)  # Field name made lowercase.
    txtPrdDt=models.DateTimeField(db_column='Prd_Dt', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Temp_Mdl_OverView'

class TempMdlRelevantPersonnel(models.Model):
    mdl_id = models.CharField(db_column='Mdl_Id', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    u_type = models.CharField(db_column='U_Type', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    u_id = models.CharField(db_column='U_ID', max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Temp_Mdl_Relevant_personnel'

class TempMdlRisks(models.Model):
    temp_mdl_risks_id = models.CharField(db_column='Temp_Mdl_Risks_Id', primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    mdl_id = models.CharField(db_column='Mdl_Id', max_length=20,  db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
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
        db_table = 'Temp_Mdl_Risks'

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



class FlSubSections(models.Model):
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
        db_table = 'FL_Sub_Sections'



class FlSubSubSections(models.Model):
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
        db_table = 'FL_Sub_Sub_Sections'

class FlSubSubSubSections(models.Model):
    sub_sub_sub_section_aid = models.AutoField(db_column='Sub_Sub_Sub_Section_AID', primary_key=True)  # Field name made lowercase.
    sub_sub_sub_section_type = models.IntegerField(db_column='Sub_Sub_Sub_Section_Type', blank=True, null=True)  # Field name made lowercase.       
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
        db_table = 'FL_Sub_Sub_Sub_Sections'

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
