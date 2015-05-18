import math

from map import Map, Obstacle, Base

class Pfield:
     
    def __init__ (self, myTeam, mapName):
        '''load in the obstacles and bases'''
        self.MYTEAM = myTeam
        self.map = Map(mapName)
        bases, obstacles = self.map.load()
        self.bases = bases
        self.obstacles = obstacles
        
    def getVector (self, tank, target):
        target = self.bases[target]
        if tank.flag in ['red', 'green', 'blue', 'purple']:
            #change the target
            target = self.bases[self.MYTEAM]
        
        #attractive field        
        attrX, attrY = self.attractive(tank, target)
        
        #repulsive fields
        repX, repY = self.repulsive(tank, target)
        
        return math.atan2(attrY + repY, attrX + repX)
          
    def repulsive (self, tank, target):
        
        REPULSIVE_S = 30
        TANGENTIAL_S = 50
        GAMMA = 1
        BETA = 1
        
        deltaX = 0
        deltaY = 0
    
        for obst in self.obstacles:
            d = self.distance(tank, obst)
            
            theta = math.atan2(obst.y - tank.y, obst.x - tank.x)

            #REPULSIVE FIELD
            if obst.r < d and d < (REPULSIVE_S + obst.r):
                deltaX -= BETA * (REPULSIVE_S + obst.r - d) * math.cos(theta)
                deltaY -= BETA * (REPULSIVE_S + obst.r - d) * math.sin(theta)
            
            #TANGENTIAL FIELD
            if obst.r < d and d < (TANGENTIAL_S + obst.r):
                obsX = obst.x - target.x
                obsY = obst.y - target.y
                tankX = tank.x - target.x
                tankY = tank.y - target.y
                dot = obsX * tankY - obsY * tankX
                rightAngle = math.pi / 2
                if dot < 0: rightAngle *= -1
                deltaX -= GAMMA * (TANGENTIAL_S + obst.r - d) * math.cos(theta + rightAngle)
                deltaY -= GAMMA * (TANGENTIAL_S + obst.r - d) * math.sin(theta + rightAngle)
            
        return (deltaX, deltaY)
                        
        
    def attractive (self, tank, target):
        ALPHA = 5
            
        d = self.distance(tank, target)
        
        if d < target.r: return (0, 0)
                
        theta = math.atan2(target.y - tank.y, target.x - tank.x)
                                  
        deltaX = ALPHA * math.cos(theta)
        deltaY = ALPHA * math.sin(theta)
        
        return (deltaX, deltaY)
        
    def distance (self, tank, obj):
        return math.sqrt( (tank.x - obj.x)**2 + (tank.y - obj.y)**2 )
