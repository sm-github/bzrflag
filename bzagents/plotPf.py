#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

from pFields import Pfield

class Answer(object):
    """BZRC returns an Answer for things like tanks, obstacles, etc.

    You should probably write your own code for this sort of stuff.  We
    created this class just to keep things short and sweet.

    """
    pass
    
if __name__ == '__main__':

	pFields = Pfield()

	fig = plt.figure()
	ax = fig.add_subplot(111)
	 
	# generate grid
	x=np.linspace(-2, 2, 32)
	y=np.linspace(-1.5, 1.5, 24)
	x, y=np.meshgrid(x, y)


	# calculate vector field

	print len(x[0])


	vx = []
	vy = []

	for i in range(0, len(x)):
		rowX = []
		rowY = []
		for j in range(0, len(x[i])):
			tank = Answer()
			tank.x = x[i][j]
			tank.y = y[i][j]
			newX, newY = pFields.attractive(tank, pFields.bases['1'])
			rowX.append(newX)
			rowY.append(rowY)
		vx.append(rowX)
		vy.append(rowY)
		
	vx = np.array(vx)
	vy = np.array(vy)

	'''
	vx= y/np.sqrt(x**2+y**2)*np.exp(-(x**2+y**2))
	vy= x/np.sqrt(x**2+y**2)*np.exp(-(x**2+y**2))
	

	'''

	# plot vector field
	ax.quiver(x, y, vx, vy, pivot='middle', color='r', headwidth=4, headlength=6)
	ax.set_xlabel('x')
	ax.set_ylabel('y')
	plt.show()
	#plt.savefig('visualization_quiver_demo.png')


