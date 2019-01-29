#!/usr/bin/env python

""" CAPS_Bias - Function to create bias for CAPS polarimetric data
    v1.0: 2018-10-02, mdevogele@lowell.edu
"""

import argparse

import numpy as np

from astropy.io import fits


#def Median(Bias):
#    Master = np.median(Bias,axis=0)
#    print('Computed median')
#    return Master
#
#def Mean(Bias):
#    Master = np.mean(Bias,axis=0)
#    print('Computed mean')    
#    return Master




class Result(object):
    def Indiv_to_Master(self, method, Bias):
        Master = getattr(self, method, lambda x: getattr(self, 'Default')(Bias))(Bias)
        # Call the method as we return it
        return Master
 
    def Median(self,Bias):
        Master = np.median(Bias,axis=0)
        return Master
 
    def Mean(self,Bias):
        Master = np.mean(Bias,axis=0)
        return Master

    def Default(self, Bias):
        Master = np.median(Bias,axis=0)
        print("Invalid method, use of the median as default")
        return Master 


def Create_Bias(filenames,MasterName,Verbose,Method,Bin):
    
    
    if Verbose:
        print('Beginning bias processing')
        print('Processing files:')
        print('index \t filename')
        for idx,elem in enumerate(filenames):
            print('{} \t {}'.format(idx+1,elem))
        print('Creating the master bias')
        
        
    Bias = []
    for image in filenames:
        hdulist = fits.open(image)
        data = hdulist[0].data
        Bias.append(data)
    
    Res = Result()
    MasterBias = Res.Indiv_to_Master(Method, Bias)
    hdulist[0].data = MasterBias
    hdulist.writeto(MasterName, overwrite = True)
    hdulist.close()     
        

    if Verbose:
        print('Master bias save to {}'.format(MasterName))
        hdulist = fits.open(MasterName)
        data = hdulist[0].data
        print('Statistics of the Master bias')
        print('Mean: {} \t Median: {} \t std: {}'.format(np.mean(data), np.median(data), np.std(data)))
        print('End of bias processing')
        hdulist.close()
        
    




if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Processing and creation of master bias')
    parser.add_argument('-v',
                        help='Increase verbosity',
                        action="store_true")    
    parser.add_argument('-o',
                        help='Name of the master bias file',
                        default='MasterBias.fits')
    parser.add_argument('-m',
                        help='Method to use to compute the master bias: Mean, Median',
                        default='Median') 
    
    parser.add_argument('-bin',
                        help='Binning factor',
                        default=1) 
    parser.add_argument('images', help='images to process or \'all\'',
                        nargs='+')

    args = parser.parse_args()

    Verbose = args.v
    MasterName = args.o
    filenames = args.images    
    Method = args.m 
    Bin = int(args.bin) 

    Create_Bias(filenames,MasterName,Verbose,Method,Bin)
    pass