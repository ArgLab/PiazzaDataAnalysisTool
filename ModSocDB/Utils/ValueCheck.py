#!/usr/bin/env python
"""
ValueCheck.py
:Author: Collin F. Lynch
:Date: 03/10/2015

Simple scripts to handle value checking and evaluation.
"""

# ---------------------------------------------------
# Imports.
# ---------------------------------------------------

import ModSocDB


# -----------------------------------------------------
def checkIntStr(Str):
    """
    Given a string that should be an int convert it or if
    it is empty return None
    """
    if (Str == ""): return None
    else: return int(Str)



        
# -----------------------------------------------------
def checkFloatStr(Str):
    """
    Given a string that should be a float convert it or if
    it is empty return None
    """
    if (Str == ""): return None
    else: return float(Str)


# -----------------------------------------------------
def checkNonemptyValStr(Val, ErrOnNone=True):
    """
    Given a string value confirm that it is not ""
    if it is then either return None or throw an error.
    """
    if (Val == ""):
        if (ErrOnNone == True):
            raise ModSocDB.ModSocDBError, \
            "Empty val supplied."
        else: return None
        
    return Val
