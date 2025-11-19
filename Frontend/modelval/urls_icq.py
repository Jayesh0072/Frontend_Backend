from django.urls import path 

from . import icq
from . import flviews
urlpatterns = [

    ##ICQ Questionnaire
    path('ICQQtnsFinal/',icq.ICQQtnsFinal,name='ICQQtnsFinal'),
    path('getICQSecQtnFinal/',icq.getICQSecQtnFinal,name='getICQSecQtnFinal'),
    path('saveICQRatingsFinal/',icq.saveICQRatingsFinal,name='saveICQRatingsFinal'),
    path('publushICQ/',icq.publushICQ,name='publushICQ'),
    path('getICQSections/',icq.getICQSections,name='getICQSections'),
    path('ICQFetchResidualRating/',icq.ICQFetchResidualRating,name='ICQFetchResidualRating'),
    path('generate_icq_pdf/',icq.generate_icq_pdf,name='generate_icq_pdf'),

    path('FLending/',flviews.FLeanding,name='FLending'),

    ##ICQ Allocation
    path('allocate_icq/',icq.allocate_icq,name='allocate_icq') , # type: ignore
    path('save_allocation/',icq.save_allocation,name='save_allocation') ,
    path('section_save_comment/',icq.section_save_comment,name='section_save_comment') ,
    path('fetch_section_comment/',icq.fetch_section_comment,name='fetch_section_comment') ,
    path('getsectionQtnResp/',icq.getsectionQtnResp,name='getsectionQtnResp') ,
    # Jayesh
    path('ICQ_Report/',icq.ICQ_Report,name='ICQ_Report'),
    path('get_Report_section_data/',icq.get_Report_section_data,name='get_Report_section_data'),
    path('ICQ_savereportcontent/',icq.ICQ_savereportcontent,name='ICQ_savereportcontent'),
    path('ICQgenerateReportTxtEd/',icq.ICQgenerateReportTxtEd,name='ICQgenerateReportTxtEd'),
    path('generatepdf_ICQRatings/',icq.generatepdf_ICQRatings,name='generatepdf_ICQRatings') ,
    path('generateReport_IcqRatings/',icq.generateReport_IcqRatings,name='generateReport_IcqRatings') ,
    
]