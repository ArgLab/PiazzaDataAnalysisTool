# This file is covered by the LICENSE file in the root of this project.
# @license <https://github.com/ArgLab/PiazzaDataAnalysisTool/blob/master/LICENSE>
README.txt
Collin F. Lynch & Niki Gitinabard
Updated 8/22/2018

This directory contains loading scripts to parse raw course data into the MongoDB format.  Only the LoadRawDB.sh and should be called directly and it will call the rest as needed.


* LoadRawDB.sh
-------------------------------------------
Shell script to load raw course data into the database.  This should be updated as new data is made available.  

Example:
./LoadRawDB.sh DATA_DIRECTORY DATASET_SHORT_NAME


* MigrateRawContent.py
-------------------------------------------
This script will migrate any raw loaded data for Piazza from the loaded format to the broken out type.  This is called by LoadRawDB.sh



