from django.shortcuts import render ,redirect
import traceback
import os 
from pathlib import Path
import json 
import pandas as pd
from django.http import JsonResponse
from django.core import serializers 
from django.core.files.storage import FileSystemStorage
from datetime import *
from django.template import RequestContext
import numpy as np
import shutil 
import requests
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework import generics, permissions, status,serializers
from .RegModel.registermodel import RegisterModel as Register 

from .Adm_Utils.Masters import MasterTbls
from .DAL.dboperations import dbops
from .models import Users,UA
from .UserInfo.user import UserInfo
from .Validation.validation import Validation
from .RMSE.RMSE import RMSEModel
objreg=Register()  
objmaster=MasterTbls()
objvalidation=Validation()
objdbops=dbops()
objrmse=RMSEModel() 
from .models import *

def getAPIURL():
    api_url=os.environ['API_URL']
    return api_url


def dashboard(request):
    print("check dashboard")
    try:  
        api_url=getAPIURL()+"save_comments_mdl_overview/"       
        data_to_save={ 
            'uid':request.session['uid']
            } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)         
        api_data_comments=response.json() 
        print("api_data_comments",api_data_comments)

        objreg=Register()
        request.session['canAdd']="0"
        ps=request.GET.get('ps','')
        #Get_User_Deatils 
        uc = request.session['utype']
        dept = request.session['dept']
        print("uc----------",uc)
        print("dept--------",dept)
        api_url = getAPIURL()+'Get_User_Deatils/' 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }       
        data_params={
            'uc':uc,
            'dept':dept 
        }
        response = requests.post(api_url, data= json.dumps(data_params),headers=header)         
        api_data=response.json()     
        dttbl=  pd.DataFrame.from_dict(api_data['ucdata'], orient='index') 
        
        if dttbl.empty == False:
            request.session['li_mrm']=dttbl[dttbl['r_label'] == 'Model Risk Management'].values[0][2]
            request.session['li_qv']=dttbl[dttbl['r_label'] =='Dashboard'].values[0][2] 
            request.session['li_modinv']=dttbl[dttbl['r_label'] =='Model Inventory'].values[0][2] 
            request.session['li_modtasks']=dttbl[dttbl['r_label'] =='Tasks'].values[0][2]  
            request.session['li_adduser']=dttbl[dttbl['r_label'] =='Dept Head'].values[0][2] 
            request.session['li_task']=dttbl[dttbl['r_label'] =='Tasks'].values[0][2]
            request.session['task_registration']=dttbl[dttbl['r_label'] =='Tasks'].values[0][2] 
            request.session['li_issuesReg']= dttbl[dttbl['r_label'] =='Issues'].values[0][2]  
            request.session['li_taskApprv']='block' 
            request.session['li_taskComplete']='block'
            request.session['li_issueComplete']='block'
            request.session['li_issueApprv']='block'
            request.session['li_icqqtn']=dttbl[dttbl['r_label'] =='ICQ'].values[0][2]   
            request.session['li_perfmntr']=dttbl[dttbl['r_label'] =='Performance Monitoring'].values[0][2]   
            if dttbl[dttbl['r_label'] =='Model Inventory'].values[0][3] == "rw":
                request.session['canAdd']="1" 

            if(str(objmaster.checkMRMHead(str(request.session['uid']))))=="1" or (str(objmaster.checkMRMMgr(str(request.session['uid']))))=="1" or (str(objmaster.checkMRMUser(str(request.session['uid']))))=="1":
                request.session['li_icqqtnfinal']='block'
                request.session['li_modval']='block'
                request.session['li_icqqtn']='none' 
                request.session['is_mrm_user']='Yes'
            else:
                request.session['li_icqqtnfinal']='none'
                request.session['li_modval']='none' 
                request.session['is_mrm_user']='No'
            if(str(objmaster.checkMRMHead(str(request.session['uid']))))=="1":
                 request.session['is_mrm']='Yes'
            else: 
                request.session['is_mrm']='No'

        del dttbl
        
        api_url=getAPIURL()+"dashboard/"
        
        data_to_save={'utype':request.session['utype'],
            'dept':request.session['dept'],
            'uid':request.session['uid'],
            'ulvl':request.session['ulvl'],
            'is_mrm':request.session['is_mrm'],
            'type':'Qtr',
            'issue_from_dt':'',
            'issue_to_dt':''
            } 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json() 
        print("API_data new-----------------",api_data)
        if(str(objmaster.isAutherized(request.session['ucaid'],"Dashboard")) =="0"): 
            return render(request, 'blank.html',{'actPage':'RMSE'}) 
        modelinfo=api_data['modelinfo']#objreg.getModelListByUSerid(request.session['uid'],str(request.session['ulvl']),'0')
        # modelriskcnt=api_data['modelriskcnt']#objreg.getModelRiskCntByUserid(request.session['uid'],str(request.session['ulvl'])) 
        # modelsrccnt=api_data['modelsrccnt']#objreg.getModelSrcCntByUserid('0',request.session['uid'])
       
        taskList=api_data['taskLst']#objreg.getTaskListByUSerid(request.session['uid'])
        issueList=api_data['issueList']#objreg.getIssueListByUserId(request.session['uid'])
        icqratings=api_data['icqratings']#objreg.isICQPublished() 
        if(icqratings=='-'):
            icq_exp="Experimentation"
            icqratings="0"
        else:
            icq_exp="Program Score"
        srcCnt= api_data['srcCnt']

        # colorArr=['info', 'info-300','warning-300','danger-300','success-300','primary']
        colorArr=['#0dcaf0', '#fd7e14','#ffc107','#dc3545','#198754','#0d6efd']
         
        cnt=api_data['mdlRiskCnt']
        toolCnt=api_data['toolCnt']
        modeltypes=api_data['modeltypes']
        issuesByQtrOrMonth= api_data['issuesByQtrOrMonth']
        findingsByElements=api_data['findingsByElements']
        findingsCntByCategory=api_data['findingsCntByCategory']
        #new code 
        # end_date = datetime.now()
        # start_date = end_date - timedelta(days=7)
        # last_7_days_records = ActivityTrail.objects.filter(added_on__range = (start_date, end_date)).distinct().order_by('-added_on')
        # # lst = activityinfo(last_7_days_records)
        # latest = last_7_days_records.values('refference_id').distinct()
        # print("latest",latest)
        lst = []
        irow=1 
        latest=api_data['activityData']
        for key,activity_obj in latest.items(): 
            # max_record = ActivityTrail.objects.filter(refference_id = activity_obj['refference_id']).last()
            dict={}
            activity_trigger = latest[key]['activity_trigger']
            refference_id = latest[key]['refference_id']
            
            
            dict['activity_trigger'] = activity_trigger
            dict['refference_id'] = refference_id
            dict['user'] = latest[key]['usernm'] 
            dict['date'] = latest[key]['add_dt']
            dict['time'] = latest[key]['add_time']
            dict['activity_details'] =latest[key]['activity_details']
            if irow== len(latest):
                dict['is_last']='Yes'
            else:
                dict['is_last']='No'
                irow+=1
            lst.append(dict)  
        mdl_cat=api_data['mdl_cat'] 
        request.session['overdueTasks']=api_data['overdueTasks'] 
        request.session['overdueIssues']=api_data['overdueIssues']
        valstscnt=api_data['valstscnt']
        mdlstscnt=api_data['mdlstscnt']  
        riskcnts=api_data['riskcnts']
        dashboardSetting=api_data['dashboardSetting']
        findingsByUpstreamMdl=api_data['findingsByUpstreamMdl']
        findingsCntByMdls=api_data['findingsCntByMdls']
        mdl_cat_data=[]
        mdl_cat_lbl=[]
        mdl_cat_color=[] 
        for key,obj in mdl_cat.items():
            print('obj' ,obj)
            mdl_cat_data.append(obj['cnt'])
            mdl_cat_color.append(obj['color'])
            mdl_cat_lbl.append(obj['Category_Label'])

        ##model types
        mdl_typ_data=[]
        mdl_typ_lbl=[]
        mdl_typ_color=[]
        for key,obj in modeltypes.items():
            print('obj' ,obj)
            mdl_typ_data.append(obj['cnt'])
            mdl_typ_color.append(obj['color'])
            mdl_typ_lbl.append(obj['Mdl_Type_Label'])

        ##mdl source
        mdl_src_data=[]
        mdl_src_lbl=['Internal','Legacy','Vendor']
        mdl_src_color=[]
        print("srcCnt",srcCnt)
        for obj in srcCnt:
            print('obj' ,obj)
            mdl_src_data.append(obj['value'])
            mdl_src_color.append(obj['itemStyle']['color'])
        print("mdl_src_data",mdl_src_data)
        print("mdl_src_color",mdl_src_color)
        print("mdl_src_lbl",mdl_src_lbl)

        ##mdl status
        mdl_sts_data=[]
        mdl_sts_lbl=[]
        mdl_sts_color=['#0dcaf0', '#fd7e14','#ffc107','#dc3545','#198754','#0d6efd']
        print("model status",mdlstscnt)
        
        for key,obj in mdlstscnt.items():
            print('obj' ,obj)
            mdl_sts_data.append(obj['cnt'])
            mdl_sts_lbl.append(obj['lbl'])

        print("mdl_sts_data",mdl_sts_data)
        print("mdl_sts_color",mdl_sts_color)
        print("mdl_sts_lbl",mdl_sts_lbl)

        ## validation status 
        print("validation status",valstscnt)
        val_sts_data=[]
        val_sts_lbl=[]
        val_sts_color=['#0dcaf0', '#fd7e14','#ffc107','#dc3545','#198754','#0d6efd']
        for key,obj in valstscnt.items():
            print('obj' ,obj)
            val_sts_data.append(obj['cnt'])
            val_sts_lbl.append(obj['lbl'])

        print("val_sts_data",val_sts_data)
        print("val_sts_color",val_sts_color)
        print("val_sts_lbl",val_sts_lbl)

        # plotdoughnut(mdl_cat_data,mdl_cat_lbl,mdl_cat_color,para='mdl_cat')   ##model cat
        # plotdoughnut(mdl_typ_data,mdl_typ_lbl,mdl_typ_color,para='mdl_type')   ##model type
        # plotdoughnut(mdl_src_data,mdl_src_lbl,mdl_typ_color,para='mdl_source')   ##model source
        # plotdoughnut(mdl_sts_data,mdl_sts_lbl,mdl_sts_color,para='mdl_status')   ##model status
        # plotdoughnut(val_sts_data,val_sts_lbl,val_sts_color,para='val_status')   ##Val status

        ##Bar chart
        ##Validation Rating

        arrvalrating= api_data['arrvalrating']
        print("arrvalrating",arrvalrating)
         
        val_rate_data=[]
        val_rate_lbl=['Fail', 'Needs Improvement','Satisfactory',  'None']
        val_rate_color=[]
        print("srcCnt",srcCnt)
        for obj in arrvalrating:
            print('obj' ,obj)
            val_rate_data.append(obj['value'])
            val_rate_color.append(obj['itemStyle']['color'])
        print("val_rate_data",val_rate_data)
        print("val_rate_color",val_rate_color)
        print("val_rate_lbl",val_rate_lbl)

        ##Model Risk Tier
        
        mdl_risk_tier_data=[]
        mdl_risk_tier_lbl=['High', 'Medium','Low',  'None']
        mdl_risk_tier_color=[]
        print("Model Risk Tier",cnt)
        for obj in cnt:
            print('obj' ,obj)
            mdl_risk_tier_data.append(obj['value'])
            mdl_risk_tier_color.append(obj['itemStyle']['color'])
        print("mdl_risk_tier_data",mdl_risk_tier_data)
        print("mdl_risk_tier_color",mdl_risk_tier_color)
        print("mdl_risk_tier_lbl",mdl_risk_tier_lbl)

        # bar_chart(val_rate_data,val_rate_lbl,val_rate_color,para='val_rate') ##Validation Rating
        # bar_chart(mdl_risk_tier_data,mdl_risk_tier_lbl,mdl_risk_tier_color,para='risk_tier') ##Model Risk Tier

        ## stacked bar chart
        print("riskcnts",riskcnts)
        data_stacked=riskcnts['data']
        labels=['High','Medium','Low','None']
        x_labels=['Intrinsic','Reliance','Materiality','None']
        colors_stacked=['#dc3545','#ffc107','#198754','gray']
        stacked_bar(data_stacked,labels,x_labels,colors_stacked,para='mdl_risk') ##model risk
        issuePriority=issuesByQtrOrMonth['data']
        chartSeries=issuesByQtrOrMonth['series']
        print("issuePriority",issuePriority)
        print("chartSeries",chartSeries)
        data_issue=issuePriority
        labels_issue=['High','Medium','Low']
        x_labels_issue=chartSeries
        colors_issue=['#dc3545','#ffc107','#198754']
        # stacked_bar(data_issue,labels_issue,x_labels_issue,colors_issue,para='issues') ##issue 

        a = stacked_bar(data_issue, labels_issue, x_labels_issue, colors_issue, para='issues')
        b = bar_chart(val_rate_data, val_rate_lbl, val_rate_color, para='val_rate')
        c = plotdoughnut(mdl_cat_data, mdl_cat_lbl, mdl_cat_color, para='mdl_cat')
        print("A",a)
        print("B",b)
        print("C",c)
        print("issueList",issueList)
        # generate_table_pdf(
        #     modelinfo,
        #     findingsByElements,
        #     findingsCntByCategory,
        #     findingsByUpstreamMdl,
        #     findingsCntByMdls,
        #     issueList,
        #     chart_paths=[a, b, c]   # new arg
        # )
        # generate_table_pdf()
        # generate_table_pdf(modelinfo,findingsByElements,findingsCntByCategory,findingsCntByMdls,findingsByUpstreamMdl)
        return render(request, 'dashboard_icon.html',{'icqratings':icqratings,'icq_exp':icq_exp,'modelinfo':modelinfo,'srcCnt':srcCnt,
                        'colorArr':colorArr,'issueCnt':len(issueList),'issueList':issueList,'issuePriority':issuesByQtrOrMonth['data'],'chartSeries':issuesByQtrOrMonth['series'],
                        'taskCnt':api_data['taskCnt'],'taskLst':taskList,'arrvalrating':api_data['arrvalrating'],
                        'toolCnt':toolCnt ,'findingsByElements':findingsByElements, 'modelttl':str(len(modelinfo)),'mdlRiskCnt':cnt,'findingsCntByCategory':findingsCntByCategory,
                        'modeltypes':modeltypes, 'actPage':'Quick View','activity_lst':lst,'mdl_cat':mdl_cat,'showOverdueModal':str(ps),
                        'valstscnt':valstscnt,'mdlstscnt':mdlstscnt,'riskcnts':riskcnts['data'],'issuecnt':api_data['issuecnt'],
                        'dashboardSetting':dashboardSetting,'findingsByUpstreamMdl':findingsByUpstreamMdl,'findingsCntByMdls':findingsCntByMdls,
                        'comments':api_data_comments})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
        error_saving(request,e)


