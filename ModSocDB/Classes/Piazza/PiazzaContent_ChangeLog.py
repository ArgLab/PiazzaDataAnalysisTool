# This file is covered by the LICENSE file in the root of this project.
# @license <https://github.com/ArgLab/PiazzaDataAnalysisTool/blob/master/LICENSE>
#!/usr/bin/env python
"""
PiazzaContent_ChangeLog.py
:Author: Collin Lynch
:Date: 09/30/2014

This module defines the PiazzaContent_ChangeLog which reflects
the changes made to the PiazzaContent information.

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
class PiazzaContent_ChangeLog(MappedClass):
    """
    This class solely deals with the good tag of the piazza content.  It is
    used to handle the cases where a user has tagged a post as good.  It is
    in a 1-1 relationship with a PiazzaUser and a one to many relationship
    with the PiazzaContent class to which it is attached.

    For the most part these should match the user information in the users
    but because of Piazza's odd data structure this may or may not vary hence
    the decision to combine the information here.

    This class is linked to the "piazza_content_changelog" collection.
    
    Relationships:
    * Dataset: Link to the associated Dataset.
    * Content: Link to the associated PiazzaContent instance.
    * Author:  Link to the associated PiazzaUser instance.
    * CentralAuthor: The Central author object for this user.

    Fields:
    * Course_ID: Link to the associated Dataset.
    * Content_ID: MongoID of the parent content.
    * Author_ID: Mongoid of the author of this change.
    * CentralAuthor_ID: Mongoid of the Central author of this change.
    * _id: Mongodb ID.
    * ParentPostID :   (string) which appears to be an index to a target post;
    * ThreadID: (int) thread ID of the post, similar for content, children and subchildren.
    * data: (string) of the change which appears to be another key;
    * uid:  (string) the uid of the individual making the change;
    * anon: (string) whether or not the change is anonymous;
    * type: (string) the type of the change; and
    * when: (datetime) when the change was made.
    """

    # ---------------------------------------------
    # Mongometa information.
    # =============================================
    class __mongometa__:
        session = ModSocDB.Session
        name = "piazza_content_changelog"

    
    # ------------------------------------------------
    # Link information.
    # ================================================

    # Link to the associated Dataset.
    Course_ID = ForeignIdProperty('Dataset')
    Course    = RelationProperty('Dataset')

    # Parent Piazza Content.
    # ------------------------------------------------
    Content_ID = ForeignIdProperty('PiazzaContent')
    Content = RelationProperty('PiazzaContent')

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

    # The ChangeLog is a record of when updates were
    # made to the relevant content. This stores:
    #   'to': which appears to be an index to a target post;
    #   data: of the change which appears to be another key;
    #   uid:  the uid of the individual making the change;
    #   anon: whether or not the change is anonymous;
    #   type: the type of the change; and
    #   when: it took place (appears to be GMT)
    # int for post number.
    ParentPostID   = FieldProperty(str)
    data = FieldProperty(str)
    uid  = FieldProperty(str)
    anon = FieldProperty(str)
    type = FieldProperty(str)
    when = FieldProperty(datetime.datetime)    
    ThreadID = FieldProperty(int)


    # ---------------------------------------------
    # Anonymization Code.
    # =============================================

    @staticmethod
    def overwriteUserData(DatasetID=None, Timeout=False):
        Changelogs = findAllChangeLogs(DatasetID=DatasetID)
        for C in Changelogs:
            C.uid = None
        ModSocDB.Session.flush()


# =================================================
# Utility Functions.
# =================================================

def findAllChangeLogs(DatasetID=None):
    """
    Collect All of the changelogs in the data.
    """
    if (DatasetID == None):
        Set = PiazzaContent_ChangeLog.query.find()
    else:
        Set = PiazzaContent_Changelog.query.find({'Course_ID':DatasetID})
    return Set.all()

def findChangeLogByDate(date):
    content = PiazzaContent_ChangeLog.query.find({'when':date}).all()
    return content
