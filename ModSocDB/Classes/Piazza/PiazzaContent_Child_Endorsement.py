#!/usr/bin/env python
"""
PiazzaContent_Child_Endorsement.py
:Author: Collin Lynch
:Date: 10/29/2014

Endorsement tag module for PiazzaContent_Child
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
import ModSocDB
import PiazzaUser
from .. import User as UserMod


# ================================================
class PiazzaContent_Child_Endorsement(MappedClass):
    """
    This class deals with the TagEndorse Dict element of the
    child elements.  This is a list of all of the users that
    chose to endorse this child post as being good.

    Collection: piazza_content_children_tagendorse

    Relations:
    * Dataset: Link to the associated Dataset.
    * Parent: PiazzaContent_Child instance.
    * Author: PiazzaUser instance who authored this.
    * CentralAuthor: The Central author object for this user.

    Fields:
    * Dataset_ID: ID of the associated Dataset.
    * Parent_ID: Mongodb ID of the Piazza Content Child that
                 this is an endorsement of
    * Author_ID: Mongodb id of the piazza user that endorsed
                 this content.
    * CentralAuthor_ID: Mongoid of the Central author of this change.
    * _id: unique mongodb Id.
    * name: (string) piazza user name if included.
    * admin: (bool) flag indicating whether the user was in admin status
             when this endorsement was made.
    * photo: (string) binary string representing the user photo if uploaded.
    * email: (string) the endorsers e-mail if given.
    * role: (string) the endorsers role at the time of endorsement.
    * facebook_id: (string) the facebook id of the endorsing party.
    * class_sections: (string) class section of the endorser.
    * admin_permission: (int) numerical indication of whether the admin
                         permission was used.
    """

    # ---------------------------------------------
    # Mongometa information.
    # =============================================
    class __mongometa__:
        session = ModSocDB.Session
        name = "piazza_content_children_tagendorse"

    
    # ------------------------------------------------
    # Link information.
    # ================================================

    # Link to the associated Dataset.
    Dataset_ID = ForeignIdProperty('Dataset')
    Dataset    = RelationProperty('Dataset')

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

    # User name. 
    name = FieldProperty(str) 

    # Admin status for the user at the time this was done?
    admin = FieldProperty(bool)

    # String content for a photo.
    photo = FieldProperty(str)

    # False for all the data, so removed
    # us = FieldProperty(bool)

    # User e-mail. 
    email = FieldProperty(str)

    # Role of the user at the time done.  
    role = FieldProperty(str)
    
    # Facebook id of the user. 
    facebook_id = FieldProperty(str)
    
    # Id of the author, redundant so removed
    # id = FieldProperty(str)

    # Class section of the endorsement.
    class_sections = FieldProperty([str])

    # Admin permissions used?
    admin_permission = FieldProperty(int)

    # ---------------------------------------------
    # Anonymization Code.
    # =============================================

    @staticmethod
    def overwriteUserData(DatasetID=None, Timeout=False):
        Endorsements = findAllChildEndorsements(DatasetID=DatasetID)
        for E in Endorsements:
            E.name = None
            E.email = None
            E.id = None
        ModSocDB.Session.flush()

# -------------------------------------------------
# Query Functions.
# =================================================

def findAllChildEndorsements(DatasetID=None):
    """
    Find all of the child endorsements from the database.
    """
    if (DatasetID == None):
        Set = PiazzaContent_Child_Endorsement.query.find()
    else:
        Set = PiazzaContent_Child_Endorsement.query.find({'Dataset_ID':DatasetID})
    return Set.all()


