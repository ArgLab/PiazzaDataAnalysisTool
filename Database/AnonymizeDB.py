# This file is covered by the LICENSE file in the root of this project.
# @license <https://github.com/ArgLab/PiazzaDataAnalysisTool/LICENSE>
#!/usr/bin/env python2.7
"""
AnonymizeDB.py
@author: Collin F. Lynch
@date: 12/5/2014

This script provides a basic anonymization of a ModSocDB.  When run
it will strip out raw content from the database and will anonymize
all user information in the remaining User fields and will then, for
all linked objects that contain user data it will replace any
identifying information.

Links between objects will be maintained but instances of user ID
or identifying features will be replaced with anonymous id information
which will be generated according to the static anon formula.

This code will then trawl through the text of the comments and entries
to replace name instances with <ID>_First and <ID>_Second.

When run this code will also dump a csv file that maps the new anonymous
ID to the user_id and name fields.

TODO: Anonymize Post ID numbers.
"""


# ===============================================================
# Imports.
# ===============================================================

import csv, sys
from pyexcel_xlsx import get_data
import ModSocDB
import ModSocDB.Classes.Piazza as PiazzaMod
import ModSocDB.Classes.User as UserMod
# ===============================================================
# Static Variables. 
# ===============================================================

SAVE_FILE_FIELDS = ["RealName", "RawUID", "AnonID", "PiazzaID"]



# ==================================================
# Main Loop
# ==================================================

def anonymizeDB(SaveFile, LoadFile):
    """
    Anonymize the linked ModSocDB.  This is a 3-pass process:
    1) Delete all raw content.
    2) Generate anonymous IDs for the users and store them
       on the users in lieu of the existing ids.
    3) Iterate over the content converting all instances of
       a user to their linked anonymous name.
    4) Finally anonymize the user instance itself.
    """
    dropRawContent()
    makeAnonUsers(SaveFile, LoadFile)
    ModSocDB.Session.flush()


    
def dropRawContent():
    """
    Iterate over the RawPiazzaContent collection deleting each
    instance in it.
    """
    print "================== Dropping Raw Content ==============="
    Items = PiazzaMod.RawPiazzaContent.findAllRawContent()
    for I in Items:
        print I
        I.delete()



