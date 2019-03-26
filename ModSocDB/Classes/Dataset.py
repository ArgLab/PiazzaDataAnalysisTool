# This file is covered by the LICENSE file in the root of this project.
# @license <https://github.com/ArgLab/PiazzaDataAnalysisTool/LICENSE>
#!/usr/bin/env python
"""
Dataset.py
:Author: Collin Lynch
:Date: 01/13/2015

This module defines the dataset class and associated query
methods.  The dataset is used to segment classes or other
study sources as needed. 
"""


# ===========================================
# imports.
# ===========================================

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
class Dataset(MappedClass):
    """
    The Dataset class has a simple pair of fields and acts as
    an index to more complex content.  It should have a set of
    relations to the underlying indexed content such as users
    and content as they are needed.  
    
    Collection: Datasets

    Relations:
    * Users:       A list of users in this dataset.
    * PiazzaUsers: A list of Piazza Users in this dataset.
    * ExamGrades:  A list of all the exam grades from this dataset.

    
    Fields:
    * _id: Unique  Mongodb ID.
    * ShortName:   Mnemonic name.
    * LongName:    Full name.
    * Description: Descriptive text.
    """

    # ---------------------------------------------
    # Mongometa information.
    #
    # You should change only the "name" field to be
    # the name of the associated database collection.
    # =============================================
    class __mongometa__:
        session = ModSocDB.Session
        name = "datasets"

    # ------------------------------------------------
    # Link information.
    #
    # The dataset is a hub class.  It should have a link here
    # to every single other class who will connect to it with
    # a back-link and an ID to make it link back.
    #
    # TODO:: Add back-links to Piazza Data.
    # ================================================

    # Base Classes.
    # -------------------------------------------------
    Users = RelationProperty('User')

    
    # Piazza Classes
    # ------------------------------------------------
    PiazzaUsers = RelationProperty('PiazzaUser')

    
    # Grade Classes, removed since was not being filled anymore
    # ---------------------------------------------
    # ExamGrades = RelationProperty("ExamGrade")


    
    # ------------------------------------------------
    # Link information.
    #
    # Every object will have an _id field so that need
    # not be changed.  Other lines will be a FieldProperty
    # for the association information.  
    # ================================================

    # Mongodb object ID (unique).
    _id     = FieldProperty(schema.ObjectId)

    # ShortName: Mnemonic name.
    ShortName = FieldProperty(str)

    # LongName: Full name.
    LongName = FieldProperty(str)

    # Description: Descriptive text.
    Description = FieldProperty(str)



    # -------------------------------------------------
    # Accessors
    # =================================================

    def getShortName(self):
        """
        Get the short name of the dataset.
        """
        return self.ShortName
    

    # -------------------------------------------------
    # Input Functions.
    # =================================================

    @staticmethod
    def loadDescriptionFile(DescFile):
        """
        Load the supplied description file and return
        a new instance of a Dataset with it.

        Note, this does *not* add it to the database
        with a flush.  That is up to the user.
        """
        In = open(DescFile)

        # Read in the ShortName from the top of the list.
        NewShort = In.readline()[:-1]

        # Read the Long name.
        NewLong = In.readline()[:-1]

        # Read in the remaining text.
        NewDesc = ""
        for Line in In.readlines():
            NewDesc += Line
            
        In.close()

        # Generate the new Dataset instance.
        NewDataset = Dataset(
            ShortName=NewShort,
            LongName=NewLong,
            Description=NewDesc)
        return NewDataset
    
    



# -------------------------------------------------
# Query Functions.
# =================================================

def findDatasetByShortName(Name):
    """
    Simple query method to load all skeletons in the DB.
    """
    Set = Dataset.query.find({'ShortName':Name}).all()[0]
    return Set


def findAllDatasets(Timeout=True):
    """
    Collect all datasets from the database.
    """
    Set =  Dataset.query.find()#(timeout=Timeout)
    return Set.all()



