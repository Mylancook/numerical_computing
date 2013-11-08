# import matplotlib
# matplotlib.rcParams = matplotlib.rc_params_from_file('../../matplotlibrc')
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import ode

#--------------------------------------------------------------
# Good example of the secant method. Code given in lab.
def Example1(): 
# y'' +4y = -9sin(x), y(0) = 1., y(3*pi/4.) = -(1.+3*sqrt(2))/2., y'(0) = -2
# Exact Solution: y(x) = cos(2x) + (1/2)sin(2x) - 3sin(x)
	
	a, b = 0., 3*np.pi/4.
	alpha, beta =  1., -(1.+3*np.sqrt(2))/2.
	t0,t1 = 3., 1.
	dim, iterate = 2,10
	reltol, abstol = 1e-9,1e-8
	def ode_f(x,y): return np.array([y[1] , -4.*y[0] - 9.*np.sin(x)])
	
	
	print '\nj = 1','\nt = ', t0
	
	for j in range(2,iterate):
		print '\nj = ', j,'\nt = ', t1
		
		if j >2: 
			y0 = y1			# Update
		else:
			example = ode(ode_f).set_integrator('dopri5',atol=abstol,rtol=reltol) 
			example.set_initial_value(np.array([alpha,t0]),a) 
			y0 = example.integrate(b)[0]
			
		example = ode(ode_f).set_integrator('dopri5',atol=abstol,rtol=reltol) 
		example.set_initial_value(np.array([alpha,t1]),a) 
		y1 = example.integrate(b)[0]
		if abs(y1-beta)<1e-8: 
			print '\n--Solution y computed successfully--',\
			'\n|y(b) - beta| = ',np.abs(beta-y1),'\n'
			break
		
		t2 = t1 - (y1 - beta)*(t1-t0)/(y1- y0)
		t0 = t1
		t1 = t2
	
	# Plots the solution
	example = ode(ode_f).set_integrator('dopri5',atol=abstol,rtol=reltol)
	example.set_initial_value(np.array([alpha,t1]),a) 
	X = np.linspace(a,b,401)
	Y = np.zeros((len(X),dim))
	Y[0,:] = np.array([alpha, t1])
	
	for j in range(1,len(X)): 
		Y[j,:] = example.integrate(X[j]) 
	plt.plot(X,Y[:,0],'-k')
	plt.show()
	return 


#--------------------------------------------------------------
# Good example of Newton's method. Code given in lab.
def Example2():
	a, b = 0., 3*np.pi/4.
	alpha, beta =  1., -(1.+3*np.sqrt(2))/2.
	dim, iterate = 4,10
	reltol, abstol,TOL = 1e-9,1e-8,1e-9
	t = (beta-alpha)/(b-a)  # Initial guess for the slope y'(1)
	def ode_f(x,y): 
		return np.array([y[1], -4.*y[0] - 9.*np.sin(x), 
						 y[3],  -4.*y[2]                  ])
	
	
	for j in range(1,iterate):
		print '\nj = ', j,'\nt = ', t
		
		example = ode(ode_f).set_integrator('dopri5',atol=abstol,rtol=reltol,nsteps=5000) 
		example.set_initial_value(np.array([alpha,t,0.,1.]),a) 
		X = example.integrate(b)
		y0, z0 = X[0],X[2]
		
		if abs(y0-beta)<TOL: 
			print '\n--Solution y computed successfully--',\
			'\n|y(b) - beta| = ',np.abs(beta-y0),'\n'
			break
		t = t - (y0 - beta)/z0   # Update guess y'(1) = t
		
	# Plot the computed solution vs. the analytic solution
	example = ode(ode_f).set_integrator('dopri5',atol=abstol,rtol=reltol)
	example.set_initial_value(np.array([alpha,t,0.,1.]),a) 
	T = np.linspace(a,b,401)
	Y = np.zeros((len(T),dim))
	Y[0,:] = np.array([alpha,t,0.,1.])
	
	for j in range(1,len(T)): 
		Y[j,:] = example.integrate(T[j])  
	plt.plot(T[::20],Y[::20,0],'*k')			# Numerical Solution
	Y2 = np.cos(2*T) + (1/2.)*np.sin(2*T) - 3.*np.sin(T)
	plt.plot(T,Y2,'-r')							# Exact Solution
	plt.show()	
	return


