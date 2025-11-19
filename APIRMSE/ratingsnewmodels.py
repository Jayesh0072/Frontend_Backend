# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ResidualRating(models.Model):
    residual_rating_aid = models.AutoField(db_column='Residual_Rating_AID', primary_key=True)  # Field name made lowercase.
    ratings = models.CharField(db_column='Ratings', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_On', blank=True, null=True)  # Field name made lowercase.
    inherent_risk_rating = models.CharField(db_column='Inherent_risk_rating', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    control_effectiveness_rating = models.CharField(db_column='Control_effectiveness_rating', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Residual_Rating'
