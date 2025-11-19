# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class FlRptSubSectionMaster(models.Model):
    fl_rpt_sub_section_aid = models.AutoField(db_column='FL_Rpt_Sub_section_AID')  # Field name made lowercase.
    rpt_section_aid = models.IntegerField(db_column='Rpt_section_AID', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_section_text = models.CharField(db_column='Rpt_Sub_section_text', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_section_description = models.CharField(db_column='Rpt_Sub_section_Description', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', blank=True, null=True)  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FL_RPT_Sub_Section_Master'


class FlRptSubSubSectionMaster(models.Model):
    fl_rpt_sub_sub_section_aid = models.AutoField(db_column='FL_Rpt_Sub_Sub_section_AID')  # Field name made lowercase.
    rpt_section_aid = models.IntegerField(db_column='Rpt_section_AID', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_section_aid = models.IntegerField(db_column='Rpt_Sub_section_AID', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_sub_section_text = models.CharField(db_column='Rpt_Sub_Sub_section_text', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_sub_section_description = models.CharField(db_column='Rpt_Sub_Sub_section_Description', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', blank=True, null=True)  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FL_RPT_Sub_Sub_Section_Master'
