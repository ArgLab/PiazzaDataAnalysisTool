#!/usr/bin/env python2.7
"""
DropDuplicates.py

:Author: Collin F. Lynch
:Date: 03/22/2015

The raw data for the raw piazza contend and the users contains a
number of duplicate posts as do the piazza users as we are compelled
to load both sets of files.  This script will iterate over both and
will drop duplicate instances from the database based upon the
user_id in the case of users and id in the case of the content.
"""


# ==============================================================
# imports
# ==============================================================

import sys
import ModSocDB
import ModSocDB.Classes.Dataset as DatasetMod
import ModSocDB.Classes.Piazza.PiazzaUser as UserMod
import ModSocDB.Classes.Piazza.RawPiazzaContent as RawContentMod


# ==============================================================
# Main iteration
# ==============================================================

DatasetShortName = sys.argv[1]

Dataset = DatasetMod.findDatasetByShortName(DatasetShortName)

if (Dataset == None):
    raise ModSocDB.ModSocDBError, \
      "No matching Dataset found: %s" % (DatasetShortName)

print Dataset

UserMod.PiazzaUser.removeDuplicateUsers(Dataset._id)
RawContentMod.RawPiazzaContent.removeDuplicateContent(Dataset._id)

