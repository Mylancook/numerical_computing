from __future__ import division
from math import pi, sqrt, sin, cos, exp
from numpy import linspace, array, tanh, cosh, ones, arctan
import numpy as np
from scipy.special import erf
from scipy.optimize import root
from scikits import bvp_solver
import matplotlib.pyplot as plt

###################################################################
# Code taken from the matplotlib gallery:
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt

def matplotlib_example(vars):
	if 1:
		# plt.rc("font", size=16)
		host = host_subplot(111, axes_class=AA.Axes)
		plt.subplots_adjust(right=0.75)

		par1 = host.twinx()
		par2 = host.twinx()

		offset = 80
		new_fixed_axis = par2.get_grid_helper().new_fixed_axis
		par2.axis["right"] = new_fixed_axis(loc='right',
											axes=par2,
											offset=(offset, 0))

		par2.axis["right"].toggle(all=True)
		host.set_xlim(0, vars[0][-1])
		host.set_ylim(.26, .38)

		host.set_xlabel("time (sec)",fontsize=24)
		host.set_ylabel("$v$",fontsize=24)
		par1.set_ylabel(r"$\gamma$",fontsize=24)
		par2.set_ylabel(r"$\xi$",fontsize=24)
		p1, = host.plot(vars[0], vars[1], linewidth=2.0,label="velocity")
		p2, = par1.plot(vars[0], vars[2], linewidth=2.0,label="angle of trajectory")
		p3, = par2.plot(vars[0],vars[3], linewidth=2.0,label="altitude")

		par1.set_ylim(-.15,.05)
		par2.set_ylim(.008,.02)
		host.legend(loc='right')
		
		host.axis["left"].label.set_fontsize(18)
		host.axis["left"].label.set_color(p1.get_color())
		par1.axis["right"].label.set_fontsize(18)
		par1.axis["right"].label.set_color(p2.get_color())
		par2.axis["right"].label.set_fontsize(18)
		par2.axis["right"].label.set_color(p3.get_color())

		plt.draw()
		plt.savefig("solutions.pdf")
		plt.show()
		plt.clf()

		
###################################################################
###################################################################
###################################################################



