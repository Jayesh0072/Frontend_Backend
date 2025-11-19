# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class IcqReportContent(models.Model):
    icq_report_content_aid = models.AutoField(db_column='ICQ_Report_Content_AID')  # Field name made lowercase.
    icq_section_id = models.IntegerField(db_column='ICQ_Section_ID', blank=True, null=True)  # Field name made lowercase.
    icq_cycle_id = models.IntegerField(db_column='ICQ_Cycle_ID', blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ICQ_Report_Content'