from pathlib import Path
import matplotlib.pyplot as plt
import os
BASE_DIR = Path(__file__).resolve().parent.parent

def plotdoughnut(data, label, colors, para): 
    print("plotdoughnut", data, label, colors, para)

    

    # Custom function to display actual values instead of %
    def absolute_value(val):
        # val is the percentage, so we convert it back to the actual value
        total = sum(data)
        absolute = int(round(val/100.*total))
        return f"{absolute}"  # just value, no %

    # Pie chart
    plt.figure(figsize=(6,6))
    plt.pie(
        data, 
        colors=colors, 
        labels=label,
        autopct=absolute_value,   # <--- custom formatter here
        pctdistance=0.85
    )

    # draw circle for doughnut
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Set title based on para
    if para == "mdl_cat":
        chart_title = "Model Category"
    elif para == "mdl_type":
        chart_title = "Model Type"
    elif para == "mdl_source":
        chart_title = "Model Source"
    elif para == "mdl_status":
        chart_title = "Model Status"
    elif para == "val_status":
        chart_title = "Validation Status"
    else:
        chart_title = para  # fallback in case of new category

    plt.title(chart_title)

    # save to different files based on para
    filename = f"{chart_title}.png"
    save_path = os.path.join(BASE_DIR, "static", "media", filename)

    plt.savefig(save_path, bbox_inches="tight", dpi=150)
    plt.close()
    return save_path

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import os

