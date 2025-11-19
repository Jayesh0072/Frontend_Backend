from app1.DAL.dboperations import dbops
import json
class UserInfo:
    objdbops =None

    def __init__(self):
        self.objdbops=dbops()

    def validateUser(self,uname,pwd):
        return self.objdbops.getTable("select usr.*,uc.UC_Level from Users usr, User_Category uc where uc.uc_AID=usr.UC_AID and u_name='" + uname + "' and U_password ='" + pwd.replace("'","''") +"'") 