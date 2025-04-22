import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse
#from scipy.optimize import curve_fit
from scipy import optimize

def chebychev_poly(x,coef):
    sigma = 0
    nmax = len(coef)
    #for i in range(n):
    #    sigma +=
    t=[]
    t.append(1)
    t.append(x)
    for i in range(nmax-2):
        t.append(2*x*t[i+1]-t[i])
    
    for i in range(nmax):
        sigma += coef[i]*t[i]
    '''sigma += a*t[0]
    sigma += b*t[1]
    sigma += c*t[2]
    sigma += d*t[3]
    sigma += e*t[4]
    return sigma
    
    sigma += a
    sigma += b*x
    sigma += c*(2*x**2-1)
    sigma += d*(4*x**3-3*x)
    sigma += e*(8*x**4-8*x**2-1)'''
    return sigma 



class Inverse_Finder():
    coef = np.zeros(1)
    T = 0
    def __init__(self,coef,T):
        self.coef = coef
        self.T = T
        #print(np.shape(T))



    def chebychev_poly(self,x,coef):
        sigma = 0
        nmax = len(coef)
        #for i in range(n):
        #    sigma +=
        t=[]
        t.append(1)
        t.append(x)
        for i in range(nmax-2):
            t.append(2*x*t[i+1]-t[i])
        
        for i in range(len(coef)):
            sigma+=coef[i]*t[i]
        return sigma
    
    def rootfunc(self,x):
        coef = self.coef
        T = self.T
        return self.chebychev_poly(x,coef) - T

    def findinv(self):
        x = optimize.broyden1(self.rootfunc, np.zeros(np.shape(self.T)),iter=50)
        return x





# Parse arguments
parser = argparse.ArgumentParser(description='')
parser.add_argument('-dc','--data-calibrated',type=str,required=True,dest='fn_cal',
                    help='Data from the calibrated thermometer')
parser.add_argument('-uc','--data-uncalibrated',type=str,required=True,dest='fn_ucal',
                    help='Data from the uncalibrated thermometer')
parser.add_argument('-rc','--reference-calcurve',type=str,required=True,dest='fn_ccurv',
                    help='Calibration curve for calibrated thermometer')
parser.add_argument('-of','--new-filename',type=str,required=True,dest='fn_ncurv',
                    help='Filename for new  curve')
parser.add_argument('-pf','--plot-filename',type=str,required=True,dest='fn_plot',
                    help='Filename for calibration curve analysis plot')
parser.add_argument('-p','--polynomial-order',type=int,required=False,dest='polyN',default=2,
                    help='Order for the polynomial fit between thermometer resistances')
parser.add_argument('-sm','--sensor-model',type=str,required=False,dest='model',default='LS_ROX',
                    help='Sensor model for the output file header. Typically LS-Cernox or LS-ROX')
parser.add_argument('-sn','--serial-number',type=str,required=False,dest='sn',default='000.000',
                    help='Serial number of sensor')
parser.add_argument('-minT',type=float,required=False,dest='minT',default=0.,
                    help='Minimum temperature to fit down to.')
parser.add_argument('-maxT',type=float,required=False,dest='maxT',default=300.,
                    help='Maximum temperature to fit up to.')
parser.add_argument('-minc',type=float,required=False,dest='minctime',default=0.,
                    help='Minimum ctime to use.')
parser.add_argument('-maxc',type=float,required=False,dest='maxctime',default=9e9,
                    help='Maximum ctime to use.')
args = parser.parse_args()


# Load the calibrated thermometer data
df_cal =  pd.read_csv(args.fn_cal, names=['time','ch','res','temp'],skiprows=1,comment='#')
# Load the uncalibrated thermometer data
df_ucal = pd.read_csv(args.fn_ucal,names=['time','ch','res','temp'],skiprows=1,comment='#')
# Clip the data using the ctime bounds
df_cal  = df_cal[ (df_cal.time  > args.minctime) & (df_cal.time  < args.maxctime)]
df_ucal = df_ucal[(df_ucal.time > args.minctime) & (df_ucal.time < args.maxctime)]
# Make sure both datasets have the same length (crude)
N = min(len(df_cal),len(df_ucal))
df_cal  = df_cal.head(N).reset_index(drop=True)
df_ucal = df_ucal.head(N).reset_index(drop=True)

# Remove data points where df_cal is zero
df_ucal = df_ucal[df_cal.res != 0]
df_cal  = df_cal[ df_cal.res != 0]


