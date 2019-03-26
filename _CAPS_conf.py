#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
configuration file for CAPS pipeline

2018-04-20, mdevogele@lowell.edu
"""
from __future__ import print_function

import os
import sys
import logging
import warnings

try:
    from astropy import wcs
    from astropy.io import fits
except ImportError:
    print('Module astropy not found. Please install with: pip install astropy')
    sys.exit()

try:
    import numpy as np
except ImportError:
    print('Module numpy not found. Please install with: pip install numpy')
    sys.exit()


# set-up data directories

WorkingFolder = '/Users/maximedevogele/Documents/C2PU_Data/CAPS'
BiasFolder = '/Users/maximedevogele/Documents/C2PU_Data/CAPS/Calibs/Master_Bias'
DarkFolder = '/Users/maximedevogele/Documents/C2PU_Data/CAPS/Calibs/Master_Dark'
Data = '/Users/maximedevogele/Documents/C2PU_Data/CAPS/Data'



# read CAPS pipeline root path from environment variable
rootpath = os.environ.get('CAPSDIR')
if rootpath is None:
    print('ERROR: CAPSDIR variable has not been set')
    sys.exit(0)

