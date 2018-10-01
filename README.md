README.txt
Collin Lynch
9/21/2014

Overview
==================================================

This repository contains code for the storage and analysis of the Barnes course data for the ModSoc repository.  It should *not* contain data itself but only code to load and manipulate said data.  

This code will be run as a database-backed analysis project.  Thus there will be a sinle central database (initialized in the Database directory) and all of the Anonymization and Analysis code should interact with that database.  The database itself will be stored as a MongoDB database with Anonymization being accomplished by production of a separate anonymous database.  Most users will not need to generate the database from scratch but should simply install an anonymous database from the separate data store (TBD).  

For the sake of code sharing most of the code that touches the database should be done with Bash, Python, PyMongo, and Ming the Merciless unless another ORM is preferred.  Database initialization will be accomplished via shell scripts and a separate script will be built for database loading. 


Requirements
================================================
This library depends upon the following packages:

   * Python 2.7 or later (not yet compatable with Python 3)
     The existing libraries are compatible with Python 2.7 you can download it from www.python.org You should not try it with Python 3 as the libraries do not support it.  Tutorial: https://docs.python.org/2.7/

   * MongoDB:
     We use Mongodb to provide the underlying support database for our library.  Mongodb can be found at: https://www.mongodb.org/ and can be installed on any OS.  Installation instructions can be found at: http://docs.mongodb.org/manual/installation/  You should not need to write detailed mongo data for this project only use our wrapper scripts.  

   * Pymongo 2.6.3 or later.
     PyMongo is the basic python library wrapper for the MongoDB.  It may be installed with your distribution, if not then you can find it here: https://pypi.python.org/pypi/pymongo.  As with Mongodb use of PyMongo is wrapped up by our library and thus should not need to be dealt with directly.
     
   * Ming ODB 0.5.0 for Python and Mongodb.
     Ming is an Object-Relational database wrapper for Mongdb based upon PyMongo.  We use it to provide relatonal support for the library.  If it is not installed with your Python distribution then you can find it here: https://pypi.python.org/pypi/Ming along with some tutorials for its use.  Example information can also be found in the ModSoc library itself.
     
   * NLTK (for Anonymization) 2.0 or later.
     The NLTK is a natural language toolkit for python.  It is used to provide basic NLP support and can be installed on most platforms instructions and installation access can be found here: http://www.nltk.org/

   * name_tools 0.1.3 for Python.
     Name_tools is a basic python library for name recognition and parsing.  It is required for some aspects of the data processing.  You will need to install it in order to run the library and you can find it here: https://pypi.python.org/pypi/name_tools/0.1.2 

   * pyexcel >= 0.2.5
     & pyexcel-xlsx >= 0.2.2
     These are excel manipulation libraries that are used in the transaction code.	
     https://pypi.python.org/pypi/pyexcel
     https://pypi.python.org/pypi/pyexcel-xlsx

   * python-igraph
      It's used in some analysis parts for creating graphs, can be installed by pip
      Also needs "libigraph0-dev" installed before igraph can be installed (can be found via apt-get)

   * statistics(pip), scipy(pip), numpy(pip), python-cairo(apt), libcairo2-dev(apt) are needed for the social network analysis.

   * unicodecsv



Windows
================================================
The codebase uses python and bash scripts to manage much of the functionality including loading and extraction of data.  Therefore the following steps are advised for windows users:
Steps to get Code and Data ready on Windows machine:

- For sh scripts such as Database/LoadDBDumps.sh this can be done via the "git shell" or "git bash" commands.
- In order for the code to function the MongoDB bin folder must be added to the system path.


Contents:
================================================
The repository is organized as follows:


Database/
---------------------------------------------
This directory contains scripts to initialize and update the database as well as code to process the raw datafiles.  The three data sources will be listed separately under this directory.  


Stats/
--------------------------------------------
Location for statistical and analysis scripts.  Such code should be designed to accumulate data tables or other relevant fields.  


Scripts/
--------------------------------------------
Miscellaneous database access and evaluation scripts used to peek at content or make other checks but no major updates.  


ModSocDB/
---------------------------------------------
The ModSocDB python database wrapper with utility code.  


=============================================
Helpful Notes:

- This must be done if you installed/updated pip libraries or a library is already installed and you cannot access it.
sudo chmod -R ugo+rX /lib/python2.7/site-packages/

- If ModSocDB is not sim-linked to the directory you work at, run export PYTHONPATH='.' in a directory ModSocDB is present in



