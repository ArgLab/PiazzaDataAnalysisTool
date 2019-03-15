# This file is covered by the LICENSE file in the root of this project.
# @license <https://github.com/ArgLab/PiazzaDataAnalysisTool/LICENSE>
#!/usr/bin/env python
"""
TransactionConversion.py
:Author: Adithya Seshadri
:Date: 2/9/2016

This module defines PiazzaTransanction class that aggregates 
the data from all the piazza collections and wraps it up in 
to a transactional format.
"""

import ModSocDB
from ModSocDB.Classes.Piazza.PiazzaContent import *
from ModSocDB.Classes.Piazza.PiazzaContent_Child import *
from ModSocDB.Classes.Piazza.PiazzaContent_Child_Subchild import *

import unicodecsv as csv

class PiazzaTransaction:
    """
    This class consists of a transaction object corresponding to 
    the Piazza data.This class object represents the data aggregated 
    over all the piazza collectionsand combined to a single class.

    Collection: 
    ------------------------------------------------------------------------------
    piazza_content
    piazza_content_changelog
    piazza_content_children
    piazza_content_history
    piazza_content_children_history
    piazza_content_children_subchildren

    Fields:
    ------------------------------------------------------------------------------ 
    username :         Username of the author
    ThreadID :         Thread ID of the Post
    MongoPostID :      Mongodb Object ID (Unique)
    MongoAuthorID :    Mongodb ID of the Author
    MongoParentID :    Mongodb ID of the Parent Post
    PiazzaPostID :     Piazza ID of the Post
    PiazzaAuthorID :   Piazza ID of the Author
    PiazzaParentID:    Piazza ID of the parent post
    Time :             Date of the Content creation
    ActionType :       Type of the Action represented by the log
    PostType :         Type of Post for the parent post
    PostStatus :       Status of the post
    Subject :          Subject of the Content
    Anon :             String indicating anonimity of the author
    Folders :          (string) List of folders it is in.
    Content :          Post Content
    Source :           Source location of the transaction.   
    """
    def __init__(self):        
        self.username = ""
        self.ThreadID = ""  
        self.PiazzaAuthorID = ""
        self.Time = ""
        # self.ActionType = ""
        self.PostType = ""
        self.PostStatus = ""
        self.Anon = ""
        self.Subject = ""
        self.Folders = ""
        self.Content = ""
        # self.Source = ""

    def createPostTransaction(self,post):
        if  post.CentralAuthor:
            self.username = post.CentralAuthor.username
            self.PiazzaAuthorID = post.CentralAuthor.PiazzaID
        else:
            self.username = None
            self.PiazzaAuthorID = None
        self.ThreadID = post.ThreadID
        self.Time = post.created
        # self.ActionType = post.type
        self.PostType = 'Post'
        self.PostStatus = post.status
        # self.Anon = post.anon
        self.Folders = set(post.folders)
        self.Folders = self.Folders.intersection(set(validFolders))
        self.Folders = [folder in self.Folders for folder in validFolders]
        # self.Source = "Piazza"
        history = post.getLatestHistory()
        if history:
            self.Subject = history.subject
            self.Content = history.content  
        # for hist in post.Content.History:
        #     if abs(hist.created-post.created).total_seconds() < 60:
        #         self.Subject = hist.subject
        #         self.Content = hist.content           
    
    def createFollowupTransactions(self, post):
        if  post.CentralAuthor:
            self.username = post.CentralAuthor.username
            self.PiazzaAuthorID = post.CentralAuthor.PiazzaID
        else:
            self.username = None
            self.PiazzaAuthorID = None
        self.ThreadID = post.ThreadID
        self.Time = post.created
        # self.ActionType = post.type
        self.PostType = 'Reply'
        # self.PostStatus = post.status
        # self.Anon = post.anon
        self.Folders = set(post.folders)
        self.Folders = self.Folders.intersection(set(validFolders))
        self.Folders = [folder in self.Folders for folder in validFolders]
        # self.Source = "Piazza"
        # history = post.getLatestHistory()
        self.Subject = ""
        self.Content = post.content
        # if log.anon != 'full' and log.CentralAuthor:
        #     self.username = log.CentralAuthor.username
        #     self.PiazzaAuthorID = log.CentralAuthor.PiazzaID
        # else:
        #     self.username = None
        #     self.PiazzaAuthorID = None
        # self.ThreadID = log.ThreadID
        # self.Time = log.created
        # self.ActionType = log.type
        # self.PostType = log.Content.type
        # self.PostStatus = log.Content.status
        # self.Anon = log.anon        
        # self.Source = "Piazza"    
        # for ch in log.Content.Children:
        #     if abs(ch.created-log.created).total_seconds() < 60:
        #         self.PiazzaPostID = ch.id
        #         self.Folders = set(ch.folders)
        #         self.Folders = self.Folders.intersection(set(validFolders))
        #         self.Folders = [folder in self.Folders for folder in validFolders]
        #         if ch.getLatestHistory():
        #             print 'something has history'
        #         self.Content = ch.content 
            
    # def createDupeTransactions(self,log):
    #     if log.anon != 'full' and log.CentralAuthor:
    #         self.username = log.CentralAuthor.username
    #         self.PiazzaAuthorID = log.CentralAuthor.PiazzaID
    #     else:
    #         self.username = None
    #         self.PiazzaAuthorID = None
    #     self.ThreadID = log.ThreadID
    #     self.Time = log.created
    #     self.ActionType = log.type
    #     self.PostType = log.Content.type
    #     self.PostStatus = log.Content.status
    #     self.Anon = log.anon        
    #     self.Source = "Piazza"

    def createFeedbackTransactions(self,post):
        if  post.CentralAuthor:
            self.username = post.CentralAuthor.username
            self.PiazzaAuthorID = post.CentralAuthor.PiazzaID
        else:
            self.username = None
            self.PiazzaAuthorID = None
        self.ThreadID = post.ThreadID
        self.Time = post.created
        # self.ActionType = post.type
        self.PostType = 'ReplyToReply'
        # self.PostStatus = post.status
        # self.Anon = post.anon
        self.Folders = set(post.folders)
        self.Folders = self.Folders.intersection(set(validFolders))
        self.Folders = [folder in self.Folders for folder in validFolders]
        # self.Source = "Piazza"
        # history = post.getLatestHistory()
        self.Subject = ""
        self.Content = post.content
        # if log.anon != 'full' and log.CentralAuthor:
        #     self.username = log.CentralAuthor.username
        #     self.PiazzaAuthorID = log.CentralAuthor.PiazzaID
        # else:
        #     self.username = None
        #     self.PiazzaAuthorID = None     
        # self.ThreadID = log.ThreadID        
        # self.Time = log.created
        # self.ActionType = log.type
        # self.PostType = log.Content.type
        # self.PostStatus = log.Content.status
        # self.Anon = log.anon        
        # self.Source = "Piazza"    
        # for ch in log.Content.Children:
        #     for sc in ch.Subchildren:
        #         if abs(sc.created-log.created).total_seconds() < 60:
        #             # print 'here'
        #             self.PiazzaPostID = sc.id
        #             self.PiazzaParentID = sc.Parent.id
        #             self.Folders = set(sc.folders)
        #             self.Folders = self.Folders.intersection(set(validFolders))
        #             self.Folders = [folder in self.Folders for folder in validFolders]
        #             self.Content = sc.content                       

    # def createAnswerTransactions(self,log):
    #     if log.anon != 'full' and log.CentralAuthor:
    #         self.username = log.CentralAuthor.username
    #         self.PiazzaAuthorID = log.CentralAuthor.PiazzaID
    #     else:
    #         self.username = None
    #         self.PiazzaAuthorID = None
    #     self.ThreadID = log.ThreadID
    #     self.Time = log.created
    #     self.ActionType = log.type
    #     self.PostType = log.Content.type
    #     self.PostStatus = log.Content.status
    #     self.Anon = log.anon        
    #     self.Source = "Piazza"            
    #     for ch in log.Content.Children:
    #         if abs(ch.created-log.created).total_seconds() < 60 or log.type == 'i_answer_update' or log.type == 's_answer_update':
    #             for chist in ch.History:
    #                 if abs(chist.created-log.created).total_seconds() < 60:
    #                     self.PiazzaPostID = chist.Parent.id
    #                     self.Folders = set(chist.Parent.folders)
    #                     self.Folders = self.Folders.intersection(set(validFolders))
    #                     self.Folders = [folder in self.Folders for folder in validFolders]
    #                     self.Content = chist.content
            
