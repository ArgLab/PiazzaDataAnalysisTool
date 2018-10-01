#!/usr/bin/env python
"""
User.py
:Author: Collin Lynch
:Date: 01/14/2015

This class provides for a central system user instance.
"""


# ===========================================
# imports.
# ===========================================

import csv

# Ming imports required for class definition.
# -------------------------------------------
from ming import schema
from ming.odm.declarative import MappedClass
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty

# Load of core library and error class.
# -----------------------------------------------------
import ModSocDB
from ModSocDB import ModSocDBError
import ModSocDB.Utils as Utils
# Split libraries.
# --------------------------------------------------
import name_tools




# ================================================
class User(MappedClass):
    """
    The User class provides a central identifier for a user.  It is
    based on the PiazzaUser instance primarily and includes some of
    the same content including the anonymous ID.  It will ultimately
    be a vehicle for adding in other methods to calculate per-user
    statistics.  
    
    Collection: users

    Relations:
    * PiazzaUser: Link to the associated Piazza User.
    * Dataset: Link to the associated Dataset.
   
    Fields:
    * _id: Unique Mongodb ID.
    * PiazzaUser_ID: Mongo ID of the Piazza User.
    * Dataset_ID: ID of the associated Dataset.
    * local_user_id: Local anonymously assigned user ID info.
    * PiazzaID:      Piazza ID for user.
    * StudentNumber: Student ID number. 
    * name:          Full student name.
    * first_name:    Split first name.
    * middle_name:   Split middle name.
    * last_name:     Split last name.
    * email:         Student's email address.
    * piazza_alt_email: Alternate email address.
    * username:      system username.
    * Instructor:    instructor name.
    * SectionNumber: integer section number. 
    * role:          Role in the course - Student, Instructor, or TA
    * postCount:    Count for number of piazza posts.
    * PiazzaDays:   Days active or logged in.
    * PiazzaViews:  Count of views made.
    * PiazzaAsks:   Count of asks made.
    * PiazzaAnswers:    Count of answers given to question.
    * FinalGrade:   Final grade of the student.
    """

    # ---------------------------------------------
    # Mongometa information.
    #
    # You should change only the "name" field to be
    # the name of the associated database collection.
    # =============================================
    class __mongometa__:
        session = ModSocDB.Session
        name = "users"

    # ------------------------------------------------
    # Link information.
    #
    # Put any links here following the model of the
    # author link below.
    # ================================================

    # Link to the associated Dataset.
    Dataset_ID = ForeignIdProperty('Dataset')
    Dataset    = RelationProperty('Dataset')

    # Link to the associated Piazza User.
    PiazzaUser_ID = ForeignIdProperty('PiazzaUser.PiazzaUser')
    PiazzaUser = RelationProperty('PiazzaUser.PiazzaUser')

    # ------------------------------------------------
    # Link information.
    #
    # Every object will have an _id field so that need
    # not be changed.  Other lines will be a FieldProperty
    # for the association information.  
    # ================================================

    # Mongodb object ID (unique).
    _id     = FieldProperty(schema.ObjectId)

    # Unique user ID set on introduction by the counter
    # mechanism.  
    local_user_id = FieldProperty(str)
    
    PiazzaID = FieldProperty(str)
    StudentNumber = FieldProperty(str)    

    # Student real name or anonymized name.
    name      = FieldProperty(str)
        
    # Split field for individual names.
    first_name  = FieldProperty(str)
    middle_name = FieldProperty(str)
    last_name   = FieldProperty(str)

    # User's email address (is in standard form so can be split.)
    email   = FieldProperty(str)
    
    # User's alternate email address (is in standard form so can be split.)
    piazza_alt_email   = FieldProperty(str)

    # Username
    username = FieldProperty(str)

    # Instructor they have and Section number to which they are assigned. 
    # The loading code needs to be modified based on the inputs to update these field.
    Instructor = FieldProperty(str)
    SectionNumber = FieldProperty(int)


    # Class role - Student, Instructor, or TA
    # The loading code needs to be modified based on the inputs to update this field.
    role = FieldProperty(str)

    #Count for piazza posts
    postCount = FieldProperty(int)
    
    # Count of answers given to questions.
    PiazzaAnswers = FieldProperty(int)
    
     # Count of views made.  
    PiazzaViews   = FieldProperty(int)
    
    # Count of asks made.  
    PiazzaAsks    = FieldProperty(int)
    
    # Days active or logged in?
    PiazzaDays    = FieldProperty(int)
    
    #final letter grade of student
    # The loading code needs to be modified based on the inputs to update this field.
    FinalGrade = FieldProperty(str)

    # -------------------------------------------------
    # Static Constructor.
    # =================================================

    @staticmethod
    def makeNewUser(DatasetID, Name, PiazzaUserID=None, PiazzaId = None,
                    WebAssignUserID=None, MoodleActionID=None, Studentnumber = None,
                    Email=None, Alt_Email=None, FirstName=None, MiddleName=None,
                    LastName=None, Username=None, Instructor=None,
                    SectionNumber=None,isPeerTutor=None, 
                    Role=None, FlushSession=True):
        """
        Construct a new user.  This will set the email
        and name fields directly from the argument and
        will then return the user instance.  The
        *_name fields will be set via the split name
        function and the local_user_id field will be
        set based upon the current number of users.
        This is not reset safe.
        """

        # Calculate the new ID.
        LocalID = "USER_%d" % (countAllUsers())
        if not Username and Email:
            Username = Email.split('@')[0]
        # Calculate the Split name field values unless
        # they are supplied.  If however the Name is None
        # then all will be None.
        if (Name == None):
            NewUser = User(
                Dataset_ID=DatasetID,
                PiazzaUser_ID=PiazzaUserID,
                WebAssignUser_ID=WebAssignUserID,
                MoodleAction_ID=MoodleActionID,
                local_user_id=LocalID,
                PiazzaID = PiazzaId,
                StudentNumber = Studentnumber,
                name=None,
                first_name=None,
                middle_name=None,
                last_name=None,
                email=Email,
                piazza_alt_email = Alt_Email,
                username=Username,
                Instructor=Instructor,        
                SectionNumber=SectionNumber)
                
        elif (FirstName == None):
            SplitNameDict = ModSocDB.NLP.makeSplitNameDict(Name)
            NewUser = User(
                Dataset_ID=DatasetID,
                PiazzaUser_ID=PiazzaUserID,
                WebAssignUser_ID=WebAssignUserID,
                MoodleAction_ID=MoodleActionID,
                local_user_id=LocalID,
                PiazzaID = PiazzaId,
                StudentNumber = Studentnumber,
                name=Name,
                first_name=SplitNameDict["FirstName"],
                middle_name=SplitNameDict["MiddleName"],
                last_name=SplitNameDict["LastName"],
                email=Email,
                piazza_alt_email = Alt_Email,
                username=Username,
                Instructor=Instructor,
                SectionNumber=SectionNumber)
                
        else:
            NewUser = User(
                Dataset_ID=DatasetID,
                PiazzaUser_ID=PiazzaUserID,
                WebAssignUser_ID=WebAssignUserID,
                MoodleAction_ID=MoodleActionID,
                local_user_id=LocalID,
                PiazzaID = PiazzaId,
                StudentNumber = Studentnumber,
                name=Name,
                first_name=FirstName,
                middle_name=MiddleName,
                last_name=LastName,
                email=Email,
                piazza_alt_email = Alt_Email,
                username=Username,
                Instructor=Instructor,        
                SectionNumber=SectionNumber)

        # If we are set to flush then do so.
        if (FlushSession == True):
            ModSocDB.Session.flush()

        return NewUser



    # -------------------------------------------------
    # User Data.
    # =================================================

    def getUserDataDict(self):
        """
        Make the user data dictionary.
        """
        Dict = {}
        Dict["UserID"] = self.ID
        return Dict


    # -------------------------------------------------
    # Accessors/Settors
    # =================================================

    def getName(self):
        """
        Return the user name.
        """
        return self.name


    def setName(self, NewName):
        """
        Set the new user name.
        """
        self.name = NewName
    

    def getLocalUserID(self):
        """
        Get the local user Id value.
        """
        return self.local_user_id

        
    def setLocalUserID(self, NewID):
        """
        Set the local user ID value.
        """
        self.local_user_id = NewID


    def getFirstName(self):
        """
        Get the first_name value.
        """
        return self.first_name


    def setFirstName(self, NewName):
        """
        Set the first_name field.
        """
        self.first_name = NewName


    def getMiddleName(self):
        """
        Get the middle_name value.
        """
        return self.middle_name

    
    def setMiddleName(self, NewName):
        """
        Set the middle_name field.
        """
        self.middle_name = NewName


    def getLastName(self):
        """
        Get the last_name value.
        """
        return self.last_name

    
    def setLastName(self, NewName):
        """
        Set the last_name field.
        """
        self.last_name = NewName


    def getEmail(self):
        """
        Get the email.
        """
        return self.email

    
    def setEmail(self, NewEmail):
        """
        Set the new email.
        """
        self.email = NewEmail


    def getUsername(self):
        """
        Get the username.
        """
        return self.username

    
    def setUsername(self, NewUsername):
        """
        Set the new username.
        """
        self.username = NewUsername 


    def getRole(self):
        """
        Get the role.
        """
        return self.role


    def setRole(self, NewRole):
        """
        Set the new role.
        """
        self.role = NewRole


    def getPostCount(self):
        """
        Get the role.
        """
        return self.postCount


    def setPostCount(self, NewCount):
        """
        Set the new role.
        """
        self.postCount = NewCount


    # ---------------------------------------------
    # Anonymization Code.
    # =============================================

    def anonymizeNameFields(self):
        """
        This code resets all of the local name fields to contain
        an anonymous form based upon the salted user ID.  This
        will simply set the specific name fields for the user to
        the IDs and will purge the group name field.

        For the sake of clarity this will only anonymize cases where
        the field is nonempty.  In cases where it is none then it 
        will simply be left as is.  
        """
        # NewID = self.getUserID()

        if (self.getFirstName() != None):
            self.setFirstName(self.makeFirstNameAnonForm())
            
        if (self.getMiddleName() != None):    
            self.setMiddleName(self.makeMiddleNameAnonForm())

        if (self.getLastName() != None):
            self.setLastName(self.makeLastNameAnonForm())

        if (self.name != None):
            self.setName(self.makeNameAnonForm())

        if (self.email != None):
            self.setEmail(self.makeEmailAnonForm())

        if (self.username != None):
            self.setUsername(self.makeUsernameAnonForm())


    def makeFirstNameAnonForm(self):
        """
        This is a stock method that returns the anon form of
        the first name for later use.
        """
        return "%s_FirstName" % (self.getLocalUserID())


    def makeMiddleNameAnonForm(self):
        """
        This is a stock method that returns the anon form of
        the middle name for later use.
        """
        return "%s_MiddleName" % (self.getLocalUserID())


    def makeLastNameAnonForm(self):
        """
        This is a stock method that returns the anon form of
        the last name for later use.
        """
        return "%s_LastName" % (self.getLocalUserID())


    def makeNameAnonForm(self):
        """
        This is a stock method that returns the anon form of
        the name for later use.
        """
        return "%s_Name" % (self.getLocalUserID())


    def makeEmailAnonForm(self):
        """
        This is a stock method that returns the anon form of
        the email for later use.
        """
        return "%s_Email" % (self.getLocalUserID())

    def makeUsernameAnonForm(self):
        """
        This is a stock method that returns the anon form of
        the username for later use.
        """
        return "%s_Username" % (self.getLocalUserID())

    # ----------------------------------------------------
    # NLP Tasks.
    # ====================================================

    def nameInTextP(self, TextStr):
        """
        Given a text string check to see if the user's first name,
        last name, or full name appear in it.  This depends upon
        the nltk library.  If the Name is None then this will return
        False.
        """
        if (self.name == None): return False
        else: return ModSocDB.NLP.findNameInText(self.name, TextStr)


    def anonymizeNamesInText(self, TextStr):
        """
        Performs a replacement of the names in the text with the anonymized form
        of the names as generated by the makeAnon methods above.
        
        NOTE:: This is not a destructive replacement and only
          returns an updated form.  Or None if no changes are
          made.

        NOTE:: If the name is none then this will do nothing.
        """
        
        return self.replaceNameInText(
            self.makeFirstNameAnonForm(),
            self.makeLastNameAnonForm(),
            TextStr)
    
        
    def replaceNameInText(self, FirstNameReplacement, LastNameReplacement, TextStr):
        """
        Given a text string replace the user's name in it if
        it is present using the supplied first and last
        replacement strings.

        NOTE:: This is not a destructive replacement and only
          returns an updated form.  Or None if no changes are
          made.

        NOTE:: If the FirstName and LastName are none then this 
          will do nothing.
        """

        if ((self.getFirstName() == None) and (self.getLastName() == None)):
            return None
        
        return ModSocDB.NLP.replaceNameInText(
            self.getFirstName(), self.getLastName(),
            FirstNameReplacement, LastNameReplacement,
            TextStr)


    

    

