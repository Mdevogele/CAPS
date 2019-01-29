#!/usr/bin/env python
"""
Created on Mon Jul 24 23:17:57 2017

@author: devogele
"""

import CAPS
from astropy.io import fits
from photutils import CircularAperture
from photutils import aperture_photometry
from photutils import CircularAnnulus
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from astropy.modeling import models, fitting
import numpy as np 
from numpy import unravel_index
from astropy.stats import biweight_location
from astropy.stats import sigma_clipped_stats
from photutils import make_source_mask


coors = []
global coors
def onclick(event):
    ix, iy = event.xdata, event.ydata
    print 'x = %d, y = %d'%(ix, iy)
        
    coors.append((ix, iy))
#    if len(coords) == 1:
#        fig.figure.canvas.mpl_disconnect(cid)
#        plt.close()


q_u = []
global q_u
def onclick_Stokes(event):
    ix, iy = event.xdata, event.ydata
    print 'x = %f, y = %f'%(ix, iy)
    
    q_u.append(iy)
    print(q_u)


def raise_window(figname=None):
    if figname: plt.figure(figname)
    cfm = plt.get_current_fig_manager()
    cfm.window.activateWindow()
    cfm.window.raise_()

FOLDERS = CAPS.GetFolder(CAPS.Data)  # Get all the folders in the Data folder

Box_Size = 30
SLIT = [(300, 480, 1120, 1600), (528, 720, 1127, 1610), (765, 950, 1145, 1680), (988, 1180,1152,1680 ) ]
radii = range(3,50)

y, x = np.mgrid[:Box_Size*2, :Box_Size*2] 
fit_p = fitting.LevMarLSQFitter()

#ax1 = plt.subplots(141)
#ax2 = plt.subplots(142)
#ax3 = plt.subplots(143)
#ax4 = plt.subplots(144)



