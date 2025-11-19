
from xml.dom.minidom import TypeInfo
from django.shortcuts import render ,redirect
from django.http import HttpResponse 
import pandas as pd
from pycaret.datasets import get_data
import shap
import sklearn
from sklearn.model_selection import train_test_split
import pycaret
from datetime import date
import os
from pathlib import Path
import json
from django.core.files.storage import FileSystemStorage
import pycaret
import traceback  
from pycaret.classification import *
import matplotlib.pyplot as plt
import vaex as vx 
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import VotingClassifier, AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier, BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import VotingClassifier, AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier, BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from statsmodels.stats.outliers_influence import variance_inflation_factor
from typing import Reversible
from sklearn import preprocessing
from sklearn.feature_selection import SelectPercentile, chi2, RFE
from sklearn.preprocessing import StandardScaler, label_binarize
from sklearn.model_selection import train_test_split, RandomizedSearchCV, GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.metrics import _classification, classification_report, roc_curve, auc, roc_auc_score, confusion_matrix, recall_score, precision_score, accuracy_score
import seaborn as sns
from scipy.stats import ks_2samp
from scipy import stats
from scipy.stats import randint as sp_randint 
from .models import descData, lstCnfrmSrc, lstOutlieranomalies, missingDataList, lstColFreq, lstOutlierGrubbs,lstTestModelPerf,SavedModels
from django.http import JsonResponse 
import numpy as np 
import shutil
# Create your views here.
from pymongo import MongoClient
file_path2 ='static/prediction_files/'
import datetime 
import joblib

# mongodb set up
import environ
env = environ.Env()
# reading .env file
environ.Env.read_env()
# mongodb set up
cluster=MongoClient('localhost',27017,connect=False)
dbname=env("MongoDB_NM")
db=cluster[dbname]
collection=db["SrcData"]
collection_file_info=db["SrcFileInfo"]
collection_target=db["TargetData"]
collection_process_status=db["ProcessStatus"]
collection_model_information=db["ModelInformation"]
collection_model_risk=db["ModelRisk"]
collection_model_documents=db["ModelDocuments"]
collection_model_process_status=db['ProcessStatus']
collection_model_target_value=db['TargetValue']
collection_model_chart_image=db['ChartImage']
collection_model_implementation_control=db['ImplementationControls']
collection_conceptual_soundness=db['ConceptualSoundness']
collection_data_integrity=db['DataIntegrity']
collection_confirm_data_source=db['DataSource']
collection_pyconfig=db['PyConfig']
collection_comparemodels=db['CompareModels']
collection_Chartimg=db['Chartimg']
BASE_DIR = Path(__file__).resolve().parent.parent
# Create your views here.
user_name = "user1"
file_path = os.path.join(BASE_DIR, 'static/csv_files/')
file_name =user_name 
processingFile_path='static/reportTemplates/processing.csv' 

plot_dir='/static/media/'
plot_dir_view='static/media/'


src_files='static/cnfrmsrc_files/'
mail_pwd="sxovbflfjwhgssvx"
savefile_name = file_path +  "csvfile_user1.csv"  

param_file_name = "paramfile_"+user_name
param_file_path = os.path.join(BASE_DIR, 'static/param_files/')

def setuppycaret(request):
    try:
        print('inside setuppycaret')
         
        return render(request, 'pycaretsetup.html',{'dataTypes': dropfeatures(request.session['vt_mdl'],request.session['vt_dataset'] )})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 

root_path = "C://Chen_project//project1//"


def dropfeatures(vt_mdl,vt_dataset):
    try:
        # savefile_x = file_path + file_name + "_x.csv"
        _isDisabled="disabled"
        file_id=find_max_file_id(vt_mdl)
        dataset=vt_dataset
        df=find_src_data(file_id,dataset)
        targetVar =find_target_value(file_id)  
        if(not (targetVar=="None")):
            df = df.drop(targetVar, axis=1)
        # x = pd.read_csv(savefile_x, na_values='?')
        gridDttypes = []
        cols = df.columns
        x_categori = pd.DataFrame(df, columns=cols)
        for col in x_categori.columns:
            objlstColFreq = lstColFreq()
            col_count = x_categori[col].value_counts()
            # print(dict(col_count))

            objlstColFreq.colName = col
            objlstColFreq.freqVal = dict(col_count)
            objlstColFreq.total_rows = x_categori[col].count()
            objlstColFreq.missing_rows = len(
                x_categori[col])-x_categori[col].count()
            gridDttypes.append(objlstColFreq)

        # print('gridDttypes is ',gridDttypes)
        return  gridDttypes 

    except Exception as e:
        print('eror is',e,' stacktrace is  ',traceback.print_exc()) 

def saveConfig(request): 
    try:
        from multiprocessing import Process, Pipe  
        train_size=request.GET.get('train_size', 'False') 
        categorical_imputation=request.GET.get('categorical_imputation', 'False')  
        numeric_imputation =request.GET.get('numeric_imputation', 'False') 
        ignore_features =request.GET.get('ignore_features', 'False') 
        normalize_method=request.GET.get('normalize_method', 'False') 
        transformationmethod=request.GET.get('transformationmethod', 'False') 
        transformtargetmethod=request.GET.get('transformtargetmethod', 'False')  
        multicollinearity_threshold=request.GET.get('multicollinearity_threshold', 'False') 
        outliers_threshold=request.GET.get('outliers_threshold', 'False') 
        polynomial_degree=request.GET.get('polynomial_degree', 'False') 
        fix_imbalance=request.GET.get('fix_imbalance', 'False') 
        remove_outliers =request.GET.get('remove_outliers', 'False') 
        normalize=request.GET.get('normalize', 'False') 
        transformation=request.GET.get('transformation', 'False') 
        transform_target=request.GET.get('transform_target', 'False') 
        remove_multicollinearity=request.GET.get('remove_multicollinearity', 'False') 
        feature_interaction=request.GET.get('feature_interaction', 'False') 
        feature_ratio=request.GET.get('feature_ratio', 'False') 
        polynomial_features=request.GET.get('polynomial_features', 'False') 
        trigonometry_features=request.GET.get('trigonometry_features', 'False') 
        
        
        i=0
        df = pd.DataFrame(
            columns=['train_size', 'categorical_imputation','numeric_imputation','ignore_features','normalize','normalize_method',
            'fix_imbalance','transformation','transformation_method','transform_target','transform_target_method','remove_outliers','outliers_threshold',
            '','','','','','','','','','','','',''])
        if len(train_size)<1:
            train_size="0.7"
        # df.loc[i] = ['train_size',train_size]
        # i=i+1
        # df.loc[i] = ['categorical_imputation',"'"+ categorical_imputation +"'"]
        # i=i+1
        # df.loc[i] = ['numeric_imputation',"'"+ numeric_imputation +"'"]
        # i=i+1
        if len(ignore_features)<1:
            ignore_features="None"
        else:
            ignore_features = ignore_features.split(",")
        # df.loc[i] = ['ignore_features',ignore_features]
        # i=i+1
        # df.loc[i] = ['normalize',normalize]
        # i=i+1
        # df.loc[i] = ['normalize_method',"'"+normalize_method+"'"]
        # i=i+1
        # df.loc[i] = ['fix_imbalance',fix_imbalance]
        # i=i+1
        # df.loc[i] = ['transformation',transformation]
        # i=i+1
        # df.loc[i] = ['transformation_method',"'"+transformationmethod+"'"]
        # i=i+1
        # df.loc[i] = ['transform_target',transform_target]
        # i=i+1
        # df.loc[i] = ['transform_target_method',"'"+transformtargetmethod+"'"]
        # i=i+1
        # df.loc[i] = ['remove_outliers',remove_outliers]
        # i=i+1
        # df.loc[i] = ['outliers_threshold',outliers_threshold]
        # i=i+1
        # df.loc[i] = ['remove_multicollinearity',remove_multicollinearity]
        # i=i+1
        # df.loc[i] = ['multicollinearity_threshold',multicollinearity_threshold]
        # i=i+1
        # df.loc[i] = ['feature_interaction',feature_interaction]
        # i=i+1
        # df.loc[i] = ['feature_ratio',feature_ratio]
        # i=i+1
        # df.loc[i] = ['polynomial_features',polynomial_features]
        # i=i+1
        # df.loc[i] = ['polynomial_degree',polynomial_degree]
        # i=i+1
        # df.loc[i] = ['trigonometry_features',trigonometry_features] 
        if len(train_size)<1:
            train_size="0.7" 
        df = pd.DataFrame([[request.session['vt_mdl'],str(request.session['uid']),train_size , categorical_imputation  , numeric_imputation  ,ignore_features 
        ,normalize , normalize_method  ,fix_imbalance ,transformation , transformationmethod  ,transform_target
         , transformtargetmethod ,remove_outliers ,outliers_threshold ,remove_multicollinearity ,multicollinearity_threshold
         ,feature_interaction ,feature_ratio ,polynomial_features ,polynomial_degree ,trigonometry_features]] ,
            columns=['mdl_id','user_id','train_size', 'categorical_imputation','numeric_imputation','ignore_features'
            ,'normalize','normalize_method','fix_imbalance','transformation','transformation_method','transform_target'
            ,'transform_target_method','remove_outliers','outliers_threshold',
            'remove_multicollinearity','multicollinearity_threshold','feature_interaction','feature_ratio','polynomial_features','polynomial_degree','trigonometry_features'])
         # df.to_csv( file_path + user_name + "_pyconfig.csv", index=False, encoding='utf-8')

        if collection_pyconfig.find_one({'mdl_id':request.session['vt_mdl'],'user_id':str(request.session['uid'])}):
            collection_pyconfig.delete_many({'mdl_id':request.session['vt_mdl'],'user_id':str(request.session['uid'])})
            collection_pyconfig.insert_many(df.to_dict('records'))
        else:
            collection_pyconfig.insert_many(df.to_dict('records'))
        print('ignore_features is ',ignore_features )
        return JsonResponse({"is_taken":"True"})
    except Exception as e:
        print('eror is',e,' stacktrace is  ',traceback.print_exc())


def cmpmodels(request):
    try: 
        # print('inside cmpmodels',request.method)
        # gridDttypes=[]
        # result=[]
        print("request.session",request.session.items())
        vt_mdl='M050100'
        # dataset_a = {'$and': [{'file_id': 5}, {'$and': [{'Number of times pregnant': 3}, {'Triceps skin fold thickness (mm)': 10}]}]}
        msg=""
        # file_id=find_max_file_id(request.session['vt_mdl'])
        file_id=find_max_file_id(vt_mdl)
        dataset=request.session['vt_dataset'] 
        # dataset = dataset_a

        df=find_src_data(file_id,dataset)
        dfConfig=find_pyconfig(request.session['vt_mdl'],str(request.session['uid']))
        if request.method=='GET':
            if len(df)>0: #os.path.exists(savefile_name):
                if len(dfConfig)>0: #os.path.exists(file_path + user_name + "_pyconfig.csv"):
                    if(len(df)>1000): 
                        ind = np.random.choice(len(df),1000,replace=False)
                        df = df.iloc[ind,:] 
                    targetVar =find_target_value(file_id) 
                    print("targetvar",type(targetVar))
                    if targetVar == "None":
                        print('Please Select Target Variable')
                        msg="Please Select Target Variable."
                    else:
                        print("target variable not None") 
                        # return render(request, 'comparemodels.html',  {'dataTypes': gridDttypes, 'df': result,'msg':msg})
                else:
                    print('pycaret config does not exist')
                    msg="Please complete data preparation."
            else:
                print('file does not exist')
                msg="Please import data."
        return render(request, 'comparemodels.html',{'msg':msg})
    except Exception as e:
        print('setuppycaret error is ',e,traceback.print_exc()) 


