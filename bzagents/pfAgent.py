#!/usr/bin/python -tt

import sys
import math
import time

from pFields import Pfield
from bzrc import BZRC, Command

class Agent(object):

    MYTANK = 0
    lastError = 0
    KP = 1
    KD = 0

    def __init__(self, bzrc):
        self.bzrc = bzrc
        self.pField = Pfield()
        self.constants = self.bzrc.get_constants()
        bzrc.speed(0, 1)


    def tick(self, timeDiff, shoot=False):

        mytanks, othertanks, flags, shots = self.bzrc.get_lots_o_stuff()
        self.mytank = [tank for tank in mytanks if tank.index == self.MYTANK][0]
        
        targetAngle = self.pField.getVector(self.mytank)
        print targetAngle, self.mytank.angle
        newAngVel = self.getAngVel(targetAngle, timeDiff)
        self.bzrc.angvel(0, newAngVel)
        self.bzrc.shoot(0)
        
        print newAngVel


    def getAngVel(self, targetAngle, timeDiff):
        angError = self.normalizeAngle(targetAngle - self.mytank.angle)
        deltaError = (angError - self.lastError) / timeDiff
        angVel = self.KP * angError + self.KD * deltaError
        self.lastError = angError
        
        angVel = 1 if angVel > 1 else -1 if angVel < -1 else angVel
           
        return angVel
        
    def normalizeAngle(self, angle):
    
        angle -= 2 * math.pi * int (angle / (2 * math.pi))
        if angle <= -math.pi:
            angle += 2 * math.pi
        elif angle > math.pi:
            angle -= 2 * math.pi
        return angle


def main():
    # Process CLI arguments.
    try:
        execname, port = sys.argv
    except ValueError:
        execname = sys.argv[0]
        print >>sys.stderr, '%s: incorrect number of arguments' % execname
        print >>sys.stderr, 'usage: %s port' % sys.argv[0]
        sys.exit(-1)

    # Connect.
    #bzrc = BZRC(host, int(port), debug=True)
    bzrc = BZRC('128.187.80.142', int(port))
    agent = Agent(bzrc)
    prevTime = time.time()

    # Run the agent

    try:
        while True:
            if time.time() > prevTime + 0.01:
                agent.tick(time.time() - prevTime)
                prevTime = time.time()
            
    except KeyboardInterrupt:
        print "Exiting due to keyboard interrupt."
        bzrc.close()


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
