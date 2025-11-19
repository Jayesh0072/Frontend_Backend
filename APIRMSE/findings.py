# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class FindingValSubElements(models.Model):
    element_sub_aid = models.AutoField(db_column='Element_Sub_AID', primary_key=True)  # Field name made lowercase.
    element_aid = models.IntegerField(db_column='Element_AID', blank=True, null=True)  # Field name made lowercase.
    element_text = models.CharField(db_column='Element_text', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    element_description = models.CharField(db_column='Element_Description', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    addedby = models.IntegerField(db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.
    addedon = models.DateTimeField(db_column='Addedon', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Finding_val_sub_elements'
