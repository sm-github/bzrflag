#!/usr/bin/python -tt

import sys
import math
import time

from pFields import Pfield
from bzrc import BZRC, Command

class Agent(object):

    MYTANK = 0
    lastError = {}
    KP = 1
    KD = 0
    
    # 1 - red, 2 - green, 3 - blue, 4 - purple
    TARGET = '3'
    MYTEAM = '4'
    
    #MAP_NAME = '../maps/four_ls.bzw'
    MAP_NAME = '../maps/rotated_box_world.bzw'

    def __init__(self, bzrc):
        self.bzrc = bzrc
        self.pField = Pfield(self.MYTEAM, self.MAP_NAME)
        self.constants = self.bzrc.get_constants()
        
        for i in range(0,10):
            self.lastError[i] = 0

    def tick(self, timeDiff, shoot=False):

        mytanks, othertanks, flags, shots = self.bzrc.get_lots_o_stuff()
        self.mytank = [tank for tank in mytanks if tank.index == self.MYTANK][0]
        self.enemies = [tank for tank in othertanks if tank.color !=
                        self.constants['team']]
                        
        commands = []
        
        for tank in mytanks:
            if tank.flag in ['red', 'green', 'blue', 'purple'] or tank.index % 2:
                targetAngle = self.pField.getVector(tank, self.TARGET)
                newAngVel = self.getAngVel(tank, targetAngle, timeDiff)
                commands.append(Command(tank.index, 1, newAngVel, 1))
            else:
                commands.append(self.attack_enemies(tank))
            
        self.bzrc.do_commands(commands)

    def getAngVel(self, tank, targetAngle, timeDiff):
        angError = self.normalizeAngle(targetAngle - tank.angle)
        deltaError = (angError - self.lastError[tank.index]) / timeDiff
        angVel = self.KP * angError + self.KD * deltaError
        self.lastError[tank.index] = angError
        
        angVel = 1 if angVel > 1 else -1 if angVel < -1 else angVel
           
        return angVel
        
    def attack_enemies(self, tank):
        """Find the closest enemy and chase it, shooting as you go."""
        best_enemy = None
        best_dist = 2 * float(self.constants['worldsize'])
        for enemy in self.enemies:
            if enemy.status != 'alive':
                continue
            dist = math.sqrt((enemy.x - tank.x)**2 + (enemy.y - tank.y)**2)
            if dist < best_dist:
                best_dist = dist
                best_enemy = enemy
        if best_enemy is None:
            return Command(tank.index, 0, 0, False)
           
        return self.move_to_position(tank, best_enemy.x, best_enemy.y)

    def move_to_position(self, tank, target_x, target_y):
        """Set command to move to given coordinates."""
        target_angle = math.atan2(target_y - tank.y,
                                  target_x - tank.x)
        relative_angle = self.normalizeAngle(target_angle - tank.angle)
        return Command(tank.index, 1, 2 * relative_angle, True)
        
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
    bzrc = BZRC('localhost', int(port))
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
