#!/usr/bin/env bash
# LoadDBDumps.sh
# Collin F. Lynch
# 1/11/2014
#
# This code is used to load backed-up database dumps 
# into MongoDB from a backup directory.  When called 
# it will read through the dumps loading each one into
# a named collection.  
#
# This assumes that the tarball has been unpacked and 
# that the user has access to it.  

# ---------------------------------------------
# Shared Parameters. 
# ---------------------------------------------
DBName="DM_ModSocDB"
DataDir=$1


# ---------------------------------------------
# Basic Code.
# ---------------------------------------------

CurrDir=$(pwd)

cd $DataDir

for File in $(ls *.json) 
do
    echo ""
    echo "Loading: $File"
    CollectionName=$(basename $File .json)
    mongoimport --db $DBName \
	--collection $CollectionName \
	--file $File \
	--jsonArray
done

cd $CurrDir
