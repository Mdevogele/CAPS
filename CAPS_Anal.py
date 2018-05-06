#!/usr/bin/env python

""" CAPS_Anal - Extract best q and u from curve of growth
    v1.0: 2018-05-05, mdevogele@lowell.edu
"""

import matplotlib.pyplot as plt
import argparse
import numpy as np
import operator


def Anal(filenames,Auto,Plot):

    stokes = []
    with open(filenames[0],'r') as f:
        for elem in f.readlines():
            stokes.append(float(elem.replace('\n','')))
            
    stokes = np.array(stokes)
    SS = stokes.reshape(len(stokes)/47,47)      

    if Plot:    
        plt.figure()
        for elem in SS:
            plt.plot(elem)
        plt.show()
    
    if Auto:
        min_index, min_value = min(enumerate(np.std(SS,axis=0)), key=operator.itemgetter(1))
        print('%.5f +- %.5f' % (np.median(SS[:,min_index]), np.std(SS[:,min_index])/np.sqrt(len(SS[:,min_index]))))
    
    with open('Best_' + filenames[0],'w') as f:
        f.write('%.5f +- %.5f' % (np.median(SS[:,min_index]), np.std(SS[:,min_index])/np.sqrt(len(SS[:,min_index]))))


if __name__ == '__main__':
    
    
    # define command line arguments
    parser = argparse.ArgumentParser(description='manual target identification')
    parser.add_argument('-auto', action="store_true")
    parser.add_argument('-plot', action="store_true")
    parser.add_argument('images', help='images to process', nargs='+')
    args = parser.parse_args()
    
    filenames = args.images
    Auto = args.auto
    Plot = args.plot

    Anal(filenames,Auto,Plot)


    pass