def getrebestmodelsut(request):
    try: 
        print('inside cmpmodels',request.method)
        gridDttypes=[]
        result=[]
        msg=""
        print("MDL id",request.session['vt_mdl'])
        file_id=find_max_file_id(request.session['vt_mdl'])
        print("file_id--------------------------",file_id)
        dataset=request.session['vt_dataset'] 
        df=find_src_data(file_id,dataset)
        dfConfig=find_pyconfig(request.session['vt_mdl'],str(request.session['uid']))
        if request.method=='GET':
            if  len(df)>0:
                if len(dfConfig)>0:
                    if(len(df)>1000):
                        ind = np.random.choice(len(df),1000,replace=False)
                        df = df.iloc[ind,:] 
                     
                    targetVar =find_target_value(file_id) 
                     
                    print("targetvar",type(targetVar),targetVar)
                    if targetVar == "None":
                        print('Please Select Target Variable')
                        msg="Please Select Target Variable."
                    else:
                        print("target variable not None")
                        for index, row in dfConfig.iterrows():    
                            print('row["normalize"] is ',   row["normalize"]  )               
                        # clf=setup(data = df, target = 'status', train_size = 0.7,html=False,silent=True,normalize = False, transformation = False )
                            clf=setup(data = df, target = targetVar, html=False,silent=True,           
                            train_size=float(row["train_size"]), categorical_imputation=eval("'" +row["categorical_imputation"] +"'"),
                            numeric_imputation =eval("'"+row["numeric_imputation"]+"'"),ignore_features =eval(row["ignore_features"])
                            ,normalize =eval(row["normalize"]) ,normalize_method=eval("'"+ row["normalize_method"] +"'"),
                            remove_outliers=eval(row["remove_outliers"]) ,outliers_threshold =float(row["outliers_threshold"]),
                            remove_multicollinearity =eval(row["remove_multicollinearity"]),multicollinearity_threshold=float(row["multicollinearity_threshold"]),
                            feature_interaction=eval(row["feature_interaction"]) ,feature_ratio=eval(row["feature_ratio"])
                            ,polynomial_features =eval(row["polynomial_features"]),polynomial_degree=int(row["polynomial_degree"]) ,trigonometry_features=eval(row["trigonometry_features"]) 
                            ,fix_imbalance=eval(row["fix_imbalance"])
                            )
                            #  transform_target =row["transform_target"], not working  transform_target_method=eval("'"+row["transform_target_method"]+"'"
                            #  
                            #
                            # ,feature_interaction=row["feature_interaction"] ,feature_ratio=row["feature_ratio"]
                            # ,polynomial_features =row["polynomial_features"],polynomial_degree=row["polynomial_degree"] ,trigonometry_features=row["trigonometry_features"] )
                            try:
                                best = compare_models()
                            except Exception as e:
                                print('compare_models error is ',e) 

                            dfmodels = pull()
                            
                            gridDttypes = []
                            dttypes = dict(dfmodels.dtypes)
                            # print(dttypes)
                            for key, value in dttypes.items():
                                gridDttypes.append({'colName': key, 'dataType': value})
                            result = dfmodels.to_json(orient="records")
                            result = json.loads(result)
                            print('gridDttypes is ',gridDttypes)
                            # dfmodels.reset_index(level=0, inplace=True)
                            dfmodels['mdl_id']=request.session['vt_mdl']
                            dfmodels['user_id']=str(request.session['uid'])
                            # dfmodels['modelSN'] = dfmodels.index
                            dfmodels.insert(0,'modelSN', dfmodels.index )
                            # dfmodels.to_csv( file_path + user_name + "_comparemodels.csv", index=True, encoding='utf-8')
                            # 
                            if collection_comparemodels.find_one({'mdl_id':request.session['vt_mdl'],'user_id':str(request.session['uid'])}):
                                collection_comparemodels.delete_many({'mdl_id':request.session['vt_mdl'],'user_id':str(request.session['uid'])})
                                collection_comparemodels.insert_many(dfmodels.to_dict('records'))
                            else:
                                collection_comparemodels.insert_many(dfmodels.to_dict('records'))
                            print('file saved') 
                            del dfmodels
                        del df
                        # return render(request, 'comparemodels.html',  {'dataTypes': gridDttypes, 'df': result,'msg':msg})
                else:
                    print('pycaret config does not exist')
                    msg="Please complete data preparation."
            else:
                print('file does not exist')
                msg="Please import data."
        return JsonResponse({'df': result,'msg':msg})
    except Exception as e:
        print('setuppycaret error is ',e)
        print('stacktrace is ',traceback.print_exc())

def runBestModel(request):
    try: 
        msg=""
        gridDttypes=[]
        result=[]
        lendf=""
        file_id=find_max_file_id(request.session['vt_mdl'])
        dataset=request.session['vt_dataset'] 
        df=find_src_data(file_id,dataset)
        dfConfig=find_pyconfig(request.session['vt_mdl'],str(request.session['uid']))
        if len(df)>0:
            lendf=len(df)
            if len(dfConfig)>0:           
                dfmodels =find_comparemodels(request.session['vt_mdl'],str(request.session['uid']))               
                result = dfmodels.to_json(orient="records")
                result = json.loads(result)  
                gridDttypes = []
                dttypes = dict(dfmodels.dtypes)
                # print(dttypes)
                for key, value in dttypes.items():
                    gridDttypes.append({'colName': key, 'dataType': value})
                result = dfmodels.to_json(orient="records")
                result = json.loads(result)        
                del dfmodels
            else:
                print('pycaret config does not exist')
                msg="Please complete data preparation."
        else:
            print('file does not exist')
            msg="Please import data." 
        return render(request, 'runBestpycr.html',  {'dataTypes': gridDttypes, 'df': result,'msg':msg,'lendf':lendf})
    except Exception as e:
        print('setuppycaret error is ',e) 
        print(traceback.print_exc())

def runSelectedModel(request):
     
    try: 
        model =request.GET.get('model', 'False') 
        dataSize=request.GET.get('dataSize', '1000') 
        file_id=find_max_file_id(request.session['vt_mdl'])
        dataset=request.session['vt_dataset'] 
        df=find_src_data(file_id,dataset)
        dfConfig=find_pyconfig(request.session['vt_mdl'],str(request.session['uid']))
        if len(df)>0:
            if len(dfConfig)>0:
                
                ind = np.random.choice(len(df),int(dataSize),replace=False)
                df = df.iloc[ind,:]
                 
                 
                bestModel=model
                targetVar =find_target_value(file_id) 
                
                for index, row in dfConfig.iterrows():    
                    print('row["normalize"] is ',   row["normalize"]  )               
                # clf=setup(data = df, target = 'status', train_size = 0.7,html=False,silent=True,normalize = False, transformation = False )
                    clf=setup(data = df, target = targetVar, html=False,silent=True,           
                            train_size=float(row["train_size"]), categorical_imputation=eval("'" +row["categorical_imputation"] +"'"),
                            numeric_imputation =eval("'"+row["numeric_imputation"]+"'"),ignore_features =eval(row["ignore_features"])
                            ,normalize =eval(row["normalize"]) ,normalize_method=eval("'"+ row["normalize_method"] +"'"),
                            remove_outliers=eval(row["remove_outliers"]) ,outliers_threshold =float(row["outliers_threshold"]),
                            remove_multicollinearity =eval(row["remove_multicollinearity"]),multicollinearity_threshold=float(row["multicollinearity_threshold"]),
                            feature_interaction=eval(row["feature_interaction"]) ,feature_ratio=eval(row["feature_ratio"])
                            ,polynomial_features =eval(row["polynomial_features"]),polynomial_degree=int(row["polynomial_degree"]) ,trigonometry_features=eval(row["trigonometry_features"]) 
                            ,fix_imbalance=eval(row["fix_imbalance"])
                            )
                    #  transform_target =row["transform_target"], not working  transform_target_method=eval("'"+row["transform_target_method"]+"'"
                    best = create_model(bestModel)                      
                    joblib.dump(best, 'Temp_'+request.session['username'] +'.joblib')

                    plotOutput(best,bestModel,"Test")  
                    # context={'clsrpt':plot_dir_view+'//'+ user_name+ '_classification_report_'+bestModel+'_Test.png',
                    # 'auc':plot_dir_view+'//'+ user_name+ '_ROCAUC_'+bestModel+'_Test.png',
                    # 'cnfmtrx':plot_dir_view+'//'+ user_name+ '_Confusion_Matrix_'+bestModel+'_Test.png'}
                     
                    # return  render(request,"showModelOutputPycr.html")
                    # return redirect('showPycrOutputs') 
                del df,dfConfig 
            else:
                print('pycaret config does not exist')
        else:
            print('file does not exist')
        return JsonResponse({'run':'sucess'})
    except Exception as e:
        print('setuppycaret error is ',e) 
        print('stacktrace is ',traceback.print_exc())
        return JsonResponse({'run':'fail'})

def saveModel(request):
     
    try: 
        print("request 1",request.GET)
        model =request.GET.get('model', 'False') 
        print("select model jsh",model)
        model_id = request.session['vt_mdl']
        print("model_id",model_id)
        user_id = request.session['uid']
        print("user_id",user_id)
        ml_model_name = request.GET.get('ml_model_name','False')
        print("ml_model_name",ml_model_name)
        dataSize=request.GET.get('dataSize', '1000') 
        file_id=find_max_file_id(request.session['vt_mdl'])
        dataset=request.session['vt_dataset'] 
        print("dataset11",dataset)
        df=find_src_data(file_id,dataset)
        dfConfig=find_pyconfig(request.session['vt_mdl'],str(request.session['uid']))
        if len(df)>0:
            if len(dfConfig)>0:
                
                ind = np.random.choice(len(df),int(dataSize),replace=False)
                df = df.iloc[ind,:]
                 
                 
                bestModel=model
                targetVar =find_target_value(file_id) 
                
                for index, row in dfConfig.iterrows():    
                    print('row["normalize"] is ',   row["normalize"]  )               
                # clf=setup(data = df, target = 'status', train_size = 0.7,html=False,silent=True,normalize = False, transformation = False )
                    clf=setup(data = df, target = targetVar, html=False,silent=True,           
                            train_size=float(row["train_size"]), categorical_imputation=eval("'" +row["categorical_imputation"] +"'"),
                            numeric_imputation =eval("'"+row["numeric_imputation"]+"'"),ignore_features =eval(row["ignore_features"])
                            ,normalize =eval(row["normalize"]) ,normalize_method=eval("'"+ row["normalize_method"] +"'"),
                            remove_outliers=eval(row["remove_outliers"]) ,outliers_threshold =float(row["outliers_threshold"]),
                            remove_multicollinearity =eval(row["remove_multicollinearity"]),multicollinearity_threshold=float(row["multicollinearity_threshold"]),
                            feature_interaction=eval(row["feature_interaction"]) ,feature_ratio=eval(row["feature_ratio"])
                            ,polynomial_features =eval(row["polynomial_features"]),polynomial_degree=int(row["polynomial_degree"]) ,trigonometry_features=eval(row["trigonometry_features"]) 
                            ,fix_imbalance=eval(row["fix_imbalance"])
                            )
                    #  transform_target =row["transform_target"], not working  transform_target_method=eval("'"+row["transform_target_method"]+"'"
                    best = create_model(bestModel)  
                    print("temp_username",request.session['username'])
                  
                    dataset=request.session['vt_dataset'] 
                    print("dataset",dataset)
                    check_ml_model_name = SavedModels.objects.filter(ml_model_name = ml_model_name)  
                    if check_ml_model_name:
                        SavedModels.objects.filter(ml_model_name = ml_model_name).update(model_id = model_id,selected_model = model,dataset = dataset)
                    else:
                        model_obj = SavedModels(model_id = model_id,selected_model = model,ml_model_name = ml_model_name,user_id = user_id,dataset = dataset)
                        model_obj.save()
                del df,dfConfig 
            else:
                print('pycaret config does not exist')
        else:
            print('file does not exist')
        return JsonResponse({'run':'sucess'})
    except Exception as e:
        print('setuppycaret error is ',e) 
        print('stacktrace is ',traceback.print_exc())
        return JsonResponse({'run':'fail'})