def bar_chart(data, label, colors, para):
    print("bar_chart", data, label, colors, para)

    BASE_DIR = Path(__file__).resolve().parent.parent

    x = np.arange(len(label))   # positions for bars
    y = np.array(data)

    plt.figure(figsize=(8,6))
    bars = plt.bar(x, y, color=colors, width=0.6)

    # Add labels on top of bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2.,  # x center
            height + 0.5,                      # little above bar
            str(y[i]),                         # show actual value
            ha='center', va='bottom', fontsize=10
        )

    # Axis labels and title
    plt.xticks(x, label, rotation=30, ha="right")
    plt.ylim(0, max(y) * 1.15)

    if para == "val_rate":
        chart_title = "Validation Rating"
    elif para == "risk_tier":
        chart_title = "Model Risk Tier"
    else:
        chart_title = para

    plt.title(chart_title)

    # Save chart
    filename = f"{chart_title}.png"
    save_path = os.path.join(BASE_DIR, "static", "media", filename)

    plt.savefig(save_path, bbox_inches="tight", dpi=300)
    plt.close()
    return save_path

import pandas as pd
import matplotlib.pyplot as plt
import os


def stacked_bar(data, labels, x_labels, colors, para):

    print("stacked_bar", data, labels, x_labels, colors, para)

    # Pad rows to match x_labels length
    data = np.array([row + [0]*(len(x_labels)-len(row)) for row in data])

    N = len(x_labels)       # number of x-axis groups
    ind = np.arange(N)      # x locations
    width = 0.6             # bar width

    fig, ax = plt.subplots(figsize=(10, 7))

    # Stack bars
    bottoms = np.zeros(N)
    for row, lbl, color in zip(data, labels, colors):
        bars = ax.bar(ind, row, width, bottom=bottoms, label=lbl, color=color)

        # Add value labels on each bar
        for bar, value in zip(bars, row):
            if value > 0:  # only show non-zero
                ax.text(
                    bar.get_x() + bar.get_width()/2,
                    bar.get_y() + bar.get_height()/2,
                    str(value),
                    ha="center", va="center", fontsize=9, color="white", fontweight="bold"
                )

        bottoms += row

    if para == "mdl_risk":
        chart_title = "Model Risks"
    elif para == "issues":
        chart_title = "Issues"
    else:
        chart_title = para

    # Labels and formatting
    # ax.set_ylabel("Contribution")
    ax.set_title(chart_title)
    ax.set_xticks(ind)
    ax.set_xticklabels(x_labels, rotation=45)
    ax.legend()

    # Save
    filename = f"{para}.png"
    save_path = os.path.join(BASE_DIR, "static", "media", filename)
    plt.savefig(save_path, bbox_inches="tight", dpi=300)
    plt.close()
    return save_path

from django.conf import settings
import os, pathlib
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import landscape, A4
from fpdf import FPDF

from fpdf import FPDF
import os
from datetime import datetime
from django.conf import settings

# from fpdf.fonts import FontFace

# def build_table(pdf, title, data, headers=None, key_map=None):
#     # Section title
#     pdf.set_font("Helvetica", "B", 14)
#     pdf.cell(0, 10, title, ln=True)

#     # Normalize data
#     if isinstance(data, dict):
#         if all(isinstance(v, dict) for v in data.values()):
#             data = list(data.values())
#         else:
#             data = [data]

#     if not data:
#         pdf.set_font("Helvetica", "", 10)
#         pdf.cell(0, 10, "No data available", ln=True)
#         pdf.ln(5)
#         return

#     # Prepare rows
#     if headers and key_map:
#         rows = [headers] + [[str(row.get(k, "")) for k in key_map] for row in data]
#     else:
#         cols = list(data[0].keys())
#         rows = [cols] + [[str(row.get(k, "")) for k in cols] for row in data]

#     # --- Auto-fit column widths ---
#     page_width = pdf.epw
#     col_count = len(rows[0])
#     max_text_widths = [max(len(str(r[col_idx])) for r in rows) for col_idx in range(col_count)]
#     total_len = sum(max_text_widths)
#     col_widths = [(page_width * l / total_len) for l in max_text_widths]

#     # Styles
#     header_style = FontFace(emphasis="B", fill_color=(220, 220, 220))  # bold + gray fill
#     body_style = FontFace()
#     alt_row_style = FontFace(fill_color=(245, 245, 245))  # light gray alt rows

#     pdf.set_font("Helvetica", size=9)
#     with pdf.table(borders_layout="ALL", col_widths=col_widths) as table:
#         for row_idx, row_data in enumerate(rows):
#             row = table.row()
#             for datum in row_data:
#                 # Center numbers, left-align text
#                 align = "C" if datum.replace(".", "", 1).isdigit() else "L"

#                 if row_idx == 0:
#                     style = header_style
#                 elif row_idx % 2 == 0:
#                     style = alt_row_style
#                 else:
#                     style = body_style

#                 row.cell(datum, align=align, style=style)

# def generate_table_pdf(modelinfo, findingsByElements, findingsCntByCategory,
#                        findingsByUpstreamMdl, findingsCntByMdls,
#                        issueList=None, chart_paths=None):

#     pdf = FPDF(orientation="L", unit="mm", format="A4")
#     pdf.add_page()

#     # --- Model Info ---
#     if modelinfo:
#         headers = ["Model ID", "Primary Model Name", "Model Source", "Model Type", "Model Risk"]
#         key_map = ["Mdl_Id", "Prm_Name", "Mdl_Src_Label", "Mdl_Type_Label", "Mdl_Risk_Label"]
#         build_table(pdf, "Model Info", modelinfo, headers=headers, key_map=key_map)

#     # --- Issues ---
#     if issueList:
#         build_table(
#             pdf,
#             "Issue Info",
#             issueList,
#             headers=["Issue ID", "Priority", "Approval Status", "Issue Function", "Issue Type",
#                      "Completion Status", "End Date"],
#             key_map=["Issue_ID", "Issue_Priority_Label", "Issue_ApprovalStatus_Label",
#                      "Issue_Function_Label", "Issue_Type_label", "Completion_Status", "end_dt"]
#         )

#     # --- Findings ---
#     build_table(pdf, "Findings By Elements", findingsByElements)
#     build_table(pdf, "Findings Count By Category", findingsCntByCategory)
#     build_table(pdf, "Findings By Upstream Models", findingsByUpstreamMdl)
#     build_table(pdf, "Findings Count By Models", findingsCntByMdls)

#     # --- Charts ---
#     if chart_paths:
#         pdf.add_page()
#         pdf.set_font("Helvetica", "B", 14)
#         pdf.cell(0, 10, "Charts", ln=True)
#         for chart in chart_paths:
#             if os.path.exists(chart):
#                 pdf.image(chart, w=150)
#                 pdf.ln(10)

#     # --- Save File ---
#     filename = f"model_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
#     file_path = os.path.join(settings.MEDIA_ROOT, "reports", filename)
#     os.makedirs(os.path.dirname(file_path), exist_ok=True)

#     pdf.output(file_path)
#     return file_path


from fpdf import FPDF
import os
from datetime import datetime
from django.conf import settings

# Reuse your updated build_table from earlier
# (the one with auto-fit widths, bold header, striped rows, multi-line support)

# from fpdf.fonts import FontFace

# def build_table(pdf, title, data, headers=None, key_map=None):
#     # Section title
#     pdf.set_font("Helvetica", "B", 14)
#     pdf.cell(0, 10, title, ln=True)

