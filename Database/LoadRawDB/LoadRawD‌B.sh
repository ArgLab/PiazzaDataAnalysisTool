#!/usr/bin/env bash
# LoadRawDB.sh
# Collin F. Lynch
# 09/29/2014
#
# This code manages loading of the raw data files into the database.  It performs
# direct bash calls for the loading of the Piazza data and can call relevant 
# python scripts for the installation of the other data as needed. This 
# is only for use in setting up the database initially. To restore from a backup
# directory the LoadDBDump.sh script should be used.  
#
# This takes as an argument a root directory where the RawData is stored and also the short name of the dataset.  These
# arguments will be passed to all subsidiary items.  
#
# NOTE:: This does not clear the existing database before being called.  

# ---------------------------------------------
# Shared Parameters. 
# ---------------------------------------------
DBName="DM_ModSocDB"
RawDataDir=$1
dataset_name=$2


# ------------------------------------------------------
# Load Dataset Description.
# ------------------------------------------------------
DescFile="$RawDataDir/Dataset/Dataset.desc"

echo "----------------------------------------------"
echo "Loading Dataset Description"

python LoadDescriptionFile.py $DescFile  || exit 0


# ------------------------------------------------------
# Load Piazza Data.
# Per Mike's test these are json objects form a mongodb
# project and thus can be loaded directly.  
# ------------------------------------------------------
echo "--------------------------------------------"
echo "Adding Piazza Data."

PiazzaDir="$RawDataDir/PiazzaData"


RawPiazzaDir="$PiazzaDir/"

# Load the users.
mongoimport --db $DBName \
--collection piazza_users \
--file "$RawPiazzaDir/users.json" \
--jsonArray \
--stopOnError \
-vvv \
|| exit 1
   

# Replace the 'd-bucket' name with d_bucket in the json
# file.  
rm -f "$RawPiazzaDir/class_content_clean.json"  || exit 1

sed s/d-bucket/d_bucket/g $RawPiazzaDir/class_content.json > $RawPiazzaDir/class_content_clean.json  || exit 1

mongoimport --db $DBName \
--collection raw_piazza_content \
--file "$RawPiazzaDir/class_content_clean.json" \
--jsonArray \
--stopOnError \
-vvv \
|| exit 1



# And drop the duplicates.
python DropDuplicates.py "$dataset_name" || exit 1


# ------------------------------------------------------
# Migrate Content from raw form.
# ------------------------------------------------------
echo "Migrating Raw Content."
python MigrateRawContent.py "$dataset_name" "$RawDataDir" || exit 1

python CleanData.py "$dataset_name" "$RawDataDir/users_data.csv" || exit 1

