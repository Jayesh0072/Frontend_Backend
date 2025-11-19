# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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
