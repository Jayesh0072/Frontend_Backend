from xml.dom.minidom import TypeInfo
from django.shortcuts import render ,redirect
from django.http import HttpResponse 
import pandas as pd
from pycaret.datasets import get_data
import shap
import sklearn
from sklearn.model_selection import train_test_split
import pycaret

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
from .models import descData, lstCnfrmSrc, lstOutlieranomalies, missingDataList, lstColFreq, lstOutlierGrubbs,lstTestModelPerf
from django.http import JsonResponse 
import numpy as np 
# Create your views here.

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
         
        return render(request, 'pycaretsetup.html',{'dataTypes': dropfeatures()})
    except Exception as e:
        print('setuppycaret is ',e)
        print('setuppycaret traceback is ', traceback.print_exc()) 

root_path = "C://Chen_project//project1//"


def dropfeatures():
    try:
        # savefile_x = file_path + file_name + "_x.csv"
        _isDisabled="disabled"
        savefile_withoutnull = file_path + "csvfile_"+file_name + ".csv" 
        df = pd.read_csv(savefile_withoutnull, na_values='?')

        targetVarFile = file_path + "csvfile_"+file_name + "_targetVar.txt"
        file1 = open(targetVarFile, "r")  # write mode
        targetVar = file1.read()
        file1.close()
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

        print('gridDttypes is ',gridDttypes)
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
        df = pd.DataFrame( [[train_size , categorical_imputation  , numeric_imputation  ,ignore_features 
        ,normalize , normalize_method  ,fix_imbalance ,transformation , transformationmethod  ,transform_target
         , transformtargetmethod ,remove_outliers ,outliers_threshold ,remove_multicollinearity ,multicollinearity_threshold
         ,feature_interaction ,feature_ratio ,polynomial_features ,polynomial_degree ,trigonometry_features]] ,
            columns=['train_size', 'categorical_imputation','numeric_imputation','ignore_features'
            ,'normalize','normalize_method','fix_imbalance','transformation','transformation_method','transform_target'
            ,'transform_target_method','remove_outliers','outliers_threshold',
            'remove_multicollinearity','multicollinearity_threshold','feature_interaction','feature_ratio','polynomial_features','polynomial_degree','trigonometry_features'])
        df.to_csv( file_path + user_name + "_pyconfig.csv", index=False, encoding='utf-8')
        print('ignore_features is ',ignore_features )
        return JsonResponse({"is_taken":"True"})
    except Exception as e:
        print('eror is',e,' stacktrace is  ',traceback.print_exc())

def cmpmodels(request):
    try: 
        # print('inside cmpmodels',request.method)
        # gridDttypes=[]
        # result=[]
        msg=""
        if request.method=='GET':
            if os.path.exists(savefile_name):
                if os.path.exists(file_path + user_name + "_pyconfig.csv"):
                    df = pd.read_csv(savefile_name, na_values='?') 
                    # df=df.head(100)
                    ind = np.random.choice(len(df),1000,replace=False)
                    df = df.iloc[ind,:] 
                    dfConfig = pd.read_csv(file_path + user_name + "_pyconfig.csv", na_values='?')
                    csv_file_name = "csvfile_"+user_name
                    targetVarFile = file_path + csv_file_name + "_targetVar.txt"
                    file1 = open(targetVarFile, "r")  # write mode
                    targetVar = file1.read()
                    file1.close()
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
        print('setuppycaret error is ',e) 


