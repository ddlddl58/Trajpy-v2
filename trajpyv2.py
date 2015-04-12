#--------------------------------------------------------        
#
# trajPy.py
# Created by Christopher D. Walsh
# Updated & improved by Jonathan H. Tamsut
#--------------------------------------------------------        

import os
import math
import csv
import trajvarsv2

#--------------------------------------------------------        
#
# function readTraj:
#--------------------------------------------------------  

def readTraj(filename):

    trajList=[]
    trajReader=csv.reader(open(filename),dialect='excel')

    R1=trajReader.next()
    numMetfiles = eval(R1[0])
    print numMetfiles,' Met files used: [type, year, month, date]'
    
    for row in range(0,numMetfiles):
        Rc=trajReader.next()
        print Rc[0:4]

    R3=trajReader.next()
    numTraj=eval(R3[0])

    print ''
    print numTraj,'Trajectories in file'
    print ''
    print 'start date, time, lat and lon:'
    for row in range(1,numTraj+1):
        Rc=trajReader.next()
        print row, Rc[0:6]
    
    R5=trajReader.next()
    print ''
    print 'metadump: ',R5

# ---------------------------------------------
# numHrs must be manually set :(
# ---------------------------------------------
    numHrs=240
    numPoints=numTraj*numHrs
    print ''
    print 'numtraj:',numTraj,' numpoints:', numPoints
    
    for count in range(1,numTraj+1):
        current = trajvars.trajectory()
        current.ID=count-1
        trajList.append(current)
    print ''
    print numTraj,'Trajectory objects, list initialized.'
    
    for row in range(0,numPoints):
        current=trajvars.trajectory()
        Rc=trajReader.next()
        current.ID=eval(Rc[0])-1
        current.grid=eval(Rc[1])
        trajList[current.ID].grid.append(current.grid)
        current.year=eval(Rc[2])
        trajList[current.ID].year.append(current.year)
        current.month=eval(Rc[3])
        trajList[current.ID].month.append(current.month)
        current.date=eval(Rc[4])
        trajList[current.ID].date.append(current.date)
        current.hour=eval(Rc[5])
        trajList[current.ID].hour.append(current.hour)
        current.min=eval(Rc[6])
        trajList[current.ID].min.append(current.min)
        current.forcasthour=eval(Rc[7])
        trajList[current.ID].forcasthour.append(current.forcasthour)   
        current.age=eval(Rc[8])
        trajList[current.ID].age.append(current.age)   
        current.lat=eval(Rc[9])
        trajList[current.ID].lat.append(current.lat)
        current.lon=eval(Rc[10])
        trajList[current.ID].lon.append(current.lon)   
        current.hag=eval(Rc[11])
        trajList[current.ID].hag.append(current.hag)   
        current.pressure=eval(Rc[12])
        trajList[current.ID].pressure.append(current.pressure)
        current.theta=eval(Rc[13])
        trajList[current.ID].theta.append(current.theta)
        current.airtemp=eval(Rc[14])
        trajList[current.ID].airtemp.append(current.airtemp)
        current.rain=eval(Rc[15])
        trajList[current.ID].rain.append(current.rain)
        current.mixdepth=eval(Rc[16])
        trajList[current.ID].mixdepth.append(current.mixdepth)
        current.rh=eval(Rc[17])
        trajList[current.ID].rh.append(current.rh)
        current.msl=eval(Rc[18])
        trajList[current.ID].msl.append(current.msl)
        current.flux=eval(Rc[19])
        trajList[current.ID].flux.append(current.flux)
        
    for x in range(0,numTraj):
        trajList[x].numpoints=numPoints
        trajList[x].numtraj=numTraj
    print ''
    print 'trajList populated.'
    print ''
    return trajList

