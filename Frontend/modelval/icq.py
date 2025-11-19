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
from django.http import HttpResponse, Http404
from docx.enum.section import WD_ORIENT
from docx import Document

objreg=Register()  
objmaster=MasterTbls()
objvalidation=Validation()
objdbops=dbops()
objrmse=RMSEModel() 
from .models import *

def getAPIURL():
    api_url=os.environ['API_URL']
    return api_url

def allocate_icq(request): 
    try:
        if request.method=="POST":
            section=request.POST.get('section','False')
            sub_section=request.POST.get('sub_section','False')
            sub_sub_section=request.POST.get('sub_sub_section','False')
            sub_sub_sub_section=request.POST.get('sub_sub_sub_section','False')

            print(section,sub_section,sub_sub_section,sub_sub_sub_section)

            if sub_section == '' and sub_sub_section == '' and sub_sub_sub_section == '':
                print("session selected")
                question_obj_filter=IcqQuestionMaster.objects.filter(section_aid=section)
            elif sub_sub_section == '' and sub_sub_sub_section == '':
                print("sub section selected")
                question_obj_filter=IcqQuestionMaster.objects.filter(Q(sub_section_aid=sub_section) | Q(section_aid=section))
            elif sub_sub_sub_section == '':
                print("sub sub section selected")
                question_obj_filter=IcqQuestionMaster.objects.filter(Q(sub_sub_section_aid=sub_sub_section) | Q(sub_section_aid=sub_section) | Q(section_aid=section))  
    
            else:
                print("else")
                question_obj_filter=IcqQuestionMaster.objects.filter(section_aid=section,sub_section_aid=sub_section,
                                            sub_sub_section_aid=sub_sub_section,sub_sub_sub_section_aid=sub_sub_sub_section)
            
            list_data=[]
            dict_data=dict()
            for i in question_obj_filter:
                print("question",i.question_label)
                print('question id',i.question_aid)
                dict_data[i.question_aid]=i.question_label
                # dict_data['question']=i.question_label
                # dict_data['id']=i.question_aid
                print("dict_data",dict_data)
                # list_data.append(dict_data)
            #print('list data',list_data)    
            return JsonResponse(dict_data,safe=False)
	#Jayesh Code 
        userobj = Users.objects.all()
        review_name = IcqQuestionRatingAllocation.objects.values('review_id','review_name').distinct()
        print("review name",review_name)
        return render(request,'allocate_icq.html',{'sections':objmaster.getSections(),'user':userobj,'review':objmaster.getICQIds()})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 


def save_allocation(request):
    request_data = {x:request.GET.get(x) for x in request.GET.keys()}
    section_aid = request.GET.getlist('section_aid[]')
    users = request.GET.getlist('users[]')
    api_url=getAPIURL()+"save_allocation/"       
    data_to_save={'section_aid':section_aid,
        'users':users,
        'rv_id': request_data['rv_id'],
        'rv_name':request_data['rv_name'],} 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
        
    api_data=response.json()
    return JsonResponse({"isvalid":api_data['isvalid']}) 
    # request_data = {x:request.GET.get(x) for x in request.GET.keys()}
    # section_aid = request.GET.getlist('section_aid[]')
    # users = request.GET.getlist('users[]')
    # # end_date = request_data['end_date'][6:] + "-" + request_data['end_date'][3:5] + "-" + request_data['end_date'][:2]
    # if request_data['rv_id'] == "addnew":
    #     last_rvid_obj = IcqQuestionRatingAllocation.objects.aggregate(Max('review_id'))
    #     last_rvid = last_rvid_obj['review_id__max']
    #     splt_rvid = last_rvid.split('_')
    #     latest_rvid = int(splt_rvid[1]).__add__(1) #used magic method django
    #     for user, section_id in [(x,y) for x in users for y in section_aid]:
    #         allocate_obj = IcqQuestionRatingAllocation(review_id ="Rv_"+str(latest_rvid),review_name = request_data['rv_name'],section_aid = section_id,allocated_to = user,end_date = None)
    #         allocate_obj.save()
    #     return JsonResponse({"isvalid":"true"}) 
    # else:
    #     for user, section_id in [(x,y) for x in users for y in section_aid]:
    #         allocate_obj = IcqQuestionRatingAllocation(review_id =request_data['rv_id'],review_name = request_data['rv_name'],section_aid = section_id,allocated_to = user,end_date = None)
    #         allocate_obj.save()
    #     return JsonResponse({"isvalid":"true"}) 

def section_save_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            print("data",data)
            section_id = data.get('section_id')
            comment_text = data.get('comments')
            para=data.get('para')

            if para == 'comment':
                api_url=getAPIURL()+"section_save_comment/"       
                data_to_save={'section_aid':section_id,
                    'comment_text':comment_text,
                    'addedby': request.session['uid']} 
                header = {
                "Content-Type":"application/json",
                'Authorization': 'Token '+request.session['accessToken']
                }
                response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
                    
                api_data=response.json()

                print("api_data",api_data)
            
                return JsonResponse({'msg':api_data['msg']})
            elif para == 'discussion':
                api_url=getAPIURL()+"section_save_discussion/"       
                data_to_save={'section_aid':section_id,
                    'comment_text':comment_text,
                    'addedby': request.session['uid']} 
                header = {
                "Content-Type":"application/json",
                'Authorization': 'Token '+request.session['accessToken']
                }
                response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
                    
                api_data=response.json()

                print("api_data",api_data)
            
                return JsonResponse({'msg':api_data['msg']})
            

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def fetch_section_comment(request):
    section_id = request.GET.get('section_id')
    print("section_id",section_id)
    api_url=getAPIURL()+"section_save_comment/"       
    
    data_send={
        'section_id':section_id
    }
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url,data= json.dumps(data_send),headers=header)
        
    api_data=response.json()
    print("api_data",api_data)
    return JsonResponse(api_data)

