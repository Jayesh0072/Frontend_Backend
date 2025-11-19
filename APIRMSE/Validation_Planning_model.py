# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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
