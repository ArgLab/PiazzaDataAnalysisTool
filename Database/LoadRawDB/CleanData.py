#!/usr/bin/env python2.7
"""
CleanData.py
:Author: Adithya Seshadri	
:Date: 2/12/2016

This code cleans the Users, Piazza, and Moodle Data that are not in the class and redundant.
"""

#-----------------------------------------------
#Imports.
#-----------------------------------------------
import sys
from pyexcel_xlsx import get_data
# import unicodecsv as csv
import datetime
import pandas as pd
# Ming imports required for class definition.
# -------------------------------------------
from ming import schema
from ming.odm.declarative import MappedClass
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty

# Load of core library and error class.
# -----------------------------------------------------
import ModSocDB
from ModSocDB import ModSocDBError
import ModSocDB.Utils as Utils
import ModSocDB.Classes.Piazza as PiazzaMod
import ModSocDB.Classes.User as UserMod
from ModSocDB.Classes.User import *
import ModSocDB.Classes.Dataset as DatasetMod


# a date to cut all the activities after. For removing any logs made after the class finished.
cutoff = datetime.datetime.strptime("2018-12-26 23:59:59", "%Y-%m-%d %H:%M:%S") # @Ri changed the cutoff time to match our data

#------------------------------------------------
#Main Arguments.
#------------------------------------------------

DatasetShortName = sys.argv[1]
MasterFile = sys.argv[2]

# -------------------------------------------------
# Get the Dataset.
# -------------------------------------------------

Dataset = DatasetMod.findDatasetByShortName(DatasetShortName)

if (Dataset == None):
    raise ModSocDB.ModSocDBError, \
      "No matching Dataset found: %s" % (DatasetShortName)

print Dataset


#--------------------------------------------------
#Load the Master user file.
#--------------------------------------------------

filename = MasterFile.split("/")[-1]
# user_data = get_data(MasterFile)[filename]
df = pd.read_csv(MasterFile) # @Ri changing the pd.read_csv to read comma-separated .csv file instead of \t-separated .csv file
print list(df)
# print user_data
# in some type of OS, it doesn't return list and needs to change to become the list
# masterUserData = user_data if isinstance(user_data, list) else user_data['master-cleaned-2016-02']
# masterUserData = [dict(zip(user_data[0],row)) for row in user_data[1:]]
# print masterUserData[0]

# masterUserDataDict = [row['username'] for row in masterUserData]
masterUserDataDict = df['username'].tolist()
# ----------------------------------------------------
# Merge the TA users
# ----------------------------------------------------
unknown_user = UserMod.User.makeNewUser(Dataset._id, "unknown",
                    Email="unknown@ncsu.edu", Username="unknown",
                    Role="Student")

masterUserDataDict.append("unknown") # to add it as an acceptable user

#List of TAs and Instructors
TAusernames = []
TAnames = []


#--------------------------------------------------
#Clean the Piazza Activities.
#--------------------------------------------------
Content = PiazzaMod.PiazzaContent.findAllContent()

for c in Content:
    if not c.CentralAuthor:
        # Add the unknown user for users with no Author (anonymous posts)
        if c.CentralAuthor_ID and len(User.query.find({'_id': c.CentralAuthor_ID}).all())>0:
                u = User.query.find({'_id': c.CentralAuthor_ID}).all()[0]
                c.CentralAuthor = u
        else:    
            c.CentralAuthor = unknown_user 
    if (c.CentralAuthor != None and c.CentralAuthor.username not in masterUserDataDict):
    # if c.created > cutoff or (c.CentralAuthor != None and c.CentralAuthor.username not in masterUserDataDict):
        for cl in c.ChangeLog:
            cl.delete()
        for h in c.History:
            h.delete()
        for cd in c.Children:
            for ch in cd.History:
                ch.delete()
            for sc in cd.Subchildren:
                sc.delete()
            cd.delete()
        c.delete()
                
    # if c.CentralAuthor == None:
        # for cl in c.ChangeLog:
        #     if cl.type == 'create' and cl.anon == 'no':
        #         # writer.writerow([c.CentralAuthor_ID,c.id,c.created])
        #         for cl in c.ChangeLog:
        #             cl.delete()
        #             # writer.writerow(['','log '+cl.type,cl.when])
        #         for h in c.History:
        #             h.delete()
        #             # writer.writerow(['','history',h.created])
        #         for cd in c.Children:
        #             # writer.writerow(['','child '+cd.id,cd.created])                    
        #             for ch in cd.History:
        #                 ch.delete()
        #                 # writer.writerow(['','child history',ch.created])
        #             for sc in cd.Subchildren:
        #                 sc.delete()
        #                 # writer.writerow(['','subchild '+sc.id,sc.created])
        #             cd.delete()
        #         c.delete()
ModSocDB.Session.flush()

logs = PiazzaMod.PiazzaContent_ChangeLog.findAllChangeLogs()    
# with open('removepiazzalogs.csv','wb') as fp:
#     writer = csv.writer(fp, delimiter=',',encoding='utf-8')
for log in logs:
    if log.CentralAuthor != None:
        if log.when > cutoff or log.CentralAuthor.username not in masterUserDataDict:            
            log.delete()
            # writer.writerow([log.CentralAuthor.username,log.type,log.when,log.anon])                       
    else:
        if log.anon == 'no' or log.when > cutoff:
            log.delete()
            # writer.writerow(['',log.type,log.when,log.anon])