def getsectionQtnResp(request):
    print("GET data",request.GET)
    section_id = request.GET.get('section_id')
    print("section_id",section_id)
    api_url=getAPIURL()+"getsectionQtnResp/"       
    
    data_send={
        'section_id':section_id,
        'uid':request.session['uid']
    }
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url,data= json.dumps(data_send),headers=header)
        
    api_data=response.json()
    print("api_data",api_data)
    
    return JsonResponse({"Qtns":api_data['Qtns']})

def ICQQtnsFinal(request):
    print("ICQQtnsFinal")
    try: 
        sectionid =request.POST.get('ddlSection', '0') 
        api_url=getAPIURL()+"ICQQtnsFinal/"       
         
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url,headers=header)
         
        api_data=response.json()

        api_url_a=getAPIURL()+"ICQInherentRiskRatingAPI/"       
         
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response_a = requests.get(api_url_a,headers=header)
         
        api_data_a=response_a.json() 
        r1 = [i['ratings'] for i in api_data_a['rating_1']] 
        r2 = [i['ratings'] for i in api_data_a['rating_2']] 
        r3 = [i['Ratings'] for i in api_data_a['rating_3']] 
        
        # print("Qtns",api_data['Qtns'])
        # generate_table_pdf(api_data['Qtns'])
        return render(request, 'ICQQtnsFinal.html',
                      {'ICQRating':api_data['ICQRating'],
                       'sectionid':sectionid,
                       'sections':api_data['sections'],
                       'Qtns':api_data['Qtns'],'rating_1':r1,'rating_2':r2,
                                               'rating_3':r3})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def generate_icq_pdf(request):
    if request.method == "GET":
        try:
            # body = json.loads(request.body.decode("utf-8"))  # full payload
            # Qtns = body.get("Qtns", {})  # this is already a dict
            # print("generate_icq_pdf", Qtns)
            api_url=getAPIURL()+"ICQQtnsFinal/"       
            
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response = requests.get(api_url,headers=header)
            
            api_data=response.json()
            Qtns=api_data['Qtns']
            # print("Qtns",Qtns)
           

            api_url_a=getAPIURL()+"ICQInherentRiskRatingAPI/"       
         
            header = {
            "Content-Type":"application/json",
            'Authorization': 'Token '+request.session['accessToken']
            }
            response_a = requests.get(api_url_a,headers=header)
            
            api_data_a=response_a.json() 
            r1 = [i['ratings'] for i in api_data_a['rating_1']] 
            r2 = [i['ratings'] for i in api_data_a['rating_2']] 
            r3 = [i['Ratings'] for i in api_data_a['rating_3']] 
            
            file_path,file_path2 = generate_table_pdf(Qtns,r1,r2,r3)
            print("file_paths",file_path,file_path2)
            print("sections",api_data['sections'])
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})


# from fpdf.fonts import FontFace
from fpdf import FPDF
import os
from datetime import datetime
from django.conf import settings

# def build_dynamic_table(pdf, title, data,r1,r2,r3):
#     print("r1,",r1)
#     print("r2",r2)
#     print("r3",r3)

#     # Use ArialUnicodeMS (registered regular + bold)
#     pdf.set_font("ArialUnicodeMS", "B", 14)
#     pdf.cell(0, 10, title, ln=True)

#     # Normalize input
#     if isinstance(data, dict):
#         data = list(data.values())

#     if not data:
#         pdf.set_font("ArialUnicodeMS", "", 10)
#         pdf.cell(0, 10, "No data available", ln=True)
#         pdf.ln(5)
#         return

#     # Keep only selected columns
#     cols = ["qtnNo", "qtnsArr",
#             "Inherent_Risk_Rating","Control_Effectiveness_Ratings","Control_description",
#             "Residual_Ratings","override_residual_ratings","override_comments"]
#     headers = ["Qtn No", "Question", 
#                "Inherent Risk","Control Effectiveness","Control Description",
#                "Residual Ratings","Residual Rating (Manual)","Mitigating Factor"]

#     rows = [headers] + [[str(row.get(k, "")) for k in cols] for row in data]

#     page_width = pdf.epw

#     # Fixed % widths
#     col_widths = [
#         page_width * 0.05,  # Qtn No
#         page_width * 0.35,  # Question
#         page_width * 0.09,  #risk
#         page_width * 0.10,  #Control Effectiveness
#         page_width * 0.35, #Control Description
#         page_width * 0.10, #Residual Ratings
#         page_width * 0.10, #Residual Rating (Manual)
#         page_width * 0.35, #Mitigating Factor
#     ]

#     # Styles (use FontFace with emphasis → works since Bold is registered)
#     header_style = FontFace(emphasis="B", fill_color=(200, 200, 200))
#     body_style = FontFace()
#     alt_row_style = FontFace(fill_color=(245, 245, 245))

#     pdf.set_font("ArialUnicodeMS", "", 9)

#     i = 0
#     n = len(data)
#     while i < n:
#         row_dict = data[i]
#         section_label = str(row_dict.get("Section_Label", "") or "").strip()

#         # ✅ Section heading before table
#         if section_label:
#             pdf.set_fill_color(220, 220, 220)
#             pdf.set_font("ArialUnicodeMS", "B", 11)
#             pdf.cell(0, 8, section_label, ln=True, fill=True, border=0)
#             pdf.ln(1)
#             pdf.set_font("ArialUnicodeMS", "", 9)