def model_screen(request):
    print()
    try:  
        user_id = request.session['uid'] 
        print("user id",user_id)
        model_obj = SavedModels.objects.filter(user_id = user_id) 

        file_id=find_max_file_id(request.session['vt_mdl'])
        dataset=request.session['vt_dataset'] 
        df=find_src_data(file_id,dataset)
        print('len df columns ',df.columns) 
        return render(request, 'mlmodel.html',{'modelobj':model_obj})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 

def rename_filename(request):
    model =request.GET.get('model', 'False')  
    model_id = request.session['vt_mdl'] 
    user_id = request.session['uid']   
    dataset=request.session['vt_dataset'] 
    ml_model_name = request.GET.get('file_name', 'False')
     
    # path=os.path.join(BASE_DIR, plot_dir_view)
    check_ml_model_name = SavedModels.objects.filter(ml_model_name = ml_model_name)  
    if check_ml_model_name:
        SavedModels.objects.filter(ml_model_name = ml_model_name).update(model_id = model_id,selected_model = model,dataset = dataset)
    else:
        model_obj = SavedModels(model_id = model_id,selected_model = model,ml_model_name = ml_model_name,user_id = user_id,dataset = dataset)
        model_obj.save()
    os.rename('Temp_'+request.session['username'] +'.joblib' ,ml_model_name +'.joblib')
    data = {
        'msg':'ok'
    }
    return JsonResponse(data)

def loadModel(request):

    mdl_id = request.session['vt_mdl'] 
    if request.method == 'POST':  
        filename = request.POST.get('filenm','none')
        print(' filename ',filename)
        files = request.FILES
        myfile = files.get('filename', None)
        print('myfile ',myfile,' filename ',filename)
        if myfile=="":
            res = JsonResponse({'data':'Invalid Request'})
            return res
        else:     
            fs = FileSystemStorage() 
            filePath=os.path.join(BASE_DIR, file_path2+user_name+'_'+mdl_id+'_predictionfiles/',filename)
            if os.path.exists(filePath):
                os.remove(filePath)
                print("remove filename",filePath)
            fs.save(os.path.join(BASE_DIR, file_path2+user_name+'_'+mdl_id+'_predictionfiles/',filename), myfile) 
            
            if os.path.exists(filePath):
                uploaded_df = pd.read_csv(filePath, na_values='?')
                print("uploaded df lenght and col",len(uploaded_df),uploaded_df.columns)
            uploaded_df_len = len(uploaded_df)
            list1 = uploaded_df.columns.tolist()
            mdlname = request.POST.get('mdlname','False') 
            print("mdlname",mdlname)            
            dataset_obj = SavedModels.objects.get(ml_model_name = mdlname)
            dataset = dataset_obj.dataset
            file_id=find_max_file_id(request.session['vt_mdl'])
            df=find_src_data(file_id,dataset) 
            print("original df lenght and col",len(df),df.columns)
            original_df_len = len(df)
            list2 = df.columns.tolist()
            print("list ",list1,list2)
            if list1 == list2 and len(list1) == len(list2) :
                print("equal")
            else:
                print('validation')
                if len(list1) != len(list2):
                    return JsonResponse({"msg":"Numer of features in prediction data different than the data used for model training."})
                if list1 != list2:
                    missing_val = (set(list2).difference(list1))
                    missing_col = []
                    for col in missing_val:
                        missing_col.append(col)
                    print("missing columns",missing_col)
                    return JsonResponse({"msg":"Prediction data does not contain following features "+ ','.join(missing_col)})      
                #if number of columns mistch
                #Numer of columns  in prediction data different than the data used for model training.
                # elif 
                #compare list of df and uploadeddf
                #show the columns which are in df but notin uploaded df
                #Prediction data does not contain following features append list
                # return JsonResponse({"msg":"msg"})

            targetVar =find_target_value(file_id)   
            dfConfig=find_pyconfig(request.session['vt_mdl'],str(request.session['uid']))
            if len(df)>0:
                if len(dfConfig)>0:  
                    targetVar =find_target_value(file_id) 

                    for index, row in dfConfig.iterrows():    
                        print('row["normalize"] is ',   row["normalize"]  )               
                    # clf=setup(data = df, target = 'status', train_size = 0.7,html=False,silent=True,normalize = False, transformation = False )
                        clf=setup(data = df, target = targetVar, html=False,silent=True,           
                                train_size=0.99, categorical_imputation=eval("'" +row["categorical_imputation"] +"'"),
                                numeric_imputation =eval("'"+row["numeric_imputation"]+"'"),ignore_features =eval(row["ignore_features"])
                                ,normalize =eval(row["normalize"]) ,normalize_method=eval("'"+ row["normalize_method"] +"'"),
                                remove_outliers=eval(row["remove_outliers"]) ,outliers_threshold =float(row["outliers_threshold"]),
                                remove_multicollinearity =eval(row["remove_multicollinearity"]),multicollinearity_threshold=float(row["multicollinearity_threshold"]),
                                feature_interaction=eval(row["feature_interaction"]) ,feature_ratio=eval(row["feature_ratio"])
                                ,polynomial_features =eval(row["polynomial_features"]),polynomial_degree=int(row["polynomial_degree"]) ,trigonometry_features=eval(row["trigonometry_features"]) 
                                ,fix_imbalance=eval(row["fix_imbalance"])
                                )
                        #  transform_target =row["transform_target"], not working  transform_target_method=eval("'"+row["transform_target_method"]+"'"
                        X_test= get_config('X_train')
                       
                        reg = joblib.load(mdlname+'.joblib')
                        print("Loded save model",reg)
                        print("x_test",X_test.columns)
                        y_pred = reg.predict(X_test)
                        print("prediction",y_pred)
                        test_Y= get_config('y_train')
                        try:
                            base_fpr, base_tpr, _ = roc_curve(test_Y, [1 for _ in range(len(test_Y))])
                            model_fpr, model_tpr, _ = roc_curve(test_Y, reg.predict_proba(X_test)[:, 1])
                            model_fprx, model_tprx, _ = roc_curve(1-test_Y,reg.predict_proba(X_test)[:, 0]) 
                            plt.figure(figsize=(10, 5))
                            plt.rcParams['font.size'] = 12
                            # Plot both curves
                            plt.plot(base_fpr, base_tpr, 'b')
                            plt.plot(model_fpr, model_tpr, 'r', label='ROC of class 1, AUC = '+str(round(auc(model_fpr, model_tpr),2)))
                            plt.plot(model_fprx, model_tprx, 'g', label='ROC of class 0, AUC = '+str(round(auc(model_fprx, model_tprx),2)))
                            plt.legend()
                            plt.xlabel('False Positive Rate')
                            plt.ylabel('True Positive Rate')
                            plt.title('ROC Curves')
                            plt.tight_layout()
                            plt.savefig(os.path.join(
                                BASE_DIR, plot_dir_view, mdl_id + "_ROCAUC.png"))
                            scn_files_Roc = plot_dir_view+ mdl_id + "_ROCAUC.png"
                            print("scnfiles",scn_files_Roc)

                            plt.close()
                        except Exception as e:
                            print(e,traceback.print_exc())
                            print('roc not supported')

                        try:

                            pred_rf_test = reg.predict(X_test) 
                            
                            drawConfMatrix(test_Y, pred_rf_test, mdlname + "_Confusion_Matrix_"+mdl_id+".png", "Test")
                            scn_files_Confusion_Matrix = plot_dir_view+ mdlname + "_Confusion_Matrix_"+mdl_id+".png"
                            print("scnfiles",scn_files_Confusion_Matrix)
                            clf_report = classification_report(test_Y, pred_rf_test, output_dict=True)  
                            
                            clf_report=pd.DataFrame(clf_report).T
                            plt.figure(figsize=(10, 5))
                            clf_report['support'] = clf_report['support'].astype(int)
                            
                            sns.heatmap(clf_report, annot=True, fmt='.4g')
                            plt.tight_layout()
                            plt.savefig(os.path.join(
                                BASE_DIR, plot_dir_view, mdlname+ '_classification_report_'+mdl_id+ '.png'))                           
                            scn_files_classification_report = plot_dir_view+ mdlname+ '_classification_report_'+mdl_id+ '.png'
                            print("scnfiles",scn_files_classification_report)
                            plt.close()
                        except:
                            print('cnf mtrx ,cls rpt not supported')
                        data = {
                            'Roc': scn_files_Roc,
                            'classification_report':scn_files_classification_report,
                            'Confusion_matrix':scn_files_Confusion_Matrix
                        }                      
                        print("data",data)
    return JsonResponse(data)

