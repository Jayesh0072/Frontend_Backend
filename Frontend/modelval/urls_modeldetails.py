from django.urls import path 

from . import modeldetails

urlpatterns = [

    path('modelDetails/',modeldetails.modelDetails,name='modelDetails'),

    path('validation_planning/',modeldetails.validation_planning,name='validation_planning'),
    path('SaveValidationPlanning/',modeldetails.SaveValidationPlanning,name='SaveValidationPlanning'),
    path('check_validated_or_not/',modeldetails.check_validated_or_not,name='check_validated_or_not'),
    path('CurrentValidation/',modeldetails.CurrentValidation,name='CurrentValidation'),
    path('fetch_val_freq/',modeldetails.fetch_val_freq,name='CurrentValidation'),
    
]


