#--------------------------------------------------------        
#
#trajvars.py
#--------------------------------------------------------

# input classes

class trajectory():
    def __init__(self):
        self.name=''
        self.ID=0
        self.numpoints=0
        self.numtraj=0
        self.grid=[]
        self.year=[]
        self.month=[]
        self.date=[]
        self.hour=[]
        self.min=[]
        self.forcasthour=[]
        self.age=[]
        self.lat=[]
        self.lon=[]
        self.hag=[]
        self.pressure=[]
        self.theta=[]
        self.airtemp=[]
        self.rain=[]
        self.mixdepth=[]
        self.rh=[]
        self.msl=[]
        self.flux=[]

              
        
# output classes

class srifcount():
    def __init__(self):
        self.ID=0
        self.count1km=0.
        self.count2km=0.
        self.count3km=0.
        self.countTotal=0.
    

