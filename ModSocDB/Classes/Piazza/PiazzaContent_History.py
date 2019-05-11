# This file is covered by the LICENSE file in the root of this project.
# @license <https://github.com/ArgLab/PiazzaDataAnalysisTool/blob/master/LICENSE>
#!/usr/bin/env python
"""
PiazzaContent_History.py
:Author: Collin Lynch
:Date: 09/30/2014

This module defines the PiazzaContent_History class which wraps up
historical records for the piazza posts.

TODO: Confirm relationship with ChangeLog.
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
class PiazzaContent_History(MappedClass):
    """
    This class deals with history updates to the piazza content
    itself.  This will include a link to the parent post being
    edited as well as to the updated author information.  It is
    In turn linked to by the history information.
      
    Collection: piazza_content_history

    Relations:
    * Dataset: Link to the associated Dataset.
    * Content: Parent Piazza Content.
    * Author: Link to the user that authored this change.
    * CentralAuthor: The Central author object for this user.
    
    Fields:
    * Course_ID: ID of the associated Dataset.
    * Content_ID: ID of parent content.
    * Author_ID: ID of original author.
    * _id: Mongodb object ID (unique).
    * ThreadID: (int) Unknown int believed to be post number.
    * content: (string) (i.e. text) of the post itself.
    * subject: (string) line of the post.
    * uid: (string) of the author (will be None if anon is 'Full')
    * anon: (string) whether or not the change is anonymous (full | no)
    * created: (datetime) date the history element was created.
                (appears to be GMT)
    """

    # ---------------------------------------------
    # Mongometa information.
    # =============================================
    class __mongometa__:
        session = ModSocDB.Session
        name = "piazza_content_history"

    # ------------------------------------------------
    # Link information.
    # ================================================

    # Link to the associated Dataset.
    Course_ID = ForeignIdProperty('Dataset')
    Course    = RelationProperty('Dataset')

    # Parent Piazza Content.
    Content_ID = ForeignIdProperty('PiazzaContent')
    Content = RelationProperty('PiazzaContent')

    # Link to the user that authored this change.
    Author_ID = ForeignIdProperty('PiazzaUser.PiazzaUser')
    Author = RelationProperty('PiazzaUser.PiazzaUser')

    # Direct link to the central author instance.
    CentralAuthor_ID = ForeignIdProperty('User')
    CentralAuthor = RelationProperty('User')

    # ------------------------------------------------
    # Link information.
    # ================================================

    # Mongodb object ID (unique).
    _id     = FieldProperty(schema.ObjectId)

    # History of the content for the post.
    #   content: (i.e. text) of the post itself.
    #   subject: line of the post.
    #   uid:     of the author (will be None if anon is 'Full')
    #   anon:    whether or not the change is anonymous (full | no)
    #   created: date the history element was created.  (appears to be GMT)
    # int for post number.
    content = FieldProperty(str)
    subject = FieldProperty(str)
    uid = FieldProperty(str)
    anon = FieldProperty(str)
    created = FieldProperty(datetime.datetime)    
    ThreadID = FieldProperty(int)


    # ---------------------------------------------
    # Anonymization Code.
    # =============================================

    @staticmethod
    def overwriteUserData(DatasetID=None, Timeout=False):
        Histories = findAllContentHistory(DatasetID=DatasetID)
        for H in Histories:
            H.uid = None
        ModSocDB.Session.flush()

# -------------------------------------------------
# Query Functions.
# =================================================

def findAllContentHistory(DatasetID=None):
    """
    Find all of the PiazzaContent_History instances in
    the database.
    """
    if(DatasetID == None):
        Set = PiazzaContent_History.query.find()
    else:
        Set = PiazzaContent_History.query.find({'Course_ID':DatasetID})
    return Set.all()

def findHistoryByDate(date):
    history = PiazzaContent_History.query.find({'created':date}).all()
    return history
