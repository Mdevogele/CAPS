# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 01:29:59 2017

@author: devogele
"""

from astropy.io import fits
import numpy as np
import os
import re 
import scipy 
import sys

import _CAPS_conf


WorkingFolder = _CAPS_conf.WorkingFolder
BiasFolder = _CAPS_conf.BiasFolder
DarkFolder = _CAPS_conf.DarkFolder
Data = _CAPS_conf.Data




def Check_Proc(hdulist,Exit = True):

    # check if the file has been pre-processed
    # if it is, the function return True
    # if it is not, the function can aboard the pipeline or return False 
    # to ignore the non un processed file   
    
    Proc = hdulist[0].header['PROCTYPE']
    
    if 'RAW' in Proc:
        if Exit:
            print('The files that you want to process have not been pre-processed')
            sys.exit()
        else:
            return False
    else:
        return True



def Check_CAPS(hdulist,Exit = True ):

    # check if the file is a ToPol data
    # if it is, the function return True
    # if it is not, the function can aboard the pipeline or return False 
    # to ignore the non ToPol file in the processing
    
    Instru = hdulist[0].header['INSTRUME']
    
    if 'CAPS' not in Instru:
        if Exit:
            print('The files that you want to process are not CAPS data')
            sys.exit()
        else:
            return False
    else:
        return True


def Gauss_fit(x,a,x0,sigma,y0):
    return (a/(sigma*scipy.sqrt(2*3.14))*scipy.exp(-(x-x0)**2/(2*sigma**2)))+y0



def CheckCAPSData(HDULIST):
    if 'CAPS' in HDULIST[0].header['INSTRUME']:
        print('bla')
        
    

def GetCCDTemp(name):
    hdulist = fits.open(name)
    Temp = hdulist[0].header['TCAMCCD']

    return  Temp

def GetFolder(ToWalk):

    TargetList1 = []
    for root, dirs, files in os.walk( ToWalk , topdown=False):
        for name in dirs:
            TargetList1.append(root + '/' + name)
    
    return TargetList1  

def GetList(ToWalk):

    TargetList1 = []
    for root, dirs, files in os.walk( ToWalk , topdown=False):
        for name in files:
            if '.fits' in name:
                TargetList1.append(ToWalk + '/' + name)
    
    return TargetList1        


def  ApplyPreProc(Filelist,MasterDark,MasterFlat):

    DarkInfo = MasterDark.split('_')
    DarkInfo = DarkInfo[-1].split('s')
    ExpTime = float(DarkInfo[0])
    
    Dark = fits.getdata(MasterDark)
    Flat = fits.getdata(MasterFlat)
    

    InfoDir = Filelist[0].split('/')
    
    path = ""
    for st in InfoDir[0:-1]:
        path = path+st+"//"           
 
    os.mkdir(path + "Reduced//")
    for i in Filelist:
        ii = i.split('/')
        if '.fits' in i:
            InfoData = ParseFits(i)
            if InfoData['ExpTime'] == ExpTime:
                data = fits.getdata(i)
                datared = (data-Dark)/(Flat)
                print path + "Reduced//" + ii[-1]
                fits.writeto(path + "Reduced//" + ii[-1],datared)


def  ApplyPreProcCAPS(Filelist,MasterDark):

    DarkInfo = MasterDark.split('_')
 #   DarkInfo = DarkInfo[-1].split('s')
    ExpTime = float(DarkInfo[-3][:-1])
    
    Dark = fits.getdata(MasterDark)
    
#    InfoDir = Filelist[0].split('/')
    
#    path = ""
#    for st in InfoDir[0:-1]:
#        path = path+st+"//"           
 
#    os.mkdir(path + "Reduced//")
    for i in Filelist:
        InfoDir = i.split('/')
        path = ""
        for st in InfoDir[0:-1]:
            path = path+st+"//"
        if os.path.isdir(path + "Reduced//") == False:
            os.mkdir(path + "Reduced//")
        ii = i.split('/')
        if '.fits' in i:
            InfoData = ParseFits(i)
            if InfoData['ExpTime'] == ExpTime:
                hdulist = fits.open(i)
                data = hdulist[0].data
                datared = np.array(data-Dark)
                hdulist[0].data = datared
                print path + "Reduced//" + ii[-1]
                hdulist[0].header['PROCTYPE'] = 'DARK'
                hdulist.writeto(path + "Reduced//" + ii[-1], clobber=True)





def ParseFolder(name):
    
    tamp = re.split('/',name)
    Parsed = re.split('_',tamp[-1])
    
    Folder = dict([('Date', Parsed[-6]), ('Telescope', Parsed[-5]), ('Focus', Parsed[-4]),('Instrument', Parsed[-3]),('Camera', Parsed[-2]),('Object', Parsed[-1])])
    
    return Folder 
    
    
def ParseFits(name):
    Parsed1 = name.split('/')
    Parsed = Parsed1[-1].split('_')
    
    Time = Parsed[-2]

    TimeSplit = Time.split('s')
    T = float(TimeSplit[0])+float('0.' + TimeSplit[1])
    
    File = dict([('Object', Parsed[0]), ('Time', Parsed[1]), ('Type', Parsed[2]) , ('Filter', Parsed[3]),('ExpTime', T)])
    
    return File


def ParseTime(Time):
    Parsed1 = Time.split('T')

    Day = dict([('Year',Parsed1[0][0:4]),('Month',Parsed1[0][4:6]) ,  ('Day',Parsed1[0][6:8])])    
    
    return Day




def MakeFlat(filelist):
    
    
    Cube=[]
    Filter = []
    for i in filelist:
        if '.fits' in i:
            FileInfo = ParseFits(i)            
            Filter.append(FileInfo['Filter'])
    
    for i in set(Filter):
        for j in filelist:
            if '.fits' in j:
                FileInfo = ParseFits(j)
                if FileInfo['Filter'] == i:
                    data, header = fits.getdata(j,header=True)
                    Cube.append(data/np.median(data))

        MedianFlat = np.median(Cube,axis=0)
        fits.writeto('MFlat' + '_' + FileInfo['Filter'] + '_' + str(i) + 's.fits',MedianFlat,header=header)
    
    return MedianFlat      






def MakeDark(filelist):
    
    
    Cube=[]
    ExpTime = []
    for i in filelist:
        if '.fits' in i:
            FileInfo = ParseFits(i)            
            ExpTime.append(FileInfo['ExpTime'])
    
    for i in set(ExpTime):
        for j in filelist:
            if '.fits' in j:
                FileInfo = ParseFits(j)
                if FileInfo['ExpTime'] == i:
                    HDU = fits.open(j)
                    Cube.append(HDU[0].data)
        DarkCube = np.array(Cube)
        MedianDark = np.median(DarkCube,axis=0)
        #HDU.data = MedianDark
        #HDU.writeto('MDark' + '_' + FileInfo['Time'] + '_' + str(i) + 's.fits')
    
    return MedianDark      



#coords = []


def onclick(event):
    ix, iy = event.xdata, event.ydata
    print 'x = %d, y = %d'%(ix, iy)
    
    coords= []
    coords.append((ix, iy))
    
    return coords
#cid = fig.figure.canvas.mpl_connect('button_press_event', onclick)
#fig.figure.canvas.mpl_disconnect(cid)


class Get_Target:
    def __init__(self,fig):
#        self.line = line
#        self.xs = list(line.get_xdata())
#        self.ys = list(line.get_ydata())
        self.xs = []
        self.ys = []
        self.cid = fig.figure.canvas.mpl_connect('button_press_event', self)
    
    def __call__(self, event, fig):
        print('click', event)
#        if event.inaxes!=self.line.axes: return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        fig.figure.canvas.mpl_disconnect(self.cid)
#        self.line.set_data(self.xs, self.ys)
#        self.line.figure.canvas.draw()

