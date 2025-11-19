# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class FlReportTemplate(models.Model):
    fl_report_template_aid = models.AutoField(db_column='FL_Report_Template_AID')  # Field name made lowercase.
    template_name = models.CharField(db_column='Template_Name', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    department = models.IntegerField(db_column='Department', blank=True, null=True)  # Field name made lowercase.
    rpt_section_aid = models.IntegerField(db_column='Rpt_section_AID', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_section_aid = models.IntegerField(db_column='Rpt_Sub_section_AID', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_sub_section_aid = models.IntegerField(db_column='Rpt_Sub_Sub_section_AID', blank=True, null=True)  # Field name made lowercase.
    index_section = models.IntegerField(db_column='Index_Section', blank=True, null=True)  # Field name made lowercase.
    index_sub_section = models.IntegerField(db_column='Index_Sub_Section', blank=True, null=True)  # Field name made lowercase.
    index_sub_sub_section = models.IntegerField(db_column='Index_Sub_Sub_Section', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FL_Report_Template'


class FlReportContent(models.Model):
    fl_report_content_aid = models.AutoField(db_column='FL_Report_Content_AID')  # Field name made lowercase.
    fl_report_template_aid = models.IntegerField(db_column='FL_Report_Template_AID', blank=True, null=True)  # Field name made lowercase.
    template_name = models.CharField(db_column='Template_Name', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FL_Report_Content'


class FlReportHeaderTableContent(models.Model):
    fl_report_header_table_content_aid = models.AutoField(db_column='FL_Report_Header_Table_Content_AID')  # Field name made lowercase.
    template_name = models.CharField(db_column='Template_Name', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    title_id = models.IntegerField(blank=True, null=True)
    mdl_id = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    header_1 = models.CharField(db_column='Header_1', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    header_2 = models.CharField(db_column='Header_2', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    header_3 = models.CharField(db_column='Header_3', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    header_4 = models.CharField(db_column='Header_4', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    header_5 = models.CharField(db_column='Header_5', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(blank=True, null=True)
    added_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FL_Report_Header_Table_Content'


class FlReportHeaderTitleContent(models.Model):
    fl_report_header_title_content_aid = models.AutoField(db_column='FL_Report_Header_Title_Content_aid')  # Field name made lowercase.
    template_name = models.CharField(db_column='Template_Name', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    title_id = models.IntegerField(blank=True, null=True)
    header_or_title = models.IntegerField(db_column='Header_or_Title', blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    label = models.CharField(db_column='Label', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mdl_id = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    added_by = models.IntegerField(blank=True, null=True)
    added_on = models.DateTimeField(blank=True, null=True)
    title_placeholder = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    title_sort_idx = models.IntegerField(blank=True, null=True)
    fontsize = models.IntegerField(blank=True, null=True)
    alignment = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    title_type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FL_Report_Header_Title_Content'


class FlReportTemplateHeader(models.Model):
    fl_report_template_header_aid = models.AutoField(db_column='FL_Report_Template_Header_aid')  # Field name made lowercase.
    fl_report_template_name = models.CharField(db_column='FL_Report_Template_Name', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    header_template_name = models.CharField(db_column='Header_Template_Name', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(blank=True, null=True)
    added_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FL_Report_Template_Header'


class FlReportTemplateTemp(models.Model):
    fl_report_template_temp_aid = models.AutoField(db_column='FL_Report_Template_Temp_AID')  # Field name made lowercase.
    template_name = models.CharField(db_column='Template_Name', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    department = models.IntegerField(db_column='Department', blank=True, null=True)  # Field name made lowercase.
    rpt_section_aid = models.IntegerField(db_column='Rpt_section_AID', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_section_aid = models.IntegerField(db_column='Rpt_Sub_section_AID', blank=True, null=True)  # Field name made lowercase.
    rpt_sub_sub_section_aid = models.IntegerField(db_column='Rpt_Sub_Sub_section_AID', blank=True, null=True)  # Field name made lowercase.
    index_section = models.IntegerField(db_column='Index_Section', blank=True, null=True)  # Field name made lowercase.
    index_sub_section = models.IntegerField(db_column='Index_Sub_Section', blank=True, null=True)  # Field name made lowercase.
    index_sub_sub_section = models.IntegerField(db_column='Index_Sub_Sub_Section', blank=True, null=True)  # Field name made lowercase.
    added_by = models.IntegerField(db_column='Added_by', blank=True, null=True)  # Field name made lowercase.
    added_on = models.DateTimeField(db_column='Added_on', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FL_Report_Template_Temp'


class FlReportTitleTemplate(models.Model):
    title_aid = models.AutoField()
    title_id = models.IntegerField(blank=True, null=True)
    title_or_heading = models.IntegerField(blank=True, null=True)
    title_label = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    added_by = models.IntegerField(blank=True, null=True)
    added_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    template_name = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    title_type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    title_placeholder = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    title_sort_idx = models.IntegerField(blank=True, null=True)
    fontsize = models.IntegerField(blank=True, null=True)
    alignment = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    fill_color = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    font_color = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FL_Report_title_template'
