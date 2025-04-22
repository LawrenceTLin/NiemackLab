from glob import glob
import os

datadir = './csvOutput/'
outdir = './new_curves/'
SSBDRcurves = {
               #  'Ch1': './therm_cal_curves/Pt1557.340',
                'Ch2': './therm_cal_curves/prime-cam_DR_curves/X157535.340'}
                # 'Ch5': './therm_cal_curves/x134059.340',
               #'Ch6': './therm_cal_curves/prime-cam_DR_curves/R30197.340'}

'''
masterdict = {'U09980': {'Ch': '7', 'SensorModel': 'RX-102A-CD', 'minT': 0.05, 'CalCh': '6', 'minc': 0, 'maxc': 9e9,
                         'Cooldown': 'SSBDR_cal_data_2023_05_10_16_00_00', 'polyN': 4},
             'U09984': {'Ch': '8', 'SensorModel': 'RX-102A-CD', 'minT': 0.05, 'CalCh': '6', 'minc': 0, 'maxc': 9e9,
                         'Cooldown': 'SSBDR_cal_data_2023_05_10_16_00_00', 'polyN': 4}}
masterdict =
{'X186991': {'Ch': '3', 'SensorModel': 'CX-1080-CD', 'minT': 4.0, 'CalCh': '2', 'minc': 0, 'maxc': 9e9,
                          'Cooldown': 'SSBDR_cal_data_2023_09_27_11_00_00', 'polyN': 7},
              'X186990': {'Ch': '4', 'SensorModel': 'CX-1080-CD', 'minT': 4.0, 'CalCh': '2', 'minc': 0, 'maxc': 9e9,
                          'Cooldown': 'SSBDR_cal_data_2023_09_27_11_00_00', 'polyN': 7}},
{'X186995': {'Ch': '3', 'SensorModel': 'CX-1080-CD', 'minT': 4.0, 'CalCh': '2', 'minc': 0, 'maxc': 9e9,
                          'Cooldown': 'SSBDR_cal_data_2023_09_09_11_00_00', 'polyN': 7},
              'X186996': {'Ch': '4', 'SensorModel': 'CX-1080-CD', 'minT': 10.0, 'CalCh': '2', 'minc': 0, 'maxc': 9e9,
                          'Cooldown': 'SSBDR_cal_data_2023_09_09_11_00_00', 'polyN': 7}}
                          {'X186994': {'Ch': '3', 'SensorModel': 'CX-1080-CD', 'minT': 4.0, 'CalCh': '2', 'minc': 0, 'maxc': 9e9,
                          'Cooldown': 'SSBDR_cal_data_2023_10_06_12_00_00', 'polyN': 7},
              'X186997': {'Ch': '4', 'SensorModel': 'CX-1080-CD', 'minT': 10.0, 'CalCh': '2', 'minc': 0, 'maxc': 9e9,
                          'Cooldown': 'SSBDR_cal_data_2023_10_06_12_00_00', 'polyN': 7}}
                          'X186994': {'Ch': '3', 'SensorModel': 'CX-1080-CD', 'minT': 5.0, 'CalCh': '2', 'minc': 0, 'maxc': 9e9,
                          'Cooldown': 'SSBDR_cal_data_2023_05_09_11_00_00', 'polyN': 7},
              'X186997': {'Ch': '4', 'SensorModel': 'CX-1080-CD', 'minT': 5.0, 'CalCh': '2', 'minc': 0, 'maxc': 9e9,
                          'Cooldown': 'SSBDR_cal_data_2023_05_09_11_00_00', 'polyN': 7}
'X186993': {'Ch': '4', 'SensorModel': 'CX-1080-CD', 'minT': 10.0, 'CalCh': '2', 'minc': 0, 'maxc': 9e9,
                          'Cooldown': 'SSBDR_cal_data_2023_11_30_15_00_00', 'polyN': 7}
                          
                          {'X186989': {'Ch': '3', 'SensorModel': 'CX-1080-CD', 'minT': 4.0, 'CalCh': '2', 'minc': 0, 'maxc': 9e9,
                          'Cooldown': 'SSBDR_cal_data_2023_12_05_19_00_00', 'polyN': 7}}
                          {'X187000': {'Ch': '3', 'SensorModel': 'CX-1080-CD', 'minT': 4.0, 'CalCh': '2', 'minc': 0, 'maxc': 9e9,
                          'Cooldown': 'SSBDR_cal_data_2023_12_12_22_00_00', 'polyN': 7},
              'X186999': {'Ch': '4', 'SensorModel': 'CX-1080-CD', 'minT': 4.0, 'CalCh': '2', 'minc': 0, 'maxc': 9e9,
                          'Cooldown': 'SSBDR_cal_data_2023_12_12_22_00_00', 'polyN': 7}}
                          {'X187001': {'Ch': '3', 'SensorModel': 'CX-1080-CD', 'minT': 4.0, 'CalCh': '2', 'minc': 0, 'maxc': 9e9,
                          'Cooldown': 'SSBDR_cal_data_2024_01_12_19_00_00', 'polyN': 7},
              'X186998': {'Ch': '4', 'SensorModel': 'CX-1080-CD', 'minT': 4.0, 'CalCh': '2', 'minc': 0, 'maxc': 9e9,
                          'Cooldown': 'SSBDR_cal_data_2024_01_12_19_00_00', 'polyN': 7}}
                          
                          {'X187001': {'Ch': '3', 'SensorModel': 'CX-1080-CD', 'minT': 4.0, 'CalCh': '2', 'minc': 0, 'maxc': 9e9,
                          'Cooldown': 'SSBDR_cal_data_2024_01_24_00_00_00', 'polyN': 7}
                          
            X212388': {'Ch': '3', 'SensorModel': 'CX-1050-CU', 'minT': 4.0, 'CalCh': '2', 'minc': 0, 'maxc': 9e9,
                          'Cooldown': 'SSBDR_cal_data_2024_05_01_12_00_00', 'polyN': 7}
                          
            'X186989': {'Ch': '3', 'SensorModel': 'CX-1080-CD', 'minT': 3.2, 'CalCh': '2', 'minc': 0, 'maxc': 9e9,
                          'Cooldown': 'SSBDR_cal_data_2024_09_05_12_00_00', 'polyN': 7}
'''

masterdict = {'X187002': {'Ch': '3', 'SensorModel': 'CX-1080-CD', 'minT': 3.2, 'CalCh': '2', 'minc': 0, 'maxc': 9e9,
                          'Cooldown': 'SSBDR_cal_data_2024_10_06_12_00_00', 'polyN': 7}}

# {'X186989': {'Ch': '3', 'SensorModel': 'CX-1080-CD', 'minT': 4.0, 'CalCh': '2', 'minc': 0, 'maxc': 9e9,
#                           'Cooldown': 'SSBDR_cal_data_2023_10_25_10_00_00', 'polyN': 7},
#               'X186993': {'Ch': '4', 'SensorModel': 'CX-1080-CD', 'minT': 4.0, 'CalCh': '2', 'minc': 0, 'maxc': 9e9,
#                           'Cooldown': 'SSBDR_cal_data_2023_10_25_10_00_00', 'polyN': 7}}

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
