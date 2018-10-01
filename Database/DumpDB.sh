#!/usr/bin/env bash
# 
# DumpDB.sh
# Collin F. Lynch
# 1/11/2015
#
# This script provides a basic database dump operation.  When run 
# it takes as an argument the name of an output file.  It will then
# dump the DM_ModSocDB database to the named file so that it can be 
# loaded elsewhere.  
#
# When run it will generate a temporary directory and will dump
# successive collections there as JsonArrays and will then tarball
# the whole thing.  
#
# NOTE:: This is not done as a production backup but as an export 
#   of json objects with the 

# ---------------------------------------------
# Shared Parameters. 
# ---------------------------------------------
DBName="DM_ModSocDB"
DataOutputDir=$1

# ---------------------------------------------
# Process
# ---------------------------------------------


# Make the dump dir and change to it after backing 
# up the current location.
# edit for the output folder name
SaveDir="$DataOutputDir/BarnesCourse/"
mkdir $SaveDir || exit 1
CurrDir=$(pwd)
cd $SaveDir


# Start the save file.
echo "-- Script to create database load for ModSocDB. --" > CreateMysqlTables.sql
echo "-- Collin F. Lynch.  (cflynch@ncsu.edu) --" > CreateMysqlTables.sql
# echo "CREATE DATABASE DM_ModSocDB;" > CreateMysqlTables.sql

echo "# Load this file to load the data." > LoadDatabase.sh
echo "# For questions contact Collin F. Lynch (cflynch@ncsu.edu) or Niki Gitinabard (ngitina@ncsu.edu)" > LoadDatabase.sh

# Dump each of the collections in turn to the database.  
# This will need to be updated as new collections are added. 



for Collection in \
        piazza_content \
	piazza_content_changelog \
	piazza_content_history \
	piazza_content_children \
	piazza_content_children_history \
	piazza_content_children_subchildren \
	datasets \
	users \

do
    echo "Exporting $Collection"
    mongoexport -d $DBName -c $Collection --jsonArray > "$Collection.json";
    echo "mysqlimport --fields-terminated-by=\",\" --ignore-lines=1 --fields-optionally-enclosed-by=\"\\\"\" -u root -p\$1 \$2 --local $Collection.csv" >> LoadDatabase.sh
    
done

# Then generate the sql script for database construction.
echo "Generating Table Scripts."
csvsql -i mysql *.csv >> CreateMysqlTables.sql


#mysqlimport -u root -p --local DM_ModSocDB users.csv


# Tarball up the directory and return.
echo "Building Tarball."
pwd
cd ..

# rename for the archive file name and the folder name
tar -cvjf "BarnesCourse.tar.bz2" BarnesCourse/

cd $CurrDir