# -------------------------------------------------
# Query Functions.
# =================================================

def collectAllUserIDs(DatasetID=None):
    """
    Collect a list of all PiazzaIDs from the database.
    """
    Set = [U._id for U in findAllUsers(DatasetID=DatasetID)]
    return Set


def findAllUsers(DatasetID=None, Timeout=True):
    """
    Collect all users from the database.
    """
    if (DatasetID == None): Set =  User.query.find()#(timeout=Timeout)
    else: Set =  User.query.find({'Dataset_ID': DatasetID})#(timeout=Timeout)
    return Set.all()


def countAllUsers():
    """
    Simple query method to count all users in the DB.
    """
    Count = User.query.find().count()
    return Count


def findUserByName(UserName):
    """
    Find the user with the set name.
    """
    U = User.query.find({'name':UserName}).all()
    U = U[0] if len(U) > 0 else None
    return U


def findUserByFirstLast(FirstName, LastName):
    """
    Find the user with the set name.
    """
    U = User.query.find({'first_name':FirstName, 'last_name':LastName}).all()
    U = U[0] if len(U) > 0 else None
    return U


def findUserByUsername(UserName):
    """
    Find the user with the set name.
    """
    U = User.query.find({'username':UserName}).all()
    U = U[0] if len(U) > 0 else None
    return U


def findUserBy_ID(UserID):
    """
    Find the user with the set name.
    """
    U = User.query.find({'_id':UserID}).all()
    U = U[0] if len(U) > 0 else None
    return U

def findUserByEmail(Email):
    """
    Find the user with the set email.
    """
    U = User.query.find({'email':Email}).all()
    U = U[0] if len(U) > 0 else None
    return U
