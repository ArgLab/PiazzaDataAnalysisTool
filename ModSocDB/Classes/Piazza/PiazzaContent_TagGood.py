# This file is covered by the LICENSE file in the root of this project.
# @license <https://github.com/ArgLab/PiazzaDataAnalysisTool/blob/master/LICENSE>
#!/usr/bin/env python
"""
PiazzaContent.py
:Author: Collin Lynch
:Date: 09/30/2014

This module defines the PiazzaContent class which wraps up
the Piazza content elements in a complex accessor class.
It also defines several subsidiary objects which will be used
to access the content.
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
#from .. import ModSocDB
import ModSocDB
import PiazzaUser
from PiazzaContent import PiazzaContent
from .. import User as UserMod


# ================================================
class PiazzaContent_TagGood(MappedClass):
    """
    This class solely deals with the good tag of the piazza content.  It is
    used to handle the cases where a user has tagged a post as good.  It is
    in a 1-1 relationship with a PiazzaUser and a one to many relationship
    with the PiazzaContent class to which it is attached.

    For the most part these should match the user information in the users
    but because of Piazza's odd data structure this may or may not vary hence
    the decision to combine the information here.
      
    Collection: piazza_content_tag_good

    Relations:
    ----------------------------------------------------------
    * Dataset: Link to the associated Dataset.
    * Content_ID: Parent Piazza Content.
    * Author_ID: Link to the associated user.
    * CentralAuthor: The Central author object for this user.
    
    Fields:
    ----------------------------------------------------------
    * Dataset_ID: ID of the associated Dataset.
    * Content_ID: Parent Piazza Content.
    * Author_ID: Link to the associated user.
    * CentralAuthor_ID: Link to the associated central user.
    * _id: mongo db id (unique).
    * name: (string) user's real name.
    * admin: (bool) Status of admin on class.
    * photo: (string) if present, always None in present dataset.
    * us: (bool) Purpose unknown bool, always false in present dataset.
    * email: (string) real user email string.
    * role: (string) with role in course.
    * facebook_id: (string) external id, also always none in course.
    * id: (string) user ID from Piazza Users class.
    """

    # ---------------------------------------------
    # Mongometa information.
    # =============================================
    class __mongometa__:
        session = ModSocDB.Session
        name = "piazza_content_tag_good"

    
    # ------------------------------------------------
    # Link information.
    # ================================================

    # Link to the associated Dataset.
    Dataset_ID = ForeignIdProperty('Dataset')
    Dataset    = RelationProperty('Dataset')

    # Parent Piazza Content.
    Content_ID = ForeignIdProperty('PiazzaContent')
    Content = RelationProperty('PiazzaContent')

    # Link to the associated user.
    Author_ID = ForeignIdProperty('PiazzaUser.PiazzaUser')
    Author = RelationProperty('PiazzaUser.PiazzaUser')

    # Direct link to the central author instance.
    CentralAuthor_ID = ForeignIdProperty('User')
    CentralAuthor = RelationProperty('User')

    # ------------------------------------------------
    # Field Information
    # ================================================
    
    #   name:   user's real name.
    #   admin:  Status of admin on class (bool)
    #   photo:  if present, always None in present dataset.
    #   us:     Purpose unknown bool, always false in present dataset.
    #   email:  real user email string.
    #   role:   string with role in course.
    #   facebook_id: external id, also always none in course.
    #   id:     user ID from Piazza Users class.

    _id         = FieldProperty(schema.ObjectId)
    name        = FieldProperty(str)
    admin       = FieldProperty(bool)
    photo       = FieldProperty(str)
    us          = FieldProperty(bool)
    email       = FieldProperty(str)
    role        = FieldProperty(str)
    facebook_id = FieldProperty(str)
    id          = FieldProperty(str)
    # oid          = FieldProperty(str)


    # -------------------------------------------------
    # Accessors / Settors.
    # =================================================


    # ---------------------------------------------
    # Anonymization Code.
    # =============================================

    @staticmethod
    def overwriteUserData(DatasetID=None, Timeout=False):
        TagGoods = findAllTagGood(DatasetID=DatasetID)
        for T in TagGoods:
            T.id = None
            T.name = None
            T.email = None
            T.facebook_id = None
        ModSocDB.Session.flush()

# -------------------------------------------------
# Query Functions.
# =================================================

def findAllTagGood(DatasetID=None):
    """
    Find all of the PiazzaContent_TagGood instances in
    the database.
    """
    if(DatasetID == None):
        Set = PiazzaContent_TagGood.query.find()
    else:
        Set = PiazzaContent_TagGood.query.find({'Dataset_ID':DatasetID})
    return Set.all()

    
# -------------------------------------------------
# Compile the classes.
# =================================================

# Mapper.compile_all()