def updateParams(request):
    try: 
        model =request.GET.get('model', 'False')
        nitr =int(request.GET.get('nitr', '10'))
        matric =request.GET.get('matric', 'Accuracy')
        library =request.GET.get('library', 'scikit-learn')
        algo =request.GET.get('algo', 'None')
        autobetter =request.GET.get('autobetter', 'False')
        dataSize=request.GET.get('dataSize', '1000') 
        file_id=find_max_file_id(request.session['vt_mdl'])
        dataset=request.session['vt_dataset'] 
        df=find_src_data(file_id,dataset)
        dfConfig=find_pyconfig(request.session['vt_mdl'],str(request.session['uid']))
        if len(df)>0:
            if len(dfConfig)>0:
                 
                ind = np.random.choice(len(df),int(dataSize),replace=False)
                df = df.iloc[ind,:]
                 
                 
                bestModel=model
               
                targetVar = find_target_value(file_id)
                for index, row in dfConfig.iterrows():    
                    # print('row["normalize"] is ',   row["normalize"]  )               
                # clf=setup(data = df, target = 'status', train_size = 0.7,html=False,silent=True,normalize = False, transformation = False )
                    clf=setup(data = df, target = targetVar, html=False,silent=True,           
                            train_size=float(row["train_size"]), categorical_imputation=eval("'" +row["categorical_imputation"] +"'"),
                            numeric_imputation =eval("'"+row["numeric_imputation"]+"'"),ignore_features =eval(row["ignore_features"])
                            ,normalize =eval(row["normalize"]) ,normalize_method=eval("'"+ row["normalize_method"] +"'"),
                            remove_outliers=eval(row["remove_outliers"]) ,outliers_threshold =float(row["outliers_threshold"]),
                            remove_multicollinearity =eval(row["remove_multicollinearity"]),multicollinearity_threshold=float(row["multicollinearity_threshold"]),
                            feature_interaction=eval(row["feature_interaction"]) ,feature_ratio=eval(row["feature_ratio"])
                            ,polynomial_features =eval(row["polynomial_features"]),polynomial_degree=int(row["polynomial_degree"]) ,trigonometry_features=eval(row["trigonometry_features"]) 
                            ,fix_imbalance=eval(row["fix_imbalance"])
                            )
                    #  transform_target =row["transform_target"], not working  transform_target_method=eval("'"+row["transform_target_method"]+"'"
                    best = create_model(bestModel)
                    joblib.dump(best, 'Temp_'+request.session['username'] +'.joblib')
                    print('inside tune  models')
                    # tune model
                    tuned_dt = tune_model(best, n_iter = nitr, optimize = matric, search_library =library, search_algorithm = algo)
                    plotOutput(tuned_dt,bestModel,"Tune") 
                    # context={'clsrpt':plot_dir_view+'//'+ user_name+ '_classification_report_'+bestModel+'_Test.png',
                    # 'auc':plot_dir_view+'//'+ user_name+ '_ROCAUC_'+bestModel+'_Test.png',
                    # 'cnfmtrx':plot_dir_view+'//'+ user_name+ '_Confusion_Matrix_'+bestModel+'_Test.png'}
                     
                    # return  render(request,"showModelOutputPycr.html")
                    # return redirect('showPycrOutputs') 
                del df,dfConfig 
            else:
                print('pycaret config does not exist')
        else:
            print('file does not exist')
        return JsonResponse({'run':'sucess'})
    except Exception as e:
        print('setuppycaret error is ',e) 
        # print('stacktrace is ',traceback.print_exc())
        return JsonResponse({'run':'fail'})


def plotOutput(best,bestModel,type):
    path=os.path.join(BASE_DIR, plot_dir_view) #root_path+"demo_picture" #  you can change the path 
    featureFileNm="NA.png"
    summaryNm="NA.png"
    #  plot_model(best, plot = 'auc', save = path)
    
    # if os.path.exists(path+"//"+ user_name+'_AUC_'+bestModel+'_'+ type+ '.png'):
    #     os.remove(path+"//"+ user_name+'_AUC_'+bestModel+'_'+ type+ '.png')
    # os.rename(path+"//AUC.png" ,path+"//"+ user_name+'_AUC_'+bestModel+'_'+ type+ '.png')
    
    # plot_model(best, plot = 'confusion_matrix', save = path)
    # if os.path.exists(path+"//"+ user_name+'_pycr_Confusion_Matrix_'+bestModel+'_'+ type+ '.png'):
    #     os.remove(path+"//"+ user_name+'_pycr_Confusion_Matrix_'+bestModel+'_'+ type+ '.png')
    # os.rename(path+"//Confusion Matrix.png" ,path+"//"+ user_name+'_pycr_Confusion_Matrix_'+bestModel+'_'+ type+ '.png')
    
    try:
        plot_model(best, plot = 'feature', save = path)
        if os.path.exists(path+"//"+ user_name+'_Feature_Importance_'+bestModel+'_'+ type+ '.png'):
            os.remove(path+"//"+ user_name+'_Feature_Importance_'+bestModel+'_'+ type+ '.png')
        os.rename(path+"//Feature Importance.png" ,path+"//"+ user_name+'_Feature_Importance_'+bestModel+'_'+ type+ '.png')
        featureFileNm=user_name+'_Feature_Importance_'+bestModel+'_'+ type+ '.png'
    except:
        print('feature not suported')
    
    try:
        plot_model(best, plot = 'ks',save=path)
        if os.path.exists(path+"//"+ user_name+'_KS_'+bestModel+'_'+ type+ '.png'):
            os.remove(path+"//"+ user_name+'_KS_'+bestModel+'_'+ type+ '.png')
        os.rename(path+"//KS Statistic Plot.png" ,path+"//"+ user_name+'_KS_'+bestModel+'_'+ type+ '.png')
    except:
        print('ks not suported')
    # plot_model(best, plot = 'error',save=path)
    # if os.path.exists(path+"//"+ user_name+'_Feature_Importance_'+bestModel+'_'+ type+ '.png'):
    #     os.remove(path+"//"+ user_name+'_Feature_Importance_'+bestModel+'_'+ type+ '.png')
    # os.rename(path+"//Feature Importance.png" ,path+"//"+ user_name+'_Feature_Importance_'+bestModel+'_'+ type+ '.png')
    
    try:
        plot_model(best, plot = 'lift',save=path)
        if os.path.exists(path+"//"+ user_name+'_Lift_'+bestModel+'_'+ type+ '.png'):
            os.remove(path+"//"+ user_name+'_Lift_'+bestModel+'_'+ type+ '.png')
        os.rename(path+"//Lift Chart.png" ,path+"//"+ user_name+'_Lift_'+bestModel+'_'+ type+ '.png')
    except:
        print('lift not suported')

    try:
        plot_model(best, plot = 'gain',save=path)
        if os.path.exists(path+"//"+ user_name+'_Gain_'+bestModel+'_'+ type+ '.png'):
            os.remove(path+"//"+ user_name+'_Gain_'+bestModel+'_'+ type+ '.png')
        os.rename(path+"//Gain Chart.png" ,path+"//"+ user_name+'_Gain_'+bestModel+'_'+ type+ '.png')
    except:
        print('gain not suported')

    try:    
        plot_model(best, plot = 'calibration',save=path) 
        if os.path.exists(path+"//"+ user_name+'_Calibration_'+bestModel+'_'+ type+ '.png'):
            os.remove(path+"//"+ user_name+'_Calibration_'+bestModel+'_'+ type+ '.png')
        os.rename(path+"//Calibration Curve.png" ,path+"//"+ user_name+'_Calibration_'+bestModel+'_'+ type+ '.png')
    except:
        print('valibration not suported')

    test_X=get_config('X_test')
    test_Y=get_config('y_test')
    # test_X=get_config('X_train')
    # test_Y=get_config('y_train') 
    # Calculate false positive rates and true positive rates
    try:
        base_fpr, base_tpr, _ = roc_curve(test_Y, [1 for _ in range(len(test_Y))])
        model_fpr, model_tpr, _ = roc_curve(test_Y, best.predict_proba(test_X)[:, 1])
        model_fprx, model_tprx, _ = roc_curve(1-test_Y, best.predict_proba(test_X)[:, 0]) 
        plt.figure(figsize=(10, 5))
        plt.rcParams['font.size'] = 12
        # Plot both curves
        plt.plot(base_fpr, base_tpr, 'b')
        plt.plot(model_fpr, model_tpr, 'r', label='ROC of class 1, AUC = '+str(round(auc(model_fpr, model_tpr),2)))
        plt.plot(model_fprx, model_tprx, 'g', label='ROC of class 0, AUC = '+str(round(auc(model_fprx, model_tprx),2)))
        plt.legend()
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curves')
        plt.tight_layout()
        plt.savefig(os.path.join(
            BASE_DIR, plot_dir_view, user_name + "_ROCAUC_"+bestModel+"_"+ type+ ".png"))
        plt.close()
    except:
        print('roc not supported')
    
    try:
        pred_rf_test = best.predict(test_X) 
        
        drawConfMatrix(test_Y, pred_rf_test, user_name + "_Confusion_Matrix_"+bestModel+"_"+ type+ ".png", "Test")

        clf_report = classification_report(test_Y, pred_rf_test, output_dict=True)  
        
        clf_report=pd.DataFrame(clf_report).T
        clf_report['support'] = clf_report['support'].astype(int)
        
        plt.figure(figsize=(10, 5))
        sns.heatmap(clf_report, annot=True, fmt='.4g')
        plt.tight_layout()
        plt.savefig(os.path.join(
            BASE_DIR, plot_dir_view, user_name+ '_classification_report_'+bestModel+'_'+ type+ '.png'))
        plt.close()
    except:
        print('cnf mtrx ,cls rpt not supported')

    try:
        
        if os.path.exists(path+"//"+ user_name+'_summary_'+bestModel+'_'+ type+ '.png'):
            os.remove(path+"//"+ user_name+'_summary_'+bestModel+'_'+ type+ '.png')
        interpret_model(best,save=path) 
        os.rename(path+"//SHAP summary.png" ,path+"//"+ user_name+'_summary_'+bestModel+'_'+ type+ '.png')
         
        interpret_model(best, plot = 'correlation',save=path) 
        if os.path.exists(path+"//"+ user_name+'_correlation_'+bestModel+'_'+ type+ '.png'):
            os.remove(path+"//"+ user_name+'_correlation_'+bestModel+'_'+ type+ '.png')
        os.rename(path+"//SHAP correlation.png",path+"//"+ user_name+'_correlation_'+bestModel+'_'+ type+ '.png')
    except:
        print('shap not suported')

    try:
        if os.path.exists(path+"//"+ user_name+'_pdp_'+bestModel+'_'+ type+ '.png'):
            os.remove(path+"//"+ user_name+'_pdp_'+bestModel+'_'+ type+ '.png')
        if os.path.exists(path+"//PDP pdp.html"):
            os.remove(path+"//PDP pdp.html")
        if os.path.exists(path+"//"+ user_name+'_pdp_'+bestModel+'_'+ type+ '.html'):
            os.remove(path+"//"+ user_name+'_pdp_'+bestModel+'_'+ type+ '.html')
        interpret_model(best, plot = 'pdp',save=path)
        os.rename(path+"//PDP pdp.html",path+"//"+ user_name+'_pdp_'+bestModel+'_'+ type+ '.html')
        htmltopng(user_name+'_pdp_'+bestModel+'_'+ type+ '.html',user_name+'_pdp_'+bestModel+'_'+ type+ '')  
    except:
        print('pdp not suported')

    try:
        if os.path.exists(path+"//"+ user_name+'_msa_'+bestModel+'_'+ type+ '.png'):
                os.remove(path+"//"+ user_name+'_msa_'+bestModel+'_'+ type+ '.png')
        if os.path.exists(path+"//"+ user_name+'_msa_'+bestModel+'_'+ type+ '.html'):
            os.remove(path+"//"+ user_name+'_msa_'+bestModel+'_'+ type+ '.html')
        interpret_model(best, plot = 'msa',save=path)
        os.rename(path+"//MSA msa.html",path+"//"+ user_name+'_msa_'+bestModel+'_'+ type+ '.html')
        htmltopng(user_name+'_msa_'+bestModel+'_'+ type+ '.html',user_name+'_msa_'+bestModel+'_'+ type)
    except:
        print('msa not suported')

    try:
        if os.path.exists(path+"//"+ user_name+'_pfi_'+bestModel+'_'+ type+ '.png'):
            os.remove(path+"//"+ user_name+'_pfi_'+bestModel+'_'+ type+ '.png')
        if os.path.exists(path+"//"+ user_name+'_pfi_'+bestModel+'_'+ type+ '.html'):
            os.remove(path+"//"+ user_name+'_pfi_'+bestModel+'_'+ type+ '.html')
        interpret_model(best, plot = 'pfi',save=path)
        os.rename(path+"//PFI pfi.html",path+"//"+ user_name+'_pfi_'+bestModel+'_'+ type+ '.html')
        htmltopng(user_name+'_pfi_'+bestModel+'_'+ type+ '.html',user_name+'_pfi_'+bestModel+'_'+ type)
    except:
        print('pfi not suported')


    # y_type, y_true, y_pred =_classification._check_targets(test_Y, pred_rf_test)                   
    # print('y_true  ')                    
    # unique, counts = np.unique(y_true, return_counts=True)
    # print(dict(zip(unique, counts)))

    # print('y_pred ')                    
    # unique, counts = np.unique(y_pred, return_counts=True)
    # print(dict(zip(unique, counts)))

    # plot_model(best, plot = 'class_report',save=path)

    # paramFiles = param_file_path + param_file_name + "_"+bestModel +"_RS_pycr.csv"
    # param_grid = {}
    # if os.path.exists(paramFiles):
    #     df = pd.read_csv(paramFiles)
    #     for index, row in df.iterrows():
    #         param_grid[row['paramName']] = eval(row['paramValue'])
        
    #     best_rs = create_model(bestModel)
    #     # Create the random search model
        
    #     rf_search = tune_model(best_rs, search_algorithm = "random",custom_grid=param_grid)#,n_iter=1,estimator ='xgboost') #random :random grid
        
    #     plot_model(rf_search, plot = 'auc', save = path)
    #     if os.path.exists(path+"//"+ user_name+'_AUC_'+bestModel+'_RS.png'):
    #         os.remove(path+"//"+ user_name+'_AUC_'+bestModel+'_RS.png')
    #     os.rename(path+"//AUC.png" ,path+"//"+ user_name+'_AUC_'+bestModel+'_RS.png')

    #     plot_model(rf_search, plot = 'confusion_matrix', save = path)
    #     if os.path.exists(path+"//"+ user_name+'_Confusion_Matrix_'+bestModel+'_RS.png'):
    #         os.remove(path+"//"+ user_name+'_Confusion_Matrix_'+bestModel+'_RS.png')
    #     os.rename(path+"//Confusion Matrix.png" ,path+"//"+ user_name+'_Confusion_Matrix_'+bestModel+'_RS.png')
        
    #     plot_model(rf_search, plot = 'feature', save = path)
    #     if os.path.exists(path+"//"+ user_name+'_Feature_Importance_'+bestModel+'_RS.png'):
    #         os.remove(path+"//"+ user_name+'_Feature_Importance_'+bestModel+'_RS.png')
    #     os.rename(path+"//Feature Importance.png" ,path+"//"+ user_name+"_Feature_Importance_"+bestModel+"_RS.png")
        
        
        
    #     if os.path.exists(path+"//"+ user_name+'_pdp_'+bestModel+'_RS.png'):
    #         os.remove(path+"//"+ user_name+'_pdp_'+bestModel+'_RS.png') 
    #     if os.path.exists(path+"//"+ user_name+'_pdp_'+bestModel+'_RS.html'):
    #         os.remove(path+"//"+ user_name+'_pdp_'+bestModel+'_RS.html')
    #     interpret_model(rf_search, plot = 'pdp',save=path)
    #     os.rename(path+"//PDP pdp.html",path+"//"+ user_name+'_pdp_'+bestModel+'_RS.html')
    #     htmltopng(user_name+'_pdp_'+bestModel+'_RS.html',user_name+'_pdp_'+bestModel+'_RS')


    # paramFiles = param_file_path + param_file_name + "_"+bestModel +"_GS_pycr.csv"
    # param_grid = {}
    # if os.path.exists(paramFiles):
    #     df = pd.read_csv(paramFiles)
    #     for index, row in df.iterrows():
    #         param_grid[row['paramName']] = eval(row['paramValue'])
        
    #     best_gd = create_model(bestModel)
    #     # Create the random search model
    #     gs_search = tune_model(best_gd, search_algorithm = "random",custom_grid=param_grid)#,n_iter=1,estimator ='xgboost') #random :random grid