def makeAnonUsers(SaveFile, LoadFile):
    """
    SECRET

    This file implements the secret transition to anonymous IDs for all
    of the Piazza Content.  It operates by first updating the PiazzaUser
    instances by generating a new ID number for them.  This is based upon
    a computation of the polynomial function below that converts the user
    ID to a numerical value and then adds the secret key to it before
    replacing the nonanonymous content with associated information.

    This code will then anonymize the data linked to the user.  For each
    of the posts or post history items it will search the text for a given
    instance of the user's name and will then anonymize it by replacing the
    instances of the first and last name with the ID of the form: <ID>_FirstName
    and <ID>_LastName.  This will be a rough pass that checks for full names and
    does not always deal well with duplicate names.

    The code will then update the user instances with their new names in the
    split name fields.  The Full name field will simply be deleted.  

    This amounts to a destructive update of the PiazzaUser class and is
    dealt with by generating a csv that maps IDs and real names to the
    new anonymous ID.

    NOTE:: This is in essence the Caeser cypher on strings with an 
      adaptive shift value.  
    """
    print "================= Making Anon Users ==================="

    # Open the save file for the updates and create a
    # CSV DictWriter for the updates.
    # ------------------------------------------------
    Out = open(SaveFile, "w")
    Writer = csv.DictWriter(Out, SAVE_FILE_FIELDS)
    Writer.writeheader()
    Out.flush()
    
    # Collect the set of users and iterate over them
    # for anonymization.  This will iteratively update
    # the UserHash which maps old IDs to new users.
    # ---------------------------------------------
    UIDMap = {}

    user_data = get_data(LoadFile)

    # in some type of OS, it doesn't return list and needs to change to become the list
    masterUserData = user_data if isinstance(user_data, list) else user_data.items()[0][1]
    masterUserData = [dict(zip(masterUserData[0],row)) for row in masterUserData[1:] if row !=None]    
    master_data_dict = {user['username']: user['anonID'] for user in masterUserData}
    master_data_dict['unknown'] = 'unknown'
    # NewVal = master_data_dict[User.username]
    # for row in masterUserData:
    #     if User.getUsername() == row['username']:
    #         NewVal = str(row['anonID'])
    

    NewIDs = []
    # NewShiftVal = ShiftVal
    # Users = ModSocDB.Classes.PiazzaUser.findAllUsers(Timeout=False)\
    UserIDs = UserMod.collectAllUserIDs()
    for UID in UserIDs:
        print "--------- Handling User: %s ---------------" % (UID)
        User = UserMod.findUserBy_ID(UID)
        NewVal = master_data_dict[User.getUsername()]
        (NewID, Dict) = setAnonID(User, NewIDs, UIDMap, Writer, NewVal)
        NewIDs.append(NewID)
        print "USER DICT::"
        print Dict
        print "\n\n"
        Out.flush()
        ModSocDB.Session.flush()
            
    # Close the output file.
    # -----------------------------------------------
    Out.close()

    print "##### FINISH STAGE 1 #####"
    
    # And finally deal with the back-linked objects such as the
    # individual classes via the sync-user-data calls or by name
    # replacement in the case of the isolated data.
    #
    # This code relies on the fact that the objects are all linked
    # to the data and that the central linked users have already
    # been anonymized and thus that the code will only need to copy
    # in the names from the user instance.
    #
    # This assumes that the syncUserInfo method has been implemented
    # appropriately and is added here. 
    # ----------------------------------------------------------
    # UNCOMMENT FOR RUN
    replaceUnlinkedPiazzaRefs(UIDMap)
    PiazzaMod.PiazzaUser.PiazzaUser.overwriteUserData()
    PiazzaMod.PiazzaContent.PiazzaContent.overwriteUserData()
    PiazzaMod.PiazzaContent_Child.PiazzaContent_Child.resetIds()
    PiazzaMod.PiazzaContent_Child_History.PiazzaContent_Child_History.overwriteUserData()
    PiazzaMod.PiazzaContent_Child_Subchild.PiazzaContent_Child_Subchild.overwriteUserData()
    PiazzaMod.PiazzaContent_Child_Endorsement.PiazzaContent_Child_Endorsement.overwriteUserData()
    PiazzaMod.PiazzaContent_TagGood.PiazzaContent_TagGood.overwriteUserData()
    PiazzaMod.PiazzaContent_History.PiazzaContent_History.overwriteUserData()
    PiazzaMod.PiazzaContent_ChangeLog.PiazzaContent_ChangeLog.overwriteUserData()


def setAnonID(User, NewIDs, UIDMap, Writer, NewVal):
    """
    Given a User, a ShiftVal, a dict mapping old IDs to users, and a
    DictWriter that has already been opened and primed this code will
    first calculate a new anonymous ID for the user and will set that
    in the user instance.  

    It will then iterate over all text content in the database
    updating it to anonymize the user content.
    
      NOTE:: This is messy and problematic to say the least.

    It will then update the local name fields on the user instance
    to use the Anon ID if they are present.

    This means creating the ID, resetting the content and then
    updating all of the elements but not the links as the objects
    have not changed in the database.  
    """

    # Create the new ID and set it locally.
    # Note that the local ID is counter based so it will be
    # introduced on that premise.  
    # --------------------------------------------------------
    UID = User.getLocalUserID()
    AnonID = makeAnonID(User, NewIDs, NewVal)    

    User.setLocalUserID(AnonID)
 
    if (User.PiazzaID != None):
        PiazzaID = User.PiazzaID
        UIDMap[PiazzaID] = AnonID
    else: PiazzaID = None
    
    
    # Write out the csv field with the updated information.
    # ---------------------------------------------------------
    Dict = { "RealName" : User.getName(),
             "RawUID"   : UID,
             "AnonID"   : AnonID,
             "PiazzaID" : PiazzaID }

    # The WriteDict is encoded to avoid output errors while the
    # working is left in the raw form.  
    WriteDict = { "RawUID"   : UID.encode("utf8"),
                  "AnonID"   : AnonID.encode("utf8") }
    
    if (User.getName() == None): WriteDict["RealName"] = None
    else: WriteDict["RealName"] = User.getName().encode("utf8")

    if (PiazzaID == None): WriteDict["PiazzaID"] = None
    else: WriteDict["PiazzaID"] = PiazzaID.encode("utf8") 
        
    Writer.writerow(WriteDict)
    
    
    # Anonymize all of the content.
    # ----------------------------------------------------------
    # UNCOMMENT FOR RUN
    replaceUserName(User)
    # replaceMoodleUserName(User)
    
    # Anonymize the name fields.
    # ----------------------------------------------------------
    # UNCOMMENT FOR RUN.
    User.anonymizeNameFields()
        
    # Return the Anon Dict.
    # ---------------------------------------------------------
    return (AnonID, Dict)

    