# Load the calibration curve of the calibrated thermometer
df_ccurv = pd.read_csv(args.fn_ccurv,names=['r','t'],skiprows=9,sep='   |\t',engine='python')
df_ccurv['R'] = 10**df_ccurv.r

# Make the header for the output calibration file
header = '\n'.join(['Sensor Model:   %s'%args.model,
                    'Serial Number:  %s'%args.sn,
                    'Data Format:    4      (Log Ohms/Kelvin)',
                    'SetPoint Limit: 100.0      (Kelvin)',
                    'Temperature coefficient:  1 (Negative)',
                    'Number of Breakpoints:   %d'%len(df_ccurv),
                    '',
                    'No.   Units      Temperature (K)',
                    '',
                    ''])


# Find where the calibrated thermometer was between minT and max T
sel = (df_cal.temp<args.maxT) & (df_cal.temp>args.minT)
sel2 = (df_cal.temp<args.maxT) & (df_cal.temp>10.0)


Rmax = np.max(df_ucal.res[sel])
Rmin = np.min(df_ucal.res[sel])
Zmax = np.log10(Rmax)
Zmin = np.log10(Rmin)


Rmax2 = np.max(df_ucal.res[sel2])
Rmin2 = np.min(df_ucal.res[sel2])
Zmax2 = np.log10(Rmax2)
Zmin2 = np.log10(Rmin2)
#Zmax = Rmax
#Zmin = Rmin


#print(Zmax)
#print(Zmin)


x_ucal = (2*np.log10(df_ucal.res[sel])-Zmin-Zmax)/(Zmax-Zmin)

x_ucal2 = (2*np.log10(df_ucal.res[sel2])-Zmin2-Zmax2)/(Zmax2-Zmin2)

#x_ucal = (2*(df_ucal.res[sel])-Zmin-Zmax)/(Zmax-Zmin)

#print(np.max(x_ucal))
#print(np.min(x_ucal))

#fit = np.polynomial.polynomial.Polynomial.fit(np.log10(df_ucal.res[sel]),df_cal.temp[sel],10)
#fitxx, fityy = fit.linspace()
#fitcoef = np.polyfit(np.log10(df_ucal.res[sel]),df_cal.temp[sel],10)

# Fit a polynomial to the calibrated resistance vs the uncalibrated resistance

fit = np.polyfit(df_cal.res[sel],df_ucal.res[sel],args.polyN)

fit2 = np.polyfit(df_cal.res[sel2],df_ucal.res[sel2],args.polyN)


#popt, pcov = optimize.curve_fit(chebychev_poly, x_ucal, df_cal.temp[sel])
#fitline = chebychev_poly(x_ucal, popt[0],popt[1],popt[2],popt[3],popt[4])

#fitdeg = 4
fitobj = np.polynomial.chebyshev.Chebyshev.fit(x_ucal, df_cal.temp[sel],10)

coef = np.polynomial.chebyshev.chebfit(x_ucal, df_cal.temp[sel],10)


fitobj2 = np.polynomial.chebyshev.Chebyshev.fit(x_ucal2, df_cal.temp[sel2],10)

coef2 = np.polynomial.chebyshev.chebfit(x_ucal2, df_cal.temp[sel2],10)
#fitline = np.polynomial.chebyshev.chebval(x_ucal,coef)
#fitline = chebychev_poly(x_ucal, coef)

#polycoef = np.polynomial.cheb2poly(coef)


xx, yy = fitobj.linspace()

temp=np.polynomial.chebyshev.chebval(x_ucal,coef)


# xx3, yy3 = difference.linspace()

xx2, yy2 = fitobj2.linspace()

#print(np.shape(x_ucal))
#print(np.shape(df_cal.temp[sel]))
#print(np.shape(fitline))
#print(fitline)

#print(popt[0])
#print(popt[1])
#print(popt[2])
#print(popt[3])
#print(popt[4])


#popt=np.zeros(4)
#for i in range(fitdeg):
#    popt[i] = fitline.convert().coef

# Evaluate fit using resistances in master calibration curve to get resistances of new calibration curve
#newcalR = np.polyval(fit,df_ccurv.R)
#newcalT = df_ccurv.t.values

#newcalT = df_ccurv.t.values
#print(newcalT)
#inverser = Inverse_Finder(coef,newcalT)

#x_ccurv = (2*np.log10(df_ccurv.R)-np.log10(Rmin)-np.log10(Rmax))/(np.log10(Rmax)-np.log10(Rmin))

#x_ccurv = inverser.findinv()
#x_ccurv = np.ones(len(newcalT))