#--------------------------------------------------------        
#
# procedure makeBox:
#-------------------------------------------------------- 
def makeBox(Tag,Box,numtraj):
   
    textFile=open("trajPy_output.csv", "a")
    for q in range(0,numtraj):
        srifTmp=srifMake(trajResult[q], Box[0], Box[1], Box[2], Box[3])
        impfactor=100.*srifTmp[3]/240.
        csvTxt=Tag+","+str(impfactor)+'\n'
        textFile.write(csvTxt)
    
    textFile.close()
    
#--------------------------------------------------------        
#
# function srifMake:
#-------------------------------------------------------- 

def srifMake(Tc,srifN,srifS,srifE,srifW):
    
    srifReturn=[0,0,0,0]
    nump=240 # 10-day back trajectory

    for y in range(0,nump):
        lat=Tc.lat[y]
        lon=Tc.lon[y]
        alt=Tc.hag[y]
        
        if (lon<srifE) and (lon>srifW) and \
        (lat<srifN) and (lat>srifS):
            if alt<1000:
                srifReturn[0]=srifReturn[0]+1
            if alt<2000:
                srifReturn[1]=srifReturn[1]+1
            if alt<3000:
                srifReturn[2]=srifReturn[2]+1
            if alt<10000:
                srifReturn[3]=srifReturn[3]+1
    
    return srifReturn

#--------------------------------------------------
#   Define SRIF boxes here:
#   ___Box=[ N,S,E,W] boundaries in decimal lat/lon
#--------------------------------------------------

asiaBox=[50.,15.,180.,100.]
siberiaBox=[70.,50.,180.,100.]
akBox=[70.,55.,-140.,-170.]
bcBox=[60.,49.,-115.,-132.]
waBox=[49.,46.,-117.,-125.]
orBox=[46.,42.,-117.,-125.]
uwaBox=[50.,47.,-121.5,-125.]
uorBox=[46.,44.,-122.,-123.5]
uca1Box=[40.,36.5,-120.,-125.]
uca2Box=[36.,32.,-115.,-120.]
eowBox=[49.,45.,-117.,-120.5]
worBox=[46.,44.,-122.,-123.5]
cvBox=[39.5,36.,-119.,-123.]

#--------------------------------------------------------        
#
# Main:
#--------------------------------------------------------  
Snum=''
listFile=open('trajlist.txt','r')
Snum=listFile.readline()
num=int(Snum)

for z in range(0,num):
    filename=listFile.readline()
    filename=filename[:-1]
    print ''
    print z,' ',filename
    trajResult=readTraj(filename)
    numtraj=trajResult[1].numtraj
    numpoints=trajResult[1].numpoints
    numhrs=72
    print '# of trajectories, points in file:',numtraj, numpoints
    print 'hours of back trajectory analyzed:',numhrs
    print '--------------------------------------------------'
    print ''
    textFile=open('trajPy_output.csv', 'a')
    header='20'+str(trajResult[0].year[0])+'-'+str(trajResult[0].month[0])+\
        '-'+str(trajResult[0].date[0])+' '+str(trajResult[0].hour[0])+ '\n'
    textFile.write(header)
    textFile.close()
    
    trajsrif=[]
    for j in range(0,numtraj): 
        tmpRcd=trajvars.srifcount
        trajsrif.append(tmpRcd)
    
    makeBox('Asia',asiaBox,numtraj)
    makeBox('Siberia',siberiaBox,numtraj)
    makeBox('Alaska',akBox,numtraj)
    makeBox('BC',bcBox,numtraj)
    makeBox('WA',waBox,numtraj)    
    makeBox('OR',orBox,numtraj)    
    makeBox('urban WA',uwaBox,numtraj)
    makeBox('urban OR',uorBox,numtraj)    
    makeBox('SF',uca1Box,numtraj)
    makeBox('LA',uca2Box,numtraj)    
    makeBox('Eastern WA and OR',eowBox,numtraj)    
    makeBox('Willamette Valley',worBox,numtraj)
    makeBox('CA Central Valley',cvBox,numtraj)

listFile.close()

# -------------------------------------------
# end
# -------------------------------------------
