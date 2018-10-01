#!/usr/bin/env python
"""
ModSocDBError.py
:Author: Collin Lynch
:Date: 09/29/2014

Basic error class for the database.
"""

# --------------------------------------------
# imports.
# --------------------------------------------
import exceptions


# --------------------------------------------
# Classes.
# --------------------------------------------

class ModSocDBError(exceptions.RuntimeError):
    """
    Basic error class for the ModSocDB.
    """

    def __init__(self, value=None):
        """
        Initialize the error.
        """
        self.value = value

    def __str__(self):
        return repr(self.value)
