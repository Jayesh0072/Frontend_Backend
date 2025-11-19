# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ValidationFindings(models.Model):
    findings_aid = models.AutoField(db_column='Findings_AId')  # Field name made lowercase.
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
