#--------------------------------------------------------        
#
# Trajpyv2.py
# Created by Christopher D. Walsh and Jonathan H. Tamsut
#--------------------------------------------------------   

import csv
import trajvarsv2

#--------------------------------------------------------        
#
# function readTraj:
#--------------------------------------------------------  

def readTraj(filename):
    nump = 0 # This is the number of points in your trajectory. 
    # This number is only correct if the dump file only has one starting trajectory
    # First this will tell you the name of file input and the number of trajectories used
    trajListReader=csv.reader(open(filename), dialect='excel') # this text file of all the trajectory dump file names
    number_of_traj_files = trajListReader.next()[0]
    print ' '
    print "You are using " + number_of_traj_files + " HYSPLIT trajectory files."
    print ' '
    # Now lets process each data dump!
    num_files = int(number_of_traj_files) # number of files in the text file with with file names
    # We now must create as many ID files as we have backwards trajectories
    trajList=[]
    for count in range(1,num_files+1):
        current = trajvarsv2.trajectory()
        current.ID=count-1
        trajList.append(current)
    print "Trajectory objects, list initialized."
    print ''    
    print "Reading trajectory files and appending to Trajvars version 2.0!"
    for i in range(0, num_files):
        with open(trajListReader.next()[0], 'r+') as csvfile:
            trajReader=csv.reader(csvfile, dialect='excel')
            for row in trajReader:
                new_row=row[0].split()
                if len(new_row) > 10:
                    nump += 1
                    current=trajvarsv2.trajectory()
                    current.ID=i
                    current.grid=eval(new_row[1])
                    trajList[current.ID].grid.append(current.grid)
                    current.year=eval(new_row[2])
                    trajList[current.ID].year.append(current.year)
                    current.month=eval(new_row[3])
                    trajList[current.ID].month.append(current.month)
                    current.date=eval(new_row[4])
                    trajList[current.ID].date.append(current.date)
                    current.hour=eval(new_row[5])
                    trajList[current.ID].hour.append(current.hour)
                    current.min=eval(new_row[6])
                    trajList[current.ID].min.append(current.min)
                    current.forecasthour=eval(new_row[7])
                    trajList[current.ID].forcasthour.append(current.forcasthour)   
                    current.age=eval(new_row[8])
                    trajList[current.ID].age.append(current.age)   
                    current.lat=eval(new_row[9])
                    trajList[current.ID].lat.append(current.lat)
                    current.lon=eval(new_row[10])
                    trajList[current.ID].lon.append(current.lon)   
                    current.hag=eval(new_row[11])
                    trajList[current.ID].hag.append(current.hag)   
                    current.pressure=eval(new_row[12])
                    trajList[current.ID].pressure.append(current.pressure)
                    current.theta=eval(new_row[13])
                    trajList[current.ID].theta.append(current.theta)
                    current.airtemp=eval(new_row[14])
                    trajList[current.ID].airtemp.append(current.airtemp)
                    current.rain=eval(new_row[15])
                    trajList[current.ID].rain.append(current.rain)
                    current.mixdepth=eval(new_row[16])
                    trajList[current.ID].mixdepth.append(current.mixdepth)
                    current.rh=eval(new_row[17])
                    trajList[current.ID].rh.append(current.rh)
                    current.msl=eval(new_row[18])
                    trajList[current.ID].msl.append(current.msl)
                    current.flux=eval(new_row[19])
                    trajList[current.ID].flux.append(current.flux)  
    print ' '
    print 'HYSPLIT paramters stored!' 
    for x in range(0,num_files):
        trajList[x].numpoints=nump
        trajList[x].numtraj=num_files
    print ''
    print 'trajList populated! You are using ' + str(nump) + ' trajectory endpoints!'
    print ''
    return trajList

#--------------------------------------------------------        
#
# procedure makeBox:
#-------------------------------------------------------- 

