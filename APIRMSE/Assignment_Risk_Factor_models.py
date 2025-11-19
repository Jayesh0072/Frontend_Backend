# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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