#         # Collect rows for this section until the next section label
#         batch = []
#         while i < n and not str(data[i].get("Section_Label", "") or "").strip():
#             batch.append(data[i])
#             i += 1

#         if not batch:
#             i += 1
#             continue

#         # ✅ Render a table for this batch
#         with pdf.table(borders_layout="ALL", col_widths=col_widths) as table:
#             # Header
#             header_row = table.row()
#             for h in headers:
#                 header_row.cell(h, align="C", style=header_style)

#             # Rows
#             for ridx, row_dict in enumerate(batch):
#                 r = table.row()
#                 for col_idx, key in enumerate(cols):
#                     text = str(row_dict.get(key, ""))
#                     if col_idx == 0:
#                         align = "R"
#                     elif col_idx in (2, 3):
#                         align = "C"
#                     else:
#                         align = "L"
#                     style = alt_row_style if ridx % 2 == 0 else body_style
#                     r.cell(text, align=align, style=style)



BASE_DIR = Path(__file__).resolve().parent.parent

font_files = os.path.join(BASE_DIR, 'static/fonts/')

def build_table(pdf, title, data):
    pdf.set_font("ArialUnicodeMS", "B", 14)
    pdf.cell(0, 10, title, ln=True)

    # Normalize input
    if isinstance(data, dict):
        data = list(data.values())

    if not data:
        pdf.set_font("ArialUnicodeMS", "", 10)
        pdf.cell(0, 10, "No data available", ln=True)
        pdf.ln(5)
        return

    # Columns (no Section_Label here)
    cols = ["qtnNo", "qtnsArr", "Rating_Yes_NO", "Doc_Yes_No", "comments"]
    headers = ["Qtn No", "Question", "Yes/No/NA", "Doc Yes/No/NA", "Comments"]

    page_width = pdf.epw
    col_widths = [
        page_width * 0.05,  # Qtn No
        page_width * 0.35,  # Question
        page_width * 0.10,  # Yes/No/NA
        page_width * 0.10,  # Doc Yes/No/NA
        page_width * 0.40,  # Comments
    ]

    # Styles
    header_style = FontFace(emphasis="B", fill_color=(200, 200, 200))
    body_style = FontFace()
    alt_row_style = FontFace(fill_color=(245, 245, 245))

    pdf.set_font("ArialUnicodeMS", "", 9)

    i = 0
    n = len(data)
    while i < n:
        row_dict = data[i]
        section_label = str(row_dict.get("Section_Label", "") or "").strip()

        # ✅ Section heading before table
        if section_label:
            pdf.set_fill_color(220, 220, 220)
            pdf.set_font("ArialUnicodeMS", "B", 11)
            pdf.cell(0, 8, section_label, ln=True, fill=True, border=0)
            pdf.ln(1)
            pdf.set_font("ArialUnicodeMS", "", 9)

        # Collect rows for this section until the next section label
        batch = []
        while i < n and not str(data[i].get("Section_Label", "") or "").strip():
            batch.append(data[i])
            i += 1

        if not batch:
            i += 1
            continue

        # ✅ Render a table for this batch
        with pdf.table(borders_layout="ALL", col_widths=col_widths) as table:
            # Header
            header_row = table.row()
            for h in headers:
                header_row.cell(h, align="C", style=header_style)

            # Rows
            for ridx, row_dict in enumerate(batch):
                r = table.row()
                for col_idx, key in enumerate(cols):
                    text = str(row_dict.get(key, ""))
                    if col_idx == 0:
                        align = "R"
                    elif col_idx in (2, 3):
                        align = "C"
                    else:
                        align = "L"
                    style = alt_row_style if ridx % 2 == 0 else body_style
                    r.cell(text, align=align, style=style)


def generate_table_pdf(Qtns,r1,r2,r3):
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.add_page()

    # Register Arial Unicode 
    pdf.add_font("ArialUnicodeMS", "", font_files + "ARIALUNI.ttf", uni=True)
    pdf.add_font("ArialUnicodeMS", "B", font_files + "ARLRDBD.ttf", uni=True)

    # Default font
    pdf.set_font("ArialUnicodeMS", "", 9)

    print("fonts:", pdf.fonts)  # should show arialunicodems and arialunicodemsB

    # Build table
    build_table(pdf, "ICQ Question", Qtns)

    # Save PDF
    filename = f"icq_question_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, "reports", filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    pdf.output(file_path)

    pdf2 = FPDF(orientation="L", unit="mm", format="A4")
    pdf2.add_page()

    # Register fonts again
    pdf2.add_font("ArialUnicodeMS", "", font_files + "ARIALUNI.ttf", uni=True)
    pdf2.add_font("ArialUnicodeMS", "B", font_files + "ARLRDBD.TTF", uni=True)

    pdf2.set_font("ArialUnicodeMS", "", 9)

    build_dynamic_table(pdf2, "ICQ Question (All Columns)", Qtns,r1,r2,r3)

    filename2 = f"icq_question_all_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    file_path2 = os.path.join(settings.MEDIA_ROOT, "reports", filename2)
    os.makedirs(os.path.dirname(file_path2), exist_ok=True)
    pdf2.output(file_path2)

    return file_path,file_path2


def getICQSecQtnFinal(request):
    try:  
        api_url=getAPIURL()+"getICQSecQtnFinal/"       
         
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url,headers=header)
         
        api_data=response.json()
        return JsonResponse({'sections':api_data['sections']})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())