C = []
for i in FOLDERS:
    if "Reduced" in i: 
        coords = []
        print(i)
        LIST = CAPS.GetList(i)
        image_data = fits.getdata(LIST[0])
        
        Slit1 = image_data[SLIT[0][0]:SLIT[0][1],SLIT[0][2]:SLIT[0][3]]
        Slit2 = image_data[SLIT[1][0]:SLIT[1][1],SLIT[1][2]:SLIT[1][3]]
        Slit3 = image_data[SLIT[2][0]:SLIT[2][1],SLIT[2][2]:SLIT[2][3]]
        Slit4 = image_data[SLIT[3][0]:SLIT[3][1],SLIT[3][2]:SLIT[3][3]]
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.imshow(Slit1, cmap='gray', norm=LogNorm())
        plt.pause(0.05)
        raise_window()
        plt.pause(0.05)
 #       fig.figure.canvas.manager.window.raise_()
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        raw_input()
        plt.pause(0.05)
        coords = coors
        fig.canvas.mpl_disconnect(cid)
        print(coords)
        print(coors)
        plt.pause(0.05)
        for j in LIST:
            print(coords)
            image_data = fits.getdata(j)
            IM1 = image_data[SLIT[0][0]-Box_Size+int(coords[0][1]):SLIT[0][0]+ Box_Size + int(coords[0][1]) ,SLIT[0][2]-Box_Size + int(coords[0][0]):SLIT[0][2]+ Box_Size + int(coords[0][0])]
            IM2 = image_data[SLIT[1][0]-Box_Size+int(coords[0][1]):SLIT[1][0]+ Box_Size + int(coords[0][1]) ,SLIT[1][2]-Box_Size + int(coords[0][0]):SLIT[1][2]+ Box_Size + int(coords[0][0])]
            IM3 = image_data[SLIT[2][0]-Box_Size+int(coords[0][1]):SLIT[2][0]+ Box_Size + int(coords[0][1]) ,SLIT[2][2]-Box_Size + int(coords[0][0]):SLIT[2][2]+ Box_Size + int(coords[0][0])]
            IM4 = image_data[SLIT[3][0]-Box_Size+int(coords[0][1]):SLIT[3][0]+ Box_Size + int(coords[0][1]) ,SLIT[3][2]-Box_Size + int(coords[0][0]):SLIT[3][2]+ Box_Size + int(coords[0][0])]
            
 #           fig1 = plt.figure()           
 #           plt.imshow(IM1, cmap='gray', norm=LogNorm())
 #           fig2 = plt.figure()
 #           plt.imshow(IM2, cmap='gray', norm=LogNorm())            
            Maximum1 = unravel_index(IM1.argmax(), IM1.shape)
            Maximum2 = unravel_index(IM2.argmax(), IM2.shape)
            Maximum3 = unravel_index(IM3.argmax(), IM3.shape)
            Maximum4 = unravel_index(IM4.argmax(), IM4.shape)
            
            G2D1 = models.Gaussian2D(IM1.max(),Maximum1[0],Maximum1[1],4,4)
            G2D2 = models.Gaussian2D(IM2.max(),Maximum2[0],Maximum2[1],4,4)
            G2D3 = models.Gaussian2D(IM3.max(),Maximum3[0],Maximum3[1],4,4)
            G2D4 = models.Gaussian2D(IM4.max(),Maximum4[0],Maximum4[1],4,4)
            
            p1 = fit_p(G2D1, x, y, IM1)
            p2 = fit_p(G2D2, x, y, IM2)
            p3 = fit_p(G2D3, x, y, IM3)
            p4 = fit_p(G2D4, x, y, IM4)
            
            print(p1)
            print(p2)
            print(p3)
            print(p4)
            
            if p1.x_mean[0] < 0 or p1.x_mean[0] > Box_Size*2:
                print('bla')  
            IM1 = image_data[SLIT[0][0]-Box_Size*2+int(coords[0][1])+int(p1.y_mean[0]):SLIT[0][0]+ int(coords[0][1]) + int(p1.y_mean[0])  ,SLIT[0][2]-Box_Size*2 + int(coords[0][0]) + int(p1.x_mean[0]):SLIT[0][2] + int(coords[0][0]) + int(p1.x_mean[0])]
            IM2 = image_data[SLIT[1][0]-Box_Size*2+int(coords[0][1])+int(p2.y_mean[0]):SLIT[1][0]+ int(coords[0][1]) + int(p2.y_mean[0])  ,SLIT[1][2]-Box_Size*2 + int(coords[0][0]) + int(p2.x_mean[0]):SLIT[1][2] + int(coords[0][0]) + int(p2.x_mean[0])]
            IM3 = image_data[SLIT[2][0]-Box_Size*2+int(coords[0][1])+int(p3.y_mean[0]):SLIT[2][0]+ int(coords[0][1]) + int(p3.y_mean[0])  ,SLIT[2][2]-Box_Size*2 + int(coords[0][0]) + int(p3.x_mean[0]):SLIT[2][2] + int(coords[0][0]) + int(p3.x_mean[0])]
            IM4 = image_data[SLIT[3][0]-Box_Size*2+int(coords[0][1])+int(p4.y_mean[0]):SLIT[3][0]+ int(coords[0][1]) + int(p4.y_mean[0])  ,SLIT[3][2]-Box_Size*2 + int(coords[0][0]) + int(p4.x_mean[0]):SLIT[3][2] + int(coords[0][0]) + int(p4.x_mean[0])]
            
            fig1 = plt.figure()
            ax1 = fig1.add_subplot(141)
            ax2 = fig1.add_subplot(142)
            ax3 = fig1.add_subplot(143)
            ax4 = fig1.add_subplot(144)
            ax1.imshow(IM1, cmap='gray', norm=LogNorm())
            ax2.imshow(IM2, cmap='gray', norm=LogNorm())
            ax3.imshow(IM3, cmap='gray', norm=LogNorm())
            ax4.imshow(IM4, cmap='gray', norm=LogNorm())
                        
            plt.pause(0.05)
            raise_window()
            plt.pause(0.05)          
            raw_input()
            N_C_X1 = coords[0][0]+p1.x_mean[0]-Box_Size
            N_C_Y1 = coords[0][1]+p1.y_mean[0]-Box_Size
            N_C_X2 = coords[0][0]+p2.x_mean[0]-Box_Size
            N_C_Y2 = coords[0][1]+p2.y_mean[0]-Box_Size
            N_C_X3 = coords[0][0]+p3.x_mean[0]-Box_Size
            N_C_Y3 = coords[0][1]+p3.y_mean[0]-Box_Size
            N_C_X4 = coords[0][0]+p4.x_mean[0]-Box_Size
            N_C_Y4 = coords[0][1]+p4.y_mean[0]-Box_Size
            
            coords = [(int(coords[0][0])+int(p1.x_mean[0]-Box_Size), int(coords[0][1]) + int(p1.y_mean[0] -Box_Size))]
            print(coords)
            plt.close()
            plt.close()
            plt.close()
            plt.close()
                        
            positions = [(N_C_X1, N_C_Y1)]
            apertures = [CircularAperture(positions, r=r) for r in radii]
            annulus_apertures = CircularAnnulus(positions, r_in=51., r_out=63.)
            phot_table = aperture_photometry(Slit1, apertures)
            phot_background = aperture_photometry(Slit1, annulus_apertures)
            bkg_mean = phot_background['aperture_sum'] / annulus_apertures.area()
            Int= []
            Area = []
            Int_bkg1 = []
            mask = make_source_mask(Slit1, snr=2, npixels=5, dilate_size=11)
            mean, median, std = sigma_clipped_stats(Slit1, sigma=3.0, mask=mask)
            for num in range(3,50):
                Int.append(phot_table[0][num])
                Area.append(apertures[num-3].area())
                Int_bkg1.append(phot_table[0][num] - apertures[num-3].area()*mean)
            Int_bkg1 = np.array(Int_bkg1)    
            
            positions = [(N_C_X2, N_C_Y2)]
            apertures = [CircularAperture(positions, r=r) for r in radii]
            annulus_apertures = CircularAnnulus(positions, r_in=51., r_out=63.)
            phot_table = aperture_photometry(Slit2, apertures)
            phot_background = aperture_photometry(Slit2, annulus_apertures)
            bkg_mean = phot_background['aperture_sum'] / annulus_apertures.area()
            Int= []
            Area = []
            Int_bkg2 = []
            mask = make_source_mask(Slit2, snr=2, npixels=5, dilate_size=11)
            mean, median, std = sigma_clipped_stats(Slit2, sigma=3.0, mask=mask)
            for num in range(3,50):
                Int.append(phot_table[0][num])
                Area.append(apertures[num-3].area())
                Int_bkg2.append(phot_table[0][num] - apertures[num-3].area()*mean)
            Int_bkg2 = np.array(Int_bkg2)
            
            positions = [(N_C_X3, N_C_Y3)]
            apertures = [CircularAperture(positions, r=r) for r in radii]
            annulus_apertures = CircularAnnulus(positions, r_in=51., r_out=63.)
            phot_table = aperture_photometry(Slit3, apertures)
            phot_background = aperture_photometry(Slit3, annulus_apertures)
            bkg_mean = phot_background['aperture_sum'] / annulus_apertures.area()
            Int= []
            Area = []
            Int_bkg3 = []
            mask = make_source_mask(Slit3, snr=2, npixels=5, dilate_size=11)
            mean, median, std = sigma_clipped_stats(Slit3, sigma=3.0, mask=mask)
            for num in range(3,50):
                Int.append(phot_table[0][num])
                Area.append(apertures[num-3].area())
                Int_bkg3.append(phot_table[0][num] - apertures[num-3].area()*mean)
            Int_bkg3 = np.array(Int_bkg3)
            
            positions = [(N_C_X4, N_C_Y4)]
            apertures = [CircularAperture(positions, r=r) for r in radii]
            annulus_apertures = CircularAnnulus(positions, r_in=51., r_out=63.)
            phot_table = aperture_photometry(Slit4, apertures)
            phot_background = aperture_photometry(Slit4, annulus_apertures)
            bkg_mean = phot_background['aperture_sum'] / annulus_apertures.area()
            Int= []
            Area = []
            Int_bkg4 = []
            mask = make_source_mask(Slit4, snr=2, npixels=5, dilate_size=11)
            mean, median, std = sigma_clipped_stats(Slit4, sigma=3.0, mask=mask)
            for num in range(3,50):
                Int.append(phot_table[0][num])
                Area.append(apertures[num-3].area())
                Int_bkg4.append(phot_table[0][num] - apertures[num-3].area()*mean)
            Int_bkg4 = np.array(Int_bkg4)
            
            
            q = (Int_bkg1-Int_bkg2)/(Int_bkg1+Int_bkg2)
            fig_QU = plt.figure()
            ax_Q = fig_QU.add_subplot(121)            
            ax_Q.plot(radii[8:],q[8:])