#     # Normalize input → always list of dicts
#     if isinstance(data, dict):
#         data = [data]
#     elif not isinstance(data, list):
#         return

#     if not data:
#         pdf.set_font("Helvetica", "", 10)
#         pdf.cell(0, 10, "No data available", ln=True)
#         pdf.ln(5)
#         return

#     # Build rows
#     if headers and key_map:
#         rows = [headers] + [[str(row.get(k, "")) for k in key_map] for row in data]
#     else:
#         cols = list(data[0].keys())
#         rows = [cols] + [[str(row.get(k, "")) for row in data]]

#     # --- Auto-fit column widths with minimum size ---
#     page_width = pdf.epw
#     col_count = len(rows[0])
#     max_text_widths = [max(len(str(r[col_idx])) for r in rows) for col_idx in range(col_count)]
#     total_len = sum(max_text_widths)

#     # At least 20 mm per column
#     min_width = 20
#     col_widths = [(page_width * l / total_len) for l in max_text_widths]
#     col_widths = [max(w, min_width) for w in col_widths]

#     # If total > page_width, rescale proportionally
#     scale_factor = page_width / sum(col_widths)
#     col_widths = [w * scale_factor for w in col_widths]

#     # Styles
#     header_style = FontFace(emphasis="B", fill_color=(220, 220, 220))
#     body_style = FontFace()
#     alt_row_style = FontFace(fill_color=(245, 245, 245))

#     pdf.set_font("Helvetica", size=9)

#     # Render table
#     with pdf.table(borders_layout="ALL", col_widths=col_widths) as table:
#         for row_idx, row_data in enumerate(rows):
#             row = table.row()
#             for datum in row_data:
#                 align = "C" if datum.replace(".", "", 1).isdigit() else "L"

#                 if row_idx == 0:
#                     style = header_style
#                 elif row_idx % 2 == 0:
#                     style = alt_row_style
#                 else:
#                     style = body_style

#                 row.cell(datum, align=align, style=style)


def generate_table_pdf():
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.add_page()

    # --- Dummy Data---
    dummy_data = [
        {
            "ID": "1",
            "Name": "Alice",
            "Department": "Engineering",
            "Remarks": "Quick learner",
            "Notes": "Short"
        },
        {
            "ID": "2",
            "Name": "Bob",
            "Department": "Finance",
            "Remarks": "Needs improvement",
            "Notes": "This is a very long dummy note meant to check if wrapping works correctly "
                     "across multiple lines in the same PDF cell. It should break nicely."
        },
        {
            "ID": "3",
            "Name": "Charlie",
            "Department": "Marketing",
            "Remarks": "Great communication skills",
            "Notes": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor "
                     "incididunt ut labore et dolore magna aliqua. This should span at least 2 or 3 lines."
        },
        {
            "ID": "4",
            "Name": "Diana",
            "Department": "HR",
            "Remarks": "Handles recruitment",
            "Notes": "Short again"
        },
        {
            "ID": "5",
            "Name": "Eve",
            "Department": "IT Support",
            "Remarks": "Manages infrastructure",
            "Notes": "This dummy entry contains enough text to wrap into three or more lines when "
                     "rendered in the PDF table cell to fully test multi-line wrapping and row height adjustment."
        },
    ]

    headers = ["ID", "Name", "Department", "Remarks", "Notes"]
    key_map = ["ID", "Name", "Department", "Remarks", "Notes"]

    # Build table with dummy multi-line data
    build_table(pdf, "Dummy Employee Table", dummy_data, headers=headers, key_map=key_map)

    # --- Save PDF to media/reports ---
    filename = f"dummy_multiline_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, "reports", filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    pdf.output(file_path)
    return file_path






# def generate_table_pdf(modelinfo, findingsByElements, findingsCntByCategory,
#                        findingsByUpstreamMdl, findingsCntByMdls,issueList, chart_paths=None):

#     from django.conf import settings
#     import os, pathlib
#     from datetime import datetime
#     from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
#     from reportlab.lib import colors
#     from reportlab.lib.styles import getSampleStyleSheet
#     from reportlab.lib.pagesizes import landscape, A4

#     styles = getSampleStyleSheet()
#     normal_style = styles['Normal']
#     header_style = styles['Heading2']

#     # ---- File Path ----
#     filename = f"model_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
#     file_path = os.path.join(settings.MEDIA_ROOT, "reports", filename)
#     os.makedirs(os.path.dirname(file_path), exist_ok=True)

#     # ---- PDF Setup ----
#     doc = SimpleDocTemplate(
#         file_path,
#         pagesize=landscape(A4),
#         rightMargin=20,
#         leftMargin=20,
#         topMargin=20,
#         bottomMargin=20
#     )

#     elements = []

#     # ---- Helper: Auto-fit Table ----
#     def build_table(title, data_dict, headers=None, key_map=None):
#         elements.append(Paragraph(title, header_style))
#         elements.append(Spacer(1, 6))

#         if not data_dict:
#             elements.append(Paragraph("No Data Available", normal_style))
#             elements.append(PageBreak())
#             return

#         # Prepare table data
#         if headers and key_map:
#             table_data = [[Paragraph(f"<b>{h}</b>", normal_style) for h in headers]]
#             for row in data_dict.values():
#                 table_row = []
#                 for k in key_map:
#                     text = str(row.get(k, "")).replace("\n", "<br/>")
#                     table_row.append(Paragraph(text, normal_style))
#                 table_data.append(table_row)
#         else:
#             headers = list(list(data_dict.values())[0].keys())
#             table_data = [[Paragraph(f"<b>{h}</b>", normal_style) for h in headers]]
#             for row in data_dict.values():
#                 table_row = []
#                 for h in headers:
#                     text = str(row.get(h, "")).replace("\n", "<br/>")
#                     table_row.append(Paragraph(text, normal_style))
#                 table_data.append(table_row)

#         # ---- Dynamic column width ----
#         max_widths = []
#         for col_idx in range(len(headers)):
#             max_len = max(len(str(row[col_idx].text)) for row in table_data)  # longest text in this col
#             max_widths.append(min(max_len * 6, 200))  # 6pt per char, cap at 200px

#         table = Table(table_data, colWidths=max_widths)

#         # Styling
#         table.setStyle(TableStyle([
#             ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
#             ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#             ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
#             ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#             ('FONTSIZE', (0, 0), (-1, -1), 8),
#             ('LEFTPADDING', (0, 0), (-1, -1), 4),
#             ('RIGHTPADDING', (0, 0), (-1, -1), 4),
#             ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
#         ]))

#         elements.append(table)
#         elements.append(PageBreak())

#     # ---- Add Model Info (restricted columns) ----
#     build_table(
#         "Model Info",
#         modelinfo,
#         headers=["Model ID", "Primary Model Name", "Model Source", "Model Type", "Model Risk"],
#         key_map=["Mdl_Id", "Prm_Name", "Mdl_Src_Label", "Mdl_Type_Label", "Mdl_Risk_Label"]
#     )
#     ##issue
#     build_table(
#         "Issue Info",
#         issueList,
#         headers=["Issue ID", "Priority", "Approval Status", "Issue Function", "Issue Type","Completion Status","End Date"],
#         key_map=["Issue_ID", "Issue_Priority_Label", "Issue_ApprovalStatus_Label", "Issue_Function_Label", "Issue_Type_label","Completion_Status","end_dt"]
#     )
#     # ---- Other Tables ----
#     build_table("Findings By Elements", findingsByElements)
#     build_table("Findings Count By Category", findingsCntByCategory)
#     build_table("Findings By Upstream Models", findingsByUpstreamMdl)
#     build_table("Findings Count By Models", findingsCntByMdls)

#     # ---- Add Charts ----
#     if chart_paths:
#         for chart in chart_paths:
#             chart_path = pathlib.Path(chart)
#             if chart_path.exists():
#                 elements.append(Paragraph(chart_path.stem.replace("_", " ").title(), header_style))
#                 elements.append(Spacer(1, 10))
#                 img = Image(str(chart_path), width=500, height=300)
#                 elements.append(img)
#                 elements.append(PageBreak())