def reentry_init(plot=False):
	R = 209
	beta = 4.26
	rho0 = 2.704e-3
	g = 3.2172e-4
	s = 26600		# 53200;
	T_init = 230
	
	p1, p2, p3 = 1.6, 4, .5 # 1.09835, 6.48578, .347717
	
	#############################################################
	def guess_auxiliary(x):
		out = array([ .5*(.36+.27)-.5*(.36-.27)*tanh(.025*(x-.45*T_init)),
			pi/180*(.5*(-8.1 + 0)-.5*(-8.1 - 0)*tanh(.025*(x-.25*T_init)) ), 
			(1/R)*( .5*(4+2.5)-.5*(4-2.5)*tanh(.03*(x-.3*T_init)) - 
			1.4*cosh(.025*(x-.25*T_init))**(-2) ), 
			p1*ones(x.shape),
			p2*ones(x.shape),
			p3*ones(x.shape)   ])
		return out
	
	#############################################################
	def F(x,y):
		u =	 arctan((6*y[4])/(9*y[0]*y[3] ))
		rho = rho0*exp(-beta*R*y[2])
		out = y[6]*array([
				 -s*rho*y[0]**2*C_d(u) - g*sin(y[1])/(1+y[2])**2,		 # G_0
				( s*rho*y[0]*C_l(u) + y[0]*cos(y[1])/(R*(1 + y[2])) - 
				  g*cos(y[1])/(y[0]*(1+y[2])**2) ),						 # G_1
				y[0]*sin(y[1])/R,										 # G_2
				-( 30*y[0]**2.*sqrt(rho)+ y[3]*(-2*s*rho*y[0]*C_d(u)) + 
				   y[4]*( s*rho*C_l(u) +cos(y[1])/(R*(1 + y[2])) + 
						  g*cos(y[1])/( y[0]**2*(1+y[2])**2 ) 
							) + 
				   y[5]*(sin(y[1])/R)	   ),							 # G_3
				-( y[3]*( -g*cos(y[1])/(1+y[2])**2	) + 
				   y[4]*( -y[0]*sin(y[1])/(R*(1+y[2])) + 
						  g*sin(y[1])/(y[0]*(1+y[2])**2 ) 
							) + 
				   y[5]*(y[0]*cos(y[1])/R )	   ),						 # G_4
				  -( 5*y[0]**3.*sqrt(rho)*(-beta*R) + 
					 y[3]*(s*beta*R*rho*y[0]**2*C_d(u) + 2*g*sin(y[1])/(1+y[2])**3 ) +
					 y[4]*(-s*beta*R*rho*y[0]*C_l(u) - y[0]*cos(y[1])/(R*(1+y[2])**2) + 
						  2*g*cos(y[1])/(y[0]*(1+y[2])**3) 
						  )
						  ),											 # G_5
					0 # T' = 0											 # G_6
			   ])
		return out

	#############################################################
	def F_auxiliary(x,y):
		u = y[3]*erf( y[4]*(y[5]-x/T_init) )
		rho = rho0*exp(-beta*R*y[2])
		out = array([-s*rho*y[0]**2*C_d(u) - g*sin(y[1])/(1+y[2])**2,
					  ( s*rho*y[0]*C_l(u) + y[0]*cos(y[1])/(R*(1 + y[2])) - 
					  g*cos(y[1])/(y[0]*(1+y[2])**2) ),
					  y[0]*sin(y[1])/R,
					  0,
					  0,
					  0		])
		return out
	
	#############################################################
	def bc2_auxiliary(ya,yb):
		out1 = array([ ya[0]-.36,
					  ya[1]+8.1*pi/180,
					  ya[2]-4/R
					  ])
		out2 = array([ yb[0]-.27,
					  yb[1],
					  yb[2]-2.5/R
					  ])
		return out1, out2
	
	#############################################################
	def bc2(ya,yb):
		out1 = array([ ya[0]-.36,
					  ya[1]+8.1*pi/180,
					  ya[2]-4/R
					  ])
		out2 = array([yb[0]-.27,
					  yb[1],
					  yb[2]-2.5/R,
					  H(yb)
					  ])
		return out1, out2
	
	#############################################################
	def H(y):
		u =	 arctan((6*y[4])/(9*y[0]*y[3] )) 
		rho = rho0*exp(-beta*R*y[2])

		out = (  10*y[0]**3*sqrt(rho) + 
					y[3]*(-s*rho*y[0]**2*C_d(u) - g*sin(y[1])/(1+y[2])**2 ) + 
					y[4]*(	s*rho*y[0]*C_l(u) + y[0]*cos(y[1])/(R*(1 + y[2])) - 
							g*cos(y[1])/(y[0]*(1+y[2])**2)
							) + 
					y[5]*y[0]*sin(y[1])/R   )
		return out
	
	#############################################################
	def C_d(u):
		return 1.174 - 0.9*cos(u)

	def C_l(u):
		return 0.6*sin(u)


	auxiliary_problem = bvp_solver.ProblemDefinition(num_ODE = 6,
										  num_parameters = 0,
										  num_left_boundary_conditions = 3,
										  boundary_points = (0., T_init),
										  function = F_auxiliary,
										  boundary_conditions = bc2_auxiliary)
									
	auxiliary_solution = bvp_solver.solve(auxiliary_problem,
								solution_guess = guess_auxiliary)
	
	# plt.rc("font", size=16)
	
	# x0 = linspace(0,T_init,120)
	# y0 = guess_auxiliary(x0)
	# plt.plot(x0,y0[1,:],'-k',linewidth=2.0)
	# plt.ylabel('$v$'); plt.show(); plt.clf()
	#
	# plt.plot(x0,180/pi*y0[2,:],'-b',linewidth=2.0)
	# plt.ylabel('$\gamma$'); plt.show(); plt.clf()
	#
	# plt.plot(x0,R*y0[3,:],'-g',linewidth=2.0)
	# plt.ylabel('$h$'); plt.show(); plt.clf()


	# xint = linspace(0,T_init,120)
	# yint = solution(xint)
	# g = guess_auxiliary(xint)
	# for j in range(3):
	#	plt.plot(xint,np.real(yint[j,:]),'-k',linewidth=2.0)
	#	plt.plot(xint,g[j,:],'-r',linewidth=2.0)
	# plt.xlabel('$x$')
	# plt.ylabel('$y$')
	# plt.show()
	N = 240 # Number of subintervals
	xint_guess = linspace(0,T_init,N+1)
	yint_guess = auxiliary_solution(xint_guess)
	if plot==True:
		# Plot guess for v
		plt.plot(xint_guess,np.real(yint_guess[0,:]),'-k',linewidth=2.0)
		plt.xlabel('$t$',fontsize=18); plt.ylabel('$v$',fontsize=18)
		plt.savefig('guess_v.pdf')
		plt.show(); plt.clf()
		
		# Plot guess for gamma
		plt.plot(xint_guess,np.real(yint_guess[1,:]),'-k',linewidth=2.0)
		plt.xlabel('$t$',fontsize=18); plt.ylabel(r'$\gamma$',fontsize=18)
		plt.savefig('guess_gamma.pdf')
		plt.show(); plt.clf()
		
		# Plot guess for xi
		plt.plot(xint_guess,np.real(yint_guess[2,:]),'-k',linewidth=2.0)
		plt.xlabel('$t$',fontsize=18); plt.ylabel(r'$\xi$',fontsize=18)
		plt.savefig('guess_xi.pdf')
		plt.show(); plt.clf()
		
		# Plot guess for control u
		p1, p2, p3 = yint_guess[3,0], yint_guess[4,0], yint_guess[5,0]
		plt.plot(xint_guess,p1*erf( p2*(p3-xint_guess/T_init) ),'-k',linewidth=2.0)
		plt.xlabel('$t$',fontsize=18); plt.ylabel(r'$u$',fontsize=18)
		plt.savefig('guess_u.pdf')
		plt.show(); plt.clf()
	
	
	xint = linspace(0,T_init,N+1)
	yint = auxiliary_solution(xint)
	yint = np.concatenate( (yint,T_init*np.ones((1,N+1))) ,axis=0)
	yint[3,:] = -1
	p1, p2, p3 = yint[3,0], yint[4,0], yint[5,0]
	u = p1*erf( p2*(p3-xint/T_init) )
	
	yint[4,:] = 1.5*yint[0,:]*yint[3,:]*np.tan(u)
	
	for j in range(len(yint[5,:])):
		y = yint[:6,j]
		def new_func(x):
			if y[1] < 0 and y[1] > -.05: y[1] = -.05
			if y[1] > 0 and y[1] < .05: y[1] = .05
			y[5] = x
			return H(y)
		if j>0:
			sol = root(new_func,-8)
			if sol.success == True: yint[5,j] = sol.x
			else: yint[5,j] = yint[5,j-1]
		else: 
			sol = root(new_func,-8)
			if sol.success == True: yint[5,0] = sol.x
	# yint[5,:] = -yint[5,:]
	plt.plot(xint,yint[5,:])
	plt.show(); plt.clf()
	
	
	# assert 1>2
	# print bvp_solver.solve.__doc__
	original_problem = bvp_solver.ProblemDefinition(num_ODE = 7,			   
										  num_parameters = 0,				   
										  num_left_boundary_conditions = 3,	   
										  boundary_points = (0., 1),		   
										  function = F,				 
										  boundary_conditions = bc2) 
									
	original_solution = bvp_solver.solve(original_problem,
								solution_guess = yint,
								initial_mesh = linspace(0,1,N+1),
								max_subintervals=10000,
								trace = 0)
	# # For more info on the available options for these methods, run
	# print bvp_solver.ProblemDefinition.__doc__
	# print bvp_solver.solve.__doc__
	
	xint = linspace(0,1,N+1)
	yint = original_solution(xint)
	if plot==True:
		# Plot guess for v
		plt.plot(xint_guess,np.real(yint_guess[0,:]),'-r',linewidth=2.0)
		plt.plot(xint_guess,np.real(yint[0,:]),'-k',linewidth=2.0)
		plt.xlabel('$t$',fontsize=18); plt.ylabel('$v$',fontsize=18)
		plt.savefig('solution_v.pdf')
		plt.show(); plt.clf()
		
		# Plot guess for gamma
		plt.plot(xint_guess,np.real(yint_guess[1,:]),'-r',linewidth=2.0)
		plt.plot(xint_guess,np.real(yint[1,:]),'-k',linewidth=2.0)
		plt.xlabel('$t$',fontsize=18); plt.ylabel(r'$\gamma$',fontsize=18)
		plt.savefig('solution_gamma.pdf')
		plt.show(); plt.clf()
		
		# Plot guess for xi
		plt.plot(xint_guess,np.real(yint_guess[2,:]),'-r',linewidth=2.0)
		plt.plot(xint_guess,np.real(yint[2,:]),'-k',linewidth=2.0)
		plt.xlabel('$t$',fontsize=18); plt.ylabel(r'$\xi$',fontsize=18)
		plt.savefig('solution_xi.pdf')
		plt.show(); plt.clf()
		
		# Plot guess for control u
		u =	 arctan((6*yint[4,:])/(9*yint[0,:]*yint[3,:] )) 
		p1, p2, p3 = yint_guess[3,0], yint_guess[4,0], yint_guess[5,0]
		plt.plot(xint_guess,p1*erf( p2*(p3-xint_guess/T_init) ) ,'-r',linewidth=2.0)
		plt.plot(xint_guess,u,'-k',linewidth=2.0)
		plt.xlabel('$t$',fontsize=18); plt.ylabel(r'$u$',fontsize=18)
		plt.savefig('solution_u.pdf')
		plt.show(); plt.clf()
	
	
	# return auxiliary_solution
	xint = linspace(0,yint[6,0],N+1)
	u =	 arctan((6*yint[4,:])/(9*yint[0,:]*yint[3,:] )) 
	return (xint,yint[0,:], yint[1,:], yint[2,:], yint[3,:], yint[4,:], yint[5,:], u)