def saveICQRatingsFinal(request):
    try:       
  
        colDataLst = request.POST['colDataLst']
        uid=request.session['uid']
        # json_colDataLst = json.loads(colDataLst)
        # objreg=Register()
        # maxid=objmaster.getmaxICQId()
        # for colval in json_colDataLst:
        #     print('list is ' ,colval)
        #     objreg.updateICQRatingsFinal(colval["qtnId"],colval["ddl_yesno_"],colval["ddl_doc_"],colval["txt_comment_"],uid,maxid)
        api_url=getAPIURL()+"saveICQRatingsFinal/"       
        data_to_save={
            'colDataLst':colDataLst, 
            'uid':request.session['uid'], 
            } 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.post(api_url, data= json.dumps(data_to_save),headers=header)
         
        api_data=response.json()    
        return JsonResponse({'is_taken':api_data['is_taken']})
    except Exception as e:
        print('reqValidation is ',e)
        print('reqValidation traceback is ', traceback.print_exc())

def publushICQ(request):
    try:
        objmaster.publishICQ()
        return JsonResponse({"isvalid":"true"})
    except Exception as e:
        print('publushICQ is ',e)
        print('publushICQ traceback is ', traceback.print_exc()) 
        JsonResponse({"isvalid":"false"})


def getICQSections(request):
    try:    
        api_url=getAPIURL()+"getICQSections/"       
        data_to_save={ 
            'uid':request.session['uid'],} 
        header = {
        "Content-Type":"application/json",
	    'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
         
        response=response.json()
        return JsonResponse({'sections':response['sections']})
    except Exception as e:
        print('addSection is ',e)
        print('addSection traceback is ', traceback.print_exc()) 

def ICQFetchResidualRating(request): 
    inherendRisk =request.GET.get('inherendRisk', 'False')
    controleffect =request.GET.get('controleffect', 'False')
    api_url=getAPIURL()+"ICQFetchResidualRating/"       
    data_to_get={
        'inherendRisk':inherendRisk,             
        'controleffect':controleffect } 
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.get(api_url, data= json.dumps(data_to_get),headers=header)
    
    api_data=response.json()
    print("Apii daata",api_data)

    return JsonResponse(api_data)

def ICQ_Report(request):
    return render(request, 'ICQ_exportReportTxtEdV.html')

def get_Report_section_data(request):
    third_party_api_url = getAPIURL()+'GetICQReportData/'
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response_user = requests.get(third_party_api_url, headers=header)
    # print("response userlist",response_user.content)
    Rpt_icq_data = json.loads(response_user.content)
    print("Rpt_icq_data",Rpt_icq_data)
    df = pd.json_normalize(Rpt_icq_data['report_data'])
    print("check df",df)
    divSection = ""
    for index, row in df.iterrows(): 
        print("index",index,"row",row)
        divSection = divSection+"<div style='display: flex; justify-content: flex-start;'><div style='width:17px;'><i id='tggl_" + str(row["section_id"]) + "' class='bi bi-plus-square'' style='margin-right:5px;cursor:pointer;' onclick='toggleHeight("+str(row["section_id"]) +",this.id)'></i></div><div style='width:20px;'><i class='bi bi-pencil-square' style='margin-right:5px;cursor:pointer;'  title='Edit comment' onclick='getData("+str(row["section_id"]) +")'></i> </div><div id='div_" + str(row["section_id"]) + "' style='height:20px;overflow:hidden;'>"+ str(row["comment"])+"</div></div>"


        data = {
            'df':divSection,
        }
    return JsonResponse(data)


def ICQ_getSavedReportDataNew(accessToken): 
    # SummaryDataFiles = file_path + file_name + "_SummaryData.csv" 
    print("ICQ_getSavedReportDataNew")
    ####
    third_party_api_url = getAPIURL()+'GetICQReportData/'
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+accessToken
    }

    responseget = requests.get(third_party_api_url,headers=header)
    print("responseget show------------------",json.loads(responseget.content))
    data = json.loads(responseget.content)
    
    df = pd.json_normalize(data['report_data'])
    
    newTitles=[]
    divSection = ""
    
    for index, row in df.iterrows(): 
        divSection = divSection+"<div style='display: flex; justify-content: flex-start;'><div style='width:17px;'><i id='tggl_" + str(row["section_id"]) + "' class='bi bi-plus-square'' style='margin-right:5px;cursor:pointer;' onclick='toggleHeight("+str(row["section_id"]) +",this.id)'></i></div><div style='width:20px;'><i class='bi bi-pencil-square' style='margin-right:5px;cursor:pointer;'  title='Edit comment' onclick='getData("+str(row["section_id"]) +")'></i> </div><div id='div_" + str(row["section_id"]) + "' style='height:20px;overflow:hidden;'>"+ str(row["comment"])+"</div></div>"
                
    return divSection,newTitles

def ICQ_savereportcontent(request): 
    print("ICQ_savereportcontent",request.POST)
    comments =request.POST.get('comment', 'False') 
    reqId = request.POST.get('reqId','False') 
    
    third_party_api_url = getAPIURL()+'ICQ_ReportContentAPI/'
    data_to_save = {
        'icq_section_id':reqId,
        'comment':comments,
        'added_by':request.session['uid']
    }
    header = {
    "Content-Type":"application/json",
    'Authorization': 'Token '+request.session['accessToken']
    }
    response = requests.post(third_party_api_url, data= json.dumps(data_to_save),headers=header)
    data=json.loads(response.content) 
    print("data",data)

    savedData,newTtl = ICQ_getSavedReportDataNew(request.session['accessToken'])
    print('savedData ICQ ', savedData)
    data = {
        'is_taken': True,
        'reqId': str(reqId), 
        'savedReportData': savedData,
        'msg':data['msg']
    }
    return JsonResponse(data)