#     # ---- Build PDF ----
#     doc.build(elements)
#     return file_path


# from fpdf import FPDF
# import os
# from datetime import datetime
# import pathlib

# class PDF(FPDF):
#     def header(self):
#         # Custom header for each page
#         self.set_font("Arial", "B", 14)
#         self.cell(0, 10, "Model Info Report", ln=True, align="C")
#         self.ln(5)

# def generate_table_pdf(modelinfo, findingsByElements, findingsCntByCategory,
#                        findingsByUpstreamMdl, findingsCntByMdls, chart_paths=None):
#     print("modelinfo", modelinfo)
#     print("findingsByElements", findingsByElements)
#     print("findingsCntByCategory", findingsCntByCategory)
#     print("findingsByUpstreamMdl", findingsByUpstreamMdl)
#     print("findingsCntByMdls", findingsCntByMdls)
#     print("chart_paths", chart_paths)

#     pdf = PDF(orientation="L", unit="mm", format="A4")
#     pdf.add_page()

#     # Helper function to draw a styled table
#     def add_table(title, data_dict):
#         pdf.set_font("Helvetica", "B", 14)
#         pdf.cell(0, 10, title, ln=True, align="L")
#         pdf.ln(2)

#         if not data_dict:
#             pdf.set_font("Times", size=11)
#             pdf.cell(0, 10, "No Data Available", ln=True)
#             return

#         # Headers
#         headers = list(list(data_dict.values())[0].keys())
#         col_width = (pdf.w - 20) / len(headers)   # evenly distribute
#         row_height = 8

#         # Draw header row
#         pdf.set_fill_color(200, 200, 200)  # light gray
#         pdf.set_font("Arial", "B", 10)
#         for h in headers:
#             pdf.multi_cell(col_width, row_height, str(h), border=1, align="C", fill=True, ln=3, max_line_height=pdf.font_size)
#         pdf.ln(row_height)

#         # Rows
#         pdf.set_font("Times", size=9)
#         fill = False
#         for row in data_dict.values():
#             y_before = pdf.get_y()
#             x_before = pdf.get_x()

#             # Draw each column with wrapping text
#             for h in headers:
#                 text = str(row.get(h, ""))
#                 pdf.multi_cell(col_width, row_height, text, border=1, align="L", ln=3, max_line_height=pdf.font_size)
#                 x_after = pdf.get_x()
#                 y_after = pdf.get_y()
#                 pdf.set_xy(x_before + col_width, y_before)  # move to next col
#                 x_before = pdf.get_x()
#                 y_before = y_after

#             pdf.ln(row_height)  # move to next row
#             fill = not fill

#         pdf.ln(5)  # spacing
#         pdf.add_page()  # force each table to new page

#     # ---- Add Tables ----
#     add_table("Model Info", modelinfo)
#     add_table("Findings By Elements", findingsByElements)
#     add_table("Findings Count By Category", findingsCntByCategory)
#     add_table("Findings By Upstream Models", findingsByUpstreamMdl)
#     add_table("Findings Count By Models", findingsCntByMdls)

#     # ---- Add Charts ----
#     if chart_paths:
#         for chart in chart_paths:
#             chart_path = pathlib.Path(chart)
#             if chart_path.exists():
#                 pdf.add_page()
#                 pdf.set_font("Arial", "B", 14)
#                 pdf.cell(0, 10, chart_path.stem.replace("_", " ").title(), ln=True, align="C")
#                 img_w = 180   # for landscape
#                 img_h = 110   # adjust proportionally

#                 # Calculate centered X, Y
#                 x_pos = (pdf.w - img_w) / 2
#                 y_pos = 40  # top margin

#                 pdf.image(str(chart_path), x=x_pos, y=y_pos, w=img_w, h=img_h)
#                 # pdf.image(str(chart_path), x=15, y=40, w=180, h=120)


#     # ---- Save File ----
#     filename = f"model_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
#     file_path = os.path.join(settings.MEDIA_ROOT, "reports", filename)
#     os.makedirs(os.path.dirname(file_path), exist_ok=True)

#     pdf.output(file_path)

#     return file_path



# from fpdf import FPDF
# import os
# from datetime import datetime
# import pathlib

# def generate_table_pdf(modelinfo, findingsByElements, findingsCntByCategory,
#                        findingsByUpstreamMdl, findingsCntByMdls, chart_paths=None):
#     print("modelinfo", modelinfo)
#     print("findingsByElements", findingsByElements)
#     print("findingsCntByCategory", findingsCntByCategory)
#     print("findingsByUpstreamMdl", findingsByUpstreamMdl)
#     print("findingsCntByMdls", findingsCntByMdls)
#     print("chart_paths", chart_paths)

#     pdf = FPDF(orientation="L", unit="mm", format="A4")  # Landscape
#     pdf.add_page()
#     pdf.set_font("Times", size=12)

#     # ---- Helper: add a table ----
#     def add_table(title, data_dict):
#         pdf.set_font("Arial", "B", 14)
#         pdf.cell(0, 10, title, ln=True, align="C")
#         pdf.set_font("Times", size=11)

#         if not data_dict:
#             pdf.cell(0, 10, "No Data Available", ln=True)
#             return

#         # Extract header
#         headers = list(list(data_dict.values())[0].keys())
#         col_width = pdf.w / (len(headers) + 1)

#         # Header row
#         for h in headers:
#             pdf.cell(col_width, 10, str(h), border=1, align="C")
#         pdf.ln()

#         # Data rows
#         for row in data_dict.values():
#             for h in headers:
#                 pdf.cell(col_width, 10, str(row.get(h, "")), border=1)
#             pdf.ln()

#         pdf.ln(5)  # spacing

#     # ---- Add Tables ----
#     add_table("Model Info", modelinfo)
#     add_table("Findings By Elements", findingsByElements)
#     add_table("Findings Count By Category", findingsCntByCategory)
#     add_table("Findings By Upstream Models", findingsByUpstreamMdl)
#     add_table("Findings Count By Models", findingsCntByMdls)

#     # ---- Add Charts (Images) ----
#     if chart_paths:
#         for chart in chart_paths:
#             try:
#                 chart_path = pathlib.Path(chart)
#                 if chart_path.exists():
#                     pdf.add_page()
#                     pdf.set_font("Arial", "B", 14)
#                     pdf.cell(0, 10, chart_path.stem.replace("_", " ").title(), ln=True, align="C")
#                     pdf.image(str(chart_path), x=30, y=30, w=230)  # scale to page
#             except Exception as e:
#                 print("Error adding chart:", chart, e)

#     # ---- Save file ----
#     filename = f"model_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
#     file_path = os.path.join(settings.MEDIA_ROOT, "reports", filename)
#     os.makedirs(os.path.dirname(file_path), exist_ok=True)

#     pdf.output(file_path)

#     return file_path


# import os
# from django.conf import settings
# from django.template.loader import render_to_string
# from weasyprint import HTML, CSS
# import pathlib

# def generate_table_pdf(modelinfo, findingsByElements, findingsCntByCategory,
#                        findingsByUpstreamMdl, findingsCntByMdls, chart_paths=None):
#     # Convert Windows paths to proper file:// URIs for WeasyPrint
#     print("chart_paths",chart_paths)
#     chart_paths = [pathlib.Path(p).as_uri() for p in (chart_paths or [])]
#     context = {
#         "modelinfo": modelinfo,
#         "findingsByElements": findingsByElements,
#         "findingsCntByCategory": findingsCntByCategory,
#         "findingsByUpstreamMdl": findingsByUpstreamMdl,
#         "findingsCntByMdls": findingsCntByMdls,
#         "chart_paths": chart_paths or []
#     }

#     print("modelinfo",modelinfo)
#     print("findingsByElements",findingsByElements)
#     print("findingsCntByCategory",findingsCntByCategory)
#     print("findingsByUpstreamMdl",findingsByUpstreamMdl)
#     print("findingsCntByMdls",findingsCntByMdls)
#     print("chart_paths",chart_paths)


