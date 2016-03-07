#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Mon Dec 28 11:04:09 2015

@author: Xavier XU
"""
import ftplib
import os
#os.path.join('C:/Users/Xavier XU/Documents/github/wificonnect')
import glob
import time
#import shutil
#import win32gui,win32con,win32console
#Minimize = win32gui.GetForegroundWindow()
#time.sleep(1)
#win32gui.ShowWindow(Minimize,win32con.SW_MINIMIZE)

if __name__=="__main__":

  if not os.path.exists('../uploaded_files'):
    os.makedirs('../uploaded_files')
  n=0  
  for q in range(9999999):
    try:
        n=n+1; print n
        files=[]
        for x in ('2016','2017','2018','2019'):
           for y in ('01','02','03','04','05','06','07','08','09','10','11','12'):
              files.extend(sorted(glob.glob(x+'/'+y+'/'+'*.csv')))
        print files     
        time.sleep(30)
        if files==[]:
            print 'no new file was found'
            time.sleep(120)
            pass
     
        for u in files:
            #print u
            session = ftplib.FTP('216.9.9.126','huanxin','123321')
            file = open('C:/Program Files (x86)/Aquatec/AQUAtalk for AQUAlogger/DATA/'+u[:7]+'/'+u[8:],'rb') 
            session.cwd("/huanxin")  
            #session.retrlines('LIST')               # file to send
            session.storlines("STOR " +u[8:], open(u[:7]+'/'+u[8:], 'r'))   # send the file
            #session.close()
            session.quit()
            file.close() 
            print u[:7]+'/'+u[8:];print u[8:]
            os.rename('C:/Program Files (x86)/Aquatec/AQUAtalk for AQUAlogger/DATA/'+u[:7]+'/'+u[8:], 'C:/Program Files (x86)/Aquatec/AQUAtalk for AQUAlogger/uploaded_files/'+u[8:])
            print u[8:]+' uploaded'
            #os.rename(u[:7]+'/'+u[8:], "uploaded_files/"+u[8:]) 
            time.sleep(6)                     # close file and FTP
            


   
    except:
        print 'no '
        time.sleep(120)
        print 'no wifi'
        pass


#session = ftplib.FTP('mapdata.assetlinkglobal.com','NOAAfisheries','TransientEddyFormations')

'''
import pysftp
with pysftp.Connection('mapdata.assetlinkglobal.com', username='noaafisheries', password='TransientEddyFormations') as sftp:
    #with sftp.cd('public'):
    sftp.get_r('myfiles', '/backup')    # recursively copy myfiles/ to local
'''

