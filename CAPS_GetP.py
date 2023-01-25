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
import pandas as pd

def Analyse(Filename,Instrum):
    
    Q_Inst = []
    U_Inst = []

    Ref = np.loadtxt(Instrum)

    Q_Inst = Ref[0][0]
    U_Inst = Ref[1][0]
    
    Q_Inst = np.array(Q_Inst).flatten()
    U_Inst = np.array(U_Inst).flatten()


    T = pd.read_fwf(Filename[0],skiprows=1,names=['JD','Alpha','PLA','q','u'])

    # JD = []
    # Alpha = []
    # PlAng = []
    # Q = []
    # U = []
    
    # with open(Target[0],'r') as f:
    #     for elem in f.readlines():
    #         JD.append(float(elem.replace('\n',' ').replace('\t',' ').split()[0]))
    #         Alpha.append(float(elem.replace('\n',' ').replace('\t',' ').split()[1]))
    #         PlAng.append(float(elem.replace('\n',' ').replace('\t',' ').split()[2]))
    #         Q.append((float(elem.replace('\n',' ').replace('\t',' ').split()[3])+float(U_Inst)))
    #         U.append((float(elem.replace('\n',' ').replace('\t',' ').split()[4])-float(Q_Inst)))        
     

    Q  = np.array(T['q'])
    U  = np.array(T['u'])
    JD = np.array(T['JD'])
    PlAng = np.array(T['PLA'])
    Alpha = np.array(T['Alpha'])
         
    Angle = 45
    
    Pr  = [] # q
    Pr2 = [] # u 
    P_Final = []

        
    f2 = open('Final_Result_Tot','w')
    
    f = open('Final_Result.txt','w')
    f.write('JD          Alpha  Q       Q_Err   U       U_Err   P       P_Err   Pr      Pr_Err  U_Pr    U_Pr_Err  \n')  
    
    for idx ,elem in enumerate(Q):
        Pr.append(np.sin((2*(PlAng[idx]+Angle))*np.pi/180)*(U[idx])+np.cos((2*(PlAng[idx]+Angle))*np.pi/180)*(Q[idx]));
        Pr2.append(-np.sin((2*(PlAng[idx]+Angle))*np.pi/180)*(-Q[idx])+np.cos((2*(PlAng[idx]+Angle))*np.pi/180)*(-U[idx]))
        P_Final.append(np.sqrt(Q[idx]**2+U[idx]**2))
    
    Pr = np.array(Pr)
    Pr2 = np.array(Pr2)
    P_Final = np.array(P_Final)
    JD = np.array(JD)
    Alpha = np.array(Alpha)
    Q = np.array(Q)
    U = np.array(U)
    
    

    filtered_data_Q = sigma_clip(Q, sigma=3)
    filtered_data_U = sigma_clip(U, sigma=3)
    filtered_data_P = sigma_clip(P_Final, sigma=3)
    filtered_data_Pr = sigma_clip(Pr, sigma=3)
    filtered_data_Pr2 = sigma_clip(Pr2, sigma=3)

    
    Mask = filtered_data_Q.mask + filtered_data_U.mask + filtered_data_P.mask + filtered_data_Pr.mask + filtered_data_Pr2.mask


    Mask = np.array(Mask)
    print(Mask)

    PlAng = np.array(PlAng)
    U = np.array(U)
    Q = np.array(Q)

    PlAng_Final = np.median(PlAng[~Mask])
    U_Final = np.median(U[~Mask])
    Q_Final = np.median(Q[~Mask])
    P = np.sqrt(U_Final**2+Q_Final**2)

    Pr_Final = np.sin((2*(PlAng_Final+Angle))*np.pi/180)*(U_Final)+np.cos((2*(PlAng_Final+Angle))*np.pi/180)*(Q_Final)
    Pr_Err = np.std(Pr[~Mask])/np.sqrt(len(Pr[~Mask]))
    P_Err = np.std(P_Final[~Mask])/np.sqrt(len(P_Final[~Mask]))
    Pr2_Err = np.std(Pr2[~Mask])/np.sqrt(len(Pr2[~Mask]))  
    Q_Err = np.std(Q[~Mask])/np.sqrt(len(Q[~Mask]))
    U_Err = np.std(U[~Mask])/np.sqrt(len(U[~Mask]))    
    Pr2_Final = -np.sin((2*(PlAng_Final+Angle))*np.pi/180)*(-Q_Final)+np.cos((2*(PlAng_Final+Angle))*np.pi/180)*(-U_Final)

    To_Write = '{:.5f} {:>5.2f} {:>7.4f} {:>7.4f} {:>7.4f} {:>7.4f} {:>-7.4f} {:>-7.4f} {:>-7.4f} {:>-7.4f} {:>-7.4f} {:>-7.4f}'.format(np.median(JD),
                                                                                       np.median(Alpha),
                                                                                       Q_Final*100,
                                                                                       Q_Err*100,
                                                                                       U_Final*100,
                                                                                       U_Err*100,
                                                                                       P*100,
                                                                                       P_Err*100,
                                                                                       Pr_Final*100,
                                                                                       Pr_Err*100,
                                                                                       Pr2_Final*100,
                                                                                       Pr2_Err*100)
    
    f.write(To_Write)

    print(To_Write)       

    f2.write('JD           Alpha  Q       U       P       Pr        U_Pr   \n')  
    for idx, elem in enumerate(JD):
        f2.write('{:.5f} {:6.2f} {: 7.4f} {: 7.4f} {:7.4f} {: 7.4f} {: 7.4f} \n'.format(elem,
                                                                                            Alpha[idx],
                                                                                            Q[idx]*100,
                                                                                            U[idx]*100,
                                                                                            P_Final[idx]*100,
                                                                                            Pr[idx]*100, 
                                                                                            Pr2[idx]*100))
    f2.close()
    f.close()
    
    
    

if __name__ == '__main__':
    
    
    # define command line arguments
    parser = argparse.ArgumentParser(description='manual target identification')
    parser.add_argument('-Ref', help='',
                        default=3)    
    parser.add_argument('file', help='File with the processed data', nargs='+')
    args = parser.parse_args()
    
    filenames = args.file
    PI = args.Ref

    Analyse(filenames,PI)


    pass