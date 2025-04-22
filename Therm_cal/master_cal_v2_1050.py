from glob import glob
import os

datadir = './csvOutput/'
outdir = './new_curves/'
SSBDRcurves = {
               #  'Ch1': './therm_cal_curves/Pt1557.340',
                # 'Ch2': './therm_cal_curves/prime-cam_DR_curves/X157535.340'}
                # 'Ch5': './therm_cal_curves/x134059.340',
                'Ch6': './therm_cal_curves/prime-cam_DR_curves/R30197.340'}

'''

'''

masterdict = {'X181444': {'Ch': '7', 'SensorModel': 'CX-1050-CD', 'minT': 1.2, 'CalCh': '6', 'minc': 0, 'maxc': 9e9,
                          'Cooldown': 'SSBDR_cal_data_2024_10_15_08_00_00', 'polyN': 7},
             'X181344': {'Ch': '8', 'SensorModel': 'CX-1050-CD', 'minT': 1.2, 'CalCh': '6', 'minc': 0, 'maxc': 9e9,
                          'Cooldown': 'SSBDR_cal_data_2024_10_15_08_00_00', 'polyN': 7}}


Nsn = len(masterdict)
for isn,sn in enumerate(masterdict.keys()):
    model  = masterdict[sn]['SensorModel']
    #if 'CX-1050-CU-HT' not in model: continue;
    print(model,sn,'%d of %d'%(isn+1,Nsn))
    ucalfn = glob('%s/%s_ch%s.csv'%(datadir,masterdict[sn]['Cooldown'],masterdict[sn]['Ch']))[0]
    calfn  = glob('%s/%s_ch%s.csv'%(datadir,masterdict[sn]['Cooldown'],masterdict[sn]['CalCh']))[0]
    reffn  = SSBDRcurves['Ch%s'%masterdict[sn]['CalCh']]
    outfn  = outdir+model+'_'+sn+'_v2'+'.340' #'.curve'
    plotfn = outdir+model+'_'+sn+'_v2'+'.pdf'
    #polyN  = '4'
    polyN   = masterdict[sn]['polyN']
    minT   = masterdict[sn]['minT']
    minc   = masterdict[sn]['minc']
    maxc   = masterdict[sn]['maxc']


    args = (ucalfn,calfn,reffn,outfn,plotfn,polyN,model,sn,minT,minc,maxc)
    cmd = 'python3 therm_cal_v2.py -uc  %s -dc %s -rc %s -of %s -pf %s -p %s -sm %s -sn %s -minT %f -minc %d -maxc %d'%args
    print(cmd)
    os.system(cmd)
    print()
