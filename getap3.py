# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 13:51:53 2015

@author: hxu
"""

import pysftp
import os
from dateutil import parser
import glob
import json
import datetime
def read_codes():
  # get id,depth from /data5/jmanning/drift/codes.dat
  inputfile1="codes.dat"
  path1="/net/data5/jmanning/drift/"
  f1=open(path1+inputfile1,'r')
  esn,id,depth=[],[],[]
  for line in f1:
    esn.append(line.split()[0])
    id.append(line.split()[1])
    depth.append(line.split()[2]) 
 	

  return esn, id,depth
  
esn2, id,depth=read_codes()

sftp=pysftp.Connection('mapdata.assetlinkglobal.com', username='noaafisheries', password='TransientEddyFormations')
    #with sftp.cd('outgoing') :             # temporarily chdir to public
        #sftp.put('/my/local/filename')  # upload file to public/ on remote
sftp.get_d('outgoing', 'backup')    # recursively copy myfiles/ to local
files=sorted(glob.glob('backup/*.json'))
for i in files:
    sftp.remove('outgoing'+i[6:])

'''
exist_id=[]
with open('exist_json.dat','a') as file_exist_json:
    exist_id.append(file_exist_json.readlines())
'''    
   
    
esn,date,lat,lon,battery=[],[],[],[],[]
for i in files:
  with open(i) as data_file:    
    data = json.load(data_file)
  try:  
      lat.append(data['momentForward'][0]['Device']['moments'][0]['Moment']['points'][3]['PointLoc']['Lat']) #possiblely have problem to read this data
      esn.append(data['momentForward'][0]['Device']['esn'])
      date.append(parser.parse(data['momentForward'][0]['Device']['moments'][0]['Moment']['date']))
      
      lon.append(data['momentForward'][0]['Device']['moments'][0]['Moment']['points'][3]['PointLoc']['Lon'])
      battery.append(data['momentForward'][0]['Device']['moments'][0]['Moment']['points'][5]['Point']['Battery'])
      os.remove(i)
  except:
      print 'file'+i+'may has a problem'
      os.rename(i, "../bad_"+i)
      pass
#esn=sorted(esn)

date=[x for (y,x) in sorted(zip(esn,date))]
lat=[x for (y,x) in sorted(zip(esn,lat))]
lon=[x for (y,x) in sorted(zip(esn,lon))]
battery=[x for (y,x) in sorted(zip(esn,battery))]
esn=sorted(esn)




deploy_id=[]
for y in esn:  
  for x in range(len(esn2)):
    if esn2[x]==esn[0][-6:]:
        deploy_id.append(id[x])





if len(deploy_id)<>len(esn):
    print 'check if your esn and deploy_id is in codes.dat'

else:
    
    dict_f=dict
    f=open('ap3_'+  str(datetime.datetime.now())[:16]+'.dat', 'w')
    for i in range(len(esn)):
        f.writelines(esn[i][-6:]+','+deploy_id[i]+','+date[i].strftime('%Y-%m-%d %H:%M:%S')+','+str(round(lat[i],6))+','+str(round(lon[i],6))+','+str(battery[i])+'\n')
    f.close()
'''
file_exist_json  
'''  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  