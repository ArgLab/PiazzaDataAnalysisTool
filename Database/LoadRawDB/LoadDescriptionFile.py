# This file is covered by the LICENSE file in the root of this project.
# @license <https://github.com/ArgLab/PiazzaDataAnalysisTool/blob/master/LICENSE>
#!/usr/bin/env python2.7
"""
ReadDescFile.py
:Author: Collin Lynch
:Date: 10/11/2014

Simple input code to read in a data description file. Said file
should have a format where 1st line is the short name,
2nd line the long name, and the rest is the description.

This relies on the code in the Dataset class. 
"""

import ModSocDB, sys

DataFile = sys.argv[1]

print ModSocDB.Classes.Dataset.Dataset.loadDescriptionFile(DataFile)
ModSocDB.Session.flush()
