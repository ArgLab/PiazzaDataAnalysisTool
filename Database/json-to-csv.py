# This file is covered by the LICENSE file in the root of this project.
# @license <https://github.com/ArgLab/PiazzaDataAnalysisTool/LICENSE>
#!/usr/bin/env python2.7
"""
Json to CSV converter (simple)
Collin F. Lynch
11/02/2015

Simple code that opens a json file and named csv file and iterates 
over it to dump the items out.  It can deal with at most one level
of nesting and for such things it simply prefixes the column names
when dumping.
"""


# ===============================================================
# Imports
# ===============================================================
import sys
#import ujson as json
import unicodecsv
#import csv
import json


# ===============================================================
# Code
# ==============================================================

def main(JSONFileName, CSVFileName):
    """
    Given the filenames open the JSON file and read it into memory.  We 
    then process the files to see what happens.  
    """

    # Read in the JSON File and dump the results.
    In = open(JSONFileName)
    Data = json.load(In)
    In.close()

    # Now assemble the flattened data and keys.
    (FlatData, Keys) = flattenData(Data)

    #print Data[0].keys()
    #print FlatData[0]
    #print Keys

    # Write out the designated CSV File.
    Out = open(CSVFileName, "w")
    Writer = unicodecsv.DictWriter(Out, Keys)
    Writer.writeheader()
    Writer.writerows(FlatData)
    Out.close()
    
    
def flattenData(Data):
    """
    Iterate over the data.  For any data item that is a dict convert the 
    elements in it to top-level elements in the new data list and return.
    """

    ResultData = []
    KeyList = []

    # Assuming that the data is a list of dicts iterate
    # over them and go from there.  
    for Element in Data:

        # Perform the recursive flatten of the item.
        FlatElement = flattenElement(Element)
        ResultData.append(FlatElement)
        
        # Iterate over the keys in the item and add
        # them to the KeyList.
        for K in FlatElement.keys():
            if (K not in KeyList):
                KeyList.append(K)

    return (ResultData, KeyList)


def flattenElement(EltDict):
    """
    Given an element dict iterate over them and then 
    compile the flattened form.  
    """

    # Setup storage for the new flat dict that will be returned.
    ResultDict = {}

    # For each key in the dict we check its type.  In the event
    # of a dict we handle a recursive process of generating a
    # flattened sub-dict then add it in.  Else we just add it.
    for Key in EltDict.keys():
        Val = EltDict[Key]

        # If the value supplied is a dict then go through the
        # process of flatteng it recursively and then adding
        # sub-key elements.  
        if (isinstance(Val, dict)):
            NewDict = flattenElement(Val)
            for SubKey in NewDict:
                NewKey = "%s_%s" % (Key, SubKey) 

                if (ResultDict.has_key(NewKey)):
                    raise RuntimeError("Known key: %s" % (NewKey))
                else: ResultDict[NewKey] = NewDict[SubKey]

        # All other cases will simply be added in.  This will also
        # swap out instances of $oid to just oid
        else:
            if (ResultDict.has_key(Key)):
                raise RuntimeError("Known key: %s" % (Key))
            elif (Key == "$oid"):
                ResultDict["oid"] = Val
            else: ResultDict[Key] = Val

    # And return the results.
    #print ResultDict
    return ResultDict
    


# ===============================================================
# Main Loop
# ==============================================================

if __name__ == "__main__":

    JSONName = sys.argv[1]
    CSVName  = sys.argv[2]

    main(JSONName, CSVName)
