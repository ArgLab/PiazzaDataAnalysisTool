# This file is covered by the LICENSE file in the root of this project.
# @license <https://github.com/ArgLab/PiazzaDataAnalysisTool/LICENSE>
#!/usr/bin/env python
import ModSocDB
"""
This File can test if the Piazza Contents and children have been loaded successfully.
"""


#User = ModSocDB.Classes.PiazzaUser.PiazzaUser(name="a")

#print User

#Set =  ModSocDB.Classes.Piazza.PiazzaUser.PiazzaUser.query.find()
#Set =  ModSocDB.Classes.Piazza.PiazzaContent.RawPiazzaContent.query.find()
#Set =  ModSocDB.Classes.Piazza.PiazzaContent.PiazzaContent.query.find()
Set =  ModSocDB.Classes.Piazza.PiazzaContent_Child.PiazzaContent_Child.query.find()
#Set =  ModSocDB.Classes.Piazza.PiazzaContent_History.PiazzaContent_History.query.find()
#Set =  ModSocDB.Classes.Piazza.PiazzaContent_Child_Subchild.PiazzaContent_Child_Subchild.query.find()
#Set =  ModSocDB.Classes.Piazza.PiazzaContent_ChangeLog.PiazzaContent_ChangeLog.query.find()
#Set = ModSocDB.Classes.Piazza.PiazzaContent_TagGood.PiazzaContent_TagGood.query.find()


for R in Set:
    print R.content

