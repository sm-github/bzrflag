#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

ax = plt.figure().add_subplot(111)
ax.axis([-400,400,-400,400])
ax.set_xlabel('x')
ax.set_ylabel('y')

'''
sigma_x = 70
sigma_y = 100
rho = 0.3

mean = [0,0]
cov = [
	[sigma_x**2,rho*sigma_x*sigma_y],
	[rho*sigma_x*sigma_y,sigma_y**2]] # diagonal covariance, points lie on x or y-axis
'''

def plotMultivariate (mean, a, b):

	cov = [[a, 0],[0, b]] #a = height; b = width

	x,y = np.random.multivariate_normal(mean,cov,1000).T
	plt.plot(x,y,'x')
	plt.show()

def plotBivariate ():
	# generate grid
	x = np.linspace(-400, 400, 100)
	y = np.linspace(-400, 400, 100)
	x, y = np.meshgrid(x, y)

	sigma_x = 70
	sigma_y = 200

	Z = plt.mlab.bivariate_normal(x, y, sigma_x, sigma_y)

	# plt.figure()
	CS = plt.contour(x, y, Z)
	plt.show()


plotMultivariate([0,0], 400, 800)
plotBivariate()


# plt.show()
# plt.savefig('./plots/attrField.png')