#ICQ Export PDF
font_files = os.path.join(BASE_DIR, 'static/fonts/')
def ICQaddSummarynCommentsHTMLNew(pdf, document, columnPageIdx, edaPageIdx, modelsPageIdx,mdl_id,accessToken):

    ####
    try:
        third_party_api_url = getAPIURL()+'GetICQReportData/'
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+accessToken
        }

        responseget = requests.get(third_party_api_url,headers=header)
        # print("responseget------------------ ",responseget.content)
        data = json.loads(responseget.content)
        # df = pd.DataFrame(data['df'])
        df = pd.json_normalize(data['report_data'])
        print("df-------------",df)
        ###
        
        for index, row in df.iterrows():
            print("row-------",row)
            pdf, linkArr, valFindingsLinkIdx, pageNoArr, columnPageIdx, edaPageIdx, modelsPageIdx = ICQaddTableofContents(
                pdf, df, document, valFindingsLinkIdx, columnPageIdx, edaPageIdx, modelsPageIdx)
            x, y = 10, pdf.get_y()
            if(str(row["comment"]) != "-"):
                
                y = pdf.get_y()
                # print('y at start is ',y)
                pdf.set_xy(x, y)
                pdf.add_font("ArialUnicodeMS", "",
                                font_files + "ARIALUNI.ttf", uni=True)
                pdf.set_font('ArialUnicodeMS', '', 9)
                # ##pdf.set_font("Arial",  size=9)
                pdf.set_text_color(0.0, 0.0, 0.0)
                pdf.set_left_margin(10)
                # pdf.set_link(linkArr[index], y, pdf.page_no())
                encdStr = str(row["comment"]).replace(
                    'src="/static', 'src="static').replace('height="24"', 'height="20"')
                 
                encdStr=encdStr.replace('\\','/')
                encdStr=encdStr.replace('/static','static')
                encdStr = str(encdStr.encode('utf-8'), 'utf-8')
                commentstr = ""
                import re
                tblLst = re.findall(
                    '<div class="appTblsss" id="', encdStr) 
                for match in re.finditer('<div class="appTblsss" id="', encdStr):
                    print('match is ', match)

                tbl_index = -1
                # print('encdStr is ',encdStr)
                if '<div class="appTblsss" id="'.lower() in encdStr.lower():
                    tbl_index = encdStr.index(
                        '<div class="appTblsss" id="')
                    print('tbl_index is ',tbl_index)
                    try:
                        tblid_index = encdStr.index('"><table style=', tbl_index)
                    except Exception as e:
                        tblid_index = encdStr.index('"><table width=', tbl_index)
                    # print('tblid_index ', tblid_index)
                    # print(' tableId is ', encdStr[(tbl_index+27):tblid_index])
                    table_ID = encdStr[(tbl_index+27):tblid_index]
                    tblend_index = encdStr.index(table_ID+'End"')
                    tblend_index = tblend_index+17+len(table_ID)
                # print('tblend_index is ', tblend_index)
                itr = 0
                # print('coment after replacing the table is ',
                #       encdStr[:tbl_index] + "" + encdStr[tblend_index:])
                # print('len of encdStr ', len(encdStr))
                while itr < len(encdStr):
                    # for itr in range(len(encdStr)):
                    # print('itr is ', itr)
                    if tbl_index == itr:
                        y = pdf.get_y()
                        x = 10
                        pdf.set_xy(x, y)
                        pdf.set_font('Arial', '', 9)
                        pdf.write_html(commentstr) 
                        commentstr = ""
                        print('table_ID is ',table_ID)
                        addTabletoRpt(pdf, table_ID)
                        itr = tblend_index
                        print('added here  1', commentstr)
                    elif(checkSymbol(encdStr[itr:itr+1]) == False):
                        commentstr += encdStr[itr:itr+1]

                    else:
                        # print('commentstr ', commentstr)
                        pdf.set_font('Arial', '', 9)
                        pdf.write_html(commentstr)
                        y = pdf.get_y()
                        x = pdf.get_x()
                        # print('x before cell', pdf.get_x(), pdf.get_y())
                        pdf.set_xy(x, y)
                        pdf.set_font('ArialUnicodeMS', '', 9)
                        pdf.cell(2, 5, encdStr[itr:itr+1])
                        y = pdf.get_y()
                        x = pdf.get_x()
                        # print('x,y  ', pdf.get_x(), pdf.get_y())
                        # print('added here  2',commentstr)
                        commentstr = ""
                    itr += 1
                if len(encdStr) == itr and commentstr != "":
                    # print('commentst at end is ', commentstr)
                    # print('y at srite html is ',y)                        
                    pdf.set_font('Arial', '', 9)
                    pdf.write_html(commentstr)
                    y = pdf.get_y()
                    x = pdf.get_x()
                    # print('added here  3',commentstr,' y is ',y)
                    commentstr = "" 
                y = pdf.get_y()+5
                pdf.set_xy(x, y)
                pdf.multi_cell(0, 5, "", align='L')
            else:
                y = pdf.get_y()
                # print('y at start is ',y)
                pdf.set_xy(x, y)
                pdf.add_font("ArialUnicodeMS", "",
                                font_files + "ARIALUNI.ttf", uni=True)
                pdf.set_font('ArialUnicodeMS', '', 9)
                # ##pdf.set_font("Arial",  size=9)
                pdf.set_text_color(0.0, 0.0, 0.0)
                pdf.set_left_margin(10)
                # pdf.set_link(linkArr[index], y, pdf.page_no())
                commentstr = "<b>"+ str(row["lbl_idx"]) + ' '+ str(row["lbl_txt"]).replace(
                    'src="/static', 'src="static').replace('height="24"', 'height="20"') +"</b>"                               
                pdf.set_font('Arial', '', 9)
                pdf.write_html(commentstr)
                y = pdf.get_y()
                x = pdf.get_x()
                # print('added here  3',commentstr,' y is ',y)
                commentstr = "" 
                y = pdf.get_y()+5
                pdf.set_xy(x, y)
                pdf.multi_cell(0, 5, "", align='L')
        return pdf, columnPageIdx, edaPageIdx, modelsPageIdx
    except Exception as e:
        print("report error is",e)