def makeBox(Tag,box_points,numtraj,polygon,radius):
    points_in_box = 0
    points_below_alt = 0
    rain_scav = 0
    for q in range(0,numtraj):
        srifTmp=srifMake(trajResult[q],box_points,polygon,radius)
        points_in_box += srifTmp[3]
        points_below_alt += srifTmp[1] 
        rain_scav += srifTmp[4]
    cond_imp = points_below_alt/points_in_box
    impfactor= (points_in_box/75.)
    print 'SRIF: ' + str(impfactor)
    print ' '
    print "Conditional prob: " + str(cond_imp) 
    print ' '
    print "In " + str(rain_scav) + " source regions rainfall was above the cutoff value."
    print " "

#--------------------------------------------------------        
#
# function srifMake:
#-------------------------------------------------------- 
 
def lat(point):      # helper function that gives you latitude
    return point[0]
 
def long(point):     # helper function that gives you latitude
    return point[1]
 
# check_intersect checks if a ray pointing due east crosses
# a line of a polygon. This polygon is a SRIF box. check_intersect is
# a helper function for the ray casting algorithm.
 
def check_cross(point, segstart, segend):
    plat = lat(point)
    plong = long(point)
    # Here we are checking to see if a ray due east will pass a horizontal line
    # created by the boundaries of an apportionment.
    cond1 = lat(segstart) < plat and lat(segend) > plat
    cond2 = lat(segstart) > plat and lat(segend) < plat
    # note that the when specifying (lat, long) you must specify
    # coordinates opposite of what is normally expressed in Cartesian coordinates
    # (y,x) => (lat, long)
    if (not cond1) and (not cond2):
        return False
    y = long(segstart) - long(segend) # distance in x direction
    x = lat(segend) - lat(segstart) # distance in the y direction
    c = x * long(segstart) + y * lat(segstart)
    x = (c-y*plat)/x
    if x < plong:
        return True
    else:
        return False
     
# box_points should be a list of lists made up
# of a series of points specified as [lat, long] 
# connected to one another.
 
def is_in_box(point,box_points,radius=None):
    # box_points must be a list of points (a list of lists) in (lat,long) form
    count, k = 0, 0
    while k + 1 < len(box_points):
        if check_cross(point, box_points[k], box_points[k+1]):
            count += 1
        k += 1
    if count % 2 != 1:
        return False
    else:
        return True
 
def is_in_circle(center,point,radius):
    plat = lat(point)
    plong = long(point)
    cen_lat=lat(center)
    cen_long=long(center)
    d = ((plat-cen_lat)**2 + (plong-cen_long)**2)**(1/2)
    if d < radius:
        return True
    else:
        return False
 
def srifMake(Tc,box_points,polygon,radius):  
    srifReturn=[0,0,0,0,0]
    # srifMake outputs srifReturn which is a list of numbers.
    # Each number corresponds to the number of trajectory endpoints 
    # that were below some altitude and were in a given source region.
    nump=len(Tc.lat) # 10-day back trajectory; must specify how many points 
                     # you are working with here
    for y in range(0,nump):
        point = []
        lat=Tc.lat[y]
        lon=Tc.lon[y]
        alt=Tc.hag[y]
        rainfall=Tc.rain[y]
        point.insert(0, lat)
        point.insert(1, lon)
        # in order to compute the conditional probability below simply change
        # the altitude to whatever the cutoff is
        if polygon is True:
            if is_in_box(point, box_points):
                if alt<1000:
                    srifReturn[0]+=1
                if alt<2000:
                    srifReturn[1]+=1
                if alt<3000:
                    srifReturn[2]+=1
                if alt<10000:
                    srifReturn[3]+=1
        else:
            if is_in_circle(point, box_points, radius):
                if alt<1000:
                    srifReturn[0]+=1
                if alt<2000:
                    srifReturn[1]+=1
                if alt<3000:
                    srifReturn[2]+=1
                if alt<10000:
                    srifReturn[3]+=1
        if rainfall > 0:   # set rainfall cut off
        	srifReturn[4]+=1
    return srifReturn


#--------------------------------------------
# 
# Main: This is where you execute Trajpy v2. 
#
#--------------------------------------------

trajResult=readTraj("trajlist.txt")
trajsrif=[]
numtraj=trajResult[1].numtraj
for j in range(0,numtraj):
    tmpRcd=trajvarsv2.srifcount
    trajsrif.append(tmpRcd)
