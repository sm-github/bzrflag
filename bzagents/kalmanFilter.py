#!/usr/bin/env python

import sys
import math
import time
import numpy as np
from bzrc import BZRC, Command

MYTANK = 0
# 1 - red, 2 - green, 3 - blue, 4 - purple
TARGET = '3'
MYTEAM = '4'
bzrc = None
constants = None

#CONSTANTS
C = 0
DELTA_TIME = 0.2

I = np.identity(6)
F = np.matrix([
    [1, DELTA_TIME, (DELTA_TIME**2)/2, 0, 0,            0],
    [0, 1,          DELTA_TIME,        0, 0,            0],
    [0, -C,         1,                 0, 0,            0],
    [0, 0,          0,                 1, DELTA_TIME,   (DELTA_TIME**2)/2],
    [0, 0,          0,                 0, 1,            DELTA_TIME],
    [0, 0,          0,                 0,-C,            1]])
H = np.matrix([
    [1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0]])

#TRANSPOSE
FT = F.getT()
HT = H.getT()
# 

MU = np.matrix('0; 0; 0; 0; 0; 0')

sig = np.matrix([
    [100, 0, 0, 0, 0, 0],
    [0, 0.1, 0, 0, 0, 0],
    [0, 0, 0.1, 0, 0, 0],
    [0, 0, 0, 100, 0, 0],
    [0, 0, 0, 0, 0.1, 0],
    [0, 0, 0, 0, 0, 0.1]])
sigX = np.matrix([
    [0.1, 0, 0, 0, 0, 0],
    [0, 0.1, 0, 0, 0, 0],
    [0, 0, 100, 0, 0, 0],
    [0, 0, 0, 0.1, 0, 0],
    [0, 0, 0, 0, 0.1, 0],
    [0, 0, 0, 0, 0, 100]])
sigZ = np.matrix([
    [25, 0],
    [0, 25]])

def updateFilter (tank):
    global I, F, FT, H, HT, MU, sig, sigX, sigZ

    print tank.x, tank.y
    printMatrixes()

    Z = np.matrix([[tank.x], [tank.y]])

    term = (F * sig * FT) + sigX
    
    K = term * HT * (H * term * HT + sigZ) - 1
    
    MU = F * MU + K * (Z + 1 - (H * F * MU))
    
    sig = (I - K * H) * term

    center = (MU.item(0, 0), MU.item(3, 0))
    ellipseWidth = sig.item((0, 0))
    ellipseHeight = sig.item((3, 3))

    print center
    print ellipseWidth, ellipseHeight
    
    #apply predictions into the future
    # mu [t + 1] = F * mu [t]

def printMatrixes ():
    global I, F, FT, H, HT, MU, sig, sigX, sigZ

    print 'MU:\n', MU, '\nsig:\n', sig

def tick(timeDiff):

    mytanks, othertanks, flags, shots = bzrc.get_lots_o_stuff()
    mytank = [tank for tank in mytanks if tank.index == MYTANK][0]
    greenTank = [tank for tank in othertanks if tank.color == 'green'][0]
    # blueTeam

    commands = []

    updateFilter(greenTank)

    # for tank in mytanks:

    bzrc.do_commands(commands)

def getAngVel(tank, targetAngle, timeDiff):
    KP = 1
    KD = 0
    angError = normalizeAngle(targetAngle - tank.angle)
    deltaError = (angError - lastError[tank.index]) / timeDiff
    angVel = KP * angError + KD * deltaError
    lastError[tank.index] = angError

    angVel = 1 if angVel > 1 else -1 if angVel < -1 else angVel

    return angVel

def attack_enemies(tank):
    """Find the closest enemy and chase it, shooting as you go."""
    best_enemy = None
    best_dist = 2 * float(constants['worldsize'])
    for enemy in enemies:
        if enemy.status != 'alive':
            continue
        dist = math.sqrt((enemy.x - tank.x)**2 + (enemy.y - tank.y)**2)
        if dist < best_dist:
            best_dist = dist
            best_enemy = enemy
    if best_enemy is None:
        return Command(tank.index, 0, 0, False)

    return move_to_position(tank, best_enemy.x, best_enemy.y)

def move_to_position(tank, target_x, target_y):
    """Set command to move to given coordinates."""
    target_angle = math.atan2(target_y - tank.y,
                              target_x - tank.x)
    relative_angle = normalizeAngle(target_angle - tank.angle)
    return Command(tank.index, 1, 2 * relative_angle, True)

def normalizeAngle(angle):

    angle -= 2 * math.pi * int (angle / (2 * math.pi))
    if angle <= -math.pi:
        angle += 2 * math.pi
    elif angle > math.pi:
        angle -= 2 * math.pi
    return angle

def main():

    # get port
    host = "localhost"
    port = raw_input("port: ")

    global bzrc
    global constants
    bzrc = BZRC(host, int(port))
    constants = bzrc.get_constants()

    prevTime = time.time()

    # Run the agent

    try:
        while True:
            if time.time() > prevTime + DELTA_TIME:
                tick(time.time() - prevTime)
                prevTime = time.time()

    except KeyboardInterrupt:
        print "Exiting due to keyboard interrupt."
        bzrc.close()


if __name__ == '__main__':
    main()