#newcalZ = 0.5*(Zmax+Zmin+(Zmax-Zmin)*x_ccurv)
#newcalR = np.power(10,newcalZ) 
#newcalR = newcalZ

#fitxx = np.power(10,fitxx)

xx = 0.5*(Zmax+Zmin+(Zmax-Zmin)*xx)
xx = np.power(10,xx)


xx2 = 0.5*(Zmax2+Zmin2+(Zmax2-Zmin2)*xx2)
xx2 = np.power(10,xx2)
'''
newcalRpower = np.linspace(1,12,num=1000)
newcalR = np.power(10,newcalRpower)
newcalZ = np.log10(newcalR)
newcalX = (2*newcalZ-Zmax-Zmin)/(Zmax-Zmin)
newcalT = np.polynomial.chebyshev.chebval(newcalX,coef)

Tmax = np.max(df_ccurv.t.values)
Tmin = np.min(df_ccurv.t.values)
sel2 = (newcalT<Tmax) & (newcalT>Tmin)
sel4 = (newcalR<np.max(xx)) & (newcalR>np.min(xx))
print(np.shape(newcalR[sel4]))
'''
Rpowermax = np.log10(np.max(xx))
Rpowermin = np.log10(np.min(xx))
newcalRpower = np.linspace(Rpowermin,Rpowermax,num=180)
newcalR = np.power(10,newcalRpower)
newcalZ = np.log10(newcalR)
newcalX = (2*newcalZ-Zmax-Zmin)/(Zmax-Zmin)
newcalT = np.polynomial.chebyshev.chebval(newcalX,coef)

Tmax = np.max(df_ccurv.t.values)
Tmin = np.min(df_ccurv.t.values)


Rpowermax2 = np.log10(np.max(xx2))
Rpowermin2 = np.log10(np.min(xx2))
newcalRpower2 = np.linspace(Rpowermin2,Rpowermax2,num=180)
newcalR2 = np.power(10,newcalRpower2)
newcalZ2 = np.log10(newcalR2)
newcalX2 = (2*newcalZ2-Zmax2-Zmin2)/(Zmax2-Zmin2)
newcalT2 = np.polynomial.chebyshev.chebval(newcalX2,coef2)

Tmax2 = np.max(df_ccurv.t.values)
Tmin2 = np.min(df_ccurv.t.values)
# sel2 = (newcalT<Tmax) & (newcalT>Tmin)
# sel4 = (newcalR<np.max(xx)) & (newcalR>np.min(xx))








# fitconvert = fit.convert(domain=[1,12])
# newcalX2, newcalT2 = fitconvert.linspace()
'''newcalRpower2 = np.linspace(1,12,num=1000)
newcalR2 = np.power(10,newcalRpower2)
newcalZ2 = np.log10(newcalR2)
newcalX2 = (2*newcalZ2-Zmax-Zmin)/(Zmax-Zmin)
newcalT2 = np.polyval(fitcoef,newcalX2)
'''
#newcalR2 = np.power(10,newcalX2)
# sel3 = (newcalT2<Tmax) & (newcalT2>Tmin)
#print(np.shape(newcalT2))
#print(np.shape(newcalR2))



#r_ucal = 0.5*(Zmax+Zmin+(Zmax-Zmin)*x_ucal)
#r_ucal = np.power(10,r_ucal)

# Reorganize for saving to file
df_ncurv = pd.DataFrame(np.vstack([np.log10(newcalR),newcalT]).T,columns=['calR','calT'])
df_ncurv.index += 1
with open(args.fn_ncurv, 'w') as f:
         f.write(header)
         for i,(r,t) in enumerate(df_ncurv.values.tolist()):
                  line  = '{:d}'.format(i+1).rjust(3)
                  line += '{:.5f}'.format(r).rjust(9)
                  line += '{:.3f}'.format(t).rjust(14)
                  f.write(line+'\n')
                  #f.write('{:d}  {:.6f}       {:.3f}\n'.format(i+1,r,t))
                    

                    
#df_ncurv.to_csv(args.fn_ncurv,header=False,sep='\t',float_format='%.4f',mode='a')
#df_ncurv.to_csv(args.fn_ncurv,header=False,sep=' ',float_format='%.4f',mode='a')



# The rest is plotting

# Get the Lakeshore channel numbers of the thermometers
cal_chN = df_cal.ch.values[0]
ucal_chN = df_ucal.ch.values[0]

