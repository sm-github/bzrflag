import pprint

class Map:

    bases = {}
    obstacles = []

    def __init__ (self, mapName, target):
        self.target = target
        self.mapName = mapName
        
    def load (self):
        with open(self.mapName, 'r') as mapInfo:
            self.readMapFile(mapInfo)
            
        return (self.bases, self.obstacles)

    def readMapFile (self, mapInfo):
        
        line = mapInfo.readline()

        while line:
            if line == 'base\n':
                self.loadBase(mapInfo)
            if line == 'box\n':
                self.loadObstacle(mapInfo)

            line = mapInfo.readline()
            
        pprint.pprint(self.bases)
        pprint.pprint(self.obstacles)
        
    def loadBase (self, mapInfo):
    
        position = mapInfo.readline().split()
        mapInfo.readline() #rotation
        mapInfo.readline() #size
        color = mapInfo.readline().split()[1]
        
        #create the base and store it in a dictionary
        self.bases[color] = Base(position[1], position[2], color)
        
        line = mapInfo.readline() #end
    
    def loadObstacle (self, mapInfo):
  
        position = mapInfo.readline().split()
        mapInfo.readline() #rotation
        mapInfo.readline() #size
        self.obstacles.append(Obstacle(position[1], position[2]))
            
class Obstacle:
    
    def __init__ (self, cx, cy):
        self.cx = float(cx)
        self.cy = float(cy)
        self.r = 30 #this might need to change later
        
    def __repr__ (self):
        return 'position: ' + str(self.cx) + ',' + str(self.cy)

class Base:

    def __init__ (self, cx, cy, color):
        self.cx = float(cx)
        self.cy = float(cy) 
        self.color = color
        self.r = 5
        
    def __repr__ (self):
        return 'color: ' + self.color + '\nposition: ' + str(self.cx) + ',' + str(self.cy)