# def bvp_solver_example():
# 	"""
# 	Using scikits.bvp_solver to solve the bvp
# 	"""
# 	epsilon = .1
# 	lbc, rbc = 0., 1.
#
# 	def function1(x , y):
# 		return np.array([y[1] , (4./epsilon)*(pi-x**2.)*y[0] + 1./epsilon*np.cos(x) ])
#
#
# 	def boundary_conditions(ya,yb):
# 		return (np.array([ya[0] - lbc]),
# 				np.array([yb[0] - rbc]))
#
# 	problem = bvp_solver.ProblemDefinition(num_ODE = 2,
# 										  num_parameters = 0,
# 										  num_left_boundary_conditions = 1,
# 										  boundary_points = (0., pi/2.),
# 										  function = function1,
# 										  boundary_conditions = boundary_conditions)
#
# 	solution = bvp_solver.solve(problem,
# 								solution_guess = (1.,
# 												  0.))
#
# 	A = np.linspace(0.,pi/2., 200)
# 	T = solution(A)
# 	plt.plot(A, T[0,:],'-k',linewidth=2.0)
# 	plt.show()
# 	plt.clf()
# 	return


def reentry(x_guess,guess,N=240,plot=False):
	R = 209
	beta = 4.26
	rho0 = 2.704e-3
	g = 3.2172e-4
	s = 26600	
	T_init = x_guess[-1]
	
	def C_d(u): return 1.174 - 0.9*cos(u)

	def C_l(u): return 0.6*sin(u)
	
	#############################################################
	def ode(x,y):
		u =	 arctan((6*y[4])/(9*y[0]*y[3] ))
		rho = rho0*exp(-beta*R*y[2])
		out = y[6]*array([
				 -s*rho*y[0]**2*C_d(u) - g*sin(y[1])/(1+y[2])**2,		 # G_0
				( s*rho*y[0]*C_l(u) + y[0]*cos(y[1])/(R*(1 + y[2])) - 
				  g*cos(y[1])/(y[0]*(1+y[2])**2) ),						 # G_1
				y[0]*sin(y[1])/R,										 # G_2
				-( 30*y[0]**2.*sqrt(rho)+ y[3]*(-2*s*rho*y[0]*C_d(u)) + 
				   y[4]*( s*rho*C_l(u) +cos(y[1])/(R*(1 + y[2])) + 
						  g*cos(y[1])/( y[0]**2*(1+y[2])**2 ) 
							) + 
				   y[5]*(sin(y[1])/R)	   ),							 # G_3
				-( y[3]*( -g*cos(y[1])/(1+y[2])**2	) + 
				   y[4]*( -y[0]*sin(y[1])/(R*(1+y[2])) + 
						  g*sin(y[1])/(y[0]*(1+y[2])**2 ) 
							) + 
				   y[5]*(y[0]*cos(y[1])/R )	   ),						 # G_4
				  -( 5*y[0]**3.*sqrt(rho)*(-beta*R) + 
					 y[3]*(s*beta*R*rho*y[0]**2*C_d(u) + 2*g*sin(y[1])/(1+y[2])**3 ) +
					 y[4]*(-s*beta*R*rho*y[0]*C_l(u) - y[0]*cos(y[1])/(R*(1+y[2])**2) + 
						  2*g*cos(y[1])/(y[0]*(1+y[2])**3) 
						  )
						  ),											 # G_5
					0 # T' = 0											 # G_6
			   ])
		return out
	
	#############################################################
	def bcs(ya,yb):
		out1 = array([ ya[0]-.36,
					  ya[1]+8.1*pi/180,
					  ya[2]-4/R
					  ])
		out2 = array([yb[0]-.27,
					  yb[1],
					  yb[2]-2.5/R,
					  H(yb)
					  ])
		return out1, out2
	
	#############################################################
	def H(y):
		u =	 arctan((6*y[4])/(9*y[0]*y[3] )) 
		rho = rho0*exp(-beta*R*y[2])

		out = (  10*y[0]**3*sqrt(rho) + 
					y[3]*(-s*rho*y[0]**2*C_d(u) - g*sin(y[1])/(1+y[2])**2 ) + 
					y[4]*(	s*rho*y[0]*C_l(u) + y[0]*cos(y[1])/(R*(1 + y[2])) - 
							g*cos(y[1])/(y[0]*(1+y[2])**2)
							) + 
					y[5]*y[0]*sin(y[1])/R   )
		return out
	
	#############################################################
	
	yint = np.concatenate( (guess,T_init*np.ones((1,len(x_guess)))) ,axis=0)
	yint[3,:] = -1
	p1, p2, p3 = yint[3,0], yint[4,0], yint[5,0]
	u = p1*erf( p2*(p3-x_guess/T_init) )
	
	yint[4,:] = 1.5*yint[0,:]*yint[3,:]*np.tan(u)
	
	for j in range(len(yint[5,:])):
		y = yint[:6,j]
		def new_func(x):
			if y[1] < 0 and y[1] > -.05: y[1] = -.05
			if y[1] > 0 and y[1] < .05: y[1] = .05
			y[5] = x
			return H(y)
		sol = root(new_func,-8)
		if j>0:
			if sol.success == True: yint[5,j] = sol.x
			else: yint[5,j] = yint[5,j-1]
		else: 
			if sol.success == True: yint[5,0] = sol.x
	plt.plot(x_guess,yint[5,:])
	plt.show(); plt.clf()
	
	problem = bvp_solver.ProblemDefinition(num_ODE = 7,			   
										  num_parameters = 0,				   
										  num_left_boundary_conditions = 3,	   
										  boundary_points = (0., 1),		   
										  function = ode,				 
										  boundary_conditions = bcs) 
									
	solution = bvp_solver.solve(problem,
								solution_guess = yint,
								initial_mesh = linspace(0,1,len(x_guess)),
								max_subintervals=1000,
								trace = 1)
	# # For more info on the available options for these methods, run
	# print bvp_solver.ProblemDefinition.__doc__
	# print bvp_solver.solve.__doc__
	
	numerical_soln = solution(linspace(0,1,N+1))
	u =	 arctan((6*numerical_soln[4,:])/(9*numerical_soln[0,:]*numerical_soln[3,:] )) 
	domain = linspace(0,numerical_soln[6,0],N+1)
	
	if plot==True:
		# Plot guess for v
		plt.plot(x_guess,np.real(guess[0,:]),'-r',linewidth=2.0)
		plt.plot(domain,np.real(numerical_soln[0,:]),'-k',linewidth=2.0)
		plt.xlabel('$t$',fontsize=18); plt.ylabel('$v$',fontsize=18)
		plt.savefig('solution_v.pdf')
		plt.show(); plt.clf()
		
		# Plot guess for gamma
		plt.plot(x_guess,np.real(guess[1,:]),'-r',linewidth=2.0)
		plt.plot(domain,np.real(numerical_soln[1,:]),'-k',linewidth=2.0)
		plt.xlabel('$t$',fontsize=18); plt.ylabel(r'$\gamma$',fontsize=18)
		plt.savefig('solution_gamma.pdf')
		plt.show(); plt.clf()
		
		# Plot guess for xi
		plt.plot(x_guess,np.real(guess[2,:]),'-r',linewidth=2.0)
		plt.plot(domain,np.real(numerical_soln[2,:]),'-k',linewidth=2.0)
		plt.xlabel('$t$',fontsize=18); plt.ylabel(r'$\xi$',fontsize=18)
		plt.savefig('solution_xi.pdf')
		plt.show(); plt.clf()
		
		# Plot guess for control u
		p1, p2, p3 = guess[3,0], guess[4,0], guess[5,0]
		plt.plot(x_guess,p1*erf( p2*(p3-x_guess/T_init) ) ,'-r',linewidth=2.0)
		plt.plot(domain,u,'-k',linewidth=2.0)
		plt.xlabel('$t$',fontsize=18); plt.ylabel(r'$u$',fontsize=18)
		plt.savefig('solution_u.pdf')
		plt.show(); plt.clf()
	
	return ( domain, numerical_soln[0,:], numerical_soln[1,:], numerical_soln[2,:], 
			 numerical_soln[3,:], numerical_soln[4,:], numerical_soln[5,:], u )