from fpdf import FPDF, HTMLMixin    
class MyFPDF(FPDF, HTMLMixin):
    pass

def ICQgenerateReportTxtEd(request):

    try: 
        print("request_data _report",request.GET)
        mdl_id=request.session['vt_mdl']
        # template_name = request.GET.get('template_name')
        # print("template_name",template_name)
        # a variable pdf
        pdf = MyFPDF()
        document = Document()
        section = document.sections[0]
        # Changing the orientation to landscape
        section.orientation = WD_ORIENT.LANDSCAPE

        # Printing the new orientation.
        columnPageIdx = -1  
        edaPageIdx = -1
        modelsPageIdx = -1

        # pdf.add_page('P')
        # pdf = addTitlenComments(pdf, document,mdl_id)

        # pdf.add_page('P')
        # addDocumentVesrionHistory(pdf, document)

        # #pdf = addCommentsnImgs(pdf)
        pdf.add_page('P')
        document.add_page_break()
        pdf, columnPageIdx, edaPageIdx, modelsPageIdx = ICQaddSummarynCommentsHTMLNew(
            pdf, document, columnPageIdx, edaPageIdx, modelsPageIdx,mdl_id,request.session['accessToken'])
        # pdf = addReferences(pdf)
        # pdf.add_page('P')
        # document.add_page_break()
        # pdf = addDocumentationComments(pdf, document,mdl_id)

        # pdf.add_page('P')
        # document.add_page_break()
        # pdf = addDataQuality(pdf, document,mdl_id)

        pdf.output(os.path.join(
            BASE_DIR, "static/media/ICQValidationReport_"+mdl_id+".pdf"))

        document.save(os.path.join(
            BASE_DIR, "static/media/demo.docx"))

        reportFilepath = os.path.join(
            BASE_DIR, "static/media/ValidationReport_"+mdl_id+".pdf")
        if os.path.exists(reportFilepath):
            # with open(reportFilepath, 'rb') as fh:
            #     response = HttpResponse(
            #         fh.read(), content_type="application/force-download")
            #     response['Content-Disposition'] = 'attachment; filename=' + \
            #         os.path.basename(reportFilepath)
            #     return response
            # from django.utils.encoding import smart_str

            # # mimetype is replaced by content_type for django 1.7
            # response = HttpResponse(content_type="application/force-download")
            # response['Content-Disposition'] = 'attachment; filename=' + \
            #     os.path.basename(reportFilepath)
            # response['X-Sendfile'] = smart_str(reportFilepath)
            # return response
            data = {"is_taken": True}
            return JsonResponse(data)
        raise Http404
    except Exception as e:
        print(e)
        print(traceback.print_exc())
        data = {"is_taken": False}
        return JsonResponse(data)

#added on 06.09.25 
def ICQaddTableofContents(pdf, df, document, valFindingsLinkIdx, columnPageIdx, edaPageIdx, modelsPageIdx):
    pdf.set_left_margin(32)
    pdf.add_page()
    document.add_page_break()
    x, y = 10, pdf.get_y()
    pdf.set_xy(x, y)
    pdf.set_font("Arial", size=9)
    pdf.set_text_color(0.0, 0.0, 0.0)
    pdf.cell(0, 5, "Table of Contents", align='L')
    linkArr = [0] * len(df)
    pageNoArr = [0] * len(df) 
    print('df-----------------',df)

    # print('df_new is', df)
    for index, row in df.iterrows():
        # if str(row["lbl_lvl"]) =='1':             
        y = pdf.get_y()+7
        pdf.set_xy(x, y)
        pdf.set_font("Arial", size=9)
        pdf.set_text_color(0.0, 0.0, 0.0)
        to_page = pdf.add_link()
        linkArr[index] = to_page
        pdf.cell((0, 5, str(row["section_label"])).encode(
            'utf-8', 'replace').decode('utf-8'), align='L', link=to_page) 
        # elif str(row["lbl_lvl"]) != '1':
        #     y = pdf.get_y()+7
        #     pdf.set_xy(x, y)
        #     pdf.set_font("Arial",  size=9)
        #     pdf.set_text_color(0.0, 0.0, 0.0)
        #     to_page = pdf.add_link()
        #     linkArr[index] = to_page
        #     pdf.cell(0, 5, "    "+str(row["lbl_idx"])+" "+str(row["lbl_txt"]).encode(
        #         'utf-8', 'replace').decode('utf-8'), align='L', link=to_page)
             
    return pdf, linkArr, valFindingsLinkIdx, pageNoArr, columnPageIdx, edaPageIdx, modelsPageIdx 

def generatepdf_ICQRatings(request):
    try: 
        return render(request, 'generate_pdf_icqratings.html',{ 'actPage':'Pdf Generation'})
    except Exception as e:
        print('adduser is ',e)
        print('adduser traceback is ',traceback.print_exc())

