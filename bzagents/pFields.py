import math

from map import Map, Obstacle, Base

class Pfield:

    #it might not be the same each time.
    # 2 - blue, 4 - red, 1 - purple, 3 -green

    TARGET = '3'
    MAP_NAME = '../maps/four_ls.bzw'
    #MAP_NAME = '../maps/rotated_box_world.bzw'
    
    ALPHA = 5
    BETA = 1
    REPULSIVE_S = 20
    TANGENTIAL_S = 20
    
    def __init__ (self):
        '''do something here'''
        self.map = Map(self.MAP_NAME, self.TARGET)
        bases, obstacles = self.map.load()
        self.bases = bases
        self.obstacles = obstacles
        
    def getVector (self, tank):
        
        print 'getDirection'
        #iterate over obstacles and figure out repulsive fields
        
        self.repulsive(tank)
        
        #figure out tangential fields
        
        #combine that with the attractive field
        
        
        return self.attractive(tank)
        
    def repulsive (self, tank):
    
        for o in self.obstacles:
            print o
        
    def attractive (self, tank):
        target = self.bases[self.TARGET]

        if tank.flag in ['red', 'green', 'blue', 'purple']:
            #change the target
            print 'got the flag'
            
        d = self.distance(tank, target)
        
        if d < target.r: return 0
        
        print target, d
        
        targetAngle = math.atan2(target.cx - tank.y,
                                  target.cy - tank.x)
        return targetAngle
        
    def distance (self, tank, obj):
        return math.sqrt( (tank.x - obj.cx)**2 + (tank.y - obj.cy)**2 )