def reentry_auxiliary_problem(N=240,plot=True):
	R = 209
	beta = 4.26
	rho0 = 2.704e-3
	g = 3.2172e-4
	s = 26600	
	T_init = 230
	
	def C_d(u): return 1.174 - 0.9*cos(u)

	def C_l(u): return 0.6*sin(u)
	
	# p1, p2, p3 = 1.2, 4, .5 # 1.09835, 6.48578, .347717
	p1, p2, p3 = 1.3, 4.5, .5
	# # Plot initial guess for control u in the auxiliary problem
	# x_array = linspace(0,T_init,100)
	# plt.plot(x_array,p1*erf( p2*(p3-x_array/T_init) ),'-k',linewidth=2.0)
	# plt.show(); plt.clf()
	
	#############################################################
	def guess_auxiliary(x):
		out = array([ .5*(.36+.27)-.5*(.36-.27)*tanh(.025*(x-.45*T_init)),
			pi/180*(.5*(-8.1 + 0)-.5*(-8.1 - 0)*tanh(.025*(x-.25*T_init)) ), 
			(1/R)*( .5*(4+2.5)-.5*(4-2.5)*tanh(.03*(x-.3*T_init)) - 
			1.4*cosh(.025*(x-.25*T_init))**(-2) ), 
			p1*ones(x.shape),
			p2*ones(x.shape),
			p3*ones(x.shape)   ])
		return out
	
	#############################################################
	def ode_auxiliary(x,y):
		u = y[3]*erf( y[4]*(y[5]-x/T_init) )
		rho = rho0*exp(-beta*R*y[2])
		out = array([-s*rho*y[0]**2*C_d(u) - g*sin(y[1])/(1+y[2])**2,
					  ( s*rho*y[0]*C_l(u) + y[0]*cos(y[1])/(R*(1 + y[2])) - 
					  g*cos(y[1])/(y[0]*(1+y[2])**2) ),
					  y[0]*sin(y[1])/R,
					  0,
					  0,
					  0		])
		return out
	
	#############################################################
	def bcs_auxiliary(ya,yb):
		out1 = array([ ya[0]-.36,
					  ya[1]+8.1*pi/180,
					  ya[2]-4/R
					  ])
		out2 = array([ yb[0]-.27,
					  yb[1],
					  yb[2]-2.5/R
					  ])
		return out1, out2
	
	#############################################################
	
	problem_auxiliary = bvp_solver.ProblemDefinition(num_ODE = 6,
										  num_parameters = 0,
										  num_left_boundary_conditions = 3,
										  boundary_points = (0., T_init),
										  function = ode_auxiliary,
										  boundary_conditions = bcs_auxiliary)
									
	solution_auxiliary = bvp_solver.solve(problem_auxiliary,
								solution_guess = guess_auxiliary)
								
	# N = 240 # Number of subintervals
	xint_guess = linspace(0,T_init,N+1)
	yint_guess = solution_auxiliary(xint_guess)
	if plot==True:
		# Plot guess for v
		plt.plot(xint_guess,np.real(yint_guess[0,:]),'-k',linewidth=2.0)
		plt.xlabel('$t$',fontsize=18); plt.ylabel('$v$',fontsize=18)
		plt.savefig('guess_v.pdf')
		plt.show(); plt.clf()
		
		# Plot guess for gamma
		plt.plot(xint_guess,np.real(yint_guess[1,:]),'-k',linewidth=2.0)
		plt.xlabel('$t$',fontsize=18); plt.ylabel(r'$\gamma$',fontsize=18)
		plt.savefig('guess_gamma.pdf')
		plt.show(); plt.clf()
		
		# Plot guess for xi
		plt.plot(xint_guess,np.real(yint_guess[2,:]),'-k',linewidth=2.0)
		plt.xlabel('$t$',fontsize=18); plt.ylabel(r'$\xi$',fontsize=18)
		plt.savefig('guess_xi.pdf')
		plt.show(); plt.clf()
		
		# Plot guess for control u
		p1, p2, p3 = yint_guess[3,0], yint_guess[4,0], yint_guess[5,0]
		plt.plot(xint_guess,p1*erf( p2*(p3-xint_guess/T_init) ),'-k',linewidth=2.0)
		plt.xlabel('$t$',fontsize=18); plt.ylabel(r'$u$',fontsize=18)
		plt.savefig('guess_u.pdf')
		plt.show(); plt.clf()
	
	
	return xint_guess, yint_guess