def showPycrOutputs(request):
    try:
        bestModel=request.GET['bestModel']  
        modelNm=request.GET['modelNm']   
        ty=request.GET['ty']                 
        print('bestModel is ',bestModel) 
        # ty="Test"#request.Get.get('type', 'False')
        summaryNm,rocaucNm,featureNm,correlationNm ,pdpNm,pfiNm,msaNm="NA.png","NA.png","NA.png","NA.png","NA.png","NA.png","NA.png"
        if os.path.exists(plot_dir_view+"//"+ user_name+'_summary_'+bestModel+'_'+ ty+ '.png'):
            summaryNm=user_name+'_summary_'+bestModel+'_'+ ty+ '.png'
        
        if os.path.exists(plot_dir_view+"//"+ user_name+'_ROCAUC_'+bestModel+'_'+ ty+ '.png'):
            rocaucNm=user_name+'_ROCAUC_'+bestModel+'_'+ ty+ '.png'

        if os.path.exists(plot_dir_view+"//"+ user_name+'_Feature_Importance_'+bestModel+'_'+ ty+ '.png'):
            featureNm=user_name+'_Feature_Importance_'+bestModel+'_'+ ty+ '.png'

        if os.path.exists(plot_dir_view+"//"+ user_name+'_correlation_'+bestModel+'_'+ ty+ '.png'):
            correlationNm=user_name+'_correlation_'+bestModel+'_'+ ty+ '.png'

        if os.path.exists(plot_dir_view+"//"+ user_name+'_pdp_'+bestModel+'_'+ ty+ '.png'):
            pdpNm= user_name+ '_pdp_'+bestModel+'_'+ ty+ '.png'

        if os.path.exists(plot_dir_view+"//"+ user_name+'_pdp_'+bestModel+'_'+ ty+ '.png'):
            pfiNm=user_name+ '_pfi_'+bestModel+'_'+ ty+ '.png'

        if os.path.exists(plot_dir_view+"//"+ user_name+'_msa_'+bestModel+'_'+ ty+ '.png'):
            msaNm=user_name+ '_msa_'+bestModel+'_'+ ty+ '.png'

        context={'bestModel':modelNm,'modelSS':bestModel,
                'clsrpt':'/'+plot_dir_view+'/'+ user_name+ '_classification_report_'+bestModel+'_'+ ty+ '.png',
                 'auc':'/'+plot_dir_view+'/'+ rocaucNm,
                 'cnfmtrx':'/'+plot_dir_view+'/'+ user_name+ '_Confusion_Matrix_'+bestModel+'_'+ ty+ '.png',
                 'calibration':'/'+plot_dir_view+'/'+ user_name+ '_Calibration_'+bestModel+'_'+ ty+ '.png',
                 'lift':'/'+plot_dir_view+'/'+ user_name+ '_Lift_'+bestModel+'_'+ ty+ '.png',
                 'gain':'/'+plot_dir_view+'/'+ user_name+ '_Gain_'+bestModel+'_'+ ty+ '.png',
                 'ks':'/'+plot_dir_view+'/'+ user_name+ '_KS_'+bestModel+'_'+ ty+ '.png',
                 'features':'/'+plot_dir_view+'/'+ featureNm,
                 'summary':'/'+plot_dir_view+'/'+ summaryNm,
                 'correlation':'/'+plot_dir_view+'/'+correlationNm,
                 'pdp':'/'+plot_dir_view+'/'+pdpNm,
                 'pfi':'/'+plot_dir_view+'/'+ pfiNm,
                 'msa':'/'+plot_dir_view+'/'+msaNm}
        return render(request, 'showModelOutputPycr.html', context)
        # return render(request, 'runModels.html', context)
    except Exception as e:
        print(e)
        return render(request, 'error.html')
    
def saveModelChartImage(request):
    
    predict = request.GET.get('predict','')
    chartImg = request.GET['chartImg']
    chartType = request.GET['chartType']
    modelSS = request.GET['modelSS']
    imgPath = request.GET['imgPath']
    imgPath = imgPath.split('/')[-1] 
    
    imgPath='static/media/'+imgPath.split('?')[0]
    
    print('chartImg ', chartImg, ' chartType ',
          chartType, ' imgPath ', imgPath.split('/')[-1])
    chartcomment = ""
    modelid=request.session['vt_mdl']
    if modelSS == "lr":
        modelSS= "LOG"
    elif modelSS == "rf":
        modelSS= "RFC"
    elif modelSS == "et":
        modelSS= "XTC"
    elif modelSS == "dummy":
        modelSS= "DC"
    elif modelSS == "xgboost":
        modelSS= "XGB"
    elif modelSS == "ridge":
        modelSS= "RC"
    elif modelSS == "lightgbm":
        modelSS= "LGB" 

    if predict=='yes':
        destfilenm='Test_'+modelid+'_'+modelSS.upper()+'_'+chartImg+'_'+date.today().strftime("%m.%d.%Y") +'.png'
    else:
        destfilenm=modelid+'_'+modelSS.upper()+'_'+chartImg+'_'+date.today().strftime("%m.%d.%Y") +'.png'
     
        
    destination = plot_dir_view+user_name+'Chartimgs/'+destfilenm
    print('destination is ',destination)
    data = [[request.session['vt_mdl'],str(request.session['uid']),chartType, destfilenm, destination,
            chartcomment]]
    dfnew = pd.DataFrame(
        data, columns=['mdl_id','user_id','chartType', 'chartImg', 'destination', 'comments'])

    if collection_Chartimg.find_one({'mdl_id':request.session['vt_mdl'],'user_id':str(request.session['uid']),'chartType':chartType}):
        collection_Chartimg.delete_many({'mdl_id':request.session['vt_mdl'],'user_id':str(request.session['uid']),'chartType':chartType})
        collection_Chartimg.insert_many(dfnew.to_dict('records'))
    else: 
        collection_Chartimg.insert_many(dfnew.to_dict('records'))
    source = os.path.join(
        BASE_DIR, imgPath)

    # Destination path
    destpath=plot_dir_view+user_name+'Chartimgs/'+destfilenm
    destination = os.path.join(
        BASE_DIR,destpath)
    shutil.copyfile(source, destination)
    print("File copied successfully.")
        #     del dffilter 
         

    data = {"is_taken": True,'fileNm':destfilenm}
    return JsonResponse(data)