#     # Render template with context
#     html_string = render_to_string("test_debug.html",context)

#     print("DEBUG HTML >>>", html_string[:500])
#     css = CSS(string='''
#         @page { size: A4 landscape; margin: 20mm; }
#         body { font-family: "Times New Roman", serif; font-size: 18px; }
#         h1 { font-family: "Arial"; font-size: 18px; text-align: center; }
#         table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
#         th, td { border: 1px solid #ccc; padding: 8px; }
        
#         /* Force each table on a new page */
#         .page-break { page-break-before: always; }
#     ''')
#     # Generate PDF
#     pdf_bytes = HTML(string=html_string).write_pdf(stylesheets=[css])

#     # Save dynamically with timestamp
#     from datetime import datetime
#     filename = f"model_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
#     file_path = os.path.join(settings.MEDIA_ROOT, "reports", filename)

#     os.makedirs(os.path.dirname(file_path), exist_ok=True)

#     with open(file_path, "wb") as f:
#         f.write(pdf_bytes)

#     return file_path



# from django.shortcuts import render
# from django.http import HttpResponse
# from io import BytesIO
# from xhtml2pdf import pisa

# def generate_table_pdf(request):
#     print("generate_table_pdf")
#     # Sample data for your table (e.g., from a Django model)
#     table_data = [
#         {'name': 'Alice', 'age': 30, 'city': 'New York'},
#         {'name': 'Bob', 'age': 24, 'city': 'London'},
#         {'name': 'Charlie', 'age': 35, 'city': 'Paris'},
#     ]

#     # Render the HTML template with the table data
#     template_path = 'modelval/dashboard_icon.html'
#     context = {'table_data': table_data}
#     html = render(request, template_path, context).content.decode('utf-8')

#     # Create a file-like buffer to receive PDF data
#     buffer = BytesIO()

#     # Convert HTML to PDF
#     pisa_status = pisa.CreatePDF(
#         html,
#         dest=buffer
#     )

#     # If PDF creation was successful
#     if not pisa_status.err:
#         buffer.seek(0)
#         return HttpResponse(buffer, content_type='application/pdf')

#     # If there was an error
#     return HttpResponse('We had some errors <pre>' + html + '</pre>')


# from django.http import HttpResponse
# from django.template.loader import get_template
# from xhtml2pdf import pisa
# from django.conf import settings
# import os

# def generate_table_pdf(request):
#     print("generate_table_pdf")
#     # Example data
#     table_data = [
#         {"id": 1, "name": "Alice", "score": 90},
#         {"id": 2, "name": "Bob", "score": 85},
#         {"id": 3, "name": "Charlie", "score": 92},
#     ]

#     # Render HTML
#     template = get_template("dashboard_icon.html")
#     html = template.render({"table_data": table_data})

#     # File path inside MEDIA_ROOT
#     file_path = os.path.join(settings.MEDIA_ROOT, "pdfs", "table.pdf")

#     # Ensure directory exists
#     os.makedirs(os.path.dirname(file_path), exist_ok=True)

#     # Write PDF to file
#     with open(file_path, "wb") as pdf_file:
#         pisa_status = pisa.CreatePDF(html, dest=pdf_file)

#     if pisa_status.err:
#         return HttpResponse("Error generating PDF")

#     return HttpResponse(f"PDF saved at: {file_path}")


# def stacked_bar(data, labels, x_labels, colors, para):
#     import numpy as np
#     import matplotlib.pyplot as plt
#     import os

#     print("stacked_bar", data, labels, x_labels, colors, para)

#     # Convert to numpy for consistency
#     data = np.array([row + [0]*(len(x_labels)-len(row)) for row in data])

#     N = len(x_labels)       # number of x-axis groups
#     ind = np.arange(N)      # x locations
#     width = 0.6             # bar width

#     fig, ax = plt.subplots(figsize=(10, 7))

#     # Stack bars
#     bottoms = np.zeros(N)
#     for row, lbl, color in zip(data, labels, colors):
#         ax.bar(ind, row, width, bottom=bottoms, label=lbl, color=color)
#         bottoms += row

#     if para == "mdl_risk":
#         chart_title = "Model Risks"
#     elif para == "issues":
#         chart_title = "Issues"
#     else:
#         chart_title = para
#     # Labels and formatting
#     # ax.set_ylabel("Contribution")
#     ax.set_title(chart_title)
#     ax.set_xticks(ind)
#     ax.set_xticklabels(x_labels, rotation=45)
#     ax.legend()

#     # Save
#     filename = f"{para}.png"
#     save_path = os.path.join(BASE_DIR, "static", "media", filename)
#     plt.savefig(save_path, bbox_inches="tight", dpi=300)
#     plt.close()


# def stacked_bar(data, labels, x_labels, colors, para):
#     print("stacked_bar", data, labels, x_labels, colors, para)

#     data = np.array(data)   # shape = (len(labels), len(x_labels))

#     N = len(x_labels)       # number of x-axis groups
#     ind = np.arange(N)      # x locations
#     width = 0.6             # bar width

#     fig, ax = plt.subplots(figsize=(10, 7))

#     # Stack bars
#     bottoms = np.zeros(N)
#     bars = []
#     for i, (row, lbl, color) in enumerate(zip(data, labels, colors)):
#         bar = ax.bar(ind, row, width, bottom=bottoms, label=lbl, color=color)
#         bars.append(bar)
#         bottoms += row

#     if para == "mdl_risk":
#         chart_title = "Model Risks"
#     elif para == "issues":
#         chart_title = "Issues"
#     else:
#         chart_title = para
#     # Labels and formatting
#     # ax.set_ylabel("Contribution")
#     ax.set_title(chart_title)
#     ax.set_xticks(ind)
#     ax.set_xticklabels(x_labels, rotation=45)
#     ax.legend()

#     # Save
#     filename = f"{para}.png"
#     save_path = os.path.join(BASE_DIR, "static", "media", filename)
#     plt.savefig(save_path, bbox_inches="tight", dpi=300)
#     plt.close()

# def stacked_bar(data, labels, colors, para):
#     import pandas as pd
#     import matplotlib.pyplot as plt
#     import os

#     print("stacked_bar", data, labels, colors, para)

#     # Example: data = {"Group1": [1,2,3], "Group2": [4,5,6]}
#     labels = [item for item in labels if item != 'None']

#     # Convert dict to DataFrame (labels = columns, keys = x-axis)
#     df = pd.DataFrame(data, columns=labels)

#     # Set the index (this will appear on x-axis)
#     df.index.name = "X-axis values"

#     print("df >>>\n", df)

#     # Plot stacked bar
#     ax = df.plot(
#         kind='bar',
#         stacked=True,
#         color=colors,
#         figsize=(8, 6),
#         title="Model Risk"
#     )

#     plt.xlabel("X-axis values")
#     plt.ylabel("Values")
#     plt.legend(title="Labels")
#     plt.tight_layout()

#     # Save chart
#     filename = f"{para}.png"
#     save_path = os.path.join(BASE_DIR, "static", "media", filename)
#     plt.savefig(save_path, bbox_inches="tight", dpi=300)
#     plt.show()
#     plt.close()


# def bar_chart(data, label, colors, para):
#     print("bar_chart",data, label, colors, para)
#     import matplotlib.pyplot as plt
#     import numpy as np

#     x = np.array(label)
#     y = np.array(data)

#     plt.bar(x, y, color = colors)
#     plt.show()
#     filename = f"{para}.png"
#     save_path = os.path.join(BASE_DIR, "static", "media", filename)

#     plt.savefig(save_path, bbox_inches="tight", dpi=300)
#     plt.close()

# def plotdoughnut(data,label,colors,para):
#     print("plotdoughnut",data,label,colors,para)

#     import matplotlib.pyplot as plt
#     BASE_DIR = Path(__file__).resolve().parent.parent
#     # Setting labels for items in Chart
#     Employee = label
#     # Setting size in Chart based on 
#     # given values
#     Salary =data
#     # colors
#     colors = colors
#     # explosion
#     explode = (0.05, 0.05, 0.05, 0.05)
#     # Pie Chart
#     plt.pie(Salary, colors=colors, labels=Employee,
#             autopct='%1.1f%%', pctdistance=0.85 )

