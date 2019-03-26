# This file is covered by the LICENSE file in the root of this project.
# @license <https://github.com/ArgLab/PiazzaDataAnalysisTool/LICENSE>
#!/usr/bin/env python
"""
PiazzaContent_Child_History.py
:Author: Collin Lynch
:Date: 09/30/2014

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
class PiazzaContent_Child_History(MappedClass):
    """
    History elements for the child posts.  This tracks updates to
    them and can be used as needed.

    Collection: piazza_content_children_history

    Relations:
    * Dataset: Link to the associated Dataset.
    * Parent: Link to parent PiazzaContent_Child instance.
    * Author: Link to PiazzaUser author instance. 
    * CentralAuthor: The Central author object for this user.

    Fields:
    * Course_ID: ID of the associated Dataset.
    * Parent_ID: unique mongodb id of the child post.
    * Author_ID: unique mongodb id of the author.   
    * CentralAuthor_ID: Mongoid of the Central author of this change.
    * _id: Mongodb object ID (unique).
    * ThreadID: (int) Unknown int believed to be post number.
    * content: (string) Content of the history change. 
    * anon: (string) Whether this was an anonymous change.
    * subject: (string) Subject of the content.
    * uid: (string) Piazza id of the author (may be hidden if anon).
    * created: (datetime) Datetime this was created. 
    """

    # ---------------------------------------------
    # Mongometa information.
    # =============================================
    class __mongometa__:
        session = ModSocDB.Session
        name = "piazza_content_children_history"

    
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
    
    # int for post number.
    ThreadID = FieldProperty(int)

    # Content of the history change. 
    content = FieldProperty(str)

    # Whether this was an anonymous change.
    anon = FieldProperty(str)

    # Subject of the content.
    subject = FieldProperty(str)

    # UID of the author (may be hidden if anon).
    uid = FieldProperty(str)

    # Datetime this was created. 
    created = FieldProperty(datetime.datetime)

    # ---------------------------------------------
    # Anonymization Code.
    # =============================================

    @staticmethod
    def overwriteUserData(DatasetID=None, Timeout=False):
        Histories = findAllChildHistories(DatasetID=DatasetID)
        for H in Histories:
            H.uid = None
        ModSocDB.Session.flush()

# -------------------------------------------------
# Query Functions.
# =================================================

def findAllChildHistories(DatasetID=None):
    """
    Find all of the child histories from the database.
    """
    if(DatasetID == None):
        Set = PiazzaContent_Child_History.query.find()
    else:
        Set = PiazzaContent_Child_History.query.find({'Course_ID':DatasetID})
    return Set.all()
    
def findChildHistoryByDate(date):
    history = PiazzaContent_Child_History.query.find({'created':date}).all()
    return history   

