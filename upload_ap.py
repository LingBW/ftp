# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 09:13:28 2016

@author: hxu
"""

import ftplib
import os
#os.path.join('C:/Users/Xavier XU/Documents/github/wificonnect')



session = ftplib.FTP('216.9.9.126','huanxin','123321')
file = open('bc.txt','rb')
session.cwd("/huanxin") 
session.retrlines('LIST')               # file to send
session.storlines("STOR " + 'bc.txt', open('bc.txt', 'r'))   # send the file

file.close()                                    # close file and FTP
session.quit()