#     # draw circle
#     centre_circle = plt.Circle((0, 0), 0.70, fc='white')
#     fig = plt.gcf()

#     # Adding Circle in Pie chart
#     fig.gca().add_artist(centre_circle)

#     # Adding Title of chart
#     plt.title('Model Category')

#     # Displaying Chart
#     plt.savefig(os.path.join(BASE_DIR, 'static\\media\\' +'foo.png'))

#added on 15.07.25 starts
def updateDashboardSetting(request):
    try:
        pane = request.GET.get('pane')
        userSel = request.GET.get('userSel')
        third_party_api_url = getAPIURL()+'updateDashboardSetting/'
        data_to_save = {
            'pane':pane, 
            'userSel':userSel,
            'uid':request.session['uid']
        }
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header) 
        return JsonResponse(json.loads(response.content))
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Failed to connect .', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
#added on 15.07.25 ends

def modelList(request):
    print("modelList................................")
    try:
        ty =request.GET.get('ty', 'False') 
        colnm =request.GET.get('colnm', 'False') 
        chartnm =request.GET.get('chartnm', 'False') 
        mdlType =request.GET.get('mdlType', 'None') 
        canAdd=request.session['canAdd']
        Authorization(request,request.session['ucaid'],'Model Inventory')
        api_url=getAPIURL()+"projectsInfo/"       
        data_to_save={ 
            'uid':request.session['uid'],
            'filterType':ty,
            'filterColumn':chartnm,
            'filterValue':colnm,
            'mdlType':mdlType,
            'istool':'0'} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)         
        api_data=response.json() 
        modelinfo=api_data['modelinfo']#objreg.getModelByFilter(request.session['uid'],ty,chartnm,colnm,'0')
        if ty=='pie' and chartnm=='Model Category':
            modeltype='Model Category - ' +colnm
        elif ty=='pie'  :
            modeltype='Model Type - ' +colnm
        elif ty =='bar':
            modeltype=chartnm +' - '+ colnm
        else:
            modeltype=''
             
        # return render(request, 'addICQQtns.html',{'sections':objmaster.getSections(),'actPage':'RMSE','notifylen':str(len(objvalidation.getVTNotifications(request.session['uid'])))})
        return render(request, 'modelList.html',{'actPage':'RMSE','modelinfo':modelinfo,'canAdd':canAdd,'modeltype':modeltype})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 

# views.py
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings

@csrf_exempt
def save_chart(request):
    if request.method == "POST":
        image_data = request.POST.get("imageData")
        filename = request.POST.get("filename", "chart.png")  # default fallback
        print("filename",filename   )
        image_data = image_data.replace("data:image/png;base64,", "")
        image_binary = base64.b64decode(image_data)

        save_dir = os.path.join(settings.BASE_DIR, "static/dashboard_charts")
        os.makedirs(save_dir, exist_ok=True)

        # Add timestamp to filename
        # name, ext = os.path.splitext(filename)
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # unique_filename = f"{name}_{timestamp}{ext}"

        # file_path = os.path.join(save_dir, unique_filename)

        file_path = os.path.join(save_dir, filename)

        with open(file_path, "wb") as f:
            f.write(image_binary)

        return JsonResponse({"status": "success", "filepath": f"/static/dashboard_charts/{filename}"})

# import base64
# import os
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
# from datetime import datetime

# @csrf_exempt
# def save_chart(request):
#     if request.method == "POST":
#         image_data = request.POST.get("imageData")
#         filename = request.POST.get("filename", "chart.png")  # base name from JS

#         if not image_data:
#             return JsonResponse({"status": "error", "message": "No image data"}, status=400)

#         # Remove the "data:image/png;base64," prefix
#         image_data = image_data.replace("data:image/png;base64,", "")
#         image_binary = base64.b64decode(image_data)

#         # Ensure save directory exists
#         save_dir = os.path.join(settings.BASE_DIR, "static/dashboard_charts")
#         os.makedirs(save_dir, exist_ok=True)

#         # Add timestamp to filename
#         name, ext = os.path.splitext(filename)
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         unique_filename = f"{name}_{timestamp}{ext}"

#         file_path = os.path.join(save_dir, unique_filename)

#         # Write image
#         with open(file_path, "wb") as f:
#             f.write(image_binary)

#         return JsonResponse({
#             "status": "success",
#             "filepath": f"/static/dashboard_charts/{unique_filename}"
#         })

#     return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


def modelList(request):
    print("modelList................................")
    try:
        ty =request.GET.get('ty', 'False') 
        colnm =request.GET.get('colnm', 'False') 
        chartnm =request.GET.get('chartnm', 'False') 
        mdlType =request.GET.get('mdlType', 'None') 
        canAdd=request.session['canAdd']
        Authorization(request,request.session['ucaid'],'Model Inventory')
        api_url=getAPIURL()+"projectsInfo/"       
        data_to_save={ 
            'uid':request.session['uid'],
            'filterType':ty,
            'filterColumn':chartnm,
            'filterValue':colnm,
            'mdlType':mdlType,
            'istool':'0'} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)         
        api_data=response.json() 
        modelinfo=api_data['modelinfo']#objreg.getModelByFilter(request.session['uid'],ty,chartnm,colnm,'0')
        if ty=='pie' and chartnm=='Model Category':
            modeltype='Model Category - ' +colnm
        elif ty=='pie'  :
            modeltype='Model Type - ' +colnm
        elif ty =='bar':
            modeltype=chartnm +' - '+ colnm
        else:
            modeltype=''
             
        # return render(request, 'addICQQtns.html',{'sections':objmaster.getSections(),'actPage':'RMSE','notifylen':str(len(objvalidation.getVTNotifications(request.session['uid'])))})
        return render(request, 'modelList.html',{'actPage':'RMSE','modelinfo':modelinfo,'canAdd':canAdd,'modeltype':modeltype})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 



def getMdlDetailsById(request):
    try:
        mdl_id =request.GET.get('mdlId', 'False') 
        api_url=getAPIURL()+"getMdlDetailsById/"       
        data_to_save={
            'mdl_id':mdl_id} 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
        # 'pdfFile': "/static/media/ValidationReport_"+request.session['vt_mdl']+".pdf", 
        api_data=response.json() 

        Owner=api_data['Owner']

        Developer=api_data['Developer']#objMdlRelvPern.getRelevantPersonal(mdl_id,'Developer')

        User=api_data['User']#objMdlRelvPern.getRelevantPersonal(mdl_id,'User')

        PrdnSupport=api_data['PrdnSupport']#objMdlRelvPern.getRelevantPersonal(mdl_id,'PrdnSupport')
 
        dependencies =api_data['dependencies']#objdependencies.getMdlDependencies(mdl_id) 
        isvrpublished=api_data['isvrpublished'] 
        PerformMon=objreg.getPerfomanceMonitor(mdl_id)
        print(str(api_data['mdldata']["0"]['AddedBy']) ,',', str(request.session['uid']))
        is_owner='No'
        if str(api_data['mdldata']["0"]['AddedBy'])== str(request.session['uid']):
            is_owner='Yes'
        return JsonResponse({'istaken':'true','dependencies':dependencies,'PerformMon':PerformMon,'Owner':Owner,'is_owner':is_owner,
                             'Developer':Developer,'User':User,'PrdnSupport':PrdnSupport,'mdldata':api_data['mdldata'],'isvrpublished':isvrpublished})
    except Exception as e:
        print('getMdlDetails is ',e)
        print('getMdlDetails traceback is ', traceback.print_exc()) 


def checkUserRole(request):
    try:
        mdl_id = request.GET.get('mdl_id','none') 
        return JsonResponse({'role': objrmse.checkUserRole(request.session['uid'],mdl_id)})
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())     