#--------------------------------------------------------------
# y''=6y**2-6x**4-10, x in [1,3]
# Solution is y=x**2 + x**(-2), y'(x) = 2x -2x^(-3), y'(1) = 0 
# Shooting Algorithm: Converges for t0 in [-.1,.25]
# If the interval is [1,2], convergence occurs for t0 in [-1.4,3.9]
def Exercise1(t):
	def ode_f(x,y): 
		return np.array([y[1], 2. + 6.*y[0]**2.-12.*x**2.*y[0]+6.*x**4., 
						 y[3],  12.*(y[0]-x**2.)*y[2]                  ])
	
	a,b = 1.,2.
	alpha, beta = 2., b**2 + b**(-2) # 4.+(1./4.)
	reltol, abstol = 1e-9,1e-9
	iterate = 15
	# t = .01  # Initial guess for the slope y'(1)
	
	# Plot the solution of the IVP with initial slope t
	def ode_f2(x,y): 
		return np.array([y[1], 2. + 6.*y[0]**2.-12.*x**2.*y[0]+6.*x**4.])
	
	example = ode(ode_f2).set_integrator('dopri5',atol=abstol,rtol=reltol)
	example.set_initial_value(np.array([alpha,t]),a) 
	T = np.linspace(a,b,401)
	dim=2
	Y = np.zeros((len(T),dim))
	Y[0,:] = np.array([alpha,t])
	
	for j in range(1,len(T)): 
		Y[j,:] = example.integrate(T[j])  
	plt.plot(T,Y[:,0],'-g')
	# plt.show()
	# plt.clf()
	
	for j in range(1,iterate):
		print '\nj = ', j,'\nt = ', t
		
		example1 = ode(ode_f).set_integrator('dopri5',atol=abstol,rtol=reltol,nsteps=5000) 
		example1.set_initial_value(np.array([alpha,t,0.,1.]),a) 
		X = example1.integrate(b)
		y0, z0 = X[0],X[2]
		
		if abs(y0-beta)<1e-9: 
			print '\n--Solution y computed successfully--',\
			'\n|y(b) - beta| = ',np.abs(beta-y0),'\n'
			break
		t = t - (y0 - beta)/z0   # Update guess y'(1) = t
		
	# Plot the computed solution vs. the analytic solution
	example = ode(ode_f).set_integrator('dopri5',atol=abstol,rtol=reltol)
	example.set_initial_value(np.array([alpha,t,0.,1.]),a) 
	T = np.linspace(a,b,401)
	dim=4
	Y = np.zeros((len(T),dim))
	Y[0,:] = np.array([alpha,t,0.,1.])
	
	for j in range(1,len(T)): 
		Y[j,:] = example.integrate(T[j])  
	plt.plot(T[::10],Y[::10,0],'*k')
	Y2 = T**2+T**(-2)
	plt.plot(T,Y2,'-r')
	plt.show()	
	return



#--------------------------------------------------------------
# y''(x) = 3 + 2*y/x^2, x  in [1,e], y(1) = 6, y(e)= e^2 + 6/e
def Exercise2():
	# Exact Solution: y(x) = x^2*ln(x)+6*x^(-1)
	# y'(x) = 2xln(x) + x^2*(1/x) - 6x^(-2)
	# y'(x) = 2xln(x) + x - 6x^(-2)
	# y''(x)= 2 ln(x)+2+1 +12x^(-3)
	# y''(x) = 3 + 2*y/x^2
	def ode_f(x,y): 
		return np.array([y[1] , 3+2.*y[0]/x**2.,y[3],
			(2./x**2.)*y[2] ])
	
	a,b = 1.,np.exp(1.)
	alpha, beta = 6.,np.exp(2.) + 6.*np.exp(-1.)
	t = 150.
	abstol, reltol = 1e-9, 1e-9
	iterate = 15
	
	for j in range(1,iterate):
		print '\nj = ', j,'\nt = ', t
		
		example1 = ode(ode_f).set_integrator('dopri5',atol=abstol,rtol=reltol,nsteps=5000) 
		example1.set_initial_value(np.array([alpha,t,0.,1.]),a) 
		X = example1.integrate(b)
		y0, z0 = X[0],X[2]
		
		if abs(y0-beta)<1e-9: 
			print '\n--Solution y computed successfully--',\
			'\n|y(b) - beta| = ',np.abs(beta-y0),'\n'
			break
		t = t - (y0 - beta)/z0   # Update guess y'(1) = t
		
	example = ode(ode_f).set_integrator('dopri5',atol=abstol,rtol=reltol)
	example.set_initial_value(np.array([alpha,t,0.,1.]),a) 
	T = np.linspace(a,b,401)
	dim=4
	Y = np.zeros((len(T),dim))
	Y[0,:] = np.array([alpha,t,0.,1.])
	
	for j in range(1,len(T)): 
		Y[j,:] = example.integrate(T[j])  
	plt.plot(T[::20],Y[::20,0],'*k')
	Y2 = (T**2.)*np.log(T)+6*(T**(-1.))
	plt.plot(T,Y2,'-r')
	plt.show()	
	return


