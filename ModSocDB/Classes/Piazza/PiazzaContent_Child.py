#!/usr/bin/env python
"""
PiazzaContent_Child.py
:Author: Collin Lynch
:Date: 10/29/2014

Piazzacontent child class.
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
class PiazzaContent_Child(MappedClass):
    """
    This class covers child elements from the PiazzaContent information
    and will link to subsidiary classes for the endorsement tag, history
    and sub-children.
    
    Collection: piazza_content_children

    Relations:
    * Dataset: Link to the associated Dataset.
    * Parent: Link to parent content.
    * Author: Link to authoring user if other authors change it
              they show up in the change log.  
    * CentralAuthor: The Central author object for this user.
    * Endorsements: Link to the endorsed tag elements.  
    * History: Link to the history elements.
    * Subchildren: Link to subsidiary subchildren.

    Fields: 
    * Course_ID: ID of the associated Dataset.
    * Parent_ID: ID of the parent piazza content.
    * Author_ID: ID of the original Author.
    * CentralAuthor_ID: Mongoid of the Central author of this change.
    * _id: Mongodb object ID (unique).
    * folders: (string) List of folders it is in.
    * updated:  (string) string form of when it was updated.
    * tag_endorse_arr: (string) list of user id's who endorsed this.
    * no_upvotes: (string) an int listing (I suspect) the number of upvotes
                  received.
    * uid: (string) Piazza User ID for the author.
    * ThreadID: (int) Unknown int believed to be post number.
    * created: (datetime) form of creation date.
    * config:  (dictionary) dict of unknown information, always empty in current dataset.
    * no_answer: (int) of answer count (I suspect).
    * anon: (string) string indicating anonymity status in data (full | no)
    * bucket_name: (string) name of bucket for this item (e.g. 'Yesterday')
    * bucket_order: (int) int order in the bucket.
    * id:  string form of the child post id.
    * type: (string) string of child type.
    * subject: (string) form of post subject (often long).
    
    """

    # ---------------------------------------------
    # Mongometa information.
    # =============================================
    class __mongometa__:
        session = ModSocDB.Session
        name = "piazza_content_children"

    
    # ------------------------------------------------
    # Link information.
    # ================================================

    # Link to the associated Dataset.
    Course_ID = ForeignIdProperty('Dataset')
    Course    = RelationProperty('Dataset')

    # Parent Piazza Content.
    Parent_ID = ForeignIdProperty('PiazzaContent')
    Parent = RelationProperty('PiazzaContent')

    # Link to the associated user.
    Author_ID = ForeignIdProperty('PiazzaUser.PiazzaUser')
    Author = RelationProperty('PiazzaUser.PiazzaUser')

    # Direct link to the central author instance.
    CentralAuthor_ID = ForeignIdProperty('User')
    CentralAuthor = RelationProperty('User')

    # Link to the endorsed tag elements.
    Endorsements = RelationProperty('PiazzaContent_Child_Endorsement')
    
    # Link to the history elements.
    History = RelationProperty('PiazzaContent_Child_History')

    # Link to subsidiary subchildren.
    Subchildren = RelationProperty('PiazzaContent_Child_Subchild')

    # ------------------------------------------------
    # Fields
    # ================================================

    # Mongodb object ID (unique).
    _id     = FieldProperty(schema.ObjectId)

    #  folders:  List of folders it is in.
    folders = FieldProperty([str])
    
    #  updated:  string form of when it was updated.
    updated = FieldProperty(datetime.datetime)

    #  tag_endorse_arr: list of user id's who endorsed this.
    tag_endorse_arr = FieldProperty([str])

    #  no_upvotes: an int listing (I suspect) the number of upvotes
    #    received.
    no_upvotes = FieldProperty(int)
    
    # int for post number.
    ThreadID = FieldProperty(int)

    # User ID for the author.
    uid = FieldProperty(str)
        
    #  created: string form of creation date.
    # created = FieldProperty(str)
    created = FieldProperty(datetime.datetime)

    #  config:  dict of unknown information, always empty in current dataset.
    config = FieldProperty(dict())

    #  no_answer: int of answer count (I suspect).
    no_answer = FieldProperty(int)

    #  anon: string indicating anonymity status in data (full | no)
    anon = FieldProperty(str)

    #  bucket_name:  name of bucket for this item (e.g. 'Yesterday')
    bucket_name = FieldProperty(str)

    #  bucket_order: int order in the bucket.
    bucket_order = FieldProperty(int)
    
    #  id:  string of the child id.
    id = FieldProperty(str)

    #  type: string of child type.
    type = FieldProperty(str)

    #  subject: string form of post subject (often long).
    content = FieldProperty(str)

    
    # ------------------------------------------------------
    # Anonymization Methods.
    # ======================================================

    def resetTagEndorseArr(self, UIDMap):
        """
        Reset the endorsement array for this item using the
        attached UIDMap which maps old to new IDs. 
        """
        NewArr = []
        for ID in self.tag_endorse_arr:
            if ID in UIDMap:
                NewArr.append(UIDMap[ID])
            else:
                print "User %s not found for reseting tag endorse in piazza_content_child" % ID
        self.tag_endorse_arr = NewArr
        # self.tag_endorse_arr = [E.id for E in self.Endorsements]

    def getLatestHistory(self):
        """
        Get the earliest history entry by date.
        """

        if len(self.History) < 1:
            # print 'hereeee', self.subject
            return None
        Last = self.History[0]

        # print 'some history found', len(self.History)
        for Hist in self.History[1:]:
            if (Hist.created > Last.created):
                Last = Hist

        return Last


    @staticmethod
    def resetIds(DatasetID=None, Timeout=False):
        Children = findAllChildren(DatasetID=DatasetID)
        for C in Children:
            C.id = None
            C.uid = None
        ModSocDB.Session.flush()

    def overwriteUserData(self):
        for E in self.Endorsements:
            E.name = None
            E.email = None
            E.id= None
        for S in self.Subchildren:
            S.uid = None
            S.id = None
        for H in self.History:
            H.uid = None


    # ------------------------------------------------------
    # Simple Accessors
    # ======================================================

    def getAuthor(self):
        """
        Pull the author of this item.
        """
        return self.Author
    
    # ------------------------------------------------------
    # Complex Accessors
    # ======================================================

    def getOlderSubchildren(self, Date):
        """
        Get children that predate the specified cutoff
    
        NOTE:: This treats a None date as a zero date.
        """
        
        return [ C for C in self.Subchildren
                 if ((C.created == None) or (C.created <= Date)) ]


# -------------------------------------------------
# Query Functions.
# =================================================

def findAllChildren(DatasetID=None):
    """
    Find all of the children from the database.
    """
    if(DatasetID == None):
        Set = PiazzaContent_Child.query.find()
    else:
        Set = PiazzaContent_Child.query.find({'Course_ID': DatasetID})
    return Set.all()

def findChildByDate(date):
    child = PiazzaContent_Child.query.find({'created':date}).all()
    return child
