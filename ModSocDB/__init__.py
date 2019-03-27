# This file is covered by the LICENSE file in the root of this project.
# @license <https://github.com/ArgLab/PiazzaDataAnalysisTool/blob/master/LICENSE>
#!/usr/bin/env python
"""
ModSocDB Package.

 ModSocDB/__init__.py
 :Author: Collin Lynch
 :Date: 09/29/2014

This library provides a Ming-based wrapper on the DM_ModSocDB database.  As presently structured it supports the insertion of data from the Barnes 2014 course and provides access to the code to evaluate it.  It may be modified in future to include other components.

Most of the library core resides in the Classes/ subpackage.  This package should contain one module per object in the library with each object being linked to a raw data source of some type.  For more complex data sources a sub-mpodule of Classes is preferred.  the Classes/Piazza/ sub-module provides classes designed to deal with Piazza data.  Similar tactics should be used for the Moodle data and other sources.

In general the preference is for exposed data with objects having limited complexity and for objects in a contains relationship to be described separately and linked to one-another via relationships as is done in the Piazza sub-package.  This is preferable for analysis purposes as it makes it easier to write data-specific analysis functions rather than loading the code onto a single complex instance with many internal classes.  While this runs counter to the standard MongoDB preference it is easier for shared analysis code.

Additional special-purpose subpackages should be added as needed for common code tasks such as NLP processing (see NLP/).
"""

from ModSocDBError import *
from ModSocDB import *

import Classes
import NLP

import Utils
