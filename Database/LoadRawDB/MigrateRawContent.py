# This file is covered by the LICENSE file in the root of this project.
# @license <https://github.com/ArgLab/PiazzaDataAnalysisTool/blob/master/LICENSE>
#!/usr/bin/env python2.7
# MigrateRawContent.py
# @author: Collin Lynch
# @date: 10/11/2014
#
# Migrate all of the raw content to the split classes format.
# ===============================================
# Imports.
# ===============================================
import sys
import ModSocDB

# ===============================================
# Main Code.
# ===============================================

# -----------------------------------------------------------------------
# Load the dataset.
# -----------------------------------------------------------------------
DatasetShortName = sys.argv[1]
data_dir = sys.argv[2]
Dataset = ModSocDB.Classes.Dataset.findDatasetByShortName(DatasetShortName)
if (Dataset == None):
    raise ModSocDB.ModSocDBError, \
        "No matching Dataset found: %s" % (DatasetShortName)


# ----------------------------------------------------------------------
# Migrate the Piazza Data and perform the internal linking. 
# This will also split off the raw
# content files into the split elements.
# ----------------------------------------------------------------------
ModSocDB.Classes.Piazza.PiazzaUser.PiazzaUser.migrateRawContent(Dataset._id)
ModSocDB.Classes.Piazza.RawPiazzaContent.RawPiazzaContent.migrateRawContent(Dataset._id)

