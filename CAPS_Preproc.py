#!/usr/bin/env python

""" NOT_Preproc - Apply the bias to science data
    v1.0: 2018-10-02, mdevogele@lowell.edu        
"""
import argparse

from astropy.io import fits
import numpy as np

def Preproc(filenames,MasterBias,Verbose,Suffix,MasterFlat,OutFolder):

    
    if MasterBias:
        if Verbose: 
            print('Opening master bias file: ' + str(MasterBias))            
        hdulist = fits.open(MasterBias)
        Bias_data = hdulist[0].data  

        
    for idx, elem in enumerate(filenames):
        hdulist = fits.open(elem)
        data = hdulist[0].data


        data = data.astype(int) - Bias_data.astype(int)

        files = elem.split('/')[-1]

        hdulist[0].data = data
        hdulist.writeto(OutFolder + files.split('.')[0] + '_' +  Suffix + '.fits',overwrite = True)
        if Verbose: 
            print('{} \t {} processed'.format(idx+1,elem))


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Preprocessing of the NOT polarimetric files')
#    parser.add_argument('-prefix', help='data prefix',
#                        default=None)
    
    parser.add_argument('-o',
                        help='Folder where to write the files',
                        default='./')
    parser.add_argument('-s',
                        help='Suffix to add to processed files',
                        default='Procc')
    parser.add_argument('-b',
                        help='Name of the master bias to use \n || Default to None if no bias',
                        default=None)
    parser.add_argument('-v',
                        help='Increase verbosity',
                        action="store_true")    
    parser.add_argument('images', help='images to process or \'all\'',
                        nargs='+')
    
    parser.add_argument('-f',
                        help='Name of the master flat to use \n || || Default to None if no flat',
                        default=None)    

    args = parser.parse_args()
    Suffix = args.s
    MasterBias = args.b
    Verbose = args.v
    filenames = args.images  
    MasterFlat = args.f
    OutFolder = args.o

    
    print(filenames)
    
    Preproc(filenames,MasterBias,Verbose,Suffix,MasterFlat,OutFolder)
    pass