#!/usr/bin/env python

""" CAPS_GetPola - Convert individual observation to P taking into account ref stars 
    v1.0: 2018-10-05, mdevogele@lowell.edu
"""

import matplotlib.pyplot as plt
import argparse
import numpy as np
import operator
from scipy.optimize import curve_fit
from astroquery.jplhorizons import Horizons
from astropy.stats import sigma_clip


def Analyse(Target,Instrum):
    
    Q_Inst = []
    U_Inst = []

    with open(Instrum,'r') as f:
        for elem in f.readlines():
            Q_Inst.append(float(elem.replace('\n',' ').replace('\t',' ').split()[0]))
            U_Inst.append(float(elem.replace('\n',' ').replace('\t',' ').split()[1]))
    
    
    Q_Inst = np.array(Q_Inst).flatten()
    U_Inst = np.array(U_Inst).flatten()

    JD = []
    Alpha = []
    PlAng = []
    Q = []
    U = []
    
    with open(Target[0],'r') as f:
        for elem in f.readlines():
            JD.append(float(elem.replace('\n',' ').replace('\t',' ').split()[0]))
            Alpha.append(float(elem.replace('\n',' ').replace('\t',' ').split()[1]))
            PlAng.append(float(elem.replace('\n',' ').replace('\t',' ').split()[2]))
            Q.append((float(elem.replace('\n',' ').replace('\t',' ').split()[3])+float(U_Inst)))
            U.append((float(elem.replace('\n',' ').replace('\t',' ').split()[4])-float(Q_Inst)))        
     
         
    Angle = 45
    
    Pr  = []
    Pr2 = [] 
    P_Final = []

        
    
    
    f2 = open('Final_Result_Tot','w')
    
    f = open('Final_Result.txt','w')
    f.write('JD \t Alpha \t Q \t U \t P \t Pr \t Err \n')    
    
    for idx ,elem in enumerate(Q):
        Pr.append(np.sin((2*(PlAng[idx]+Angle))*np.pi/180)*(U[idx])+np.cos((2*(PlAng[idx]+Angle))*np.pi/180)*(Q[idx]));
        Pr2.append(-np.sin((2*(PlAng[idx]+Angle))*np.pi/180)*(-Q[idx])+np.cos((2*(PlAng[idx]+Angle))*np.pi/180)*(-U[idx]))
        P_Final.append(np.sqrt(Q[idx]**2+U[idx]**2))
    
    Pr = np.array(Pr)
    P_Final = np.array(P_Final)
    JD = np.array(JD)
    Alpha = np.array(Alpha)
    Q = np.array(Q)
    U = np.array(U)
    
    

    filtered_data = sigma_clip(Pr, sigma=3)

    
    print(Pr[~filtered_data.mask])
    
    Results = '{:.5f}\t{:.2f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\n'.format(np.nanmedian(JD[~filtered_data.mask]),
                                    np.nanmedian(Alpha[~filtered_data.mask]),
                                    np.nanmedian(Q[~filtered_data.mask]),
                                    np.nanmedian(U[~filtered_data.mask]),
                                    np.nanmedian(P_Final[~filtered_data.mask]),
                                    np.nanmedian(Pr[~filtered_data.mask]),
                                    np.nanstd(Pr[~filtered_data.mask])/np.sqrt(len(Pr[~filtered_data.mask])))
    
    # f.write(str(np.median(JD[~filtered_data.mask])) + '\t' + str(np.median(Alpha[~filtered_data.mask])) + '\t' + str(np.median(Q[~filtered_data.mask])) + '\t' + str(np.median(U[filtered_data.mask])) + '\t' + str(np.median(P_Final[~filtered_data.mask])) + '\t' + str(np.median(Pr[~filtered_data.mask])) + '\t' + str(np.std(Pr[~filtered_data.mask])/np.sqrt(len(Pr[~filtered_data.mask]))) + '\n')
    f.write(Results)

    print(Results)       

    for idx, elem in enumerate(JD):
        f2.write(str(elem) + '\t' + str(Alpha[idx]) + '\t' + str(Q[idx]) + '\t' + str(U[idx]) + '\t' + str(P_Final[idx]) + '\t' + str(Pr[idx]) + '\n')
        
    f2.close()
    f.close()
    
    
    

if __name__ == '__main__':
    
    
    # define command line arguments
    parser = argparse.ArgumentParser(description='manual target identification')
    parser.add_argument('-Ref', help='',
                        default=3)    
    parser.add_argument('images', help='images to process', nargs='+')
    args = parser.parse_args()
    
    filenames = args.images
    PI = args.Ref


    Analyse(filenames,PI)


    pass