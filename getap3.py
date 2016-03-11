# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 13:51:53 2015

@author: hxu
"""
from matplotlib.dates import date2num
import time
from dateutil import parser
import glob
import json
import datetime
import numpy as np
def read_codes():
  # get id,depth from /data5/jmanning/drift/codes.dat
  inputfile1="codes_temp.dat"
  #path1="/net/data5/jmanning/drift/"
  path1='/home/hxu/Downloads/'
  f1=open(path1+inputfile1,'r')
  esn,id,depth=[],[],[]
  for line in f1:
    esn.append(line.split()[0])
    id.append(line.split()[1])
    depth.append(line.split()[2]) 
 	

  return esn, id,depth
  
esn2, ide,depth=read_codes()
'''
sftp=pysftp.Connection('mapdata.assetlinkglobal.com', username='noaafisheries', password='TransientEddyFormations')
    #with sftp.cd('outgoing') :             # temporarily chdir to public
        #sftp.put('/my/local/filename')  # upload file to public/ on remote
sftp.get_d('outgoing', 'backup')    # recursively copy myfiles/ to local
'''
files=sorted(glob.glob('backup/*.json'))

##for i in files:
  ##  sftp.remove('outgoing'+i[6:])

'''
exist_id=[]
with open('exist_json.dat','a') as file_exist_json:
    exist_id.append(file_exist_json.readlines())
'''    

f_output=open('ap3_'+  str(datetime.datetime.now())[:16]+'.dat','w')    
esn,date,lat,lon,battery,data_send,meandepth,rangedepth,timelen,meantemp,sdeviatemp=[],[],[],[],[],[],[],[],[],[],[],
c=0
for i in files:
    try:
      with open(i) as data_file:    
        data = json.load(data_file)
      try:
          if data['momentForward'][0]['Device']['moments'][0]['Moment']['points'][2]['PointHex']['hex'][18:19]=='9': #make sure that is aquetec data
              
                  sdeviatemp=float(data['momentForward'][0]['Device']['moments'][0]['Moment']['points'][2]['PointHex']['hex'][32:36])/100
                  meantemp=float(data['momentForward'][0]['Device']['moments'][0]['Moment']['points'][2]['PointHex']['hex'][28:32])/100
                  timelen=float(data['momentForward'][0]['Device']['moments'][0]['Moment']['points'][2]['PointHex']['hex'][25:28])/1000
                  rangedepth=float(data['momentForward'][0]['Device']['moments'][0]['Moment']['points'][2]['PointHex']['hex'][22:25])
                  meandepth=float(data['momentForward'][0]['Device']['moments'][0]['Moment']['points'][2]['PointHex']['hex'][19:22])
                  
                  
                  lat=data['momentForward'][0]['Device']['moments'][0]['Moment']['points'][3]['PointLoc']['Lat'] #possiblely have problem to read this data
                  esn=data['momentForward'][0]['Device']['esn']
                  date=int(parser.parse(data['momentForward'][0]['Device']['moments'][0]['Moment']['date']).strftime('%s'))
                  time_tuple=time.gmtime(date)
                  #time_tuple=time.gmtime(unixtime)
                  yr1=time_tuple.tm_year
                  mth1=time_tuple.tm_mon
                  day1=time_tuple.tm_mday
                  hr1=time_tuple.tm_hour
                  mn1=time_tuple.tm_min
                  yd1=date2num(datetime.datetime(yr1,mth1,day1,hr1,mn1))-date2num(datetime.datetime(yr1,1,1,0,0))
                  datet=datetime.datetime(yr1,mth1,day1,hr1,mn1,tzinfo=None)                    
                  data_send=data['momentForward'][0]['Device']['moments'][0]['Moment']['points'][2]['PointHex']['hex']
                  lon=data['momentForward'][0]['Device']['moments'][0]['Moment']['points'][3]['PointLoc']['Lon']
                  battery=data['momentForward'][0]['Device']['moments'][0]['Moment']['points'][5]['Point']['Battery']
          try :
              
              
              index_idn1=(np.where(str(esn[-6:])==np.array(ide)))[0][0]
              print index_idn1
              id_idn1=esn2[index_idn1] # where "caseid" is the consecutive time this unit was used
              depth_idn1=-1.0*float(depth[index_idn1]) # make depth negative
              #f_output=open('ap3_'+  str(datetime.datetime.now())[:16]+'.dat', 'w')
              f_output.write(str(id_idn1).rjust(10)+" "+str(esn).rjust(7)+ " "+str(mth1).rjust(2)+ " " +
                      str(day1).rjust(2)+" " +str(hr1).rjust(3)+ " " +str(mn1).rjust(3)+ " " )
              f_output.write(("%10.7f") %(yd1))
              #f_output.write(" "+str(lon).rjust(10)+' '+str(lat).rjust(10)+ " " +str(float(depth_idn1)).rjust(4)+ " "
              #        +str(np.nan))
              f_output.write(" "+("%10.5f") %(lon)+' '+("%10.5f") %(lat)+' '+str(float(depth_idn1)).rjust(4)+ " "
                      +str(np.nan))
              #f_output.write(" "+str(meandepth).rjust(10)+' '+str(rangedepth).rjust(10)+' '+str(len_day).rjust(10)+  " " +str(mean_temp).rjust(4)+ " "
              #        +str(sdevia_temp)+'\n')            
              f_output.write(" "+str(meandepth).rjust(10)+' '+str(rangedepth).rjust(10)+' '+str(timelen).rjust(10)+  " " +("%6.2f") %(meantemp)+ " "
                      +("%6.2f") %(sdeviatemp)+("%6.0f") %(yr1)+'\n')          
          except:
              pass
          #os.remove(i)
          
      except:
          c=c+1
          print 'file:'+i+'may has a problem'
          #os.rename(i, "backup/bad_"+i[7:])
          pass
    except:
        print 'no data in '+ i
f_output.close()
#esn=sorted(esn)
'''
date=[x for (y,x) in sorted(zip(esn,date))]
lat=[x for (y,x) in sorted(zip(esn,lat))]
lon=[x for (y,x) in sorted(zip(esn,lon))]
battery=[x for (y,x) in sorted(zip(esn,battery))]
data_send=[x for (y,x) in sorted(zip(esn,data_send))]
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
        f.writelines(esn[i][-6:]+','+deploy_id[i]+','+date[i].strftime('%Y-%m-%d %H:%M:%S')+','+str(round(lat[i],6))+','+str(round(lon[i],6))+','+str(data_send[i])+','+str(battery[i])+'\n')
    f.close()

'''    
'''
file_exist_json  
'''  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  