#--------------------------------------------------------------
def Exercise3(t0,t1): 
# y'' +4y = -9sin(x), y(0) = 1., y(3*pi/4.) = -(1.+3*sqrt(2))/2., y'(0) = -2
# Exact Solution: y(x) = cos(2x) + (1/2)sin(2x) - 3sin(x)
	
	a, b = 0., 4.*np.pi/4.
	alpha, beta =  1., 1.#np.cos(2.*b) + (1./2.)*np.sin(2.*b) - 3.*np.sin(b)
	# t0,t1 = 3., 1.
	dim, iterate = 2,10
	reltol, abstol = 1e-9,1e-8
	def ode_f(x,y): return np.array([y[1] , -4.*y[0] - 9.*np.sin(x)])
	
	print '\nj = 1','\nt = ', t0
	
	for j in range(2,iterate):
		print '\nj = ', j,'\nt = ', t1
		if j >2: 
			y0 = y1			# Update
		else:
			example = ode(ode_f).set_integrator('dopri5',atol=abstol,rtol=reltol) 
			example.set_initial_value(np.array([alpha,t0]),a) 
			y0 = example.integrate(b)[0]
				
		example = ode(ode_f).set_integrator('dopri5',atol=abstol,rtol=reltol) 
		example.set_initial_value(np.array([alpha,t1]),a) 
		y1 = example.integrate(b)[0]
		if abs(y1-beta)<1e-8: 
			print '\n--Solution y computed successfully--',\
			'\n|y(b) - beta| = ',np.abs(beta-y1),'\n'
			break
		t2 = t1 - (y1 - beta)*(t1-t0)/(y1- y0)
		t0 = t1
		t1 = t2		
	# Plots the solution
	example = ode(ode_f).set_integrator('dopri5',atol=abstol,rtol=reltol)
	example.set_initial_value(np.array([alpha,t1]),a) 
	X = np.linspace(a,b,401)
	Y = np.zeros((len(X),dim))
	Y[0,:] = np.array([alpha, t1])
		
	for j in range(1,len(X)): 
		Y[j,:] = example.integrate(X[j]) 
	
	Y2 = np.cos(2.*X) + (1./2.)*np.sin(2.*X) - 3.*np.sin(X)
	plt.plot(X[::10],Y[::10,0],'-*k')
	plt.plot(X,Y2,'-r')
	plt.show()
	return 


#--------------------------------------------------------------
def Exercise4(ya,va,nu,t0,t1): 
	a, b = 0., 120.
	beta =  0.
	# ya, va = 0.,35.
	# t0,t1 = np.pi/6., np.pi/7
	dim, iterate = 3,18
	reltol, abstol = 1e-9,1e-8
	
	# Initial_Conditions = np.array([z=0.,v=0.5,phi=t])
	# nu, g = 0., 9.8067
	g = 9.8067
	def ode_f(x,y): 
		# y = [z,v,phi]
		return np.array([np.tan(y[2]), -(g*np.sin(y[2]) + nu*y[1]**2.)/(y[1]*np.cos(y[2])), 
		-g/y[1]**2.])	
	
	
	# # Here we plot the solution 
	# example = ode(ode_f).set_integrator('dopri5',atol=abstol,rtol=reltol)
	# example.set_initial_value(np.array([ya,va,t0]),a) 
	# X = np.linspace(a,b,801)
	# Y = np.zeros((len(X),dim))
	# Y[0,:] = np.array([ya,va,t0])
	# 
	# for j in range(1,len(X)): 
	# 	Y[j,:] = example.integrate(X[j]) 
	# print '\n|y(b) - beta| = ',np.abs(beta-Y[-1,0]),'\n'
	# plt.plot(X,Y[:,0],'-k')
	# plt.show()
	# if True: return
	
	print '\nj = 1','\nt = ', t0
	for j in range(2,iterate):
		print '\nj = ', j,'\nt = ', t1
		example1 = ode(ode_f).set_integrator('dopri5',atol=abstol,rtol=reltol) 
		example1.set_initial_value(np.array([ya,va,t1]),a) 
		y1 = example1.integrate(b)[0]
		
		if abs(y1-beta)<1e-8: 
			print '\n--Solution y computed successfully--'
			break
		# Update
		example0 = ode(ode_f).set_integrator('dopri5',atol=abstol,rtol=reltol) 
		example0.set_initial_value(np.array([ya,va,t0]),a) 
		y0 = example0.integrate(b)[0]
		
		t2 = t1 - (y1 - beta)*(t1-t0)/(y1- y0)
		t0 = t1
		t1 = t2
		
	# Here we plot the solution 
	example = ode(ode_f).set_integrator('dopri5',atol=abstol,rtol=reltol)
	example.set_initial_value(np.array([ya,va,t1]),a) 
	X = np.linspace(a,b,801)
	Y = np.zeros((len(X),dim))
	Y[0,:] = np.array([ya,va,t1])
	
	for j in range(1,len(X)): 
		Y[j,:] = example.integrate(X[j]) 
	print '\n|y(b) - beta| = ',np.abs(beta-Y[-1,0]),'\n'
	# plt.plot(X,Y[:,0],'-k')
	return t2,X,Y[:,0]


