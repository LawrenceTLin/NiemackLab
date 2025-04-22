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
masterdict = {'U09980': {'Ch': '7', 'SensorModel': 'RX-102A-CD', 'minT': 0.05, 'CalCh': '6', 'minc': 0, 'maxc': 9e9,
                         'Cooldown': 'SSBDR_cal_data_2023_05_10_16_00_00', 'polyN': 4},
             'U09984': {'Ch': '8', 'SensorModel': 'RX-102A-CD', 'minT': 0.05, 'CalCh': '6', 'minc': 0, 'maxc': 9e9,
                         'Cooldown': 'SSBDR_cal_data_2023_05_10_16_00_00', 'polyN': 4}}
            {'U09793': {'Ch': '7', 'SensorModel': 'RX-102A-CD', 'minT': 0.05, 'CalCh': '6', 'minc': 0, 'maxc': 9e9,
                         'Cooldown': 'SSBDR_cal_data_2023_10_07_08_00_00', 'polyN': 4},
             'U10091': {'Ch': '8', 'SensorModel': 'RX-102A-CD', 'minT': 0.05, 'CalCh': '6', 'minc': 0, 'maxc': 9e9,
                         'Cooldown': 'SSBDR_cal_data_2023_10_07_08_00_00', 'polyN': 4}}
'U10084': {'Ch': '7', 'SensorModel': 'RX-102A-CD', 'minT': 0.05, 'CalCh': '6', 'minc': 0, 'maxc': 9e9,
                         'Cooldown': 'SSBDR_cal_data_2023_11_17_10_00_00', 'polyN': 4},
             'U09979': {'Ch': '8', 'SensorModel': 'RX-102A-CD', 'minT': 0.05, 'CalCh': '6', 'minc': 0, 'maxc': 9e9,
                         'Cooldown': 'SSBDR_cal_data_2023_11_17_10_00_00', 'polyN': 4}
                         {'U10077': {'Ch': '7', 'SensorModel': 'RX-102A-CD', 'minT': 0.05, 'CalCh': '6', 'minc': 0, 'maxc': 9e9,
                         'Cooldown': 'SSBDR_cal_data_2023_12_13_09_00_00', 'polyN': 4},
             'U10088': {'Ch': '8', 'SensorModel': 'RX-102A-CD', 'minT': 0.05, 'CalCh': '6', 'minc': 0, 'maxc': 9e9,
                         'Cooldown': 'SSBDR_cal_data_2023_12_13_09_00_00', 'polyN': 4}}
'''

masterdict = {'U10080': {'Ch': '7', 'SensorModel': 'RX-102A-CD', 'minT': 0.05, 'CalCh': '6', 'minc': 0, 'maxc': 9e9,
                         'Cooldown': 'SSBDR_cal_data_2024_01_13_09_30_00', 'polyN': 4},
             'U10078': {'Ch': '8', 'SensorModel': 'RX-102A-CD', 'minT': 0.05, 'CalCh': '6', 'minc': 0, 'maxc': 9e9,
                         'Cooldown': 'SSBDR_cal_data_2024_01_13_09_30_00', 'polyN': 4}}
Nsn = len(masterdict)
for isn,sn in enumerate(masterdict.keys()):
    model  = masterdict[sn]['SensorModel']
    # if 'CX-1050-CU-HT' not in model: continue;
    print(model,sn,'%d of %d'%(isn+1,Nsn))
    ucalfn = glob('%s/%s_ch%s.csv'%(datadir,masterdict[sn]['Cooldown'],masterdict[sn]['Ch']))[0]
    calfn  = glob('%s/%s_ch%s.csv'%(datadir,masterdict[sn]['Cooldown'],masterdict[sn]['CalCh']))[0]
    reffn  = SSBDRcurves['Ch%s'%masterdict[sn]['CalCh']]
    outfn  = outdir+model+'_'+sn+'.340' #'.curve'
    plotfn = outdir+model+'_'+sn+'.pdf'
    #polyN  = '4'
    polyN   = masterdict[sn]['polyN']
    minT   = masterdict[sn]['minT']
    minc   = masterdict[sn]['minc']
    maxc   = masterdict[sn]['maxc']
    
    args = (ucalfn,calfn,reffn,outfn,plotfn,polyN,model,sn,minT,minc,maxc)
################################################################################
#CHANGE TO master_cal_v2.py IF FITTING CD
    
    cmd = 'python3 therm_cal.py -uc  %s -dc %s -rc %s -of %s -pf %s -p %s -sm %s -sn %s -minT %f -minc %d -maxc %d'%args
    print(cmd)
    os.system(cmd)
    print()