def convertToTransactions():
    PiazzaTransactions = list()
    posts = PiazzaContent.query.find().all()
    replies = PiazzaContent_Child.query.find().all() 
    reply_to_replies = PiazzaContent_Child_Subchild.query.find().all()
    for post in posts:
        PiazzaTrans = PiazzaTransaction()            
        PiazzaTrans.createPostTransaction(post) 
        PiazzaTransactions.append(PiazzaTrans)        
    for post in replies:
        PiazzaTrans = PiazzaTransaction()            
        PiazzaTrans.createFollowupTransactions(post) 
        PiazzaTransactions.append(PiazzaTrans)
    for post in reply_to_replies:
        PiazzaTrans = PiazzaTransaction()            
        PiazzaTrans.createFeedbackTransactions(post) 
        PiazzaTransactions.append(PiazzaTrans)  
    return PiazzaTransactions      
    # logs = Piazza.PiazzaContent_ChangeLog.findAllChangeLogs()
    # PiazzaTransactions = list()
    # for log in logs:      
    #     # if log.type == 'create' or log.type == 'update':
    #     PiazzaTrans = PiazzaTransaction()            
    #     PiazzaTrans.createPostTransaction(log)
    #         PiazzaTransactions.append(PiazzaTrans)
    #     elif log.type == 'followup':
    #         PiazzaTrans = PiazzaTransaction()
    #         PiazzaTrans.createFollowupTransactions(log)
    #         PiazzaTransactions.append(PiazzaTrans)
    #     elif log.type == 'feedback':
    #         PiazzaTrans = PiazzaTransaction()
    #         PiazzaTrans.createFeedbackTransactions(log)
    #         PiazzaTransactions.append(PiazzaTrans)
    #     elif log.type == 'attach' or log.type == 'dupe':
    #         PiazzaTrans = PiazzaTransaction()
    #         PiazzaTrans.createDupeTransactions(log)
    #         PiazzaTransactions.append(PiazzaTrans)
    #     else:
    #         PiazzaTrans = PiazzaTransaction()
    #         PiazzaTrans.createAnswerTransactions(log)
    #         PiazzaTransactions.append(PiazzaTrans)
    # return PiazzaTransactions

validFolders = []
PostTransactions = convertToTransactions()
PostTransactions.sort(key=lambda x:(x.ThreadID, x.Time))
with open("PiazzaTransactions.csv","wb") as fp:
    writer = csv.writer(fp,delimiter=',')
    writer.writerow(['Username','Thread ID','Piazza Author ID','Time','Post Type','Post Status','Anon','Subject','Content'])
    for trans in PostTransactions:
        writer.writerow([trans.username,trans.ThreadID,trans.PiazzaAuthorID,trans.Time,trans.PostType,trans.PostStatus,trans.Anon,trans.Subject,trans.Content])