# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class FlDataanalysisImages(models.Model):
    fl_dataanalysis_images_aid = models.AutoField(db_column='Fl_DataAnalysis_Images_AID')  # Field name made lowercase.
    image_name = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    utility = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    chart_type = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    variable = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    department = models.IntegerField(blank=True, null=True)
    portfolio = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Fl_DataAnalysis_Images'