#            plt.pause(0.05)
#            cid2 = fig_QU.canvas.mpl_connect('button_press_event', onclick_Stokes)
#            plt.pause(0.05)  
#            raise_window()
#            plt.pause(0.05)  
#            raw_input()
#            fig.figure.canvas.mpl_disconnect(cid2)
#            print(q_u)
#            plt.close()            
            
            u = (Int_bkg4-Int_bkg3)/(Int_bkg3+Int_bkg4)
#            fig_U = plt.figure()
            ax_U = fig_QU.add_subplot(122)            
            plt.plot(radii[8:],u[8:])
            plt.pause(0.05)
            raise_window()
            plt.pause(0.05)
            cid3 = fig_QU.canvas.mpl_connect('button_press_event', onclick_Stokes)            
            plt.pause(0.05)            
            raw_input()
            plt.pause(0.05)
            #fig.canvas.mpl_disconnect(cid3)            
            print(q_u)
            plt.close()
            
            Resh = np.reshape(q_u,(len(q_u)/2,2))
            Median = np.median(Resh,0)
            Error = np.std(Resh,0)/(np.sqrt(len(Resh)))
            FILE = CAPS.ParseFits(j)







from photutils import Background2D, SigmaClip, MedianBackground
sigma_clip = SigmaClip(sigma=3., iters=10)
bkg_estimator = MedianBackground()
bkg = Background2D(Slit1, (120, 120), filter_size=(5, 5), sigma_clip=sigma_clip, bkg_estimator=bkg_estimator)
plt.imshow(bkg.background, origin='lower', cmap='Greys_r')




positions = [(Target_Loc.xs[0], Target_Loc.ys[0])]
apertures = [CircularAperture(positions, r=r) for r in radii]
annulus_apertures = CircularAnnulus(positions, r_in=60., r_out=70.)

phot_table = aperture_photometry(Slit1, apertures)
phot_background = aperture_photometry(Slit1, annulus_apertures)

bkg_mean = phot_background['aperture_sum'] / annulus_apertures.area()

Int= []
Area = []
Int_bkg = []
for i in range(3,50):
    Int.append(phot_table[0][i])
    Area.append(apertures[i-3].area())
    Int_bkg.append(phot_table[0][i] - apertures[i-3].area()*bkg_mean*1.2)

    

positions = [(Target_Loc.xs[0], Target_Loc.ys[0])]
apertures = CircularAperture(positions, r=3.)


fig = plt.imshow(image_data, cmap='gray', norm=LogNorm())
linebuilder = Get_Target()

plt.show()        