def getPycrParamName(request):
    RF = ['criterion', 'max_features', 'max_depth', 'min_samples_leaf',
          'min_samples_split', 'n_estimators', 'max_leaf_nodes', 'bootstrap']
    XGB = ['objective', 'colsample_bytree', 'learning_rate',
           'max_depth', 'lambda', 'n_estimators', 'missing', 'seed']
    MLP = ['hidden_layer_sizes', 'activation',
           'solver', 'alpha', 'momentum', 'learning_rate']
    GB = ['loss', 'learning_rate', 'n_estimators', 'criterion', 'min_samples_split',
          'min_samples_leaf', 'max_depth', 'max_features', 'max_leaf_nodes', 'init', 'validation_fraction']
    KNN = ['n_neighbors', 'weights', 'algorithm', 'p']
    SVM = ['C', 'kernel', 'gamma', 'probability', 'class_weight']
    BC = ['base_estimator', 'n_estimators', 'max_samples',
          'max_features', 'bootstrap', 'bootstrap_features', 'oob_score']
    modelName = request.GET['modelName']
    tuneMethod = request.GET['tuneMethod']
    paramFiles = param_file_path + param_file_name + "_"+ modelName +"_" + tuneMethod + "_pycr.csv"
    if (modelName == "rf"):
        
        if os.path.exists(paramFiles):
            df = pd.read_csv(paramFiles)
            result = df.to_json(orient="records")
            result = json.loads(result)
            data = {
                'params': RF,
                'paramVals': result
            }
        else:
            data = {
                'params': RF,
                'paramVals': []
            }
    elif (modelName == "xgb"): 
        if os.path.exists(paramFiles):
            df = pd.read_csv(paramFiles)
            result = df.to_json(orient="records")
            result = json.loads(result)
            data = {
                'params': XGB,
                'paramVals': result
            }
        else:
            data = {
                'params': XGB,
                'paramVals': []
            }
    elif (modelName == "mlp"): 
        if os.path.exists(paramFiles):
            df = pd.read_csv(paramFiles)
            result = df.to_json(orient="records")
            result = json.loads(result)
            data = {
                'params': MLP,
                'paramVals': result
            }
        else:
            data = {
                'params': MLP,
                'paramVals': []
            }
    elif (modelName == "gbc"): 
        if os.path.exists(paramFiles):
            df = pd.read_csv(paramFiles)
            result = df.to_json(orient="records")
            result = json.loads(result)
            data = {
                'params': GB,
                'paramVals': result
            }
        else:
            data = {
                'params': GB,
                'paramVals': []
            }
    elif (modelName == "knn"): 
        if os.path.exists(paramFiles):
            df = pd.read_csv(paramFiles)
            result = df.to_json(orient="records")
            result = json.loads(result)
            data = {
                'params': KNN,
                'paramVals': result
            }
        else:
            data = {
                'params': KNN,
                'paramVals': []
            }
    elif (modelName == "svm"): 
        if os.path.exists(paramFiles):
            df = pd.read_csv(paramFiles)
            result = df.to_json(orient="records")
            result = json.loads(result)
            data = {
                'params': SVM,
                'paramVals': result
            }
        else:
            data = {
                'params': SVM,
                'paramVals': []
            }
    elif (modelName == "ada"): 
        if os.path.exists(paramFiles):
            df = pd.read_csv(paramFiles)
            result = df.to_json(orient="records")
            result = json.loads(result)
            data = {
                'params': BC,
                'paramVals': result
            }
        else:
            data = {
                'params': BC,
                'paramVals': []
            }
    return JsonResponse(data)


def setPycrParamName(request):
    modelName = request.GET['modelName']
    tuneMethod = request.GET['tuneMethod']
    paramName = request.GET['paramName']
    paramValue = request.GET['paramValue']
    # if (modelName == "Random_Forest"):
    #     paramFiles = param_file_path + param_file_name + "_RF_" + tuneMethod + ".csv"
    # elif (modelName == "XGBoost"):
    #     paramFiles = param_file_path + param_file_name + "_XGB_" + tuneMethod + ".csv"
    # elif (modelName == "MLP"):
    #     paramFiles = param_file_path + param_file_name + "_MLP_" + tuneMethod + ".csv"
    # elif (modelName == "Gradient_Boosting"):
    #     paramFiles = param_file_path + param_file_name + "_GB_" + tuneMethod + ".csv"
    # elif (modelName == "KNN"):
    #     paramFiles = param_file_path + param_file_name + "_KNN_" + tuneMethod + ".csv"
    # elif (modelName == "SVM"):
    #     paramFiles = param_file_path + param_file_name + "_SVM_" + tuneMethod + ".csv"
    # elif (modelName == "Bagging_Classifier"):
    #     paramFiles = param_file_path + param_file_name + "_BC_" + tuneMethod + ".csv"
 
    paramFiles = param_file_path + param_file_name + "_"+ modelName +"_" + tuneMethod + "_pycr.csv"
    if os.path.exists(paramFiles):
        df_old = pd.read_csv(paramFiles)
        if (df_old["paramName"] == paramName).any():
            df_old.loc[df_old.paramName ==
                       paramName, "paramValue"] = paramValue
            df_old.to_csv(paramFiles, index=False)
        else:
            data = [[paramName, paramValue]]
            df_new = pd.DataFrame(
                data, columns=['paramName', 'paramValue'])
            df = pd.concat([df_old, df_new], axis=0)
            df.to_csv(paramFiles, index=False)
    else:
        data = [[paramName, paramValue]]
        df = pd.DataFrame(data, columns=['paramName', 'paramValue'])
        df.to_csv(paramFiles, index=False)

    if os.path.exists(paramFiles):
        df = pd.read_csv(paramFiles)
        result = df.to_json(orient="records")
        result = json.loads(result)
    data = {
        'paramVals': result
    }
    return JsonResponse(data)

def drawConfMatrix(y_val, pred_rf_val, fileName="cnfmtrx", strLbl="test"):
    cnf_matrix = confusion_matrix(y_val, pred_rf_val, labels=[0, 1])
 
    plt.figure(figsize=(10, 5))
    sns.heatmap(pd.DataFrame(cnf_matrix), annot=True,
                cmap="YlGnBu", fmt='g')
    plt.title('Confusion matrix: '+strLbl+' data')
    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    plt.savefig(os.path.join(
        BASE_DIR, plot_dir_view + fileName))
    plt.close()

    print('confusion matrix done')


def Interpret_shape(best_model,shape_type,save_path,save_name):
    path=os.path.join(BASE_DIR, plot_dir_view) #root_path+"demo_picture" #  you can change the path 
    if shape_type=="shape":
        interpret_model(best_model,save=path) 
        if os.path.exists(path+"//"+ save_name+'_summary.png'):
            os.remove(path+"//"+ save_name+'_summary.png')
        os.rename(path+"//SHAP summary.png" ,path+"//"+ save_name+'_summary.png')

        interpret_model(best_model, plot = 'correlation',save=path)
        """
        os.rename(file,file2),, file2 is the name we want to change
        """
        if os.path.exists(path+"//"+ save_name+'_correlation.png'):
            os.remove(path+"//"+ save_name+'_correlation.png')
        os.rename(path+"//SHAP correlation.png",path+"//"+ save_name+'_correlation.png')
     
        if os.path.exists(path+"//"+ save_name+'_pdp.png'):
            os.remove(path+"//"+ save_name+'_pdp.png')
        if os.path.exists(path+"//PDP pdp.html"):
            os.remove(path+"//PDP pdp.html")
        if os.path.exists(path+"//"+ save_name+'_pdp.html'):
            os.remove(path+"//"+ save_name+'_pdp.html')
        interpret_model(best_model, plot = 'pdp',save=path)
        os.rename(path+"//PDP pdp.html",path+"//"+ save_name+'_pdp.html')
        htmltopng(save_name+'_pdp.html',save_name+'_pdp')

        if os.path.exists(path+"//"+ save_name+'_msa.png'):
            os.remove(path+"//"+ save_name+'_msa.png')
        if os.path.exists(path+"//"+ save_name+'_msa.html'):
            os.remove(path+"//"+ save_name+'_msa.html')
        interpret_model(best_model, plot = 'msa',save=path)
        os.rename(path+"//MSA msa.html",path+"//"+ save_name+'_msa.html')
        htmltopng(save_name+'_msa.html',save_name+'_msa')


        if os.path.exists(path+"//"+ save_name+'_pfi.png'):
            os.remove(path+"//"+ save_name+'_pfi.png')
        if os.path.exists(path+"//"+ save_name+'_pfi.html'):
            os.remove(path+"//"+ save_name+'_pfi.html')
        interpret_model(best_model, plot = 'pfi',save=path)
        os.rename(path+"//PFI pfi.html",path+"//"+ save_name+'_pfi.html')
        htmltopng(save_name+'_pfi.html',save_name+'_pfi')
    
    if shape_type=="msa":   
        if os.path.exists(path+"//"+ save_name+'_pdp.png'):
            os.remove(path+"//"+ save_name+'_pdp.png')
        if os.path.exists(path+"//PDP pdp.html"):
            os.remove(path+"//PDP pdp.html")
        if os.path.exists(path+"//"+ save_name+'_pdp.html'):
            os.remove(path+"//"+ save_name+'_pdp.html')
        interpret_model(best_model, plot = 'pdp',save=path)
        os.rename(path+"//PDP pdp.html",path+"//"+ save_name+'_pdp.html')
        htmltopng(save_name+'_pdp.html',save_name+'_pdp')

        if os.path.exists(path+"//"+ save_name+'_msa.png'):
            os.remove(path+"//"+ save_name+'_msa.png')
        if os.path.exists(path+"//"+ save_name+'_msa.html'):
            os.remove(path+"//"+ save_name+'_msa.html')
        interpret_model(best_model, plot = 'msa',save=path)
        os.rename(path+"//MSA msa.html",path+"//"+ save_name+'_msa.html')
        htmltopng(save_name+'_msa.html',save_name+'_msa')


        if os.path.exists(path+"//"+ save_name+'_pfi.png'):
            os.remove(path+"//"+ save_name+'_pfi.png')
        if os.path.exists(path+"//"+ save_name+'_pfi.html'):
            os.remove(path+"//"+ save_name+'_pfi.html')
        interpret_model(best_model, plot = 'pfi',save=path)
        os.rename(path+"//PFI pfi.html",path+"//"+ save_name+'_pfi.html')
        htmltopng(save_name+'_pfi.html',save_name+'_pfi')
    
    if shape_type=="pfi":
        interpret_model(best_model, plot = 'pfi',save=path)
        os.rename(path+"//PFI pfi.html",path+"//"+"%s.html" % save_name)

def htmltopng(filename,pngname):
    path=os.path.join(BASE_DIR, plot_dir_view)
    from html2image import Html2Image
    import shutil
    hti = Html2Image(output_path=  path) 
    with open(path+"//"+ filename) as f:
        hti.screenshot(f.read(), save_as= pngname+'.png', size=(900, 500))
    os.remove(path+"//"+ filename) 

def randomForestAjax():
    try:
        csv_file_name = "csvfile_"+user_name
        savefile_x_final = file_path + csv_file_name + "_x_model.csv"
        df = pd.read_csv(savefile_x_final)
        targetVarFile = file_path + csv_file_name + "_targetVar.txt"
        file1 = open(targetVarFile, "r")  # write mode
        targetVar = file1.read()
        file1.close()
        print(df.head(5))
        clf1=setup(data = df, target = targetVar, train_size = 0.7,html=False,silent=True)
         
        log_rf = create_model('rf')
        # tuned_dt = tune_model(log_rf, optimize = 'MAE')
        # X_train = get_config("X_train")
        # X_train.to_csv( file_path + csv_file_name + "_xTrain_keep.csv", index=False, encoding='utf-8')
        # X_test = get_config("X_test")
        # X_test.to_csv( file_path + csv_file_name + "_xTest_keep.csv", index=False, encoding='utf-8')
        # before  run the model please check which parameters can be used. using thi command
        log_rf.get_params().keys()
        save_path=root_path+"demo_picture"
        save_name=file_name+"_RF_NT"
        Interpret_shape(log_rf,"shape",save_path,save_name)
        
        # split the dastaset into train, validation and test with the ratio 0.7, 0.2 and 0.1
         
        # Random Search
        paramFiles = param_file_path + param_file_name + "_RF_RS.csv"
        param_grid = {}
        if os.path.exists(paramFiles):
            df = pd.read_csv(paramFiles)
            for index, row in df.iterrows():
                param_grid[row['paramName']] = eval(row['paramValue'])
        

        # Create the random search model
        rf_search = tune_model(log_rf, search_algorithm = "random",custom_grid=param_grid,n_iter=1)#,estimator ='xgboost') #random :random grid

        save_path=root_path+"demo_picture"
        save_name=file_name+"_RF_RS"
        Interpret_shape(rf_search,"shape",save_path,save_name)
  

         
        # paramFiles = param_file_path + param_file_name + "_RF_GS.csv"
        # param_grid = {}
        # if os.path.exists(paramFiles):
        #     df = pd.read_csv(paramFiles)
        #     for index, row in df.iterrows():
        #         param_grid[row['paramName']] = eval(row['paramValue'])

        # Estimator for use in random search 

        # Create the random search model
        rf_grid  = tune_model(log_rf, search_algorithm = "grid",custom_grid=param_grid,n_iter=1) #random :random grid
        save_path=root_path+"demo_picture"
        save_name=file_name+"_RF_GS"
        Interpret_shape(rf_grid,"shape",save_path,save_name)
        # return render(request, 'runModels.html', context) 
    except Exception as e:
        print(e)
        print('stacktrace is ',traceback.print_exc())


