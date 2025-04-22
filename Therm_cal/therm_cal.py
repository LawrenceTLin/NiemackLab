import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse

# Parse arguments
parser = argparse.ArgumentParser(description='')
parser.add_argument('-dc','--data-calibrated',type=str,required=True,dest='fn_cal',
                    help='Data from the calibrated thermometer')
parser.add_argument('-uc','--data-uncalibrated',type=str,required=True,dest='fn_ucal',
                    help='Data from the uncalibrated thermometer')
parser.add_argument('-rc','--reference-calcurve',type=str,required=True,dest='fn_ccurv',
                    help='Calibration curve for calibrated thermometer')
parser.add_argument('-of','--new-filename',type=str,required=True,dest='fn_ncurv',
                    help='Filename for new calibration curve')
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
# Fit a polynomial to the calibrated resistance vs the uncalibrated resistance
fit = np.polyfit(df_cal.res[sel],df_ucal.res[sel],args.polyN)
# Evaluate fit using resistances in master calibration curve to get resistances of new calibration curve
newcalR = np.polyval(fit,df_ccurv.R)
newcalT = df_ccurv.t.values
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

fig,((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2,figsize=(12,10))
# res vs time
ax1.plot((df_cal.time-df_cal.time.values[0])/60.,df_cal.res,ls='-',label='Cal Ch%d'%cal_chN)
ax1.plot((df_ucal.time-df_ucal.time.values[0])/60.,df_ucal.res,ls='-',label='UCal Ch%d'%ucal_chN)
ax1.legend()
# res vs temp
ax2.semilogx(df_cal.temp,df_cal.res,marker='.',ls='',label='Cal Ch%d'%cal_chN)
ax2.semilogx(df_cal.temp,df_ucal.res,marker='.',ls='',label='UCal Ch%d'%ucal_chN)
#colors = df_ucal.time-df_ucal.time.values[0]; colors = colors/colors.values[-1]
#ax2.scatter(df_cal.temp,df_cal.res,marker='.',label='Cal Ch%d'%cal_chN)
#ax2.scatter(df_cal.temp,df_ucal.res,c=colors,marker='.',label='UCal Ch%d'%ucal_chN,cmap='viridis')
ax2.axvspan(max([args.minT,df_cal.temp.min()]),min([args.maxT,df_cal.temp.max()]),alpha=0.1,color='red',label='Calibration\nRegion')
ax2.set_xscale('log')
ax2.legend()
# res vs res
ax3.loglog(df_cal[sel].res,df_ucal[sel].res,marker='.',ls='',label='Data')
ax3.loglog(df_cal[sel].res.sort_values(),np.polyval(fit,df_cal[sel].res.sort_values()),label='Polynomial Fit (order %d)'%args.polyN)
ax3.legend()
# cal_T vs res
ax4.loglog(df_ccurv.t,df_ccurv.R,marker='.',ls='-',label='BF Cal Curve')
ax4.loglog(df_ccurv.t,newcalR,marker='.',ls='-',label='NewcalR')
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
