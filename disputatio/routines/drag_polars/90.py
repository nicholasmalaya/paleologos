import numpy as np
import matplotlib.pyplot as plt

def poly_print(c,name):
    #
    # prints coefficients for lift or drag functions
    #
    p=0
    print ''
    for item in c:
        # last step
        if(p == len(c)-1):
            print '        '+str(item)+'*x^'+str(p)+"'",
        # first step
        elif(p==0):
            print name +" = '"+str(item)+'*x^'+str(p)+" + "
            p=p+1
        # middle steps
        else:
            print '        '+str(item)+'*x^'+str(p)+" + "
            p=p+1
    print ''
    return 0

def reader(fl):
    #
    # reads a file and returns function values
    # 
    angle = []
    cd    = []
    
    # open
    fo = open(fl, "r")
    
    #
    # iterate
    #
    for line in fo:
        two_var = line.split()
        angle.append(float(two_var[0].split(',')[0]))
        cd.append(float(two_var[1]))
        
    # close
    fo.close()
    return angle, cd


# -----------------------
# main function
# -----------------------
#
# http://docs.scipy.org/doc/numpy/reference/routines.polynomials.poly1d.html
#
# grab original data
#
f1 = "cd_90.dat"
f2 = "cl_90.dat"
anglecd, cd = reader(f1)
anglecl, cl = reader(f2)

#
# plot interpolated function
#
# theta := ((t+pi/2)%pi)-pi/2
# lift = ' if ( abs ( theta )< pi / 24 , theta * 9 , sin ( 2 * theta ) ) '
# drag = if(abs(theta)<pi/24,0.005+theta*theta*81/25, 1-0.8cos(2*theta))
# 
#rad = np.linspace(0.0, 360.0)
#

anglecd = -1 + 2*np.array(anglecd)/360.0
anglecl = -1 + 2*np.array(anglecl)/360.0

#
# interpolate!
# interp1d(x, y, kind='cubic')
#
#from scipy.interpolate import interp1d
from numpy.polynomial import polynomial as P

inter_cd,stat_cd = P.polyfit(anglecd, cd, 16,full=True)
inter_cl,stat_cl = P.polyfit(anglecl, cl, 16,full=True)

rad    = np.linspace(-0.99, 0.99)
t      = (rad+np.pi)%np.pi - np.pi/2.0
#anglei = (rad+1)*180.
anglei = rad

#cdi = np.cos(2 * np.pi * rad) * np.exp(-rad)
#cli = np.cos(2 * np.pi * rad)

#cli = np.where(abs(t) > np.pi/24., t, np.sin(2*t))
#cdi = np.where(abs(t) > np.pi/24., t*t*81/25., 1-0.8*np.cos(2*t))

poly_print(inter_cl,'lift')
poly_print(inter_cd,'drag')

#
# plot!
#
plt.subplot(2, 1, 1)
plt.plot(anglecd, cd, 'ko-',label='Duane Data')
plt.plot(anglei, P.polyval(anglei,inter_cd), color='blue',label='Interpolant')
plt.title(r'Coefficient of Lift/Drag as function of $\alpha$')
plt.xlabel(r'$\alpha$')
plt.ylabel(r'$C_d$')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(anglecl, cl, 'ko-',label='Duane Data')
plt.plot(anglei, P.polyval(anglei,inter_cl), color='blue',label='Interpolant')
plt.ylabel(r'$C_l$')
plt.xlabel(r'$\alpha$')
plt.legend()
plt.savefig("90.png")


#
# nick
# 3/30/15
#