# def makeAnonID(CurrID, ShiftVal, NewIDs):
#     """
#     Given an ID string implement a basic Caeser Cypher(ish) shift 
#     of the string given the ShiftVal.  To that end we convert the 
#     existing ID to a number and then multiply it by the shift value.
#     We then modulo this number to within 1663* the number of existing
#     IDs and form a candidate ID.  If that ID already exists we increment
#     the number by 1 until an unused ID is found and then repeat.  

#     We then update the Shift value 
    
#     This is anonymous enough for our needs.
#     """

#     Shift = ShiftVal

#     Result = "USERID_"
#     for Char in CurrID:
#         NewVal = (ord(Char) * Shift)
#         # NewVal += (ShiftVal % 1663)
#         # NewVal = (NewVal * ShiftVal)
#         Shift = (NewVal % 79)
#         Result += "%s:" % (NewVal)
#     print "Checking ID: %s %d" % (Result, Shift)

#     print (len(NewIDs))
    
#     while (Result in NewIDs):
#         Result = "USERID_"
#         for Char in CurrID:
#             NewVal = (ord(Char) * Shift)
#             # NewVal += (ShiftVal % 1663)
#             # NewVal = (NewVal * ShiftVal)
#             Shift = (NewVal % 79)
#             Result += "%s:" % (NewVal)
#             print "Checking ID: %s %d" % (Result, Shift)
            
#     return (Result[:-1], Shift)


def makeAnonID(User, NewIDs, NewVal):
    """
    This code takes the ShiftVal and performs a basic 
    Caesar cypher on a unique ID composed of the User 
    ID and a shift value which should be prime.  That
    value is given as an argument to the initial call.

    The decision to include the list of NewIDs as an 
    argument and the ShiftVal as a return value was 
    done to support the more complex adaptive cypher 
    that is tested above.  
    """

    # Extract the content for the new ID.
    # ---------------------------------------------
    UID = User.getLocalUserID()
    Name = User.getName()
    
    if (Name == None): CurrID = UID
    else: CurrID = "%s|%s" % (UID, Name)
    
            
    print "AnonID:", NewVal

    
    # Generate the new anonymized ID character
    # by character.
    # -----------------------------------------
    Result = "USERID_"
    # for Char in CurrID:
    #     NewVal = (ord(Char) * ShiftVal)
    #     # NewVal += (ShiftVal % 1663)
    #     # NewVal = (NewVal * ShiftVal)
    #     Result += "%s:" % (NewVal)
    Result += str(NewVal)
        
    # And finally return the new values.
    # ---------------------------------------------
    return (Result)




def replaceUserName(User):
    """
    Given a user, find all instances of the user's real name in the
    content objects.  The areas of concern are the PiazzaContent_History
    instances as well as the PiazzaContent_Child instances and their
    associated _History and _Subchild data.

    The names will be replaced with anonymized forms based upon the
    UserID which presumes that the ID has been anonymized already but
    that the name fields have not.  

    This will ignore any name fields that are blank in the system.  They 
    will be left untouched and no attempt will be made to anonymize them.
    """
    # print "======================================================="
    # print "Checking User: %s %s" % (User.user_id, User.name)

    # Check all of the content history.
    # --------------------------------------------------------
    print "Checking Content History."
    ContentHistory = PiazzaMod.PiazzaContent_History.findAllContentHistory()

    for H in ContentHistory:
        anonymizeSubjectField(User, H)
        anonymizeContentField(User, H)
        

    # Check all of the children.
    # --------------------------------------------------------
    print "Checking Children."
    Children = PiazzaMod.PiazzaContent_Child.findAllChildren()

    for C in Children:
        anonymizeContentField(User, C)

        # And check all of the child history elements.
        print "Checking Child History."
        for H in C.History:
            anonymizeSubjectField(User, H)
            anonymizeContentField(User, H)

        # And do the change for each subchild.
        print "Checking Subchildren."
        for S in C.Subchildren:
            anonymizeContentField(User, S)

    # Check all of the peer tutor transaction descriptions.
    # --------------------------------------------------------
    # print "Checking PeerTutor Transaction Descriptions."
    # Transactions = PeerTutorMod.findAllTransactions()

    # for T in Transactions:
    #     anonymizeDescriptionField(User, T)

