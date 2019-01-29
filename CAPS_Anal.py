#!/usr/bin/env python

""" CAPS_Anal - Extract best q and u from curve of growth
    v1.0: 2018-05-05, mdevogele@lowell.edu
"""

import matplotlib.pyplot as plt
import argparse
import numpy as np
import operator
from astroquery.jplhorizons import Horizons



def Anal(filenames,Auto,Plot,SS):

    if not SS:
        Target = int(filenames[0].split('-')[0])
    print(Target)
    
    qq = []
    uu = [] 
    Alpha = []
    PlAng = []
    
    JD = []
    for elem in filenames:
        FileInfo = elem.split('_')
        q = []
        u = []
        with open(elem,'r') as f:
            for elem in f.readlines():
                print(elem)
                q.append(float(elem.replace('\n',' ').replace('\t',' ').split()[1]))
                u.append(float(elem.replace('\n',' ').replace('\t',' ').split()[2]))
        q = np.array(q)
        u = np.array(u)

        JD.append(float(elem.replace('\n',' ').replace('\t',' ').split()[0]))
        qq.append(q)
        uu.append(u)
        print(float(elem.replace('\n',' ').replace('\t',' ').split()[0]))
        if not SS:
            obj = Horizons(id=Target, location='010', epochs=float(elem.replace('\n',' ').replace('\t',' ').split()[0]))
            eph = obj.ephemerides()
            Alpha.append(eph['alpha'][0])
            PlAng.append(eph['sunTargetPA'][0])  


#    q = []
#    u = []
#    JD = []
#    for files in filename:
#        f.open(files,'r')
#        for elem in f.readlines().split():
#            q.append(elem[1])
#            u.append(elem[2])
#            JD.append(elem[0])

#    q = np.array(q) 
#    u = np.array(u)
#    JD = np.array(JD)        
#    stokes = np.array(stokes)
#    SS = stokes.reshape(len(stokes)/27,27)      

    if Plot:    
        plt.figure()
        for elem1,elem2 in zip(qq,uu):
            plt.plot(elem1)
            plt.plot(elem2)
        plt.show()
    
    qq = np.array(qq)
    uu = np.array(uu)
    if Auto:
        min_index, min_value = min(enumerate(np.std(qq,axis=0)), key=operator.itemgetter(1))
        print(min_index)
        print('%.5f +- %.5f' % (np.median(qq[:,min_index]), np.std(qq[:,min_index])/np.sqrt(len(qq[:,min_index]))))
        
    
    with open('Best_q','w') as f:
        f.write('%.5f +- %.5f' % (np.median(qq[:,min_index]), np.std(qq[:,min_index])/np.sqrt(len(qq[:,min_index]))))

    
    Q = qq[:,min_index]
    
    
    ff = open('Result','w')


    if Auto:
        min_index, min_value = min(enumerate(np.std(uu,axis=0)), key=operator.itemgetter(1))
        print('%.5f +- %.5f' % (np.median(uu[:,min_index]), np.std(uu[:,min_index])/np.sqrt(len(uu[:,min_index]))))
        
    
    with open('Best_u','w') as f:
        f.write('%.5f +- %.5f' % (np.median(uu[:,min_index]), np.std(uu[:,min_index])/np.sqrt(len(uu[:,min_index]))))

    U = uu[:,min_index]

    Alpha = np.array(Alpha)
    PlAng = np.array(PlAng)

    if not SS:
        for JDD,AA,PL, QQ, UU in zip(JD,Alpha,PlAng,Q,U):
            ff.write('%.5f \t %.2f \t %.2f \t %.5f \t %.5f \n' % (JDD, AA, PL, QQ, UU))
        ff.close()
    else:
        ff.write('%.5f \t %.5f \t %.5f \n' % (np.median(JD), np.median(Q), np.median(U)))
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

    Anal(filenames,Auto,Plot,SS)


    pass