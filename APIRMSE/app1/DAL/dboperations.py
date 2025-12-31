import pyodbc 
import traceback
import os

import json 
import pandas as pd
# DEFINE THE DATABASE CREDENTIALS
# user = 'sa'
# password = 'sqlAdm_18'
# host = 'DESKTOP-NH98228\HCSPL18'
# port = 1433
# database = 'RMSE'

user = 'sa'
password = 'Ajit@123'
host = 'LENOVOARUN\SQL2022'
port = 1433
database = 'prope_db'

class dbops:
    
    def getscalar(self,strQ :str):
        try:
            cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+host+';DATABASE='+database+';UID='+user+';PWD='+password) 
            # Create a cursor from the connection
            cursor = cnxn.cursor()
            val = cursor.execute(strQ).fetchval()
            cnxn.close()
            return val
        except Exception as e:
            print('getscalar is ',e)
            print('getscalar traceback is ', traceback.print_exc()) 

    def insertRow(self,strQ :str):
        try:
            # Specifying the ODBC driver, server name, database, etc. directly
            cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+host+';DATABASE='+database+';UID='+user+';PWD='+password)

            # Create a cursor from the connection
            cursor = cnxn.cursor()

            # Do the insert
            cursor.execute(strQ)
            #commit the transaction
            cnxn.commit()
            cnxn.close()
        except Exception as e:
            print('insertRow is ',strQ,e)
            print('insertRow traceback is ', traceback.print_exc()) 

    def getTable(self,strQ :str):
        try:
            cnxn=pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+host+';DATABASE='+database+';UID='+user+';PWD='+password)
            cursor = cnxn.cursor()
            cursor.execute(strQ)
            data = cursor.fetchall() 
            tableResult = pd.DataFrame.from_records(data, columns=[col[0] for col in cursor.description])    
            cnxn.close()
            return tableResult
        except Exception as e:
            print('getTable is ',e)
            print('getTable traceback is ', traceback.print_exc()) 
