# This file is covered by the LICENSE file in the root of this project.
# @license <https://github.com/ArgLab/PiazzaDataAnalysisTool/blob/master/LICENSE>
README.txt
Collin Lynch & Niki Gitinabard
Updated 8/22/2018

This directory should be used for database loading code.  It contains scripts to erase the database, load raw files in and dump and import backup data.  

Code:

* ClearDB.mongo
------------------------------------------
Mongo DB Script that initializes and clears the DM_ModSocDB.

Example:
mongo ClearDB.mongo



* DumpDB.sh
-------------------------------------------
Dumps the DM_ModSocDB to a tarball containing JSON array files for each collection.  This must be updated as collections are added. You can change what the output dump archive is called in this script.

Example:
./DumpDB.sh DATA_OUTPUT_DIRECTORY


* LoadDBDumps.sh
-------------------------------------------
Code to load a tarball of collections saved as JSON arrays.  

Example:
./LoadDBDumps.sh DATA_OUTPUT_DIRECTORY


* AnonymizeDB.py
-------------------------------------------
Code to anonymize the content of the database clearing usernames and other content.
This should be called only once after raw loading takes place. For running this script, you need one csv file with all the students' usernames and a number matched to any of them (the columns should be called username and anonID).

Example:
python AnonymizeDB.py FILE_ADDRESS_TO_SAVE_THE_FINAL_MAPPINGS INPUT_FILE_WITH_USERNAMES


LoadRawDB/
---------------------------------------------
This directory contains scripts for loading and parsing the raw DB data.  Of it the central script LoadRawDB.sh is what should be called.

Example:
./LoadRawDB.sh DATA_DIRECTORY DATASET_SHORT_NAME


ModSocDB/
--------------------------------------------
Symlink to the local ModSocDB library.  

