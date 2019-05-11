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
from .. import User as UserMod

# ================================================
class PiazzaContent(MappedClass):
    """
    The PiazzaContent class is used to represent the PiazzaContent
    with the complex sub-classes such as children linked separately
    allowing us to iterate over all of the elements and the sub-
    posts.

    Collection: piazza_content

    Relations:
    --------------------------------------------------------
    * Dataset: Link to the associated Dataset.
    * Author: PiazzaUser who wrote the Content.
    * CentralAuthor: The Central author object for this user.
    * GoodTags: Relationship with good tags by this user. The GoodTag objects are used intermediately. They get removed while data cleanup
    * History: Relationship with edited history elements.
    * ChangeLog: Change Log listing.
    * Children: Child Posts.

    Fields:
    --------------------------------------------------------
    * Course_ID: ID of the associated Dataset.
    * Author_ID: Mongo ID of the associated PiazzaUser.
    * CentralAuthor_ID: Mongoid of the Central author of this change.
    * _id: Mongodb object ID (unique).
    * tags: (list of strings) Array of Tags on the posts.
    * status: (string) Status of the post.
    * folders: (list of strings) List of folders this is a part of.
    * id: piazza id of post.
    * type: (string) Post system type.
    * unique_views: (int) View count.
    * created: (datetime) Date created.
    * ThreadID: (int) An ID, same for each post and all the follow-ups
    * no_answer_followup: (int) Followups with no answer?
    * tag_good_arr(str): Array of "good" tags, ids of GoodTags related to this post. 
    *   This is kept because GoodTags are intermediate. They get filled while initialization
    *   and get removed while cleanup. This should be used to access good tags
     
    """

    # ---------------------------------------------
    # Mongometa information.
    # =============================================
    class __mongometa__:
        session = ModSocDB.Session
        name = "piazza_content"


    # ---------------------------------------------
    # Link Information
    # =============================================

    # Link to the associated Dataset.
    Course_ID = ForeignIdProperty('Dataset')
    Course    = RelationProperty('Dataset')

    # Link to the associated PiazzaUser (author of the content)
    Author_ID = ForeignIdProperty('PiazzaUser')
    Author = RelationProperty('PiazzaUser')

    # Direct link to the central author instance.
    CentralAuthor_ID = ForeignIdProperty('User')
    CentralAuthor = RelationProperty('User')

    # Relationship with good tags by this user.
    # The GoodTag objects are used intermediately. They get removed while data cleanup
    GoodTags = RelationProperty("PiazzaContent_TagGood")

    # Relationship with edited history elements.
    History = RelationProperty("PiazzaContent_History")

    # Change Log listing.
    ChangeLog = RelationProperty("PiazzaContent_ChangeLog")

    # Children.
    Children = RelationProperty("PiazzaContent_Child")

    
    # ------------------------------------------------------------
    # Fields
    # =================================================

    # Mongodb object ID (unique).
    _id     = FieldProperty(schema.ObjectId)


    # Status of the post. active or private
    status = FieldProperty(str)

    # Array of "good" tags, ids of GoodTags related to this post. 
    # This is kept because GoodTags are intermediate. They get filled while initialization
    # and get removed while cleanup. This should be used to access good tags
    tag_good_arr = FieldProperty([str])

    # List of folders this is a part of.
    folders = FieldProperty([str])

    # Post key ID.
    id = FieldProperty(str)

    # Post system type. note, question, or poll
    type = FieldProperty(str)

    # View count.
    unique_views = FieldProperty(int)

    # Date created.
    created = FieldProperty(datetime.datetime)
    # created = FieldProperty(str)

    # int for post number.
    ThreadID = FieldProperty(int)

    # Followups with no answer?
    no_answer_followup = FieldProperty(int)


    # ------------------------------------------------------------
    # Anonymization Methods.
    # =================================================

    def resetTagGoodArr(self, UIDMap):
        """
        The Tag_Good_array contains a list of users who have
        tagged this array as good via the links.  This code
        will iterate over the contents of the TagGood array
        updating with the new user IDs.
        """
        NewArr = []
        for ID in self.tag_good_arr:
            if ID in UIDMap:
                NewArr.append(UIDMap[ID])
            else:
                print "User with id %s not fount in UIDMap to be updated in tag_good_arr" % ID
        self.tag_good_arr = NewArr
        # self.tag_good_arr = [T.id for T in self.GoodTags]




    # ----------------------------------------------------
    # Relational Accessors.
    # ====================================================

    def getFirstSubject(self):
        """
        Get the first subject line for the content from the first history.
        """
        FirstHist = self.getEarliestHistory()
        return FirstHist.subject
    
    
    def getEarliestHistory(self):
        """
        Get the earliest history entry by date.
        """
        First = self.History[0]

        for Hist in self.History[1:]:
            if (Hist.created < First.created):
                First = Hist

        return First

    
    def getFirstAuthor(self):
        """
        Get the first author of this content based upon the
        history entries.
        """
        Hist = self.getEarliestHistory()
        return Hist.Author

    def getLatestHistory(self):
        if len(self.History) < 1:
            # print 'hereeee', self.subject
            return None
        Last = self.History[0]

        # print 'some history found', len(self.History)
        for Hist in self.History[1:]:
            if ((Hist.created > Last.created) and Hist.subject and Hist.content):
                Last = Hist

        return Last

    def getAuthors(self):
        """
        This code iterates over the history extracting all authors
        from the content updates.
        """
        Authors = []
        for Hist in self.History:
            if (not Hist.Author in Authors):
                Authors.append(Hist.Author)
        return Authors


    def getOlderChildren(self, Date):
        """
        Get children that predate the specified cutoff
        """
        return [ C for C in self.Children
                 if (C.created <= Date) ]
    
    
    # ---------------------------------------------
    # Anonymization Code.
    # =============================================

    @staticmethod
    def overwriteUserData(DatasetID=None, Timeout=False):
        Contents = findAllContent(DatasetID=DatasetID)
        for C in Contents:
            C.id = None
        ModSocDB.Session.flush()


# -------------------------------------------------
# Query Functions.
# =================================================

def findAllContent(DatasetID=None):
    """
    Find all of the content from the database.
    """
    if(DatasetID == None):
        Set = PiazzaContent.query.find()
    else:
        Set = PiazzaContent.query.find({'Course_ID':DatasetID})
    return Set.all()

def findContentByPostID(postID):
    """
    Find all of the content from the database.
    """
    Post = PiazzaContent.query.find({'id':postID}).all()[0]
    return Post
    
def findContentByDate(date):
    content = PiazzaContent.query.find({'created':date}).all()
    return content

