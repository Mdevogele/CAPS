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
    
# import pipeline-specific modules

# only import if Python3 is used
if sys.version_info > (3, 0):
    from past.builtins import execfile


def setup_diagnostics():
    """
    This function sets the current data and diagnostics root
    directories. The setup can and should be re-run in the current working
    directory
    """

    # set up data and diagnostics directories
    dataroot = os.getcwd() + '/'
    diagroot = dataroot + '.diagnostics/'

    # create diagnostics directory
    if not os.path.exists(diagroot):
        os.mkdir(diagroot)

    # define diagnostic website filenames
    index_filename = 'diagnostics.html'
    reg_filename = '.diagnostics/' + 'registration.html'
    cal_filename = '.diagnostics/' + 'calibration.html'
    res_filename = '.diagnostics/' + 'results.html'

    return (dataroot, diagroot, index_filename,
            reg_filename, cal_filename, res_filename)


# set-up data directories

WorkingFolder = '/Users/maximedevogele/Documents/C2PU_Data/CAPS'
BiasFolder = '/Users/maximedevogele/Documents/C2PU_Data/CAPS/Calibs/Master_Bias'
DarkFolder = '/Users/maximedevogele/Documents/C2PU_Data/CAPS/Calibs/Master_Dark'
Data = '/Users/maximedevogele/Documents/C2PU_Data/CAPS/Data'



# suppress runtime and astropy warnings
warnings.simplefilter(action="ignore", category=RuntimeWarning)
warnings.filterwarnings('ignore', category=wcs.FITSFixedWarning)
warnings.filterwarnings('ignore', category=fits.column.VerifyWarning)
warnings.filterwarnings('ignore', category=fits.card.VerifyWarning)
# following warning gets cast by Gaia query: XXX.convert_unit_to(u.deg)
warnings.filterwarnings('ignore', category=np.ma.core.MaskedArrayFutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

# read CAPS pipeline root path from environment variable
rootpath = os.environ.get('CAPSDIR')
if rootpath is None:
    print('ERROR: CAPSDIR variable has not been set')
    sys.exit(0)


# set diagnostics root directory and logging file

# master_diagroot is the directory where the pipeline has been started from
# i.e., potentially, the root directory of all underlying data
# this definition is outside setup_diagnostics(), as it is called only once
diagnostics_summary = os.getcwd() + '/summary.html'
use_diagnostics_summary = False
# set this to True, if you want each
# pp_run process to report into a summary html catalog

# setting up directory paths and logging file
dataroot, diagroot, index_filename, \
    reg_filename, cal_filename, res_filename = setup_diagnostics()

# logging setup
log_formatline = '%(filename)s: %(message)s [%(asctime)s]'
log_level = logging.DEBUG
log_datefmt = '%m/%d/%Y %H:%M:%S'
log_filename = diagroot+'LOG'

# start pp_process_idx counter (if using 'pp_run all')
pp_process_idx = 0

# Translation table to transform target names to file names
# space and / --> _
if sys.version_info > (3, 0):
    target2filename = str.maketrans(' /()', '____')
else:
    import string
    target2filename = string.maketrans(' /()', '____')

# available catalogs

# list of available catalogs
allcatalogs = ['URAT-1', '2MASS', 'SDSS-R9', 'SDSS-R13', 'APASS9', 'GAIA',
               'PANSTARRS', 'TGAS']

# catalog magnitude systems
allcatalogs_magsys = {'URAT-1': 'Vega',
                      '2MASS': 'Vega',
                      'SDSS-R9': 'AB',
                      'SDSS-R13': 'AB',
                      'APASS9': 'Vega',
                      'GAIA': 'Vega',
                      'PANSTARRS': 'AB',
                      'TGAS': 'Vega'}

# ---- pipeline preferences
# (if you don't know what you're doing, better don't mess around here)

# minimum number of reference sources in astrometric reference catalog
# in one of the frames (middle one of sequence); try other catalog
# if number of sources less than this number
min_sources_astrometric_catalog = 10

# how often to run SCAMP using one single catalog?
n_registration_repetitions = 2

# minimum number of reference sources in photometric reference catalog
min_sources_photometric_catalog = 3

# SCAMP contrast criteria for a good fit
scamp_as_contrast_limit = 2.5
scamp_xy_contrast_limit = 2.5

# positional uncertainty (arcsec) for target identification and
# cross-matching used in pp_photometry
pos_epsilon = 0.5

# flux threshold and margin for finding optimum aperture radius in
# pp_photometry
fluxlimit_aprad = 0.7
fluxmargin_aprad = 0.05

# minimum number of stars (integer number) or fraction (float) to use in
# photometric calibration
minstars = 0.5

# solar color margin
# solar color filtering allows for color indices
# [color-_pp_conf.solcol -- color+_pp_conf.solcol]
solcol = 0.2


# photometry flavor ['APER', 'ISOCOR', 'AUTO']
photmode = 'APER'
## don't change this unless you understand what you are doing