def xgboostpycr():
    try:
        csv_file_name = "csvfile_"+user_name
        savefile_x_final = file_path + csv_file_name + "_x_model.csv"
        df = pd.read_csv(savefile_x_final)
        targetVarFile = file_path + csv_file_name + "_targetVar.txt"
        file1 = open(targetVarFile, "r")  # write mode
        targetVar = file1.read()
        file1.close() 
        clf1=setup(data = df, target = targetVar, train_size = 0.7,html=False,silent=True)
         
        log_rf = create_model('xgboost')

        # before  run the model please check which parameters can be used. using thi command
        log_rf.get_params().keys()
        save_path=root_path+"demo_picture"
        save_name=file_name+"_XGB_NT"
        Interpret_shape(log_rf,"shape",save_path,save_name)
        
        # split the dastaset into train, validation and test with the ratio 0.7, 0.2 and 0.1
         
        # Random Search
        paramFiles = param_file_path + param_file_name + "_XGB_RS.csv"
        param_grid = {}
        if os.path.exists(paramFiles):
            df = pd.read_csv(paramFiles)
            for index, row in df.iterrows():
                param_grid[row['paramName']] = eval(row['paramValue'])
        

        # Create the random search model
        rf_search = tune_model(log_rf, search_algorithm = "random",custom_grid=param_grid,n_iter=1)#,estimator ='xgboost') #random :random grid

        save_path=root_path+"demo_picture"
        save_name=file_name+"_XGB_RS"
        Interpret_shape(rf_search,"shape",save_path,save_name) 

        # Create the random search model
        rf_grid  = tune_model(log_rf, search_algorithm = "grid",custom_grid=param_grid,n_iter=1) #random :random grid
        save_path=root_path+"demo_picture"
        save_name=file_name+"_XGB_GS"
        Interpret_shape(rf_grid,"shape",save_path,save_name)
        # return render(request, 'runModels.html', context)
    except Exception as e:
        print(e)
        print('stacktrace is ',traceback.print_exc())


def GBCpycr(request):
    try:
        csv_file_name = "csvfile_"+user_name
        savefile_x_final = file_path + csv_file_name + "_x_model.csv"
        df = pd.read_csv(savefile_x_final)
        targetVarFile = file_path + csv_file_name + "_targetVar.txt"
        file1 = open(targetVarFile, "r")  # write mode
        targetVar = file1.read()
        file1.close()
        
        clf1=setup(data = df, target = targetVar, train_size = 0.7,html=False,silent=True)
         
        log_rf = create_model('gbc')

        # before  run the model please check which parameters can be used. using thi command
        log_rf.get_params().keys()
        save_path=root_path+"demo_picture"
        save_name="SHAP_summary_GBC_NT"
        Interpret_shape(log_rf,"msa",save_path,save_name)
        
        # split the dastaset into train, validation and test with the ratio 0.7, 0.2 and 0.1
         
        # Random Search
        paramFiles = param_file_path + param_file_name + "_GBC_RS.csv"
        param_grid = {}
        if os.path.exists(paramFiles):
            df = pd.read_csv(paramFiles)
            for index, row in df.iterrows():
                param_grid[row['paramName']] = eval(row['paramValue'])
        

        # Create the random search model
        rf_search = tune_model(log_rf, search_algorithm = "random",custom_grid=param_grid,n_iter=1)#,estimator ='xgboost') #random :random grid

        save_path=root_path+"demo_picture"
        save_name="SHAP_summary_GBC_RS"
        Interpret_shape(rf_search,"msa",save_path,save_name) 

        # Create the random search model
        rf_grid  = tune_model(log_rf, search_algorithm = "grid",custom_grid=param_grid,n_iter=1) #random :random grid
        save_path=root_path+"demo_picture"
        save_name="SHAP_summary_GBC_GS"
        Interpret_shape(rf_grid,"msa",save_path,save_name)
        # return render(request, 'runModels.html', context)
        return render(request, 'showdata.html')
    except Exception as e:
        print(e)
        print('stacktrace is ',traceback.print_exc())



def MLPpycr():
    try:
        csv_file_name = "csvfile_"+user_name
        savefile_x_final = file_path + csv_file_name + "_x_model.csv"
        df = pd.read_csv(savefile_x_final)
        targetVarFile = file_path + csv_file_name + "_targetVar.txt"
        file1 = open(targetVarFile, "r")  # write mode
        targetVar = file1.read()
        file1.close()
        print('inside MLP')
        clf1=setup(data = df, target = targetVar, train_size = 0.7,html=False,silent=True)
         
        log_rf = create_model('mlp')

        # before  run the model please check which parameters can be used. using thi command
        log_rf.get_params().keys()
        save_path=root_path+"demo_picture"
        save_name=file_name+"_MLP_NT"
        Interpret_shape(log_rf,"msa",save_path,save_name)
        
        # split the dastaset into train, validation and test with the ratio 0.7, 0.2 and 0.1
         
        # Random Search
        paramFiles = param_file_path + param_file_name + "_MLP_RS.csv"
        param_grid = {}
        if os.path.exists(paramFiles):
            df = pd.read_csv(paramFiles)
            for index, row in df.iterrows():
                param_grid[row['paramName']] = eval(row['paramValue'])
        

        # Create the random search model
        rf_search = tune_model(log_rf, search_algorithm = "random",custom_grid=param_grid,n_iter=1)#,estimator ='xgboost') #random :random grid

        save_path=root_path+"demo_picture"
        save_name=file_name+"_MLP_RS"
        Interpret_shape(rf_search,"msa",save_path,save_name) 

        # Create the random search model
        rf_grid  = tune_model(log_rf, search_algorithm = "grid",custom_grid=param_grid,n_iter=1) #random :random grid
        save_path=root_path+"demo_picture"
        save_name=file_name+"_MLP_GS"
        Interpret_shape(rf_grid,"msa",save_path,save_name)
    except Exception as e:
        print('error is ',e)
        print('stacktrace is ',traceback.print_exc())


def KNNpycr():
    try:
        csv_file_name = "csvfile_"+user_name
        savefile_x_final = file_path + csv_file_name + "_x_model.csv"
        df = pd.read_csv(savefile_x_final)
        targetVarFile = file_path + csv_file_name + "_targetVar.txt"
        file1 = open(targetVarFile, "r")  # write mode
        targetVar = file1.read()
        file1.close() 
        clf1=setup(data = df, target = targetVar, train_size = 0.7,html=False,silent=True)
         
        log_rf = create_model('knn')

        # before  run the model please check which parameters can be used. using thi command
        log_rf.get_params().keys()
        save_path=root_path+"demo_picture"
        save_name=file_name+"_KNN_NT"
        Interpret_shape(log_rf,"shape",save_path,save_name)
        
        # split the dastaset into train, validation and test with the ratio 0.7, 0.2 and 0.1
         
        # Random Search
        paramFiles = param_file_path + param_file_name + "_KNN_RS.csv"
        param_grid = {}
        if os.path.exists(paramFiles):
            df = pd.read_csv(paramFiles)
            for index, row in df.iterrows():
                param_grid[row['paramName']] = eval(row['paramValue'])
        

        # Create the random search model
        rf_search = tune_model(log_rf, search_algorithm = "random",custom_grid=param_grid,n_iter=1)#,estimator ='xgboost') #random :random grid

        save_path=root_path+"demo_picture"
        save_name=file_name+"_KNN_RS"
        Interpret_shape(rf_search,"msa",save_path,save_name) 

        # Create the random search model
        log_rf = create_model('knn')
        rf_grid  = tune_model(log_rf, search_algorithm = "grid",custom_grid=param_grid,n_iter=1) #random :random grid
        save_path=root_path+"demo_picture"
        save_name=file_name+"_KNN_GS"
        Interpret_shape(rf_grid,"msa",save_path,save_name)
    except Exception as e:
        print('error is ',e)
        print('stacktrace is ',traceback.print_exc())



def build_model_multi_choice(mode, classifier,n_select):
    """
    
    #1) You can also pass the untrained models in the include parameter of the compare_models and it will just work normally.
    best=compare_models(include=["lr","dt","knn",ngboost])
     2) #we also can use the scikit-learn model in pycaret
    # such as
    #from ngboost import NGBClassifier
    #ngc=NGBClassifier()
    #ngboost=create_model(ngc)
    """
    if mode=="special_model":
        if classifier=="knn":
            return  create_model(classifier)
        else:
            return  compare_models(include=[classifier])
#           return create_model(classifier, average='None')
    if mode=="all_model_select":
        return compare_models(n_select)
    if mode=="all_model":
        return compare_models()

def Run_and_save_model(model_name,model_save_name,data): 
    best_model=build_model_multi_choice("special_model",model_name,None)
    
    print(best_model)
    predict_model(best_model)
    final_model = finalize_model(best_model)
    save_model(final_model, model_save_name)
    saved_model = load_model(model_save_name)
    train_pipe = saved_model[:-1].transform(data)
    
  
    return saved_model,train_pipe


def shape_all_feather(train_pipe,saved_model):
    print('shape_all_feather inside')
    explainer = shap.TreeExplainer(saved_model.named_steps["trained_model"])
    shap_values = explainer.shap_values(train_pipe)
    shap.initjs()
# # shap.force_plot(explainer.expected_value[0], shap_values[0])
    shap.summary_plot(shap_values,get_config("X_train"),show=False)
    plt.savefig('all_feather_ECAR.png')

def shape_multi_value(train_pipe,saved_model):
    """
    Randomly examine the effect of each feature of one of the samples on the predicted value
    """
    explainer = shap.TreeExplainer(saved_model.named_steps["trained_model"])
    shap_interaction_values = explainer.shap_interaction_values(train_pipe)
    shap.initjs()
    shap.summary_plot(shap_interaction_values[0], get_config("X"), max_display=4,show=False)
    plt.savefig('muti_feather_ECAR.png')

def shape_two_value(train_pipe,saved_model):
    """
    Randomly examine the effect of each feature of one of the samples on the predicted value
    """
    explainer = shap.TreeExplainer(saved_model.named_steps["trained_model"])
    shap_values = explainer.shap_values(train_pipe)
    shap.initjs()
    for i in ["absmax_scaled_raw_score"]:
        shap.dependence_plot('absmax_scaled_raw_score', shap_values[0], get_config("X"), interaction_index=i, show=False)

    plt.savefig('shape_two_value_ECAR.png')