def plot_u_guess():
	
	a = pi/2.*(3./4)
	b = -a
	
	plt.plot([0,.5],[a,a],'-k',linewidth=2.0)
	plt.plot([.5,1],[b,b],'-k',linewidth=2.0)
	plt.show(); plt.clf()
	p1, p2, p3 = 1.3, 4.5, .5 # 1.09835, 6.48578, .347717
	
	# # Plot initial guess for control u in the auxiliary problem
	T_guess = 230
	x_array = linspace(0,T_guess,100)
	plt.plot([0,.5*T_guess],[a,a],'-r',linewidth=2.0)
	plt.plot([.5*T_guess,T_guess],[b,b],'-r',linewidth=2.0)
	plt.plot(x_array,p1*erf( p2*(p3-x_array/T_guess) ),'-k',linewidth=2.0)
	plt.yticks([-pi/2.,0, pi/2],
	           [r'$-\frac{\pi}{2}$', '$0$', r'$-\frac{\pi}{2}$'])
	plt.savefig('u_heuristic_smooth.pdf')
	plt.show(); plt.clf()
	
	return

if __name__ == "__main__":
	# bvp_solver_example()
	# reentry_init(plot=True)
	
	# soln = reentry_init(plot=True)
	# matplotlib_example(soln)
	
	# x,y = reentry_auxiliary_problem(240)
	# soln = reentry(x,y,plot=True)
	# matplotlib_example(soln)
	
	plot_u_guess()