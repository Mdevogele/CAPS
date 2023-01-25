#!/usr/bin/env python

""" CAPS_Anal - Extract best q and u from curve of growth
    v1.0: 2018-05-05, mdevogele@lowell.edu
    v1.1: 2023-01-25, mdevogele@ucf.edu
"""

import matplotlib.pyplot as plt
import argparse
import numpy as np
import operator
from astroquery.jplhorizons import Horizons
import sys



def Anal(filenames,Auto,Plot,SS,Target):

    if not SS and not Target:
        Target = int(filenames[0].split('-')[0])
        if isinstance(Target,int):
            print('The target is: {:d}'.format(Target))
        else:
            print('The target is: {:s}'.format(Target))
    elif Target:
        Target = Target
    
    ## Initiate some variable
    qq = []
    uu = [] 
    Alpha = []
    PlAng = []
    JD = []

    for elem in filenames:
        q = []
        u = []
        with open(elem,'r') as f:
            for elem in f.readlines():
                q.append(float(elem.replace('\n',' ').replace('\t',' ').split()[1]))
                u.append(float(elem.replace('\n',' ').replace('\t',' ').split()[2]))
        q = np.array(q)
        u = np.array(u)

        JD.append(float(elem.replace('\n',' ').replace('\t',' ').split()[0]))
        qq.append(q)
        uu.append(u)
        # print(float(elem.replace('\n',' ').replace('\t',' ').split()[0]))
        if not SS:
            obj = Horizons(id=Target, location='010', epochs=float(elem.replace('\n',' ').replace('\t',' ').split()[0]))
            ## Try to get the ephemeris
            try:
                eph = obj.ephemerides()
            except ValueError:
                ## Sometime if a previous attempt to get the ephemeris failed
                ## and that attempt was saved into the cache we need to ignore the cache files
                eph = obj.ephemerides(cache=False)

            ## Store the phase angle and the suntargetPA angle
            Alpha.append(eph['alpha'][0])
            PlAng.append(eph['sunTargetPA'][0])  


  



    if Plot:    
        plt.figure()
        for elem1,elem2 in zip(qq,uu):

            plt.plot(np.linspace(0,39,40),np.median(qq,axis=0),linewidth = 5,color = 'r')
            plt.fill_between(np.linspace(0,39,40),np.median(qq,axis=0)-np.std(qq,axis=0),np.median(qq,axis=0)+np.std(qq,axis=0),alpha = 0.3)
            plt.plot(np.median(uu,axis=0),linewidth = 5,color = 'r')
            plt.fill_between(np.linspace(0,39,40),np.median(uu,axis=0)-np.std(uu,axis=0),np.median(uu,axis=0)+np.std(uu,axis=0),alpha = 0.3)

        plt.show()

    # Here q and u are reversed. q should be the value around 3-4% and u should be the small one. 
    # The values are corrected for the print statements so q is printed first then u    

    qq = np.array(qq)
    uu = np.array(uu)

    if Auto:
        min_index, min_value = min(enumerate(np.std(uu,axis=0)/np.abs(np.median(uu,axis=0))), key=operator.itemgetter(1))
        print('%.5f +- %.5f' % (np.median(uu[:,min_index]), np.std(uu[:,min_index])/np.sqrt(len(uu[:,min_index]))))
    else:
        min_index = int(input("What aperture do you want to use?: "))
        print('q = %.5f +- %.5f' % (np.median(uu[:,min_index]), np.std(uu[:,min_index])/np.sqrt(len(uu[:,min_index]))))
    
    with open('Best_q','w') as f:
        f.write('%.5f +- %.5f' % (np.median(uu[:,min_index]), np.std(uu[:,min_index])/np.sqrt(len(uu[:,min_index]))))

    U = uu[:,min_index]
    
    min_index_u = min_index


    if Auto:
        min_index, min_value = min(enumerate(np.std(qq,axis=0)/np.abs(np.median(qq,axis=0))), key=operator.itemgetter(1))
        print(min_index)
        print('%.5f +- %.5f' % (np.median(qq[:,min_index]), np.std(qq[:,min_index])/np.sqrt(len(qq[:,min_index]))))
    else:
        print('u = %.5f +- %.5f' % (-np.median(qq[:,min_index]), np.std(qq[:,min_index])/np.sqrt(len(qq[:,min_index]))))
        
    
    with open('Best_u','w') as f:
        f.write('%.5f +- %.5f' % (-np.median(qq[:,min_index]), np.std(qq[:,min_index])/np.sqrt(len(qq[:,min_index]))))

    
    Q = qq[:,min_index]
    
    min_index_q = min_index

    Alpha = np.array(Alpha)
    PlAng = np.array(PlAng)

    ff = open('Result','w')

    if not SS:
        ff.write('JD           Alpha  PL angle     u       q \n')
        for JDD,AA,PL, QQ, UU in zip(JD,Alpha,PlAng,Q,U):
            ff.write('{:.5f} {:6.2f} {:6.2f} {: 9.5f} {: 9.5f} \n'.format(JDD, AA, PL, QQ, UU))
            # ff.write('%.5f \t %.2f \t %.2f \t %.5f \t %.5f \n' % (JDD, AA, PL, QQ, UU))
        ff.close()
    else:
        ff.write('%.5f \t %.5f \n' % (np.median(U), -np.median(Q)))
        ff.close()


if __name__ == '__main__':
    
    
    # define command line arguments
    parser = argparse.ArgumentParser(description='manual target identification')
    parser.add_argument('-auto', action="store_true")
    parser.add_argument('-plot', action="store_true")
    parser.add_argument('-SS', action="store_true")

    parser.add_argument('-object', help='Name of the target for retrieving alpha and scaterring plane angle values',
                        default=False)
    parser.add_argument('images', help='images to process', nargs='+')

    
    args = parser.parse_args()
    
    Auto = args.auto
    Plot = args.plot
    Target = args.object
    filenames = args.images
    SS = args.SS

    Anal(filenames,Auto,Plot,SS,Target)


    pass