def checkUserRole_Issue(request):
    try:
        issue_id = request.GET.get('mdl_id','none') 
      
        api_url=getAPIURL()+"checkUserRole_Issue/"       
        data_to_save={'uid':request.session['uid'] ,
                      'mdl_id':issue_id} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)         
        api_data=response.json() 
        context={'role':api_data['role']}  
        return JsonResponse(context)
    except Exception as e:
        print('adduser is ',e) 
        print('adduser traceback is ', traceback.print_exc())  



def activitytrail(request):
    try: 
        if request.method  == 'GET':
            refer_id=request.GET.get('selectSection','')
        else:
            refer_id=request.POST.get('selectSection','')
        activityobj = ActivityTrail.objects.filter(refference_id = refer_id).order_by('-added_on')  
        activity_lst = activityinfo(activityobj)

        mdl_id = ActivityTrail.objects.values('refference_id').distinct()
        mdlid_lst = []
        for val in mdl_id:
            mdlid_lst.append(val['refference_id'])

        return render(request, 'activitytrail.html',{'actPage':'Activity Trail','activity_lst':activity_lst,'mdlid_lst':mdlid_lst,'refer_id':refer_id})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ', traceback.print_exc())


def activityinfo(record):
    lst = []
    irow=1
    for activity_obj in record: 
        dict={}
        activity_trigger = activity_obj.activity_trigger
        refference_id = activity_obj.refference_id
        addon = activity_obj.added_on
        # print('addon ',addon)
        # addon = datetime.strptime(str(addon), '%y-%m-%d %I:%M %p')

        x = str(addon).split(" ") 
        userobj = Users.objects.get(u_aid = activity_obj.addedby)
        user = userobj.u_name
        f_name = userobj.u_fname
        f_n = f_name[:1].capitalize()
        l_name = userobj.u_lname
        l_n = l_name[:1].capitalize()
        dict['activity_trigger'] = activity_trigger
        dict['refference_id'] = refference_id
        dict['user'] = user
        dict['f_name'] = f_n
        dict['l_name'] = l_n
        dict['date'] = addon.strftime('%m/%d/%Y')
        dict['time'] = addon.strftime('%I:%M %p') 
        dict['activity_details'] =activity_obj.activity_details
        if irow== len(record):
            dict['is_last']='Yes'
        else:
            dict['is_last']='No'
            irow+=1
        lst.append(dict)
    return lst   




def getIssuesByQtrOrMonth(request):
    try: 
        print('Token ',request.session['accessToken'])
        objreg=Register()
        api_url=getAPIURL()+"getIssuesByQtrOrMonth/"
        data_to_save={'utype':request.session['utype'],
            'dept':request.session['dept'],
            'uid':request.session['uid'],
            'ulvl':request.session['ulvl'],
            'is_mrm':request.session['is_mrm'],
            'ptype':request.GET['ptype'],   
            'issue_from_dt':request.GET['frdate'],
            'issue_to_dt':request.GET['todt'],
            'issue_sts':request.GET.getlist('sts[]')
            } 
        #'Qtr',
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json() 
        if(str(objmaster.isAutherized(request.session['ucaid'],"Dashboard")) =="0"): 
            return render(request, 'blank.html',{'actPage':'RMSE'}) 

        issuesByQtrOrMonth= api_data['issuesByQtrOrMonth']
        print('issuesByQtrOrMonth ',issuesByQtrOrMonth['data'])         
        
        return JsonResponse({'issuePriority':issuesByQtrOrMonth['data'],'chartSeries':issuesByQtrOrMonth['series']})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
        error_saving(request,e)

    
def Authorization(request,ucaid,resource_id): 
    if(str(objmaster.isAutherized(ucaid,resource_id)) =="0"): 
        return render(request, 'blank.html',{'msg':'You are not authorized to access this utility.'})



def error_saving(request,data):
    print("data print",data)
    file = open('logs.txt', 'w')
    file.write(str(data))
    file.close()
    print("file save")
    # return redirect(request,'error.html')

def issueLst(request):
    try: 
        print('Token ',request.session['accessToken'])
        objreg=Register()
        dttbl=objreg.getUserDeatils(request.session['utype'],request.session['dept']) 
        if dttbl.empty == False:
            request.session['li_mrm']=dttbl[dttbl['r_label'] == 'Model Risk Management'].values[0][2]
            request.session['li_qv']=dttbl[dttbl['r_label'] =='Dashboard'].values[0][2] 
            request.session['li_modinv']=dttbl[dttbl['r_label'] =='Model Inventory'].values[0][2] 
            request.session['li_modtasks']=dttbl[dttbl['r_label'] =='Tasks'].values[0][2]  
            request.session['li_adduser']=dttbl[dttbl['r_label'] =='Dept Head'].values[0][2] 
            request.session['li_task']=dttbl[dttbl['r_label'] =='Tasks'].values[0][2]
            request.session['task_registration']='block'
            request.session['li_issuesReg']='block'
            request.session['li_taskApprv']='block' 
            request.session['li_taskComplete']='block'
            request.session['li_issueComplete']='block'
            request.session['li_issueApprv']='block'
            request.session['li_icqqtn']='block' 
            if(str(objmaster.checkMRMHead(str(request.session['uid']))))=="1" or (str(objmaster.checkMRMMgr(str(request.session['uid']))))=="1":
                request.session['li_icqqtnfinal']='block'
                request.session['li_modval']='block'
                request.session['li_icqqtn']='none' 
            else:
                request.session['li_icqqtnfinal']='none'
                request.session['li_modval']='none' 

            if(str(objmaster.checkMRMHead(str(request.session['uid']))))=="1":
                 request.session['is_mrm']='Yes'
            else: 
                request.session['is_mrm']='No'

        del dttbl
        
        api_url=getAPIURL()+"FiterIssue/"
        print(request.GET['chartnm'])
        data_to_save={'utype':request.session['utype'],
            'dept':request.session['dept'],
            'uid':request.session['uid'],
            'ulvl':request.session['ulvl'],
            'is_mrm':request.session['is_mrm'],
            'type':request.GET['ty'],
            'priority':request.GET['chartnm'],
            'colval':request.GET['colnm']
            } 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json() 
        if(str(objmaster.isAutherized(request.session['ucaid'],"Dashboard")) =="0"): 
            return render(request, 'blank.html',{'actPage':'RMSE'})  
        issueList=api_data['issueList'] 
         
        return render(request, 'issueLst.html',{  'issueCnt':len(issueList),'issueList':issueList})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 
        error_saving(request,e)


def getModelsByValFindingsPriority(request):
    try:
        ty =request.GET.get('ty', 'False') 
        colnm =request.GET.get('colnm', 'False') 
        chartnm =request.GET.get('chartnm', 'False') 
        valPriority =request.GET.get('valPriority', 'False') 
        canAdd=request.session['canAdd']
        element_txt =request.GET.get('element_txt', 'False') 
        category_txt=request.GET.get('category_txt', 'False') 
        Authorization(request,request.session['ucaid'],'Model Inventory')
        api_url=getAPIURL()+"modelsByValPriority/"       
        data_to_save={ 
            'uid':request.session['uid'],
            'filterType':ty,
            'filterColumn':chartnm,
            'filterValue':colnm,
            'istool':'0',
            'valPriority':valPriority,
            'element_txt':element_txt,
            'category_txt':category_txt,
            } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)         
        api_data=response.json() 
        modelinfo=api_data['modelinfo']#objreg.getModelByFilter(request.session['uid'],ty,chartnm,colnm,'0')
        return render(request, 'modelsByValPriority.html',{'modelinfo':modelinfo,'canAdd':canAdd, 'actPage':'Model Inventory'})
            
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 


def save_comments_mdl_overview(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("save_comments_mdl_overview ",data)
        pane_name = data.get("pane_name")       # e.g. "Model Overview"
        comments = data.get("comments", {})     # dict with properties, status, risks, summary

        api_url=getAPIURL()+"save_comments_mdl_overview/"       
        data_to_save={ 
            'uid':request.session['uid'],
            'pane_name':pane_name,
            'comments':comments
            } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)         
        api_data=response.json() 

       
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request"})