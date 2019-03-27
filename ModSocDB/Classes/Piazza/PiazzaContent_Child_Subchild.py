# This file is covered by the LICENSE file in the root of this project.
# @license <https://github.com/ArgLab/PiazzaDataAnalysisTool/blob/master/LICENSE>
#!/usr/bin/env python
"""
PiazzaContent_Child_Subchild.py
:Author: Collin Lynch
:Date: 10/28/2014

History record for Piazza Content Children.
"""


# -------------------------------------------
# imports.
# ===========================================
import datetime, copy

from ming import schema
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty
# from ming.odm import Mapper
from ming.odm.declarative import MappedClass


# Load the shared session objects and library classes.
# -----------------------------------------------------
import ModSocDB
import PiazzaUser
from .. import User as UserMod


# ================================================
class PiazzaContent_Child_Subchild(MappedClass):
    """
    Subchildren of the child posts that is, replies to replies.
  
    Collection: piazza_content_children_subchildren  

    Relations:
    * Dataset: Link to the associated Dataset.
    * Parent: Parent Piazza Content.
    * Author: Link to the associated user.
    * CentralAuthor: The Central author object for this user.

    Fields:
    * Course_ID: ID of the associated Dataset.
    * Parent_ID: ID of parent content.
    * Author_ID: ID of original author.
    * CentralAuthor_ID: Mongoid of the Central author of this change.
    * _id: Mongodb object ID (unique).
    * ThreadID: (int) Unknown int believed to be post number.
    * folders: (string) Folders this element is in.
    * updated: (datetime) Date of last update?
    * uid: (string) Piazza id of original author.
    * created: (datetime) Date created.
    * anon: (string) setting indicating anonymous creation.
    * bucket_name: (string) Storage bucket for this item.
    * bucket_order: (int) Location in the bucket.
    * id: (string) internal id of the subchild item.
    * type: (string) Sub-post type.  
    * subject: (string) Sub-post subject.
    """

    # ---------------------------------------------
    # Mongometa information.
    # =============================================
    class __mongometa__:
        session = ModSocDB.Session
        name = "piazza_content_children_subchildren"

    
    # ------------------------------------------------
    # Link information.
    # ================================================

    # Link to the associated Dataset.
    Course_ID = ForeignIdProperty('Dataset')
    Course    = RelationProperty('Dataset')

    # Parent Piazza Content.
    Parent_ID = ForeignIdProperty('PiazzaContent_Child')
    Parent = RelationProperty('PiazzaContent_Child')

    # Link to the associated user.
    Author_ID = ForeignIdProperty('PiazzaUser.PiazzaUser')
    Author = RelationProperty('PiazzaUser.PiazzaUser')

    # Direct link to the central author instance.
    CentralAuthor_ID = ForeignIdProperty('User')
    CentralAuthor = RelationProperty('User')


    # ------------------------------------------------
    # Fields
    # ================================================

    # Mongodb object ID (unique).
    _id     = FieldProperty(schema.ObjectId)

    # Folders this element is in.
    folders = FieldProperty([str])

    # Date of last update?
    updated = FieldProperty(datetime.datetime)

    # Not containing a valuable information, removed for now
    # d_bucket = FieldProperty(str)

    # int for post number.
    ThreadID = FieldProperty(int)
    
    # UID of author now in link.
    uid = FieldProperty(str)
    
    # Date created.
    created = FieldProperty(datetime.datetime)

    # config information empty at present.
    config = FieldProperty(dict())

    # Created anonymously
    anon = FieldProperty(str)

    # Storage bucket for this item.
    bucket_name = FieldProperty(str)

    # Location in the bucket.
    bucket_order = FieldProperty(int)

    # Id of the subchild item.
    id = FieldProperty(str)
    
    # Sub-post type.  
    type = FieldProperty(str)

    # Sub-post subject.
    content = FieldProperty(str)

    #
    # NOTE:: None in extant data. So should be removed for now
    # data = FieldProperty(str)
    
    #
    # NOTE:: Empty in extant data. So should be removed for now
    # children = FieldProperty([str])


    def getLatestHistory(self):
        """
        Get the latest history entry by date.
        """

        print 'subchild', self.subject
        if len(self.History) < 1:
            return None
        Last = self.History[0]

        for Hist in self.History[1:]:
            if (Hist.created > Last.created):
                Last = Hist

        return Last

    # ---------------------------------------------
    # Anonymization Code.
    # =============================================

    @staticmethod
    def overwriteUserData(DatasetID=None, Timeout=False):
        Subchildren = findAllSubchildren(DatasetID=DatasetID)
        for S in Subchildren:
            S.uid = None
            S.id = None
        ModSocDB.Session.flush()


# -------------------------------------------------
# Query Functions.
# =================================================

def findAllSubchildren(DatasetID=None):
    """
    Find all of the children from the database.
    """
    if(DatasetID == None):
        Set = PiazzaContent_Child_Subchild.query.find()
    else:
        Set = PiazzaContent_Child_Subchild.query.find({'Course_ID':DatasetID})
    return Set.all()

def findChildSubChildByDate(date):
    subchild = PiazzaContent_Child_Subchild.query.find({'created':date}).all()
    return subchild    