#--------------------------------------------------------------
def Cannon_Shooting(t0,t1): 
	a, b = 0., 6.
	beta =  0.
	
	# t0,t1 = np.pi/6., np.pi/7
	dim, iterate = 3,18
	reltol, abstol = 1e-9,1e-8
	
	# Initial_Conditions = np.array([z=0.,v=0.5,phi=t])
	nu, g = .02, .032
	def ode_f(x,y): 
		# y = [z,v,phi]
		return np.array([np.tan(y[2]), -(g*np.sin(y[2]) + nu*y[1]**2.)/(y[1]*np.cos(y[2])), 
		-g/y[1]**2.])
	
	
	print '\nj = 1'
	print 't = ', t0
	for j in range(2,iterate):
		print '\nj = ', j
		print 't = ', t1
		example1 = ode(ode_f).set_integrator('dopri5',atol=abstol,rtol=reltol) 
		example1.set_initial_value(np.array([0.,0.5,t1]),a) 
		y1 = example1.integrate(b)[0]
		
		if abs(y1-beta)<1e-8: 
			print '\n--Solution y computed successfully--'
			break
		# Update
		example0 = ode(ode_f).set_integrator('dopri5',atol=abstol,rtol=reltol) 
		example0.set_initial_value(np.array([0.,0.5,t0]),a) 
		y0 = example0.integrate(b)[0]
		
		t2 = t1 - (y1 - beta)*(t1-t0)/(y1- y0)
		t0 = t1
		t1 = t2
		
	# Here we plot the solution 
	example = ode(ode_f).set_integrator('dopri5',atol=abstol,rtol=reltol)
	example.set_initial_value(np.array([0.,0.5,t1]),a) 
	X = np.linspace(a,b,801)
	Y = np.zeros((len(X),dim))
	Y[0,:] = np.array([0.,0.5,t1])
	
	for j in range(1,len(X)): 
		Y[j,:] = example.integrate(X[j]) 
	print '\n|y(b) - beta| = ',np.abs(beta-Y[-1,0]),'\n'
	plt.plot(X,Y[:,0],'-k')
	# plt.show()
	return X,Y


# Exercises in Lab

# Example1()
# Example2()
# Exercise1((2**2+2**(-2.)-2.)/(2.2-1))
# Exercise2()
# Exercise3(3.,-2.) 
# Exercise3(3.,1.)

phi1,X,Y = Exercise4(0.,35., 0.,np.pi/3.5,np.pi/3.)
plt.plot(X,Y,'-k')
phi2,X,Y = Exercise4(0,35.,0.,np.pi/6.,np.pi/6.5)
plt.plot(X,Y,'-k')
print '\n'*4,"Angle giving the furthest distance: "
print 'pi/4 =   ', np.pi/4.
print "\nSolutions to BVP:"
print "phi(0) = ", phi1
print "         ", phi2
plt.show()




# X,Y = Cannon_Shooting(np.pi/4., np.pi/4.5)
# X1,Y1 = Cannon_Shooting(np.pi/3.5, np.pi/3.0)
# plt.plot(X,Y[:,0],'-k')
# plt.plot(X1,Y1[:,0],'-k')
# plt.show()