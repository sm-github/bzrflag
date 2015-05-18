#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

from pFields import Pfield

class Tank(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.flag = 'die'
    pass
    
def limiter (value):
    if value < -10:
        return -10
    if value > 10:
        return 10
    
    return value
        
    
if __name__ == '__main__':
    
    # 1 - red, 2 - green, 3 - blue, 4 - purple
    TARGET = '1'
    
    MAP_NAME = '../maps/four_ls.bzw'
    #MAP_NAME = '../maps/rotated_box_world.bzw'

    pFields = Pfield('3', MAP_NAME)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.axis([-400,400,-400,400]) 
    # generate grid
    x=np.linspace(-400, 400, 30)
    y=np.linspace(-400, 400, 30)
    # x, y=np.meshgrid(x, y)

    base =  pFields.bases[TARGET]
    
    '''

    # plot attractive field
    for r in range(0, len(x)):
        for c in range(0, len(y)):
            tank = Tank(x[r], y[c])
            newX, newY = pFields.attractive(tank, base)
            ax.arrow(x[r], y[c], limiter(newX), limiter(newY), head_width=4, head_length=6)

	'''
    
    circ = plt.Circle((base.x, base.y), base.r, fc='r')
    plt.gca().add_patch(circ)


    #plot repulsive or tangential field
    for r in range(0, len(x)):
        for c in range(0, len(y)):
            tank = Tank(x[r], y[c])
            #newX, newY = pFields.attractive(tank, base)
            newX, newY = pFields.repulsive(tank, base)
            ax.arrow(x[r], y[c], limiter(newX), limiter(newY), head_width=4, head_length=6)


    for o in pFields.obstacles:
        plt.gca().add_patch(plt.Circle((o.x, o.y), o.r, fc='g'))
        
	'''
    #plot the combined fields
    for r in range(0, len(x)):
        for c in range(0, len(y)):
            tank = Tank(x[r], y[c])
            newX, newY = pFields.attractive(tank, base)
            repX, repY = pFields.repulsive(tank, base)
            ax.arrow(x[r], y[c], limiter(newX+ repX), limiter(newY + repY), head_width=4, head_length=6)
	'''
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    plt.show()
    plt.savefig('./plots/attrField.png')


