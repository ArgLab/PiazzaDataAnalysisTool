#!/usr/bin/env python
"""
Classes
:Author: Collin Lynch
:Date: 09/29/2014

Subsidiary class library.
"""

# ----------------------------------------
# External Package Imports.
# ----------------------------------------

from ming.odm import Mapper


# ----------------------------------------
# Load the Classes (add new packages here).
# ----------------------------------------
import Dataset
import User
import Piazza

# ----------------------------------------
# Compile all defined classes.
# ----------------------------------------

Mapper.compile_all()

