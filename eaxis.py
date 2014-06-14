#!/bin/env python

import numpy as np
import scipy.io as sio
import scipy.optimize as spopt
import mytools.slactrac as sltr
import matplotlib.pyplot as plt
import mytools as mt
import copy

def eaxis(camname, *args, **kwargs):
	if camname=='CMOS_FAR':
		# return eaxis = eaxis_CMOS_far(y,res,E0=None,etay=None,etapy=None,ypinch=None,img=None)
		ymotor=kwargs.pop('ymotor')
		return eaxis_CMOS_far(*args,**kwargs)
	elif camname=='ELANEX':
		return eaxis_ELANEX(*args,**kwargs)

def eaxis_ELANEX(y,res,E0=None,etay=None,etapy=None,ypinch=None,img=None,ymotor=None):
	ymotor=np.float64(ymotor)
	ypinch = 130
	print ymotor/res
	y=y+ymotor/res
	ypinch = 130 + (-1e-3)/(4.65e-6)

	# E0=20.35 observed at 130px, motor position -1mm
	E0=20.35

	theta = 6e-3
	Lmag = 2*4.889500000E-01
	Ldrift=8.792573

	out=E_no_eta(y,ypinch,res,Ldrift,Lmag,E0,theta)
	# print out
	return out

def eaxis_CMOS_far(y,res,E0=None,etay=None,etapy=None,img=None):
	# The axis is flipped.  Since the offset is arbitrary and
	# calibrated for below, I can use an arbitrary offset here
	# in order to flip the axis. I've decided on a random value of 4000
	# since I'm pretty sure none of our photos have a resolution
	# greater than that, and I'm trying to error out on a negative
	# value.
	ypinch = 1660
	y_flip_offset = max(y) + 10
	y = y_flip_offset - y
	ypinch = y_flip_offset - ypinch
	if min(y) < 0:
		raise ValueError('y<0 indicates my arbitrary offset is bad. Change source code!')
	if etay==None:
		etay = input('Dispersion in y in mm (eta_y)? ')
		etay = etay * 1e-3
		print 'Dispersion entered is {}'.format(etay)

	if etapy==None:
		etapy = input('Dispersion-prime in y in mrad (eta''_y)? ')
		etapy = etapy * 1e-3
		print 'Dispersion-prime entered is {}'.format(etapy)

	if img!=None:
		plt.imshow(img)
		plt.show()
	if ypinch==None:
		ypinch = input('Location of zero energy in y in pixels? ')

	# E0 = 20.35
	if E0==None:
		E0 = input('Zero energy in GeV? ')
	theta = 6e-3

	Lmag = 2*4.889500000E-01
	Ldrift=8.792573 + 0.8198
	# out = np.zeros(y.shape[0])
	# for i,yval in enumerate(y):
	# 	args=np.array([yval,ypinch,res,E0,theta,Ldrift,Lmag,etay,etapy])
	# 	outval=spopt.minimize(merit_fcn,x0=np.array([20]),args=args)
	# 	out[i]=outval.x[0]
	#
	out=E_no_eta(y,ypinch,res,Ldrift,Lmag,E0,theta)
	# print out
	return out

def merit_fcn(E,ypx,ypinch,res,E0,theta,Ldrift,Lmag,eta0=np.float64(0),etap0=np.float64(0)):
	E=E[0]
	yoffset=yanalytic(E0,E0,theta,Ldrift,Lmag,eta0,etap0) - ypinch*res
	y = ypx*res + yoffset
	yana = yanalytic(E,E0,theta,Ldrift,Lmag,eta0,etap0)

	# print '====================='
	# print E
	# print y
	# print yana
	# print np.power(y-yana,2)*1e14
	# print '====================='
	return np.power(y-yana,2)*1e14

def yanalytic(E,E0,theta,Ldrift,Lmag,eta0,etap0):
	return y_no_eta(E,E0,theta,Ldrift,Lmag) + (E/E0 -1)*(eta0+etap0*(Ldrift+Lmag))

def y_no_eta(E,E0,theta,Ldrift,Lmag):
	return Ldrift/np.sqrt(np.power(E/(E0*np.sin(theta)),2)-1) + (E*Lmag)/(E0*np.sin(theta)) * (1 - np.sqrt(1-np.power(E0*np.sin(theta)/E,2)))

def E_no_eta(ypx,ypinch,res,Ldrift,Lmag,E0,theta):
	yoffset=yanalytic(E0,E0,theta,Ldrift,Lmag,eta0=0,etap0=0) - ypinch*res
	y = ypx*res + yoffset
	return np.sqrt(np.power(Ldrift/y,2)+1)*E0*np.sin(theta)