def runpycaret(request):
    try:
        from multiprocessing import Process, Pipe 
        content =request.GET.get('model', 'False')  
        print('pycaret content is ', content) 
        if(content == "RF"): 
            randomForestAjax()
            if os.path.exists(os.path.join(BASE_DIR, plot_dir_view + file_name + "_RF_RS_summary.png")) and os.path.exists(os.path.join(BASE_DIR, plot_dir_view + file_name + "_RF_NT_correlation.png")):
                nt_summary = plot_dir + file_name + "_RF_NT_summary.png"
                nt_correlation = plot_dir + file_name + "_RF_NT_correlation.png"
                nt_msa = plot_dir + file_name + "_RF_NT_msa.png"
                nt_pdp = plot_dir + file_name + "_RF_NT_pdp.png"
                nt_pfi = plot_dir + file_name + "_RF_NT_pfi.png" 
                rs_summary = plot_dir + file_name + "_RF_RS_summary.png"
                rs_correlation = plot_dir + file_name + "_RF_RS_correlation.png"
                rs_msa = plot_dir + file_name + "_RF_RS_msa.png"
                rs_pdp = plot_dir + file_name + "_RF_RS_pdp.png"
                rs_pfi = plot_dir + file_name + "_RF_RS_pfi.png" 
                gs_summary = plot_dir + file_name + "_RF_GS_summary.png"
                gs_correlation = plot_dir + file_name + "_RF_GS_correlation.png" 
                gs_msa = plot_dir + file_name + "_RF_GS_msa.png"
                gs_pdp = plot_dir + file_name + "_RF_GS_pdp.png"
                gs_pfi = plot_dir + file_name + "_RF_GS_pfi.png" 
                context = {'is_data': True,  'model': 'RF', 
                            'nt_summary': nt_summary, 'nt_correlation': nt_correlation, 'nt_msa':nt_msa,'nt_pdp':nt_pdp,'nt_pfi' :nt_pfi,                           
                           'rs_summary': rs_summary, 'rs_correlation': rs_correlation,  'rs_msa':rs_msa,'rs_pdp':rs_pdp,'rs_pfi' :rs_pfi,  
                           'gs_summary': gs_summary, 'gs_correlation': gs_correlation, 'gs_msa':gs_msa,'gs_pdp':gs_pdp,'gs_pfi' :gs_pfi}
            else:
                context = {'is_data': False} 

            return JsonResponse(context)
        elif(content == "XGB"):
            print('xgBoost process started')
            xgboostpycr() 
            if os.path.exists(os.path.join(BASE_DIR, plot_dir_view + file_name + "_XGB_RS_summary.png")) and os.path.exists(os.path.join(BASE_DIR, plot_dir_view + file_name + "_XGB_NT_correlation.png")):
                nt_summary = plot_dir + file_name + "_XGB_NT_summary.png"
                nt_correlation = plot_dir + file_name + "_XGB_NT_correlation.png"
                nt_msa = plot_dir + file_name + "_XGB_NT_msa.png"
                nt_pdp = plot_dir + file_name + "_XGB_NT_pdp.png"
                nt_pfi = plot_dir + file_name + "_XGB_NT_pfi.png" 
                rs_summary = plot_dir + file_name + "_XGB_RS_summary.png"
                rs_correlation = plot_dir + file_name + "_XGB_RS_correlation.png"
                rs_msa = plot_dir + file_name + "_XGB_RS_msa.png"
                rs_pdp = plot_dir + file_name + "_XGB_RS_pdp.png"
                rs_pfi = plot_dir + file_name + "_XGB_RS_pfi.png" 
                gs_summary = plot_dir + file_name + "_XGB_GS_summary.png"
                gs_correlation = plot_dir + file_name + "_XGB_GS_correlation.png" 
                gs_msa = plot_dir + file_name + "_XGB_GS_msa.png"
                gs_pdp = plot_dir + file_name + "_XGB_GS_pdp.png"
                gs_pfi = plot_dir + file_name + "_XGB_GS_pfi.png" 
                context = {'is_data': True,  'model': 'XGB', 
                            'nt_summary': nt_summary, 'nt_correlation': nt_correlation, 'nt_msa':nt_msa,'nt_pdp':nt_pdp,'nt_pfi' :nt_pfi,                           
                           'rs_summary': rs_summary, 'rs_correlation': rs_correlation,  'rs_msa':rs_msa,'rs_pdp':rs_pdp,'rs_pfi' :rs_pfi,  
                           'gs_summary': gs_summary, 'gs_correlation': gs_correlation, 'gs_msa':gs_msa,'gs_pdp':gs_pdp,'gs_pfi' :gs_pfi}
            else:
                context = {'is_data': False} 
            return JsonResponse(context)
        elif(content == "MLP"):
            print('MLP process started')
            MLPpycr() 
            if os.path.exists(os.path.join(BASE_DIR, plot_dir_view + file_name + "_MLP_RS_pdp.png")) and os.path.exists(os.path.join(BASE_DIR, plot_dir_view + file_name + "_MLP_NT_pdp.png")):
                nt_summary = plot_dir + file_name + "_MLP_NT_summary.png"
                nt_correlation = plot_dir + file_name + "_MLP_NT_correlation.png"
                nt_msa = plot_dir + file_name + "_MLP_NT_msa.png"
                nt_pdp = plot_dir + file_name + "_MLP_NT_pdp.png"
                nt_pfi = plot_dir + file_name + "_MLP_NT_pfi.png" 
                rs_summary = plot_dir + file_name + "_MLP_RS_summary.png"
                rs_correlation = plot_dir + file_name + "_MLP_RS_correlation.png"
                rs_msa = plot_dir + file_name + "_MLP_RS_msa.png"
                rs_pdp = plot_dir + file_name + "_MLP_RS_pdp.png"
                rs_pfi = plot_dir + file_name + "_MLP_RS_pfi.png" 
                gs_summary = plot_dir + file_name + "_MLP_GS_summary.png"
                gs_correlation = plot_dir + file_name + "_MLP_GS_correlation.png" 
                gs_msa = plot_dir + file_name + "_MLP_GS_msa.png"
                gs_pdp = plot_dir + file_name + "_MLP_GS_pdp.png"
                gs_pfi = plot_dir + file_name + "_MLP_GS_pfi.png" 
                context = {'is_data': True,  'model': 'MLP', 
                            'nt_summary': nt_summary, 'nt_correlation': nt_correlation, 'nt_msa':nt_msa,'nt_pdp':nt_pdp,'nt_pfi' :nt_pfi,                           
                           'rs_summary': rs_summary, 'rs_correlation': rs_correlation,  'rs_msa':rs_msa,'rs_pdp':rs_pdp,'rs_pfi' :rs_pfi,  
                           'gs_summary': gs_summary, 'gs_correlation': gs_correlation, 'gs_msa':gs_msa,'gs_pdp':gs_pdp,'gs_pfi' :gs_pfi}
            else:
                context = {'is_data': False}  
            return JsonResponse(context)
        elif(content == "KNN"):
            print('KNN process started')
            KNNpycr()  
            if os.path.exists(os.path.join(BASE_DIR, plot_dir_view + file_name + "_KNN_GS_pdp.png")) and os.path.exists(os.path.join(BASE_DIR, plot_dir_view + file_name + "_KNN_NT_pdp.png")):
                nt_summary = plot_dir + file_name + "_KNN_NT_summary.png"
                nt_correlation = plot_dir + file_name + "_KNN_NT_correlation.png"
                nt_msa = plot_dir + file_name + "_KNN_NT_msa.png"
                nt_pdp = plot_dir + file_name + "_KNN_NT_pdp.png"
                nt_pfi = plot_dir + file_name + "_KNN_NT_pfi.png" 
                rs_summary = plot_dir + file_name + "_KNN_RS_summary.png"
                rs_correlation = plot_dir + file_name + "_KNN_RS_correlation.png"
                rs_msa = plot_dir + file_name + "_KNN_RS_msa.png"
                rs_pdp = plot_dir + file_name + "_KNN_RS_pdp.png"
                rs_pfi = plot_dir + file_name + "_KNN_RS_pfi.png" 
                gs_summary = plot_dir + file_name + "_KNN_GS_summary.png"
                gs_correlation = plot_dir + file_name + "_KNN_GS_correlation.png" 
                gs_msa = plot_dir + file_name + "_KNN_GS_msa.png"
                gs_pdp = plot_dir + file_name + "_KNN_GS_pdp.png"
                gs_pfi = plot_dir + file_name + "_KNN_GS_pfi.png" 
                context = {'is_data': True,  'model': 'KNN', 
                            'nt_summary': nt_summary, 'nt_correlation': nt_correlation, 'nt_msa':nt_msa,'nt_pdp':nt_pdp,'nt_pfi' :nt_pfi,                           
                        'rs_summary': rs_summary, 'rs_correlation': rs_correlation,  'rs_msa':rs_msa,'rs_pdp':rs_pdp,'rs_pfi' :rs_pfi,  
                        'gs_summary': gs_summary, 'gs_correlation': gs_correlation, 'gs_msa':gs_msa,'gs_pdp':gs_pdp,'gs_pfi' :gs_pfi}
            else:
                context = {'is_data': False}  
            return JsonResponse(context)

        return render(request, 'showPycaretOutput.html',    {'pdfFile': "", 'model': '0'})
    except Exception as e:
        print(e)
        print('traceback ', traceback.print_exc())
        return render(request, 'error.html')
    

def find_max_file_id(mdlid=""):
    
    print("find_max_file_id")
    src_file_obj = collection_file_info.find({'Mdl_Id':mdlid})
    df =  pd.DataFrame(list(src_file_obj)) 
    if len(df)>0: 
        file_id=df['file_id'].max()
    else:
        file_id=1 #changed by nilesh on 11.4.23
    return file_id

def find_target_value(file_id=0):
    print("find_target_value")    
    target_value_obj=collection_model_target_value.find({'file_id':int(file_id)},{'_id':0})
    a = ''
    for j in target_value_obj:
        # print('j',j)
        print("target value data",j['column_name'])
        a = target_value=j['column_name']  
    return a

def find_src_data(file_id,dataset=''): 
    print('dataset is method is ',dataset)
    if(dataset==''):
        print('inside blank filter')
        src_file_obj = collection.find({"file_id":int(file_id)},{'_id':0})
    else:
        print('dataset ', str(dataset)) 
        dataset = dataset.replace("\'", "\"") 
        dataset=json.loads(dataset)    
        print('dataset is ',dataset)      
        src_file_obj = collection.find(dataset)

    df =  pd.DataFrame(list(src_file_obj)) 
    if len(df)>0:  
        df.pop('file_id')
    print("src fn dataframe",len(df))
    return df 


def find_pyconfig(mdl_id,userid):  
     
    src_file_obj = collection_pyconfig.find({"mdl_id":mdl_id,"user_id":userid})    
    df =  pd.DataFrame(list(src_file_obj))    
    if len(df)>0:
        df.pop('mdl_id')
        df.pop('user_id')
    print("src fn dataframe",len(df))
    return df 

def find_comparemodels(mdl_id,userid):       
    src_file_obj = collection_comparemodels.find({"mdl_id":mdl_id,"user_id":userid})    
    df =  pd.DataFrame(list(src_file_obj))    
    if len(df)>0:
        df.pop('mdl_id')
        df.pop('user_id')
        df.pop('_id')
    print("src fn dataframe",len(df))
    return df 
     