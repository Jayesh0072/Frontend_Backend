# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class IcqSectionComments(models.Model):
    response_id = models.AutoField()
    section_id = models.IntegerField(blank=True, null=True)
    comments = models.TextField(db_column='Comments', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.CharField(db_column='AddedBy', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    cycle_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Icq_section_comments'


class IcqSetting(models.Model):
    icqs_aid = models.AutoField(db_column='ICQS_AID')  # Field name made lowercase.
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