def getrebestmodelsut(request):
    try: 
        print('inside cmpmodels',request.method)
        gridDttypes=[]
        result=[]
        msg=""
        if request.method=='GET':
            if os.path.exists(savefile_name):
                if os.path.exists(file_path + user_name + "_pyconfig.csv"):
                    df = pd.read_csv(savefile_name, na_values='?') 
                    # df=df.head(100)
                    ind = np.random.choice(len(df),1000,replace=False)
                    df = df.iloc[ind,:] 
                    dfConfig = pd.read_csv(file_path + user_name + "_pyconfig.csv", na_values='?')
                    csv_file_name = "csvfile_"+user_name
                    targetVarFile = file_path + csv_file_name + "_targetVar.txt"
                    file1 = open(targetVarFile, "r")  # write mode
                    targetVar = file1.read()
                    file1.close()
                    print("targetvar",type(targetVar))
                    if targetVar == "None":
                        print('Please Select Target Variable')
                        msg="Please Select Target Variable."
                    else:
                        print("target variable not None")
                        for index, row in dfConfig.iterrows():    
                            print('row["normalize"] is ',   row["normalize"]  )               
                        # clf=setup(data = df, target = 'status', train_size = 0.7,html=False,silent=True,normalize = False, transformation = False )
                            clf=setup(data = df, target = targetVar, html=False,silent=True,           
                            train_size=row["train_size"], categorical_imputation=eval("'" +row["categorical_imputation"] +"'"),
                            numeric_imputation =eval("'"+row["numeric_imputation"]+"'"),ignore_features =eval(row["ignore_features"])
                            ,normalize =row["normalize"] ,normalize_method=eval("'"+ row["normalize_method"] +"'"),
                            remove_outliers=row["remove_outliers"] ,outliers_threshold =row["outliers_threshold"],
                            remove_multicollinearity =row["remove_multicollinearity"],multicollinearity_threshold=row["multicollinearity_threshold"],
                            feature_interaction=row["feature_interaction"] ,feature_ratio=row["feature_ratio"]
                            ,polynomial_features =row["polynomial_features"],polynomial_degree=row["polynomial_degree"] ,trigonometry_features=row["trigonometry_features"] 
                            ,fix_imbalance=row["fix_imbalance"]
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
                            dfmodels.to_csv( file_path + user_name + "_comparemodels.csv", index=True, encoding='utf-8')
                            # 
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
        if os.path.exists(savefile_name):
            dfcnt = pd.read_csv(savefile_name)
            lendf=len(dfcnt)
            print(str(lendf))
            if os.path.exists(file_path + user_name + "_pyconfig.csv"):      
                if os.path.exists(file_path + user_name + "_comparemodels.csv"): 
                    dfmodels = pd.read_csv(file_path + user_name + "_comparemodels.csv")
                
                    dfmodels.columns.values[0] = "modelSN"
                    gridDttypes = []
                    dttypes = dict(dfmodels.dtypes)
                    # print(dttypes)
                    for key, value in dttypes.items():
                        gridDttypes.append({'colName': key, 'dataType': value})
                    result = dfmodels.to_json(orient="records")
                    result = json.loads(result)
                    

                    del dfmodels
                else:
                    print("Please Select Compare Model First")    
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
        print('model selected is ',model)
        print('dataSize is ',dataSize)
        if os.path.exists(savefile_name):
            if os.path.exists(file_path + user_name + "_pyconfig.csv"):
                df = pd.read_csv(savefile_name, na_values='?') 
                ind = np.random.choice(len(df),int(dataSize),replace=False)
                df = df.iloc[ind,:]
                dfConfig = pd.read_csv(file_path + user_name + "_pyconfig.csv", na_values='?')
                 
                bestModel=model
                csv_file_name = "csvfile_"+user_name
                targetVarFile = file_path + csv_file_name + "_targetVar.txt"
                file1 = open(targetVarFile, "r")  # write mode
                targetVar = file1.read()
                file1.close()
                
                for index, row in dfConfig.iterrows():    
                    print('row["normalize"] is ',   row["normalize"]  )               
                # clf=setup(data = df, target = 'status', train_size = 0.7,html=False,silent=True,normalize = False, transformation = False )
                    clf=setup(data = df, target = targetVar, html=False,silent=True,           
                     train_size=row["train_size"], categorical_imputation=eval("'" +row["categorical_imputation"] +"'"),
                      numeric_imputation =eval("'"+row["numeric_imputation"]+"'"),ignore_features =eval(row["ignore_features"])
                      ,normalize =row["normalize"] ,normalize_method=eval("'"+ row["normalize_method"] +"'"),
                      remove_outliers=row["remove_outliers"] ,outliers_threshold =row["outliers_threshold"],
                    remove_multicollinearity =row["remove_multicollinearity"],multicollinearity_threshold=row["multicollinearity_threshold"],
                     feature_interaction=row["feature_interaction"] ,feature_ratio=row["feature_ratio"]
                    ,polynomial_features =row["polynomial_features"],polynomial_degree=row["polynomial_degree"] ,trigonometry_features=row["trigonometry_features"] 
                    ,fix_imbalance=row["fix_imbalance"]
                    )
                    #  transform_target =row["transform_target"], not working  transform_target_method=eval("'"+row["transform_target_method"]+"'"
                    best = create_model(bestModel) 
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

def updateParams(request):
    try:
        print("tryblock")
        model =request.GET.get('model', 'False')
        nitr =int(request.GET.get('nitr', '10'))
        matric =request.GET.get('matric', 'Accuracy')
        library =request.GET.get('library', 'scikit-learn')
        algo =request.GET.get('algo', 'None')
        autobetter =request.GET.get('autobetter', 'False')
        dataSize=request.GET.get('dataSize', '1000') 
        print('nitr is ',nitr)
        if os.path.exists(savefile_name):
            if os.path.exists(file_path + user_name + "_pyconfig.csv"):
                df = pd.read_csv(savefile_name, na_values='?') 
                ind = np.random.choice(len(df),int(dataSize),replace=False)
                df = df.iloc[ind,:]
                dfConfig = pd.read_csv(file_path + user_name + "_pyconfig.csv", na_values='?')
                 
                bestModel=model
                csv_file_name = "csvfile_"+user_name
                targetVarFile = file_path + csv_file_name + "_targetVar.txt"
                file1 = open(targetVarFile, "r")  # write mode
                targetVar = file1.read()
                file1.close()
                for index, row in dfConfig.iterrows():    
                    # print('row["normalize"] is ',   row["normalize"]  )               
                # clf=setup(data = df, target = 'status', train_size = 0.7,html=False,silent=True,normalize = False, transformation = False )
                    clf=setup(data = df, target = targetVar, html=False,silent=True,           
                     train_size=row["train_size"], categorical_imputation=eval("'" +row["categorical_imputation"] +"'"),
                      numeric_imputation =eval("'"+row["numeric_imputation"]+"'"),ignore_features =eval(row["ignore_features"])
                      ,normalize =row["normalize"] ,normalize_method=eval("'"+ row["normalize_method"] +"'"),
                      remove_outliers=row["remove_outliers"] ,outliers_threshold =row["outliers_threshold"],
                    remove_multicollinearity =row["remove_multicollinearity"],multicollinearity_threshold=row["multicollinearity_threshold"],
                     feature_interaction=row["feature_interaction"] ,feature_ratio=row["feature_ratio"]
                    ,polynomial_features =row["polynomial_features"],polynomial_degree=row["polynomial_degree"] ,trigonometry_features=row["trigonometry_features"] 
                    ,fix_imbalance=row["fix_imbalance"]
                    )
                    #  transform_target =row["transform_target"], not working  transform_target_method=eval("'"+row["transform_target_method"]+"'"
                    best = create_model(bestModel)
 
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
        print('stacktrace is ',traceback.print_exc())
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
        # ty="Test"#request.Get.get('type', 'False'
      
        summaryNm,rocaucNm,featureNm,correlationNm ,pdpNm,pfiNm,msaNm,ksNm,liftNm,gainNm,calibrationNm,rocNm="NA.png","NA.png","NA.png","NA.png","NA.png","NA.png","NA.png","NA.png","NA.png","NA.png","NA.png","NA.png"
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

        if os.path.exists(plot_dir_view+"//"+ user_name+'_Calibration_'+bestModel+'_'+ ty+ '.png'):
            calibrationNm=user_name+ '_Calibration_'+bestModel+'_'+ ty+ '.png'

        if os.path.exists(plot_dir_view+"//"+ user_name+'_KS_'+bestModel+'_'+ ty+ '.png'):
            ksNm=user_name+ '_KS_'+bestModel+'_'+ ty+ '.png'

        if os.path.exists(plot_dir_view+"//"+ user_name+'_Gain_'+bestModel+'_'+ ty+ '.png'):
            gainNm=user_name+ '_Gain_'+bestModel+'_'+ ty+ '.png'

        if os.path.exists(plot_dir_view+"//"+ user_name+'_Lift_'+bestModel+'_'+ ty+ '.png'):
            liftNm=user_name+ '_Lift_'+bestModel+'_'+ ty+ '.png'        

        context={'bestModel':modelNm,'modelSS':bestModel,
                'clsrpt':'/'+plot_dir_view+'/'+ user_name+ '_classification_report_'+bestModel+'_'+ ty+ '.png',
                 'auc':'/'+plot_dir_view+'/'+ rocaucNm,
                 'cnfmtrx':'/'+plot_dir_view+'/'+ user_name+ '_Confusion_Matrix_'+bestModel+'_'+ ty+ '.png',
                 'calibration':'/'+plot_dir_view+'/'+ calibrationNm,
                 'lift':'/'+plot_dir_view+'/'+liftNm,
                 'gain':'/'+plot_dir_view+'/'+ gainNm,
                 'ks':'/'+plot_dir_view+'/'+ksNm,
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