# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class FlReportTitleComment(models.Model):
    fl_report_title_comment_aid = models.AutoField(db_column='Fl_Report_Title_Comment_AID')  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    portfolio = models.CharField(db_column='Portfolio', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    utility = models.CharField(db_column='Utility', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    commentl = models.CharField(db_column='Commentl', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Fl_Report_Title_Comment'



class Emailsettings(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    senderaddress = models.CharField(db_column='SenderAddress', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    senderpassword = models.CharField(db_column='SenderPassword', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    smtpserver = models.CharField(db_column='SmtpServer', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    port = models.IntegerField(db_column='Port')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='UpdatedAt', blank=True, null=True)  # Field name made lowercase.
 
    class Meta:
        managed = False
        db_table = 'EmailSettings'
