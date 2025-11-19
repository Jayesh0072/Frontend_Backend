# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class IcqQuestionRatingDataFinal(models.Model):
    rating_id = models.AutoField(db_column='Rating_id', primary_key=True)  # Field name made lowercase.
    review_id = models.CharField(db_column='Review_id', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    question_aid = models.IntegerField(db_column='Question_AID')  # Field name made lowercase.
    rating_yes_no = models.CharField(db_column='Rating_Yes_NO', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    doc_yes_no = models.CharField(db_column='Doc_Yes_No', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addedby = models.CharField(db_column='AddedBy', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    adddate = models.DateTimeField(db_column='AddDate', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.
    inherent_risk_rating = models.CharField(db_column='Inherent_Risk_Rating', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    control_effectiveness_ratings = models.CharField(db_column='Control_Effectiveness_Ratings', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    residual_ratings = models.CharField(db_column='Residual_Ratings', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    control_description = models.CharField(db_column='Control_description', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ICQ_Question_Rating_Data_Final'
