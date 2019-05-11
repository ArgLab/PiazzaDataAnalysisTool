# This file is covered by the LICENSE file in the root of this project.
# @license <https://github.com/ArgLab/PiazzaDataAnalysisTool/blob/master/LICENSE>
#!/usr/bin/env python
"""
ModSocDB.py

:Author: Collin Lynch
:Date: 09/29/2014

This package provides for a basic interface to the MOOT database.
When initialized it will setup a thread-local working session as
well as other features.  It also defines a class structure that
can be used to wrap up connections if necessary.
"""


# ---------------------------------------------------
# Imports.
# ---------------------------------------------------
import ming
import ming.odm

# import ModSocDBError


# =====================================================================
# Global Variables.
#
# The library defines a set of shared session objects on initialization
# making a functioning MongoDB instance a requirement.  These should be
# then accessible to users of the library as needed.  
# =====================================================================

# name of the database being used.  
DatastoreName = "DM_ModSocDB"

# This is a predefined bound datastore linked to the database.  It will
# be available to the library and should be used for all calls.
BoundDatastore = ming.create_datastore(DatastoreName)


# The document session is a general (non thread-safe) session that will
# be used for access to the documents as needed.
DocumentSession = ming.Session(BoundDatastore)


# The Session session is a thread-safe session that should be used for
# all activity calls and will be the basis for the document calls. 
Session  = ming.odm.ThreadLocalODMSession(doc_session=DocumentSession)






# # ========================================================
# class ModSocDB(object):
#     """
#     The ModSocDB class provides an interface to the threadlocal session
#     for access to object queries, additions and production.  When used
#     it should be treated like a proxy to the session and as a basis
#     for basic class wrappers.
#     """

#     # -------------------------------------------------------
#     # Init.
#     # =======================================================

#     def __init__(self, DatastoreName="DM_ModSocDB"):
#         """
#         Initialize the datastore and provide access for queries.
#         This uses the threadlocal session for acces.
#         """

#         # Bind the datastore to produce working ODM Session.
#         # ---------------------------------------------------
#         BoundDatastore = ming.create_datastore(Datastorname)
#         DocumentSession = ming.Session(BoundDatastore)
#         WorkingSession  = ming.odm.ThreadLocalODMSession(
#             doc_seeion=DocumentSession)




        
#     # ----------------------------------------------
#     # Accessors.
#     # ==============================================

#     def getWorkingSession(self):
#         """
#         Get the working session 
