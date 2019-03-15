# This file is covered by the LICENSE file in the root of this project.
# @license <https://github.com/ArgLab/PiazzaDataAnalysisTool/LICENSE>
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
from ming.odm.declarative import MappedClass


# Load the shared session objects and library classes.
# -----------------------------------------------------
import ModSocDB

import PiazzaUser
from PiazzaContent import PiazzaContent
from PiazzaContent_TagGood import PiazzaContent_TagGood
from PiazzaContent_History import PiazzaContent_History
from PiazzaContent_ChangeLog import PiazzaContent_ChangeLog
from PiazzaContent_Child import PiazzaContent_Child
from PiazzaContent_Child_Endorsement import PiazzaContent_Child_Endorsement
from PiazzaContent_Child_Subchild import PiazzaContent_Child_Subchild
from PiazzaContent_Child_History import PiazzaContent_Child_History



# ================================================
class RawPiazzaContent(MappedClass):
    """
    The RawPiazzaContent class wraps up the raw_piazza_content 
    collection this contains complex data that includes both the 
    metadata for the original post as well as a record of all 
    sub-posts.  These will be used to set the separate objects
    for the piazza_content and the other complex classes also
    defined here.

    The internals of this class make heavy use of the captive
    session via the ModSocDB.Session direct link.  It should
    remain that way so that the session and connection can be
    adaptive.  
  
    Collection: raw_piazza_content
    """

    # ---------------------------------------------
    # Mongometa information.
    # =============================================
    class __mongometa__:
        session = ModSocDB.Session
        #name = "raw_piazza_content"
        name = "raw_piazza_content"

    # ------------------------------------------------------------
    # Parameters.
    # =================================================

    # Mongodb object ID (unique).
    _id     = FieldProperty(schema.ObjectId)

    # Array of Tags on the posts.
    tags = FieldProperty([str])

    # Status of the post.
    status = FieldProperty(str)

    # Additional array of "good" tags?  Use unknown.
    tag_good_arr = FieldProperty([str])

    # List of folders this is a part of.
    folders = FieldProperty([str])

    # Post key ID.
    id = FieldProperty(str)

    # Post system type.
    type = FieldProperty(str)

    # View count.
    unique_views = FieldProperty(int)

    # Date created.
    # created = FieldProperty(datetime.datetime)
    created = FieldProperty(str)

    # Unknown int believed to be post number.
    nr = FieldProperty(int)

    # Followups with no answer?
    no_answer_followup = FieldProperty(int)

    # Configuration elements.
    #  meaning of is_default unclear. 
    config = FieldProperty( dict(
        is_default = int,
        bypass_email = int,
        is_announcement = int,
        feed_groups = str
        ),
        required=False,
        if_missing=None)

    # Array of users who tagged this 'good'
    #  NOTE:: These should be users in the PiazzaUsers list but
    #   they are presented as a dict of user information that
    #   actually includes information not present in the PiazzaUsers
    #   table and possibly unique to the class.  As such it may need
    #   to be handled separately.
    #
    #   name:  user's real name.
    #   admin:  Status of admin on class (bool)
    #   photo:  if present, always None in present dataset.
    #   us: Purpose unknown bool, always false in present dataset.
    #   email:  real user email string.
    #   role:  string with role in course.
    #   facebook_id: external id, also always none in course.
    #   id:  user ID from Piazza Users class. 
    tag_good = FieldProperty([ dict(
        name = str,
        admin = bool,
        photo = str,
        us = bool,
        email = str,
        role = str,
        facebook_id = str,
        id = str
        )],
        required=False,
        if_missing=None)


    # Child posts,
    #  folders:  List of folders it is in.
    #  updated:  string form of when it was updated.
    #  d_bucket:  string of when to bin it (e.g. 'Yesterday')
    #  tag_endorse_arr: list of user id's who endorsed this.
    #  tag_endorse: list of users who endorsed this, apparently
    #    same as tag_good list above with the addition of
    #    class_sections a list of string section names,
    #    and admin_permissions an int indicating permission levels.
    #  no_upvotes: an int listing (I suspect) the number of upvotes
    #    received.
    #  created: string form of creation date.
    #  config:  dict of unknown information, always empty in current dataset.
    #  no_answer: int of answer count (I suspect).
    #  anon: string indicating anonymity status in data (full | no)
    #  bucket_name:  name of bucket for this item (e.g. 'Yesterday')
    #  id:  string of the child id.
    #  bucket_order: int order in the bucket.
    #  type: string of child type.
    #  subject: string form of post subject (often long).
    children = FieldProperty([ dict(
        folders = [str],
        updated = str,
        d_bucket = str,
        tag_endorse_arr = [str],
        tag_endorse = [ dict(
            name = str,
            admin = bool,
            photo = str,
            us = bool,
            email = str,
            role = str,
            facebook_id = str,
            id = str,
            class_sections = [str],
            admin_permission = int
            )],
        no_upvotes = int,
        uid = str,
        created = str,
        config = dict(),
        no_answer = int,
        anon = str,
        bucket_name = str,
        id = str,
        bucket_order = int,
        type = str,
        subject = str,

        # Recursive sub-structure of children for this post.  
        children = [ dict(
            folders = [str],
            updated = str,
            d_bucket = str,
            uid = str,
            created = str,
            config = dict(),
            anon = str,
            bucket_name = str,
            id = str,
            bucket_order = int,
            type = str,
            subject = str,
            #
            # NOTE:: None in extant data.
            data = str,
            #
            # NOTE:: Empty in extant data.
            children = [str]
            )],

        # History structure for this child.  
        history = [ dict(
            content = str,
            anon = str,
            subject = str,
            uid = str,
            # created = datetime.datetime
            created = str
            )],

        # In some cases this is empty in the current dataset triggering
        # an error hence it is hidden.  The right format is the commented
        # format.  
        data = None,
        )],
        required=False,
        if_missing=None)
    

    # The ChangeLog is a record of when updates were
    # made to the relevant content. This stores:
    #   'to' which appears to be an index to a parent post;
    #   data of the change which appears to be another key;
    #   the uid of the individual making the change;
    #   whether or not the change is anonymous;
    #   the type of the change; and
    #   when it took place
    change_log = FieldProperty([dict( 
        ParentPostID   = str,
        data = str,
        uid  = str,
        anon = str,
        type = str,
        when = str
        )],
        required=False,
        if_missing=None)

    # History of the content for the post.
    #   Content of the post itself.
    #   subject line of the post.
    #   uid of the author.
    #   whether or not the change is anonymous.
    #   date the history element was created.  
    history = FieldProperty( [ dict(
        content = str,
        subject = str,
        uid = str,
        anon = str,
        # created = datetime.datetime
        created = str
        )],
        required=False,
        if_missing=None)

    # ======================================================================
    # Accessors.
    # ======================================================================

    def getFirstSubject(self):
        """
        Get the first subject line.
        """
        if (len(self.history) == 0): return None
        else: return self.history[0]["subject"]
    
    

    # ======================================================================
    # Duplicate Methods.
    #
    # Remove Duplace elements from the database.  
    # ======================================================================

    @staticmethod
    def removeDuplicateContent(DatasetID):
        """
        Remove duplicate content from the dataset.
        """
        ContentIDs = set(collectAllRawContentIDs())
        for ID in ContentIDs:
            Contents = collectRawContentByID(ID)
            if (len(Contents) > 1):
                # print "%s %d" % (ID, len(Contents))
                for C in Contents[1:]:
                    C.delete()
                    
        ModSocDB.Session.flush()


    # ======================================================================
    # Migration Function.
    #
    # These methods are used for the migration of the content to the rich
    # content classes defined below.
    # ======================================================================

    @staticmethod
    def migrateRawContent(DatasetID):
        """
        This method is used to handle iterative migration and linking of all
        raw Piazza content.  When run it will iterate over the full set of
        raw content items in the list and will generate subsidiary elements
        for them.
        """
        RawContentList = RawPiazzaContent.query.find()
        RawContentList = RawContentList.all()
        # print "RAW COUNT: %d" % (len(RawContentList))
        Results = [C.makeSplitContent(DatasetID) for C in RawContentList]
        # print "RESULTS: %d" % (len(Results))
        ModSocDB.Session.flush()
        return Results

    
    def makeSplitContent(self, DatasetID):
        """
        Convert this item to a new instance of PiazzaContent with its attached
        structures and store that in the database.  This is a destructive db
        update and thus should be called sparingly.
        """

        # --------------------------------------------
        # Produce the new instance object for use.
        # --------------------------------------------

        # Get the author of the Content: the first author in the history list.
        if self.history:
            firstHistory = min(self.history,key = lambda x:x.created)
            author_uid = firstHistory['uid']
            FirstAuthor = PiazzaUser.findUserByPiazzaID(author_uid)
            if (FirstAuthor == None):
                UserID = _migrateHandleMissingUser(author_uid)
                CentralID = None
            else:
                UserID = FirstAuthor._id
                CentralID = FirstAuthor.CentralUser_ID
        else:
            UserID = None
            CentralID = None

  
        New = PiazzaContent(
            Course_ID=DatasetID,
            Author_ID=UserID,
            CentralAuthor_ID=CentralID,            
            status=self.status,
            tag_good_arr=self.tag_good_arr,
            folders=list(set(self.folders) | set(self.tags)),
            id=self.id,
            type=self.type,
            unique_views=self.unique_views,
            created=parseDateFormat(self.created),
            ThreadID=self.nr,
            no_answer_followup=self.no_answer_followup)
            # config=copy.copy(self.config))

        ModSocDB.Session.flush()

        # --------------------------------------------
        # Produce the list of good tag instances.
        # --------------------------------------------

        for TagDict in self.tag_good:

            self._makeSplitTagGood(New, TagDict, DatasetID)
            
        # --------------------------------------------
        # Add the History elements.
        # --------------------------------------------
        
        for HistDict in self.history:
            # print "HistDict Found"
            self._makeSplitHist(New, HistDict, DatasetID)

        # --------------------------------------------
        # Add the ChangeLog elements.
        # --------------------------------------------

        for ChangeDict in self.change_log:
            # print "ChangeDict Found"
            self._makeSplitChange(New, ChangeDict, DatasetID)


        # --------------------------------------------
        # Add the Children.
        # --------------------------------------------

        for ChildDict in self.children:
            # print "ChildDict Found"
            self._makeSplitChild(New, ChildDict, DatasetID)


        # --------------------------------------------
        # Flush to catch previously-unsolved content.
        # --------------------------------------------
        ModSocDB.Session.flush()


    def _makeSplitTagGood(self, NewContent, TagDict, DatasetID):
        """
        Given a new Content item and a TagDict from the current
        instance this code will produce a new split TagGood instance
        and will add it into the database.
        """
     
        # Load the user for this tag to construct a link.  If
        # none is found then throw an error.  This uses the
        # database 'user_id' of the PiazzaUsers to find the user.
        TagUser = PiazzaUser.findUserByPiazzaID(TagDict['id'])
        # print "TagUser: %s" % (TagUser)
        if (TagUser == None):
            _migrateHandleMissingUser(TagDict['id'])
            #raise RuntimeError, "foo"
        else:
            # print TagDict['id']
            # print TagUser

            # Having set the UserID we now set the CentralUserID by either
            # chaining off of it or by using None.
            CentralID = TagUser.CentralUser_ID #PiazzaUser.getCentralUserIDByPiazzaUserID(TagUser._id)
                    
            # Now generate the new tag.
            NewTag = PiazzaContent_TagGood(
                Course_ID=DatasetID,
                Content_ID=NewContent._id,
                Author_ID=TagUser._id,
                CentralAuthor_ID=CentralID,
                name=TagDict['name'],
                admin=TagDict['admin'],
                photo=TagDict['photo'],
                email=TagDict['email'],
                role=TagDict['role'],
                facebook_id=TagDict['facebook_id'])

            return NewTag
        

    
    def _makeSplitHist(self, NewContent, HistDict, DatasetID):
        """
        Given a new Content instance and a HistDict this will generate
        a new PiazzaContent_History instance and will return it.
        """

        # print "Proc: Make Split Hist"
        
        # The history can have a None user if it is set to anonymous.
        # In this case the UserID will be set to None.  Else we will
        # throw an exception if no matching user is found.  The
        # 'uid' field here appears to be the piazza user_id field
        # and thus that will be used.
        #
        # However posts can be generated by the automatic piazza system
        # that are by the system itself and thus not linked to any
        # user.  Ergo this code will add those but leave them unlinked
        # to a user.
        #
        # Also if the user is found get the CentralUser_ID.  If it is not
        # then make a user and get the ID.  
        HistUser = PiazzaUser.findUserByPiazzaID(HistDict['uid'])
        # print HistDict
        if (HistUser == None):

            UserID = _migrateHandleMissingUser(HistDict['uid'])
            CentralID = None
            
        else:
            UserID = HistUser._id
            CentralID = HistUser.CentralUser_ID

        NewHist = PiazzaContent_History(
            Course_ID=DatasetID,
            Content_ID=NewContent._id,
            Author_ID=UserID,
            CentralAuthor_ID=CentralID,
            ThreadID = NewContent.ThreadID,
            content=HistDict['content'],
            subject=HistDict['subject'],
            uid=HistDict['uid'],
            anon=HistDict['anon'],
            created=parseDateFormat(HistDict['created']))

        return NewHist


    
    def _makeSplitChange(self, NewContent, ChangeDict, DatasetID):
        """
        Given a ChangeDict and a new split content item this code will
        produce a new change element for the data and will store it into
        the database.
        """

        # Find the user from the Piazza ID and return it as a user.
        ChangeUser = PiazzaUser.findUserByPiazzaID(ChangeDict['uid'])
        if (ChangeUser == None):
            UserID = _migrateHandleMissingUser(ChangeDict['uid'])
            # UserID = None
            CentralID = None
        else:
            UserID = ChangeUser._id
            CentralID = ChangeUser.CentralUser_ID

        NewLog = PiazzaContent_ChangeLog(
            Course_ID=DatasetID,
            Content_ID=NewContent._id,
            Author_ID=UserID,
            CentralAuthor_ID=CentralID,
            ParentPostID=ChangeDict['ParentPostID'],
            ThreadID = NewContent.ThreadID,
            data=ChangeDict['data'],
            uid=ChangeDict['uid'],
            anon=ChangeDict['anon'],
            type=ChangeDict['type'],
            when=parseDateFormat(ChangeDict['when']))


    def _makeSplitChild(self, NewContent, ChildDict, DatasetID):
        """
        Given a child dict and a new PiazzaContent instance this
        code will generate a split PiazzaContent_Child instance and
        will generate an instance of the subsidiary subchildren and
        child history instances.
        """

        Child_UID = ChildDict['uid']

        # As with the other cases pull the user who created the
        # child if any and add it here.   Unless the ID is None
        # Which sometimes happens for unexplained reasons thus
        # setting the user to None.  

        if (Child_UID == None):
            UserID = None
            CentralID = None
        else:
            User = PiazzaUser.findUserByPiazzaID(Child_UID)
            if (User == None):
                UserID = _migrateHandleMissingUser(Child_UID)
                UserID = None
                CentralID = None
            else:
                UserID = User._id
                # print User
                CentralID = User.CentralUser_ID

        # The data field is sometimes None or sometimes a dict that
        # contains a single 'embed-links' list.  This will extract
        # that if it is present as the NewData.
        if (ChildDict['data'] == None):
            NewData = {}
        else:
            NewData = ChildDict['data']

        # Now make the root child post instance.
        #  folders:  List of folders it is in.
        #  updated:  string form of when it was updated.
        #  d_bucket:  string of when to bin it (e.g. 'Yesterday')
        #  tag_endorse_arr: list of user id's who endorsed this.
        #  no_upvotes: an int listing (I suspect) the number of upvotes
        #    received.
        #  created: string form of creation date.
        #  config:  dict of unknown information, always empty in current dataset.
        #  no_answer: int of answer count (I suspect).
        #  anon: string indicating anonymity status in data (full | no)
        #  bucket_name:  name of bucket for this item (e.g. 'Yesterday')
        #  id:  string of the child id.
        #  bucket_order: int order in the bucket.
        #  type: string of child type.
        #  subject: string form of post subject (often long).
        NewChild = PiazzaContent_Child(
            Course_ID=DatasetID,
            Parent_ID=NewContent._id,
            Author_ID=UserID,
            CentralAuthor_ID=CentralID,
            ThreadID = NewContent.ThreadID,
            folders=self.folders,
            updated=parseDateFormat(ChildDict['updated']),
            tag_endorse_arr=ChildDict['tag_endorse_arr'],
            no_upvotes=ChildDict['no_upvotes'],
            uid=Child_UID,
            created=parseDateFormat(ChildDict['created']),
            config=ChildDict['config'],
            no_answer=ChildDict['no_answer'],
            anon=ChildDict['anon'],
            bucket_name=ChildDict['bucket_name'],
            id=ChildDict['id'],
            bucket_order=ChildDict['bucket_order'],
            type=ChildDict['type'],
            content=ChildDict['subject'])

        ModSocDB.Session.flush()

        # Then chain down to produce the sub-children endorsements
        # and history.
        for EndorseDict in ChildDict['tag_endorse']:
            # print "EndorseDict Found"    
            self._makeSplitChildEndorse(NewChild, EndorseDict, DatasetID)

        for SubchildDict in ChildDict['children']:
            # print "SubchildDict Found"
            self._makeSplitChildSubchild(NewChild, SubchildDict, DatasetID)

        for HistDict in ChildDict['history']:
            # print "HistDict Found"
            self._makeSplitChildHistory(NewChild, HistDict, DatasetID)
            

    def _makeSplitChildEndorse(self, NewChild, Dict, DatasetID):
        """
        Given a parent child instance and an endorsement dict this code will
        build the split Endorsement Dict instance and will link it in to the
        user.
        """

        User = PiazzaUser.findUserByPiazzaID(Dict['id'])
        
        if (User == None):
            UserID = _migrateHandleMissingUser(Dict['id'])
            CentralID = None
        else:
            UserID = User._id
            CentralID = User.CentralUser_ID
        
        Endorsement = PiazzaContent_Child_Endorsement(
            Course_ID=DatasetID,
            Parent_ID=NewChild._id,
            Author_ID=UserID,
            CentralAuthor_ID=CentralID,
            name=Dict['name'],
            admin=Dict['admin'],
            photo=Dict['photo'],
            us=Dict['us'],
            email=Dict['email'],
            role=Dict['role'],
            facebook_id=Dict['facebook_id'],
            id=Dict['id'],
            class_sections=Dict['class_sections'],
            in_permission=Dict['admin_permission'])


    def _makeSplitChildSubchild(self, NewChild, Dict, DatasetID):
        """
        Given a parent child instance and a dict containing subchild info
        produce the child itself.  This will include some variable parsing
        as we have to deal with dates.  
        """
        
        User = PiazzaUser.findUserByPiazzaID(Dict['uid'])

        if (User == None):
           UserID = _migrateHandleMissingUser(Dict['uid'])
           CentralID = None
        else:
            UserID = User._id
            CentralID = User.CentralUser_ID

        Subchild = PiazzaContent_Child_Subchild(
            Course_ID=DatasetID,
            Parent_ID=NewChild._id,
            Author_ID=UserID,
            CentralAuthor_ID=CentralID,
            ThreadID = NewChild.ThreadID,
            folders=self.folders,
            updated=parseDateFormat(Dict['updated']),
            d_bucket=Dict['d_bucket'],
            uid=Dict['uid'],
            created=parseDateFormat(Dict['created']),
            config=Dict['config'],
            anon=Dict['anon'],
            bucket_name=Dict['bucket_name'],
            id=Dict['id'],
            bucket_order=Dict['bucket_order'],
            type=Dict['type'],
            content=Dict['subject'])

        return Subchild


    def _makeSplitChildHistory(self, NewChild, Dict, DatasetID):
        """
        given a New Child instance and a dict representing history generate an
        appropriate subchild of it that can then be used to store the split
        history element for later use.  
        """
        User = PiazzaUser.findUserByPiazzaID(Dict['uid'])
        
        if (User == None):
            UserID = _migrateHandleMissingUser(Dict['uid'])
            CentralID = None
        else:
            UserID = User._id
            CentralID = User.CentralUser_ID
        
        NewHistory = PiazzaContent_Child_History(
            Course_ID=DatasetID,
            Parent_ID=NewChild._id,
            Author_ID=UserID,
            CentralAuthor_ID=CentralID,
            ThreadID = NewChild.ThreadID,
            content=Dict['content'],
            anon=Dict['anon'],
            subject=Dict['subject'],
            uid=Dict['uid'],
            created=parseDateFormat(Dict['created']))

        return NewHistory
    
def _migrateHandleMissingUser(UserID):
    """
    Handle cases where the supplied UserID is missing.
    just return None.
    """
    return None


# -------------------------------------------------
# Utility functions.
# =================================================

def parseDateFormat(DateStr):
    """
    Parse the date string for the fields.
    """
    if (DateStr == None): return None
    else: return datetime.datetime.strptime(
        DateStr,
        "%Y-%m-%dT%H:%M:%S.%fZ") # @Ri - Changes made to match the Piazza data date-time format

# -------------------------------------------------
# Query Functions.
# =================================================

def findAllRawContent(DatasetID=None):
    """
    Find all of the content from the database.
    """
    if (DatasetID == None): Set = RawPiazzaContent.query.find()
    else: Set = RawPiazzaContent.query.find({'Course_ID':DatasetID})
    return Set.all()


def collectRawContentByID(ContentID):
    """
    Find the user with the set Piazza ID.
    """
    Contents = RawPiazzaContent.query.find({'id':ContentID}).all()
    return Contents


def collectAllRawContentIDs(DatasetID=None):
    """
    Collect a list of all PiazzaIDs from the database.
    """
    Set = [C.id for C in findAllRawContent(DatasetID=DatasetID)]
    return Set