def generateReport_IcqRatings(request):
    try: 
        # a variable pdf
        pdf = FPDF(orientation = 'P', unit = 'mm', format='Legal')#PDF()
        document = Document()
        section = document.sections[0]
        # Changing the orientation to landscape
        section.orientation = WD_ORIENT.LANDSCAPE

        api_url=getAPIURL()+"ICQQtns/"       
        data_to_save={ 
            'uid':request.session['uid'],} 
        header = {
        "Content-Type":"application/json",
        'Authorization': 'Token '+request.session['accessToken']
        }
        response = requests.get(api_url, data= json.dumps(data_to_save),headers=header)
            
        api_data=response.json()
        print("Icq qtns api data",api_data['Qtns'])
        
        # pdf = addheaderpages(pdf)
    
        # pdf = generate_pdf_underwritting(pdf)

        # pdf = generate_pdf_pricing(pdf)

        # pdf = generate_pdf_marketing(pdf)

        pdf = generate_pdf_ICQRatings(pdf,api_data['Qtns'])

        pdf.output(os.path.join(
            BASE_DIR, "static/IcqRatings.pdf"))

        # document.save(os.path.join(
        #     BASE_DIR, "static/media/demo.docx"))

        # reportFilepath = os.path.join(
        #     BASE_DIR, "static/IcQRatingReport.pdf")
        # if os.path.exists(reportFilepath):
            
        return JsonResponse({'msg':"PDF Generated successfully"})
        
    except Exception as e:
        print(e)
        print(traceback.print_exc())
        data = {"is_taken": True}
        return JsonResponse(data)

