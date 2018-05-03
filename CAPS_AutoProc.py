#!/usr/bin/env python

""" CAPS_AutoProc - Automatically apply dark to CAPS data
    v1.0: 2018-04-20, mdevogele@lowell.edu
"""




import os 
import sys
#sys.path.append('/Users/tanga/Documents/Astro_Data/C2PU_Data')
import CAPS
import glob
from astropy.io import fits
import _CAPS_conf

import argparse

def ApplyDark(Verbose):



    WorkingFolder = _CAPS_conf.WorkingFolder
    BiasFolder = _CAPS_conf.BiasFolder
    DarkFolder = _CAPS_conf.DarkFolder
    Data = _CAPS_conf.Data
    
    
    # Check the dark file already existing and creating a list of DARK
    
    LIST_DARK = CAPS.GetList(DarkFolder)
    
    
    FOLDERS = CAPS.GetFolder(Data)  # Get all the folders in the Data folder
    
    for i in FOLDERS:                                       # loop in all the folders
        print(i)
        if not "Reduced" in i:
            I = CAPS.ParseFolder(i)                             # Parse the folders
            Instrument = I.get('Instrument')                    # Get the instrument used
            if Instrument == 'CAPS':                            # go inside the loop if CAPS was used 
                Type = I.get('Object')                          # Get the acquisition type
                if Type == 'DARK':                                # go inide the loop if the folder is of DARK type
                    LIST = CAPS.GetList(i)
                    for k in LIST:
                        K = CAPS.ParseFits(k)
                        Temp = CAPS.GetCCDTemp(k)
                        Day = CAPS.ParseTime(K['Time'])
                        FILE_NAME = 'DARK_QSI_' + str(K['ExpTime']) + 's' + '_' + Day['Year'] +'-'+Day['Month'] + '-' + Day['Day'] + '_' + str(Temp) + 'Deg'
                        FILE_NAME_TAMP =  FILE_NAME +'_TAMP'                
                        PATH_TXT =  DarkFolder + FILE_NAME_TAMP               
                        if os.path.isfile(PATH_TXT) == False:
                            f = open(PATH_TXT, 'w')
                            f.close
                        f = open(PATH_TXT,'a')
                        f.write(k)
                        f.write('\n')
                        f.close
                else:
                    LIST = CAPS.GetList(i)
                    K = CAPS.ParseFits(LIST[0])
                    if K['Type'] == 'SC':
                        for k in LIST:
                            K = CAPS.ParseFits(k)
                            Temp = CAPS.GetCCDTemp(k)
                            Day = CAPS.ParseTime(K['Time'])
                            FILE_NAME = 'DARK_QSI_' + str(K['ExpTime']) + 's' + '_' + '*' + '_' + str(Temp) + 'Deg.fits'
                            MM_DARK = glob.glob(DarkFolder + FILE_NAME)
         #                   MM_DARK_Split = MM_DARK[0].split('/')
                            if len(MM_DARK) > 0: 
        #                    PATH_TXT =  DarkFolder + FILE_NAME_TAMP 
                                FILE_NAME_TAMP =  MM_DARK[0] +'_TAMPPROC'
        #                    PATH_TXT =  DarkFolder + FILE_NAME_TAMP 
                                if os.path.isfile(FILE_NAME_TAMP) == False:
                                    f = open(FILE_NAME_TAMP, 'w')
                                    f.close
                                f = open(FILE_NAME_TAMP,'a')
                                f.write(k)
                                f.write('\n')
                                f.close
    
    
                        
    
    DARKS_LIST = glob.glob(DarkFolder + '*_TAMP')              
    for i in DARKS_LIST:
        with open(i) as f:
            lines = f.read().splitlines()
        if os.path.isfile(i[:-5] +'.fits') == False:
            MDark = CAPS.MakeDark(lines)
            hdu = fits.PrimaryHDU(MDark)
            hdu.writeto(i[:-5] +'.fits')
        os.remove(i)
    
    
    Process_LIST = glob.glob(DarkFolder + '*_TAMPPROC')
    for i in Process_LIST:
        with open(i) as f:
            lines = f.read().splitlines()
        print(lines)    
        CAPS.ApplyPreProcCAPS(lines,i[:-9])
        os.remove(i)
    


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Apply dark to CAPS data')

    parser.add_argument('-v',
                        help='Increase verbosity',
                        action="store_true")    

    args = parser.parse_args()

    Verbose = args.v


    
    
    # call run_the_pipeline only on filenames
    ApplyDark(Verbose)
    pass