# def replaceMoodleUserName(User):
# 	print "Checking Moodle Information"
# 	Actions = MoodleMod.findAllActions()

# 	for A in Actions:
# 		anonymizeInformationField(User, A)

def anonymizeDescriptionField(User, Obj):
    """
    Given a user and an object with a description field make the
    anonymization to the text.  If the field is None then
    it will do nothing.  If the Name is None then this will
    do nothing. 
    """
    
    if (Obj.description != None):
        AnonymizedText = Obj.description
        username = User.username
        if (username == None):
            if (User.email):
                username = User.email.split('@')[0]
        if (username != None and AnonymizedText != None):
            AnonymizedText = AnonymizedText.replace(username, User.makeUsernameAnonForm())
        AnonymizedText = User.anonymizeNamesInText(AnonymizedText)
        if (AnonymizedText != None):
            print "Updated: %s" % (AnonymizedText.encode("UTF-8"))
            Obj.description = AnonymizedText


def anonymizeInformationField(User, Obj):
    """
    Given a user and an object with a description field make the
    anonymization to the text.  If the field is None then
    it will do nothing.  If the Name is None then this will
    do nothing. 
    """
    
    if (Obj.information != None):
        AnonymizedText = Obj.information
        username = User.username
        if (username == None):
            if (User.email):
                username = User.email.split('@')[0]
        if (username != None and AnonymizedText != None):
            AnonymizedText = AnonymizedText.replace(username, User.makeUsernameAnonForm())
        AnonymizedText = User.anonymizeNamesInText(AnonymizedText)
        if (AnonymizedText != None):
            print "Updated: %s" % (AnonymizedText.encode("UTF-8"))
            Obj.information = AnonymizedText

def anonymizeSubjectField(User, Obj):
    """
    Given a user and an object with a subject field make the
    anonymization to the text.  If the field is None then
    it will do nothing.  If the Name is None then this will
    do nothing. 
    """
    if (Obj.subject != None):
        # print "Checking Subject: %s" % (Obj.subject.encode("UTF-8"))
        AnonymizedText = User.anonymizeNamesInText(Obj.subject)
        if (AnonymizedText != None):
            print "Updated: %s" % (AnonymizedText.encode("UTF-8"))
            Obj.subject = AnonymizedText


def anonymizeContentField(User, Obj):
    """
    Anonymize the content field of the supplied object.
    """
    if (Obj.content != None):
        # print "Checking Content: %s" % (Obj.content.encode("UTF-8"))
        AnonymizedText = User.anonymizeNamesInText(Obj.content)
        if (AnonymizedText != None):
            print "Updated: %s" % (AnonymizedText.encode("UTF-8"))
            Obj.content = AnonymizedText


def replaceUnlinkedPiazzaRefs(UIDMap):
    """
    Given the UID to user map as an optional argument replace the
    name in all of the back-linked content.  In this case the
    issue is the list of tag_good_arr and endorsements in the
    database that cache the user IDs.  These are replaced from
    the original via the simple dict mapping.
    """

    Content = PiazzaMod.PiazzaContent.findAllContent() #(Timeout=False)
    for C in Content: C.resetTagGoodArr(UIDMap)

    Children = PiazzaMod.PiazzaContent_Child.findAllChildren() #(Timeout=False)
    for C in Children: C.resetTagEndorseArr(UIDMap)

    # ModSocDB.Session.flush()


    
# =================================================
# Main Loop.
# =================================================

if __name__ == "__main__":
    import sys

    SaveFile = sys.argv[1]
    LoadFile = sys.argv[2]
    
    #anonymizeDB(1277, SaveFile)
    anonymizeDB(SaveFile, LoadFile)
    

    # https://oeis.org/A035497
