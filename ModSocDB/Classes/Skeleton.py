# This file is covered by the LICENSE file in the root of this project.
# @license <https://github.com/ArgLab/PiazzaDataAnalysisTool/blob/master/LICENSE>
#!/usr/bin/env python
"""
Skeleton.py
:Author: Collin Lynch
:Date: 01/13/2015

This module provides basic skeleton information and a class instance for the
ModSocDB class.  It should be copied to start any new classes.

** DO NOT LOAD THIS CLASS IT WILL NOT COMPILE. **

"""


# ===========================================
# imports.
# ===========================================
import datetime
# Ming imports required for class definition.
# -------------------------------------------
from ming import schema
from ming.odm.declarative import MappedClass
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty

# Load of core library and error class.
# -----------------------------------------------------
import ModSocDB
from ModSocDB import ModSocDBError




# ================================================
class SkeletonClass(MappedClass):
    """
    Sample class with docstring for content. 
    
    Collection: <put collection assoc here>

    Relations:
    
    Fields:
    * _id: Unique Mongodb ID.
    """

    # ---------------------------------------------
    # Mongometa information.
    #
    # You should change only the "name" field to be
    # the name of the associated database collection.
    # =============================================
    class __mongometa__:
        session = ModSocDB.Session
        name = "<Change>"

    # ------------------------------------------------
    # Link information.
    #
    # Put any links here following the model of the
    # dataset link below.
    #
    # NOTE:: The dataset link must be preserved and
    #   updated on imports so that everything points
    #   to the correct dataset.  
    # ================================================

    # Link to the associated Dataset.
    Dataset_ID = ForeignIdProperty('Dataset')
    Dataset    = RelationProperty('Dataset')


    # ------------------------------------------------
    # Link information.
    #
    # Every object will have an _id field so that need
    # not be changed.  Other lines will be a FieldProperty
    # for the association information.  
    # ================================================

    # Mongodb object ID (unique).
    _id     = FieldProperty(schema.ObjectId)

    # content: (i.e. text) of the post itself.
    content = FieldProperty(str)
    created = FieldProperty(datetime.datetime)


    # -------------------------------------------------
    # Anonymization of user data (if present)
    #
    # The code below should be uncommented and adapted
    # to the current needs if the object in question
    # is directly connected to a user instance and
    # contains any user identifiable fields that must
    # be anonymized.  Those will propagate from the
    # user instance itself.  
    # =================================================

    # @staticmethod
    # def overwriteUserData(DatasetID=None):
    #     """
    #     Sync the name information with the linked user.
    #     This is used for anonymization primarily.
    #     """
    #     Grades = findAllExamSkeletons(DatasetID=DatasetID)
    #     for Grade in Grades:
    #         LastName  = Grade.Student.getLastName()
    #         FirstName = Grade.Student.getFirstName()
    #         Username  = Grade.Student.getLocalUserID()


# -------------------------------------------------
# Query Functions.
# =================================================

def findAllSkeletons(DatasetID=None):
    """
    Simple query method to load all skeletons in the DB.
    """
    if (DatasetID == None): Set = Skeleton.query.find()
    else: Set = Skeleton.query.find(Dataset_ID=DatasetID)
    return Set.all()