ModSocDB.Session.flush()
                
history = PiazzaMod.PiazzaContent_History.findAllContentHistory()    
# with open('removepiazzahistory.csv','wb') as fp:
#     writer = csv.writer(fp, delimiter=',',encoding='utf-8')
for hist in history:
    if hist.CentralAuthor != None:
        if hist.created > cutoff or hist.CentralAuthor.username not in masterUserDataDict:            
            hist.delete()
            # writer.writerow([hist.CentralAuthor.username,hist.subject,hist.created,hist.anon])           
    else:
        if hist.anon == 'no' or hist.created > cutoff:
            hist.delete()
            # writer.writerow(['',hist.subject,hist.created,hist.anon])
ModSocDB.Session.flush()

children = PiazzaMod.PiazzaContent_Child.findAllChildren()    
# with open('removepiazzachildren.csv','wb') as fp:
#     writer = csv.writer(fp, delimiter=',',encoding='utf-8')
for child in children :
    if child.CentralAuthor != None:      
        if child.created > cutoff or child.CentralAuthor.username not in masterUserDataDict or child.Parent is None:            
            child.delete()
            # writer.writerow([child.CentralAuthor.username,child.id,child.created,child.anon])                                              
    else:
        if child.anon == 'no' or child.created > cutoff:
            child.delete()
        else:
            if child.CentralAuthor_ID and len(User.query.find({'_id': child.CentralAuthor_ID}).all())>0:
                u = User.query.find({'_id': child.CentralAuthor_ID}).all()[0]
                child.CentralAuthor = u
            else:    
                # c.CentralAuthor = unknown_user 
                child.CentralAuthor = unknown_user
            # writer.writerow(['',child.id,child.created,child.anon])
ModSocDB.Session.flush()

subchildren = PiazzaMod.PiazzaContent_Child_Subchild.findAllSubchildren()    
# with open('removepiazzasubchildren.csv','wb') as fp:
#     writer = csv.writer(fp, delimiter=',',encoding='utf-8')
for subchild in subchildren :
    if subchild.CentralAuthor != None:      
        if subchild.created > cutoff or subchild.CentralAuthor.username not in masterUserDataDict or subchild.Parent is None:            
            subchild.delete()
            # writer.writerow([subchild.CentralAuthor.username,subchild.id,subchild.created,subchild.anon])                                              
    else:
        if subchild.anon == 'no' or subchild.created > cutoff:
            subchild.delete()
        else:
            if subchild.CentralAuthor_ID and len(User.query.find({'_id': subchild.CentralAuthor_ID}).all())>0:
                u = User.query.find({'_id': subchild.CentralAuthor_ID}).all()[0]
                subchild.CentralAuthor = u
        else:    
            subchild.CentralAuthor = unknown_user 

            # subchild.CentralAuthor = unknown_user
            # writer.writerow(['',subchild.id,subchild.created,subchild.anon])
ModSocDB.Session.flush()

childrenhistory = PiazzaMod.PiazzaContent_Child_History.findAllChildHistories()    
# with open('removepiazzachildrenhistory.csv','wb') as fp:
#     writer = csv.writer(fp, delimiter=',',encoding='utf-8')
for childhist in childrenhistory :
    if childhist.CentralAuthor != None:      
        if childhist.created > cutoff or childhist.CentralAuthor.username not in masterUserDataDict:            
            childhist.delete()
            # writer.writerow([childhist.CentralAuthor.username,childhist.content,childhist.created,childhist.anon])                                              
    else:
        if childhist.anon == 'no' or childhist.created > cutoff:
            childhist.delete()
            # writer.writerow(['',childhist.content,childhist.created,childhist.anon])
ModSocDB.Session.flush()



                
#--------------------------------------------------
#Clean the Central Users.
#--------------------------------------------------

CentralUsers = UserMod.findAllUsers()

for cusr in CentralUsers:
    if cusr.username in masterUserDataDict:     
        if cusr.PiazzaUser:
            # writer1.writerow([cusr.username,cusr.name,cusr.role,cusr.email,"True","False",(cusr.MoodleActions!=[])])
            pass
        elif cusr.username == 'unknown': # this user is used for anonymous posts, there is no relating user with it
            pass
        else:  
            cusr.delete() 
    else:
        cusr.delete()
            
ModSocDB.Session.flush()


#--------------------------------------------------
#Clean the Piazza Users.
#--------------------------------------------------
pUsers = PiazzaMod.PiazzaUser.findAllUsers()
remove = list()
for user in pUsers:
    if not user.CentralUser:
        user.delete()
    else:
        user.CentralUser.PiazzaDays = user.days
        user.CentralUser.PiazzaViews = user.views
        user.CentralUser.PiazzaAnswers = user.answers
        user.CentralUser.PiazzaAsks = user.asks
        user.delete()
ModSocDB.DocumentSession.db.drop_collection('piazza_users')        
ModSocDB.Session.flush()    

#--------------------------------------------------
#Remove endorsements.
#--------------------------------------------------
ModSocDB.DocumentSession.db.drop_collection('piazza_content_tag_good')
ModSocDB.DocumentSession.db.drop_collection('piazza_content_children_tagendorse')