def generate_pdf_ICQRatings(pdf,datalist):

    # print("datalist check",datalist)
            
    x,y=25,10 
    utility = 'ICQ Ratings Report'
    pdf.set_auto_page_break(auto=True,margin = 15) 
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, utility, border=0, ln=1, align="C")
    pdf.ln(5)  # Add a small vertical space
    

    counter = 0
    for key, val in datalist.items():
        print("key--------",key)

        # x,y=25,50 
        # utility = 'ICQ Ratings Report'
        # counter += 1
        if int(key) % 2 == 0:
            pdf.add_page()
            x,y=25,10 
            print('page added')
        # pdf.set_font("Arial", "B", 12)
        # pdf.cell(0, 10, utility, border=0, ln=1, align="C")
        # pdf.ln(0)  # Add a small vertical space
        
        print("val---------------------",val)
        if val['Sub_Sub_Section_Label'] != '':
            #1 row
            x,y=pdf.get_x(),pdf.get_y()
            pdf.set_xy(x, y) 
            pdf.set_font  ("Arial", "B", size=9)
            pdf.set_fill_color(255, 255, 255)
            y = pdf.get_y()#+10
            pdf.set_xy(10, y)
            pdf.multi_cell(35,10, "Q. NO",
                    1, fill=True, align='C')
            pdf.set_xy(45, y)
            pdf.multi_cell(155,10, "Question",
                    1, fill=True, align='C')
            
            #11 
            y=pdf.get_y()
            pdf.set_xy(x, y) 
            pdf.set_font("Arial", "B", size=9)
            pdf.set_fill_color(255, 255, 255)
            y = pdf.get_y()#+10    
            pdf.set_font("Arial",size=9)
            pdf.set_xy(10, y)
            pdf.cell(35, 10, val['qtnNo'],
                    1, fill=True, align='C')
            pdf.set_xy(45, y)
            pdf.cell(155, 10, val['Sub_Sub_Section_Label'],
                    1, fill=True, align='C')
            
        elif val['Sub_Section_Label'] != '':
            #1 row
            x,y=pdf.get_x(),pdf.get_y() 
            pdf.set_xy(x, y) 
            pdf.set_font  ("Arial", "B", size=9)
            pdf.set_fill_color(255, 255, 255)
            y = pdf.get_y()#+10
            pdf.set_xy(10, y)
            pdf.multi_cell(35,10, "Q. NO",
                    1, fill=True, align='C')
            pdf.set_xy(45, y)
            pdf.multi_cell(155,10, "Question",
                    1, fill=True, align='C')
            
            #11 
            y=pdf.get_y()
            pdf.set_xy(x, y) 
            pdf.set_font("Arial", "B", size=9)
            pdf.set_fill_color(255, 255, 255)
            y = pdf.get_y()#+10    
            pdf.set_font("Arial",size=9)
            pdf.set_xy(10, y)
            pdf.cell(35, 10, val['qtnNo'],
                    1, fill=True, align='C')
            pdf.set_xy(45, y)
            pdf.cell(155, 10, val['Sub_Section_Label'],
                    1, fill=True, align='C')

        elif val['Section_Label'] != '':
            #1 row
            x,y=pdf.get_x(),pdf.get_y() 
            pdf.set_xy(x, y) 
            pdf.set_font  ("Arial", "B", size=9)
            pdf.set_fill_color(255, 255, 255)
            y = pdf.get_y()#+10
            pdf.set_xy(10, y)
            pdf.multi_cell(35,10, "Q. NO",
                    1, fill=True, align='C')
            pdf.set_xy(45, y)
            pdf.multi_cell(155,10, "Question",
                    1, fill=True, align='C')
            
            #11 
            y=pdf.get_y()
            pdf.set_xy(x, y) 
            pdf.set_font("Arial", "B", size=9)
            pdf.set_fill_color(255, 255, 255)
            y = pdf.get_y()#+10    
            pdf.set_font("Arial",size=9)
            pdf.set_xy(10, y)
            pdf.cell(35, 10, val['qtnNo'],
                    1, fill=True, align='C')
            pdf.set_xy(45, y)
            pdf.cell(155, 10, val['qtnsArr'],
                    1, fill=True, align='C')


        if val['qtnsArr'] != "":            
            #1 row
            x,y=pdf.get_x(),pdf.get_y()
            pdf.set_xy(x, y) 
            pdf.set_font  ("Arial", "B", size=9)
            pdf.set_fill_color(255, 255, 255)
            y = pdf.get_y()#+10
            pdf.set_xy(10, y)
            pdf.multi_cell(35,10, "Q. NO",
                    1, fill=False, align='C')
            pdf.set_xy(45, y)
            pdf.multi_cell(155,10, "Question",
                    1, fill=False, align='C')
            
            #11 
            y=pdf.get_y()
            pdf.set_xy(x, y) 
            pdf.set_font("Arial", "B", size=9)
            pdf.set_fill_color(255, 255, 255)
            y = pdf.get_y()#+10    
            pdf.set_font("Arial",size=9)
            pdf.set_xy(10, y)
            pdf.cell(35, 10, val['qtnNo'],
                1, fill=True, align='C')
            pdf.set_xy(45, y)
            pdf.cell(155, 10, val['qtnsArr'],
                1, fill=True, align='C')
            #2
            y=pdf.get_y()
            pdf.set_xy(x, y)
            pdf.set_font("Arial",  "B",size=9)
            pdf.set_fill_color(255, 255, 255)
            y = pdf.get_y()+10 
            pdf.set_xy(10, y)
            pdf.multi_cell(35,10, "",
                    1,fill=True, align='C')
            pdf.set_xy(45, y)
            pdf.multi_cell(35,10, "Yes/No/NA",
                    1,fill=True, align='C')
            pdf.set_xy(80, y)
            pdf.multi_cell(35, 10, "Document References",1, fill=True, align='C')
            pdf.set_xy(115, y)
            pdf.multi_cell(85, 10,"Comments" , 1,
                    fill=True, align='C')


            y=pdf.get_y()
            pdf.set_xy(x, y) 
            pdf.set_font("Arial", "B", size=9)
            pdf.set_fill_color(255, 255, 255)
            y = pdf.get_y()#+10    
            pdf.set_font("Arial",size=9)
            pdf.set_xy(10, y)
            pdf.cell(35, 10, '',
                    1, fill=True, align='C')
            pdf.set_xy(45, y)
            pdf.cell(35, 10, str(val['Rating_Yes_NO']),
                    1, fill=True, align='C')
            pdf.set_xy(80, y)
            pdf.cell(35, 10,str(val['Doc_Yes_No']) ,
                    1, fill=True, align='C')
            pdf.set_xy(115, y)   ##
            pdf.multi_cell(85, 10,str(val['comments']) ,
                    1, fill=True, align='C')


            #3
            y=pdf.get_y()
            pdf.set_xy(x, y)
            pdf.set_font("Arial",  "B",size=9)
            pdf.set_fill_color(255, 255, 255)
            y = pdf.get_y()#+10 
            pdf.set_xy(10, y)
            pdf.multi_cell(35,10, "",
                    1,fill=True, align='C')
            pdf.set_xy(45, y)
            pdf.multi_cell(85,10, "Control Description",
                    1,fill=True, align='C')
            pdf.set_xy(130, y)
            pdf.multi_cell(35, 10, "Inherent Risk Rating",1, fill=True, align='C')
            pdf.set_xy(165, y)
            pdf.multi_cell(35, 5,"Control Effectiveness Ratings" , 1,
                    fill=True, align='C')


            y=pdf.get_y()
            pdf.set_xy(x, y) 
            pdf.set_font("Arial", "B", size=9)
            pdf.set_fill_color(255, 255, 255)
            y = pdf.get_y()#+10    
            pdf.set_font("Arial",size=9)
            pdf.set_xy(10, y)
            pdf.multi_cell(35,10, "",
                    1,fill=True, align='C')
            pdf.set_xy(45, y)
            pdf.cell(85, 10, str(val['Control_Description']),
                    1, fill=True, align='C')
            pdf.set_xy(130, y)
            pdf.cell(35, 10, str(val['Inherent_Risk_Rating']),
                    1, fill=True, align='C')
            pdf.set_xy(165, y)   ##
            pdf.multi_cell(35, 10, str(val['Control_Effectiveness_Ratings']),
                    1, fill=True, align='C')


            #4
            y=pdf.get_y()
            pdf.set_xy(x, y)
            pdf.set_font("Arial",  "B",size=9)
            pdf.set_fill_color(255, 255, 255)
            y = pdf.get_y()#+10
            pdf.set_xy(10, y)
            pdf.multi_cell(35,10, "",
                    1,fill=True, align='C') 
            pdf.set_xy(45, y)
            pdf.multi_cell(35,10, "Residual Ratings",
                    1,fill=True, align='C')
            pdf.set_xy(80, y)
            pdf.multi_cell(35, 5, "Residual Rating (Manual)",1, fill=True, align='C')
            pdf.set_xy(115, y)
            pdf.multi_cell(85, 10,"Mitigating Factor" , 1,
                    fill=True, align='C')


            y=pdf.get_y()
            pdf.set_xy(x, y) 
            pdf.set_font("Arial", "B", size=9)
            pdf.set_fill_color(255, 255, 255)
            y = pdf.get_y()#+10    
            pdf.set_font("Arial",size=9)
            pdf.set_xy(10, y)
            pdf.multi_cell(35,10, "",
                    1,fill=True, align='C')
            pdf.set_xy(45, y)
            pdf.cell(35, 10, str(val['Residual_Ratings']),
                    1, fill=True, align='C')
            pdf.set_xy(80, y)
            pdf.cell(35, 10, str(val['override_residual_ratings']),
                    1, fill=True, align='C')
            pdf.set_xy(115, y)   ##
            pdf.multi_cell(85, 10, str(val['override_comments']),
                    1, fill=True, align='C')

    return pdf 




