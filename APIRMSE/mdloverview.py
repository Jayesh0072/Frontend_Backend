# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class MdlOverview(models.Model):
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