# fig,((ax1,ax2),(ax3,ax4),(ax5,ax6)) = plt.subplots(3,2,figsize=(12,10))
fig,((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2,figsize=(12,10))

# res vs time
ax1.plot((df_cal.time-df_cal.time.values[0])/60.,df_cal.res,ls='-',label='Cal Ch%d'%cal_chN)
ax1.plot((df_ucal.time-df_ucal.time.values[0])/60.,df_ucal.res,ls='-',label='UCal Ch%d'%ucal_chN)
ax1.legend()
# res vs temp
# ax2.semilogx(df_cal.temp,df_cal.res,marker='.',ls='',label='Cal Ch%d'%cal_chN)
# ax2.semilogx(df_cal.temp,df_ucal.res,marker='.',ls='',label='UCal Ch%d'%ucal_chN)

ax2.loglog(df_cal.temp,df_ucal.res,marker='.',ls='',label='UCal Ch%d'%ucal_chN)

#ax2.semilogx(fityy,fitxx,label='Polynomial Fit (order 10)')
ax2.loglog(yy,xx,label='Chebychev Fit (order 10)')
# ax2.loglog(yy2,xx2,label='Chebychev Fit Small (order 10)')


# ax5.scatter(temp,temp-df_cal.temp[sel], marker='.')
# ax5.set_xlabel("Cheby Fit Temp")
# ax5.set_ylabel("Cheby Fit - Ucal Temp")
# # ax5.set_yscale('log')
# ax5.set_xscale('log')
# ax5.set_ylim([-3,2])
# ax2.semilogx(newcalT3,newcalR2,label='Chebychev Fit Difference (order 10)')
# ax2.set_xlim([10, 13])
ax2.set_xlim([1e0, 250])
# ax2.set_ylim([4e4, 0.075e6])
# ax2.set_ylim([1e0, 0.075e6])




# ax5.semilogx()



#ax2.semilogx(fitline,r_ucal,label='test2')

#colors = df_ucal.time-df_ucal.time.values[0]; colors = colors/colors.values[-1]
#ax2.scatter(df_cal.temp,df_cal.res,marker='.',label='Cal Ch%d'%cal_chN)
#ax2.scatter(df_cal.temp,df_ucal.res,c=colors,marker='.',label='UCal Ch%d'%ucal_chN,cmap='viridis')
ax2.axvspan(max([args.minT,df_cal.temp.min()]),min([args.maxT,df_cal.temp.max()]),alpha=0.1,color='red',label='Calibration\nRegion')


ax2.set_xscale('log')
ax2.legend()

# res vs res
ax3.loglog(df_cal[sel].res,df_ucal[sel].res,marker='.',ls='',label='Calibrated vs Uncalibrated Data')
# ax3.loglog(df_cal[sel].res.sort_values(),np.polyval(fit,df_cal[sel].res.sort_values()),label='Polynomial Fit (order %d)'%args.polyN)
ax3.legend()


# cal_T vs res
ax4.loglog(df_ccurv.t,df_ccurv.R,marker='.',ls='-',label='BF Cal Curve')
# ax4.loglog(newcalT[sel2],newcalR[sel2],marker='.',ls='-',label='NewcalR Cheby')
ax4.loglog(newcalT,newcalR,marker='.',ls='-',label='NewcalR Cheby')
# ax4.loglog(newcalT2[sel3],newcalR2[sel3],marker='.',ls='-',label='NewcalR Poly')
ax4.axvspan(max([args.minT,df_cal.temp.min()]),min([args.maxT,df_cal.temp.max()]),alpha=0.1,color='red',label='Calibration\nRegion')
ax4.legend()

# plot formatting
#fig.suptitle(fn)
ax1.grid()
ax2.grid()
ax3.grid()
ax4.grid(True,which='both',axis='y');ax4.grid(True,which='major',axis='x')

ax1.set_xlabel('Time [Mins]')
ax1.set_ylabel('Resistance [Ohms]')
ax2.set_xlabel('Calibrated Ch%d Temperature [K]'%cal_chN)
ax2.set_ylabel('Resistance [Ohms]')
ax3.set_xlabel('Calibrated Ch%d Resistance [Ohms]'%cal_chN)
ax3.set_ylabel('Uncalibrated Ch%d Resistance [Ohms]'%ucal_chN)
ax4.set_xlabel('Calibrated Temperature [K]')
ax4.set_ylabel('Resistance [Ohms]')

#fig.show()
fig.suptitle(args.model+' '+args.sn+'\n'+args.fn_ucal)
fig.savefig(args.fn_plot,bbox_inches='tight',dpi=200)

